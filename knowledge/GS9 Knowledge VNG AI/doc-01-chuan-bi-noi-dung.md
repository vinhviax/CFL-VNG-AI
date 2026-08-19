<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 01 - Chuẩn bị nội dung nguồn {#01-chuan-bi-noi-dung}

## Bạn sẽ biết gì sau khi đọc

- Cách làm sạch file trước khi nạp.
- Cấu trúc Markdown thân thiện với người đọc và hệ thống truy hồi.
- Cách chuẩn bị ảnh để vừa đọc offline vừa hiển thị trong chat Knowledge VNG.

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

Nhưng chat Knowledge VNG **không render ảnh** từ đường dẫn tương đối, kể cả khi file Markdown và file ảnh đều đã được nạp vào KB.

<!-- LOCAL_ASSET: ./image-14-chat-khong-hien-thi-duong-dan-tuong-doi.png -->
![Câu trả lời có mô tả ảnh nhưng không render ảnh khi Markdown dùng đường dẫn tương đối](minio://knowledge-base-prd/10012/ec7c629c-1648-41a9-bc8e-d00e80abc180/35602691-18ca-48e6-96fc-ac7350dcfb6b.png)

*Ảnh 01.1 - Trường hợp không đạt: câu trả lời có phần “Hình minh họa” nhưng không có ảnh nào hiện ra.*

Cách làm đúng để chat hiển thị được ảnh:

1. Nạp ảnh như một tài liệu độc lập vào KB Tài liệu có VLM.
2. Chờ ảnh ở trạng thái **Hoàn tất**.
3. Lấy URI nội bộ dạng `minio://knowledge-base-prd/.../ten-anh.png` từ nội dung nguồn mà hệ thống tạo.
4. Chèn URI đó vào Markdown:

   ```markdown
   ![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/.../ten-anh.png)
   ```

5. Nạp hoặc phân tích lại file Markdown.
6. Hỏi câu buộc trả lời kèm hình và xác nhận ảnh thật xuất hiện trong câu trả lời.

**Lưu ý vận hành:** URI `minio://` gắn với tài nguyên trong hệ thống. Không xóa ảnh nguồn nếu còn file Markdown đang tham chiếu URI đó.

Kiểm tra định dạng thật của ảnh trước khi nạp. Đừng chỉ đổi đuôi file JPEG thành `.png`: hệ thống nhận diện theo nội dung thật của file, nên file sai định dạng sẽ sinh URI đuôi `.jpg`. Nếu gặp trường hợp này, chuyển đổi ảnh sang PNG thật, giữ nguyên tên file và kích thước ảnh, rồi nạp lại.

## Ảnh và tài liệu để chung một Knowledge Base

Không cần tách ảnh sang một KB riêng. Ảnh và file Markdown để chung một KB là cách làm hiện hành và an toàn.

Làm theo thứ tự này:

1. Nạp toàn bộ ảnh vào KB trước.
2. Chờ từng ảnh sang trạng thái **Hoàn tất**.
3. Lấy URI `minio://` của từng ảnh.
4. Gắn URI vào đúng vị trí trong file Markdown.
5. Nạp file Markdown vào cùng KB đó.

Về sau, sửa nội dung tài liệu rồi nạp lại **không** làm mất ảnh, miễn là bạn không đụng vào dòng chứa URI ảnh. Nếu cần đổi ảnh, hãy sửa cả dòng đó và kiểm thử lại chat.

Khi đổi nơi lưu ảnh, làm đúng thứ tự: nạp ảnh vào nơi mới → lấy URI mới → cập nhật Markdown → kiểm thử chat → chỉ sau đó mới xóa ảnh ở nơi cũ.
