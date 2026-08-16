<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 18 - Agent: chat, nguồn, lịch sử và đánh giá {#18-chat-nguon-lich-su-va-danh-gia}

## Bạn sẽ biết gì sau khi đọc

- Cách kiểm một câu trả lời bằng nguồn tham khảo thay vì bằng cảm giác.
- Lịch sử hội thoại dùng được vào việc gì và không dùng được vào việc gì.
- Cách gửi và xử lý đánh giá **Hữu ích** / **Chưa hữu ích**.
- Bộ bằng chứng tối thiểu khi báo một lỗi câu trả lời.

## Câu trả lời nghe hợp lý chưa phải là câu trả lời đúng

Chat là bề mặt người dùng nhìn thấy. Nguồn tham khảo, lịch sử, đánh giá và **Thông tin request** là bề mặt để bạn kiểm chứng.

Một câu trả lời trôi chảy chỉ là giả thuyết. Phải mở nguồn, xem tài liệu đó có thật sự chứa điều Agent vừa nói hay không, rồi mới kết luận về Agent hay về kho tri thức.

Mỗi lần bấm **Cuộc trò chuyện mới** là một phiên riêng. Câu hỏi nối tiếp phải được thử **trong cùng một hội thoại**. Đừng giả định Agent nhớ những gì đã nói ở phiên trước.

<!-- LOCAL_ASSET: ./image-33-agent-chat-nguon-va-anh.png -->
![Câu trả lời RAG, nguồn và ảnh trong Markdown](minio://knowledge-base-prd/10012/b211db99-3998-40d2-ac2f-190becd86008/ba25c89e-5909-4656-bf78-3ec5b1384da4.png)

*Ảnh 18.1 - Câu trả lời cần kiểm cả nguồn tham khảo và ảnh hiển thị, không chỉ phần chữ.*

## Các bề mặt trong màn hình chat

| Bề mặt | Dùng để làm gì | Cách kiểm |
|---|---|---|
| Cuộc trò chuyện mới | Cô lập một tình huống thử | Mỗi phiên đặt một câu hỏi, ghi lại cấu hình đang dùng |
| Lịch sử | Mở lại hội thoại cũ, hỏi nối tiếp | Dùng để tái hiện ngữ cảnh, không dùng để suy ra Agent có trí nhớ lâu dài |
| Nguồn tham khảo / Xem file | Căn cứ của câu trả lời | Mở đúng tệp, đối chiếu từng khẳng định với nội dung |
| Hữu ích / Chưa hữu ích | Tín hiệu từ người dùng | Là chỉ dấu cần điều tra, không phải kết luận nguyên nhân |
| Hộp xử lý | Hàng đợi điều tra phản hồi | Chuyển **Mới → Đang xem → Đã xử lý** kèm bằng chứng đã chạy lại |
| Thông tin request | Thông tin kỹ thuật của một lượt hỏi | Dùng để định vị đúng lượt hỏi khi cần hỗ trợ |

Ngoài ra mỗi câu trả lời còn có nút **Sao chép** và **Thêm vào tri thức**.

## Các bước kiểm một câu trả lời

1. Mở **Cuộc trò chuyện mới**. Ghi lại Agent, mô hình, kho tri thức đang gắn.
2. Gửi câu hỏi và chờ trả lời xong. Đừng chụp màn hình khi giao diện còn báo đang tải, dễ ghi nhầm câu trả lời dở dang.
3. Mở nguồn của từng khẳng định quan trọng. Kiểm đúng tên tệp và đúng đoạn được trích.
4. Nếu cần báo lỗi hoặc nhờ hỗ trợ, bấm **Thông tin request**. Che các mã định danh và đường dẫn trước khi gửi ảnh chụp cho người khác.
5. Bấm **Hữu ích** hoặc **Chưa hữu ích** kèm một câu nhận xét ngắn về điều bạn mong đợi.
6. Trong **Hộp xử lý**, phân loại phản hồi rồi mới xử lý: lỗi nguồn, lỗi truy hồi, lỗi prompt, lỗi mô hình hoặc hạn mức, lỗi tệp đính kèm, hay lỗi quyền truy cập.

## Vòng đời một phản hồi

```text
hội thoại → câu trả lời kèm nguồn
          → người dùng đánh giá (Hữu ích / Chưa hữu ích + bình luận)
          → tổng quan đánh giá → Hộp xử lý
          → điều tra bằng nguồn và Thông tin request
          → sửa đúng một lớp → chạy lại → Đã xử lý
```

Lịch sử giúp tái hiện ngữ cảnh hội thoại. Nó không thay việc ghi lại cấu hình: mô hình, hạn mức hoặc thiết lập Agent đều có thể đã đổi sau đó.

## Bộ tình huống nên chạy thử

| Tình huống | Thao tác | Cần chứng minh |
|---|---|---|
| Hỏi thẳng | Một câu hỏi có đáp án chuẩn trong kho | Nguồn đúng và câu trả lời đúng |
| Hỏi nối tiếp | "Ai phụ trách?" ngay sau câu trên | Ghi rõ Agent có dùng ngữ cảnh trước đó hay không |
| Nội dung mâu thuẫn | Câu hỏi chạm vào hai tài liệu khác nhau | Agent lộ ra chỗ mâu thuẫn thay vì che đi |
| Không có dữ liệu | Hỏi một chính sách không tồn tại | Agent kết luận thiếu nguồn, không bịa |
| Mở nguồn | Bấm vào nguồn tham khảo | Nội dung được dẫn có thật trong tệp |
| Thông tin request | Mở bảng thông tin | Lấy được thông tin định vị lượt hỏi |
| Đánh giá | Bấm Hữu ích / Chưa hữu ích | Phản hồi xuất hiện trong Hộp xử lý kèm mô tả |

<!-- LOCAL_ASSET: ./image-34-agent-danh-gia-cau-tra-loi.png -->
![Tổng quan feedback và Hộp xử lý](minio://knowledge-base-prd/10012/9e924efb-908a-45e0-8f27-7ad48eef0bf0/a2eab4ab-b837-4f68-9ef0-c995badd4880.png)

*Ảnh 18.2 - Phần đánh giá nên vận hành như một hàng đợi điều tra, không chỉ là bảng tỷ lệ.*

## Hai bẫy lý luận về nguồn

| Bẫy | Sự thật |
|---|---|
| "Có nguồn tham khảo nên câu trả lời đúng" | Mô hình vẫn có thể tổng hợp sai hoặc chọn nhầm đoạn. Phải mở nguồn kiểm từng khẳng định. |
| "Câu trả lời đúng nên truy hồi đạt" | Mô hình có thể đã biết sẵn từ trước. Khi công việc đòi hỏi câu trả lời có căn cứ, bắt buộc kiểm nguồn. |

Có trường hợp câu hỏi không có dữ liệu trong kho nhưng vẫn hiện nguồn tham khảo, vì kho chứa một tài liệu gần chủ đề. Nguồn hiện ra **không** chứng minh nội dung bạn hỏi tồn tại.

## Thông tin request và quyền riêng tư

Bảng **Thông tin request** hiển thị các mã định danh của lượt hỏi, phương thức, đường dẫn và thời điểm gửi. Nó rất hữu ích khi cần nhờ người khác tra cứu đúng lượt hỏi.

Trước khi chia sẻ ảnh chụp bảng này, hãy che các mã định danh và đường dẫn. Không sao chép nội dung yêu cầu dạng JSON, đường dẫn nội bộ có chứa mã, khóa truy cập hay dữ liệu lưu trong trình duyệt vào tài liệu dùng chung.

<!-- LOCAL_ASSET: ./image-48-agent-lich-su-va-request-information.png -->
![Request Information đã che định danh](minio://knowledge-base-prd/10012/3b75aea4-fef9-40fc-8c5b-f2f26fa8e660/a8dd2c3e-d559-421d-b871-29b4d9544338.png)

*Ảnh 18.3 - Chỉ dùng thông tin trên giao diện để định vị lượt hỏi; các giá trị định danh đã được che trước khi chia sẻ.*

## Điều tra một phản hồi "Chưa hữu ích"

Đi theo bảy bước, theo đúng thứ tự:

1. Mở lại hội thoại, xác định người dùng đang mong đợi điều gì.
2. Mở nguồn tham khảo của câu trả lời đó.
3. Phân loại: **không có nguồn** / **nguồn sai** / **nguồn đúng nhưng câu trả lời sai**.
4. Xem lại cấu hình Agent tại thời điểm đó.
5. Sửa **đúng một lớp** thôi.
6. Chạy lại câu hỏi gốc **và** một câu diễn đạt khác cùng ý.
7. Ghi lại việc đã làm, rồi mới chuyển sang **Đã xử lý**.

Đừng đóng một phản hồi chỉ vì câu trả lời mới nghe trôi chảy hơn.

| Loại lỗi | Dấu hiệu | Ai thường xử lý | Bằng chứng để đóng |
|---|---|---|---|
| Thiếu nguồn | Không có nguồn tham khảo, hoặc báo không có dữ liệu một cách sai | Người phụ trách Agent hoặc kho tri thức | Đã kiểm phạm vi, công cụ, chỉ mục và có nguồn đúng |
| Nguồn sai | Nguồn hiện ra không chứa nội dung được dẫn | Người phụ trách kho tri thức | Chạy lại câu hỏi và ra đúng tệp, đúng đoạn |
| Tổng hợp sai | Nguồn đúng nhưng kết luận sai | Người phụ trách prompt hoặc mô hình | Câu trả lời mới đúng, nguồn vẫn đúng |
| Lỗi tệp đính kèm | Khung soạn tin, thông báo lỗi hoặc yêu cầu bất thường | Người phụ trách Agent và quản trị hệ thống | Tệp mẫu chạy được, hoặc chỉ ra rõ điểm bị chặn |
| Lỗi quyền | Không nhìn thấy Agent hoặc kho tri thức | Quản trị không gian làm việc | Vai trò và phạm vi được xác nhận theo phê duyệt |

## Nguồn hiển thị và ảnh trong câu trả lời

Với tài liệu Markdown có ảnh, có **hai** việc kiểm khác nhau, đừng gộp làm một:

1. Nguồn tham khảo mở ra đúng tệp Markdown, đúng số đoạn được trích.
2. Ảnh hiển thị thật trong câu trả lời, không phải một đường dẫn trần hay một ô trống.

Nếu câu trả lời nhắc tới ảnh mà chỉ hiện đường dẫn hoặc chỗ trống, coi như phần hiển thị chưa đạt. Ngược lại, nếu ảnh hiện đẹp nhưng nguồn Markdown sai, cũng không chấp nhận câu trả lời đó.

## Gói bằng chứng tối thiểu khi báo lỗi

Một báo cáo lỗi đủ dùng cần có: câu hỏi đã che dữ liệu nhạy cảm, thời điểm hỏi, Agent và mô hình, kho tri thức đang gắn, câu trả lời nhận được, nội dung nguồn tham khảo, trạng thái tệp liên quan, **Thông tin request** đã che định danh, và câu hỏi chạy lại sau khi sửa.

Thiếu một mục thì trạng thái vẫn là **Đang xem**, chưa phải **Đã xử lý**.

Khi phản hồi chạm tới một khẳng định nghiệp vụ, hãy hỏi người phụ trách nội dung để xác nhận đâu là nguồn chuẩn. Đừng ép mô hình trả lời theo một phản hồi đơn lẻ.

Một nguồn trước đây tìm được mà sau khi cập nhật lại không tìm ra nữa là một lỗi hồi quy cần có người chịu trách nhiệm, không chỉ là một phản hồi trên giao diện.

## Giới hạn cần nhớ

- Nguồn đúng không đồng nghĩa câu trả lời đúng. Kiểm cả hai.
- Câu trả lời đúng không đồng nghĩa truy hồi đúng. Kiểm cả hai.
- Đánh giá của người dùng là chỉ dấu, không phải chẩn đoán nguyên nhân.
- Nếu câu trả lời lộ ra ký hiệu dạng `[[chunk#...]]`, đó là lỗi định dạng, không tính là đạt. Ký hiệu đó vẫn có ích cho người kỹ thuật khi cần xác nhận đoạn nội dung có tồn tại.

## Checklist

- [ ] Đã tách rõ phiên chat mới và câu hỏi nối tiếp trong cùng hội thoại.
- [ ] Mỗi khẳng định quan trọng đều đã mở nguồn để kiểm.
- [ ] Câu hỏi không có dữ liệu và câu hỏi chạm nội dung mâu thuẫn đều có kết quả rõ ràng.
- [ ] Ảnh chụp **Thông tin request** đã che mã định danh và đường dẫn trước khi chia sẻ.
- [ ] Mỗi phản hồi đều có trạng thái, người điều tra và một lần chạy lại trước khi đóng.
