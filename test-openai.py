import openai
import tiktoken

# Set your OpenAI API key
openai.api_key = ''

# Choose the model (e.g., gpt-3.5-turbo, gpt-4, etc.)
model = "gpt-3.5-turbo"

# Create a function to count tokens using tiktoken
def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.get_encoding("cl100k_base")  # Choose the appropriate tokenizer for the model
    tokens = encoding.encode(text)
    return len(tokens)


# Example chat prompt (a conversation-based model)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Can you explain the principles of quantum mechanics in simple terms?"}
]

# Check token usage for the prompt
prompt_tokens = sum(count_tokens(msg["content"]) for msg in messages)

# Call OpenAI API with the chat endpoint
response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    max_tokens=100  # You can adjust the max_tokens depending on the response length you want
)

# Check token usage for the response
response_tokens = count_tokens(response.choices[0].message["content"], model)

# Calculate total token usage
total_tokens = prompt_tokens + response_tokens

print(f"Prompt Tokens: {prompt_tokens}")
print(f"Response Tokens: {response_tokens}")
print(f"Total Tokens (Prompt + Response): {total_tokens}")

# Access rate limit headers
rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
rate_limit_reset = response.headers.get('X-RateLimit-Reset')

print(f"Rate limit remaining: {rate_limit_remaining}")
print(f"Rate limit resets at: {rate_limit_reset}")


