# Google Drive Connector Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bổ sung bằng chứng, hướng dẫn và trạng thái kiểm chứng Google Drive connector ngày 07/08/2026 mà không lưu secret hoặc phá vỡ pipeline phát hành.

**Architecture:** Ảnh gốc được lưu ở lớp audit; hướng dẫn human dùng ảnh local; nội dung nghiệp vụ được sửa ở master rồi builder sinh lại 13 module và HTML. Module Google Drive được tạo ngay với ảnh local; bản nạp chỉ đạt trạng thái chat-ready sau khi có đủ mapping MinIO.

**Tech Stack:** Markdown, PNG, Python builder, Python `unittest`, PowerShell.

## Global Constraints

- Master `so-tay-tao-knowledge-base-v3.md` là nguồn nội dung chuẩn duy nhất.
- Không sửa trực tiếp `knowledge-vng/*.md` hoặc `so-tay-tao-knowledge-base.html`.
- Không lưu service-account JSON, private key hoặc credential khác.
- Mọi khẳng định live mới phải có ngày, evidence và mức chắc chắn.
- Workspace không phải Git repository; không có bước commit.

---

### Task 1: Lưu evidence và viết audit Google Drive

**Files:**
- Create: `audit/evidence/2026-08-07-google-drive-*.png`
- Create: `audit/audit-google-drive-connector-2026-08-07.md`

**Interfaces:**
- Consumes: ảnh PNG người dùng cung cấp trong thư mục Temp.
- Produces: bộ evidence có tên ổn định và audit làm nguồn cho master/status/handoff.

- [x] **Step 1:** Sao chép từng PNG vào `audit/evidence/` bằng tên mô tả, không chỉnh sửa nội dung ảnh.
- [x] **Step 2:** Kiểm tra file tồn tại, kích thước lớn hơn 0 và không có ảnh chụp nội dung private key.
- [x] **Step 3:** Viết audit gồm môi trường, chuỗi thao tác, kết quả thành công, bảng control bước 4 và backlog P4.
- [x] **Step 4:** Kiểm tra toàn bộ link ảnh audit bằng `Test-Path`.

### Task 2: Viết hướng dẫn human và cập nhật master

**Files:**
- Create: `docs human/huong-dan-ket-noi-google-drive-knowledge-vng.md`
- Modify: `so-tay-tao-knowledge-base-v3.md`

**Interfaces:**
- Consumes: audit ngày 07/08/2026 và evidence Task 1.
- Produces: hướng dẫn có ảnh cho người đọc và nội dung module 08 sẵn build.

- [x] **Step 1:** Viết hướng dẫn từ chuẩn bị Google Cloud đến kiểm tra trạng thái `Thành công`.
- [x] **Step 2:** Mô tả cấu hình khuyến nghị, cảnh báo `keys`, parser tenant-specific và đồng bộ xóa.
- [x] **Step 3:** Nâng phiên bản master lên `3.1.0`, ngày `07/08/2026`, cập nhật nguồn audit.
- [x] **Step 4:** Thay mục Google Drive bị chặn bằng kết quả bước 3–4 đã kiểm chứng và backlog P4 còn mở.
- [x] **Step 5:** Cập nhật ma trận kiểm chứng cuối master.

### Task 3: Cập nhật trạng thái dự án

**Files:**
- Modify: `AGENTS.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`

**Interfaces:**
- Consumes: master và audit đã cập nhật.
- Produces: điểm vào phiên sau nhất quán với baseline `3.1.0`.

- [x] **Step 1:** Cập nhật version/date/inventory trong AGENTS và STATUS.
- [x] **Step 2:** Đóng P3 cho Google Drive; giữ Notion/NAS và P4 ở trạng thái chưa xác định.
- [x] **Step 3:** Viết lại handoff với evidence, việc đã làm và bước kiểm thử nguồn tiếp theo.

### Task 4: Sinh artifact và kiểm chứng

**Files:**
- Regenerate: `knowledge-vng/*.md`
- Regenerate: `so-tay-tao-knowledge-base.html`

**Interfaces:**
- Consumes: master `3.1.0`, 14 mapping MinIO hiện hữu.
- Produces: 13 module và HTML offline nhất quán.

- [ ] **Step 1:** Chạy `python scripts\build_handbook.py`; yêu cầu exit code 0 và dòng `Build complete`. Đang chờ 11 mapping MinIO; bản local đã sinh bằng `--allow-missing-minio`.
- [x] **Step 2:** Chạy `python -m unittest discover -s tests -v`; yêu cầu `Ran 7 tests` và `OK`.
- [x] **Step 3:** Kiểm tra 13 module, một H1 mỗi module, link ảnh human/audit hợp lệ; ghi rõ 14 mapping hiện có và 11 mapping Google Drive còn thiếu nếu chưa được cấp quyền upload.
- [x] **Step 4:** So sánh metadata/version giữa master và HTML, rồi ghi kết quả thực tế vào báo cáo cuối.
