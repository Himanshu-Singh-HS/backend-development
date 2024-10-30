from pymongo import MongoClient

# Define the MongoDB URI and create a client connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)

# Define the database
database = client["your_database"]

# Define the collection
collection = database["your_collection"]

# Define a document (in Python, this is a dictionary)
document = {
    "name": "Alice",
    "age": 22,
    "course": "Computer Science"
}

# Insert the document into the collection
result = collection.insert_one(document)
print(f"Inserted document with ID: {result.inserted_id}")

# Retrieve all documents from the collection
for doc in collection.find({}):
    print(doc)
