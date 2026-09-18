Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root repo Git:

```
J:\My Drive\VNGGames AI\Knowledge Base VNG Source
```

Xác nhận bằng `git rev-parse --show-toplevel` (ổ đĩa có thể khác `J:` trên máy khác — nếu vậy, hỏi người dùng đường dẫn thật trên máy này).

**Kiến trúc hiện hành (DEC-082, 18/09/2026):** `knowledge/` nằm **trong** repo tại `<root>\knowledge`. Git chỉ theo dõi phần text/ảnh nhẹ (~30 MB); 4 thư mục binary nặng (`H5 Promotion`, `Kho Tài Liệu Chưa Tích Hợp`, `GS9 CFL PUM`, `GS9 CFL Item Profile`) và `Keys Drive` (credential) bị `.gitignore` loại trừ, chỉ tồn tại trên Drive. Đọc `README.md` mục "Phạm vi git" trước khi `git add`.

Đọc theo thứ tự: `README.md` → `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `DECISIONS.md` (tra từ DEC-088 khi cần — đó là mốc phiên trước bàn giao).

==================================================
0. TRẠNG THÁI KHI BÀN GIAO (kiểm chứng 18/09/2026, cuối phiên 10)
==================================================

- Repo **sạch**, HEAD = `759cf5f`, đã **push lên `origin/main`** — máy khác `git pull --ff-only origin main` sẽ thấy đúng trạng thái này.
- 3 file untracked ở root là cố ý giữ, **đừng xoá**: `knowledge-20260820T085450Z-1-001.zip`, `CFL Thu Thập Dữ Liệu.xlsx`, `VNGGames AI.html`.
- `knowledge/` nay có **14 thư mục con** (không phải 12 như tài liệu cũ ghi) — hai thư mục mới: `GS9 CFL Metric Playbook/` và `GS9 Dokploy VNG AI/` (nay **10 file**, không phải 6). Cả hai đã commit.
- **`GS9 Dokploy VNG AI` đã được người dùng tự trỏ Google Drive connector** cuối phiên 10 — dự kiến tự đồng bộ lên Web sáng hôm sau. **Chưa xác nhận đồng bộ thành công**, kiểm tra đầu tiên ở Việc A bên dưới. `GS9 CFL Metric Playbook` thì **chưa** trỏ connector.
- Nếu git báo `fatal: bad object refs/desktop.ini`: chạy `find .git -type f -name desktop.ini -delete` rồi `git for-each-ref` — đây là rác Google Drive tái sinh liên tục (DEC-083), không phải repo hỏng.

**Phiên trước (phiên 10) đã đóng Việc 1 và Việc 2, soạn xong nội dung Việc 3 (10 file, gồm cả kinh nghiệm thực tế từ một lần migrate dự án thật lên Dokploy), và người dùng đã tự trỏ connector cho KB Dokploy.** Việc còn lại chủ yếu là **xác nhận đồng bộ Web + chat-test cho Việc A**, hoàn tất Việc B (Metric Playbook chưa trỏ connector), Việc C (backup) và Việc D (dùng file xlsx dựng KB còn thiếu) — phần lớn cần **người dùng ra quyết định hoặc tự thao tác trên Web**.

==================================================
VIỆC A — XÁC NHẬN ĐỒNG BỘ + CHAT-TEST KB "GS9 DOKPLOY VNG AI" (ưu tiên cao nhất)
==================================================

Nội dung **đã viết xong, đã commit, connector đã được người dùng tự trỏ** — `knowledge/GS9 Dokploy VNG AI/doc-00` → `doc-09` (10 file): giới thiệu, điều kiện truy cập, quy trình 9 bước, xác thực & bảo mật, FAQ, trang riêng cho dev dùng GigiKit CLI, và 4 file kinh nghiệm thực tế (`doc-06`–`doc-09`: kiến trúc Swarm/Traefik, cấu hình build + 2 bẫy deploy quan trọng nhất, volume/biến môi trường/domain, case thực tế). Biên tập theo DEC-053. Nguồn thô: `scripts/one-off/dokploy-source-a-raw.md`, `dokploy-source-b-raw.md`; nguồn kinh nghiệm thực tế người dùng cung cấp trực tiếp qua chat (không lưu file thô riêng, đã viết thẳng vào 4 doc mới).

**Việc cần làm theo thứ tự:**

1. **Kiểm tra đồng bộ đã chạy chưa và có đủ 10 tài liệu không** — qua Web hoặc MCP `list_documents` (đừng chỉ tin "đã trỏ connector là xong", per thói quen dự án: luôn kiểm bằng chứng, không tin lời báo). Nếu chưa đồng bộ hoặc thiếu tài liệu, hỏi người dùng.
2. **Bật công cụ truy hồi** cho Agent nào sẽ dùng kho này (DEC-061 — gắn KB **không** tự bật `Tìm theo ngữ nghĩa`/`Tìm theo từ khóa`).
3. **Chat-test** theo checklist DEC-062 (không bịa, không lộ PII, truy hồi chạy đúng, trích dẫn đúng nguồn). **Ưu tiên thử câu hỏi về nội dung mới** (`doc-07`/`doc-08`) — ví dụ "deploy xong sao vẫn thấy code cũ?", "container báo lỗi quyền ghi vào volume thì sao?" — để xác nhận agent tra trúng phần kinh nghiệm thực tế vừa thêm, không chỉ phần hướng dẫn cơ bản cũ.
4. Cập nhật `HANDOFF.md` mục 4.13 và `STATUS.md` khi xong từng bước — đừng chờ xong hết mới ghi.

==================================================
VIỆC B — LÊN WEB KB "GS9 CFL METRIC PLAYBOOK"
==================================================

`gs9-metric-playbook.docx` (52 metric, 4 phần) đã được chuyển vào kho riêng `knowledge/GS9 CFL Metric Playbook/doc-00-metric-playbook.docx`, đã commit. **Chưa lên Web.**

Việc cần làm: giống Việc A bước 2–4 — tạo KB `GS9 CFL Metric Playbook` trên `vnggames.ai`, trỏ connector đúng thư mục, bật công cụ truy hồi, chat-test. Xem `HANDOFF.md` mục 4.12.

==================================================
VIỆC D — DÙNG "CFL Thu Thập Dữ Liệu.xlsx" ĐỂ DỰNG CÁC KB NGHIỆP VỤ CÒN THIẾU (DEC-075)
==================================================

File `CFL Thu Thập Dữ Liệu.xlsx` ở root (untracked, cố ý giữ) là sheet người dùng tạo từ 20/08/2026 để team gửi tài liệu nguồn, có 4 sheet: `Huong Dan`, `Loai Doc` (9 loại tài liệu), `Thu Thap Doc` (nơi team điền tài liệu thật — cột J "Kho đích" quyết định tài liệu vào KB nào), `TuDien` (danh sách kho đích để chọn).

**Kiểm tra đầu tiên:** mở sheet `Thu Thap Doc`, xem có dòng nào ngoài **dòng 2 là dòng ví dụ** ("VÍ DỤ — xoá cả dòng này trước khi dùng") không. Lần kiểm gần nhất (18/09/2026) sheet **chưa có dữ liệu thật nào**, chỉ có dòng ví dụ. Nếu vẫn vậy, hỏi người dùng đã có ai gửi tài liệu chưa — đây không phải việc agent tự tạo ra được, phải chờ team gửi.

**Nếu đã có dữ liệu thật:** dùng cột "Kho đích" (đối chiếu `TuDien`) để xếp từng tài liệu vào đúng KB. Danh sách kho đích trong `TuDien` gồm cả các KB **chưa tồn tại**, cần dựng mới:

- `GS9 CFL GM Policy & Sanction` — kho điều khoản xử phạt còn thiếu cho `GM Policy Advisor` (đang dùng kho tạm `GS9 Knowledge VNG AI`).
- `GS9 CFL Event Calendar & Brief` — kho lịch sự kiện/brief đã duyệt còn thiếu cho `Player Communications` (đang dùng kho tạm `GS9 CFL Plan Version`).
- `GS9 CFL Item Catalog` — kho danh mục vật phẩm/giá còn thiếu cho `Economy Offer Analyst` (đang dùng kho tạm `GS9 CFL Data Daily`; phải tách khỏi `GS9 CFL Item Profile`, rà dữ liệu P0 trước khi đưa vào).
- `GS9 CFL CS FAQ & Policy` — đã có khung nhưng nội dung còn sơ khai, cần bổ sung câu hỏi/chính sách CS thật cho `CS Copilot`.

Đây chính là cách đóng nốt tình trạng "4 Agent dùng kho tạm" đã ghi ở `HANDOFF.md` mục 4.2 — làm xong việc này thì không cần vá tạm nữa. Quy trình dựng từng KB mới: soạn nội dung theo DEC-053 (không `DEC-xxx`/audit/nhãn kiểm chứng) → đặt tên `doc-NN-slug` (DEC-042) → tạo thư mục trong `knowledge/` → xin phép người dùng trước khi tạo KB/trỏ connector trên Web (như Việc A/B) → bật công cụ truy hồi → chat-test.

==================================================
VIỆC C — BACKUP 2,75 GB (còn treo từ phiên 10, DEC-085)
==================================================

Bốn thư mục **chỉ tồn tại trên Drive, không có bản sao nào khác**: `H5 Promotion` (1,74 GB), `Kho Tài Liệu Chưa Tích Hợp` (895 MB, nay 180 file), `GS9 CFL PUM` (127 MB), `GS9 CFL Item Profile` (24 MB). Phiên 10 đã hỏi, người dùng chọn **chấp nhận rủi ro tạm thời** — chưa backup.

**Hỏi lại người dùng đầu phiên này** xem đã sẵn sàng quyết định nơi backup chưa (ổ ngoài / Drive khác / tiếp tục chấp nhận rủi ro). Đừng tự ý chọn thay, và đừng để việc này rơi vào quên lãng — nhắc mỗi phiên cho tới khi giải quyết.

==================================================
VIỆC ĐÃ ĐÓNG TRONG PHIÊN 10 — không cần làm lại
==================================================

- **Gate build/test:** đã chạy lại sau đổi tài khoản Drive, sạch hoàn toàn (`Ran 30 tests OK`, builder khớp tuyệt đối `knowledge/` thật). Xem `HANDOFF.md` mục 4.11 nếu cần lặp lại cách chạy an toàn (bản cô lập trong scratchpad, không đụng `knowledge/` thật).
- **Nghi vấn ảnh minh hoạ thành nguồn dữ kiện sai (mục 4.5 HANDOFF cũ):** đã chạy lại Case 2 — không tái hiện lỗi, không có trích dẫn ảnh nào trong câu trả lời/bước suy luận. Cơ chế gốc (ảnh có thể được OCR và truy hồi làm nguồn) **vẫn đúng về kỹ thuật**, chỉ là không bị kích hoạt lần này — không cần điều tra thêm trừ khi lỗi tái xuất hiện thật. Bằng chứng: `audit/case2-retest-2026-09-18.md`.
- **README.md** đã có mục "KB và Agent hiện có trên VNG AI" — danh sách đầy đủ 14 KB local (9 tracked + 4 không tracked + 1 web-only) và 16 Agent (6 mặc định + 10 CFL custom, kèm kho đang gắn và đúng/tạm chuyên môn). **Cập nhật lại mục này nếu binding Agent × KB đổi.**

==================================================
LỆNH KIỂM TRA ĐẦU PHIÊN
==================================================

```bash
git rev-parse --show-toplevel
git status --short
git fetch origin && git diff --stat origin/main HEAD    # phải rỗng
ls knowledge/                                            # phải thấy 14 thư mục
find .git -type f -name desktop.ini -delete              # dọn rác Drive nếu có
```

==================================================
CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- Trả lời ngắn gọn, đi thẳng vào việc. **Hỏi gộp một lượt rồi làm**, đừng hỏi lắt nhắt.
- Phân biệt rõ **"đã kiểm chứng" / "chưa chứng minh" / "còn biến số"**. Không báo cáo suông.
- Kiểm chứng bằng nhiều lớp, **đối chiếu 2 nguồn độc lập** khi có thể.
- Khi công cụ báo lỗi, **tách nguyên nhân bằng test tối thiểu** trước khi kết luận.
- **Không grep/find đệ quy từ root** — `knowledge/` 2,75 GB trên Drive làm `grep -r` và `git status` timeout. Chỉ nhắm đúng file; việc nặng đẩy sang background.
- **Ghi file trên Drive qua file tạm + `os.replace`**; console Windows là cp1252 nên `print()` tiếng Việt sẽ `UnicodeEncodeError` *sau khi* tác vụ đã chạy xong — đừng nhầm là thất bại.
- **Trước mỗi `git add` diện rộng:** chạy `git check-ignore -v` trên đúng file credential (`knowledge/Keys Drive/*.json`). Pattern chung **không** phủ hết — đã suýt push service-account key (DEC-083).
- **Trước mỗi `git push`:** quét diff tìm secret/token thật (không chỉ tin từ khoá chung chung như "password" xuất hiện trong văn bản hướng dẫn — phân biệt với giá trị thật).
- Không tự ý: sửa file trong `knowledge/GS9 Knowledge VNG AI/` (KB đang sync chính), chạy builder ghi đè `knowledge/`, tạo/share KB trên Web, `git push --force`, `git add -f`.
- **Chỉ commit khi người dùng đồng ý** — không tự động commit giữa chừng, hỏi trước khi commit và trước khi push.
