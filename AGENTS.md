# Quy tắc làm việc — Knowledge Base VNG

## Root và thứ tự đọc

Root duy nhất của project là `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`.

Khi bắt đầu phiên, đọc `HANDOFF.md`, `STATUS.md`, `PROJECT.md` và `DECISIONS.md`. Chỉ mở audit/report liên quan khi cần bằng chứng có ngày.

## Cấu trúc quản lý trên VNG AI

- `knowledge/` chứa mirror/dữ liệu của các Knowledge Base trên Web.
- `knowledge/GS9 Knowledge VNG AI/` là consumer: đúng 20 Markdown sinh tự động và `image-map.json`; không chứa PNG.
- `knowledge/GS9 Knowledge VNG - Image Assets/` là asset host: đúng 49 PNG; không chứa Markdown.
- `knowledge/GS9 CFL Knowledge Agent/` là meta-KB riêng cho Human: đúng 25 Markdown về 6 Agent mặc định và 10 Agent custom; không có binary hoặc dữ liệu player.
- Ba tên trên là tên chính thức trên Web; không tự ý đổi tên hoặc nhập meta-KB vào consumer/asset host.
- `agent/` dành cho manifest, prompt, cấu hình, test và handoff quản trị của Agent. Chỉ nội dung Human-facing đã biên tập/kiểm chứng mới được đưa vào meta-KB; không upload nguyên artifact quản trị một cách máy móc.

## Nguồn chuẩn và artifact

- `so-tay-tao-knowledge-base-v3.md` là nguồn nội dung sổ tay chuẩn.
- `scripts/build_handbook.py` sinh 20 module vào consumer và sinh `so-tay-tao-knowledge-base.html` tự chứa.
- Không sửa trực tiếp 20 module sinh hoặc HTML. `image-map.json` là dependency build và phải giữ 49 URI MinIO duy nhất.
- Mỗi module dùng URI MinIO hoạt động cho Web và comment `LOCAL_ASSET` trỏ tương đối sang folder asset host.

## An toàn

- Không xóa asset host hoặc PNG còn được Markdown tham chiếu.
- Thay ảnh theo thứ tự: asset host → map → strict build → phát hành Markdown → chat-test nguồn/ảnh → cleanup consumer.
- Không mutation live, gửi chia sẻ, xóa KB/Agent hoặc upload dữ liệu private nếu nhiệm vụ hiện tại chưa cho phép rõ ràng.
- Meta-KB Agent không tự động trở thành corpus nghiệp vụ của các Agent LiveOps/CS/GM/Product/Data/Marketing; chỉ bind nguồn sau audit nội dung, owner, ACL, retention và freshness.
- Không lưu credential, token, private key hoặc service-account mới trong project/audit. Nếu phát hiện credential hiện hữu, không đọc nội dung và không tự xóa khi chưa xác định dependency.
- `Data Private Weapon` và dữ liệu định danh/hành vi không được tự động trộn vào consumer tài liệu.

## Build và kiểm tra

Chạy tại root:

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

Gate hiện hành: strict build, đúng 20 module, 49 PNG/URI duy nhất, 60 MinIO + 60 `LOCAL_ASSET`, HTML offline tự chứa và `Ran 16 tests`/`OK`. Không dùng `--allow-missing-minio` cho bản bàn giao.

## GitHub và chuyển máy

- Repository bàn giao: `https://github.com/vinhviax/CFL-VNG-AI.git`, branch chuẩn `main`.
- Repository chứa toàn bộ project theo phê duyệt người dùng, gồm các dataset/binary nội bộ hiện có; phải giữ repository ở phạm vi cá nhân/private và không tạo public fork/mirror.
- `.gitignore` bắt buộc loại credential/private key/`.env`, cache, metadata hệ điều hành và shortcut `.gsheet` không portable. Không xóa rule bảo vệ vùng `knowledge/GS9 CFL Item Profile/keys CFL ItemID/keys/` nếu chưa rotate/revoke credential và có phê duyệt rõ ràng.
- Không dùng `git add -f` để vượt `.gitignore`; không force-push. Trước push phải chạy secret/file-size gate mà không in giá trị nhạy cảm.
- Trên máy khác, chạy `git pull --ff-only origin main`, sau đó đọc `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `PROJECT.md` → `DECISIONS.md`.
- Prompt khởi động phiên mới nằm tại `NEXT_SESSION_PROMPT.md`.

## Kết thúc phiên

Ghi bằng chứng vào audit trước, rồi cập nhật `STATUS.md` và `HANDOFF.md`. Phân loại kết luận live thành **Đã kiểm chứng**, **Có điều kiện** hoặc **Bị chặn/Chưa xác định**. Nếu phiên có thay đổi local được phép publish, commit/push không force và ghi lại kết quả remote trong handoff.
