<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 12 - Kết nối Google Drive {#12-ket-noi-google-drive}

Đọc xong bạn tự nối được một thư mục Google Drive vào KB: cấp quyền đọc tối thiểu, chọn đúng phạm vi, chọn đúng chế độ đồng bộ, và xác nhận lượt đồng bộ đầu tiên thật sự chạy được.

## Bạn sẽ biết gì sau khi đọc

- Cách tạo quyền đọc tối thiểu bằng service account.
- Cách chọn đúng thư mục hoặc tệp trên Google Drive.
- Cách chọn lịch, chế độ đồng bộ, chiến lược xung đột, filter, tag và parser.
- Cách nhận biết lượt đồng bộ đầu tiên đã thành công.

## 1. Chuẩn bị Google Cloud và quyền Drive

1. Tạo hoặc chọn một Google Cloud project dành riêng cho connector.
2. Bật **Google Drive API** trong đúng project đó.
3. Tạo service account riêng, rồi tạo key JSON trong tab **Keys**.
4. Chia sẻ đúng thư mục nguồn cho `client_email` của service account, quyền **Viewer**.
5. Không đưa JSON key vào Drive, vào KB, vào Markdown hay ảnh chụp màn hình.

<!-- LOCAL_ASSET: ./image-15-google-drive-xac-thuc-service-account.png -->
![Nhập service-account JSON cho Google Drive](minio://knowledge-base-prd/10012/exports/64266508-8a5f-44c2-bb27-b6103bd9b1d6.png)

*Ảnh 12.1 - Dán nguyên JSON; để trống Shared Drive ID khi nguồn nằm trong My Drive.*

Chỉ cấp quyền **Viewer** cho đúng thư mục cần đồng bộ. Không chia sẻ toàn bộ My Drive.

Nếu **Kiểm tra kết nối** trả về `connection validation failed`, kiểm tra Google Drive API trước. Bật API rồi thử lại thường là đủ, không cần tạo lại service account hay key JSON.

## 2. Chọn tài nguyên

<!-- LOCAL_ASSET: ./image-16-google-drive-chon-tai-nguyen.png -->
![Chọn thư mục hoặc tệp Google Drive](minio://knowledge-base-prd/10012/exports/a189c9b7-b453-4852-92ee-3fc4e27c61e8.png)

*Ảnh 12.2 - Dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

- Chọn cả thư mục nếu muốn tệp mới thêm vào thư mục cũng tự nằm trong phạm vi đồng bộ.
- Chọn một tệp riêng khi muốn thử nghiệm hẹp.
- Mục có nhãn **Hiện chưa hỗ trợ** sẽ không được xử lý.
- **Không chọn thư mục `keys` hoặc bất kỳ vùng chứa credential nào.** Đã lọt vào phạm vi đồng bộ là nội dung đó sẽ nằm trong KB và có thể bị chat trả ra.
- Mỗi nguồn nên trỏ vào đúng một thư mục nội dung. Không trỏ vào thư mục gốc của cả project.

## 3. Chọn lịch và cách đồng bộ

<!-- LOCAL_ASSET: ./image-17-google-drive-lich-va-cach-dong-bo.png -->
![Lịch, chế độ và chiến lược xung đột](minio://knowledge-base-prd/10012/exports/b86b4101-8e8d-42c0-b8cb-14aa26de03c3.png)

*Ảnh 12.3 - Chế độ đồng bộ và chiến lược xung đột là hai lựa chọn riêng biệt.*

### Hai lựa chọn này trả lời hai câu hỏi khác nhau

Đây là chỗ dễ nhầm nhất. Chúng không thay thế nhau.

**Chế độ đồng bộ** trả lời: *lần chạy này quét những tệp nào?*

| Chế độ | Nghĩa là gì | Dùng khi nào |
|---|---|---|
| **Tăng dần** | Chỉ lấy tệp đã thay đổi kể từ lần đồng bộ trước | Vận hành thường xuyên. Nhanh, ít tải |
| **Toàn bộ** | Liệt kê lại toàn bộ tài nguyên trong phạm vi ở mỗi lần chạy | Khi vừa đổi tên hoặc di chuyển nhiều tệp. Chậm hơn nhưng chắc chắn không bỏ sót |

**Chiến lược xung đột** trả lời: *tệp đã có sẵn trong kho thì làm gì?*

| Chiến lược | Nghĩa là gì | Dùng khi nào |
|---|---|---|
| **Ghi đè** | Thay bằng bản mới khi tệp nguồn đổi | Drive là nguồn chuẩn |
| **Bỏ qua nếu đã có** | Giữ nguyên bản cũ trong kho | Muốn giữ bản đang có. Lưu ý: nội dung vừa sửa trên Drive sẽ **không** lên kho |

### Điểm mấu chốt

**Cả hai chế độ đều chỉ nạp lại tệp thực sự có thay đổi.** Chọn Toàn bộ không có nghĩa là mọi tệp bị nạp lại từ đầu; nó chỉ mở rộng danh sách được quét.

Hệ quả thực dụng: tệp không đổi thì không bị đụng tới. Ảnh đã gắn trong một tài liệu vẫn giữ nguyên khi bạn sửa và đồng bộ lại một tài liệu khác.

Nếu cần ép nạp lại một tệp không đổi, hãy sửa thật tệp đó ở nguồn, hoặc dùng **Phân tích lại** trên đúng tài liệu đó trong KB.

### Khuyến nghị ban đầu

| Cấu hình | Khuyến nghị |
|---|---|
| Lịch | 15 phút khi đang thử; Giờ hoặc Hằng ngày cho phần lớn nguồn vận hành |
| Chế độ | **Tăng dần** cho vận hành thường xuyên |
| Xung đột | **Ghi đè** khi Drive là nguồn chuẩn; **Bỏ qua nếu đã có** khi cần giữ bản đang có trong KB |

Sau khi đổi bất kỳ lựa chọn nào ở đây, chạy lại bộ câu hỏi đối chứng.

## 4. Lọc tệp và tag

<!-- LOCAL_ASSET: ./image-18-google-drive-loc-tep-va-tag.png -->
![Regex lọc tên tệp và gắn tag](minio://knowledge-base-prd/10012/exports/667cfd07-ec8e-4106-8ed7-c6cd50c11c28.png)

*Ảnh 12.4 - Để trống regex để đồng bộ mọi tệp hợp lệ trong phạm vi.*

- Thêm được nhiều mẫu regex. Tệp khớp **một trong** các mẫu sẽ được đồng bộ.
- Dùng `(?i)` để không phân biệt hoa thường.
- Thử ít nhất một tên khớp và một tên không khớp trước khi dùng cho production.
- Tag mặc định nên mô tả nguồn hoặc nghiệp vụ.
- Rule gắn tag theo đường dẫn chỉ nên dùng khi cấu trúc thư mục đã ổn định.

## 5. Giữ mặc định xử lý ở lượt đầu

<!-- LOCAL_ASSET: ./image-19-google-drive-ghi-de-xu-ly.png -->
![Ghi đè chunking ở cấp nguồn](minio://knowledge-base-prd/10012/exports/0d0b7fca-af3f-470d-884a-e79bd171cad4.png)

*Ảnh 12.5 - Giá trị 0 dùng cấu hình mặc định của KB.*

Giữ kích thước đoạn, độ chồng đoạn và giới hạn token ở `0`. Để trống ký tự phân tách nếu chưa có lý do kiểm thử rõ ràng. Chỉ bật đoạn cha-con khi nội dung cần giữ ngữ cảnh của phần cha lớn hơn.

<!-- LOCAL_ASSET: ./image-20-google-drive-da-phuong-thuc-va-parser.png -->
![Đa phương thức, ASR, OCR và parser](minio://knowledge-base-prd/10012/exports/463a8a6f-5f35-4dcd-b564-749ba6e283df.png)

*Ảnh 12.6 - VLM, ASR và OCR cần model/cấu hình tương ứng.*

- **Đa phương thức**: bật khi cần đọc nội dung trong hình và KB đã có model VLM.
- **ASR**: bật cho tệp âm thanh khi có model ASR khả dụng.
- **Ép OCR toàn bộ PDF**: chỉ dùng cho bản scan hoặc PDF có lớp text hỏng.
- **Sinh câu hỏi**: tùy chọn bổ sung. Nó không cứu được nguồn viết kém.

## 6. Chọn parser đúng loại tệp

<!-- LOCAL_ASSET: ./image-21-google-drive-parser-office-text.png -->
![Parser cho Office, CSV, Markdown và text](minio://knowledge-base-prd/10012/exports/04d66134-3b6b-4233-becc-a468d1c33c71.png)

<!-- LOCAL_ASSET: ./image-22-google-drive-parser-media-web.png -->
![Parser cho media, email, ebook và web](minio://knowledge-base-prd/10012/exports/a2a0ab9c-e71f-49c0-9af0-e93eace1516b.png)

*Ảnh 12.7-12.8 - Danh sách parser có thể khác nhau theo tenant.*

| Loại tệp | Parser |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

<!-- LOCAL_ASSET: ./image-24-google-drive-parser-excel-tuy-chinh.png -->
![Parser Excel tùy chỉnh](minio://knowledge-base-prd/10012/exports/bd3e7580-e22d-417d-a1c6-9610417cfb48.png)

*Ảnh 12.9 - Parser có tiền tố lạ là cấu hình riêng của tenant, không phải mặc định chung.*

Chọn Excel ở chế độ **Thủ công** có thể hiện thêm những parser do tenant của bạn đăng ký. Đừng chọn parser tùy chỉnh chỉ vì tên nghe hợp lý. Workbook phải đúng cấu trúc mà parser đó yêu cầu, nếu không nội dung sẽ bị đọc sai.

## 7. Thận trọng với đồng bộ xóa

<!-- LOCAL_ASSET: ./image-23-google-drive-dong-bo-xoa.png -->
![Bật hoặc tắt đồng bộ xóa](minio://knowledge-base-prd/10012/exports/c2ec9f4c-a640-4908-aec2-7791fdfd0e78.png)

*Ảnh 12.10 - UI mô tả bật control sẽ gỡ tri thức khi tệp nguồn bị xóa.*

**Để tắt trong lượt thử đầu.**

Chỉ bật sau khi đã thử bằng một tệp không quan trọng, đã có backup, và đã xác nhận được cách phục hồi. Xóa tri thức khỏi KB là thao tác không hoàn tác trong giao diện.

## 8. Tạo nguồn và xác nhận thành công

Bấm **Tạo & đồng bộ ngay**.

<!-- LOCAL_ASSET: ./image-25-google-drive-dong-bo-thanh-cong.png -->
![Google Drive đã kết nối và đồng bộ thành công](minio://knowledge-base-prd/10012/exports/dea09974-90cf-42ed-80f9-25d00dfb3f4e.png)

*Ảnh 12.11 - Card nguồn báo Đã kết nối và Kết quả Thành công.*

> **Ảnh chụp một thời điểm, không phải danh mục hiện hành.** Tên kho, tên trợ lý, tên nguồn dữ liệu và các con số đếm nhìn thấy trong ảnh là của lúc chụp màn hình để viết hướng dẫn này. Chúng đổi liên tục. Xem ảnh để biết **giao diện nằm ở đâu**, đừng lấy ảnh để biết **hệ thống đang có gì** — mở thẳng hệ thống mà xem.

Card nguồn hiển thị: Trạng thái, Chế độ đồng bộ, Phạm vi, Lịch, Đồng bộ gần nhất và Kết quả. Đọc lại card và đối chiếu từng ô với đúng cấu hình bạn vừa chọn, nhất là chế độ và phạm vi.

Card báo **Thành công** chưa đủ. Vẫn phải:

1. Mở Documents và xác nhận tài liệu đã xuất hiện.
2. Chờ trạng thái xử lý hoàn tất.
3. Mở phân đoạn để kiểm tra parser đọc nội dung có đúng không.
4. Hỏi câu đúng, câu gần đúng, câu loại trừ và câu ngoài phạm vi.
5. Kiểm tra nguồn truy hồi, không chỉ đánh giá câu trả lời nghe có hợp lý hay không.
