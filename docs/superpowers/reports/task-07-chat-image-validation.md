# Task 07 — Kiểm thử chat và ảnh MinIO mới

Ngày kiểm thử: 07/08/2026  
KB: `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`)

## Trước khi gỡ 11 PNG khỏi KB sử dụng

Chat: `fa208715-1472-4a90-bb43-68216d9f8925`

| # | Câu hỏi | Kết quả trả lời | Ảnh render | URI trong đoạn nguồn |
|---|---|---|---|---|
| 1 | `Knowledge Base là gì? Hãy trả lời ngắn gọn và hiển thị kèm hình minh họa trang danh sách Knowledge Base.` | Trả lời đúng định nghĩa KB; nguồn có `00-gioi-thieu-va-quick-start.md` | PASS — alt `Trang danh sách Knowledge Base và nút tạo Knowledge Base mới` | `minio://knowledge-base-prd/10012/exports/78c9450c-2273-45fe-84b1-09f217328b53.png` |
| 2 | `Vì sao ảnh dùng đường dẫn tương đối assets/... không hiển thị trong chat Knowledge VNG? Hãy giải thích ngắn gọn và hiển thị hình minh họa lỗi này.` | Giải thích đúng đường dẫn tương đối không tạo ảnh trong câu trả lời; nguồn có `01-chuan-bi-noi-dung.md` | PASS — alt mô tả lỗi đường dẫn tương đối | `minio://knowledge-base-prd/10012/exports/227784d8-277b-4198-a8c5-77c3f49f7912.png` |
| 3 | `Trong kết nối Google Drive, cấu hình lọc tệp và gắn tag theo đường dẫn như thế nào? Hãy trả lời ngắn gọn và hiển thị kèm hình minh họa màn hình lọc tệp và tag.` | Trả lời đúng regex lọc file, tag mặc định và tag theo đường dẫn; nguồn có `12-ket-noi-google-drive.md` | PASS — alt `Regex lọc tệp và gắn tag` | `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png` |

Mỗi câu đều hiển thị `Hoàn tất 3 bước`. URI được xác minh bằng cách mở **Nguồn tham khảo**, mở đúng file Markdown, mở đoạn truy hồi và đọc trực tiếp Markdown nguồn; không suy diễn từ blob URL của thẻ ảnh.

## Sau khi gỡ 11 PNG khỏi KB sử dụng

Chat: `25bc7d2c-ac5b-455d-ab12-55af8135de63`

- Chạy lại câu Google Drive lọc tệp/tag.
- Câu trả lời đúng và ảnh có alt `Regex lọc tệp và gắn tag` vẫn render: **PASS**.
- **Nguồn tham khảo (7 tài liệu)** chỉ gồm các file `.md`; không có nguồn `.png`.
- Nguồn có cả `12-ket-noi-google-drive.md` và `08-chia-se-va-nguon-du-lieu.md`.
- Mở đoạn 1 của `12-ket-noi-google-drive.md` xác nhận trực tiếp URI `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png`.

## Kết luận gate

**PASS.** Ảnh trong chat được phục vụ qua URI MinIO nằm trong Markdown của consumer; 11 PNG độc lập không còn cần thiết trong `Knowledge VNG AI`. KB asset vẫn là dependency và không được xóa.

## Kiểm tra cuối sau khi sửa link sinh tự động

Chat: `2625ff6e-7e92-46d3-9fa4-eee81a1bf63c`.

- Chạy lại câu Google Drive filter/tag sau khi thay module 12 đã được builder rebase link.
- Câu trả lời đúng, `Hoàn tất 3 bước`, ảnh alt `Regex lọc tệp và gắn tag` render: **PASS**.
- 7 nguồn đều là `.md`; không có `.png`.
- Mở đoạn nguồn `12-ket-noi-google-drive.md` xác nhận cùng lúc:
  - URI ảnh `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png`;
  - link audit đã rebase thành `../audit/audit-google-drive-connector-2026-08-07.md`.
