# Handoff — Knowledge Base VNG

**Cập nhật:** 19/08/2026 (phiên 7, máy nhà — hàng đợi thông, gate sạch hoàn toàn, xem mục 4.9) · trước đó 18/08/2026 (phiên 6, máy nhà) · 17/08/2026 (phiên 5, máy công ty — converter Plan V5 kiểm chứng, KB-20, dọn artifact dư thừa, sửa file thuyết trình, tính năng "Thêm vào tri thức", đính chính DEC-052)
**Phiên bản:** 3.8.0 · **Test:** `Ran 30 tests OK` — không còn FAIL nào (xem mục 4.9, hàng đợi đã thông 19/08)

---

## 1. Đọc gì trước

| Thứ tự | File | Vì sao |
|---|---|---|
| 1 | `AGENTS.md` | Quy tắc làm việc, ranh giới an toàn, bảng phân loại đối tượng đọc |
| 2 | File này | Trạng thái và việc đang mở |
| 3 | `STATUS.md` | Nhật ký theo phiên, chi tiết hơn |
| 4 | `DECISIONS.md` | 70 quyết định — tra khi không hiểu vì sao làm vậy |
| 5 | `PROJECT.md` | Cây thư mục chuẩn, hợp đồng artifact |

---

## 2. Kiến trúc nội dung — hiểu sai chỗ này là làm hỏng việc

Nội dung đi theo **ba tầng**, tách theo **đối tượng đọc** (DEC-053):

```
docs KB/Dev/      25 file · cơ chế, kết quả kiểm chứng, cấu hình
                  → cho Dev và Agent config. KHÔNG lên Web.

docs KB/Human/    29 file · hướng dẫn thao tác
                  → NGUỒN BUILD. Sửa nội dung ở đây.

knowledge/<KB>/   bản sinh bởi build_handbook.py
                  → lên Web. KHÔNG sửa tay, sẽ bị ghi đè.
```

**Quy ước tiền tố tên file** trong `docs KB/`, builder tự đổi sang `doc-` khi sinh (giữ DEC-042 vì regex đồng bộ khoá `^(doc|image)-`):

| Tiền tố nguồn | Dải số | Đổ về KB |
|---|---|---|
| `KB-NN-*` | 00–12 | `GS9 Knowledge VNG AI` |
| `Agent-NN-*` | 13–19 | `GS9 Knowledge VNG AI` |
| `AgentCFL-NN-*` | 00–05 | `GS9 CFL Knowledge Agent` |
| `KBCFL-NN-*` | 10–12 | `GS9 CFL Knowledge Agent` |

Thêm tính năng mới thì thêm tiền tố vào `HUMAN_SOURCE_PREFIXES` hoặc `SIMPLE_KB_TARGETS` trong `scripts/build_handbook.py` — **không tạo thư mục con**.

**Quy tắc phân loại một câu:** câu hỏi người dùng cuối đặt ra khi đang chat → Human. Câu hỏi chỉ người sửa hệ thống mới cần → Dev. Mã `DEC-xxx`, link `audit/`, cụm "đã/chưa kiểm chứng" **không được** xuất hiện trong `docs KB/Human` và `knowledge/`.

---

## 3. Trạng thái hai KB chính

| KB | Local | Web | Ghi chú |
|---|---|---|---|
| `GS9 Knowledge VNG AI` | 20 doc + 49 ảnh | **Đã sync** | Chat-test ảnh ĐẠT |
| `GS9 CFL Knowledge Agent` | 8 doc | **Đã sync** (17/08) | Có bảng binding Agent-KB |

`GS9 CFL Plan Version`: 12 doc + 29 ảnh, URI đã vá, **đã up lên Web** (17/08).

---

## 4. Việc đang mở

### 4.1 ĐÃ XONG — người dùng xác nhận 17/08/2026
1. ~~Sync `knowledge/GS9 CFL Knowledge Agent` (8 file) lên Web~~ ✅
2. ~~Up lại `knowledge/GS9 CFL Plan Version/V5` (12 file, URI đã vá)~~ ✅
3. ~~Chat-test `GS9 CFL Knowledge Curator` xem luật trích dẫn ảnh có ăn không~~ ✅

### 4.2 ĐÃ XỬ TẠM 17/08/2026 — bốn Agent nay đã có KB, nhưng là **kho tạm**

`Player Communications` → `GS9 CFL Plan Version`; `Economy Offer Analyst` → `GS9 CFL Data Daily`; `CS Copilot` và `GM Policy Advisor` → `GS9 Knowledge VNG AI` (fallback nền tảng). Đã xác minh bằng cách đọc lại dialog Web sau khi lưu (DEC-060, `audit/agent-kb-binding-4-agent-2026-08-17.md`).

**Chưa đóng được gap thật.** Kho tạm là giải pháp cầu. Bốn KB nghiệp vụ đúng vẫn cần soạn nội dung, khi có phải đổi binding và cập nhật lại bảng ở `AgentCFL-02-ma-tran-so-sanh-16-agent.md` (Human) + `Agent-ho-so-16-agent-cfl.md` (Dev):

| Agent | KB đúng còn thiếu | Cần gì để dựng |
|---|---|---|
| `CS Copilot` | `GS9 CFL CS FAQ & Policy` | mới có file định dạng — cần top câu hỏi CS, câu trả lời chuẩn, ranh giới escalation GM/kỹ thuật, chính sách hoàn tiền |
| `GM Policy Advisor` | `GS9 CFL GM Policy & Sanction` | chưa tồn tại — cần bảng điều khoản xử phạt, quy trình, tiền lệ |
| `Player Communications` | `GS9 CFL Event Calendar & Brief` | chưa tồn tại — cần lịch sự kiện, brief đã duyệt, mẫu thông báo |
| `Economy Offer Analyst` | `GS9 CFL Item Catalog` | chưa tồn tại — phải tách khỏi `GS9 CFL Item Profile`, rà dữ liệu P0 trước |

Đặc biệt lưu ý `CS Copilot` và `GM Policy Advisor`: kho đang gắn **không chứa chính sách CS hay điều khoản xử phạt nào**, nên câu trả lời của chúng về hai mảng đó vẫn không có nguồn CFL bảo chứng.

### 4.3 Gate chất lượng — đã mở một phần 17/08/2026

Chat-test thật 3 Agent trên KB an toàn (DEC-062, `audit/agent-chat-test-2026-08-17.md`):

| Agent | Kết quả |
|---|---|
| `Player Communications` × Plan Version | **Đạt** — nội dung khớp nguồn, ảnh render thật, tự đánh dấu chỗ thiếu bằng chứng |
| `Knowledge Curator` × 2 kho | **Có điều kiện** — không bịa chính sách, nhưng sai sự thật về cấu hình hệ thống |
| `CS Copilot` × Knowledge VNG AI | **Đạt về guardrail** — từ chối trả lời vì kho không đúng loại nguồn |

**13/16 Agent vẫn *Bị chặn–Chưa xác định*.** Chưa test 3 Agent gắn KB nhạy cảm (`Incident Triage`→PUM, `Player Voice Analyst`→Sentiment, `KPI Experiment Analyst`→Kho Tổng Hợp) vì lượt này giới hạn ở KB an toàn.

### 4.4 CẠM BẪY MỚI — gắn KB xong phải bật công cụ truy hồi (DEC-061)

Gắn KB **không** tự cho Agent quyền đọc kho. Công cụ `Tìm theo ngữ nghĩa` / `Tìm theo từ khóa` là tập cấu hình riêng, bị mờ khi Agent chưa có KB, và **không tự bật** sau khi bind. Triệu chứng: cây suy luận trả `tool not found: search_knowledge_base (available: ask_user, thinking, todo_write)` rồi Agent quay ra hỏi lại người dùng.

Đã bật cho 3 Agent (Player Communications 3→5 tool, Economy Offer Analyst 3→5, GM Policy Advisor 2→4). `CS Copilot` chế độ Trả lời nhanh không có tab Công cụ, truy hồi chạy ngầm.

**Dựng Agent mới luôn phải kiểm bước này.**

### 4.5 ⚠️ ƯU TIÊN CAO — nghi vấn ảnh minh hoạ thành nguồn dữ kiện sai, CHƯA KẾT LUẬN

`Knowledge Curator` khẳng định 3 thứ sai (hệ thống "chỉ có 6 trợ lý"; có kho `Knowledge VNG - Image Assets`; có nguồn `Drive CFL Viax` sync 15 phút). Cả 3 khớp gần như từng ký tự với nội dung trong 3 **ảnh chụp màn hình** nằm trong `GS9 Knowledge VNG AI` (`image-26`, `image-41`, `image-25`).

**Đã kiểm chứng bằng `keyword_search` vào chỉ mục:** nền tảng OCR ảnh **và** sinh mô tả ảnh **lúc nạp**, lưu thành chunk chữ tra cứu được (`chunk_type: image_caption` và `text`).

**BẰNG CHỨNG MỚI cuối phiên — đã rõ cơ chế.** Trace lượt chạy lại ghi thẳng bước `Lấy tài liệu: image-01-tong-quan-danh-sach-knowledge.png` (ảnh `docs KB/Asset/chat/case2-trace-lay-tai-lieu-anh.png`). Agent **chủ động truy hồi một tài liệu ảnh làm nguồn**, gọi đích danh tên tệp `.png`. Mệnh đề "ảnh trong kho được truy hồi làm nguồn, nội dung trong ảnh thành dữ kiện" nay ở mức **Đã kiểm chứng**.

**Biến số còn lại:** lượt này chạy model `deepseek-v4-flash` (khác lượt trước `hosted_vllm/qwen3.6-...`); test lại phải ghi rõ model.

**Không dùng lời Agent tự nhận làm bằng chứng.** Khi bị hỏi vặn nó quay ra nhận "tự chế toàn bộ" và nói 4 KB "không tồn tại / rỗng" — **cả 4 đều sai** (thực tế 7, 8, 8, 8 tài liệu).

**Đã vá tạm:** gắn cảnh báo "ảnh chụp một thời điểm" cạnh 7 ảnh mang danh sách trong nguồn Human. **Không giải quyết gốc.**

**CẬP NHẬT 17/08/2026 (phiên 5) — chưa chạy lại được, và có giả thuyết cạnh tranh mới.** Đọc trực tiếp trạng thái phân tích tệp trên Web: **49 ảnh đã `Hoàn tất`, nhưng cả 21 tài liệu chữ đang `Chờ xử lý`** (1 file `Đang xử lý`, hàng đợi chạy tuần tự). Nghĩa là hiện tại **ảnh là nguồn duy nhất trong chỉ mục**.

→ Sinh ra giả thuyết cạnh tranh chưa loại trừ: Case 2 sai **không phải vì Agent ưu tiên ảnh hơn chữ**, mà có thể vì lúc đó **chữ cũng chưa vào chỉ mục** nên ảnh là thứ duy nhất truy hồi được. Khớp với chi tiết vòng tìm ngữ nghĩa đầu tiên trả `Không có kết quả`.

→ **Không chạy lại Case 2 khi chữ còn Chờ xử lý** — sẽ tái hiện lỗi vì lý do tầm thường, không phân biệt được hai giả thuyết. **Điều kiện để chạy:** lọc `Chờ xử lý` + `Đang xử lý` đều rỗng, và lọc `Hoàn tất` đếm đủ **70** tài liệu.

**Việc phiên sau:** đợi đủ điều kiện trên → chạy lại câu hỏi Case 2, ghi rõ model → nếu vẫn sai thì **thử tắt VLM/đọc ảnh ở KB thuần hướng dẫn** (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`), giữ VLM ở KB nghiệp vụ (`Plan Version` — Case 1 chứng minh chạy tốt) → so 3 kết quả. Chi tiết: `audit/agent-chat-test-2026-08-17.md` mục 6, 7 và **8**.

### 4.6 Việc phát sinh khác từ chat-test

- Lỗi truy hồi `Knowledge Curator`: kho có nội dung nhưng lấy nhầm đoạn → thử tăng Top K hoặc bật `Thông tin tài liệu` rồi test lại.
- Case 1 bỏ sót 2 ảnh **có thật** trong kho (`image-v5-06`, `image-v5-07`) khi lập bảng đối chiếu.

### 4.7 THIẾU NỘI DUNG — chưa có tài liệu "nên dựng những loại kho nào"

Người dùng phát hiện cuối phiên 4: **cả file thuyết trình lẫn kho `GS9 Knowledge VNG AI` đều không có phần hướng dẫn thiết kế danh mục kho.** Đã kiểm: `docs KB/Human/` chỉ có `KB-03-tai-lieu-rag-wiki.md` (loại kho **kỹ thuật**: Tài liệu vs FAQ) và `KBCFL-12-quy-uoc-va-ranh-gioi-du-lieu.md` (ranh giới dữ liệu riêng của CFL). Không tài liệu nào trả lời "một nhóm mới bắt đầu thì nên dựng những kho nào".

**Đã vá một nửa:** thêm vào HTML mục 10 phần *"Bắt đầu từ đâu — bốn loại kho hầu như nhóm nào cũng cần"* (kho sự thật đã chốt · quy trình và chính sách · kế hoạch và lịch · kết quả), kèm 3 câu hỏi quyết định tách/gộp (ai được xem · bao lâu đổi một lần · đã chốt hay chưa) và cảnh báo lỗi hay gặp là chia kho theo *nguồn dữ liệu* thay vì theo *câu hỏi người ta sẽ hỏi*.

**ĐÃ LÀM 17/08/2026 (phiên 5, DEC-065).** Tạo `docs KB/Human/KB-20-thiet-ke-danh-muc-kho.md` → sinh ra `doc-20-thiet-ke-danh-muc-kho.md` trong `GS9 Knowledge VNG AI`.

Đính chính ghi chép cũ: **không cần mở rộng `HUMAN_SOURCE_PREFIXES`** — hằng đó chỉ liệt kê tiền tố (`KB`, `Agent`), **không khoá dải số nào**. Chỉ cần đánh số từ 20 trở đi là tránh được va chạm với `Agent-13`. Năm chỗ khoá cứng số 20 đã sửa: `EXPECTED_MODULE_COUNT` trong builder, 3 chỗ trong `test_build_handbook.py`, `so-tay-tao-knowledge-base-v3.md`, `PROJECT.md`.

Nội dung gồm: nguyên tắc quyền ở cấp kho · bảng 4 loại kho nên dựng theo thứ tự · 3 câu hỏi tách/gộp · lỗi chia kho theo nguồn dữ liệu · cách đặt tên kho · khi nào rà lại danh mục.

**ĐÃ LÊN WEB** — người dùng nạp `doc-20` vào KB `GS9 Knowledge VNG AI` trên `vnggames.ai` ngày 17/08/2026. Mục 4.7 khép lại. Chưa chat-test xem Agent có tra trúng tài liệu này không.

### 4.8 Chưa kiểm chứng
- Hành vi connector khi **đổi tên / di chuyển / xoá** tệp
- Ảnh render 2 lần trong chat (xem mục 5) — chưa báo cho ai chịu trách nhiệm nền tảng

**Đã đóng 17/08/2026 (phiên 5, máy công ty, DEC-063):** Converter Plan V5 bố cục ảnh phẳng (DEC-054) nay **đã kiểm chứng end-to-end**. 6 test trước đây skip nay chạy và pass, 29 ảnh sinh ra khớp SHA256 tuyệt đối với bundle đang commit. Sửa 1 dòng test sai vị trí thư mục (`tests/test_convert_cfl_plan_html.py:94`). Gate hiện tại: `Ran 30 tests / OK`, 0 skip.

### 4.9 ĐÃ XONG 19/08/2026 — hàng đợi nền tảng thông, gate sạch (DEC-073)

**Bối cảnh:** cuối phiên 5, người dùng (1) đưa tính năng mới **"Thêm vào tri thức"** (nút `+` dưới câu trả lời chat, lưu thành tài liệu Markdown vào kho, có `Lưu nháp`/`Xuất bản`) — đã viết vào `KB-11-chat-kiem-thu-va-bao-tri.md`, kèm 3 ảnh `image-50/51/52`; (2) crop lại 23 ảnh cũ cho gọn (nội dung không đổi) — `image-01`→`image-14` (trừ vài số), `image-26`→`image-34`; (3) đồng bộ cả 26 ảnh (23 sửa + 3 mới) lên Web.

**Cập nhật 18/08/2026 (phiên 6) — đã kiểm chứng, không còn là nghi vấn:**

- Sau ~9,5 tiếng (17/08 18:49 → 18/08 04:20) vẫn **0/26 ảnh `completed`**: 21 `pending`, 4 `processing` (`image-02/27/51/52`), 1 `finalizing` (`image-28`).
- Panel **"Xem tiến trình"** (menu ⋯ của từng tài liệu trên Web) cho `image-28` và `image-02`: cả hai **`Chờ` · 0/5 giai đoạn**, 5 bước đều "Đang chờ", kèm bộ đếm lần thử `#1 #2` và `#1 #2 #3`. → job **được xếp hàng và thử lại nhiều lần nhưng không worker nào chạy**. Đây là tắc ở tầng nền tảng, không phải lỗi nội dung file hay lỗi cấu hình KB (DEC-071).
- `image-28` có `failed_stages.summary = "failed to update knowledge: context deadline exceeded"`, từng lên `finalizing` rồi tụt về `pending`.
- **Không lọc ra tài liệu nào ở trạng thái "Lỗi"** — MCP không trả `parse_status` lỗi cho tài liệu nào.
- **"Phân tích lại" không gỡ được tắc** (chỉ thêm một lần thử vào hàng đợi đang không chạy) → đừng bấm hàng loạt.
- Phát sinh thêm: **21 `doc-*.md` bị nạp lại lúc 00:00–00:01 ngày 18/08**, ID mới, `pending`, `disabled` → KB hiện **không có tài liệu chữ nào được lập chỉ mục** (DEC-072).
- **Việc cần làm tiếp là báo team vận hành nền tảng**, kèm: KB id `cefadf09-4187-46ac-a765-591e3255a4a4`, tenant `10012`, 47 tài liệu treo (26 png + 21 md), mốc treo 17/08 18:49 và 18/08 00:01, thông điệp lỗi ở trên.

**Trạng thái lúc dừng phiên 5:** 26/52 ảnh trong `GS9 Knowledge VNG AI` đứng ở `pending`/`processing`/`finalizing`, **0 tiến triển sau 25 phút theo dõi** (2 lần kiểm qua MCP `list_documents`, cách nhau 20 phút, số liệu y hệt). Nghi hàng đợi xử lý ảnh trên nền tảng bị tắc — đã đề nghị người dùng tự kiểm trên Web (mục Documents, lọc trạng thái, xem có rơi vào "Lỗi" không, thử "Phân tích lại" một file) nhưng **chưa có phản hồi trước khi dừng phiên**.

**Việc phải làm khi vào lại, theo thứ tự:**
1. Hỏi người dùng tình trạng hàng đợi (có tự hết tắc chưa, có phải bấm gì không).
2. Kiểm lại qua MCP: `list_documents(knowledge_base_id="cefadf09-4187-46ac-a765-591e3255a4a4", page_size=100)`, lọc `file_type == "png"`, đếm `parse_status`. Cần **52/52 `completed`**.
3. Khi đủ điều kiện: lấy `file_path` của **26 ảnh vừa xử lý xong** (không phải cả 52 — 26 ảnh còn lại giữ nguyên URI, xem DEC-069), viết lại `image-map.json`.
4. `python scripts/build_handbook.py` — sẽ tự nhúng URI mới vào các module tham chiếu, gồm cả `doc-11` (nội dung mới "Thêm kiến thức ngay trong lúc chat" chưa từng build thành công vì thiếu URI).
5. ~~Sửa 2 chỗ khoá cứng "49 ảnh" → "52 ảnh" trong test~~ — **đã làm 18/08** (`tests/test_build_handbook.py:87-88`). Còn một chỗ phải sửa **sau khi build lại**: `test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs` khoá số lượt tham chiếu ảnh là `61`, sẽ đổi khi `doc-11` nhúng thêm 3 ảnh.
6. Chạy full gate (`build_handbook.py`, `unittest discover`, `link_plan_v5_minio.py --check`), báo người dùng đủ 30 test OK.
7. Người dùng đồng bộ các `.md` đã build lại (ít nhất `doc-11`) lên Web lần cuối.

**Đừng lặp lại sai lầm cũ:** không cần rà lại URI của tất cả 52 ảnh — DEC-069 đã chứng minh 26 ảnh không đổi giữ nguyên URI, chỉ cần lấy URI cho đúng 26 ảnh vừa chuyển trạng thái.

**Việc 1 (ưu tiên cao, mục 4.5) vẫn đang chờ đúng điều kiện tương tự** — không chạy lại Case 2 cho tới khi toàn bộ 21 tài liệu chữ + 52 ảnh đều `Hoàn tất` (xem `audit/agent-chat-test-2026-08-17.md` mục 8).

---

## 5. Cạm bẫy đã gặp thật

**Google Drive mất kết nối rồi tự "Restore" ra layout cũ (DEC-059, 17/08/2026).** Đây là sự cố nặng nhất từng gặp: Drive rớt mount, sau đó tự phục hồi nhưng trộn cấu trúc cũ (trước 15/08) chồng lên cấu trúc mới — thư mục `knowledge` thật bị đẩy thành `knowledge (1)`, `.git` mất lịch sử, hàng trăm file lệch nội dung.
→ **Cách khôi phục đã dùng, làm lại được nếu tái diễn:** (1) clone bản sạch từ GitHub ra **ngoài** Drive để đối chiếu, không sửa gì trên Drive trước khi biết rõ; (2) nếu thư mục thật đổi tên thành `(1)` thì **đổi tên lại** (không xoá-tạo-mới) để giữ ID và không đứt kết nối connector; (3) thay `.git` hỏng bằng bản sạch từ clone; (4) `git restore .` rồi `git clean -f` từng thư mục con; (5) rà thủ công toàn cây tìm file/thư mục kiểu `(1)`, `(2)`, `Copy of`, thư mục chỉ có `desktop.ini`; (6) xác nhận cuối bằng `git diff --stat origin/main HEAD` phải **rỗng tuyệt đối**, không chỉ tin `git status`.

**Google Drive khoá file khi ghi.** Project nằm trên Drive nên file hay bị khoá ngay sau khi ghi. Dấu hiệu: `Invalid request code` / `OSError: Errno 22` / `Incorrect function`, và `stat` cho `Links: 0`. Không tool nào của agent vượt qua được — chỉ File Explorer ép tải về được.
→ **Ghi file qua file tạm rồi `os.replace`.** Ghi đè trực tiếp đã từng làm **mất sạch nội dung một file nguồn** (16/08).

**URI ảnh chết sau khi re-sync.** Nạp lại ảnh qua connector là URI cũ chết toàn bộ. Lấy lại hàng loạt bằng trường `file_path` của API, đừng lấy URI trong `description` (chỉ 24/49 ảnh có, nhiều ảnh lại có 2 URI khó chọn).

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. Với KB chưa share (ví dụ `GS9 CFL Plan Version`), lấy token qua `/api/auth/token?sub_app=kb` rồi gọi `https://miniapp.vnggames.ai/kb/v1/api/...` kèm `Authorization: Bearer` — gọi bằng cookie bị CORS chặn. Cùng API này (`GET /kb/v1/api/agents`) dùng để lấy binding KB thật của từng Agent qua trường `config.knowledge_bases`.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun. Tool đọc trang thường không thấy nội dung; phải qua `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. Dialog cấu hình Agent thì lại render ở document chính.

**Ảnh render 2 lần trong chat.** Nền tảng tự render khi gặp `minio://` mà không đợi markdown khép kín → ảnh hiện 2 lần kèm ký tự `![`, `](`, `)` lộ ra. **Lỗi nền tảng, không phải lỗi tài liệu.**

---

## 6. Lệnh chuẩn

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

**Gate:** strict build ra 20 module + 8 doc KB Agent, 60 link MinIO, HTML offline tự chứa, `Ran 30 tests`/`OK`. Không dùng `--allow-missing-minio` cho bản bàn giao.

---

## 7. An toàn

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che (vá 16/08 — trước đó **không** được che).
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. Đã đổi tên file theo quy ước (DEC-055) nhưng **không mở, không đọc nội dung**.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` từng bị đánh giá rủi ro, nay **người dùng xác nhận giữ nguyên** vì nền tảng chỉ dùng nội bộ.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → mọi cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại trước khi kết luận.

---

## 8. Tài liệu thuyết trình

`gioi-thieu-knowledge-base-va-agent.html` — bản giới thiệu cho team, **12 mục gom thành 5 phần** (1,35 MB, tự chứa, in PDF được), sắp xếp lại 17/08/2026 theo DEC-067:

| Phần | Mục |
|---|---|
| **I Vì sao cần** | 01 Vấn đề đang giải |
| **II KB và Agent là gì** | 02 Knowledge Base · 03 Agent · 04 Cách phối hợp |
| **III Có lợi thế nào** | 05 Thử thật trên dữ liệu CFL (3 case) |
| **IV Đang có gì** | 06 Kho của CFL · 07 Trợ lý của CFL · 08 Ai gắn kho nào · 09 Trạng thái |
| **V Xây tiếp thế nào** | 10 Đề xuất cấu trúc · 11 Quy trình 6 bước · 12 Nguyên tắc an toàn |

**Sửa file này phải biết:** mốc `<!-- N -->` giữa các section trong bản gốc **không đồng nhất** (có mục thiếu, có mục ghi sai số). Tách section phải quét theo thẻ `<section id=>`, đừng dựa vào mốc comment. Ghi qua tệp tạm + `os.replace`, sao lưu trước, rồi kiểm lại số section, link mục lục, cân bằng `<div>`, số ảnh.

- **Mục 09 Thử thật trên dữ liệu CFL** — 3 case chat-test ngày 17/08/2026 kèm **5 ảnh chụp hội thoại thật** do người dùng cung cấp (`docs KB/Asset/chat/`). **Chỉ trình bày phần năng lực**: case 1 làm được việc thật, case 2 biết nói "không tìm thấy" thay vì bịa, case 3 CS Copilot ra bản DRAFT trả lời khách + đề xuất chuyển tiếp.

  ⚠️ **File HTML là bản GIỚI THIỆU tính năng để present cho team** — chỉ đưa vào những gì đã chốt và cho thấy giá trị. **Không đưa lỗi, nghi vấn, hay điều tra nội bộ vào file này** (người dùng đã nhắc thẳng hai lần). Chỗ đó thuộc `STATUS.md` và `audit/`. Ảnh case 2 đã được **cắt bỏ phần chứa thông tin sai** trước khi nhúng.
- **Mục 10 Đề xuất cấu trúc** — mở đầu bằng *"Bắt đầu từ đâu — bốn loại kho hầu như nhóm nào cũng cần"* (bổ sung cuối phiên, xem 4.7), rồi hai phương án đặt cạnh nhau kèm đánh đổi: **A** chia theo mức nhạy cảm × đối tượng đọc × nhịp cập nhật (bản 7 tầng đã chốt, viết lại cho dễ đọc), **B** chia theo 4 nhóm công việc. Kèm bảng 4 kho cần dựng + ai cung cấp gì, gợi ý thứ tự làm, 4 câu hỏi để team chốt. **Đây là phần soạn để team bàn, chưa chốt.**

**Đã sửa lỗi tồn tại từ trước:** 10 ảnh cũ có `loading="lazy"` nên **không render khi in PDF**. Đã bỏ lazy toàn bộ, kiểm chứng 13/13 ảnh tải được.

**Số liệu trong file là ảnh chụp 17/08/2026** — binding và danh sách KB đổi thì phải cập nhật lại.
