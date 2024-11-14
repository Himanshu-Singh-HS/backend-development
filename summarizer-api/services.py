# monolith.summarizer.service module

# importing standard modules ==================================================
from typing import List, Dict, Tuple
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
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
    """Download patents by UCIDs from the database and handle any download errors."""
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
    
    prompts = {
        "abstract_summary": "Write a concise summary from the input abstract and summary of an invention. Generated summary must incorporate all the important features.",
        "abstract_claims": """Write a concise summary from the input abstract and claims of an invention. Generated summary must incorporate all the important features mentioned in claims and abstract. Avoid writing the exact claim language, you need to summarize using each claim and their clauses.""",
        "summary": "Write a concise summary from the input text of an invention. Generated summary must incorporate all the important features mentioned in input text."
    }
    return prompts.get(prompt_type, "")


def openai_generate_summary(prompt: str, gen_content: str) -> str:
   
    gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": gen_content},
    ]
    return Openai_API().generate_text(messages=messages)


def convert_to_batches(lst, batch_size):
    return [lst[i: i + batch_size] for i in range(0, len(lst), batch_size)]


def summarize_single_patent(ucid: str, data: dict) -> Tuple[str, str, str, str]:
    
    abstract, summary, independent_claims, prompt, gen_content = "", "", "", "", ""
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
        gen_content = abstract.strip()
        
    else:
        selected_title = next((title.get("text") for title in data.get("titles", []) if title.get("lang") == "EN"), "")
        gen_content = selected_title.strip()

    return patent_number, prompt, gen_content, ucid


def generate_summaries_multithreaded(prompts: List[Tuple[str, str, str]]) -> Dict[str, str]:
    summaries = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_prompt = {
            executor.submit(openai_generate_summary, prompt, content): ucid
            for ucid, prompt, content, _ in prompts
        }
        for future in as_completed(future_to_prompt):
            ucid = future_to_prompt[future]
            try:
                summaries[ucid] = future.result()
            except Exception as e:
                logger.error(f"Error during OpenAI API call for UCID {ucid}: {e}")
    return summaries


def generate_patents_summary123(ucids: List[str]) -> List[PatentSummary]:
    total_start_time = time.time()
    summaries = []
    batch_size = 100

    for batch in convert_to_batches(ucids, batch_size):
        patent_data = downloaded_patents(batch)

        start_time = time.time()

        # First  multiprocessing
        prompts = []
        with ProcessPoolExecutor() as executor:
            future_to_ucid = {
                executor.submit(summarize_single_patent, ucid, data): ucid
                for ucid, data in patent_data.items()
            }
            for future in as_completed(future_to_ucid):
                ucid = future_to_ucid[future]
                try:
                    patent_number, prompt, gen_content, ucid = future.result()
                    if gen_content:
                        prompts.append((ucid, prompt, gen_content, patent_number))
                except Exception as e:
                    logger.error(f"Unhandled error in process for patent {ucid}: {e}")

        # Second - multithreading for OpenAI API calls
        summaries_dict = generate_summaries_multithreaded(prompts)

        # Collect results into the PatentSummary list
        for ucid, summary in summaries_dict.items():
            if summary:
                summaries.append(PatentSummary(ucid=ucid, summary=summary))

    logger.info("Total time taken by summary API: %s seconds", time.time() - total_start_time)
    logger.info("Time calculated after patent downloaded: %s seconds", time.time() - start_time)
    return summaries
