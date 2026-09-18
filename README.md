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
| 4 | [`DECISIONS.md`](DECISIONS.md) | 83 quyết định bền vững — tra khi không hiểu "vì sao lại làm vậy" |
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

**Chỉ sửa nội dung tại `docs KB/Human/`, rồi build.** Thư mục `knowledge/` là bản phát hành, sửa tay sẽ bị build ghi đè.

---

## ⚠️ Phạm vi git của `knowledge/` — đọc trước khi `git add`

`knowledge/` trên đĩa có **354 file / 2,75 GB**, nhưng git chỉ theo dõi **139 file / 29,7 MB**.

| Thư mục | Trên đĩa | Git | Vì sao |
|---|---|---|---|
| `GS9 Knowledge VNG AI` | 21 `.md` + 52 `.png` + map | ✅ | KB nền tảng |
| `GS9 CFL Plan Version/V5` | 12 `.md` + 29 `.jpg` | ✅ | |
| `GS9 CFL Knowledge Agent` | 8 `.md` | ✅ | meta-KB cho Human |
| `GS9 CFL Data Daily`, `Glossary & Systems`, `CS FAQ & Policy`, `Sentiment Feedback User` | nhẹ | ✅ | |
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

> **Gate build/test chưa được chạy lại sau khi chuyển tài khoản (18/09/2026).** Builder ghi vào `knowledge/` — nay đã trở lại trong repo nên *có thể* chạy được, nhưng chưa ai thử. Kiểm trước khi tin kết quả.

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
