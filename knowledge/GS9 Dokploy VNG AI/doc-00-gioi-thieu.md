# Dokploy là gì và vì sao VNGGames dùng

Dokploy là nền tảng triển khai (deploy) tự phục vụ (self-hosted) của VNGGames AIT. Nó cho phép bất kỳ ai trong team tự đưa dịch vụ của mình lên môi trường chạy thật (live), mà không cần chờ team Platform xử lý từng bước.

Nói đơn giản: thay vì phải nhờ team hạ tầng "deploy giúp em cái này", bạn có thể tự làm — miễn có tài khoản và đã cấu hình đúng.

## Vì sao dùng Dokploy?

- **Tự chủ:** Ai cũng có thể tự deploy dịch vụ của mình, không phải chờ team Platform.
- **Linh hoạt:** Hỗ trợ nhiều loại ứng dụng và database khác nhau, không giới hạn một công nghệ cụ thể.
- **Bảo mật sẵn có:** Quét lỗ hổng mã nguồn (SAST), phát hiện rò rỉ thông tin nhạy cảm (Secret Detection), và đăng nhập tập trung qua VNG SSO đều được tích hợp sẵn trong quy trình — không phải tự thiết lập thêm.

## Hai công cụ cốt lõi

| Công cụ | Địa chỉ | Vai trò |
|---|---|---|
| Dokploy (App Platform) | host.vnggames.ai | Tạo và quản lý dịch vụ (service) |
| GitLab | code.vnggames.ai | Quản lý mã nguồn và pipeline CI (kiểm tra/build tự động mỗi khi có thay đổi code) |

Hai công cụ này luôn đi cùng nhau: GitLab giữ mã nguồn, Dokploy lấy mã nguồn đó để chạy thành dịch vụ thật.

> **Lưu ý dùng đúng mục đích:** nền tảng này phục vụ công việc hợp pháp của công ty. Mọi hành vi lạm dụng, vi phạm chính sách bảo mật, hoặc gây hại cho hệ thống công ty — dù cố ý hay vô ý — người thực hiện phải tự chịu trách nhiệm theo quy định công ty.

## Bắt đầu từ đâu

Bốn tài liệu tiếp theo trong kho này đi theo đúng trình tự một người mới nên đọc:

1. [Điều kiện truy cập](doc-01-dieu-kien-truy-cap.md) — cần chuẩn bị gì trước khi deploy lần đầu.
2. [Quy trình triển khai](doc-02-quy-trinh-trien-khai.md) — 9 bước từ lúc có tài khoản tới lúc dịch vụ chạy thật, có tên miền công khai.
3. [Xác thực và bảo mật](doc-03-xac-thuc-va-bao-mat.md) — cách đăng nhập và các lớp bảo mật đang có.
4. [Hỏi đáp và hỗ trợ](doc-04-hoi-dap-va-ho-tro.md) — câu hỏi thường gặp và liên hệ khi cần giúp đỡ.

Nếu team bạn đang dùng bộ công cụ AI hỗ trợ code có tên GigiKit (lệnh dạng `/gk:...` trong Claude Code), còn có thêm [Triển khai qua GigiKit](doc-05-trien-khai-qua-gigikit.md) — cách deploy lên Dokploy bằng dòng lệnh, dành cho developer.
