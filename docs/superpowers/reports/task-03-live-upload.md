# Task 03 — Nạp 25 ảnh vào KB asset mới

**Trạng thái:** PASS — chờ review độc lập

## Đích live đã đối chiếu

- Tên: `Knowledge VNG - Image Assets`
- Knowledge Base ID: `6da8657c-dd96-4170-a698-074043475014`
- Tenant: `10012`
- Mô tả hiển thị: `Chứa Image Assets KB VNG`
- Baseline trước upload: `0` Documents.

## Inventory local

- `knowledge-vng/assets/` có đúng 25 file `.png`.
- Tên duy nhất, theo thứ tự từ `01-tong-quan-danh-sach-knowledge.png` đến `25-google-drive-dong-bo-thanh-cong.png`.

## Thao tác và kết quả

1. Mở `Tải tài liệu lên` trong đúng KB asset.
2. Chọn một lượt đúng 25 đường dẫn tuyệt đối từ `knowledge-vng/assets/`.
3. Không mở hoặc thay đổi `Xử lý nâng cao`; giữ cấu hình mặc định KB.
4. Trước submit, nút hiển thị `Tải lên 25 tệp` và danh sách đủ 25 filename.
5. Sau submit, toast hiển thị `25 thành công / 0 lỗi`.
6. Sidebar hiển thị `Tất cả tài liệu 25`.
7. Đối chiếu DOM sau upload: không thiếu filename nào trong 25 tên local; không có tài liệu `.md`.

## Trạng thái pipeline

Ngay sau upload, các ảnh lần lượt ở `Chờ xử lý`/`Đang xử lý`. Task 04 chỉ thu URI sau khi từng trang chi tiết đã tạo asset PNG; không coi trạng thái xử lý ban đầu là bằng chứng URI hoàn tất.

## Mutation chưa thực hiện

- Chưa upload hoặc thay thế Markdown trong `Knowledge VNG AI`.
- Chưa xóa 11 PNG khỏi `Knowledge VNG AI`.
- Chưa sửa `knowledge-vng/image-map.json`.
