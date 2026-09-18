Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root repo Git:

```
J:\My Drive\VNGGames AI\Knowledge Base VNG Source
```

Xác nhận bằng `git rev-parse --show-toplevel` (ổ đĩa có thể khác `J:` trên máy khác).

**Kiến trúc hiện hành (DEC-082, 18/09/2026):** `knowledge/` nằm **trong** repo tại `<root>\knowledge`. Không còn shortcut `.shortcut-targets-by-id` sang Drive công ty — kiến trúc DEC-076 đã bị thay thế. Trên đĩa `knowledge/` có 354 file / 2,75 GB nhưng **git chỉ theo dõi 139 file / 29,7 MB**; 4 thư mục binary nặng bị `.gitignore` loại trừ (`H5 Promotion`, `Kho Tài Liệu Chưa Tích Hợp`, `GS9 CFL PUM`, `GS9 CFL Item Profile`) và `Keys Drive` (credential). Đọc `README.md` mục "Phạm vi git" trước khi `git add`.

Đọc theo thứ tự: `README.md` → `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `DECISIONS.md` (tra từ DEC-075 khi cần).

==================================================
0. TRẠNG THÁI KHI BÀN GIAO (kiểm chứng 18/09/2026, phiên 10)
==================================================

- Repo **sạch**, HEAD = `196029d`, khớp `origin/main`, `git diff --stat origin/main HEAD` rỗng. 485 file tracked.
- Đã chuyển sang tài khoản Google Drive mới, **không mất dữ liệu** (đối chiếu HEAD/tree/hash index/số file với mốc trước khi chuyển — khớp tuyệt đối).
- 3 file untracked ở root là cố ý giữ, **đừng xoá**: `knowledge-20260820T085450Z-1-001.zip`, `CFL Thu Thập Dữ Liệu.xlsx`, `VNGGames AI.html`.
- **Nếu git báo `fatal: bad object refs/desktop.ini`:** Drive lại rải `desktop.ini` vào `.git/`. Chạy `find .git -type f -name desktop.ini -delete` rồi `git for-each-ref`. Repo **không** hỏng — chuyện này tái diễn liên tục (DEC-083). Đã gặp lại chỉ ~30 phút sau lần dọn đầu.

**Người dùng đã chốt thứ tự làm việc:** làm **Việc 1 → Việc 2 → Việc 3** dưới đây. Nhóm tài liệu Membership / Content Game / Function Game / Event / Localize / Survey trong `Kho Tài Liệu Chưa Tích Hợp` **để từ từ sau**, chưa đụng tới.

==================================================
VIỆC 1 — DỌN NỢ KỸ THUẬT
==================================================

**1a. Chạy gate build/test — chưa ai chạy lại từ khi đổi kiến trúc.**

`scripts/build_handbook.py` sinh module vào `knowledge/GS9 Knowledge VNG AI/`. Trước đây `knowledge/` không nằm trong repo nên builder chắc chắn lỗi; nay đã trở lại nên **có thể** chạy được — nhưng chưa kiểm chứng.

⚠️ **Người dùng dặn không được sửa gì trong `knowledge/`** (đó là bản mới nhất đang sync lên VNG AI). Nên **đừng chạy builder thẳng vào thư mục thật**. Cách an toàn:

1. Copy `knowledge/GS9 Knowledge VNG AI/` sang scratchpad.
2. Chạy builder trỏ vào bản copy (hoặc chạy rồi `git diff` ngay để xem nó đổi gì, và `git checkout -- knowledge/` để hoàn tác nếu có).
3. So sánh bản sinh với bản thật: nếu khớp → builder còn đúng; nếu lệch → báo cáo lệch chỗ nào, **đừng tự ghi đè**.
4. Chạy `python -m unittest discover -s tests -v`. Gate cũ kỳ vọng `Ran 30 tests`; nhiều test khoá cứng số lượng (49/52 ảnh, 61/64 lượt tham chiếu) nên có thể FAIL do số liệu đã đổi — **đọc kỹ từng FAIL, đừng sửa test cho pass**.

**1b. Backup 2,75 GB đang không có bản sao.**

Bốn thư mục bị loại khỏi git **chỉ tồn tại trên Drive**: `H5 Promotion` (1,74 GB), `Kho Tài Liệu Chưa Tích Hợp` (895 MB), `GS9 CFL PUM` (127 MB), `GS9 CFL Item Profile` (24 MB). Vừa chuyển tài khoản Drive một lần — mất lần nữa là mất hẳn. **Hỏi người dùng** muốn backup đi đâu (ổ ngoài / Drive khác / chấp nhận rủi ro), đừng tự quyết.

==================================================
VIỆC 2 — ĐÓNG NGHI VẤN CŨ (HANDOFF mục 4.5)
==================================================

Mục 4.5 đánh dấu **ƯU TIÊN CAO** từ 17/08/2026 và **chưa bao giờ được đóng**: nghi vấn Agent lấy nội dung trong **ảnh minh hoạ** làm nguồn dữ kiện, rồi trả lời sai.

**Đã kiểm chứng trước đó:** nền tảng OCR nội dung ảnh **và** sinh caption ngay lúc nạp, lưu thành chunk tra cứu được; trace một lượt chạy ghi rõ Agent chủ động truy hồi `image-01-...png` làm nguồn.
**Chưa chứng minh:** câu trả lời sai có *lấy đúng* từ các chunk đó không.

Việc cần làm: chạy lại Case 2 (`audit/agent-chat-test-2026-08-17.md` mục 8), so kết quả. Nếu vẫn sai → thử tắt VLM/đọc ảnh cho KB thuần hướng dẫn rồi chạy lại, so ba kết quả.

**Vì sao đáng làm trước khi dựng KB mới:** nếu lỗi này có thật, mọi KB dựng sau đều dính. Chốt được nguyên nhân sẽ định hình cách chèn ảnh vào KB Dokploy sắp làm.

**Việc treo nhỏ kèm theo:** `knowledge/Kho Tài Liệu Chưa Tích Hợp/gs9-metric-playbook.docx` (529 KB, dựng 25/08) chưa quyết đưa vào KB nào và chưa đổi tên theo quy ước `doc-`. **Không tái tạo lại được** — bản HTML nguồn đã mất. Hỏi người dùng.

==================================================
VIỆC 3 — DỰNG KB "DOKPLOY VNG AI" (việc chính người dùng muốn)
==================================================

Nguồn: hai site tài liệu nội bộ. **Đã trinh sát 18/09/2026, số liệu dưới đây là thật.**

### ⚠️ Cả hai site đều sau SSO — đừng phí thời gian với WebFetch

`WebFetch` **luôn thất bại**: bị 302 sang `auth.vnggames.ai/auth/realms/AITransformation/...`. Đã thử, đã xác nhận.
→ **Dùng Chrome thật** (`mcp__claude-in-chrome__*`), nơi người dùng đã đăng nhập sẵn. Đã kiểm: mở được cả 2 site, không bị chặn.
→ Đọc nội dung bằng `get_page_text` hoặc `javascript_tool` (`document.body.innerText`), không cần screenshot.

### Nguồn A — Dokploy VNG (đọc TOÀN BỘ, đúng 5 trang)

`https://docs.hub.vnggames.ai/docs/dokploy`

| # | Trang | URL |
|---|---|---|
| 1 | Introduction | `/docs/dokploy` |
| 2 | Access Requirements | `/docs/dokploy/getting-started` |
| 3 | Deployment Flow | `/docs/dokploy/deployment-flow` |
| 4 | SSO & Security | `/docs/dokploy/auth-security` |
| 5 | FAQ & Support | `/docs/dokploy/faq` |

### Nguồn B — GigiKit (CHỈ lấy phần liên quan Dokploy)

`https://docs-gigikit.hub.vnggames.ai` — tổng 29 trang. Trang trực tiếp về Dokploy:

- **`/guides/skills/deploy-dokploy`** — "gk:deploy-dokploy — Deploy to Dokploy", ~4.500 ký tự, 16 mục: When to Use · Prerequisites (Install CLI, Authenticate) · What the Skill Does · Workflow: Deploy an App · Key Commands Reference (Project & App, Database, Environment Variables, Create Environment) · Post-Deploy · Error Reference · Security Notes.

Ngoài ra **phải quét 28 trang còn lại tìm chỗ nhắc Dokploy** (rất có thể có trong `commands-cheat-sheet`, `workflow-recipes`, `primary-workflow`). Danh sách nav đầy đủ: `/guides/getting-started/{introduction,installation,quickstart,commands-cheat-sheet,command-finder}`, `/guides/agents/{overview,planner,developer,tester,reviewer}`, `/guides/skills/{catalog,using-skills,creating-skills,deploy-dokploy,nexus-ui,skill-creator}`, `/guides/workflows/{primary-workflow,orchestration,chaining-patterns,workflow-recipes}`, `/guides/rules/{development-rules,team-coordination}`, `/guides/hooks/{overview,custom-hooks}`, `/guides/teams/{multi-agent,file-ownership}`, `/guides/plans/{creating-plans,templates}`.

### Cách làm đề xuất

1. **Thu thập:** duyệt 5 trang nguồn A + trang `deploy-dokploy` + quét 28 trang nguồn B tìm `dokploy`. Lưu bản thô ra scratchpad **và** `scripts/one-off/` (bài học: scratchpad bị xoá giữa các phiên, mất hết script/dữ liệu trung gian).
2. **Biên tập theo DEC-053:** nội dung lên KB là **hướng dẫn cho người đọc**, không chứa mã `DEC-xxx`, link `audit/`, hay nhãn "đã/chưa kiểm chứng".
3. **Đặt tên theo DEC-042:** file `doc-NN-<slug>.md`, regex đồng bộ khoá `^(doc|image)-`. Ảnh (nếu có) `image-NN-...`.
4. **Vị trí:** tạo thư mục mới `knowledge/GS9 Dokploy VNG AI/` (tiền tố `GS9` là bắt buộc theo quy định công ty). **Hỏi người dùng xác nhận tên KB** trước khi tạo.
5. **Đưa lên Web:** tạo KB trên vnggames.ai + trỏ connector vào thư mục — **việc này cần người dùng làm hoặc cho phép rõ ràng**, tuyệt đối không tự share/cấu hình sync (AGENTS.md).
6. **Chat-test** sau khi sync, và nhớ **bật công cụ truy hồi** cho Agent (DEC-061: gắn KB thôi chưa đủ, `Tìm theo ngữ nghĩa`/`Tìm theo từ khóa` không tự bật).

### Câu hỏi nên gộp hỏi người dùng một lượt

- Tên KB chính thức? (đề xuất `GS9 Dokploy VNG AI`)
- KB này cho ai đọc — dev nội bộ hay cả team? (quyết định độ sâu kỹ thuật)
- Có cần chụp ảnh giao diện Dokploy chèn vào không? (lưu ý nghi vấn mục 4.5 ở Việc 2)
- Phần GigiKit: chỉ lấy `deploy-dokploy`, hay lấy cả bối cảnh GigiKit để người đọc hiểu skill nằm trong hệ thống nào?

==================================================
LỆNH KIỂM TRA ĐẦU PHIÊN
==================================================

```bash
git rev-parse --show-toplevel
git status --short
git fetch origin && git diff --stat origin/main HEAD    # phải rỗng
ls knowledge/                                            # phải thấy 12 thư mục
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
- Không tự ý: sửa file trong `knowledge/`, chạy builder ghi đè `knowledge/`, tạo/share KB trên Web, `git push --force`, `git add -f`.
