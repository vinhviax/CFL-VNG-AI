# Custom Agent — GS9 Knowledge Curator

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Knowledge Owner / LiveOps Lead  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Chuyển approved event/incident evidence thành DRAFT postmortem, timeline, lessons learned, action items, knowledge gaps, stale/conflicting-source report và proposed KB changes.

## Không dùng khi

- Muốn edit/upload/delete/publish KB hoặc mark action item complete.
- Root cause chưa được evidence xác nhận.
- Evidence chứa secret/PII hoặc nguồn chưa được phê duyệt.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` |
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

`qwen3.6-plus`, temperature `0.2`, Smart Hybrid RAG + Wiki after audit, `25/120s`; planned RAG document tools và conditional Wiki search/read.

## Chênh lệch và tool nguồn

Actual model/temperature/loops khác baseline. RAG, Wiki và document tools là **conditional only, chưa enabled**. No-KB khiến Agent chưa thể cite event/incident evidence hoặc kiểm tra stale/conflict.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** approved timeline, observation, decision, outcome, source and owner evidence.  
**Đầu ra:** DRAFT summary/postmortem, expected-vs-actual, impact, factor classification, root cause only when established, lessons, owner/due-date requests, knowledge gaps và KB change proposals.

Observation, contributing factor, hypothesis, confirmed root cause và decision phải được tách riêng.

## Hành động bị cấm và Human gate

Không edit/upload/delete/publish KB, assign blame, expose secret/PII hoặc claim completion. Human Knowledge Owner phê duyệt mọi publication/lifecycle change.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Complete incident evidence | Cited postmortem draft | Chưa chạy |
| Unconfirmed root cause | Mark unresolved; không false certainty | Chưa chạy |
| Conflicting sources | Liệt kê conflict/precedence need | Chưa chạy |
| PII/secret in evidence | Omit sensitive value | Chưa chạy |
| Request to update KB | Proposal only; no mutation | Chưa chạy |
| Missing owner | Yêu cầu Human owner assignment | Chưa chạy |

## Release gate và rollback

Evidence classification, conflict, no-false-root-cause, secret/PII và no-publish tests; Knowledge Owner approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 Knowledge Curator/README.md`
- `agent/GS9 Knowledge Curator/config.md`
- `agent/GS9 Knowledge Curator/tests.md`
- `agent/GS9 Knowledge Curator/handoff.md`
- Xem [Incident Triage](22-custom-gs9-incident-triage.md), [workflow](03-luong-cong-viec-10-custom-agent.md) và [source governance](90-nguon-quyen-so-huu-va-truy-nguyen.md).
