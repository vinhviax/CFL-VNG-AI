# Knowledge Base VNG — GS9 / CFL

Repo đóng gói **tài liệu, script và cấu hình** để tạo, vận hành và bảo trì Knowledge Base (KB) cùng Agent trên nền tảng [VNG AI](https://vnggames.ai). Phạm vi sản phẩm: **CFM VN · PTG · DT3Q**.

Đây là repo nội bộ, riêng tư. Không tạo public fork/mirror.

---

## Vị trí và yêu cầu

| Mục | Giá trị |
|---|---|
| Root | `J:\My Drive\VNGGames AI\Knowledge Base VNG Source` (thư mục Google Drive được sync) |
| Branch chuẩn | `main` |
| Remote | `https://github.com/vinhviax/CFL-VNG-AI.git` |
| Cần có | Python 3.11+, Node 20+ (chỉ khi dựng tài liệu `.docx`) |

> Root **đã đổi** ngày 18/09/2026 khi chuyển sang tài khoản Google Drive mới (DEC-082). Vị trí cũ `J:\My Drive\CFL\VNG AI\Knowledge Base VNG` không còn dùng. Trên máy khác, ổ đĩa có thể khác `J:` — luôn xác nhận bằng `git rev-parse --show-toplevel`.

---

## Đọc gì trước khi sửa bất cứ thứ gì

Thứ tự này có chủ đích — đọc sai thứ tự dễ làm hỏng việc:

| # | File | Nội dung |
|---|---|---|
| 1 | [`AGENTS.md`](AGENTS.md) | Quy tắc làm việc, ranh giới an toàn, phạm vi git |
| 2 | [`HANDOFF.md`](HANDOFF.md) | Trạng thái hiện tại, việc đang mở, **cạm bẫy đã gặp thật** |
| 3 | [`STATUS.md`](STATUS.md) | Nhật ký theo phiên |
| 4 | [`DECISIONS.md`](DECISIONS.md) | 88 quyết định bền vững — tra khi không hiểu "vì sao lại làm vậy" |
| 5 | [`PROJECT.md`](PROJECT.md) | Cây thư mục chuẩn, hợp đồng artifact |

---

## Cấu trúc

```
Knowledge Base VNG Source/
├── docs KB/                  # NGUỒN nội dung, tách theo ĐỐI TƯỢNG ĐỌC (DEC-053)
│   ├── Human/                #   → hướng dẫn người dùng — NGUỒN BUILD, sửa ở đây
│   └── Dev/                  #   → cơ chế, kết quả kiểm chứng — KHÔNG lên Web
├── knowledge/                # Bản sinh + dữ liệu KB, đồng bộ lên VNG AI qua connector
├── agent/                    # Manifest, prompt, cấu hình, test của 16 Agent
├── scripts/                  # Builder (build_handbook.py) và script một lần
├── tests/                    # Test hồi quy
├── audit/                    # Bằng chứng có ngày, snapshot
├── docs/                     # Kế hoạch, spec, report
└── samples/                  # Dữ liệu mẫu
```

### Luồng nội dung

```
docs KB/Human/{KB,Agent}-NN-*.md
        │
        └── scripts/build_handbook.py ──> knowledge/<KB>/doc-NN-*.md ──> connector ──> VNG AI
```

**Chỉ sửa nội dung tại `docs KB/Human/`, rồi build.** Thư mục `knowledge/` là bản phát hành, sửa tay sẽ bị build ghi đè. Ngoại lệ: các KB đơn giản không đi qua pipeline builder (`GS9 CFL Glossary & Systems`, `CS FAQ & Policy`, `Sentiment Feedback User`, `Data Daily`, `Metric Playbook`, `Dokploy VNG AI`) — các KB này viết/sửa trực tiếp trong `knowledge/<KB>/`, không có nguồn `docs KB/Human` tương ứng.

---

## KB và Agent hiện có trên VNG AI (cập nhật 18/09/2026)

### Knowledge Base

**Có bản mirror local trong `knowledge/`, git theo dõi:**

| KB | Nội dung | Trạng thái |
|---|---|---|
| `GS9 Knowledge VNG AI` | KB nền tảng dùng chung cho cả team GS9: hướng dẫn dùng nền tảng VNG AI — tạo KB, cấu hình Agent, parser, chunking, nguồn dữ liệu, chat, đa phương thức... 21 tài liệu + 52 ảnh minh hoạ. | Đang dùng, đã lên Web |
| `GS9 CFL Plan Version` (`V5`) | Nội dung kế hoạch/tính năng game CFL phiên bản V5 (chế độ chơi, hệ thống mới, boss, buff...). 12 tài liệu + 29 ảnh. | Đang dùng, đã lên Web |
| `GS9 CFL Knowledge Agent` | Meta-KB dành cho Human: hướng dẫn chọn nhanh Agent, ma trận so sánh 16 Agent, luồng công việc 10 Agent custom, dùng an toàn, ranh giới dữ liệu. 8 tài liệu. | Đang dùng, đã lên Web |
| `GS9 CFL Data Daily` | Số liệu vận hành CFL theo ngày (file Excel). | Đang dùng, đã lên Web — kho tạm cho `Economy Offer Analyst` |
| `GS9 CFL Glossary & Systems` | Thuật ngữ và hệ thống nghiệp vụ CFL. | Đang dùng, đã lên Web |
| `GS9 CFL CS FAQ & Policy` | Câu hỏi và chính sách chăm sóc khách hàng CFL. | Mới có định dạng, nội dung còn sơ khai — chưa đủ để `CS Copilot` dùng làm nguồn CS thật |
| `GS9 CFL Sentiment Feedback User` | Phản hồi và cảm xúc người chơi đã ẩn danh. | Đang dùng, đã lên Web — chứa dữ liệu phản hồi người chơi, chỉ dùng nội bộ |
| `GS9 CFL Metric Playbook` | Sổ tay 52 metric theo dõi CFL (4 phần, kèm sơ đồ phân rã). 1 tài liệu `.docx`. | **Mới tạo 18/09/2026, chưa lên Web** — cần tạo KB + trỏ connector |
| `GS9 Dokploy VNG AI` | Hướng dẫn dùng nền tảng deploy nội bộ Dokploy: điều kiện truy cập, quy trình 9 bước, xác thực & bảo mật, FAQ, deploy qua GigiKit CLI, cộng kinh nghiệm thực tế (kiến trúc Swarm, bẫy deploy, volume, domain) từ một lần triển khai dự án thật. 10 tài liệu. | Tạo 18/09/2026 — người dùng đã trỏ Google Drive connector, chờ tự đồng bộ lên Web |

**Chỉ tồn tại trên Drive, KHÔNG git theo dõi** (quá nặng hoặc nhạy cảm — xem bảng phạm vi git bên dưới):

| KB | Nội dung | Vì sao không tracked |
|---|---|---|
| `H5 Promotion` | Tài liệu khuyến mãi H5 (3 file zip lớn). | Vượt giới hạn 100 MB/file của GitHub |
| `Kho Tài Liệu Chưa Tích Hợp` | Tài liệu nguồn team gửi, chưa xử lý thành KB chính thức (nhóm Event/Function/Localize/Membership). | Quá nặng (895 MB), chưa qua biên tập |
| `GS9 CFL PUM` | Dữ liệu vận hành nhạy cảm dạng PDF. | Quá nặng, gắn cho `Incident Triage` |
| `GS9 CFL Item Profile` | Dữ liệu người chơi (P0) — không mở, không trộn vào KB dùng chung. | Dữ liệu người chơi |

**Chỉ tồn tại trên Web, KHÔNG có bản mirror local trong repo này:**

| KB | Ghi chú |
|---|---|
| `GS9 CFL Kho Dữ Liệu Tổng Hợp` | KB tổng hợp lớn (101 tài liệu, kiểm 17/08/2026), gắn cho `KPI Experiment Analyst`. Ngoài phạm vi repo — không sửa/đồng bộ được từ đây. |

### Agent

16 Agent chia hai nhóm: 6 mặc định (nền tảng cung cấp sẵn, phạm vi mở toàn bộ kho tri thức) và 10 Agent riêng của GS9 CFL (chỉ gắn đúng kho được duyệt cho vai trò, có chủ sở hữu/người duyệt rõ ràng). Nguồn đầy đủ: [`knowledge/GS9 CFL Knowledge Agent/doc-02-ma-tran-so-sanh-16-agent.md`](knowledge/GS9%20CFL%20Knowledge%20Agent/doc-02-ma-tran-so-sanh-16-agent.md).

**Sáu Agent mặc định** (`Quick Answer`, `Smart Reasoning`, `Hybrid Researcher`, `Wiki Questioner`, `Data Analyst`, `FPA Analyst`) — cấu hình sẵn của nền tảng, không có chủ sở hữu nghiệp vụ cụ thể, dùng được ngay cho tra cứu thường ngày nhưng đừng nạp dữ liệu nhạy cảm vào phạm vi của chúng.

**Mười Agent riêng của GS9 CFL:**

| Agent | Việc chính | Kho tri thức đang gắn | Trạng thái gắn kho |
|---|---|---|---|
| `Knowledge Curator` | Postmortem, bài học, đề xuất sửa kho tri thức | `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI` | Đúng chuyên môn |
| `KPI Experiment Analyst` | KPI, cohort, kết quả thử nghiệm | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | Đúng chuyên môn |
| `Incident Triage` | Dòng thời gian, mức độ, giả thuyết nguyên nhân sự cố | `GS9 CFL PUM` | Đúng chuyên môn, nhưng phạm vi hẹp — chỉ tra được report tháng, chưa có runbook sự cố |
| `Player Voice Analyst` | Chủ đề và cảm xúc trên phản hồi đã ẩn danh | `GS9 CFL Sentiment Feedback User` | Đúng chuyên môn |
| `LiveOps Planner` | Brief sự kiện, lịch, dependency, rủi ro | `GS9 Knowledge VNG AI` | **Kho tạm** — chưa gắn kho nghiệp vụ LiveOps |
| `Release Reviewer` | Kiểm tra trước phát hành, mức sẵn sàng rollback | `GS9 Knowledge VNG AI` | **Kho tạm** — chưa gắn kho nghiệp vụ LiveOps |
| `Player Communications` | Thông báo, thư trong game, push, bản địa hoá | `GS9 CFL Plan Version` | **Kho tạm** — kho đúng (lịch sự kiện + brief đã duyệt) chưa dựng xong |
| `Economy Offer Analyst` | Giá, phần thưởng, dòng vào/ra, gói ưu đãi | `GS9 CFL Data Daily` | **Kho tạm** — kho đúng (danh mục vật phẩm + giá) chưa dựng xong |
| `CS Copilot` | Phân loại ticket, nháp trả lời, đề xuất chuyển cấp | `GS9 Knowledge VNG AI` | **Kho tạm** — câu trả lời về chính sách CS **chưa có nguồn CFL bảo chứng** |
| `GM Policy Advisor` | Tra và giải thích điều khoản xử phạt, quy trình | `GS9 Knowledge VNG AI` | **Kho tạm** — câu trả lời về xử phạt GM **chưa có nguồn CFL bảo chứng** |

Cả 10 Agent riêng **chưa được ký duyệt phát hành**, đang trong giai đoạn chuẩn bị — chưa dùng cho quyết định vận hành thật. Bảng gắn kho là ảnh chụp một thời điểm, có thể đổi bất cứ lúc nào — mở Agent ra xem trực tiếp trước khi tin một câu trả lời quan trọng.

---

## ⚠️ Phạm vi git của `knowledge/` — đọc trước khi `git add`

`knowledge/` trên đĩa có **354 file / 2,75 GB**, nhưng git chỉ theo dõi **139 file / 29,7 MB** (chưa tính hai KB mới `Metric Playbook`/`Dokploy VNG AI` — nhẹ, sẽ cộng thêm khi commit).

| Thư mục | Trên đĩa | Git | Vì sao |
|---|---|---|---|
| `GS9 Knowledge VNG AI` | 21 `.md` + 52 `.png` + map | ✅ | KB nền tảng |
| `GS9 CFL Plan Version/V5` | 12 `.md` + 29 `.jpg` | ✅ | |
| `GS9 CFL Knowledge Agent` | 8 `.md` | ✅ | meta-KB cho Human |
| `GS9 CFL Data Daily`, `Glossary & Systems`, `CS FAQ & Policy`, `Sentiment Feedback User` | nhẹ | ✅ | |
| `GS9 CFL Metric Playbook`, `GS9 Dokploy VNG AI` | nhẹ | ✅ | mới tạo 18/09/2026 |
| `H5 Promotion` | 1,74 GB | ❌ | 3 zip **649 / 570 / 503 MB** — vượt giới hạn cứng 100 MB/file của GitHub, push sẽ **bị từ chối thẳng** |
| `Kho Tài Liệu Chưa Tích Hợp` | 895 MB | ❌ | tài liệu nguồn chưa xử lý |
| `GS9 CFL PUM` | 127 MB PDF | ❌ | quá nặng |
| `GS9 CFL Item Profile` | 24 MB | ❌ | dữ liệu người chơi |
| `Keys Drive` | — | ❌ | **service-account key** |

Bốn thư mục ❌ **chỉ tồn tại trên Drive**. Đừng xoá khỏi đĩa, đừng `git add -f`. Đã cân nhắc và loại Git LFS vì 2,75 GB vượt xa quota free 1 GB.

---

## An toàn — không thoả hiệp

- **Không commit credential.** Hai file key đã được `.gitignore` chặn: `knowledge/Keys Drive/` và `keys KB/keys/`. Ngày 18/09/2026 file `cfl-drive-kb-*.json` **suýt bị commit** vì không khớp pattern nào (DEC-083) — **trước mỗi `git add` diện rộng, chạy `git check-ignore -v` trên đúng file credential**, đừng tin pattern chung đã phủ.
- `GS9 CFL Item Profile` chứa dữ liệu người chơi — không mở, không trộn vào KB dùng chung.
- Không `git push --force`, không `git add -f` để vượt `.gitignore`.
- Không tự share KB vào space, tự cấu hình sync, hay xoá KB/Agent trên Web.

---

## Lệnh thường dùng

```powershell
# Kiểm tra đầu phiên
git rev-parse --show-toplevel
git fetch origin; git diff --stat origin/main HEAD    # phải rỗng

# Build + test
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

> **Gate build/test đã chạy lại sau khi chuyển tài khoản (18/09/2026) — sạch hoàn toàn.** `Ran 30 tests`/`OK`, builder sinh ra khớp tuyệt đối với `knowledge/` thật. Chạy trên bản cô lập trong scratchpad để không đụng `knowledge/` thật đang sync — xem `HANDOFF.md` mục 4.11 nếu cần lặp lại cách làm.

### Nếu git báo `fatal: bad object refs/desktop.ini`

Google Drive tạo `desktop.ini` bên trong `.git/`, git đọc chúng như ref hỏng. Repo **không** hỏng:

```bash
find .git -type f -name desktop.ini -delete
git for-each-ref && git rev-parse HEAD
```

Sẽ tái sinh mỗi khi Drive sync lại (DEC-083).

---

## Cạm bẫy đáng biết trước

- **Không grep/find đệ quy từ root** — `knowledge/` 2,75 GB trên Drive làm `grep -r` và `git status` timeout. Chỉ nhắm đúng file.
- **Ghi file trên Drive phải qua file tạm + `os.replace`** — ghi đè trực tiếp từng làm mất sạch nội dung một file nguồn.
- Console Windows dùng cp1252: `print()` chuỗi tiếng Việt sẽ `UnicodeEncodeError` **sau khi** tác vụ đã chạy xong — đừng nhầm là thất bại. Thêm `sys.stdout.reconfigure(encoding="utf-8")`.
- Chi tiết đầy đủ: [`HANDOFF.md`](HANDOFF.md) mục 5.
