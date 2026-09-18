Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root repo Git:

```
J:\My Drive\VNGGames AI\Knowledge Base VNG Source
```

Xác nhận bằng `git rev-parse --show-toplevel` (ổ đĩa có thể khác `J:` trên máy khác — nếu vậy, hỏi người dùng đường dẫn thật trên máy này).

**Kiến trúc hiện hành (DEC-082, 18/09/2026):** `knowledge/` nằm **trong** repo tại `<root>\knowledge`. Git chỉ theo dõi phần text/ảnh nhẹ (~30 MB); 4 thư mục binary nặng (`H5 Promotion`, `Kho Tài Liệu Chưa Tích Hợp`, `GS9 CFL PUM`, `GS9 CFL Item Profile`) và `Keys Drive` (credential) bị `.gitignore` loại trừ, chỉ tồn tại trên Drive. Đọc `README.md` mục "Phạm vi git" trước khi `git add`.

Đọc theo thứ tự: `README.md` → `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `DECISIONS.md` (tra từ DEC-084 khi cần — đó là mốc phiên trước bàn giao).

==================================================
0. TRẠNG THÁI KHI BÀN GIAO (kiểm chứng 18/09/2026, cuối phiên 10)
==================================================

- Repo **sạch**, HEAD = `3c417ac`, đã **push lên `origin/main`** — máy khác `git pull --ff-only origin main` sẽ thấy đúng trạng thái này.
- 3 file untracked ở root là cố ý giữ, **đừng xoá**: `knowledge-20260820T085450Z-1-001.zip`, `CFL Thu Thập Dữ Liệu.xlsx`, `VNGGames AI.html`.
- `knowledge/` nay có **14 thư mục con** (không phải 12 như tài liệu cũ ghi) — hai thư mục mới: `GS9 CFL Metric Playbook/` và `GS9 Dokploy VNG AI/`. Cả hai đã commit, **chưa lên Web**.
- Nếu git báo `fatal: bad object refs/desktop.ini`: chạy `find .git -type f -name desktop.ini -delete` rồi `git for-each-ref` — đây là rác Google Drive tái sinh liên tục (DEC-083), không phải repo hỏng.

**Phiên trước (phiên 10) đã đóng Việc 1 và Việc 2 trong `NEXT_SESSION_PROMPT.md` cũ, và làm được phần thu thập/soạn nội dung của Việc 3.** Việc còn lại của phiên này chủ yếu là **hoàn tất Việc 3** (đưa lên Web + chat-test) và **Việc 1b** (backup) — cả hai đều cần **người dùng ra quyết định hoặc tự thao tác trên Web**, agent không tự làm được.

==================================================
VIỆC A — HOÀN TẤT KB "GS9 DOKPLOY VNG AI" (ưu tiên cao nhất — đây là việc chính người dùng muốn)
==================================================

Nội dung **đã viết xong, đã commit** tại `knowledge/GS9 Dokploy VNG AI/doc-00` → `doc-05` (giới thiệu, điều kiện truy cập, quy trình 9 bước, xác thực & bảo mật, FAQ, và trang riêng cho dev dùng GigiKit CLI). Biên tập theo DEC-053 (không `DEC-xxx`, không link `audit/`, không nhãn "đã/chưa kiểm chứng"). Nguồn thô lưu tại `scripts/one-off/dokploy-source-a-raw.md` và `dokploy-source-b-raw.md` nếu cần đối chiếu lại.

**Việc cần làm theo thứ tự:**

1. **Hỏi người dùng đã đọc/duyệt 6 file nội dung chưa** — nếu muốn sửa gì, sửa trực tiếp trong `knowledge/GS9 Dokploy VNG AI/` (KB này viết tay, không qua `build_handbook.py`, không có nguồn `docs KB/Human` tương ứng).
2. **Tạo KB `GS9 Dokploy VNG AI` trên `vnggames.ai`** — việc này **cần người dùng tự làm hoặc cho phép rõ ràng** (AGENTS.md: không tự share/cấu hình sync). Nếu người dùng cho phép agent thao tác qua `claude-in-chrome` (Chrome thật, đã đăng nhập), làm theo đúng quy trình DEC-046 (Google Drive connector, trỏ đúng một thư mục con `knowledge/GS9 Dokploy VNG AI/`, tuyệt đối không trỏ root project).
3. **Sau khi lên Web: bật công cụ truy hồi** cho Agent nào sẽ dùng kho này (DEC-061 — gắn KB **không** tự bật `Tìm theo ngữ nghĩa`/`Tìm theo từ khóa`).
4. **Chat-test** theo checklist DEC-062 (không bịa, không lộ PII, truy hồi chạy đúng, trích dẫn đúng nguồn).
5. Cập nhật `HANDOFF.md` mục 4.13 và `STATUS.md` khi xong từng bước — đừng chờ xong hết mới ghi.

==================================================
VIỆC B — LÊN WEB KB "GS9 CFL METRIC PLAYBOOK"
==================================================

`gs9-metric-playbook.docx` (52 metric, 4 phần) đã được chuyển vào kho riêng `knowledge/GS9 CFL Metric Playbook/doc-00-metric-playbook.docx`, đã commit. **Chưa lên Web.**

Việc cần làm: giống Việc A bước 2–4 — tạo KB `GS9 CFL Metric Playbook` trên `vnggames.ai`, trỏ connector đúng thư mục, bật công cụ truy hồi, chat-test. Xem `HANDOFF.md` mục 4.12.

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
