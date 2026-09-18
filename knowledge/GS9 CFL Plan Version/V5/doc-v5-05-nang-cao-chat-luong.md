# 03 — Nâng Cao Chất Lượng

> **Phân loại:** Đã kiểm chứng trực tiếp từ HTML nguồn.
>
> **Nguồn:** `CFL5_0- Plan Ver 5.0-14082026.html`
>
> **SHA-256:** `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`
>
> **Vị trí trong nguồn:** `section#quality`

## Mở đầu từ nguồn

Phiên bản này tiếp tục dự án trải nghiệm cơ bản, triển khai theo 3 hướng: thể hiện hình ảnh, cảm giác thao tác và dung lượng gói cài đặt.

## Điểm chính

- **01** — Nâng cao cảm quan hình ảnh và giao diện
- **02** — Hiệu chỉnh chi tiết cảm giác bắn súng
- **03** — Tiếp tục tối ưu dung lượng gói và tương thích máy

## Hình Ảnh & Giao Diện

**ID nhóm nguồn:** `quality-g01`

**Mã figure trong nguồn:** FIG-06

<!-- LOCAL_ASSET: image-v5-11-nang-cao-chat-luong-hud-trong-tran.jpg -->
![Nâng cao chất lượng HUD trong trận](minio://knowledge-base-prd/10012/exports/a14e9315-14dc-4bd3-8263-9d4778c12b7d.jpg)

*Chú thích ảnh trong nguồn: Nâng cao chất lượng HUD trong trận*

> **Chú thích cụm hình trong nguồn:** Ảnh so sánh trước và sau khi nâng độ phân giải (cùng cảnh, cùng máy, 1 ảnh chất lượng cao và 1 ảnh chất lượng thấp) FIG-06

### 1. Nâng cấp chất lượng quy trình trận đấu Đấu Rank

**ID nguồn:** `quality-g01-i01`

Nâng cấp toàn diện chất lượng hình ảnh trong trận. Độ phân giải game sẽ theo thiết lập chất lượng hình ảnh — khi chọn chất lượng cao nhất, độ phân giải sẽ khôi phục 1:1, đồng thời HUD trong trận được nâng cao toàn diện.

**Chi tiết bổ sung từ nguồn:**

- Độ phân giải được gộp vào mục thiết lập chất lượng hình ảnh, không đặt công tắc riêng
- Tối ưu tập hình trong trận: bổ sung Icon, giảm tỉ lệ hiển thị của chữ dựng bằng code
- Thời điểm áp dụng giống với thiết lập chất lượng hình ảnh (loading giữa các cảnh hoặc khởi động lại)

### 2. Làm mới HUD 5.0

**ID nguồn:** `quality-g01-i02`

Tiếp nối phần công việc làm mới HUD trong trận còn lại từ phiên bản 4.0.

### 3. Mặc định thay thế khi chưa tải tài nguyên Sơn Xịt

**ID nguồn:** `quality-g01-i03`

Khi chưa tải tài nguyên Sơn Xịt, hệ thống sẽ tự động dùng Sơn Xịt mặc định để hiển thị, tránh hiện trạng để trống làm gián đoạn trải nghiệm.


## Thao Tác & Cảm Giác Chơi

**ID nhóm nguồn:** `quality-g02`

### 1. Dễ làm quen hơn

**ID nguồn:** `quality-g02-i01`

Bộ tối ưu cảm giác thao tác trên di động: giảm tốc độ di chuyển, điều chỉnh giảm tốc khi trúng đạn, tăng cường hỗ trợ ngắm bắn. Phiên bản này ưu tiên triển khai "tính năng điều chỉnh hỗ trợ ngắm bắn thống nhất".

**Chi tiết bổ sung từ nguồn:**

- Nhắm thẳng vào ngưỡng làm quen của người chơi di động ở thị trường nước ngoài


## Dung Lượng & Tương Thích

**ID nhóm nguồn:** `quality-g03`

### 1. Dự án gói nhẹ tháng 9

**ID nguồn:** `quality-g03-i01`

Tiếp tục nén dung lượng gói cài đặt đầu tiên.

### 2. Tương thích Dynamic Island trên iOS

**ID nguồn:** `quality-g03-i02`

Tương thích hiển thị trên các dòng iPhone có Dynamic Island.
