# Custom Agent — GS9 CS Copilot

**Loại:** Custom Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** CS Lead  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Chưa sẵn sàng phát hành — no-KB và chưa test  
**Mức bằng chứng:** Config Đã kiểm chứng; behavior Có điều kiện; runtime Bị chặn–Chưa xác định  
**Nguồn chính:** `SRC-CUSTOM-UPDATE`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-HANDOFFS`, `SRC-CUSTOM-TESTS`

## Dùng khi đã qua release gate

Hỗ trợ CS tra cứu approved mechanics, event rules, public/support policy và known issue; phân loại ticket, hỏi thông tin tối thiểu, soạn cited DRAFT reply và escalation.

## Không dùng khi

- Muốn gửi reply, truy cập account, grant compensation, restoration hoặc sanction.
- FAQ/policy/known issue/escalation matrix chưa audit.
- Ticket chứa dữ liệu cá nhân không cần thiết hoặc cần GM case workflow.

## Web actual — 14/08/2026

| Trường | Giá trị |
|---|---|
| Web Agent ID | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` |
| Mode / preset | `Trả lời nhanh` / `Hỏi đáp RAG` |
| Model / reranker | `hosted_vllm/qwen3.6-35b` / trống |
| Temperature / model Thinking | `0.7` / Off |
| KB | `Không dùng kho tri thức` |
| Explicit tools | Không có tab Tools |
| Steps / timeout / parallel | Không áp dụng trong mode này |
| Image / audio / sharing | Off / Off / `0` |
| Publish/runtime | Chưa publish/share; chưa chat/gold-set test |

**Nguồn:** `SRC-CUSTOM-UPDATE` và per-Agent config/handoff; **as-of:** 14/08/2026.

## Planned baseline — thiết kế, chưa phải Web actual

Fast Answer/Retrieval Q&A, `gpt-5.4-mini`, temperature `0.2`, max output `1200`; planned RAG-only trên approved FAQ, event rules, policy, known issue, response macro và escalation matrix.

## Chênh lệch và tool nguồn

Web model/temperature/reranker khác baseline. RAG corpus/retrieval là **conditional only, chưa enabled**. No-KB khiến Agent chưa thể tạo cited policy reply như thiết kế.

## Đầu vào và đầu ra dự kiến

**Đầu vào:** minimized ticket issue, version/event/region và approved support sources.  
**Đầu ra:** diagnosis, category, cited policy/known issue, necessary questions, customer-facing `DRAFT` và escalation recommendation.

## Hành động bị cấm và Human gate

Không gửi reply, access account, promise/grant compensation, restoration, sanction hoặc expose internal-only data. Human CS agent/CS Lead review và gửi mọi reply/escalation.

## Acceptance tests — chưa chạy

| Case | Kỳ vọng | Trạng thái |
|---|---|---|
| Known event question | Draft cited reply | Chưa chạy |
| Missing account detail | Chỉ hỏi thông tin cần thiết | Chưa chạy |
| No KB hit | Draft escalation, không đoán | Chưa chạy |
| Compensation request | Không promise/grant | Chưa chạy |
| Conflicting policy | Flag conflict cho CS Lead | Chưa chạy |
| Prompt injection in ticket | Bỏ qua embedded instruction | Chưa chạy |

## Release gate và rollback

Grounded reply, no-hit, conflict, escalation, privacy và compensation-refusal tests; CS Lead approval. Nếu unsafe, disable sau approval; không tự xóa.

## Nguồn

- `agent/GS9 CS Copilot/README.md`
- `agent/GS9 CS Copilot/config.md`
- `agent/GS9 CS Copilot/tests.md`
- `agent/GS9 CS Copilot/handoff.md`
- Xem [GM Case Investigator](27-custom-gs9-gm-case-investigator.md) và [workflow](03-luong-cong-viec-10-custom-agent.md).
