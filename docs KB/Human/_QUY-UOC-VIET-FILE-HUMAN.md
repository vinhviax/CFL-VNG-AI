# Quy ước viết file trong `docs KB/Human`

Đọc trước khi thêm hoặc sửa bất kỳ file nào ở đây.

## Đây là nguồn nội dung lên Web

File trong thư mục này được build thành tài liệu trong `knowledge/`, rồi đồng bộ lên Knowledge Base để người dùng chat. Viết sai ở đây là sai trên sản phẩm.

Bản chi tiết cho Dev nằm ở `docs KB/Dev` — thư mục đó **không** lên Web.

## Đối tượng đọc

Người dùng cuối đang làm việc trên nền tảng VNG AI. Họ hỏi: *"tôi phải làm gì, bấm ở đâu, chọn cái nào?"*

Họ **không** hỏi: hệ thống chạy thế nào bên trong, đã test ra sao, ai quyết định điều này.

## Đặt tên file

`<TínhNăng>-<NN>-<chu-de>.md` — ví dụ `KB-00-gioi-thieu-va-quick-start.md`, `Agent-13-tong-quan-va-kien-truc.md`.

Số thứ tự giữ trật tự đọc. Tiền tố cho biết thuộc tính năng nào. Khi build, tiền tố được đổi thành `doc-` để khớp quy ước tài liệu trên Web (DEC-042).

## Phải có

- Câu mở đầu nói rõ đọc xong biết làm được gì.
- Các bước thao tác theo thứ tự, đủ để làm theo mà không phải hỏi ai.
- Ảnh minh họa đặt ngay cạnh bước mà nó minh họa.
- Cảnh báo thực dụng: cái gì làm hỏng dữ liệu, cái gì không hoàn tác được.

## Tuyệt đối không đưa vào

| Không viết | Lý do |
|---|---|
| Mã `DEC-xxx` | Người dùng không tra sổ quyết định |
| Link tới `audit/`, `docs/superpowers/` | Thư mục nội bộ, người dùng không có |
| *"Đã kiểm chứng ngày…"*, *"chưa kiểm chứng"* | Nhật ký thử nghiệm, không phải hướng dẫn |
| Tên file config, ID tài liệu, UUID | Chi tiết vận hành nội bộ |
| Lịch sử đổi kiến trúc, lý do từng chọn cách khác | Người dùng chỉ cần cách làm hiện hành |

Nếu một thông tin chỉ hữu ích cho người sửa hệ thống thì nó thuộc `docs KB/Dev`, không thuộc đây.

## Ảnh

Giữ nguyên đường dẫn ảnh dạng `![mô tả](<knowledge/GS9 Knowledge VNG AI/image-NN-....png>)`. Builder tự thay bằng URI MinIO khi sinh tài liệu. Không tự gõ URI `minio://` vào đây.

Không xoá ảnh khi rút gọn nội dung — ảnh là phần giá trị nhất với người đọc.
