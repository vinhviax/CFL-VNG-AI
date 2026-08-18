Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root project là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), team GS9 dùng.

Hiện có **10 kho tri thức** và **16 trợ lý** (6 mặc định của nền tảng + 10 custom cho LiveOps). `GS9 Knowledge VNG AI` local có **21 tài liệu Markdown** (`doc-00`→`doc-20`) + **52 ảnh PNG** (`image-01`→`image-52`, kể cả 3 ảnh mới thêm hai phiên trước).

File thuyết trình: `gioi-thieu-knowledge-base-va-agent.html` — **12 mục gộp thành 5 phần**, tự chứa, in PDF được, mục lục dạng cột trái.

==================================================
1. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -3 --oneline`. Commit mới nhất phải là `af4a1e2` ("docs: xác định nguyên nhân hàng đợi tắc (DEC-071/072), sửa test khoá 49→52 ảnh") — đã push GitHub cuối phiên 6 (18/08, máy nhà).

**Luôn xác nhận local khớp remote trước khi tin `git status`:**
```powershell
git fetch origin
git diff --stat origin/main HEAD
```
Phải rỗng tuyệt đối. Nếu KHÔNG rỗng — có thể Drive lại gây sự cố như đã gặp nhiều lần (xem mục 7).

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` (đặc biệt mục 4.9 — việc treo đầu phiên, đã cập nhật 18/08 với bằng chứng cụ thể) → `STATUS.md` (mục mới nhất trên cùng, mục 18/08 phiên 6). `DECISIONS.md` (72 quyết định) tra khi cần hiểu vì sao.

==================================================
2. VIỆC ƯU TIÊN SỐ 1 KHI VÀO PHIÊN — HÀNG ĐỢI NỀN TẢNG TẮC, ĐÃ XÁC ĐỊNH NGUYÊN NHÂN, CHỜ THÔNG
==================================================

**Đã kiểm chứng ở phiên 6 (18/08, máy nhà) — không còn là nghi vấn:** hàng đợi xử lý của nền tảng bị tắc, không phải lỗi file hay cấu hình KB. Mở panel **"Xem tiến trình"** (menu ⋯ của tài liệu, trên Web, đọc qua shadow DOM) cho `image-28` và `image-02`: cả hai đứng ở **`Chờ` · 0/5 giai đoạn**, 5 bước (Phân tích tài liệu → Chia đoạn → Vector hóa → Đa phương thức → Hậu xử lý) đều "Đang chờ", kèm bộ đếm lần thử `#1 #2` / `#1 #2 #3` — job xếp hàng, hết giờ, xếp lại, **không worker nào chạy**. `image-28` có `failed_stages.summary = "failed to update knowledge: context deadline exceeded"`. Chi tiết đầy đủ: DEC-071, `HANDOFF.md` mục 4.9.

**Trạng thái treo, tính tới lúc dừng phiên 6:**
- 26 ảnh (23 crop lại `image-01→14, 26→34` phần + 3 ảnh mới `image-50/51/52`), nạp lúc 17/08 18:48–18:49: **0/26 `completed`** (21 `pending`, 4 `processing`, 1 `finalizing`).
- 21 file `doc-*.md`, bị nạp lại lúc 18/08 00:00–00:01 (một lần đồng bộ Toàn bộ định kỳ, không phải ai đó sửa tay — xem DEC-072): **0/21 `completed`**, tất cả `disabled`. Hệ quả: KB `GS9 Knowledge VNG AI` hiện **không có tài liệu chữ nào được lập chỉ mục**, Agent trỏ vào kho này (CS Copilot, GM Policy Advisor, Knowledge Curator) chỉ tra được ảnh.

**Gate hiện đang có đúng 1 FAIL đã biết** (`test_project_image_map_covers_all_merged_assets`, thiếu URI MinIO cho `image-50/51/52`) — tín hiệu đúng, KHÔNG phải lỗi cần vá tạm. Đừng dùng `--allow-missing-minio`. Test khoá cứng "49 ảnh" đã sửa thành "52" (phiên 6) — đừng sửa lại lần nữa.

**Việc làm theo thứ tự:**
1. Hỏi người dùng: đã báo team vận hành nền tảng chưa, có phản hồi gì không (bản mô tả sự cố soạn sẵn nằm trong lịch sử chat phiên 6, cũng có thể dựng lại từ DEC-071).
2. Kiểm qua MCP: `list_documents(knowledge_base_id="cefadf09-4187-46ac-a765-591e3255a4a4", page_size=100)` (4 trang, page_size 20 mỗi lần nếu 100 quá dài), lọc `file_type=="png"` đếm `parse_status`, riêng lọc `file_type=="md"` đếm `parse_status`/`enable_status`. Cần đủ **52/52 png `completed`** VÀ **21/21 md `completed` + `enabled`**. Kết quả dài — ghi ra file rồi lọc bằng Python, đừng đọc thẳng cả JSON.
3. Khi đủ điều kiện: lấy `file_path` của **đúng 26 ảnh vừa xử lý xong** (không phải cả 52 — xem mục 3 bên dưới lý do), viết lại `image-map.json` trong `knowledge/GS9 Knowledge VNG AI/image-map.json` (script: đọc JSON hiện có, merge, ghi qua file tạm + `os.replace`).
4. `python scripts/build_handbook.py` — build lại 21 module, gồm cả `doc-11` (nội dung "Thêm kiến thức ngay trong lúc chat" chưa từng build thành công vì thiếu URI).
5. Sửa nốt chỗ khoá cứng còn lại: `test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs` (trong `tests/test_build_handbook.py`) đang khoá số lượt tham chiếu ảnh là `61` — tính lại số đúng sau khi `doc-11` có thêm 3 ảnh rồi sửa.
6. Chạy full gate, xác nhận `Ran 30 tests OK` không còn FAIL nào.
7. Báo người dùng — họ sẽ đồng bộ `.md` đã build lại lên Web lần cuối (ít nhất `doc-11`).

**Nếu hàng đợi vẫn 0 tiến triển khi vào phiên:** đừng tự chờ nhiều vòng — hỏi người dùng ngay tình trạng phản hồi từ team nền tảng, rồi làm việc khác không phụ thuộc hàng đợi (xem có việc gì ở mục 6 "Trạng thái Agent" có thể làm).

==================================================
3. ĐÍNH CHÍNH QUAN TRỌNG — ĐỒNG BỘ GOOGLE DRIVE KHÔNG LÀM CHẾT MỌI URI (DEC-069, xác nhận lại DEC-072)
==================================================

Ghi chép cũ (DEC-052) từng khiến hiểu lầm rằng "mọi lần đồng bộ Drive đều làm chết URI ảnh". **Sai.** Vụ chết URI 49/49 ngày 11/08 có nguyên nhân riêng: 49 ảnh khi đó bị **di trú sang một KB khác hẳn** (từ `GS9 Knowledge VNG - Image Assets` sang `GS9 Knowledge VNG AI`, DEC-043) — tức tạo lại thành tài liệu mới trong KB mới, chắc chắn sinh ID/URI mới cho toàn bộ.

**Bằng chứng đo được hai lần độc lập:**
- Phiên 5 (17/08): đồng bộ Tăng dần trong CÙNG một KB (23 ảnh sửa + 3 ảnh mới) → 26 ảnh không đổi giữ nguyên `completed` VÀ URI y hệt.
- Phiên 6 (18/08, DEC-072): đọc trực tiếp cấu hình nguồn trên Web thấy **Chế độ đồng bộ = Toàn bộ** (không phải Tăng dần như tưởng), lần chạy ~00:00 ngày 18/08 tạo lại toàn bộ 21 `doc-*.md` nhưng **26 ảnh không đổi vẫn giữ nguyên document cũ và URI cũ** — đối chiếu bằng script: 26/26 khớp tuyệt đối với `image-map.json` sinh 16/08, 0 lệch.

**Quy tắc đúng để dùng từ nay:** dù chế độ đồng bộ là Tăng dần hay Toàn bộ, chỉ file **thật sự đổi nội dung** (hash khác) hoặc file mới mới bị tạo lại document/URI; **không cần rà lại toàn bộ `image-map.json` sau mỗi lần sync** — chỉ cần xác định đúng tập file vừa chuyển trạng thái khỏi `completed` rồi lấy URI cho đúng tập đó.

**Hệ quả cần nhớ (DEC-072):** một lần đồng bộ Toàn bộ có thể đưa cả kho tài liệu chữ về `pending`/`disabled` một khoảng thời gian (lần này toàn bộ 21 `doc-*.md`) — dù ảnh không đổi vẫn an toàn. Tránh sửa hàng loạt `.md` rồi đồng bộ sát giờ cần demo/chat-test.

**Chưa làm rõ:** UI ghi lịch đồng bộ "Vào 02:00" nhưng lần chạy quan sát được lại ở ~00:00 — chưa biết vì sao lệch, chưa cần điều tra trừ khi ảnh hưởng việc đang làm.

==================================================
4. KIẾN TRÚC NỘI DUNG — HIỂU SAI CHỖ NÀY LÀ LÀM HỎNG VIỆC
==================================================

Nội dung đi theo BA TẦNG, tách theo ĐỐI TƯỢNG ĐỌC (DEC-053):

```
docs KB/Dev/      cơ chế, kết quả kiểm chứng, cấu hình
                  → cho Dev và Agent config. KHÔNG lên Web.

docs KB/Human/    hướng dẫn thao tác
                  → NGUỒN BUILD. Sửa nội dung ở đây.

knowledge/<KB>/   bản sinh bởi scripts/build_handbook.py
                  → lên Web. KHÔNG sửa tay, sẽ bị ghi đè.
```

| Tiền tố nguồn | Dải số | Đổ về KB |
|---|---|---|
| `KB-NN-*` | 00–20 (00–12 cũ + 20 mới) | `GS9 Knowledge VNG AI` |
| `Agent-NN-*` | 13–19 | `GS9 Knowledge VNG AI` |
| `AgentCFL-NN-*` | 00–05 | `GS9 CFL Knowledge Agent` |
| `KBCFL-NN-*` | 10–12 | `GS9 CFL Knowledge Agent` |

Thêm tính năng mới thì **đánh số tiếp từ 20 trở lên** (KB-20 đã dùng, tiếp theo là KB-21). `HUMAN_SOURCE_PREFIXES` trong `scripts/build_handbook.py` chỉ liệt kê tiền tố (`KB`, `Agent`), KHÔNG khoá dải số — đừng phí công sửa hằng đó. Nhưng nhớ sửa `EXPECTED_MODULE_COUNT` trong builder và các chỗ khoá số trong `tests/test_build_handbook.py` mỗi lần thêm module (xem DEC-065 để biết đúng các chỗ phải sửa).

**Quy tắc phân loại một câu:** câu hỏi người dùng cuối đặt ra khi đang chat → Human. Câu hỏi chỉ người sửa hệ thống mới cần → Dev. Mã `DEC-xxx`, link `audit/`, cụm "đã/chưa kiểm chứng", `Mức bằng chứng` KHÔNG được xuất hiện trong `docs KB/Human` và `knowledge/`.

**Hai artifact ở root đã dọn (DEC-066):** `so-tay-tao-knowledge-base-v3.md` (master cũ, đã chết, dời vào `audit/archive/`) và `so-tay-tao-knowledge-base.html` (31MB, gỡ khỏi git, vẫn còn trên đĩa, `.gitignore` che). Đừng khôi phục hai file này về root.

==================================================
5. FILE THUYẾT TRÌNH — ĐỌC KỸ TRƯỚC KHI SỬA
==================================================

`gioi-thieu-knowledge-base-va-agent.html`, 12 mục gộp thành **5 phần** theo mục đích (DEC-067): I Vì sao cần · II KB và Agent là gì · III Có lợi thế nào · IV Đang có gì · V Xây tiếp thế nào. Mục lục dạng **cột trái cố định**, có nhãn phần và link từng mục.

**MỤC ĐÍCH (người dùng nhắc nhiều lần):** đây là bản **GIỚI THIỆU tính năng KB và Agent** — cho người ta thấy **nó hữu dụng**, làm nền để **team bàn cách xây cấu trúc**.

→ **CHỈ đưa vào những gì đã chốt và cho thấy giá trị.**
→ **TUYỆT ĐỐI KHÔNG đưa lỗi, nghi vấn, điều tra nội bộ vào file này.** Chỗ đó thuộc `STATUS.md` và `audit/`.
→ Ảnh nào chứa thông tin sai thì **cắt bỏ phần đó** trước khi nhúng.

**Cạm bẫy kỹ thuật khi sửa file này:**
- File KHÔNG có script build hay manifest nối ảnh nhúng với nguồn trong `knowledge/` — ảnh được ghép tay, alt text paraphrase khác chữ trong `docs KB/Human`. Muốn thay ảnh phải **trích ảnh đang nhúng ra, đọc, so khớp bằng mắt** với ảnh nguồn trước khi thay — không suy đoán theo tên biến số.
- Mốc `<!-- N -->` giữa các section từng **không đồng nhất** trong bản gốc (thiếu ở vài mục, sai số ở mục khác) — tách section phải quét theo thẻ `<section id=>`, đừng dựa vào mốc comment.
- Ảnh nhúng base64 quá dài để dùng Edit tool trực tiếp (một số vượt 40.000 ký tự) — phải viết script Python đọc/ghi qua tệp tạm + `os.replace`.
- Luôn sao lưu trước khi sửa (`Copy-Item` sang scratchpad), rồi kiểm lại sau: số section, số link mục lục không gãy, `<div>` cân, số ảnh, không tham chiếu ngoài, không còn `loading="lazy"`.

==================================================
6. TRẠNG THÁI 16 AGENT — CHƯA CÓ GÌ ĐỔI SO VỚI PHIÊN TRƯỚC
==================================================

**6 Agent đã có kho đúng chuyên môn:** Knowledge Curator (2 kho), KPI Experiment Analyst, Incident Triage (PUM), Player Voice Analyst (Sentiment), LiveOps Planner, Release Reviewer.

**4 Agent dùng KHO TẠM (DEC-060), chưa đóng được gap thật:**

| Agent | Kho tạm | Kho đúng còn thiếu |
|---|---|---|
| `Player Communications` | `GS9 CFL Plan Version` | `GS9 CFL Event Calendar & Brief` |
| `Economy Offer Analyst` | `GS9 CFL Data Daily` | `GS9 CFL Item Catalog` (tách khỏi Item Profile, rà P0 trước) |
| `CS Copilot` | `GS9 Knowledge VNG AI` | `GS9 CFL CS FAQ & Policy` (mới có file định dạng) |
| `GM Policy Advisor` | `GS9 Knowledge VNG AI` | `GS9 CFL GM Policy & Sanction` (chưa tồn tại) |

`CS Copilot` và `GM Policy Advisor` đang trỏ kho hướng dẫn nền tảng — **không chứa chính sách CS hay điều khoản xử phạt nào**. Lưu ý thêm phiên 6: `GS9 Knowledge VNG AI` hiện tạm thời không có tài liệu chữ nào `completed` (xem mục 2) — hai Agent này đang **không tra được gì cả**, không riêng gì "sai kho".

**Gắn kho xong PHẢI bật công cụ truy hồi (DEC-061).** Gắn KB không tự cho Agent quyền đọc kho. Triệu chứng: `tool not found: search_knowledge_base` rồi Agent quay ra hỏi lại người dùng.

**Gate chất lượng mở một phần (DEC-062):** `Player Communications` **ĐẠT** đầy đủ. `Knowledge Curator` **Có điều kiện**. `CS Copilot` **đạt về guardrail**. **13/16 Agent vẫn Bị chặn–Chưa xác định.** Chưa test 3 Agent gắn KB nhạy cảm (PUM, Sentiment, Kho Tổng Hợp).

==================================================
7. CẠM BẪY ĐÃ GẶP THẬT — ĐỌC KỸ
==================================================

**Google Drive mất kết nối rồi tự "Restore" ra layout cũ — đã gặp 2 lần (DEC-059, DEC-064).** Runbook đã kiểm chứng hoạt động đúng cả 2 lần: (1) KHÔNG sửa gì trước khi Drive sync xong hoàn toàn; (2) nếu thư mục thật bị đổi tên thành `(1)` thì **đổi tên lại**, KHÔNG xoá-tạo-mới (giữ ID, không đứt connector); (3) nếu `.git` hỏng, thay bằng bản clone sạch từ GitHub; (4) xác nhận cuối bằng `git diff --stat origin/main HEAD` rỗng tuyệt đối — **đừng chỉ tin `git status`**, và đừng chạy `git status` khi Drive còn đang đồng bộ dở (từng timeout 2 phút, cho trạng thái giả).

**Google Drive khoá file khi đọc/ghi — có thể cần restart Drive for Desktop, không chỉ chờ.** Dấu hiệu: `Invalid request code` (Bash) / `OSError: Errno 22` (Python) / `Incorrect function` (PowerShell), lặp lại cả với `Read` tool và `cat`/`type`. Phiên 6 (18/08) gặp việc này ngay đầu phiên — mount G: còn sống (`ls` thấy file, đúng dung lượng) nhưng lớp đọc nội dung chết hẳn, PID `GoogleDriveFS.exe` đứng yên. Cách xử: người dùng Quit hẳn Google Drive for Desktop từ tray (không chỉ đóng cửa sổ) rồi mở lại — sau đó PID đổi và đọc lại được ngay. Khi ghi file: luôn qua file tạm rồi `os.replace`.

**Line ending.** Toàn bộ file trong repo dùng **CRLF**. Sau mỗi lần ghi bằng script, kiểm và ép lại CRLF (`grep -c $'\r$' file | so với wc -l file`).

**Đồng bộ Drive không mặc định làm chết URI** — xem mục 3. Chỉ rà lại URI cho đúng tập file vừa đổi trạng thái.

**Hàng đợi xử lý của nền tảng có thể tắc hoàn toàn (DEC-071, phiên 6).** Không phải mọi lần tài liệu đứng `pending` lâu là do đợi lượt — kiểm bằng panel "Xem tiến trình" (0/5 giai đoạn, đếm số lần thử) để phân biệt "đang xử lý chậm" với "worker không nhận job". "Phân tích lại" không gỡ được tắc thật, chỉ thêm job vào hàng đợi đang đứng yên.

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. `list_documents` trả kết quả rất dài (>100K ký tự) — luôn bị chặn in thẳng ra, phải ghi ra file rồi lọc bằng Python/jq.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun — `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. Dialog cấu hình Agent render ở document chính. Menu ngữ cảnh (⋯) của từng dòng tài liệu (Xem chi tiết/Xem tiến trình/Phân tích lại/...) render ra **document chính**, không phải trong shadow root — cần dò cả hai khi tìm phần tử qua JS.

**Toạ độ click trên trình duyệt dao động giữa các phiên.** Luôn `find` lấy `ref` thay vì toạ độ tuyệt đối khi có thể; nếu phải dùng toạ độ, test bằng một click vô hại rồi chụp lại kiểm chứng trước.

**Claude in Chrome hay rớt kết nối giữa phiên.** Gặp lỗi "not connected", thử lại 1-2 lần trước khi kết luận cần cài lại extension — nhiều lần chỉ là tạm thời.

**Không lưu được ảnh chụp trình duyệt xuống đĩa qua tool.** Cần ảnh chat thật thì nhờ người dùng chụp và thả vào `docs KB/Asset/chat/`.

**JavaScript exec trong trang bị chặn bởi classifier an toàn** khi dùng để gọi API xác thực (`fetch('/api/auth/token...')`). Dùng MCP tool chuyên dụng (`list_documents` v.v.) thay vì tự gọi API qua JS injection.

==================================================
8. LỆNH CHUẨN VÀ GATE
==================================================

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

Gate mục tiêu: 21 module + 8 doc KB Agent, HTML offline tự chứa, `Ran 30 tests`/`OK` — **hiện đang có 1 FAIL đã biết chờ ảnh xử lý xong, xem mục 2**. Không dùng `--allow-missing-minio` cho bản bàn giao.

Console Windows là cp1252 nên script in tiếng Việt sẽ crash ở dòng `print` cuối — chạy với `$env:PYTHONIOENCODING='utf-8'`.

==================================================
9. AN TOÀN
==================================================

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che.
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. KHÔNG mở, KHÔNG đọc nội dung.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` **người dùng xác nhận giữ nguyên** (DEC-058). Đừng cảnh báo lại.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại từ Web trước khi kết luận.
- Tính năng "Thêm vào tri thức" (mục 2) không có bước duyệt bắt buộc giữa `Lưu nháp`/`Xuất bản` — nếu ai dùng nó để thêm nội dung vào kho sự thật đã chốt, nhắc họ tự đọc lại trước khi Xuất bản.
- Không tự mutation live nếu nhiệm vụ hiện tại chưa cho phép rõ.

==================================================
10. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- **Trả lời ngắn gọn, đi thẳng vào việc.** Người dùng làm nhanh và không thích vòng vo.
- **Hỏi gộp một lượt** rồi làm, đừng hỏi lắt nhắt.
- **Phân biệt rõ mức bằng chứng.** Tách bạch "đã kiểm chứng" / "chưa chứng minh" / "còn biến số".
- **Kiểm chứng thật bằng nhiều lớp**, đừng báo cáo suông. Người dùng đã nhắc: *"tôi sợ nhiều khi bạn nhầm file cũ thành file mới rồi giữ lại file cũ xóa file mới"*.
- Lấy trạng thái thật từ hệ thống (API/UI/MCP), đừng tin tài liệu cũ — kể cả DECISIONS.md, như đã thấy ở DEC-052 phải tự đính chính hai lần (mục 3).
- Khi phát hiện điều mới: ghi vào `DECISIONS.md` (+ `audit/` hoặc `docs KB/Dev` nếu cần chi tiết), rồi chắt phần "người dùng cần làm gì" sang `docs KB/Human`.
- **Nhớ mục đích của từng artifact.** File HTML giới thiệu là để present — không phải chỗ đổ lỗi kỹ thuật vào. `STATUS.md`/`HANDOFF.md`/`DECISIONS.md` mới là chỗ ghi thật, ghi cả lỗi.
- Khi chờ việc mất thời gian (KB xử lý ảnh, Drive sync), giãn chu kỳ tự kiểm lại thay vì hỏi dồn dập; nếu qua nhiều lượt vẫn 0 tiến triển, báo người dùng thay vì tiếp tục tự chờ.
