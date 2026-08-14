# Audit — GitHub project handoff 14/08/2026

## Phạm vi và phê duyệt

- Root: `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`.
- Remote đích: `https://github.com/vinhviax/CFL-VNG-AI.git`.
- Branch đích: `main`.
- Người dùng đã yêu cầu publish toàn bộ project để tiếp tục trên máy cá nhân khác.
- Ngoại lệ bắt buộc: credential/private key, `.env`, cache và metadata hệ điều hành; không mở hoặc ghi giá trị bí mật vào audit.

## Preflight chỉ-đọc

- Trước phiên publish, root chưa phải Git repository và remote chưa có ref.
- `git ls-remote` truy cập được remote qua credential manager nhưng trả về không có ref; GitHub API không xác thực trả `404`, phù hợp với repository private đang trống.
- Inventory trước ignore: khoảng `301` file / `238.087 MiB`; `9` file từ `10 MiB`, không file nào từ `50 MiB` hoặc `100 MiB`.
- Phát hiện một JSON dạng service-account trong vùng key của Item Profile bằng metadata tên/path. Không đọc nội dung; `.gitignore` loại toàn bộ thư mục key đó.
- Shortcut Google Drive `CFL ItemID.gsheet` dài `173` byte tái hiện ổn định lỗi `git hash-object ... Invalid argument` trên Google Drive filesystem. Đây không phải payload dữ liệu portable; `.gitignore` loại `*.gsheet`, còn CSV/JSON export thật vẫn trong scope.
- Scan sơ bộ vùng tài liệu an toàn không phát hiện PEM/private key/client secret/refresh token/GitHub token/AWS key; hai chuỗi giống Google key trong HTML là dữ liệu ảnh base64 và không được coi là credential.

## Gate bắt buộc trước push

1. Danh sách staged không chứa vùng key đã biết hoặc file bị `.gitignore` chặn.
2. Không staged file nào đạt giới hạn GitHub `100 MiB`.
3. Strict builder và toàn bộ `16` unit tests đạt.
4. Meta-KB giữ đúng `25` Markdown; 10 custom Agent giữ Web ID/tool/no-KB/sharing-0 đúng snapshot.
5. `git push` không dùng force; local HEAD phải khớp `refs/heads/main` trên remote.

## Kết quả publish

- Pre-commit staging: `303` file / `238.101 MiB`; `9` file từ `10 MiB`, `0` file từ `50 MiB`, `0` file từ `100 MiB`.
- Known credential staged: `False`; `.gsheet` staged: `False`.
- Secret scan: `200` staged text files, `0` high-confidence hit sau khi dùng boundary chặt; các false positive trước đó là tên `task-*` và dữ liệu ảnh base64 trong HTML.
- Strict build: `20` module / `125,609` bytes; HTML offline `30,859,005` bytes.
- Regression: `Ran 16 tests`, `OK`.
- Agent/meta-KB gate: `PASS` — 25 Markdown, 25 H1 duy nhất, 0 link hỏng, 0 secret pattern, 10 custom Agent và 10 Web ID duy nhất.
- Trạng thái: **Đã sẵn sàng commit/push**.
- Commit snapshot: chưa ghi.
- Commit handoff cuối: chưa ghi.
- Remote verification: chưa chạy.
