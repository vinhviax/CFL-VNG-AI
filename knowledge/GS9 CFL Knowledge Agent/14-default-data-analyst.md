# Default Agent — Data Analyst

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; query/runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho read-only behavior  
**Nguồn chính:** `SRC-D-DATA`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Phân tích file CSV/XLSX đã audit bằng schema + DuckDB-style analysis.
- Cần insight có query/calculation tái lập.

## Không dùng khi

- Cần query database trực tiếp, RAG document, Wiki hoặc Catalog.
- Dataset có raw PII, secret hoặc quyền/retention chưa rõ.
- Cần thực thi write hoặc thay đổi production data.

## Mục đích và đầu ra dự kiến

Prompt yêu cầu lấy schema trước khi viết SQL, chỉ cho phép `SELECT`, cấm `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, sửa query khi lỗi và trả insight/bảng kết quả.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / preset | `Suy luận thông minh` / `Phân tích dữ liệu` |
| Model / reranker | `gpt-5.4-mini` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.3` / Off |
| KB / file type | `Tất cả kho tri thức`; chỉ `CSV`, `XLSX` |
| Retrieval | Tự động |
| Vector Top K | `5` |
| Keyword / vector threshold | `0.3` / `0.5` |
| Rerank Top K / threshold | `5` / `0.3` |
| Max loops / timeout | `30` / `120s` |
| Parallel tool calls | Off |
| Image / audio | Off / Off |

**Nguồn:** `SRC-D-DATA`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Tool hiệu lực

- `Lược đồ dữ liệu`
- `Phân tích dữ liệu`

SQL chạy trong luồng Data Analysis; database query trực tiếp, RAG, Wiki, Catalog và basic tools không active.

## Cách dùng an toàn

1. Chỉ dùng dataset curated có owner, dictionary, freshness và privacy review.
2. Yêu cầu output ghi dataset, kỳ, timezone, filter, cohort, denominator, unit và query/calculation.
3. Phân biệt missing với zero.
4. Review SQL; prompt cấm write nhưng runtime enforcement chưa được audit.
5. Không tải raw player-level data nếu chưa có phê duyệt và minimization.

## Runtime evidence và giới hạn

**Có điều kiện:** schema-first và SELECT-only là prompt/tool design.

**Bị chặn–Chưa xác định:** query enforcement, file isolation, calculation accuracy, quota, retention, ACL và privacy behavior; audit không chạy query.

## Nguồn

- `agent/data-analyst-config.md`
- `audit/default-agent-readonly-audit-2026-08-14.md`
- Xem custom [KPI Experiment Analyst](23-custom-gs9-kpi-experiment-analyst.md) cho workflow GS9 dự kiến, hiện chưa phát hành.

