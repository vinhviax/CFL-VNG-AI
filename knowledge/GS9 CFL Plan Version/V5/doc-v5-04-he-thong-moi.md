# 02 — Hệ Thống Mới

> **Phân loại:** Đã kiểm chứng trực tiếp từ HTML nguồn.
>
> **Nguồn:** `CFL5_0- Plan Ver 5.0-14082026.html`
>
> **SHA-256:** `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`
>
> **Vị trí trong nguồn:** `section#system`

## Mở đầu từ nguồn

Về hệ thống, phiên bản này có 3 trọng tâm: nâng cấp toàn diện trải nghiệm hệ thống Đấu Rank, củng cố chuỗi hướng dẫn người chơi mới, và trau chuốt chi tiết hệ thống xã hội và phát triển nhân vật.

## Điểm chính

- **01** — Nâng cấp trọn bộ trải nghiệm Đấu Rank, ưu tiên cảm giác ghép trận và kết toán
- **02** — Củng cố chuỗi trận đầu tiên của người chơi mới, giảm tỉ lệ rời bỏ ngay từ đầu
- **03** — Trau chuốt nhiều điểm trải nghiệm về xã hội, phát triển nhân vật và kho đồ

## Nâng cấp trải nghiệm Đấu Rank

**ID nhóm nguồn:** `system-g01`

**Mã figure trong nguồn:** FIG-05

Sau khi Đấu Rank Kinh Tế lên sóng ở phiên bản tháng 6, hệ thống Đấu Rank bước vào giai đoạn tối ưu. Phiên bản này cải tổ có hệ thống về giao diện, ghép trận, cách hiển thị phần thưởng, trải nghiệm người dùng mới.

<!-- LOCAL_ASSET: image-v5-09-trang-ket-toan-dau-rank-phien-ban-moi.jpg -->
![Trang kết toán Đấu Rank phiên bản mới](minio://knowledge-base-prd/10012/44438f3c-3436-453e-83e8-3f95f4db444b/a376d9e6-bf7d-43d3-a277-d4d4f5354efc.jpg)

*Chú thích ảnh trong nguồn: Trang kết toán Đấu Rank phiên bản mới*

<!-- LOCAL_ASSET: image-v5-10-hien-thi-tien-trinh-nhiem-vu-vu-khi-mua-giai.jpg -->
![Hiển thị tiến trình nhiệm vụ vũ khí mùa giải](minio://knowledge-base-prd/10012/15d22802-5d0a-4dfc-96dc-1260b0d0d6d0/6da643a3-c9aa-49b5-931c-a775f425b85f.jpg)

*Chú thích ảnh trong nguồn: Hiển thị tiến trình nhiệm vụ vũ khí mùa giải*

> **Chú thích cụm hình trong nguồn:** Ảnh chụp giao diện Đấu Rank phiên bản mới FIG-05

### 1. Cải tiến giao diện Đấu Rank

**ID nguồn:** `system-g01-i01`

Cải tiến giao diện Đấu Rank, phiên bản hiện tại chưa có tính năng sức mạnh chiến đấu, các hiển thị liên quan sẽ được ẩn đi.

### 2. Cảnh báo thời gian ghép trận

**ID nguồn:** `system-g01-i02`

Khi ghép trận quá 30 giây, hiển thị thông báo thân thiện cho người chơi, gợi ý thử chế độ khác, tránh việc chờ đợi quá lâu gây rời bỏ.

**Chi tiết bổ sung từ nguồn:**

- Mỗi loại Đấu Rank có thể cấu hình ngưỡng riêng
- Sau khi hiển thị 5 giây, thông báo sẽ tự động quay lại thành "Thời gian ghép trận dự kiến"

### 3. Tối ưu hiển thị phần thưởng Đấu Rank

**ID nguồn:** `system-g01-i03`

Tiến trình nhiệm vụ vũ khí mùa giải mở rộng từ "chỉ hiển thị trong Sổ Tay Mùa Giải" sang hiển thị cả ở sảnh Đấu Rank và trang kết toán, đồng thời luôn hiển thị mục tiêu phần thưởng.

**Chi tiết bổ sung từ nguồn:**

- Khi chưa đạt điều kiện, phần thưởng hiển thị bằng hình tĩnh để giữ cảm giác mục tiêu
- Khi có thể nhận sẽ thêm hiệu ứng vòng sáng và nút nhận, nhấn vào sẽ chuyển đến Sổ Tay Mùa Giải

### 4. Điều chỉnh phần thưởng Đấu Rank

**ID nguồn:** `system-g01-i04`

Điều chỉnh cấu trúc phần thưởng Đấu Rank (cấu hình bảng), phương án cụ thể đang được lên kế hoạch.

### 5. Logic chọn bản đồ Đấu Rank

**ID nguồn:** `system-g01-i05`

Luật chọn bản đồ Đấu Rank quay về phương án của bản Trung Quốc: bậc điểm thấp chọn ngẫu nhiên bản đồ trực tiếp, bậc điểm cao khôi phục cơ chế bình chọn "chọn 1 trong 10", đội ngũ thiết kế sẽ cấu hình mốc điểm.

### 6. Tối ưu trải nghiệm người dùng mới trong Đấu Rank

**ID nguồn:** `system-g01-i06`

Sửa lỗi phân mảnh bậc điểm trong trải nghiệm Đấu Rank của người dùng mới. Trước đây người chơi có số đuôi ID 00–04 không có "trận ấm áp" AI, khiến bậc điểm của họ dừng ở khoảng 1200 điểm, trong khi người chơi khác đã đạt 1400–1500 điểm, hai nhóm không thể ghép trận với nhau, khiến nhóm trước phải chờ ghép trận rất lâu.

**Chi tiết bổ sung từ nguồn:**

- Thống nhất chiến lược triển khai AI cho người dùng mới, xóa bỏ khác biệt theo dải số ID
- Rút ngắn thời gian chờ ghép trận Đấu Rank của người dùng mới

### 7. Tối ưu tài nguyên cá nhân hóa trong Đấu Rank

**ID nguồn:** `system-g01-i07`

Tinh giản các hiển thị cá nhân hóa dư thừa trong Đấu Rank.

### 8. Cập nhật giao diện lập đội + bản đồ mùa giải

**ID nguồn:** `system-g01-i08`

Đồng bộ giao diện lập đội theo phiên bản mới nhất của bản Trung Quốc, bao phủ lập đội Đấu Rank và Thi Đấu ở các chế độ Đặt Bom, Đồng Đội, C4 Kinh Tế, C4 Kinh Tế Tốc Độ, đồng thời bổ sung trang bản đồ mùa giải.


## Tối ưu Giải Đấu

**ID nhóm nguồn:** `system-g02`

Hệ thống Giải Đấu ở phiên bản này tập trung giải quyết tính công bằng khi ghép trận và trải nghiệm lập đội.

### 1. Vào nhóm ghép trận theo bậc điểm

**ID nguồn:** `system-g02-i01`

Nhóm ghép trận Giải Đấu được chia theo bậc thực lực, tránh việc chênh lệch thực lực quá lớn làm ảnh hưởng trải nghiệm.

**Chi tiết bổ sung từ nguồn:**

- Lấy điểm ghép trận MMR làm căn cứ phân chia
- Phiên bản đầu chia thành 5 nhóm, mỗi nhóm cách nhau 400 điểm
- Người chơi chỉ ghép trận trong nhóm của mình, không ghép qua nhóm khác
- Số lượng nhóm và khoảng cách điểm đều có thể cấu hình, để dành không gian mở rộng

### 2. Giảm mức độ thể hiện yếu tố Đấu Rank

**ID nguồn:** `system-g02-i02`

Giảm hiển thị yếu tố Đấu Rank bên trong Giải Đấu, tách biệt trải nghiệm với hệ thống Đấu Rank.

### 3. Giao diện lập đội được cập nhật theo

**ID nguồn:** `system-g02-i03`

Giao diện lập đội của Giải Đấu được đồng nhất với giao diện lập đội của Đấu Rank.


## Củng cố trải nghiệm người chơi mới

**ID nhóm nguồn:** `system-g03`

Một loạt cải tiến nhắm vào vấn đề rời bỏ ở trận đầu tiên của người chơi mới.

### 1. Tối ưu trường bắn người mới (Tàu Vận Chuyển)

**ID nguồn:** `system-g03-i01`

Tối ưu quy trình trường bắn người mới (Tàu Vận Chuyển), kèm AB-TEST để kiểm chứng hiệu quả.

### 2. Hướng dẫn người mới · Hướng dẫn cài đặt

**ID nguồn:** `system-g03-i02`

Tối ưu hướng dẫn cài đặt cho người chơi mới, giúp người chơi hoàn tất các thiết lập thao tác quan trọng trước trận đầu tiên.


## Xã hội & Hiển thị cá nhân

**ID nhóm nguồn:** `system-g04`

Một loạt tối ưu về chuỗi xã hội và hiển thị hình ảnh cá nhân.

### 1. Tối ưu danh thiếp

**ID nguồn:** `system-g04-i01`

Bao phủ toàn bộ các nơi hiển thị danh thiếp: trong trận, sảnh chờ, bạn bè, trò chuyện, chiến đội, phòng lập đội.

### 2. Tối ưu chuỗi thêm bạn trong game

**ID nguồn:** `system-g04-i02`

Đơn giản hóa quy trình thêm bạn trong game, giảm số bước thao tác để tăng tỉ lệ thêm bạn thành công, đặt nền tảng cho việc giữ chân người chơi qua yếu tố xã hội.

### 3. Popup hướng dẫn kết bạn mới

**ID nguồn:** `system-g04-i03`

Bổ sung popup hướng dẫn người chơi thêm bạn, chủ động thúc đẩy xây dựng quan hệ xã hội vào thời điểm phù hợp.

### 4. Chụp màn hình kích hoạt thành phần chia sẻ

**ID nguồn:** `system-g04-i04`

Chụp màn hình trong trận có thể kích hoạt chia sẻ trực tiếp, hỗ trợ tải về máy và chia sẻ qua Facebook.


## Phát Triển & Kho Đồ

**ID nhóm nguồn:** `system-g05`

Hoàn thiện các tính năng trong chuỗi phát triển vũ khí.

### 1. Ghép linh kiện vũ khí thông dụng

**ID nguồn:** `system-g05-i01`

Tính năng ghép linh kiện vũ khí thông dụng, giải quyết vấn đề mảnh vũ khí giá trị thấp, bị trùng lặp không thể sử dụng, đồng thời giúp người chơi bỏ lỡ chu kỳ hoạt động vẫn có cách để có đủ vũ khí hoàn chỉnh.

**Chi tiết bổ sung từ nguồn:**

- Nâng cao tỉ lệ sử dụng tổng thể của tài nguyên linh kiện
- Giảm bớt cảm giác bực bội khi bỏ lỡ hoạt động là mất linh kiện vĩnh viễn

### 2. Trực quan hóa tiến trình ghép mảnh

**ID nguồn:** `system-g05-i02`

Hiển thị trực tiếp tiến trình ghép mảnh vũ khí/đạo cụ ngay trong popup nhận thưởng.

### 3. Chuyển Weapon Laboratory

**ID nguồn:** `system-g05-i03`

Chuyển "Weapon Laboratory" từ bản Trung Quốc và bản địa hóa. Người chơi có thể dùng thử vũ khí mới và tham gia đánh giá, hệ thống đánh giá đổi từ bình luận văn bản sang chấm điểm 1–5.

**Chi tiết bổ sung từ nguồn:**

- 3 lớp phản hồi: dùng thử vũ khí + chấm điểm + thả tim
- Số lượt thả tim được làm mới mỗi ngày
- Mang vũ khí dùng thử vào trận đủ số lần quy định sẽ nhận thêm lượt thả tim
- Hiển thị kết quả thống kê sau khi kết thúc bình chọn


## Cập nhật hệ thống khác

**ID nhóm nguồn:** `system-g06`

### 1. Triển khai chế độ ở sảnh Arcade 5.0

**ID nguồn:** `system-g06-i01`

Sảnh Arcade ra mắt lối vào chế độ mới của phiên bản này.

### 2. Làm mới hình lối vào Arcade

**ID nguồn:** `system-g06-i02`

Sửa lỗi làm mới hình lối vào Arcade, đảm bảo hình ảnh lối vào khớp với nội dung thực tế.

### 3. Tối ưu AI

**ID nguồn:** `system-g06-i03`

Tối ưu tên, ảnh đại diện, nhân vật, cấu hình vũ khí của AI, nâng cao độ giống người thật.

### 4. Loại nhiệm vụ mới

**ID nguồn:** `system-g06-i04`

Bổ sung 2 loại luật xét nhiệm vụ, ngăn chặn việc lập phòng để cày nhiệm vụ: "Hoàn thành 1 trận ở chế độ chỉ định" cần đấu đến trang kết toán, thoát giữa chừng sẽ không tính; "Tham gia 1 trận ở chế độ chỉ định" chỉ cần tham gia là được tính, cả hai đều loại trừ phòng tự tạo.

### 5. Tối ưu giao tiếp trong trận

**ID nguồn:** `system-g06-i05`

Thống nhất và bản địa hóa hệ thống giao tiếp chiến thuật trong trận. Hợp nhất nội dung hiển thị và cách phát ra của tin nhắn nhanh và tin nhắn bộ đàm, kèm giọng nói nhân vật và cung cấp bản địa hóa 4 ngôn ngữ.

**Chi tiết bổ sung từ nguồn:**

- Tin nhắn chung có thời gian hồi 10 giây, gửi liên tiếp tối đa 4 tin
- Loại bỏ các thông tin chiến thuật trùng lặp ý nghĩa, đưa thông tin thường dùng lên vị trí trước
- Bổ sung thêm nhiều cách diễn đạt chiến thuật, ví dụ "Tôi solo", "Ném khói qua điểm", "Tôi mang C4"
