<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 09 - Vận hành Documents, Wiki và Graph {#09-van-hanh-documents-wiki-graph}

## Bạn sẽ biết gì sau khi đọc

- Các cách thêm nội dung vào KB Tài liệu.
- Hành vi của Lưu nháp, Sửa nội dung và Phân tích lại.
- Giới hạn đã biết của upload thư mục và Graph.

**Kiểm chứng giao diện: 06/08/2026.**

## Menu Thêm tài liệu

Menu quan sát được có:

- **Tải tệp lên**
- **Tải thư mục lên**
- **Nhập từ URL** - đang disabled
- **Soạn thảo trực tuyến**

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/08-tai-tep-thu-muc-va-soan-thao.png -->
![Menu thêm tài liệu với tải tệp, tải thư mục, nhập URL và soạn trực tuyến](minio://knowledge-base-prd/10012/exports/633bc6ad-b471-4590-979c-1b637d086052.png)

*Ảnh 09.1 - `Nhập từ URL` đang vô hiệu hóa tại thời điểm kiểm tra.*

## Tải tệp lên

1. Bấm **Thêm tài liệu > Tải tệp lên**.
2. Chọn file hoặc kéo thả.
3. Mở **Xử lý nâng cao** nếu cần ghi đè parser/chunk cho lượt nạp.
4. Bấm tải lên và chờ **Hoàn tất**.
5. Mở chi tiết file để xem tóm tắt, toàn văn và phân đoạn.

Trạng thái Hoàn tất chỉ xác nhận pipeline kết thúc; vẫn phải kiểm tra nội dung phân đoạn và chat.

## Nạp một bộ Markdown có ảnh

1. Xác nhận KB asset có đủ 49 ảnh PNG đã được kiểm tra định dạng thật và mọi file đều có mapping MinIO.
2. Chạy build nghiêm ngặt.
3. Chỉ chọn đúng 20 file `.md` trong `knowledge/GS9 Knowledge VNG AI/` để nạp vào KB sử dụng.
4. Không chọn `knowledge/GS9 Knowledge VNG - Image Assets/` và không nạp PNG cùng bộ Markdown.
5. Sau khi xử lý xong, hỏi câu buộc trả lời kèm ảnh và mở nguồn tham khảo để kiểm tra URI.

## Tải thư mục lên

Modal thật dùng input `multiple` và `webkitdirectory`, có **Xử lý nâng cao**. Tuy nhiên extension không gắn được thư mục vào hộp chọn native, nên phép thử end-to-end “chọn thư mục thật rồi xác nhận cấu trúc” bị chặn.

Các file Aurora/Borealis được nạp riêng để tiếp tục test nội dung, không được dùng làm bằng chứng upload thư mục giữ cấu trúc thư mục con.

## Soạn thảo trực tuyến, Lưu nháp và Xuất bản

Phép thử tạo tài liệu `AUDIT-NHAP-20260806`:

- Bấm **Lưu nháp** hiện toast “Đã lưu bản nháp”.
- Tài liệu xuất hiện với trạng thái **Bản nháp**.
- Chat hỏi mã độc nhất trong bản nháp không truy hồi được nội dung đó.

Kết luận vận hành: dùng **Lưu nháp** để giữ nội dung chưa phát hành; cần **Xuất bản** và chờ lập chỉ mục nếu muốn chat sử dụng.

## Sửa nội dung tài liệu MANUAL

Với tài liệu tạo bằng Soạn thảo trực tuyến, menu chi tiết có nhãn chính xác **Sửa nội dung**.

Phép thử:

1. Tài liệu gốc có 3 chunk.
2. Thêm marker kiểm thử và bấm **Xuất bản**.
3. Toast báo bắt đầu lập chỉ mục; trạng thái đi qua Chờ xử lý, Đang hoàn tất, Hoàn tất.
4. Tóm tắt có marker và số chunk thành 4.
5. Phục hồi đúng nội dung gốc, Xuất bản lại; marker biến mất và số chunk trở về 3.

Do đó, **Sửa nội dung + Xuất bản** thực sự kích hoạt lập chỉ mục lại.

## Phân tích lại

**Phân tích lại** giữ tài liệu trong KB và chạy pipeline lần nữa. Trong test Aurora/Borealis, thời gian tải lên không đổi, tóm tắt đổi cách diễn đạt, số chunk giữ nguyên. Ghi ảnh hoặc số liệu trước/sau nếu muốn đánh giá thay đổi; đừng dựa vào cảm giác.

## Wiki và Graph sau cập nhật

Sau khi nạp thêm ảnh và tài liệu, Graph tăng từ 66 lên 93 node. Ở lượt đối chiếu cuối cùng, Graph tiếp tục tăng lên 159 node khi các nguồn nền tiếp tục hoàn tất; phân bố lúc đó là Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0 và So sánh 0. Số node thay đổi chứng minh Graph tiếp tục được cập nhật, nhưng **Tổng hợp** và **So sánh** vẫn bằng 0 ngay cả khi có tài liệu so sánh rõ và Wiki ở mức Toàn diện.

Không có nút tạo tay hai node này trong menu node hoặc hướng dẫn canvas đã quan sát. Điều kiện sinh vẫn là backlog.

## Quy trình vận hành một thay đổi

1. Lưu bản nguồn có phiên bản.
2. Sửa một nhóm nội dung.
3. Nạp hoặc Xuất bản.
4. Chờ Hoàn tất.
5. So sánh số chunk, tóm tắt và nguồn truy hồi.
6. Chạy bộ câu hỏi hồi quy.
7. Kiểm tra Wiki/Graph nếu đang dùng.
8. Ghi ngày, người thực hiện và kết quả.
