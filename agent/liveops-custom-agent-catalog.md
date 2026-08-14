# Catalog custom Agent LiveOps

**Ngày thiết kế được phê duyệt:** 14/08/2026  
**Trạng thái local:** Config v0.1 giữ nguyên làm planned baseline; mỗi `config.md` ghi riêng snapshot Web actual  
**Trạng thái Web:** Đã tạo đủ 10 Agent ngày 14/08/2026; chưa bind KB, chưa publish/share và chưa chat/runtime/gold-set test  
**Nguyên tắc:** Read-only hoặc draft-only; Human approval cho mọi hành động gửi, publish, thay đổi live, compensation, sanction hoặc ghi dữ liệu.

| Agent | Web Agent ID | Mục đích | Phạm vi dữ liệu ban đầu | Trạng thái Web |
|---|---|---|---|---|
| `GS9 LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` | Lập event brief, calendar, dependency, checklist và approval map | Chưa bind — chờ audit lịch/event spec/runbook | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | Review change/config trước phát hành và chuẩn bị rollback | Chưa bind — chờ audit config dictionary/change ticket | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` | Lập timeline, severity đề xuất, giả thuyết và bước kiểm tra sự cố | Chưa bind — chờ audit runbook/known issue/monitoring snapshot | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | Phân tích KPI, cohort, segment và experiment | Chưa bind — chờ audit metric dictionary/curated tables | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | Kiểm tra giá, reward, nguồn–sink và rủi ro offer | Chưa bind — chờ audit item/economy/offer data | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | Tổng hợp feedback đã ẩn danh thành chủ đề và xu hướng | Chưa bind — chờ privacy/retention audit | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | Tra cứu policy, phân loại ticket và soạn reply/escalation | Chưa bind — chờ audit FAQ/CS policy/known issue | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 GM Case Investigator` | `01d42d42-dd08-4907-9d4a-913142bc554c` | Tạo evidence bundle và đề xuất xử lý case cho GM duyệt | Chưa bind — chờ case-scoped view và policy audit | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | Soạn notice, patch note, in-game mail/push và localization | Chưa bind — chờ audit brand/glossary/approved claims | Đã tạo; no-KB; sharing `0`; untested |
| `GS9 Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | Soạn postmortem, lessons learned và đề xuất cập nhật KB | Chưa bind — chờ audit incident/event evidence | Đã tạo; no-KB; sharing `0`; untested |

## Web actual — 14/08/2026

- **Đã kiểm chứng:** danh sách sau khi tạo hiển thị `Tất cả 18`, `Của tôi 12`, `Mặc định 6`, shared-with-me `0`.
- Cả 10 dùng preset `Hỏi đáp RAG`, model `hosted_vllm/qwen3.6-35b`, reranker trống, temperature `0.7`, Thinking Off, KB `Không dùng kho tri thức`, image/audio Off và sharing `0`.
- Cả chín Smart Agent dùng `20` steps, timeout `120s`, parallel Off. `GS9 CS Copilot` dùng mode `Trả lời nhanh`, không có tab Tools, steps hoặc timeout và có `0` explicit tools.
- Tool active của Planner, Release Reviewer, Incident Triage, KPI Experiment Analyst, Economy Offer Analyst, Player Communications và Knowledge Curator: `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`.
- Tool active của Player Voice Analyst: `Hỏi người dùng`, `Suy nghĩ`.
- Tool active của GM Case Investigator: `Hỏi người dùng`, `Lập kế hoạch (todo)`.
- Không có tool phụ thuộc KB/Wiki/data nào đang active: `Tìm theo ngữ nghĩa`, `Tìm theo từ khóa`, `Liệt kê đoạn`, `Thông tin tài liệu`, `Tìm Wiki`, `Đọc trang Wiki`, `Đọc tài liệu nguồn`, `Lược đồ dữ liệu`, `Phân tích dữ liệu`, `Truy vấn CSDL` và `Danh mục sản phẩm` đều chỉ là lựa chọn tương lai có điều kiện nếu được nêu trong config từng vai trò.
- Không bind KB, không publish/share và không chat/runtime test.
- Planned baseline trong từng file có thể khác Web actual về model, temperature, reranker hoặc tool. Khi mô tả trạng thái đang chạy, **Web actual là nguồn chuẩn**.

### Ma trận tool active hiện tại

| Agent | Tool active trên Web | Tool phụ thuộc nguồn active |
|---|---|---|
| `GS9 LiveOps Planner` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Release Reviewer` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Incident Triage` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 KPI Experiment Analyst` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Economy Offer Analyst` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Player Voice Analyst` | `Hỏi người dùng`; `Suy nghĩ` | Không có |
| `GS9 CS Copilot` | Không có tab Tools; `0` explicit tools | Không có |
| `GS9 GM Case Investigator` | `Hỏi người dùng`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Player Communications` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |
| `GS9 Knowledge Curator` | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có |

## Phân loại bằng chứng

- **Đã kiểm chứng:** identity, Web Agent ID, cấu hình UI-visible và count danh sách nêu trên.
- **Có điều kiện:** hành vi dự kiến từ System Prompt/planned baseline; chưa được chứng minh bằng chat.
- **Bị chặn–Chưa xác định:** runtime, gold-set, chất lượng, grounding, tool behavior và quota thực tế vì chưa chat/runtime/gold-set test.

## Boundary chung

- Không dùng `Tất cả kho tri thức`.
- Không bind `GS9 Knowledge VNG - Image Assets` làm corpus hỏi đáp.
- `GS9 Knowledge VNG AI` là sổ tay nền tảng, không tự động dùng làm nguồn nghiệp vụ game.
- Các KB CFL hiện hữu chỉ là ứng viên; không bind theo tên khi chưa audit nội dung, owner, ACL và retention.
- Không dùng `Data Private Weapon`.
- Không bật tool gửi tin, publish, sửa config, rollback, grant item, compensation, sanction, account mutation hoặc database write.
