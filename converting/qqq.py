import asposewordscloud
import asposewordscloud.models.requests
from asposewordscloud.rest import ApiException

# Configure Aspose API client with your credentials
client_id = '5aefba5d-0675-4889-a07f-ff5e836027f7'
client_secret = 'dca55b2c0e287d835cbcb224af0580ca'

# Initialize the Words API with your client credentials
words_api = asposewordscloud.WordsApi(client_id, client_secret)

# Specify the path of the input PDF and output DOCX
input_pdf = 'path/to/your/input.pdf'
output_docx = 'path/to/your/output.docx'
input_pdf = '/Users/patdelanalytics/backend-development/converting/xyz.pdf'
output_docx = '/Users/patdelanalytics/backend-development/converting/oo.doc'

# Upload the PDF file to Aspose Cloud storage (optional step if file is already stored)
upload_request = asposewordscloud.models.requests.UploadFileRequest(
    open(input_pdf, 'rb'), "/input.pdf")
words_api.upload_file(upload_request)

# Convert the PDF to DOCX and save it
try:
    # Conversion request
    convert_request = asposewordscloud.models.requests.ConvertDocumentRequest(
        document=open(input_pdf, 'rb'), format='docx')

    # Perform the conversion
    result = words_api.convert_document(convert_request)

    # Write the result to a file
    with open(output_docx, 'wb') as output_file:
        output_file.write(result)
        
    print("PDF successfully converted to DOCX with Aspose!")
    
except ApiException as e:
    print("Exception when calling Aspose Words API:", e)
