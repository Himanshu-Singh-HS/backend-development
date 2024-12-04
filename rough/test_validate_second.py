import pandas as pd
import requests
import json

# Read the Excel file
# df = pd.read_excel("rough/test3.xlsx")
df=pd.read_excel("rough/test4.xlsx")
df=pd.read_excel("aaksh-work/aksh_ucids.xlsx")

 
print(df.columns)
num_rows = len(df)   
print(f"Total number of rows: {num_rows}")

 
url = "https://beta.patdelanalytics.ai/api/v1/patent/number/validate"

 
publication_numbers = df['Publication numbers with kind code'].tolist()

 
payload = {"numbers": publication_numbers}

 
successful_numbers = []
does_not_exists=[]

try:
    
    response = requests.post(url, json=payload)
    response.raise_for_status()  

 
    data = response.json()

    
    for item in data.get("numbers", []):
        if item.get("status") == "OK": 
            successful_numbers.append(item["number"])
        if item.get("status") == "ERROR": 
            does_not_exists.append(item["number"])
    print("succesfull")

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")

 
with open("rough/output2/success_data2.json", "w") as json_file:
    json.dump(successful_numbers, json_file, indent=4)
with open("rough/output2/error_data2.json", "w") as json_file:
    json.dump(does_not_exists, json_file, indent=4)

print(f"Validation complete. Total successful numbers saved: {len(successful_numbers)},and,error/does not exists{len(does_not_exists)}")   
#first file - Validation complete. Total successful numbers saved: 20458, and, error/does not exists1386
#second file - Validation complete. Total successful numbers saved: 28779,and,error/does not exists1699