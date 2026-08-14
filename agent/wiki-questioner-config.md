# Wiki Questioner — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu.

## Danh tính và mục tiêu

- **Tên:** `Wiki Questioner`
- **Mô tả:** `Specialized agent for answering questions based on Wiki knowledge bases`
- **Mục tiêu sử dụng nhìn thấy:** Hỏi đáp chuyên biệt trên Wiki Knowledge Base.
- **Mode:** `Suy luận thông minh`
- **Preset:** `Hỏi đáp Wiki`

## System Prompt, biến và Intent

- Workflow Search–Read–Expand cho Wiki.
- Dùng `index` cho overview, `log` cho timeline/lịch sử, đọc trang Wiki trước khi trả lời, theo link 1–2 hop và chỉ đọc source document khi Wiki thiếu quote/raw data.
- Prompt cho phép MCP ngoài chỉ khi được expose, nhưng Wiki vẫn là nguồn chính.
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

RAG chunk, SQL/database, product catalog, data analysis/schema và basic tools không active nhìn thấy.

## Chia sẻ, lifecycle, UX và giới hạn

- **Max steps/loops:** `30`
- **LLM timeout:** `120` giây
- **Parallel tool calls:** Tắt
- **Upload ảnh/audio:** Tắt
- **Tab Hội thoại:** Không có
- Có nhãn `Mặc định`; menu `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Share policy, quyền backend, quota/retention và runtime behavior: **Bị chặn–Chưa xác định**.

## Caveat

- **Đã kiểm chứng (static mismatch):** Prompt nhắc `wiki_flag_issue`, nhưng UI không liệt kê tool này là active.
- **Bị chặn–Chưa xác định:** UI không xác nhận MCP external tool nào đang active.
