# Hybrid Researcher — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu.

## Danh tính và mục tiêu

- **Tên:** `Hybrid Researcher`
- **Mô tả:** `Fans out across wiki and chunk search at once for a broad overview, then drills in for precise, cited answers`
- **Mục tiêu sử dụng nhìn thấy:** Nghiên cứu kết hợp Wiki và chunk RAG, mở rộng rồi đi sâu vào câu trả lời có trích dẫn.
- **Mode:** `Suy luận thông minh`
- **Preset:** `Kết hợp RAG + Wiki`

## System Prompt, biến và Intent

- Prompt route theo capability của KB, fan-out đồng thời Wiki + semantic chunk + keyword chunk, sau đó bắt buộc deep-read.
- Wiki là bản đồ khái niệm; raw chunk là nền bằng chứng cho quote/number/code.
- Prompt yêu cầu gắn cờ `wiki_flag_issue` nếu Wiki mâu thuẫn nguồn.
- Biến prompt: `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`.
- Prompt theo Intent: `Chọn intent` — không có override Intent được chọn.

## Model và tham số

- **Model:** `qwen3.6-plus`
- **Reranker:** `bge-reranker-v2-m3`
- **Temperature:** `0.7`
- **Extended thinking/reasoning:** Tắt

## Knowledge Base và retrieval

- **Knowledge Base:** `Tất cả kho tri thức`
- **Loại tệp:** `Tất cả loại tệp`
- **Chế độ truy hồi:** Tự động truy hồi.
- **Vector Top K:** `10`
- **Keyword / vector threshold:** `0.3` / `0.5`
- **Rerank Top K / threshold:** `10` / `0.3`

## Tools hiệu lực

- `Tìm Wiki`
- `Đọc trang Wiki`
- `Đọc tài liệu nguồn`
- `Tìm theo ngữ nghĩa`
- `Tìm theo từ khóa`
- `Liệt kê đoạn`
- `Thông tin tài liệu`

Basic tools, SQL/database, product catalog và data analysis/schema không active nhìn thấy.

## Chia sẻ, lifecycle, UX và giới hạn

- **Max steps/loops:** `40`
- **LLM timeout:** `120` giây
- **Parallel tool calls:** Bật
- **Upload ảnh/audio:** Tắt
- **Tab Hội thoại:** Không có
- Có nhãn `Mặc định`; menu `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Share policy, quyền backend, quota/retention và runtime behavior: **Bị chặn–Chưa xác định**.

## Caveat

- **Đã kiểm chứng (static mismatch):** Prompt nhắc `wiki_flag_issue`, nhưng tool này không nằm trong danh sách active của UI.
- **Có điều kiện:** Routing và fan-out Wiki/chunk mới là prompt/config claim; chưa runtime chat-test.
