import time

from app import config
from app.guardrails import input_filter, output_filter
from app.llm import chat
from app.prompts import FALLBACK_MESSAGE, SYSTEM_PROMPT


def respond(history, user_text):
    """
    history: list[{"role": "user"|"assistant", "content": str}]
    Trả về (reply, meta). meta ghi lại lớp nào chặn, lý do, latency
    -> dùng trực tiếp khi chạy eval ở Phần D.
    """
    t0 = time.time()

    ok, reason = input_filter(user_text)
    if not ok:
        return FALLBACK_MESSAGE, _meta("input", reason, t0, raw=None)

    trimmed = history[-config.MAX_HISTORY_MESSAGES:]
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + trimmed
        + [{"role": "user", "content": user_text}]
    )
    answer = chat(messages)

    ok, reason = output_filter(answer)
    if not ok:
        # raw giữ lại câu bị chặn để phân tích lỗi sau này
        return FALLBACK_MESSAGE, _meta("output", reason, t0, raw=answer)

    return answer, _meta(None, "", t0, raw=answer)


def _meta(blocked_by, reason, t0, raw):
    return {
        "blocked_by": blocked_by,
        "reason": reason,
        "latency_s": round(time.time() - t0, 2),
        "raw_answer": raw,
    }
