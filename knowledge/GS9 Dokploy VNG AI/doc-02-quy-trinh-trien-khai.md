# Quy trình triển khai — 9 bước, 3 giai đoạn

Đây là hướng dẫn đầy đủ để đưa một ứng dụng lên chạy thật trên Dokploy, từ lúc chưa có gì tới lúc có tên miền công khai truy cập được.

| Giai đoạn | Các bước | Làm gì |
|---|---|---|
| Giai đoạn 1 — Chuẩn bị | Bước 1–4 | Xin tài khoản, kết nối mạng, đăng nhập |
| Giai đoạn 2 — Cấu hình dự án | Bước 5–7 | Tạo dịch vụ, kết nối GitLab, đẩy code kèm bảo mật |
| Giai đoạn 3 — Deploy và công bố | Bước 8–9 | Deploy ứng dụng và gắn tên miền công khai |

## Giai đoạn 1 — Chuẩn bị (Bước 1–4)

**Bước 1 — Xin cấp tài khoản**
Gửi yêu cầu cấp quyền cho cả hai hệ thống: `host.vnggames.ai` và `code.vnggames.ai`. Xem chi tiết ở [Điều kiện truy cập](doc-01-dieu-kien-truy-cap.md).

**Bước 2 — Kết nối đúng mạng**
Đảm bảo đang dùng VNGCorp Wi-Fi, mạng dây, hoặc Global VPN trước khi mở một trong hai công cụ.

**Bước 3 — Đăng nhập**
Đăng nhập vào `host.vnggames.ai` và `code.vnggames.ai` bằng **VNG SSO – OIDC** (tài khoản công ty, không có mật khẩu riêng cho từng hệ thống).

**Bước 4 — Chờ duyệt quyền**
Sau khi yêu cầu được duyệt, bạn có toàn quyền sử dụng cả hai hệ thống.

## Giai đoạn 2 — Cấu hình dự án (Bước 5–7)

**Bước 5 — Tạo dịch vụ trong dự án của bạn**
Trên `host.vnggames.ai`, vào đúng dự án (project) của bạn và tạo một Service bên trong đó.

**Bước 6 — Kết nối GitLab với Dokploy**
Đăng ký một GitLab OAuth Application trên `code.vnggames.ai` và liên kết nó với Dokploy. Bước này cho phép Dokploy truy cập vào repository của bạn để lấy mã nguồn đưa vào pipeline deploy.

**Bước 7 — Đẩy code và bật quét bảo mật**
Đẩy (push) code lên GitLab, sau đó bật hai tính năng:

| Tính năng | Tác dụng |
|---|---|
| SAST | Quét mã nguồn tìm lỗ hổng bảo mật đã biết mỗi lần push |
| Secret Detection | Phát hiện API key, token, thông tin đăng nhập bị lỡ commit vào code |

Khi tạo project mới trên GitLab (`code.vnggames.ai` → New project → Create blank project), kéo xuống mục **Project Configuration** ở cuối trang và bật cả hai tuỳ chọn trên **trước khi** bấm Create project.

## Giai đoạn 3 — Deploy và công bố (Bước 8–9)

**Bước 8 — Deploy dịch vụ**
Trong Application/Service của bạn trên Dokploy, bấm **Deploy** để chạy lần deploy đầu tiên (thủ công). Đợi build xong và xác nhận dịch vụ đang chạy.

> Muốn tự động deploy lại mỗi khi push code mới (không cần bấm tay), xem phần Auto Deploy — liên hệ AIT nếu cần hướng dẫn thiết lập cụ thể.

**Bước 9 — Gắn tên miền**
Trong Application, vào tab **Domains** và bấm **Add Domain**. Có hai lựa chọn:

- **Lựa chọn 1 — traefik.me (HTTP):** miễn phí, Dokploy tự sinh subdomain dạng `*.traefik.me`, không cần cấu hình gì thêm — chỉ cần khai đúng cổng (port) ứng dụng đang lắng nghe.

  | Trường | Giá trị |
  |---|---|
  | Host | Dokploy tự điền |
  | Container Port | Cổng ứng dụng của bạn (ví dụ: 3000) |
  | HTTPS | Để tắt (off) |

  > `traefik.me` là dịch vụ HTTP công khai, **không hỗ trợ SSL/HTTPS**. Có bật tuỳ chọn HTTPS/chứng chỉ cũng không có tác dụng gì.

- **Lựa chọn 2 — nip.io (HTTPS):** lựa chọn thứ hai nếu cần HTTPS. Liên hệ AIT nếu cần hướng dẫn cấu hình chi tiết cho lựa chọn này.

## Xem tiếp

- [Xác thực và bảo mật](doc-03-xac-thuc-va-bao-mat.md) — hiểu thêm về SSO và các lớp bảo mật đang bật.
- [Hỏi đáp và hỗ trợ](doc-04-hoi-dap-va-ho-tro.md) — vướng ở bước nào thì liên hệ ai.
