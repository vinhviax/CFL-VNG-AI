# Audit tạo custom Agent LiveOps — 14/08/2026

**Phạm vi:** 10 custom Agent trong chuỗi công việc LiveOps + CS/GM + Product/Data/Marketing trên VNG AI.  
**Phương pháp:** kiểm chứng identity, ID và cấu hình UI-visible sau khi tạo; không gọi private API, không đọc cookie/local storage/session.  
**Mutation được phép trong đợt này:** tạo Agent và lưu cấu hình được giao. Không bind KB, publish/share, chat-test, tắt/bật, clone hoặc xóa Agent/KB.

## Kết quả danh sách

- **Đã kiểm chứng:** `Tất cả 18`, `Của tôi 12`, `Mặc định 6`, shared-with-me `0`.
- **Đã kiểm chứng:** đủ 10 custom Agent có identity và Web Agent ID như bảng dưới.
- **Đã kiểm chứng:** sharing của từng Agent là `0`; không có KB được bind.
- **Có điều kiện:** System Prompt và planned baseline mô tả hành vi dự kiến nhưng chưa được chứng minh bằng chat.
- **Bị chặn–Chưa xác định:** runtime, grounding, chất lượng, latency, quota và tool behavior vì không chat/runtime test.

## Inventory và cấu hình Web actual

| Agent | Web Agent ID | Mode | Steps / timeout | Tool hiệu lực |
|---|---|---|---|---|
| `GS9 LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` | Smart | `20` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | Smart | `20` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` | Smart | `30` / `180s` | Chỉ `Hỏi người dùng` |
| `GS9 KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | Smart | `30` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | Smart | `25` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | Smart | `30` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | Fast Answer | Không có | Không có tab tool |
| `GS9 GM Case Investigator` | `01d42d42-dd08-4907-9d4a-913142bc554c` | Smart | `20` / `180s` | Chỉ `Hỏi người dùng` |
| `GS9 Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | Smart | `15` / `120s` | Chỉ `Hỏi người dùng` |
| `GS9 Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | Smart | `25` / `120s` | Chỉ `Hỏi người dùng` |

## Cấu hình chung đã kiểm chứng

- Preset: `Hỏi đáp RAG`.
- Model: `hosted_vllm/qwen3.6-35b`.
- Reranker: trống.
- Temperature: `0.7`.
- Thinking: Off.
- Knowledge Base: `Không dùng kho tri thức`.
- Image upload: Off.
- Audio/ASR: Off.
- Sharing: `0`.
- Parallel tool calls của chín Smart Agent: Off.
- `GS9 CS Copilot` là Fast Answer nên không có tool, steps hoặc timeout.

## Planned baseline so với Web actual

- System Prompt và planned baseline trong `agent/<Agent>/config.md` được giữ nguyên để bảo toàn thiết kế đã phê duyệt.
- Planned baseline có thể khác Web actual về model, temperature, reranker, preset hoặc tool.
- Khi báo trạng thái đang lưu trên Web, mục `Web actual — 14/08/2026` và audit này là nguồn chuẩn.
- Không suy diễn rằng prompt behavior, RAG, citations hoặc approval guardrail đã hoạt động; chưa có KB và chưa chat/runtime test.

## Boundary tiếp theo

- Không bind bất kỳ KB CFL nào chỉ dựa trên tên. Phải audit nội dung, owner, ACL, retention và dữ liệu nhạy cảm trước.
- Không dùng `Data Private Weapon` hoặc dữ liệu định danh/hành vi khi chưa có phê duyệt riêng.
- Không publish/share, gửi tin, thay đổi live, compensation, sanction, account mutation hoặc database write nếu chưa có Human approval và chỉ định mới.
