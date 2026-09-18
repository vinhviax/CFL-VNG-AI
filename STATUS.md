# Trạng thái Knowledge Base VNG

**Ngày snapshot:** 18/09/2026 (phiên 10, máy công ty — chuyển tài khoản Google Drive)
**Phiên bản:** 5.0.0 — đổi tài khoản Drive, `knowledge/` trở lại trong repo, giới hạn phạm vi git

## MỚI 18/09/2026 (phiên 10) — chuyển tài khoản Google Drive, `knowledge/` trở lại repo, chặn 2 sự cố hạ tầng (DEC-082/083)

**Người dùng chuyển toàn bộ project sang tài khoản Google Drive mới.** Root mới: `J:\My Drive\VNGGames AI\Knowledge Base VNG Source`. `knowledge/` nay là thư mục thật trong project, không còn shortcut `.shortcut-targets-by-id` sang Drive công ty — **thay thế kiến trúc DEC-076**.

**1. Di trú không mất dữ liệu — đã kiểm chứng bằng mốc chụp trước khi chuyển.** Bốn giá trị khớp tuyệt đối trước/sau: HEAD `c56eeb9`, tree `966f9272`, hash index `f7b3848d`, 345 file tracked. `origin/main` cũng khớp. Không tái diễn sự cố DEC-059/064.

**2. Suýt push service-account key lên GitHub (DEC-083).** `knowledge/Keys Drive/cfl-drive-kb-f36f5888736e.json` không khớp bất kỳ pattern credential nào trong `.gitignore` — rule cũ chỉ chặn thư mục tên đúng `keys`, không chặn `Keys Drive`. Đã thêm rule chặn; kiểm lịch sử git xác nhận **chưa từng bị commit** nên không cần rotate key. Không mở nội dung, không xoá khỏi đĩa (connector đang dùng).

**3. Google Drive làm hỏng `.git` (DEC-083).** 155 file `desktop.ini` Drive tạo bên trong `.git/` — những cái ở `refs/*` khiến git báo `fatal: bad object refs/desktop.ini` và `git fsck` báo `badRefContent`. Đã xoá; HEAD/tree không đổi. Sẽ tái sinh khi Drive sync lại.

**4. Đối chiếu tài liệu với thực tế `knowledge/` — tìm ra 3 chỗ sai/thiếu:**
- `GS9 CFL Knowledge Agent` thực tế **8** `.md`, tài liệu ghi **28** — sai.
- `GS9 Knowledge VNG AI` thực tế **52** PNG, tài liệu ghi **49** — lỗi thời từ phiên 7.
- Hai kho **chưa từng được mô tả ở đâu**: `H5 Promotion` (6 file, 1,74 GB) và `Kho Tài Liệu Chưa Tích Hợp` (181 file, 895 MB, gồm `gs9-metric-playbook.docx` và 4 nhóm tài liệu nguồn team gửi).

**5. Phạm vi git mới (DEC-082).** `knowledge/` = 354 file / 2,75 GB, nhưng chỉ **139 file / 29,7 MB** được theo dõi. Loại trừ 4 thư mục binary nặng vì **3 file zip trong `H5 Promotion` (649/570/503 MB) vượt giới hạn cứng 100 MB/file của GitHub — push sẽ bị từ chối thẳng**. Đã loại Git LFS vì 2,75 GB vượt xa quota free 1 GB.

**6. Ghi nhận muộn việc ngày 25/08/2026.** Phiên đó dựng `gs9-metric-playbook.docx` (529 KB, 4 phần, 52 metric, nhúng sơ đồ phân rã) từ `gs9-metric-playbook.html`, nhưng **không được ghi vào tài liệu nào**. File hiện ở `knowledge/Kho Tài Liệu Chưa Tích Hợp/`, còn nguyên vẹn (690 đoạn, 12 bảng, 1 ảnh). **Không tái tạo lại được**: bản HTML nguồn đã không còn trên đĩa và scratchpad phiên đó đã bị xoá. Vẫn treo: chưa quyết đưa vào KB nào và chưa đổi tên theo quy ước `doc-`.

**Đã viết `README.md` cho repo** (trước đây không có).

## Snapshot trước đó — phiên 9 (21/08/2026)

## MỚI 21/08/2026 (phiên 9, tiếp) — đóng vòng relink Plan Version, kiểm chứng bằng Chrome thật (DEC-081)

**Người dùng tự nạp 12 file `.md` Plan Version lên Web xong.** Kiểm qua Chrome thật (không chỉ tin lời báo):
- 12/12 file `doc-v5-*.md` đều `Hoàn tất`, cập nhật `21 thg 8, 2026` — khớp mốc sửa local.
- Tổng tài liệu KB hiện 43 (không phải 41 kỳ vọng) — điều tra ra 2 "dư" chỉ là `source-manifest.json` và `image-map.json` bị connector tự đánh chỉ mục làm tài liệu, không phải trùng lặp thật.
- Mở `doc-v5-03-cach-choi-moi.md` (8 ảnh nhúng), tab "Toàn văn": 8/8 `<img>` có `naturalWidth > 0`, đối chiếu `read_network_requests` thấy đúng 8 request `files?file_path=...exports/<uuid>` **status 200**, uuid khớp tuyệt đối MAP đã dùng relink.

**Kết luận: cả 2 KB (`GS9 Knowledge VNG AI` 52 ảnh + `GS9 CFL Plan Version` 29 ảnh) đã đóng vòng relink hoàn toàn, có bằng chứng kỹ thuật (không chỉ trạng thái tài liệu).** Xem DEC-081.

## Snapshot trước đó — phiên 9, phần đầu (21/08/2026, máy công ty)

## MỚI 21/08/2026 (phiên 9, máy công ty) — hoàn tất relink 81/81 ảnh (2 KB), commit xoá `knowledge/` local (DEC-080)

**Đóng vòng mục 4.10 HANDOFF từ phiên trước.** Đầu phiên xác nhận: đường dẫn Drive công ty còn đúng, `get_document_info` **vẫn chưa** trả `file_path` (DEC-079 chưa tự phục hồi).

**1. `GS9 Knowledge VNG AI` (52 ảnh): viết lại `image-map.json` với 52 URI `exports/` đã lấy từ phiên trước.** Người dùng xác nhận đã nạp 20 file `.md` relink lên Web và kiểm ảnh hiện đúng — vòng này đã khép kín thật, không chỉ là thay đổi cục bộ.

**2. `GS9 CFL Plan Version` (29 ảnh) — relink xong, KHÔNG cần share vào MCP.** Người dùng chọn duyệt qua trình duyệt thay vì thử API bearer token. Dùng Chrome thật (đã đăng nhập), mở từng tài liệu trên Web UI. 18/29 ảnh có URI `exports/` nhúng sẵn trong "Tóm tắt" giống cơ chế KB kia; **11/29 ảnh không có embed trong Tóm tắt lẫn Toàn văn dạng text** — phải bắt thuộc tính `data-protected-src` của `<img class="markdown-image">` ngay khi tab "Toàn văn" vừa mount, **trước khi** React tự xoá attribute này lúc ảnh resolve xong thành `blob:` (phải poll ~50ms/lần). Phân biệt ảnh chính với icon nhỏ minh hoạ cùng tài liệu bằng `alt` khớp đúng tên file. Đối chiếu chéo 1 case (`image-v5-13`) giữa 2 phương pháp — khớp tuyệt đối. Relink 29 URI vào 12 file `doc-v5-*.md` (2 định dạng khác nhau: `LOCAL_ASSET` comment + embed, và bảng danh mục `- **Asset:** [tên](URI)` trong `doc-v5-10`) và viết lại `image-map.json` Plan Version. Xem DEC-080.

**Còn treo lúc đó — đã đóng ngay trong cùng phiên, xem mục "MỚI" phía trên.**

**3. `knowledge/` trong repo local: người dùng chọn commit chính thức việc xoá.** Đã `git rm -r knowledge/` (153 file) + commit + push lên `origin/main`. Kiến trúc mới (Drive công ty là nguồn duy nhất) nay đã chốt trong lịch sử git, không còn ở trạng thái working-tree-khác-HEAD dễ nhầm lẫn.

**4. Dọn root:** xoá `CFL Thu Thập Dữ Liệu.xlsx` (bản export cũ, đã có bản sống trên Drive công ty). Giữ lại `knowledge-20260820T085450Z-1-001.zip` (backup) và `VNGGames AI.lnk` (không cần track, nhưng vô hại).

## Snapshot trước đó — phiên 8 (20/08/2026, máy công ty)

## MỚI 20/08/2026 (phiên 8, máy công ty) — đổi kiến trúc sang Drive công ty, đứt URI ảnh, relink 52/52 ảnh, còn treo image-map.json + Plan Version

**Thay đổi lớn nhất phiên này: dự án đang chuyển pha.** Người dùng xác nhận KB và Agent hiện tại **không phải bản cuối** — sẽ dựng lại sau khi thu thập xong tài liệu team qua Sheet `CFL Thu Thập Dữ Liệu` (Drive công ty, 4 sheet: HuongDan/LoaiDoc/ThuThapDoc/TuDien). Từ nay **không nên đầu tư công sức lớn chỉnh sửa cấu trúc KB/Agent cũ**.

**1. Kiến trúc đổi: bỏ `knowledge/` trong repo Drive cá nhân, dùng thẳng Drive công ty.** Đường dẫn mới: `J:\.shortcut-targets-by-id\1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG\VNGGames AI\knowledge` (ID thư mục có thể đổi theo máy — xác nhận lại đầu phiên). Người dùng tự xoá `knowledge/` khỏi repo local (153 file). **CHƯA COMMIT** — `git status` vẫn thấy 153 file `D`, `origin/main` chưa đổi. Có bản sao lưu `knowledge-20260820T085450Z-1-001.zip` (164 MB) tại root, untracked — giữ lại. Xem DEC-076.

**2. Đổi Service Account JSON của `GS9 Knowledge VNG AI` sang key Drive công ty → toàn bộ URI ảnh gốc chết.** `knowledge_id` mỗi tài liệu giữ nguyên (Ghi đè theo tên file), nhưng nội dung/URI lưu trữ nạp lại từ đầu. Xem DEC-077.

**3. Công cụ MCP mất khả năng trả `file_path` giữa phiên — không liên quan việc đổi Drive.** Trùng thời điểm với việc một tool khác cùng server bị ngắt/thay thế, không phải do đổi Drive. Xem DEC-079.

**4. Tìm và xác nhận đường vòng: URI `exports/` (bản kết xuất OCR) render đúng khi nhúng vào `.md`.** Thực nghiệm thật: sửa `doc-00`, nạp lên Web, ảnh hiện, xác nhận qua network request 200 — không phải suy đoán. Lấy đủ **52/52 URI** cho `GS9 Knowledge VNG AI`, relink **63 lượt URI trong 20/21 file `.md`** trên Drive công ty (dùng comment `LOCAL_ASSET` làm neo, tránh thay nhầm placeholder ví dụ trong văn bản). Xem DEC-078.

**5. Rủi ro chưa chứng minh:** URI `exports/` là bản kết xuất phụ, không phải blob gốc — chưa rõ có bền lâu dài không.

**Còn treo cho phiên sau:**
- **`image-map.json` trên Drive công ty CHƯA cập nhật 52 URI mới** — nếu ai chạy `build_handbook.py` trước khi cập nhật, sẽ ghi đè mất công relink vừa làm. **Việc ưu tiên số 1 đầu phiên sau.**
- **`GS9 CFL Plan Version` (29 ảnh) hoàn toàn chưa relink** — KB này ngoài phạm vi MCP (`list_knowledge_bases` không thấy), cần người dùng share vào không gian MCP hoặc tìm cách khác.
- Chưa xác nhận người dùng đã nạp 20 file `.md` vừa sửa lên Web.
- `knowledge/` trong repo local vẫn ở trạng thái xoá chưa commit — cần quyết định commit hay khôi phục.
- 3 file untracked ở root cần dọn: zip backup (giữ), `CFL Thu Thập Dữ Liệu.xlsx` cũ (có thể xoá), `VNGGames AI.lnk` (không cần trong git).

Chi tiết đầy đủ: `audit/session-2026-08-20-migration-va-relink-anh.md`.

## Snapshot trước đó — phiên 7 (19/08/2026, máy nhà)

**Ngày snapshot:** 19/08/2026 (phiên 7, máy nhà)
**Phiên bản:** 3.8.0

## MỚI 19/08/2026 (phiên 7, máy nhà) — hàng đợi nền tảng thông, gate sạch hoàn toàn (DEC-073)

**Hàng đợi đã thông.** Kiểm qua MCP `list_documents` (4 trang, `page_size=20`): **52/52 ảnh PNG và 21/21 tài liệu `.md` đều `parse_status: completed` + `enable_status: enabled`** trong `GS9 Knowledge VNG AI`. Đúng 26 ảnh đổi URI (23 crop lại + 3 ảnh mới `image-50/51/52`), 26 ảnh còn lại giữ nguyên URI như dự đoán DEC-069/072 — khớp tuyệt đối.

**Đã viết lại `image-map.json` đủ 52 entry, build lại 20 module bị ảnh hưởng** (`build_handbook.py`), trong đó `doc-11-chat-kiem-thu-va-bao-tri.md` lần đầu build thành công với 3 ảnh mới (6 tham chiếu: 3 comment `LOCAL_ASSET` + 3 URI `minio://`).

**Sửa nốt chỗ khoá cứng cuối cùng:** `test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs` khoá số lượt tham chiếu ảnh `61` → `64` (tăng đúng 3, khớp 3 ảnh mới trong `doc-11`).

**Gate sạch hoàn toàn:** `Ran 30 tests OK` (6 skip do thiếu nguồn Plan V5 ở máy nhà, bình thường) — **không còn FAIL nào**. `link_plan_v5_minio.py --check` báo 0 thay đổi cần thiết.

**Sự cố vận hành gặp giữa phiên (đã tự xử lý, không mất dữ liệu):** `git commit` đầu tiên bị Bash tool cắt ngang ở mốc 2 phút vì ghi 20 file qua Google Drive chậm — tiến trình con vẫn chạy ngầm và để lại 3 file khoá rác (`HEAD.lock`, `refs/heads/main.lock`, `objects/maintenance.lock`, cái cuối có từ 17/08). Xác nhận không còn tiến trình `git` nào chạm tới repo này (`Get-CimInstance Win32_Process` lọc theo đường dẫn) trước khi xoá tay từng lock — đúng runbook git tự khuyến nghị khi lock bị treo. Commit thứ hai `3cec768` thành công, không mất staged changes.

**Đã đóng vòng — người dùng xác nhận đã đồng bộ 19 file `.md` lên Web.** Kiểm bằng hash: `doc-11-chat-kiem-thu-va-bao-tri.md` trên Web có `file_hash` **khớp tuyệt đối** với bản local vừa build (`b12393cfa21bb51be7fe71d33f274181`), `parse_status: completed`, `enable_status: enabled`, cập nhật lúc 20/08/2026 04:16. **Toàn bộ 73 tài liệu (52 ảnh + 21 md) trong `GS9 Knowledge VNG AI` nay đều `Hoàn tất`.**

**Hệ quả mở khoá:** điều kiện chạy lại Case 2 (mục 4.5 HANDOFF, nghi vấn Agent lấy ảnh làm nguồn dữ kiện sai) trước đây ghi "đủ 70 tài liệu Hoàn tất" — con số đó lỗi thời từ trước khi thêm `image-50/51/52` (70 = 49 ảnh cũ + 21 md). Điều kiện đúng bây giờ là **73/73**, và đã đạt. Việc phiên sau có thể chạy lại Case 2.

## MỚI 18/08/2026 (phiên 6, máy nhà) — hàng đợi xử lý của nền tảng tắc thật, không phải lỗi file; DEC-069 được xác nhận lần hai

**1. Hàng đợi xử lý tài liệu tắc ở tầng nền tảng (DEC-071).** 26 ảnh nạp lên lúc 17/08 18:48–18:49 tới 18/08 04:20 vẫn **0 ảnh `completed`** (21 `pending`, 4 `processing`, 1 `finalizing`). Mở panel "Xem tiến trình" trên Web cho `image-28` và `image-02`: cả hai đều **`Chờ` · 0/5 giai đoạn**, cả 5 bước (Phân tích tài liệu → Chia đoạn → Vector hóa → Đa phương thức → Hậu xử lý) đều "Đang chờ", và có bộ đếm lần thử `#1 #2` / `#1 #2 #3` — tức job được xếp hàng, hết giờ, xếp lại, **không worker nào chạy**. `image-28` từng lên tới `finalizing` rồi tụt về `pending`, `failed_stages.summary = "failed to update knowledge: context deadline exceeded"`. → "Phân tích lại" chỉ thêm một lần thử nữa, **không gỡ được tắc**; việc cần làm là báo team vận hành nền tảng.

**2. Toàn bộ 21 `doc-*.md` bị nạp lại lúc 00:00–00:01 ngày 18/08** — document ID mới, `parse_status: pending`, `enable_status: disabled`. Hệ quả đang có: KB `GS9 Knowledge VNG AI` **hiện không có tài liệu chữ nào được lập chỉ mục**; Agent trỏ vào kho này (`CS Copilot`, `GM Policy Advisor`, `Knowledge Curator`) chỉ còn tra được ảnh. Không phải do ai sửa nội dung — đây là lần chạy đồng bộ định kỳ (xem DEC-072).

**3. DEC-069 được xác nhận lần hai bằng dữ liệu mới (DEC-072).** Đối chiếu bằng script toàn bộ 26 ảnh `completed` với `image-map.json` (sinh 16/08): **26/26 URI khớp tuyệt đối, 0 lệch**. Chuyện này xảy ra **sau** một lần đồng bộ chạy ở chế độ `Toàn bộ` — nên quy tắc đúng là: kể cả chế độ Toàn bộ, file không đổi nội dung vẫn giữ nguyên document và URI; chỉ file đổi hash hoặc file mới mới bị tạo lại.

**4. Trạng thái `image-map.json` hiện tại:** 49 entry — **26 còn sống**, **23 đã chết** (23 ảnh crop lại có document ID mới, ví dụ `image-01` map `009e72d5…` vs live `493336f4…`), **thiếu hẳn `image-50/51/52`**. Cần đủ 52 URI hợp lệ mới build lại được `doc-11`.

**5. Đã sửa 2 chỗ khoá cứng "49 ảnh" trong test** (`tests/test_build_handbook.py:87-88`, `49` → `52`). Cả hai nằm trong test đang FAIL sẵn (`test_project_image_map_covers_all_merged_assets`) nên không làm hỏng thêm test nào. **Còn một chỗ phải sửa sau khi có URI:** `test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs` đang khoá số lượt tham chiếu ảnh là `61`; khi `doc-11` nhúng thêm 3 ảnh mới, số này sẽ đổi.

**Gate cuối phiên:** vẫn đúng **1 FAIL đã biết** (`test_project_image_map_covers_all_merged_assets`) — chờ nền tảng xử lý xong ảnh, không được che bằng `--allow-missing-minio`.

## MỚI 17/08/2026 (phiên 5, máy công ty) — converter Plan V5, KB-20, dọn artifact, sửa file thuyết trình, tính năng "Thêm vào tri thức", đính chính DEC-052

**1. Converter Plan V5 kiểm chứng end-to-end (DEC-063).** Máy công ty có HTML nguồn Plan V5 nên 6 test trước đây skip nay chạy và **pass toàn bộ**. 29 ảnh converter sinh ra khớp SHA256 tuyệt đối với bundle đang commit. Sửa 1 dòng test còn khoá bố cục `assets/` cũ (đã đổi sang phẳng từ DEC-054).

**2. `KB-20-thiet-ke-danh-muc-kho.md` — nội dung "nên dựng những loại kho nào" đã vào kho thật (DEC-065).** Trước đó chỉ có trong file HTML thuyết trình. Đính chính ghi chép cũ: không cần sửa `HUMAN_SOURCE_PREFIXES` (hằng đó không khoá dải số), chỉ cần đánh số tiếp từ 20. Đã build ra `doc-20`, người dùng đã nạp lên Web — `GS9 Knowledge VNG AI` nay 21 tài liệu.

**3. Dọn 2 artifact dư thừa ở root (DEC-066).** `so-tay-tao-knowledge-base-v3.md` — kiểm bằng số liệu (20 khối `MODULE` vs 21 file nguồn Human thật) xác nhận đây là code chết, dời vào `audit/archive/` bằng `git mv`. `so-tay-tao-knowledge-base.html` (31MB, tăng dần mỗi lần build) — gỡ khỏi git, giữ nguyên trên đĩa.

**4. `gioi-thieu-knowledge-base-va-agent.html` sửa nhiều đợt theo phản hồi người dùng (DEC-067/068/070):**
- Sắp xếp lại 12 mục thành 5 phần theo mục đích (Vì sao cần → KB/Agent là gì → Có lợi thế nào → Đang có gì → Xây tiếp thế nào).
- Chuyển mục lục từ thanh ngang sang cột trái cố định.
- Phát hiện và sửa 1 ảnh nằm lạc từ trước (ảnh "chat hiện được hình" nằm sai trong mục An toàn, chuyển đúng về mục Knowledge Base là gì).
- Thay 8 ảnh bằng bản người dùng crop lại (`case1-bang-doi-chieu`, `case2-trace-lay-tai-lieu-anh`, `case3-tu-choi`, `image-01/02/08/26/27/29/33`) — xác định từng cặp bằng cách đọc nội dung, không suy đoán theo tên (file không có manifest nối ảnh nhúng với nguồn).
- Sửa số liệu cũ (20→21 tài liệu, bỏ mục đã xong khỏi "đang làm tiếp").

**5. Tính năng nền tảng mới ghi nhận — "Thêm vào tri thức" (viết vào `KB-11-chat-kiem-thu-va-bao-tri.md`).** Nút `+` dưới câu trả lời chat lưu thành tài liệu Markdown vào kho tri thức bất kỳ. Hai điểm dễ hiểu lầm: (a) nội dung lưu là **câu trả lời của trợ lý**, không phải nguyên văn người dùng gõ; (b) `Lưu nháp` khác `Xuất bản` — nháp không vào chỉ mục, trợ lý chưa tra được. Không có bước duyệt bắt buộc giữa hai nút này — rủi ro thật với kho sự thật đã chốt.

**6. Đính chính quan trọng DEC-052 → DEC-069.** DEC-052 từng ghi "đồng bộ Drive làm chết URI ảnh" theo cách đọc sai là *mọi* lần đồng bộ. Kiểm lại bằng dữ liệu thật (người dùng crop 23 ảnh + thêm 3 ảnh mới, đồng bộ, đọc qua MCP `list_documents`): **chỉ 26 ảnh thay đổi/mới chuyển sang xử lý lại; 26 ảnh không đổi giữ nguyên `parse_status: completed` VÀ giữ nguyên URI y hệt** (đối chiếu khớp tuyệt đối với `image-map.json` đang có). Nguyên nhân chết URI 49/49 ngày 11/08 thực ra là **di trú giữa hai KB khác nhau** (DEC-043), không phải bản chất của đồng bộ trong cùng KB. Sửa quy tắc vận hành: từ nay chỉ cần lấy URI cho đúng tập ảnh vừa đổi trạng thái, không cần rà lại toàn bộ.

**7. Việc treo cuối phiên — hàng đợi xử lý ảnh có dấu hiệu tắc.** 26/52 ảnh (23 crop lại + 3 mới) đứng ở `pending`/`processing`/`finalizing` **0 tiến triển sau 25 phút** theo dõi qua MCP (2 lần kiểm, cách 20 phút, số liệu y hệt). Đã đề nghị người dùng tự kiểm trên Web, chưa có phản hồi khi dừng phiên. Xem `HANDOFF.md` mục 4.9 để biết việc cần làm tiếp khi vào lại.

**Gate cuối phiên:** `Ran 30 tests` — **1 FAIL đã biết** (`test_project_image_map_covers_all_merged_assets`, chờ URI 3 ảnh mới). Đây là tín hiệu đúng, không phải lỗi — sẽ tự hết khi ảnh xử lý xong và `image-map.json` được viết lại.

## Snapshot trước đó — phiên 4 (17/08/2026, gắn kho tạm, bật công cụ truy hồi, chat-test thật, dựng case study)

## MỚI 17/08/2026 (phiên 4, tiếp) — chat-test thật và case study, DEC-061/062

**Đối chiếu số tài liệu Web vs local: khớp 100%.** Kiểm cả 10 KB: `GS9 Knowledge VNG AI` 69, `Plan Version` 41, `Knowledge Agent` 8, `Data Daily` 8, `Item Profile` 8, `PUM` 7, `Glossary` 3, `Sentiment` 1, `CS FAQ` 1, `Kho Dữ Liệu Tổng Hợp` 101. Người dùng đã đồng bộ đủ. Hai thay đổi so với tài liệu cũ: KB `GS9 Knowledge VNG - Image Assets` **không còn trong danh sách** (đã gỡ), và `Kho Dữ Liệu Tổng Hợp` tăng từ 16 (audit 14/08) lên **101**.

**Phát hiện chặn đường — gắn KB thôi chưa đủ (DEC-061).** Chat-test lượt đầu của `Player Communications` thất bại với `tool not found: search_knowledge_base (available: ask_user, thinking, todo_write)`. Công cụ truy hồi là tập cấu hình **riêng**, trước đây bị mờ vì Agent chưa có KB, sau khi bind mới bật được nhưng **không tự bật**. Đã bật `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` cho 3 Agent (Player Communications 3→5 tool, Economy Offer Analyst 3→5, GM Policy Advisor 2→4); `CS Copilot` chế độ Trả lời nhanh không có tab Công cụ. **Quy tắc mới: dựng Agent phải kiểm bước "đã bật công cụ truy hồi chưa".**

**Chat-test 3 Agent trên KB an toàn (DEC-062), bằng chứng `audit/agent-chat-test-2026-08-17.md`:**

| Agent | Kết quả | Ghi chú |
|---|---|---|
| `Player Communications` × Plan Version | **Đạt** | 31 bước/5m24s, 5 tính năng V5 khớp nguồn, ảnh render thật, tự để trống ô nguồn ở 2/5 khẳng định thiếu bằng chứng |
| `Knowledge Curator` × 2 kho | **Có điều kiện** | Từ chối bịa điều khoản xử phạt (đúng), nhưng khẳng định sai "chỉ có 6 Agent mặc định" và liệt kê KB đã bị gỡ |
| `CS Copilot` × Knowledge VNG AI | **Đạt về guardrail** | Từ chối trả lời vì kho không phải nguồn CS được duyệt — bằng chứng kho tạm không thay được kho đúng |

**Gate 4.2 mở một phần** — lần đầu có Agent đạt chat-test đầy đủ. 13/16 Agent vẫn *Bị chặn–Chưa xác định*. Ba Agent gắn KB nhạy cảm (PUM, Sentiment, Kho Tổng Hợp) chưa test vì giới hạn phạm vi ở KB an toàn.

**File thuyết trình `gioi-thieu-knowledge-base-va-agent.html` nâng từ 10 lên 12 mục:**
- Mục 08 vá bảng binding theo trạng thái mới, thêm cảnh báo 4 Agent đang dùng kho tạm.
- **Mục 09 mới — Case study**, 3 case thật kèm 3 ảnh Plan V5 nhúng base64, giữ nguyên cả phần lỗi vì đó là lập luận cho việc dựng đủ kho.
- **Mục 10 mới — Đề xuất cấu trúc**, hai phương án đặt cạnh nhau (A chia theo mức nhạy cảm/nhịp cập nhật, B chia theo 4 nhóm công việc) kèm đánh đổi từng bên, bảng 4 kho cần dựng và ai phải cung cấp gì, gợi ý thứ tự làm, 4 câu hỏi để team chốt.
- **Sửa lỗi tồn tại từ trước:** 10 ảnh cũ có `loading="lazy"` nên **không render khi in PDF**. Đã bỏ lazy toàn bộ — nay 13/13 ảnh tải, kiểm chứng bằng trình duyệt.
- Vá số đếm KB lệch trong mục 06 (`~97`→`101`, Item Profile `7`→`8`). File 0,44 → 0,66 MB.

**Nguồn Human đã vá:** `KBCFL-10-cac-kho-tri-thuc-cua-cfl.md` cập nhật số đếm 10 kho theo Web, bổ sung mục `GS9 Knowledge VNG AI` kèm cảnh báo đây không phải kho nghiệp vụ. Rebuild sinh lại `doc-02` và `doc-10` trong meta-KB.

## ⚠️ NGHI VẤN CHƯA KẾT LUẬN — ảnh minh hoạ có thể đang thành nguồn dữ kiện sai (ưu tiên kiểm lại)

Phát sinh cuối phiên 4, **chưa chốt nguyên nhân, phải test lại**. Chi tiết đầy đủ ở `audit/agent-chat-test-2026-08-17.md` mục 6.

**Hiện tượng.** `Knowledge Curator` khẳng định ba thứ sai: hệ thống "chỉ có 6 trợ lý mặc định, không có agent nào tên CFL"; tồn tại kho `Knowledge VNG - Image Assets`; có nguồn `Drive CFL Viax` sync mỗi 15 phút. Cả ba khớp gần như từng ký tự với nội dung nhìn thấy trong 3 ảnh nằm trong `GS9 Knowledge VNG AI`: `image-26-agent-tong-quan-danh-sach.png`, `image-41-agent-test-kb-da-nguon.png`, `image-25-google-drive-dong-bo-thanh-cong.png`.

**Đã kiểm chứng (truy vấn thẳng chỉ mục bằng `keyword_search`):** nền tảng OCR nội dung ảnh **và** sinh mô tả ảnh **ngay lúc nạp**, lưu thành chunk văn bản tra cứu được. Có thật hai chunk từ `image-25`: `chunk_type: "image_caption"` ghi *"a connected data source: 'Drive CFL Viax' (Google Drive)… every 15 minutes… status 'Thành công'"*, và `chunk_type: "text"` do OCR. Chuỗi này còn nằm ở `image-15` và `image-33`.

**BẰNG CHỨNG MỚI cuối phiên:** trace lượt chạy lại ghi rõ bước **`Lấy tài liệu: image-01-tong-quan-danh-sach-knowledge.png`** — Agent chủ động truy hồi **một tài liệu ảnh** làm nguồn, gọi đích danh tên tệp. Ảnh: `docs KB/Asset/chat/case2-trace-lay-tai-lieu-anh.png`. Mệnh đề "ảnh trong kho được truy hồi làm nguồn và nội dung trong ảnh trở thành dữ kiện" nay **Đã kiểm chứng**. Lượt này dùng model `deepseek-v4-flash`, khác lượt trước.

**Vẫn chưa kết luận:**
- Chưa chứng minh câu trả lời sai **lấy đúng** từ các chunk đó. Trùng chuỗi rất mạnh nhưng không có trace chỉ đích danh chunk.
- **KB chưa phân tích xong** các tệp mới sync tại thời điểm test → trạng thái còn biến động, kết quả có thể khác khi xử lý xong.
- Chưa loại trừ giả thuyết Agent bịa, hoặc giữ lại thông tin cũ từ ngữ cảnh khác.

**Lời Agent tự nhận KHÔNG dùng làm bằng chứng.** Khi bị hỏi vặn "có phải bạn tự chế ra không", nó quay ra nhận đã bịa toàn bộ và nói `GS9 CFL PUM`, `GS9 CFL Data Daily`, `GS9 CFL Item Profile` "không hề tồn tại", `GS9 CFL Knowledge Agent` "rỗng 0 tài liệu" — **cả bốn đều sai**, thực tế lần lượt 7, 8, 8, 8 tài liệu. Nó nhận bừa theo hướng câu hỏi gợi ý. Không tin lời Agent tự mô tả về chính nó theo cả hai chiều; kiểm bằng API/UI.

**Đã vá tạm:** gắn dòng cảnh báo "ảnh chụp một thời điểm, không phải danh mục hiện hành" cạnh 7 ảnh mang danh sách trong nguồn Human (`Agent-13` ×1, `Agent-16` ×3, `KB-08` ×2, `KB-12` ×1).

**Vá tạm không giải quyết gốc** — không thể chụp lại ảnh mỗi lần hệ thống đổi, trong khi ảnh chỉ để minh hoạ giao diện. Hướng người dùng đề xuất, **cần thử ở phiên sau**:
1. **Tắt VLM / đọc ảnh ở KB thuần hướng dẫn** (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`). Chưa biết nền tảng có cho tắt riêng từng KB không, và tắt rồi ảnh có còn hiện trong câu trả lời không.
2. **Giữ VLM ở KB nghiệp vụ** như `GS9 CFL Plan Version` — ở đó nội dung trong ảnh chính là thứ cần tra, Case 1 chứng minh chạy tốt.
3. Che phần danh sách khi chụp ảnh minh hoạ.

**Cách test lại:** đợi KB xử lý xong toàn bộ tệp → chạy lại đúng câu hỏi Case 2 → nếu vẫn sai thì tắt VLM một KB hướng dẫn → chạy lại lần nữa → so ba kết quả.

**Không đưa nghi vấn này vào `gioi-thieu-knowledge-base-va-agent.html`** — file đó để present cho team, chỉ chứa kết luận đã chốt.

**Việc phát sinh còn mở khác:** lỗi truy hồi của `Knowledge Curator` (kho có nội dung nhưng lấy nhầm đoạn) — thử tăng Top K hoặc bật `Thông tin tài liệu` rồi test lại; truy hồi bỏ sót 2 ảnh có thật trong kho ở case 1; `CS Copilot` không render thân câu trả lời.

## Snapshot trước đó trong cùng ngày — phiên 4, phần đầu

## MỚI 17/08/2026 (phiên 4) — gắn kho tạm cho 4 Agent, DEC-060

**Bốn Agent custom cuối cùng nay đã có KB.** Trước phiên này `CS Copilot`, `Economy Offer Analyst`, `GM Policy Advisor`, `Player Communications` đều ở `kb_selection_mode: none`. Đã kiểm tra và xác định nguyên nhân gốc **không phải thiếu quyền mà là thiếu nội dung**: bốn KB nghiệp vụ đúng cho từng vai trò chưa có nội dung hoặc chưa tồn tại. Người dùng quyết định hoãn việc soạn nội dung, gắn tạm kho gần đúng nhất, phần thiếu ghi lại chuẩn bị sau.

| Agent | Kho tạm đã gắn | KB đúng còn thiếu |
|---|---|---|
| `GS9 CFL Player Communications` | `GS9 CFL Plan Version` | `GS9 CFL Event Calendar & Brief` |
| `GS9 CFL Economy Offer Analyst` | `GS9 CFL Data Daily` | `GS9 CFL Item Catalog` (phải tách khỏi Item Profile, có dữ liệu P0) |
| `GS9 CFL CS Copilot` | `GS9 Knowledge VNG AI` (fallback) | `GS9 CFL CS FAQ & Policy` (mới có file định dạng) |
| `GS9 CFL GM Policy Advisor` | `GS9 Knowledge VNG AI` (fallback) | `GS9 CFL GM Policy & Sanction` (chưa tồn tại) |

**Cách làm:** mở dialog cấu hình từng Agent trên Web bằng `claude-in-chrome`, tab `Kho tri thức`, đổi từ `Không dùng kho tri thức` sang `Kho tri thức đã chọn`, chọn đúng một KB, `Lưu`. Cả 4 lần đều nhận toast `Đã cập nhật trợ lý`. **Sau đó mở lại cả 4 dialog đọc trực tiếp để xác minh** — không tin toast. Không đụng mode chạy, model, tool, prompt hay chia sẻ. Agent ID đọc được: `Player Communications` = `4b8e6d78-9217-4dbb-8ab3-919628a48440`.

**Kho tạm không đóng được lý do chặn ban đầu ở DEC-058.** `CS Copilot` và `GM Policy Advisor` đang trỏ kho hướng dẫn nền tảng, hoàn toàn không chứa chính sách CS hay điều khoản xử phạt — câu trả lời của chúng về hai mảng đó vẫn không có nguồn CFL bảo chứng. Chất lượng runtime của cả 4 vẫn **Bị chặn–Chưa xác định** vì chưa chat-test.

**Đã cập nhật:** `audit/agent-kb-binding-4-agent-2026-08-17.md` (bằng chứng), `DECISIONS.md` (DEC-060), `docs KB/Human/AgentCFL-02-ma-tran-so-sanh-16-agent.md` (bảng ai gắn kho nào + bảng kho tạm/kho đúng), `docs KB/Dev/Agent-ho-so-16-agent-cfl.md` (3 chỗ: bảng binding Web actual, bảng hồ sơ 10 Agent, mục 3.5 lý do chặn). Gate: strict build ra 20 module + 8 doc KB Agent, `Ran 30 tests`/`OK` (6 skip), `link_plan_v5_minio.py --check` = 0 thay đổi.

**Cạm bẫy kỹ thuật mới ghi nhận (chi tiết trong audit):** toạ độ ảnh chụp trình duyệt không khớp toạ độ click — viewport thật `2080x1032` nhưng ảnh trả về `1568x778`, phải nhân `1.3265`, không nhân thì mở nhầm Agent khác. Phím `Escape` đóng cả dialog và mất thay đổi chưa lưu, muốn đóng dropdown phải click vùng trống trong dialog.

## Snapshot trước đó — 17/08/2026 (phiên 3, tiếp)

**Phiên bản khi đó:** 3.4.1
**Giai đoạn:** Nguồn nội dung đã tách ba tầng (DEC-053): `docs KB/Dev` (25 file, không lên Web) → `docs KB/Human` (29 file, nguồn build) → `knowledge/` (bản sinh, lên Web). `build_handbook.py` sinh 2 KB: `GS9 Knowledge VNG AI` (20 doc + 49 ảnh) và `GS9 CFL Knowledge Agent` (8 doc — 5 về Agent CFL, 3 về KB CFL). Toàn bộ URI ảnh đã vá: 49 ảnh sổ tay (DEC-052) và 29 ảnh Plan V5 (DEC-057). **Chat-test ảnh ĐẠT** — ảnh render thật trong câu trả lời. Đã chèn luật trích dẫn ảnh vào System Prompt của 10/10 Agent custom (DEC-056). Bảng ai gắn kho nào đã bổ sung cho cả bản Human và Dev; hai binding rủi ro (Incident Triage → PUM, Player Voice Analyst → Sentiment) đã được người dùng xác nhận giữ nguyên vì nền tảng chỉ dùng nội bộ (DEC-058). `Ran 30 tests`/`OK`.

**Sự cố Google Drive ngày 17/08/2026 (DEC-059) — đã khôi phục hoàn toàn, không mất dữ liệu đã commit.** Drive mất kết nối rồi tự "Restore" ra một layout trộn cấu trúc cũ (trước 15/08) chồng lên cấu trúc mới, làm thư mục `knowledge` thật bị đẩy thành `knowledge (1)`, `.git` hỏng mất lịch sử. Khôi phục bằng cách: clone bản sạch từ GitHub ra ngoài Drive để đối chiếu, đổi tên `knowledge (1)` → `knowledge` (giữ nguyên ID nên **không mất kết nối Web**), thay `.git` hỏng bằng bản sạch, `git restore` + `git clean` dọn file cũ chui vào. Rà soát kỹ toàn bộ cây thư mục sau đó, xoá 6 thư mục rác Drive để lại (`V5/assets`, `V5/assets (1)`, `docs KB/Dev/Agent`, `docs KB/Dev/KB`, `docs KB/Asset/New folder`, `knowledge/Test`). Xác nhận cuối: `git diff --stat origin/main HEAD` rỗng tuyệt đối, `Ran 30 tests OK`. Bài học ghi vào memory hệ thống: ghi file phải qua file tạm rồi `os.replace`, không ghi đè trực tiếp khi làm việc trên Drive.

**Đã bổ sung ảnh minh họa vào file thuyết trình** `gioi-thieu-knowledge-base-va-agent.html` — 10 ảnh chụp màn hình thật, nén và nhúng base64 (0,43 MB), có lightbox phóng to khi bấm.

**Đã commit lên GitHub trong phiên này.**

## MỚI 16/08/2026 (phiên 3, mới nhất) — tách nội dung Dev/Human và vá URI ảnh

### Việc đã xong

1. **Kết thúc test đồng bộ KB `Test`** (việc treo từ phiên 2). Ba vòng: Toàn bộ lần đầu → Tăng dần có sửa nội dung → Toàn bộ có thêm file mới. Kết luận: ảnh giữ nguyên ở cả hai chế độ, miễn không đụng dòng chứa URI. **DEC-051** xác nhận DEC-043 (gộp ảnh + tài liệu chung một KB) là đúng. Phát hiện phụ: cả hai chế độ đều **chỉ nạp lại tệp thực sự thay đổi** — đây là lý do chạy Toàn bộ + Ghi đè khi không sửa gì thì không thấy hiệu lực.
2. **Vá toàn bộ URI ảnh chết (DEC-052).** `image-map.json` sinh 11/08 có 49/49 URI đã chết sau khi ảnh re-sync qua Drive connector. Kiểm chứng dạng `file_path` render được (thử trên `doc-02`, người dùng xác nhận ảnh hiện), rồi lấy tự động 49 URI mới qua MCP, viết lại map, build lại. Giải quyết điểm treo của DEC-045.
3. **Tách nội dung theo đối tượng đọc (DEC-053).** 20 file `docs KB/Dev` + 20 file `docs KB/Human`, kèm hai file quy ước biên tập. Builder đọc nguồn mới, map tên sang `doc-`.
4. **Bundle Plan V5 sang bố cục ảnh phẳng (DEC-054).** Sửa cả converter, linker, test và 29 dòng `LOCAL_ASSET`. Trước đó ba thành phần lệch pha, chạy lại converter sẽ sinh hai bộ 29 ảnh trùng tên.
5. **`Item Profile` đổi 7 CSV sang quy ước `doc-` (DEC-055)** — chỉ đổi tên, không mở nội dung, giữ boundary P0.
6. **Vá lỗ hổng `.gitignore`:** `keys KB/` không được che, một lệnh `git add -A` là service-account key vào repo. Đã thêm `/keys KB/` và `**/keys/`; xác nhận key chưa từng bị commit.
7. Soạn đoạn prompt buộc Agent trích dẫn ảnh — `docs KB/Dev/Agent-prompt-trich-dan-hinh-anh.md`, **chưa dán lên Agent nào**.

### Việc còn mở

1. **Tách `knowledge/GS9 CFL Knowledge Agent`** (28 file) — đang làm dở. 5 file sang Human, 23 file sang Dev.
2. **Chat-test thật** trên `GS9 Knowledge VNG AI` sau khi sync — mới xác nhận ảnh hiện ở mức xem trước tài liệu, chưa qua chat.
3. **Xoá tài liệu tên cũ trên Web:** `doc-13-agent-tong-quan-va-kien-truc.md` (đã đổi thành `doc-13-tong-quan-va-kien-truc.md`), nếu không sẽ có hai bản trùng nội dung.
4. **Dán prompt trích dẫn ảnh cho 10 Agent custom** — người dùng đã đồng ý cho agent tự thao tác trên Web.
5. **Rủi ro chưa xử:** KB `PUM` và `Sentiment Feedback User` bị đánh dấu rủi ro dữ liệu cá nhân nhưng **cùng ngày đã được bind** cho `Incident Triage` và `Player Voice Analyst`, không có bước phê duyệt nào được ghi lại.

## CŨ 15/08/2026 (phiên 2) — test đồng bộ tăng dần KB `Test`, đã kết thúc, xem DEC-051

**Việc đang mở, ưu tiên cao nhất khi vào phiên mới:** kiểm chứng xem gộp ảnh + tài liệu chung một KB (kiến trúc đã chọn, DEC-043) có an toàn khi sync tăng dần hay không. Toàn bộ tiến trình và mốc so sánh ghi tại `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`.

**Đã làm (vòng 1 — sync Toàn bộ):**
1. Tạo `knowledge/Test/` với `C.png`, `D.png`, `a.md` (tham chiếu C), `b.md` (tham chiếu D).
2. Người dùng cấu hình connector: **Toàn bộ + Ghi đè + Mọi tệp**, sync lần 1 — cả 4 file `Hoàn tất`. KB ID: `d7295a59-03b1-496c-86eb-9ecaa3364aa7`.
3. **Phát hiện quan trọng: Google Drive connector KHÔNG tự resolve link ảnh tương đối trong Markdown.** Sau sync, nội dung `b.md` vẫn còn nguyên `![Ảnh test D](D.png)` — không tự đổi thành `minio://...`. Nghĩa là quy trình gắn URI thủ công (kiểu `link_plan_v5_minio.py`) vẫn bắt buộc cho Phase 3 thật; connector không tự làm thay.
4. Lấy ID tài liệu nội bộ (`knowledge_id`) làm mốc so sánh (không phải URI, vì D.png không lộ URI qua caption — chỉ C.png lộ do model caption tự chèn markdown):
   - `C.png` → `aa308f81-fa83-4098-bac0-235c0fbe5ec9`
   - `D.png` → `2852c79a-e3c0-4393-ae78-16db25650541`
   - `a.md` → `4b48546d-6fd4-4ee9-bbb8-19362fd17c53`
   - `b.md` → `136f2601-cf49-4898-99d5-bb8b8f1bb7e8`
5. **Người dùng tự lấy được URI thật** qua UI và nhúng vào cả 2 file:
   - `a.md` → `minio://knowledge-base-prd/10012/exports/13b88b2e-a43d-485a-b255-173d37a476cf.png` (ảnh C)
   - `b.md` → `minio://knowledge-base-prd/10012/exports/9aa0a0d8-0905-43ef-b7d1-7da9f23f1c68.png` (ảnh D)
6. Agent đã sửa phần văn xuôi của cả `a.md` (giữ nguyên, dùng làm **nhóm đối chứng**) và `b.md` (sửa nội dung xung quanh, dùng làm **nhóm thử nghiệm**) — cả hai **không đụng dòng ảnh**.

**Đang chờ (vòng 2 — sync Tăng dần):** người dùng sẽ chuyển "Chế độ đồng bộ" sang **Tăng dần** và sync lại. Khi có kết quả, agent cần:
1. Mở lại `a.md`/`b.md`/`C.png`/`D.png`, so `knowledge_id` với bảng trên — đổi hay giữ nguyên.
2. Xác nhận ảnh C (nhóm đối chứng) và ảnh D (nhóm thử nghiệm, nội dung xung quanh đã đổi) còn hiển thị đúng không.
3. Kiểm tra `e.md` (nếu người dùng đã thêm) xuất hiện với `knowledge_id` mới.
4. **Kết luận và chốt kiến trúc:** nếu ảnh vẫn giữ nguyên sau khi sửa nội dung xung quanh (dù chung KB) → giữ kiến trúc gộp (DEC-043 đúng). Nếu ảnh bị mất/đổi URI khi tài liệu khác trong cùng KB được sync lại → cần xem xét tách ảnh ra KB riêng (rollback DEC-043), ảnh hưởng cả `GS9 Knowledge VNG AI` (đã gộp) và Phase 3 nói chung.
5. Ghi kết quả thành DEC mới, cập nhật `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` phần Phase 3 cho phù hợp.

**Việc khác đang mở song song:** dựa vào 3 KB đã có số liệu khớp local (xem trên), rất có thể người dùng đã tự chạy Phase 3 thật cho `GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`, `GS9 CFL Plan Version` — cần hỏi lại và xác minh (chưa chat-test, chưa kiểm tra URI ảnh trong 20 module có còn đúng không sau sync).

## MỚI 15/08/2026 (phiên 2, tiếp) — xác minh Web actual 10 custom Agent sau khi người dùng chỉnh

Người dùng tự thực hiện 4 mutation live trên Web cho cả 10 custom Agent (đổi tên `GS9 CFL`, bật reranker, bật tải ảnh + VLM, share space `CFL Member` quyền `Được chỉnh sửa`). Agent xác minh read-only bằng trình duyệt, **mở dialog từng Agent và đọc trực tiếp** — không suy từ lời kể. Ghi DEC-049, DEC-050.

**Đã xác minh (Đã kiểm chứng, 15/08/2026):**

- **10/10 Agent ID khớp** hồ sơ local; **10/10 tên đã đổi** sang tiền tố `GS9 CFL`.
- **9 Agent mode `Suy luận thông minh`, preset `Loại trợ lý` = `Hỏi đáp RAG`.** `GS9 CFL CS Copilot` mode `Trả lời nhanh` — **không có control `Loại trợ lý`**, đồng thời có thêm tab `Hội thoại` và trường `Mẫu ngữ cảnh` mà Agent Smart không có.
- **`Prompt theo intent` để trống ở cả 10** (`Chọn intent`, dùng template mặc định) — kiểm mẫu trực tiếp trên Economy Offer Analyst và CS Copilot.
- Reranker `bge-reranker-v2-m3`, `Chế độ suy nghĩ` **Bật**, tải ảnh **Bật** + VLM `qwen3.6-plus`, audio Off — đọc trực tiếp trên CS Copilot và Knowledge Curator; 8 Agent còn lại ghi là *suy ra* trong `config.md`.
- Chia sẻ: space `CFL Member` quyền **Được chỉnh sửa** (đọc trực tiếp trên CS Copilot; sidebar `SPACES · CFL Member 10` xác nhận đủ 10).
- Bind KB và tool giữ nguyên như 14/08: 6/10 đã bind (Curator 2 KB/6 tool; Incident 1/5; KPI 1/6; Player Voice 1/4; LiveOps 1/6; Release 1/5), 4/10 chưa bind (Economy 3 tool, Communications 3, GM 2, CS Copilot 0).

**Phát hiện ngoài khai báo:** `Chế độ suy nghĩ` đang **Bật** — trái baseline `Thinking Off` ghi từ 14/08. Không tự tắt; ghi DEC-050 và cần người dùng xác nhận có chủ đích hay không.

**Lỗi đã sửa trong lượt này:** ban đầu 3 Agent (Incident Triage, KPI Experiment Analyst, Economy Offer Analyst) chưa đổi tên; người dùng đã đổi nốt. Danh sách Agent trên UI **cache tên cũ** — phải mở dialog mới thấy tên thật.

**Đã cập nhật local:** 10 file `agent/GS9 CFL .../config.md` (khối `Web actual` → 15/08/2026, phân biệt rõ *đọc trực tiếp* và *suy ra*), `agent/liveops-custom-agent-catalog.md` (bảng trạng thái, ma trận tool, xoá tên `GM Case Investigator` cuối cùng). **Nợ DEC-034 về khối `Web actual` sai đã xử lý xong.**

## MỚI 15/08/2026 (phiên 2, tiếp nữa) — folder Plan Version đổi tên tay + đổi tên 10 custom Agent local

1. **Người dùng tự đổi tên folder** `knowledge/GS9 Plan Version/` → `knowledge/GS9 CFL Plan Version/` (khớp đúng tên KB Web). Phát hiện phụ: thư mục con `assets/` (29 JPEG) bị **làm phẳng** ra ngoài `V5/` trong quá trình đổi tên — đã khôi phục lại `V5/assets/`. Đã sửa mọi path cứng trong `scripts/link_plan_v5_minio.py`, `tests/test_link_plan_v5_minio.py`, `scripts/convert_cfl_plan_html.py` (+ `bundle_name` trong `source-manifest.json` đã sinh) và toàn bộ tài liệu sống (`STATUS.md`, `HANDOFF.md`, `PROJECT.md`, `DECISIONS.md`, `NEXT_SESSION_PROMPT.md`, `knowledge/README.md`, kế hoạch Phase 3). Không đụng `audit/*.md` và kế hoạch cũ 14/08 (lịch sử). Gate: strict build PASS, `Ran 29 tests OK`, `link_plan_v5_minio.py --check` idempotent.
2. **DEC-048 — đổi tên local 10 custom Agent** từ `GS9 ...` sang `GS9 CFL ...` (khớp quy ước tên KB), theo yêu cầu người dùng. Đổi: 10 folder `agent/GS9 CFL <Agent>/`, 10 hồ sơ meta-KB (`doc-20`→`doc-29`, `doc-27`), catalog/README trong `agent/`, và mọi tài liệu sống nhắc tên đầy đủ có tiền tố `GS9`. **Không đổi:** `audit/*.md`, `agent/kb-allowlist-proposal-2026-08-14.md` (lịch sử); các chỗ chỉ dùng tên rút gọn không tiền tố (`doc-02`, `doc-03`, bản đồ kiến trúc mục 9-10) vì không mang tiền tố cần đổi. **Người dùng tự đổi tên thật trên Web** — đây chỉ là đổi tên local. `GS9 GM Policy Advisor` giữ nguyên (không hoàn tác DEC-039, người dùng xác nhận bỏ qua ý định revert). Link chết cũ (4 file trỏ `27-custom-gs9-gm-case-investigator.md`) vẫn còn, chưa nằm trong phạm vi việc này.
3. **Đã tạo `knowledge/Test/`** — bộ test tay để kiểm chứng hành vi "Tăng dần" (Incremental) của Google Drive connector: `a.md`↔`C.png`, `b.md`↔`D.png`. Người dùng đang tự cấu hình connector Web (đã xác nhận: Toàn bộ + Ghi đè + Mọi tệp cho lượt sync đầu). Việc mở: sync lần 1 xong → agent lấy URI 4 file làm mốc → người dùng thêm `e.md` + sửa `b.md` (không đụng link ảnh) → chuyển "Tăng dần" → so URI `a.md`/`C.png`/`D.png` có đổi không.

## MỚI 15/08/2026 (phiên 2) — Phase 1+2 tái cấu trúc đã thực thi cục bộ

Kế hoạch: `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` — Phase 1 (đổi tên) và Phase 2 (gộp ảnh + soạn 3 file cấu trúc CFL) **đã xong**. Phase 3 (Google Drive connector sync lên Web) **chưa làm**, chờ go-ahead riêng vì hành vi đổi tên khi sync chưa từng được kiểm chứng.

Quyết định người dùng chốt đầu phiên: quy ước Plan Version dùng `doc-v5-NN-...`/`image-v5-NN-...` (chống trùng tên khi V6 lên); thực thi luôn cả Phase 2.2 (soạn 3 file cấu trúc CFL), không hoãn.

1. **Hash-check bảo toàn nội dung — PASS.** Tính hash chuẩn hóa (bỏ `LOCAL_ASSET` + URI minio) cho 20 module + 25 file meta-KB (khi đó) + 12 Markdown Plan V5 **trước khi đổi tên**. Sau khi đổi tên xong, chạy lại: 34/57 file khớp hash tuyệt đối (không cross-link); 23/57 file lệch hash nhưng **toàn bộ đã xác minh chỉ do đổi target link nội bộ (nhãn = tên file) và 2 bổ sung có chủ đích** (thêm mục lục 3 file mới vào `doc-00`, cập nhật số đếm trong `doc-91`) — đã diff từng file so với bản gốc git HEAD để xác nhận không có câu chữ/tiêu đề/bảng nào khác bị đổi.
2. **20 module sổ tay + 49 PNG đã gộp và đổi tên.** Marker `MODULE` trong master đổi `NN-...md` → `doc-NN-...md`; 20 tên cũ thêm vào `LEGACY_GENERATED_MODULE_NAMES` để builder tự dọn. 49 PNG chuyển từ `GS9 Knowledge VNG - Image Assets/` sang cùng thư mục `GS9 Knowledge VNG AI/`, đổi tên `image-NN-...png`. `build_handbook.py` viết lại: bỏ `ASSET_KB_NAME`/asset-dir riêng, `local_asset_prefix` đổi thành `.` (cùng thư mục). 60 link MinIO + 60 `LOCAL_ASSET: ./image-...` — strict build PASS.
3. **25 file meta-KB Agent đổi tên `doc-NN-...`.** Sửa 21/25 file có cross-link nội bộ (chỉ đổi target, giữ nguyên nhãn hiển thị). **Phát hiện lỗi cũ:** 4 file (`doc-00`, `doc-01`, `doc-02`, `doc-26`) vẫn còn link chết trỏ `27-custom-gs9-gm-case-investigator.md` — tên này đã không tồn tại từ lần đổi vai trò GM 15/08 (phiên 1) sang `GM Policy Advisor`, chỉ 4 file này chưa được cập nhật khi đó. **Chưa sửa trong phiên này** vì sửa nhãn "GM Case Investigator" → "GM Policy Advisor" là đổi nội dung/prose, ngoài phạm vi việc đổi tên thuần túy; cần một lượt sửa nội dung riêng.
4. **3 trang cấu trúc KB CFL mới đã soạn:** `doc-30-cau-truc-kb-cfl.md` (bản đồ 7 tầng dạng tra cứu), `doc-31-ban-chat-tung-kb.md` (bảng bản chất từng KB), `doc-32-quy-uoc-dat-ten-va-nhung-anh.md` (quy ước đặt tên + cú pháp ảnh, dạng tra cứu nhanh). Đã tích hợp vào mục lục `doc-00` và cập nhật số đếm file trong `doc-91`. Meta-KB local nay **28 file** (không phải 25).
5. **Plan Version 5 — 12 Markdown + 29 JPEG đổi tên `doc-v5-`/`image-v5-`.** Không rerun được `convert_cfl_plan_html.py` trên máy này (thiếu source HTML, đường dẫn thuộc máy công ty) — áp dụng đổi tên tương đương thủ công lên bundle đã sinh sẵn, giữ nguyên URI MinIO (chưa đổi vì Web chưa sync lại). `convert_cfl_plan_html.py` đã sửa (`VERSION_TAG = "v5"`) để lần sinh sau (máy có source, hoặc V6) tự sinh đúng tên. `link_plan_v5_minio.py` không cần sửa (logic không phụ thuộc tên cụ thể); chạy `--check` xác nhận idempotent, 0 thay đổi cần thiết.
6. **3 bộ test đã cập nhật, không nới lỏng assertion:** `test_build_handbook.py` (bỏ `ASSET_DIR`/`ASSET_KB_NAME`, cập nhật tên file kỳ vọng, sửa 1 collision giữa fixture test và `LEGACY_GENERATED_MODULE_NAMES` mở rộng), `test_convert_cfl_plan_html.py` (cập nhật `EXPECTED_MODULES`), `test_link_plan_v5_minio.py` (không cần sửa, đã pass nguyên trạng). Gate: `Ran 29 tests`, `OK` (skipped=6, do thiếu source HTML — không liên quan thay đổi phiên này).
7. **DEC-041 → DEC-046 đã ghi** vào `DECISIONS.md`; `AGENTS.md` và `PROJECT.md` đã cập nhật theo kiến trúc mới.
8. **Git: chưa commit** thêm gì trong phiên này; toàn bộ vẫn là thay đổi local.

## MỚI 15/08/2026 (phiên 2, tiếp) — mở rộng đổi tên sang 5 KB nữa, theo yêu cầu người dùng

Người dùng yêu cầu đổi tên "tất cả" — đã làm rõ phạm vi qua hỏi đáp và mở rộng đổi tên thêm 5 KB ngoài kế hoạch gốc:

- **`GS9 CFL PUM`** — 7 file PDF (`CFL MMR GMT 2026.01`–`.07.pdf`) → thêm tiền tố `doc-`, giữ nguyên phần tên còn lại (không slugify). `desktop.ini` (file hệ thống Windows) **không đổi**.
- **`GS9 CFL Data Daily`** — 8 file XLSX (`CFL_MMYYYY.xlsx`) → thêm tiền tố `doc-`. Local mirror vẫn thiếu `doc-CFL_082026.xlsx` như trước (G4 chưa xử lý, không liên quan việc đổi tên).
- **`GS9 CFL Sentiment Feedback User`** — 1 file XLSX → thêm tiền tố `doc-`.
- **`GS9 CFL Glossary & Systems`** — 3 file `.md` → thêm tiền tố `doc-` (KB nháp, chưa có nội dung đầy đủ, chưa upload Web).
- **`GS9 CFL CS FAQ & Policy`** — 1 file format `.md` → thêm tiền tố `doc-`.

**Quyết định người dùng về rủi ro Google Drive:** người dùng xác nhận thư mục các KB này đang liên kết với Google Drive và **chủ động chấp nhận** việc đổi tên sẽ khiến Google Drive tự đồng bộ đổi tên tương ứng — khác với cách tiếp cận "thử nhỏ trước" áp dụng cho Phase 3 của 3 KB chính. Đây là quyết định có ý thức của người dùng, không phải suy luận của agent.

**`GS9 CFL Item Profile` loại trừ hoàn toàn** — không mở, không đọc, không đổi tên bất kỳ file nào, giữ đúng boundary P0.

**`GS9 CFL Kho Dữ Liệu Tổng Hợp`** không có thư mục local (KB dẫn xuất, không có mirror) — không có gì để đổi tên.

Không có cross-reference nào bị hỏng: đã kiểm tra không có file nào trong hoặc ngoài 5 KB này link tới các tên cũ trước khi đổi.

## Việc tiếp theo (Phase 3 — chưa làm, cần go-ahead riêng)

Theo `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` mục 3: đưa nội dung lên Web bằng Google Drive connector, mỗi KB trỏ đúng một thư mục con của `knowledge/` (tuyệt đối không trỏ root — có credential + dữ liệu P0). **Bắt buộc thử nhỏ 2–3 file trước** vì hành vi đổi tên khi sync chưa từng được kiểm chứng (`audit/audit-google-drive-connector-2026-08-07.md` mục 6). Sync hai lượt (ảnh trước, Markdown sau khi có URI mới). Thu URI qua MCP `list_documents` (cần KB share vào space trước — người dùng tự làm hoặc cho phép rõ).

## MỚI 15/08/2026 (cuối phiên 1) — người dùng giao 3 việc tái cấu trúc, đã có kế hoạch (ĐÃ THỰC THI Ở PHIÊN 2, xem trên)

Kế hoạch chi tiết: `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` — **ĐÃ CHỐT**, chưa thực hiện bước nào.

**Ràng buộc cứng:** chỉ đổi tên file và sửa link, **KHÔNG đổi nội dung tài liệu**. Kiểm chứng bằng hash nội dung đã chuẩn hóa (bỏ `LOCAL_ASSET` và URI) trước/sau — lệch một hash là phải hoàn tác.

**Đưa lên Web bằng Google Drive connector**, không upload tay — thư mục project nằm trong Drive. Rủi ro lớn nhất: hành vi **đổi tên khi sync CHƯA TỪNG được kiểm chứng** (`audit/audit-google-drive-connector-2026-08-07.md` mục 6). Phải thử trên 2–3 file trước khi làm 135 file. Phạm vi sync phải khoanh từng thư mục con của `knowledge/`, tuyệt đối không trỏ root vì cây thư mục chứa service-account key và dữ liệu P0.

1. **Sửa lỗi ảnh render 2 lần + ra quy tắc nhúng ảnh** — người dùng cho biết định dạng cũ `![minio://...](minio://...)` trước đây chỉ ra 1 ảnh, nay ra 2. Cần thí nghiệm tìm cú pháp đúng rồi ghi thành luật ở 4 chỗ (`AGENTS.md`, master sổ tay, template KB, `DECISIONS.md`).
2. **Gộp ảnh + tài liệu vào chung KB, đổi tên toàn bộ:** ảnh tiền tố `image-`, tài liệu không phải ảnh tiền tố `doc-`. Ngoại lệ: tài liệu đồng bộ Google Drive do người dùng tự đổi.
3. **Tái phân bổ 2 KB nền tảng:** `GS9 Knowledge VNG AI` = tri thức 2 tính năng Knowledge Base + Agent kèm ảnh của chúng, dùng chung cho cả team GS9. `GS9 CFL Knowledge Agent` = 6 Agent mặc định + Agent custom CFL + **cấu trúc/KB riêng của CFL** (phần cấu trúc CFL là nội dung MỚI, phải soạn).

**CẬP NHẬT SAU PHÉP THỬ CỦA NGƯỜI DÙNG — giả thuyết cũ đã bị bác bỏ:** người dùng chat-test một KB **chỉ chứa `.md` có link ảnh, không upload ảnh vào KB đó** — ảnh **vẫn duplicate**. Vậy nguyên nhân là **cú pháp gắn link**, KHÔNG phải việc gộp ảnh chung KB. Gate cứng ở bản kế hoạch đầu đã gỡ; việc gộp KB là an toàn.
**Chi phí URI và đường tắt vừa tìm được:** người dùng sẽ **upload lại toàn bộ**, nên mọi URI MinIO cũ sẽ chết và phải thu lại — trước đây việc này tốn ~100 lượt thao tác browser cho 29 ảnh.

**ĐÃ KIỂM CHỨNG một đường rẻ hơn nhiều:** MCP `list_documents` chạy được trên KB `GS9 Knowledge VNG AI` (`cefadf09-...`) và trả về **toàn bộ 20 tài liệu kèm `file_path: minio://...` trong MỘT lệnh**. KB `GS9 Knowledge VNG - Image Assets` trả `not found or not accessible` → xác nhận điều kiện là **KB phải được share vào space**. Nếu dùng được, phần thu URI rút từ ~250 lượt xuống 1–2 lệnh.

**CÒN PHẢI KIỂM:** `file_path` MCP trả về có dạng `minio://.../10012/<doc_id>/<uuid>.md`, **khác** dạng `minio://.../10012/exports/<uuid>.png` mà `image-map.json` đang dùng và đang chạy đúng. Chưa biết với tài liệu ảnh thì `file_path` ra dạng nào và dạng nào render được. Cách kiểm: share tạm một KB có ảnh → `list_documents` → `get_image(url=<file_path>)`.

## Ghi chú — lỗi duplicate ảnh đã bỏ khỏi phạm vi

Người dùng đã kiểm chứng và chốt: **cú pháp gắn link ảnh trong file `.md` hoàn toàn đúng**, không sai chỗ nào. Hiện tượng ảnh hiện hai lần chỉ là hành vi không ổn định của model khi soạn câu trả lời, chat lại thì bình thường.

**Hạng mục sửa lỗi này đã bỏ.** Không sửa file `.md`, không sửa `build_handbook.py` / `convert_cfl_plan_html.py` / `link_plan_v5_minio.py`, không điều tra lại. Cú pháp chuẩn giữ nguyên: `![mô tả](minio://.../exports/<uuid>.<ext>)` kèm comment `<!-- LOCAL_ASSET: ... -->`. Bằng chứng lịch sử: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

## MỚI 15/08/2026 — tóm tắt nhanh phiên này

1. **Sự cố hạ tầng đã sửa:** `.git/index` bị mất do Google Drive sync xen vào giữa lúc git ghi `index.lock`; đã phục hồi bằng `git reset` từ HEAD, không đụng file trên đĩa. 3 tiến trình `git.exe` treo đã dọn.
2. **Plan Version 5 — URI MinIO đã gắn xong:** lấy 29 URI MinIO qua deep-link + nút `Toàn văn`, kiểm chứng bằng byte-size (29/29 kích thước unique trong manifest) và MCP `get_image` (5 mẫu xác nhận trực tiếp). Ghi `knowledge/GS9 CFL Plan Version/V5/image-map.json`, chạy `link_plan_v5_minio.py` → 29 ảnh nhúng + 29 link registry (58 link) trên 7/12 file, idempotent. **Phát hiện quan trọng:** mỗi ảnh sinh 2–10 URI (MinerU tách ảnh con); quy tắc chọn là "URI đầu tiên = ảnh gốc", đã kiểm chứng không suy diễn.
3. **Người dùng đã upload 12 Markdown** lên KB Web `GS9 CFL Plan Version` — KB hiện 41 tài liệu (12 MD + 29 JPEG), đang xử lý dần. **Chưa chat-test (gate G6 vẫn mở).**
4. **Bản đồ kiến trúc KB 7 tầng đã chốt:** `docs/superpowers/specs/2026-08-15-kb-architecture-design.md`. Nguyên tắc cốt lõi: ranh giới KB vẽ theo (mức nhạy cảm × đối tượng đọc × nhịp cập nhật), không theo nguồn dữ liệu. DEC-036 đến DEC-040.
5. **Quyết định người dùng đã áp vào thiết kế:** không đổi tên KB đang chạy (chỉ ghi "bản chất" — mục 5.1); `Kho Dữ Liệu Tổng Hợp` là dẫn xuất có chủ đích để xem Wiki, không phải trùng lặp; `Data Daily` giữ dùng bình thường; PUM hạ P1→P2 nội bộ (cả team đọc doanh thu) nhưng vẫn cấm doanh thu lọt vào nội dung gửi người chơi; nhịp sự kiện LiveOps là theo tháng; hai guardrail G-A (chống trộn phiên bản) và G-B (kế hoạch nội bộ ≠ brief duyệt) đã duyệt nguyên văn.
6. **Agent GM đổi vai trò — mutation live đã thực hiện:** `GS9 GM Case Investigator` → `GS9 CFL GM Policy Advisor` (Agent ID `01d42d42-dd08-4907-9d4a-913142bc554c` không đổi). Lý do: case-scoped view không tồn tại trên nền tảng, bind KB toàn tenant để điều tra 1 vụ vi phạm least privilege. Vai trò mới: tra cứu chính sách + trích mã điều khoản, bằng chứng vụ việc qua tệp đính kèm hội thoại (không qua KB). **Tên, mô tả và System Prompt đã đổi trên Web** (2 lần lưu, toast `Đã cập nhật trợ lý` cả hai lần, Agent ID xác minh trước mỗi lần sửa). Local: đổi tên thư mục `agent/GS9 CFL GM Policy Advisor/` (4 file viết lại) + hồ sơ meta-KB `27-custom-gs9-gm-policy-advisor.md` (viết lại, meta-KB vẫn đúng 25 file).
7. **2 KB nháp mới, local-only, chưa upload Web:**
   - `GS9 CFL Glossary & Systems` — 3 file. `01-thuat-ngu-vu-khi.md` sinh từ 1.227+2.599 dòng dữ liệu item thật, phát hiện 3 lỗi dữ liệu nguồn (`Whtie`→`White` 15 dòng; phẩm chất rỗng 24 dòng; hai hệ phẩm chất `A/B/C` vs màu lẫn lộn 100 dòng). `02-thuat-ngu-he-thong-va-che-do.md` rút tên hệ thống/chế độ chơi tiếng Việt chính thức từ 146 tiêu đề Plan V5.
   - `GS9 CFL CS FAQ & Policy` — chỉ có `00-huong-dan-va-quy-uoc.md` (format). **Chưa có nội dung thật** — cần người dùng cung cấp top câu hỏi CS + câu trả lời chuẩn + ranh giới chuyển tiếp GM/kỹ thuật.
8. **Sửa 1 test bị khoá vào trạng thái tạm thời:** `test_link_plan_v5_minio.py::test_bundle_currently_has_29_embeds_and_29_registry_links` chỉ đúng trước khi chạy script gắn link; đã sửa để đếm đúng ở cả hai trạng thái (`assets/...` và `minio://...`), thêm test chặn link tương đối sót lại. `Ran 7 tests, OK`.
9. **Full test gate CHƯA chạy được trên máy nhà** — thiếu package `markdown` và `bs4` (`pip install markdown beautifulsoup4`), không liên quan thay đổi phiên này.
10. **Git: chưa commit gì.** HEAD vẫn `a2285e6`, upstream `origin/main`. Working tree có 7 file modified (3 từ phiên 14/08, đã cộng thêm 3 file agent config, README, DECISIONS/STATUS/HANDOFF của phiên này) + nhiều file mới (xem `git status --short`).

## Kết quả hiện tại

- Root chính thức: `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`.
- `knowledge/` quản lý mirror/dữ liệu của các KB trên Web; `agent/` quản lý artifact cấu hình/test/handoff của Agent.
- Tên chính thức hiện tại trên Web: `GS9 Knowledge VNG AI`, `GS9 Knowledge VNG - Image Assets` và `GS9 CFL Knowledge Agent`; giữ nguyên chính xác tên trên Web (chưa Phase 3 sync).
- **Local đã tái cấu trúc 15/08/2026 (phiên 2, DEC-043/044):** `GS9 Knowledge VNG AI/` nay chứa 20 Markdown `doc-00`→`doc-19` **và** 49 PNG `image-01`→`image-49` cùng thư mục + `image-map.json`; không còn thư mục `GS9 Knowledge VNG - Image Assets/` riêng ở local (Web KB đó vẫn còn nguyên).
- Master v3.3.0 đã được phục hồi từ 20 module phát hành sau khi file bị thất lạc trong lần di chuyển. Dry-run vòng lặp so sánh 20/20 module không có sai lệch ngoài hai thay đổi đường dẫn có chủ đích.
- Builder/test đã chuyển khỏi `knowledge-vng/` và khỏi layout hai-folder cũ, sang một folder gộp `GS9 Knowledge VNG AI/`.
- Gate mới nhất: strict build PASS; 20 module tên `doc-NN-...`; HTML offline tự chứa; `Ran 29 tests`, `OK` (6 skip do thiếu source HTML Plan V5 trên máy này).
- Ba module local `01`, `09`, `11` có sửa SOP có chủ đích để thay 14/34 và layout cũ bằng 20/49 cùng tên/path `GS9`; chưa phát hành live trong đợt chuẩn hóa này.
- Audit chỉ-đọc 14/08/2026 của 6 Agent mặc định VNG AI đã hoàn tất; bằng chứng tổng ở `audit/default-agent-readonly-audit-2026-08-14.md` và bản ghi từng Agent ở `agent/*-config.md`.
- Đã tạo và lưu cấu hình 10 custom Agent LiveOps trên Web. Snapshot sau tạo: `Tất cả 18`, `Của tôi 12`, `Mặc định 6`, shared-with-me `0`. Cả 10 chưa bind KB, sharing `0`, chưa publish/share và chưa chat/runtime test; bằng chứng tại `audit/liveops-custom-agent-creation-2026-08-14.md`.
- Web actual chung: preset `Hỏi đáp RAG`, model `hosted_vllm/qwen3.6-35b`, reranker trống, temperature `0.7`, Thinking Off, KB `Không dùng kho tri thức`, image/audio Off. Planner, Release, Incident, KPI, Economy, Communications và Curator có `Hỏi người dùng` + `Suy nghĩ` + `Lập kế hoạch (todo)`; Player Voice có Ask + Think; GM có Ask + Todo; `GS9 CFL CS Copilot` là Fast Answer không có Tools tab. Chín Smart Agent giữ `20` loop, `120s`, parallel Off.
- Identity/config UI-visible của 10 Agent là **Đã kiểm chứng**; behavior từ prompt là **Có điều kiện**; runtime/quality là **Bị chặn–Chưa xác định**.
- **Local meta-KB nay có đúng 28 Markdown phẳng** (tên `doc-00`→`doc-92`) tại `knowledge/GS9 CFL Knowledge Agent/`: 6 hướng dẫn chung, 6 hồ sơ Agent mặc định, 10 hồ sơ Agent custom, 3 trang cấu trúc KB CFL mới (`doc-30`–`doc-32`) và 3 trang governance; không có binary/folder con. **Phát hiện 1 link chết tồn tại từ trước** (4 file vẫn trỏ tên cũ `27-custom-gs9-gm-case-investigator.md`, không tồn tại từ khi Agent đổi vai trò sang GM Policy Advisor) — chưa sửa vì đó là đổi nội dung/nhãn, ngoài phạm vi việc đổi tên phiên này.
- Web meta-KB `GS9 CFL Knowledge Agent` (`1d92448f-7ee2-46c4-b202-5efbe9cc5616`) vẫn ở trạng thái 25/25 Markdown `Hoàn tất` với tên cũ (chưa Phase 3 sync), sharing 0. Chat test dùng Quick Answer đã chọn đúng LiveOps Planner + Release Reviewer, nêu đúng tool/Human gate và hiển thị `Nguồn tham khảo (15 tài liệu)`, gồm hai hồ sơ Agent tương ứng.
- Git handoff đích là `https://github.com/vinhviax/CFL-VNG-AI.git`, branch `main`. Người dùng đã phê duyệt publish toàn bộ project để dùng cá nhân; credential/private key/cache là ngoại lệ bắt buộc và được chặn bằng `.gitignore`.
- Prompt chuyển máy/phiên nằm tại `NEXT_SESSION_PROMPT.md`; audit publish nằm tại `audit/github-publish-2026-08-14.md`.
- Snapshot commit `1502d798debe46674cb5271fc92bd0c6240f2452` đã push thành công; `origin/main` khớp local HEAD tại gate sau push. Commit handoff cuối tiếp tục cập nhật tài liệu trạng thái này.

## Local Knowledge Base — CFL Plan Version 5

- Đã chuyển đổi chỉ-đọc file `CFL5_0- Plan Ver 5.0-14082026.html` vào `knowledge/GS9 CFL Plan Version/V5/`; SHA-256 nguồn `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`.
- Bundle có 42 file: 12 Markdown, 29 JPEG giải mã lossless và `source-manifest.json`; không có upload/bind/mutation Web.
- Độ phủ khóa theo nguồn: 9 section, 20 key point, 29 group, 115 item, 35 danh sách/91 highlight bullet, 15 figure slot và 29 ảnh (1.872.262 byte).
- Giữ rõ ba vị trí chưa có dữ liệu hình/lịch (FIG-00, FIG-11, FIG-12), một mô tả DOM rỗng có CSS fallback điều kiện, ba nhóm mô tả trùng và chênh lệch 47 nội dung thương mại hóa so với 46 item card.
- Converter: `scripts/convert_cfl_plan_html.py`; test: `tests/test_convert_cfl_plan_html.py`; audit: `audit/cfl-plan-v5-html-to-kb-2026-08-14.md`.
- Gate mới nhất cho toàn project: `Ran 22 tests`, `OK`; secret-pattern scan phạm vi đầu ra mới có 0 finding; `git diff --check` PASS.

### MỚI 15/08/2026 — URI MinIO đã gắn, đã upload Web

- `image-map.json` mới: 29 mục, 29 URI MinIO duy nhất, tên khớp `source-manifest.json` 1-1. Lấy bằng deep-link `?knowledge_id=` + nút `Toàn văn` + bắt request `GET /kb/v1/api/files?file_path=minio://...`.
- **Cạm bẫy đã xử lý:** mỗi ảnh sinh 2–10 URI (MinerU tách ảnh con). Quy tắc chọn: URI đầu tiên trong log = ảnh gốc, kiểm chứng bằng byte-size (29/29 kích thước manifest unique) + MCP `get_image` trên 5 mẫu (ca 2, 3, 10 URI và ca log tích luỹ).
- Đã chạy `scripts/link_plan_v5_minio.py`: 29 ảnh nhúng + 29 link registry (58 link `minio://`, 29 comment `LOCAL_ASSET`, 0 link tương đối sót) trên 7/12 file. Idempotent — chạy lại cho `0 thay đổi`.
- Audit: `audit/cfl-plan-v5-minio-uri-harvest-2026-08-15.md`.
- **Người dùng đã upload 12 Markdown lên KB Web `GS9 CFL Plan Version` (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`).** KB hiện **41 tài liệu** (12 MD + 29 JPEG), trạng thái xử lý hỗn hợp `Chờ xử lý`/`Đang xử lý`/`Hoàn tất` tại thời điểm kiểm tra.
- **Chưa chat-test.** Gate G6 (câu hỏi buộc trả lời kèm ảnh, xác nhận `Nguồn tham khảo` dùng đúng URI mới) là việc mở tiếp theo, độ ưu tiên cao — vừa đóng gate vừa nghiệm thu quy tắc "URI đầu tiên" từ *Có điều kiện* lên *Đã kiểm chứng*.
- Sửa `tests/test_link_plan_v5_minio.py`: 1 test cũ khoá vào trạng thái trước-khi-gắn-link (sẽ đỏ vĩnh viễn vì thao tác một chiều), đã sửa đếm đúng ở cả hai trạng thái; thêm test chặn link tương đối sót. `Ran 7 tests, OK`.

## Bản đồ kiến trúc KB 7 tầng — 15/08/2026, thiết kế đã chốt

Tài liệu: `docs/superpowers/specs/2026-08-15-kb-architecture-design.md`. Thay thế vai trò "nguồn chuẩn allowlist" của `agent/kb-allowlist-proposal-2026-08-14.md` (file cũ vẫn giữ làm bằng chứng lịch sử Phase 1).

- **7 tầng:** L0 Nền tảng & Meta · L1 Canon · L2 Kế hoạch · L3 Vận hành · L4 Kết quả · L5 Tiếng nói người chơi · L6 Dịch vụ người chơi · L7 Cách ly.
- **5/12 KB đích chưa tồn tại và chưa có nguồn:** `GS9 CFL Item Catalog`, `GS9 CFL Glossary & Systems` (đã bootstrap một phần — xem dưới), `GS9 CFL Event Calendar & Brief`, `GS9 CFL Runbook & Known Issues`, `GS9 CFL CS FAQ & Policy` (mới có format), `GS9 CFL GM Policy & Sanction`. Đây là việc soạn nội dung, không phải việc cấu hình.
- **Quyết định người dùng đã áp (DEC-036 → DEC-040):** không đổi tên KB đang chạy, chỉ ghi "bản chất" trong luồng (mục 5.1 spec); `Kho Dữ Liệu Tổng Hợp` là dẫn xuất có chủ đích để xem Wiki/Graph toàn cảnh, không phải trùng lặp — **bật nhóm tool Wiki** cho Agent bind KB này, cấm bind đồng thời KB tổng hợp và KB lẻ cấu thành cho cùng một Agent; `Data Daily` giữ dùng bình thường; `PUM` hạ P1→P2 nội bộ (cả team đọc doanh thu) nhưng cấm doanh thu lọt nội dung gửi người chơi; nhịp sự kiện LiveOps theo tháng; hai guardrail G-A (chống trộn phiên bản, mọi Agent bind Plan Version) và G-B (kế hoạch nội bộ ≠ brief duyệt, riêng Player Communications) đã duyệt nguyên văn tại mục 12.1 spec, áp khi bind.
- **2 KB nháp local-only đã dựng, chưa upload Web:**
  - `knowledge/GS9 CFL Glossary & Systems/` — 3 file. `01-thuat-ngu-vu-khi.md` sinh từ dữ liệu Item Profile thật (1.227+2.599 dòng), phát hiện 3 lỗi dữ liệu cần xử lý trước khi nạp (`Whtie`→`White` 15 dòng; phẩm chất rỗng 24 dòng; hệ `A/B/C` lẫn hệ màu 100 dòng). `02-thuat-ngu-he-thong-va-che-do.md` rút 146 tiêu đề từ Plan V5 thành tên chính thức tiếng Việt của chế độ chơi/hệ thống; còn treo 4 điểm cần chốt (đáng chú ý: `Weapon Laboratory` chưa có tên tiếng Việt).
  - `knowledge/GS9 CFL CS FAQ & Policy/` — chỉ có `00-huong-dan-va-quy-uoc.md` (format, chọn `Loại: FAQ` không phải `Tài liệu` — quyết định không đảo ngược được). **Chưa có nội dung thật**, cần người dùng cung cấp top câu hỏi CS + câu trả lời chuẩn + ranh giới chuyển tiếp GM/kỹ thuật + chính sách hoàn tiền/đền bù.

## Mutation live 15/08/2026 — đổi vai trò Agent GM

Agent `GS9 GM Case Investigator` (Agent ID `01d42d42-dd08-4907-9d4a-913142bc554c`, không đổi) đổi thành **`GS9 CFL GM Policy Advisor`**. Lý do: case-scoped view không tồn tại trên nền tảng (share/bind chỉ ở cấp KB), bind KB toàn tenant để "điều tra 1 vụ" vi phạm least privilege. Vai trò mới: tra cứu chính sách xử phạt/quy trình/tiền lệ, bắt buộc trích mã điều khoản, bằng chứng vụ việc qua tệp đính kèm hội thoại (không qua KB), tách bạch nhãn POLICY/CASE EVIDENCE.

- **Đã áp lên Web:** tên, mô tả tiếng Việt, System Prompt — 2 lần lưu riêng, cả hai đều có toast `Đã cập nhật trợ lý`, Agent ID xác minh trước mỗi lần sửa. Model/temperature/tool/KB không đổi (vẫn no-KB, sharing `0`).
- **Local:** đổi tên thư mục `agent/GS9 GM Case Investigator/` → `agent/GS9 CFL GM Policy Advisor/`, viết lại cả 4 file. Hồ sơ meta-KB `27-custom-gs9-gm-case-investigator.md` → `27-custom-gs9-gm-policy-advisor.md`, viết lại nội dung — **meta-KB local vẫn đúng 25 file**, nhưng **bản trên Web meta-KB (`GS9 CFL Knowledge Agent`) chưa đồng bộ** — vẫn là hồ sơ cũ tên `Case Investigator`, cần upload lại 1 file.
- Bỏ `Truy vấn CSDL` khỏi lộ trình tool (thay đổi so với bản `0.1-draft`).
- **Chưa bind KB** (chờ tạo `GS9 CFL GM Policy & Sanction`), chưa chat-test.

## Audit KB nghiệp vụ 14/08/2026 — read-only, không mutation

Bằng chứng: `audit/business-kb-readonly-audit-2026-08-14.md`; đề xuất: `agent/kb-allowlist-proposal-2026-08-14.md`.

- Danh mục KB Web actual là **9**, không phải 3: `Tất cả 9`, `Tôi tạo 8`, `Được chia sẻ 1`. Hai KB chưa từng ghi trong tài liệu project là `GS9 CFL Kho Dữ Liệu Tổng Hợp` (`574d4d12-8421-4e6f-9628-d03f4f7fb475`, 16 tài liệu) và `GS9 test knowledge base` (`6f887ec5-dab1-4505-999f-fb99c2280da9`, 0 tài liệu, do người khác sở hữu). ID mới ghi nhận: PUM `90484cd2-93fa-4d45-a37f-43c0d50430f2` (7), Data Daily `7be35c7c-c1fc-4538-bb1c-470f18378ae9` (9), Item Profile `e99b635f-04ec-44ad-9bcc-f12cae587c7d` (8). ID của `GS9 CFL Sentiment Feedback User` (1 tài liệu) chưa lấy được.
- **ACL:** năm KB `GS9 CFL Kho Dữ Liệu Tổng Hợp`, `GS9 Knowledge VNG AI`, `GS9 CFL Data Daily`, `GS9 CFL PUM` và `GS9 CFL Item Profile` đang chia sẻ cho space `CFL Member` (6 thành viên) với quyền **Chỉnh sửa**, tức quyền ghi. `sharing 0` chỉ đúng cho meta-KB `GS9 CFL Knowledge Agent`; `GS9 Knowledge VNG - Image Assets` và `GS9 CFL Sentiment Feedback User` cũng không share.
- **Blocker P0:** 7/7 CSV của `Data Private Weapon` đã live trong `GS9 CFL Item Profile` (khớp byte-size và số dòng với `audit/cfm-private-weapon-export-2026-08-14.md`), tổng 383.788 dòng cấp player có `openid`/`roleid`/`nickname`/lịch sử nạp. Mâu thuẫn trực tiếp với DEC-029 và Boundary "Không dùng `Data Private Weapon`". Nghiêm trọng hơn: description/summary do hệ thống sinh đã chứa nickname và giá trị nạp cụ thể, nên PII sẽ xuất hiện trong `Nguồn tham khảo` của mọi Agent bind KB này. Chưa xử lý; cần Human quyết định phương án.
- **Retention:** nền tảng không có control TTL/expiry/auto-purge ở cấp KB. Tab `Tổng quan` chỉ có Loại, Chiến lược lập chỉ mục (bị khóa khi KB đã có nội dung), Tên, Mô tả. Retention là **Bị chặn–Chưa xác định**, phải xử lý bằng quy ước vận hành.
- **Freshness:** Web Data Daily có 9 tài liệu, mirror local có 8 — thiếu `CFL_082026.xlsx`. `CFL ItemID.xlsx` vào KB qua `channel: google_drive` nên nội dung đổi được mà không qua build/audit. Hai tài liệu còn `error_message` pipeline (`01_weapons_usage.csv`, `CFL_082026.xlsx`) dù `parse_status: completed`.
- **Phạm vi MCP:** MCP KB connector chỉ thấy đúng tập KB đã share vào space `CFL Member`; ba KB không share trả `not found or not accessible`. Share KB vào space đồng thời mở KB đó cho MCP connector — một đường truy cập song song với Agent binding.
- Đề xuất allowlist Phase 1: bind 7 Agent (Planner, Release Reviewer, Incident Triage, KPI Experiment Analyst, Player Voice Analyst, Player Communications, Knowledge Curator), hoãn `GS9 CFL Economy Offer Analyst` chờ tách Item Profile, không bind `GS9 CFL CS Copilot` và `GS9 GM Case Investigator` vì thiếu nguồn. Chưa thực hiện bind nào.
- Người dùng tự xử lý G1 (hạ quyền share 5 KB xuống Chỉ đọc); agent không cần làm, chỉ theo dõi khi hoàn tất để mở khóa bind KB nghiệp vụ.

## Mutation live 14/08/2026 — bind KB + Việt hóa mô tả 10 Agent

Bằng chứng: `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md`. Đây là mutation live đầu tiên trên Agent kể từ lúc tạo.

- 6 Agent đã bind KB bằng `Kho tri thức đã chọn`: Knowledge Curator (2 KB, 6 tool), Incident Triage (PUM, 5), KPI Experiment Analyst (Kho Dữ Liệu Tổng Hợp, 6), Player Voice Analyst (Sentiment Feedback User, 4), LiveOps Planner (Knowledge VNG AI, 6), Release Reviewer (Knowledge VNG AI, 5).
- 4 Agent chưa bind có lý do: Player Communications, Economy Offer Analyst, GM Case Investigator, CS Copilot.
- Tool thêm: `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` cho cả 6; thêm `Thông tin tài liệu` cho Curator/KPI/Planner. Toàn bộ nhóm Wiki, data/SQL và `Danh mục sản phẩm` giữ Off.
- Cả 10 mô tả Agent đã chuyển sang tiếng Việt; System Prompt giữ nguyên tiếng Anh có chủ đích.
- Phát hiện UI: tool truy hồi bị mờ khi Agent chưa bind KB (`Cần có kho tri thức trong phạm vi`) nên phải bind trước rồi mới bật tool; danh sách Agent tự sắp lại sau mỗi lần lưu.
- Chưa chat/runtime/gold-set test; sharing Agent vẫn `0`; G6 chưa chạy.
- Nợ tài liệu: 10 file `agent/GS9 .../config.md` còn ghi `Không dùng kho tri thức` ở khối Web actual, cần đồng bộ theo DEC-034.

## Việc mới được giao 14/08/2026 — chưa hoàn tất

1. **Upload CFL Plan Version 5 lên Web KB `GS9 CFL Plan Version`** (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`) — **tạm dừng do blocker kỹ thuật**. Chi tiết: `audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`. Baseline KB: 0 tài liệu, Loại `Tài liệu`, RAG+Wiki, model `deepseek-v4-flash`/`text-embedding-3-large`, parser ảnh `MinerU` — sẵn sàng nhận cả 12 Markdown và 29 JPEG trong cùng một KB (không tách host ảnh riêng, theo chỉ định người dùng). Công cụ `file_upload` của Claude in Chrome từ chối mọi đường dẫn file thật trong project bằng một whitelist riêng, độc lập với quyền đọc file thường của agent; không mutation nào xảy ra, KB vẫn 0 tài liệu. Bước tiếp theo cần con người tự chọn 29 file `.jpg` qua Explorer trong hộp thoại Tải lên, sau đó agent lấy 29 URI MinIO (theo quy trình `docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md` Task 4 Step 2), ghi `knowledge/GS9 CFL Plan Version/V5/image-map.json`, sửa 12 Markdown, upload, chat-test.
2. **Xác định Agent nào dùng KB nào và cần tool gì** — **đã hoàn tất phần đề xuất** 14/08/2026. Ma trận đầy đủ 10 Agent × KB × tool nằm ở `agent/kb-allowlist-proposal-2026-08-14.md`; ba file `agent/GS9 .../config.md` của Planner, Release Reviewer và Player Communications đã ghi KB đề xuất kèm ràng buộc. Chưa bind gì trên Web — mọi mục vẫn cần Human approval.
   - Phase 1 (KB đã live, bind được sau G1): 7 Agent — Planner + Release Reviewer + Knowledge Curator dùng `GS9 Knowledge VNG AI` (Curator thêm meta-KB Agent); Incident Triage dùng `GS9 CFL PUM`; KPI Experiment Analyst dùng `GS9 CFL Kho Dữ Liệu Tổng Hợp`; Player Voice Analyst dùng `GS9 CFL Sentiment Feedback User`; Player Communications tạm dùng PUM.
   - Hoãn: `GS9 CFL Economy Offer Analyst` chờ tách `GS9 CFL Item Catalog` khỏi Item Profile (G2). Không bind: `GS9 CFL CS Copilot` và `GS9 GM Case Investigator` vì thiếu nguồn, là gap nội dung chứ không phải gap quyền.
   - Thay đổi do KB `GS9 CFL Plan Version`: `Player Communications` **đổi nguồn chính từ PUM sang Plan Version** (PUM là báo cáo kết quả tháng đã qua, Plan Version là nội dung sắp phát hành — đúng việc soạn patch note/notice hơn); `LiveOps Planner` và `Release Reviewer` bổ sung Plan Version. Cả ba có điều kiện: chỉ hiệu lực sau khi KB đó có nội dung live và chat-test grounding đạt.
   - **Xung đột phải xử lý trước khi bind Plan Version cho `Player Communications`:** System Prompt hiện yêu cầu chỉ dùng "approved event briefs", nhưng Plan V5 là tài liệu kế hoạch nội bộ chưa chốt (footer "không phổ biến ra ngoài"; FIG-00/11/12 còn chờ; chênh lệch 47 vs 46 item). Đã đề xuất câu guardrail cụ thể để chèn vào System Prompt, cần Human duyệt câu chữ.
   - Hai điều kiện bind cứng C1 (tài liệu nội bộ, không trích nguyên văn ra người chơi, không share space rộng) và C2 (kế hoạch chưa chốt, không trình bày như đã lên sóng) áp dụng cho mọi Agent bind vào Plan Version.

## Snapshot live cuối đã kiểm chứng (Web actual — CHƯA Phase 3 sync)

| Vai trò | KB | Inventory Web (chưa đổi) |
|---|---|---|
| Consumer | `GS9 Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`) | 20 MD, 0 PNG; 20/20 Hoàn tất |
| Asset host | `GS9 Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`) | 49 PNG, 0 MD; 49/49 Hoàn tất |
| Agent meta-KB | `GS9 CFL Knowledge Agent` (`1d92448f-7ee2-46c4-b202-5efbe9cc5616`) | 25 MD, 0 binary; 25/25 Hoàn tất; sharing 0 |

Snapshot live này kế thừa kiểm chứng rollout ngày 12/08/2026; việc đổi prefix theo quy định công ty không phải một lần upload hoặc migration mới. **Bảng này mô tả Web actual, KHÔNG phải local sau tái cấu trúc 15/08/2026 phiên 2** — local nay là 69 tài liệu gộp trong `GS9 Knowledge VNG AI/` (20 `doc-` + 49 `image-`) và 28 tài liệu trong `GS9 CFL Knowledge Agent/`. Web chỉ đổi sau khi Phase 3 (Google Drive connector sync) chạy.

## Việc đã chuẩn hóa local

- Khôi phục master và sinh lại HTML offline.
- Vòng phục hồi ban đầu giữ nguyên nội dung 20 module; sau đó sửa đúng ba SOP đang hoạt động còn count/path cũ. Không đổi các kết quả lịch sử có ghi rõ thời điểm test.
- Có backup nguyên byte trước build tại `audit/workspace-normalization-prebuild-2026-08-14.zip`.
- Có backup năm file context cũ tại `audit/workspace-docs-before-normalization-2026-08-14.zip`.
- Các cache, ảnh tạm đã phát hành, output trùng và fixture audit upload cũ được dọn/lưu trữ theo audit chuẩn hóa workspace.

## Backlog

- **Ưu tiên cao — chat-test Plan V5 (G6):** câu hỏi buộc trả lời kèm ảnh trên KB `GS9 CFL Plan Version`, xác nhận ảnh render thật và `Nguồn tham khảo` dùng đúng URI mới. Vừa đóng gate vừa nâng quy tắc "URI đầu tiên = ảnh gốc" từ Có điều kiện lên Đã kiểm chứng.
- **Đồng bộ meta-KB Web:** upload lại `27-custom-gs9-gm-policy-advisor.md` lên KB `GS9 CFL Knowledge Agent` — bản trên Web vẫn là hồ sơ `Case Investigator` cũ.
- **Nợ tài liệu cũ (từ 14/08, vẫn chưa xử lý):** 10 file `agent/GS9 .../config.md` còn ghi `Không dùng kho tri thức` ở khối Web actual — sai với 6 Agent đã bind. Đồng bộ theo DEC-034.
- **Cài package thiếu để chạy full gate:** `pip install markdown beautifulsoup4` — `test_build_handbook.py` và `test_convert_cfl_plan_html.py` đang lỗi `ModuleNotFoundError` trên máy này, không liên quan thay đổi 15/08.
- **Soạn nội dung cho 5 KB còn thiếu** theo bản đồ kiến trúc (DEC-036): ưu tiên Glossary (đã có bản nháp, cần bổ sung tiền tệ/sự kiện/giao diện) → CS FAQ (gỡ được Agent đang trắng hoàn toàn) → Runbook → Event Calendar → GM Policy.
- Bind lại `LiveOps Planner`/`Release Reviewer` khỏi tầng L0 sai (`GS9 Knowledge VNG AI`) sang tầng đúng khi KB L2/L3 sẵn sàng — không gỡ vội vì gỡ ngay sẽ làm Agent mất tool truy hồi.
- Upload folder thật và kiểm tra folder con.
- Xác định điều kiện sinh node Tổng hợp/So sánh.
- Kiểm thử Google Drive nhiều chu kỳ: thêm, sửa, đổi tên, di chuyển, xóa và quyền.
- Kiểm chứng Notion/NAS bằng credential test quyền tối thiểu.
- Kiểm chứng Image Analysis, audio/ASR và quota model khi tenant đủ điều kiện.
- ~~Audit nội dung, owner, ACL, retention và dữ liệu nhạy cảm của từng KB nghiệp vụ~~ — **hoàn tất 14/08/2026**. Việc còn lại là các gate G1–G6 trong `audit/business-kb-readonly-audit-2026-08-14.md`:
  - G1 (cần approval): hạ quyền share 5 KB từ `Chỉnh sửa` xuống `Chỉ đọc`.
  - G2 (cần approval): quyết định phương án dữ liệu player trong `GS9 CFL Item Profile`, gồm re-index để loại PII khỏi description/summary.
  - G3: bổ sung 6 KB còn thiếu kèm ID vào `PROJECT.md`/`STATUS.md`.
  - G4: đồng bộ mirror local Data Daily (thiếu `CFL_082026.xlsx`).
  - G5: đối chiếu 20 module trên Web với master sau khi siết quyền.
  - G6 (cần approval): chat-test grounding sau bind, xác nhận `Nguồn tham khảo` không lộ PII.
- Lấy ID của `GS9 CFL Sentiment Feedback User` và xác nhận danh sách 6 thành viên space `CFL Member` có đúng least privilege.
- Lập và chạy gold-set/chat/runtime test riêng cho từng Agent chỉ khi được giao; planned baseline có thể khác Web actual và Web actual là nguồn chuẩn cho trạng thái đang lưu.
- Khi thay tool, ID, mode hoặc quyền Agent, cập nhật `agent/`, 25 Markdown meta-KB và Web KB theo cùng một audit có ngày; không trình bày planned claim như Web actual.
- Rà soát credential hiện hữu trong dữ liệu của các KB CFL khác; không tự xóa khi chưa xác định dependency và phương án thay thế.
- Trên máy tiếp theo, xác minh `git status --short --branch` sạch và chạy `git pull --ff-only origin main` trước khi làm việc.

## Quy tắc giữ nguyên

- Không xóa 49 PNG/asset KB khi Markdown còn tham chiếu URI MinIO.
- Không dùng asset host làm corpus hỏi đáp thông thường.
- Không sửa trực tiếp module hoặc HTML; sửa master rồi strict build.
- Không upload dữ liệu private vào consumer dùng chung khi chưa có phê duyệt rõ ràng.
- Không dùng meta-KB Agent như corpus nghiệp vụ game và không tự gán KB CFL khác cho custom Agent khi chưa audit owner/ACL/retention/sensitivity/freshness.
