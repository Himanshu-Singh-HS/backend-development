import pysolr
import json
# python -m src.monolith.landscaping.testing1   to run this command in betamonolith

SOLR_URL = 'http://localhost:8983/solr/saved_data'   
solr = pysolr.Solr(SOLR_URL, always_commit=True) 

# Example Document to add
documents = [
    # {
    #     "id": "1",
    #     "name": "Example Document 1",
    #     "category": "Category A",
    #     "description": "This is a description for the first document."
    # },
    # {
    #     "id": "2",
    #     "name": "Example Document 2",
    #     "category": "Category B",
    #     "description": "This is a description for the second document."
    # },
     {
        "id": "24",
        "name": "Example Document 24",
        "category": "Category B",
        "description": "This is a description for the himanshu singh."
    }
]

# Adding documents to Solr
def add_documents_to_solr():
    try:
        solr.add(documents)
        print("Documents added successfully!")
    except Exception as e:
        print(f"Error adding documents: {e}")

# Query Solr
def search_solr(query):
    try:
        results = solr.search(query)
        print(f"Found {len(results)} results")
        for result in results:
            print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error querying Solr: {e}")

# Add documents to Solr
add_documents_to_solr()

# Search Solr for documents with name "Example Document"
# search_query = "name:Example"
search_query="*:*"
search_solr(search_query)


####
