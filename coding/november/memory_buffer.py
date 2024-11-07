# import io
# buffer=io.BytesIO()
# buffer.write(b"saving data in memory")
# print(len("saving data in memory"))
# buffer.seek(0) #reset pointer at the begining 
# buffer.seek(0,io.SEEK_END)
# buffer.write(b"saving data i")
# buffer.seek(0)
# print(len("yes save data"))
# data=buffer.read()
# print(data.decode('utf-8'))

# print(buffer.read(5))
# my_dict={}
# my_dict['1']="himanshu singh"
# print(my_dict)

import pickle,json

# Example dictionary
my_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "skills": ["Python", "Data Science", "Machine Learning"]
}

# Serialize the dictionary using pickle (convert it into a byte stream)
serialized_data = pickle.dumps(my_dict)
print(json.dumps(my_dict),type(json.dumps(my_dict)))

# Check the serialized data (this is just a byte stream)
print("Serialized data (byte stream):", serialized_data)

