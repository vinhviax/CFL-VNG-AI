# Audit bind KB + Việt hóa mô tả 10 custom Agent — 14/08/2026

## Phạm vi được giao

Người dùng chỉ định rõ: sửa config 10 custom Agent trên Web cho đúng kho tri thức, đúng prompt và đủ tool; đồng thời viết lại mô tả Agent bằng tiếng Việt thay cho tiếng Anh. Đây là **mutation live có phê duyệt**, khác với trạng thái read-only của các audit trước.

## Kết quả — Web actual sau phiên

| Agent | Agent ID | KB đã bind | Số tool | Mô tả |
|---|---|---|---:|---|
| `GS9 Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | `GS9 Knowledge VNG AI` + `GS9 CFL Knowledge Agent` | 6 | Tiếng Việt |
| `GS9 Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` | `GS9 CFL PUM` | 5 | Tiếng Việt |
| `GS9 KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | 6 | Tiếng Việt |
| `GS9 Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | `GS9 CFL Sentiment Feedback User` | 4 | Tiếng Việt |
| `GS9 LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` | `GS9 Knowledge VNG AI` | 6 | Tiếng Việt |
| `GS9 Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | `GS9 Knowledge VNG AI` | 5 | Tiếng Việt |
| `GS9 Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | **Không bind** | 3 | Tiếng Việt |
| `GS9 GM Case Investigator` | `01d42d42-dd08-4907-9d4a-913142bc554c` | **Không bind** | 2 | Tiếng Việt |
| `GS9 Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | **Không bind** | 3 | Tiếng Việt |
| `GS9 CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | **Không bind** | 0 (Trả lời nhanh, không có tab Công cụ) | Tiếng Việt |

**Đã kiểm chứng:** mỗi lần lưu đều có toast `Đã cập nhật trợ lý`; hàng danh sách sau lưu hiển thị đúng số KB và số tool nêu trên; mọi Agent ID đối chiếu khớp `agent/liveops-custom-agent-catalog.md` trước khi sửa.

## Tool đã bật

Phạm vi KB dùng `Kho tri thức đã chọn` cho cả 6 Agent có bind — **không dùng `Tất cả kho tri thức`**, đúng boundary.

- 3 tool cơ bản giữ nguyên như trước (`Suy nghĩ`, `Lập kế hoạch (todo)`, `Hỏi người dùng`); Player Voice Analyst vẫn chỉ có Ask + Think; GM Case Investigator vẫn Ask + Todo.
- Thêm `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` cho cả 6 Agent có KB.
- Thêm `Thông tin tài liệu` cho Knowledge Curator, KPI Experiment Analyst và LiveOps Planner.
- **Giữ Off:** `Liệt kê đoạn`, `Truy vấn CSDL`, `Danh mục sản phẩm`, `Phân tích dữ liệu`, `Lược đồ dữ liệu`, và toàn bộ nhóm Wiki (`Tìm wiki`, `Đọc trang wiki`, `Đọc tài liệu nguồn`) — Wiki index chưa được kiểm chứng có nội dung nên chưa bật.

## Phát hiện mới về hành vi UI

- **Tool truy hồi phụ thuộc KB:** khi Agent chưa bind KB, toàn bộ nhóm `TRUY HỒI TRI THỨC` bị mờ với chú thích `Cần có kho tri thức trong phạm vi`. Bắt buộc bind KB trước, mới bật được tool. Nhóm Wiki có chú thích riêng `Cần kho tri thức đã bật Wiki`.
- **Tab Công cụ hiển thị phạm vi KB** dạng `n KB RAG · n KB Wiki` — dùng để xác nhận bind thành công trước khi lưu.
- **Danh sách Agent tự sắp lại sau mỗi lần lưu:** Agent vừa cập nhật nhảy lên đầu nhóm `Tôi tạo`. Hệ quả vận hành: phải chụp lại danh sách trước mỗi lần bấm, không dùng lại tọa độ cũ.
- Cả 9 KB đều hiển thị nhãn `RAG` và `WIKI` trong dropdown chọn KB.

## Sự cố trong phiên và cách xử lý

Lần bấm đầu tiên mở sai Agent (`Kiểm thử Agent Knowledge VNG 2026-08-11`, ID `3c644ac2-ab5f-4141-959d-f1fa13ce8c41`) vì danh sách cuộn giữa lúc chụp ảnh và lúc bấm. **Đã đóng ngay bằng `Hủy`, không sửa và không lưu bất cứ gì.** Từ đó áp dụng quy tắc: xác minh tên và Agent ID trong dialog trước khi thao tác. Hai Agent kiểm thử (`Kiểm thử Agent Knowledge VNG 2026-08-11` và bản sao) không bị thay đổi.

## Quyết định có chủ đích: không bind PUM cho `GS9 Player Communications`

`agent/kb-allowlist-proposal-2026-08-14.md` từng đề xuất PUM làm nguồn tạm cho Agent này. Khi thực hiện, tôi **không bind** vì rủi ro cụ thể: PUM chứa doanh thu thực, ngân sách marketing, chi phí UA và roadmap chưa công bố; còn Player Communications lại soạn nội dung **hướng ra người chơi**. Nếu retrieval kéo chunk chứa số liệu tài chính vào một bản nháp thông báo thì đó là rò rỉ dữ liệu nội bộ. System Prompt hiện chỉ cấm "invent benefits", không cấm trích số liệu nội bộ.

Nguồn đúng cho vai trò này là `GS9 CFL Plan Version` (nội dung phiên bản sắp phát hành), hiện còn 0 tài liệu. Giữ Agent ở trạng thái không bind cho tới khi KB đó có nội dung và guardrail C1/C2 được duyệt.

## Chưa làm, có lý do

- `GS9 Economy Offer Analyst`: không bind vì KB đúng (`GS9 CFL Item Catalog`, chỉ dữ liệu item-level) chưa tồn tại; `GS9 CFL Item Profile` bị cấm bind do chứa dữ liệu player (blocker P0).
- `GS9 GM Case Investigator`: không bind vì cần case-scoped view theo từng vụ, không có nguồn nào phù hợp.
- `GS9 CS Copilot`: không bind vì chưa có KB FAQ/CS policy nào tồn tại. Mode `Trả lời nhanh` không có tab `Công cụ` (thay bằng tab `Hội thoại`) — khớp đúng tài liệu cũ.
- **System Prompt: không sửa.** Người dùng yêu cầu Việt hóa "mô tả"; System Prompt là trường khác, chứa guardrail đã cân chỉnh và kết thúc bằng `Reply in {{language}}` nên câu trả lời vẫn ra tiếng Việt. Không tự dịch để tránh làm suy giảm hành vi đã thiết kế.
- **Chiến lược truy hồi: giữ mặc định.** Không đổi Top K hay ngưỡng vector/keyword vì chưa có dữ liệu eval; tài liệu thiết kế cũng ghi các ngưỡng này "must be tuned by eval".

## Trạng thái còn lại

- **Chưa chat/runtime test.** Toàn bộ 10 Agent vẫn là **Bị chặn–Chưa xác định** về chất lượng grounding. Gate G6 (chat-test xác nhận `Nguồn tham khảo` đúng và không lộ PII) chưa chạy.
- **G1 chưa xong.** Bốn trong sáu KB vừa bind (`Knowledge VNG AI` ×3 Agent, `PUM`, `Kho Dữ Liệu Tổng Hợp`) vẫn đang share quyền `Chỉnh sửa` cho space `CFL Member` (6 thành viên). Người dùng tự xử lý việc hạ quyền. Bind không làm rủi ro này nặng thêm, nhưng nội dung KB vẫn có thể bị sửa ngoài quy trình build.
- **Sharing Agent vẫn `0`** — không publish/share Agent nào trong phiên này.
- **Nợ tài liệu:** khối `Web actual — 14/08/2026` trong 10 file `agent/GS9 .../config.md` vẫn ghi `Knowledge Base: Không dùng kho tri thức` và `chưa bind KB`. Thông tin đó nay đã sai với 6 Agent. Audit này là bản ghi đúng; cần đồng bộ lại 10 file config theo DEC-034.
