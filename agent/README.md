# Agent trên VNG AI

Folder này dùng để quản lý những Agent được tạo trên trang VNG AI. Mỗi Agent nên có một folder riêng mang đúng tên trên Web, tối thiểu gồm:

- `README.md`: mục tiêu, owner, Human phục vụ và KB được bind;
- `config.md`: mode, model, preset, System Prompt, Intent, tools và retrieval;
- `tests.md`: ma trận câu hỏi, nguồn, no-hit, lỗi/giới hạn và ngày kiểm chứng;
- `handoff.md`: phiên bản đang phát hành, quyền, dependency và quy trình rollback.

Không lưu credential, token hoặc dữ liệu cá nhân trong folder Agent.

## Audit Agent mặc định (read-only)

Các file `*-config.md` trong thư mục này là bản ghi cấu hình nhìn thấy trên UI của 6 Agent mặc định VNG AI tại ngày 14/08/2026. Đây là artifact audit local, không phải manifest của Agent mới và không biểu thị rằng đã tạo, clone, publish hoặc thay đổi Agent trên Web.

- [Quick Answer](quick-answer-config.md)
- [Smart Reasoning](smart-reasoning-config.md)
- [Hybrid Researcher](hybrid-researcher-config.md)
- [Wiki Questioner](wiki-questioner-config.md)
- [Data Analyst](data-analyst-config.md)
- [FPA Analyst](fpa-analyst-config.md)

Các kết luận được phân loại `Đã kiểm chứng`, `Có điều kiện` hoặc `Bị chặn–Chưa xác định`. Chi tiết phương pháp và bảng đối chiếu nằm tại `audit/default-agent-readonly-audit-2026-08-14.md`.

## Custom Agent LiveOps

Thiết kế được phê duyệt ngày 14/08/2026 gồm mười Agent theo chuỗi công việc LiveOps, không ánh xạ máy móc từ sáu Agent mặc định. Cả 10 đã được tạo trên Web nhưng vẫn ở trạng thái no-KB/sharing-0/untested: không bind KB, không publish/share và chưa chat/runtime/gold-set test. Catalog, Web Agent ID và snapshot cấu hình nằm tại [liveops-custom-agent-catalog.md](liveops-custom-agent-catalog.md); bằng chứng rollout nằm tại `../audit/liveops-custom-agent-creation-2026-08-14.md`.

Planned baseline và System Prompt được giữ trong từng `config.md`. Mục `Web actual — 14/08/2026` là nguồn chuẩn cho cấu hình đang lưu trên Web nếu model, temperature, reranker hoặc tool khác baseline thiết kế. Identity/config UI-visible là `Đã kiểm chứng`; behavior prompt là `Có điều kiện`; runtime/quality là `Bị chặn–Chưa xác định`.

Snapshot Web actual sau lần lưu cấu hình cuối ngày 14/08/2026:

- Cả chín Smart Agent dùng `20` steps, timeout `120s`, parallel Off.
- Planner, Release Reviewer, Incident Triage, KPI Experiment Analyst, Economy Offer Analyst, Player Communications và Knowledge Curator bật đúng `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`.
- Player Voice Analyst bật đúng `Hỏi người dùng`, `Suy nghĩ`; GM Case Investigator bật đúng `Hỏi người dùng`, `Lập kế hoạch (todo)`.
- CS Copilot dùng `Trả lời nhanh`, không có tab Tools và có `0` explicit tools.
- Cả 10 vẫn `Không dùng kho tri thức`; không có tool RAG, Wiki, data, `Truy vấn CSDL` hoặc `Danh mục sản phẩm` nào đang active. Mọi tool phụ thuộc nguồn trong từng `config.md` chỉ là thiết kế có điều kiện sau audit.
- Chưa chạy chat/runtime hoặc gold-set cho snapshot này.

- `GS9 CFL LiveOps Planner`
- `GS9 CFL Release Reviewer`
- `GS9 CFL Incident Triage`
- `GS9 CFL KPI Experiment Analyst`
- `GS9 CFL Economy Offer Analyst`
- `GS9 CFL Player Voice Analyst`
- `GS9 CFL CS Copilot`
- `GS9 GM Case Investigator`
- `GS9 CFL Player Communications`
- `GS9 CFL Knowledge Curator`
