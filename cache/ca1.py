# from functools import lru_cache

# @lru_cache(maxsize=128)
# def get_data_from_api(param):
#     # Simulate an expensive operation
#     print("Fetching data...")
#     return f"Data for {param}"

# # Example usage
# print(get_data_from_api("test"))  # Fetches data
# print(get_data_from_api("test"))  # Uses cache

# import requests
# import requests_cache
# from fastapi import FastAPI

# requests_cache.install_cache("my_cache", backend="memory", expire_after=60)
# app = FastAPI()

# @app.get("/cached-api")
# def cached_api():
#     url = "https://jsonplaceholder.typicode.com/posts"
#     response = requests.get(url)
#     print("eee",response)

#     # This will use the cached data if available
#     return {"data": response.json()}
# cached_api()
# print("hfhfh")


import requests
import requests_cache
from fastapi import FastAPI

 
# requests_cache.install_cache("my_cache", backend="memory", expire_after=60)
requests_cache.install_cache(
    "my_cache",
    backend="memory",
    expire_after=60,
    allowable_methods=["GET", "POST"],  # Allow POST requests to be cached
    # cache_control=True,  # Honor Cache-Control headers
    # include_get_headers=True,  # Include headers in cache key
)

def cached_api():
    url = "https://beta.patdelanalytics.ai/api/v1/summarizer/generate_summary?dummy_data=false"

    payload = {
        "ucids": [
            "US-10977293-B2"
        ]
    }

    # Fetch response using requests
    response = requests.post(url,json=payload)

    # Check if the response came from the cache
    if response.from_cache:
        print("Cache Hit: Data was fetched from the cache.")
    else:
        print("Cache Miss: Data was fetched from the API.")

    # Return the API data

    return {"data": response.json()}

 
output1=cached_api()
output2=cached_api()
output3=cached_api()
output4=cached_api()
output5=cached_api()
output6=cached_api()
print("output1",output1)
print("\n")
print("output2",output2)
print("output1",output3)
print("\n")
print("output2",output4)

print("output1",output5)
print("\n")
print("output2",output6)

 
print("Cache check complete.")
