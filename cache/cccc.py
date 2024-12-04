import requests
import requests_cache

# Install cache with memory backend and enable caching for POST requests
requests_cache.install_cache(
    "my_cache",
    backend="memory",
    expire_after=60,
    allowable_methods=["GET", "POST"],  # Allow POST requests to be cached
    cache_control=True,  # Honor Cache-Control headers
    include_get_headers=True,  # Include headers in cache key
)
def cached_api():
    url = "https://beta.patdelanalytics.ai/api/v1/summarizer/generate_summary?dummy_data=false"

    payload = {
        "ucids": [
            "US-10977293-B2"
        ]
    }
    print(f"{payload=}")
    # Fetch response using requests
    response = requests.post(url, json=payload)

    # Determine the data source
    if response.from_cache:
        source = "Cache"
    else:
        source = "API"

    print(f"Data Source: {source}")

    # Return the API data along with its source
    return {"source": source, "data": response.json()}

# Test the caching behavior
output1 = cached_api()
output2 = cached_api()
output2 = cached_api()
output2 = cached_api()

# Print results
print("Output 1:", output1)
print("Output 2:", output2)
