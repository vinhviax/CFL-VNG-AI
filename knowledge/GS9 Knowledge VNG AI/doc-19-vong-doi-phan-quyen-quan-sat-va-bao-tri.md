<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 19 - Agent: vòng đời, phân quyền, quan sát và bảo trì {#19-vong-doi-phan-quyen-quan-sat-va-bao-tri}

## Bạn sẽ biết gì sau khi đọc

- Các thao tác trong vòng đời một Agent và cần cẩn thận ở đâu.
- Điều phải cân nhắc trước khi chia sẻ Agent cho người khác.
- Các bước kiểm tra bắt buộc trước khi phát hành Agent cho người khác dùng.
- Lịch bảo trì và cách quay lại trạng thái cũ khi có sự cố.

## Hai vòng đời tách rời

Vòng đời một Agent gồm: tạo, cấu hình, thử, phát hành, sửa, nhân bản, tắt hoặc bật, chia sẻ và xóa.

Nội dung trong kho tri thức có vòng đời riêng. Agent vẫn tồn tại nguyên vẹn khi tài liệu bị thay. Vì vậy **quay lại cấu hình Agent cũ không thay được việc quay lại nội dung cũ**, và ngược lại.

Muốn đổi nội dung thì đi theo đường sửa nguồn, dựng lại tài liệu, nạp lại vào kho rồi chat thử. Xóa Agent không phải cách làm mới nội dung.

<!-- LOCAL_ASSET: ./image-49-agent-chia-se-va-vong-doi.png -->
![Menu vòng đời và UI chia sẻ](minio://knowledge-base-prd/10012/exports/e5c15742-730b-4e8f-9ea5-0f54001ff535.png)

*Ảnh 19.1 - Menu của Agent do bạn tạo có Trò chuyện, Chỉnh sửa, Nhân bản, Tắt hoặc Bật và Xóa; tab Chia sẻ chỉ xuất hiện khi sửa Agent.*

## Các thao tác vòng đời

| Thao tác | Điều kiện và rào chắn |
|---|---|
| Tạo Agent để thử | Đặt tên có tiền tố `TEST -`, mô tả ghi rõ sẽ xóa sau khi thử xong |
| Nhân bản | Kiểm lại cấu hình của bản sao trước khi dùng, đừng mặc định là giống hệt |
| Tắt rồi bật | Có thông báo xác nhận ở mỗi lần; kiểm trạng thái cuối cùng đúng như mong muốn |
| Chỉnh sửa | Lưu lại cấu hình gốc, mỗi lần chỉ đổi một thông số, đổi xong thì khôi phục |
| Xóa Agent thử | Chỉ làm sau khi đã lưu bằng chứng; xác nhận đúng tên và đúng người tạo |
| Chia sẻ | Chỉ gửi khi đã rõ ai nhận, quyền gì và đã có phê duyệt |
| Xóa Agent đang phục vụ người dùng | Sao lưu cấu hình, kiểm xem đang chia sẻ cho ai, và có đường quay lại trước khi làm |

Agent mặc định của hệ thống thường không hiện tùy chọn xóa. Đừng sửa Agent mặc định chỉ để thử giao diện, hãy tạo một Agent riêng.

Khi tạo Agent mới, hệ thống yêu cầu bật ít nhất một công cụ. Chọn chế độ dựng sẵn không tự bảo đảm bộ công cụ đã hợp lệ, luôn kiểm lại danh sách công cụ sau khi chọn.

## Chia sẻ và phân quyền

Tab **Chia sẻ** chỉ xuất hiện khi bạn sửa một Agent đã có, không có lúc tạo mới. Khi chia sẻ, bạn chọn không gian làm việc và một trong hai vai trò:

| Vai trò | Ý nghĩa |
|---|---|
| Chỉ xem | Người nhận dùng được Agent |
| Được chỉnh sửa | Người nhận sửa được cấu hình Agent |

> **Chia sẻ quyền `Được chỉnh sửa` nghĩa là bất kỳ ai trong nhóm nhận cũng sửa được Agent.**

Hệ quả cần lường trước:

- Prompt, mô hình, công cụ, phạm vi kho tri thức và các ngưỡng đều nằm trong tầm sửa của mọi thành viên được chia sẻ.
- Bản ghi cấu hình bạn lưu hôm nay chỉ là ảnh chụp một thời điểm. Trước khi kết luận điều gì về hành vi Agent, hãy mở lại cấu hình thật để đối chiếu.
- Kho tri thức cũng có cơ chế chia sẻ riêng. Nếu kho được chia sẻ quyền chỉnh sửa, nội dung có thể bị đổi ngoài quy trình dựng tài liệu, và tài liệu trên hệ thống có thể không còn khớp bản gốc.
- Nếu Agent có bật tải ảnh, mọi người trong nhóm được chia sẻ đều có thể đưa ảnh vào hội thoại. Xem thêm phần cảnh báo riêng tư ở mục đa phương thức.

Nguyên tắc: chỉ cấp quyền `Được chỉnh sửa` cho người thực sự phụ trách cấu hình. Với người dùng thông thường, `Chỉ xem` là đủ.

## Ai quyết định việc gì

| Vai trò | Quyết định | Không được tự ý làm |
|---|---|---|
| Người phụ trách nội dung | Nguồn chuẩn, phiên bản, xử lý mâu thuẫn nghiệp vụ | Đổi mô hình hoặc quyền để che lỗi nguồn |
| Người phụ trách Agent | Prompt, phạm vi kho tri thức, công cụ, bộ câu hỏi kiểm tra | Sửa thẳng vào tài liệu đã sinh ra thay vì sửa bản gốc |
| Quản trị không gian làm việc | Quyền truy cập, cấp phát mô hình | Mở rộng quyền chỉ để thử một lỗi |
| Người duyệt | Xem bằng chứng, nguồn, đường quay lại | Duyệt chỉ dựa trên ảnh chụp một câu trả lời |
| Người dùng Agent | Gửi phản hồi, nêu yêu cầu làm rõ | Bị mặc định coi là người chịu trách nhiệm dữ liệu trong kho |

## Trước khi phát hành cho người khác dùng

Lưu cấu hình thành công **không** đồng nghĩa Agent đã sẵn sàng phát hành. Kiểm đủ năm điểm sau:

| Điểm kiểm | Đạt khi |
|---|---|
| Có mốc phiên bản | Mỗi thay đổi quan trọng có một mốc ghi lại ngày và nội dung thay đổi |
| Có bộ câu hỏi kiểm tra | Gồm câu hỏi có đáp án chuẩn, câu chạm nội dung mâu thuẫn, câu hỏi đúng một mã cụ thể, và câu không có dữ liệu trong kho |
| Đã chat thử thật | Câu trả lời đúng, nguồn tham khảo mở ra đúng tệp, ảnh hiển thị được |
| Có người chịu trách nhiệm | Có tên cụ thể sẽ đưa Agent về trạng thái cũ khi câu trả lời hoặc nguồn bị hỏng |
| Có đường quay lại | Sao lưu cấu hình và sao lưu nội dung, để riêng hai chỗ |

Ngoài ra, khi phát hành nhớ chốt luôn: chu kỳ rà soát định kỳ và kênh để người dùng gửi phản hồi.

## Thứ tự nạp nội dung mới

Khi cập nhật nội dung cho kho tri thức mà Agent đang dùng, làm tuần tự:

1. Nạp ảnh trước, chờ tất cả ở trạng thái **Hoàn tất**.
2. Cập nhật đường dẫn ảnh trong tài liệu.
3. Dựng lại tài liệu từ bản gốc và chạy bộ kiểm tra.
4. Nạp **từng tài liệu một**, chờ trạng thái **Hoàn tất**.
5. Chat thử ngay tài liệu vừa nạp: kiểm nội dung, kiểm nguồn tham khảo, kiểm ảnh hiển thị.
6. Chỉ khi đạt mới nạp tài liệu kế tiếp.

Không nạp chồng nhiều tài liệu cùng lúc. Không xóa bản cũ trước khi bản thay thế chat thử đạt.

## Bốn xác nhận trước khi xóa

Trước khi bấm Xóa, phải đủ cả bốn:

1. Đúng **tên hiển thị**.
2. Đúng **người tạo**.
3. Đúng **mục đích** — là tài nguyên dùng để thử, không phải Agent mặc định hay Agent đang phục vụ người dùng.
4. Đã có **bản sao lưu và bằng chứng** cần giữ.

Thiếu một xác nhận thì dừng lại, đừng bấm Xóa. Hộp thoại xác nhận có ghi tên tài nguyên, hãy đọc kỹ.

Sau khi dọn dẹp, tải lại danh sách và đối chiếu số lượng cùng tên để chắc chắn không xóa nhầm và không còn sót tài nguyên thử. Nếu cần giữ lịch sử chat để làm bằng chứng, hãy lưu ảnh đã che thông tin nhạy cảm trước khi xóa, thay vì giữ Agent thử vô thời hạn.

## Bộ tình huống nên chạy thử

| Nhóm | Thử | Đạt khi | Không được làm |
|---|---|---|---|
| Tạo | Tạo Agent thử có kho tri thức và công cụ hợp lệ | Tạo được và chat được | Không dùng Agent mặc định làm đối tượng thử |
| Nhân bản | Nhân bản Agent thử | Bản sao xuất hiện với cấu hình mong đợi | Không nhân bản Agent đang phục vụ người dùng |
| Tắt / Bật | Tắt rồi bật bản sao | Có thông báo ở cả hai lần, trạng thái cuối đúng | Không tắt Agent đang có người dùng |
| Chia sẻ | Mở tab Chia sẻ xem các vai trò | Thấy không gian làm việc và hai vai trò | Không gửi chia sẻ khi chưa được phê duyệt |
| Xóa | Xóa đúng Agent thử sau khi đã lưu bằng chứng | Tài nguyên biến mất, bằng chứng còn | Không xóa khi tên hoặc người tạo còn mơ hồ |
| Bảo trì | Chạy lại bộ câu hỏi sau khi cập nhật kho | Mỗi tài liệu mới có nguồn và ảnh | Không gộp đổi nội dung với nhiều thay đổi cấu hình |

## Lịch bảo trì

| Chu kỳ | Việc làm | Kết quả tối thiểu |
|---|---|---|
| Sau khi đổi nội dung kho tri thức | Chạy câu hỏi chuẩn, câu mâu thuẫn, câu không có dữ liệu; mở nguồn và ảnh | Ghi lại ngày và kết quả đạt hoặc không đạt của từng nguồn |
| Sau khi đổi mô hình, prompt hoặc công cụ | Đổi **một** thông số rồi so sánh; không đạt thì khôi phục | Ghi lại thông số đã đổi và kết quả chạy lại |
| Hàng tuần | Xem phản hồi chưa xử lý, theo dõi lỗi và hạn mức | Mỗi mục có người phụ trách và trạng thái trong Hộp xử lý |
| Hàng tháng | Rà soát quyền chia sẻ, Agent đang tắt, Agent thử còn tồn | Danh sách giữ hoặc xóa, có người duyệt |
| Trước khi xóa hoặc ngừng dùng | Sao lưu cấu hình và bằng chứng, xác nhận đúng đối tượng | Kế hoạch quay lại và người duyệt |

Nếu Agent được chia sẻ quyền chỉnh sửa cho nhiều người, thêm một việc nữa: **rà soát xem cấu hình có bị lệch không** — mở lại từng Agent và so với bản ghi — trước mỗi lần kết luận về hành vi của nó.

Reranker nên được coi là thành phần phụ thuộc, không phải tùy chọn. Khi nó không dùng được, hãy chạy lại phần truy hồi trước khi tin rằng câu trả lời cũ vẫn còn đúng.

## Quay lại trạng thái cũ

| Loại | Cách làm | Không được làm |
|---|---|---|
| Cấu hình Agent | Khôi phục từ bản ghi cấu hình đã lưu | Không dùng Xóa Agent để "làm mới" |
| Nội dung kho tri thức | Sửa bản gốc, dựng lại, nạp lại, chat thử lại | Không xóa tài liệu để coi như đã quay lại |
| Ảnh | Đối chiếu với bảng ánh xạ ảnh đã lưu | Không thay đường dẫn bằng địa chỉ tự đoán |
| Khi nạp lỗi giữa chừng | Giữ nguyên tài liệu đã hoàn tất, ghi lại lỗi, không đụng bản cũ | Không nạp tiếp tài liệu kế khi chưa xử lý xong |

Sao lưu nguyên vẹn bản cũ trước khi thay thế là việc bắt buộc, không phải tùy chọn.

## Cạm bẫy thường gặp

| Cạm bẫy | Cách nhận biết và xử lý |
|---|---|
| Danh sách Agent hiển thị tên cũ | Tên trên danh sách khác tên trong hộp thoại. Mở hộp thoại ra mới thấy tên thật |
| Danh sách tự sắp lại sau mỗi lần lưu | Agent vừa sửa nhảy lên đầu nhóm. Nhìn lại danh sách trước mỗi lần bấm |
| Bấm nhầm Agent | Luôn xác minh tên trong hộp thoại trước khi thao tác. Nếu mở nhầm thì bấm Hủy, đừng sửa gì |
| Xóa nhầm Agent | Đủ bốn xác nhận. Còn mơ hồ thì dừng |
| Cấu hình bị lệch dần | Lưu bản gốc, có bộ câu hỏi kiểm tra, mỗi lần chỉ đổi một thông số |
| Gộp nhiều thay đổi | Không đổi nội dung và đổi cấu hình trong cùng một lần |
| Chia sẻ sai phạm vi | Xem giao diện trước; chỉ gửi khi rõ người nhận và vai trò |
| Quan sát thiếu bối cảnh | Lưu kèm nguồn, mô hình, kho tri thức đang gắn và thông tin lượt hỏi đã che định danh |

## Checklist

- [ ] Agent mặc định và Agent đang phục vụ người dùng không bị dùng làm đối tượng thử.
- [ ] Nhân bản, tắt bật và xóa chỉ làm trên tài nguyên thử đã xác định chính xác.
- [ ] Chỉ chia sẻ khi đã rõ người nhận, vai trò và có phê duyệt.
- [ ] Đã có người chịu trách nhiệm, bộ câu hỏi kiểm tra, lịch rà soát và đường quay lại.
- [ ] Bằng chứng được lưu trước khi dọn dẹp tài nguyên thử.
