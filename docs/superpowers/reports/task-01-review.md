# Review độc lập Task 01 — Test bảo vệ kiến trúc KB asset

**Verdict:** APPROVED  
**Cho phép chuyển Task 2:** CÓ

## Tóm tắt

Implementation đáp ứng Task 01: đã thêm `import json`, thêm đúng hai test được chỉ định trong Task 1 của plan, giữ nguyên dữ liệu migration để test metadata tiếp tục đỏ theo chủ đích, và test liên kết local đạt trên các module hiện tại.

## Findings theo severity

### 🔴 Blocker

Không có.

### 🟡 Suggestion

Không có thay đổi bắt buộc trước Task 2.

### 💭 Nit / rủi ro còn lại

- Bộ dò fenced code dùng cơ chế toggle khi dòng bắt đầu bằng ````` hoặc `~~~`. Cơ chế này xử lý đúng fixture hiện tại trong `01-chuan-bi-noi-dung.md`: liên kết `](assets/...)` nằm giữa fence không bị tính là liên kết hoạt động. Nếu sau này module dùng fence CommonMark phức tạp hơn, như fence dài hơn có delimiter ngắn hơn trong nội dung, nên bổ sung test chuyên biệt theo độ dài và loại delimiter; đây không phải yêu cầu chặn của Task 01 vì implementation khớp chính xác code trong plan và baseline hiện tại đã được kiểm chứng.
- Workspace không phải Git repository như plan đã nêu, nên phạm vi được đối chiếu từ các file được giao và trạng thái hiện tại thay vì VCS diff. Không thấy dấu hiệu Task 01 sửa `knowledge-vng/image-map.json`, master, module sinh tự động hoặc dữ liệu live; failure metadata còn nguyên xác nhận dữ liệu chưa bị sửa chỉ để làm test xanh.

## Đối chiếu yêu cầu và phạm vi

- `tests/test_build_handbook.py` có `import json`.
- Có `test_project_image_map_covers_all_assets_from_dedicated_asset_kb` đúng nội dung Task 1 trong plan.
- Có `test_generated_project_modules_have_no_active_local_image_links` đúng nội dung Task 1 trong plan và bỏ qua fenced code của module hiện tại.
- `docs/superpowers/reports/task-01-implementer.md` ghi đủ trạng thái, file, lệnh/kết quả, failure dự kiến và rủi ro còn lại.
- Failure metadata là failure dự kiến; không được sửa `image-map.json` trong Task 01.

## Lệnh test và kết quả review độc lập

1. `python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb`
   - Exit code: `1`.
   - Chạy `1` test; kết quả `FAILED (failures=1)`.
   - Failure đúng dự kiến: `knowledge_base` thực tế là `Mixed; see provenance`, khác `Knowledge VNG - Image Assets`.

2. `python -m unittest discover -s tests -v -k generated_project_modules_have_no_active_local_image_links`
   - Exit code: `0`.
   - Chạy `1` test; kết quả `OK`.

## Quyết định gate

Task 01 được **APPROVED**. Cho phép bắt đầu **Task 2**; test metadata tiếp tục đỏ là checkpoint migration có chủ đích, không phải blocker của Task 01.
