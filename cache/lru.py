




#  corrected code for caching 


# @summarizer_router.post(
#     path="/generate_summary",
#     response_model=PatentSummaryResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_summary(request: PatentSummaryRequest, dummy_data: bool = Query(default=False)) -> PatentSummaryResponse:
 
#     request.ucids = [ucid for ucid in request.ucids if ucid.strip()]
#     if not request.ucids:
#         raise HTTPException(status_code=400, detail="UCID list cannot be empty or contain only empty strings.")
    
#     all_summaries = []
#     for ucid in request.ucids:
#         cached_summary = await cache.get(ucid)   
        
#         if cached_summary:
#             all_summaries.append(PatentSummary(ucid=ucid, summary=cached_summary))
#         else:
#             try:
#                 new_summary : List[PatentSummary] = generate_patents_summary([ucid], dummy_data)
                
#                 if new_summary:
#                     if not isinstance(new_summary, str):
#                         new_summary = str(new_summary) 
                   
#                     await cache.set(ucid, new_summary, ttl=180)  
#                     all_summaries.append(PatentSummary(ucid=ucid, summary=new_summary))
#                 else:
#                     logging.warning(f"No summary generated for UCID {ucid}")
#             except Exception as e:
#                 logging.error(f"Error processing UCID {ucid}: {e}")
#                 raise HTTPException(status_code=500, detail="An error occurred during summarization.")
    
 
#     if not all_summaries:
#         raise HTTPException(status_code=404, detail="No summaries were generated.")
 
#     return PatentSummaryResponse(summaries=all_summaries)
