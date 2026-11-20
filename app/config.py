import os

CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen/qwen3.8-27b")
TEMPERATURE = 0.6
MAX_TOKENS = 400

# Số tin nhắn gần nhất giữ lại trong history (tiết kiệm token)
MAX_HISTORY_MESSAGES = 8
