import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Get command line argument for API provider
if len(sys.argv) > 1:
    provider = sys.argv[1].lower()
else:
    provider = "vveai"  # default

# Set environment variable names based on provider
if provider == "openai":
    api_key_env = 'OPENAI_API_KEY'
    base_url_env = 'OPENAI_API_BASE'
elif provider == "vveai":
    api_key_env = 'VVEAI_API_KEY'
    base_url_env = 'VVEAI_API_BASE'
else:
    print(f"Error: Unsupported provider '{provider}'. Use 'openai' or 'vveai'.")
    sys.exit(1)

# Get API credentials from environment
api_key = os.getenv(api_key_env)
base_url = os.getenv(base_url_env)

if not api_key:
    print(f"Error: {api_key_env} environment variable not found.")
    sys.exit(1)

print(f"-- debug -- using {provider} provider's urlq {base_url}")
print(f"-- debug -- {provider} api key is {api_key[0:10]}******")

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)


response = client.chat.completions.create(
    model="o3-mini",
    messages=[
        {"role": "user", "content": "Hello world!"}
    ]
)

print(response.choices[0].message.content)


# 正常会输出结果：Hello! It's great to see you. How can I assist you today?