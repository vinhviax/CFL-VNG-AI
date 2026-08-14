# FPA Analyst — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu.

## Danh tính và mục tiêu

- **Tên:** `FPA Analyst`
- **Mô tả:** `Fixed pipeline: works out what the question is about, routes to the sources that cover it, then retrieves. Copy it to configure your own models.`
- **Mục tiêu sử dụng nhìn thấy:** Báo cáo/phân tích hiệu suất theo pipeline FPA.
- **Mode:** `Quy trình`
- **Các bước:** Tab `Các bước` ghi workflow cố định `fpa`, không sửa được tại đây.

## System Prompt, biến và Intent

- Prompt nói pipeline đã hiểu câu hỏi và scope nguồn trước khi truy hồi.
- Yêu cầu chỉ trả lời từ nội dung đã truy hồi, ghi chính xác số liệu/kỳ/đơn vị, không coi missing là zero và truy vấn source inventory khi người dùng hỏi về nguồn.
- Biến prompt: `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`.
- Prompt theo Intent: `Chọn intent` — không có override Intent được chọn.

## Model và tham số

- **Model:** `qwen3.6-plus`
- **Reranker:** `bge-reranker-v2-m3`
- **Temperature:** `0.7`
- **Extended thinking/reasoning:** Bật

## Knowledge Base và retrieval

- **Knowledge Base trên UI:** `Tất cả kho tri thức`
- **Loại tệp:** `Tất cả loại tệp`
- **Chế độ truy hồi:** Tự động truy hồi.
- **Vector Top K:** `10`
- **Keyword / vector threshold:** `0.3` / `0.3`
- **Rerank Top K / threshold:** `10` / `0.3`

## Tools hiệu lực

- `Danh mục sản phẩm`
- `Hỏi người dùng`
- `Tìm theo ngữ nghĩa`
- `Tìm theo từ khóa`
- `Liệt kê đoạn`
- `Thông tin tài liệu`
- `Truy vấn CSDL`

Wiki, data analysis/schema và basic thinking/todo không active nhìn thấy.

## Chia sẻ, lifecycle, UX và giới hạn

- **Max steps/loops:** `10`
- **LLM timeout:** `180` giây
- **Parallel tool calls:** Tắt
- **Upload ảnh/audio:** Tắt
- **Tab Hội thoại:** Không có
- Có nhãn `Mặc định`; menu `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Share policy, quyền backend, quota/retention và runtime behavior: **Bị chặn–Chưa xác định**.

## Caveat

- **Có điều kiện:** Prompt nói pipeline đã scope nguồn, nhưng UI vẫn để `Tất cả kho tri thức`. Chỉ runtime test mới chứng minh scope thực tế.
- Không thực hiện truy vấn CSDL, chat-test hoặc thao tác mutation.
