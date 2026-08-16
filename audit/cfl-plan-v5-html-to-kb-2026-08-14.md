# Audit chuyển đổi CFL Plan Version 5 HTML sang Knowledge Base

**Ngày:** 14/08/2026  
**Phạm vi:** local-only; không truy cập hoặc mutation VNG AI Web  
**Trạng thái:** Hoàn tất local; gate tự động và review độc lập PASS

## Nguồn và đích

- Nguồn chỉ đọc: `C:\Users\CPU13114\Downloads\CFL5_0- Plan Ver 5.0-14082026.html`.
- Tên tài liệu: `Nội Dung Phiên Bản CFL 5.0`.
- Kích thước nguồn: 2.582.011 byte.
- Encoding: UTF-8, không BOM.
- SHA-256 nguồn: `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`.
- Đích: `knowledge/GS9 Plan Version/V5/`.

## Phương pháp

1. Parse DOM tĩnh bằng BeautifulSoup; script JavaScript duy nhất chỉ xử lý scroll/TOC và không sinh nội dung.
2. Khóa checksum và hợp đồng cấu trúc của đúng file nguồn trước khi cho phép chuyển đổi.
3. Ánh xạ theo class/section của tài liệu thay vì dùng HTML-to-Markdown chung.
4. Giữ thứ tự DOM của section, group, item và figure; cấp ID nguồn ổn định cho từng group/item/key point.
5. Giải mã trực tiếp các data-URI JPEG; không resize, không nén lại.
6. Lưu manifest keyed record để đối chiếu title, description, highlights, figure và asset theo từng nguồn.

## Inventory đã kiểm chứng

| Thành phần | Số lượng |
|---|---:|
| Section | 9 |
| Key point | 20 |
| Group | 29 |
| Group description | 16 |
| Item | 115 |
| Mô tả item có nội dung / rỗng | 114 / 1 |
| Danh sách highlight / bullet | 35 / 91 |
| Figure DOM | 14 |
| Figure có ảnh / placeholder | 12 / 2 |
| Placeholder lịch FIG-00 | 1 |
| Tổng figure slot FIG-00…FIG-14 | 15 |
| Ảnh JPEG nhúng | 29 |
| Tổng byte JPEG đã giải mã | 1.872.262 |

## Đầu ra

- 12 Markdown phẳng: index, 9 module theo section, danh mục figure/ảnh và ghi chú/truy nguyên.
- 29 JPEG trong `assets/`.
- 1 `source-manifest.json` chứa coverage, 20 key point, 29 group, 115 item, 15 figure, 29 asset và checksum.
- Tổng cộng: 42 file, 2.086.721 byte.
- Tree SHA-256 theo `relative-path + NUL + file-sha256 + LF`: `6d21a0d814e39b785ae59250d10f07d8ddfe563dd2f27d01dd264be62558aff4`.
- SHA-256 của 29 JPEG nối theo thứ tự DOM: `69535d8f59b68a0b1cd99cd62e6a647c31f93e317cb36b1fe609169a848fdba4`.

## Dữ kiện thiếu hoặc mâu thuẫn được giữ nguyên

- FIG-00 chưa có sơ đồ/thời điểm chi tiết; FIG-11 và FIG-12 chưa có ảnh.
- Item `Đạo cụ lên kệ trên cửa hàng web` có `.d` rỗng. CSS có fallback `Sẽ bổ sung chi tiết sau`, nhưng node rỗng đồng thời bị `display:none`; đầu ra phân loại fallback là có điều kiện, không biến nó thành mô tả DOM đã kiểm chứng.
- Mở đầu section thương mại hóa nêu 47 nội dung, trong khi DOM có 46 item card. Cả hai dữ kiện được giữ và cảnh báo, không tự điều chỉnh.
- Có 3 cặp mô tả trùng chính xác dưới các title khác nhau; tất cả bản ghi được giữ riêng.
- Thứ tự figure trong DOM là `FIG-00`, `FIG-01`…`FIG-09`, `FIG-14`, `FIG-10`, `FIG-11`, `FIG-13`, `FIG-12`; không tự sort lại theo số.

## Bộ chuyển đổi và kiểm thử

- Script: `scripts/convert_cfl_plan_html.py`.
- Test: `tests/test_convert_cfl_plan_html.py`.
- Test chuyên biệt hiện tại: `Ran 6 tests`, `OK`.
- Toàn bộ test suite project: `Ran 22 tests`, `OK`.
- Các test khóa checksum/cấu trúc nguồn, keyed source record, độ phủ semantic text, hình dạng đầu ra, idempotence, JPEG magic/dimensions/checksum và liên kết Markdown.
- Review độc lập: PASS, không có blocker/thiếu dữ liệu quan trọng. Finding mức Low về tên trường hidden đã được xử lý bằng hai trường tách biệt `dom_or_inline_hidden_elements: 0` và `css_hidden_empty_descriptions: 1`.

## Boundary

- Không sửa/di chuyển file HTML nguồn.
- Không đọc credential hoặc dữ liệu ngoài phạm vi.
- Không tạo, upload, publish, bind hoặc sửa Knowledge Base/Agent trên Web.
- Bộ `knowledge/GS9 Plan Version/V5/` hiện chỉ là local source-of-truth; mọi lần upload Web cần yêu cầu và approval riêng.

## Gate cuối

- [x] Test converter chuyên biệt PASS.
- [x] Toàn bộ test suite project PASS (`Ran 22 tests`, `OK`).
- [x] Link/asset và secret-pattern scan PASS trên đầu ra mới (0 secret-pattern finding).
- [x] Review độc lập PASS; không có finding nghiêm trọng, finding Low đã xử lý.
- [x] `git diff --check` PASS.
