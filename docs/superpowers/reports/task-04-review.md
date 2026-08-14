# Task 04 — Review độc lập migration KB ảnh

**Ngày review:** 07/08/2026  
**Kết luận:** **APPROVED**

## Tóm tắt

Task 4 đáp ứng toàn bộ tiêu chí local được giao. `image-map.json` ánh xạ đúng 25 asset PNG sang 25 URI MinIO mới, các audit ID nhất quán, snapshot trước migration tồn tại và khác map hiện tại, và hai test metadata/signature đều đạt. Không phát hiện blocker về tính đúng đắn, mất dữ liệu hoặc tính nhất quán của artifact.

Review này không có quyền mở browser live. Vì vậy, các kết luận về URI phát sinh trên trang chi tiết, thao tác xóa 14 bản cũ và inventory live sau xóa chỉ được đánh giá dựa trên báo cáo/audit do main agent cung cấp; phần được kiểm chứng độc lập là filesystem, nội dung JSON, magic bytes, quan hệ tập hợp và test local.

## Findings

Không có 🔴 blocker.

🟡 **Testing: test metadata chưa khóa đuôi `.png`**

`test_project_image_map_covers_all_assets_from_dedicated_asset_kb` kiểm tra metadata, tập key, số lượng, URI duy nhất và prefix tenant, nhưng chưa assert `uri.endswith(".png")`.

**Vì sao:** Gate Task 4 phụ thuộc trực tiếp vào việc chọn asset gốc `.png`; một URI `.jpg` vẫn có thể làm test metadata hiện tại xanh.

**Gợi ý:** Bổ sung assertion suffix `.png` trong một task hardening sau. Đây không phải blocker cho Task 4 vì kiểm tra độc lập ở review này xác nhận cả 25 URI hiện tại đều kết thúc `.png`.

💭 **Ranh giới bằng chứng live**

Các file audit local chứng minh nội bộ rằng có 25 ID mới, 14 ID cũ khác tập và record inventory `25/25/0`; chúng không tự chứng minh trạng thái live tại thời điểm review. Không nâng các record đó thành quan sát browser độc lập.

## Đối chiếu tiêu chí

| Tiêu chí | Kết quả độc lập | Trạng thái |
|---|---|---|
| Map khớp asset | 25 file `knowledge-vng/assets/*.png`; 25 key map; hai tập tên bằng nhau | PASS |
| URI MinIO | 25 URI duy nhất; tất cả có prefix `minio://knowledge-base-prd/10012/exports/` và suffix `.png` | PASS |
| Magic bytes | Cả 25 file bắt đầu bằng `89 50 4E 47 0D 0A 1A 0A`; không có mismatch | PASS |
| ID mới | 25 entry, 25 ID duy nhất; tập filename cũng khớp 25 asset | PASS |
| ID cũ | 14 entry, 14 ID duy nhất; đúng nhóm filename 01–14 | PASS |
| Giao ID cũ/mới | Tập giao rỗng | PASS |
| Inventory audit sau xóa | `documents=25`, `png_documents=25`, `markdown_documents=0`, `legacy_size_matches=0` | PASS theo audit local |
| Snapshot trước migration | File tồn tại; khác map mới cả raw bytes lẫn JSON; cả 25 giá trị mapping đã đổi | PASS |
| Test metadata/signature | `Ran 2 tests`; `OK` | PASS |

Các artifact đã đối chiếu:

- [`knowledge-vng/image-map.json`](../../../knowledge-vng/image-map.json)
- [`audit/image-assets-knowledge-ids-2026-08-07.json`](../../../audit/image-assets-knowledge-ids-2026-08-07.json)
- [`audit/image-assets-replaced-knowledge-ids-2026-08-07.json`](../../../audit/image-assets-replaced-knowledge-ids-2026-08-07.json)
- [`audit/image-map-before-assets-migration-2026-08-07.json`](../../../audit/image-map-before-assets-migration-2026-08-07.json)
- [`tests/test_build_handbook.py`](../../../tests/test_build_handbook.py)

## Đánh giá logic `task-04-format-debug.md`

Logic trong [`task-04-format-debug.md`](task-04-format-debug.md) là nhất quán và có điểm dừng an toàn:

1. Hiện tượng `.png` theo tên nhưng chỉ phát sinh URI `.jpg` được truy về payload JPEG/JFIF thật của ảnh 01–14.
2. Giả thuyết sửa chỉ thay container/encoding sang PNG, giữ filename và kích thước.
3. Ảnh 01 được dùng làm canary; chỉ khi sinh đúng một URI `.png` mới rollout 02–14.
4. Map chỉ được cập nhật sau khi đủ 25 tên, 25 URI duy nhất, đúng tenant và đúng suffix; tránh trạng thái map cập nhật một phần.
5. Xóa bản cũ theo tên + dung lượng + knowledge ID, đồng thời giữ bản mới cùng tên, là guard hợp lý chống xóa nhầm.

Kiểm tra chéo local bổ sung bằng Pillow cho thấy backup có đúng 14 file 01–14; mọi cặp đều chuyển từ format `JPEG` sang `PNG`, không đổi kích thước và không đổi pixel RGB sau giải mã (`format_mismatches=[]`, `size_mismatches=[]`, `pixel_mismatches=[]`). Điều này hỗ trợ trực tiếp cho mô tả “lossless theo pixel”. Việc Knowledge VNG sinh URI `.png` sau canary và inventory live sau dọn dẹp vẫn là bằng chứng do main agent ghi nhận, không phải quan sát browser của reviewer.

## Lệnh và kết quả

### 1. Assertion local/audit tổng hợp

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
import json
from pathlib import Path

r = Path(".")
assets = sorted((r / "knowledge-vng/assets").glob("*.png"))
names = {p.name for p in assets}
new_path = r / "knowledge-vng/image-map.json"
before_path = r / "audit/image-map-before-assets-migration-2026-08-07.json"
image_map = json.loads(new_path.read_text(encoding="utf-8"))["images"]
new_ids = json.loads((r / "audit/image-assets-knowledge-ids-2026-08-07.json").read_text(encoding="utf-8"))["knowledge_ids"]
replaced = json.loads((r / "audit/image-assets-replaced-knowledge-ids-2026-08-07.json").read_text(encoding="utf-8"))
old_ids = replaced["deleted_knowledge_ids"]
inventory = replaced["post_delete_inventory"]
uris = list(image_map.values())
prefix = "minio://knowledge-base-prd/10012/exports/"

checks = {
    "assets_map_25_exact": len(assets) == len(image_map) == 25 and set(image_map) == names,
    "uris_25_unique_prefix_png": len(set(uris)) == 25 and all(u.startswith(prefix) and u.endswith(".png") for u in uris),
    "png_magic_25": all(p.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" for p in assets),
    "new_ids_25_unique": len(new_ids) == len(set(new_ids.values())) == 25,
    "old_ids_14_unique": len(old_ids) == len(set(old_ids.values())) == 14,
    "old_new_ids_disjoint": set(old_ids.values()).isdisjoint(new_ids.values()),
    "inventory_25_25_0": [inventory[k] for k in ("documents", "png_documents", "markdown_documents")] == [25, 25, 0],
    "before_map_exists_and_differs": before_path.exists() and before_path.read_bytes() != new_path.read_bytes(),
}
for key, value in checks.items():
    print(f"{key}={value}")
assert all(checks.values())
'@ | python -
```

Kết quả: exit code `0`; cả tám dòng đều `True`:

```text
assets_map_25_exact=True
uris_25_unique_prefix_png=True
png_magic_25=True
new_ids_25_unique=True
old_ids_14_unique=True
old_new_ids_disjoint=True
inventory_25_25_0=True
before_map_exists_and_differs=True
```

Kiểm tra mở rộng cùng phiên còn cho kết quả `mapping_values_changed=25`, `png_magic_bad=[]`, `old_new_id_intersection=[]` và không có UUID lỗi.

### 2. Test metadata và signature

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest -v tests.test_build_handbook.BuildHandbookTests.test_project_image_map_covers_all_assets_from_dedicated_asset_kb tests.test_build_handbook.BuildHandbookTests.test_local_png_assets_have_png_signature
```

Kết quả: exit code `0`:

```text
test_project_image_map_covers_all_assets_from_dedicated_asset_kb ... ok
test_local_png_assets_have_png_signature ... ok
Ran 2 tests in 0.452s
OK
```

### 3. Kiểm tra logic transcode bằng backup

Chạy script Pillow chỉ đọc để so sánh 14 cặp backup/current theo format, kích thước và pixel RGB. Kết quả: exit code `0`:

```text
backup_files=14
format_mismatches=[]
size_mismatches=[]
pixel_mismatches=[]
```

## Phạm vi thay đổi của reviewer

Workspace không phải Git repository (`git status --short` trả exit code `128`), nên không có VCS diff để dùng làm bằng chứng phạm vi. Reviewer chỉ chạy lệnh đọc/test với `PYTHONDONTWRITEBYTECODE=1`; không chạy builder và không sửa master, source, generated file, asset hay audit. File duy nhất reviewer tạo là báo cáo này.

## Kết luận cuối

**APPROVED.** Task 4 có đủ bằng chứng local để chấp nhận mapping và migration record hiện tại. Có thể chuyển sang bước tiếp theo của plan, với điều kiện mọi quyết định dựa trên trạng thái live tiếp tục dùng audit/report có ngày hoặc được main agent kiểm tra lại bằng browser.
