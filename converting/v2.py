
import subprocess,os

# # Define the path to the soffice executable and the PDF file
soffice_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
input_pdf = '/Users/patdelanalytics/backend-development/converting/xyz.pdf'
output_dir = '/Users/patdelanalytics/backend-development/converting/doc12'
command = [
    soffice_path, 
    '--headless', 
    '--convert-to', 'doc:writer8',  # specify docx output format
    # '--convert-to', 'docx:"MS Word 2007 XML"', 
    # '--convert-to', 'docx:MS Word 2007 XML',
    # '--convert-to', 'doc:writer',  
    # '--convert-to', 'rtf',
    '--convert-to', 'docx', 
    '--outdir', output_dir, 
    input_pdf
]
 
try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("PDF successfully converted to DOCX!")
    print("Output:", result.stdout.decode('utf-8'))
    print("Error Output (if any):", result.stderr.decode('utf-8'))
except subprocess.CalledProcessError as e:
    print(f"Error during conversion: {e.stderr.decode('utf-8')}")


 