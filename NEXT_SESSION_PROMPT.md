Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root repo Git:

```
J:\My Drive\VNGGames AI\Knowledge Base VNG Source
```

Xác nhận bằng `git rev-parse --show-toplevel` (ổ đĩa có thể khác `J:` trên máy khác).

**Kiến trúc hiện hành (DEC-082, 18/09/2026):** `knowledge/` nằm **trong** repo tại `<root>\knowledge`. Không còn shortcut `.shortcut-targets-by-id` sang Drive công ty — kiến trúc DEC-076 đã bị thay thế. Trên đĩa `knowledge/` có 354 file / 2,75 GB nhưng **git chỉ theo dõi 139 file / 29,7 MB**; 4 thư mục binary nặng bị `.gitignore` loại trừ (`H5 Promotion`, `Kho Tài Liệu Chưa Tích Hợp`, `GS9 CFL PUM`, `GS9 CFL Item Profile`) và `Keys Drive` (credential). Đọc `README.md` mục "Phạm vi git" trước khi `git add`.

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` (mục 4.5 là việc ưu tiên còn mở) → `STATUS.md` → `DECISIONS.md` từ DEC-075 tra khi cần.

==================================================
0. TRẠNG THÁI KHI BÀN GIAO (kiểm chứng 18/09/2026, phiên 10)
==================================================

- Đã **chuyển sang tài khoản Google Drive mới**. Di trú không mất dữ liệu: HEAD/tree/hash index/số file tracked khớp tuyệt đối với mốc chụp trước khi chuyển (DEC-082).
- Repo có commit mới của phiên 10 (cập nhật tài liệu + `README.md` + đưa `knowledge/` vào git theo phạm vi giới hạn).
- Tài liệu đã đối chiếu với thực tế `knowledge/` ngày 18/09: sửa 3 chỗ sai (Knowledge Agent 28→8 `.md`, ảnh 49→52, bổ sung 2 kho chưa từng được mô tả).
- **Gate build/test CHƯA chạy lại** sau khi chuyển tài khoản — `build_handbook.py` ghi vào `knowledge/`, nay đã trở lại trong repo nên *có thể* chạy được, nhưng chưa ai thử.
- Nếu git báo `fatal: bad object refs/desktop.ini`: Drive lại rải `desktop.ini` vào `.git/`. Chạy `find .git -type f -name desktop.ini -delete`. Repo không hỏng (DEC-083).

==================================================
1. VIỆC ƯU TIÊN SỐ 1 — CÓ VIỆC ĐÃ LÀM NHƯNG CHƯA VÀO SỔ
==================================================

**Ngày 25/08/2026 có một phiên làm việc không được ghi vào bất kỳ tài liệu nào.** Tìm chuỗi `metric.playbook` trong các file `.md` chỉ khớp đúng file prompt này — nghĩa là `STATUS.md`, `HANDOFF.md`, `DECISIONS.md` đều không biết việc này từng xảy ra. Cần ghi lại thành **DEC-082** + mục mới trong `STATUS.md` + cập nhật `HANDOFF.md`.

**Việc đã làm hôm đó:** dựng tài liệu KB dạng `.docx` từ file `gs9-metric-playbook.html` (playbook bộ metric chuẩn của GS9 cho CFM VN · PTG · DT3Q).

Kết quả: `knowledge/Kho Tài Liệu Chưa Tích Hợp/gs9-metric-playbook.docx` (529 KB). Đã kiểm lại 18/09: file **còn nguyên vẹn** — 690 đoạn, 12 bảng, 1 ảnh nhúng, 36.065 ký tự văn bản, zip không lỗi.

Cấu trúc file: bìa + bảng thông tin tài liệu · Mục lục (trường tự động) · Phần I quy ước chung và nhãn phụ trách · Phần II định nghĩa 52 metric theo 10 nhóm · Phần III bảng tổng hợp nhanh (10 bảng) · Phần IV phân rã chỉ số gộp (sơ đồ D0 nhúng ảnh + 4 thẻ D1–D4 + bảng ma trận Install type × User status).

**Mức bằng chứng của phiên đó:**

| Việc | Mức |
|---|---|
| Độ phủ nội dung 100% (từng từ hiển thị trong HTML đều có trong `.docx`) | **Đã kiểm chứng** — đối chiếu token tự động |
| XML hợp lệ, đủ thành phần OOXML, 12/12 bảng khớp độ rộng cột | **Đã kiểm chứng** — parser UTF-8 riêng |
| Bố cục/màu/bảng/sơ đồ hiển thị đúng | **Đã kiểm chứng** — render thật từng phần qua `docx-preview` |
| File mở đúng trong Word thật | **CHƯA kiểm chứng** — không xuất được PDF trên máy này (xem mục 3) |

**Phát hiện cần ghi vào sổ:** file HTML nguồn ghi *"10 nhóm · 53 metric"* nhưng thực tế chỉ có **52** — đếm 2 nguồn độc lập trong HTML đều ra 52 (52 thẻ `article.metric` và 52 dòng bảng). File `.docx` dùng số đúng là 52. Nếu bản HTML còn ở đâu đó, nên sửa con số này.

==================================================
2. VIỆC CẦN QUYẾT ĐỊNH — ĐANG TREO, KHÔNG TỰ Ý LÀM
==================================================

**Số phận file `gs9-metric-playbook.docx`.** Câu hỏi này đã đặt ra cuối phiên 25/08 nhưng **người dùng chưa trả lời**:

File đang nằm trong `Kho Tài Liệu Chưa Tích Hợp` — thư mục này **không được connector đồng bộ vào KB nào**, nên nội dung playbook hiện chưa lên Web, Agent chưa tra được. Muốn đưa lên thì cần quyết:

1. Chuyển vào KB nào? (`GS9 Knowledge VNG AI` là kho hướng dẫn nền tảng — playbook metric có thể không thuộc đây; có thể cần kho nghiệp vụ Data riêng)
2. Đổi tên theo quy ước `doc-` (DEC-042) chưa? Tên hiện tại `gs9-metric-playbook.docx` không khớp regex đồng bộ `^(doc|image)-`.

**Hỏi người dùng trước khi di chuyển** — chuyển file vào thư mục KB sẽ kích hoạt connector đồng bộ lên Web thật.

==================================================
3. CẢNH BÁO: KHÔNG TÁI TẠO LẠI ĐƯỢC FILE NÀY
==================================================

Hai thứ cần cho việc dựng lại `.docx` **đều đã mất**:

- **File HTML nguồn đã không còn.** `find` toàn cây `knowledge/` chỉ thấy `.docx`, không còn `gs9-metric-playbook.html` (bản gốc 153 KB, còn tồn tại lúc 24/08 17:16). Không rõ người dùng xoá, chuyển đi, hay đổi tên — **hỏi, đừng suy đoán**.
- **Scratchpad phiên cũ đã bị xoá.** Toàn bộ script dựng file (`extract.py` trích HTML→JSON, `build.js` dựng DOCX, `verify_docx.py`, `coverage.py`, `preview.html`, `srv.py`) và `content.json`, `diagram-d0.png` đều mất — scratchpad là theo phiên, không lưu lâu dài.

→ **Hệ quả:** `gs9-metric-playbook.docx` hiện là bản duy nhất của nội dung đó. Muốn sửa nội dung thì phải sửa thẳng trên `.docx` (hoặc tìm lại bản HTML). Nếu người dùng cần pipeline tái tạo, phải viết lại từ đầu — lần này **lưu script vào `scripts/one-off/`** như tiền lệ `relink_images_2026-08-20.py`, đừng để trong scratchpad.

==================================================
4. CẠM BẪY MÔI TRƯỜNG ĐÃ KIỂM CHỨNG (máy công ty) — tiết kiệm nhiều giờ nếu đọc trước
==================================================

Phát hiện 25/08 khi làm `.docx`, chưa ghi vào `HANDOFF.md` mục 5 (nên ghi vào):

- **Không xuất được PDF bằng Word.** Word COM mở file bình thường (~2s) nhưng `ExportAsFixedFormat` **treo vô hạn** — đã thử với tài liệu trắng chỉ chứa chữ "Hello" cũng treo, nên là vấn đề của Word/máy, không phải của file. Đã đốt ~15 phút mới tách được nguyên nhân. Máy **không có** LibreOffice, `pandoc`, `pdftoppm`.
- **Cách kiểm chứng `.docx` thay thế (đã dùng được):** `npm install docx-preview jszip` trong scratchpad → dựng trang HTML dùng `docx.renderAsync()` → chạy server cục bộ (`python -m http.server`) → mở bằng Chrome thật và chụp. **Bắt buộc render 1 trang mỗi lần tải** (tham số `?p=N`, xoá các `section.docx` khác khỏi DOM): để cả tài liệu (~19.000 px) thì `Page.captureScreenshot` timeout.
- **Trình duyệt in-app không đăng nhập được vnggames.ai** — dùng Chrome thật (`mcp__claude-in-chrome__*`). Trình duyệt in-app cũng chỉ render **snapshot tĩnh** với file ngoài project folder, không chạy JS → muốn chạy JS trên file local phải copy vào scratchpad rồi serve qua HTTP.
- **`scripts/office/validate.py` của skill docx báo lỗi giả trên Windows:** nó mở XML bằng codec `charmap` (cp1252) nên vỡ ở chữ tiếng Việt, báo "FAILED - found NEW validation errors". Tự kiểm bằng parser UTF-8 thì **22/22 phần XML hợp lệ, 0 lỗi**. Đừng tin kết quả của script đó trên máy này.
- **`scripts/office/soffice.py` của skill crash trên Windows:** dùng `socket.AF_UNIX` (chỉ có trên Unix).
- **`convertMillimetersToTwip` làm tròn xuống:** A4 210mm → 11905 (không phải 11906), lề 20mm → 1133. Nên chiều rộng nội dung = **9639** twip, không phải 9638. `columnWidths` của bảng phải cộng đúng bằng số này, nếu không Word co giãn cột sai. Nên tính cột cuối = `CONTENT_W - tổng các cột trước` thay vì gõ tay.
- **`docx` npm không có sẵn** dù SKILL.md nói preinstalled → `npm install docx` trong scratchpad.
- **Không đặt `keepNext` trên hàng trăm đoạn liên tiếp** — làm Word thrash khi phân trang.
- Console Git Bash/PowerShell là cp1252: `print()` chuỗi tiếng Việt sẽ `UnicodeEncodeError` **sau khi** tác vụ đã chạy xong. Đừng nhầm là tác vụ thất bại; thêm `sys.stdout.reconfigure(encoding="utf-8")`.
- **Ghi file trên Drive phải qua file tạm + `os.replace`** (cạm bẫy cũ, vẫn đúng) — ghi đè trực tiếp từng làm mất sạch nội dung một file.

==================================================
5. BỐI CẢNH MỚI — TEAM ĐANG DỒN TÀI LIỆU NGUỒN VÀO
==================================================

Từ 26–28/08, `Kho Tài Liệu Chưa Tích Hợp` mọc thêm 4 thư mục con chứa tài liệu nghiệp vụ thật (chưa ai xử lý, chưa vào KB nào):

| Thư mục | Nội dung |
|---|---|
| `Event/` | `Event Control`, `Event Plan` |
| `Function/` | `Content Game`, `Function Game`, `Quản lý lỗi Function`, `Survey` |
| `Localize/` | `总翻译表20260824.xlsx` (bảng dịch tổng) |
| `Membership/` | 6 file `.docx`/`.xlsx` về Membership, Săn Thẻ Đổi Quà |

Việc này khớp hướng DEC-075: **KB/Agent hiện tại không phải bản cuối**, team đang thu thập lại nguồn qua Sheet `CFL Thu Thập Dữ Liệu` để dựng lại cấu trúc kho từ đầu. Rất có thể đây mới là việc chính người dùng muốn làm tiếp — **hỏi trước khi đầu tư công sức**, và **đừng tối ưu cấu trúc KB/Agent cũ** vì sẽ bị thay.

==================================================
6. LỆNH KIỂM TRA ĐẦU PHIÊN
==================================================

```powershell
# 1. Repo
git rev-parse --show-toplevel
git status --short
git fetch origin; git diff --stat origin/main HEAD    # phải rỗng

# 2. knowledge/ co day du khong
ls knowledge/    # phai thay 12 thu muc kho

# 3. File playbook còn đó và nội dung chưa vào sổ
ls -la "knowledge/Kho Tài Liệu Chưa Tích Hợp/"
grep -ril "metric.playbook" --include=*.md .          # chỉ thấy NEXT_SESSION_PROMPT.md = vẫn chưa vào sổ
```

Nếu lệnh (2) thiếu thư mục, Drive chưa sync xong — **đợi sync hết** rồi kiểm lại, đừng kết luận mất dữ liệu (DEC-064).

==================================================
7. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- Trả lời ngắn gọn, đi thẳng vào việc. **Hỏi gộp một lượt rồi làm**, đừng hỏi lắt nhắt.
- Phân biệt rõ **"đã kiểm chứng" / "chưa chứng minh" / "còn biến số"**. Không báo cáo suông.
- Kiểm chứng thật bằng nhiều lớp; khi có thể, **đối chiếu 2 nguồn độc lập** trước khi kết luận (cách này đã bắt được lỗi đếm 53↔52 và 3 khối nội dung bị bỏ sót khi trích HTML).
- Khi một công cụ báo lỗi, **tách nguyên nhân bằng test tối thiểu** trước khi kết luận — đừng đoán (bài học Word COM: tưởng do tài liệu phức tạp, thực ra treo cả với tài liệu trắng).
- Khi phát hiện điều mới: ghi vào `DECISIONS.md`, rồi chắt phần "người dùng cần làm gì" sang `docs KB/Human` nếu liên quan hướng dẫn thao tác.
- Không tự ý: chuyển file vào thư mục KB (kích hoạt sync lên Web), xoá file, commit/push khi chưa được yêu cầu.
