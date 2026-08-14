# Mẫu tài liệu có ảnh cho Knowledge VNG

> **Trạng thái:** Nội dung minh họa, phải thay bằng quy trình nghiệp vụ đã được duyệt trước khi đưa vào production.  
> **Chủ sở hữu mẫu:** Studio 9  
> **Ngày kiểm tra kỹ thuật:** 06/08/2026  
> **Ngày xem lại:** 06/11/2026

## Mục đích

Mẫu này minh họa cấu trúc một file Document dễ truy hồi và có ảnh có thể hiển thị trực tiếp trong câu trả lời chat.

## Khi nào dùng

- Dùng cho hướng dẫn nhiều bước, SOP hoặc tài liệu cần giải thích bối cảnh.
- Không dùng thay FAQ khi mỗi câu hỏi cần được quản lý như một mục độc lập.

## Quy trình chuẩn bị

1. Viết một H1 duy nhất mô tả đúng chủ đề file.
2. Chia nội dung thành các H2 theo ý định người hỏi.
3. Ghi rõ điều kiện áp dụng, ngoại lệ và người chịu trách nhiệm.
4. Tải ảnh lên KB test như một nguồn riêng và chờ xử lý hoàn tất.
5. Lấy URI `minio://` trong đoạn nguồn do hệ thống tạo.
6. Đặt URI đó vào cú pháp ảnh Markdown, tải file MD lên rồi kiểm thử trong chat.

## Kết quả mong đợi

Chat trả lời dựa trên nội dung file và hiển thị ảnh trong phần trả lời, không chỉ nêu tên ảnh hoặc mô tả ảnh bằng chữ.

<!-- LOCAL_ASSET: assets/chat-hien-thi-anh-minio.png -->
![Ví dụ câu trả lời Knowledge VNG hiển thị ảnh lấy từ URI MinIO](minio://knowledge-base-prd/10012/exports/07dbea9e-18be-42b8-b8c8-2fd0edf4bc4c.jpg)

## Không áp dụng cho

- Đường dẫn tương đối như `assets/ten-anh.png` khi mục tiêu là để chat render ảnh.
- Ảnh chưa được tải lên và chưa có URI nội bộ của Knowledge VNG.
- Ảnh chứa token, mật khẩu, khóa API, thông tin cá nhân hoặc dữ liệu nhạy cảm.

## Câu hỏi kiểm thử

- Tài liệu này hướng dẫn quy trình nào?
- Hãy liệt kê sáu bước chuẩn bị và hiển thị ảnh minh họa.
- Vì sao đường dẫn ảnh tương đối không đủ để chat hiển thị ảnh?

## Tiêu chí đạt

- Nguồn tham khảo trỏ đúng file này.
- Câu trả lời không bịa thêm bước ngoài tài liệu.
- Ảnh xuất hiện trong DOM của câu trả lời.
- Không có dữ liệu nhạy cảm trong ảnh hoặc nội dung.
