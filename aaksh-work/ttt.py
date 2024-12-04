import re
import xml.etree.ElementTree as ET
import requests

# Fetch XML from URL
url = "https://www.orbit.com/export/QPRPL003/XML/1bf86291-e32c-4cd8-824c-a022db147629-095139.full.xml"
response = requests.get(url)

if response.status_code == 200:
    xml_data = response.text
else:
    print(f"Failed to fetch XML, status code {response.status_code}")
    exit()

# Parse XML
root = ET.fromstring(xml_data)

# Function to extract the patent number
def extract_patent_number(element):
    # Find the field with name="PN"
    pn_field = element.find(".//QOfield[@name='PN']")
    if pn_field is not None:
        # Extract the text from the QOsen tag within the PN field
        qosen = pn_field.find(".//QOsen")
        if qosen is not None:
            patent_number = "".join(qosen.itertext()).strip()  # Combine all text
            # Clean up the number if needed (e.g., remove invalid characters or add hyphens)
            patent_number = re.sub(r"\s+", "", patent_number)  # Remove spaces
            return patent_number
    return "N/A"

# Iterate over all QOdocument elements and extract the patent number
for document in root.findall(".//QOdocument"):
    patent_number = extract_patent_number(document)
    print(f"Extracted Patent Number: {patent_number}")
