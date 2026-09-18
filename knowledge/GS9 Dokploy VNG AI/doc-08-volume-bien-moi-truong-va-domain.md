# Volume, biến môi trường và domain

## Volume và dữ liệu

### Gắn volume

Tab Advanced → Volumes → Add Volume. Có 3 kiểu: Bind Mount, Volume Mount (named volume), File Mount.

### Bẫy quyền ghi khi dùng named volume

Named volume mặc định thuộc quyền `root`. Nếu Dockerfile chạy ứng dụng bằng một user không phải root (ví dụ dòng `USER node`), container **sẽ không ghi được vào volume và bị lỗi ngay lúc khởi động** (lỗi quyền truy cập bị từ chối).

Cách khắc phục — tạo sẵn thư mục với đúng quyền ngay trong image, để volume mới kế thừa đúng quyền đó:

```dockerfile
RUN mkdir -p /data && chown node:node /data
VOLUME ["/data"]
USER node
```

Cách này chỉ đúng với **named volume**. Nếu dùng bind mount (gắn trực tiếp một thư mục có sẵn trên máy chủ), quyền của thư mục đó trên máy chủ mới là cái quyết định — phải tự chỉnh quyền ở máy chủ, hoặc bỏ dòng `USER` để chạy bằng root.

### Volume của Application không có công cụ quản lý file

Mục Volumes trên giao diện chỉ hiện bảng tên/đường dẫn kèm nút sửa và xóa — **không có trình quản lý file, không upload được qua giao diện, và không có backup tự động** (backup/restore tự động chỉ có sẵn ở loại dịch vụ Database, không áp dụng cho Application). Muốn đưa một file dung lượng lớn vào volume mà không có quyền truy cập trực tiếp vào máy chủ thì cần một cách vòng khác — xem ví dụ thật ở [Kinh nghiệm thực tế](doc-09-kinh-nghiem-thuc-te.md), hoặc liên hệ AIT nếu gặp tình huống này.

## Biến môi trường, build args và secret

Tab Environment có 3 ô riêng biệt, mục đích khác nhau hoàn toàn — dễ nhầm nếu không biết trước:

| Ô | Có tác dụng lúc nào | Dùng cho |
|---|---|---|
| Environment Settings | Lúc ứng dụng đang chạy (runtime) | Biến ứng dụng đọc trong lúc hoạt động |
| Build-time Arguments | Lúc build image | Biến `ARG` khai trong Dockerfile |
| Build-time Secrets | Lúc build image | Secret không muốn để lại dấu vết trong các lớp (layer) của image |

**Nếu ứng dụng dùng Vite hoặc Create React App:** biến môi trường kiểu `VITE_*` bị nhúng cứng vào bundle ngay lúc build — ứng dụng **không đọc được chúng lúc đang chạy**. Muốn đổi giá trị (ví dụ đổi địa chỉ API), phải khai lại ở **Build-time Arguments** rồi **build lại image**; chỉ restart ứng dụng là không đủ, giá trị cũ vẫn còn nguyên trong bundle đã build sẵn.

Khung nhập biến là một trình soạn thảo có đánh số dòng, định dạng mỗi dòng là `KEY=value`. Có nút hình con mắt để ẩn/hiện giá trị, nhưng khi bật hiện thì **giá trị hiện ra ở dạng chữ thường, không tự che như ô mật khẩu** — cẩn thận khi chia sẻ màn hình hoặc chụp ảnh lúc đang mở ô này.

## Domain và SSL

Tab Domains → Add Domain, các trường cần điền:

| Trường | Ví dụ |
|---|---|
| Host | tên miền hoặc subdomain muốn dùng |
| Path | `/` |
| Container Port | cổng ứng dụng đang lắng nghe **bên trong** container |
| HTTPS | Bật, chọn Certificate Provider |
| Certificate Provider | Let's Encrypt |

Nếu chưa có domain riêng, `nip.io` là một dịch vụ DNS công cộng miễn phí: ghép bất kỳ tên nào với `<địa chỉ IP>.nip.io` sẽ tự động trỏ về đúng địa chỉ IP đó, không cần cấu hình DNS gì thêm — tiện để dựng nhanh một dịch vụ thử nghiệm.

> **Cảnh báo an toàn:** gắn domain — kể cả dạng `nip.io` — nghĩa là ứng dụng đã công khai ra Internet, và Let's Encrypt sẽ cấp một chứng chỉ hợp lệ xác nhận điều đó. Đừng deploy ứng dụng có cơ chế "không đặt mật khẩu thì cho phép tất cả" lên một domain công khai — đặc biệt nếu ứng dụng đó có dữ liệu thật của người dùng.

## Xem tiếp

[Kinh nghiệm thực tế và lưu ý khi triển khai](doc-09-kinh-nghiem-thuc-te.md)
