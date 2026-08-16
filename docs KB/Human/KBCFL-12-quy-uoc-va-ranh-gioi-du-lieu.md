# Quy ước đặt tên và ranh giới dữ liệu

Đọc xong phần này bạn biết: thêm tài liệu vào kho thì đặt tên thế nào, nội dung nào được phép nằm ở kho nào, và cần kiểm gì trước khi bấm nạp.

## 1. Quy ước đặt tên tài liệu

Mọi tài liệu đưa vào kho tri thức của GS9 CFL đều mang tiền tố cố định.

| Loại | Tiền tố | Ví dụ |
|---|---|---|
| Tài liệu (văn bản, bảng tính, PDF…) | `doc-` | `doc-00-huong-dan-va-quy-uoc.md` |
| Ảnh | `image-` | `image-01-tong-quan-danh-sach.png` |
| Kho chứa nhiều phiên bản | chèn số hiệu phiên bản **ngay sau** tiền tố | `doc-v5-00-index-va-pham-vi.md`, `image-v5-01-so-do.jpg` |

Ba chi tiết nhỏ nhưng làm hỏng việc nếu sai:

- Dấu phân cách là **gạch ngang** `-`, không phải gạch dưới `_`. `doc_01_...` là sai.
- Số hiệu phiên bản đứng **sau** tiền tố loại: `doc-v5-00-...`, không phải `v5-doc-00-...` hay `V5-00-...`.
- Tên viết thường, không dấu, các từ nối bằng gạch ngang.

### Vì sao phải đúng tiền tố

Không phải để cho đẹp. Bộ lọc đồng bộ giữa thư mục nguồn và kho tri thức **khoá vào đúng hai tiền tố này**. File nào không bắt đầu bằng `doc-` hoặc `image-` thì bộ lọc bỏ qua.

Hai hệ quả trực tiếp:

- **Đặt sai tiền tố → tài liệu không lên kho.** Không có thông báo lỗi. Bạn tưởng đã nạp xong, thực tế kho không có gì. Đây là kiểu sai âm thầm, thường chỉ lộ ra khi ai đó hỏi và trợ lý trả lời "không tìm thấy".
- **Đặt đúng tiền tố → những file rác tự động bị loại.** File cấu hình, file tạm, file lạc trong thư mục sẽ không lọt vào kho.

### Vì sao kho nhiều phiên bản bắt buộc có số hiệu

`GS9 CFL Plan Version` chứa mọi phiên bản trong cùng một kho. Tài liệu của các phiên bản được sinh ra theo cùng một khuôn, nên nếu không chèn số hiệu, phiên bản mới sẽ ra **đúng tên file** của phiên bản cũ.

Khi đó hai chuyện xảy ra cùng lúc: hai tài liệu cùng tên khác nội dung nằm chung một kho, và trợ lý trộn nội dung hai phiên bản vào một câu trả lời — **không có dấu hiệu nào cho thấy nó đang nhầm**.

Vì vậy: tài liệu nào vào `Plan Version` cũng phải mang số hiệu phiên bản trong tên, và nên ghi rõ phiên bản ngay trong phần mở đầu nội dung.

### Ngoại lệ

Tài liệu đồng bộ trực tiếp từ Google Drive giữ nguyên tên người dùng đã đặt. Đừng đổi tên loại này nếu bạn không phải chủ sở hữu kho — đổi tên ở thư mục nguồn sẽ kéo theo thay đổi trên kho.

## 2. Ranh giới dữ liệu nhạy cảm

### Nguyên tắc gốc: mức nhạy cảm của kho bằng mức của tài liệu nhạy cảm nhất trong đó

Quyền chia sẻ nằm ở cấp kho, không ở cấp tài liệu. Một file chứa dữ liệu định danh người chơi sẽ kéo toàn bộ kho xuống mức cao nhất, kể cả khi 9 file còn lại hoàn toàn vô hại.

`GS9 CFL Item Profile` là ví dụ sống: phần danh mục vật phẩm hoàn toàn dùng được, nhưng vì nằm chung kho với dữ liệu cấp người chơi nên **cả kho bị cách ly**.

Suy ra một luật đơn giản khi thêm nội dung: **đừng bao giờ bỏ một file nhạy cảm vào kho đang mở rộng**. Tách kho, đừng trộn.

### Bốn mức nội dung và nơi được để

| Mức | Loại nội dung | Được để ở đâu | Được gắn vào trợ lý? |
|---|---|---|---|
| Định danh người chơi | Tài khoản, nhân vật, nickname, lịch sử nạp | Chỉ kho cách ly | **Không bao giờ** |
| Nội bộ mật | Kế hoạch chưa công bố, doanh thu, ngân sách | Kho nội bộ, chia sẻ hẹp | Chỉ trợ lý hướng nội bộ |
| Nội bộ thường | Chỉ số tổng hợp, phản hồi đã ẩn danh | Kho nội bộ | Có điều kiện |
| Nội bộ phổ biến | Thuật ngữ, tài liệu hướng dẫn, chính sách đã phát hành | Kho dùng chung | Được |

### Các đường ranh không được bước qua

- **Không sao chép dữ liệu định danh người chơi ra ngoài kho cách ly.** Kể cả một vài dòng, kể cả để dán tạm vào bảng tính cá nhân.
- **Không gắn kho chứa dữ liệu định danh vào trợ lý.** Trợ lý gắn cả kho, không gắn được một phần, và thông tin nhạy cảm sẽ xuất hiện trong phần dẫn nguồn của câu trả lời.
- **Không trích nguyên văn phản hồi người chơi.** Chỉ tổng hợp theo chủ đề và sắc thái. Văn bản tự do có thể chứa tên, số điện thoại, mã đơn hàng.
- **Không để số liệu doanh thu lọt vào nội dung gửi người chơi.** Cả team được đọc doanh thu, nhưng đọc được không có nghĩa là phát ra được.
- **Không trích nguyên văn kế hoạch phiên bản vào thông báo ra ngoài.** Đó là tài liệu nội bộ và là kế hoạch chưa chốt.
- **Không mở rộng phạm vi của một trợ lý ra tất cả kho** để nó "tra được nhiều hơn". Cách đó vô hiệu hoá mọi ranh giới ở trên cùng một lúc.

### Chia sẻ kho là một quyết định, không phải thao tác

Khi một kho được chia sẻ vào không gian làm việc, nó đồng thời mở thêm một đường truy cập ngoài trợ lý. Nghĩa là phạm vi thật của kho rộng hơn danh sách trợ lý đang gắn nó.

Trước khi chia sẻ, hỏi: *nếu toàn bộ nội dung kho này lọt ra ngoài danh sách người hiện tại, có vấn đề gì không?* Nếu câu trả lời không phải là "không", hãy dừng lại và hỏi chủ sở hữu kho.

## 3. Nguyên tắc khi thêm nội dung mới

Trước khi nạp một tài liệu vào kho, đi qua bảy câu này.

| # | Câu hỏi | Không đạt thì làm gì |
|---|---|---|
| 1 | Tài liệu này thuộc kho nào, và **chỉ một** kho? | Chọn một kho làm nguồn chuẩn. Bản sao ở nơi khác phải ghi rõ là bản dẫn xuất |
| 2 | Tên file đã đúng tiền tố `doc-` / `image-` chưa? | Đổi tên trước khi nạp, không nạp rồi sửa sau |
| 3 | Kho này chứa nhiều phiên bản? Đã chèn số hiệu chưa? | Chèn số hiệu vào tên và ghi phiên bản trong nội dung |
| 4 | Nội dung có dữ liệu định danh người chơi không? | Loại bỏ, hoặc chuyển sang kho cách ly. Không nạp vào kho đang chia sẻ |
| 5 | Mức nhạy cảm của tài liệu có cao hơn mức hiện tại của kho không? | Không nạp. Kho khác hoặc kho mới |
| 6 | Ai là chủ sở hữu nội dung này, và họ đã đồng ý chưa? | Hỏi trước khi nạp |
| 7 | Tài liệu ghi rõ trạng thái của nó chưa (nháp, đã duyệt, đã phát hành)? | Ghi vào phần mở đầu. Người đọc sau cần biết tin được tới đâu |

Ba nguyên tắc nền, áp cho mọi kho:

- **Một tài liệu chỉ có một kho là nguồn chuẩn.** Cùng một nội dung nằm ở hai kho mà không ghi rõ đâu là gốc là cách chắc chắn nhất để tạo ra hai câu trả lời mâu thuẫn.
- **Sửa ở nguồn, không sửa trực tiếp trên kho.** Nhiều kho được sinh ra từ tài liệu gốc. Sửa thẳng trên kho thì lần cập nhật sau sẽ ghi đè mất, không cảnh báo.
- **Ghi trạng thái ngay trong nội dung.** Dòng mở đầu nói rõ đây là bản nháp hay bản đã duyệt, áp dụng cho phiên bản nào. Dòng đó đi theo tài liệu vào mọi câu trả lời của trợ lý — đó là lớp phòng vệ rẻ nhất và hiệu quả nhất.

## 4. Khi bạn không chắc

Không chắc tài liệu thuộc kho nào, không chắc dữ liệu có nhạy cảm không, không chắc được phép chia sẻ — **hỏi chủ sở hữu kho trước khi nạp**.

Gỡ một tài liệu đã nạp nhầm khó hơn nhiều so với việc chờ một câu trả lời. Nội dung nhạy cảm nạp vào kho không chỉ nằm ở file gốc: nó lan sang phần mô tả và tóm tắt tự sinh, và xoá file thôi thì chưa đủ.

## Đọc tiếp

- **Các kho tri thức của GS9 CFL** — mỗi kho chứa gì, ai phụ trách.
- **Chọn kho tri thức** — câu hỏi loại nào thì tra kho nào.
- **Sử dụng an toàn** — điều cấm và người duyệt khi làm việc với trợ lý.
