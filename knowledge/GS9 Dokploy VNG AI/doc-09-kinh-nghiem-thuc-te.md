# Kinh nghiệm thực tế và lưu ý khi triển khai

## Dựng ứng dụng nhiều thành phần trong một repo (monorepo)

Nếu một repo chứa cả backend và frontend (ví dụ thư mục `worker/` và `frontend/` trong cùng một repo), tạo **hai Application riêng biệt**, cùng trỏ vào một repo và branch, nhưng khác nhau ở Docker File và Docker Context Path (xem [Dựng và deploy Application](doc-07-dung-va-deploy-application.md)). Nếu frontend cần biết địa chỉ của backend, truyền qua Build-time Arguments (ví dụ một biến dạng `VITE_API_BASE`) trỏ đúng vào domain của Application backend.

## Khảo sát trước khi dựng dịch vụ mới

Trước khi tạo một Application hoàn toàn mới, nên mở một dịch vụ có sẵn của team khác trên cùng hệ thống để xem họ đang theo chuẩn nào: provider nào đang dùng, cách đặt tên domain ra sao, build type nào phổ biến. Việc này giúp dịch vụ mới khớp với cách team đang làm, thay vì tự nghĩ ra một kiểu khác biệt không cần thiết.

## Đưa dữ liệu lớn vào volume khi không có quyền truy cập máy chủ trực tiếp

Volume của Application không có công cụ upload file qua giao diện (xem [Volume, biến môi trường và domain](doc-08-volume-bien-moi-truong-va-domain.md)), và cửa sổ Terminal có sẵn trên giao diện chỉ phù hợp để gõ lệnh ngắn — không thể dùng để đưa một file dung lượng lớn vào.

Một cách đã dùng thật để giải quyết tình huống này: thêm **tạm thời** một điểm cuối (endpoint) ngay trong mã nguồn của chính ứng dụng, chỉ dùng để nhận file và ghi vào đúng vị trí trên volume, kèm các điều kiện an toàn bắt buộc:

- Yêu cầu xác thực bằng một mật khẩu quản trị riêng — nếu chưa đặt mật khẩu thì từ chối mọi yêu cầu (cố tình làm chặt hơn phần lớn điểm cuối khác trong ứng dụng, vì ghi đè dữ liệu là rủi ro lớn hơn nhiều so với đọc dữ liệu).
- Kiểm tra đúng định dạng file mong đợi trước khi ghi, từ chối mọi định dạng khác.
- Ghi ra một file tạm trước, rồi đổi tên đè lên file thật — để việc ghi luôn trọn vẹn, không bị dở dang nếu quá trình bị ngắt giữa chừng.
- Ngay sau khi dùng xong, **xoá hẳn điểm cuối này khỏi mã nguồn** ở lần commit kế tiếp — không để nó tồn tại lâu dài.

Đây là một cách vòng chấp nhận được **khi bạn kiểm soát được mã nguồn của chính ứng dụng**, nhưng phải giới hạn phạm vi thật hẹp, luôn có xác thực, và gỡ bỏ ngay sau khi dùng xong.

## Những điểm chưa được thử nghiệm đầy đủ

Vài khu vực của Dokploy chưa được kiểm chứng qua sử dụng thật, nên đừng coi là đã có kết luận chắc chắn:

- Backup/restore của dịch vụ kiểu Database lên lưu trữ ngoài.
- Dịch vụ kiểu Compose (nhận trực tiếp một file `docker-compose.yml`) và kiểu Template.
- Tính năng Preview Deployments và Schedules.
- Cách Rollback (Configure Rollbacks) hoạt động trong thực tế.
- Chạy nhiều máy chủ (multi-server) hoặc máy chủ build riêng.
- Giới hạn tài nguyên (Memory/CPU Limit) có được áp dụng nghiêm ngặt hay không.

Gặp phải khu vực nào trong danh sách này thì nên tự kiểm tra kỹ trước khi dùng cho việc quan trọng, thay vì giả định nó hoạt động giống các nền tảng tương tự khác.

## Liên hệ khi gặp vướng

Những tình huống trên đều từng gặp thật khi triển khai một dự án lên Dokploy. Nếu gặp lỗi không nằm trong các mục đã nêu ở kho này, liên hệ theo bảng ở [Hỏi đáp và hỗ trợ](doc-04-hoi-dap-va-ho-tro.md).
