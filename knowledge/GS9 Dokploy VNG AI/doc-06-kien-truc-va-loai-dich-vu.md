# Kiến trúc Dokploy và các loại dịch vụ

> Từ đây trở xuống (doc-06 đến doc-09) là kinh nghiệm đúc kết từ một lần triển khai dự án thật lên Dokploy trên hệ thống nội bộ VNG. Không phải tài liệu chính thức của Dokploy, nhưng là những gì thực sự xảy ra khi thao tác — dành cho ai chuẩn bị tự dựng và vận hành một ứng dụng thật trên nền tảng này.

## Dokploy là gì (nhắc lại, chi tiết hơn)

Dokploy là nền tảng triển khai tự host, mã nguồn mở — kiểu "Heroku/Vercel/Railway nhưng cài trên máy chủ của công ty". So với việc tự viết `docker-compose` và cấu hình nginx tay, Dokploy có sẵn: giao diện quản lý, tự xin chứng chỉ SSL, quản lý biến môi trường, xem log, rollback, và backup dữ liệu (cho một số loại dịch vụ nhất định).

## Kiến trúc bên dưới

- **Chạy trên Docker Swarm**, không phải lệnh `docker run` đơn giản. Dấu hiệu nhận biết: mục Cluster Settings có "Replicas", tên container có dạng `<tên-dịch-vụ>.<số-replica>.<mã-task>`.

  Điều này quan trọng vì nhiều hành vi "lạ" của Dokploy thực ra là hành vi của Swarm bên dưới — đặc biệt là chuyện **container không tự nhận image mới sau khi deploy** (xem [Dựng và deploy Application](doc-07-dung-va-deploy-application.md)).

- **Traefik** đóng vai trò reverse proxy: tự xin chứng chỉ Let's Encrypt và định tuyến request theo domain đã khai.

- **Máy chủ chạy theo giờ UTC** — hiển thị ngay ở góc giao diện. Nếu ứng dụng có tác vụ chạy theo lịch (cron) mà code viết theo giờ Việt Nam (UTC+7), tác vụ sẽ chạy lệch 7 tiếng mà **không có dấu hiệu báo lỗi nào** — chỉ phát hiện được khi để ý thời điểm thực tế nó chạy. Luôn viết lịch cron theo UTC, hoặc tự quy đổi múi giờ ngay trong code.

## Các loại dịch vụ khi tạo mới (Create Service)

| Loại | Dùng khi | Ghi chú |
|---|---|---|
| **Application** | Một ứng dụng từ Git, Docker image, hoặc file zip | Loại phổ biến nhất, dùng cho hầu hết trường hợp |
| **Database** | Postgres, MySQL, MariaDB, MongoDB, Redis | Có sẵn backup/restore — tính năng mà Application không có |
| **Compose** | Chạy nguyên một file `docker-compose.yml` có sẵn | |
| **Template** | Cài sẵn ứng dụng phổ biến (n8n, Supabase...) | |
| **AI Assistant** | — | |

> **Lưu ý khi chọn loại dịch vụ:** backup/restore tự động **chỉ có ở loại Database**. Nếu ứng dụng của bạn là Application và cần lưu dữ liệu lâu dài qua volume, dữ liệu đó **không có cơ chế backup tự động đi kèm** — xem thêm ở [Volume, biến môi trường và domain](doc-08-volume-bien-moi-truong-va-domain.md).

## Xem tiếp

[Dựng và deploy Application](doc-07-dung-va-deploy-application.md) — cấu hình chi tiết và những điểm dễ vấp nhất khi deploy một ứng dụng thật.
