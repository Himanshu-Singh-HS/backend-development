import os
import json
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import logging

load_dotenv()
url = os.getenv("ELASTICSEARCH_URL")

 
es = Elasticsearch([url])
if es.ping():
    print("Successfully connected to Elasticsearch")
else:
    print("Connection failed")
    exit()


index_name = "hs1"

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

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=settings)
    print(f"Created index: {index_name}")
else:
    print(f"Index {index_name} already exists")


# Function to index JSON file data
def index_json_file(file_path, index_name):
    with open(file_path, "r") as file:
        response_data = json.load(file)
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
    helpers.bulk(es, [doc])

# List of JSON file paths
json_files = [
     "aaksh-work/xmldata/data2/US1332667.json",
     "/Users/patdelanalytics/backend-development/aaksh-work/xmldata/data11/US20090045107.json"
]

# Index each JSON file
# for file_path in json_files:
#     index_json_file(file_path, index_name)

print("All files indexed successfully.")
