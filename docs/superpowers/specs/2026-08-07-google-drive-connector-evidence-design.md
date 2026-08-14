# Thiết kế bổ sung bằng chứng Google Drive connector

**Ngày:** 07/08/2026  
**Phạm vi:** cập nhật tài liệu và bằng chứng; không lưu service-account JSON/private key; không thao tác thêm trên KB ngoài phạm vi người dùng đang thực hiện.

## Mục tiêu

Ghi lại quy trình Google Drive connector từ xác thực, chọn tài nguyên, cấu hình chiến lược đến lượt đồng bộ đầu tiên thành công. Nội dung phải hữu ích cho người đọc human, đồng thời giữ quy tắc master là nguồn chuẩn và mở rộng gói phân phối thành 13 Markdown/HTML offline.

## Phương án được chọn

1. Sao chép toàn bộ ảnh người dùng cung cấp vào `audit/evidence/` với tên có ngày và ý nghĩa rõ ràng.
2. Tạo audit riêng ngày 07/08/2026, phân biệt điều đã quan sát thành công với hành vi chưa được thử.
3. Tạo hướng dẫn human riêng trong `docs human/`, dùng ảnh local để mô tả quy trình và cấu hình khuyến nghị.
4. Cập nhật module 08 tại master bằng nội dung đã kiểm chứng, đồng thời tạo module độc lập `12-ket-noi-google-drive.md` để người dùng có thể nạp riêng lên KB.
5. Cập nhật ma trận kiểm chứng, trạng thái và handoff; sinh lại 13 module và HTML bằng builder. Bản local có thể được sinh trong lúc chờ mapping, nhưng bản bàn giao cho chat ảnh phải qua build nghiêm ngặt.

## Phân loại bằng chứng

### Đã kiểm chứng ngày 07/08/2026

- Google Drive dùng service-account JSON và scope `drive.readonly`.
- Kết nối thất bại khi Google Drive API chưa bật; kết nối được sau khi bật API.
- Với My Drive, có thể để trống Shared Drive ID và cấp Viewer cho email service account.
- Bước Tài nguyên hiển thị cây thư mục/tệp, trạng thái chọn một phần và nhãn loại chưa hỗ trợ.
- Bước Chiến lược có lịch phút/giờ/ngày/tuần/tháng; tăng dần/toàn bộ; ghi đè/bỏ qua; regex tên tệp; tag; cấu hình xử lý nâng cao; parser theo loại; đồng bộ xóa.
- Nút `Tạo & đồng bộ ngay` tạo nguồn ở trạng thái `Đã kết nối`; lượt đầu quan sát được có kết quả `Thành công`.

### Có điều kiện

- Danh sách parser Excel tùy chỉnh `FPA · ...` là cấu hình tenant đã quan sát, không phải mặc định sản phẩm.
- Parser, VLM, ASR, OCR và sinh câu hỏi phụ thuộc cấu hình KB/model và loại tệp.

### Chưa xác định

- Kết quả thực tế của các chu kỳ incremental/full tiếp theo.
- Hành vi khi sửa, đổi tên, di chuyển, xóa hoặc thu hồi quyền ở Google Drive.
- Hiệu lực thực tế của regex, tag theo đường dẫn, chiến lược xung đột và đồng bộ xóa trên dữ liệu đối chứng.

## Chiến lược ảnh

- Audit và hướng dẫn human giữ toàn bộ ảnh local.
- 13 module dùng ảnh local cho bản đọc và URI MinIO cho bản nạp để chat có thể render.
- Trước khi công nhận module Google Drive sẵn sàng cho chat ảnh, phải tải 11 ảnh lên KB được phép, lấy URI MinIO, cập nhật `knowledge-vng/image-map.json`, rồi chạy build nghiêm ngặt.

## An toàn

- Không sao chép hoặc chụp nội dung JSON key/private key.
- Email service account có thể xuất hiện trong audit kỹ thuật nhưng không được coi là bí mật xác thực.
- Hướng dẫn khuyến nghị quyền Viewer và không chọn thư mục chứa credential như `keys`.
- Không khẳng định P4 hoàn tất chỉ từ một lượt đồng bộ đầu tiên.

## Tiêu chí hoàn tất

- Ảnh bằng chứng tồn tại và mọi link ảnh trong audit/human guide đều hợp lệ.
- Master ghi đúng trạng thái Google Drive và không còn nói bước 3–4 bị chặn hoàn toàn.
- 13 module và HTML được sinh lại; kết quả bàn giao cuối phải qua build nghiêm ngặt.
- Toàn bộ test hiện có đạt; asset/mapping MinIO hiện hữu vẫn nhất quán.
- `STATUS.md` và `HANDOFF.md` phản ánh P3 hoàn tất cho Google Drive, P4 còn mở.
