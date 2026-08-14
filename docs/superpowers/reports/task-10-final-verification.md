# Task 10 — Verification cuối và bàn giao

Ngày: 07/08/2026

## Local gate

- Strict build: `Build complete`; 13 module, 65.865 byte; HTML offline 14.504.975 byte.
- Full suite: `Ran 11 tests`; `OK`; 0 failure, 0 error.
- Invariant: 25 PNG local đúng signature, 25 URI `.png` duy nhất, 36 link MinIO, 36 `LOCAL_ASSET`, 0 link ảnh local hoạt động.
- Module 12 dùng `../audit/audit-google-drive-connector-2026-08-07.md`; target tồn tại.

## TDD cho lỗi link sinh tự động

Reviewer vòng một phát hiện link `audit/...` đúng trong master nhưng hỏng khi module được đặt trong `knowledge-vng/`. Regression test `test_write_modules_rebases_master_relative_document_links` được tạo và quan sát thất bại trước khi sửa. Builder sau đó rebase liên kết local từ source root sang output directory; test riêng và full suite đều PASS.

Module 12 live được thay lại để khớp artifact cuối:

- ID cũ đã xóa: `748baf80-3d87-427b-acbf-9de20f8461e8`.
- ID hiện hành: `e58fb441-74cc-44cf-83a9-972954fa697c`, trạng thái **Hoàn tất**.
- Audit: `audit/consumer-markdown-link-fix-2026-08-07.json`.

## Live gate

| Đối tượng | Kết quả cuối |
|---|---|
| `Knowledge VNG - Image Assets` | 25 PNG, 0 MD; 25/25 **Hoàn tất** |
| `Knowledge VNG AI` | 13 MD, 0 PNG; 13/13 **Hoàn tất**, 13 tên duy nhất |
| Chat cuối | `2625ff6e-7e92-46d3-9fa4-eee81a1bf63c`; câu Drive filter/tag đúng, ảnh render, `Hoàn tất 3 bước` |
| Nguồn chat | 7/7 là `.md`; nguồn module 12 chứa đúng URI ảnh 18 và link `../audit/...` |

## Review độc lập

Review vòng một tìm thấy đúng một lỗi link tương đối. Sau sửa và đồng bộ live, review vòng hai kết luận **APPROVED**:

- không còn link nội bộ hoạt động bị hỏng;
- current ID và các audit nhất quán;
- invariant 25 asset/map, 13 module, 36 MinIO và 36 `LOCAL_ASSET` đạt;
- baseline cuối là 11 test; số 10/10 chỉ còn trong report lịch sử Task 05.

## Kết luận

**PASS.** Tất cả task trong plan đã hoàn tất; không còn bước bắt buộc cho migration ảnh. Asset KB phải được giữ lâu dài khi Markdown còn tham chiếu URI.
