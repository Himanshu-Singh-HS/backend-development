# '''
#  ->>>>   these are the command for elastic search for indexing

# 1. print(es.cat.indices())
# 2. response = es.indices.delete(index=index_name, ignore=[400, 404])


# '''

# from elasticsearch import Elasticsearch, helpers
# from elasticsearch import Elasticsearch
# from dotenv import load_dotenv
# load_dotenv()
# import os
# import json
# index_name="hs"

# url=os.getenv("ELASTICSEARCH_URL")
# es = Elasticsearch([url])
# if es.ping():
#     print("Successfully connected to Elasticsearch")
# else:
#     print("Connection failed")


# settings = {
#     "settings": {
#         "analysis": {
#             "analyzer": {
#                 "custom_text_analyzer": {
#                     "type": "custom",
#                     "tokenizer": "standard",
#                     "filter": ["lowercase"]
#                 }
#             }
#         }
#     },
#     "mappings": {
#         "properties": {
#             "Ucid": {"type": "keyword"},
#             "Title": {"type": "text", "analyzer": "custom_text_analyzer"},
#             "Abstract": {"type": "text", "analyzer": "custom_text_analyzer"},
#             "Claims": {"type": "text", "analyzer": "custom_text_analyzer"},
#             "Description": {"type": "text", "analyzer": "custom_text_analyzer"}
#         }
#     }
# }

# if not es.indices.exists(index=index_name):
#     es.indices.create(index=index_name, body=settings)
#     print(f"Created index: {index_name}")
# else:
#     print(f"Index {index_name} already exists")


# def print_all_data_from_index(index_name):
#     query = {
#         "query": {
#             "match_all": {}
#         },
#         "_source": True,
#         "size": 10000
#     }
#     response = es.search(index=index_name, body=query)
#     for hit in response['hits']['hits']:
#         print(json.dumps(hit['_source'], indent=4))

# def convert_to_batches(lst, batch_size):
#     return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]

# def index_json_file(file_path, index_name):
#     with open(file_path, "r") as file:
#         response_data = json.load(file)
#     bulk_data=[]
#     doc = {
#         "_index": index_name,
#         "_source": {
#                 "Ucid": response_data.get("patent_number",""),
#                 "Title": response_data.get("title","") ,
#                 "Abstract": response_data.get("abstract","") ,
#                 "Claims": response_data.get("claims","") ,
#                 "Description": response_data.get("descriptions","") ,
#         }
#     }
#     bulk_data.append(doc)
#     helpers.bulk(es, bulk_data)


# json_file_path = "/Users/patdelanalytics/backend-development/aaksh-work/xml"
# index_json_file(json_file_path, index_name)
# # print_all_data_from_index(index_name)


import os
import json
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("ELASTICSEARCH_URL")
index_name = "himanshu-index2"

# Initialize Elasticsearch
es = Elasticsearch([url], timeout=60, max_retries=3, retry_on_timeout=True)
if es.ping():
    print("Successfully connected to Elasticsearch")
else:
    print("Connection failed")
    exit()

# Define index settings and mappings
settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_text_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "Ucid": {"type": "keyword"},
            "Title": {"type": "text", "analyzer": "custom_text_analyzer"},
            "Abstract": {"type": "text", "analyzer": "custom_text_analyzer"},
            "Claims": {"type": "text", "analyzer": "custom_text_analyzer"},
            "Description": {"type": "text", "analyzer": "custom_text_analyzer"}
        }
    }
}


if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=settings)
    print(f"Created index: {index_name}")
else:
    print(f"Index {index_name} already exists")


def index_json_files_in_directory(directory_path, index_name):

    bulk_data = []
    file_count = 0

    for folder_name in os.listdir(directory_path):
        subdirectory_path = os.path.join(directory_path, folder_name) 

        if os.path.isdir(subdirectory_path):
            print(f"Processing folder: {folder_name}")

            for file_name in os.listdir(subdirectory_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(subdirectory_path, file_name)

                    
                    with open(file_path, "r") as file:
                        try:
                            response_data = json.load(file)
                        except json.JSONDecodeError as e:
                            print(
                                f"Skipping invalid JSON file: {file_path}. Error: {e}")
                            continue

                 
                    doc = {
                        "_index": index_name,
                        "_source": {
                            "Ucid": response_data.get("patent_number", ""),
                            "Title": response_data.get("title", ""),
                            "Abstract": response_data.get("abstract", ""),
                            "Claims": response_data.get("claims", ""),
                            "Description": response_data.get("descriptions", ""),
                        }
                    }
                    bulk_data.append(doc)
                    file_count += 1

                    # Index in batches of 500
                    if len(bulk_data) >= 100:
                        helpers.bulk(es, bulk_data)
                        bulk_data = []

    if bulk_data:
        helpers.bulk(es, bulk_data)

    print(
        f"Successfully indexed {file_count} JSON files from directory: {directory_path}")


main_directory_path = "/Users/patdelanalytics/backend-development/aaksh-work/xml"

index_json_files_in_directory(main_directory_path, index_name)


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
