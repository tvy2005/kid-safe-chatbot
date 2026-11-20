"""Guardrails: để trống ở Phần A. Phần B sẽ cài đặt:
- input_filter: keyword/regex + LLM classifier
- output_filter: LLM-as-judge
Mỗi hàm trả về (ok: bool, reason: str).
"""


def input_filter(user_text: str):
    return True, ""


def output_filter(bot_text: str):
    return True, ""
