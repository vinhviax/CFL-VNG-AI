# Handoff — Knowledge Base VNG

**Cập nhật:** 17/08/2026 (phiên 4 — kho tạm, công cụ truy hồi, chat-test, case study)
**Phiên bản:** 3.6.0 · **Test:** `Ran 30 tests` / `OK` (6 skip do thiếu HTML nguồn Plan V5 trên máy này)

---

## 1. Đọc gì trước

| Thứ tự | File | Vì sao |
|---|---|---|
| 1 | `AGENTS.md` | Quy tắc làm việc, ranh giới an toàn, bảng phân loại đối tượng đọc |
| 2 | File này | Trạng thái và việc đang mở |
| 3 | `STATUS.md` | Nhật ký theo phiên, chi tiết hơn |
| 4 | `DECISIONS.md` | 62 quyết định — tra khi không hiểu vì sao làm vậy |
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

**Việc phiên sau:** đợi KB xử lý xong → chạy lại câu hỏi Case 2 → nếu vẫn sai thì **thử tắt VLM/đọc ảnh ở KB thuần hướng dẫn** (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`), giữ VLM ở KB nghiệp vụ (`Plan Version` — Case 1 chứng minh chạy tốt) → so 3 kết quả. Chi tiết: `audit/agent-chat-test-2026-08-17.md` mục 6.

### 4.6 Việc phát sinh khác từ chat-test

- Lỗi truy hồi `Knowledge Curator`: kho có nội dung nhưng lấy nhầm đoạn → thử tăng Top K hoặc bật `Thông tin tài liệu` rồi test lại.
- Case 1 bỏ sót 2 ảnh **có thật** trong kho (`image-v5-06`, `image-v5-07`) khi lập bảng đối chiếu.

### 4.7 THIẾU NỘI DUNG — chưa có tài liệu "nên dựng những loại kho nào"

Người dùng phát hiện cuối phiên 4: **cả file thuyết trình lẫn kho `GS9 Knowledge VNG AI` đều không có phần hướng dẫn thiết kế danh mục kho.** Đã kiểm: `docs KB/Human/` chỉ có `KB-03-tai-lieu-rag-wiki.md` (loại kho **kỹ thuật**: Tài liệu vs FAQ) và `KBCFL-12-quy-uoc-va-ranh-gioi-du-lieu.md` (ranh giới dữ liệu riêng của CFL). Không tài liệu nào trả lời "một nhóm mới bắt đầu thì nên dựng những kho nào".

**Đã vá một nửa:** thêm vào HTML mục 10 phần *"Bắt đầu từ đâu — bốn loại kho hầu như nhóm nào cũng cần"* (kho sự thật đã chốt · quy trình và chính sách · kế hoạch và lịch · kết quả), kèm 3 câu hỏi quyết định tách/gộp (ai được xem · bao lâu đổi một lần · đã chốt hay chưa) và cảnh báo lỗi hay gặp là chia kho theo *nguồn dữ liệu* thay vì theo *câu hỏi người ta sẽ hỏi*.

**CÒN THIẾU — việc phiên sau:** đưa nội dung này vào **kho `GS9 Knowledge VNG AI`** để Agent tra được, không chỉ nằm trong file HTML.
Vướng kỹ thuật: dải `KB-NN-*` đang kín 00–12, `KB-13` sẽ **đụng** `Agent-13`. Hai cách:
1. Chèn vào một file đã có — hợp nhất là `KB-03-tai-lieu-rag-wiki.md` (đang nói về loại kho) hoặc `KB-00-gioi-thieu-va-quick-start.md`.
2. Mở rộng dải trong `HUMAN_SOURCE_PREFIXES` (`scripts/build_handbook.py`) rồi tạo file mới — phải sửa cả test khoá số lượng module (`test_build_handbook.py` đang khoá đúng 20 module).

Cách 1 nhanh và không đụng gate. **Chưa làm, chờ người dùng chọn.**

### 4.8 Chưa kiểm chứng
- Converter Plan V5 chạy với bố cục ảnh phẳng mới (DEC-054) — 6 test luôn skip vì HTML nguồn chỉ có trên máy công ty
- Hành vi connector khi **đổi tên / di chuyển / xoá** tệp
- Ảnh render 2 lần trong chat (xem mục 5) — chưa báo cho ai chịu trách nhiệm nền tảng

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

`gioi-thieu-knowledge-base-va-agent.html` — bản giới thiệu cho team, **12 phần** (0,66 MB, tự chứa, in PDF được): vấn đề · KB là gì · Agent là gì · cách phối hợp · quy trình 6 bước · 10 kho của CFL · 16 trợ lý · bảng binding · **case study** · **đề xuất cấu trúc** · nguyên tắc an toàn · trạng thái.

- **Mục 09 Thử thật trên dữ liệu CFL** — 3 case chat-test ngày 17/08/2026 kèm **5 ảnh chụp hội thoại thật** do người dùng cung cấp (`docs KB/Asset/chat/`). **Chỉ trình bày phần năng lực**: case 1 làm được việc thật, case 2 biết nói "không tìm thấy" thay vì bịa, case 3 CS Copilot ra bản DRAFT trả lời khách + đề xuất chuyển tiếp.

  ⚠️ **File HTML là bản GIỚI THIỆU tính năng để present cho team** — chỉ đưa vào những gì đã chốt và cho thấy giá trị. **Không đưa lỗi, nghi vấn, hay điều tra nội bộ vào file này** (người dùng đã nhắc thẳng hai lần). Chỗ đó thuộc `STATUS.md` và `audit/`. Ảnh case 2 đã được **cắt bỏ phần chứa thông tin sai** trước khi nhúng.
- **Mục 10 Đề xuất cấu trúc** — mở đầu bằng *"Bắt đầu từ đâu — bốn loại kho hầu như nhóm nào cũng cần"* (bổ sung cuối phiên, xem 4.7), rồi hai phương án đặt cạnh nhau kèm đánh đổi: **A** chia theo mức nhạy cảm × đối tượng đọc × nhịp cập nhật (bản 7 tầng đã chốt, viết lại cho dễ đọc), **B** chia theo 4 nhóm công việc. Kèm bảng 4 kho cần dựng + ai cung cấp gì, gợi ý thứ tự làm, 4 câu hỏi để team chốt. **Đây là phần soạn để team bàn, chưa chốt.**

**Đã sửa lỗi tồn tại từ trước:** 10 ảnh cũ có `loading="lazy"` nên **không render khi in PDF**. Đã bỏ lazy toàn bộ, kiểm chứng 13/13 ảnh tải được.

**Số liệu trong file là ảnh chụp 17/08/2026** — binding và danh sách KB đổi thì phải cập nhật lại.
