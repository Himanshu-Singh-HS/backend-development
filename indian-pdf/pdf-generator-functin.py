
from fastapi.responses import StreamingResponse
@handle_errors
@time_decorator
def export_patent_drafting_file(
    search_id: str, file_type: DraftingFileType, user: AuthorizedUser
) ->  Union[StreamingResponse, str]:
    s3_key = f"{search_id}/export_file.{file_type.value}"
    s3_url: str = f"https://{DRAFTING_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    try:
        existing_report = fetch_drafting_report_registry(
            search_id=search_id, user_uuid=user.user_uuid
        )
        search_request = fetch_drafting_request_registry(
            search_id=search_id, user_uuid=user.user_uuid
        )
        jurisdiction = search_request.search_parameters.jurisdiction
        # if jurisdiction not in {'US', 'EP' ,'IN'}:
        if jurisdiction not in [SelectJurisdiction.US.value, SelectJurisdiction.EP.value, SelectJurisdiction.IN.value]:
            raise ValueError(f"Unsupported jurisdiction: {jurisdiction}")
        
        if jurisdiction in [SelectJurisdiction.EP, SelectJurisdiction.IN]:
            if file_type in {DraftingFileType.DOCX, DraftingFileType.DOC}:
                document_buffer=PdfGeneratorEP().convert_json_to_pdf_buffer(existing_report.dict(),search_request) 
                document_buffer=pdf_buffer_to_docx_buffer(document_buffer)
            elif file_type == DraftingFileType.PDF:
                document_buffer=PdfGeneratorEP().convert_json_to_pdf_buffer(existing_report.dict(),search_request) 
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        else:
            if file_type in {DraftingFileType.DOCX, DraftingFileType.DOC}:
                document_buffer=DocGeneratorUS().convert_json_to_doc_buffer(existing_report.dict(),search_request)   
            elif file_type == DraftingFileType.PDF:
                document_buffer=PdfGeneratorUS().convert_json_to_pdf_buffer(existing_report.dict(),search_request)
            else:
                raise ValueError(f"Unsupported file type: {file_type}") 
        
        # s3_client = get_s3_client()
        # s3_client.upload_fileobj(document_buffer, DRAFTING_BUCKET_NAME, s3_key)
        # logger.info(f"Drafting file uploaded to S3 at URL: {s3_url}")
    
        existing_report.status = ServiceHistroyStatus.COMPLETE
        existing_report.save_changes()

        existing_user_request_history: UserSearchHistoryRegistry = (
            UserSearchHistoryRegistry.find_one(
                UserSearchHistoryRegistry.user_uuid == user.user_uuid,
                UserSearchHistoryRegistry.request_id == search_id,
            ).run()
        )

        if existing_user_request_history is None:
            error_msg = f"Document with search ID '{search_id}' not found."
            logger.error(error_msg)
            raise NotFoundException(error_msg) from None

        existing_user_request_history.request_status = ServiceHistroyStatus.COMPLETE
        existing_user_request_history.save_changes()
        return StreamingResponse(
            document_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=export_file.{file_type.value}"
            },
        )

        return s3_url
    
    
    

@file_generator.get(
    path="/drafting_export_file",
    status_code=status.HTTP_200_OK,
    # response_model=FileGeneratorResponseBody,
    responses={
        200: {"content": {"application/pdf": {}}},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def get_drafting_export_file(
    current_user: AuthorizedUser = Depends(get_authorized_user),
    search_id: str = Query(..., alias="search_id", title="a user search id"),
    file_type: DraftingFileType = Query(...),
):
    try:
        response = export_patent_drafting_file(search_id, file_type, current_user)
        return response
    except NotFoundException as not_found_error:
        logger.error(not_found_error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=HTTPExceptionDetails(message=str(not_found_error)).dict(),
        ) from not_found_error

    except Exception as any_exception:
        logger.error(any_exception, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=HTTPExceptionDetails(message=str(any_exception)).dict(),
        ) from any_exception

    # return FileGeneratorResponseBody(file_path=response)
