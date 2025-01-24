import json

# Serialization: Converting a dictionary (or other data structure) into a JSON string.
# Deserialization: Converting a JSON string back into a dictionary (or similar object in another language).
# Serialization (dumps): Converting a Python object (like a dictionary) into a JSON string.
# Deserialization (loads): Converting a JSON string back into a Python object (like a dictionary).


# Python dictionary   #seralization in python 
my_dict = {"name": "John", "age": 30, "city": "New York"}
print(type(my_dict))
# Convert dictionary to JSON string
json_string = json.dumps(my_dict)
print(json_string,type(json_string))  #  here why not priting in string 

#deseralization in python 

# JSON string
json_string = '{"name": "John", "age": 30, "city": "New York"}'
print(type(json_string))
# Convert JSON string to dictionary
my_dict = json.loads(json_string)
print(my_dict,type(my_dict))


print("himnahusbdndr")


# The reason you don’t see the outer quotes printed when you use print(json_string) is because Python doesn’t print the quotes of a string when you use print(). It just prints the content of the string itseyoutulf.

# In both cases (manual JSON string and the string produced by json.dumps()), the printed result will look like JSON without the surrounding quotes, because that’s what a string’s value is when printed in Python.

