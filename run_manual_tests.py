"""Chạy toàn bộ tests/manual_prompts.txt và xuất results/manual_test_results.md
để bạn đọc và ghi nhận xét (tốt / chưa tốt / vì sao). Đây là hạt giống cho bộ eval."""
from pathlib import Path

from app.pipeline import respond

SRC = Path("tests/manual_prompts.txt")
OUT = Path("results/manual_test_results.md")


def main():
    rows = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        category, prompt = [p.strip() for p in line.split("|", 1)]
        reply, meta = respond([], prompt)
        rows.append((category, prompt, reply, meta["blocked_by"], meta["latency_s"]))
        print(f"[{category}] {prompt}\n  -> {reply}\n")

    lines = [
        "| # | Nhóm | Prompt | Trả lời | Chặn bởi | Latency | Nhận xét của bạn |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, (c, p, r, b, t) in enumerate(rows, 1):
        r = r.replace("\n", " ").replace("|", "/")
        lines.append(f"| {i} | {c} | {p} | {r} | {b or '-'} | {t}s |  |")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Đã ghi {OUT}")


if __name__ == "__main__":
    main()
