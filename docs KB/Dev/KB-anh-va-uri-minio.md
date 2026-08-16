# KB — Ảnh và URI MinIO

Cơ chế hiển thị ảnh của Knowledge Base VNG AI: vì sao phải dùng `minio://`, lấy URI ở đâu, chọn đúng URI nào, và những bẫy đã gặp thật.

**Phạm vi:** tenant `10012`. Mọi khẳng định dưới đây kèm ngày kiểm chứng.

---

## 1. Sự thật nền: chat KHÔNG render ảnh từ đường dẫn tương đối

**Đã kiểm chứng 06/08/2026, tái kiểm 07/08/2026.**

Nạp file Markdown chứa `![...](assets/xxx.png)` vào KB, nạp cả file ảnh vào cùng KB — chat vẫn **không** hiện ảnh. Câu trả lời có phần "Hình minh họa" nhưng DOM không có thẻ ảnh nào.

```markdown
![Màn hình cấu hình](assets/02-cau-hinh-tong-quan-document.png)   ← KHÔNG render trong chat
```

Đây là kết quả thử trực tiếp, không phải suy đoán từ tài liệu nền tảng. Bằng chứng:

- `so-tay-tao-knowledge-base-v3.md`, khối `MODULE:doc-01-chuan-bi-noi-dung.md`, mục "Ảnh trong file Markdown: hai mục đích, hai đường dẫn".
- Ảnh chứng minh: `knowledge/GS9 Knowledge VNG AI/image-14-chat-khong-hien-thi-duong-dan-tuong-doi.png`.
- Chat test câu 2 ngày 07/08/2026: `docs/superpowers/reports/task-07-chat-image-validation.md`.
- Lặp lại độc lập trên bundle CFL Plan V5 ngày 15/08/2026: `audit/cfl-plan-v5-minio-uri-harvest-2026-08-15.md` ("đường dẫn tương đối `assets/...` không hoạt động").
- Lặp lại lần thứ ba qua Google Drive connector ngày 15/08/2026: nội dung `b.md` sau ingest **vẫn còn nguyên** `![Ảnh test D](D.png)`, connector không tự đổi thành `minio://` (`audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`).

Cách duy nhất đã kiểm chứng để chat render ảnh là dùng URI nội bộ `minio://`.

---

## 2. Hai đường ảnh, hai vai trò (DEC-004)

| Đường | Dùng cho | Ai đọc |
|---|---|---|
| PNG/JPG cục bộ, đường dẫn tương đối | HTML offline, người mở bộ file trên máy | Builder + con người |
| URI `minio://knowledge-base-prd/<tenant>/exports/<uuid>.<ext>` | Chat trên Web | Bộ render chat của Knowledge VNG |

Cả hai phải cùng tồn tại trong file Markdown phát hành. Đổi ảnh thì phải kiểm cả hai đường.

---

## 3. Cú pháp chuẩn

**Đã kiểm chứng — DEC-041, 15/08/2026.**

```markdown
<!-- LOCAL_ASSET: <đường dẫn ảnh local> -->
![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/10012/exports/<uuid>.png)
```

Ví dụ thật từ bộ sổ tay:

```markdown
<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/14-chat-khong-hien-thi-duong-dan-tuong-doi.png -->
![Câu trả lời có mô tả ảnh nhưng không render ảnh khi Markdown dùng đường dẫn tương đối](minio://knowledge-base-prd/10012/exports/227784d8-277b-4198-a8c5-77c3f49f7912.png)
```

Hai dòng, đúng thứ tự: comment trước, link ảnh ngay sau.

### `LOCAL_ASSET` KHÔNG phải link mà chat dùng

`LOCAL_ASSET` là **metadata truy nguyên**, chỉ để builder tìm file ảnh cục bộ khi dựng HTML offline. Chat không đọc dòng này. Xoá nó thì chat vẫn render bình thường nhưng HTML offline mất ảnh.

Nguồn: spec `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md` (quy tắc 4), docstring `scripts/link_plan_v5_minio.py`, module `doc-01`.

### Ảnh render hai lần trong chat — không phải lỗi cú pháp

**DEC-041, đóng 15/08/2026.** Ngày 15/08/2026 chat trên KB `GS9 CFL Plan Version` hiện mỗi ảnh hai lần, kèm ba mảnh cú pháp literal `![` · `](` · `)`. Điều tra: file `.md` local sạch (0 trường hợp URI lọt vào ô alt text trên cả 12 file), bản lưu trên Web ở tab **Toàn văn** render đúng một lần.

Hai phép thử của người dùng chốt lại:

1. KB chỉ chứa `.md`, không upload ảnh vào KB đó → vẫn duplicate.
2. Chat lại lần nữa trên cùng dữ liệu → hiển thị bình thường.

Kết luận: **hành vi không ổn định của model khi soạn câu trả lời** (đôi lúc tự xuất ra `![url](url)`, bộ render chèn `<img>` ở cả hai vị trí). Không sửa file, không sửa script. Giảm nhẹ nếu cần: thêm câu vào System Prompt của Agent bind KB có ảnh, đại ý *"khi trích dẫn ảnh, xuất tham chiếu ảnh đúng một lần, không lặp URI"*.

Bằng chứng: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

---

## 4. Quy trình lấy URI

**Đã kiểm chứng 06–07/08/2026 (25 ảnh), lặp lại 15/08/2026 (29 ảnh Plan V5).**

1. Nạp ảnh làm **tài liệu độc lập** vào một KB Tài liệu **có bật VLM**.
2. Chờ tài liệu ảnh sang trạng thái **Hoàn tất**.
3. Lấy URI `minio://knowledge-base-prd/<tenant>/exports/<uuid>.<ext>` do hệ thống sinh.
4. Chèn URI vào Markdown theo cú pháp mục 3.
5. Nạp lại (hoặc **Phân tích lại**) file Markdown.
6. Hỏi một câu buộc trả lời kèm hình; xác nhận ảnh **thật** xuất hiện, và mở **Nguồn tham khảo** → đúng file `.md` → đọc trực tiếp đoạn nguồn để xác minh URI. Không suy diễn từ blob URL của thẻ `<img>`.

Bước 6 là gate bắt buộc: `docs/superpowers/reports/task-07-chat-image-validation.md` xác minh URI bằng cách đọc Markdown nguồn, không đọc DOM.

### Ba cách lấy URI ở bước 3

| Cách | Thao tác | Trạng thái |
|---|---|---|
| Tóm tắt tự sinh của tài liệu ảnh | Mở tài liệu ảnh, đọc phần tóm tắt — đôi khi lộ thẳng URI | Có điều kiện. `C.png` lộ URI, `D.png` **không** lộ (15/08/2026) |
| Bắt network khi mở **Toàn văn** | Deep-link `.../kb/knowledge/<KB_ID>?tenant_id=10012&knowledge_id=<DOC_ID>` → bấm **Toàn văn** (KHÔNG phải *Xem trước*) → đọc request `GET /kb/v1/api/files?file_path=minio://...` rồi URL-decode | Đã kiểm chứng 15/08/2026 trên 29 ảnh |
| MCP `list_documents` | Trả `file_path` cho toàn bộ tài liệu trong một lệnh | DEC-045, 15/08/2026. Điều kiện: KB phải được share vào space trước. **Dạng `file_path` cho tài liệu ảnh chưa được kiểm chứng** là khớp dạng `.../exports/<uuid>.<ext>` |

Cạm bẫy thao tác đã gặp: menu `...` của tài liệu chỉ có **Phân tích lại / Chuyển / Xóa** — **không có "Sao chép link"**. Với ảnh không tự lộ URI trong tóm tắt, không có đường tắt qua UI (15/08/2026).

---

## 5. Một ảnh sinh NHIỀU URI — bẫy nguy hiểm nhất

**Đã kiểm chứng 15/08/2026** — `audit/cfl-plan-v5-minio-uri-harvest-2026-08-15.md`.

Parser `MinerU` tách thêm ảnh con từ ảnh gốc. Mở **Toàn văn** một tài liệu ảnh có thể nạp **2–10 URI**.

> Chọn nhầm thì ảnh **vẫn hiển thị** nhưng là bản cắt sai. **Không có lỗi nào báo.**

### Quy tắc chọn

**Chính (Đã kiểm chứng):** URI có **byte-size trùng khớp** file gốc trong manifest.

Điều kiện đủ để quy tắc này phân giải duy nhất: mọi kích thước trong manifest phải unique. Với Plan V5 đã kiểm: 29/29 unique.

**Phụ (Có điều kiện):** URI xuất hiện **ĐẦU TIÊN** trong log luôn là ảnh gốc.

Ví dụ `image-29-qbb95-bo-ngua.jpg` (local 21.122 byte, 720×720):

| URI | Bytes | Kết luận |
|---|---|---|
| `.../e6e45329-87e1-4ded-9515-247ff7c4cfde.jpg` | **21.122** | ảnh gốc — chọn |
| `.../86caa5d8-5b21-4c1c-bda9-d4367fb0824d.jpg` | 14.967 | bản MinerU cắt viền — loại |

Mẫu đã đo trực tiếp bằng byte-size (MCP `get_image`):

| Ảnh | Số URI trả về | Bytes đo | Bytes manifest | Kết quả |
|---|---|---|---|---|
| image-02 | 3 | 92.979 | 92.979 | khớp |
| image-04 | 10 | 56.479 | 56.479 | khớp |
| image-24 | 6 (tích luỹ) | 62.368 | 62.368 | khớp |
| image-28 | 2 | 14.242 | 14.242 | khớp |
| image-29 | 2 | 21.122 | 21.122 | khớp |

5/29 đo trực tiếp, phủ ca 2 URI, 3 URI, 10 URI và ca log tích luỹ. 24 ảnh còn lại áp quy tắc "URI đầu tiên" — **phân loại Có điều kiện** tại thời điểm ghi audit.

**Bằng chứng vận hành bổ sung (15/08/2026):** chat trên KB Plan V5 trả về đúng ảnh nội dung được hỏi (ảnh chủ đề Halloween, ảnh lịch nổi bật hoạt động) kèm `Nguồn tham khảo (6 tài liệu)` — chứng minh chuỗi bind + truy hồi + phân giải URI chạy thật và `image-map.json` ánh xạ đúng.

**Hiện tượng lặp lại ở KB khác:** KB test `Test` ngày 15/08/2026, `C.png` cũng sinh 2 URI (`...13b88b2e....png` và `...9b816769....jpg`).

### Phân biệt `.png` và `.jpg` của cùng một ảnh

Với một PNG thật, Knowledge VNG sinh:

- một URI đuôi `.png` — **asset gốc**, dùng cái này;
- một hoặc nhiều URI đuôi `.jpg` — bản **hậu xử lý**, bỏ qua.

Đã quan sát trên `15-google-drive-xac-thuc-service-account.png` ngày 07/08/2026 (`docs/superpowers/reports/task-04-format-debug.md`).

---

## 6. Bẫy PNG giả — file `.png` nhưng payload là JPEG

**Đã kiểm chứng 07/08/2026 — DEC-014.**

### Hiện tượng

Ảnh `01-tong-quan-danh-sach-knowledge.png` đã xử lý xong trong KB. Mở **Xem trước** → inventory mạng phát sinh **11 URI và tất cả đều kết thúc `.jpg`**. Không có URI `.png` nào để chọn.

### Nguyên nhân

Ảnh 01–14 mang đuôi `.png` nhưng byte payload thực tế là JPEG. Knowledge VNG nhận diện **nội dung thật**, không tin phần mở rộng filename, nên xuất asset gốc lẫn hậu xử lý đều dạng `.jpg`.

Khác biệt duy nhất quyết định là **MIME/payload thật của file local** — không phải đuôi file, không phải cấu hình map.

### Cách kiểm — magic bytes

| Định dạng thật | 8 byte đầu |
|---|---|
| PNG | `89 50 4E 47 0D 0A 1A 0A` (`b'\x89PNG\r\n\x1a\n'`) |
| JPEG/JFIF | `FF D8 FF E0 ... JFIF` (`b'\xff\xd8\xff\xe0\x00\x10JF'`) |

Kiểm bằng Pillow hoặc đọc thẳng 8 byte đầu. Test hồi quy đang khoá điều kiện này:

```powershell
python -m unittest -v tests.test_build_handbook.BuildHandbookTests.test_local_png_assets_have_png_signature
```

Test này đã chạy RED đúng mục tiêu trước khi sửa (`docs/superpowers/reports/task-04a-test-red.md`), GREEN sau transcode.

### Cách sửa — thứ tự an toàn đã thực hiện

1. Backup nguyên byte 14 file JPEG cũ vào `audit/image-assets-original-jpeg-mislabeled-2026-08-07/`.
2. Transcode lossless theo pixel sang PNG thật, **giữ nguyên filename và kích thước pixel**.
3. Kiểm magic bytes `89 50 4E 47 0D 0A 1A 0A`.
4. Thử **ảnh 01 trước**; chỉ nạp tiếp 02–14 khi ảnh 01 phát sinh đúng một URI `.png` gốc. Ảnh 01 (554.0 KB) sinh `minio://knowledge-base-prd/10012/exports/78c9450c-2273-45fe-84b1-09f217328b53.png`.
5. Nạp bản đúng, xác nhận **Hoàn tất**.
6. Chỉ sau khi đủ 25 tên / 25 URI không trùng / đúng tenant / đúng đuôi `.png` mới cập nhật `image-map.json` **một lần**.
7. Xoá tuần tự 14 bản cũ theo bộ ba điều kiện **tên file + dung lượng cũ + knowledge ID**; mỗi lần chỉ xoá khi bản mới cùng tên vẫn còn.

**Quy tắc rút ra (DEC-014):** không đổi đuôi JPEG thành `.png` để giả định dạng. Transcode và kiểm signature **trước** khi upload/build.

---

## 7. Tự động hoá — `scripts/link_plan_v5_minio.py`

Script đọc `image-map.json` (filename → URI MinIO) rồi viết lại link trong `.md`.

Hai regex nó xử lý:

```python
# ![alt](assets/name.jpg)  — ảnh nhúng, sẽ render trong chat
EMBED_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\(assets/(?P<name>[^)]+)\)")
# [text](assets/name.jpg)  — link tham chiếu trong registry ảnh
LINK_RE  = re.compile(r"(?<!!)\[(?P<text>[^\]]*)\]\(assets/(?P<name>[^)]+)\)")

LOCAL_ASSET_TMPL = "<!-- LOCAL_ASSET: assets/{name} -->"
```

Hành vi cần biết:

- **Idempotent**: chạy nhiều lần cho cùng kết quả; không nhân đôi `LOCAL_ASSET`, không sửa link đã là `minio://`.
- Chèn `LOCAL_ASSET` **ngay trước** dòng ảnh nhúng.
- Với link registry, nếu text hiển thị bắt đầu bằng `assets/` thì đổi thành tên file, cho khỏi hiểu nhầm là còn dùng đường dẫn cục bộ.
- Validate map trước khi ghi: đúng `knowledge_base_id`, phủ đủ asset trên đĩa, mọi URI đúng tiền tố `minio://knowledge-base-prd/10012/exports/`, không URI trùng.
- `--check` để dry-run.

**Cảnh báo bảo trì:** 12 file `.md` của Plan V5 là artifact sinh từ `convert_cfl_plan_html.py`. Chạy lại converter sẽ ghi đè link MinIO về `assets/...`; phải chạy lại `link_plan_v5_minio.py` sau đó.

Kết quả chạy 15/08/2026: 29 ảnh nhúng + 29 link registry trên 7/12 file → tổng 58 link `minio://`, 29 comment `LOCAL_ASSET`, 0 link tương đối còn sót. Chạy lại: `0 thay đổi`.

---

## 8. Bảng cạm bẫy — tra nhanh

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Chat mô tả ảnh nhưng không hiện ảnh | Markdown dùng đường dẫn tương đối | Thay bằng URI `minio://` (mục 4) |
| Ảnh hiện nhưng là bản cắt sai, không báo lỗi | Chọn nhầm URI con do MinerU tách | Đối chiếu byte-size với manifest (mục 5) |
| Không tìm được URI `.png` nào, chỉ toàn `.jpg` | File `.png` có payload JPEG | Kiểm magic bytes, transcode (mục 6) |
| Ảnh hiện hai lần + mảnh `![` `](` `)` literal | Model tự xuất `![url](url)` | Không sửa file. DEC-041 (mục 3) |
| Ảnh không lấy được URI qua tóm tắt | Tài liệu ảnh không tự lộ URI | Bắt network khi mở **Toàn văn** (mục 4) |
| Link MinIO biến mất sau khi chạy converter | Artifact sinh bị ghi đè | Chạy lại `link_plan_v5_minio.py` (mục 7) |

---

## 9. Ràng buộc vòng đời

- **DEC-005 (Đang áp dụng):** không xoá ảnh nguồn hoặc KB chứa ảnh khi còn Markdown tham chiếu URI đó.
- **DEC-015 (Đang áp dụng):** thứ tự thay ảnh bắt buộc là **asset host → map → strict build → replace MD → chat test → cleanup PNG**. Không đảo thứ tự, không cleanup trước chat test.
- Nếu KB cấp URI bị xoá, phải coi **toàn bộ mapping liên quan là cần tái kiểm chứng**, kể cả khi một số link vẫn tạm thời render.
- URI gắn cứng vào KB đã cấp. Chuyển ảnh sang KB mới = upload lại = URI mới = chạy lại toàn bộ quy trình thu URI.

---

## 10. Chưa kiểm chứng

- **Dạng `file_path` mà MCP `list_documents` trả về cho tài liệu ảnh** — chưa đối chiếu với dạng `.../exports/<uuid>.<ext>` mà `image-map.json` dùng. DEC-045 ghi rõ phải kiểm trước khi dùng làm nguồn ghi map.
- **Quy tắc "URI đầu tiên = ảnh gốc"** — mới đo byte-size trực tiếp 5/29 ảnh. 24 ảnh còn lại là *Có điều kiện*.
- **Text chunk thô của tài liệu chứa ảnh** — tab `Xem phân đoạn` bị kẹt cuộn, chưa đọc được. Vì vậy chưa loại trừ tuyệt đối giả thuyết "parser lúc nạp viết lại markdown thay alt text bằng đường dẫn ảnh" bằng bằng chứng chunk (hai phép thử ở mục 3 đã loại trừ bằng đường khác).
- **Vòng đời object trên MinIO** — chưa biết object tồn tại bao lâu, có bị GC khi tài liệu ảnh gốc bị xoá khỏi KB hay không. Suy luận hiện tại (DEC-051) là URI tĩnh và độc lập với document, nhưng chưa test bằng cách xoá tài liệu ảnh.
- **Sửa trực tiếp nội dung/caption của chính tài liệu ảnh** rồi xem URI có đổi không.
- **Ảnh nạp qua Google Drive connector có sinh URI theo cùng cơ chế không** — mọi ảnh đã lấy URI đều nạp bằng upload tay hoặc do người dùng upload.

---

## Nguồn

- `audit/audit-image-assets-migration-2026-08-07.md`
- `audit/cfl-plan-v5-minio-uri-harvest-2026-08-15.md`
- `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`
- `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`
- `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`
- `docs/superpowers/reports/task-04-format-debug.md`, `task-04a-test-red.md`, `task-07-chat-image-validation.md`
- `so-tay-tao-knowledge-base-v3.md`, khối `MODULE:doc-01-chuan-bi-noi-dung.md`
- `scripts/link_plan_v5_minio.py`
- `DECISIONS.md`: DEC-004, DEC-005, DEC-014, DEC-015, DEC-041, DEC-045, DEC-051
