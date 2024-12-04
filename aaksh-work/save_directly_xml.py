import requests
import os

# List of URLs
urls = [
    "https://www.orbit.com/export/QPRPL003/XML/1bf86291-e32c-4cd8-824c-a022db147629-095139.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/2df911c8-4104-4ac4-b9c6-afb62681cad5-134838.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/dc20f9af-1df7-4e4d-95a4-742477e63ad0-135011.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/cce79836-b6a6-4fbf-8a32-a855ff1c2fb0-135108.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/0e0b0f2a-6d3f-4d82-ab40-76571bcb49c4-135210.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/862b8826-0939-4142-8a69-361236601c39-135313.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/748f95e7-32bd-47ad-8104-1b19a51429a2-140304.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/53aaf72b-6363-4c24-a9cd-a20f7da5cfa9-140524.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/24364add-e93d-49bf-863e-ef996160eeba-140704.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/53ee9a3a-1fbc-4216-9600-e9afc5f552b4-141449.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/b476f572-411b-4934-8669-01afb80477a1-141802.full.xml",
    "https://www.orbit.com/export/MDD70RQR/XML/b3693056-e48b-489f-a842-b80d0f653051-142056.full.xml",
]

# Output directory for saving the downloaded XML files
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)

# Loop through each URL
for url in urls:
    # Extract the filename from the URL
    filename = os.path.basename(url)
    file_path = os.path.join(output_dir, filename)

    try:
        # Download the XML data
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"File saved: {file_path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while downloading {url}: {e}")

print("All downloads completed!")
