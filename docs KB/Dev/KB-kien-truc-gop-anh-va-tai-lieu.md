# KB — Kiến trúc lưu ảnh: từ tách hai KB đến gộp một KB

Lịch sử kiến trúc lưu ảnh của bộ sổ tay `GS9 Knowledge VNG AI`: vì sao từng tách ảnh ra KB riêng, vì sao đã gộp lại, và thực nghiệm nào chứng minh gộp là an toàn.

**Đọc kèm:** [`KB-anh-va-uri-minio.md`](KB-anh-va-uri-minio.md) — cơ chế URI MinIO và cú pháp nhúng ảnh.

---

## 1. Dòng thời gian

| Ngày | Kiến trúc | Quyết định |
|---|---|---|
| 06/08/2026 | Hai đường ảnh: local cho HTML offline, MinIO cho chat | DEC-004 |
| 07/08/2026 | **Tách**: KB asset giữ 25 PNG, KB consumer giữ 13 MD | DEC-011 → DEC-012 |
| 11/08/2026 | Vẫn tách, mở rộng: 34 PNG / 14 MD | DEC-019 |
| 12/08/2026 | Vẫn tách, mở rộng: 49 PNG / 20 MD | DEC-024, DEC-025 |
| 15/08/2026 | **Gộp**: 49 ảnh + 20 doc chung một KB `GS9 Knowledge VNG AI` | DEC-043, DEC-044 |
| 16/08/2026 | Thực nghiệm xác nhận gộp là an toàn | DEC-051 |

---

## 2. Kiến trúc CŨ — tách KB asset và KB consumer

**Triển khai và kiểm chứng 07/08/2026.** Spec: `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`. Audit: `audit/audit-image-assets-migration-2026-08-07.md`.

### Cấu trúc

```text
knowledge-vng/assets/*.png
        │
        │ upload một lần
        ▼
Knowledge VNG - Image Assets          ← KB asset (asset host)
  6da8657c-dd96-4170-a698-074043475014
        │
        │ 25 URI minio://
        ▼
knowledge-vng/image-map.json
        │
        │ strict build
        ├──────────────► knowledge-vng/00–12.md
        │                         │
        │                         │ upload CHỈ Markdown
        │                         ▼
        │                Knowledge VNG AI          ← KB consumer
        │                  cefadf09-4187-46ac-a765-591e3255a4a4
        │
        └──────────────► so-tay-tao-knowledge-base.html
                          dùng ảnh local/data URI
```

Vai trò: **KB asset sở hữu vòng đời ảnh. KB consumer chỉ tiêu thụ URI qua Markdown.** Cùng tenant `10012`, nhưng consumer không phụ thuộc vào việc ảnh xuất hiện như tài liệu trong chính nó.

### Vì sao từng chọn tách

Lý do được ghi trong spec 07/08/2026:

1. **Sạch corpus truy hồi.** Consumer chỉ chứa 13 Markdown thay vì 24 tài liệu (13 MD + 11 PNG). Ảnh độc lập nằm chung sẽ vào corpus của Agent như tài liệu bình thường.
2. **Ổn định URI.** 14 ảnh nền trước đó phụ thuộc KB `Test Doc RAG+Wiki` — KB đó đã bị người dùng xoá (DEC-017). Bài học: không được giả định URI từ một KB đã xoá sẽ tồn tại bền vững. Toàn bộ ảnh phải chuyển sang một host ổn định và cấp lại URI từ host đó.
3. **Vòng đời tách bạch.** KB asset là dependency lâu dài, không được xoá khi Markdown còn tham chiếu (DEC-005). Tách ra thì ranh giới "được xoá / không được xoá" rõ ràng.
4. **Chống upload nhầm.** Quy tắc ghi vào master: không upload thư mục `assets/` hoặc PNG cùng gói Markdown vào KB consumer, để agent hoặc human sau này không làm bẩn consumer.

### Kết quả kiểm chứng 07/08/2026

| KB | Inventory cuối |
|---|---|
| `Knowledge VNG - Image Assets` | 25 PNG, 0 MD; 25/25 **Hoàn tất** |
| `Knowledge VNG AI` | 13 MD, 0 PNG; 13/13 **Hoàn tất** |

Ba phép thử chat trước cleanup đều PASS; một phép thử hậu-cleanup PASS với 7 nguồn đều là `.md`, không có nguồn `.png` (`docs/superpowers/reports/task-07-chat-image-validation.md`).

Migration đi đúng thứ tự an toàn: mỗi Markdown cũ chỉ bị xoá sau khi bản mới cùng tên đã **Hoàn tất**; 11 PNG chỉ bị dọn sau khi ba gate chat đạt.

---

## 3. Kiến trúc MỚI — gộp ảnh và tài liệu chung một KB

**DEC-043 và DEC-044, 15/08/2026.**

### Nội dung quyết định

Gộp vật lý 49 PNG từ `GS9 Knowledge VNG - Image Assets` vào cùng thư mục `GS9 Knowledge VNG AI`, đổi tên theo quy ước `image-NN-...` (DEC-042). Bỏ khái niệm `ASSET_KB_NAME` / asset-dir riêng trong `build_handbook.py`; `local_asset_prefix` đổi thành `.` (cùng thư mục).

DEC-043 **thay thế** DEC-012, DEC-019, DEC-024.

### Nội dung KB sau khi gộp (DEC-044)

| KB | Nội dung | Số tài liệu |
|---|---|---|
| `GS9 Knowledge VNG AI` | Tài liệu Knowledge Base (`doc-00`→`doc-12`) + Agent (`doc-13`→`doc-19`) + 49 ảnh của chính hai tính năng đó | 69 |
| `GS9 CFL Knowledge Agent` | 6 Agent mặc định + 10 Agent custom CFL + cấu trúc/KB riêng của CFL | 28 |

`GS9 Knowledge VNG AI` được định vị lại là **tri thức nền tảng dùng chung cho cả team GS9**.

Nội dung nghiệp vụ của 20 module **không đổi** — chỉ đổi tên file và gộp thư mục ảnh.

### Trạng thái trên Web tại thời điểm quyết định

DEC-043 ghi rõ: KB Web `GS9 Knowledge VNG - Image Assets` (`6da8657c-...`) **chưa bị xoá hay đổi tên trên Web** — chỉ local đã gộp. Xoá KB đó trên Web phải chờ Phase 3 (Drive sync) hoàn tất và chat-test đạt, giữ nguyên tinh thần DEC-005.

`image-map.json` ghi rõ URI hiện tại **vẫn do KB cũ cấp** cho tới khi resync.

---

## 4. Thực nghiệm xác nhận — DEC-051, 16/08/2026

Câu hỏi cần trả lời: gộp ảnh và tài liệu chung một KB có an toàn không, khi tài liệu khác trong cùng KB bị sửa nội dung rồi sync lại? Nếu không an toàn thì phải quay về kiến trúc tách.

**Thiết lập:** KB test `Test` (`d7295a59-03b1-496c-86eb-9ecaa3364aa7`), nạp qua Google Drive connector.

| File | Vai trò |
|---|---|
| `C.png` | ảnh, tài liệu độc lập |
| `D.png` | ảnh, tài liệu độc lập |
| `a.md` | nhóm **đối chứng** — nhúng ảnh C qua URI MinIO |
| `b.md` | nhóm **thử nghiệm** — nhúng ảnh D qua URI MinIO |

Cả `a.md` và `b.md` dùng đúng cú pháp chuẩn `<!-- LOCAL_ASSET: ... -->` + `minio://...`.

### Ba vòng test

| Vòng | Cấu hình sync | Thao tác | Kết quả |
|---|---|---|---|
| 1 | Toàn bộ + Ghi đè + Mọi tệp | Sync lần đầu | 4 file **Hoàn tất**, ingest sạch |
| 2 (16/08) | **Tăng dần** + Ghi đè + Mọi tệp | Thêm đoạn "Sửa lần 2" vào `b.md`, **giữ nguyên dòng ảnh D** | `b.md` được re-ingest (nội dung mới hiển thị, thời gian tải lên cập nhật `Aug 16, 2026, 4:40:37 AM`). **Ảnh D vẫn hiển thị đúng** |
| 3a (16/08) | **Toàn bộ** + Ghi đè + Mọi tệp | **Không sửa file nào** | "Ghi đè không có hiệu lực" — không thấy dấu hiệu re-ingest rõ ràng |
| 3b (16/08) | **Toàn bộ** + Ghi đè + Mọi tệp | Thêm file mới `e.md`; sửa nội dung **cả** `a.md` (ảnh C) và `b.md` (ảnh D), giữ nguyên dòng ảnh ở cả hai | `e.md` ingest đủ pipeline, KB tăng từ 4 lên 5 tài liệu. `b.md` hiện đúng nội dung "Sửa lần 3". **Ảnh C và D vẫn còn nguyên.** `C.png`/`D.png` vẫn là tài liệu độc lập, không bị xoá hay tạo trùng |

### Kết luận

Gộp ảnh + tài liệu chung một KB **AN TOÀN** khi tài liệu khác trong cùng KB được sửa nội dung và sync lại — **cả chế độ Tăng dần lẫn Toàn bộ** — miễn là dòng ảnh (URI MinIO) không bị đụng tới trong lần sửa.

Phủ: 2 chế độ đồng bộ × 3 lần sửa nội dung (`b.md` ×2, `a.md` ×1). Không có trường hợp nào ảnh bị mất hay đổi link.

### Lý do kỹ thuật

> Link ảnh nhúng trong `a.md`/`b.md` là **URI MinIO tĩnh trỏ thẳng vào MinIO**, không phải tham chiếu động vào document `C.png`/`D.png` trong KB.

Nên ảnh "sống" hay "chết" trong tài liệu **không** phụ thuộc việc tài liệu ảnh gốc có được re-sync hay không. Nó phụ thuộc hai điều kiện:

1. Object đó còn tồn tại trên MinIO.
2. Pipeline ingest của connector không sửa/chuẩn hoá lại dòng ảnh khi re-ingest tài liệu chứa nó.

**Lưu ý phân loại:** DEC-051 ghi đây là **lý do suy ra, không xác minh bằng log connector**.

### Giới hạn xác minh của thực nghiệm

- **Không so sánh được `knowledge_id`.** Kế hoạch ban đầu là dùng `knowledge_id` làm chỉ số so sánh chính. MCP không truy cập được KB `Test` (`list_knowledge_bases` không thấy KB; tra thẳng bằng ID trả `not found or not accessible`) — có thể do phạm vi KB đã đăng ký cho MCP server bị giới hạn ở KB production.
- Kết luận dựa hoàn toàn trên **quan sát UI**: nội dung xem trước, ảnh render, danh sách tài liệu, timestamp tải lên. Không dựa trên log hệ thống.

### Hệ quả

Không cần hoàn tác kiến trúc gộp của `GS9 Knowledge VNG AI`. Phase 3 (sync thật cho KB production) có thể tiếp tục theo kế hoạch đã gộp.

---

## 5. Một nghi ngờ đã được loại trừ dọc đường

Ngày 15/08/2026, khi chat trên KB `GS9 CFL Plan Version` (12 Markdown **+ 29 JPEG chung một KB**) hiện mỗi ảnh hai lần, **nghi phạm số một được nêu là chính việc gộp ảnh chung KB**. Lập luận khi đó: bộ sổ tay dùng đúng y hệt cú pháp nhưng ảnh nằm ở KB riêng và chat render bình thường; khác biệt cấu trúc duy nhất giữa hai KB là chỗ để ảnh.

| | Sổ tay (lúc đó) | Plan V5 |
|---|---|---|
| Ảnh | KB riêng `GS9 Knowledge VNG - Image Assets` | **Cùng KB** với Markdown |
| KB tiêu thụ | 20 Markdown, 0 ảnh | 12 Markdown + 29 JPEG |

Audit khi đó cảnh báo rằng nếu giả thuyết này đúng thì **xung đột với quyết định gộp**, và phải đưa lại cho người dùng chọn: tách KB ảnh, hay đổi định dạng nhúng.

Giả thuyết bị **bác bỏ cùng ngày** bằng hai phép thử: (1) KB chỉ chứa `.md` có link ảnh, không upload ảnh vào KB đó → vẫn duplicate; (2) chat lại lần nữa trên cùng dữ liệu → hiển thị bình thường. Kết luận là hành vi không ổn định của model (DEC-041), không liên quan cấu trúc KB.

Ghi lại ở đây vì đây là lần duy nhất kiến trúc gộp bị nghi ngờ, và vì nó minh hoạ nguyên tắc: **chạy phép thử đối chứng trước khi sửa file theo giả thuyết**. Bằng chứng: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

---

## 6. So sánh hai kiến trúc

| Tiêu chí | Tách (cũ) | Gộp (mới) |
|---|---|---|
| Số KB phải quản | 2 | 1 |
| Ảnh trong corpus truy hồi của consumer | Không | Có — ảnh là tài liệu độc lập trong cùng KB |
| Nguồn tham khảo của câu trả lời | Chỉ `.md` (đã kiểm 07/08/2026) | Có thể gồm cả tài liệu ảnh — **chưa đo** |
| Rủi ro xoá nhầm host ảnh | Cao — KB asset phải được đánh dấu "không được xoá" | Thấp hơn — ảnh nằm cùng KB đang dùng |
| Cấu hình builder | `ASSET_KB_NAME` + asset-dir riêng | `local_asset_prefix = "."` |
| Sửa nội dung tài liệu khác rồi sync | — | An toàn, đã kiểm chứng (DEC-051) |
| Sync bằng Google Drive connector | Phải trỏ 2 thư mục | Một KB một thư mục con (DEC-046) |

---

## 7. Chưa kiểm chứng

Những điều dưới đây **chưa ai thử**. Không suy diễn từ kết quả DEC-051.

### Về connector và vòng đời file ảnh

- **Đổi tên tệp ảnh** qua connector rồi sync lại — URI MinIO có đổi không, ảnh trong Markdown có chết không.
- **Di chuyển tệp ảnh** sang thư mục khác trong phạm vi sync.
- **Xoá tệp ảnh** khỏi nguồn Drive (kèm hoặc không kèm bật **Đồng bộ xóa**) — object MinIO còn tồn tại không.
- DEC-046 ghi rõ: hành vi đổi tên khi sync (135 file đổi tên trong phiên 15/08) **chưa được kiểm chứng trên nền tảng**; bắt buộc thử trên 2–3 file trước khi sync toàn bộ.

### Về sửa chính tài liệu ảnh

- **Sửa trực tiếp nội dung/caption/tóm tắt của chính `C.png`/`D.png`** trong khi `a.md`/`b.md` không đổi. DEC-051 ghi đây là case biên nằm ngoài phạm vi câu hỏi gốc, chưa test.
- **Sửa đúng dòng ảnh** trong tài liệu Markdown rồi sync lại. Mọi vòng test đều cố ý **giữ nguyên** dòng ảnh — điều kiện "miễn không đụng dòng ảnh" chưa từng bị vi phạm để xem chuyện gì xảy ra.
- **Phân tích lại** (re-analyze) một tài liệu ảnh — URI cũ còn hợp lệ không.

### Về kiến trúc gộp trên KB production

- **Sync thật cho `GS9 Knowledge VNG AI` với layout đã gộp.** DEC-046 ghi Phase 3 chưa thực hiện, cần go-ahead riêng.
- **URI sau resync.** `image-map.json` hiện ghi URI do KB `GS9 Knowledge VNG - Image Assets` cấp. Sau khi 49 ảnh được nạp lại vào `GS9 Knowledge VNG AI` qua connector, URI mới sẽ khác — chưa thu, chưa map, chưa chat-test.
- **Xoá KB `GS9 Knowledge VNG - Image Assets` trên Web.** Chưa làm, và theo DEC-043/DEC-005 chỉ được làm sau khi Phase 3 hoàn tất và chat-test đạt.
- **Ảnh có lọt vào `Nguồn tham khảo` của câu trả lời không** khi ảnh và Markdown chung KB. Ở kiến trúc tách, 07/08/2026 đo được 7/7 nguồn là `.md`. Ở kiến trúc gộp chưa đo.
- **Chất lượng truy hồi** khi corpus có thêm 49 tài liệu ảnh — chưa benchmark.

### Bất nhất tài liệu cần biết

Master `so-tay-tao-knowledge-base-v3.md`, khối `MODULE:doc-01-chuan-bi-noi-dung.md`, mục **"Hai KB, hai vai trò"** vẫn đang mô tả **kiến trúc CŨ**:

> "KB asset giữ 49 ảnh PNG độc lập… KB sử dụng chỉ nhận 20 file Markdown… Không upload folder ảnh hoặc PNG cùng bộ Markdown vào KB này."

Nội dung này **mâu thuẫn với DEC-043/DEC-044** đã chốt ngày 15/08/2026. Master chưa được cập nhật theo quyết định gộp. Khi sửa, nhớ DEC-001: sửa ở master rồi để builder sinh lại module, không sửa trực tiếp module sinh.

---

## Nguồn

- `docs/superpowers/specs/2026-08-07-image-assets-kb-design.md`
- `audit/audit-image-assets-migration-2026-08-07.md`
- `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`
- `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`
- `docs/superpowers/reports/task-07-chat-image-validation.md`
- `so-tay-tao-knowledge-base-v3.md`, khối `MODULE:doc-01-chuan-bi-noi-dung.md`
- `DECISIONS.md`: DEC-004, DEC-005, DEC-011, DEC-012, DEC-017, DEC-019, DEC-024, DEC-025, DEC-041, DEC-042, DEC-043, DEC-044, DEC-046, DEC-051
