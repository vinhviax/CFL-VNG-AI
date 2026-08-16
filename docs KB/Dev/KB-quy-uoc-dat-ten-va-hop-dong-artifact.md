# KB — Quy ước đặt tên và hợp đồng artifact

**Đối tượng:** Dev và người vận hành pipeline. Người cần biết *file này phải tên gì, và cái gì được coi là "đúng" khi build xong*.
**Ngày viết:** 16/08/2026.

**Nguồn:**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| `AGENTS.md` mục "Quy ước đặt tên" | 15/08/2026 | Luật rút gọn |
| `PROJECT.md` mục "Hợp đồng artifact", "Kiến trúc local và Web" | 15/08/2026 | Hợp đồng số lượng |
| `DECISIONS.md` DEC-031, 037, 042, 047, 048 | 14–15/08/2026 | Luật bền vững |
| `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` | 15/08/2026 | Kế hoạch đổi tên, lý do kỹ thuật |
| Quan sát trực tiếp cây thư mục | **16/08/2026** | Đối chiếu thực tế — xem mục 7 |

---

## 1. Ba lớp tên, đừng nhầm

| Lớp | Ai đặt | Đổi được không | Luật |
|---|---|---|---|
| **Tên KB trên Web** | Người dùng, theo quy định công ty | **Không đổi KB đang chạy** | DEC-031, DEC-037 |
| **Tên thư mục local** | Project | Đổi được, phải khớp tên KB Web | DEC-030, DEC-031 |
| **Tên file trong KB** | Pipeline hoặc người dùng | Đổi được, theo tiền tố `doc-`/`image-` | DEC-042, DEC-047 |

Nhầm ba lớp này là nguồn lỗi thật: phiên 15/08/2026 người dùng đổi tên thư mục `knowledge/GS9 Plan Version/` → `knowledge/GS9 CFL Plan Version/` để khớp tên KB Web, và thao tác đó **làm phẳng thư mục con `assets/`** ra ngoài — 29 JPEG rơi khỏi vị trí mọi script trỏ tới (`STATUS.md`, 15/08/2026). Chuyện xảy ra lần thứ hai ngày 16/08, và lần này cách xử lý ngược lại: giữ bố cục phẳng rồi sửa script theo. Xem mục 7.3.

---

## 2. Tên KB

**Quy ước cho KB tạo mới:** `GS9 CFL <Miền> [& <Miền phụ>]` — tiếng Anh cho miền, prefix `GS9` **bắt buộc** theo quy định công ty.

**KB đang chạy: không đổi tên** (DEC-037, 15/08/2026). Lý do: đổi tên phá vỡ tham chiếu, thói quen người dùng và tài liệu cũ. Thay vào đó mỗi KB có một dòng "bản chất" trong bảng tra cứu — xem `KB-quy-hoach-nghiep-vu-7-tang.md` mục 5.

Ba tên KB nền tảng phải giữ **chính xác từng ký tự** (DEC-031): `GS9 Knowledge VNG AI`, `GS9 Knowledge VNG - Image Assets`, `GS9 CFL Knowledge Agent`. Builder khoá cứng chuỗi `"GS9 Knowledge VNG AI"` (`scripts/build_handbook.py`, hằng `CONSUMER_KB_NAME`) và test khoá lại chuỗi đó (`tests/test_build_handbook.py::test_project_layout_uses_exact_web_knowledge_base_names`). Đổi tên thư mục mà không sửa hằng số = build ghi vào thư mục sai.

---

## 3. Tên Agent

**DEC-048 (15/08/2026):** 10 custom Agent đổi tiền tố local từ `GS9 …` sang `GS9 CFL …`, khớp quy ước tên KB.

Phạm vi áp dụng:

| Có đổi | Không đổi |
|---|---|
| Thư mục `agent/GS9 CFL <Agent>/` | `audit/*.md` (bằng chứng lịch sử) |
| Hồ sơ meta-KB `doc-20`→`doc-29` | `agent/kb-allowlist-proposal-2026-08-14.md` (lịch sử) |
| `STATUS.md`, `HANDOFF.md`, `PROJECT.md`, `NEXT_SESSION_PROMPT.md`, bản đồ kiến trúc | Tên rút gọn không có tiền tố `GS9` (bảng so sánh `doc-02`, sơ đồ `doc-03`) |

**Chỉ đổi tên local.** Người dùng tự đổi tên thật trên Web.

**Ngoại lệ giữ nguyên:** `GS9 GM Policy Advisor` — không hoàn tác DEC-039 (đổi vai trò từ `GM Case Investigator`). Lưu ý tên này **không mang tiền tố `CFL`** trong `DECISIONS.md` nhưng thư mục local là `agent/GS9 CFL GM Policy Advisor/` (kiểm tra 16/08/2026). Hai chỗ ghi khác nhau.

**Nợ kỹ thuật đã biết:** 4 file meta-KB (`doc-00`, `doc-01`, `doc-02`, `doc-26`) còn link chết trỏ `27-custom-gs9-gm-case-investigator.md`. Tên đó không tồn tại từ 15/08/2026. Chưa sửa vì sửa nhãn hiển thị là đổi nội dung, ngoài phạm vi việc đổi tên thuần tuý.

---

## 4. Tên tài liệu — `doc-` và `image-`

### 4.1 Luật (DEC-042, 15/08/2026)

| Loại | Tiền tố | Ví dụ |
|---|---|---|
| Ảnh | `image-` | `image-01-tong-quan-danh-sach-knowledge.png` |
| Tài liệu không phải ảnh | `doc-` | `doc-00-gioi-thieu-va-quick-start.md` |
| KB nhiều phiên bản | chèn phiên bản **sau** tiền tố loại | `doc-v5-00-index-va-pham-vi.md`, `image-v5-01-….jpg` |

**Ngoại lệ:** tài liệu đồng bộ từ Google Drive — người dùng tự đặt tên, agent không đụng.

Dấu phân cách là **gạch ngang** `-`, không phải gạch dưới `_`.

Thứ tự trong tên có phiên bản là điểm dễ sai: **`doc-v5-00-…`**, không phải `V5-00-…` hay `v5-doc-00-…`. Spec kiến trúc bản đầu từng đề xuất `V5-00-...`; quy ước đã chốt lại theo DEC-042 và spec đã ghi đính chính tại mục 8.1.

### 4.2 Hai lý do đặt tiền tố, không phải một

1. **Dễ đọc / phân loại.**
2. **Google Drive connector lọc được bằng regex** (kế hoạch 15/08, mục 3.3; dựa trên `audit/audit-google-drive-connector-2026-08-07.md` mục 4):
   - Regex tên tệp `^(doc|image)-` → chỉ nhận file đúng quy ước, **tự động loại** `image-map.json`, `source-manifest.json`, `desktop.ini` và mọi file lạc.
   - Rule gắn tag theo đường dẫn có capture: bắt `V5` từ `.../GS9 CFL Plan Version/V5/...` → tự gắn nhãn `ver:v5`, thay cho việc gắn tay 41 lần.

Lý do thứ hai là lý do kỹ thuật thật. Ai bỏ tiền tố để "cho gọn" sẽ phá luôn bộ lọc sync.

### 4.3 Phạm vi mở rộng (DEC-047, 15/08/2026)

Quy ước `doc-` được mở sang 5 KB ngoài kế hoạch gốc, theo yêu cầu trực tiếp của người dùng. Giữ nguyên phần tên gốc, chỉ thêm tiền tố; `desktop.ini` không đổi.

| KB | Số file khi ra quyết định | Ghi chú |
|---|---|---|
| `GS9 CFL PUM` | 7 PDF | `doc-CFL MMR GMT 2026.01.pdf` … |
| `GS9 CFL Data Daily` | 8 XLSX | thiếu `doc-CFL_082026.xlsx` (G4 chưa xử lý) |
| `GS9 CFL Sentiment Feedback User` | 1 XLSX | |
| `GS9 CFL Glossary & Systems` | 3 MD | KB nháp |
| `GS9 CFL CS FAQ & Policy` | 1 MD | KB nháp |

**Người dùng xác nhận rõ và chủ động chấp nhận** rằng các thư mục này đang liên kết Google Drive nên đổi tên local sẽ khiến Web tự đồng bộ đổi tên theo — khác cách "thử nhỏ trước" áp cho Phase 3 của 3 KB nền tảng.

**`GS9 CFL Item Profile` loại trừ hoàn toàn** — không đổi tên, không mở, không đọc (boundary P0). Xem mục 7.4: thực tế 16/08 mâu thuẫn với điều này.

**`GS9 CFL Kho Dữ Liệu Tổng Hợp`** không có mirror local nên không áp dụng.

---

## 5. Cú pháp nhúng ảnh (DEC-041, 15/08/2026)

```markdown
<!-- LOCAL_ASSET: <đường dẫn cục bộ> -->
![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/10012/exports/<uuid>.<ext>)
```

Hai đường ảnh song song (DEC-004):

- **URI MinIO** — đường Web đọc. Đường dẫn tương đối **không hoạt động** khi Markdown nạp vào KB; chat sẽ không render.
- **Comment `LOCAL_ASSET`** — truy nguyên file cục bộ, dùng cho HTML offline và cho người đọc repo.

**DEC-041 xác nhận cú pháp này hoàn toàn đúng.** Hiện tượng ảnh render hai lần trong chat là hành vi không ổn định của model khi soạn câu trả lời, **không phải lỗi cú pháp hay cấu trúc KB**. Không sửa `build_handbook.py`/`convert_cfl_plan_html.py`/`link_plan_v5_minio.py` vì lý do này, không điều tra lại. Bằng chứng: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

---

## 6. Hợp đồng artifact

Theo `PROJECT.md` (15/08/2026). Đây là định nghĩa "build đúng".

### 6.1 Kiến trúc local ↔ Web

```text
so-tay-tao-knowledge-base-v3.md            <-- master nghiệp vụ (nguồn thật, xem 7.2)
            │
            ├── strict builder ──> knowledge/GS9 Knowledge VNG AI/doc-NN-*.md
            │                              │                    (cùng thư mục)
            │                              │                    image-NN-*.png
49 PNG ─────┴──> HTML offline tự chứa      │
                                           └── Agent ──> Human
                                      │
                                      └──> 49 URI MinIO trong image-map.json

agent/ + audit Agent ──> knowledge/GS9 CFL Knowledge Agent/doc-NN-*.md
                                      │
                                      └──> Human chọn, hiểu và dùng Agent
```

| Vai trò | Tên trên Web | ID | Inventory phát hành |
|---|---|---|---|
| KB nền tảng (KB + Agent, kèm ảnh) | `GS9 Knowledge VNG AI` | `cefadf09-4187-46ac-a765-591e3255a4a4` | 20 MD (`doc-00`→`doc-19`) + 49 PNG (`image-01`→`image-49`) = 69, **cùng thư mục local** |
| Asset host (Web, chưa retire) | `GS9 Knowledge VNG - Image Assets` | `6da8657c-dd96-4170-a698-074043475014` | 49 PNG, 0 MD — không còn thư mục local riêng |
| Agent meta-KB | `GS9 CFL Knowledge Agent` | `1d92448f-7ee2-46c4-b202-5efbe9cc5616` | 28 MD (`doc-00`→`doc-92`), 0 binary |

Ba KB cùng tenant `10012`.

### 6.2 Các điều khoản đếm được

| # | Điều khoản | Nguồn |
|---|---|---|
| 1 | Master có **đúng 20** cặp marker `MODULE`, tên marker mang tiền tố `doc-` | DEC-042 |
| 2 | `GS9 Knowledge VNG AI` local có **20 Markdown** (`doc-00`→`doc-19`), **49 PNG** signature hợp lệ (`image-01`→`image-49`) và một map — **cùng một thư mục** | DEC-043 |
| 3 | Map có **49 key** khớp 49 tên PNG và **49 URI** `minio://knowledge-base-prd/10012/exports/*.png` **duy nhất** | DEC-025 |
| 4 | 20 module có **60 link MinIO** và **60 `LOCAL_ASSET`** dạng `./image-NN-...` | DEC-025, DEC-043 |
| 5 | HTML offline **không phụ thuộc tài nguyên remote** | DEC-003 |
| 6 | Nội dung chỉ sửa tại nguồn rồi build; thư mục KB là **mirror phát hành**, không phải nơi biên tập | DEC-001 |
| 7 | Meta-KB Agent có đúng **28 Markdown phẳng** (`doc-00`→`doc-92`): 6 hướng dẫn chung, 6 hồ sơ default, 10 hồ sơ custom, 3 trang cấu trúc KB CFL (`doc-30`–`doc-32`), 3 trang governance. Không file ngoài Markdown, không folder con | DEC-044 |
| 8 | PNG phải có magic bytes `89 50 4E 47 0D 0A 1A 0A`; không đổi đuôi JPEG để giả định dạng | DEC-014 |

### 6.3 Hợp đồng bundle Plan Version V5

| # | Điều khoản | Trạng thái 16/08/2026 |
|---|---|---|
| 1 | 12 Markdown `doc-v5-00`→`doc-v5-11` | có đủ |
| 2 | 29 JPEG `image-v5-01`→`image-v5-29` | có đủ, nằm **phẳng trong `V5/`** (mục 7.3) |
| 3 | 29 ảnh nhúng + 29 link registry = 58 tham chiếu MinIO | đếm được 58 chuỗi `minio://` trong 12 file |
| 4 | 29 comment `LOCAL_ASSET` | đếm được 29, dạng **tên trần**, đường dẫn khớp file thật |
| 5 | `image-map.json` có `knowledge_base_id = 1452bc9a-c8b4-487b-b623-34e0b00a83e9`, 29 URI duy nhất, tiền tố `minio://knowledge-base-prd/10012/exports/` | đạt |

### 6.4 Ràng buộc cứng khi đổi tên: KHÔNG đổi nội dung

Kế hoạch 15/08 đặt ràng buộc và cách nghiệm thu:

| Được phép đổi | Không được đổi |
|---|---|
| Tên file | Bất kỳ câu chữ, tiêu đề, bảng, thứ tự mục nào |
| Đường dẫn trong `<!-- LOCAL_ASSET: ... -->` | Phần mô tả trong `![mô tả](...)` |
| URI `minio://...` | Cấu trúc heading, số thứ tự mục |
| Marker `<!-- MODULE:... -->` (chính là tên file) | Nội dung bên trong marker |

**Cách nghiệm thu:** chuẩn hoá nội dung bằng cách bỏ dòng `LOCAL_ASSET` và thay mọi URI minio bằng placeholder, rồi hash SHA-256. Chạy trước và sau khi đổi tên. Hash lệch = đã lỡ đụng nội dung, phải hoàn tác.

Kết quả áp dụng thật (`STATUS.md`, 15/08/2026): 34/57 file khớp hash tuyệt đối; 23/57 lệch nhưng **đã xác minh từng file** là do đổi target link nội bộ và 2 bổ sung có chủ đích. Phép kiểm này bắt được cả trường hợp builder vô tình đổi cách render.

---

## 7. Đối chiếu với thực tế ngày 16/08/2026 (17:34)

Kiểm tra trực tiếp cây thư mục, đếm chuỗi trong file, và chạy `python -m unittest discover -s tests -v`.

**Kết luận: hợp đồng đếm được ở mục 6 hiện ĐẠT. Còn lại hai chỗ lệch luật ở 7.3 và 7.4.**

> **Cảnh báo về bản cũ:** mục 7 này từng ghi ngược lại — rằng thư mục KB rỗng và hợp đồng không thoả mãn. Điều đó đúng vào **buổi sáng 16/08**, khi repo đang giữa chừng một đợt tái cấu trúc. Trạng thái đã được khôi phục trong ngày. Nếu bạn đọc một bản sao cũ của tài liệu này, hãy chạy lại các lệnh ở 7.1 trước khi tin.

### 7.1 Các con số hợp đồng — đo trực tiếp

| # | Điều khoản | Đo được 16/08/2026 | Đạt? |
|---|---|---|---|
| 1 | Master 20 cặp marker `MODULE` tiền tố `doc-` | `extract_modules()` trả **20** module, tên `doc-00-…` → `doc-19-…` | Đạt |
| 2 | `GS9 Knowledge VNG AI`: 20 MD + 49 PNG + 1 map, cùng thư mục | **20** `.md`, **49** `.png`, có `image-map.json` | Đạt |
| 3 | Map 49 key / 49 URI duy nhất | `49 / 49`, `knowledge_base_id = cefadf09-…` | Đạt |
| 4 | 60 link MinIO + 60 `LOCAL_ASSET` dạng `./image-NN-…` | 17:34 → **60** và **60** · 17:40 → **59** và 60 | **Vỡ lúc 17:40**, xem dưới |
| 5 | HTML offline không phụ thuộc tài nguyên remote | 30.859.005 byte, mtime 16/08 06:40 | Đạt |
| 7 | Meta-KB Agent đúng 28 Markdown phẳng | **28** `.md`, `doc-00`→`doc-92`, không folder con | Đạt |

#### Hợp đồng vỡ ngay trong lúc viết tài liệu này — 16/08/2026 lúc 17:37

Lần đo đầu (17:34) cho 60/60, **Đạt**. Lần chạy lại lúc 17:40 cho `AssertionError: 59 != 60` tại `test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs`.

Nguyên nhân, truy được chính xác một file: `knowledge/GS9 Knowledge VNG AI/doc-02-tao-kb-nhanh-va-nang-cao.md` có mtime **17:37**, trong khi 19 module còn lại đều là **06:40**. Dòng ảnh duy nhất của nó đã bị đổi:

```text
map:  minio://knowledge-base-prd/10012/exports/2413cc24-8243-48d9-8b54-d24dfd0a6ecb.png
file: minio://knowledge-base-prd/10012/986e3126-…-90b90/7429057a-…-726bb0.png
```

Ba điều đọc được từ sự cố này:

1. **Đây là dạng URI thứ hai** — `<doc_id>/<uuid>` thay vì `exports/<uuid>`, đúng dạng mà MCP `list_documents` trả về. Chính là câu hỏi treo ở DEC-045 và kế hoạch 15/08 mục 0.2: *"chưa biết dạng nào render được trong chat"*. Có vẻ ai đó đang **thử nghiệm dạng URI mới** trên một module.
2. **Đây là sửa tay vào artifact sinh** — vi phạm DEC-001. Dòng marker ngay đầu file đã cảnh báo. Lần `build_handbook.py` kế tiếp sẽ **ghi đè mất** thay đổi này mà không báo, vì builder lấy URI từ `image-map.json`.
3. **`image-map.json` chưa được cập nhật theo**, nên file và map đang mâu thuẫn.

Không xử lý trong phiên này: đây là thay đổi của người khác đang dở dang, không thuộc phạm vi tài liệu. **Ghi nhận, không hoàn tác** (theo tinh thần DEC-050).

Giá trị của sự cố: nó chứng minh cả hai thứ mà tài liệu này khẳng định — rằng **test contract project sống thực sự bắt được** sửa tay ngoài quy trình, và rằng mọi con số ở mục 7 có **hạn dùng tính bằng phút** chứ không phải ngày.

Lệnh dùng lại được:

```powershell
(Get-ChildItem "knowledge\GS9 Knowledge VNG AI\*.md").Count        # kỳ vọng 20
(Get-ChildItem "knowledge\GS9 Knowledge VNG AI\*.png").Count       # kỳ vọng 49
(Get-ChildItem "knowledge\GS9 CFL Knowledge Agent\*.md").Count     # kỳ vọng 28
python -m unittest discover -s tests -v                            # kỳ vọng Ran 29 tests / OK (skipped=6)
```

Bộ test chạy ngày 16/08: `Ran 29 tests … OK (skipped=6)`. Sáu skip đều do thiếu HTML nguồn Plan V5 — mức bình thường trên máy này theo `AGENTS.md`.

### 7.2 Nguồn sổ tay: master ở root, không phải `docs KB/Human/`

`scripts/build_handbook.py` (sửa 16/08/2026) ưu tiên đọc `doc-*.md` từ `docs KB/Human/` (phẳng) và hai thư mục con `KB/`, `Agent/`. Nếu **không tìm thấy file nào**, nó quay về master `so-tay-tao-knowledge-base-v3.md` ở root.

Thực tế 16/08: `docs KB/Human/` **rỗng**, nên builder đang chạy **nhánh fallback** và master ở root vẫn là nguồn thật. Đây là hành vi đúng theo mã, không phải lỗi.

Hai điều cần biết khi đặt tên file nguồn trong tương lai:

- Tên file nguồn **chính là tên module đầu ra**. Đặt sai tên ở `docs KB/Human/` là đổi luôn tên file trong KB.
- Dòng marker sinh ra ghi `<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->` — trỏ vào thư mục đang rỗng. Ai làm theo và tạo file mới ở đó sẽ **chuyển builder sang nhánh thư mục**, và nếu số file khác 20 thì gate `Expected 20 modules` sẽ đỏ.

Cơ chế đầy đủ ở `KB-pipeline-build-va-kiem-thu.md` mục 2.1.

**Chưa có mã DEC nào** cho cấu trúc `docs KB/`; không tài liệu sống nào (`AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md`, `DECISIONS.md`) nhắc tới nó.

### 7.3 Bundle Plan V5 đã chuyển sang bố cục phẳng

29 JPEG nằm trực tiếp trong `knowledge/GS9 CFL Plan Version/V5/`; thư mục `assets/` không tồn tại. Khác với lần 15/08 (khi đó khôi phục lại `assets/`), lần này **script được sửa theo bố cục phẳng**:

| Thành phần | Trạng thái 16/08/2026 |
|---|---|
| 29 comment `LOCAL_ASSET` | dạng **tên trần** `<!-- LOCAL_ASSET: image-v5-NN-….jpg -->`; đếm được **0** comment còn tiền tố `assets/` |
| `link_plan_v5_minio.py` | `ASSETS = BUNDLE`; regex nhận **cả hai** dạng có và không có `assets/` |
| `--check` | mã thoát `0`, `0 ảnh nhúng + 0 link registry` cần đổi — bundle đã gắn link xong |
| 58 tham chiếu MinIO | **29 ảnh nhúng + 29 link registry**, đếm khớp |
| `image-map.json` | 29 URI duy nhất, `knowledge_base_id = 1452bc9a-…` | 
| `source-manifest.json` | vẫn đăng ký 42 `generated_files` với 29 mục dạng **`assets/image-v5-NN-….jpg`** |
| `convert_cfl_plan_html.py` | vẫn ghi ảnh vào `assets/` — **chưa sửa** |

Hai dòng cuối là nợ kỹ thuật thật: converter và manifest còn ở bố cục cũ, chỉ linker và ảnh đã sang bố cục mới. Chạy lại converter hôm nay sẽ sinh ra **hai bộ ảnh cùng tên ở hai chỗ**. Phân tích đầy đủ ở `KB-pipeline-build-va-kiem-thu.md` mục 3.3 và 6.2.

Bảng hợp đồng 6.3 vì vậy cần đọc lại: điều khoản 2 ("29 JPEG") **đạt**, điều khoản 4 ("29 `LOCAL_ASSET`") **đạt và đường dẫn nay sống**, không còn chết như bản cũ ghi.

### 7.4 `Item Profile` đã đổi sang đúng quy ước `doc-` (16/08/2026)

Liệt kê tên file (không mở, không đọc nội dung — giữ boundary P0):

```text
knowledge/GS9 CFL Item Profile/
├── desktop.ini
├── doc-01-weapons-usage.csv
├── doc-02-weapon-name-map.csv
├── doc-03-sample-users.csv           <-- player-level, P0
├── doc-04-sample-user-weapons.csv    <-- player-level, P0
├── doc-05-issued-items-timeseries.csv
├── doc-06-users-detailed.csv         <-- player-level, P0
├── doc-07-users-cb.csv               <-- player-level, P0
└── doc_CFL ItemID.gsheet
```

**Lịch sử:** trước 16/08/2026 tám file này mang dấu gạch dưới (`doc_01_weapons_usage.csv`), vi phạm hai điều cùng lúc: DEC-047 và `AGENTS.md` ghi KB này *"loại trừ hoàn toàn — không đổi tên, không mở, không đọc"*, và dấu phân cách sai so với DEC-042 nên regex lọc `^(doc|image)-` của Google Drive connector **không** khớp.

Ngày 16/08/2026 người dùng chỉ định đổi 7 file `.csv` sang đúng quy ước `doc-NN-slug`. Thao tác chỉ đổi tên, không mở nội dung — boundary P0 vẫn giữ. Nay cả 7 file đều khớp regex sync.

`doc_CFL ItemID.gsheet` **giữ nguyên tên**: shortcut Google Drive, không phải định dạng tài liệu nạp lên KB, và DEC-035 quy định `.gsheet` không phải artifact Git.

Lưu ý còn lại: thư mục `keys CFL ItemID/keys/` (service-account key) không còn trong cây thư mục này.

### 7.5 Hai KB nháp đã có nội dung

`knowledge/GS9 CFL Glossary & Systems/` có **3 Markdown** (`doc-00-huong-dan-va-quy-uoc.md`, `doc-01-thuat-ngu-vu-khi.md`, `doc-02-thuat-ngu-he-thong-va-che-do.md`) và `knowledge/GS9 CFL CS FAQ & Policy/` có **1 Markdown** (`doc-00-huong-dan-va-quy-uoc.md`) — khớp số lượng DEC-047 ghi, và **đúng quy ước `doc-`** với dấu gạch ngang.

Hai thư mục này tương ứng hai KB đích ưu tiên 1 và 2 trong lộ trình soạn nội dung (xem `KB-quy-hoach-nghiep-vu-7-tang.md` mục 10). Chúng **chưa nạp lên Web**, nên chưa có ID và chưa thuộc hợp đồng artifact nào ở mục 6.

---

## Chưa kiểm chứng và rủi ro còn lại

**Chưa kiểm chứng:**

- **Không biết vì sao trạng thái thư mục dao động mạnh trong ngày 16/08.** Buổi sáng cùng ngày, `knowledge/GS9 Knowledge VNG AI/` và `knowledge/GS9 CFL Knowledge Agent/` chỉ còn `desktop.ini`; buổi chiều đã đầy đủ 20 MD + 49 PNG và 28 MD. Chưa xác định là do một thao tác đồng bộ Google Drive đang chạy dở, một lần dời thư mục, hay khôi phục thủ công. **Không có audit nào ghi lại sự kiện này.**
- **Không biết `docs KB/Human/KB` và `/Agent` từng có nội dung hay chưa.** Mã và test giả định hai thư mục con này tồn tại, nhưng chúng không có trên đĩa.
- **Hành vi đổi tên khi Google Drive connector sync chưa từng được kiểm chứng** (`audit/audit-google-drive-connector-2026-08-07.md` mục 6). Hai kết cục có thể: connector coi đổi tên = xoá + tạo mới (cần bật `Đồng bộ xóa`), hoặc không nhận ra đổi tên và sinh bản trùng. Bắt buộc thử 2–3 file trước khi làm 135 file.
- **Dạng `file_path` cho tài liệu ảnh chưa biết.** MCP `list_documents` trả `minio://.../10012/<doc_id>/<uuid>.md` cho Markdown — **khác** dạng `minio://.../10012/exports/<uuid>.png` mà `image-map.json` đang dùng và đang chạy đúng (DEC-045). Chưa biết dạng nào render được trong chat.
- **Tên trên Web của 10 Agent** — DEC-048 chỉ đổi local; chưa có audit xác nhận Web đã đổi theo.

**Rủi ro còn lại:**

- **Quy ước đặt tên hiện tồn tại ở 4 nơi:** `AGENTS.md` (rút gọn), `DECISIONS.md` DEC-042/047 (đầy đủ), `knowledge/GS9 CFL Knowledge Agent/doc-32-quy-uoc-dat-ten-va-nhung-anh.md` (bản Human-facing, **có tồn tại** — kiểm 16/08/2026) và chính file này. Bốn bản không có cơ chế nào giữ đồng bộ; sửa luật ở một chỗ sẽ để ba chỗ kia lạc hậu mà không ai biết.
- **`doc_` vs `doc-`.** Một dấu phân cách sai làm hỏng bộ lọc regex khi sync, và chỉ lộ ra sau khi sync chạy. Hiện có **8 file** ở `Item Profile` mang dạng sai (7.4) — nhưng KB đó không sync nên chưa bùng.
- **Trạng thái cây thư mục đổi được trong vòng vài giờ.** Mục 7 là ảnh chụp lúc 17:34 ngày 16/08. Bản viết buổi sáng cùng ngày đã sai hoàn toàn. Đừng tin các con số ở mục 7 mà không chạy lại lệnh ở 7.1.
- **Hợp đồng artifact được viết theo số lượng tuyệt đối** (20/49/60/28). Số cứng dễ kiểm nhưng cũng nghĩa là mọi thay đổi hợp lệ đều phải sửa đồng thời `PROJECT.md`, `DECISIONS.md`, builder và test. Bỏ sót một chỗ là gate đỏ giả.
- **`.gsheet` không hash/clone được**, nên bất kỳ nội dung nào chỉ tồn tại dưới dạng shortcut đều nằm ngoài mọi kiểm chứng bằng hash.
