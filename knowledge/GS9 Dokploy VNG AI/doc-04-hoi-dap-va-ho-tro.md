# Hỏi đáp và hỗ trợ

## Câu hỏi thường gặp

**Có cần cả tài khoản GitLab lẫn Dokploy không?**
Có. Cần cả hai để hoàn tất quy trình deploy. GitLab quản lý mã nguồn và pipeline CI; Dokploy tạo và quản lý dịch vụ chạy thật.

**Có deploy được từ nhà không?**
Có, nhưng phải kết nối Global VPN trước. Cả `host.vnggames.ai` và `code.vnggames.ai` đều không truy cập được từ Internet công khai.

**Auto Push Deploy hoạt động thế nào?**
Mỗi khi bạn push một commit mới lên GitLab, Dokploy tự động kích hoạt một lần deploy mới thông qua webhook đã cấu hình sẵn. Liên hệ AIT nếu cần hướng dẫn thiết lập cụ thể cho dự án của bạn.

**SAST và Secret Detection có bắt buộc không?**
Không bắt buộc về mặt kỹ thuật, nhưng được khuyến nghị mạnh cho mọi dự án — giúp phát hiện sớm lỗ hổng bảo mật và thông tin nhạy cảm bị lỡ đưa vào code.

## Liên hệ hỗ trợ

| Vấn đề | Liên hệ |
|---|---|
| Cấp tài khoản | AI Transformation - HungHNT |
| Sự cố mạng / VPN | Team IT / Network |
| Cấu hình SSO | AI Transformation - HungHNT |
| Sự cố repository trên GitLab | AI Transformation - HungHNT |
| Sự cố dịch vụ trên Dokploy | AI Transformation - HungHNT |
