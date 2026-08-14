<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 07 - Phân đoạn và chunking {#07-phan-doan-chunking}

## Bạn sẽ biết gì sau khi đọc

- Chunk là gì, chế độ cha-con dùng để làm gì.
- Cấu hình đang quan sát được trong KB test.
- Cách đo ảnh hưởng của phân đoạn bằng truy hồi thật.

**Kiểm chứng giao diện: 06/08/2026.**

## Chunk là gì

Chunk, hay phân đoạn, là đơn vị nội dung được dùng cho tìm kiếm. Chunk quá lớn dễ mang nhiều chủ đề; chunk quá nhỏ dễ mất điều kiện và ngoại lệ. Cấu hình tốt phụ thuộc cấu trúc nguồn và dạng câu hỏi.

## Trạng thái hiện hữu đã kiểm tra

Trong KB Tài liệu test:

- Chiến lược: **Tự động**.
- Chế độ: **Cha-con**.
- Kích thước cha: **32.768 ký tự**.
- Kích thước con: **8.192 ký tự**.
- Chồng lấp cha/con: **0 / 0**.
- **Truy hồi theo ngữ cảnh:** bật.
- **Sinh câu hỏi:** tắt.
- **Giới hạn token:** 0.
- Dấu phân cách hiển thị gồm dòng trống, dòng mới, `。`, `！`, `？`, `;`, `；`.
- Gợi ý ngôn ngữ có nút **DE, EN, ZH**; ô hiện để trống.

Đây là trạng thái của KB test, không phải cam kết mặc định cho mọi KB mới.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/05-xu-ly-phan-doan-cha-con.png -->
![Tab Xử lý với chế độ phân đoạn cha-con và các kích thước](minio://knowledge-base-prd/10012/exports/fe6f61d9-fbdb-4ec8-b39e-e8ca2c28cbc5.png)

*Ảnh 07.1 - Giao diện cấu hình chunk cha-con trong KB Tài liệu.*

## Hiểu chế độ cha-con

- **Chunk con** giúp tìm đúng phần nhỏ có từ ngữ liên quan.
- **Chunk cha** cung cấp bối cảnh rộng hơn cho câu trả lời.

Lợi ích chỉ có thật khi chunk cha chứa đúng ngữ cảnh của chunk con. Nếu file trộn nhiều chủ đề trong cùng section, tăng kích thước có thể kéo thêm nhiễu.

## Các chiến lược và điều cần đo

Giao diện có các lựa chọn phân đoạn khác nhau theo cấu hình. Không nên kết luận một chiến lược “tốt nhất” nếu chỉ nhìn preview. Với mỗi chiến lược, đo:

- Số chunk được tạo.
- Heading hoặc đường dẫn cấu trúc đi cùng chunk.
- Chunk chứa điều kiện, ngoại lệ và kết quả có bị tách không.
- Câu hỏi diễn đạt khác từ nguồn có truy hồi đúng không.
- Câu gần giống nhưng ngoài phạm vi có bị kéo nhầm không.

## Phép thử Phân tích lại đã thực hiện

Tài liệu `03-so-sanh-aurora-borealis.md` có 1 chunk trước khi chạy. Sau khi đổi độ chi tiết Wiki từ **Tiêu chuẩn** sang **Toàn diện** và bấm **Phân tích lại**:

- Trạng thái đi qua **Chờ xử lý, Đang hoàn tất, Hoàn tất**.
- Số chunk vẫn là 1.
- Thời gian tải lên không đổi.
- Tóm tắt được sinh lại và thay đổi cách diễn đạt.

Kết luận: **Phân tích lại** có thể tái xử lý và tái sinh tóm tắt, nhưng không bảo đảm số chunk thay đổi nếu cấu hình hoặc nội dung không tạo ranh giới khác.

## Bộ câu hỏi kiểm thử chunk

Với mỗi tài liệu, chuẩn bị ít nhất:

1. Câu hỏi có đáp án nằm trọn trong một mục.
2. Câu cần ghép điều kiện và ngoại lệ trong cùng mục.
3. Câu cần liên kết hai mục xa nhau.
4. Câu dùng từ đồng nghĩa, không trùng từ nguồn.
5. Câu có cùng từ khóa nhưng khác phạm vi.

Xem phần nguồn truy hồi trước khi đánh giá văn phong câu trả lời.
