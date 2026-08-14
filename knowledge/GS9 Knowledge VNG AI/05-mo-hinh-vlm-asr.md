<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 05 - Model, VLM và ASR {#05-mo-hinh-vlm-asr}

## Bạn sẽ biết gì sau khi đọc

- Vai trò của model chat, Embedding, Wiki, VLM và ASR.
- Những gì đang bị khóa hoặc chưa hoạt động đầy đủ.
- Cách chọn model mà không phụ thuộc vào danh sách nhất thời.

**Kiểm chứng giao diện: 06/08/2026.**

## Các vai trò model

- **Chat / tóm tắt:** tạo tóm tắt, câu trả lời và nội dung tổng hợp.
- **Embedding:** biến nội dung thành vector để tìm tương đồng; thay model có thể làm thay đổi toàn bộ không gian tìm kiếm.
- **Tổng hợp Wiki:** dùng cho quá trình tạo trang Wiki ở KB Tài liệu.
- **VLM:** đọc nội dung hình ảnh.
- **ASR:** chuyển âm thanh thành văn bản.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/03-cau-hinh-mo-hinh-vlm-asr.png -->
![Tab Mô hình với model chat, Embedding, Wiki, VLM và ASR](minio://knowledge-base-prd/10012/exports/0d708d7c-f524-45e1-aca3-ebc192e2a33f.png)

*Ảnh 05.1 - Tab Mô hình của KB Tài liệu; cấu hình trong ảnh là trạng thái của KB test, không phải mặc định sản phẩm.*

## Trạng thái đã quan sát

Trong KB Tài liệu, dropdown chat tại thời điểm kiểm tra có:

- `gpt-oss-120b`
- `hosted_vllm/qwen3.6-35b`
- `qwen3.6-plus`

Trong FAQ, UI từng hiển thị thêm `deepseek-v4-flash`, nhưng backend từ chối lưu với lỗi `LLM model not found`. Đây là mâu thuẫn UI/backend và là lý do không coi “có trong dropdown” đồng nghĩa “dùng được”.

## Embedding

Khi KB đã có nội dung, model Embedding hiển thị khóa. Điều này hợp lý về vận hành vì đổi embedding cần lập chỉ mục lại toàn bộ nội dung. Hãy chốt model bằng KB test trước khi nạp dữ liệu lớn.

## VLM

Trong KB Tài liệu test, VLM đang bật và dùng `hosted_vllm/qwen3.6-35b`. Trạng thái này chỉ chứng minh cấu hình hiện hữu. Không suy ra VLM mặc định bật cho KB mới.

VLM đã xử lý được ảnh giao diện và tạo tóm tắt, nhưng OCR có thể đọc sai tên thương hiệu hoặc chữ nhỏ. Ảnh phải đi kèm caption văn bản; đừng để một quy trình quan trọng chỉ tồn tại trong ảnh.

## ASR

Khi bật toggle ASR, giao diện hiện thêm **Mô hình ASR** và **Ngôn ngữ**. Dropdown model quan sát được đang rỗng. Dòng cảnh báo cũ “Chưa có model - liên hệ admin” không còn xuất hiện trong giao diện hiện tại.

Kết luận đúng là: **chưa chọn được model ASR trong môi trường đã kiểm thử**. Không khẳng định toàn bộ sản phẩm không hỗ trợ ASR ở mọi môi trường.

## Cách chọn và ghi nhận model

1. Mở dropdown trong chính loại KB cần dùng.
2. Chọn model, bấm **Lưu** và xác nhận không có toast lỗi.
3. Mở lại tab để xem model có được giữ không.
4. Chạy cùng một bộ câu hỏi và ghi độ đúng, nguồn truy hồi, độ trễ.
5. Ghi tên model kèm ngày kiểm thử trong hồ sơ vận hành, không hard-code vào hướng dẫn dài hạn.

## Khi model lỗi

- Nếu UI cho chọn nhưng lưu lỗi, đổi sang model đã lưu được và ghi bằng chứng UI/backend.
- Nếu câu trả lời kém nhưng nguồn truy hồi đúng, kiểm tra model chat và prompt.
- Nếu nguồn truy hồi sai, ưu tiên kiểm tra embedding, dữ liệu và chunking trước khi đổi model chat.
