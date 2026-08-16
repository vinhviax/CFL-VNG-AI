<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 08 - Chia sẻ và nguồn dữ liệu {#08-chia-se-va-nguon-du-lieu}

Đọc xong bạn biết cách chia sẻ KB qua Space với đúng mức quyền, và cách kết nối một nguồn dữ liệu ngoài — đặc biệt là Google Drive — từ xác thực đến lượt đồng bộ đầu tiên.

## Chia sẻ qua Space

Tab **Chia sẻ** cho phép chọn Space và gán quyền:

- **Chỉnh sửa:** thành viên có thể thay đổi nội dung theo quyền hệ thống.
- **Chỉ đọc:** thành viên đọc, truy hồi hoặc hỏi đáp nhưng không sửa nội dung.

<!-- LOCAL_ASSET: ./image-06-chia-se-va-phan-quyen.png -->
![Tab Chia sẻ với lựa chọn Space và quyền Chỉnh sửa hoặc Chỉ đọc](minio://knowledge-base-prd/10012/4ab738a4-8895-46b5-acf5-017d3087c51a/5f83573b-3478-4fb6-8540-67508b8caa7b.png)

*Ảnh 08.1 - Chia sẻ là quyết định quyền truy cập, không phải cách nạp dữ liệu.*

Trước khi chia sẻ:

1. Đặt owner của KB và owner nội dung.
2. Kiểm tra tài liệu có dữ liệu hạn chế không.
3. Cấp **Chỉ đọc** theo mặc định; chỉ cấp **Chỉnh sửa** cho nhóm vận hành.
4. Dùng một tài khoản hoặc thành viên đại diện để xác nhận quyền thật.

## Nguồn dữ liệu ngoài

Tab **Nguồn dữ liệu** có ba connector:

- **Notion**
- **Google Drive**
- **NAS**

<!-- LOCAL_ASSET: ./image-07-nguon-du-lieu-notion-drive-nas.png -->
![Tab Nguồn dữ liệu với Notion, Google Drive và NAS](minio://knowledge-base-prd/10012/290342ca-a20f-48aa-aa3f-7777f196b780/edbd9f6c-4985-4c18-8ee9-5c60a023c354.png)

*Ảnh 08.2 - Khi chưa cấu hình, trang hiện nút thêm nguồn dữ liệu đầu tiên.*

Wizard có bốn bước:

1. Chọn loại.
2. Thông tin xác thực.
3. Tài nguyên.
4. Chiến lược.

### Trường xác thực theo từng nguồn

| Nguồn | Trường chính |
|---|---|
| Notion | Tên, Integration Token, kiểm tra kết nối |
| Google Drive | Tên, Service account JSON, Shared Drive ID tùy chọn |
| NAS | Tên, UNC share, username, password |

## Google Drive - chuẩn bị quyền và xác thực

Google Drive connector dùng scope chỉ đọc `drive.readonly`.

1. Tạo hoặc chọn một Google Cloud project.
2. Bật **Google Drive API** trong đúng project đó.
3. Tạo service account riêng. Không cần gán Google Cloud role chỉ để đọc tài nguyên Drive đã được chia sẻ.
4. Trong tab **Keys**, tạo key loại JSON. Google tự sinh `private_key`; không thêm key thủ công.
5. Chia sẻ đúng thư mục nguồn cho `client_email` của service account với quyền **Viewer**.
6. Trong Knowledge VNG, dán nguyên nội dung JSON. Để trống **Shared Drive ID** khi nguồn nằm trong My Drive.
7. Bấm **Kiểm tra kết nối** trước khi đi tiếp.

<!-- LOCAL_ASSET: ./image-15-google-drive-xac-thuc-service-account.png -->
![Màn hình xác thực Google Drive bằng service-account JSON](minio://knowledge-base-prd/10012/598229c9-ecfd-4c6a-9111-8f14c2bd029c/dc62c1ea-99a8-4c18-9aee-771f0d8dc6c4.png)

*Ảnh 08.3 - Không chụp hoặc lưu nội dung JSON key; ảnh chỉ ghi nhận các trường cấu hình.*

**Nếu gặp lỗi `connection validation failed`:** kiểm tra Drive API đã bật trong đúng project chưa. Đây là nguyên nhân phổ biến nhất, và lỗi hiển thị rất chung chung. Sau khi bật API, cùng service account và key đó đi tiếp được — không cần tạo lại credential.

## Google Drive - chọn tài nguyên

<!-- LOCAL_ASSET: ./image-16-google-drive-chon-tai-nguyen.png -->
![Cây chọn thư mục và tệp Google Drive](minio://knowledge-base-prd/10012/69d6b4ae-a92d-41ba-ba28-43942d2b6908/b838949f-000e-4db1-a836-873534640363.png)

*Ảnh 08.4 - Có thể chọn một tệp hoặc thư mục; dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

Ý nghĩa các trạng thái trong cây:

| Ký hiệu | Nghĩa |
|---|---|
| ✓ màu cam | Đã chọn |
| − màu cam ở thư mục | Chọn một phần nội dung con |
| Vòng tròn trắng | Chưa chọn |
| **Hiện chưa hỗ trợ** | Connector thấy tài nguyên nhưng chưa hỗ trợ loại đó |

Chọn cả thư mục khi muốn tệp mới thêm vào thư mục cũng nằm trong phạm vi đồng bộ. Chọn một tệp khi muốn thử nghiệm hẹp.

**Không chọn thư mục chứa credential**, ví dụ thư mục tên `keys`.

## Google Drive - lịch, chế độ và xung đột

<!-- LOCAL_ASSET: ./image-17-google-drive-lich-va-cach-dong-bo.png -->
![Lịch và cách đồng bộ Google Drive](minio://knowledge-base-prd/10012/b5ff709e-6c03-4a0e-ad8d-6925c1c91ca6/a6ffd964-b5e7-49d6-82c0-1a17e2d8852b.png)

*Ảnh 08.5 - Ví dụ cấu hình: Tăng dần, Ghi đè và mỗi 15 phút.*

| Control | Lựa chọn | Cách dùng |
|---|---|---|
| Lịch | Phút, Giờ, Hằng ngày, Hằng tuần, Hằng tháng | Chọn theo nhịp cập nhật nguồn; 15 phút phù hợp khi thử nghiệm, không phải giá trị bắt buộc |
| Chế độ | Tăng dần, Toàn bộ | Tăng dần cho vận hành; Toàn bộ khi cần quét lại có chủ đích |
| Xung đột | Ghi đè, Bỏ qua nếu đã có | Ghi đè khi Drive là nguồn chuẩn; Bỏ qua để giữ bản hiện có trong KB |

## Google Drive - lọc tệp và tag

<!-- LOCAL_ASSET: ./image-18-google-drive-loc-tep-va-tag.png -->
![Regex lọc tệp và gắn tag](minio://knowledge-base-prd/10012/f4fbcd6a-a8de-492d-9020-6fd5b0c24416/3a817b35-4417-4bed-95cc-91e9146e6a8a.png)

*Ảnh 08.6 - Có thể thêm nhiều regex tên tệp, tag mặc định và rule tag theo đường dẫn.*

- Để trống regex để nhận mọi tệp hợp lệ trong phạm vi đã chọn.
- Khi có nhiều mẫu, tệp khớp **một trong các** regex sẽ được đồng bộ.
- Thêm `(?i)` để không phân biệt hoa thường.
- Rule tag theo đường dẫn dùng được capture regex như `$1` hoặc `${name}`.
- Trước khi dùng cho dữ liệu thật, thử một tệp khớp và một tệp không khớp.

## Google Drive - ghi đè xử lý

<!-- LOCAL_ASSET: ./image-19-google-drive-ghi-de-xu-ly.png -->
![Ghi đè chunking cho nguồn Google Drive](minio://knowledge-base-prd/10012/4eb19f57-dbd1-4697-806e-46bfde0c4128/0cce3cde-40e1-493e-b9f5-b6e09e4c548d.png)

*Ảnh 08.7 - Giá trị 0 dùng mặc định KB; chỉ ghi đè khi có bộ câu hỏi đối chứng.*

Nguồn có thể ghi đè kích thước đoạn, độ chồng lấp, giới hạn token, đoạn cha-con, ký tự phân tách và ngôn ngữ. Giữ `0` hoặc để trống ở lượt đầu để kế thừa cấu hình KB.

<!-- LOCAL_ASSET: ./image-20-google-drive-da-phuong-thuc-va-parser.png -->
![Đa phương thức, ASR, OCR và parser theo loại tệp](minio://knowledge-base-prd/10012/4a7ca009-5eb5-4070-bf4b-c4b03a9bc40f/37565725-8a2c-46ca-b027-f9c62605efcc.png)

*Ảnh 08.8 - Các toggle và parser kế thừa yêu cầu model/cấu hình tương ứng của KB.*

- Bật đa phương thức khi cần phân tích hình và KB đã có model VLM.
- Bật ASR cho âm thanh khi có model ASR khả dụng.
- Chỉ ép OCR toàn bộ PDF khi tài liệu là bản scan hoặc lớp text bị hỏng. Bật cho PDF có lớp text tốt chỉ tốn thời gian xử lý.
- Sinh câu hỏi là tùy chọn bổ sung, không thay thế nội dung nguồn tốt.

## Google Drive - parser theo loại tệp

<!-- LOCAL_ASSET: ./image-21-google-drive-parser-office-text.png -->
![Parser cho Office, CSV, Markdown và văn bản](minio://knowledge-base-prd/10012/32ee84cd-d9d4-4dc0-a467-aa43610e5466/dd37b82f-592f-45e6-bcf5-4d76d4bc15ca.png)

<!-- LOCAL_ASSET: ./image-22-google-drive-parser-media-web.png -->
![Parser cho JSON, ảnh, email, ebook và web](minio://knowledge-base-prd/10012/6afed423-8857-4dd1-b7e3-e9e12585b4ee/888fd1aa-109a-4611-b1b1-6aa0e1e190e6.png)

*Ảnh 08.9-08.10 - Danh sách parser trong wizard nguồn dữ liệu.*

| Loại | Parser trong wizard |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in; kèm chọn Tự nhận diện hoặc Thủ công |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

**Đây không phải cùng tập lựa chọn với khi tải tệp lên tay.** Ví dụ PowerPoint ở đây chỉ hiện MinerU, còn khi tải tay có thêm markitdown; Markdown ở đây chỉ hiện Built-in, còn khi tải tay có bốn lựa chọn. Đừng chép bảng này thành bảng kia. Danh sách cũng có thể khác tùy môi trường của bạn.

<!-- LOCAL_ASSET: ./image-24-google-drive-parser-excel-tuy-chinh.png -->
![Chọn parser Excel tùy chỉnh](minio://knowledge-base-prd/10012/bd01ef91-110c-44f4-9d5a-1ab974bbe0fa/654077fd-eb21-4b8e-b5e5-df5f4c880ae0.png)

*Ảnh 08.11 - Các parser có tiền tố FPA là cấu hình riêng của từng môi trường, không phải mặc định chung.*

Nhóm Excel có thêm hai chế độ:

| Chế độ | Nghĩa |
|---|---|
| **Tự nhận diện** | Hệ thống đọc tên từng tệp để đoán khuôn mẫu Excel đã cấu hình sẵn |
| **Thủ công** | Ghim một parser cho mọi tệp Excel trong KB này; hiện thêm trường **Định dạng parser** |

Trường **Định dạng parser** không phải danh sách engine, mà là danh sách khuôn mẫu Excel đã được đăng ký sẵn cho môi trường của bạn.

- Chỉ chọn parser tùy chỉnh khi cấu trúc workbook **đúng với** cấu trúc parser đó yêu cầu.
- Không chọn chỉ vì tên nghe phù hợp.
- Nếu không chắc, dùng **Tự nhận diện** hoặc cấu hình mặc định đã kiểm thử.

## Google Drive - đồng bộ xóa

<!-- LOCAL_ASSET: ./image-23-google-drive-dong-bo-xoa.png -->
![Tùy chọn đồng bộ xóa](minio://knowledge-base-prd/10012/4685856b-38ac-44b6-875e-57ccb732589d/57af586b-ee63-4b97-a5f5-b52689da6765.png)

*Ảnh 08.12 - UI mô tả bật control sẽ gỡ tri thức khi nguồn đã bị xóa.*

Để **tắt** trong lượt thử đầu. Chỉ bật sau khi đã thử bằng tệp không quan trọng và xác nhận bạn có quy trình backup, phục hồi.

Đây là thao tác có thể làm mất nội dung trong KB mà không hoàn tác được từ giao diện.

## Kiểm tra sau khi kết nối

<!-- LOCAL_ASSET: ./image-25-google-drive-dong-bo-thanh-cong.png -->
![Google Drive đã kết nối và đồng bộ thành công](minio://knowledge-base-prd/10012/305934e0-eb75-43df-9f77-ef21d82c160c/8d4dc399-0524-4779-89be-49cf500ec1f4.png)

*Ảnh 08.13 - Card nguồn hiển thị Đã kết nối và Kết quả Thành công.*

Card nguồn hiển thị các thông tin để bạn đối chiếu với cấu hình đã đặt:

- Chế độ, ví dụ **Tăng dần**.
- Phạm vi, ví dụ **Một tệp**.
- Lịch, ví dụ **Mỗi 15 phút**.
- Đồng bộ gần nhất.
- Kết quả.

**Kết quả Thành công chưa đủ.** Card chỉ nói lượt đồng bộ chạy xong. Sau đó vẫn phải:

1. Mở **Documents**, kiểm tra trạng thái xử lý của từng tài liệu.
2. Mở chi tiết tài liệu, xem nội dung phân đoạn.
3. Chat bằng bộ câu hỏi đối chứng và xem nguồn truy hồi.

## Cách triển khai an toàn

- Bắt đầu bằng **một tệp** và lịch thưa. Mở rộng phạm vi sau khi đã xác nhận nội dung vào đúng.
- Thử một chu kỳ sửa file ở Drive, chờ đồng bộ, rồi kiểm tra nội dung trong KB trước khi giao cho người dùng thật.
- Để ảnh và tài liệu trong **cùng một KB**. Đồng bộ lại không làm mất liên kết ảnh đã nhúng, ở cả chế độ Tăng dần lẫn Toàn bộ.
- Ghi lại cấu hình bạn đã chọn để người sau còn đối chiếu.

## Bảo mật credential

- Không chụp token hoặc JSON key vào tài liệu hướng dẫn.
- Không đặt credential trong file Markdown của KB.
- Dùng tài khoản dịch vụ có quyền tối thiểu.
- Với Drive, ưu tiên quyền **Viewer** trên đúng thư mục; không chia sẻ toàn bộ My Drive.
- Ghi người sở hữu credential và quy trình xoay vòng ở nơi khác, không để trong nội dung KB.
