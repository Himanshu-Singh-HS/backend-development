'''
 ->>>>   these are the command for elastic search for indexing 

1. print(es.cat.indices())
2. response = es.indices.delete(index=index_name, ignore=[400, 404])


'''
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os
import json
import logging
import time

load_dotenv()

# Connect to Elasticsearch
url = os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch([url])

if es.ping():
    print("Successfully connected to Elasticsearch")
else:
    print("Connection failed")

index_name = "hs"

def print_all_data_from_index(index_name):
    
    query = {
        "query": {
            "match_all": {}
        },
        "_source": True,  
        "size": 10000   
    }

    response = es.search(index=index_name, body=query)
    
    for hit in response['hits']['hits']:
        print(json.dumps(hit['_source'], indent=4))   



def index_json_file(file_path, index_name):
    with open(file_path, "r") as file:
        response_data = json.load(file)

    bulk_data = []

    doc = {
        "_index": index_name,
        "_id": response_data.get("patent_number", ""), 
        "_source": {
            "Ucid": response_data.get("patent_number", ""),
            "Title": response_data.get("title", ""),
            "Abstract": response_data.get("abstract", ""),
            "Claims": response_data.get("claims", ""),
            "Description": response_data.get("descriptions", ""),
        }
    }
    bulk_data.append(doc)
    helpers.bulk(es, bulk_data)
    
    document_id = response_data.get("patent_number")
    if es.exists(index=index_name, id=document_id):
        print(f"Document {document_id} exists in index.")
    else:
        print(f"Document {document_id} does not exist in the index.")

        
    # Ensure the document is indexed
    document_id = response_data.get("patent_number")  # Use patent_number as the unique document ID
    if document_id:
        time.sleep(2)  # Adding a small delay to allow Elasticsearch to index the document
        try:
            search_response = es.get(index=index_name, id=document_id)
            if search_response['found']:
                logging.info(f"Document with patent_number {document_id} successfully indexed.")
                print("sucess")
            else:
                logging.error(f"Document with patent_number {document_id} not found after indexing.")
        except Exception as e:
            logging.error(f"Error retrieving document with patent_number {document_id}: {e}")
    else:
        logging.error("No patent_number found in the document, cannot verify indexing.")

json_file_path = "/Users/patdelanalytics/backend-development/aaksh-work/xml/data4/US2934267A.json"
# index_json_file(json_file_path, index_name)

# Print all data in the index
# print_all_data_from_index(index_name)
print(es.cat.indices())













#  # Perform bulk indexing
#     success, failed = helpers.bulk(es, bulk_data)
#     if success:
#         print(f"Successfully indexed {len(bulk_data)} documents.")
#     else:
#         print(f"Failed to index some documents.")

#     # Ensure the document is indexed by searching for Ucid
#     document_id = response_data.get("patent_number")
#     if document_id:
#         retries = 3  # Try up to 3 times
#         for _ in range(retries):
#             time.sleep(1)  # Wait a bit for Elasticsearch to process the document
#             try:
#                 # Query Elasticsearch to find the document by the "Ucid" field
#                 search_response = es.search(index=index_name, body={
#                     "query": {
#                         "term": {"Ucid.keyword": document_id}  # Use the keyword field for exact match
#                     }
#                 })
#                 if search_response['hits']['total']['value'] > 0:
#                     logging.info(f"Document with patent_number {document_id} successfully indexed.")
#                     break  # Document found, exit retry loop
#             except Exception as e:
#                 logging.error(f"Error retrieving document with patent_number {document_id}: {e}")
#                 continue  # Retry if there's an error
#         else:
#             logging.error(f"Document with patent_number {document_id} not found after retries.")