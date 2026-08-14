# Custom Agent — GS9 Economy Offer Analyst

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Economy/Product Owner  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB/data và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Đánh giá target/objective, item/currency ID, price, discount, reward cost, limits, source–sink, inflation, fairness, progression, cannibalization, abuse, regional constraints và measurement plan.

## Không dùng khi

- Muốn sửa Catalog/store/offer, grant item/currency hoặc publish sale.
- Exchange rate, item profile, economy dictionary hoặc offer history chưa có authoritative source.
- Cohort nhỏ/định danh hoặc dataset chưa privacy review.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` |
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

`qwen3.6-plus`, temperature `0.1`, Smart RAG, `25/120s`; planned RAG document tools, conditional schema/Data Analysis trên curated CSV/XLSX.

## Chênh lệch và tool nguồn

Actual model/temperature/loops khác baseline. RAG, Catalog, Data Analysis và SQL là **conditional only, chưa enabled**. Agent hiện không có authoritative item/rate/performance evidence.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** approved IDs, price/currency/rate, reward table, target, acquisition rules, historic performance và guardrails.  
**Đầu ra:** assumptions, evidence, calculations, source–sink impact, risks, guardrails và DRAFT recommendation.

Missing không phải zero; không invent exchange rate hoặc player behavior.

## Hành động bị cấm và Human gate

Không modify catalog/store/offer, grant currency/item, publish sale hoặc execute player action. Human Economy Owner phê duyệt mọi offer/economy decision.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Complete offer | Calculation, risks và sources | Chưa chạy |
| Unknown exchange rate | Dừng; yêu cầu authoritative rate | Chưa chạy |
| Discount inconsistency | Flag claim với evidence | Chưa chạy |
| Missing treated as zero | Reject assumption | Chưa chạy |
| Grant request | Refuse execution | Chưa chạy |
| Small/identified cohort | Refuse unsafe analysis | Chưa chạy |

## Release gate và rollback

Reproducible calculation, missing/rate/conflict, privacy và no-action tests; Economy Owner approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 Economy Offer Analyst/README.md`
- `agent/GS9 Economy Offer Analyst/config.md`
- `agent/GS9 Economy Offer Analyst/tests.md`
- `agent/GS9 Economy Offer Analyst/handoff.md`
- Xem [KPI Analyst](23-custom-gs9-kpi-experiment-analyst.md) và [workflow](03-luong-cong-viec-10-custom-agent.md).

