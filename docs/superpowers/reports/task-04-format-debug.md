# Task 04 — Điều tra sai định dạng ảnh 01–14

## Hiện tượng tái hiện

- `01-tong-quan-danh-sach-knowledge.png` đã xử lý xong trong KB asset.
- Khi mở **Xem trước**, inventory mạng phát sinh 11 URI MinIO và tất cả đều kết thúc `.jpg`; không có URI `.png` duy nhất như gate Task 4 dự kiến.
- Vì vậy chưa cập nhật `knowledge-vng/image-map.json`.

## Truy vết dữ liệu

1. Local inventory có 25 filename kết thúc `.png`.
2. Pillow và 8 magic bytes xác nhận:
   - 01–14: định dạng thật `JPEG`, signature bắt đầu `FF D8 FF E0 ... JFIF`.
   - 15–25: định dạng thật `PNG`, signature `89 50 4E 47 0D 0A 1A 0A`.
3. Mẫu đang hoạt động `15-google-drive-xac-thuc-service-account.png` trong KB consumer phát sinh:
   - một URI `.png` gốc đã biết trong map;
   - một URI `.jpg` hậu xử lý.
4. Khác biệt duy nhất quyết định là MIME/payload thật của file local, không phải phần mở rộng filename hay cấu hình map.

## Root cause

Ảnh 01–14 đã được lưu dưới tên `.png` nhưng byte payload là JPEG. Knowledge VNG nhận diện nội dung thực và xuất asset gốc/hậu xử lý dạng `.jpg`, làm mất tiêu chí lựa chọn “một URI `.png` duy nhất”.

## Giả thuyết sửa tại nguồn

Transcode lossless theo pixel 01–14 từ JPEG sang PNG thật, giữ nguyên filename và kích thước. Sau khi nạp bản đã sửa, KB asset phải phát sinh đúng một URI `.png` gốc; các `.jpg` còn lại được xem là hậu xử lý và bỏ qua.

## Gate kiểm chứng

- Regression test `test_local_png_assets_have_png_signature` phải đỏ trước khi sửa và xanh sau transcode.
- Giữ backup nguyên byte JPEG cũ trong audit để có thể phục hồi.
- Thử bản PNG đã sửa của ảnh 01 trước; chỉ nạp tiếp 02–14 khi ảnh 01 phát sinh URI `.png` duy nhất.
- Không sửa image map cho tới khi đủ 25 URI hợp lệ.

## Kết quả kiểm chứng

- Đã backup nguyên byte 14 JPEG cũ tại `audit/image-assets-original-jpeg-mislabeled-2026-08-07/`.
- Đã transcode 01–14 thành PNG thật, giữ nguyên filename và kích thước pixel; regression test chuyển từ RED sang GREEN.
- Bản thử ảnh 01 dung lượng `554.0 KB` sinh đúng một URI gốc `.png`: `minio://knowledge-base-prd/10012/exports/78c9450c-2273-45fe-84b1-09f217328b53.png`.
- Sau khi giả thuyết được xác nhận, đã nạp 02–14 và thu đủ 25 URI `.png` duy nhất cùng 25 knowledge ID.
- Chỉ sau khi kiểm tra đủ 25 tên, 25 URI không trùng, đúng tenant và đúng đuôi `.png` mới cập nhật `knowledge-vng/image-map.json` một lần.
- Đã xóa tuần tự 14 bản cũ theo bộ ba điều kiện **tên file + dung lượng cũ + knowledge ID**; mỗi lần chỉ xác nhận xóa khi hàng PNG mới cùng tên vẫn còn.
- Kiểm kê live sau dọn dẹp: **25 tài liệu / 25 PNG / 0 MD**, không còn dung lượng nào của 14 bản JPEG cũ.
- ID 25 bản PNG mới được lưu tại `audit/image-assets-knowledge-ids-2026-08-07.json`; ID 14 bản cũ đã xóa được lưu tại `audit/image-assets-replaced-knowledge-ids-2026-08-07.json`.
