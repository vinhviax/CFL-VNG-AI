<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 10 - Vận hành FAQ {#10-van-hanh-faq}

## Bạn sẽ biết gì sau khi đọc

- Cách thêm, kiểm tra, nhập và xuất FAQ.
- Cách dùng ngưỡng tìm kiếm.
- Quy trình backup trước thao tác thay toàn bộ.

**Kiểm chứng giao diện: 06/08/2026.**

## Thanh công cụ FAQ

Trang Documents của FAQ đã kiểm tra có:

- **Chọn tất cả**
- **Kiểm tra tìm kiếm**
- **Xuất**
- **Nhập**
- **Thêm Q&A**

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/11-faq-danh-sach-nhap-xuat-tim-kiem.png -->
![Danh sách FAQ với các nút kiểm tra tìm kiếm, xuất, nhập và thêm Q&A](minio://knowledge-base-prd/10012/exports/1d61af93-8434-4a18-8eba-c0500d685f73.png)

*Ảnh 10.1 - Trang vận hành FAQ tập trung vào từng mục Q&A và chất lượng tìm kiếm.*

## Thêm Q&A bằng tay

1. Bấm **Thêm Q&A**.
2. Viết câu hỏi chuẩn rõ ý định.
3. Thêm biến thể từ ticket thật.
4. Thêm câu loại trừ nếu có ý định gần giống.
5. Viết câu trả lời và phạm vi áp dụng.
6. Gán phân loại.
7. Lưu và chạy **Kiểm tra tìm kiếm** ngay.

## Kiểm tra tìm kiếm

Modal quan sát được có:

- Ngưỡng từ **0 đến 1**, bước **0,1**, giá trị mở ra là **0,5**.
- Số kết quả tối đa từ **1 đến 50**, giá trị mở ra là **10**.

Câu đối chứng “Server bảo trì lúc nào?” ở ngưỡng 0 trả về mục chính xác với điểm 1,000. Từ khóa chỉ nằm trong câu trả lời không trả kết quả ở chế độ Chỉ câu hỏi, kể cả ngưỡng 0.

Không đặt ngưỡng chỉ từ một câu hỏi. Thu thập:

- câu đúng nguyên văn;
- câu diễn đạt lại;
- câu gần giống nhưng phải loại trừ;
- câu ngoài phạm vi;
- câu có mã lỗi hoặc tên riêng.

Chọn ngưỡng cân bằng bỏ sót và kéo nhầm theo rủi ro nghiệp vụ.

## Xuất FAQ

Nút **Xuất** đã tạo file CSV gồm 5 dòng Q&A. Header file xuất dùng tiếng Anh và một số trường nhiều giá trị nối bằng `##`.

Chính file CSV xuất đó được chọn lại trong modal **Nhập**; hệ thống đọc đủ 5 mục và bật nút Nhập. Phép thử dừng ở preview để tránh tạo trùng.

Kết luận: **Xuất** là bước backup thực dụng trước khi nhập thay toàn bộ, dù header của file xuất khác header tiếng Việt trong CSV mẫu.

## Nhập và file mẫu

Menu tải file mẫu có **JSON, CSV, Excel**. Bộ mẫu dự án nằm trong `samples/faq/` và được chuẩn hóa từ template của tool.

Trước khi nhập:

1. Xuất backup hiện tại.
2. Kiểm tra số mục trong file nguồn.
3. Xác nhận cách xử lý câu hỏi tương tự, loại trừ và nhiều câu trả lời.
4. Dùng chế độ thêm vào nếu đang thử.
5. Chỉ dùng **Thay toàn bộ** trong KB test hoặc khi đã có kế hoạch phục hồi.

## Sau nhập

- Đối chiếu số mục.
- Mở ngẫu nhiên ít nhất 5 mục.
- Kiểm tra ký tự tiếng Việt, xuống dòng và dấu phân cách `##`.
- Chạy bộ câu hỏi hồi quy ở cùng cấu hình index và ngưỡng.
- Lưu file nguồn cùng ngày nhập và người thực hiện.
