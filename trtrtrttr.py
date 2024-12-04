import requests
import os

# The URL of the XML file
url = "https://www.orbit.com/export/QPRPL003/XML/1bf86291-e32c-4cd8-824c-a022db147629-095139.full.xml"

# Output directory for saving the downloaded XML
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)

# Extract the filename from the URL
filename = os.path.basename(url)

# Full path to save the file
file_path = os.path.join(output_dir, filename)

# Download the XML data
response = requests.get(url)
if response.status_code == 200:
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"File saved: {file_path}")
else:
    print(f"Failed to download XML. Status code: {response.status_code}")
