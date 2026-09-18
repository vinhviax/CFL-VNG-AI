# Xác thực và bảo mật

## Đăng nhập tập trung qua VNG SSO

Tất cả hệ thống trong bộ Dokploy dùng chung **VNG SSO – OIDC** làm cổng xác thực duy nhất — không có mật khẩu riêng cho từng hệ thống.

| Hệ thống | Cách đăng nhập |
|---|---|
| Dokploy (host.vnggames.ai) | Đăng nhập qua VNG SSO |
| GitLab (code.vnggames.ai) | Đăng nhập qua VNG SSO |
| Dịch vụ bạn tự host (`*.hub.vnggames.ai`) | Có sẵn mẫu tích hợp SSO (SSO Template), dùng nếu dịch vụ của bạn cần đăng nhập người dùng |

**Muốn tích hợp SSO vào dịch vụ của mình?** Dùng SSO Template có sẵn và liên hệ team AIT để được hỗ trợ cấu hình (đầu mối: AI Transformation - HungHNT).

## Các lớp bảo mật đang có

| Tính năng | Mô tả | Cách bật |
|---|---|---|
| VNGCorp Whitelist | Chặn truy cập từ Internet công khai | Áp dụng sẵn ở tầng hạ tầng, không cần tự làm |
| VNG SSO – OIDC | Xác thực tập trung cho mọi dịch vụ `*.hub.vnggames.ai` | Liên hệ team AIT để đăng ký |
| SAST | Quét lỗ hổng bảo mật tĩnh trong mã nguồn | Cấu hình trong phần cài đặt repository trên GitLab |
| Secret Detection | Phát hiện secret/thông tin đăng nhập lỡ commit vào code | Cấu hình trong phần cài đặt repository trên GitLab |
| Basic Auth | Yêu cầu nhập username/password khi truy cập URL công khai của ứng dụng | Cấu hình trong tab Advanced của Dokploy |

> SAST và Secret Detection **không bắt buộc về mặt kỹ thuật**, nhưng được khuyến nghị mạnh cho mọi dự án để đảm bảo an toàn thông tin.

## Muốn thêm một lớp bảo mật đơn giản?

Có thể thêm HTTP Basic Auth (yêu cầu nhập username/password) vào URL công khai của ứng dụng mà **không cần sửa code** — cấu hình trực tiếp trong tab Advanced của Dokploy.

## Xem tiếp

[Hỏi đáp và hỗ trợ](doc-04-hoi-dap-va-ho-tro.md) — câu hỏi thường gặp và đầu mối liên hệ theo từng loại vấn đề.
