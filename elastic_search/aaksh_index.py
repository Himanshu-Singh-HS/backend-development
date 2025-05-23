import os
import json
import re
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
from bs4 import BeautifulSoup
# Load environment variables
load_dotenv()
url = os.getenv("ELASTICSEARCH_URL")
# index_name = "himanshu-index2"
index_name = "himanshu_custom_tokenizer"
# index_name='abcd'


# Initialize Elasticsearch
es = Elasticsearch([url], timeout=60, max_retries=3, retry_on_timeout=True)
print('himanhsu singh ')
if es.ping():
    print("Successfully connected to Elasticsearch")
 
else:
    print("Connection failed")

settings = {
  "settings": {
    "analysis": {
      "analyzer": {
        # "edge_ngram_analyzer": {
        #   "tokenizer": "edge_ngram_tokenizer",
        #   "filter": ["lowercase"]
        # },
        "custom_text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        # "filter": ["lowercase"]  # This makes indexing case-insensitive
                        "filter": ["lowercase_filter", "stop_filter"]

                    }
      },
    #   "tokenizer": {
    #     "edge_ngram_tokenizer": {
    #       "type": "edge_ngram",
    #       "min_gram": 2,
    #       "max_gram": 10,
    #       "token_chars": ["letter", "digit"]
    #     }
    #   }
    }
  },
  "_source": {
    "enabled": False
  },
  "mappings": {
    "properties": {
      "PublicationDate": {
        "type": "date",
        "format": "yyyy-MM-dd",
                "store": True

      },
      "AssigneeNames": {
        "type": "keyword",
        "fields": {
          "partial": {
            "type": "text",
            "analyzer": "custom_text_analyzer"
          }
        },
        "store": False

      },
      "CpcClasses": {
        "type": "keyword",
        "store": False

        # "fields": {
        #   "partial": {
        #     "type": "text",
        #     "analyzer": "edge_ngram_analyzer"
        #   }
        # }
      },
      "IpcClasses": {
        "type": "keyword",
          "store": False
        # "fields": {
        #   "partial": {
        #     "type": "text",
        #     "analyzer": "edge_ngram_analyzer"
        #   }
        # }
      },
      "IpcrClasses": {
        "type": "keyword",
          "store": False
        # "fields": {
        #   "partial": {
        #     "type": "text",
        #     "analyzer": "edge_ngram_analyzer"
        #   }
        # }
      },
    "Title": {
        "type": "text",
        "store": False
      },
    "Ucid": {
        "type": "keyword",
        "store": True
      },
    "Description": {
        "type": "text",
        "store": False
      },
    "Abstract": {
        "type": "text",
        "store": False
      },
    "Claims": {
        "type": "text",
        "store": False
      }
    }
  }
}

 

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=settings)
    print(f"Created index: {index_name}")
else:
    print(f"Index {index_name} already exists")


def extract_text_from_markup(abstracts):
    extracted_texts = []
    for abstract in abstracts:
        markup = abstract.get('paragraph_markup', '')
        # Parse the HTML and extract plain text
        soup = BeautifulSoup(markup, 'html.parser')
        extracted_texts.append(soup.get_text().strip())
    return " ".join(extracted_texts)

def extract_classification_levels(classification_code):
    # Extract the primary classification part
    match = re.match(r"([A-Z]\d{2}[A-Z])\s*(\d+)/(\d+)", classification_code)
    if not match:
        return  None
    
    main_class, subclass, group = match.groups()
    subclass_padded = subclass.zfill(4)
    group_padded = group  # Keep group as-is (don't pad with zeros)
    
    
    levels = [
        main_class[0],                 # First letter (section)
        main_class[:3],                # First three characters (subsection)
        main_class,                    # Full main class
        f"{main_class}{subclass_padded}",  # Main class + subclass (4-digit format)
        f"{main_class}{subclass_padded}{group_padded}"  # Full classification with slash
    ]
    
    return  " ".join(levels)

def extract_claims_text(claims_section):
    """
    Extract and clean paragraph_markup content from claims in the given claims_section.
    
    :param claims_section: List containing claims dictionaries.
    :return: List of cleaned claims text.
    """
    claims_text = []
    # Safely access the first element of claims_section and its 'claims' field
    if claims_section and isinstance(claims_section, list) and len(claims_section) > 0:
        claims_data = claims_section[0].get('claims', [])
        for claim in claims_data:
            paragraph_markup = claim.get('paragraph_markup', '')
            if paragraph_markup:
                # Clean the HTML tags using BeautifulSoup
                soup = BeautifulSoup(paragraph_markup, 'html.parser')
                clean_text = soup.get_text().strip()
                claims_text.append(clean_text)
    return " ".join(claims_text)


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

                    abstracts=response_data['abstracts']
                    cleaned_abstracts = extract_text_from_markup(abstracts)
                    claims=response_data['claims']
                    cleaned_claims=extract_claims_text(claims)
                    description_datas=response_data['descriptions']
                    description_datas = extract_text_from_markup(description_datas)
                    icpr_classes=[]
                    cpc_classes=[]
                    ipc_classes=[]
                    for item in response_data["ipcr_classes"]:
                        icpr_classes=extract_classification_levels(item["label"])
                        icpr_classes.append(icpr_classes) 
                    for item in response_data["ipcr_classes"]:
                        icpr_classes=extract_classification_levels(item["label"])
                        cpc_classes.append(icpr_classes) 
                    for item in response_data["ipcr_classes"]:
                        icpr_classes=extract_classification_levels(item["label"])
                        ipc_classes.append(icpr_classes) 
                        
                    doc = {
                        "_index": index_name,
                        "_source": {
                            "Ucid": response_data.get("patent_number", ""),
                            "Title": response_data["titles"][0]['text'],
                            "Abstract": cleaned_abstracts,
                            "Claims": cleaned_claims,
                            "Description": description_datas,
                            "IpcrClasses":icpr_classes,
                            "CpcClasses":cpc_classes,
                            "ipc_classes":ipc_classes
                        }
                    }
                    # print(doc)
                    bulk_data.append(doc)
                    file_count += 1

                    # Index in batches of 500
                    if len(bulk_data) >= 100:
                        helpers.bulk(es, bulk_data)
                        bulk_data = []

    if bulk_data:
        helpers.bulk(es, bulk_data)

    print(f"Successfully indexed {file_count} JSON files from directory: {directory_path}")


main_directory_path = "elastic_search/data_JhtmMcE"
index_json_files_in_directory(main_directory_path, index_name)
# settings = {
#     "settings": {
#         # "number_of_shards": 3,
#         # "number_of_replicas": 1,
#         "analysis": {
#             # "char_filter": {
#             #     "line_break_dot": {
#             #         "type": "pattern_replace",
#             #         "pattern": "\\.\\s",
#             #         "replacement": " .\n"
#             #     }
#             # },
#             "tokenizer": {
#                 "custom_tokenizer": {
#                     "type": "pattern",
#                     # "pattern": "(?<!\\d)\\.(?!\\d)|[\\s\\n]+|[\\(\\)\\[\\]\\{\\}]|[,;:/-]+"
#                     # "pattern": r"(?<!\\d)\\.(?!\\d)|[\\s\\n]+|[\\(\\)\\[\\]\\{\\}]|[,;:/-]+|[!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]+"
#                     # "pattern": "(?<=\\S)\\.(?=\\s)|[\\s\\n]+|[\\(\\)\\[\\]\\{\\}]|[,;:/-!\"#$%&'*+,-./:;\\<=\\>?@^_`|~]+"
#                     "pattern": r"(\.\s)|[\s\t\n]+|[\!\#\$\&\'\\\"(\)\*\+\,/\:;<=>\?@\[\\\]\^\_\`\{\|\}\~]"


#                     # "pattern": re.escape(string.punctuation + " \t\n")
#                 }
#             },
#             "filter": {
#                 "lowercase_filter": {
#                     "type": "lowercase"
#                 },
#                 "stop_filter": {
#                     "type": "stop",
#                     "stopwords": "_english_"
#                 }
#             },
#             "analyzer": {
#                 "custom_analyzer": {
#                     "type": "custom",
#                     # "char_filter": ["line_break_dot"],
#                     "tokenizer": "custom_tokenizer",
#                     "filter": ["lowercase_filter", "stop_filter"]
#                 }
#             }
#         }
#     },
#     "mappings": {
#         "properties": {
#             "content": {
#                 "type": "text",
#                 "analyzer": "custom_analyzer",
#                 "search_analyzer": "custom_analyzer"
#             },
#             "metadata": {
#                 "type": "object",
#                 "enabled": False
#             }
#         }
#     }
# }


# import os
# import json
# from elasticsearch import helpers

# def index_json_files_in_directory(directory_path, index_name):
#     """
#     Index JSON files from a directory into Elasticsearch.

#     :param directory_path: Path to the directory containing JSON files.
#     :param index_name: Elasticsearch index name.
#     :param es: Elasticsearch client instance.
#     """
#     bulk_data = []
#     file_count = 0

#     # Iterate through all files in the directory
#     for file_name in os.listdir(directory_path):
#         if file_name.endswith(".json"):
#             file_path = os.path.join(directory_path, file_name)

#             # Read and parse the JSON file
#             with open(file_path, "r") as file:
#                 try:
#                     response_data = json.load(file)
#                 except json.JSONDecodeError as e:
#                     print(f"Skipping invalid JSON file: {file_path}. Error: {e}")
#                     continue

#             # Process the extracted data
#             abstracts = response_data.get('abstracts', [])
#             cleaned_abstracts = extract_text_from_markup(abstracts)
#             claims = response_data.get('claims', [])
#             cleaned_claims = extract_claims_text(claims)
#             descriptions = response_data.get('descriptions', [])
#             cleaned_descriptions = extract_text_from_markup(descriptions)

#             # Prepare the document for Elasticsearch
#             doc = {
#                 "_index": index_name,
#                 "_source": {
#                     "Ucid": response_data.get("patent_number", ""),
#                     "Title": response_data.get("titles", [{}])[0].get('text', ""),
#                     "Abstract": cleaned_abstracts,
#                     "Claims": cleaned_claims,
#                     "Description": cleaned_descriptions,
#                 }
#             }

#             # Append the document to bulk data
#             bulk_data.append(doc)
#             file_count += 1
#             print(f"Processed file {file_count}: {file_name}")

#             # Bulk index every 100 documents
#             if len(bulk_data) >= 100:
#                 helpers.bulk(es, bulk_data)
#                 print(f"Indexed a batch of 100 documents. Total files processed: {file_count}")

#                 bulk_data = []

#     # Index any remaining documents
#     if bulk_data:
#         helpers.bulk(es, bulk_data)
#         print(f"Indexed the final batch of {len(bulk_data)} documents.")


#     print(f"Successfully indexed {file_count} JSON files from directory: {directory_path}")


# # Example usage
# main_directory_path = "/Users/patdelanalytics/backend-development/elastic_search/data_peGTGZl"
# index_json_files_in_directory(main_directory_path,index_name)


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
