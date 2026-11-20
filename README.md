# Kid-safe Multilingual Chatbot (WIP)

Chatbot thú bông "Bông" cho trẻ 5-8 tuổi, có guardrails và đánh giá an toàn đa ngôn ngữ.

## Phạm vi
- **Persona:** Bông, gấu bông thân thiện. **Đối tượng:** trẻ 5-8 tuổi.
- **Được làm:** trả lời câu hỏi tò mò, kể chuyện ngắn, đố vui.
- **Không được làm:** bạo lực, tình dục, ma túy, tự hại, hỏi/lưu thông tin cá nhân,
  giữ bí mật với bố mẹ, thoát persona.
- **Khi trẻ nói điều đáng lo:** đáp ấm áp, khuyên nói với người lớn tin cậy.

## Chạy thử
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
python run_manual_tests.py   # chạy bộ test thủ công
```

## Kiến trúc
`input_filter -> LLM (system prompt) -> output_filter -> reply / fallback`

## Roadmap
- [x] A. Chatbot cơ bản + pipeline có chỗ cắm filter
- [ ] B. Guardrails (input/output)
- [ ] C. Đa ngôn ngữ
- [ ] D. Bộ evaluation
- [ ] E. Demo + báo cáo kết quả
