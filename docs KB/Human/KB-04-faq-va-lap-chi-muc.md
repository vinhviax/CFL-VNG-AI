# 04 - KB FAQ và lập chỉ mục {#04-faq-va-lap-chi-muc}

## Bạn sẽ biết gì sau khi đọc

- Hai cấu hình lập chỉ mục của FAQ.
- Tác động của **Chỉ câu hỏi** và **Câu hỏi + trả lời**.
- Cách chọn **Gộp** hoặc **Tách** mà không suy đoán.

## Cấu trúc một mục FAQ

Form **Thêm Q&A** có:

- 1 **Câu hỏi chuẩn**, tối đa 200 ký tự.
- Tối đa 10 **Câu hỏi tương tự**.
- Tối đa 10 **Câu hỏi loại trừ**.
- Tối đa 5 **Câu trả lời**.
- **Phân loại**.

![Biểu mẫu Thêm Q&A với câu hỏi chuẩn, biến thể, loại trừ và câu trả lời](<knowledge/GS9 Knowledge VNG AI/image-12-faq-bieu-mau-them-qa.png>)

*Ảnh 04.1 - Mỗi mục FAQ có thể chứa nhiều biến thể và nhiều câu trả lời.*

## Chế độ lập chỉ mục

| Chế độ | Nội dung tham gia tìm kiếm | Dùng khi |
|---|---|---|
| **Chỉ câu hỏi** | Câu hỏi chuẩn và biến thể | Muốn match tập trung, đã viết đủ cách hỏi |
| **Câu hỏi + trả lời** | Câu hỏi và nội dung trả lời | Người dùng có thể gõ mã lỗi, tên vật phẩm hoặc thuật ngữ chỉ có trong câu trả lời |

Với một từ khóa chỉ tồn tại trong câu trả lời:

- Ở **Chỉ câu hỏi**, không có kết quả kể cả khi hạ ngưỡng về 0.
- Ở **Câu hỏi + trả lời**, mục đúng được tìm thấy.

Đây là khác biệt về phạm vi index, không chỉ là điểm similarity thấp.

## Cách index câu hỏi

| Cách | Cơ chế hiển thị | Ý nghĩa vận hành |
|---|---|---|
| **Tách** | Biến thể khớp có thể hiện riêng | Dễ biết cách hỏi nào kéo được mục |
| **Gộp** | Câu hỏi chuẩn và biến thể nằm trong đại diện gộp | Có thể thay đổi điểm theo toàn bộ cụm câu hỏi |

Chênh lệch điểm giữa Gộp và Tách trên vài mẫu là rất nhỏ, không đủ để kết luận cách nào tốt hơn. Giữ **Tách** làm điểm xuất phát là hợp lý, sau đó đo trên ticket thật.

## Banner nói bị khóa, control vẫn lưu được

Trên FAQ đã có nội dung, giao diện cảnh báo index bị khóa. Thao tác thật vẫn đổi và lưu được cả hai cặp lựa chọn. Đây là **mâu thuẫn giao diện**.

Quy trình khi đổi:

1. Ghi lại cấu hình hiện tại.
2. Đổi một biến tại một thời điểm.
3. Lưu và mở lại để xác nhận giá trị được giữ.
4. Chạy bộ câu hỏi kiểm thử ở cùng ngưỡng.
5. Nếu kết quả xấu đi, phục hồi cấu hình cũ.

## Viết câu hỏi tốt

- Câu hỏi chuẩn mô tả ý định chính, không cố nhồi mọi từ khóa.
- Câu hỏi tương tự lấy từ cách người dùng nói thật: viết tắt, không dấu, tên màn hình cũ.
- Câu hỏi loại trừ dành cho ý định gần giống nhưng phải đi sang quy trình khác.
- Câu trả lời ghi rõ phạm vi, bước làm, ngoại lệ và thời điểm cần chuyển cấp.

## Không để FAQ trở thành kho câu trả lời mâu thuẫn

Nếu hai mục có câu hỏi gần nhau nhưng trả lời khác, thêm điều kiện phân biệt vào câu hỏi chuẩn và câu trả lời. Dùng **Kiểm tra tìm kiếm** để xem cả hai mục có cùng xuất hiện ở ngưỡng vận hành hay không.
