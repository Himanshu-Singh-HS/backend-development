
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()
import os
url=os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch([url])

if es.ping():
    print("Successfully connected to Elasticsearch")
else:
    print("Connection failed")

document = {
    "title": "Understanding Elasticsearch",
    "author": "John Doe",
    "content": "This document explains how to use Elasticsearch with Python."
}

# response = es.index(
#     index="my-index",   
#     id=1,   
#     body=document 
# )

# print("Document indexed:", response)

#  Document indexed: {'_index': 'my-index', '_id': '1', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}


# Search for documents

response = es.search(
    index="sher_sir_data",   
    body={
        "query": {
            "match": {
                "content": "elasticsearch"   
            }
        }
    }
)

if response['hits']['hits']:
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Source: {hit['_source']}")
else:
    print("No results found.")
    
# indices = es.cat.indices(format="json")
# for index in indices:
#     print(index['index'])  # Prints the name of each index
# Get all index names


# indices_to_check = ["my-index", "sher_sir_data", "patents"]
# indices_to_check=["sher_sir_data"]

# for index in indices_to_check:
#     try:
#         response = es.search(index=index, body={"query": {"match_all": {}}}, size=1000)  
#         print(f"\nDocuments in index '{index}':")
        
#         # Check if any documents exist
#         if response["hits"]["hits"]:
#             for doc in response["hits"]["hits"]:
#                 print(doc["_source"])  # Prints the document content
#         else:
#             print("No documents found in this index.")
#     except Exception as e:
#         print(f"Error fetching documents from index '{index}': {e}")







# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch(["http://your-cluster-name:9200"])

# # List all indices in the cluster
# indices = es.cat.indices(format="json")

# # Print out the indices
# print("Indices in the cluster:")
# for index in indices:
#     print(index['index'])






# #updfate 
# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch(["http://your-cluster-name:9200"])

# # Update a document
# response = es.update(
#     index="my-index",  # The index name
#     id=1,  # The ID of the document you want to update
#     body={
#         "doc": {
#             "content": "This is an updated explanation of how to use Elasticsearch with Python."
#         }
#     }
# )

# print("Document updated:", response)



# #delete 
# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch(["http://your-cluster-name:9200"])

# # Delete a document by ID
# response = es.delete(
#     index="my-index",  # The index name
#     id=1  # The document ID
# )

# print("Document deleted:", response)

# #monitor cluster health 
# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch(["http://your-cluster-name:9200"])

# # Get the health status of the cluster
# health = es.cluster.health()

# print("Cluster health:", health)










#jsonresponse of elastic search


# {
#   "took": 5,
#   "timed_out": false,
#   "_shards": {
#     "total": 1,
#     "successful": 1,
#     "skipped": 0,
#     "failed": 0
#   },
#   "hits": {
#     "total": {
#       "value": 1,
#       "relation": "eq"
#     },
#     "max_score": 0.2876821,
#     "hits": [
#       {
#         "_index": "my-index",
#         "_id": "1",
#         "_score": 0.2876821,
#         "_source": {
#           "title": "Understanding Elasticsearch",
#           "author": "John Doe",
#           "content": "This document explains how to use Elasticsearch with Python."
#         }
#       }
#     ]
#   }
# }
