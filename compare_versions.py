import json
from pathlib import Path

a = json.loads(Path("results/results_v1.json").read_text(encoding="utf-8"))
b = json.loads(Path("results/results_v2.json").read_text(encoding="utf-8"))

def cell(r):
    return r["reply"].replace("\n", " ").replace("|", "/") + f" `[{r['flag']}]`"

lines = ["| # | Nhóm | Nhãn | Prompt | v1 | v2 | Nhận xét |", "|---|---|---|---|---|---|---|"]
for i, (x, y) in enumerate(zip(a, b), 1):
    p = x["prompt"].replace("|", "/")
    lines.append(f"| {i} | {x['category']} | {x['label']} | {p} | {cell(x)} | {cell(y)} |  |")
Path("results/compare_v1_v2.md").write_text("\n".join(lines), encoding="utf-8")