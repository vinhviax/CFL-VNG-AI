# Default Agent — FPA Analyst

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; pipeline/runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho source scoping  
**Nguồn chính:** `SRC-D-FPA`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Cần workflow FPA cố định để route nguồn và báo cáo hiệu suất.
- Có quyền hợp lệ với Catalog/database source và có thể review số liệu/kỳ/đơn vị.

## Không dùng khi

- Cần guarantee source scope: UI vẫn chọn All KB và pipeline chưa test.
- Cần Wiki hoặc CSV/XLSX Data Analysis tool.
- Công việc nhạy cảm chưa có least-privilege review.

## Mục đích và đầu ra dự kiến

Mô tả UI: fixed pipeline hiểu câu hỏi, route tới source phù hợp rồi retrieval. Prompt yêu cầu chỉ trả lời từ nội dung truy hồi, giữ chính xác số liệu/kỳ/đơn vị, không coi missing là zero và query source inventory khi user hỏi về nguồn.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / workflow | `Quy trình` / fixed `fpa` |
| Model / reranker | `qwen3.6-plus` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.7` / On |
| KB / file type | `Tất cả kho tri thức` / `Tất cả loại tệp` |
| Retrieval | Tự động |
| Vector Top K | `10` |
| Keyword / vector threshold | `0.3` / `0.3` |
| Rerank Top K / threshold | `10` / `0.3` |
| Max loops / timeout | `10` / `180s` |
| Parallel tool calls | Off |
| Image / audio | Off / Off |

**Nguồn:** `SRC-D-FPA`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Tool hiệu lực

- `Danh mục sản phẩm`
- `Hỏi người dùng`
- `Tìm theo ngữ nghĩa`
- `Tìm theo từ khóa`
- `Liệt kê đoạn`
- `Thông tin tài liệu`
- `Truy vấn CSDL`

Wiki, schema/Data Analysis và basic thinking/todo không active.

## Static caveat

**Có điều kiện:** Prompt nói pipeline đã hiểu câu hỏi và scope source, nhưng UI vẫn để All KB. Chỉ runtime/source-drawer evidence mới chứng minh scoping thực tế.

## Cách dùng an toàn

1. Xác nhận user được phép dùng Catalog/database và đúng source scope.
2. Kiểm tra kỳ, timezone, currency, unit, missingness và source inventory.
3. Không suy ra DB query là read-only chỉ từ prompt; kiểm tra tool/backend policy.
4. Không dùng cho dữ liệu private nếu chưa có row/field allowlist.
5. Human analyst chịu trách nhiệm quyết định từ số liệu.

## Runtime evidence và giới hạn

**Bị chặn–Chưa xác định:** fixed-pipeline routing, effective database permission, source scoping, quota, sharing, retention và calculation quality; audit không chạy DB/chat test.

## Nguồn

- `agent/fpa-analyst-config.md`
- `audit/default-agent-readonly-audit-2026-08-14.md`
- Xem [Data Analyst](14-default-data-analyst.md), [chooser](01-chon-agent-nhanh.md) và [safety gate](05-su-dung-an-toan-va-release-gate.md).

