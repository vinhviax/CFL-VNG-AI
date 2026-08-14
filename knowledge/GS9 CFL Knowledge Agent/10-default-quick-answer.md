# Default Agent — Quick Answer

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho behavior  
**Nguồn chính:** `SRC-D-QUICK`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Cần câu trả lời nhanh từ nội dung KB và không cần tool orchestration nhiều bước.
- Có thể kiểm tra lại source và chấp nhận giới hạn của mode Fast Answer.

## Không dùng khi

- Công việc nhạy cảm cần KB allowlist hoặc least privilege; Agent đang chọn All KB.
- Câu trả lời không được phép fallback sang general knowledge.
- Cần Wiki, SQL, Data Analysis, Catalog hoặc action tool.

## Mục đích và đầu ra dự kiến

Mô tả UI: `Knowledge base RAG Q&A for fast and accurate answers`. Prompt định vị Agent là trợ lý hỏi đáp theo context truy hồi, giữ marker/link ảnh, trả Markdown theo `{{language}}` và báo khi không tìm thấy.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / preset | `Trả lời nhanh`; không có Smart preset |
| Model / reranker | `gpt-5.4-mini` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.7` / Off |
| Max output tokens | `0` — UI giải thích không giới hạn |
| KB / file type | `Tất cả kho tri thức` / `Tất cả loại tệp` |
| Retrieval | Tự động; `Chỉ truy hồi khi được nhắc` Off |
| Query expansion | On |
| Vector Top K | `10` |
| Keyword / vector threshold | `0.3` / `0.5` |
| Rerank Top K / threshold | `10` / `0.3` |
| Table data analysis | Off |
| Fallback | `Mô hình tự sinh` |
| Image / audio | Off / Off |
| Multi-turn / history | On / `5` lượt |
| Query rewrite | On; dùng model chat chính nếu rewrite model để trống |

**Nguồn:** `SRC-D-QUICK`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Intent và prompt variables

- Biến nhìn thấy: `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`.
- Không có per-intent prompt override được chọn.
- Rewrite classifier có: `greeting`, `summarize`, `kb_search`, `clarification`, `follow_up`, `image_only`, `doc_only`, `chitchat`; default `kb_search`.
- Rewrite output là JSON gồm rewritten query, intent và image description.

## Tools và quyền

Không có tab Tools. Việc menu có `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt` không chứng minh user hiện tại có quyền thực thi hoặc Agent được share thế nào.

## Caveat quan trọng

**Đã kiểm chứng — static conflict:** System Prompt nói không dùng prior knowledge, nhưng fallback prompt cho phép general knowledge khi document listing rỗng. Vì chưa chat-test, không biết nhánh nào thắng trong runtime.

## Cách dùng an toàn

1. Không nhập dữ liệu nhạy cảm khi Agent vẫn All KB.
2. Nêu rõ phạm vi và thời điểm trong câu hỏi.
3. Mở nguồn và kiểm chứng fact quan trọng; không dựa vào fluency.
4. Với no-hit, không chấp nhận câu trả lời không nguồn cho quyết định vận hành.
5. Dùng [Smart Reasoning](11-default-smart-reasoning.md) nếu cần evidence-first nhiều bước, nhưng vẫn phải kiểm tra All KB.

## Runtime evidence và giới hạn

**Bị chặn–Chưa xác định:** grounding thực tế, citation, image rendering, ACL/share, quota, retention, latency, model availability và behavior fallback.

## Nguồn

- `agent/quick-answer-config.md` — per-Agent config snapshot.
- `audit/default-agent-readonly-audit-2026-08-14.md` — audit tổng chỉ-đọc.
- Xem [ma trận so sánh](02-ma-tran-so-sanh-16-agent.md) và [quy tắc an toàn](05-su-dung-an-toan-va-release-gate.md).

