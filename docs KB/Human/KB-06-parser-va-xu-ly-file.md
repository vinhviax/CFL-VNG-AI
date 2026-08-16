# 06 - Parser và xử lý file {#06-parser-va-xu-ly-file}

Đọc xong bạn biết parser là gì, mỗi định dạng chọn được parser nào, đổi parser ở đâu và làm sao kiểm tra parser đã đọc đúng nội dung.

## Parser là gì

Parser là bộ đọc, chuyển file thành nội dung văn bản để hệ thống chia đoạn và lập chỉ mục. Đổi parser thì nội dung đoạn đổi, kết quả truy hồi đổi theo — dù file nguồn không thay đổi một byte.

Parser nằm ở **Cài đặt → Xử lý** và **chỉ có ở KB Tài liệu**. KB FAQ không có tab Xử lý.

Tên engine trên giao diện gồm **Built-in, Simple, MinerU, LLM, markitdown, liteparse**. Không định dạng nào có đủ cả sáu.

![Tab Xử lý với cấu hình parser theo từng định dạng file](<knowledge/GS9 Knowledge VNG AI/image-04-xu-ly-parser-theo-dinh-dang.png>)

*Ảnh 06.1 - Các lựa chọn parser thay đổi theo từng nhóm file.*

## Parser theo nhóm định dạng khi tải tệp lên

| Nhóm file | Các lựa chọn trong dropdown |
|---|---|
| PDF | Built-in, MinerU, LLM, markitdown, liteparse |
| Word | Built-in, MinerU, LLM, markitdown |
| PPT/PPTX | MinerU, markitdown |
| Excel | Built-in, MinerU, LLM, markitdown |
| CSV | Simple, LLM, markitdown |
| Markdown | Built-in, Simple, LLM, markitdown |
| TXT | Simple, LLM |
| JSON | Simple |
| Images | Built-in, Simple, MinerU |
| Email | Built-in, LLM |
| EPUB | Built-in |
| HTML | Built-in, markitdown |
| MHTML | Built-in |
| Audio | Giá trị hiển thị là Built-in, nhưng dropdown chỉ có Simple |

Ba điểm cần ghi nhớ:

- **PPT/PPTX không có Built-in.** Nếu quy trình cũ của bạn giả định PPT dùng Built-in thì giả định đó sai.
- **Audio có mâu thuẫn** giữa giá trị đang hiển thị và tập lựa chọn mở ra được.
- Danh sách này **có thể khác tùy môi trường bạn đang dùng**. Luôn mở dropdown xác nhận trước khi chốt cấu hình, đừng chép nguyên bảng này vào quy trình.

## Hiểu tên engine để chọn bài test

| Engine | Cách hiểu thực dụng |
|---|---|
| **Built-in** | Bộ đọc tích hợp của hệ thống |
| **Simple** | Trích xuất đơn giản, hợp với văn bản ít bố cục |
| **MinerU** | Hướng tới tài liệu có bố cục, bảng hoặc hình phức tạp |
| **LLM** | Dùng model diễn giải cấu trúc; tốn thời gian, có thể tạo cách viết khác nguồn |
| **markitdown** | Chuyển nhiều định dạng sang Markdown |
| **liteparse** | Lựa chọn riêng, chỉ thấy ở PDF |

Đây là cách hiểu để chọn bài test, không phải bảng xếp hạng chất lượng. Chưa có engine nào được chứng minh là tốt hơn engine khác trên mọi loại tài liệu — phải tự chạy A/B trên tài liệu của bạn.

## Parser ghi đè được ở ba nơi

| Vị trí | Control |
|---|---|
| Modal **Tải tệp lên** / **Tải thư mục lên** | Mục **Xử lý nâng cao** — ghi đè cho riêng lượt nạp này |
| Menu chi tiết tài liệu | **Phân tích lại với tùy chọn nâng cao** |
| Wizard nguồn dữ liệu, bước Chiến lược | Ghi đè parser theo loại tệp cho cả nguồn |

Wizard nguồn dữ liệu ngoài (Google Drive, Notion, NAS) **hiển thị tập parser khác** với khi tải tệp lên tay. Đừng giả định hai nơi giống nhau — xem chi tiết ở phần Chia sẻ và nguồn dữ liệu.

## Quy trình A/B parser

1. Chọn một file đại diện có heading, bảng, chú thích ảnh và **một mã độc nhất** để tra lại trong chat.
2. Giữ nguyên mọi cấu hình khác, chỉ đổi parser.
3. Xử lý bằng parser A, ghi số đoạn và nội dung một số đoạn.
4. Dùng **Phân tích lại với tùy chọn nâng cao**, hoặc một KB test riêng, để chạy parser B.
5. Hỏi câu dựa vào bảng, heading và caption ảnh — ba chỗ parser hay làm hỏng nhất.
6. Chọn parser theo khả năng giữ đúng cấu trúc và dữ kiện, không theo độ dài tóm tắt.

## Dấu hiệu parser chưa phù hợp

- Heading bị nối vào đoạn trước.
- Cột bảng bị đảo hoặc mất tên cột.
- Text trong ảnh được đọc nhưng gắn sai khu vực.
- Một PDF dài chỉ thành một khối, khó truy hồi.
- Tóm tắt nghe hợp lý nhưng mã, số và ngoại lệ biến mất.

## Trạng thái Hoàn tất không có nghĩa là parse đúng

**Hoàn tất** chỉ xác nhận pipeline đã chạy xong. Tài liệu vẫn có thể ở trạng thái Hoàn tất mà kèm thông báo lỗi bên trong, hoặc nội dung bị mất mát.

Luôn kiểm tra bằng hai bước, không dùng riêng badge trạng thái làm căn cứ:

1. Mở chi tiết tài liệu → **Xem phân đoạn**, đọc nội dung thật của vài đoạn.
2. Chat bằng câu hỏi đối chứng và xem phần nguồn truy hồi.

Danh sách Documents và khả năng truy hồi thực tế có thể lệch pha nhau: tài liệu còn hiện **Đang hoàn tất** nhưng chat đã tìm ra nội dung, hoặc ngược lại. Nếu trạng thái treo lâu, tải lại danh sách trước khi kết luận là lỗi.

## Đừng đổi đuôi tệp

Parser suy ra định dạng và đường dẫn xuất từ **nội dung thật** của file, không phải từ tên file. Một ảnh JPEG được đổi tên thành `.png` sẽ sinh liên kết ảnh sai đuôi và làm hỏng ảnh trong tài liệu.

Nếu cần định dạng PNG, hãy chuyển đổi thật sự bằng công cụ ảnh rồi mới tải lên.

## File Markdown vẫn cần cấu trúc tốt

Parser không thay thế việc viết heading. Với Markdown, đặt một `#` cho tên tài liệu và dùng `##` cho từng ý định người dùng thường hỏi. Cách này bền vững hơn việc dựa vào ký hiệu trang trí hoặc chữ in đậm.
