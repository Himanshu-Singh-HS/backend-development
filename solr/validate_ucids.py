

from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

patdelanalytics = os.getenv('PATDELANALYTICS_URL') 
 


url = f"{patdelanalytics}/api/v1/patent/number/validate"

df = pd.read_excel("/Users/patdelanalytics/backend-development/solr/test1.xlsx")

print(df.head())
