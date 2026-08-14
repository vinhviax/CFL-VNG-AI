<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 08 - Chia sẻ và nguồn dữ liệu {#08-chia-se-va-nguon-du-lieu}

## Bạn sẽ biết gì sau khi đọc

- Cách chia sẻ KB qua Space và hai mức quyền.
- Các nguồn Notion, Google Drive, NAS và yêu cầu credential.
- Cách kết nối Google Drive bằng service account, chọn tài nguyên và cấu hình đồng bộ.
- Phần nào đã kiểm chứng, phần nào vẫn cần test qua nhiều chu kỳ.

**Kiểm chứng giao diện: 06-07/08/2026.**

## Chia sẻ qua Space

Tab **Chia sẻ** cho phép chọn Space và gán quyền:

- **Chỉnh sửa:** thành viên có thể thay đổi nội dung theo quyền hệ thống.
- **Chỉ đọc:** thành viên dùng để đọc, truy hồi hoặc hỏi đáp nhưng không sửa nội dung.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/06-chia-se-va-phan-quyen.png -->
![Tab Chia sẻ với lựa chọn Space và quyền Chỉnh sửa hoặc Chỉ đọc](minio://knowledge-base-prd/10012/exports/e61e4fcc-6d62-48b0-b572-a1d85f6f90cf.png)

*Ảnh 08.1 - Chia sẻ là quyết định quyền truy cập, không phải cách nạp dữ liệu.*

Trước khi chia sẻ:

1. Đặt owner của KB và owner nội dung.
2. Kiểm tra tài liệu có dữ liệu hạn chế không.
3. Cấp **Chỉ đọc** theo mặc định; chỉ cấp **Chỉnh sửa** cho nhóm vận hành.
4. Dùng một tài khoản hoặc thành viên đại diện để xác nhận quyền thật.

## Nguồn dữ liệu ngoài

Tab **Nguồn dữ liệu** quan sát được có ba connector:

- **Notion**
- **Google Drive**
- **NAS**

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/07-nguon-du-lieu-notion-drive-nas.png -->
![Tab Nguồn dữ liệu với Notion, Google Drive và NAS](minio://knowledge-base-prd/10012/exports/0666adc3-8abe-422b-94ae-ef52020a956c.png)

*Ảnh 08.2 - Khi chưa cấu hình, trang hiện nút thêm nguồn dữ liệu đầu tiên.*

Wizard có bốn bước:

1. Chọn loại.
2. Thông tin xác thực.
3. Tài nguyên.
4. Chiến lược.

## Trường xác thực đã quan sát

| Nguồn | Trường chính |
|---|---|
| Notion | Tên, Integration Token, kiểm tra kết nối |
| Google Drive | Tên, Service account JSON, Shared Drive ID tùy chọn |
| NAS | Tên, UNC share, username, password |

## Google Drive - chuẩn bị quyền và xác thực

Google Drive connector dùng scope chỉ đọc `drive.readonly`. Quy trình đã kiểm chứng ngày 07/08/2026:

1. Tạo hoặc chọn một Google Cloud project.
2. Bật **Google Drive API** trong đúng project.
3. Tạo service account riêng; không cần gán Google Cloud role chỉ để đọc tài nguyên Drive đã được chia sẻ.
4. Trong tab **Keys**, tạo key loại JSON. Google tự sinh `private_key`; không thêm key thủ công.
5. Chia sẻ đúng thư mục nguồn cho `client_email` của service account với quyền **Viewer**.
6. Trong Knowledge VNG, dán nguyên JSON. Để trống **Shared Drive ID** khi nguồn nằm trong My Drive.
7. Bấm **Kiểm tra kết nối** trước khi đi tiếp.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/15-google-drive-xac-thuc-service-account.png -->
![Màn hình xác thực Google Drive bằng service-account JSON](minio://knowledge-base-prd/10012/exports/ec4b9360-ad0d-4764-b20f-83651394aca4.png)

*Ảnh 08.3 - Không chụp hoặc lưu nội dung JSON key; ảnh chỉ ghi nhận các trường cấu hình.*

Lỗi tổng quát `connection validation failed` đã xuất hiện khi Drive API chưa được bật. Sau khi Enable API trong đúng project, cùng service account và key đi tiếp được; không cần tạo lại credential.

## Google Drive - chọn tài nguyên

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/16-google-drive-chon-tai-nguyen.png -->
![Cây chọn thư mục và tệp Google Drive](minio://knowledge-base-prd/10012/exports/45102d91-6bba-4f63-baa0-a6f5e3532ded.png)

*Ảnh 08.4 - Có thể chọn một tệp hoặc thư mục; dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

Trạng thái quan sát được:

- ✓ màu cam: đã chọn.
- − màu cam ở thư mục: chọn một phần nội dung con.
- vòng tròn trắng: chưa chọn.
- **Hiện chưa hỗ trợ:** connector thấy tài nguyên nhưng chưa hỗ trợ loại đó.

Chọn thư mục khi muốn tệp mới trong thư mục thuộc phạm vi đồng bộ. Chọn một tệp để thử nghiệm hẹp. Không chọn thư mục chứa credential như `keys`.

## Google Drive - lịch, chế độ và xung đột

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/17-google-drive-lich-va-cach-dong-bo.png -->
![Lịch và cách đồng bộ Google Drive](minio://knowledge-base-prd/10012/exports/e8c84875-4614-4da9-bc8b-30e75ce5276b.png)

*Ảnh 08.5 - Lượt test dùng Tăng dần, Ghi đè và mỗi 15 phút.*

| Control | Lựa chọn đã quan sát | Cách dùng |
|---|---|---|
| Lịch | Phút, Giờ, Hằng ngày, Hằng tuần, Hằng tháng | Chọn theo nhịp cập nhật nguồn; 15 phút phù hợp test, không phải mặc định bắt buộc |
| Chế độ | Tăng dần, Toàn bộ | Tăng dần cho vận hành; Toàn bộ khi cần quét lại có chủ đích |
| Xung đột | Ghi đè, Bỏ qua nếu đã có | Ghi đè khi Drive là nguồn chuẩn; Bỏ qua để giữ bản hiện có trong KB |

## Google Drive - lọc tệp và tag

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/18-google-drive-loc-tep-va-tag.png -->
![Regex lọc tệp và gắn tag](minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png)

*Ảnh 08.6 - Có thể thêm nhiều regex tên tệp, tag mặc định và rule tag theo đường dẫn.*

- Để trống regex để nhận mọi tệp hợp lệ trong phạm vi đã chọn.
- Khi có nhiều mẫu, tệp khớp một trong các regex sẽ được đồng bộ.
- `(?i)` cho phép không phân biệt hoa/thường.
- Rule tag theo đường dẫn có thể dùng capture regex như `$1` hoặc `${name}`.
- Trước khi dùng production, thử một tệp khớp và một tệp không khớp.

## Google Drive - ghi đè xử lý

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/19-google-drive-ghi-de-xu-ly.png -->
![Ghi đè chunking cho nguồn Google Drive](minio://knowledge-base-prd/10012/exports/ed516990-0d0b-44fc-b767-691c1f3abd85.png)

*Ảnh 08.7 - Giá trị 0 dùng mặc định KB; chỉ ghi đè khi có bộ câu hỏi đối chứng.*

Nguồn có thể ghi đè kích thước đoạn, độ chồng, giới hạn token, đoạn cha-con, ký tự phân tách và ngôn ngữ. Khuyến nghị giữ `0` hoặc để trống ở lượt đầu để kế thừa cấu hình KB.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/20-google-drive-da-phuong-thuc-va-parser.png -->
![Đa phương thức, ASR, OCR và parser theo loại tệp](minio://knowledge-base-prd/10012/exports/712f2d4c-730d-45b5-a5b7-fb8dd0aed4c0.png)

*Ảnh 08.8 - Các toggle và parser kế thừa yêu cầu model/cấu hình tương ứng của KB.*

- Bật đa phương thức khi cần phân tích hình và đã có VLM.
- Bật ASR cho âm thanh khi có model ASR khả dụng.
- Chỉ ép OCR toàn bộ PDF khi tài liệu là scan hoặc text-layer hỏng.
- Sinh câu hỏi là tùy chọn bổ sung, không thay thế nội dung nguồn tốt.

## Google Drive - parser theo loại tệp

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/21-google-drive-parser-office-text.png -->
![Parser cho Office, CSV, Markdown và văn bản](minio://knowledge-base-prd/10012/exports/e6ebb4ad-5657-4e68-bd4a-09ab8d2e1dd2.png)

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/22-google-drive-parser-media-web.png -->
![Parser cho JSON, ảnh, email, ebook và web](minio://knowledge-base-prd/10012/exports/168abd45-3e25-4ef7-b182-55e458037cdb.png)

*Ảnh 08.9-08.10 - Danh sách parser quan sát trong wizard ngày 07/08/2026.*

| Loại | Parser đang hiển thị trong lượt test |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in; Tự nhận diện hoặc Thủ công |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

Danh sách parser có thể phụ thuộc tenant và thay đổi theo thời điểm.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/24-google-drive-parser-excel-tuy-chinh.png -->
![Chọn parser Excel tùy chỉnh](minio://knowledge-base-prd/10012/exports/275a026c-5970-45de-bc5d-3c0a4dc9164c.png)

*Ảnh 08.11 - Các parser có tiền tố FPA là cấu hình riêng của tenant test, không phải mặc định chung.*

Khi Excel để **Thủ công**, dropdown có thể hiện parser do tenant đăng ký. Chỉ chọn parser tùy chỉnh khi cấu trúc workbook đúng với parser đó; nếu không, dùng Tự nhận diện hoặc cấu hình mặc định đã kiểm thử.

## Google Drive - đồng bộ xóa

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/23-google-drive-dong-bo-xoa.png -->
![Tùy chọn đồng bộ xóa](minio://knowledge-base-prd/10012/exports/88efc5bd-c974-4c0b-9bf7-35c65739f348.png)

*Ảnh 08.12 - UI mô tả bật control sẽ gỡ tri thức khi nguồn đã bị xóa.*

Khuyến nghị để **tắt** trong lượt thử đầu. Chỉ bật sau khi đã thử bằng tệp không quan trọng và xác nhận quy trình backup/phục hồi. Lượt ngày 07/08/2026 mới quan sát control, chưa thử xóa end-to-end.

## Kết quả kết nối và đồng bộ đầu tiên

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/25-google-drive-dong-bo-thanh-cong.png -->
![Google Drive đã kết nối và đồng bộ thành công](minio://knowledge-base-prd/10012/exports/947d9103-edd6-4dfa-b5a5-295bcae2c66f.png)

*Ảnh 08.13 - Card nguồn hiển thị Đã kết nối và Kết quả Thành công.*

Lượt kiểm chứng hiển thị:

- Chế độ: **Tăng dần**.
- Phạm vi: **Một tệp**.
- Lịch: **Mỗi 15 phút**.
- Đồng bộ gần nhất: **Vừa xong**.
- Kết quả: **Thành công**.

Kết quả này xác nhận wizard bước 3-4 và lượt đồng bộ đầu tiên trong điều kiện test. Sau đó vẫn phải mở Documents, kiểm tra trạng thái xử lý, nội dung chunk và chat bằng câu hỏi đối chứng.

## Phần chưa xác định sau lượt Google Drive đầu tiên

Chưa khẳng định:

- Tăng dần và Toàn bộ cho kết quả ra sao qua nhiều chu kỳ.
- Regex, tag theo đường dẫn hoặc parser tùy chỉnh áp dụng đúng trên mọi bộ dữ liệu.
- Sửa, đổi tên, di chuyển, xóa hoặc thu hồi quyền ở Drive phản ánh thế nào vào KB.
- Đồng bộ xóa có thể phục hồi bằng quy trình nào.
- Shared Drive hoạt động giống My Drive; lượt test này để trống Shared Drive ID.
- Notion và NAS đi hết bước 3-4; hai connector này vẫn thiếu credential test.

## Không tự suy luận hành vi đồng bộ

Cho đến khi có ma trận nhiều chu kỳ, không khẳng định:

- file bị xóa ở nguồn sẽ tự bị xóa trong KB;
- quyền xem ở Notion/Drive được giữ nguyên sau đồng bộ;
- cập nhật xảy ra ngay lập tức;
- mọi định dạng trong nguồn ngoài dùng cùng parser với upload tay.

Khi có credential test, cần chạy ma trận: thêm file, sửa file, đổi tên, di chuyển, xóa, thu hồi quyền và lỗi kết nối.

## Bảo mật credential

- Không chụp token hoặc JSON key vào tài liệu hướng dẫn.
- Không đặt credential trong file Markdown của KB.
- Dùng tài khoản dịch vụ có quyền tối thiểu.
- Với Drive, ưu tiên Viewer trên đúng thư mục; không chia sẻ toàn bộ My Drive.
- Ghi người sở hữu credential và quy trình xoay vòng ngoài KB nội dung.
