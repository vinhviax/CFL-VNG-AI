# Báo cáo Task 01 — Test bảo vệ kiến trúc KB asset

**Trạng thái:** PASS

## File đã sửa

- `tests/test_build_handbook.py`
- `docs/superpowers/reports/task-01-implementer.md`

## Lệnh test và kết quả

1. `python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb`
   - Kết quả: `FAILED (failures=1)`, exit code `1`.
   - Failure: `knowledge_base` thực tế là `Mixed; see provenance`, khác giá trị đích `Knowledge VNG - Image Assets`.
2. `python -m unittest discover -s tests -v -k generated_project_modules_have_no_active_local_image_links`
   - Kết quả: `OK`, exit code `0`; chạy `1` test.

## Xác nhận failure dự kiến

Failure của test metadata là failure dự kiến theo brief Task 01. Test đã bắt đúng metadata cũ trong `knowledge-vng/image-map.json`; file dữ liệu này không được sửa để làm test đạt trong task hiện tại.

## Rủi ro và ghi chú còn lại

- Test metadata sẽ tiếp tục đỏ cho đến khi task migration được phép cập nhật đầy đủ metadata sang KB `Knowledge VNG - Image Assets`.
- Không chạy build, full test suite hoặc test nào ngoài đúng hai lệnh riêng trong brief.
- Không sửa `image-map.json`, master, module sinh tự động hay artifact khác.
