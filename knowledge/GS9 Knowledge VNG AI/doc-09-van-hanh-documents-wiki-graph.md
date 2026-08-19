<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 09 - Vận hành Documents, Wiki và Graph {#09-van-hanh-documents-wiki-graph}

Đọc xong bạn biết cách đưa nội dung vào KB Tài liệu, cách sửa lại nội dung đã nạp, và cách kiểm tra kết quả trước khi coi là xong.

## Bạn sẽ biết gì sau khi đọc

- Các cách thêm nội dung vào KB Tài liệu.
- Hành vi của Lưu nháp, Sửa nội dung và Phân tích lại.
- Giới hạn đã biết của upload thư mục và Graph.

## Menu Thêm tài liệu

Menu **Thêm tài liệu** có bốn lựa chọn:

- **Tải tệp lên**
- **Tải thư mục lên**
- **Nhập từ URL** - đang vô hiệu hóa
- **Soạn thảo trực tuyến**

<!-- LOCAL_ASSET: ./image-08-tai-tep-thu-muc-va-soan-thao.png -->
![Menu thêm tài liệu với tải tệp, tải thư mục, nhập URL và soạn trực tuyến](minio://knowledge-base-prd/10012/0cae5894-ed0a-4380-b3f5-5577d9eb03d2/8349685e-136a-4901-ae2f-e037ec38e17e.png)

*Ảnh 09.1 - `Nhập từ URL` đang vô hiệu hóa tại thời điểm kiểm tra.*

## Tải tệp lên

1. Bấm **Thêm tài liệu > Tải tệp lên**.
2. Chọn file hoặc kéo thả.
3. Mở **Xử lý nâng cao** nếu cần ghi đè parser hoặc phân đoạn cho riêng lượt nạp này.
4. Bấm tải lên và chờ trạng thái **Hoàn tất**.
5. Mở chi tiết file để xem tóm tắt, toàn văn và phân đoạn.

Trạng thái **Hoàn tất** chỉ xác nhận pipeline đã chạy xong. Nó không xác nhận nội dung được đọc đúng. Vẫn phải mở phân đoạn kiểm tra và hỏi thử trong chat.

## Nạp một bộ Markdown có ảnh

Khi bộ tài liệu có ảnh minh họa, tách hai việc ra:

1. Nạp ảnh một lần vào kho tri thức dành riêng cho ảnh, có vòng đời ổn định.
2. Gắn liên kết ảnh vào các file Markdown phân phối.
3. Chỉ nạp các file `.md` vào KB dùng để chat. Không nạp lẫn PNG cùng bộ Markdown.
4. Sau khi xử lý xong, hỏi một câu buộc câu trả lời phải kèm hình.
5. Mở **Nguồn tham khảo** để xác nhận ảnh lấy đúng từ liên kết đã gắn.

Cách làm ảnh hiển thị được trong chat nằm ở phần Ảnh trong chat của module 11.

## Tải thư mục lên

Modal **Tải thư mục lên** cho chọn cả thư mục và có **Xử lý nâng cao** như khi tải từng tệp.

Chưa xác nhận được thư mục con có giữ nguyên cấu trúc sau khi nạp hay không. Nếu cấu trúc thư mục quan trọng với bạn, hãy nạp thử một thư mục nhỏ trước rồi đối chiếu danh sách tài liệu, thay vì nạp cả bộ lớn ngay.

## Soạn thảo trực tuyến, Lưu nháp và Xuất bản

Soạn thảo trực tuyến tạo tài liệu ngay trên nền tảng, không cần file nguồn.

- **Lưu nháp** hiện thông báo *"Đã lưu bản nháp"* và tài liệu xuất hiện với trạng thái **Bản nháp**.
- **Bản nháp không được đưa vào chỉ mục.** Chat sẽ không tìm thấy nội dung trong bản nháp.

Dùng **Lưu nháp** để giữ nội dung chưa muốn phát hành. Khi muốn chat sử dụng được, phải bấm **Xuất bản** và chờ lập chỉ mục xong.

## Sửa nội dung tài liệu đã soạn trực tuyến

Với tài liệu tạo bằng Soạn thảo trực tuyến, menu chi tiết có mục tên chính xác là **Sửa nội dung**.

Cách sửa và xác nhận:

1. Ghi lại số phân đoạn hiện tại của tài liệu.
2. Mở **Sửa nội dung**, chỉnh nội dung.
3. Bấm **Xuất bản**. Thông báo báo bắt đầu lập chỉ mục; trạng thái đi qua Chờ xử lý, Đang hoàn tất rồi Hoàn tất.
4. So lại tóm tắt và số phân đoạn với con số đã ghi.

**Sửa nội dung + Xuất bản** thực sự kích hoạt lập chỉ mục lại. Nội dung thêm vào sẽ làm số phân đoạn tăng; bỏ đi thì giảm về như cũ.

## Phân tích lại

**Phân tích lại** giữ nguyên tài liệu trong KB và chạy lại pipeline xử lý.

Kết quả thường thấy: thời gian tải lên không đổi, tóm tắt được sinh lại nên đổi cách diễn đạt, số phân đoạn có thể giữ nguyên.

Muốn biết Phân tích lại có tác dụng gì với tài liệu của bạn, hãy ghi ảnh chụp hoặc số liệu trước và sau. Đừng dựa vào cảm giác.

## Wiki và Graph sau cập nhật

Sau mỗi lượt nạp thêm nội dung, số node trên Graph tăng dần trong lúc các tài liệu tiếp tục được xử lý. Số node còn thay đổi nghĩa là Graph chưa dừng cập nhật, hãy chờ rồi xem lại.

Hai loại node **Tổng hợp** và **So sánh** có thể vẫn bằng 0 ngay cả khi KB đã có tài liệu so sánh rõ ràng và Wiki đặt ở mức Toàn diện. Không có nút tạo tay hai loại node này. Đừng mất thời gian tìm cách ép sinh chúng.

## Quy trình vận hành một thay đổi

1. Lưu bản nguồn có phiên bản.
2. Sửa một nhóm nội dung, không sửa dàn trải nhiều chỗ cùng lúc.
3. Nạp lại hoặc Xuất bản.
4. Chờ trạng thái **Hoàn tất**.
5. So sánh số phân đoạn, tóm tắt và nguồn truy hồi với trước khi sửa.
6. Chạy bộ câu hỏi hồi quy.
7. Kiểm tra Wiki và Graph nếu đang dùng.
8. Ghi lại ngày, người thực hiện và kết quả.
