from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()
import os
 
url = os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch([url])
try:
    if es.ping():
        print("Successfully connected to Elasticsearch")
    else:
        print("Connection failed")
        exit()
        
except Exception as e :
    print("not connected with database ",e)

    
#==============================================

def search_data(index,body):
    try:
        result=es.search(index=index,body=body)
        if result['hits']['hits']:
            for hit in result['hits']['hits']:
                print(hit,hit['_source'])
        else:
            print("no data found in documents")
    except Exception as e:
        print("error here ",e)
     
#==============================================


# response = es.search(
#     index="sher_sir_data",   
#     body={
#         "query": {
#             "match": {
#                 "content": "elasticsearch"   
#             }
#         }
#     }
# # )
# search_data( index="my-index", body={
#         "query": {
#             "match": {
#                 "content": "elasticsearch"   
#             }
#         }
#     })
# search_data("sher_sir_data",body={"query": {"match_all": {}}})




 