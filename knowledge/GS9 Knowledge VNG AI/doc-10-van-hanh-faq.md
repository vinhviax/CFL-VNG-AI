<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 10 - Vận hành FAQ {#10-van-hanh-faq}

Đọc xong bạn biết cách thêm và sửa từng mục Q&A, cách dùng công cụ Kiểm tra tìm kiếm để chỉnh ngưỡng, và cách nhập file mà không mất dữ liệu đang có.

## Bạn sẽ biết gì sau khi đọc

- Cách thêm, kiểm tra, nhập và xuất FAQ.
- Cách dùng ngưỡng tìm kiếm.
- Quy trình backup trước thao tác thay toàn bộ.

## Thanh công cụ FAQ

Trang Documents của KB FAQ có:

- **Chọn tất cả**
- **Kiểm tra tìm kiếm**
- **Xuất**
- **Nhập**
- **Thêm Q&A**

<!-- LOCAL_ASSET: ./image-11-faq-danh-sach-nhap-xuat-tim-kiem.png -->
![Danh sách FAQ với các nút kiểm tra tìm kiếm, xuất, nhập và thêm Q&A](minio://knowledge-base-prd/10012/d6ed46f4-2f75-4146-878d-3cf72e3de6bd/308f357b-bdef-42f9-b55c-37f70b628814.png)

*Ảnh 10.1 - Trang vận hành FAQ tập trung vào từng mục Q&A và chất lượng tìm kiếm.*

## Thêm Q&A bằng tay

1. Bấm **Thêm Q&A**.
2. Viết câu hỏi chuẩn rõ ý định.
3. Thêm biến thể lấy từ ticket thật của người dùng.
4. Thêm câu loại trừ nếu có ý định khác nhưng nghe gần giống.
5. Viết câu trả lời và nói rõ phạm vi áp dụng.
6. Gán phân loại.
7. Lưu và chạy **Kiểm tra tìm kiếm** ngay.

## Kiểm tra tìm kiếm

Modal **Kiểm tra tìm kiếm** có hai tham số:

| Tham số | Khoảng giá trị | Giá trị khi mở |
|---|---|---|
| Ngưỡng tương đồng | 0 đến 1, bước 0,1 | 0,5 |
| Số kết quả tối đa | 1 đến 50 | 10 |

Hai điều cần nhớ khi đọc kết quả:

- Ngưỡng mặc định 0,5 có thể che mất một mục khớp yếu nhưng vẫn đúng. Khi FAQ báo không tìm thấy gì, hạ ngưỡng về 0 để biết là không có mục nào gần đúng, hay có mà bị ngưỡng lọc.
- Ở chế độ index **Chỉ câu hỏi**, từ khóa chỉ nằm trong phần câu trả lời sẽ không ra kết quả, kể cả khi hạ ngưỡng về 0. Đây là khác biệt phạm vi index, không phải điểm số thấp.

Đừng chọn ngưỡng chỉ dựa vào một câu hỏi. Thu thập đủ các nhóm:

- câu đúng nguyên văn;
- câu diễn đạt lại;
- câu gần giống nhưng phải loại trừ;
- câu ngoài phạm vi;
- câu có mã lỗi hoặc tên riêng.

Chọn ngưỡng cân bằng giữa bỏ sót và kéo nhầm, theo mức rủi ro của nghiệp vụ.

## Xuất FAQ

Nút **Xuất** tạo file CSV chứa toàn bộ mục Q&A đang có.

Lưu ý về file xuất:

- Header dùng tiếng Anh, khác header tiếng Việt trong file CSV mẫu.
- Trường có nhiều giá trị được nối bằng `##`.
- File xuất này nhập ngược lại được: chọn nó trong modal **Nhập**, hệ thống đọc đủ số mục và bật nút Nhập.

Vì vậy **Xuất là bước backup thực dụng** trước mọi thao tác nhập.

## Nhập và file mẫu

Menu tải file mẫu có **JSON, CSV, Excel**.

**Thay toàn bộ là thao tác phá hủy dữ liệu.** Popup xác nhận ghi rõ *"Không thể hoàn tác."* Sau khi chạy, các mục cũ biến mất hoàn toàn và không có bước khôi phục trong giao diện.

Trước khi nhập:

1. Xuất backup hiện tại.
2. Kiểm tra số mục trong file nguồn.
3. Xác nhận cách xử lý câu hỏi tương tự, câu loại trừ và trường hợp nhiều câu trả lời.
4. Dùng chế độ **Thêm vào** khi còn đang thử.
5. Chỉ dùng **Thay toàn bộ** trong KB test, hoặc khi đã có kế hoạch phục hồi.

## Sau khi nhập

- Đối chiếu số mục với file nguồn.
- Mở ngẫu nhiên ít nhất 5 mục.
- Kiểm tra ký tự tiếng Việt, dấu xuống dòng và dấu phân cách `##`.
- Chạy bộ câu hỏi hồi quy ở đúng cấu hình index và ngưỡng như trước.
- Lưu file nguồn kèm ngày nhập và tên người thực hiện.
