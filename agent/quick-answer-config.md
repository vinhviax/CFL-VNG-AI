# Quick Answer — cấu hình Agent mặc định

**Trạng thái:** Audit chỉ-đọc UI, ngày 14/08/2026  
**Nguồn:** `https://vnggames.ai/kb/agents` trên trình duyệt tích hợp Codex  
**Phân loại:** Mọi trường bên dưới là **Đã kiểm chứng** từ UI, trừ mục được đánh dấu **Có điều kiện** hoặc **Bị chặn–Chưa xác định**.

## Danh tính và mục tiêu

- **Tên:** `Quick Answer`
- **Mô tả:** `Knowledge base RAG Q&A for fast and accurate answers`
- **Mục tiêu sử dụng nhìn thấy:** Trả lời nhanh dựa trên truy hồi Knowledge Base.
- **Mode:** `Trả lời nhanh`
- **Preset:** Không có preset smart-reasoning hiển thị.

## System Prompt, biến và Intent

- System prompt định vị Agent là trợ lý hỏi đáp dựa trên thông tin đã truy hồi; yêu cầu không dùng prior knowledge, giữ nguyên marker/link ảnh từ context, trả lời Markdown theo `{{language}}` và báo rõ khi không tìm thấy.
- Context runtime được mô tả là metadata, gồm `{{current_time}}`, `{{current_week}}`, `{{query}}`.
- Biến prompt nhìn thấy: `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`.
- Prompt theo Intent: `Chọn intent` — không có override Intent được chọn.
- Classifier viết lại hội thoại có các nhãn: `greeting`, `summarize`, `kb_search`, `clarification`, `follow_up`, `image_only`, `doc_only`, `chitchat`; mặc định `kb_search`.
- Prompt rewrite yêu cầu JSON gồm `rewrite_query`, `intent`, `image_description`.

## Model và tham số

- **Model:** `gpt-5.4-mini`
- **Reranker:** `bge-reranker-v2-m3`
- **Temperature:** `0.7`
- **Max output tokens:** `0` (UI giải thích là không giới hạn)
- **Extended thinking/reasoning:** Tắt

## Knowledge Base và retrieval

- **Knowledge Base:** `Tất cả kho tri thức`
- **Loại tệp:** `Tất cả loại tệp`
- **Chế độ truy hồi:** Tự động truy hồi; `Chỉ truy hồi khi được nhắc` tắt.
- **Query expansion:** Bật
- **Vector Top K:** `10`
- **Keyword threshold:** `0.3`
- **Vector threshold:** `0.5`
- **Rerank Top K / threshold:** `10` / `0.3`
- **Phân tích bảng dữ liệu:** Tắt
- **Fallback:** `Mô hình tự sinh`.

## Tools, multimodal và hội thoại

- **Tab Tools:** Không có tab Tools hiển thị.
- **Upload ảnh:** Tắt
- **Upload audio/ASR:** Tắt
- **Multi-turn:** Bật; giữ lịch sử `5` lượt.
- **Query rewrite:** Bật; model hiểu truy vấn để trống, tức dùng model chat chính.

## Chia sẻ, lifecycle, UX và giới hạn

- Có nhãn `Mặc định`; menu UI hiển thị `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`.
- Không có panel Share hiển thị; quyền public/private, người được dùng/sửa và khả năng thực thi thật của menu là **Bị chặn–Chưa xác định**.
- Quota tenant, retention và giới hạn backend thực tế không hiển thị: **Bị chặn–Chưa xác định**.

## Caveat

- **Có điều kiện:** System prompt chính yêu cầu chỉ dùng context truy hồi, nhưng fallback prompt cho phép dùng general knowledge khi danh sách tài liệu rỗng. Chưa chat-test nên hành vi runtime chưa xác định.
- Không gọi private API, không đọc cookie/storage/session và không thực hiện Save/Chat/Clone/Disable/Delete.
