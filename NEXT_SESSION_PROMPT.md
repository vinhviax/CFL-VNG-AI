# Prompt bắt đầu phiên tại nhà

Copy toàn bộ khối dưới đây vào phiên Codex mới:

```text
Tiếp tục dự án CFL-VNG-AI từ repository:
https://github.com/vinhviax/CFL-VNG-AI

Nếu máy này chưa có project, clone repository. Nếu đã clone, chạy `git pull --ff-only origin main`. Làm việc tại root do `git rev-parse --show-toplevel` trả về; không giả định đường dẫn ổ J: của máy cũ.

Bắt đầu bằng cách kiểm tra `git status --short --branch`, sau đó đọc đầy đủ theo thứ tự:
1. AGENTS.md
2. HANDOFF.md
3. STATUS.md
4. PROJECT.md
5. DECISIONS.md

Chỉ mở audit liên quan khi cần bằng chứng có ngày; không nạp toàn bộ lịch sử.

Snapshot cần giữ:
- Project v3.3.0, strict gate gần nhất: 20 module, 49 PNG/URI, 60 MinIO + 60 LOCAL_ASSET, HTML offline tự chứa, 16 tests.
- Consumer Web `GS9 Knowledge VNG AI`: 20 Markdown, 0 PNG.
- Asset host `GS9 Knowledge VNG - Image Assets`: 49 PNG, 0 Markdown.
- Meta-KB `GS9 CFL Knowledge Agent`, ID `1d92448f-7ee2-46c4-b202-5efbe9cc5616`: 25/25 Markdown Hoàn tất, sharing 0.
- 6 Agent mặc định đã audit UI read-only.
- 10 custom Agent đã tạo, no-KB, sharing 0, chưa publish/share và chưa runtime/gold-set test.
- Tool actual: 7 Smart Agent dùng Ask + Think + Todo; Player Voice dùng Ask + Think; GM dùng Ask + Todo; CS Copilot là Fast Answer không có Tools tab. 9 Smart Agent có 20 loop, timeout 120s, parallel Off.
- Chat test đã kiểm chứng meta-KB trả đúng Agent/tool/Human gate; đây không phải runtime test của 10 custom Agent.
- Không có mutation live đang chạy.

An toàn bắt buộc:
- Không đọc, copy, commit hoặc hiển thị credential/token/private key. Không dùng `git add -f` để vượt `.gitignore`.
- Không tự bind các KB CFL nghiệp vụ, `Data Private Weapon` hoặc dữ liệu player vào Agent khi chưa audit owner, ACL, retention, sensitivity và freshness.
- Không tạo/sửa/publish/share/xóa Agent hoặc KB trên Web nếu tôi chưa giao rõ trong phiên mới.
- Mọi gửi tin, thay dữ liệu, account action hoặc vận hành live cần Human approval.
- Phân loại kết luận là Đã kiểm chứng / Có điều kiện / Bị chặn–Chưa xác định; không suy diễn cấu hình không thấy.

Sau khi đọc xong, hãy tóm tắt trạng thái Git + project hiện tại, nêu rõ blocker nếu có và hỏi tôi muốn tiếp tục backlog nào. Không tự chạy builder/test nếu chưa có thay đổi local cần kiểm chứng.
```

