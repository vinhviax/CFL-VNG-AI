<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 00 - Giới thiệu và quick start {#00-gioi-thieu-va-quick-start}

## Bạn sẽ biết gì sau khi đọc

- Knowledge Base giải quyết việc gì.
- Khi nào chọn **Tài liệu**, khi nào chọn **FAQ**.
- Luồng tối thiểu từ tạo kho đến câu trả lời đã kiểm thử.

## Knowledge Base là gì

Knowledge Base, viết tắt là KB, là kho nội dung có cấu trúc để hệ thống tìm và dùng làm nguồn khi trả lời. Knowledge VNG hiện có hai loại chính:

- **Tài liệu:** nạp file hoặc soạn nội dung dài; hệ thống phân tích file, chia đoạn và có thể tạo Wiki/Graph.
- **FAQ:** lưu từng mục câu hỏi và câu trả lời; có công cụ kiểm tra tìm kiếm, nhập và xuất dữ liệu.

Hai loại này phục vụ hai bài toán khác nhau. Không cần ép toàn bộ tri thức vào một KB duy nhất.

<!-- LOCAL_ASSET: ./image-01-tong-quan-danh-sach-knowledge.png -->
![Trang danh sách Knowledge Base và nút tạo Knowledge Base mới](minio://knowledge-base-prd/10012/009e72d5-a746-48b4-b594-4d286ed2c547/d6746417-8921-4501-b61f-372b0ff7e65b.png)

*Ảnh 00.1 - Trang Knowledge hiển thị danh sách kho và nút `Knowledge Base mới`.*

## Chọn loại nào

| Tình huống | Chọn | Lý do |
|---|---|---|
| Hướng dẫn dài, SOP, chính sách, tài liệu dự án | Tài liệu | Cần parser, phân đoạn và truy hồi theo nội dung |
| Onboarding cần đọc theo chủ đề liên kết | Tài liệu + Wiki | Wiki tổng hợp thành các trang có liên kết |
| Câu trả lời phải được quản lý theo từng mục | FAQ | Mỗi Q&A là một đơn vị độc lập |
| Có sẵn bảng câu hỏi, biến thể và câu trả lời | FAQ | Nhập JSON, CSV hoặc Excel thuận tiện |
| Vừa có quy định cứng vừa có tài liệu giải thích | Hai KB | FAQ cho câu chuẩn; Tài liệu cho bối cảnh |

## Quick start 8 bước

1. Xác định người dùng sẽ hỏi gì và ai chịu trách nhiệm nội dung.
2. Chọn **Tài liệu** hoặc **FAQ** trước khi nạp dữ liệu.
3. Chuẩn hóa nguồn: bỏ bản cũ, chia chủ đề, đặt heading rõ.
4. Tạo KB test và chọn model đang dùng được.
5. Mở **Cài đặt** để kiểm tra lại cấu hình thật, kể cả khi dùng chế độ Nhanh.
6. Nạp một bộ nhỏ đại diện trước, chờ trạng thái **Hoàn tất**.
7. Dùng **Trò chuyện** hoặc **Kiểm tra tìm kiếm** để chạy câu hỏi đúng, câu hỏi diễn đạt lại, câu ngoài phạm vi và câu dễ nhầm.
8. Chỉ mở rộng dữ liệu sau khi đã xem nguồn truy hồi và sửa được lỗi.

## Bản đồ màn hình

Knowledge VNG có hai bộ tab khác nhau:

- **Trong Cài đặt:**
  - Tài liệu: **Tổng quan, Mô hình, Xử lý, Chia sẻ, Nguồn dữ liệu**.
  - FAQ: **Tổng quan, Mô hình, Chia sẻ, Nguồn dữ liệu**.
- **Trong trang làm việc:** **Documents, Wiki, Graph** xuất hiện ở cả hai loại. Với FAQ, Wiki và Graph chỉ hiện thông báo chưa bật chứ chưa có chức năng thật.

Đừng nhầm tab **Xử lý** trong Cài đặt với tab **Documents** ở trang làm việc.

## Ba nguyên tắc trước khi dùng thật

1. **Thử trên KB test.** Không dùng thao tác nhập thay toàn bộ trên kho đang phục vụ người dùng.
2. **Đo bằng câu hỏi thật.** Một file được xử lý thành công chưa chứng minh câu trả lời đúng.
3. **Giữ bản nguồn và bản xuất.** KB là lớp phân phối, không thay thế kho lưu trữ có phiên bản.
