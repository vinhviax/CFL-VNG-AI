<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 11 - Chat, kiểm thử và bảo trì {#11-chat-kiem-thu-va-bao-tri}

## Bạn sẽ biết gì sau khi đọc

- Cách đánh giá một câu trả lời bằng nguồn, không chỉ bằng văn phong.
- Cách làm ảnh xuất hiện trong chat Knowledge VNG.
- Cách duy trì KB mà không mất khả năng phục hồi.

**Kiểm chứng giao diện: 06/08/2026.**

## Quy trình kiểm thử chat

1. Chờ tài liệu ở trạng thái **Hoàn tất**.
2. Mở **Trò chuyện**.
3. Hỏi một câu có đáp án rõ trong nguồn.
4. Mở **Nguồn tham khảo** hoặc các bước truy hồi.
5. Kiểm tra file và đoạn được lấy có đúng không.
6. Đánh giá câu trả lời có giữ đúng điều kiện, số liệu và ngoại lệ không.
7. Hỏi lại bằng từ khác.
8. Hỏi một câu ngoài phạm vi để kiểm tra hệ thống có bịa hoặc kéo nguồn gần giống không.

## Chẩn đoán theo lớp

| Hiện tượng | Kiểm tra trước |
|---|---|
| Không có nguồn đúng | File đã xuất bản, trạng thái, index, parser, chunking |
| Có nguồn nhưng thiếu đoạn quan trọng | Ranh giới chunk, heading, kích thước cha-con |
| Nguồn đúng nhưng trả lời sai | Model chat, prompt, nội dung mâu thuẫn |
| FAQ kéo nhầm mục | Biến thể, câu loại trừ, chế độ index, ngưỡng |
| Ảnh được mô tả nhưng không hiện | Loại đường dẫn ảnh trong Markdown |

## Ảnh trong chat: kết quả kiểm thử

Khi Markdown dùng đường dẫn tương đối `assets/...`, retriever tìm thấy file và nội dung ảnh, nhưng câu trả lời chỉ ghi mô tả và không có thẻ ảnh.

Khi Markdown dùng URI nội bộ `minio://...`, retriever chuyển liên kết thành ảnh và câu trả lời hiển thị đúng hình.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/13-chat-hien-thi-anh-minio.png -->
![Câu trả lời Knowledge VNG hiển thị ảnh khi nguồn Markdown dùng URI MinIO](minio://knowledge-base-prd/10012/exports/4d21ed4e-4907-4f09-a8c5-1399f499ee03.png)

*Ảnh 11.1 - Trường hợp đạt: ảnh xuất hiện trực tiếp trong câu trả lời chat.*

Quy trình chuẩn cho bộ Knowledge có ảnh:

1. Giữ ảnh local trong `knowledge/GS9 Knowledge VNG - Image Assets/` để dựng HTML offline.
2. Nạp ảnh một lần vào KB asset có vòng đời ổn định.
3. Lấy và lưu URI MinIO trong `knowledge/GS9 Knowledge VNG AI/image-map.json`.
4. Chạy builder để sinh liên kết MinIO vào 20 file phân phối.
5. Chỉ nạp 20 file MD vào KB sử dụng; không nạp PNG vào KB sử dụng.
6. Hỏi câu có chủ đích “trả lời kèm hình minh họa”.
7. Xác nhận ảnh thật xuất hiện và nguồn Markdown dùng URI của KB asset.
8. Không xóa KB asset hoặc ảnh độc lập khi còn Markdown tham chiếu.

## Bản nháp không phải nguồn chat

Phép thử mã độc nhất trong tài liệu **Bản nháp** không được truy hồi. Vì vậy checklist phát hành phải có bước **Xuất bản**, chờ index và chạy câu hỏi xác nhận.

## Bộ kiểm thử tối thiểu

Mỗi KB nên có một file kiểm thử gồm:

- 5 câu hỏi đúng nguyên văn.
- 5 câu diễn đạt tự nhiên hoặc không dấu.
- 3 câu cần điều kiện/ngoại lệ.
- 3 câu gần giống nhưng không cùng ý định.
- 3 câu ngoài phạm vi.
- 2 câu yêu cầu ảnh nếu nội dung có ảnh.

Ghi kết quả theo ngày, model, cấu hình index/chunk và phiên bản nguồn.

## Bảo trì

- Chỉ định owner nghiệp vụ và owner kỹ thuật.
- Ghi phiên bản, ngày hiệu lực và lịch xem lại cho nguồn.
- Xuất FAQ trước thay đổi lớn; giữ file gốc của KB Tài liệu ngoài hệ thống.
- Sau khi đổi model, parser, chunking hoặc index, chạy lại toàn bộ câu hỏi hồi quy.
- Khi thêm hoặc thay ảnh, kiểm tra lại định dạng thật trước khi upload; nếu cần transcode, giữ nguyên tên và kích thước ảnh khi phù hợp.
- Không xóa ảnh độc lập nếu MD còn tham chiếu URI MinIO của ảnh đó.
- Ghi các mục chưa kiểm chứng riêng, không trộn thành hướng dẫn chắc chắn.

## Tiêu chí phát hành

Một KB sẵn sàng khi:

1. Nguồn đã có owner và phiên bản.
2. Cấu hình nền tảng được ghi lại.
3. Các file đều Hoàn tất và nội dung phân đoạn đọc được.
4. Bộ câu hỏi đúng, gần đúng, loại trừ và ngoài phạm vi đã chạy.
5. Nguồn truy hồi đúng, không chỉ câu trả lời nghe hay.
6. Ảnh quan trọng đã được kiểm thử đến đầu ra chat.
7. Có backup và quy trình phục hồi.
