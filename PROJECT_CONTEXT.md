# Project Knowledge: Kid-safe Multilingual Chatbot

## 1. Mục tiêu & Công nghệ
- **Mục tiêu dự án:** Xây dựng chatbot thú bông **Bông** dành cho trẻ 5–8 tuổi. Chatbot trả lời các câu hỏi tò mò phù hợp, kể chuyện ngắn và chơi đố vui; đồng thời cần tránh nội dung bạo lực, tình dục, ma túy, vũ khí, tự hại và việc thu thập thông tin cá nhân. Khi trẻ buồn, sợ hoặc bị làm hại, Bông cần phản hồi ấm áp và khuyên trẻ tìm người lớn đáng tin cậy, có input/output filter, fallback, đa ngôn ngữ (Việt, Anh, +1), bộ eval 100-150 prompt, demo deploy.
- **Công nghệ:** Python, Groq API (`qwen/qwen3.8-27b`, temp 0.6, max_tokens 400), `python-dotenv`; sau này Streamlit + Hugging Face Spaces/Streamlit Cloud.

## 2. Cấu trúc hiện tại

```text
main.py # chat terminal, giữ 6-10 lượt history
requirements.txt        # groq, python-dotenv
.env
app/
  config.py              # model, temperature, max tokens, history limit
  guardrails.py          # input/output filter (hiện trống)
  llm.py                # wrapper gọi Groq
  pipeline.py            # input_filter -> LLM -> output_filter (filter hiện là stub)
  prompts.py            # persona, system prompt (v1), fallback
eval/ # (trống, làm ở Phần D)
tests/manual_prompts.txt
run_manual_tests.py     # chạy prompt và ghi kết quả
results/manual_test_results.md
README.md
```

- **Dữ liệu:** bảng manual test v1 (23 ca: normal, sensitive, gray_area, emotion, personal_info, attack) với cột Latency (~0.3s), "Chặn bởi", Nhận xét (người dùng chưa điền).

## 3. Quy ước & Quyết định đã chốt

- Persona: Bông; đối tượng 5-8 tuổi; được làm: trả lời tò mò, kể chuyện, đố vui; không được: bạo lực, tình dục, ma túy, vũ khí, hỏi/lưu thông tin cá nhân, giữ bí mật với bố mẹ, rời persona.
- System prompt chia khối: Voice / What you do / Safety rules / Language. Dùng ràng buộc đo được (câu ≤15 từ, 2-4 câu, ≤1 emoji).
- `respond()` luôn trả kèm **metadata** (`blocked_by`, `reason`) để phục vụ eval.
- System prompt chỉ là lớp 1, không đủ; guardrail 2 lớp: rule/keyword rồi LLM classifier (input), LLM-as-judge (output).
- Eval: gán nhãn kỳ vọng (nên trả lời / chuyển hướng / chặn) bằng tay; đo tỷ lệ chặn đúng, **chặn nhầm**, nhất quán giữa ngôn ngữ, độ trễ/chi phí; mỗi prompt chạy 3-5 lần; thêm ca đa lượt.
- **Quyết định sẽ áp dụng ở prompt v2 (từ phản hồi test):**
  - Xưng hô tiếng Việt nhất quán (Bông xưng "Bông", gọi trẻ là "bạn").
  - Gọi đúng cảm xúc trẻ nói (sợ ≠ buồn), không giảm nhẹ, rồi nhẹ nhàng hướng về người lớn.
  - Fallback thống nhất: "đây là chuyện của người lớn / hỏi bố mẹ", không nói "Bông không biết".
  - Không mở đầu mọi câu bằng lời chào.
  - Dùng "thông tin riêng tư", không dùng "bí mật".
  - Cần chính sách rõ cho chủ đề nhạy cảm nhẹ (sinh sản, cái chết, chiến tranh) vì hiện đang không nhất quán.
  - Ca trẻ tiết lộ nguy hiểm nghiêm trọng (bị đánh, tự hại) cần phản hồi riêng, không để LLM tự do.


## 4. Tiến độ & Bước tiếp theo

- Đã hoàn thành khung chatbot CLI, persona, system prompt, Groq wrapper và pipeline có metadata/đo latency.
- Đã có 23 prompt thủ công thuộc các nhóm bình thường, nhạy cảm, vùng xám, cảm xúc, thông tin cá nhân và tấn công prompt.
- Đã chạy và lưu kết quả mẫu tại `results/manual_test_results.md`; phản hồi nhìn chung đúng persona và an toàn theo system prompt.
- Phát hiện chính: prompt chống được tấn công đơn giản, yếu ở **cảm xúc** (câu 14, 15) và **tính nhất quán**.
- **Đang dừng ở:** chuẩn bị sửa prompt v2 và chạy lại test.
- **Làm ngay:**
  1. Điền cột Nhận xét + nhãn kỳ vọng (nên trả lời / nên chuyển hướng / nên chặn) cho 23 ca.
  2. Viết prompt v2 theo mục 3, chạy lại 23 ca, lập bảng v1 vs v2.
  3. Thêm ~15 ca mới: 5 tấn công nâng cao (đóng vai, story, đa ngôn ngữ, đa lượt), 5 cảm xúc/nguy hiểm nghiêm trọng, 5 vùng xám.
  4. Gửi lại prompt v2 + kết quả để sang **Phần B: guardrails**.
- **Phía sau:** Phần C đa ngôn ngữ (ngày 6-8), Phần D eval (9-11), Phần E đóng gói + deploy (12-14).
