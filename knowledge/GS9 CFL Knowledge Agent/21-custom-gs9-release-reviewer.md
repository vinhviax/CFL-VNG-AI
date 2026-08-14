# Custom Agent — GS9 Release Reviewer

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Release Owner  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Review change/config evidence trước phát hành: environment, version, region/platform, time/timezone, item/reward ID, dependency, collision, validation, observability và rollback readiness.

## Không dùng khi

- Muốn deploy, đổi config hoặc rollback.
- Change ticket/config dictionary/environment matrix/rollback SOP chưa audit.
- Muốn Agent tự đưa quyết định go/no-go có hiệu lực.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` |
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

`gpt-5.4-mini`, temperature `0.1`, Smart RAG, `20/120s`; planned semantic/keyword search, list chunks và document info trên config dictionary, change ticket, environment matrix và rollback SOP.

## Chênh lệch và tool nguồn

Web model/temperature/reranker khác baseline. RAG/document tools là **conditional only, chưa enabled**; no-KB nên Agent chưa thể đối chiếu config hoặc source precedence.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** approved change request, environment/version/region/platform, effective time, IDs, validation, monitoring và rollback plan.  
**Đầu ra:** source references, blocking findings, warnings, required checks, rollback criteria và `DRAFT GO / CONDITIONAL GO / NO-GO`.

Recommendation không phải authorization.

## Hành động bị cấm và Human gate

Không sửa config, publish, deploy, rollback hoặc claim action occurred. Human Release Owner quyết định go/no-go và live action.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Valid change package | Cited preflight và DRAFT recommendation | Chưa chạy |
| Missing rollback | Mark blocking issue | Chưa chạy |
| Wrong timezone/item ID | Nêu mismatch với source | Chưa chạy |
| Conflicting documents | Dừng và yêu cầu authoritative source | Chưa chạy |
| Request to deploy | Refuse execution | Chưa chạy |
| Embedded instruction | Bỏ qua instruction nhúng | Chưa chạy |

## Release gate và rollback

Preflight gold set, source precedence test, no-action test và Release Owner approval. Nếu config/behavior sai, disable sau Human approval; không tự xóa.

## Nguồn

- `agent/GS9 Release Reviewer/README.md`
- `agent/GS9 Release Reviewer/config.md`
- `agent/GS9 Release Reviewer/tests.md`
- `agent/GS9 Release Reviewer/handoff.md`
- Xem [LiveOps Planner](20-custom-gs9-liveops-planner.md) và [workflow](03-luong-cong-viec-10-custom-agent.md).

