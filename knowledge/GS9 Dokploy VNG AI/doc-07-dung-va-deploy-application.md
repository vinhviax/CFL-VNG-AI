# Dựng và deploy Application — cấu hình và các bẫy thường gặp

## Chọn nguồn code (Provider)

Bảy lựa chọn: GitHub, GitLab, Bitbucket, Gitea, Docker, Git (URL thuần), Drop (upload file zip).

- **GitHub/GitLab:** chọn Git provider đã kết nối sẵn ở cấp tổ chức (mục Settings → Git Providers), rồi chọn đúng repo và branch. Repo private vẫn thấy được nếu app đã được cấp quyền truy cập.
- **Drop:** upload trực tiếp một file zip. Nhanh cho lần thử đầu tiên, nhưng **mỗi lần sửa code phải upload tay lại từ đầu — không có deploy tự động**. Không phù hợp cho dự án còn đang phát triển liên tục.

## Build Type

Sáu lựa chọn: Dockerfile, Railpack, Nixpacks, Heroku Buildpacks, Paketo Buildpacks, Static.

Với **Dockerfile**, có 3 ô cần điền:

| Ô | Ví dụ | Ý nghĩa |
|---|---|---|
| Docker File | `worker/Dockerfile` | Đường dẫn tới file, tính từ gốc repo |
| Docker Context Path | `worker` | Thư mục dùng làm build context |
| Docker Build Stage | (để trống nếu không cần) | Với Dockerfile nhiều giai đoạn (multi-stage), để trống nghĩa là build tới giai đoạn cuối cùng |

> **Quan trọng với repo chứa nhiều ứng dụng (monorepo):** Context Path phải là đúng thư mục con chứa ứng dụng đó, không phải gốc repo. Nếu để context là gốc mà Dockerfile viết `COPY package.json ./`, lệnh đó sẽ copy nhầm file ở gốc repo thay vì file thật của ứng dụng. Ví dụ thật: một repo có cả thư mục `worker/` (backend) và `frontend/`, mỗi Application phải trỏ context riêng vào đúng thư mục của nó.

## Trigger và Watch Paths

- **Trigger Type:** On Push hoặc On Tag.
- **Watch Paths:** giới hạn chỉ deploy khi có file trong đường dẫn khai báo bị thay đổi. Hữu ích khi một repo chứa nhiều ứng dụng — ví dụ đặt `worker/**` cho backend và `frontend/**` cho web, để push code ở một bên không kéo theo build lại toàn bộ.

## Vòng đời deploy — nơi dễ tốn thời gian nhất

### Autodeploy bật sẵn nhưng không tự chạy

Dù công tắc Autodeploy đang bật, push code lên nhánh chính rồi chờ vẫn **không thấy deployment mới nào xuất hiện** — kể cả sau vài phút. Danh sách Deployments vẫn dừng ở commit cũ.

**Luôn tự vào giao diện Dokploy và bấm Deploy bằng tay sau khi push code — đừng ngồi chờ tự động chạy.** Mỗi Application có sẵn một Webhook URL riêng (dạng `https://host.vnggames.ai/api/deploy/<token>`), có thể gọi thủ công từ hệ thống CI để thay thế bước bấm tay, nhưng cách này chưa được kiểm chứng đầy đủ.

### Build xong không có nghĩa là container đang chạy code mới

Đây là điểm dễ tốn thời gian nhất khi mới dùng Dokploy. Deployment hiện trạng thái **"Done"**, log build sạch đẹp (thấy rõ các bước copy source và build đang chạy, không phải lấy từ cache) — nhưng gọi thử ứng dụng vẫn thấy đúng hành vi của **code cũ**.

**Cách kiểm tra chắc chắn:** vào tab Logs, nhìn dòng trạng thái container — nó hiển thị dạng "Up X phút" hoặc "Up X giờ". Nếu khoảng thời gian đó **dài hơn** thời điểm bạn vừa bấm deploy, nghĩa là container **chưa hề được thay mới**, vẫn là container cũ đang chạy.

Bảng đối chiếu hiệu lực thật của từng thao tác (đã kiểm chứng bằng thao tác thật, không phải suy đoán từ tài liệu):

| Thao tác | Kết quả thật |
|---|---|
| Deploy | Build ra image mới. **Không tự động thay** container đang chạy. |
| Reload | Có tác dụng ở lần dùng đầu tiên; những lần sau thường **không có tác dụng** gì. |
| **Stop → Start** | **Luôn luôn** thay container bằng bản mới. Ứng dụng gián đoạn khoảng 15 giây trong lúc chuyển đổi. |

**Quy trình deploy an toàn, nên làm theo đúng thứ tự: Deploy → chờ trạng thái Done → Stop → Start → kiểm tra lại.**

### Cách xác nhận chắc chắn container đã chạy code mới

Đừng chỉ tin vào trạng thái hiển thị trên giao diện. Hai cách chắc chắn hơn:

1. **Xem log lúc container khởi động** — dòng log in ra lúc boot (ví dụ bước chạy migration, cổng đang lắng nghe, thông báo khởi tạo cron) luôn có mốc thời gian, nên biết ngay container vừa được tạo mới khi nào.
2. **Gọi thử một chức năng mà code mới trả kết quả khác code cũ**, rồi so sánh trực tiếp. Đừng dừng lại ở việc kiểm tra "ứng dụng có phản hồi không" (health check) — ứng dụng cũ vẫn phản hồi bình thường, điều đó không chứng minh được gì về việc code đã đổi hay chưa.

## Lịch sử Deployments

Dokploy giữ lại 10 lần deploy gần nhất, xem được log build đầy đủ (bấm View), kèm commit và thời lượng build. Có sẵn các nút Kill Build, Cancel Queues, Configure Rollbacks, Clean Cache.

## Checklist — dựng Application mới

1. Xem trước một dịch vụ có sẵn của team khác trên cùng hệ thống để biết chuẩn đang dùng (domain, provider, build type) — tránh tự nghĩ ra cách khác biệt không cần thiết.
2. Create Service → Application, đặt tên và mô tả rõ ràng.
3. Chọn Provider: Git provider đã kết nối sẵn → repo → branch.
4. Chọn Build Type: Dockerfile → điền Docker File + Context Path (với monorepo: context phải là đúng thư mục con của ứng dụng).
5. Environment: điền biến chạy lúc runtime; biến kiểu build-time (ví dụ `VITE_*`) phải đặt riêng ở mục Build-time Arguments — xem [Volume, biến môi trường và domain](doc-08-volume-bien-moi-truong-va-domain.md).
6. Advanced → Volumes: gắn volume nếu ứng dụng cần lưu dữ liệu lâu dài.
7. Domains: khai Host, Container Port, bật HTTPS.
8. Chưa vội bấm deploy nếu còn secret chưa điền đầy đủ và domain sắp công khai ra Internet.
9. Deploy → chờ trạng thái Done → **Stop → Start** → kiểm tra lại bằng cách gọi thử một chức năng thật.

## Checklist — deploy một thay đổi code

1. Push code lên nhánh.
2. Vào giao diện Dokploy, bấm Deploy bằng tay (đừng chờ webhook tự bắn).
3. Chờ trạng thái Done, xem nhanh qua log build.
4. Stop → Start.
5. Vào tab Logs xác nhận container vừa khởi động lại và log lúc boot là mới.
6. Gọi thử một chức năng phản ánh đúng thay đổi vừa deploy — không dừng lại ở việc kiểm tra ứng dụng còn phản hồi hay không.

## Xem tiếp

[Volume, biến môi trường và domain](doc-08-volume-bien-moi-truong-va-domain.md)
