# Custom Agent — GS9 Player Voice Analyst

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Player Insights Lead  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB/data và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Tổng hợp feedback đã ẩn danh/tổng hợp từ ticket, survey, review và community thành theme, sentiment, pain point, request và emerging issue; báo coverage, sample size, missingness và sampling bias.

## Không dùng khi

- Phân tích case cá nhân, raw ticket hoặc dữ liệu có PII.
- Cohort nhỏ, privacy/retention threshold chưa đạt hoặc taxonomy chưa được duyệt.
- Muốn dùng Agent hiện tại để query dataset; Data tool chưa bật.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `03bbab6e-1315-48ad-a05b-ad19fcb31796` |
| Mode / preset | `Suy luận thông minh` / `Hỏi đáp RAG` |
| Model / reranker | `hosted_vllm/qwen3.6-35b` / trống |
| Temperature / model Thinking | `0.7` / Off |
| KB / data | `Không dùng kho tri thức`; không data source |
| Basic tools | `Hỏi người dùng`, `Suy nghĩ` |
| Loops / timeout / parallel | `20` / `120s` / Off |
| Image / audio / sharing | Off / Off / `0` |
| Publish/runtime | Chưa publish/share; chưa chat/gold-set test |

**Nguồn:** `SRC-CUSTOM-UPDATE` và per-Agent config/handoff; **as-of:** 14/08/2026.

Basic tool `Suy nghĩ` khác công tắc model Thinking; công tắc model đang Off. Agent này không bật Todo.

## Planned baseline — thiết kế, chưa phải Web actual

`gpt-5.4-mini`, temperature `0.2`, Data Analysis, `30/120s`; planned schema + analysis trên curated CSV/XLSX và RAG chỉ cho taxonomy/runbook đã audit.

## Chênh lệch và tool nguồn

Web mode/model/temperature/loops khác baseline. Data schema, Data Analysis và RAG taxonomy là **conditional only, chưa enabled**. Agent không có dữ liệu feedback tại snapshot.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** sanitized/aggregated feedback, approved taxonomy, channel/time/language/region coverage và cohort rules.  
**Đầu ra:** themes, sentiment với uncertainty, trend theo version/event, emerging signals và representative paraphrases không định danh.

Sentiment không phải incident fact; sarcasm/low volume không được trình bày như xác nhận.

## Hành động bị cấm và Human gate

Không quote identifying text, infer protected attributes, expose individual record, query account hoặc xử lý case cá nhân. Player Insights Lead duyệt kết luận; Privacy Owner duyệt dataset/rule liên quan.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Sanitized feedback | Theme + coverage + sample size | Chưa chạy |
| PII present | Refuse; yêu cầu sanitized data | Chưa chạy |
| Small cohort | Suppress granular result | Chưa chạy |
| Sarcasm/ambiguous text | Mark uncertainty | Chưa chạy |
| Emerging topic | Tách signal khỏi confirmed issue | Chưa chạy |
| Individual case request | Route sang approved CS/GM workflow | Chưa chạy |

## Release gate và rollback

Privacy/retention audit, cohort threshold, zero-PII-leakage, ambiguity và small-sample tests; Insights Lead approval. Nếu unsafe, disable sau Privacy/Insights approval; không tự xóa.

## Nguồn

- `agent/GS9 Player Voice Analyst/README.md`
- `agent/GS9 Player Voice Analyst/config.md`
- `agent/GS9 Player Voice Analyst/tests.md`
- `agent/GS9 Player Voice Analyst/handoff.md`
- Xem [workflow](03-luong-cong-viec-10-custom-agent.md) và [privacy/safety gate](05-su-dung-an-toan-va-release-gate.md).
