<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 02 - Tạo KB bằng chế độ Nhanh và Nâng cao {#02-tao-kb-nhanh-va-nang-cao}

## Bạn sẽ biết gì sau khi đọc

- Khác biệt giữa **Nhanh** và **Nâng cao**.
- Những lựa chọn cần chốt trước khi có nội dung.
- Cách tránh tin nhầm banner tóm tắt cấu hình.

## Chế độ Nhanh

Form Nhanh hỏi các trường chính:

- **Loại:** Tài liệu hoặc FAQ.
- **Tên** và **Mô tả**.
- **Mô hình chat / tóm tắt**.
- **Mô hình Embedding**.

Các lựa chọn RAG/Wiki, parser, phân đoạn, VLM, ASR hoặc cách lập chỉ mục FAQ được ẩn và nhận cấu hình khuyến nghị. Chế độ này phù hợp để tạo KB test nhanh, nhưng không thay thế bước mở lại **Cài đặt** để kiểm tra.

## Chế độ Nâng cao

Chế độ Nâng cao hiển thị toàn bộ tab cấu hình theo loại KB. Với Tài liệu, tab **Tổng quan** cho thấy loại và chiến lược RAG/Wiki; với FAQ, tab này có cấu hình lập chỉ mục câu hỏi.

<!-- LOCAL_ASSET: ./image-02-cau-hinh-tong-quan-document.png -->
![Tab Tổng quan của KB Tài liệu với loại, RAG, Wiki, tên và mô tả](minio://knowledge-base-prd/10012/exports/f762c7c4-60b4-48fe-bfd5-b48a5aba48b5.png)

*Ảnh 02.1 - Tab Tổng quan của KB Tài liệu đã có nội dung; một số lựa chọn bị khóa.*

## Những gì bị khóa và khi nào

Loại KB bị khóa ngay sau khi tạo. Khi KB Tài liệu đã có nội dung, loại KB, chiến lược lập chỉ mục và model Embedding hiển thị vô hiệu hóa; giao diện yêu cầu xóa tài liệu nếu muốn thay đổi cấu trúc này.

**Riêng ở FAQ, banner nói khóa nhưng control vẫn dùng được.** Banner cảnh báo cấu hình lập chỉ mục bị khóa khi KB đã có nội dung, nhưng hai lựa chọn **Chỉ câu hỏi / Câu hỏi + trả lời** và **Gộp / Tách** vẫn bấm, lưu và giữ giá trị sau khi mở lại. Vì vậy:

- Không cần xóa toàn bộ FAQ chỉ để đổi hai lựa chọn này.
- Sau mỗi lần đổi, chạy lại **Kiểm tra tìm kiếm** vì không có bảo đảm kết quả cũ giữ nguyên.
- Coi loại KB và Embedding là lựa chọn nền tảng cần chốt trước.

## Cảnh báo về banner cấu hình khuyến nghị

Banner tóm tắt của chế độ Nhanh có thể không khớp cấu hình thật. Đã có trường hợp banner ghi “sinh câu hỏi đang bật” nhưng khi mở cấu hình thì **Sinh câu hỏi** ở trạng thái tắt. Nguyên tắc: banner chỉ là bản tóm tắt; trạng thái từng control trong **Cài đặt** mới là thứ đáng tin.

## Quy trình tạo an toàn

1. Tạo KB test bằng Nâng cao nếu cần kiểm soát đầy đủ ngay từ đầu.
2. Chọn loại KB và Embedding.
3. Với Tài liệu, quyết định bật RAG, Wiki hoặc cả hai.
4. Với FAQ, chọn phạm vi nội dung được index và cách xử lý biến thể câu hỏi.
5. Đặt tên có môi trường và mục đích, ví dụ `TEST - Payment FAQ - 2026Q3`.
6. Lưu cấu hình, mở lại từng tab và chụp trạng thái trước khi nạp dữ liệu.
7. Nạp một mẫu nhỏ, kiểm thử, rồi mới mở rộng.

## Đừng dùng tên model như một quy tắc cố định

Danh sách model có thể đổi, và có model hiện trong dropdown nhưng backend không chấp nhận. Nếu không thấy model mong muốn, tải lại trang trước khi kết luận là lỗi. Hãy chọn model đang lưu được trong chính KB đó và tránh viết quy trình phụ thuộc vĩnh viễn vào một tên model.
