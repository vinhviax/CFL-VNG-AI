# Knowledge VNG Image Assets KB Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển toàn bộ 25 ảnh sang KB `Knowledge VNG - Image Assets`, cấp lại 25 URI MinIO, cập nhật quy trình trong master, và đưa `Knowledge VNG AI` về đúng 13 file Markdown không chứa tài liệu PNG.

**Trạng thái:** Đã triển khai và kiểm chứng ngày 07/08/2026. Không chạy lại plan này như một task mới; xem kết quả tại `docs/superpowers/reports/2026-08-07-image-assets-kb-migration-progress.md` và `docs/superpowers/reports/task-10-final-verification.md`.

**Architecture:** KB asset ID `6da8657c-dd96-4170-a698-074043475014` sở hữu vòng đời 25 ảnh. Builder dùng `knowledge-vng/image-map.json` để sinh 13 Markdown chứa URI MinIO; KB sử dụng ID `cefadf09-4187-46ac-a765-591e3255a4a4` chỉ nhận các Markdown này. HTML offline tiếp tục dùng 25 asset local.

**Tech Stack:** Markdown, JSON, Python `unittest`, `scripts/build_handbook.py`, PowerShell, Knowledge VNG UI qua Chrome.

## Global Constraints

- Chỉ sửa nội dung sổ tay tại `so-tay-tao-knowledge-base-v3.md`; không sửa trực tiếp 13 module hoặc HTML sinh tự động.
- Không xóa 11 PNG khỏi `Knowledge VNG AI` trước khi 25 URI mới, 13 Markdown mới và ba phép thử chat đều đạt.
- Không xóa hoặc đổi tên 25 file trong `knowledge-vng/assets/`.
- Không dùng `--allow-missing-minio` cho bất kỳ artifact bàn giao nào.
- Không dùng thao tác xóa hàng loạt trên live KB; xác định từng bản bằng tên, dung lượng, thời gian tải lên và knowledge ID.
- Workspace không phải Git repository; không tạo commit. Audit, snapshot mapping và output test là checkpoint phục hồi.
- Mọi chỉnh sửa local dùng `apply_patch`; lệnh shell chỉ đọc, build, test hoặc định dạng cơ học.

---

### Task 1: Thêm test bảo vệ kiến trúc KB asset

**Files:**
- Modify: `tests/test_build_handbook.py`
- Test: `tests/test_build_handbook.py`

**Interfaces:**
- Consumes: `knowledge-vng/assets/`, `knowledge-vng/image-map.json` và các module do builder sinh.
- Produces: Hai test tích hợp bảo đảm mapping phủ đủ asset và metadata trỏ duy nhất tới KB asset mới.

- [ ] **Step 1: Thêm import JSON và hai test tích hợp**

Thêm `import json` gần đầu file và thêm hai phương thức sau vào `BuildHandbookTests`:

```python
    def test_project_image_map_covers_all_assets_from_dedicated_asset_kb(self):
        payload = json.loads(
            (ROOT / "knowledge-vng" / "image-map.json").read_text(encoding="utf-8")
        )
        assets = {
            path.name for path in (ROOT / "knowledge-vng" / "assets").glob("*.png")
        }
        images = payload["images"]

        self.assertEqual(payload["knowledge_base"], "Knowledge VNG - Image Assets")
        self.assertEqual(
            payload["knowledge_base_id"],
            "6da8657c-dd96-4170-a698-074043475014",
        )
        self.assertEqual(payload["tenant_id"], "10012")
        self.assertEqual(set(images), assets)
        self.assertEqual(len(images), 25)
        self.assertEqual(len(set(images.values())), 25)
        for uri in images.values():
            self.assertTrue(
                uri.startswith("minio://knowledge-base-prd/10012/exports/")
            )

    def test_generated_project_modules_have_no_active_local_image_links(self):
        for module_path in sorted((ROOT / "knowledge-vng").glob("*.md")):
            rendered = module_path.read_text(encoding="utf-8")
            in_fence = False
            active_lines = []
            for line in rendered.splitlines():
                stripped = line.lstrip()
                if stripped.startswith("```") or stripped.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if not in_fence:
                    active_lines.append(line)
            active = "\n".join(active_lines)
            self.assertNotIn("](assets/", active, module_path.name)
```

- [ ] **Step 2: Chạy test mới và xác nhận test metadata thất bại**

Run:

```powershell
python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb
```

Expected: `FAIL` vì `knowledge_base` hiện là `Mixed; see provenance` hoặc thiếu `knowledge_base_id`.

- [ ] **Step 3: Chạy test link module để giữ baseline**

Run:

```powershell
python -m unittest discover -s tests -v -k generated_project_modules_have_no_active_local_image_links
```

Expected: `OK`; code fence minh họa trong file 01 không bị tính là liên kết hoạt động.

### Task 2: Ghi quy trình hai KB vào master

**Files:**
- Modify: `so-tay-tao-knowledge-base-v3.md`
- Generated later: `knowledge-vng/01-chuan-bi-noi-dung.md`
- Generated later: `knowledge-vng/09-van-hanh-documents-wiki-graph.md`
- Generated later: `knowledge-vng/11-chat-kiem-thu-va-bao-tri.md`
- Generated later: `so-tay-tao-knowledge-base.html`

**Interfaces:**
- Consumes: Thiết kế tại `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`.
- Produces: Master v3.1.1 mô tả rõ KB asset, KB sử dụng và trình tự migration an toàn.

- [ ] **Step 1: Tăng phiên bản master**

Đổi dòng đầu từ `Phiên bản: 3.1.0` thành `Phiên bản: 3.1.1`; giữ ngày cập nhật `07/08/2026`.

- [ ] **Step 2: Thay phần “Ảnh trong file Markdown: hai mục đích, hai đường dẫn”**

Giữ ví dụ local và MinIO hiện có, đồng thời thêm nguyên tắc sau ngay trước phần cảnh báo số liệu:

```markdown
### Hai KB, hai vai trò

- **KB asset** giữ ảnh độc lập và cấp URI `minio://`. Đây là dependency lâu dài, không dùng làm KB hỏi đáp cho human.
- **KB sử dụng** chỉ nhận các file Markdown đã chứa URI MinIO. Không upload thư mục `assets/` hoặc PNG cùng bộ Markdown vào KB này.

Trong dự án này, KB asset là `Knowledge VNG - Image Assets`; KB sử dụng là `Knowledge VNG AI`. `LOCAL_ASSET` trong file sinh chỉ giúp builder tìm ảnh local để dựng HTML offline, không phải liên kết ảnh mà Knowledge VNG chat sử dụng.

Khi đổi nơi lưu ảnh, làm đúng thứ tự: tạo host mới → upload ảnh → lấy URI → cập nhật mapping → build → thay Markdown → kiểm thử chat → xóa ảnh ở nơi cũ. Nếu KB asset cũ bị xóa, phải tái kiểm chứng toàn bộ mapping liên quan dù một số link vẫn tạm thời render.
```

- [ ] **Step 3: Bổ sung checklist vào phần “Tải tệp lên” của module 09**

Sau quy trình tải file thông thường, thêm:

```markdown
### Nạp một bộ Markdown có ảnh

1. Xác nhận ảnh đã tồn tại trong KB asset và mọi file đều có mapping MinIO.
2. Chạy build nghiêm ngặt.
3. Chỉ chọn các file `.md` trong `knowledge-vng/` để nạp vào KB sử dụng.
4. Không chọn `knowledge-vng/assets/` và không nạp PNG cùng bộ Markdown.
5. Sau khi xử lý xong, hỏi câu buộc trả lời kèm ảnh và mở nguồn tham khảo để kiểm tra URI.
```

- [ ] **Step 4: Thay quy trình ảnh trong phần “Ảnh trong chat” của module 11**

Quy trình mới phải gồm đúng các bước:

```markdown
1. Giữ ảnh local trong `knowledge-vng/assets/` để dựng HTML offline.
2. Nạp ảnh một lần vào KB asset có vòng đời ổn định.
3. Lấy và lưu URI MinIO trong `knowledge-vng/image-map.json`.
4. Chạy builder để sinh liên kết MinIO vào 13 file phân phối.
5. Chỉ nạp 13 file MD vào KB sử dụng; không nạp PNG vào KB sử dụng.
6. Hỏi câu có chủ đích “trả lời kèm hình minh họa”.
7. Xác nhận ảnh thật xuất hiện và nguồn Markdown dùng URI của KB asset.
8. Không xóa KB asset hoặc ảnh độc lập khi còn Markdown tham chiếu.
```

- [ ] **Step 5: Thêm lịch sử phiên bản**

Thêm hàng trên `3.1.0`:

```markdown
| 3.1.1 | 07/08/2026 | Chuẩn hóa kiến trúc KB asset riêng; quy định KB sử dụng chỉ nhận Markdown và thêm quy trình migration ảnh an toàn |
```

- [ ] **Step 6: Kiểm tra master vẫn có đúng 13 cặp marker**

Run:

```powershell
@'
from pathlib import Path
text = Path('so-tay-tao-knowledge-base-v3.md').read_text(encoding='utf-8')
print(text.count('<!-- MODULE:'), text.count('<!-- /MODULE -->'))
'@ | python -
```

Expected: `13 13`.

### Task 3: Nạp 25 ảnh vào KB asset mới

**Files:**
- Read: `knowledge-vng/assets/*.png`
- Live target: `Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`, tenant `10012`)

**Interfaces:**
- Consumes: 25 PNG local, từ `01-tong-quan-danh-sach-knowledge.png` đến `25-google-drive-dong-bo-thanh-cong.png`.
- Produces: 25 tài liệu ảnh trong KB asset và 25 knowledge ID có thể mở chi tiết.

- [ ] **Step 1: Mở đúng KB asset và xác nhận trạng thái trước mutation**

URL:

```text
https://vnggames.ai/kb/knowledge/6da8657c-dd96-4170-a698-074043475014?tenant_id=10012
```

Expected: tên `Knowledge VNG - Image Assets`, mô tả `Chứa Image Assets KB VNG`, Documents = `0`.

- [ ] **Step 2: Đối chiếu inventory local**

Run:

```powershell
Get-ChildItem -LiteralPath 'knowledge-vng\assets' -File -Filter '*.png' | Sort-Object Name | Select-Object Name,Length
```

Expected: đúng 25 file, không có tên trùng.

- [ ] **Step 3: Upload cả 25 PNG trong một lượt**

Dùng **Thêm tài liệu → Tải tệp lên**, chọn chính xác 25 đường dẫn tuyệt đối trong `J:\My Drive\AI\Knowledge Base VNG\knowledge-vng\assets\`. Giữ **Xử lý nâng cao** theo mặc định KB; không thêm chunking, parser override hoặc tag.

Expected trước submit: nút ghi `Tải lên 25 tệp`. Expected sau submit: toast `25 thành công / 0 lỗi` hoặc tổng thành công tương đương và Documents tăng lên `25`.

- [ ] **Step 4: Kiểm tra không có Markdown trong KB asset**

Lọc định dạng hoặc đọc danh sách Documents.

Expected: 25 hàng đều kết thúc `.png`; không có `.md`.

### Task 4: Thu thập 25 URI mới và cập nhật image map

**Files:**
- Create: `audit/image-map-before-assets-migration-2026-08-07.json`
- Modify: `knowledge-vng/image-map.json`
- Live source: 25 tài liệu trong KB asset.

**Interfaces:**
- Consumes: 25 document detail page và file map hiện tại.
- Produces: Mapping một-một 25 filename → 25 URI MinIO mới, cùng snapshot mapping cũ.

- [ ] **Step 1: Lưu nguyên nội dung mapping cũ vào audit bằng `apply_patch`**

Tạo `audit/image-map-before-assets-migration-2026-08-07.json` với nguyên văn `knowledge-vng/image-map.json` trước migration. Không sửa URI trong snapshot.

- [ ] **Step 2: Lấy URI cho từng ảnh theo cùng một quy trình**

Với từng hàng ảnh trong KB asset:

1. Mở chi tiết và ghi knowledge ID từ query `knowledge_id=`.
2. Mở URL chi tiết đó trong tab Chrome phụ để buộc tải asset.
3. Dùng capability `pageAssets.list()` và lọc resource URL chứa `file_path=minio`.
4. Chọn URI duy nhất kết thúc `.png`; bỏ các `.jpg` hậu xử lý/OCR.
5. Đối chiếu heading tài liệu với filename trước khi ghi mapping.

Expected mỗi ảnh: đúng một URI PNG dạng `minio://knowledge-base-prd/10012/exports/<uuid>.png`.

- [ ] **Step 3: Kiểm tra 25 URI trước khi sửa file**

Trong bộ nhớ làm việc, kiểm tra:

- 25 filename khớp đúng inventory local.
- 25 URI không trùng.
- Mọi URI dùng tenant `10012` và đuôi `.png`.

Nếu bất kỳ điều kiện nào sai, dừng và mở lại đúng tài liệu; không cập nhật map một phần.

- [ ] **Step 4: Thay toàn bộ metadata và `images` bằng `apply_patch`**

Metadata đích:

```json
{
  "generated_at": "2026-08-07",
  "knowledge_base": "Knowledge VNG - Image Assets",
  "knowledge_base_id": "6da8657c-dd96-4170-a698-074043475014",
  "tenant_id": "10012",
  "purpose": "Map local handbook screenshots to MinIO URIs owned by the dedicated Knowledge VNG image-assets KB. Upload-ready Markdown uses these URIs; offline HTML uses local assets.",
  "provenance": {
    "01-25": "Knowledge VNG - Image Assets (6da8657c-dd96-4170-a698-074043475014)"
  },
  "images": {}
}
```

Điền đủ 25 cặp thực tế vào `images`, sắp xếp theo tiền tố `01` đến `25`.

- [ ] **Step 5: Chạy test metadata đã viết ở Task 1**

Run:

```powershell
python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb
```

Expected: `OK`.

### Task 5: Sinh lại và kiểm tra artifact local

**Files:**
- Generated: `knowledge-vng/00-gioi-thieu-va-quick-start.md` … `knowledge-vng/12-ket-noi-google-drive.md`
- Generated: `so-tay-tao-knowledge-base.html`
- Test: `tests/test_build_handbook.py`

**Interfaces:**
- Consumes: Master v3.1.1 và 25 URI mới.
- Produces: 13 Markdown chat-ready và một HTML offline tự chứa.

- [ ] **Step 1: Chạy strict build**

Run:

```powershell
python scripts\build_handbook.py
```

Expected: exit code `0`, output có `Build complete`, `13 modules` và `Offline HTML`; không có `Missing MinIO mappings`.

- [ ] **Step 2: Chạy toàn bộ test**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: toàn bộ test `ok`, cuối output là `OK`; tổng test tăng từ 7 lên 9.

- [ ] **Step 3: Kiểm tra link ảnh trên 13 module**

Run:

```powershell
@'
from pathlib import Path
import re
root = Path('knowledge-vng')
modules = sorted(root.glob('*.md'))
minio = 0
comments = 0
active_local = []
for path in modules:
    text = path.read_text(encoding='utf-8')
    fenced = False
    active = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            fenced = not fenced
            continue
        if not fenced:
            active.append(line)
    active_text = '\n'.join(active)
    minio += len(re.findall(r'!\[[^\]]*\]\(minio://[^)]+\)', active_text))
    comments += active_text.count('<!-- LOCAL_ASSET:')
    if '](' + 'assets/' in active_text:
        active_local.append(path.name)
print({'modules': len(modules), 'minio': minio, 'comments': comments, 'active_local': active_local})
'@ | python -
```

Expected: `modules: 13`, `minio: 36`, `comments: 36`, `active_local: []`. Số 36 gồm 25 ảnh duy nhất được dùng lặp lại ở module 08 và 12.

- [ ] **Step 4: Kiểm tra HTML offline**

Mở `so-tay-tao-knowledge-base.html` khi ngắt mạng hoặc dùng kiểm tra tự động hiện có.

Expected: phiên bản `3.1.1`, ảnh tổng quan và ảnh Google Drive hiển thị; không có stylesheet/script/ảnh HTTP bên ngoài.

### Task 6: Thay 13 Markdown trong KB sử dụng

**Files:**
- Upload: 13 file `knowledge-vng/*.md`
- Live target: `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`, tenant `10012`)

**Interfaces:**
- Consumes: 13 Markdown đã build và 25 URI mới.
- Produces: Một bản mới duy nhất cho mỗi module trong KB sử dụng; 11 PNG tạm thời vẫn được giữ.

- [ ] **Step 1: Chụp inventory trước khi thay**

Expected baseline: 24 Documents = 13 Markdown + 11 PNG. Ghi tên, dung lượng, trạng thái và knowledge ID của 13 Markdown vào audit migration.

- [ ] **Step 2: Thay từng module theo thứ tự 00 → 12**

Với mỗi filename:

1. Tìm chính xác filename và ghi knowledge ID bản cũ.
2. Upload một file MD mới cùng tên.
3. Mở bản mới theo thời gian tải lên mới nhất; xác nhận có tóm tắt, có chunk/vector và nội dung dùng một URI mới từ map.
4. Chỉ sau bước 3 mới xóa knowledge ID bản cũ.
5. Tìm lại filename và xác nhận chỉ còn một hàng.

Không chuyển sang file tiếp theo nếu cùng filename còn hai hàng hoặc bản mới không mở được.

- [ ] **Step 3: Kiểm tra inventory sau khi thay đủ 13 file**

Expected: vẫn 24 Documents = 13 Markdown mới + 11 PNG; không có Markdown trùng tên.

### Task 7: Kiểm thử chat và nguồn MinIO mới

**Files:**
- Read live: `Knowledge VNG AI`
- Read: `knowledge-vng/image-map.json`

**Interfaces:**
- Consumes: 13 Markdown mới trong target KB.
- Produces: Ba bằng chứng chat render ảnh và nguồn tham khảo dùng URI từ KB asset mới.

- [ ] **Step 1: Kiểm thử ảnh tổng quan**

Prompt:

```text
Knowledge Base là gì? Hãy trả lời ngắn gọn và hiển thị đúng ảnh trang danh sách Knowledge Base từ nguồn.
```

Expected: câu trả lời có ảnh `01-tong-quan-danh-sach-knowledge.png`.

- [ ] **Step 2: Kiểm thử ảnh đường dẫn tương đối không đạt**

Prompt:

```text
Vì sao không nên dùng đường dẫn assets/... trong Markdown nạp Knowledge VNG? Hãy trả lời kèm ảnh minh họa trường hợp không đạt.
```

Expected: câu trả lời có ảnh `14-chat-khong-hien-thi-duong-dan-tuong-doi.png`.

- [ ] **Step 3: Kiểm thử ảnh Google Drive**

Prompt:

```text
Trong hướng dẫn Google Drive, hãy giải thích cách lọc tệp và gắn tag rồi hiển thị đúng ảnh minh họa.
```

Expected: câu trả lời có ảnh `18-google-drive-loc-tep-va-tag.png`.

- [ ] **Step 4: Kiểm tra nguồn tham khảo của cả ba câu**

Mở document source và chunk chứa ảnh. Expected: URI trùng chính xác value tương ứng trong map mới; không có URI từ snapshot cũ và không có `](assets/...)`.

- [ ] **Step 5: Áp dụng điểm dừng an toàn**

Nếu một trong ba test không render ảnh hoặc nguồn dùng link cũ, dừng tại đây. Không thực hiện Task 8; sửa map/build/Markdown rồi chạy lại cả ba test.

### Task 8: Gỡ 11 PNG khỏi KB sử dụng

**Files:**
- Delete live only after Task 7 passes: `15-google-drive-xac-thuc-service-account.png` … `25-google-drive-dong-bo-thanh-cong.png`
- Preserve: 25 PNG trong KB asset và 25 asset local.

**Interfaces:**
- Consumes: Ba test chat đạt và target đang có 24 Documents.
- Produces: Target KB chỉ còn 13 Markdown.

- [ ] **Step 1: Xác nhận dependency mới tồn tại trước mỗi lần xóa**

Mở KB asset và xác nhận ảnh cùng tên tồn tại. Đối chiếu URI mới trong map.

- [ ] **Step 2: Xóa từng PNG trong `Knowledge VNG AI`**

Tìm chính xác filename, mở menu của hàng PNG, chọn **Xóa**, đọc lại tên trong confirmation dialog rồi xác nhận. Không chọn hàng `.md`; không dùng chọn tất cả.

- [ ] **Step 3: Kiểm tra inventory cuối**

Expected `Knowledge VNG AI`: 13 Documents, tất cả `.md`, không có `.png`.  
Expected `Knowledge VNG - Image Assets`: 25 Documents, tất cả `.png`, không có `.md`.

- [ ] **Step 4: Chạy lại prompt Google Drive sau cleanup**

Expected: ảnh 18 vẫn render sau khi PNG cùng tên đã bị gỡ khỏi KB sử dụng. Nếu không, dừng và không xóa thêm tài nguyên ở KB asset.

### Task 9: Ghi audit và cập nhật tài liệu bàn giao

**Files:**
- Create: `audit/audit-image-assets-migration-2026-08-07.md`
- Modify: `AGENTS.md`
- Modify: `PROJECT.md`
- Modify: `DECISIONS.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`
- Modify: `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`

**Interfaces:**
- Consumes: Mapping mới, output build/test, inventory hai KB và bằng chứng chat.
- Produces: Bàn giao không còn nhắc KB đã xóa như dependency hoạt động.

- [ ] **Step 1: Tạo audit migration**

Audit phải ghi:

- Hai KB ID và tenant.
- Baseline 0 ảnh ở asset KB và 24 tài liệu ở target.
- Danh sách 25 filename → URI mới.
- Kết quả 13 lần thay Markdown.
- Ba prompt kiểm thử và kết quả nguồn.
- Việc gỡ đúng 11 PNG và inventory cuối 25/13.
- Không chứa credential, token hoặc nội dung bí mật.

- [ ] **Step 2: Sửa quy tắc bền vững**

`AGENTS.md`, `PROJECT.md` và `DECISIONS.md` phải ghi:

- `Knowledge VNG - Image Assets` là dependency lâu dài.
- `Knowledge VNG AI` chỉ nhận Markdown.
- Không xóa asset KB khi còn link.
- `Test Doc RAG+Wiki` chỉ là lịch sử đã bị xóa, không còn là KB được phép thao tác.

- [ ] **Step 3: Cập nhật trạng thái và bàn giao**

`STATUS.md` và `HANDOFF.md` phải ghi:

- 25/25 URI thuộc asset KB mới.
- Strict build và 9/9 test đạt.
- Target 13 MD, asset KB 25 PNG.
- Backlog mapping ảnh đóng; không còn bước dọn PNG.

- [ ] **Step 4: Đánh dấu design spec đã triển khai**

Đổi trạng thái trong design spec thành `Đã triển khai và kiểm chứng ngày 07/08/2026`, nhưng chỉ sau khi Task 8 và ba prompt đều đạt.

### Task 10: Verification cuối và bàn giao

**Files:**
- Verify: toàn workspace và hai live KB.

**Interfaces:**
- Consumes: Mọi artifact và audit sau migration.
- Produces: Kết luận hoàn tất có bằng chứng.

- [ ] **Step 1: Chạy strict build lần cuối**

Run:

```powershell
python scripts\build_handbook.py
```

Expected: `Build complete`, `13 modules`, không có warning thiếu mapping.

- [ ] **Step 2: Chạy toàn bộ test lần cuối**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: `Ran 9 tests` và `OK`.

- [ ] **Step 3: Quét tham chiếu trạng thái cũ**

Run:

```powershell
rg -n "Mixed; see provenance|14/25|thiếu 11 mapping|còn chờ mapping|Test Doc RAG\+Wiki" AGENTS.md PROJECT.md STATUS.md HANDOFF.md DECISIONS.md knowledge-vng\image-map.json
```

Expected: không còn trạng thái/mapping cũ; `Test Doc RAG+Wiki` chỉ được phép xuất hiện trong ghi chú lịch sử nói rõ đã bị xóa.

- [ ] **Step 4: Xác nhận live inventory và ảnh sau cleanup**

Expected: asset KB = 25 PNG; target KB = 13 MD; prompt ảnh 18 vẫn render; nguồn dùng URI mới.

- [ ] **Step 5: Cập nhật plan/status của phiên và báo cáo**

Đánh dấu toàn bộ task hoàn tất, dẫn link tới master, module 12, image map, audit, STATUS và HANDOFF. Nêu rõ 11 PNG cũ đã bị gỡ khỏi target và có thể phục hồi từ asset local/asset KB.
