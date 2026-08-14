# Hướng dẫn kết nối Google Drive với Knowledge VNG

> Kiểm chứng giao diện: 07/08/2026  
> Phạm vi: Google Drive bằng service account, nguồn nằm trong My Drive.  
> Không bao giờ đưa service-account JSON/private key vào tài liệu hoặc ảnh chụp.

## 1. Chuẩn bị Google Cloud

1. Tạo hoặc chọn một Google Cloud project dành cho connector.
2. Bật **Google Drive API** trong đúng project.
3. Vào **IAM & Admin → Service Accounts** và tạo một service account riêng cho KB.
4. Không cần gán Google Cloud role chỉ để đọc tài liệu Drive đã được chia sẻ.
5. Mở tab **Keys → Add key → Create new key → JSON**. Google tự sinh `private_key`; không ghi key thủ công.
6. Ghi lại trường `client_email`, sau đó giữ file JSON ở nơi quản lý secret an toàn.

## 2. Chia sẻ đúng thư mục Drive

Trong Google Drive, chia sẻ duy nhất thư mục nguồn cho `client_email` với quyền **Viewer/Người xem**.

Không chọn toàn bộ My Drive và không chia sẻ thư mục chứa key, mật khẩu hoặc credential. Nếu dùng My Drive, để trống **Shared Drive ID**. Nếu dùng Shared Drive, phải thêm service account vào đúng drive và điền ID của Shared Drive; nhánh này chưa được kiểm chứng trong lượt test ngày 07/08/2026.

## 3. Nhập thông tin xác thực

![Thông tin xác thực Google Drive](<../knowledge/GS9 Knowledge VNG - Image Assets/15-google-drive-xac-thuc-service-account.png>)

- **Tên:** nhãn dễ nhận biết, ví dụ `Drive CFL Viax`.
- **Service account JSON:** dán nguyên file JSON từ `{` đến `}`; không thêm Markdown fence.
- **Shared Drive ID:** để trống khi nguồn là My Drive.
- Bấm **Kiểm tra kết nối** trước khi bấm Tiếp.

Nếu gặp `connection validation failed`, kiểm tra Google Drive API đã được bật trong đúng `project_id` của JSON chưa. Trong phép thử thực tế, đây là nguyên nhân khiến kết nối thất bại; sau khi Enable API, không cần tạo lại key.

## 4. Chọn tài nguyên

![Chọn tài nguyên Google Drive](<../knowledge/GS9 Knowledge VNG - Image Assets/16-google-drive-chon-tai-nguyen.png>)

- Dấu ✓ cam: đã chọn.
- Dấu − cam ở thư mục cha: chỉ một phần nội dung con được chọn.
- Vòng tròn trắng: chưa chọn.
- Nhãn **Hiện chưa hỗ trợ:** connector thấy tài nguyên nhưng chưa hỗ trợ loại đó.

Chọn thư mục nếu muốn các tệp mới trong thư mục được đưa vào phạm vi đồng bộ. Chọn một tệp khi chỉ muốn thử nghiệm hẹp. Không chọn thư mục `keys` hoặc bất kỳ vùng nào chứa secret.

## 5. Chọn lịch và cách đồng bộ

![Lịch và cách đồng bộ](<../knowledge/GS9 Knowledge VNG - Image Assets/17-google-drive-lich-va-cach-dong-bo.png>)

| Control | Dùng khi nào |
|---|---|
| Phút/Giờ | Dữ liệu LiveOps thay đổi thường xuyên; 15 phút phù hợp test, không phải mặc định bắt buộc |
| Hằng ngày | Runbook hoặc báo cáo cập nhật theo ngày |
| Hằng tuần/Tháng | Tài liệu ít đổi hoặc báo cáo định kỳ |
| Tăng dần | Đồng bộ vận hành thường xuyên; chỉ lấy mục thay đổi từ lần trước |
| Toàn bộ | Khởi tạo lại hoặc cần quét toàn bộ phạm vi |
| Ghi đè | Google Drive là nguồn chuẩn và KB không được sửa tay |
| Bỏ qua nếu đã có | Muốn bảo vệ bản đang tồn tại trong KB; cần chấp nhận khả năng không nhận bản cập nhật |

Khuyến nghị chung: **Tăng dần + Ghi đè** khi Drive là nguồn chuẩn. Dùng Toàn bộ có chủ đích, không đặt làm thao tác thử liên tục trên kho lớn.

## 6. Lọc tệp và gắn tag

![Lọc tệp và gắn tag](<../knowledge/GS9 Knowledge VNG - Image Assets/18-google-drive-loc-tep-va-tag.png>)

- Để trống regex nếu muốn nhận mọi tệp hợp lệ trong phạm vi.
- Khi có nhiều regex, tệp chỉ cần khớp một mẫu.
- Dùng `(?i)` nếu muốn không phân biệt hoa/thường.
- Regex áp dụng cho tên tệp; phải kiểm thử bằng một tệp khớp và một tệp không khớp trước khi dùng production.
- Tag mặc định nên mô tả nguồn hoặc nghiệp vụ, ví dụ `source-google-drive`, `game-cfl`.
- Rule tag theo đường dẫn hỗ trợ capture regex; chỉ dùng khi quy ước thư mục ổn định.

## 7. Ghi đè cấu hình xử lý

![Cấu hình chunking nâng cao](<../knowledge/GS9 Knowledge VNG - Image Assets/19-google-drive-ghi-de-xu-ly.png>)

Để `0` hoặc để trống để dùng mặc định KB. Chỉ ghi đè kích thước đoạn, độ chồng, token, đoạn cha-con, ký tự phân tách hoặc ngôn ngữ khi đã có bộ câu hỏi kiểm thử và lý do rõ ràng.

![Đa phương thức, ASR, OCR và parser](<../knowledge/GS9 Knowledge VNG - Image Assets/20-google-drive-da-phuong-thuc-va-parser.png>)

- Bật đa phương thức khi cần phân tích ảnh/hình trong tài liệu và đã cấu hình VLM.
- Bật ASR cho tệp âm thanh khi có model ASR khả dụng.
- Chỉ ép OCR toàn bộ PDF khi tài liệu là scan hoặc text-layer hỏng; thao tác này có thể tốn thời gian hơn.
- Sinh câu hỏi là tùy chọn bổ sung, không thay thế nội dung nguồn tốt.

## 8. Parser theo loại tệp

![Parser Office và text](<../knowledge/GS9 Knowledge VNG - Image Assets/21-google-drive-parser-office-text.png>)

![Parser media và web](<../knowledge/GS9 Knowledge VNG - Image Assets/22-google-drive-parser-media-web.png>)

| Loại tệp | Parser quan sát được |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Hình ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

Danh sách model/parser có thể phụ thuộc tenant và thay đổi sau ngày kiểm chứng.

### Excel tùy chỉnh

![Parser Excel tùy chỉnh](<../knowledge/GS9 Knowledge VNG - Image Assets/24-google-drive-parser-excel-tuy-chinh.png>)

Khi chọn **Thủ công**, dropdown có thể hiện parser do tenant đăng ký. Các lựa chọn `FPA · Monthly Performance` và `FPA · Launching & Checkpoint` trong ảnh là ví dụ tenant, không phải parser mặc định cho mọi người dùng.

## 9. Đồng bộ xóa

![Đồng bộ xóa](<../knowledge/GS9 Knowledge VNG - Image Assets/23-google-drive-dong-bo-xoa.png>)

Khi bật, UI mô tả tri thức sẽ bị gỡ nếu nguồn đã bị xóa. Khuyến nghị để **tắt trong lượt thử đầu**, sau đó kiểm thử bằng một tệp không quan trọng trước khi bật trên nguồn thật. Lượt ngày 07/08/2026 chưa xác nhận hành vi xóa end-to-end.

## 10. Tạo nguồn và kiểm tra kết quả

Bấm **Tạo & đồng bộ ngay**. Sau khi hoàn tất, card nguồn cần hiển thị trạng thái kết nối, chế độ, phạm vi, lịch, thời điểm gần nhất và kết quả.

![Google Drive kết nối và đồng bộ thành công](<../knowledge/GS9 Knowledge VNG - Image Assets/25-google-drive-dong-bo-thanh-cong.png>)

Trong lượt test:

- Đã kết nối.
- Tăng dần.
- Một tệp.
- Mỗi 15 phút.
- Đồng bộ gần nhất vừa xong.
- Kết quả Thành công.

Sau đó cần mở Documents và kiểm tra tài liệu đã xuất hiện, trạng thái xử lý hoàn tất, chunk có nội dung đúng và chat trả lời được câu hỏi đối chứng. Một card “Thành công” mới chỉ xác nhận lượt connector hoàn tất, chưa chứng minh chất lượng nội dung sau parser.

## 11. Checklist vận hành

- [ ] Drive API đã Enable trong đúng project.
- [ ] JSON là key service account đầy đủ, chưa bị thu hồi.
- [ ] Service account chỉ có Viewer trên thư mục nguồn cần thiết.
- [ ] Shared Drive ID để trống cho My Drive.
- [ ] Không chọn thư mục secret/`keys`.
- [ ] Regex đã thử cả trường hợp khớp và không khớp.
- [ ] Ghi đè chỉ dùng khi Drive là nguồn chuẩn.
- [ ] Đồng bộ xóa chưa bật trước khi có phép thử an toàn.
- [ ] Card nguồn báo Thành công.
- [ ] Documents, chunk và chat đã được kiểm thử sau đồng bộ.
