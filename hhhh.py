r""" monolith.summarizer.service module """

# importing standard modules ==================================================
from typing import List
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# importing custom modules ====================================================
from monolith.summarizer.data_loader import PatentLoader
from monolith.summarizer.exceptions import DataExtractionError
from monolith.summarizer.openai_api import Openai_API
from  monolith.summarizer.processing import Processing_steps
from monolith.patent.db_service import get_db_text_document_by_ucids
from _patentdb.engine import get_engine
from monolith.summarizer.schema import PatentSummary
import requests
# importing third-party modules ===============================================
from sqlalchemy.orm import Session
from requests.exceptions import RequestException
# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)

def downloaded_patents(ucids: List[str]) -> dict:
    """ Downloads patent data from the database and returns a dictionary of patents. """
    patent_data = {}
    start = time.time()
    try:
        with Session(get_engine()) as session:
            full_documents = get_db_text_document_by_ucids(session, ucids)
        for each_doc in full_documents:
            patent_data[each_doc.patent_number.replace("-", "")] = each_doc.dict()
    except RequestException as req_err:
        logger.error("Network or database request failed: %s", req_err)
        return {"error": "Network or database request failed", "details": str(req_err)}
    except AttributeError as attr_err:
        logger.error("Error processing document attributes: %s", attr_err)
        return {"error": "Error processing document attributes", "details": str(attr_err)}
    except Exception as e:
        logger.error("Failed to download patent data due to unexpected error: %s", e)
        return {"error": "Unexpected error", "details": str(e)}
    finally:
        logger.info("Total time taken for UCIDs download from database: %s seconds", time.time() - start)
    return patent_data  

def get_summarize_prompts(prompt_type: str) -> str:
    """ Returns the prompt for summarizing based on the prompt type. """
    if prompt_type == "abstract_summary":
        return """Write a concise summary from the input abstract and summary of an invention. Generated summary must incorporate all the important features."""
    elif prompt_type == "abstract_claims":
        return """Write a concise summary from the input abstract and claims of an invention. Generated summary must incorporate all the important features mentioned in claims and abstract.
Avoid writing the exact claim language, you need to summarize using each claim and their clauses."""
    elif prompt_type == "summary":
        return """Write a concise summary from the input text of an invention. Generated summary must incorporate all the important features mentioned in input text."""
    return ""

def summarize_single_patent(ucid: str, data: dict) -> tuple:
    """ Summarizes a single patent. """
    try:
        abstract, summary, independent_claims, prompt = "", "", "", ""
        patent_number = data.get("patent_number")
        description = data.get("descriptions", [])
        
        if description:
            summary = PatentLoader().extract_summary(description, data)
            if not summary.strip():
                independent_claims = PatentLoader().extract_independent_claim(data)
                
        summary_word_count = len(summary.strip().split())
        claim_word_count = len(independent_claims.strip().split())
        
        if summary_word_count < 200:
            abstracts = data.get("abstracts")
            if abstracts:
                abstract = PatentLoader().extract_abstract(abstracts)

        if summary_word_count >= 200:
            prompt = get_summarize_prompts(prompt_type="summary")
            gen_content = f"{summary.strip()}"
            gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
            messages = [{"role": "system", "content": prompt}, {"role": "user", "content": gen_content}]
            patent_summary = Openai_API().generate_text(messages=messages)
        
        elif summary_word_count >= 20 and summary_word_count < 200:
            prompt = get_summarize_prompts(prompt_type="abstract_summary")
            gen_content = f"Abstract: {abstract.strip()}\n\n Summary of an Invention: {summary.strip()}"
            gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
            messages = [{"role": "system", "content": prompt}, {"role": "user", "content": gen_content}]
            patent_summary = Openai_API().generate_text(messages=messages)
            
        elif claim_word_count >= 40:
            prompt = get_summarize_prompts(prompt_type="abstract_claims")
            gen_content = f"Abstract: {abstract.strip()}\n\n Claims: {independent_claims.strip()}"
            gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
            messages = [{"role": "system", "content": prompt}, {"role": "user", "content": gen_content}]
            patent_summary = Openai_API().generate_text(messages=messages)
            
        elif abstract.strip():
            patent_summary = abstract.strip()
        else:
            selected_title = ""
            titles = data.get("titles")
            for each_title in titles:
                if each_title.get("lang") == "EN":
                    selected_title = each_title.get("text")
            patent_summary = selected_title.strip()    

        return (patent_number, patent_summary)
    
    except DataExtractionError as e:
        logger.error(f"Data extraction error for patent {ucid}: {e}")
    except RuntimeError as re:
        logger.error(f"Runtime error during summary generation for patent {ucid}: {re}")
        raise
    except Exception as e:
        logger.error(f"Error during generate summary {ucid}: {e}")
        raise

def convert_to_batches(lst, batch_size):
    """ Converts a list into smaller batches of a specified size. """
    return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]

def generate_patents_summary(ucids: List[str]) -> List[PatentSummary]:
    """ Generates summaries for a list of UCIDs. """
    total_start_time = time.time()  # Time before the whole process starts
    summaries = []
    total_download_time = 0  # Track total time for downloading patents
    total_summary_time = 0  # Track total time for summarizing patents

    for batch in convert_to_batches(ucids, 100):
        batch_start_time = time.time()  # Time for downloading the current batch
        patent_data = downloaded_patents(batch)
        download_time = time.time() - batch_start_time  # Time spent downloading the batch
        total_download_time += download_time

        # Log time taken for downloading each batch
        logger.info("Time taken to download batch of %d UCIDs: %s seconds", len(batch), download_time)

        start_time = time.time()  # Time for summarizing the current batch
        with ThreadPoolExecutor(max_workers=15) as executor:
            future_to_ucid = {
                executor.submit(summarize_single_patent, ucid, data): ucid
                for ucid, data in patent_data.items()
            }
            for future in as_completed(future_to_ucid):
                ucid = future_to_ucid[future]
                try:
                    patent_number, patent_summary = future.result()
                    if patent_summary:
                        summaries.append(PatentSummary(ucid=patent_number, summary=patent_summary))
                except Exception as e:
                    logger.error(f"Unhandled error in thread for patent {ucid}: {e}")

        summary_time = time.time() - start_time  # Time spent summarizing the batch
        total_summary_time += summary_time

        # Log time taken for summarizing the batch
        logger.info("Time taken to summarize batch of %d UCIDs: %s seconds", len(batch), summary_time)

    total_time = time.time() - total_start_time  # Total time for the entire process
    logger.info("Total time taken for patent summarization process: %s seconds", total_time)
    logger.info("Total time spent downloading patents: %s seconds", total_download_time)
    logger.info("Total time spent summarizing patents: %s seconds", total_summary_time)

    return summaries




from typing import List, Dict
import requests
from math import ceil

def chunk_list(data: List[str], chunk_size: int) -> List[List[str]]:
    """Utility function to split a list into chunks."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def generate_similarity_differences(subject_ucid: str, ucids: List[str], input_key_features: List[str]) -> ComparisonResponse:
    url = f"{COMPARATOR_ML_ENDPOINT}pre_steps/detect_similarity_differences"
    batch_size = 100  # Define the size of each batch
    comparisons = {}

    try:
        # Process ucids in chunks
        for batch in chunk_list(ucids, batch_size):
            payload = {
                "subject_ucid": subject_ucid,
                "ucids": batch,
                "input_key_features": input_key_features
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Merge the batch results into the main comparisons dictionary
            batch_comparisons = response.json().get("comparisons", {})
            comparisons.update(batch_comparisons)
        
        return ComparisonResponse(
            status="success",
            comparisons=comparisons
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error while connecting to comparator service: {e}")
