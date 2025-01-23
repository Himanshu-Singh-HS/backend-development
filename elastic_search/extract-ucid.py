import pandas as pd
import re

def get_patent_numbers(filepath, column_name,sheetname):
  
    try:
        df = pd.read_excel(filepath,sheet_name=sheetname)
      
        if column_name in df.columns:
            
            return df[column_name].dropna().unique().tolist()
        else:
            raise ValueError(f"Column '{column_name}' not found in the file.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")

# Usage
filepath = 'elastic_search/Seq and Structure Records Sheet.xlsx'
column_name = 'Family publication details'   
column_name="Patent Numbers"
sheetname = "Markush Structure"
# patent_numbers = get_patent_numbers(filepath, column_name,sheetname)
# for num,ucids  in enumerate(patent_numbers):
#     print(f"'{ucids}',")
# print("len of ucids ",len(patent_numbers))

# print("dfghsdfgh\n")



def extract_ucids_with_kindcode(filepath, column_name,sheetname):
    try:
        df = pd.read_excel(filepath,sheet_name=sheetname)

        if column_name in df.columns:
            column_data = df[column_name].dropna()
            ucids = []
            for entry in column_data:
             
                match = re.findall(r'[A-Z]{2}\d+[A-Z]?\d*\s+[A-Z]\d', str(entry))
                if match:
                    # Clean and format UCIDs to remove extra spaces
                    ucids.extend([re.sub(r'\s+', '', m) for m in match])
            
            # Remove duplicates and return the cleaned list
            return list(set(ucids))
        else:
            raise ValueError(f"Column '{column_name}' not found in the file.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the file: {e}")
filepath = 'elastic_search/Seq and Structure Records Sheet.xlsx'
column_name = 'Family publication details' 
sheetname = "Markush Structure" 
ucid_data = extract_ucids_with_kindcode(filepath, column_name,sheetname)

# Print the results
for num, ucid in enumerate(ucid_data):
    print(f"'{ucid}',")
print("Total Unique UCIDs:", len(ucid_data))
