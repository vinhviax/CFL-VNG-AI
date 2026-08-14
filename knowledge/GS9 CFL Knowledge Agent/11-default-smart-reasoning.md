# Default Agent — Smart Reasoning

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho behavior  
**Nguồn chính:** `SRC-D-SMART`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Cần RAG evidence-first nhiều bước trên tài liệu/chunk.
- Cần semantic + keyword fan-out rồi đọc sâu trước khi tổng hợp.

## Không dùng khi

- Cần Wiki, SQL, Data Analysis hoặc Product Catalog; các tool này không active.
- Cần dữ liệu allowlist nhạy cảm; Agent đang chọn All KB.
- Cần bằng chứng rằng behavior đã pass runtime; audit chưa chat-test.

## Mục đích và đầu ra dự kiến

Mô tả UI: `ReAct reasoning framework with multi-step thinking and tool calling`. System Prompt là Progressive Agentic RAG, Evidence-First: fresh retrieval cho câu hỏi mới, semantic/keyword fan-out, đọc full chunk/FAQ và không fallback general knowledge khi KB không có bằng chứng.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / preset | `Suy luận thông minh` / `Hỏi đáp RAG` |
| Model / reranker | `gpt-5.4-mini` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.7` / Off |
| KB / file type | `Tất cả kho tri thức` / `Tất cả loại tệp` |
| Retrieval | Tự động |
| Vector Top K | `10` |
| Keyword / vector threshold | `0.3` / `0.5` |
| Rerank Top K / threshold | `10` / `0.3` |
| Max loops / timeout | `50` / `120s` |
| Parallel tool calls | Off |
| Image / audio | Off / Off |
| Chat tab | Không có |

**Nguồn:** `SRC-D-SMART`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Tool hiệu lực

- `Tìm theo ngữ nghĩa`
- `Tìm theo từ khóa`
- `Liệt kê đoạn`
- `Thông tin tài liệu`

Wiki, database query, Catalog, schema và Data Analysis không active.

## Prompt variables

`{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có per-intent override được chọn.

## Cách dùng an toàn

1. Đặt câu hỏi có scope rõ; kiểm tra danh sách nguồn vì Agent dùng All KB.
2. Với số liệu hoặc policy, mở full source được trích thay vì chỉ nhìn answer.
3. Nếu không có evidence, yêu cầu Agent abstain; không chuyển sang general knowledge.
4. Không dùng tool count hoặc loop count như bằng chứng chất lượng.
5. Không nhập private data khi chưa xác nhận ACL của mọi KB trong All KB.

## Runtime evidence và giới hạn

**Có điều kiện:** fresh retrieval, fan-out và deep-read là prompt claim.

**Bị chặn–Chưa xác định:** runtime grounding, tool sequence, source permission, sharing, quota, retention, latency và answer quality.

## Nguồn

- `agent/smart-reasoning-config.md`
- `audit/default-agent-readonly-audit-2026-08-14.md`
- Xem [Quick Answer](10-default-quick-answer.md), [Hybrid Researcher](12-default-hybrid-researcher.md) và [ma trận](02-ma-tran-so-sanh-16-agent.md).

