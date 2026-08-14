# Review độc lập Task 03 — Nạp 25 ảnh vào KB asset mới

**Verdict:** APPROVED  
**Cho phép Task 4:** CÓ

## Tóm tắt

Task 03 đáp ứng các tiêu chí trong plan. `task-03-live-upload.md` ghi đủ bằng chứng để kết luận phiên thao tác đã mở đúng KB asset, baseline là 0 Documents, một lượt upload trả toast `25 thành công / 0 lỗi`, inventory live sau upload có 25 tài liệu mang tên `.png` và không có `.md`, đồng thời chưa tác động KB consumer `Knowledge VNG AI`.

Inventory local được kiểm chứng độc lập: `knowledge-vng/assets/` có đúng 25 file, toàn bộ mang đuôi `.png`, tên duy nhất, đủ tiền tố `01`–`25`, không có file ngoài `.png` và không có file rỗng. Review không dùng browser theo phạm vi được giao; các kết luận live dựa trên bản ghi thao tác trực tiếp trong report, còn phần local được đối chiếu lại từ filesystem.

## Findings theo severity

### 🔴 Blocker

Không có.

### 🟡 Suggestion / rủi ro cần theo dõi ở Task 4

- 14 file đầu (`01`–`14`) mang tên `.png` nhưng magic bytes là JPEG/JFIF; 11 file `15`–`25` có magic bytes PNG chuẩn. Điểm này không làm Task 03 thất bại vì tiêu chí inventory trong plan được xác định theo filename `.png`, upload đã thành công và live inventory đã đối chiếu đủ 25 tên. Tuy nhiên Task 4 không được suy diễn URI từ phần mở rộng local: với từng tài liệu phải chờ trang chi tiết sinh asset, chỉ nhận đúng một URI MinIO kết thúc `.png`, và dừng nếu không có URI PNG duy nhất như plan yêu cầu.

### 💭 Nit

Không có.

## Đối chiếu tiêu chí Task 03

| Tiêu chí | Bằng chứng | Kết luận |
|---|---|---|
| Đúng KB asset | Report ghi tên `Knowledge VNG - Image Assets`, ID `6da8657c-dd96-4170-a698-074043475014`, tenant `10012` và mô tả `Chứa Image Assets KB VNG`, khớp plan | Đạt |
| Baseline trước mutation | Report ghi `0` Documents trước upload | Đạt |
| Đúng batch local | Report ghi chọn một lượt 25 đường dẫn từ `knowledge-vng/assets/`; kiểm tra độc lập thấy 25 tên duy nhất, đủ `01`–`25` | Đạt |
| Kết quả upload | Nút trước submit là `Tải lên 25 tệp`; toast sau submit là `25 thành công / 0 lỗi` | Đạt |
| Inventory live | Sidebar là `Tất cả tài liệu 25`; đối chiếu DOM không thiếu tên local và không có tài liệu `.md` | Đạt: 25 tên `.png`, 0 `.md` |
| Không đụng consumer | Report ghi chưa upload/thay Markdown và chưa xóa 11 PNG trong `Knowledge VNG AI` | Đạt |
| Chưa vượt sang Task 4 | Report ghi chưa sửa `knowledge-vng/image-map.json`; trạng thái local hiện vẫn là map cũ với 25 entry, `knowledge_base: Mixed; see provenance` và chưa có `knowledge_base_id` mới | Đạt |

## Gate Task 4

Task 4 được phép bắt đầu. Các điều kiện dừng trong plan vẫn bắt buộc:

1. Chờ từng trang chi tiết tạo asset PNG; trạng thái `Chờ xử lý`/`Đang xử lý` ngay sau upload chưa phải bằng chứng URI hoàn tất.
2. Với từng ảnh, đối chiếu heading với filename và ghi đúng `knowledge_id` trước khi lấy URI.
3. Chỉ dùng URI duy nhất dạng `minio://knowledge-base-prd/10012/exports/<uuid>.png`; bỏ asset `.jpg` hậu xử lý/OCR.
4. Chỉ sửa map sau khi đã có đủ 25 filename, 25 URI không trùng, đúng tenant và đúng đuôi `.png`; không cập nhật từng phần.
5. Tạo snapshot mapping cũ theo Task 4 trước khi sửa map và tiếp tục không upload, thay thế hoặc xóa tài liệu trong `Knowledge VNG AI`.

## Kết luận

Không có finding chặn. Task 03 được **APPROVED** và **cho phép bắt đầu Task 4** với các điều kiện kiểm chứng URI nêu trên.
