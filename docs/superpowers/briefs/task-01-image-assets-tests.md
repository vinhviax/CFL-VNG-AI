# Task 01 — Test bảo vệ kiến trúc KB asset

## Phạm vi sở hữu

- Chỉ sửa `tests/test_build_handbook.py`.
- Không sửa `knowledge-vng/image-map.json`, master, module sinh tự động hoặc file live.
- Bạn không làm việc một mình trong workspace; không hoàn tác thay đổi ngoài phạm vi trên.

## Yêu cầu

1. Thêm `import json`.
2. Thêm test `test_project_image_map_covers_all_assets_from_dedicated_asset_kb` đúng theo Task 1 trong plan `docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md`.
3. Thêm test `test_generated_project_modules_have_no_active_local_image_links` đúng theo Task 1 trong plan; bỏ qua liên kết nằm trong fenced code.
4. Chạy riêng test metadata và ghi nhận nó thất bại vì map vẫn có `Mixed; see provenance` hoặc thiếu `knowledge_base_id`.
5. Chạy riêng test active local image links và xác nhận đạt.
6. Không sửa dữ liệu chỉ để làm test metadata đạt ở task này.

## Báo cáo bắt buộc

Tạo `docs/superpowers/reports/task-01-implementer.md` bằng `apply_patch`, gồm:

- trạng thái `PASS` hoặc `BLOCKED`;
- file đã sửa;
- lệnh test đã chạy và kết quả;
- xác nhận failure của test metadata là failure dự kiến;
- rủi ro hoặc ghi chú còn lại.
