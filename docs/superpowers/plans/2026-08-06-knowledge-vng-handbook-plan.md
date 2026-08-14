# Kế hoạch triển khai Sổ tay Knowledge Base VNGGames

Thiết kế tham chiếu: `../specs/2026-08-06-knowledge-vng-handbook-design.md`

## Giai đoạn 1 — Hoàn tất kiểm chứng giao diện

1. Lập danh sách toàn bộ tuyên bố có nhãn `[TT]`, `[Test]`, cảnh báo, backlog và tên nút trong file v3.
2. Đối chiếu từng tuyên bố với giao diện Document và FAQ hiện tại.
3. Hoàn tất các phép thử còn thiếu: upload thư mục, Xuất/nhập lại, Lưu nháp, sửa MANUAL, phân tích lại trước/sau, mô hình Wiki, Graph Tổng hợp/So sánh và ảnh trong chat.
4. Ghi kết quả vào `audit/audit-knowledge-vng-2026-08-06.md`, gồm cả phần bị chặn.

## Giai đoạn 2 — Sửa nguồn chuẩn

1. Thay các kết luận sai bằng kết quả hiện tại.
2. Loại bỏ suy luận không có bằng chứng khỏi phần hướng dẫn chính.
3. Chuẩn hóa thuật ngữ Document, FAQ, RAG, Wiki, Graph, parser, chunk và index.
4. Sắp xếp lại thành luồng: hiểu khái niệm → chuẩn bị → tạo KB → cấu hình → vận hành → kiểm thử → bảo trì → phụ lục.
5. Cập nhật mục lục, anchor, lịch sử phiên bản và trạng thái xác thực.

## Giai đoạn 3 — Tạo ảnh và bộ Knowledge

1. Chụp/cắt các màn hình có giá trị hướng dẫn cao; che dữ liệu không cần thiết.
2. Tạo `knowledge-vng/assets/` và đặt tên ảnh ổn định theo module.
3. Tách 12 module đã định nghĩa trong thiết kế.
4. Thêm alt text, chú thích, ngày kiểm chứng và liên kết chéo cần thiết.
5. Kiểm thử gói MD + ảnh trên KB test và hỏi câu truy hồi để xác nhận ảnh.

## Giai đoạn 4 — Tạo bộ mẫu

1. Chuẩn hóa mẫu FAQ JSON, CSV và XLSX theo file mẫu từ tool.
2. Chuẩn hóa mẫu Document MD có heading, bảng, cảnh báo và ảnh.
3. Kiểm tra xem file Xuất FAQ có thể được tool đọc lại ở màn hình nhập.
4. Ghi hướng dẫn “Thêm vào” và “Thay toàn bộ”, kèm cảnh báo backup.

## Giai đoạn 5 — Dựng HTML offline

1. Thiết kế bố cục dành cho người mới và người vận hành.
2. Nhúng CSS, JavaScript, font hệ thống và ảnh trực tiếp trong một file.
3. Thêm tìm kiếm, điều hướng, callout, bảng chọn Document/FAQ và chế độ in.
4. Loại bỏ mọi URL tài nguyên ngoài; chỉ giữ liên kết tham khảo dưới dạng liên kết bấm chủ động.
5. Mở file bằng `file://`, kiểm tra desktop/mobile và console.

## Giai đoạn 6 — Kiểm tra cuối

1. Kiểm tra số file, heading cấp 1, encoding UTF-8, liên kết và asset.
2. So sánh các con số/cấu hình lặp lại giữa master, module và HTML.
3. Tìm các cụm từ lỗi thời hoặc mâu thuẫn đã biết.
4. Kiểm tra HTML không tải font/CSS/JS/ảnh từ Internet.
5. Rà lại toàn bộ yêu cầu ban đầu và lưu báo cáo nghiệm thu.

