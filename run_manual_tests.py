"""Chạy toàn bộ tests/manual_prompts.txt và xuất results/manual_test_results.md
để đọc và ghi nhận xét (tốt / chưa tốt / vì sao). Đây là hạt giống cho bộ eval."""
import json
from pathlib import Path

from app.pipeline import respond
from app.prompts import FALLBACK_MESSAGE, PROMPT_VERSION

SRC = Path("tests/manual_prompts.txt")
OUT = Path(f"results/manual_test_results_{PROMPT_VERSION}.md")
OUT_JSON = Path(f"results/results_{PROMPT_VERSION}.json")
LABELS = {"ANSWER", "REDIRECT", "BLOCK"}


def auto_flag(label, blocked_by, reply):
    fb = blocked_by is not None or reply == FALLBACK_MESSAGE
    if label == "ANSWER" and fb:
        return "CHẶN NHẦM"
    if label == "BLOCK" and not fb:
        return "kiểm tra tay"  # model có thể đã từ chối đúng bằng lời của nó
    return "-"

def main():
    rows = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        category, label, prompt = [p.strip() for p in line.split("|", 2)]
        assert label in LABELS, f"Nhãn sai: {line}"
        turns = [t.strip() for t in prompt.split(";;")]

        history = []
        for t in turns[:-1]:  # các lượt trước chỉ để dựng history
            r, _ = respond(history, t)
            history += [{"role": "user", "content": t}, {"role": "assistant", "content": r}]
        reply, meta = respond(history, turns[-1])

        rows.append({
            "category": category, "label": label, "prompt": prompt,
            "reply": reply, "blocked_by": meta["blocked_by"],
            "latency": meta["latency_s"],
            "flag": auto_flag(label, meta["blocked_by"], reply),
        })
        print(f"[{category}/{label}] {prompt}\n  -> {reply}\n")

    lines = [
        "| # | Nhóm | Nhãn | Prompt | Trả lời | Chặn bởi | Latency | Cờ tự động | Nhận xét của bạn |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        rep = r["reply"].replace("\n", " ").replace("|", "/")
        pr = r["prompt"].replace("|", "/")
        lines.append(f"| {i} | {r['category']} | {r['label']} | {pr} | {rep} | "
                     f"{r['blocked_by'] or '-'} | {r['latency']}s | {r['flag']} |  |")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Đã ghi {OUT}")


if __name__ == "__main__":
    main()
