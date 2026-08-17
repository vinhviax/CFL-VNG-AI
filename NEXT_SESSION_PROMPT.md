Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root project là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), team GS9 dùng.

Hiện có **10 kho tri thức** và **16 trợ lý** (6 mặc định của nền tảng + 10 custom cho LiveOps). **10/10 kho đã đồng bộ Web khớp local** (kiểm 17/08/2026).

File thuyết trình: `gioi-thieu-knowledge-base-va-agent.html` — **12 mục**, tự chứa, in PDF được, 15 ảnh nhúng base64.

==================================================
1. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`.

HEAD phải là `46c9cde docs: bằng chứng mới — Agent truy hồi thẳng tài liệu ảnh làm nguồn` (đã push GitHub).

**Luôn xác nhận local khớp remote trước khi tin `git status`:**
```powershell
git fetch origin
git diff --stat origin/main HEAD
```
Phải rỗng tuyệt đối. Nếu KHÔNG rỗng — có thể Drive lại gây sự cố như 17/08 (xem mục 6).

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` → `STATUS.md`. `DECISIONS.md` (62 quyết định) tra khi cần hiểu vì sao.

==================================================
2. VIỆC ƯU TIÊN SỐ 1 — NGHI VẤN ẢNH THÀNH NGUỒN DỮ KIỆN SAI
==================================================

Đây là việc quan trọng nhất đang treo. Chi tiết đầy đủ: `audit/agent-chat-test-2026-08-17.md` mục 6 và 7.

**Hiện tượng.** `GS9 CFL Knowledge Curator` trả lời sai 3 thứ về chính hệ thống: "chỉ có 6 trợ lý mặc định, không có agent nào tên CFL"; tồn tại kho `Knowledge VNG - Image Assets` (đã bị gỡ); có nguồn `Drive CFL Viax` sync mỗi 15 phút (là cấu hình thử cũ).

**ĐÃ KIỂM CHỨNG — hai lớp bằng chứng:**

1. Truy vấn `keyword_search` vào chỉ mục cho thấy nền tảng **OCR ảnh và sinh mô tả ảnh ngay lúc nạp**, lưu thành chunk chữ tra cứu được (`chunk_type: "image_caption"` và `"text"`). Ảnh `image-25-google-drive-dong-bo-thanh-cong.png` sinh ra chunk ghi nguyên: *"a connected data source: 'Drive CFL Viax' (Google Drive)… every 15 minutes… status 'Thành công'"*.
2. Trace lượt chạy lại ghi thẳng bước **`Lấy tài liệu: image-01-tong-quan-danh-sach-knowledge.png`** — Agent chủ động truy hồi **một tài liệu ảnh** làm nguồn, gọi đích danh tên tệp. Ảnh chụp: `docs KB/Asset/chat/case2-trace-lay-tai-lieu-anh.png`.

Ba ảnh gây lỗi thời, đều nằm trong `GS9 Knowledge VNG AI`: `image-26-agent-tong-quan-danh-sach.png` (hiện `Tất cả agent 6 · Của tôi 0`), `image-41-agent-test-kb-da-nguon.png` (dropdown chọn KB ngày 11/08 có `Knowledge VNG - Image Assets`), `image-25-google-drive-dong-bo-thanh-cong.png`.

**CÒN BIẾN SỐ:** hai lượt chạy dùng model khác nhau (`hosted_vllm/qwen3.6-...` rồi `deepseek-v4-flash`), và KB có thể chưa phân tích xong tệp mới sync. **Khi test lại phải ghi rõ model đang dùng.**

**ĐÃ VÁ TẠM:** gắn dòng cảnh báo *"Ảnh chụp một thời điểm, không phải danh mục hiện hành"* cạnh 7 ảnh mang danh sách trong `docs KB/Human` (`Agent-13` ×1, `Agent-16` ×3, `KB-08` ×2, `KB-12` ×1). **Không giải quyết gốc** — không thể chụp lại ảnh mỗi lần hệ thống đổi.

**HƯỚNG GỐC NGƯỜI DÙNG ĐỀ XUẤT, CẦN THỬ:**
1. **Tắt VLM / đọc ảnh ở KB thuần hướng dẫn** (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`). Chưa biết nền tảng có cho tắt riêng từng KB không, và tắt rồi ảnh có còn hiện trong câu trả lời không.
2. **Giữ VLM ở KB nghiệp vụ** như `GS9 CFL Plan Version` — ở đó nội dung trong ảnh chính là thứ cần tra, Case 1 chứng minh chạy rất tốt.
3. Che phần danh sách khi chụp ảnh minh hoạ.

**Cách test:** đợi KB xử lý xong toàn bộ tệp → chạy lại đúng câu hỏi Case 2 → nếu vẫn sai thì tắt VLM một KB hướng dẫn → chạy lại → so ba kết quả, ghi rõ model từng lượt.

**QUY TẮC RÚT RA, ÁP DỤNG LUÔN:** không dùng lời Agent tự mô tả về chính nó làm bằng chứng, **theo cả hai chiều**. Khi bị hỏi vặn "có phải bạn bịa không", Agent quay ra nhận đã bịa toàn bộ và nói 4 KB "không tồn tại / rỗng" — **cả 4 đều sai** (thực tế 7, 8, 8, 8 tài liệu). Kiểm bằng API/UI.

==================================================
3. KIẾN TRÚC NỘI DUNG — HIỂU SAI CHỖ NÀY LÀ LÀM HỎNG VIỆC
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
| `KB-NN-*` | 00–12 | `GS9 Knowledge VNG AI` |
| `Agent-NN-*` | 13–19 | `GS9 Knowledge VNG AI` |
| `AgentCFL-NN-*` | 00–05 | `GS9 CFL Knowledge Agent` |
| `KBCFL-NN-*` | 10–12 | `GS9 CFL Knowledge Agent` |

Thêm tính năng mới thì thêm tiền tố vào `HUMAN_SOURCE_PREFIXES` hoặc `SIMPLE_KB_TARGETS` trong `scripts/build_handbook.py` — KHÔNG tạo thư mục con.

**Quy tắc phân loại một câu:** câu hỏi người dùng cuối đặt ra khi đang chat → Human. Câu hỏi chỉ người sửa hệ thống mới cần → Dev. Mã `DEC-xxx`, link `audit/`, cụm "đã/chưa kiểm chứng", `Mức bằng chứng` KHÔNG được xuất hiện trong `docs KB/Human` và `knowledge/`.

==================================================
4. FILE THUYẾT TRÌNH — ĐỌC KỸ TRƯỚC KHI SỬA
==================================================

`gioi-thieu-knowledge-base-va-agent.html`, 12 mục, 1,19 MB.

**MỤC ĐÍCH (người dùng nói rõ, đã bị nhắc 2 lần vì làm sai):** đây là bản **GIỚI THIỆU tính năng KB và Agent** — cho người ta thấy **nó hữu dụng**, và làm nền để **team bàn cách xây cấu trúc**.

→ **CHỈ đưa vào những gì đã chốt và cho thấy giá trị.**
→ **TUYỆT ĐỐI KHÔNG đưa lỗi, nghi vấn, điều tra nội bộ vào file này.** Chỗ đó thuộc `STATUS.md` và `audit/`.
→ Ảnh nào chứa thông tin sai thì **cắt bỏ phần đó** trước khi nhúng (ảnh case 2 đã xử lý như vậy).

Hai mục mới thêm 17/08/2026:
- **Mục 09 Thử thật trên dữ liệu CFL** — 3 case kèm 5 ảnh chụp hội thoại thật (nguồn ở `docs KB/Asset/chat/`). Chỉ trình bày phần năng lực: case 1 làm được việc thật; case 2 biết nói "không tìm thấy" thay vì bịa; case 3 CS Copilot ra bản DRAFT trả lời khách + đề xuất chuyển tiếp.
- **Mục 10 Đề xuất cấu trúc** — hai phương án kèm đánh đổi (A chia theo mức nhạy cảm × đối tượng đọc × nhịp cập nhật; B chia theo 4 nhóm công việc), bảng 4 kho cần dựng và ai cung cấp gì, gợi ý thứ tự làm, 4 câu hỏi để team chốt. **Chưa chốt, đưa ra để bàn.**

Mục 10 mở đầu bằng **"Bắt đầu từ đâu — bốn loại kho hầu như nhóm nào cũng cần"** (kho sự thật đã chốt · quy trình và chính sách · kế hoạch và lịch · kết quả) + 3 câu hỏi quyết định tách/gộp + cảnh báo lỗi chia kho theo *nguồn dữ liệu*.

**Đã sửa lỗi cũ:** 10 ảnh có `loading="lazy"` nên **không render khi in PDF**. Đã bỏ lazy toàn bộ, kiểm chứng 16/16 ảnh tải được.

==================================================
5. TRẠNG THÁI 16 AGENT
==================================================

**6 Agent đã có kho đúng chuyên môn:** Knowledge Curator (2 kho), KPI Experiment Analyst, Incident Triage (PUM), Player Voice Analyst (Sentiment), LiveOps Planner, Release Reviewer.

**4 Agent dùng KHO TẠM (DEC-060), chưa đóng được gap thật:**

| Agent | Kho tạm | Kho đúng còn thiếu |
|---|---|---|
| `Player Communications` | `GS9 CFL Plan Version` | `GS9 CFL Event Calendar & Brief` |
| `Economy Offer Analyst` | `GS9 CFL Data Daily` | `GS9 CFL Item Catalog` (tách khỏi Item Profile, rà P0 trước) |
| `CS Copilot` | `GS9 Knowledge VNG AI` | `GS9 CFL CS FAQ & Policy` (mới có file định dạng) |
| `GM Policy Advisor` | `GS9 Knowledge VNG AI` | `GS9 CFL GM Policy & Sanction` (chưa tồn tại) |

`CS Copilot` và `GM Policy Advisor` đang trỏ kho hướng dẫn nền tảng — **không chứa chính sách CS hay điều khoản xử phạt nào**.

**CẠM BẪY MỚI (DEC-061) — gắn kho xong PHẢI bật công cụ truy hồi.** Gắn KB không tự cho Agent quyền đọc kho. Triệu chứng: `tool not found: search_knowledge_base (available: ask_user, thinking, todo_write)` rồi Agent quay ra hỏi lại người dùng. Đã bật `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` cho 3 Agent (3→5, 3→5, 2→4 tool). `CS Copilot` chế độ Trả lời nhanh không có tab Công cụ.

**Gate chất lượng mở một phần (DEC-062):** `Player Communications` **ĐẠT** đầy đủ. `Knowledge Curator` **Có điều kiện**. `CS Copilot` **đạt về guardrail**. **13/16 Agent vẫn Bị chặn–Chưa xác định.** Chưa test 3 Agent gắn KB nhạy cảm (PUM, Sentiment, Kho Tổng Hợp).

**Việc khác còn mở:** lỗi truy hồi `Knowledge Curator` (kho có nội dung nhưng lấy nhầm đoạn) — thử tăng Top K hoặc bật `Thông tin tài liệu`; case 1 bỏ sót 2 ảnh **có thật** trong kho (`image-v5-06`, `image-v5-07`).

==================================================
6. CẠM BẪY ĐÃ GẶP THẬT — ĐỌC KỸ
==================================================

**Google Drive mất kết nối rồi tự "Restore" ra layout cũ (DEC-059, 17/08/2026).** Drive rớt mount rồi tự phục hồi nhưng trộn cấu trúc cũ chồng lên mới: `knowledge` thật bị đẩy thành `knowledge (1)`, `.git` mất lịch sử.
Nếu tái diễn: (1) clone bản sạch từ GitHub ra NGOÀI Drive để đối chiếu, không sửa gì trước; (2) thư mục bị đổi thành `(1)` thì **đổi tên lại**, KHÔNG xoá-tạo-mới (xoá-tạo-mới đổi ID làm đứt connector); (3) thay `.git` hỏng bằng bản clone; (4) `git restore .` rồi `git clean -f` từng thư mục; **để ý `desktop.ini` nằm trong `.gitignore` nên `git clean -f` bỏ qua**, dùng `git clean -fx` hoặc rà tay; (5) rà toàn cây tìm `(1)`, `(2)`, `Copy of`, thư mục chỉ có `desktop.ini`; (6) xác nhận cuối bằng `git diff --stat origin/main HEAD` rỗng tuyệt đối.

**Google Drive khoá file khi ghi.** Dấu hiệu: `Invalid request code` (Bash) / `OSError: Errno 22` hoặc `FileExistsError: Errno 17` (Python) / `Incorrect function` (PowerShell).
→ **Ghi file qua file tạm rồi `os.replace`.** Ghi đè trực tiếp đã từng làm MẤT SẠCH nội dung một file nguồn (16/08).
→ **Đọc file ảnh trong Drive cũng bị khoá** — chép ra scratchpad trước rồi mới xử lý.
→ `scripts/build_handbook.py` **ghi trực tiếp**, gặp lúc Drive khoá là fail giữa chừng. Chạy lại sau vài giây là được; đã gặp và xử lý bằng vòng lặp retry.

**Line ending.** Toàn bộ file trong repo dùng **CRLF**. Ghi bằng Python với `newline=''` sẽ ra LF và làm cả file lệch. Sau mỗi lần ghi bằng script, kiểm và ép lại CRLF.

**URI ảnh chết sau khi re-sync.** Lấy lại hàng loạt bằng trường `file_path` của API, ĐỪNG lấy URI trong `description`. Dạng `minio://.../10012/<knowledge_id>/<uuid>.png` đã kiểm chứng render đúng (DEC-052).

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. Với KB chưa share, lấy token qua `/api/auth/token?sub_app=kb` rồi gọi `https://miniapp.vnggames.ai/kb/v1/api/...` kèm header `Authorization: Bearer`. `GET /kb/v1/api/agents` (trường `config.knowledge_bases`) dùng để lấy binding thật.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun. Tool đọc trang thường KHÔNG thấy danh sách; phải qua `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. **Dialog cấu hình Agent lại render ở document chính** nên `find` thấy được — dùng `find` lấy `ref` cho dialog, dùng toạ độ cho danh sách.

**Toạ độ click trên trình duyệt.** Toạ độ truyền vào computer tool là **toạ độ của ảnh chụp**, không phải viewport. Nhưng tỉ lệ **dao động giữa các phiên** — có lúc 1:1, có lúc ảnh bị thu nhỏ. **Luôn test bằng một click vô hại rồi chụp lại kiểm chứng trước khi thao tác thật.** Click sai đã từng mở nhầm dialog Agent khác.

**Phím `Escape` đóng cả dialog và mất thay đổi chưa lưu.** Muốn đóng dropdown chọn KB thì click vùng trống trong dialog.

**Sau khi đóng dialog, thao tác gõ đầu tiên hay bị nuốt.** Tách thành lượt riêng hoặc gõ lại.

**Không lưu được ảnh chụp trình duyệt xuống đĩa.** `save_to_disk: true` không tạo file; trích byte qua canvas `toDataURL` bị chặn. Cần ảnh chụp chat thì **nhờ người dùng chụp và thả vào `docs KB/Asset/chat/`**.

**Ảnh render 2 lần trong chat.** Lỗi nền tảng, KHÔNG phải lỗi tài liệu, đừng sửa nội dung.

**Trình duyệt in-app chưa đăng nhập.** Thao tác trên `vnggames.ai` phải dùng `claude-in-chrome`. Agent không được tự đăng nhập.

==================================================
7. LỆNH CHUẨN VÀ GATE
==================================================

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

Gate: strict build ra 20 module + 8 doc KB Agent, 60 link MinIO, HTML offline tự chứa, `Ran 30 tests`/`OK` (6 skip do thiếu HTML nguồn Plan V5). Không dùng `--allow-missing-minio` cho bản bàn giao.

Console Windows là cp1252 nên script in tiếng Việt sẽ crash ở dòng `print` cuối — chạy với `PYTHONIOENCODING=utf-8`.

==================================================
8. AN TOÀN
==================================================

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che.
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. KHÔNG mở, KHÔNG đọc nội dung.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` **người dùng xác nhận giữ nguyên** (DEC-058). Đừng cảnh báo lại.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại từ Web trước khi kết luận.
- Không tự mutation live nếu nhiệm vụ hiện tại chưa cho phép rõ.

==================================================
9. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- **Trả lời ngắn gọn, đi thẳng vào việc.** Người dùng làm nhanh và không thích vòng vo.
- **Hỏi gộp một lượt** rồi làm, đừng hỏi lắt nhắt.
- **Phân biệt rõ mức bằng chứng.** Người dùng bắt lỗi ngay khi nói quá chắc. Tách bạch "đã kiểm chứng" / "chưa chứng minh" / "còn biến số".
- **Kiểm chứng thật bằng nhiều lớp**, đừng báo cáo suông. Người dùng đã nhắc: *"tôi sợ nhiều khi bạn nhầm file cũ thành file mới rồi giữ lại file cũ xóa file mới"*.
- Lấy trạng thái thật từ hệ thống (API/UI), đừng tin tài liệu cũ.
- Khi phát hiện điều mới: ghi vào `audit/` + `DECISIONS.md` + `docs KB/Dev`, rồi chắt phần "người dùng cần làm gì" sang `docs KB/Human`.
- **Nhớ mục đích của từng artifact.** File HTML là bản giới thiệu để present — không phải chỗ đổ lỗi kỹ thuật vào.
