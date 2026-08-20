Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root project là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), team GS9 dùng.

Hiện có **10 kho tri thức** và **16 trợ lý** (6 mặc định của nền tảng + 10 custom cho LiveOps). `GS9 Knowledge VNG AI` local có **21 tài liệu Markdown** (`doc-00`→`doc-20`) + **52 ảnh PNG** (`image-01`→`image-52`) — **cả 73 tài liệu đều `Hoàn tất` trên Web** (xác nhận 20/08/2026, DEC-073/074), không còn tài liệu nào treo.

File thuyết trình: `gioi-thieu-knowledge-base-va-agent.html` — **12 mục gộp thành 5 phần**, tự chứa, in PDF được, mục lục dạng cột trái.

==================================================
1. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -3 --oneline`. Commit mới nhất phải là `32b3e69` ("docs: ghi nhận hàng đợi nền tảng đã thông, gate sạch hoàn toàn (DEC-073)") — đã push GitHub cuối phiên 7 (20/08, máy nhà).

**Luôn xác nhận local khớp remote trước khi tin `git status`:**
```powershell
git fetch origin
git diff --stat origin/main HEAD
```
Phải rỗng tuyệt đối. Nếu KHÔNG rỗng — có thể Drive lại gây sự cố như đã gặp nhiều lần (xem mục 7).

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` (đặc biệt mục 4.5 — Case 2, việc ưu tiên số 1 giờ đã đủ điều kiện chạy; và mục 4.9 — đã ĐÓNG) → `STATUS.md` (mục mới nhất trên cùng, mục 20/08 phiên 7). `DECISIONS.md` (74 quyết định) tra khi cần hiểu vì sao.

==================================================
2. VIỆC ƯU TIÊN SỐ 1 KHI VÀO PHIÊN — CHẠY LẠI CASE 2, ĐIỀU KIỆN ĐÃ ĐẠT (mục 4.5)
==================================================

**Bối cảnh (phiên 4, 17/08):** chat-test `Knowledge Curator` khẳng định sai ba thứ — "chỉ có 6 trợ lý mặc định", tồn tại kho `Knowledge VNG - Image Assets` (đã gỡ từ lâu), có nguồn `Drive CFL Viax` sync mỗi 15 phút. Cả ba khớp gần như từng ký tự với nội dung nhìn thấy trong 3 ảnh (`image-26`, `image-41`, `image-25`) chứ không phải tài liệu chữ. Nghi vấn: Agent có đang **ưu tiên ảnh hơn chữ làm nguồn dữ kiện** không, hay lúc đó **chữ chưa vào chỉ mục** nên ảnh là thứ duy nhất truy hồi được (giả thuyết cạnh tranh, khớp với chi tiết vòng tìm ngữ nghĩa đầu tiên trả "Không có kết quả")? Chi tiết đầy đủ: `audit/agent-chat-test-2026-08-17.md` mục 6, 7, 8.

**Điều kiện để chạy lại từng ghi "đủ 70 tài liệu Hoàn tất" — con số đó LỖI THỜI** (70 = 49 ảnh cũ + 21 md, tính trước khi thêm `image-50/51/52`). Con số đúng là **73** (52 ảnh + 21 md). **Đã đạt 20/08/2026** — xác nhận 73/73 `completed`/`enabled` qua MCP, cộng hash `doc-11` trên Web khớp tuyệt đối bản local (DEC-074).

**Việc làm theo thứ tự:**
1. Xác nhận lại nhanh qua MCP (`list_documents`, lọc `parse_status`/`enable_status`) rằng vẫn còn 73/73 `completed`/`enabled` — đừng giả định trạng thái cũ còn đúng, có thể có thay đổi từ khi dừng phiên 7.
2. Chạy lại đúng câu hỏi Case 2 cũ với `Knowledge Curator` (nội dung câu hỏi trong `audit/agent-chat-test-2026-08-17.md` mục 6), ghi rõ model đang dùng.
3. Nếu vẫn trả lời sai giống cũ (dẫn nội dung từ ảnh thay vì chữ) → nghi vấn "Agent ưu tiên ảnh hơn chữ" được củng cố, không phải do thiếu chỉ mục nữa (loại được giả thuyết cạnh tranh).
4. Nếu sai → thử tắt cấu hình đọc ảnh (VLM/multimodal) ở 2 KB thuần hướng dẫn (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`), **giữ nguyên VLM** ở KB nghiệp vụ (`GS9 CFL Plan Version` — Case 1 đã chứng minh chạy tốt với VLM bật). So sánh 3 kết quả (VLM bật cả 2, tắt cả 2, và bản cũ) để kết luận.
5. Ghi kết luận vào `DECISIONS.md` + cập nhật `HANDOFF.md` mục 4.5 dù kết quả là gì (đóng nghi vấn hoặc xác nhận cần sửa cấu hình).

**Nếu MCP cho thấy có tài liệu rơi lại `pending`/`disabled`** (từng xảy ra sau một lần đồng bộ Toàn bộ định kỳ, xem DEC-072) — hỏi người dùng trước, đừng chạy Case 2 khi chưa đủ 73/73 (sẽ tái hiện lỗi vì lý do tầm thường, không phân biệt được hai giả thuyết).

==================================================
3. LỊCH SỬ HÀNG ĐỢI TẮC 17–20/08 — ĐÃ ĐÓNG, THAM KHẢO KHI CẦN
==================================================

**Đã đóng (DEC-071/072/073/074).** Từ 17/08 tới 19/08, 26 ảnh (23 crop lại + 3 mới `image-50/51/52`) và 21 file `doc-*.md` treo ở `pending`/`processing`/`finalizing` do hàng đợi xử lý của nền tảng tắc thật (kiểm bằng panel "Xem tiến trình": job xếp hàng nhiều lần thử nhưng không worker nào chạy — không phải lỗi file hay cấu hình KB). Ngày 19/08 hàng đợi tự thông (chưa xác nhận do team xử lý hay tự phục hồi). Đã viết lại `image-map.json` đủ 52 URI, build lại 20 module, sửa test, gate sạch, và đồng bộ 19 file `.md` lên Web — kiểm bằng hash `doc-11` khớp tuyệt đối.

**Đính chính quan trọng vẫn còn giá trị (DEC-069, xác nhận lại DEC-072):** đồng bộ Google Drive KHÔNG mặc định làm chết mọi URI ảnh. Dù chế độ đồng bộ là Tăng dần hay Toàn bộ, chỉ file **thật sự đổi nội dung** (hash khác) hoặc file mới mới bị tạo lại document/URI mới; **không cần rà lại toàn bộ `image-map.json` sau mỗi lần sync** — chỉ cần xác định đúng tập file vừa chuyển trạng thái khỏi `completed` rồi lấy URI cho đúng tập đó. (Vụ chết URI 49/49 ngày 11/08 là do di trú giữa hai KB khác nhau — DEC-043 — không phải bản chất đồng bộ thường.)

**Chưa làm rõ:** UI ghi lịch đồng bộ "Vào 02:00" nhưng lần chạy quan sát được lại ở ~00:00; và chưa xác nhận nguyên nhân hàng đợi tự thông ngày 19/08. Không cần điều tra trừ khi tái diễn.

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

Thêm tính năng mới thì **đánh số tiếp từ 20 trở lên** (KB-20 đã dùng, tiếp theo là KB-21). `HUMAN_SOURCE_PREFIXES` trong `scripts/build_handbook.py` chỉ liệt kê tiền tố (`KB`, `Agent`), KHÔNG khoá dải số — đừng phí công sửa hằng đó. Nhưng nhớ sửa `EXPECTED_MODULE_COUNT` trong builder và các chỗ khoá số trong `tests/test_build_handbook.py` mỗi lần thêm module (xem DEC-065 để biết đúng các chỗ phải sửa — và nhớ khoá số lượt tham chiếu ảnh cũng phải cập nhật nếu module mới có ảnh, xem bài học `61→64` ở DEC-073).

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

`CS Copilot` và `GM Policy Advisor` đang trỏ kho hướng dẫn nền tảng — **không chứa chính sách CS hay điều khoản xử phạt nào**. Kể từ 20/08, `GS9 Knowledge VNG AI` đã có đủ 73/73 tài liệu chữ + ảnh `Hoàn tất` trở lại — hai Agent này tra được nội dung hướng dẫn nền tảng bình thường, chỉ vẫn sai kho về mặt nghiệp vụ (không phải "không tra được gì" như hồi 18–19/08).

**Gắn kho xong PHẢI bật công cụ truy hồi (DEC-061).** Gắn KB không tự cho Agent quyền đọc kho. Triệu chứng: `tool not found: search_knowledge_base` rồi Agent quay ra hỏi lại người dùng.

**Gate chất lượng mở một phần (DEC-062):** `Player Communications` **ĐẠT** đầy đủ. `Knowledge Curator` **Có điều kiện** (đang chờ chạy lại Case 2, xem mục 2). `CS Copilot` **đạt về guardrail**. **13/16 Agent vẫn Bị chặn–Chưa xác định.** Chưa test 3 Agent gắn KB nhạy cảm (PUM, Sentiment, Kho Tổng Hợp).

==================================================
7. CẠM BẪY ĐÃ GẶP THẬT — ĐỌC KỸ
==================================================

**Google Drive mất kết nối rồi tự "Restore" ra layout cũ — đã gặp 2 lần (DEC-059, DEC-064).** Runbook đã kiểm chứng hoạt động đúng cả 2 lần: (1) KHÔNG sửa gì trước khi Drive sync xong hoàn toàn; (2) nếu thư mục thật bị đổi tên thành `(1)` thì **đổi tên lại**, KHÔNG xoá-tạo-mới (giữ ID, không đứt connector); (3) nếu `.git` hỏng, thay bằng bản clone sạch từ GitHub; (4) xác nhận cuối bằng `git diff --stat origin/main HEAD` rỗng tuyệt đối — **đừng chỉ tin `git status`**, và đừng chạy `git status` khi Drive còn đang đồng bộ dở (từng timeout 2 phút, cho trạng thái giả).

**Google Drive khoá file khi đọc/ghi — có thể cần restart Drive for Desktop, không chỉ chờ.** Dấu hiệu: `Invalid request code` (Bash) / `OSError: Errno 22` (Python) / `Incorrect function` (PowerShell), lặp lại cả với `Read` tool và `cat`/`type`. Cách xử: người dùng Quit hẳn Google Drive for Desktop từ tray (không chỉ đóng cửa sổ) rồi mở lại. Khi ghi file: luôn qua file tạm rồi `os.replace`.

**`git commit` nhiều file lớn qua Google Drive có thể vượt timeout công cụ (DEC-073, phiên 7).** Ghi/commit 20 file cùng lúc từng bị Bash tool cắt ngang ở mốc 2 phút trong khi tiến trình `git` con vẫn chạy ngầm thật (đang tính hash/ghi object qua lớp Drive), để lại file khoá rác (`HEAD.lock`, `refs/heads/main.lock`, đôi khi `objects/maintenance.lock`). **Đừng vội xoá lock hay kết luận thất bại** — trước tiên xác nhận không còn tiến trình `git` nào chạm tới đúng đường dẫn repo (`Get-CimInstance Win32_Process -Filter "Name='git.exe'"` lọc theo `CommandLine`), có thể cần đợi thêm vì tiến trình đang thật sự làm việc. Chỉ xoá lock khi chắc chắn không còn tiến trình sống — đúng cách git tự khuyến nghị trong thông báo lỗi.

**Line ending.** Toàn bộ file trong repo dùng **CRLF**. Sau mỗi lần ghi bằng script, kiểm và ép lại CRLF (`grep -c $'\r$' file | so với wc -l file`).

**Đồng bộ Drive không mặc định làm chết URI** — xem mục 3. Chỉ rà lại URI cho đúng tập file vừa đổi trạng thái.

**Hàng đợi xử lý của nền tảng có thể tắc hoàn toàn (DEC-071).** Không phải mọi lần tài liệu đứng `pending` lâu là do đợi lượt — kiểm bằng panel "Xem tiến trình" (0/5 giai đoạn, đếm số lần thử) để phân biệt "đang xử lý chậm" với "worker không nhận job". "Phân tích lại" không gỡ được tắc thật, chỉ thêm job vào hàng đợi đang đứng yên. Đã từng tự thông sau ~2 ngày không rõ lý do (DEC-073) — không có cách chủ động gỡ tắc ngoài chờ hoặc báo team vận hành.

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

Gate mục tiêu: 21 module + 8 doc KB Agent, HTML offline tự chứa, `Ran 30 tests`/`OK`, 0 FAIL — **đã đạt từ 19/08 (DEC-073), giữ nguyên đến giờ**. Không dùng `--allow-missing-minio` cho bản bàn giao.

Console Windows là cp1252 nên script in tiếng Việt sẽ crash ở dòng `print` cuối — chạy với `$env:PYTHONIOENCODING='utf-8'`.

==================================================
9. AN TOÀN
==================================================

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che.
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. KHÔNG mở, KHÔNG đọc nội dung.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` **người dùng xác nhận giữ nguyên** (DEC-058). Đừng cảnh báo lại.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại từ Web trước khi kết luận.
- Tính năng "Thêm vào tri thức" (`KB-11-chat-kiem-thu-va-bao-tri.md`) không có bước duyệt bắt buộc giữa `Lưu nháp`/`Xuất bản` — nếu ai dùng nó để thêm nội dung vào kho sự thật đã chốt, nhắc họ tự đọc lại trước khi Xuất bản.
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
