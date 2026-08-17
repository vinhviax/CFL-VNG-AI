# 20 - Thiết kế danh mục kho {#20-thiet-ke-danh-muc-kho}

## Bạn sẽ biết gì sau khi đọc

- Một nhóm mới bắt đầu thì nên dựng những kho nào, theo thứ tự nào.
- Khi phân vân hai nội dung nên nằm chung hay tách ra, dựa vào đâu để quyết.
- Cách chia kho nào hay hỏng, và chia thế nào thì bền.

## Nguyên tắc phải thống nhất trước

Quyền xem nằm ở **cấp kho**, không nằm ở từng tài liệu. Trợ lý cũng gắn **cả kho**, không gắn được một phần kho.

Hệ quả: **một tài liệu nhạy cảm kéo cả kho lên mức nhạy cảm đó.** Mọi cách chia kho đều phải sống được với ràng buộc này. Nếu bạn định để một bảng dữ liệu người chơi chung với hướng dẫn vận hành, thì toàn bộ hướng dẫn vận hành cũng chỉ chia sẻ được cho nhóm được xem dữ liệu người chơi.

![Tab Chia sẻ với lựa chọn Space và quyền Chỉnh sửa hoặc Chỉ đọc](<knowledge/GS9 Knowledge VNG AI/image-06-chia-se-va-phan-quyen.png>)

*Ảnh 20.1 - Quyền được đặt cho cả kho, không đặt được cho từng tài liệu bên trong. Đây là ràng buộc chi phối mọi quyết định tách hay gộp kho.*

## Bốn loại kho hầu như nhóm nào cũng cần

Xếp theo thứ tự nên làm. Làm xong loại 1 rồi hãy tính loại 2.

| Loại kho | Chứa gì | Dấu hiệu bạn đang cần nó |
|---|---|---|
| **1. Kho sự thật đã chốt** | Thuật ngữ chính thức, tên hệ thống, danh mục vật phẩm, định nghĩa chỉ số | Hai người gọi cùng một thứ bằng hai cái tên khác nhau |
| **2. Kho quy trình và chính sách** | Quy trình vận hành, điều khoản xử phạt, chính sách hỗ trợ người dùng | Cùng một tình huống, mỗi người xử một kiểu |
| **3. Kho kế hoạch và lịch** | Nội dung phiên bản, lịch sự kiện, brief đã duyệt | Phải đi hỏi từng người mới biết tháng sau chạy gì |
| **4. Kho kết quả** | Báo cáo theo kỳ, số liệu vận hành, phản hồi người dùng | Muốn biết lần trước làm thế nào thì phải lục chat cũ |

Loại 1 đứng đầu vì các loại sau đều tham chiếu tới nó. Nếu thuật ngữ chưa thống nhất, kho quy trình viết ra sẽ mỗi chỗ gọi một tên và trợ lý không nối được hai tài liệu với nhau.

## Ba câu hỏi để quyết định tách hay gộp

Khi phân vân hai nội dung nên nằm chung một kho hay tách ra hai kho, hỏi lần lượt:

1. **Ai được xem?** Khác người xem thì phải tách — vì quyền nằm ở cấp kho.
2. **Bao lâu đổi một lần?** Thứ đổi hàng tháng để chung với thứ đổi hàng năm sẽ khiến kho luôn ở trạng thái nửa cũ nửa mới, và người đọc không biết phần nào còn dùng được.
3. **Đã chốt hay chưa chốt?** Kế hoạch chưa duyệt không để chung với thứ đã công bố, tránh trợ lý trộn hai loại vào cùng một câu trả lời.

Cả ba câu đều trả lời "giống nhau" thì để chung một kho. **Chỉ cần một câu khác là nên tách.**

## Lỗi hay gặp: chia kho theo nguồn dữ liệu

Rất dễ bị cám dỗ chia kho theo nơi dữ liệu đến từ đâu — kho Drive, kho Excel, kho báo cáo. Cách đó bắt người dùng phải biết trước tài liệu nằm ở đâu mới tìm được, trong khi họ chỉ có câu hỏi trong đầu chứ không biết tệp nằm chỗ nào.

**Chia theo câu hỏi người ta sẽ hỏi, không chia theo chỗ tệp đang nằm.**

Cách kiểm nhanh: viết ra năm câu hỏi thật mà người dùng sẽ gõ vào ô chat. Nếu mỗi câu đều rơi gọn vào đúng một kho, cách chia đang ổn. Nếu một câu phải tra ba kho mới đủ, gộp lại. Nếu một kho phải trả lời năm câu chẳng liên quan gì nhau, tách ra.

## Vài lưu ý khi đặt tên kho

- Đặt tên theo **nội dung bên trong**, không theo phòng ban sở hữu — phòng ban đổi tên thì kho không phải đổi theo.
- Tên nên trả lời được câu "tra cái gì ở đây", ví dụ *Chính sách hỗ trợ người chơi* rõ hơn *Tài liệu nhóm CS*.
- Tránh đưa số phiên bản hay năm vào tên kho, trừ khi bạn thực sự giữ song song nhiều phiên bản cùng lúc.

## Khi nào rà lại danh mục kho

Rà khi có một trong các dấu hiệu sau, không cần chờ tới kỳ:

- Một kho phình lên tới mức người dùng phải đọc mục lục mới biết có gì trong đó.
- Có tài liệu bạn muốn chia sẻ cho nhóm khác nhưng vướng vì nó nằm chung kho với thứ nhạy cảm.
- Trợ lý bắt đầu trả lời trộn giữa nội dung đã chốt và nội dung còn nháp.
