# monolith.summarizer.service module

# importing standard modules ==================================================
from typing import List
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed,ThreadPoolExecutor
from multiprocessing import Pool

# importing custom modules ====================================================
from monolith.summarizer.data_loader import PatentLoader
from monolith.summarizer.exceptions import DataExtractionError
from monolith.summarizer.openai_api import Openai_API
from monolith.summarizer.processing import Processing_steps
from monolith.patent.db_service import get_db_text_document_by_ucids
from _patentdb.engine import get_engine
from monolith.summarizer.schema import PatentSummary

# importing third-party modules ===============================================
from sqlalchemy.orm import Session
from requests.exceptions import RequestException

# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)

def downloaded_patents(ucids: List[str]) -> dict:
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
    prompt = ""
    if prompt_type == "abstract_summary":
        prompt = """Write a concise summary from the input abstract and summary of an invention. Generated summary must encorporate all the important features."""
    elif prompt_type == "abstract_claims":
        prompt = """Write a concise summary from the input abstract and claims of an invention. Generated summary must encorporate all the important features mentioned in claims and abstract.
Avoid writing the exact claim language, you need to summarize using each claim and their clauses.
"""
    elif prompt_type == "summary":
        prompt = """Write a concise summary from the input text of an invention. Generated summary must encorporate all the important features mentioned in input text."""
    return prompt

def openai_generate_summary(prompt: str, gen_content: str) -> str:
    
    gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": gen_content},
    ]
    return Openai_API().generate_text(messages=messages)


def convert_to_batches(lst, batch_size):
    return [lst[i: i + batch_size] for i in range(0, len(lst), batch_size)]



def openai_generate_summary_threaded(prompt: str, gen_content: str) -> str:
    try:
        return openai_generate_summary(prompt, gen_content)
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        return ""

def summarize_single_patent(ucid: str, data: dict) -> tuple:
    try:
        abstract, summary, independent_claims, prompt = "", "", "", ""
        patent_number: str = data.get("patent_number")
        description: List = data.get("descriptions", [])

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
            
        elif summary_word_count >= 20 and summary_word_count < 200:
            prompt = get_summarize_prompts(prompt_type="abstract_summary")
            gen_content = f"Abstract: {abstract.strip()}\n\n Summary of an Invention: {summary.strip()}"
            
        elif claim_word_count >= 40:
            prompt = get_summarize_prompts(prompt_type="abstract_claims")
            gen_content = f"Abstract: {abstract.strip()}\n\n Claims: {independent_claims.strip()}"
        elif abstract.strip():
            patent_summary: str = abstract.strip()
        else:
            selected_title = ""
            titles: List = data.get("titles")
            for each_title in titles:
                if each_title.get("lang") == "EN":
                    selected_title: str = each_title.get("text")
            patent_summary: str = selected_title.strip()   

        # Multi-threading for OpenAI API call
        with ThreadPoolExecutor(max_workers=5) as thread_executor:
            future = thread_executor.submit(openai_generate_summary_threaded, prompt, gen_content)
            patent_summary = future.result()

        return (patent_number, patent_summary)

    except Exception as e:
        logger.error(f"Error during generating summary for patent {ucid}: {e}")
        return (ucid, None)

def generate_patents_summary(ucids: List[str]) -> List[PatentSummary]:
    total_start_time = time.time()
    summaries = []
    batch_size = 100

    for batch in convert_to_batches(ucids, batch_size):
        patent_data = downloaded_patents(batch)

        start_time = time.time()  # Time calculated after download

        with ProcessPoolExecutor(max_workers=15) as executor:
            future_to_ucid = {}
            for ucid, data in patent_data.items():
                future = executor.submit(summarize_single_patent, ucid, data)
                future_to_ucid[future] = ucid

            for future in as_completed(future_to_ucid):
                ucid = future_to_ucid[future]
                try:
                    patent_number, patent_summary = future.result()
                    if patent_summary:
                        summaries.append(PatentSummary(ucid=patent_number, summary=patent_summary))
                except Exception as e:
                    logger.error(f"Unhandled error in process for patent {ucid}: {e}")

    logger.info("Total time taken by summary API: %s seconds", time.time() - total_start_time)
    logger.info("Time calculated after patent downloaded: %s seconds", time.time() - start_time)
    return summaries
