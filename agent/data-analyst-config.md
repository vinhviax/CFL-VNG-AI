# Data Analyst — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu.

## Danh tính và mục tiêu

- **Tên:** `Data Analyst`
- **Mô tả:** `Professional data analysis agent with SQL query and statistical analysis for CSV/Excel files`
- **Mục tiêu sử dụng nhìn thấy:** Phân tích dữ liệu CSV/Excel bằng schema, SQL và thống kê.
- **Mode:** `Suy luận thông minh`
- **Preset:** `Phân tích dữ liệu`

## System Prompt, biến và Intent

- Prompt định hướng dùng DuckDB.
- Bắt buộc lấy `data_schema` trước khi viết SQL.
- Chỉ cho phép câu lệnh `SELECT`; cấm `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`.
- Có vòng lặp sửa lỗi query và trả insight/kết quả dạng bảng.
- Biến prompt: `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`.
- Prompt theo Intent: `Chọn intent` — không có override Intent được chọn.

## Model và tham số

- **Model:** `gpt-5.4-mini`
- **Reranker:** `bge-reranker-v2-m3`
- **Temperature:** `0.3`
- **Extended thinking/reasoning:** Tắt

## Knowledge Base và retrieval

- **Knowledge Base:** `Tất cả kho tri thức`
- **Loại tệp:** Chỉ `CSV`, `XLSX`
- **Chế độ truy hồi:** Tự động truy hồi.
- **Vector Top K:** `5`
- **Keyword / vector threshold:** `0.3` / `0.5`
- **Rerank Top K / threshold:** `5` / `0.3`

## Tools hiệu lực

- `Lược đồ dữ liệu`
- `Phân tích dữ liệu`

SQL chạy bên trong luồng Data Analysis; không có database query trực tiếp. RAG chunk, Wiki, product catalog và basic tools không active nhìn thấy.

## Chia sẻ, lifecycle, UX và giới hạn

- **Max steps/loops:** `30`
- **LLM timeout:** `120` giây
- **Parallel tool calls:** Tắt
- **Upload ảnh/audio:** Tắt
- **Tab Hội thoại:** Không có
- Có nhãn `Mặc định`; menu `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Share policy, quyền backend, quota/retention và runtime behavior: **Bị chặn–Chưa xác định**.

Không thực hiện query dữ liệu hay chat-test trong audit này.
