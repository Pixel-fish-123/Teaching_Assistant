import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise SystemExit("DEEPSEEK_API_KEY is not set")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)

response = client.chat.completions.create(
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
    messages = [{"role": "user", "content": "Reply with exactly: pong"}],
    temperature = 0,
    max_tokens = 200,
)

print(response.choices[0].message.content)
print("usage:", response.usage)
