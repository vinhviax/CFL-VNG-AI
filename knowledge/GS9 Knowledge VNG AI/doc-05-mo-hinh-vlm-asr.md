<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 05 - Model, VLM và ASR {#05-mo-hinh-vlm-asr}

Đọc xong bạn biết mỗi vai trò model dùng để làm gì, chọn model ở đâu, cái nào đổi được sau và cái nào phải chốt trước khi nạp dữ liệu.

## Các vai trò model

Mở **Cài đặt → Mô hình** của Knowledge Base. Ở đây có các vai trò:

| Vai trò | Dùng để làm gì |
|---|---|
| **Chat / tóm tắt** | Tạo tóm tắt, câu trả lời và nội dung tổng hợp |
| **Embedding** | Biến nội dung thành vector để tìm tương đồng |
| **Tổng hợp Wiki** | Sinh trang Wiki, chỉ có ở KB Tài liệu |
| **VLM** | Đọc nội dung hình ảnh |
| **ASR** | Chuyển âm thanh thành văn bản |

VLM và ASR nằm trong khối **Tùy chọn mô hình nâng cao**, bấm mở rộng ở phía dưới ba dropdown chính. Khối này không có ở KB FAQ.

<!-- LOCAL_ASSET: ./image-03-cau-hinh-mo-hinh-vlm-asr.png -->
![Tab Mô hình với model chat, Embedding, Wiki, VLM và ASR](minio://knowledge-base-prd/10012/9856f987-df97-4434-8f31-99b462ba0f51/23f448df-8ba0-4ac2-a0cc-b88fddbc6b96.png)

*Ảnh 05.1 - Tab Mô hình của KB Tài liệu.*

## Cái gì đổi được, cái gì không

| Thiết lập | Khi KB đã có nội dung |
|---|---|
| Model chat / tóm tắt | Đổi được bất cứ lúc nào |
| Model tổng hợp Wiki | Đổi được |
| **Model Embedding** | **Bị khóa** |

Embedding bị khóa vì đổi embedding là đổi toàn bộ không gian tìm kiếm, buộc phải lập chỉ mục lại mọi nội dung. Banner khóa gợi ý xóa hết tài liệu để mở lại — nghĩa là khóa có điều kiện, nhưng đừng trông chờ vào đường này.

**Hãy chốt Embedding trên một KB test trước khi nạp dữ liệu lớn.**

## Chọn model an toàn

1. Mở dropdown trong chính loại KB cần dùng — pool model của mỗi vai trò không giống nhau.
2. Chọn model, bấm **Lưu** và xác nhận không có toast lỗi.
3. Mở lại tab để kiểm tra model có thực sự được giữ không.
4. Chạy cùng một bộ câu hỏi và ghi độ đúng, nguồn truy hồi, độ trễ.

**Có model hiện trong dropdown nhưng lưu không được.** Đã gặp trường hợp chọn được model trong giao diện nhưng khi lưu báo lỗi `LLM model not found`, phải đổi sang model khác. Vì vậy đừng coi "có trong dropdown" là "dùng được" — chỉ tin model đã lưu thành công trong chính KB đó.

**Danh sách model thay đổi theo môi trường và theo thời điểm.** Số model trong dropdown có thể dao động giữa các lần mở. Nếu không thấy model bạn cần, tải lại trang hoặc mở lại cửa sổ cấu hình trước khi báo lỗi.

## VLM - đọc nội dung hình ảnh

Xử lý ảnh trong tài liệu **không tự động**. Bạn phải bật đa phương thức và chọn **Mô hình VLM**.

Pool model VLM hẹp hơn pool chat: một số model dùng được cho vai trò Chat / tóm tắt nhưng không xuất hiện trong dropdown VLM. Nếu không thấy model quen thuộc ở đây, đó là chuyện bình thường, hãy chọn model khác đang có.

VLM đọc được ảnh giao diện và sinh tóm tắt, nhưng **OCR có thể đọc sai tên thương hiệu hoặc chữ nhỏ**. Vì vậy:

- Mọi ảnh phải đi kèm caption bằng văn bản.
- Không để một quy trình quan trọng chỉ tồn tại trong ảnh.

## ASR - chuyển âm thanh thành văn bản

Bật toggle ASR sẽ hiện thêm hai trường: **Mô hình ASR** và **Ngôn ngữ**.

Dropdown **Mô hình ASR** có thể rỗng. Khi rỗng thì bạn chưa chọn được model, và tính năng ASR chưa dùng được trong môi trường đó. Hãy mở dropdown kiểm tra **trước** khi lên kế hoạch nạp nội dung âm thanh.

## Khi kết quả kém

| Triệu chứng | Kiểm tra theo thứ tự |
|---|---|
| UI cho chọn nhưng lưu lỗi | Đổi sang model khác đã lưu được |
| Câu trả lời kém nhưng nguồn truy hồi đúng | Model chat và prompt |
| Nguồn truy hồi sai | Embedding, chất lượng dữ liệu và phân đoạn — trước khi đổi model chat |
