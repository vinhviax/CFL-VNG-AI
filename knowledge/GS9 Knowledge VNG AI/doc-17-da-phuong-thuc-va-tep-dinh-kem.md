<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 17 - Agent: đa phương thức và tệp đính kèm {#17-da-phuong-thuc-va-tep-dinh-kem}

## Bạn sẽ biết gì sau khi đọc

- Phân biệt tài liệu nạp vào kho tri thức với tệp đính kèm gửi trong chat.
- Các control cần bật và cần kiểm tra khi muốn Agent đọc ảnh, âm thanh hoặc tài liệu.
- Việc cần cân nhắc về quyền riêng tư trước khi cho phép tải ảnh.
- Cách đọc lỗi khi tệp không được nhận.

## Hai đường xử lý tệp

Agent nhận tệp theo hai đường khác nhau. Đường này chạy được không có nghĩa đường kia cũng chạy.

| | Tài liệu trong kho tri thức | Tệp đính kèm trong chat |
|---|---|---|
| Vòng đời | Dùng lâu dài, tái sử dụng ở mọi lượt hỏi | Đi cùng đúng **một** câu hỏi |
| Cách xử lý | Phân tích file, chia đoạn, lập chỉ mục, rồi được công cụ truy hồi | Kiểm tra định dạng khi tải lên, rồi đưa thẳng vào phiên chat |
| Điều kiện | Tài liệu phải ở trạng thái **Hoàn tất** | Client chấp nhận định dạng và mô hình tương ứng phải có sẵn |
| Dấu hiệu thành công | Có nguồn tham khảo trong câu trả lời | Tên tệp và kích thước hiện ở khung soạn tin |

Hai đường chỉ gặp nhau ở bước mô hình trả lời. Trước đó chúng khác nhau về kiểm tra định dạng, quyền, mô hình và thời điểm xử lý.

Hai suy luận thường sai:

- PDF trong kho tri thức đọc được, nên PDF đính kèm chắc chắn cũng đọc được.
- Khung soạn tin đã hiện ảnh, nên mô hình đã nhận được ảnh.

<!-- LOCAL_ASSET: ./image-32-agent-cau-hinh-da-phuong-thuc.png -->
![Tab cấu hình đa phương thức](minio://knowledge-base-prd/10012/524d81d7-99fd-4f9e-a271-6ab3b0695619/e8883a27-0679-4170-9062-1986c8b9ef63.png)

*Ảnh 17.1 - Control tải ảnh, VLM và âm thanh cần cấu hình riêng, tách khỏi phần truy hồi tài liệu.*

## Từng loại tệp đi đường nào

| Loại tệp | Đường đi | Điều cần lưu ý |
|---|---|---|
| Markdown | Nạp vào kho tri thức, chia đoạn, truy hồi | Cách dùng ổn định nhất cho nội dung dài |
| PDF | Nạp vào kho tri thức hoặc đính kèm trong chat | Dùng được cả hai đường |
| CSV | Nạp vào kho tri thức để truy hồi hoặc phân tích dữ liệu | Đọc qua truy hồi là một chuyện; công cụ phân tích dữ liệu là chuyện khác, cần kiểm riêng |
| Ảnh | Đính kèm trong chat, cần mô hình VLM hoặc Intent phân tích ảnh | Nếu client báo định dạng không hỗ trợ thì lỗi nằm ở bước tải lên, chưa chạm tới mô hình |
| Âm thanh | Đính kèm trong chat, cần mô hình ASR chuyển thành văn bản | Nếu danh sách mô hình ASR trống thì tính năng chưa sẵn sàng, hãy liên hệ quản trị |

Danh sách định dạng mà giao diện liệt kê **không** bảo đảm mọi loại đều xử lý được. Khả năng thật còn phụ thuộc mô hình đang bật.

## Các control cần kiểm tra

| Control | Câu hỏi phải trả lời | Đừng kết luận chỉ vì nhìn giao diện |
|---|---|---|
| Tải ảnh | Đã có mô hình VLM tương thích chưa? Client có nhận tệp không? | Bật công tắc không có nghĩa mô hình đọc được ảnh |
| Intent phân tích ảnh | Prompt cho nhánh này có hợp lý không? | Ảnh hiện ở khung soạn tin không có nghĩa đã gửi đi được |
| Tải âm thanh | Có mô hình ASR và đúng ngôn ngữ không? | Bật công tắc không có nghĩa audio đã được chuyển thành văn bản |
| Intent tóm tắt / phân tích tài liệu | Câu trả lời đang dựa vào tệp đính kèm hay vào nguồn trong kho? | Trả lời trôi chảy không có nghĩa mô hình bám đúng tệp |

## Cảnh báo riêng tư khi bật tải ảnh

> **Bật `Tải ảnh` mở thêm một đường đưa thông tin cá nhân vào hội thoại.**

Ảnh người dùng gửi vào chat thường chứa nhiều dữ liệu hơn họ nghĩ: ảnh chụp màn hình phiếu hỗ trợ, ảnh hồ sơ tài khoản, ảnh giao dịch, ảnh đoạn chat đều có thể lộ họ tên, ID, số điện thoại, email hoặc thông tin thanh toán.

Khác với tài liệu nạp vào kho tri thức, ảnh đính kèm đi thẳng qua phiên chat và không qua bước duyệt nội dung nào.

Việc nên làm trước khi bật control này cho một nhóm người dùng:

- Nói rõ với người dùng: không đính kèm ảnh chứa thông tin định danh của người khác.
- Nếu công việc bắt buộc phải gửi, che phần định danh trước khi tải lên.
- Hỏi quản trị hệ thống xem ảnh đính kèm được lưu ở đâu và giữ trong bao lâu, trước khi mở rộng cho nhiều người.
- Nhớ rằng ai có quyền chat với Agent thì cũng có bề mặt này.

## Các bước làm

1. Xác định tệp sẽ dùng làm nguồn lâu dài hay chỉ là ngữ cảnh một lượt. Hai đường không thay thế nhau.
2. Với tệp nạp vào kho tri thức, chờ trạng thái **Hoàn tất** rồi mới hỏi. Đừng chat khi tệp còn đang xử lý.
3. Với tệp đính kèm, dùng một tệp PDF, CSV hoặc Markdown không nhạy cảm và hỏi những dữ kiện bạn đã biết trước câu trả lời đúng.
4. Với ảnh, chọn tệp an toàn. Kiểm tra ba mốc theo thứ tự: giao diện nhận tệp, mô hình VLM hoặc Intent được gọi, câu trả lời mô tả đúng ảnh.
5. Với âm thanh, nếu danh sách mô hình ASR báo không có model thì dừng lại và báo quản trị. Đừng tự đưa mô hình hay khóa riêng vào không gian làm việc.
6. Xóa tệp đính kèm và hội thoại thử nếu chính sách lưu trữ của tổ chức yêu cầu.

<!-- LOCAL_ASSET: ./image-45-agent-tep-dinh-kem.png -->
![PDF nằm trong composer trước khi gửi](minio://knowledge-base-prd/10012/c719a1b8-ef9d-4ca1-b370-fcc4c6cec1af/04e9f2fa-6231-4925-953d-2d1fa6ab3635.png)

*Ảnh 17.2 - Khung soạn tin xác nhận PDF đã được đính kèm và hiển thị kích thước trước khi gửi.*

## Bốn câu hỏi trước mỗi lần tải tệp

| Câu hỏi | Lý do |
|---|---|
| Đây là nguồn lâu dài hay ngữ cảnh một lượt? | Chọn đúng đường: kho tri thức hay đính kèm |
| Tệp có thông tin cá nhân, khóa hay mật khẩu không? | Ngăn rò rỉ qua hội thoại |
| Có dữ kiện đã biết trước để chấm câu trả lời không? | Phân biệt lỗi đọc tệp với lỗi tổng hợp của mô hình |
| Mô hình đang dùng có hỗ trợ ảnh hoặc âm thanh không? | Tránh kết luận sai khi control để trống |

Không dùng để thử nghiệm: hợp đồng, thông tin cá nhân, khóa truy cập, log nội bộ, tệp chưa rõ chính sách lưu trữ. Hãy dựng tệp mẫu tự tạo, có sẵn vài dữ kiện rõ ràng như mã số, người phụ trách, thời hạn xử lý.

Khi thử tệp đính kèm, kiểm ba điểm:

1. Tên tệp và kích thước **hiện ở khung soạn tin**.
2. Câu trả lời nêu đúng nội dung **của tệp vừa gửi**, không phải nguồn khác trong kho.
3. Câu trả lời không chỉ lặp lại dữ liệu đã có sẵn trong kho tri thức.

## Bộ tình huống nên chạy thử

| Tình huống | Đầu vào | Cần kiểm | Đạt khi |
|---|---|---|---|
| Nguồn Markdown | Một tài liệu chuẩn trong kho | Hỏi người phụ trách và thời hạn xử lý | Trả đúng và có nguồn tham khảo |
| Nguồn PDF | Cùng nội dung, nạp vào kho | Hỏi lại câu trên | Truy hồi ra cùng dữ liệu |
| Nguồn CSV | Bảng có hai bản ghi khác nhau | So sánh hai bản ghi | Nêu được bản chuẩn và bản mâu thuẫn |
| PDF đính kèm | Cùng tệp PDF, gửi trong khung soạn tin | Hỏi mã số, người phụ trách, thời hạn | Trả đúng cả ba trường |
| Ảnh đính kèm | Một ảnh an toàn | Yêu cầu mô tả nội dung ảnh | Mô tả đúng; nếu bị chặn thì ghi lại thông báo lỗi |
| Âm thanh đính kèm | Chỉ thử khi đã có mô hình ASR | Yêu cầu nội dung đoạn ghi âm | Chỉ tính đạt khi có văn bản chuyển đổi |

<!-- LOCAL_ASSET: ./image-46-agent-image-analysis.png -->
![Ảnh đính kèm bị từ chối ở client](minio://knowledge-base-prd/10012/9ef8e837-9f5f-49a1-84ab-12f7b7093641/336c0344-6101-4acd-9fb8-fb697ea07149.png)

*Ảnh 17.3 - Thông báo "Định dạng tệp không hỗ trợ" xuất hiện ngay ở bước tải lên; đừng dùng nó để kết luận mô hình VLM hỏng.*

<!-- LOCAL_ASSET: ./image-47-agent-document-summarize.png -->
![Document Analysis PDF trả về fact mong đợi](minio://knowledge-base-prd/10012/fb975571-2e8b-4bdc-b3d4-c73d425f7ec0/12f6710d-1dae-448c-8a38-9eef4db06f02.png)

*Ảnh 17.4 - Agent phân tích tệp PDF đính kèm và nêu đúng mã, người phụ trách, thời hạn, mức ưu tiên.*

## Tóm tắt và phân tích tài liệu

Hai Intent **Summarize Response** và **Document Analysis Response** giúp trình bày gọn, nhưng không thay bạn kiểm chứng nguồn.

- Một bản tóm tắt tốt phải giữ rõ phạm vi, nêu chỗ chưa chắc chắn và chỗ mâu thuẫn.
- Một bản phân tích tốt phải chỉ ra đang nói về tệp nào, đoạn nào.
- Khi đính kèm PDF, hãy hỏi những trường có đáp án rõ như mã số, người phụ trách, thời hạn. Dễ chấm đúng sai.
- Khi chỉ yêu cầu "tóm tắt", hãy thêm ràng buộc: bao nhiêu ý, ngôn ngữ nào, và không được thêm thông tin ngoài tệp.

## Khi tệp không chạy

| Hiện tượng | Kiểm lớp này trước | Việc nên làm |
|---|---|---|
| Tệp không hiện ở khung soạn tin | Bước kiểm tra định dạng khi tải lên | Ghi lại định dạng, kích thước, mô hình đang dùng |
| Tệp hiện nhưng Agent nói không thấy | Bước truyền tệp vào yêu cầu, hoặc Intent | Mở **Thông tin request** để lưu lại, rồi thử một tệp mẫu khác |
| PDF trong kho đọc được nhưng đính kèm thì lỗi | Hai đường xử lý khác nhau | Đừng vội sửa cấu hình phân tích tệp của kho tri thức |
| Không chọn được mô hình ASR | Cấp phát mô hình cho tổ chức | Ghi nhận là đang bị chặn và liên hệ quản trị theo kênh chuẩn |
| CSV trả lời sai | Dữ liệu, truy hồi hoặc prompt | Kiểm bản ghi và công cụ trước khi kết luận mô hình sai |

## Checklist

- [ ] Đã phân biệt rõ nguồn lâu dài trong kho với tệp đính kèm một lượt.
- [ ] Tệp thử nghiệm không nhạy cảm và có dữ kiện để chấm.
- [ ] Tệp trong kho đã ở trạng thái **Hoàn tất** trước khi chat.
- [ ] Ảnh và âm thanh chỉ được coi là chạy được khi có câu trả lời thật, không phải khi công tắc đã bật.
- [ ] Người dùng đã được nhắc về rủi ro gửi ảnh chứa thông tin cá nhân.
