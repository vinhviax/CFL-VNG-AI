<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 01 - Chuẩn bị nội dung nguồn {#01-chuan-bi-noi-dung}

## Bạn sẽ biết gì sau khi đọc

- Cách làm sạch file trước khi nạp.
- Cấu trúc Markdown thân thiện với người đọc và hệ thống truy hồi.
- Cách chuẩn bị ảnh để vừa đọc offline vừa hiển thị trong chat Knowledge VNG.

**Kiểm chứng giao diện: 06/08/2026.**

## Chất lượng nguồn quyết định giới hạn câu trả lời

Parser và model có thể giúp trích xuất, nhưng không tự giải quyết được tài liệu mâu thuẫn, thiếu ngữ cảnh hoặc đã lỗi thời. Trước khi nạp, hãy trả lời bốn câu:

1. Đây có phải bản đang hiệu lực không?
2. Mỗi chủ đề có một nơi chịu trách nhiệm rõ không?
3. Thuật ngữ, mã lỗi, thời gian và phạm vi áp dụng có được viết trực tiếp không?
4. Người đọc có thể hiểu một mục khi nó bị tách ra khỏi phần trước không?

## Checklist dọn file

- Xóa bản nháp, bản trùng và thông tin đã hết hiệu lực.
- Tách file quá dài theo nhóm chức năng hoặc hành trình người dùng.
- Đặt một tiêu đề cấp 1 cho mỗi file; dùng tiêu đề cấp 2-3 cho các phần.
- Viết đủ chủ ngữ và phạm vi. Tránh các câu như “làm như trên”, “trường hợp này”, “phiên bản mới”.
- Đưa điều kiện áp dụng, ngoại lệ và kết quả mong đợi vào cùng mục với quy trình.
- Với bảng, lặp lại tên đối tượng trong hàng thay vì dựa hoàn toàn vào vị trí cột.
- Ghi ngày hiệu lực và chủ sở hữu nội dung nếu tài liệu thay đổi thường xuyên.

## Mẫu Markdown cho KB Tài liệu

```markdown
# Người chơi không vào được game, báo Connection timeout

Ngày hiệu lực: 2026-08-06
Chủ sở hữu: LiveOps

# Dấu hiệu nhận biết

- Mã lỗi: CONNECTION_TIMEOUT
- Xảy ra sau khi bấm Đăng nhập.

# Nguyên nhân đã ghi nhận

1. Máy chủ đang bảo trì.
2. Kết nối đến cụm đăng nhập bị gián đoạn.

# Cách xử lý, theo thứ tự

1. Kiểm tra trang trạng thái vận hành.
2. Nếu không có sự cố chung, yêu cầu người chơi đổi mạng và thử lại.

# Kết quả mong đợi

Người chơi vào được màn hình chọn máy chủ.

# Không áp dụng cho

Không dùng quy trình này cho lỗi INVALID_TOKEN.
```

## Ảnh trong file Markdown: hai mục đích, hai đường dẫn

Đường dẫn tương đối như sau hữu ích khi con người mở bộ file trên máy:

```markdown
![Màn hình cấu hình](assets/02-cau-hinh-tong-quan-document.png)
```

Tuy nhiên, phép thử trực tiếp cho thấy chat Knowledge VNG **không render ảnh** từ đường dẫn tương đối, dù file MD và ảnh đều đã được nạp riêng.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/14-chat-khong-hien-thi-duong-dan-tuong-doi.png -->
![Câu trả lời có mô tả ảnh nhưng không render ảnh khi Markdown dùng đường dẫn tương đối](minio://knowledge-base-prd/10012/exports/227784d8-277b-4198-a8c5-77c3f49f7912.png)

*Ảnh 01.1 - Trường hợp không đạt: câu trả lời có phần “Hình minh họa” nhưng DOM không có ảnh.*

Đường đi đã kiểm thử thành công là:

1. Nạp ảnh như một tài liệu độc lập vào KB Tài liệu có VLM.
2. Chờ ảnh ở trạng thái **Hoàn tất**.
3. Lấy URI nội bộ dạng `minio://knowledge-base-prd/.../ten-anh.png` từ nội dung nguồn mà hệ thống tạo.
4. Chèn URI đó vào Markdown:

   ```markdown
   ![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/.../ten-anh.png)
   ```

5. Nạp hoặc phân tích lại file Markdown.
6. Hỏi câu buộc trả lời kèm hình và xác nhận ảnh thật xuất hiện trong câu trả lời.

**Lưu ý vận hành:** URI `minio://` gắn với tài nguyên trong hệ thống. Không xóa ảnh nguồn nếu các file Knowledge đang tham chiếu URI đó. Bộ 20 file phân phối của dự án dùng cả ảnh cục bộ để con người đọc và ảnh MinIO để chat có thể render.

Trước khi upload bộ ảnh vào KB asset, kiểm tra định dạng thật: file đuôi `.png` phải có payload PNG với 8 magic bytes `89 50 4E 47 0D 0A 1A 0A`; không chỉ đổi đuôi JPEG thành `.png`. Parser/VLM có thể suy ra MIME và đường dẫn xuất từ nội dung thật, nên file sai định dạng có thể sinh URI đuôi `.jpg`. Nếu phát hiện sai, transcode sang PNG thật, giữ nguyên tên file và kích thước ảnh khi phù hợp, rồi kiểm tra lại trước khi upload.

## Hai KB, hai vai trò

- **KB asset** giữ 49 ảnh PNG độc lập và cấp URI `minio://`. Đây là dependency lâu dài, không dùng làm KB hỏi đáp cho human.
- **KB sử dụng** chỉ nhận 20 file Markdown đã chứa URI MinIO. Không upload folder ảnh hoặc PNG cùng bộ Markdown vào KB này.

Trong dự án này, KB asset là `GS9 Knowledge VNG - Image Assets`; KB sử dụng là `GS9 Knowledge VNG AI`. `LOCAL_ASSET` trong file sinh chỉ giúp builder tìm ảnh local để dựng HTML offline, không phải liên kết ảnh mà Knowledge VNG chat sử dụng.

Khi đổi nơi lưu ảnh, làm đúng thứ tự: tạo host mới → upload ảnh → lấy URI → cập nhật mapping → build → thay Markdown → kiểm thử chat → xóa ảnh ở nơi cũ. Nếu KB asset cũ bị xóa, phải tái kiểm chứng toàn bộ mapping liên quan dù một số link vẫn tạm thời render.

## Không viết điều chưa có bằng chứng như số liệu

Các câu “80% lỗi AI đến từ file nguồn”, “KB không có owner sẽ chết sau một quý” hoặc các tỷ lệ tương tự không được dùng nếu không có dữ liệu đo và nguồn trích dẫn. Có thể viết dưới dạng rủi ro vận hành, không biến thành thống kê.
