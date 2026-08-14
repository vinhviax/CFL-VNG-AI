# Knowledge Base VNG Project Handoff Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo bộ năm file Markdown ở thư mục gốc để agent mới hiểu dự án, trạng thái, quyết định, quy tắc làm việc và bước tiếp theo mà không cần suy đoán.

**Architecture:** Chia thông tin theo vòng đời: `PROJECT.md` và `DECISIONS.md` giữ bối cảnh ổn định; `STATUS.md` giữ ảnh chụp trạng thái theo ngày; `HANDOFF.md` là điểm vào cho phiên tiếp theo; `AGENTS.md` là quy tắc vận hành áp dụng cho toàn workspace. Các file liên kết tới master và audit thay vì sao chép toàn bộ nội dung nghiệp vụ.

**Tech Stack:** Markdown UTF-8, PowerShell để kiểm tra file/liên kết, Python 3 và `unittest` cho build/test hiện có.

## Global Constraints

- Thư mục đích chính xác: `J:\My Drive\AI\Knowledge Base VNG`.
- Nguồn nội dung chuẩn duy nhất: `so-tay-tao-knowledge-base-v3.md`, phiên bản `3.0.1`, cập nhật `06/08/2026`.
- Không sửa trực tiếp 12 file sinh trong `knowledge-vng/` hoặc HTML sinh tự động.
- Giữ nguyên 14 ảnh local và 14 URI trong `knowledge-vng/image-map.json`.
- Không thay đổi hoặc xóa dữ liệu ngoài hai KB test được ghi trong audit.
- Mọi trạng thái live phải có ngày kiểm chứng và liên kết bằng chứng.
- Workspace không phải Git repository; không tạo bước commit giả định.

---

### Task 1: Ghi tài liệu bối cảnh và quy tắc ổn định

**Files:**

- Create: `AGENTS.md`
- Create: `PROJECT.md`
- Create: `DECISIONS.md`
- Read: `so-tay-tao-knowledge-base-v3.md`
- Read: `scripts/build_handbook.py`
- Read: `knowledge-vng/image-map.json`

**Interfaces:**

- Consumes: metadata master, cấu trúc builder, danh sách artifact và chiến lược ảnh đã kiểm chứng.
- Produces: quy tắc workspace, tổng quan dự án và nhật ký quyết định để `STATUS.md`/`HANDOFF.md` liên kết tới.

- [ ] **Step 1: Tạo `AGENTS.md` với phạm vi và thứ tự đọc**

  File phải có các phần: phạm vi áp dụng; thứ tự đọc bắt đầu bằng `HANDOFF.md`; nguồn chuẩn; vùng được sửa; quy tắc an toàn khi kiểm tra live; quy trình sửa master → build → test → cập nhật audit/status; lệnh build/test; tiêu chí hoàn tất.

- [ ] **Step 2: Tạo `PROJECT.md` với bản đồ dự án**

  File phải nêu: mục tiêu; đối tượng dùng; năm nhóm đầu ra; luồng master → 12 module/HTML; cây thư mục; chiến lược ảnh local và MinIO; hai KB test cùng ID/tenant; giới hạn phạm vi.

- [ ] **Step 3: Tạo `DECISIONS.md` với các quyết định bền vững**

  Ghi tám quyết định có mã, ngày và trạng thái: master là nguồn chuẩn; 12 module; HTML offline một file; hai đường ảnh; MinIO cần giữ nguồn; chỉ thao tác KB test; phân biệt kiểm chứng/điều kiện/bị chặn; cập nhật bàn giao cuối phiên.

- [ ] **Step 4: Kiểm tra ranh giới nội dung**

  Xác nhận `AGENTS.md` chỉ chứa chỉ dẫn, `PROJECT.md` chỉ mô tả bối cảnh ổn định và `DECISIONS.md` giải thích quyết định; không file nào nhận vai trò nguồn nghiệp vụ thay master.

### Task 2: Ghi trạng thái và bàn giao phiên tiếp theo

**Files:**

- Create: `STATUS.md`
- Create: `HANDOFF.md`
- Read: `audit/audit-knowledge-vng-2026-08-06.md`
- Read: `tests/test_build_handbook.py`

**Interfaces:**

- Consumes: kết quả audit ngày 06/08/2026, số lượng artifact và kết quả kiểm tra hiện có.
- Produces: ảnh chụp trạng thái có ngày và hướng dẫn tiếp tục có thứ tự ưu tiên.

- [ ] **Step 1: Tạo `STATUS.md`**

  Ghi chính xác: v3.0.1; 1.078 dòng master; 12 module; 14 ảnh; 14 mapping MinIO; HTML 2.379.085 byte; 7 test; Graph 159 node gồm 22/66/70/0/0; một ảnh FAQ còn `Đang hoàn tất`; cấu hình FAQ đã phục hồi; bốn nhóm backlog chưa xác thực.

- [ ] **Step 2: Tạo `HANDOFF.md`**

  Ghi trạng thái “baseline hoàn tất, không có tác vụ triển khai đang mở”; thứ tự đọc; lệnh kiểm tra đầu phiên; bốn việc tiếp theo theo mức ưu tiên; điều kiện cần quyền/credential; checklist trước/sau chỉnh sửa; bẫy không sửa file sinh và không xóa nguồn ảnh MinIO.

- [ ] **Step 3: Liên kết chéo có chủ đích**

  `HANDOFF.md` trỏ tới `STATUS.md`, `PROJECT.md`, `DECISIONS.md`, `AGENTS.md`, master và audit. `STATUS.md` trỏ tới audit/evidence thay vì sao chép toàn bộ bằng chứng.

### Task 3: Kiểm chứng bộ tài liệu và dự án

**Files:**

- Verify: `AGENTS.md`
- Verify: `PROJECT.md`
- Verify: `STATUS.md`
- Verify: `HANDOFF.md`
- Verify: `DECISIONS.md`
- Verify: `so-tay-tao-knowledge-base.html`
- Test: `tests/test_build_handbook.py`

**Interfaces:**

- Consumes: năm file mới và toàn bộ artifact hiện có.
- Produces: bằng chứng rằng liên kết nội bộ hợp lệ, số liệu nhất quán, build nghiêm ngặt thành công và test không hồi quy.

- [ ] **Step 1: Kiểm tra file và liên kết Markdown tương đối**

  Chạy một script PowerShell đọc năm file, lấy các target Markdown tương đối, bỏ qua URL/anchor và xác nhận từng target tồn tại từ thư mục chứa file. Kết quả mong đợi: `BROKEN_LINKS=0`.

- [ ] **Step 2: Kiểm tra các số liệu bắt buộc**

  Đối chiếu bằng lệnh đọc filesystem và JSON: `MODULES=12`, `ASSETS=14`, `MINIO_MAPPINGS=14`, `MASTER_LINES=1078`, `HTML_BYTES=2379085` trước khi build lại.

- [ ] **Step 3: Chạy build nghiêm ngặt**

  Run: `python scripts\build_handbook.py`

  Expected: exit code 0, dòng `Build complete`, `12 modules` và `Offline HTML`.

- [ ] **Step 4: Chạy toàn bộ test**

  Run: `python -m unittest discover -s tests -v`

  Expected: exit code 0, `Ran 7 tests` và `OK`.

- [ ] **Step 5: Đọc lại checklist yêu cầu**

  Xác nhận năm file ở thư mục gốc, không có liên kết hỏng, không có số liệu trái audit, bốn backlog vẫn mang nhãn chưa xác thực và các lệnh khôi phục quy trình đều có thể sao chép chạy trực tiếp.
