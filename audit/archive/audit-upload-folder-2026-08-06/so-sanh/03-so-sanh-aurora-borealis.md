# So sánh Aurora và Borealis

Mã dữ liệu kiểm thử: `AUDIT-KB-FOLDER-20260806`.

Aurora và Borealis cùng phục vụ đội vận hành nhưng tối ưu cho hai nhu cầu khác nhau. Aurora phù hợp khi tốc độ phản hồi là ưu tiên chính; Borealis phù hợp khi cần lưu trữ và tổng hợp dữ liệu dài hạn.

| Tiêu chí | Aurora | Borealis |
|---|---:|---:|
| Yêu cầu tối đa mỗi phút | 100 | 40 |
| Thời gian lưu lịch sử | 30 ngày | 365 ngày |
| Báo cáo theo quý | Không | Có |
| Ưu tiên chính | Tốc độ | Phân tích dài hạn |

## Khuyến nghị tổng hợp

Chọn Aurora cho trực sự cố thời gian thực. Chọn Borealis cho phân tích xu hướng và báo cáo quản trị. Nếu một nhóm cần cả hai mục tiêu, có thể dùng Aurora ở lớp tiếp nhận và chuyển dữ liệu đã chuẩn hóa sang Borealis để lưu trữ dài hạn.

