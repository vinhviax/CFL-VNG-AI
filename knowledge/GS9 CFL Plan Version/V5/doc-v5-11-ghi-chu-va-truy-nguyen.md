# Ghi Chú Và Truy Nguyên

> **Phân loại:** Đã kiểm chứng trực tiếp từ HTML nguồn.
>
> **Nguồn:** `CFL5_0- Plan Ver 5.0-14082026.html`
>
> **SHA-256:** `593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038`
>
> **Vị trí trong nguồn:** `.note, footer`

## Ghi Chú Về Tài Liệu Này

- Phạm vi nội dung: các mục có mức ưu tiên P0 (bắt buộc làm) và P1 (cố gắng làm) trong danh sách yêu cầu phiên bản 5.0, đã loại bỏ các yêu cầu đang tạm ngưng, cùng các mục thuần về quy trình phát triển (nộp duyệt, cấu hình bảng, tích hợp tài nguyên... không có giá trị thông tin ra bên ngoài).
- Các vị trí hình được đánh số FIG-xx là hình ảnh cần bổ sung, số thứ tự tương ứng 1:1 với «Danh Sách Yêu Cầu Hình Ảnh Sách Trắng CFL5.0»; sau khi có đủ hình ảnh, tài liệu này sẽ được cập nhật đồng bộ.
- Phiên bản này chưa đánh dấu mức ưu tiên nội dung (S/A/B) và xếp hạng thương mại hóa, sẽ bổ sung sau khi xác nhận quy mô nội dung và trọng tâm truyền thông.
- Tên tiếng Anh sẽ được bổ sung sau khi đồng nghiệp bản địa hóa xác nhận, phục vụ cho đội phát hành bản địa bên ngoài sử dụng.
- Sơ đồ lịch trình phiên bản sẽ được bổ sung sau khi xác nhận thời gian lên sóng của từng nội dung.

## Dòng chân trang của nguồn

Nội Dung Phiên Bản CFL 5.0 · Chu kỳ phiên bản 22/9/2026 — 8/12/2026 Đối tượng: Đồng nghiệp phát hành / marketing của nhóm dự án · Đội phát hành bản địa bên ngoài | Tài liệu nội bộ, vui lòng không phổ biến ra ngoài

## Quy tắc bảo toàn dữ liệu khi chuyển đổi

- Giữ đủ 115 hạng mục theo đúng section, nhóm và thứ tự trong HTML.
- Giữ nguyên các mô tả giống nhau thay vì tự gộp hoặc tự sửa.
- Giữ nguyên 91 gạch đầu dòng chi tiết nằm trong 35 hạng mục có danh sách bổ sung.
- Chỉ chuẩn hóa khoảng trắng do bố cục HTML; không đổi từ ngữ hoặc số liệu.
- Tách 29 data-URI JPEG thành asset cục bộ và ghi checksum từng ảnh trong manifest.
- Ba vị trí đang chờ hình/lịch (FIG-00, FIG-11, FIG-12) được giữ là “Bị chặn — Chưa xác định”.

## Dữ kiện CSS có điều kiện

Hạng mục `Đạo cụ lên kệ trên cửa hàng web` có node mô tả rỗng trong DOM. Stylesheet nguồn khai báo fallback: **Sẽ bổ sung chi tiết sau**. Tuy nhiên selector `.item .d:empty` cũng đặt node này thành `display:none`, nên fallback được lưu để bảo toàn dữ liệu nhưng không được xem là mô tả DOM đã hiển thị chắc chắn.

## Chênh lệch số lượng trong chính nguồn

- Mở đầu section thương mại hóa ghi nguyên văn: Về thương mại hóa, phiên bản này có tổng cộng 47 nội dung, là mảng có khối lượng lớn nhất trong toàn bộ phiên bản. Trục chính là xây dựng Battle Pass S5 và hệ thống Xu CF giới hạn thời gian, kết hợp một đợt tối ưu trải nghiệm hệ thống quay thưởng.
- Cùng section đó có **46** thẻ `.item` trong DOM, trong khi phần mở đầu nêu **47** nội dung.
- Hai dữ kiện được giữ song song; không tự suy diễn rằng một thẻ luôn tương ứng đúng một nội dung thương mại hóa.

## Bản ghi có mô tả trùng trong nguồn

Phát hiện 3 nhóm mô tả xuất hiện nhiều hơn một lần. Các bản ghi này vẫn được giữ nguyên; xem `source-manifest.json` để truy nguyên từng lần xuất hiện.
- Zombie Truy Đuổi · Chuyển Kẻ Hủy Diệt từ bản Trung Quốc ↔ Anh hùng Zombie mới + cấu hình Kẻ Hủy Diệt lên sóng
- Câu quảng bá Mỗi Rút Mỗi Giảm ↔ Mỗi Rút Mỗi Giảm · Dành cho người chơi nạp vừa và nhỏ
- Hoạt động quay thưởng Siêu Đại Chiến ↔ Bao bì Siêu Đại Chiến trên Tàu Vận Chuyển

## Phạm vi chưa thực hiện

- Chưa upload bộ tài liệu này lên VNG AI Knowledge Base.
- Chưa bind bộ tài liệu với Agent nào.
- Không xác nhận trạng thái live của các hạng mục; tài liệu chỉ phản ánh HTML nguồn.
