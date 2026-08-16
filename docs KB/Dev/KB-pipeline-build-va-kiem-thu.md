# KB — Pipeline build và bộ kiểm thử

**Đối tượng:** Dev sắp chạy hoặc sắp sửa script. Người cần biết *cái gì sinh ra cái gì, cái gì bị ghi đè, và chạy xong thì lấy gì làm bằng chứng đạt*.
**Ngày viết:** 16/08/2026 (bản chiều — thay bản sáng cùng ngày, xem mục 8).
**Cách kiểm chứng:** đọc mã nguồn 3 script + 3 file test; chạy `python -m unittest discover -s tests -v`, `python scripts/link_plan_v5_minio.py --check` và gọi trực tiếp `load_source_from_dirs()` trong phiên 16/08/2026. **Không sửa file nào trong `scripts/` hay `tests/`.**

**Nguồn:** `scripts/*.py`, `tests/*.py`, `AGENTS.md` mục "Build và kiểm tra", `DECISIONS.md` DEC-001, 003, 016, 021, 026, 032, 033.

**Chồng lấn có chủ đích:** quy ước tên và các con số hợp đồng nằm ở `KB-quy-uoc-dat-ten-va-hop-dong-artifact.md`; tài liệu này chỉ mô tả **cơ chế** sinh ra chúng. Cách gắn URI MinIO cho ảnh xem thêm `KB-anh-va-uri-minio.md`.

---

## 1. Bảng tổng: NGUỒN → SCRIPT → ĐẦU RA

| # | NGUỒN | SCRIPT | ĐẦU RA | Nguồn có trong repo? |
|---|---|---|---|---|
| 1 | `docs KB/Human/**/doc-*.md` (nếu có)<br>`docs KB/Human/_master-header.txt` (tuỳ chọn)<br>**fallback:** `so-tay-tao-knowledge-base-v3.md` ở root<br>`knowledge/GS9 Knowledge VNG AI/image-map.json` | `scripts/build_handbook.py` | `knowledge/GS9 Knowledge VNG AI/doc-NN-*.md` (20 file)<br>`so-tay-tao-knowledge-base.html` (root, tự chứa) | **Có** — hiện chạy bằng nhánh fallback (mục 2.1) |
| 2 | `CFL5_0- Plan Ver 5.0-14082026.html` — SHA-256 `593c3428…` | `scripts/convert_cfl_plan_html.py` | `knowledge/GS9 CFL Plan Version/V5/doc-v5-NN-*.md` (12 file)<br>`…/V5/assets/image-v5-NN-*.jpg` (29 file)<br>`…/V5/source-manifest.json` | **Không** — chỉ nằm trên máy công ty |
| 3 | `knowledge/GS9 CFL Plan Version/V5/image-map.json`<br>12 file `doc-v5-*.md` do bước 2 sinh<br>29 JPEG trong `V5/` | `scripts/link_plan_v5_minio.py` | **ghi đè tại chỗ** 12 file `doc-v5-*.md` (đổi link ảnh → `minio://…`, chèn `LOCAL_ASSET`) | Có |

Ba pipeline **độc lập**. Không script nào gọi script khác. Nhưng bước 3 phụ thuộc đầu ra của bước 2 và bị bước 2 xoá sổ nếu chạy lại — xem mục 5.

> **Chú ý ngay dòng này:** bước 2 ghi ảnh vào `V5/assets/`, còn bước 3 (từ 16/08/2026) đọc ảnh ở `V5/` phẳng. Hai script **không còn đồng bộ về vị trí ảnh**. Đây là cạm bẫy 6.2, phải đọc trước khi chạy lại converter.

---

## 2. `scripts/build_handbook.py` — pipeline sổ tay

### 2.1 Nạp nguồn — `load_source_from_dirs()`

Hàm này ghép nguồn thành một chuỗi "master ảo" rồi trả về cho phần còn lại của builder:

```text
docs KB/Human/_master-header.txt          -> header (thiếu thì chuỗi rỗng)
docs KB/Human/doc-*.md         (phẳng)    -> bọc <!-- MODULE:<tên file> --> … <!-- /MODULE -->
docs KB/Human/KB/doc-*.md      (sorted)   -> bọc tương tự
docs KB/Human/Agent/doc-*.md   (sorted)   -> bọc tương tự
```

Ba điểm về cơ chế:

1. **Quét cả thư mục phẳng lẫn thư mục con.** `search_dirs = [human_dir] + [human_dir / sub for sub in HUMAN_SOURCE_SUBDIRS]` với `HUMAN_SOURCE_SUBDIRS = ("KB", "Agent")`. Comment trong mã ghi rõ lý do: *"Quét cả hai để việc đổi bố cục không làm gãy build."*
2. **Chống trùng theo tên file.** Tập `seen` giữ tên đã nạp; file cùng tên ở thư mục con sẽ **bị bỏ qua** nếu bản phẳng đã được nạp trước. Thư mục phẳng thắng.
3. **Fallback về master ở root.** Nếu không tìm được file `doc-*.md` nào, hàm đọc `so-tay-tao-knowledge-base-v3.md`. Chỉ khi **cả hai** đều không có mới ném `ValueError: Không tìm thấy nguồn nào trong … và cũng không có master gốc.`

Tên module = **tên file nguồn** (hoặc tên trong marker `MODULE` của master khi chạy fallback).

> **Thay đổi 16/08/2026:** trước đó builder đọc thẳng master ở root. Hằng `HUMAN_SOURCE_DIR_NAME = "docs KB/Human"` và `HUMAN_SOURCE_SUBDIRS` là mới. Master ở root **không bị bỏ**, nó tụt xuống vai trò fallback.

**Trạng thái đo được 16/08/2026 (chiều):** `docs KB/Human/` tồn tại nhưng **rỗng** — không có `doc-*.md`, không có thư mục con `KB/` hay `Agent/`. Nên builder đang chạy bằng **nhánh fallback**. Gọi trực tiếp hàm để xác nhận:

```text
source len: 99145
modules: 20
first 3: ['doc-00-gioi-thieu-va-quick-start.md', 'doc-01-chuan-bi-noi-dung.md', 'doc-02-tao-kb-nhanh-va-nang-cao.md']
last:    doc-19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md
fallback used: True
```

Đủ 20 module, đúng tên. **Build chạy được.** Đây là điểm khác biệt lớn nhất so với bản viết buổi sáng cùng ngày — khi đó mã chưa có nhánh fallback nên build ném lỗi.

### 2.2 Biến đổi

| Bước | Hàm | Việc |
|---|---|---|
| 1 | `extract_modules` | Nâng cấp heading: `##`→`#`, `###`→`##`, … Mỗi module vì vậy có đúng một H1 |
| 2 | `replace_images_outside_fences` + `replace_image` | Mỗi `![alt](path)` → `<!-- LOCAL_ASSET: ./<tên file> -->` + `![alt](<URI MinIO>)`. Ảnh trong code fence **không** bị đụng |
| 3 | `rebase_master_relative_links` | Link tài liệu tương đối được rebase về vị trí thư mục đầu ra. Bỏ qua link tuyệt đối, neo `#`, và scheme `xxx:` |
| 4 | `write_modules` | Ghi từng module, **chèn dòng đầu** `<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->` |
| 5 | `build_offline_html` | Tách `##` thành section, render Markdown → HTML, **nhúng ảnh thành data URI base64**, gắn CSS/JS inline |

`local_asset_prefix = "."` — ảnh nằm cùng thư mục với module (DEC-043). Không còn `ASSET_KB_NAME` hay thư mục asset riêng.

> **Dòng marker cũng đổi 16/08/2026.** Trước đây marker trỏ về master ở root; nay ghi `docs KB/Human/`. Vì mã dọn file cũ chỉ so **tiền tố** `"<!-- GENERATED FILE - sửa nội dung tại "` nên đổi phần đuôi này không phá logic dọn — xem 2.4.

### 2.3 Gate — build đỏ khi nào

| Gate | Điều kiện đỏ | Thông báo |
|---|---|---|
| Có nguồn | không có `doc-*.md` **và** không có master fallback | `Không tìm thấy nguồn nào trong … và cũng không có master gốc.` |
| Đúng số module | `len(extracted) != 20` | `Expected 20 modules, found N` |
| Đủ URI MinIO | có ảnh không có key trong `image-map.json` | `Missing MinIO mappings: …` |
| Một H1 mỗi module | `count_h1(rendered) != 1` | `<tên> must contain exactly one H1` |
| Mỗi module có ảnh | không có ảnh ngoài code fence | `<tên> must contain at least one image` |
| Ảnh MinIO | không có ảnh nào bắt đầu `minio://` | `<tên> must contain a MinIO image` |
| HTML offline không remote | ảnh `http://`, `https://`, `minio://` khi nhúng | `Offline HTML cannot embed remote image: …` |
| Ảnh không thoát root | đường dẫn ảnh ra ngoài build root | `Image escapes build root: …` |
| Ảnh tồn tại | file ảnh không có trên đĩa | `Missing image: …` |
| HTML tự chứa | HTML chứa `src="http`, `<script src=`, `<link rel="stylesheet"` | `Offline HTML contains forbidden resource: …` |
| HTML có ảnh nhúng | không có chuỗi `data:image/` | `Offline HTML does not contain embedded images` |

`--allow-missing-minio` chỉ tắt gate "Đủ URI MinIO" và gate "Ảnh MinIO". **Không dùng cho bản bàn giao** (DEC-010, `AGENTS.md`).

Lưu ý thứ tự: gate "đúng 20 module" chạy **trước** mọi thao tác ghi; các gate còn lại chạy **sau** khi 20 file đã nằm trên đĩa. Nghĩa là một lỗi H1 sẽ để lại 20 file đã ghi rồi mới báo đỏ.

### 2.4 Logic dọn file cũ — `LEGACY_GENERATED_MODULE_NAMES`

Sau khi ghi thành công 20 module, builder duyệt danh sách **21 tên cũ** và xoá file nếu **và chỉ nếu** nội dung file bắt đầu bằng chuỗi `"<!-- GENERATED FILE - sửa nội dung tại "`.

Ba điểm cần nắm:

1. **Chỉ xoá artifact do chính builder sinh.** File người dùng tự đặt cùng tên sẽ không có dòng marker nên không bị xoá. Comment trong mã ghi rõ: *"never prune arbitrary user files from the module directory"*.
2. **So khớp theo tiền tố**, không so khớp cả dòng. Nên file sinh bởi phiên bản builder cũ (marker trỏ master ở root) **vẫn** bị nhận diện và dọn đúng. Đây là lý do việc đổi đuôi marker ở 2.2 an toàn.
3. Danh sách hiện gồm `13-tao-va-van-hanh-agent.md` (bản Agent gộp trước v3.3, DEC-023) và **20 tên không tiền tố** `00-…` → `19-…` — di sản của lần đổi tên sang `doc-` (DEC-042). Danh sách này chỉ nới ra, không co lại.

### 2.5 HTML offline (DEC-003)

Một file duy nhất ở root, không phụ thuộc tài nguyên ngoài. Ảnh nhúng base64, CSS và JS viết inline trong chuỗi Python. Metadata `Phiên bản` / `Cập nhật` được đọc từ dòng `> Phiên bản:` và `> Cập nhật:` trong header nguồn; thiếu header thì hiển thị `không ghi`.

Kích thước thực tế của `so-tay-tao-knowledge-base.html` ngày 16/08/2026: **30.859.005 byte** (mtime 06:40). Đó là hệ quả trực tiếp của việc nhúng 49 PNG dạng base64.

---

## 3. `scripts/convert_cfl_plan_html.py` — sinh bundle Plan V5

```powershell
python scripts\convert_cfl_plan_html.py <đường-dẫn-HTML-nguồn> "knowledge\GS9 CFL Plan Version\V5"
```

### 3.1 Kiểm tra hợp đồng nguồn trước khi làm gì

Script từ chối chạy nếu HTML nguồn không khớp:

| Hằng | Giá trị |
|---|---|
| `EXPECTED_SOURCE_SHA256` | `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038` |
| `section_count` | 9 |
| `group_count` | 29 |
| `item_count` | 115 |
| `figure_count` | 14 |
| `image_count` | 29 |
| `placeholder_count` | 2 |
| `schedule_placeholder_count` | 1 |
| `dom_or_inline_hidden_element_count` | 0 |

Đây là chuyển đổi **xác định**: cùng HTML vào thì ra đúng cùng bộ byte. Test `test_conversion_has_complete_deterministic_shape` chứng minh bằng cách convert hai lần rồi so hash toàn cây.

### 3.2 Đầu ra

| Loại | Số lượng | Tên |
|---|---|---|
| Module chỉ mục | 1 | `doc-v5-00-index-va-pham-vi.md` |
| Module theo section | 9 | `doc-v5-01-…` → `doc-v5-09-…` (ánh xạ `ov`, `sched`, `gameplay`, `system`, `quality`, `supply`, `act`, `biz`, `pub`) |
| Danh mục ảnh | 1 | `doc-v5-10-danh-muc-hinh-anh.md` |
| Ghi chú/truy nguyên | 1 | `doc-v5-11-ghi-chu-va-truy-nguyen.md` |
| Ảnh | 29 | **`assets/image-v5-NN-<slug alt>.jpg`** |
| Manifest | 1 | `source-manifest.json` |

`VERSION_TAG = "v5"` là hằng ở đầu file — đổi sang `"v6"` là cách sinh bundle V6 mà không đụng logic (DEC-042).

Ảnh được **giải mã từ data URI trong HTML** rồi ghi ra đĩa, kèm `sha256`, `bytes`, `width`, `height` vào manifest.

**Điểm chốt:** `extract_assets()` vẫn khoá cứng `assets_dir = output_dir / "assets"` và ghi `relative_path = f"assets/{filename}"` (kiểm tra mã 16/08/2026). Converter **chưa** được sửa theo bố cục phẳng mới. Xem 6.2.

### 3.3 `cleanup_previous_generated_files` — xoá gì

Chạy **trước** khi sinh mới. Đọc `source-manifest.json` cũ, lấy mảng `generated_files` (hiện có **42 mục**: 12 MD + 29 JPEG + 1 manifest) và `unlink()` từng file.

Chốt an toàn: mỗi đường dẫn được `resolve()` và phải nằm trong `output_dir`, nếu không thì `ValueError: Unsafe generated path in previous manifest`. Manifest hỏng hoặc thiếu → bỏ qua bước dọn, không lỗi.

**Điểm yếu đã hiện thực, kiểm chứng 16/08/2026:** manifest hiện tại đăng ký ảnh ở dạng `assets/image-v5-01-….jpg`, nhưng 29 ảnh thật đang nằm phẳng trong `V5/`. Hệ quả nếu chạy lại converter:

- Bước dọn tìm `V5/assets/image-v5-NN-….jpg` → **không thấy** → 29 ảnh phẳng **không bị xoá**.
- `extract_assets()` **tạo lại** `V5/assets/` và ghi 29 ảnh mới vào đó.
- Kết quả: **hai bộ 29 ảnh cùng tên ở hai chỗ**, và `link_plan_v5_minio.py` (đọc `V5/` phẳng) sẽ thấy bộ cũ chứ không phải bộ mới sinh.

Đây là suy luận từ mã, chưa dựng lại được vì thiếu HTML nguồn — nhưng cả ba mảnh bằng chứng (hằng trong `extract_assets`, nội dung `generated_files`, vị trí ảnh thật) đều đọc trực tiếp được.

---

## 4. `scripts/link_plan_v5_minio.py` — gắn URI MinIO cho bundle V5

```powershell
python scripts\link_plan_v5_minio.py --check    # chỉ kiểm tra, không ghi
python scripts\link_plan_v5_minio.py            # ghi vào 12 file .md
```

### 4.1 Vì sao cần

Đường dẫn tương đối **không hoạt động** khi Markdown nạp vào KB trên Web — chat không render được ảnh. Script đổi target link sang URI MinIO, giữ một comment `LOCAL_ASSET` để truy nguyên file cục bộ.

### 4.2 Bố cục ảnh — thay đổi 16/08/2026

| Hằng | Giá trị hiện tại | Trước 16/08 |
|---|---|---|
| `BUNDLE` | `knowledge/GS9 CFL Plan Version/V5` | như cũ |
| `ASSETS` | **`= BUNDLE`** (ảnh nằm thẳng trong `V5/`) | `BUNDLE / "assets"` |
| `EMBED_RE` | `!\[…\]\((?:assets/)?(?P<name>image-v5-[^)/]+)\)` — **nhận cả hai dạng** | chỉ dạng có `assets/` |
| `LINK_RE` | tương tự, có `(?:assets/)?` | chỉ dạng có `assets/` |
| `LOCAL_ASSET_TMPL` | `<!-- LOCAL_ASSET: {name} -->` — **tên trần** | `<!-- LOCAL_ASSET: assets/{name} -->` |

Comment trong mã ghi lý do giữ nhánh `assets/` trong regex: *"Vẫn nhận dạng tiền tố `assets/` cũ để bundle sinh trước 16/08 chạy lại được."* Nghĩa là script **đọc được cả hai bố cục** nhưng **chỉ ghi ra dạng tên trần**.

### 4.3 Kiểm tra `image-map.json` trước khi ghi (`load_map`)

| Kiểm tra | Lỗi khi sai |
|---|---|
| File tồn tại | `Chưa có …/image-map.json` + hướng dẫn quy trình lấy URI |
| Có khoá `images` là dict không rỗng | `image-map.json phải có khóa 'images' …` |
| `knowledge_base_id == 1452bc9a-c8b4-487b-b623-34e0b00a83e9` | `knowledge_base_id phải là …` |
| Mọi `*.jpg` trong `ASSETS` đều có URI | `N asset chưa có URI: …` |
| Map không chứa tên không tồn tại trên đĩa | `Map có N tên không tồn tại trong assets/: …` |
| Mọi URI bắt đầu `minio://knowledge-base-prd/10012/exports/` | `N URI không đúng tiền tố …` |
| URI không trùng nhau | `Có N URI bị trùng; mỗi ảnh phải có URI riêng` |

> **Bẫy đọc lỗi:** thông báo dòng thứ năm vẫn ghi nguyên văn `"không tồn tại trong assets/"` dù `ASSETS` nay là `V5/` phẳng. Nếu gặp lỗi này, **đừng đi tìm thư mục `assets/`** — nó nói rằng map có key không khớp file `.jpg` nào trong `V5/`.

### 4.4 Hai phép thay thế

| Dạng gặp | Kết quả |
|---|---|
| `![alt](image-v5-NN-x.jpg)` hoặc `![alt](assets/image-v5-NN-x.jpg)` — ảnh nhúng | dòng `<!-- LOCAL_ASSET: image-v5-NN-x.jpg -->` chèn ngay trên, link đổi thành `![alt](minio://…)` |
| `[text](image-v5-NN-x.jpg)` — link trong registry ảnh (file `doc-v5-10`) | `[image-v5-NN-x.jpg](minio://…)`; nhãn hiển thị đổi từ đường dẫn sang **tên file** cho khỏi nhầm là còn dùng đường dẫn cục bộ |

**Idempotent:** chạy nhiều lần cho cùng kết quả. Không nhân đôi comment `LOCAL_ASSET` (kiểm tra dòng liền trước), không đụng link đã là `minio://`.

**`--check`** báo cáo mà không ghi. Mã thoát: `0` đạt, `1` có tham chiếu không có URI, `2` lỗi map hoặc không thấy file `.md`.

Chạy thật ngày 16/08/2026:

```text
sẽ đổi: 0 ảnh nhúng + 0 link registry trên 0 file (tổng 12 file .md).
Ảnh có URI trong map: 29.
```

Mã thoát `0`. Bundle **đã ở trạng thái đã gắn link**, không còn gì để đổi — đúng như kỳ vọng của một script idempotent chạy lần thứ hai.

---

## 5. Cái gì ghi đè / xoá cái gì

| Script | Ghi đè | Xoá | Không bao giờ đụng |
|---|---|---|---|
| `build_handbook.py` | 20 file `knowledge/GS9 Knowledge VNG AI/doc-NN-*.md`<br>`so-tay-tao-knowledge-base.html` (root) | 21 tên trong `LEGACY_GENERATED_MODULE_NAMES`, **chỉ khi** file bắt đầu bằng marker `<!-- GENERATED FILE - sửa nội dung tại ` | Nguồn trong `docs KB/Human/`, master ở root, ảnh `image-*.png`, `image-map.json` |
| `convert_cfl_plan_html.py` | 12 MD + 29 JPEG + `source-manifest.json` trong thư mục đầu ra | Mọi file liệt kê trong `generated_files` của manifest **cũ** (42 mục) | File ngoài `output_dir` (chặn bằng kiểm tra `resolve()`); `image-map.json` |
| `link_plan_v5_minio.py` | 12 file `V5/doc-v5-*.md` **tại chỗ** | Không xoá gì | `image-map.json`, ảnh, manifest |

### Thứ tự bắt buộc

```text
convert_cfl_plan_html.py   ->  sinh 12 MD với link ảnh cục bộ
        │                      (ghi đè, xoá bản cũ theo manifest)
        v
link_plan_v5_minio.py      ->  đổi link sang minio://
                               (chạy lại converter = mất hết, phải chạy lại bước này)
```

Cảnh báo này nằm ngay trong docstring của `link_plan_v5_minio.py`: *"12 file `.md` là artifact sinh. Nếu chạy lại `convert_cfl_plan_html.py`, link MinIO sẽ bị ghi đè … và phải chạy lại script này."*

### Thứ tự thay ảnh sổ tay (DEC-015)

```text
đặt ảnh vào GS9 Knowledge VNG AI  ->  cập nhật image-map.json  ->  strict build
   ->  phát hành Markdown  ->  chat-test nguồn/ảnh
```

Không đảo thứ tự. Không cleanup PNG trước chat-test. Không xoá PNG khi còn Markdown tham chiếu (DEC-005).

---

## 6. Cạm bẫy đã gặp thật

### 6.1 Nguồn `docs KB/Human/` rỗng — build vẫn xanh, và đó mới là vấn đề

Kiểm chứng 16/08/2026:

```text
docs KB/
├── Dev/       (19 file .md)
└── Human/     <-- RỖNG
```

Builder **không báo lỗi** vì nhánh fallback nhặt master ở root. Hệ quả:

- Dòng marker sinh ra ghi `sửa nội dung tại docs KB/Human/` — trỏ vào một thư mục **rỗng**. Ai làm theo chỉ dẫn đó sẽ tạo file mới ở `docs KB/Human/`, và lần build kế tiếp sẽ nhặt file mới đó **thay vì** master, có thể ra số module khác 20 rồi đỏ gate.
- `so-tay-tao-knowledge-base-v3.md` vẫn là nguồn thật nhưng **không tài liệu nào nói vậy** — `AGENTS.md` và `PROJECT.md` (15/08) vẫn ghi master là nguồn chuẩn, đúng, nhưng không nhắc `docs KB/Human/` tồn tại.
- **Không tài liệu sống nào nhắc `docs KB/`.** `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md`, `DECISIONS.md` đều chưa ghi cấu trúc này. **Chưa có mã DEC nào** cho thay đổi 16/08.

**Cách nhận biết đang chạy nhánh nào:** nếu `docs KB/Human/` không có file `doc-*.md` nào thì đang chạy fallback.

### 6.2 Converter và linker lệch nhau về vị trí ảnh

| | `convert_cfl_plan_html.py` | `link_plan_v5_minio.py` |
|---|---|---|
| Vị trí ảnh | ghi ra `V5/assets/` | đọc ở `V5/` phẳng |
| Ngày sửa gần nhất | chưa sửa | 16/08/2026 |
| Trạng thái đĩa 16/08 | — | khớp (29 JPEG phẳng, `assets/` không tồn tại) |

Bố cục phẳng là trạng thái **hiện hành và đang chạy đúng**: `--check` trả mã `0`, `test_link_plan_v5_minio.py` xanh, 29 `LOCAL_ASSET` đều là tên trần (đếm được `0` comment còn tiền tố `assets/`).

Nhưng converter chưa theo. Chạy lại nó sẽ sinh ra kịch bản hai bộ ảnh ở mục 3.3. Và `test_convert_cfl_plan_html.py` dòng 94 vẫn khẳng định `len(list((output / "assets").glob("*.jpg"))) == 29` — nghĩa là **test đang khoá converter vào bố cục cũ**. Sửa converter mà không sửa test sẽ làm đỏ test đó.

Lịch sử: lần đầu ảnh bị làm phẳng là 15/08/2026, khi người dùng đổi tên `knowledge/GS9 Plan Version/` → `knowledge/GS9 CFL Plan Version/`; khi đó cách xử lý là **khôi phục lại `V5/assets/`** (`STATUS.md`). Lần 16/08 chọn hướng ngược lại: **giữ phẳng, sửa script theo**. Hai lần, hai cách xử lý trái nhau — đó là lý do converter bị bỏ lại phía sau.

### 6.3 12 file V5 là artifact sinh nhưng KHÔNG có dòng cảnh báo

Đây là cạm bẫy nguy hiểm nhất của bundle Plan Version.

| | 20 module sổ tay | 12 module Plan V5 |
|---|---|---|
| Dòng đầu file | `<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->` | `# Knowledge Base — Nội Dung Phiên Bản CFL 5.0` |
| Nhìn dòng đầu có biết là file sinh không? | **Có** | **Không** |
| Chạy lại pipeline thì mất sửa tay không? | Có | **Có** |

Kiểm chứng 16/08/2026 bằng cách đọc dòng đầu từng file: `doc-v5-00-index-va-pham-vi.md` bắt đầu bằng `# Knowledge Base — Nội Dung Phiên Bản CFL 5.0`; `doc-v5-10-danh-muc-hinh-anh.md` bằng `# Danh Mục Hình Ảnh Và Figure`; `doc-v5-11-ghi-chu-va-truy-nguyen.md` bằng `# Ghi Chú Và Truy Nguyên`. **Không file nào có marker.**

Hậu quả: người mở file thấy một tài liệu Markdown bình thường, sửa tay một câu, rồi mất trắng khi ai đó chạy `convert_cfl_plan_html.py` — mà **cleanup còn xoá file trước khi ghi đè**, nên không có gì để so sánh.

Cách duy nhất hiện có để biết đây là file sinh:

- `V5/source-manifest.json` liệt kê chúng trong `generated_files`.
- Docstring của `link_plan_v5_minio.py`.
- Không có dấu hiệu nào **trong chính file**.

**Quy tắc làm việc cho tới khi có marker:** trước khi sửa bất kỳ file `.md` nào trong `knowledge/GS9 CFL Plan Version/V5/`, mở `source-manifest.json` và kiểm tra tên file có nằm trong `generated_files` không. Nếu có, sửa ở HTML nguồn hoặc ở converter, không sửa file.

### 6.4 Nguồn HTML của Plan V5 không có trong repo

`CFL5_0- Plan Ver 5.0-14082026.html` chỉ tồn tại trên máy công ty. Test tìm nó ở `C:\Users\CPU13114\Downloads\…`, ghi đè được bằng biến môi trường `CFL_PLAN_V5_HTML`. Trên máy không có file, 6 test của `test_convert_cfl_plan_html.py` **skip**, không fail.

Hệ quả: bundle V5 **không dựng lại được** trên máy hiện tại. Phiên 15/08/2026 phải đổi tên 12 MD + 29 JPEG **thủ công** thay vì chạy lại converter (`STATUS.md`). Cùng lý do đó, kịch bản hai bộ ảnh ở 3.3 chưa ai dựng lại được để xác nhận.

### 6.5 Bốn thế hệ gate, DEC chưa theo kịp

| DEC | Ngày | Gate | Trạng thái |
|---|---|---|---|
| DEC-016 | 07/08/2026 | 13 module, 11/11 test | Được thay thế |
| DEC-021 | 11/08/2026 | 14 module, 11/11 test | Được thay thế |
| DEC-026 | 12/08/2026 | 20 module, 13 test | Được thay thế |
| DEC-032 | 14/08/2026 | 20 module, **16 test** | Ghi "Đang áp dụng" |

Nhưng `AGENTS.md` (15/08/2026) ghi gate là **`Ran 29 tests`/`OK`** với 6 skip, và đó là con số đo được thật. **DEC-032 chưa được cập nhật** sau khi thêm `test_convert_cfl_plan_html.py` và `test_link_plan_v5_minio.py`. Lấy DEC-032 làm chuẩn sẽ ra kết luận sai.

### 6.6 Master từng bị thất lạc một lần (DEC-033)

Ngày 14/08/2026 master bị mất trong lần di chuyển workspace. Được **phục hồi từ 20 module phát hành** bằng biến đổi xác định và kiểm tra round-trip trước khi ghi: 20/20 module sau build khớp nội dung cũ, chỉ khác đường dẫn `LOCAL_ASSET` và hai link audit. Backup nguyên byte: `audit/workspace-normalization-prebuild-2026-08-14.zip` (và `audit/workspace-docs-before-normalization-2026-08-14.zip`).

Bài học: pipeline một chiều master → module **có thể đảo ngược** vì biến đổi là xác định — nhưng chỉ khi artifact còn nguyên.

---

## 7. Bộ kiểm thử

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

### 7.1 Ba file test

| File | Số test | Phạm vi |
|---|---:|---|
| `tests/test_build_handbook.py` | **16** | Master, layout, PNG signature, image-map, hành vi `write_modules`/`extract_modules`/`count_h1`, HTML offline, build end-to-end trong tempdir, và contract của project sống |
| `tests/test_convert_cfl_plan_html.py` | **6** | Hợp đồng nguồn HTML, hình dạng chuyển đổi xác định, phủ toàn bộ text ngữ nghĩa, mọi item có title + description, manifest giữ đúng thứ tự DOM, asset/link hợp lệ. **Toàn bộ skip nếu không có HTML nguồn** |
| `tests/test_link_plan_v5_minio.py` | **7** | Ảnh nhúng nhận URI + comment, link registry đổi nhãn thành tên file, idempotent, asset thiếu map bị báo và giữ nguyên, bundle sống có đúng 29 embed + 29 registry link, không còn link tương đối sót, map trỏ đúng KB ID |

Tổng **29 test**.

Hai nhóm khác nhau về bản chất:

- **Test đơn vị** — dựng fixture trong `tempfile.TemporaryDirectory()`, không đụng project sống. Ví dụ `test_build_project_creates_twenty_modules_including_agent_deep_split` tự tạo `docs KB/Human/KB` + `Agent` giả rồi build. Test này là bằng chứng duy nhất cho biết **nhánh thư mục con vẫn chạy đúng**, vì project sống đang chạy nhánh fallback.
- **Test contract project sống** — đọc thẳng `knowledge/GS9 Knowledge VNG AI/` và `knowledge/GS9 CFL Plan Version/V5/`. Đây là nhóm biến động theo trạng thái repo.

### 7.2 Kết quả chạy ngày 16/08/2026 (chiều)

```text
Ran 29 tests in 0.327s
OK (skipped=6)
```

23 pass, 6 skip, **0 fail, 0 error**. Sáu test skip đều thuộc `test_convert_cfl_plan_html.py` với lý do đồng nhất:

```text
skipped 'Source HTML not available: C:\Users\CPU13114\Downloads\CFL5_0- Plan Ver 5.0-14082026.html'
```

Đây là mức skip **bình thường** trên máy này (`AGENTS.md` đã dự liệu: *"6 skip nếu máy không có file HTML nguồn Plan V5"*).

> Bản viết buổi sáng 16/08 của chính tài liệu này ghi `FAILED (failures=3, errors=1, skipped=6)`. Con số đó đúng **tại thời điểm đó** — khi thư mục `knowledge/GS9 Knowledge VNG AI/` còn rỗng và ảnh V5 chưa khớp script. Trạng thái đã được khôi phục trong ngày. Giữ ghi chú này để ai đọc bản cũ không tưởng bộ test đang hỏng.

#### Và rồi đỏ lại lúc 17:40 — một ca mẫu về "test contract project sống"

Chạy lần thứ hai trong cùng phiên:

```text
FAIL: test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs
AssertionError: 59 != 60
Ran 29 tests … FAILED (failures=1, skipped=6)
```

Sáu phút giữa hai lần chạy, không ai đụng `scripts/` hay `tests/`. Thủ phạm truy được bằng mtime: `knowledge/GS9 Knowledge VNG AI/doc-02-tao-kb-nhanh-va-nang-cao.md` mang mtime **17:37**, còn 19 module kia đều **06:40**. Dòng ảnh của nó bị đổi từ dạng `exports/<uuid>` sang dạng `<doc_id>/<uuid>` — dạng thứ hai mà DEC-045 ghi là *chưa biết có render được trong chat không* — và **không khớp `image-map.json`**.

Đây là **sửa tay vào artifact sinh**, đúng thứ DEC-001 cấm và đúng thứ dòng marker ở đầu file cảnh báo. Lần build kế tiếp sẽ ghi đè mất, vì builder lấy URI từ map chứ không từ file.

Ba bài học vận hành:

- **Test contract project sống làm đúng việc.** Nó không đo logic script; nó đo *hợp đồng của repo*, nên nó là thứ duy nhất bắt được thay đổi đến từ bên ngoài pipeline.
- **Đỏ không phải lúc nào cũng là lỗi mã.** Ở đây mã hoàn toàn đúng; dữ liệu mới là thứ lệch. Đọc thông báo lỗi rồi so mtime trước khi đi sửa script.
- **Không tự hoàn tác.** Đây là thay đổi của người khác đang dở dang. Ghi nhận trạng thái thật, báo lại, không đảo ngược (tinh thần DEC-050).

### 7.3 Gate bàn giao hiện hành (`AGENTS.md`, 15/08/2026)

| Điều kiện gate | Đo được 16/08/2026 | Đạt? |
|---|---|---|
| strict build, không `--allow-missing-minio` | nguồn nạp được 20 module qua fallback | Có điều kiện — xem ghi chú dưới |
| đúng 20 module tên `doc-NN-…` | 20 file `.md` trong KB nền tảng | Đạt |
| 49 PNG tên `image-NN-…`, cùng thư mục | 49 file `.png` | Đạt |
| `image-map.json` 49 key / 49 URI duy nhất | `49 / 49`, `knowledge_base_id = cefadf09-…` | Đạt |
| 60 link MinIO + 60 `LOCAL_ASSET` | 17:34 `60`/`60` · 17:40 `59`/`60` | **Vỡ lúc 17:37** (xem 7.2) |
| HTML offline tự chứa | 30.859.005 byte, mtime 16/08 06:40 | Đạt |
| `Ran 29 tests` / `OK` (6 skip) | 17:34 `OK (skipped=6)` · 17:40 `FAILED (failures=1)` | **Không đạt từ 17:40** |

**Ghi chú về dòng đầu:** trong phiên này **không chạy `build_handbook.py` ở chế độ ghi** — chỉ gọi `load_source_from_dirs()` và `extract_modules()` để xác nhận nguồn nạp được đủ 20 module, tránh ghi đè 20 artifact đang khớp hợp đồng. Vì vậy dòng đó là *Có điều kiện*: nguồn đã chứng minh đủ, nhưng chuỗi gate phía sau (H1, ảnh, MinIO, HTML) chưa được chạy lại sau lần sửa mã 16/08.

Các dòng còn lại đo trực tiếp trên artifact đang nằm trên đĩa nên là *Đã kiểm chứng*.

### 7.4 Kỷ luật khi sửa test

Kế hoạch 15/08 ghi rõ: **không nới lỏng test để cho qua sau khi đổi tên.** Phiên 15/08 tuân thủ — cập nhật tên kỳ vọng và bỏ hằng `ASSET_KB_NAME`, nhưng giữ nguyên độ chặt của assertion. Phiên 16/08 cũng vậy: `test_link_plan_v5_minio.py` đổi `ASSETS = BUNDLE` cho khớp bố cục mới chứ không hạ assertion `29 embed / 29 registry`.

Giữ nguyên tắc này. Test đỏ vì hợp đồng vỡ là test đang làm đúng việc.

---

## 8. Ghi chú về chính tài liệu này

Bản buổi sáng 16/08/2026 mô tả một trạng thái repo **đã không còn đúng** vào buổi chiều cùng ngày: khi đó `build_handbook.py` chưa có nhánh fallback, thư mục `knowledge/GS9 Knowledge VNG AI/` còn rỗng, ảnh V5 chưa khớp script, và bộ test đỏ 4 lỗi.

Ba mục bị viết lại hoàn toàn: **2.1** (nạp nguồn), **6.2** (vị trí ảnh V5) và **7.2/7.3** (kết quả test và gate). Mục **6.3** (12 file V5 không có marker) giữ nguyên vì đã kiểm chứng lại và vẫn đúng.

Bài học vận hành: tài liệu Dev mô tả trạng thái repo có **hạn dùng tính bằng giờ** khi repo đang tái cấu trúc. Mọi khẳng định ở đây đều gắn ngày; gặp mâu thuẫn thì chạy lại lệnh kiểm chứng ở đầu file chứ đừng tin con số.

---

## Chưa kiểm chứng và rủi ro còn lại

**Chưa kiểm chứng:**

- **Chưa chạy `build_handbook.py` ở chế độ ghi** sau lần sửa mã 16/08. Nhánh fallback đã chứng minh nạp đủ 20 module, nhưng các gate phía sau (H1, ảnh, MinIO, HTML offline) chưa được chạy lại end-to-end trên project sống. Xem 7.3.
- **Không biết `docs KB/Human/KB` và `/Agent` từng có nội dung hay chưa.** Hai thư mục con này được mã và test giả định là tồn tại nhưng hiện không có trên đĩa. Chưa xác định là dự định tương lai hay là dấu vết của một bố cục đã bị dời.
- **Chưa chạy `convert_cfl_plan_html.py`** vì thiếu HTML nguồn. Toàn bộ mô tả hành vi của script này là **đọc mã**, không phải quan sát chạy thật, trừ phần cấu trúc đầu ra đối chiếu với `source-manifest.json` có sẵn.
- **Kịch bản hai bộ ảnh trùng** (mục 3.3) là **suy luận từ mã**, chưa dựng lại được vì thiếu nguồn.
- **Chưa kiểm chứng hành vi connector Google Drive với việc đổi tên/di chuyển/xoá** (`audit/audit-google-drive-connector-2026-08-07.md` mục 6). Riêng câu hỏi "sửa nội dung tài liệu khác có làm mất ảnh nhúng không" đã có câu trả lời **an toàn** ở cả hai chế độ sync (DEC-051, 16/08/2026) — nhưng kết luận đó dựa trên quan sát UI, không phải log hệ thống.

**Rủi ro còn lại:**

- **Converter chưa theo bố cục phẳng.** Chạy lại nó hôm nay là sinh ra hai bộ ảnh. Sửa nó cần sửa đồng thời `test_convert_cfl_plan_html.py` dòng 94 và `generated_files` trong manifest — ba chỗ, một lần.
- **Hai pipeline, hai chuẩn cảnh báo.** Sổ tay có marker, Plan V5 không. Chừng nào chưa thống nhất, cạm bẫy 6.3 còn nguyên. Chèn marker vào converter là thay đổi nhỏ nhưng **cần phê duyệt riêng** vì nó đổi byte đầu ra của 12 file và làm lệch mọi hash đã lưu.
- **Fallback che lỗi cấu hình.** Nguồn rỗng mà build vẫn xanh nghĩa là không có gate nào bắt được việc `docs KB/Human/` bị bỏ trống. Marker sinh ra lại trỏ đúng vào thư mục rỗng đó.
- **`_master-header.txt` thiếu không gây lỗi.** Phiên bản và ngày cập nhật trên HTML âm thầm thành `không ghi`.
- **Đường dẫn HTML nguồn cứng trong test** trỏ vào profile người dùng cụ thể (`CPU13114`). Trên máy khác luôn skip, nên 6 test đó gần như không bao giờ chạy trong thực tế — và `EXPECTED_SOURCE_SHA256` vì vậy chưa từng được đối chiếu lại kể từ 14/08.
- **DEC-032 lệch với `AGENTS.md`** về số test. Phải sửa DEC hoặc ghi rõ DEC-032 đã bị thay thế.
- **Thay đổi mã ngày 16/08 chưa có mã DEC.** Nhánh fallback, `HUMAN_SOURCE_DIR_NAME`, `ASSETS = BUNDLE` và dòng marker mới đều là quyết định kiến trúc nhưng không tra ngược được vào `DECISIONS.md`.
- **`convert_cfl_plan_html.py` xoá trước, ghi sau.** HTML sai hợp đồng bị bắt trước khi xoá, nhưng lỗi ghi đĩa giữa chừng thì không — bundle có thể còn lại một phần. Không có bước backup trong script.
