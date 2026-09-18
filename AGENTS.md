# Quy tắc làm việc — Knowledge Base VNG

## Root và thứ tự đọc

Root duy nhất của project là `J:\My Drive\VNGGames AI\Knowledge Base VNG Source` (đổi 18/09/2026 khi chuyển sang tài khoản Google Drive mới — DEC-082; vị trí cũ `J:\My Drive\CFL\VNG AI\Knowledge Base VNG` không còn dùng). Xác nhận bằng `git rev-parse --show-toplevel`.

Khi bắt đầu phiên, đọc `HANDOFF.md`, `STATUS.md`, `PROJECT.md` và `DECISIONS.md`. Chỉ mở audit/report liên quan khi cần bằng chứng có ngày.

## Cấu trúc quản lý trên VNG AI

**⚠️ Cập nhật 18/09/2026 (DEC-082): `knowledge/` đã trở lại nằm TRONG repo này.** Không còn dùng shortcut sang Drive công ty (kiến trúc DEC-076 đã bị thay thế). Đường dẫn thật: `<root>\knowledge`.

**Phạm vi git của `knowledge/`:** chỉ theo dõi phần text/ảnh nhẹ đang sync lên VNG AI (139 file, ~30 MB). Bốn thư mục binary nặng bị `.gitignore` loại trừ và **chỉ tồn tại trên Drive** — `H5 Promotion/` (1,74 GB, 3 file zip vượt giới hạn cứng 100 MB/file của GitHub), `Kho Tài Liệu Chưa Tích Hợp/` (895 MB), `GS9 CFL PUM/` (127 MB PDF), `GS9 CFL Item Profile/` (dữ liệu người chơi). Đừng xoá chúng khỏi đĩa, cũng đừng `git add -f`.

**⚠️ `knowledge/Keys Drive/` chứa service-account key của connector.** Đã chặn bằng `.gitignore` (18/09/2026). Không mở nội dung, không xoá khỏi đĩa, không commit.

- `knowledge/` chứa mirror/dữ liệu của các Knowledge Base trên Web.
- `knowledge/GS9 Knowledge VNG AI/` là KB nền tảng dùng chung cho cả team GS9: **21 Markdown** `doc-00`→`doc-20` sinh tự động, **52 PNG** `image-01`→`image-52` và `image-map.json` (số đếm đã kiểm lại 18/09/2026; các bản tài liệu cũ ghi 20 module/49 ảnh là lỗi thời) — **cùng một thư mục** (tái cấu trúc 15/08/2026, DEC-043/044). Không còn thư mục `GS9 Knowledge VNG - Image Assets/` riêng ở local; Web KB đó (`6da8657c-...`) vẫn còn tồn tại nguyên trạng cho tới khi Phase 3 (Google Drive connector sync) hoàn tất và chat-test đạt.
- `knowledge/GS9 CFL Knowledge Agent/` là meta-KB riêng cho Human: **8 Markdown** trên đĩa (kiểm 18/09/2026 — con số "28 Markdown" ở các bản cũ là **sai**, không khớp thực tế); dải số `doc-00`→`doc-92` — 6 hướng dẫn chung, 6 hồ sơ Agent mặc định, 10 hồ sơ Agent custom, 3 trang cấu trúc KB CFL (`doc-30`–`doc-32`), 3 trang governance; không có binary hoặc dữ liệu player.
- Tên KB trên Web (`GS9 Knowledge VNG AI`, `GS9 Knowledge VNG - Image Assets`, `GS9 CFL Knowledge Agent`) không tự ý đổi; chỉ local đã tái cấu trúc thư mục.
- `agent/` dành cho manifest, prompt, cấu hình, test và handoff quản trị của Agent. Chỉ nội dung Human-facing đã biên tập/kiểm chứng mới được đưa vào meta-KB; không upload nguyên artifact quản trị một cách máy móc.

## Quy ước đặt tên (DEC-042)

- Ảnh: tiền tố `image-`. Tài liệu không phải ảnh: tiền tố `doc-`. Ngoại lệ: tài liệu đồng bộ Google Drive, người dùng tự đặt tên.
- KB nhiều phiên bản (`GS9 CFL Plan Version`): chèn số phiên bản ngay sau tiền tố — `doc-v5-NN-...`, `image-v5-NN-...`.
- Chi tiết và lý do: `knowledge/GS9 CFL Knowledge Agent/doc-32-quy-uoc-dat-ten-va-nhung-anh.md`.

## Nguồn chuẩn và artifact

**Nội dung tách theo đối tượng đọc (DEC-053).** Trước khi sửa bất kỳ tài liệu nào, xác định người đọc là ai:

| Thư mục | Ai đọc | Lên Web? |
|---|---|---|
| `docs KB/Human/` | Người dùng cuối chat với KB | Có — là **nguồn build** ra `knowledge/` |
| `docs KB/Dev/` | Dev và Agent config | Không — chỉ nằm trong repo |
| `agent/` | Dev và người phụ trách Agent | Không |

- Nguồn build là `docs KB/Human/` (tên `KB-NN-...`, `Agent-NN-...`). Builder đổi tiền tố tính năng sang `doc-` khi sinh, giữ DEC-042 vì regex đồng bộ khoá `^(doc|image)-`.
- Master cũ `so-tay-tao-knowledge-base-v3.md` **đã hết vai trò nguồn build**, nay nằm ở `audit/archive/` (DEC-066). Builder chỉ đọc tới nó khi `docs KB/Human` rỗng — không còn xảy ra. Đừng sửa nội dung ở đó và mong nó lên Web.
- Chủ đề KB thêm mới đánh số **từ 20 trở đi** (`KB-20`, `KB-21`…) vì dải 00–12 đã kín và 13–19 thuộc `Agent-NN`. Thêm module phải sửa kèm `EXPECTED_MODULE_COUNT` trong builder và các test khoá danh sách.
- Nội dung Dev (`DEC-xxx`, link `audit/`, `Mức bằng chứng`, "chưa kiểm chứng") **không được xuất hiện** trong `docs KB/Human` và `knowledge/`. Test hồi quy kiểm điều này cho 7 module Agent.
- `scripts/build_handbook.py` sinh 21 module (`doc-00`→`doc-20`) vào `knowledge/GS9 Knowledge VNG AI/` cùng thư mục với 49 ảnh, và `so-tay-tao-knowledge-base.html` tự chứa ở root. **HTML này không được git theo dõi** (nặng ~31 MB) — sinh lại bằng build khi cần.
- Không sửa trực tiếp 21 module sinh hoặc HTML. `image-map.json` là dependency build và phải giữ 49 URI MinIO duy nhất, khoá đặt tên `image-NN-...`.
- Mỗi module dùng URI MinIO hoạt động cho Web và comment `LOCAL_ASSET` trỏ `./image-NN-...` (cùng thư mục).
- **URI ảnh có thể chết sau khi ảnh được re-sync qua Drive connector.** Lấy lại hàng loạt bằng MCP `list_documents`, trường `file_path` (DEC-052) — dạng `minio://.../10012/<knowledge_id>/<uuid>.png` đã kiểm chứng render đúng.
- `knowledge/GS9 CFL Knowledge Agent/` (28 file) **viết tay, ngoài pipeline builder** — và đang lẫn nội dung Dev, chưa tách xong. Xem `HANDOFF.md`.

## An toàn

- Không xóa PNG còn được Markdown tham chiếu, dù đã gộp vào thư mục consumer.
- Thay ảnh theo thứ tự: đặt ảnh vào `GS9 Knowledge VNG AI` → map → strict build → phát hành Markdown → chat-test nguồn/ảnh.
- Không mutation live, gửi chia sẻ, xóa KB/Agent hoặc upload dữ liệu private nếu nhiệm vụ hiện tại chưa cho phép rõ ràng.
- Meta-KB Agent không tự động trở thành corpus nghiệp vụ của các Agent LiveOps/CS/GM/Product/Data/Marketing; chỉ bind nguồn sau audit nội dung, owner, ACL, retention và freshness.
- Không lưu credential, token, private key hoặc service-account mới trong project/audit. Nếu phát hiện credential hiện hữu, không đọc nội dung và không tự xóa khi chưa xác định dependency.
- `Data Private Weapon` và dữ liệu định danh/hành vi không được tự động trộn vào consumer tài liệu.
- Đưa nội dung lên Web dùng Google Drive connector (DEC-046), mỗi KB trỏ đúng một thư mục con của `knowledge/`, tuyệt đối không trỏ root project (chứa `audit/`, `docs/`, `scripts/`, `tests/`, `.git/` và service-account key). Không tự share KB vào space hoặc tự cấu hình sync — cần người dùng thực hiện hoặc cho phép rõ.

## Build và kiểm tra

Chạy tại root:

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

Gate hiện hành: strict build, đúng 20 module tên `doc-NN-...`, 49 PNG/URI duy nhất tên `image-NN-...` (cùng thư mục với module), 60 MinIO + 60 `LOCAL_ASSET`, HTML offline tự chứa và `Ran 29 tests`/`OK` (6 skip nếu máy không có file HTML nguồn Plan V5). Không dùng `--allow-missing-minio` cho bản bàn giao.

## GitHub và chuyển máy

- Repository bàn giao: `https://github.com/vinhviax/CFL-VNG-AI.git`, branch chuẩn `main`.
- Repository chứa toàn bộ project theo phê duyệt người dùng, gồm các dataset/binary nội bộ hiện có; phải giữ repository ở phạm vi cá nhân/private và không tạo public fork/mirror.
- `.gitignore` bắt buộc loại credential/private key/`.env`, cache, metadata hệ điều hành và shortcut `.gsheet` không portable. Không xóa rule bảo vệ vùng `knowledge/GS9 CFL Item Profile/keys CFL ItemID/keys/` nếu chưa rotate/revoke credential và có phê duyệt rõ ràng.
- Không dùng `git add -f` để vượt `.gitignore`; không force-push. Trước push phải chạy secret/file-size gate mà không in giá trị nhạy cảm.
- Trên máy khác, chạy `git pull --ff-only origin main`, sau đó đọc `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `PROJECT.md` → `DECISIONS.md`.
- Prompt khởi động phiên mới nằm tại `NEXT_SESSION_PROMPT.md`.

## Kết thúc phiên

Ghi bằng chứng vào audit trước, rồi cập nhật `STATUS.md` và `HANDOFF.md`. Phân loại kết luận live thành **Đã kiểm chứng**, **Có điều kiện** hoặc **Bị chặn/Chưa xác định**. Nếu phiên có thay đổi local được phép publish, commit/push không force và ghi lại kết quả remote trong handoff.
