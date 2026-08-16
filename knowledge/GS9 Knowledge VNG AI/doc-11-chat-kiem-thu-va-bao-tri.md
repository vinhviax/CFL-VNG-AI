<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 11 - Chat, kiểm thử và bảo trì {#11-chat-kiem-thu-va-bao-tri}

Đọc xong bạn biết cách chấm một câu trả lời bằng nguồn thay vì bằng cảm giác, cách làm ảnh hiện được trong chat, và những việc phải duy trì để KB không hỏng dần theo thời gian.

## Bạn sẽ biết gì sau khi đọc

- Cách đánh giá một câu trả lời bằng nguồn, không chỉ bằng văn phong.
- Cách làm ảnh xuất hiện trong chat.
- Cách duy trì KB mà không mất khả năng phục hồi.

## Quy trình kiểm thử chat

1. Chờ tài liệu ở trạng thái **Hoàn tất**.
2. Mở **Trò chuyện**.
3. Hỏi một câu có đáp án rõ ràng trong nguồn.
4. Mở **Nguồn tham khảo** hoặc xem các bước truy hồi.
5. Kiểm tra file và đoạn được lấy có đúng không.
6. Đánh giá câu trả lời có giữ đúng điều kiện, số liệu và ngoại lệ không.
7. Hỏi lại cùng ý nhưng bằng từ khác.
8. Hỏi một câu ngoài phạm vi để xem hệ thống có bịa, hay có kéo một nguồn gần giống không.

Nguyên tắc chung: **nếu nguồn truy hồi đã sai thì đừng đổi model chat.** Kiểm tra dữ liệu, parser và phân đoạn trước.

## Chẩn đoán theo lớp

| Hiện tượng | Kiểm tra trước |
|---|---|
| Không có nguồn đúng | File đã Xuất bản chưa, trạng thái, index, parser, phân đoạn |
| Có nguồn nhưng thiếu đoạn quan trọng | Ranh giới đoạn, heading, kích thước đoạn cha-con |
| Nguồn đúng nhưng trả lời sai | Model chat, prompt, nội dung mâu thuẫn trong chính nguồn |
| FAQ kéo nhầm mục | Biến thể, câu loại trừ, chế độ index, ngưỡng |
| Ảnh được mô tả nhưng không hiện | Loại đường dẫn ảnh trong Markdown |

## Ảnh trong chat

Ảnh chỉ hiện được trong câu trả lời khi Markdown trỏ tới đúng liên kết nội bộ mà hệ thống sinh ra sau khi ảnh được upload. Liên kết này bắt đầu bằng `minio://`, khác hẳn đường dẫn tệp trên máy bạn.

- Nếu Markdown dùng **đường dẫn tương đối** kiểu `assets/...`, hệ thống vẫn tìm thấy file và mô tả được nội dung ảnh, nhưng câu trả lời chỉ có chữ, không có hình.
- Nếu Markdown dùng **liên kết nội bộ của ảnh đã upload**, câu trả lời hiển thị đúng hình.

<!-- LOCAL_ASSET: ./image-13-chat-hien-thi-anh-minio.png -->
![Câu trả lời Knowledge VNG hiển thị ảnh khi nguồn Markdown dùng URI MinIO](minio://knowledge-base-prd/10012/626377f3-cbdb-4ab6-8ad5-9029a2d9c316/0ba30d71-7fd7-46d5-b548-69ee3e1741c3.png)

*Ảnh 11.1 - Trường hợp đạt: ảnh xuất hiện trực tiếp trong câu trả lời chat.*

Quy trình chuẩn cho một bộ tài liệu có ảnh:

1. Giữ bản ảnh gốc ở máy để dựng tài liệu offline.
2. Nạp ảnh một lần vào kho tri thức dành riêng cho ảnh, có vòng đời ổn định.
3. Lấy liên kết nội bộ (`minio://...`) của từng ảnh sau khi nạp và lưu lại thành một bảng tra.
4. Thay liên kết ảnh trong các file Markdown phân phối bằng liên kết nội bộ đó.
5. Chỉ nạp file Markdown vào KB dùng để chat; không nạp ảnh vào cùng KB đó.
6. Hỏi một câu có chủ đích *"trả lời kèm hình minh họa"*.
7. Xác nhận ảnh thật xuất hiện và nguồn tham khảo trỏ đúng liên kết mới.
8. Không xóa ảnh đã nạp khi vẫn còn tài liệu Markdown tham chiếu tới nó.

## Bản nháp không phải nguồn chat

Nội dung ở trạng thái **Bản nháp** không được đưa vào chỉ mục nên chat không truy hồi được.

Checklist phát hành vì vậy luôn phải có ba bước: **Xuất bản**, chờ lập chỉ mục xong, rồi chạy câu hỏi xác nhận.

## Bộ kiểm thử tối thiểu

Mỗi KB nên có một bộ câu hỏi cố định gồm:

| Loại câu hỏi | Số lượng |
|---|---:|
| Đúng nguyên văn | 5 |
| Diễn đạt tự nhiên hoặc không dấu | 5 |
| Cần điều kiện hoặc ngoại lệ | 3 |
| Gần giống nhưng khác ý định | 3 |
| Ngoài phạm vi | 3 |
| Yêu cầu ảnh, nếu nội dung có ảnh | 2 |

Ghi kết quả kèm ngày chạy, model, cấu hình index và phân đoạn, phiên bản nguồn.

## Bảo trì

- Chỉ định rõ owner nghiệp vụ và owner kỹ thuật cho mỗi KB.
- Ghi phiên bản, ngày hiệu lực và lịch xem lại cho từng nguồn.
- Xuất FAQ trước mọi thay đổi lớn. Giữ file gốc của KB Tài liệu ở ngoài hệ thống.
- Sau khi đổi model, parser, phân đoạn hoặc index, chạy lại toàn bộ bộ câu hỏi hồi quy.
- Khi thêm hoặc thay ảnh, kiểm tra lại định dạng thật của file trước khi upload.
- Không xóa ảnh đã nạp nếu Markdown còn tham chiếu tới liên kết của ảnh đó.
- Kiểm tra cả khối **Nguồn tham khảo**, không chỉ nội dung câu trả lời. Tóm tắt do hệ thống tự sinh cũng hiện ở đó và có thể lộ dữ liệu nhạy cảm.

## Tiêu chí phát hành

Một KB sẵn sàng khi:

1. Nguồn đã có owner và phiên bản.
2. Cấu hình nền tảng được ghi lại.
3. Các file đều **Hoàn tất** và nội dung phân đoạn đọc được.
4. Bộ câu hỏi đúng, gần đúng, loại trừ và ngoài phạm vi đã chạy hết.
5. Nguồn truy hồi đúng, không chỉ câu trả lời nghe hay.
6. Ảnh quan trọng đã được kiểm thử đến tận đầu ra chat.
7. Khối Nguồn tham khảo không lộ dữ liệu nhạy cảm.
8. Có backup và quy trình phục hồi.
