# Quy ước viết file trong `docs KB/Dev`

Tài liệu này quy định cách viết mọi file trong thư mục `docs KB/Dev`. Đọc trước khi thêm hoặc sửa file ở đây.

## Đối tượng đọc

Dev và Agent config — người cần **sửa hệ thống**, không phải người dùng cuối. Họ hỏi: *"nó chạy thế nào, tôi sửa được không, sửa rồi có gãy gì không?"*

Bản rút gọn cho người dùng cuối nằm ở `docs KB/Human`, và được chắt lọc **từ** thư mục này.

## Đặt tên file

`<TínhNăng>-<chu-de>.md` — tiền tố cho biết file thuộc tính năng nào của nền tảng VNG AI.

Tiền tố đang dùng: `KB-` (Knowledge Base) · `Agent-` (Agent). Thêm tính năng mới thì thêm tiền tố mới, không tạo thư mục con.

## Nội dung bắt buộc có

- **Cơ chế thật**: hệ thống làm gì bên trong, không chỉ mô tả nút bấm.
- **Trạng thái kiểm chứng**: cái gì đã kiểm chứng, ngày nào, bằng cách nào; cái gì **chưa** kiểm chứng phải nói thẳng.
- **Mã quyết định** `DEC-xxx` khi có, để tra ngược `DECISIONS.md`.
- **Đường dẫn tới bằng chứng** trong `audit/` khi có.
- **Cạm bẫy đã gặp thật** — lỗi từng xảy ra và cách nhận biết.

## Nguyên tắc

1. **Không bịa.** Không có bằng chứng thì ghi "chưa kiểm chứng", không suy đoán thành sự thật.
2. **Phân biệt rõ ba mức** (DEC-007): *Đã kiểm chứng* — có bằng chứng trực tiếp · *Có điều kiện* — đúng trong phạm vi hẹp đã thử · *Chưa xác định* — chưa ai thử.
3. **Ghi ngày** cho mọi khẳng định về hành vi nền tảng — nền tảng đổi được, tài liệu phải cho biết mình cũ đến đâu.
4. **Cấu hình UI không bằng hành vi runtime** (DEC-022). Đọc được thiết lập trên màn hình không có nghĩa đã biết nó chạy ra sao.
5. Một file một chủ đề. Dài quá thì tách, đừng gom.
