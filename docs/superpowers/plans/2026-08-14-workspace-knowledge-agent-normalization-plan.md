# Kế hoạch chuẩn hóa workspace Knowledge Base VNG

**Ngày:** 14/08/2026

## Mục tiêu

- Dùng `J:\My Drive\CFL\VNG AI\Knowledge Base VNG` làm root dự án.
- Giữ nguyên tên thư mục theo tên KB trên Web: `knowledge/GS9 Knowledge VNG AI` và `knowledge/GS9 Knowledge VNG - Image Assets`.
- Dùng `knowledge/` để mirror nội dung KB trên Web; dùng `agent/` để quản lý cấu hình/tài liệu Agent về sau.
- Loại bỏ đường dẫn runtime `knowledge-vng/` cũ mà không thay đổi nội dung 20 Markdown, 49 ảnh hoặc URI MinIO.
- Dọn cache, bản build trùng và ảnh tạm đã phát hành; lưu hồ sơ audit cũ theo cách có thể truy nguyên.

## Trình tự thực hiện

1. Kiểm kê dependency và xác minh inventory 20 Markdown, 49 PNG, 49 URI.
2. Viết test khóa đường dẫn mới và xác nhận test thất bại trước khi sửa builder.
3. Phục hồi master bị thất lạc từ 20 module sinh hiện hành bằng phép biến đổi xác định; kiểm tra build vòng lặp không làm lệch nội dung.
4. Sửa builder/test để đọc map và ghi module vào hai thư mục mang tên KB Web.
5. Chạy strict build và toàn bộ unit test.
6. Chỉ sau khi core pass: xóa cache/bản build trùng/ảnh tạm đã có asset phát hành; chuyển bộ audit upload cũ vào `audit/archive/`.
7. Cập nhật `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md`, `DECISIONS.md` và kiểm kê cuối.

## Rollback

- Không sửa hoặc xóa 20 module/49 PNG trước khi có bản backup nguyên byte.
- Nếu strict build không tái tạo đúng module, khôi phục backup và giữ nguyên layout dữ liệu hiện tại.
- Không đụng tới credential, file nguồn dữ liệu CFL hoặc tài nguyên live trên Web.
