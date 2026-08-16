# Catalog custom Agent LiveOps

**Ngày thiết kế được phê duyệt:** 14/08/2026  
**Trạng thái local:** Config v0.1 giữ nguyên làm planned baseline; mỗi `config.md` ghi riêng snapshot Web actual  
**Trạng thái Web (cập nhật 15/08/2026, đã xác minh trực tiếp):** đủ 10 Agent, tên đã đổi tiền tố `GS9 CFL`; 6/10 đã bind KB; cả 10 đã share vào space `CFL Member` quyền **Được chỉnh sửa**; reranker `bge-reranker-v2-m3` và `Chế độ suy nghĩ` đã bật; tải ảnh + VLM `qwen3.6-plus` đã bật. **Chưa chat/runtime/gold-set test — G6 vẫn mở.**  
**Nguyên tắc:** Read-only hoặc draft-only; Human approval cho mọi hành động gửi, publish, thay đổi live, compensation, sanction hoặc ghi dữ liệu.

| Agent | Web Agent ID | Mục đích | Phạm vi dữ liệu ban đầu | Trạng thái Web |
|---|---|---|---|---|
| `GS9 CFL LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` | Lập event brief, calendar, dependency, checklist và approval map | Chưa bind — chờ audit lịch/event spec/runbook | Bind `GS9 Knowledge VNG AI`; share `CFL Member`; untested |
| `GS9 CFL Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | Review change/config trước phát hành và chuẩn bị rollback | Chưa bind — chờ audit config dictionary/change ticket | Bind `GS9 Knowledge VNG AI`; share `CFL Member`; untested |
| `GS9 CFL Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` | Lập timeline, severity đề xuất, giả thuyết và bước kiểm tra sự cố | Chưa bind — chờ audit runbook/known issue/monitoring snapshot | Bind `GS9 CFL PUM`; share `CFL Member`; untested |
| `GS9 CFL KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | Phân tích KPI, cohort, segment và experiment | Chưa bind — chờ audit metric dictionary/curated tables | Bind `GS9 CFL Kho Dữ Liệu Tổng Hợp`; share `CFL Member`; untested |
| `GS9 CFL Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | Kiểm tra giá, reward, nguồn–sink và rủi ro offer | Chưa bind — chờ audit item/economy/offer data | Chưa bind KB; share `CFL Member`; untested |
| `GS9 CFL Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | Tổng hợp feedback đã ẩn danh thành chủ đề và xu hướng | Chưa bind — chờ privacy/retention audit | Bind `GS9 CFL Sentiment Feedback User`; share `CFL Member`; untested |
| `GS9 CFL CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | Tra cứu policy, phân loại ticket và soạn reply/escalation | Chưa bind — chờ audit FAQ/CS policy/known issue | Chưa bind KB; share `CFL Member`; untested |
| `GS9 CFL GM Policy Advisor` | `01d42d42-dd08-4907-9d4a-913142bc554c` | Tra cứu chính sách xử phạt, quy trình xử lý và tiền lệ cho GM có thẩm quyền | Chưa bind — chờ tạo `GS9 CFL GM Policy & Sanction` (L6) | Chưa bind KB; share `CFL Member`; untested |
| `GS9 CFL Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | Soạn notice, patch note, in-game mail/push và localization | Chưa bind — chờ audit brand/glossary/approved claims | Chưa bind KB; share `CFL Member`; untested |
| `GS9 CFL Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | Soạn postmortem, lessons learned và đề xuất cập nhật KB | Chưa bind — chờ audit incident/event evidence | Bind 2 KB tầng L0; share `CFL Member`; untested |

## Web actual — 15/08/2026 (đã xác minh trực tiếp trên UI)

- **Đã kiểm chứng:** danh sách sau khi tạo hiển thị `Tất cả 18`, `Của tôi 12`, `Mặc định 6`, shared-with-me `0`.
- Chín Agent `Suy luận thông minh` đều dùng preset `Hỏi đáp RAG`; `GS9 CFL CS Copilot` ở mode `Trả lời nhanh` **không có control `Loại trợ lý`**.
- Cả 10: model `hosted_vllm/qwen3.6-35b`, reranker `bge-reranker-v2-m3`, temperature `0.7`, **Chế độ suy nghĩ Bật**, tải ảnh **Bật** + VLM `qwen3.6-plus`, tải âm thanh Off, share space `CFL Member` quyền **Được chỉnh sửa**.
- **`Prompt theo intent` để trống ở cả 10** (dùng template mặc định) — kiểm chứng mẫu trên `GS9 CFL Economy Offer Analyst` và `GS9 CFL CS Copilot`.
- 6/10 đã bind KB: Knowledge Curator (2), Incident Triage, KPI Experiment Analyst, Player Voice Analyst, LiveOps Planner, Release Reviewer (mỗi Agent 1).
- Cả chín Smart Agent dùng `20` steps, timeout `120s`, parallel Off. `GS9 CFL CS Copilot` dùng mode `Trả lời nhanh`, không có tab Tools, steps hoặc timeout và có `0` explicit tools.
- Basic tool theo vai trò giữ nguyên như 14/08. Sáu Agent đã bind KB được bổ sung tool truy hồi từ 14/08 (xem ma trận bên dưới).
- Nhóm Wiki (`Tìm Wiki`, `Đọc trang Wiki`), nhóm data (`Lược đồ dữ liệu`, `Phân tích dữ liệu`, `Truy vấn CSDL`), `Liệt kê đoạn`, `Đọc tài liệu nguồn` và `Danh mục sản phẩm` vẫn **Off toàn bộ**.
- **Chưa chat/runtime/gold-set test (G6 vẫn mở).** `GS9 CFL CS Copilot` có thêm tab `Hội thoại` và trường `Mẫu ngữ cảnh` mà các Agent Smart không có.
- Planned baseline trong từng file có thể khác Web actual về model, temperature, reranker hoặc tool. Khi mô tả trạng thái đang chạy, **Web actual là nguồn chuẩn**.

### Ma trận tool active hiện tại

Số trong ngoặc là tổng tool đọc được trên thẻ Agent ngày 15/08/2026.

| Agent | Basic tool | Tool phụ thuộc nguồn active |
|---|---|---|
| `GS9 CFL LiveOps Planner` (6) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa`; `Thông tin tài liệu` |
| `GS9 CFL Release Reviewer` (5) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa` |
| `GS9 CFL Incident Triage` (5) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa` |
| `GS9 CFL KPI Experiment Analyst` (6) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa`; `Thông tin tài liệu` |
| `GS9 CFL Economy Offer Analyst` (3) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có — chưa bind KB |
| `GS9 CFL Player Voice Analyst` (4) | `Hỏi người dùng`; `Suy nghĩ` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa` |
| `GS9 CFL CS Copilot` (0) | Không có tab `Công cụ` (mode Trả lời nhanh) | Không có — chưa bind KB |
| `GS9 CFL GM Policy Advisor` (2) | `Hỏi người dùng`; `Lập kế hoạch (todo)` | Không có — chưa bind KB |
| `GS9 CFL Player Communications` (3) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | Không có — chưa bind KB |
| `GS9 CFL Knowledge Curator` (6) | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa`; `Thông tin tài liệu` |

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
