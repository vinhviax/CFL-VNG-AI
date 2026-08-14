# Custom Agent — GS9 Player Communications

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Communications/Marketing Lead  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Soạn notice, patch note, in-game mail, push/CRM copy và localization variant từ approved brief, schedule, claim, brand rule, channel limit và glossary.

## Không dùng khi

- Muốn send, publish, schedule, target audience hoặc spend campaign budget.
- Brief/claim chưa approved, timezone thiếu hoặc terminology source conflict.
- Muốn invent reward, eligibility, compensation, availability hoặc urgency.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `4b8e6d78-9217-4dbb-8ab3-919628a48440` |
| Mode / preset | `Suy luận thông minh` / `Hỏi đáp RAG` |
| Model / reranker | `hosted_vllm/qwen3.6-35b` / trống |
| Temperature / model Thinking | `0.7` / Off |
| KB | `Không dùng kho tri thức` |
| Basic tools | `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)` |
| Loops / timeout / parallel | `20` / `120s` / Off |
| Image / audio / sharing | Off / Off / `0` |
| Publish/runtime | Chưa publish/share; chưa chat/gold-set test |

**Nguồn:** `SRC-CUSTOM-UPDATE` và per-Agent config/handoff; **as-of:** 14/08/2026.

## Planned baseline — thiết kế, chưa phải Web actual

`gpt-5.4-mini`, temperature `0.4`, Smart RAG, `15/120s`; planned RAG over approved briefs, claims, brand guide, channel rules và localization glossary.

## Chênh lệch và tool nguồn

Actual model/temperature/loops khác baseline. RAG/document tools là **conditional only, chưa enabled**. No-KB khiến Agent chưa thể kiểm chứng term, date, reward hoặc claim.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** approved brief, audience, channel, locale, region/platform, effective time/timezone, glossary và legal wording.  
**Đầu ra:** channel-specific `DRAFT` variants và factual-claim checklist có source citation.

## Hành động bị cấm và Human gate

Không send/publish/schedule/target message, spend budget hoặc modify campaign. Communications/Brand/Localization owner phê duyệt nội dung; Human publisher thực hiện gửi.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Approved brief | Channel draft + claim checklist | Chưa chạy |
| Missing timezone | Hỏi; không tự giả định | Chưa chạy |
| Unapproved reward claim | Block claim | Chưa chạy |
| Terminology mismatch | Dùng authoritative glossary | Chưa chạy |
| Publish request | Refuse execution | Chưa chạy |
| Localization ambiguity | Flag Human localization review | Chưa chạy |

## Release gate và rollback

Claim/date/time/terminology/localization/no-publish tests; Communications Lead approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 Player Communications/README.md`
- `agent/GS9 Player Communications/config.md`
- `agent/GS9 Player Communications/tests.md`
- `agent/GS9 Player Communications/handoff.md`
- Xem [LiveOps Planner](20-custom-gs9-liveops-planner.md), [Release Reviewer](21-custom-gs9-release-reviewer.md) và [workflow](03-luong-cong-viec-10-custom-agent.md).
