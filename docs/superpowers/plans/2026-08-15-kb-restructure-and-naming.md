# Kế hoạch — Chuẩn hóa tên tài liệu và tái cấu trúc 2 KB nền tảng

**Ngày:** 15/08/2026 · **Bản sửa 3** (bỏ hạng mục sửa lỗi duplicate ảnh — cú pháp hiện tại đúng)
**Trạng thái:** Kế hoạch **ĐÃ CHỐT**, chưa thực hiện bước nào.
**Ràng buộc cứng:** chỉ đổi tên file và sửa link — **không đổi nội dung tài liệu**. Xem mục ngay trước Phase 1.
**Yêu cầu gốc:** (1) ~~sửa lỗi duplicate ảnh~~ — **đã bỏ, cú pháp hiện tại đúng**; (2) đổi tên toàn bộ theo `image-`/`doc-` và tái cấu trúc; (3) phân vai lại 2 KB nền tảng. **Đưa lên Web bằng Google Drive connector, không upload tay.**
**Bằng chứng nền:** `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`, `docs/superpowers/specs/2026-08-15-kb-architecture-design.md`

---

## 0. Bối cảnh

### 0.1 Ghi chú lịch sử — lỗi duplicate ảnh KHÔNG phải việc phải làm

Từng nghi ngờ file `.md` hoặc cấu trúc KB sai. Người dùng đã kiểm chứng và chốt: **cú pháp gắn link ảnh hiện tại hoàn toàn đúng**, hiện tượng nhân đôi chỉ là hành vi không ổn định của model khi soạn câu trả lời. **Hạng mục này đã bỏ khỏi kế hoạch, không sửa gì cả.** Bằng chứng lịch sử: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

Cú pháp chuẩn giữ nguyên:

```markdown
<!-- LOCAL_ASSET: <đường dẫn cục bộ> -->
![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/10012/exports/<uuid>.<ext>)
```

### 0.2 Có đường tắt rẻ để thu URI — MCP đọc được KB đã share

Đã kiểm chứng: `list_documents` trên KB `GS9 Knowledge VNG AI` (`cefadf09-...`, đang share vào space `CFL Member`) trả về **toàn bộ 20 tài liệu kèm `file_path`** trong **một lệnh duy nhất**:

```
"file_name": "13-agent-tong-quan-va-kien-truc.md",
"file_path": "minio://knowledge-base-prd/10012/b751c4c3-.../3a1f2340-....md"
```

KB `GS9 Knowledge VNG - Image Assets` **không** share nên MCP trả `not found or not accessible` — xác nhận điều kiện là *KB phải được share vào space*.

**Ý nghĩa:** phiên trước tốn ~100 lượt thao tác browser để thu 29 URI. Nếu KB được share, việc đó rút xuống **1–2 lệnh MCP**. Đây là thứ quyết định toàn bộ chi phí Phase 3.

**CÒN PHẢI KIỂM CHỨNG:** dạng `file_path` trả về là `minio://.../10012/<doc_id>/<uuid>.md` — **khác** dạng `minio://.../10012/exports/<uuid>.png` mà `image-map.json` đang dùng và đang chạy đúng. Chưa biết với tài liệu ảnh thì `file_path` là dạng nào, và dạng nào render được trong chat. Xem 3.1.

---

## RÀNG BUỘC CỨNG — KHÔNG ĐỔI NỘI DUNG TÀI LIỆU

Người dùng chốt: **chỉ đổi tên file và gắn lại link cho đúng sau khi phân bổ lại cấu trúc thư mục. Không đổi nội dung.**

| Được phép đổi | Không được đổi |
|---|---|
| Tên file | Bất kỳ câu chữ, tiêu đề, bảng, thứ tự mục nào |
| Đường dẫn trong `<!-- LOCAL_ASSET: ... -->` | Phần mô tả trong `![mô tả](...)` |
| URI `minio://...` (bắt buộc đổi vì sync lại sinh URI mới) | Cấu trúc heading, số thứ tự mục |
| Marker `<!-- MODULE:... -->` trong master (chính là tên file) | Nội dung bên trong marker |

### Cách kiểm chứng — chạy trước và sau, phải khớp

Chuẩn hóa nội dung bằng cách bỏ hết ba thứ được phép đổi rồi so hash. Nếu hash trùng thì chắc chắn nội dung không bị đụng:

```python
# Bo dong LOCAL_ASSET, thay moi URI minio bang placeholder, roi hash
norm = re.sub(r'<!-- LOCAL_ASSET:[^>]*-->
?', '', text)
norm = re.sub(r'minio://[^)\s]+', 'URI', norm)
hashlib.sha256(norm.encode()).hexdigest()
```

Chạy trên **cả 20 module + 25 file meta-KB + 12 Markdown Plan V5** trước khi đổi, lưu lại bảng hash, rồi chạy lại sau khi đổi xong. **Bất kỳ hash nào lệch = đã lỡ đụng nội dung, phải hoàn tác.**

Với 20 module sinh từ master: rebuild có thể sinh lại nội dung, nên phép kiểm này càng cần thiết — nó bắt được cả trường hợp builder vô tình đổi cách render.

### Ngoại lệ đã được yêu cầu riêng

Ba file mới ở mục 2.2 (`doc-30`, `doc-31`, `doc-32` về cấu trúc KB của CFL) là **tạo mới**, không phải sửa nội dung file cũ — nằm ngoài ràng buộc này. Nếu người dùng muốn hoãn phần này thì Phase 2.2 chỉ còn việc đổi tên 25 file.

---

## Phase 1 — Đổi tên toàn bộ (thuần local, làm được ngay)

### 1.1 Luật đặt tên

| Loại | Tiền tố | Ví dụ |
|---|---|---|
| Ảnh | `image-` | `image-01-tong-quan-danh-sach-knowledge.png` |
| Tài liệu không phải ảnh | `doc-` | `doc-00-gioi-thieu-va-quick-start.md` |

**Ngoại lệ:** tài liệu đồng bộ từ Google Drive — người dùng tự đổi, agent KHÔNG đụng.

**KB nhiều phiên bản** (`GS9 CFL Plan Version`): chèn phiên bản vào giữa — `doc-v5-00-...`, `image-v5-01-...`. Giải quyết luôn nguy cơ V6 trùng tên V5.

Vì người dùng **upload lại toàn bộ**, lần này đổi tên cả 29 JPEG của Plan V5 luôn — khuyến nghị "giữ nguyên để bảo toàn URI" ở bản 1 không còn ý nghĩa.

### 1.2 Bảng công việc

| Nhóm | Số file | Cách làm |
|---|---:|---|
| 20 module sổ tay | 20 | Sửa marker `<!-- MODULE:doc-NN-....md -->` trong master → strict build. Thêm 20 tên cũ vào `LEGACY_GENERATED_MODULE_NAMES` để builder tự dọn |
| 49 PNG sổ tay | 49 | Đổi tên file + 49 khóa trong `image-map.json` |
| 25 file meta-KB | 25 | Đổi tên trực tiếp (không có ảnh, không phụ thuộc gì) |
| 12 Markdown Plan V5 | 12 | Sửa `convert_cfl_plan_html.py` sinh `doc-v5-NN-...` → chạy lại converter → chạy lại `link_plan_v5_minio.py` |
| 29 JPEG Plan V5 | 29 | Đổi tên file + 29 khóa `image-map.json` |

### 1.3 Việc kỹ thuật kéo theo

- `scripts/build_handbook.py`: `ASSET_KB_NAME`, `local_asset_prefix`, `LEGACY_GENERATED_MODULE_NAMES`
- `tests/test_build_handbook.py`: 16 test khóa tên/layout — cập nhật đồng bộ, **không nới lỏng test để cho qua**
- `scripts/convert_cfl_plan_html.py` + `tests/test_convert_cfl_plan_html.py`
- `scripts/link_plan_v5_minio.py` + test: chỉ đổi tên file, **không đổi cú pháp**
- 60 comment `LOCAL_ASSET` trong 20 module: đổi đường dẫn theo Phase 2

---

## Phase 2 — Tái cấu trúc nội dung 2 KB nền tảng

Không còn bị chặn bởi Phase 0.

### 2.1 `GS9 Knowledge VNG AI` — tri thức nền tảng dùng chung cho cả team GS9

Nội dung: tài liệu của **hai tính năng** Knowledge Base và Agent, kèm ảnh của chính hai tính năng đó.

| Thành phần | Số lượng | Ghi chú |
|---|---:|---|
| `doc-00` → `doc-12` | 13 | Tính năng Knowledge Base |
| `doc-13` → `doc-19` | 7 | Tính năng Agent |
| `image-01` → `image-49` | 49 | Chuyển từ KB asset host vào chung |

Tổng **69 tài liệu**. Nội dung 20 module **đã đúng cấu trúc hai tính năng**, không cần viết lại — chỉ đổi tên và gộp ảnh vào cùng thư mục.

Thư mục local gộp lại: 49 PNG chuyển từ `knowledge/GS9 Knowledge VNG - Image Assets/` sang `knowledge/GS9 Knowledge VNG AI/`. `local_asset_prefix` đổi từ `../GS9 Knowledge VNG - Image Assets` thành cùng thư mục.

### 2.2 `GS9 CFL Knowledge Agent` — tri thức riêng của CFL

| Thành phần | Trạng thái |
|---|---|
| 25 file hiện có → tiền tố `doc-` | Có sẵn, chỉ đổi tên |
| **Tài liệu cấu trúc KB của CFL** | **CHƯA CÓ — phải soạn mới** |

Ba file mới, chuyển bản đồ 7 tầng từ dạng spec kỹ thuật sang dạng cả team tra được:

- `doc-30-cau-truc-kb-cfl.md` — 7 tầng, mỗi tầng để làm gì, KB nào thuộc tầng nào
- `doc-31-ban-chat-tung-kb.md` — bảng bản chất: mỗi KB thật sự là gì trong luồng, ai được bind
- `doc-32-quy-uoc-dat-ten-va-nhung-anh.md` — luật Phase 0 + Phase 1, dạng tra cứu nhanh

---

## Phase 3 — Đồng bộ lên Web bằng Google Drive connector

**Thay đổi 15/08 (cuối phiên):** người dùng **không upload tay nữa**. Thư mục project `G:\My Drive\CFL\VNG AI\Knowledge Base VNG` nằm trong Google Drive, nên sẽ dùng **Google Drive connector** để đồng bộ lên KB.

Điều này đổi bản chất Phase 3: từ "upload thủ công rồi thu URI" thành "cấu hình nguồn đồng bộ đúng phạm vi". Nhưng nó **đẻ ra bốn rủi ro mới**, và một trong số đó đánh thẳng vào việc đổi tên.

### 3.1 RỦI RO LỚN NHẤT — hành vi đổi tên khi sync CHƯA TỪNG ĐƯỢC KIỂM CHỨNG

`audit/audit-google-drive-connector-2026-08-07.md` mục 6 ghi rõ:

| Hạng mục | Trạng thái |
|---|---|
| Xác thực service account, chọn tài nguyên, chiến lược, lượt sync đầu | Đã kiểm chứng |
| **Đổi tên, di chuyển, xóa, thu hồi quyền** | **Chưa xác định** |
| Sửa nội dung tài liệu qua nhiều chu kỳ (Tăng dần lẫn Toàn bộ), ảnh nhúng URI MinIO trong Markdown có còn sống | **Đã kiểm chứng 16/08 — an toàn** ([DEC-051](../../../DECISIONS.md), xem 3.5b) |

Kế hoạch này **đổi tên 135 file rồi sync** — đúng kịch bản chưa ai thử. Hai kết cục có thể:

- Connector coi đổi tên = **xóa + tạo mới** → cần bật `Đồng bộ xóa` để dọn bản cũ, nếu không KB sẽ có **cả tên cũ lẫn tên mới** (trùng nội dung, nhiễu truy hồi).
- Connector **không nhận ra đổi tên** → sinh bản trùng, phải dọn tay.

**Bắt buộc: chạy thử trên quy mô nhỏ trước.** Đổi tên 2–3 file, sync, quan sát KB, rồi mới làm 135 file. Đây là bước không được bỏ.

### 3.2 Phạm vi sync phải khoanh chặt — có credential trong cây thư mục

Thư mục project chứa những thứ **không được** vào KB: `audit/`, `docs/`, `scripts/`, `tests/`, `.git/`, `samples/`, và đặc biệt `knowledge/GS9 CFL Item Profile/` (dữ liệu người chơi P0) cùng `knowledge/GS9 CFL Item Profile/keys CFL ItemID/keys/` (**service-account key**).

Audit 07/08 mục 3 xác nhận UI cho **chọn từng thư mục con**, dấu trừ cam báo chỉ chọn một phần. Mục 7 ghi luật: *"Chỉ cấp Viewer cho thư mục cần đồng bộ; không chọn thư mục chứa key hoặc credential."*

→ Mỗi KB trỏ vào **đúng một thư mục con** của `knowledge/`, không bao giờ trỏ vào root project.

| KB | Thư mục nguồn |
|---|---|
| `GS9 Knowledge VNG AI` | `knowledge/GS9 Knowledge VNG AI/` |
| `GS9 CFL Knowledge Agent` | `knowledge/GS9 CFL Knowledge Agent/` |
| `GS9 CFL Plan Version` | `knowledge/GS9 CFL Plan Version/` (gồm cả `V5/assets/`) |
| `GS9 CFL Item Profile` | **KHÔNG sync** — P0, chứa key |

### 3.3 Quy ước tên `image-`/`doc-` nay có thêm công dụng

Audit mục 4 xác nhận connector hỗ trợ **regex lọc tên tệp** và **rule gắn tag theo đường dẫn có capture từ regex**. Vì vậy:

- Lọc `^(doc|image)-` → chỉ nhận file đúng quy ước, tự động loại `image-map.json`, `source-manifest.json` và mọi file lạc.
- Rule tag theo path: capture `V5` từ `.../GS9 CFL Plan Version/V5/...` → tự gắn nhãn `ver:v5`. **Giải quyết luôn việc gắn nhãn phiên bản mà không phải làm tay 41 lần.**

Đây là lý do thứ hai để đặt tiền tố, ngoài lý do dễ đọc.

### 3.4 Cấu hình đề xuất cho lượt đầu

| Mục | Giá trị | Lý do |
|---|---|---|
| Chế độ | **Toàn bộ** cho lượt đầu, **Tăng dần** cho các lượt sau | Lượt đầu đổi tên hàng loạt |
| Xung đột | **Ghi đè** | Cùng tên thì lấy bản mới |
| `Đồng bộ xóa` | **Bật** — nhưng thử trên 2–3 file trước | Cần để dọn tên cũ; chưa từng kiểm chứng |
| Lịch | Thưa (hằng ngày) khi đang ổn định | Tránh sync giữa lúc đang sửa file |
| Regex tên tệp | `^(doc|image)-` | Loại file phụ trợ |

### 3.5 Thu URI sau khi sync

Sync xong, mọi URI MinIO đổi. Dùng **MCP `list_documents`** (mục 0.2) thay cho việc bắt network bằng browser — với điều kiện KB được share vào space.

Lưu ý mới: tài liệu vào qua connector có `channel: google_drive` (không phải `web`), và **nội dung đổi được mà không qua build hay audit nào** — đây là điểm audit 14/08 đã cảnh báo với `CFL ItemID.xlsx`. Phải ghi nhận datasource và tần suất sync vào audit.

### 3.5b Gộp ảnh + tài liệu chung một KB — đã kiểm chứng an toàn cho sync lặp lại (16/08)

Câu hỏi treo từ lượt trước: gộp ảnh + tài liệu chung một KB (DEC-043, áp dụng cho `GS9 Knowledge VNG AI`) có an toàn không khi một tài liệu khác trong cùng KB được sửa nội dung và sync lại? Nếu ảnh mất/đổi thì phải tách ảnh ra KB riêng (asset host, kiến trúc cũ).

Đã kiểm bằng KB test `Test` (`d7295a59-03b1-496c-86eb-9ecaa3364aa7`) qua 3 vòng sync trên Google Drive connector — chi tiết đầy đủ ở `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`, kết luận chính thức ở [DEC-051](../../../DECISIONS.md):

- **Vòng 2 (Tăng dần):** sửa nội dung văn xuôi của một tài liệu có nhúng ảnh (không đụng dòng ảnh) → tài liệu được re-ingest đúng nội dung mới, ảnh vẫn còn nguyên.
- **Vòng 3 (Toàn bộ):** thêm tài liệu mới + sửa nội dung 2 tài liệu có nhúng ảnh khác nhau (không đụng dòng ảnh) → cả hai ảnh vẫn còn nguyên, tài liệu mới được ingest đúng.
- **Kết luận:** an toàn ở cả hai chế độ đồng bộ, **miễn không đụng dòng ảnh khi sửa**. Lý do kỹ thuật suy ra: link ảnh nhúng là URI MinIO tĩnh (không phải tham chiếu động vào document ảnh trong KB) — ảnh sống/chết không phụ thuộc việc tài liệu ảnh gốc có được re-sync hay không.
- **Hệ quả cho Phase 3:** không cần tách `image-NN-...` ra KB riêng. Kiến trúc gộp của `GS9 Knowledge VNG AI` (DEC-043/044) giữ nguyên, bước 6–7 ở 3.6 dưới đây (viết lại `image-map.json`, strict build, `link_plan_v5_minio.py`) tiếp tục áp dụng bình thường.
- **Giới hạn:** kết luận dựa trên quan sát UI (nội dung xem trước, ảnh render, timestamp), không phải `knowledge_id` (MCP tool không truy cập được KB test — phạm vi MCP hiện chỉ gồm các KB production). Chưa test case sửa trực tiếp nội dung/caption của chính file ảnh, và **chưa test đổi tên/di chuyển/xóa** — rủi ro ở mục 3.1 vẫn còn nguyên, chỉ riêng câu hỏi "sửa nội dung tài liệu khác có làm mất ảnh" là đã có câu trả lời.

### 3.6 Trình tự

1. Đổi tên xong toàn bộ ở local (Phase 1+2)
2. **Thử nghiệm nhỏ:** đổi tên 2–3 file, sync, quan sát KB có sinh bản trùng không → chốt cấu hình `Đồng bộ xóa`
3. Cấu hình nguồn Drive cho từng KB theo bảng 3.2
4. Chạy sync `Toàn bộ` lượt đầu
5. Đối chiếu số tài liệu trên KB với inventory local
6. `list_documents` thu `file_path` → viết lại `image-map.json`
7. Strict build lại 20 module + chạy `link_plan_v5_minio.py` → sync lần 2 để đẩy Markdown đã có URI mới
8. Chat-test

**Lưu ý vòng lặp:** Markdown chứa URI của ảnh, mà URI chỉ có sau khi ảnh đã sync. Nên phải sync **hai lượt**: lượt 1 đẩy ảnh, lượt 2 đẩy Markdown đã gắn URI. Đừng kỳ vọng một lượt là xong.

---

## Phase 4 — Cập nhật luật và tài liệu

| Mã | Nội dung | Thay thế |
|---|---|---|
| DEC-041 | Ghi lại cú pháp nhúng ảnh chuẩn `![mô tả](minio://.../exports/<uuid>.<ext>)` — xác nhận đúng, không đổi | làm rõ DEC-004 |
| DEC-042 | Quy ước tên `image-`/`doc-`, ngoại lệ Google Drive, quy ước phiên bản | mới |
| DEC-043 | Gộp ảnh vào KB tiêu thụ, bỏ mô hình hai-KB asset host | DEC-012, DEC-019, DEC-024 |
| DEC-044 | Phân vai 2 KB nền tảng | bổ sung DEC-034 |
| DEC-045 | Ưu tiên MCP `list_documents` để thu URI; KB cần thu URI thì share vào space | mới |
| DEC-046 | Đưa nội dung lên KB bằng Google Drive connector, mỗi KB trỏ đúng một thư mục con của `knowledge/`; tuyệt đối không trỏ root project vì cây thư mục chứa credential và dữ liệu P0 | mới |

Sửa theo: `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md`, `docs/superpowers/specs/2026-08-15-kb-architecture-design.md` (mục 5.1 và L0 — bỏ vai "asset host" riêng).

### Gate nghiệm thu

- Strict build ra đúng 20 module tên mới, HTML offline tự chứa
- `image-map.json` đủ khóa tên mới, URI duy nhất
- Toàn bộ test pass sau `pip install markdown beautifulsoup4`
- Chat-test: ảnh render **đúng một lần**

---

## Thứ tự thực hiện

```
Phase 1     đổi tên toàn bộ (thuần local)             ← LÀM ĐƯỢC NGAY, không còn gì chặn
Phase 2     gộp ảnh + soạn 3 file cấu trúc CFL
   │
Phase 3.1   THỬ NHỎ: đổi tên 2-3 file → sync → xem có sinh bản trùng không
            (hành vi đổi tên khi sync CHƯA TỪNG kiểm chứng — không bỏ bước này)
Phase 3     cấu hình nguồn Drive theo đúng phạm vi → sync lượt 1 (ảnh)
            → thu URI qua MCP → build lại → sync lượt 2 (Markdown) → chat-test
Phase 4     DEC + tài liệu + gate
```

## Việc KHÔNG làm

- Không xóa KB `GS9 Knowledge VNG - Image Assets` cho tới khi 20 module đã trỏ URI mới và chat-test đạt (DEC-005).
- Không đụng tài liệu đồng bộ từ Google Drive.
- Không nới lỏng test để cho qua sau khi đổi tên.
- Không tự share KB vào space — đó là thay đổi quyền, cần người dùng thực hiện hoặc cho phép rõ.
