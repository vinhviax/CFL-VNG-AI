<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 03 - KB Tài liệu, RAG và Wiki {#03-tai-lieu-rag-wiki}

## Bạn sẽ biết gì sau khi đọc

- RAG và Wiki khác nhau ở đầu ra nào.
- Cách bật đồng thời RAG và Wiki.
- Giới hạn của Wiki và Graph đã quan sát được.

**Kiểm chứng giao diện: 06/08/2026.**

## Thuật ngữ

- **RAG:** tìm các đoạn liên quan trong nguồn và đưa chúng vào ngữ cảnh trả lời.
- **Wiki:** tổng hợp nội dung đã nạp thành các trang có cấu trúc và liên kết.
- **Graph:** biểu diễn các node và quan hệ được sinh từ nội dung.

## RAG và Wiki có thể bật cùng lúc

Trong tab **Tổng quan** của KB Tài liệu, RAG và Wiki là hai checkbox độc lập, không phải lựa chọn loại trừ. Khi bật Wiki, giao diện có ba mức chi tiết:

- **Tập trung**
- **Tiêu chuẩn** - caption quan sát được là “Số trang cân bằng.”
- **Toàn diện**

Caption “Số trang cân bằng” là mô tả, không phải trường nhập số trang.

| Nhu cầu | RAG | Wiki |
|---|---|---|
| Hỏi đáp nhanh và xem nguồn | Phù hợp | Có thể hỗ trợ gián tiếp |
| Đọc theo mục lục, hiểu bức tranh | Không phải đầu ra chính | Phù hợp |
| Kiểm soát câu chữ gốc | Dễ đối chiếu đoạn nguồn | Nội dung đã được tổng hợp lại |
| Phụ thuộc chất lượng nguồn | Cao | Rất cao vì có bước viết lại |

## Wiki trong trang làm việc

Tab Wiki của KB Tài liệu đã kiểm thử có:

- **Mục lục** và **Nhật ký hoạt động**.
- Cách xem theo **Thư mục** hoặc **Loại**.
- Khả năng tạo thư mục để tổ chức trang.
- Liên kết từ node Graph sang **Mở trong Wiki** khi node có trang liên quan.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/09-wiki-muc-luc-va-trang.png -->
![Tab Wiki với mục lục và trang tổng hợp](minio://knowledge-base-prd/10012/exports/011f18dc-0a2b-4e6a-aba3-96242f155127.png)

*Ảnh 03.1 - Wiki là lớp nội dung tổng hợp, tách với danh sách file gốc.*

## FAQ cũng hiện tab Wiki/Graph nhưng chưa có chức năng thật

Ở KB FAQ được kiểm thử, **Documents, Wiki, Graph** đều xuất hiện. Khi bấm Wiki hoặc Graph, trang chỉ báo:

> Wiki chưa được bật. Bật Wiki trong cài đặt Knowledge Base (chiến lược lập chỉ mục) để tự động tổng hợp trang wiki từ tài liệu.

FAQ không có control bật Wiki trong cấu hình. Vì vậy đây là khung giao diện dùng chung, không phải bằng chứng FAQ hỗ trợ Wiki/Graph.

## Graph và các loại node

Chú giải Graph quan sát được gồm **Tóm tắt, Thực thể, Khái niệm, Tổng hợp, So sánh**.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/10-graph-cac-loai-node.png -->
![Graph với chú giải năm loại node](minio://knowledge-base-prd/10012/exports/8ee2eedb-6160-4511-9448-b38251f438f0.png)

*Ảnh 03.2 - Chú giải có Tổng hợp và So sánh, nhưng KB test vẫn chưa sinh được hai loại node này.*

Ngay sau phép thử nạp bộ Aurora/Borealis, chuyển Wiki sang **Toàn diện** và chạy **Phân tích lại**, Graph ghi nhận 93 node: Tóm tắt 9, Thực thể 42, Khái niệm 41, Tổng hợp 0, So sánh 0. Ở lượt đối chiếu cuối cùng cùng ngày, sau khi các nguồn tiếp tục được xử lý, Graph hiển thị 159/159 node: Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0, So sánh 0. Vì vậy 93 chỉ là ảnh chụp tại một thời điểm, không phải giới hạn cố định. Không tìm thấy nút tạo tay hai loại node này.

**Kết luận:** giao diện định nghĩa hai loại node, nhưng điều kiện sinh chúng chưa được xác định. Không viết hướng dẫn khẳng định “cứ có hai tài liệu liên quan là sinh node So sánh”.

## Khi nên bật Wiki

- Nguồn đã được làm sạch, heading rõ và không có hai phiên bản mâu thuẫn.
- Người đọc cần đi theo chủ đề, không chỉ hỏi từng câu rời rạc.
- Có người kiểm tra trang tổng hợp sau mỗi đợt cập nhật lớn.

Nếu ưu tiên tuyệt đối việc trích đúng câu chữ gốc, hãy bắt đầu với RAG và kiểm tra nguồn trước khi bật Wiki.
