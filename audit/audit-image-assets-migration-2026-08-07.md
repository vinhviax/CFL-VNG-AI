# Audit migration ảnh — Knowledge VNG

**Ngày thực hiện:** 07/08/2026  
**Tenant:** `10012`  
**Asset KB:** `Knowledge VNG - Image Assets` — `6da8657c-dd96-4170-a698-074043475014`  
**Consumer KB:** `Knowledge VNG AI` — `cefadf09-4187-46ac-a765-591e3255a4a4`  
**Phân loại:** Đã kiểm chứng trên live ngày 07/08/2026  
**Bảo mật:** Audit không chứa service-account JSON, private key, token hoặc credential.

## Mục tiêu và baseline

Mục tiêu là chuyển quyền sở hữu 25 ảnh sang một KB asset chuyên dụng, cấp lại toàn bộ URI MinIO, thay 13 Markdown trong consumer và dọn 11 PNG tạm khỏi consumer mà không làm gián đoạn ảnh chat.

Baseline trước mutation:

- Asset KB: 0 tài liệu.
- Consumer: 24 tài liệu = 13 Markdown + 11 PNG Google Drive.
- 14 ảnh nền còn lại từng phụ thuộc vào KB `Test Doc RAG+Wiki`; KB đó đã bị người dùng xóa và không còn là dependency hợp lệ.
- Snapshot map trước migration: [image-map-before-assets-migration-2026-08-07.json](image-map-before-assets-migration-2026-08-07.json).

## Sửa lỗi định dạng ảnh nguồn

Ảnh 01–14 mang đuôi `.png` nhưng payload thực tế là JPEG. Đã thực hiện:

1. backup nguyên byte vào [image-assets-original-jpeg-mislabeled-2026-08-07](image-assets-original-jpeg-mislabeled-2026-08-07/);
2. transcode thành PNG thật, giữ tên và kích thước pixel;
3. kiểm tra magic bytes `89 50 4E 47 0D 0A 1A 0A`;
4. upload bản đúng, xác nhận **Hoàn tất**, rồi xóa từng bản sai định dạng theo ID.

Danh sách ID hiện hành: [image-assets-knowledge-ids-2026-08-07.json](image-assets-knowledge-ids-2026-08-07.json). Danh sách bản đã thay: [image-assets-replaced-knowledge-ids-2026-08-07.json](image-assets-replaced-knowledge-ids-2026-08-07.json).

## Mapping 25 ảnh hiện hành

| # | Filename | URI MinIO của asset KB |
|---:|---|---|
| 01 | `01-tong-quan-danh-sach-knowledge.png` | `minio://knowledge-base-prd/10012/exports/78c9450c-2273-45fe-84b1-09f217328b53.png` |
| 02 | `02-cau-hinh-tong-quan-document.png` | `minio://knowledge-base-prd/10012/exports/2413cc24-8243-48d9-8b54-d24dfd0a6ecb.png` |
| 03 | `03-cau-hinh-mo-hinh-vlm-asr.png` | `minio://knowledge-base-prd/10012/exports/0d708d7c-f524-45e1-aca3-ebc192e2a33f.png` |
| 04 | `04-xu-ly-parser-theo-dinh-dang.png` | `minio://knowledge-base-prd/10012/exports/0bdef2c5-bca0-4a1c-9171-271ec43687cc.png` |
| 05 | `05-xu-ly-phan-doan-cha-con.png` | `minio://knowledge-base-prd/10012/exports/fe6f61d9-fbdb-4ec8-b39e-e8ca2c28cbc5.png` |
| 06 | `06-chia-se-va-phan-quyen.png` | `minio://knowledge-base-prd/10012/exports/e61e4fcc-6d62-48b0-b572-a1d85f6f90cf.png` |
| 07 | `07-nguon-du-lieu-notion-drive-nas.png` | `minio://knowledge-base-prd/10012/exports/0666adc3-8abe-422b-94ae-ef52020a956c.png` |
| 08 | `08-tai-tep-thu-muc-va-soan-thao.png` | `minio://knowledge-base-prd/10012/exports/633bc6ad-b471-4590-979c-1b637d086052.png` |
| 09 | `09-wiki-muc-luc-va-trang.png` | `minio://knowledge-base-prd/10012/exports/011f18dc-0a2b-4e6a-aba3-96242f155127.png` |
| 10 | `10-graph-cac-loai-node.png` | `minio://knowledge-base-prd/10012/exports/8ee2eedb-6160-4511-9448-b38251f438f0.png` |
| 11 | `11-faq-danh-sach-nhap-xuat-tim-kiem.png` | `minio://knowledge-base-prd/10012/exports/1d61af93-8434-4a18-8eba-c0500d685f73.png` |
| 12 | `12-faq-bieu-mau-them-qa.png` | `minio://knowledge-base-prd/10012/exports/7a78554f-daa5-49a8-86f8-d16436ca3a1f.png` |
| 13 | `13-chat-hien-thi-anh-minio.png` | `minio://knowledge-base-prd/10012/exports/4d21ed4e-4907-4f09-a8c5-1399f499ee03.png` |
| 14 | `14-chat-khong-hien-thi-duong-dan-tuong-doi.png` | `minio://knowledge-base-prd/10012/exports/227784d8-277b-4198-a8c5-77c3f49f7912.png` |
| 15 | `15-google-drive-xac-thuc-service-account.png` | `minio://knowledge-base-prd/10012/exports/ec4b9360-ad0d-4764-b20f-83651394aca4.png` |
| 16 | `16-google-drive-chon-tai-nguyen.png` | `minio://knowledge-base-prd/10012/exports/45102d91-6bba-4f63-baa0-a6f5e3532ded.png` |
| 17 | `17-google-drive-lich-va-cach-dong-bo.png` | `minio://knowledge-base-prd/10012/exports/e8c84875-4614-4da9-bc8b-30e75ce5276b.png` |
| 18 | `18-google-drive-loc-tep-va-tag.png` | `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png` |
| 19 | `19-google-drive-ghi-de-xu-ly.png` | `minio://knowledge-base-prd/10012/exports/ed516990-0d0b-44fc-b767-691c1f3abd85.png` |
| 20 | `20-google-drive-da-phuong-thuc-va-parser.png` | `minio://knowledge-base-prd/10012/exports/712f2d4c-730d-45b5-a5b7-fb8dd0aed4c0.png` |
| 21 | `21-google-drive-parser-office-text.png` | `minio://knowledge-base-prd/10012/exports/e6ebb4ad-5657-4e68-bd4a-09ab8d2e1dd2.png` |
| 22 | `22-google-drive-parser-media-web.png` | `minio://knowledge-base-prd/10012/exports/168abd45-3e25-4ef7-b182-55e458037cdb.png` |
| 23 | `23-google-drive-dong-bo-xoa.png` | `minio://knowledge-base-prd/10012/exports/88efc5bd-c974-4c0b-9bf7-35c65739f348.png` |
| 24 | `24-google-drive-parser-excel-tuy-chinh.png` | `minio://knowledge-base-prd/10012/exports/275a026c-5970-45de-bc5d-3c0a4dc9164c.png` |
| 25 | `25-google-drive-dong-bo-thanh-cong.png` | `minio://knowledge-base-prd/10012/exports/947d9103-edd6-4dfa-b5a5-295bcae2c66f.png` |

## Build và 13 lần thay Markdown

- Strict build sinh 13 module và HTML offline v3.1.1; 36 link MinIO, 36 `LOCAL_ASSET`, không có link ảnh local hoạt động.
- ID trước/sau replacement nằm tại [consumer-markdown-old-knowledge-ids-2026-08-07.json](consumer-markdown-old-knowledge-ids-2026-08-07.json) và [consumer-markdown-new-knowledge-ids-2026-08-07.json](consumer-markdown-new-knowledge-ids-2026-08-07.json).
- Mỗi bản cũ chỉ bị xóa sau khi bản mới cùng tên đã **Hoàn tất** và được kiểm tra.
- File `11-chat-kiem-thu-va-bao-tri.md` cần override parser một file sang **Simple** sau hai lượt **Built-in** kẹt hậu xử lý. Bản hiện hành là `58567b75-a702-4f59-b13a-704c019b33c5`; xem [consumer-markdown-retry-2026-08-07.json](consumer-markdown-retry-2026-08-07.json).
- Review cuối phát hiện link audit tương đối sai trong module 12. Builder được sửa bằng regression test, module 12 hiện hành là `e58fb441-74cc-44cf-83a9-972954fa697c`; xem [consumer-markdown-link-fix-2026-08-07.json](consumer-markdown-link-fix-2026-08-07.json).

## Kiểm thử chat

Chat trước cleanup: `fa208715-1472-4a90-bb43-68216d9f8925`.

| Nhóm | Kết quả | URI được mở trực tiếp trong nguồn Markdown |
|---|---|---|
| Trang danh sách KB / ảnh 01 | PASS | `minio://knowledge-base-prd/10012/exports/78c9450c-2273-45fe-84b1-09f217328b53.png` |
| Lỗi đường dẫn tương đối / ảnh 14 | PASS | `minio://knowledge-base-prd/10012/exports/227784d8-277b-4198-a8c5-77c3f49f7912.png` |
| Drive filter/tag / ảnh 18 | PASS | `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png` |

Sau khi dọn PNG, chat `25bc7d2c-ac5b-455d-ab12-55af8135de63` chạy lại ảnh 18: câu trả lời và ảnh render; 7 nguồn đều là `.md`; đoạn 1 của `12-ket-noi-google-drive.md` chứa đúng URI ảnh 18. Xem [báo cáo Task 07](../docs/superpowers/reports/task-07-chat-image-validation.md).

Sau khi sửa link sinh tự động và thay lại module 12, chat cuối `2625ff6e-7e92-46d3-9fa4-eee81a1bf63c` tiếp tục PASS; đoạn nguồn chứa cả URI ảnh 18 và link audit đã rebase `../audit/...`.

## Cleanup consumer và inventory cuối

11 PNG 15–25 được xóa từng tài liệu theo ID tại [consumer-png-deleted-knowledge-ids-2026-08-07.json](consumer-png-deleted-knowledge-ids-2026-08-07.json), chỉ sau khi ba gate chat trước cleanup đạt.

| KB | Inventory cuối đã kiểm chứng |
|---|---|
| `Knowledge VNG - Image Assets` | 25 PNG, 0 MD; 25/25 **Hoàn tất** |
| `Knowledge VNG AI` | 13 MD, 0 PNG; 13/13 **Hoàn tất** |

Snapshot máy đọc: [final-live-inventory-2026-08-07.json](final-live-inventory-2026-08-07.json).

## Kết luận

**Đạt.** Kiến trúc hai KB đã được triển khai theo đúng thứ tự an toàn. Asset KB là dependency lâu dài và không được xóa khi Markdown còn tham chiếu URI. Consumer chỉ giữ 13 Markdown; 11 PNG đã dọn có thể phục hồi từ 25 asset local hoặc asset KB nếu cần điều tra lịch sử.
