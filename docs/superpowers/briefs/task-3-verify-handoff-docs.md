# Task 3: Kiểm chứng bộ tài liệu và dự án

## Global constraints

- Thư mục đích chính xác: `J:\My Drive\AI\Knowledge Base VNG`.
- Không sửa nội dung năm file bàn giao trong task này; nếu phát hiện lỗi, báo chính xác file/dòng để controller xử lý.
- Không sửa master, 12 module, image map hoặc audit.
- Build nghiêm ngặt được phép tái sinh 12 module và HTML theo master hiện tại.
- Workspace không phải Git repository; không tạo commit hay worktree.

## Files to verify

- `AGENTS.md`
- `PROJECT.md`
- `STATUS.md`
- `HANDOFF.md`
- `DECISIONS.md`
- `so-tay-tao-knowledge-base-v3.md`
- `so-tay-tao-knowledge-base.html`
- `knowledge-vng/image-map.json`
- `tests/test_build_handbook.py`

## Required checks

1. Kiểm tra cả năm file bàn giao tồn tại ở thư mục gốc.
2. Đọc link Markdown tương đối trong năm file; bỏ qua URL, `minio://`, `mailto:`, anchor thuần và ảnh; bỏ phần `#anchor`; resolve từ thư mục chứa file; báo số link hỏng. Kết quả yêu cầu: `BROKEN_LINKS=0`.
3. Đối chiếu filesystem/JSON và báo: `MODULES=12`, `ASSETS=14`, `MINIO_MAPPINGS=14`, `MASTER_LINES=1078`.
4. Chạy `python scripts\build_handbook.py`; yêu cầu exit code 0, `Build complete`, `12 modules`, `Offline HTML`.
5. Sau build, báo lại byte của HTML và xác nhận có 14 data URI ảnh, không có `<script src=`, `src="http` hoặc `<link rel="stylesheet"`.
6. Chạy `python -m unittest discover -s tests -v`; yêu cầu exit code 0, `Ran 7 tests`, `OK`.
7. Đọc yêu cầu thiết kế tại `docs/superpowers/specs/2026-08-06-project-handoff-docs-design.md` và xác nhận: số liệu không trái audit; bốn backlog vẫn mang trạng thái chưa xác thực; không có chỉ dẫn sửa trực tiếp artifact sinh tự động.

## Report contract

Không chỉnh sửa artifact ngoài việc build tái sinh output. Viết báo cáo đầy đủ tại `docs/superpowers/reports/task-3-verify-handoff-docs-report.md`, gồm từng lệnh, exit code, kết quả đếm, link hỏng nếu có và mọi sai lệch yêu cầu. Trong phản hồi cuối chỉ ghi trạng thái, tóm tắt kết quả, lo ngại và đường dẫn báo cáo.
