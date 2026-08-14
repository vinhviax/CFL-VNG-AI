# Default Agent — Wiki Questioner

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho workflow  
**Nguồn chính:** `SRC-D-WIKI`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Câu hỏi phù hợp Wiki có trang/links được quản trị tốt.
- Cần Search–Read–Expand và theo link 1–2 hop.

## Không dùng khi

- Cần raw chunk RAG làm nguồn chính: xem [Smart Reasoning](11-default-smart-reasoning.md) hoặc [Hybrid Researcher](12-default-hybrid-researcher.md).
- Cần SQL, Data Analysis hoặc Catalog.
- Wiki chưa có owner/source traceability.

## Mục đích và đầu ra dự kiến

Mô tả UI: Agent chuyên trả lời từ Wiki KB. Prompt dùng `index` cho overview, `log` cho timeline, đọc Wiki page trước khi trả lời, theo link 1–2 hop và chỉ đọc source document khi Wiki thiếu quote/raw data.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / preset | `Suy luận thông minh` / `Hỏi đáp Wiki` |
| Model / reranker | `qwen3.6-plus` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.7` / Off |
| KB / file type | `Tất cả kho tri thức` / `Tất cả loại tệp` |
| Retrieval | Tự động |
| Vector Top K | `10` |
| Keyword / vector threshold | `0.3` / `0.5` |
| Rerank Top K / threshold | `10` / `0.3` |
| Max loops / timeout | `30` / `120s` |
| Parallel tool calls | Off |
| Image / audio | Off / Off |

**Nguồn:** `SRC-D-WIKI`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Tool hiệu lực

- `Tìm Wiki`
- `Đọc trang Wiki`
- `Đọc tài liệu nguồn`

RAG chunk, SQL/database, Catalog, schema/Data Analysis và basic tools không active.

## Static mismatch và giới hạn

- **Đã kiểm chứng:** Prompt nhắc `wiki_flag_issue`, UI không liệt kê tool này active.
- **Bị chặn–Chưa xác định:** Prompt cho phép external MCP nếu exposed, nhưng audit không chứng minh external MCP nào active.
- Workflow Search–Read–Expand và behavior theo link là prompt claim, chưa runtime test.

## Cách dùng an toàn

1. Xác nhận câu hỏi thuộc Wiki đã phê duyệt.
2. Kiểm tra trang và source document cho claim quan trọng.
3. Nếu Wiki stale/conflict, dừng và báo owner; không coi graph/link là authority.
4. Không nhập dữ liệu nhạy cảm khi UI còn All KB.

## Nguồn

- `agent/wiki-questioner-config.md`
- `audit/default-agent-readonly-audit-2026-08-14.md`
- Xem [ma trận](02-ma-tran-so-sanh-16-agent.md) và [trạng thái/giới hạn](04-trang-thai-bang-chung-va-gioi-han.md).

