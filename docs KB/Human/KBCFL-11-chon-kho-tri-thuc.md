# Chọn kho tri thức theo câu hỏi

Đọc xong phần này bạn biết câu hỏi của mình nên tra ở kho nào, kho nào là nguồn chuẩn khi hai nơi lệch nhau, và những kiểu chọn nhầm hay gặp.

## Bước 1 — xác định câu hỏi thuộc loại nào

Hỏi mình một câu duy nhất: *"tôi đang hỏi về tương lai, hiện tại hay quá khứ?"*

| Câu hỏi hướng về | Ví dụ | Kho nên tra |
|---|---|---|
| Tương lai — sắp phát hành | Phiên bản tới có hệ thống gì, vật phẩm nào, dự kiến khi nào | `GS9 CFL Plan Version` |
| Quá khứ — kết quả theo tháng | Tháng trước doanh thu, chi phí, hiệu quả chiến dịch ra sao | `GS9 CFL PUM` |
| Quá khứ — biến động theo ngày | Ngày nào tụt, tụt bao nhiêu, kéo dài mấy ngày | `GS9 CFL Data Daily` |
| Toàn cảnh — nhìn nhiều nguồn cùng lúc | Bức tranh chung của cả giai đoạn, các chủ đề liên quan nhau | `GS9 CFL Kho Dữ Liệu Tổng Hợp` |
| Người chơi đang nghĩ gì | Chủ đề nào bị than phiền nhiều, cảm xúc chung ra sao | `GS9 CFL Sentiment Feedback User` |
| Gọi tên cho đúng | Hệ thống này tên chính thức là gì, vật phẩm này viết thế nào | `GS9 CFL Glossary & Systems` (bản nháp) |
| Chính sách trả lời người chơi | Trường hợp này CS trả lời ra sao, chính sách nào áp dụng | `GS9 CFL CS FAQ & Policy` (bản nháp) |
| Danh mục vật phẩm, ItemID | Vật phẩm này ID bao nhiêu, thuộc nhóm nào | `GS9 CFL Item Profile` — **kho cách ly, xem mục cảnh báo** |
| Cách dùng trợ lý và kho tri thức | Chọn trợ lý nào, kho nào, quy ước ra sao | `GS9 CFL Knowledge Agent` |

## Bước 2 — kiểm tra ba điều trước khi tin kết quả

1. **Kho này là nguồn chuẩn hay bản dẫn xuất?** `Kho Dữ Liệu Tổng Hợp` là bản dẫn xuất. Mọi kho còn lại là nguồn chuẩn cho phần nội dung của mình.
2. **Kho này đã hoàn chỉnh chưa?** `Glossary & Systems` và `CS FAQ & Policy` đang là bản nháp. Kết quả từ hai kho này là gợi ý, không phải căn cứ.
3. **Câu trả lời có dẫn nguồn không?** Luôn mở tài liệu được trích để kiểm lại con số và câu chữ quan trọng. Không có nguồn thì không dùng.

## Bước 3 — khi hai kho trả lời khác nhau

Chuyện này xảy ra thật, thường xuyên nhất là giữa `Kho Dữ Liệu Tổng Hợp` và các kho số liệu riêng lẻ.

**Quy tắc: lấy kho gốc làm chuẩn.**

| Tình huống | Xử lý |
|---|---|
| `Kho Dữ Liệu Tổng Hợp` lệch với `Data Daily` hoặc `PUM` | Tin kho lẻ. Báo chủ sở hữu kho tổng hợp để gom lại |
| Hai phiên bản trong `Plan Version` nói khác nhau | Không phải mâu thuẫn — chúng nói về hai phiên bản khác nhau. Xác định đúng phiên bản trước |
| Kho nháp nói khác tài liệu chính thức của team | Tin tài liệu chính thức. Báo để cập nhật kho nháp |
| Số trong kho khác số trong dashboard bạn quen dùng | Dừng lại, đừng chọn bên nào. Hỏi chủ sở hữu số liệu |

Lý do kho tổng hợp hay lệch: nó được gom lại theo từng đợt. Kho lẻ cập nhật xong mà kho tổng chưa gom lại thì kho tổng đang mô tả trạng thái cũ — và nó **không báo cho bạn biết điều đó**.

## Sáu cách chọn nhầm hay gặp

- **Hỏi kế hoạch tương lai trong kho báo cáo tháng.** `PUM` nhìn về quá khứ. Nó không biết phiên bản tới có gì.
- **Lấy số cuối cùng từ kho tổng hợp.** Kho tổng hợp để nhìn toàn cảnh. Con số đưa vào báo cáo phải lấy từ kho gốc.
- **Cộng kết quả của kho tổng hợp với kho lẻ.** Hai bên chồng nội dung nhau, cộng vào là đếm hai lần.
- **Coi bản nháp là chính sách.** `CS FAQ & Policy` và `Glossary & Systems` chưa được duyệt. Trả lời người chơi bằng nội dung nháp là rủi ro thật.
- **Trích nguyên văn kế hoạch phiên bản ra ngoài.** `Plan Version` là tài liệu nội bộ và là kế hoạch chưa chốt. Một hạng mục nằm trong đó không có nghĩa nó sẽ lên sóng.
- **Mở kho cách ly ra để lấy vài dòng cho nhanh.** `Item Profile` chứa dữ liệu cấp người chơi. Không có ngoại lệ "chỉ lấy một chút".

## Cảnh báo riêng cho hai kho nhạy cảm

### `GS9 CFL Item Profile`

Kho này trộn danh mục vật phẩm với dữ liệu cấp người chơi trong cùng một chỗ, nên toàn bộ kho bị coi là nhạy cảm.

- Không gắn kho này vào bất kỳ trợ lý nào.
- Không sao chép dữ liệu định danh người chơi sang tài liệu, bảng tính, slide hay tin nhắn.
- Cần danh mục vật phẩm: đề nghị chủ sở hữu kho tách phần danh mục ra kho riêng. Đó là cách duy nhất đúng.

### `GS9 CFL Sentiment Feedback User`

Phản hồi người chơi là văn bản tự do, có thể lẫn thông tin cá nhân.

- Chỉ tổng hợp theo chủ đề và sắc thái cảm xúc.
- Không trích nguyên văn bình luận, không kèm tên hay thông tin nhận dạng.
- Không đưa nội dung thô ra ngoài phạm vi người đã có quyền vào kho.

## Khi không kho nào trả lời được

Đừng mở rộng phạm vi tra cứu ra tất cả kho để mò cho ra. Làm vậy chỉ đổi một câu trả lời "không biết" thành một câu trả lời sai mà nghe có vẻ đúng.

Thay vào đó, ghi lại: câu hỏi cụ thể, loại tài liệu bạn nghĩ sẽ trả lời được, ai đang giữ tài liệu đó. Trình chủ sở hữu kho để bổ sung nguồn.

Có những mảng hiện chưa có kho nào phụ trách — lịch sự kiện đã duyệt, quy trình xử lý sự cố, chính sách xử phạt của GM. Câu hỏi thuộc các mảng này phải đi theo quy trình hiện hành của team, không tra kho.

## Đọc tiếp

- **Các kho tri thức của GS9 CFL** — mỗi kho chứa gì, ai phụ trách.
- **Quy ước và ranh giới dữ liệu** — thêm nội dung mới thì đặt tên và giới hạn thế nào.
- **Chọn trợ lý nhanh theo công việc** — chọn kho xong thì chọn trợ lý.
