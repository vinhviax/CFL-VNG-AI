# Task 06 — Thay 13 Markdown trong Knowledge VNG AI

Ngày thực hiện: 07/08/2026  
KB: `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`, tenant `10012`)  
Nguồn: 13 module sinh từ master v3.1.1 bằng strict build.

## Kết quả

- Đã nạp đủ 13 Markdown mới; 13/13 có trạng thái **Hoàn tất**.
- Chỉ xóa từng bản cũ sau khi bản mới cùng tên đã hoàn tất và nội dung/đoạn/ảnh MinIO cần thiết được kiểm tra.
- ID 13 bản cũ: `audit/consumer-markdown-old-knowledge-ids-2026-08-07.json`.
- ID 13 bản hiện hành: `audit/consumer-markdown-new-knowledge-ids-2026-08-07.json`.
- Sau replacement và trước cleanup PNG, inventory là 24 tài liệu: 13 MD mới + 11 PNG tạm thời.

## Ngoại lệ file 11

`11-chat-kiem-thu-va-bao-tri.md` bị kẹt hậu xử lý khi dùng parser Markdown **Built-in**. Hai knowledge ID mới lỗi chỉ được xóa sau khi xác nhận bản cũ **Hoàn tất** vẫn tồn tại. Upload lại cùng file với override parser một file là **Simple** đã đạt **Hoàn tất**; nội dung đầy đủ, các đoạn và alt ảnh MinIO được kiểm tra trước khi xóa bản cũ.

ID hiện hành: `58567b75-a702-4f59-b13a-704c019b33c5`. Chi tiết retry: `audit/consumer-markdown-retry-2026-08-07.json`.

Quan sát quan trọng: nút **Hủy** trong hộp tiến trình hủy pipeline và chuyển tài liệu sang **Đã hủy**; nó không chỉ đóng hộp thoại. **Phân tích lại** đã chuyển tài liệu từ **Đã hủy** sang **Đang xử lý** rồi **Đang hoàn tất**, nhưng lượt thử đó vẫn kẹt nên không được dùng làm bản cuối.

## Thay lại file 12 sau review link

Review độc lập phát hiện link `audit/audit-google-drive-connector-2026-08-07.md` đúng ở master nhưng sai khi module được đặt trong thư mục `knowledge-vng/`. Builder được sửa theo TDD để rebase thành `../audit/...`; strict build sinh lại module 12. Bản live `748baf80-3d87-427b-acbf-9de20f8461e8` chỉ bị xóa sau khi bản mới `e58fb441-74cc-44cf-83a9-972954fa697c` **Hoàn tất**, mở được đầy đủ nội dung/ảnh và hiển thị link đã sửa trong nguồn.

Chi tiết: `audit/consumer-markdown-link-fix-2026-08-07.json`.

## Kết luận

**PASS.** Consumer có đúng một bản hiện hành cho mỗi module 00–12; không còn knowledge ID Markdown cũ hoặc retry lỗi trong inventory live.
