# Trợ lý AI cho GS9 CFL — giới thiệu và phạm vi

Đọc xong phần này bạn biết: có những trợ lý nào, mỗi trợ lý làm việc gì, và bạn được phép dùng trợ lý tới đâu.

## Bộ tài liệu này nói về cái gì

Nền tảng VNG AI có hai nhóm trợ lý:

- **Sáu trợ lý mặc định** của nền tảng — ai cũng dùng được, dùng để hỏi đáp trên kho tri thức, tra Wiki hoặc phân tích file bảng.
- **Mười trợ lý riêng của GS9 CFL** — được tạo cho từng đầu việc LiveOps: lập kế hoạch sự kiện, rà soát phát hành, xử lý sự cố, phân tích KPI, kinh tế, phản hồi người chơi, hỗ trợ CS, tra chính sách GM, soạn thông báo và tổng hợp bài học.

Bộ tài liệu giúp bạn:

- hiểu mỗi trợ lý được thiết kế cho việc gì;
- chọn đúng trợ lý cho tình huống của mình;
- biết trợ lý được phép chạm vào dữ liệu nào và tuyệt đối không được làm gì;
- biết ai là người ký duyệt kết quả trước khi nó thành hành động thật.

## Bộ tài liệu này KHÔNG chứa cái gì

Đây là tài liệu **về các trợ lý**, không phải kho dữ liệu nghiệp vụ game.

Không tìm ở đây: brief sự kiện, dữ liệu người chơi, số liệu doanh thu, chính sách GM/CS, danh mục vật phẩm. Những thứ đó nằm trong các kho tri thức nghiệp vụ riêng, có chủ sở hữu và quyền truy cập riêng.

## Quy tắc lớn nhất: trợ lý không tự thực hiện hành động

Mọi kết quả trợ lý trả ra đều là **bản nháp để người rà soát**, kể cả khi nó viết rất chắc chắn.

Trợ lý không mở/tắt sự kiện, không đổi cấu hình, không phát hành, không rollback, không gửi thông báo, không tặng vật phẩm hay tiền, không hoàn tiền, không khoá tài khoản, không sửa kho tri thức. Nếu một câu trả lời nghe như "đã xong rồi", đó là câu chữ của mô hình, không phải việc đã xảy ra.

## Trước khi dùng cho công việc thật

Mười trợ lý riêng của GS9 CFL đang trong giai đoạn chuẩn bị. Chúng chưa được chủ sở hữu nghiệp vụ ký duyệt phát hành, nên **chưa dùng kết quả của chúng cho quyết định vận hành**.

Với sáu trợ lý mặc định: chúng đang mở phạm vi tra cứu ra toàn bộ kho tri thức bạn có quyền. Vì vậy đừng nhập dữ liệu nhạy cảm và luôn mở nguồn để kiểm lại con số quan trọng.

Nếu công việc của bạn dính tới thông tin cá nhân người chơi, vụ việc GM, chế tài, bồi thường, cấu hình live hoặc nội dung gửi ra ngoài: phải đi theo quy trình đã được duyệt, không thay thế bằng một trợ lý cho tiện.

## Các phần còn lại

- **Chọn trợ lý nhanh** — bảng tra theo nhu cầu công việc.
- **So sánh 16 trợ lý** — mỗi trợ lý mạnh gì, yếu gì.
- **Luồng công việc của 10 trợ lý GS9 CFL** — ai bàn giao cho ai, bàn giao cái gì.
- **Sử dụng an toàn** — điều cấm, người duyệt, cách dừng khi có sự cố.

## Thuật ngữ tối thiểu

| Thuật ngữ | Nghĩa trong bộ tài liệu này |
|---|---|
| Kho tri thức | Nguồn tài liệu mà trợ lý được phép tra để trả lời |
| Công cụ | Khả năng trợ lý gọi thêm khi trả lời, ví dụ tìm theo ngữ nghĩa, đọc trang Wiki |
| Chế độ suy nghĩ | Công tắc bật suy luận mở rộng của mô hình; khác với công cụ `Suy nghĩ` trong danh sách công cụ |
| Bản nháp | Kết quả để người rà soát, chưa phải hành động đã thực hiện |
| Người duyệt | Người bắt buộc phải đồng ý trước khi kết quả được phát hành, gửi đi hoặc áp lên hệ thống thật |
| Không gắn kho tri thức | Trợ lý chưa có nguồn nghiệp vụ nào để tra; câu trả lời khi đó không có gì bảo chứng |
