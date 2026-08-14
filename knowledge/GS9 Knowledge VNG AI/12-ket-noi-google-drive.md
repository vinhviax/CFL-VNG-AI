<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 12 - Kết nối Google Drive {#12-ket-noi-google-drive}

## Bạn sẽ biết gì sau khi đọc

- Cách tạo quyền đọc tối thiểu bằng service account.
- Cách chọn đúng thư mục hoặc tệp trên Google Drive.
- Cách chọn lịch, chế độ, xung đột, filter, tag và parser.
- Cách nhận biết lượt đồng bộ đầu tiên đã thành công.
- Phần nào vẫn phải kiểm thử trước khi dùng production.

**Kiểm chứng giao diện và lượt đồng bộ đầu tiên: 07/08/2026.**

## 1. Chuẩn bị Google Cloud và quyền Drive

1. Tạo hoặc chọn Google Cloud project dành cho connector.
2. Bật **Google Drive API** trong đúng project.
3. Tạo service account riêng và tạo key JSON trong tab **Keys**.
4. Chia sẻ đúng thư mục nguồn cho `client_email` với quyền **Viewer**.
5. Không đưa JSON key vào Drive, KB, Markdown hoặc ảnh chụp.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/15-google-drive-xac-thuc-service-account.png -->
![Nhập service-account JSON cho Google Drive](minio://knowledge-base-prd/10012/exports/ec4b9360-ad0d-4764-b20f-83651394aca4.png)

*Ảnh 12.1 - Dán nguyên JSON; để trống Shared Drive ID khi nguồn nằm trong My Drive.*

Nếu **Kiểm tra kết nối** trả về `connection validation failed`, kiểm tra Drive API trước. Trong phép thử thực tế, kết nối đi tiếp ngay sau khi Enable API; không cần tạo lại key.

## 2. Chọn tài nguyên

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/16-google-drive-chon-tai-nguyen.png -->
![Chọn thư mục hoặc tệp Google Drive](minio://knowledge-base-prd/10012/exports/45102d91-6bba-4f63-baa0-a6f5e3532ded.png)

*Ảnh 12.2 - Dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

- Chọn thư mục để tệp mới trong thư mục thuộc phạm vi đồng bộ.
- Chọn một tệp để thử nghiệm hẹp.
- Mục có nhãn **Hiện chưa hỗ trợ** sẽ không được xử lý.
- Không chọn thư mục `keys` hoặc vùng chứa credential.

## 3. Chọn lịch và cách đồng bộ

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/17-google-drive-lich-va-cach-dong-bo.png -->
![Lịch, chế độ và chiến lược xung đột](minio://knowledge-base-prd/10012/exports/e8c84875-4614-4da9-bc8b-30e75ce5276b.png)

*Ảnh 12.3 - Lượt test dùng Tăng dần, Ghi đè và mỗi 15 phút.*

| Cấu hình | Khuyến nghị ban đầu |
|---|---|
| Lịch | 15 phút để test; Giờ hoặc Hằng ngày cho phần lớn nguồn vận hành |
| Chế độ | **Tăng dần** cho vận hành thường xuyên |
| Xung đột | **Ghi đè** khi Drive là nguồn chuẩn; Bỏ qua khi cần giữ bản đang có trong KB |

Chỉ dùng **Toàn bộ** khi cần quét lại có chủ đích. Sau khi đổi chiến lược, luôn chạy bộ câu hỏi đối chứng.

## 4. Lọc tệp và tag

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/18-google-drive-loc-tep-va-tag.png -->
![Regex lọc tên tệp và gắn tag](minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png)

*Ảnh 12.4 - Để trống regex để đồng bộ mọi tệp hợp lệ trong phạm vi.*

- Nhiều regex hoạt động theo điều kiện khớp một trong các mẫu.
- Dùng `(?i)` để không phân biệt hoa/thường.
- Thử ít nhất một tên khớp và một tên không khớp trước production.
- Tag mặc định nên mô tả nguồn/nghiệp vụ; rule theo đường dẫn chỉ dùng khi cấu trúc thư mục ổn định.

## 5. Giữ mặc định xử lý ở lượt đầu

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/19-google-drive-ghi-de-xu-ly.png -->
![Ghi đè chunking ở cấp nguồn](minio://knowledge-base-prd/10012/exports/ed516990-0d0b-44fc-b767-691c1f3abd85.png)

*Ảnh 12.5 - Giá trị 0 dùng cấu hình mặc định của KB.*

Giữ kích thước đoạn, độ chồng và token ở `0`; để trống ký tự phân tách nếu chưa có lý do kiểm thử rõ ràng. Chỉ bật đoạn cha-con khi nội dung cần giữ ngữ cảnh cha lớn hơn.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/20-google-drive-da-phuong-thuc-va-parser.png -->
![Đa phương thức, ASR, OCR và parser](minio://knowledge-base-prd/10012/exports/712f2d4c-730d-45b5-a5b7-fb8dd0aed4c0.png)

*Ảnh 12.6 - VLM, ASR và OCR cần model/cấu hình tương ứng.*

- Đa phương thức: bật khi cần đọc hình và KB có VLM.
- ASR: bật cho âm thanh khi có model ASR khả dụng.
- Ép OCR toàn bộ PDF: chỉ dùng cho scan hoặc text-layer hỏng.
- Sinh câu hỏi: tùy chọn bổ sung, không sửa được nguồn viết kém.

## 6. Chọn parser đúng loại tệp

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/21-google-drive-parser-office-text.png -->
![Parser cho Office, CSV, Markdown và text](minio://knowledge-base-prd/10012/exports/e6ebb4ad-5657-4e68-bd4a-09ab8d2e1dd2.png)

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/22-google-drive-parser-media-web.png -->
![Parser cho media, email, ebook và web](minio://knowledge-base-prd/10012/exports/168abd45-3e25-4ef7-b182-55e458037cdb.png)

*Ảnh 12.7-12.8 - Parser quan sát được ngày 07/08/2026; danh sách có thể đổi theo tenant.*

| Loại | Parser quan sát được |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/24-google-drive-parser-excel-tuy-chinh.png -->
![Parser Excel tùy chỉnh](minio://knowledge-base-prd/10012/exports/275a026c-5970-45de-bc5d-3c0a4dc9164c.png)

*Ảnh 12.9 - Các parser có tiền tố FPA là cấu hình riêng của tenant test.*

Excel **Thủ công** có thể liệt kê parser do tenant đăng ký. Không chọn parser tùy chỉnh chỉ vì tên nghe phù hợp; workbook phải đúng cấu trúc mà parser yêu cầu.

## 7. Thận trọng với đồng bộ xóa

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/23-google-drive-dong-bo-xoa.png -->
![Bật hoặc tắt đồng bộ xóa](minio://knowledge-base-prd/10012/exports/88efc5bd-c974-4c0b-9bf7-35c65739f348.png)

*Ảnh 12.10 - UI mô tả bật control sẽ gỡ tri thức khi tệp nguồn bị xóa.*

Để **tắt trong lượt thử đầu**. Chỉ bật sau khi thử bằng tệp không quan trọng, có backup và đã xác nhận cách phục hồi. Lượt ngày 07/08/2026 chưa thử hành vi xóa end-to-end.

## 8. Tạo nguồn và xác nhận thành công

Bấm **Tạo & đồng bộ ngay**. Card nguồn phải cho biết trạng thái, chế độ, phạm vi, lịch, thời điểm gần nhất và kết quả.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/25-google-drive-dong-bo-thanh-cong.png -->
![Google Drive đã kết nối và đồng bộ thành công](minio://knowledge-base-prd/10012/exports/947d9103-edd6-4dfa-b5a5-295bcae2c66f.png)

*Ảnh 12.11 - Lượt test hiển thị Đã kết nối và Kết quả Thành công.*

Lượt đã kiểm chứng dùng **Tăng dần**, phạm vi **Một tệp**, lịch **Mỗi 15 phút** và kết quả **Thành công**. Sau đó vẫn phải:

1. Mở Documents và xác nhận tài liệu đã xuất hiện.
2. Chờ trạng thái xử lý hoàn tất.
3. Mở chunk để kiểm tra nội dung parser.
4. Hỏi câu đúng, gần đúng, loại trừ và ngoài phạm vi.
5. Kiểm tra nguồn truy hồi, không chỉ đánh giá câu trả lời nghe hợp lý.

## Chưa được phép suy luận

Một lượt thành công chưa chứng minh:

- Tăng dần và Toàn bộ đúng qua nhiều chu kỳ.
- Regex, tag và parser tùy chỉnh đúng cho mọi dữ liệu.
- Sửa, đổi tên, di chuyển, xóa hoặc thu hồi quyền phản ánh đúng vào KB.
- Shared Drive giống My Drive; lượt test này không điền Shared Drive ID.

Xem bằng chứng chi tiết tại [audit Google Drive ngày 07/08/2026](../../audit/audit-google-drive-connector-2026-08-07.md).
