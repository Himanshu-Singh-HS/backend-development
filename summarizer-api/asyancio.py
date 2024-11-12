# this is code for implement by asyncio function 

# @summarizer_router.post(
#     path="/generate_summary",
#     response_model=PatentSummaryResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_summary(request: PatentSummaryRequest)->PatentSummaryResponse:
#     request.ucids = [ucid for ucid in request.ucids if ucid.strip()]
#     if not request.ucids:
#         raise HTTPException(status_code=400, detail="UCID list cannot be empty or contain only empty strings.")

#     try:
#         result: Dict[str, str] = await generate_patents_summary3(request.ucids)
#         if result is None or not result:   
#             raise HTTPException(status_code=404, detail="No summaries were generated.")
#         print(result)
#         return PatentSummaryResponse(summaries=result)
#     except Exception as e:
#         logging.error(f"Error processing document: {e}")
#         raise HTTPException(status_code=500, detail="An error occurred during summarization.")
    

#and all the things are imported 

# def get_summarize_prompts(prompt_type: str) -> str:
#         prompt = ""
#         if prompt_type == "abstract_summary":
#             prompt = """Write a concise summary from the input abstract and summary of an invention. Generated summary must encorporate all the important features."""
#         elif prompt_type == "abstract_claims":
#             prompt = """Write a concise summary from the input abstract and claims of an invention. Generated summary must encorporate all the important features mentioned in claims and abstract.
# Avoid writing the exact claim language, you need to summarize using each claim and their clauses.
# """
#         elif prompt_type == "summary":
#             prompt = """Write a concise summary from the input text of an invention. Generated summary must encorporate all the important features mentioned in input text."""

#         return prompt
 

# async def summarize_single_patent(ucid: str, data: dict) -> tuple:
#     try:
#         abstract, summary, independent_claims, prompt = "", "", "", ""

#         patent_number: str = data.get("patent_number")
#         description: List = data.get("descriptions", [])
        
#         if description:
#             summary: str = PatentLoader().extract_summary(description,data)
#             if not summary.strip():
#                 independent_claims: str = PatentLoader().extract_independent_claim(data) 
                
#         summary_word_count: int = len(summary.strip().split())
#         claim_word_count: int = len(independent_claims.strip().split())
        
#         if summary_word_count < 200:
#             abstracts = data.get("abstracts")
#             if abstracts:
#                 abstract: str = PatentLoader().extract_abstract(abstracts)

#         if summary_word_count >= 200:
#             prompt: str = get_summarize_prompts(prompt_type="summary")
#             gen_content = f"{summary.strip()}"
#             gen_content = Processing_steps().string_stripper_tiktoken(gen_content)
    
#             messages = [
#                 {"role": "system", "content": prompt},
#                 {
#                     "role": "user",
#                     "content": gen_content,
#                 },
#             ]
#             patent_summary: str = Openai_API().generate_text(messages=messages)
        
#         elif summary_word_count >= 20 and summary_word_count < 200:
#             prompt: str = get_summarize_prompts(prompt_type="abstract_summary")

#             gen_content = f"Abstract: {abstract.strip()}\n\n Summary of an Invention: {summary.strip()}"
#             gen_content = Processing_steps().string_stripper_tiktoken(gen_content)

#             messages = [
#                 {"role": "system", "content": prompt},
#                 {
#                     "role": "user",
#                     "content": gen_content,
#                 },
#             ]
#             patent_summary: str = Openai_API().generate_text(messages=messages)
        
#         elif claim_word_count >= 40:
#             prompt: str = get_summarize_prompts(prompt_type="abstract_claims")

#             gen_content = f"Abstract: {abstract.strip()}\n\n Claims: {independent_claims.strip()}"
#             gen_content =  Processing_steps().string_stripper_tiktoken(gen_content)

#             messages = [
#                 {"role": "system", "content": prompt},
#                 {
#                     "role": "user",
#                     "content": gen_content,
#                 },
#             ]
#             patent_summary: str = Openai_API().generate_text(messages=messages)
#         elif abstract.strip():
#             patent_summary: str = abstract.strip()
#         else:
#             selected_title = ""
#             titles: List = data.get("titles")
#             for each_title in titles:
#                 if each_title.get("lang") == "EN":
#                     selected_title: str = each_title.get("text")

#             patent_summary: str = selected_title.strip()
            
        
#         return (patent_number, patent_summary)
    
#     except Exception as e:
#         logger.error(f"Error summarizing patent {ucid}: {e}")
#         return (ucid, None)
    
# async def generate_patents_summary3(ucids: List[str]) -> Dict[str, str]:
#     total_start_time = time.time()
#     patent_data =  downloaded_patents(ucids)  
#     # print("this is poatent data ->",patent_data)
#     summaries = {}

#     tasks = [
#         summarize_single_patent(ucid, data)
#         for ucid, data in patent_data.items()
#     ]
    
#     results = await asyncio.gather(*tasks, return_exceptions=True)

#     for result in results:
#         if isinstance(result, tuple):
#             patent_number, patent_summary = result
#             if patent_summary:
#                 summaries[patent_number] = patent_summary
#         else:
#             logger.error(f"Unhandled error in task: {result}")

#     print("Total time taken by summary API:", time.time() - total_start_time)
#     logger.info("summries generated -> ",summaries)
#     print("priting summaries ",summaries)
#     return summaries




# wrong code for implemented by asyncio below but only minor issue , after some time , will check 