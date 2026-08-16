# 01 — Cách Chơi Mới

> **Phân loại:** Đã kiểm chứng trực tiếp từ HTML nguồn.
>
> **Nguồn:** `CFL5_0- Plan Ver 5.0-14082026.html`
>
> **SHA-256:** `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`
>
> **Vị trí trong nguồn:** `section#gameplay`

## Mở đầu từ nguồn

Về cách chơi, phiên bản này xoay quanh 2 trục chính: một là C4 Kinh Tế nâng cấp từ 1.0 lên 2.0, bổ sung hoàn thiện phần "chuẩn bị ngoài trận"; hai là mở rộng nội dung Arcade và PVE, dùng các cách chơi nhẹ nhàng để phục vụ nhóm người chơi không thiên về thi đấu.

## Điểm chính

- **01** — C4 Kinh Tế bước vào 2.0: hoàn thiện phối súng và phối skin ngoài trận
- **02** — 3 cách chơi Arcade mới + BOSS Thế Giới, phục vụ người chơi nhẹ nhàng và giải trí
- **03** — Nội dung tuyến Zombie tiếp tục cập nhật, Kẻ Hủy Diệt và BUFF mới xuất trận

## C4 Kinh Tế 2.0

**ID nhóm nguồn:** `gameplay-g01`

**Mã figure trong nguồn:** FIG-01

Sau khi C4 Kinh Tế ra mắt lần đầu ở phiên bản tháng 6, phiên bản này bước vào giai đoạn 2: bổ sung khâu chuẩn bị ngoài trận, người chơi có thể hoàn tất phối súng và phối skin trước khi vào trận.

<!-- LOCAL_ASSET: image-v5-01-giao-dien-phoi-sung-ngoai-tran-ban-tieng-viet.jpg -->
![Giao diện phối súng ngoài trận (bản tiếng Việt)](minio://knowledge-base-prd/10012/87e52d64-4fdc-4cc7-b0e5-05a2deae6e19/e842591e-d702-42bf-9df0-a93ec7ef7196.jpg)

*Chú thích ảnh trong nguồn: Giao diện phối súng ngoài trận (bản tiếng Việt)*

<!-- LOCAL_ASSET: image-v5-02-giao-dien-doi-skin-ngoai-tran.jpg -->
![Giao diện đổi skin ngoài trận](minio://knowledge-base-prd/10012/28c849fb-cd96-4801-9923-27aeac3d2bfd/5a83a74f-a03c-44b6-91a9-b6d27880db9f.jpg)

*Chú thích ảnh trong nguồn: Giao diện đổi skin ngoài trận*

> **Chú thích cụm hình trong nguồn:** Giao diện phối súng ngoài trận, giao diện đổi skin ngoài trận FIG-01

### 1. Phối súng ngoài trận

**ID nguồn:** `gameplay-g01-i01`

C4 Kinh Tế bổ sung tính năng phối súng ngoài trận. Người chơi có thể thiết lập sẵn phương án mua súng trước khi vào trận, đầu trận sẽ tự động mua theo phương án đã đặt, giảm đáng kể áp lực thời gian và thao tác mua súng trong trận.

**Chi tiết bổ sung từ nguồn:**

- Giảm ngưỡng hiểu và thao tác của trận đấu kinh tế, phục vụ trực tiếp việc giữ chân người chơi mới
- Kèm theo hướng dẫn phối súng ngoài trận cho người chơi mới, kích hoạt khi vào tab Đấu Rank Kinh Tế hoặc Thi Đấu

### 2. Đổi skin ngoài trận

**ID nguồn:** `gameplay-g01-i02`

C4 Kinh Tế hỗ trợ phối skin ngoài trận. Trên tiền đề chỉ số được đồng nhất để đảm bảo công bằng, vẫn giữ lại khả năng thể hiện cá tính qua ngoại hình cho người chơi — vừa đảm bảo công bằng thi đấu, vừa không làm giảm giá trị hiển thị của skin trả phí.

**Chi tiết bổ sung từ nguồn:**

- Chỉ số đồng nhất, ngoại hình tự do, cân bằng giữa công bằng và thương mại hóa

### 3. Hướng dẫn phối súng ngoài trận cho người chơi mới

**ID nguồn:** `gameplay-g01-i03`

Hướng dẫn phối súng ngoài trận đi kèm trận đấu kinh tế 2.0. Kích hoạt khi người chơi vào tab "Đấu Rank Kinh Tế" hoặc "Thi Đấu", diễn ra sau bước hướng dẫn cài đặt, giúp người chơi mới hiểu cơ chế phối súng ngoài trận đặc thù của trận đấu kinh tế.

**Chi tiết bổ sung từ nguồn:**

- Điểm kích hoạt được đẩy lên ngay sau bước hướng dẫn cài đặt, giảm ngưỡng hiểu ở trận đầu tiên


## C4 Kinh Tế · Tối ưu trải nghiệm

**ID nhóm nguồn:** `gameplay-g02`

Tối ưu có hệ thống các vấn đề trải nghiệm trận đấu được ghi nhận sau khi phiên bản tháng 6 lên sóng.

### 1. Giới hạn mua đồ ném / vũ khí mỗi hiệp

**ID nguồn:** `gameplay-g02-i01`

Bổ sung giới hạn số lượng đồ ném và vũ khí có thể mua trong 1 hiệp, tránh việc dồn vật phẩm phá vỡ cân bằng hiệp đấu.

### 2. Rơi đồ ném và kềm cắt

**ID nguồn:** `gameplay-g02-i02`

Sau khi hy sinh, đồ ném và kềm gỡ bom có thể rơi ra và được nhặt lại, giúp tài nguyên chiến thuật luân chuyển trong hiệp đấu, tăng thêm chiều sâu đấu trí ở giai đoạn cuối hiệp.

### 3. Tối ưu hiển thị thu nhập kinh tế

**ID nguồn:** `gameplay-g02-i03`

Thu nhập trận đấu đổi sang hiển thị theo phe, đồng thời hiển thị số tiền tối thiểu sẽ có ở hiệp sau, giúp quyết định mua súng rõ ràng hơn.

### 4. Tối ưu AI Nhân Hóa

**ID nguồn:** `gameplay-g02-i04`

Mở rộng hệ thống AI Nhân Hóa trong trận đấu kinh tế. Trước đây chỉ có 2 loại "trận ấm áp" là trận người mới và trận hồi quy, lần này bổ sung thêm 2 kịch bản "trận ấm áp khi thất bại liên tục" và "trận cân bằng", giúp việc can thiệp của AI sát với hoàn cảnh thực tế của người chơi hơn.

**Chi tiết bổ sung từ nguồn:**

- Trận người mới: áp dụng cho toàn bộ người chơi dưới 1500 điểm, độ khó thấp nhất
- Trận hồi quy: độ khó cao hơn một chút, chỉ diễn ra 1 trận
- Trận ấm áp khi thất bại liên tục: kích hoạt khi người chơi thua liên tiếp, tự động điều chỉnh độ khó để đảm bảo thắng, giới hạn 2500 điểm
- Trận cân bằng: kích hoạt khi ghép trận với người thật quá lâu không thành, độ khó cố định, giới hạn 3000 điểm
- Chủng loại vũ khí của AI mở rộng từ súng trường tấn công, súng tiểu liên sang súng bắn tỉa và súng shotgun

### 5. Tối ưu giao diện xem trận

**ID nguồn:** `gameplay-g02-i05`

Sắp xếp lại cấp độ thông tin ở góc nhìn xem trận, giúp người xem dễ nắm bắt tình trạng kinh tế và trang bị.

### 6. Tối ưu hiển thị thông tin vũ khí

**ID nguồn:** `gameplay-g02-i06`

Tối ưu cách hiển thị dữ liệu vũ khí ở giao diện mua súng, tham khảo các sản phẩm thi đấu cùng thể loại để cung cấp thông tin vũ khí đầy đủ hơn, giúp người chơi đưa ra lựa chọn rõ ràng hơn.


## Mở rộng cách chơi Arcade

**ID nhóm nguồn:** `gameplay-g03`

**Mã figure trong nguồn:** FIG-02

Phiên bản này chuyển 3 cách chơi Arcade đã trưởng thành từ bản Trung Quốc sang, làm phong phú nguồn nội dung giải trí. Sảnh Arcade đồng thời triển khai chế độ và làm mới hình lối vào.

<!-- LOCAL_ASSET: image-v5-03-joker.jpg -->
![Joker](minio://knowledge-base-prd/10012/9ec32770-acd5-40e2-89ab-78a3eda9d037/d96484a0-8b58-44ab-9a90-c77cb5ce002d.jpg)

*Chú thích ảnh trong nguồn: Joker*

<!-- LOCAL_ASSET: image-v5-04-khong-gian-mat-trong-luc.jpg -->
![Không Gian Mất Trọng Lực](minio://knowledge-base-prd/10012/3b68beaa-27a7-46a9-a219-38bb3b4766d9/0cf97622-d912-4a35-b803-d12ac6521ff2.jpg)

*Chú thích ảnh trong nguồn: Không Gian Mất Trọng Lực*

<!-- LOCAL_ASSET: image-v5-05-parkour-ky-thuat.jpg -->
![Parkour-Kỹ Thuật](minio://knowledge-base-prd/10012/9c61b0cf-2758-43e2-ac96-c09a775ab8b7/5835b8dc-6e7d-40fd-bfee-343e5f55601f.jpg)

*Chú thích ảnh trong nguồn: Parkour-Kỹ Thuật*

> **Chú thích cụm hình trong nguồn:** Ảnh chụp cách chơi Joker, Không Gian Mất Trọng Lực, Parkour-Kỹ Thuật FIG-02

### 1. Joker

**ID nguồn:** `gameplay-g03-i01`

Chuyển cách chơi Arcade "Joker" từ bản Trung Quốc, phân phối qua gói tải giải trí, không làm tăng dung lượng gói cài đặt chính.

**Chi tiết bổ sung từ nguồn:**

- Cả lối vào Arcade ở sảnh chờ và lối vào bên trong Arcade đều có hình ảnh riêng
- Bổ sung giới thiệu chế độ Joker trong phần giải thích luật chơi

### 2. Không Gian Mất Trọng Lực

**ID nguồn:** `gameplay-g03-i02`

Chuyển cách chơi Arcade "Không Gian Mất Trọng Lực" từ bản Trung Quốc, mang lại trải nghiệm đối kháng khác biệt trong môi trường trọng lực thấp, phân phối qua gói tải giải trí.

**Chi tiết bổ sung từ nguồn:**

- Cả lối vào Arcade ở sảnh chờ và lối vào bên trong Arcade đều có hình ảnh riêng
- Bổ sung giới thiệu chế độ Không Gian Mất Trọng Lực trong phần giải thích luật chơi

### 3. Parkour Kỹ Thuật

**ID nguồn:** `gameplay-g03-i03`

Chuyển cách chơi giải trí "Parkour-Kỹ Thuật" từ bản Trung Quốc, bản đồ là "Mê Cung" theo luật giới hạn thời gian. Nội dung chạy nhảy đua tốc độ nhẹ nhàng, làm phong phú lựa chọn giải trí phi đối kháng.

**Chi tiết bổ sung từ nguồn:**

- Đội 8 người, dùng chung hệ thống lập đội với các chế độ khác
- Trang ghép trận tối đa 20 người, hiển thị thanh tiến trình và tên bản đồ
- Mỗi ngày 3 lượt nhận thưởng
- Bổ sung tab riêng giới thiệu cách chơi trong phần giải thích luật chơi giải trí


## PVE · BOSS Thế Giới

**ID nhóm nguồn:** `gameplay-g04`

**Mã figure trong nguồn:** FIG-03

Tiếp nối khung cách chơi BOSS Thế Giới từ phiên bản tháng 6, kỳ này ra mắt con BOSS thứ hai.

<!-- LOCAL_ASSET: image-v5-06-boss-the-gioi-varanus.jpg -->
![BOSS Thế Giới Varanus](minio://knowledge-base-prd/10012/0a4fa00d-eea1-4f79-8518-7c148a3f1bfb/e84d8b86-9792-4801-9b26-01862dd38937.jpg)

*Chú thích ảnh trong nguồn: BOSS Thế Giới Varanus*

> **Chú thích cụm hình trong nguồn:** Hình ảnh BOSS Varanus + ảnh chụp chiến đấu FIG-03

### 1. BOSS Thế Giới: Varanus

**ID nguồn:** `gameplay-g04-i01`

Chính thức chuyển nội dung PVE nổi tiếng từ bản Trung Quốc "BOSS Thế Giới-Varanus". Người chơi lập đội thử thách BOSS khổng lồ, cần né tránh kỹ năng của nó; sau khi bị hút vào bên trong BOSS, phải vừa né kỹ năng vừa tấn công tim, phá vỡ tim hoặc hết thời gian sẽ trở về mặt đất.

**Chi tiết bổ sung từ nguồn:**

- 3 mức độ khó: Thường không giới hạn số lần, Khó và Địa Ngục giới hạn số lần mỗi ngày
- Độ khó Thường thưởng bằng mở rương; Khó và Địa Ngục thưởng bằng lật bài
- Có thể tiêu Gem để lật bài thêm và nhận EXP
- PVE có 2 lối vào từ sảnh chờ và Arcade, khi chuyển chế độ hình nền sảnh chờ sẽ thay đổi đồng bộ


## Cập nhật nội dung Zombie

**ID nhóm nguồn:** `gameplay-g05`

**Mã figure trong nguồn:** FIG-04

Tuyến nội dung Zombie ở phiên bản này chủ yếu là cấu hình và chuyển từ bản khác sang, mở rộng kho nhân vật và cách chơi BUFF.

<!-- LOCAL_ASSET: image-v5-07-giao-dien-rut-buff-zombie-toi-thuong.jpg -->
![Giao diện rút BUFF Zombie Tối Thượng](minio://knowledge-base-prd/10012/96cc3e8d-c760-4680-858e-185c9a37cee6/f4171360-a093-41a5-8019-4b542c9981dc.jpg)

*Chú thích ảnh trong nguồn: Giao diện rút BUFF Zombie Tối Thượng*

<!-- LOCAL_ASSET: image-v5-08-hien-thi-buff-don-trong-tran.jpg -->
![Hiển thị BUFF đơn trong trận](minio://knowledge-base-prd/10012/ae6db75d-761e-4e02-9c6c-e0805d4a046d/e9ed05c9-118b-465b-9a33-1f37d7a3b182.jpg)

*Chú thích ảnh trong nguồn: Hiển thị BUFF đơn trong trận*

> **Chú thích cụm hình trong nguồn:** Hình ảnh Kẻ Hủy Diệt Xanh, giao diện BUFF Zombie Tối Thượng FIG-04

### 1. Cách chơi BUFF Zombie Tối Thượng

**ID nguồn:** `gameplay-g05-i01`

Chế độ Zombie Tối Thượng bổ sung cách chơi BUFF (lần này chỉ ra mắt BUFF đơn). Đầu mỗi hiệp sẽ tự động rút cho mỗi bên 1 BUFF, chỉ có hiệu lực trong hiệp đó, sang hiệp sau sẽ rút lại, giúp tổ hợp chiến thuật mỗi trận không lặp lại.

**Chi tiết bổ sung từ nguồn:**

- Trang rút có hiệu ứng cuộn biểu tượng, có thể xem tên và mô tả chi tiết của BUFF
- Biểu tượng BUFF của 2 phe hiển thị cố định phía trên màn hình trong trận
- Một số BUFF diện rộng có kèm hiệu ứng khung cảnh
- BUFF đặc biệt "Diệt Vong & Hy Vọng": khi đầy tiến trình sẽ kích hoạt biến hình, Ma biến thành Ma Mẹ Tối Thượng, Lính Đánh Thuê biến thành Thợ Săn Tối Thượng, kèm hiệu ứng giáng thế toàn màn hình

### 2. Zombie Truy Đuổi · Chuyển Kẻ Hủy Diệt từ bản Trung Quốc

**ID nguồn:** `gameplay-g05-i02`

Cách chơi Zombie Truy Đuổi đưa vào Ma Mẹ Tối Thượng "Kẻ Hủy Diệt Xanh" từ bản Trung Quốc, là phiên bản Kẻ Hủy Diệt cấp cao, bao phủ 2 giai đoạn: biến hình thành Ma lần đầu và biến hình thành Kẻ Hủy Diệt lần hai.

**Chi tiết bổ sung từ nguồn:**

- Giai đoạn biến hình hỗ trợ cấu hình
- Anh hùng Zombie mới và Kẻ Hủy Diệt được cấu hình lên sóng đồng thời

### 3. Anh hùng Zombie mới + cấu hình Kẻ Hủy Diệt lên sóng

**ID nguồn:** `gameplay-g05-i03`

Cách chơi Zombie Truy Đuổi đưa vào Ma Mẹ Tối Thượng "Kẻ Hủy Diệt Xanh" từ bản Trung Quốc, là phiên bản Kẻ Hủy Diệt cấp cao, bao phủ 2 giai đoạn: biến hình thành Ma lần đầu và biến hình thành Kẻ Hủy Diệt lần hai.

**Chi tiết bổ sung từ nguồn:**

- Giai đoạn biến hình hỗ trợ cấu hình
- Anh hùng Zombie mới và Kẻ Hủy Diệt được cấu hình lên sóng đồng thời

### 4. Điều chỉnh thời lượng trận Zombie ngắn

**ID nguồn:** `gameplay-g05-i04`

Giảm số hiệp trong chế độ Zombie, rút ngắn thời lượng mỗi trận để phù hợp với thời gian rảnh rỗi trên di động.
