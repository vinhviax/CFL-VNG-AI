# Custom Agent — GS9 KPI Experiment Analyst

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Product/Data Analytics Lead  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB/data và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Phân tích curated LiveOps KPI, cohort, segment và experiment; ghi dataset/view, freshness, period, timezone, filter, denominator, unit và calculation/query tái lập.

## Không dùng khi

- Muốn launch/stop/modify experiment, segment hoặc rollout.
- Metric dictionary/schema chưa audit hoặc dataset chứa raw PII.
- Muốn dùng Agent hiện tại để query data; Data/SQL tool chưa bật.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `37da676c-59ce-4936-9314-5ac4cc3d1a45` |
| Mode / preset | `Suy luận thông minh` / `Hỏi đáp RAG` |
| Model / reranker | `hosted_vllm/qwen3.6-35b` / trống |
| Temperature / model Thinking | `0.7` / Off |
| KB / data | `Không dùng kho tri thức`; không data source |
| Basic tools | `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)` |
| Loops / timeout / parallel | `20` / `120s` / Off |
| Image / audio / sharing | Off / Off / `0` |
| Publish/runtime | Chưa publish/share; chưa chat/gold-set test |

**Nguồn:** `SRC-CUSTOM-UPDATE` và per-Agent config/handoff; **as-of:** 14/08/2026.

## Planned baseline — thiết kế, chưa phải Web actual

`gpt-5.4-mini`, temperature `0.1`, Data Analysis, `30/120s`; planned schema + analysis trên curated CSV/XLSX, conditional database `SELECT` trên audited view.

## Chênh lệch và tool nguồn

Web mode/model/temperature và loops khác baseline. Data schema, Data Analysis, SQL/database và RAG metric dictionary là **conditional only, chưa enabled**. No-KB/no-data khiến Agent chưa thể tạo calculation evidence.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** authoritative metric definition, curated dataset/view, event metadata, period/timezone, cohort/segment.  
**Đầu ra:** target/baseline/actual/variance; control/treatment, allocation, sample, guardrail, statistical limits và reproducible calculation.

## Hành động bị cấm và Human gate

Không write data, query raw player-identifying table, launch/stop experiment hoặc đổi audience. Human Analyst/Data Lead phê duyệt số liệu trước quyết định vận hành/kinh doanh.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Valid event dataset | Source, period, timezone, filters, calculation | Chưa chạy |
| Missing metric definition | Dừng và yêu cầu dictionary | Chưa chạy |
| Missing versus zero | Giữ đúng khác biệt | Chưa chạy |
| A/B result | Control/treatment, sample, limitations | Chưa chạy |
| Write query request | Refuse | Chưa chạy |
| Raw PII request | Refuse; yêu cầu curated view | Chưa chạy |

## Release gate và rollback

Gold calculations, schema/metric conflict, missing-vs-zero, SELECT-only và zero-PII-leakage tests; Data Lead approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 KPI Experiment Analyst/README.md`
- `agent/GS9 KPI Experiment Analyst/config.md`
- `agent/GS9 KPI Experiment Analyst/tests.md`
- `agent/GS9 KPI Experiment Analyst/handoff.md`
- Xem [default Data Analyst](14-default-data-analyst.md) và [workflow](03-luong-cong-viec-10-custom-agent.md).

