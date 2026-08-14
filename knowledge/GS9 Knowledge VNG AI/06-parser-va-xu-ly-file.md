<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 06 - Parser và xử lý file {#06-parser-va-xu-ly-file}

## Bạn sẽ biết gì sau khi đọc

- Parser là gì và vì sao cùng một file có thể cho kết quả khác.
- Ma trận lựa chọn parser theo định dạng ở giao diện hiện tại.
- Cách kiểm thử parser bằng nội dung thật, không chỉ nhìn trạng thái Hoàn tất.

**Kiểm chứng giao diện: 06/08/2026.**

## Parser là gì

Parser là bộ đọc và chuyển file thành nội dung để hệ thống lập chỉ mục. Tên engine trên giao diện gồm **Built-in, Simple, MinerU, LLM, markitdown, liteparse**. Không phải định dạng nào cũng có đủ mọi engine.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/04-xu-ly-parser-theo-dinh-dang.png -->
![Tab Xử lý với cấu hình parser theo từng định dạng file](minio://knowledge-base-prd/10012/exports/0bdef2c5-bca0-4a1c-9171-271ec43687cc.png)

*Ảnh 06.1 - Các lựa chọn parser thay đổi theo từng nhóm file.*

## Ma trận quan sát trực tiếp

| Nhóm file | Các lựa chọn thấy trong dropdown |
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
| Audio | UI hiển thị Built-in đang chọn, nhưng dropdown chỉ có Simple |

Hai điểm cần ghi nhớ:

- PPT/PPTX **không có Built-in** trong dropdown đã kiểm tra.
- Audio có mâu thuẫn giữa giá trị đang hiển thị và lựa chọn có thể chọn.

## Hiểu tên engine theo hướng thực dụng

- **Built-in:** bộ đọc tích hợp của hệ thống.
- **Simple:** trích xuất đơn giản, phù hợp nội dung văn bản ít bố cục.
- **MinerU:** hướng tới tài liệu có bố cục, bảng hoặc hình phức tạp.
- **LLM:** dùng model để diễn giải cấu trúc; có thể tốn thời gian và tạo cách viết khác nguồn.
- **markitdown:** chuyển nhiều định dạng sang Markdown.
- **liteparse:** lựa chọn riêng quan sát được cho PDF.

Các mô tả trên giúp chọn bài test; không phải cam kết kỹ thuật nội bộ của từng engine.

## Quy trình A/B parser

1. Chọn một file đại diện có heading, bảng, chú thích ảnh và một mã độc nhất.
2. Giữ nguyên mọi cấu hình khác.
3. Xử lý bằng parser A, ghi số đoạn và nội dung một số đoạn.
4. Dùng **Phân tích lại với tùy chọn nâng cao** hoặc một KB test riêng để thử parser B.
5. Hỏi câu dựa vào bảng, heading và caption ảnh.
6. Chọn parser theo khả năng giữ đúng cấu trúc và dữ kiện, không theo độ dài tóm tắt.

## Dấu hiệu parser chưa phù hợp

- Heading bị nối vào đoạn trước.
- Cột bảng bị đảo hoặc mất tên cột.
- Text trong ảnh được đọc nhưng gắn sai khu vực.
- Một PDF dài chỉ thành một khối khó truy hồi.
- Tóm tắt nghe hợp lý nhưng mã, số và ngoại lệ biến mất.

## File Markdown vẫn cần cấu trúc tốt

Parser không thay thế việc viết heading. Với Markdown, đặt một `#` cho tên tài liệu và dùng `##` cho các ý định người dùng thường hỏi. Đây là cách bền vững hơn việc dựa vào ký hiệu trang trí hoặc chữ in đậm.
