# 03 - KB Tài liệu, RAG và Wiki {#03-tai-lieu-rag-wiki}

## Bạn sẽ biết gì sau khi đọc

- RAG và Wiki khác nhau ở đầu ra nào.
- Cách bật đồng thời RAG và Wiki.
- Giới hạn hiện tại của Wiki và Graph.

## Thuật ngữ

- **RAG:** tìm các đoạn liên quan trong nguồn và đưa chúng vào ngữ cảnh trả lời.
- **Wiki:** tổng hợp nội dung đã nạp thành các trang có cấu trúc và liên kết.
- **Graph:** biểu diễn các node và quan hệ được sinh từ nội dung.

## RAG và Wiki có thể bật cùng lúc

Trong tab **Tổng quan** của KB Tài liệu, RAG và Wiki là hai checkbox độc lập, không phải lựa chọn loại trừ. Khi bật Wiki, giao diện có ba mức chi tiết:

- **Tập trung**
- **Tiêu chuẩn** - caption là “Số trang cân bằng.”
- **Toàn diện**

Caption “Số trang cân bằng” là mô tả, không phải trường nhập số trang.

| Nhu cầu | RAG | Wiki |
|---|---|---|
| Hỏi đáp nhanh và xem nguồn | Phù hợp | Có thể hỗ trợ gián tiếp |
| Đọc theo mục lục, hiểu bức tranh | Không phải đầu ra chính | Phù hợp |
| Kiểm soát câu chữ gốc | Dễ đối chiếu đoạn nguồn | Nội dung đã được tổng hợp lại |
| Phụ thuộc chất lượng nguồn | Cao | Rất cao vì có bước viết lại |

## Wiki trong trang làm việc

Tab Wiki của KB Tài liệu có:

- **Mục lục** và **Nhật ký hoạt động**.
- Cách xem theo **Thư mục** hoặc **Loại**.
- Khả năng tạo thư mục để tổ chức trang.
- Liên kết từ node Graph sang **Mở trong Wiki** khi node có trang liên quan.

![Tab Wiki với mục lục và trang tổng hợp](<knowledge/GS9 Knowledge VNG AI/image-09-wiki-muc-luc-va-trang.png>)

*Ảnh 03.1 - Wiki là lớp nội dung tổng hợp, tách với danh sách file gốc.*

## FAQ cũng hiện tab Wiki/Graph nhưng chưa có chức năng thật

Ở KB FAQ, **Documents, Wiki, Graph** đều xuất hiện. Khi bấm Wiki hoặc Graph, trang chỉ báo:

> Wiki chưa được bật. Bật Wiki trong cài đặt Knowledge Base (chiến lược lập chỉ mục) để tự động tổng hợp trang wiki từ tài liệu.

FAQ không có control bật Wiki trong cấu hình. Đây là khung giao diện dùng chung giữa hai loại KB, không có nghĩa là FAQ hỗ trợ Wiki/Graph.

## Graph và các loại node

Chú giải Graph gồm **Tóm tắt, Thực thể, Khái niệm, Tổng hợp, So sánh**.

![Graph với chú giải năm loại node](<knowledge/GS9 Knowledge VNG AI/image-10-graph-cac-loai-node.png>)

*Ảnh 03.2 - Chú giải có Tổng hợp và So sánh, nhưng KB test vẫn chưa sinh được hai loại node này.*

Số node trong Graph tăng dần khi các nguồn tiếp tục được xử lý, nên con số hiển thị chỉ là ảnh chụp tại một thời điểm, không phải giới hạn cố định. Riêng hai loại **Tổng hợp** và **So sánh** vẫn ở mức 0, và không có nút tạo tay hai loại node này.

Giao diện định nghĩa năm loại node, nhưng điều kiện sinh hai loại cuối chưa rõ. Đừng lên kế hoạch dựa trên giả định “cứ có hai tài liệu liên quan là sinh node So sánh”.

## Khi nên bật Wiki

- Nguồn đã được làm sạch, heading rõ và không có hai phiên bản mâu thuẫn.
- Người đọc cần đi theo chủ đề, không chỉ hỏi từng câu rời rạc.
- Có người kiểm tra trang tổng hợp sau mỗi đợt cập nhật lớn.

Nếu ưu tiên tuyệt đối việc trích đúng câu chữ gốc, hãy bắt đầu với RAG và kiểm tra nguồn trước khi bật Wiki.
