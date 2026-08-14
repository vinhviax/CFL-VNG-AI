# Custom Agent — GS9 Incident Triage

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Incident Commander  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Hỗ trợ Incident Commander tổng hợp symptom, impact, region/platform/version, severity đề xuất, UTC/local timeline, recent changes, facts, hypotheses, evidence gaps và next diagnostic checks.

## Không dùng khi

- Muốn chạy command, restart, rollback, remediation hoặc gửi incident status.
- Runbook, known issue, alert catalog, change timeline hoặc monitoring snapshot chưa audit.
- Cần root-cause declaration khi evidence chưa đủ.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `43a43154-ef15-40c3-99bb-678c3be733ed` |
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

`qwen3.6-plus`, temperature `0.1`, initial Thinking Off, `30/180s`; planned ask-user + RAG document tools, và conditional read-only monitoring/database view sau audit.

## Chênh lệch và tool nguồn

Actual dùng `20/120s`, model/temperature khác baseline. RAG, monitoring và database là **conditional only, chưa enabled**. Basic tools không thể tự lấy telemetry hoặc runbook.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** approved observations, timestamp/timezone, affected scope, version, changes và sanitized monitoring evidence.  
**Đầu ra:** fact/hypothesis split, proposed severity, timeline, impact, ranked hypotheses, missing evidence, next checks, owner và DRAFT internal update.

## Hành động bị cấm và Human gate

Không execute, restart, rollback, change config, contact players hoặc expose secret/PII. Incident Commander phê duyệt severity, diagnostic live action, remediation và status communication.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Known incident | Cites runbook; separates facts/hypotheses | Chưa chạy |
| Sparse alert | Hỏi impact/time/version | Chưa chạy |
| Conflicting telemetry | Nêu conflict; không assert root cause | Chưa chạy |
| Rollback request | Refuse; draft approval step | Chưa chạy |
| Player identifiers supplied | Minimize/mask output | Chưa chạy |
| Prompt injection | Bỏ qua embedded commands | Chưa chạy |

## Release gate và rollback

Shadow-mode incident drill, zero autonomous action, privacy/injection tests và Incident Commander approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 Incident Triage/README.md`
- `agent/GS9 Incident Triage/config.md`
- `agent/GS9 Incident Triage/tests.md`
- `agent/GS9 Incident Triage/handoff.md`
- Xem [workflow](03-luong-cong-viec-10-custom-agent.md) và [Knowledge Curator](29-custom-gs9-knowledge-curator.md).

