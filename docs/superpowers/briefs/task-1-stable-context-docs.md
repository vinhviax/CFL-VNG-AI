# Task 1: Ghi tài liệu bối cảnh và quy tắc ổn định

## Global constraints

- Thư mục đích chính xác: `J:\My Drive\AI\Knowledge Base VNG`.
- Nguồn nội dung chuẩn duy nhất: `so-tay-tao-knowledge-base-v3.md`, phiên bản `3.0.1`, cập nhật `06/08/2026`.
- Không sửa trực tiếp 12 file sinh trong `knowledge-vng/` hoặc HTML sinh tự động.
- Giữ nguyên 14 ảnh local và 14 URI trong `knowledge-vng/image-map.json`.
- Không thay đổi hoặc xóa dữ liệu ngoài hai KB test được ghi trong audit.
- Mọi trạng thái live phải có ngày kiểm chứng và liên kết bằng chứng.
- Workspace không phải Git repository; không tạo commit hay worktree.

## Files

- Create: `AGENTS.md`
- Create: `PROJECT.md`
- Create: `DECISIONS.md`
- Read: `so-tay-tao-knowledge-base-v3.md`
- Read: `scripts/build_handbook.py`
- Read: `knowledge-vng/image-map.json`
- Read: `docs/superpowers/specs/2026-08-06-project-handoff-docs-design.md`

## Interfaces

- Consumes: metadata master, cấu trúc builder, danh sách artifact và chiến lược ảnh đã kiểm chứng.
- Produces: quy tắc workspace, tổng quan dự án và nhật ký quyết định để `STATUS.md`/`HANDOFF.md` liên kết tới.

## Required work

1. Tạo `AGENTS.md` với các phần: phạm vi áp dụng; thứ tự đọc bắt đầu bằng `HANDOFF.md`; nguồn chuẩn; vùng được sửa; quy tắc an toàn khi kiểm tra live; quy trình sửa master → build → test → cập nhật audit/status; lệnh build/test; tiêu chí hoàn tất.
2. Tạo `PROJECT.md` với: mục tiêu; đối tượng dùng; năm nhóm đầu ra; luồng master → 12 module/HTML; cây thư mục; chiến lược ảnh local và MinIO; hai KB test cùng ID/tenant; giới hạn phạm vi.
3. Tạo `DECISIONS.md` với tám quyết định có mã, ngày và trạng thái: master là nguồn chuẩn; 12 module; HTML offline một file; hai đường ảnh; MinIO cần giữ nguồn; chỉ thao tác KB test; phân biệt kiểm chứng/điều kiện/bị chặn; cập nhật bàn giao cuối phiên.
4. Xác nhận `AGENTS.md` chỉ chứa chỉ dẫn, `PROJECT.md` chỉ mô tả bối cảnh ổn định và `DECISIONS.md` giải thích quyết định; không file nào nhận vai trò nguồn nghiệp vụ thay master.

## Report contract

Viết báo cáo đầy đủ tại `docs/superpowers/reports/task-1-stable-context-docs-report.md`, gồm: nội dung đã tạo, kiểm tra đã chạy, file đã đổi, tự rà soát và mọi lo ngại. Trong phản hồi cuối chỉ ghi trạng thái, tóm tắt kiểm tra, lo ngại và đường dẫn báo cáo.
