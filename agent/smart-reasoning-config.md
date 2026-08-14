# Smart Reasoning — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu.

## Danh tính và mục tiêu

- **Tên:** `Smart Reasoning`
- **Mô tả:** `ReAct reasoning framework with multi-step thinking and tool calling`
- **Mục tiêu sử dụng nhìn thấy:** Suy luận nhiều bước và gọi công cụ cho hỏi đáp RAG có bằng chứng.
- **Mode:** `Suy luận thông minh`
- **Preset:** `Hỏi đáp RAG`

## System Prompt, biến và Intent

- System prompt là Progressive Agentic RAG, Evidence-First.
- Yêu cầu fresh retrieval cho câu hỏi mới, fan-out tìm kiếm semantic và keyword, đọc full chunk/FAQ trước khi trả lời và có thể lập kế hoạch cho tác vụ phức tạp.
- Prompt nêu không fallback sang general knowledge khi KB không có bằng chứng.
- Biến prompt: `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`.
- Prompt theo Intent: `Chọn intent` — không có override Intent được chọn.

## Model và tham số

- **Model:** `gpt-5.4-mini`
- **Reranker:** `bge-reranker-v2-m3`
- **Temperature:** `0.7`
- **Extended thinking/reasoning:** Tắt
- **Max generation token:** UI không hiển thị trong mode này.

## Knowledge Base và retrieval

- **Knowledge Base:** `Tất cả kho tri thức`
- **Loại tệp:** `Tất cả loại tệp`
- **Chế độ truy hồi:** Tự động truy hồi.
- **Vector Top K:** `10`
- **Keyword / vector threshold:** `0.3` / `0.5`
- **Rerank Top K / threshold:** `10` / `0.3`

## Tools hiệu lực

- `Tìm theo ngữ nghĩa`
- `Tìm theo từ khóa`
- `Liệt kê đoạn`
- `Thông tin tài liệu`

Wiki, SQL/database query, product catalog, data analysis/schema và basic tools không nằm trong danh sách active nhìn thấy.

## Chia sẻ, lifecycle, UX và giới hạn

- **Max steps/loops:** `50`
- **LLM timeout:** `120` giây
- **Parallel tool calls:** Tắt
- **Upload ảnh/audio:** Tắt
- **Tab Hội thoại:** Không có
- Có nhãn `Mặc định`; menu `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Share policy, quyền backend, quota/retention và runtime behavior: **Bị chặn–Chưa xác định**.

Không thực hiện thao tác mutation hoặc chat-test.
