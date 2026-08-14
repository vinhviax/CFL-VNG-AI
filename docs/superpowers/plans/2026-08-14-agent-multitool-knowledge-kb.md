# Kế hoạch cấu hình multi-tool và KB GS9 CFL Knowledge Agent

**Mục tiêu:** Audit cấu hình thực tế, cấu hình 10 Agent custom theo nguyên tắc least privilege, cập nhật đầy đủ artifact local, tạo KB Markdown về 6 Agent mặc định và 10 Agent custom, rồi tạo/upload KB `GS9 CFL Knowledge Agent` trên VNG AI.

**Phạm vi live được phép thay đổi:** 10 Agent custom đã tạo và một KB mới tên `GS9 CFL Knowledge Agent`. Không sửa 6 Agent mặc định; không share/publish; không đụng `Data Private Weapon`, credential, token, cookie, local/session storage hoặc private API.

**Nguyên tắc kiến trúc:** Tool được bật theo nhiệm vụ, dữ liệu và quyền; không bật tất cả. KB `GS9 CFL Knowledge Agent` là meta-KB cho Human hiểu/chọn/dùng Agent, không mặc nhiên là corpus nghiệp vụ cho LiveOps, CS, GM, Product hoặc Data.

**Checkpoint:** Workspace không phải Git repository; audit, snapshot Web trước/sau, ID live và kết quả kiểm tra cấu trúc là bằng chứng phục hồi.

## Task 1 — Audit nguồn dữ liệu và tool surface

- Đối chiếu 6 audit Agent mặc định, 10 config custom và danh sách tool hiển thị trong UI.
- Kiểm tra read-only các KB local có thể liên quan; loại trừ hoàn toàn dữ liệu private, credential và nguồn chưa rõ quyền.
- Lập ma trận `Agent → tool → dữ liệu cần thiết → trạng thái Đã kiểm chứng/Có điều kiện/Bị chặn`.

## Task 2 — Chốt cấu hình role-based và snapshot trước mutation

- Với mỗi Agent, ghi current Web actual và target multi-tool.
- Mặc định dùng `Suy nghĩ`, `Lập kế hoạch (todo)`, `Hỏi người dùng` khi phù hợp.
- Chỉ bật RAG/Wiki/Data/SQL/Product Catalog khi tool có ích và nguồn/quyền đã được kiểm chứng.
- Giữ Human approval cho gửi tin, thay dữ liệu, thao tác account/economy hoặc vận hành live.

## Task 3 — Cấu hình 10 Agent custom trên Web

- Chỉ dùng trình duyệt tích hợp Codex và UI công khai.
- Sửa từng Agent, lưu, mở lại, kiểm chứng persistence trước khi chuyển Agent kế tiếp.
- Không sửa prompt ngoài phần tối thiểu cần phản ánh tool/guardrail; không share/publish/tắt/xóa/clone.
- Ghi ID, cấu hình trước/sau và mục chưa xác định vào audit.

## Task 4 — Cập nhật artifact trong `agent/`

- Cập nhật catalog/README, 10 config và 10 handoff theo Web actual đã kiểm chứng.
- Bổ sung ma trận tool, lý do bật/tắt, dependency dữ liệu, Human approval và giới hạn runtime chưa test.
- Không ghi cấu hình kế hoạch như thể đã live.

## Task 5 — Tạo local KB `knowledge/GS9 CFL Knowledge Agent/`

- Chỉ tạo Markdown, không đưa PNG/private data/credential vào KB.
- Bao phủ đủ 16 Agent: 6 mặc định (read-only audit) và 10 custom (Web actual).
- Có tài liệu tổng quan, cách chọn Agent, cách dùng/an toàn, ma trận tool/dữ liệu, giới hạn và hồ sơ riêng từng Agent.
- Mọi claim phải gắn mức bằng chứng; ID nội bộ chỉ ghi khi cần quản trị, không yêu cầu Human dùng ID để chat.

## Task 6 — Kiểm tra local KB

- Kiểm tra inventory, tên file, liên kết nội bộ, UTF-8, không có file ngoài Markdown.
- Quét pattern credential/private-data và đối chiếu đủ 16 Agent.
- Review độc lập nội dung để phát hiện mâu thuẫn giữa Web actual, config local và KB.

## Task 7 — Tạo và upload Web KB

- Tạo KB đúng tên `GS9 CFL Knowledge Agent` qua UI, để phạm vi mặc định `Của tôi`/sharing 0 nếu UI không bắt buộc khác.
- Upload đúng toàn bộ Markdown từ local mirror bằng thao tác thêm mới; không dùng thay toàn bộ.
- Chờ tất cả file xử lý hoàn tất; kiểm chứng tên KB, ID nếu UI hiển thị, tổng file, loại file và trạng thái.
- Không bind KB vào Agent nghiệp vụ chỉ để mở khóa RAG; việc bind chỉ thực hiện nếu đúng vai trò và được chứng minh trong Task 1–2.

## Task 8 — Audit và bàn giao

- Ghi audit cấu hình multi-tool và audit tạo/upload KB.
- Cập nhật `STATUS.md`, `HANDOFF.md`, và `DECISIONS.md` nếu có quyết định kiến trúc bền vững.
- Chạy lại kiểm tra cấu trúc cuối, mở lại ngẫu nhiên các Agent và KB để xác minh.
- Báo rõ phần Đã kiểm chứng, Có điều kiện, Bị chặn–Chưa xác định và các hành động vẫn cần Human approval.
