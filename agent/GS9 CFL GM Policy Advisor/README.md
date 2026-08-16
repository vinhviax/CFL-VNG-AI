# GS9 CFL GM Policy Advisor

Agent tra cứu chính sách xử phạt, quy trình xử lý và tiền lệ cho GM được phân quyền. Không điều tra theo vụ, không truy cập dữ liệu người chơi, không thay đổi tài khoản.

- **Owner nghiệp vụ:** GM Lead
- **Người dùng:** Nhóm GM được phân quyền
- **KB bind:** Chưa bind — chờ tạo `GS9 CFL GM Policy & Sanction`
- **Trạng thái Web:** Tên + mô tả + System Prompt đã đổi 15/08/2026; no-KB; sharing `0`; chưa publish/share; chưa chat/runtime/gold-set test
- **Web actual — 14/08/2026:** `Hỏi người dùng`, `Lập kế hoạch (todo)`; `Suy nghĩ` không active; `20` steps / `120s` / parallel Off
- **Công cụ nguồn tương lai:** `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` trên KB policy sau khi KB tồn tại

## Vì sao đổi mục đích — 15/08/2026

Vai trò cũ `GM Case Investigator` yêu cầu **case-scoped view**: chỉ nạp bằng chứng của đúng một vụ việc. Nền tảng VNG AI không có cơ chế đó — share và bind đều ở cấp KB, không có cấp tài liệu hay cấp hàng dữ liệu. Muốn Agent "điều tra một vụ" thì phải bind một KB chứa dữ liệu của **mọi** vụ, tức là vi phạm least privilege và kéo dữ liệu người chơi vào phạm vi truy hồi.

Vai trò mới tách hai phần:

| Phần | Cách xử lý |
|---|---|
| Tri thức chính sách (ổn định, không PII) | KB `GS9 CFL GM Policy & Sanction` — bind được |
| Bằng chứng từng vụ (biến thiên, có PII) | **Tệp đính kèm trong hội thoại**, không qua KB |

Nhờ vậy Agent vẫn hỗ trợ được công việc thật của GM mà không cần một KB chứa dữ liệu người chơi.
Cơ sở: `docs/superpowers/specs/2026-08-15-kb-architecture-design.md` mục 10.2.
