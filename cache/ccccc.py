import requests
import requests_cache
import time

# Install in-memory cache with expiration
requests_cache.install_cache("my_cache", backend="memory")

# First request
response = requests.get("https://httpbin.org/get")
print("First Response:", response.from_cache)  # Should print False (not from cache)

# Second request within 10 seconds
response = requests.get("https://httpbin.org/get")
print("Second Response:", response.from_cache)  # Should print True (from cache)

# Wait for 10 seconds (cache expires)
time.sleep(10)

# Third request after cache expiry
response = requests.get("https://httpbin.org/get")
print("Third Response:", response.from_cache)  # Should print False (not from cache)
