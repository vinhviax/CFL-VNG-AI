# Task 02 — Ghi quy trình hai KB vào master

## Phạm vi sở hữu

- Chỉ sửa `so-tay-tao-knowledge-base-v3.md` và report của task này.
- Không sửa trực tiếp 13 file trong `knowledge-vng/`, HTML, image map hoặc file live.
- Bạn không làm việc một mình; không hoàn tác thay đổi ngoài phạm vi.

## Nguồn yêu cầu

- Task 2 trong `docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md`.
- Thiết kế đã duyệt: `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`.

## Yêu cầu

1. Tăng phiên bản master từ `3.1.0` lên `3.1.1`, giữ ngày `07/08/2026`.
2. Trong phần `Ảnh trong file Markdown: hai mục đích, hai đường dẫn`, thêm chính xác nguyên tắc `Hai KB, hai vai trò` và thứ tự migration an toàn theo plan.
3. Trong module 09, sau quy trình `Tải tệp lên`, thêm checklist `Nạp một bộ Markdown có ảnh` theo plan.
4. Trong module 11, thay quy trình chuẩn cũ bằng tám bước mới theo plan: asset local → KB asset → image-map → builder → chỉ 13 MD vào KB sử dụng → test ảnh → kiểm nguồn → không xóa dependency.
5. Thêm hàng lịch sử `3.1.1` đúng nội dung trong plan.
6. Không thay đổi marker module; xác nhận còn đúng `13 13`.
7. Dùng `apply_patch` cho mọi chỉnh sửa.

## Báo cáo bắt buộc

Tạo `docs/superpowers/reports/task-02-implementer.md`, gồm:

- trạng thái `PASS` hoặc `BLOCKED`;
- vị trí nội dung đã đổi;
- kết quả kiểm tra marker;
- xác nhận không sửa artifact sinh tự động;
- rủi ro hoặc ghi chú còn lại.
