# GitHub Handoff Publish Design

**Ngày:** 14/08/2026  
**Đích:** `https://github.com/vinhviax/CFL-VNG-AI`  
**Nhánh:** `main`

## Mục tiêu

Biến root hiện tại thành Git repository, ghi lại trạng thái Agent/KB và handoff đủ để tiếp tục trên máy khác, sau đó push toàn bộ project lên repository GitHub cá nhân theo yêu cầu người dùng.

## Bối cảnh đã kiểm chứng

- Root `J:\My Drive\CFL\VNG AI\Knowledge Base VNG` chưa có `.git`, `.gitignore`, remote hoặc lịch sử commit.
- Remote đích tồn tại nhưng chưa có ref; truy cập Git không xác thực được, trong khi `git ls-remote` qua credential manager trả về thành công và không có ref. Hai tín hiệu này phù hợp với repository private đang trống.
- Project có khoảng 238 MiB dữ liệu; không file nào đạt 50 MiB, nên dùng Git thường thay vì Git LFS.
- Có một JSON dạng service-account trong vùng Item Profile. Không đọc nội dung, không stage và không commit file này.

## Phạm vi publish

Theo phê duyệt của người dùng, publish toàn bộ project gồm source, tài liệu, audit, Agent, ba KB tài liệu, các KB CFL khác, PDF/XLSX/CSV/JSON, ảnh, HTML và backup hiện có.

Ngoại lệ bắt buộc:

- Credential, token, private key, `.env` và thư mục key đã nhận diện.
- Cache Python, metadata hệ điều hành và shortcut Google Drive `.gsheet` không thể hash/clone như file thường.
- `.git/` do Git tự quản lý.

## Artifact bàn giao

- `.gitignore`: ranh giới secret/cache tối thiểu; không loại các dataset đã được người dùng yêu cầu publish.
- `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md`, `DECISIONS.md`: ghi repository, trạng thái publish, quy tắc tiếp tục và safety gate.
- `NEXT_SESSION_PROMPT.md`: prompt copy/paste cho phiên làm việc tại nhà.
- `audit/github-publish-2026-08-14.md`: bằng chứng scope, verification, commit và remote.
- Plan triển khai cùng ngày trong `docs/superpowers/plans/`.

## Quy trình và gate

1. Cập nhật tài liệu/handoff và tạo prompt chuyển máy.
2. Khởi tạo `main`, gắn `origin`, stage toàn bộ file không bị ignore.
3. Kiểm tra danh sách ignored, file lớn, credential path và secret pattern mà không in giá trị bí mật. Shortcut `.gsheet` bị loại vì `git hash-object` tái hiện lỗi `Invalid argument`; dữ liệu export thật cùng folder vẫn được track.
4. Chạy strict build, 16 unit tests và validation meta-KB/Agent.
5. Commit, push `main`, đối chiếu local HEAD với `refs/heads/main` trên remote.
6. Ghi bằng chứng publish, commit lần cuối và push lại.

Nếu remote yêu cầu quyền tương tác, push bị từ chối, xuất hiện file từ 100 MiB trở lên hoặc secret scan phát hiện credential khác, dừng trước khi gửi dữ liệu và báo đúng blocker.

## Tự review

- Không có placeholder hoặc bước phụ thuộc thông tin chưa xác định.
- Scope “toàn bộ project” và ngoại lệ credential được phân biệt rõ.
- Không tuyên bố custom Agent đã qua runtime/gold-set; chỉ meta-KB chat test đã kiểm chứng.
- Human approval và nguyên tắc không tự bind/publish Agent vẫn giữ nguyên.
