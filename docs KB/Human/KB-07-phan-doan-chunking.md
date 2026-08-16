# 07 - Phân đoạn và chunking {#07-phan-doan-chunking}

Đọc xong bạn biết chunk là gì, bốn chiến lược phân đoạn khác nhau ra sao, đặt kích thước trong khoảng nào và làm sao đo được ảnh hưởng bằng truy hồi thật.

## Chunk là gì

Chunk, hay phân đoạn, là đơn vị nội dung được dùng cho tìm kiếm. Chunk quá lớn dễ mang nhiều chủ đề; chunk quá nhỏ dễ mất điều kiện và ngoại lệ. Không có cấu hình tốt tuyệt đối — nó phụ thuộc cấu trúc nguồn và dạng câu hỏi.

Mục **Phân đoạn** nằm ở **Cài đặt → Xử lý**, chỉ có ở KB Tài liệu. FAQ không có tab Xử lý.

**Mọi con số kích thước đều tính bằng KÝ TỰ, không phải TỪ.** Nếu tài liệu nội bộ nào của bạn ghi "200-500 từ" thì con số đó sai cả đơn vị lẫn giá trị.

![Tab Xử lý với chế độ phân đoạn cha-con và các kích thước](<knowledge/GS9 Knowledge VNG AI/image-05-xu-ly-phan-doan-cha-con.png>)

*Ảnh 07.1 - Giao diện cấu hình chunk cha-con trong KB Tài liệu.*

## Bốn chiến lược phân đoạn

| Chiến lược | Mô tả trên giao diện |
|---|---|
| **Tự động** | Bộ phân tích chọn giữa chia theo tiêu đề, theo cấu trúc và theo độ dài cho mỗi tài liệu |
| **Theo tiêu đề** | Chia tại ranh giới tiêu đề Markdown; mỗi đoạn mang theo đường dẫn tiêu đề |
| **Theo cấu trúc** | Chia theo dấu hiệu cấu trúc: ngắt trang, mục đánh số, dấu hiệu chương, tiêu đề viết hoa |
| **Theo độ dài** | Bỏ qua cấu trúc; chia đệ quy theo số ký tự và dấu phân tách |

Ba điều cần biết trước khi tin vào mô tả trên:

- **Theo tiêu đề chỉ nhận cú pháp `#` / `##` của Markdown.** Nó không nhận ra dấu hiệu heading mà mắt người thấy rõ, ví dụ dòng `CHƯƠNG MỘT` viết hoa hay cặp `Q:` / `A:`.
- **Theo cấu trúc thường không tách được PDF nghiệp vụ.** Một PDF nhiều trang có ngắt trang thật và mục đánh số vẫn có thể ra đúng một đoạn. Đừng chọn chiến lược này rồi coi như xong — phải mở tài liệu kiểm tra số đoạn thực tế.
- **Theo độ dài cắt cứng theo số ký tự.** Ranh giới đoạn có thể rơi vào giữa một câu. Dấu phân tách chỉ là tham khảo phụ, số ký tự được ưu tiên trước.

**Ràng buộc:** khi chọn **Theo độ dài**, hai trường **Giới hạn token** và **Gợi ý ngôn ngữ** bị vô hiệu hóa. Cần một trong hai thì phải đổi sang Tự động, Theo tiêu đề hoặc Theo cấu trúc.

## Cha-con và Thông thường

Hai chế độ cấu trúc này độc lập với bốn chiến lược ở trên, kết hợp tự do.

- **Chunk con** khớp chính xác phần nhỏ có từ ngữ liên quan, dùng cho tìm kiếm.
- **Chunk cha** được trả về kèm để câu trả lời có ngữ cảnh rộng hơn.

Lợi ích chỉ có thật khi chunk cha chứa **đúng** ngữ cảnh của chunk con. Nếu file trộn nhiều chủ đề trong cùng một mục, tăng kích thước cha chỉ kéo thêm nhiễu.

### Khoảng giá trị - chế độ Cha-con

| Thông số | Khoảng | Giá trị thường gặp |
|---|---|---|
| Kích thước đoạn **cha** | 512 - 32.768 ký tự | 32.768 |
| Kích thước đoạn **con** | 64 - 8.192 ký tự | 8.192 |
| Chồng lấp cha | 0 - 4.096 ký tự | 0 (0 = dùng độ chồng lấp chính) |
| Chồng lấp con | 0 - 2.048 ký tự | 0 |

### Khoảng giá trị - chế độ Thông thường

| Thông số | Khoảng | Giá trị thường gặp |
|---|---|---|
| Kích thước đoạn | 128 - 16.384 ký tự | 16.384 |
| Độ chồng lấp | 0 - 4.096 ký tự | 0 |

## Tùy chọn nâng cao

| Tùy chọn | Mô tả trên giao diện |
|---|---|
| **Truy hồi theo ngữ cảnh** | Thêm tiêu đề ngữ cảnh do LLM viết vào mỗi đoạn để cải thiện truy hồi |
| **Giới hạn token** | Khoảng 0 - 8.192; đặt `0` là tắt |
| **Dấu phân tách** | Ký tự mà bộ chia ưu tiên khi cắt; dấu ưu tiên cao được thử trước |
| **Sinh câu hỏi** | Khi bật hiện thêm **Số câu hỏi mỗi đoạn**, khoảng 1 - 10 |
| **Gợi ý ngôn ngữ** | Ba nút DE / EN / ZH. Để trống là tự nhận diện |

Khi bật **Truy hồi theo ngữ cảnh**, mở chi tiết tài liệu → **Xem phân đoạn** sẽ thấy khối **Ngữ cảnh tìm kiếm (LLM tạo)** ở đầu mỗi đoạn. Đó là cách xác nhận tính năng đang chạy thật.

### Ba lưu ý cho nội dung tiếng Việt

1. Bộ dấu phân tách mặc định nghiêng về ngữ pháp CJK, gồm dòng trống, dòng mới, `。`, `！`, `？`, `;`, `；`. Với tiếng Việt, các dấu `\n\n`, `\n`, `.`, `!`, `?`, `;` vẫn dùng bình thường.
2. **Gợi ý ngôn ngữ không có nút Tiếng Việt** — chỉ DE, EN, ZH.
3. Cứ để trống. Hệ thống nhận diện đúng tiếng Việt trên văn bản dài.

## Xem trước phân đoạn không đọc file đã tải lên

Nút **Xem trước phân đoạn** chỉ chạy trên văn bản bạn dán tay hoặc bốn văn bản mẫu dựng sẵn. Nó **không** đọc file đã nằm trong KB.

Muốn biết file thật bị cắt thế nào: tải lên, rồi mở chi tiết tài liệu → **Xem phân đoạn**.

## Ghi đè phân đoạn ở ba cấp

| Cấp | Vị trí | Phạm vi áp dụng |
|---|---|---|
| KB | Cài đặt → Xử lý → Phân đoạn | Tài liệu nạp sau; tài liệu cũ cần **Phân tích lại** |
| Lượt tải | Modal Tải tài liệu lên → **Xử lý nâng cao** | Riêng lượt nạp đó |
| Nguồn ngoài | Wizard nguồn dữ liệu → bước Chiến lược | Mọi tệp của nguồn đó |

Giữ giá trị `0` hoặc để trống ở lượt đầu để kế thừa cấu hình KB. Chỉ ghi đè khi đã có bộ câu hỏi đối chứng để đo trước và sau.

Khác với Embedding, cấu hình parser và phân đoạn **không bị khóa** khi KB đã có nội dung. Bạn đổi được bất cứ lúc nào.

## Phân tích lại và Sửa nội dung cho kết quả khác nhau

| | **Phân tích lại** | **Sửa nội dung + Xuất bản** |
|---|---|---|
| Chuỗi trạng thái | Chờ xử lý → Đang hoàn tất → Hoàn tất | Chờ xử lý → Đang hoàn tất → Hoàn tất |
| Số chunk | Có thể **không đổi** | Thay đổi theo nội dung, cả tăng lẫn giảm |
| Tóm tắt | Được sinh lại, cách diễn đạt có thể khác | Cập nhật theo nội dung mới |

**Phân tích lại** tái chạy pipeline và tái sinh tóm tắt, nhưng không bảo đảm số chunk thay đổi. Nếu bạn chỉ đổi một thiết lập không ảnh hưởng ranh giới đoạn — ví dụ độ chi tiết Wiki — thì số chunk sẽ giữ nguyên.

Muốn số đoạn thay đổi thật, phải đổi tham số phân đoạn hoặc đổi nội dung tài liệu.

Ghi lại số liệu trước và sau mỗi lần đổi. Đừng đánh giá bằng cảm giác.

## Đo ảnh hưởng bằng truy hồi thật

Với mỗi cấu hình, đo:

- Số chunk được tạo.
- Heading hoặc đường dẫn cấu trúc đi cùng chunk.
- Chunk chứa điều kiện, ngoại lệ và kết quả có bị tách không.
- Câu hỏi diễn đạt khác từ nguồn có truy hồi đúng không.
- Câu gần giống nhưng ngoài phạm vi có bị kéo nhầm không.

### Bộ câu hỏi kiểm thử chunk

Với mỗi tài liệu, chuẩn bị ít nhất:

1. Câu hỏi có đáp án nằm trọn trong một mục.
2. Câu cần ghép điều kiện và ngoại lệ trong cùng mục.
3. Câu cần liên kết hai mục xa nhau.
4. Câu dùng từ đồng nghĩa, không trùng từ nguồn.
5. Câu có cùng từ khóa nhưng khác phạm vi.

Xem phần nguồn truy hồi trước khi đánh giá văn phong câu trả lời.
