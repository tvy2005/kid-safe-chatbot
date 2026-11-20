import os
from dotenv import load_dotenv
from groq import Groq

from app import config

load_dotenv()
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat(messages, model=None, temperature=None, max_tokens=None):
    """Gọi Groq và trả về text. Tách riêng để sau này dễ thay model / đo latency."""
    resp = _client.chat.completions.create(
        model=model or config.CHAT_MODEL,
        messages=messages,
        temperature=config.TEMPERATURE if temperature is None else temperature,
        max_tokens=max_tokens or config.MAX_TOKENS,
    )
    return resp.choices[0].message.content.strip()
