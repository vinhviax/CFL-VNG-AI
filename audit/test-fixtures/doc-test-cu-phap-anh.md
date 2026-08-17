# Thí nghiệm cú pháp nhúng ảnh

> **Đây là file THÍ NGHIỆM, không phải nội dung nghiệp vụ.** Mục đích: tìm cú pháp nhúng ảnh cho ra ĐÚNG MỘT ảnh trong chat. Xóa sau khi có kết quả.
> Ngày: 15/08/2026 · Tất cả 5 biến thể trỏ về CÙNG MỘT ảnh: `image-17-hoat-dong-chu-de-halloween.jpg`

Cách dùng: upload file này vào một KB đang có, chờ `Hoàn tất`, rồi chat hỏi **từng mục một** theo mã A–E. Ghi lại mục nào ra đúng một ảnh.

Câu hỏi mẫu: *"Cho tôi xem hình ở mục Biến thể A"*, rồi lặp lại với B, C, D, E.

---

## Biến thể A — markdown có chú thích

Đây là cách đang dùng trong toàn bộ dự án. Nghi ngờ đang bị nhân đôi.

![Hoạt động chủ đề Halloween](minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg)

---

## Biến thể B — markdown chú thích rỗng

![](minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg)

---

## Biến thể C — URI để trần trên một dòng

Không bọc cú pháp markdown nào. Đây là biến thể được dự đoán đúng.

minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg

---

## Biến thể D — URI ở cả hai vị trí

Định dạng cũ, trước đây được cho là chỉ ra một ảnh.

![minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg](minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg)

---

## Biến thể E — thẻ HTML

<img src="minio://knowledge-base-prd/10012/exports/37db9a9c-662d-484f-82aa-51a0e51362b7.jpg" alt="Hoạt động chủ đề Halloween">

---

## Bảng ghi kết quả

Điền vào sau khi chat xong từng mục:

| Mã | Số ảnh hiện ra | Có mảnh cú pháp thừa không | Kết luận |
|---|---|---|---|
| A |  |  |  |
| B |  |  |  |
| C |  |  |  |
| D |  |  |  |
| E |  |  |  |

Biến thể đạt: ra **đúng 1 ảnh** và **không có mảnh cú pháp thừa** như `![`, `](`, `)`.
