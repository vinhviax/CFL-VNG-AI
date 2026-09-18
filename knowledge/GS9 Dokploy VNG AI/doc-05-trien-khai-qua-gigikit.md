# Triển khai qua GigiKit (dành cho developer dùng Claude Code)

> Trang này dành riêng cho developer đang dùng bộ công cụ AI hỗ trợ code **GigiKit** trong Claude Code (các lệnh dạng `/gk:...`). Nếu team bạn không dùng GigiKit, có thể bỏ qua trang này và deploy trực tiếp trên giao diện Dokploy theo [Quy trình triển khai](doc-02-quy-trinh-trien-khai.md).

GigiKit có sẵn một skill tên `gk:deploy-dokploy`, cho phép deploy và quản lý ứng dụng lên Dokploy ngay từ trong phiên làm việc với Claude Code, thông qua công cụ dòng lệnh `@lmes/dokploy-cli`.

## Kích hoạt skill

```
/gk:deploy-dokploy
/gk:deploy-dokploy "deploy my app to staging"
```

**Phạm vi skill này lo được:** đăng nhập, tạo project/app/environment/database, deploy, đồng bộ biến môi trường (env variable).

**Phạm vi skill này KHÔNG lo:** cài đặt server Dokploy, cấu hình DNS/SSL, thiết lập Docker Swarm, hay dựng pipeline CI/CD — những việc này vẫn cần làm thủ công hoặc nhờ AIT.

## Chuẩn bị

Cài CLI:
```
npm install -g @lmes/dokploy-cli
dokploy --version
```

## Đăng nhập

Skill tự kiểm tra `dokploy verify` trước. Nếu chưa đăng nhập, nó sẽ hỏi server URL và API token, rồi chạy:
```
dokploy authenticate -u <SERVER_URL> -t <API_TOKEN>
```

Chưa có token? Liên hệ team DevOps/AIT để lấy API token và tên project trước khi làm tiếp.

## Skill làm được gì

Sau khi đăng nhập, skill hiện menu hành động:

| Hành động | Mô tả |
|---|---|
| Deploy an app | Deploy từ một thư mục build cục bộ lên app đã có hoặc app mới |
| Create project/app | Tạo project và application mới |
| Create database | Tạo MariaDB, PostgreSQL, MySQL, MongoDB, hoặc Redis |
| Manage env vars | Kéo (pull) hoặc đẩy (push) biến môi trường |

Khi deploy, skill luôn lấy đúng project/app ID từ API trước, rồi chạy deploy với đầy đủ flag tường minh — không dùng chế độ hỏi tương tác:

```
dokploy app deploy -a <applicationId> -p <projectId> -e <environmentId> --from-folder ./dist -y
```

> Chạy `dokploy app deploy` mà thiếu flag `-a`, `-p`, `-e` sẽ kích hoạt chế độ hỏi tương tác — và chế độ đó bị lỗi thoát mã 130 trong Claude Code. Skill đã tự xử lý để tránh việc này; nếu tự gõ lệnh tay, nhớ luôn truyền đủ 3 flag.

## Các lệnh hay dùng

**Project & App**
```
dokploy project create -n "MyProject" -d "Description" -y
dokploy app create -p <projectId> -n "my-app" -d "Description" -y
dokploy app deploy -a <appId> -p <projectId> -e <envId> --from-folder ./dist -y
```

**Database**
```
dokploy database postgres create -p <projectId> -n "my-pg" --databaseName mydb --databasePassword secret123 -y
dokploy database mysql create -p <projectId> -n "my-mysql" --databaseName mydb --databasePassword secret123 -y
dokploy database mongo create -p <projectId> -n "my-mongo" --databaseName mydb --databasePassword secret123 -y
dokploy database redis create -p <projectId> -n "my-redis" --databasePassword secret123 -y
```

**Biến môi trường**
```
dokploy env pull .env.production   # kéo về máy
dokploy env push .env.production   # đẩy lên server
```

**Tạo environment**
```
dokploy environment create -p <projectId> -n "staging" -d "Staging env" -y
```

## Sau khi deploy xong

Skill tự xác nhận URL deploy và tạo/cập nhật `docs/deployment.md`:
```
# Deployment
## Platform: Dokploy
## Server: <DOKPLOY_URL>
## Deploy Command: dokploy app deploy -a <appId> --from-folder ./dist -y
## Environment Variables: dokploy env pull .env.production
```

## Xử lý lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| `dokploy: command not found` | Chạy `npm install -g @lmes/dokploy-cli` |
| Invalid token | Chạy lại `dokploy authenticate` với token mới |
| Project not found | Kiểm tra qua API: `curl -s -H "x-api-key: <TOKEN>" "<URL>/api/project.all"` |
| App deploy failed | Xem log build; kiểm tra đường dẫn `--from-folder` có tồn tại không |

## Lưu ý bảo mật

- API token không bao giờ được in ra output hay commit vào git.
- Luôn kiểm tra file `.env` đã nằm trong `.gitignore` trước khi deploy.
- Skill từ chối các yêu cầu vượt phạm vi hoặc cố hỏi lộ thông tin nội bộ của chính nó.
