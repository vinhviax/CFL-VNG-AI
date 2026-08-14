# Audit export dữ liệu Private Weapon — 14/08/2026

## Phạm vi và trạng thái

- **Đã kiểm chứng local:** HTML nguồn tồn tại; JSON raw và 7 CSV tồn tại tại `J:\My Drive\CFL\KB VNG\Data Private Weapon`.
- **Đã kiểm chứng cấu trúc:** 7 CSV có tổng 388.820 dòng dữ liệu; UTF-8 hợp lệ; mọi record có đúng số cột; record đầu/cuối của từng file khớp JSON nguồn.
- **Không thực hiện live:** chưa upload JSON/CSV vào `Knowledge VNG AI`, `Knowledge VNG - Image Assets` hoặc KB khác.
- Audit này không lưu `openid`, `roleid`, nickname hoặc giá trị giao dịch cụ thể.

## Nguồn

| Hạng mục | Giá trị |
|---|---|
| HTML nguồn | `C:\Users\CPU13114\Downloads\cfm-sung-theo-thoi-gian.html` |
| Kích thước HTML | 25.993.269 byte |
| SHA-256 HTML | `1063bdfac47a74b6aaf86d1459fb5d8308430fcdbde91e586ca1b28a86daca2e` |
| JSON raw | `J:\My Drive\CFL\KB VNG\Data Private Weapon\cfm-sung-theo-thoi-gian.raw.json` |
| Kích thước JSON raw | 25.953.259 byte |
| SHA-256 JSON raw | `1a2c72ba6606b1acb3fab8def89dd5314cf03e59f2e16efd35d8c5f6a1b23a0b` |
| Dataset nhúng đã tách | `WE`, `NM`, `US`, `ORG`, `USERS`, `CB` |
| Dependency ngoài | HTML có tham chiếu `cfm-hub-data-cb-weapons.js`; file không tồn tại cạnh HTML khi kiểm tra và không nằm trong export |

## CSV đã xuất

| File | Dòng dữ liệu | Cột | Byte | SHA-256 |
|---|---:|---:|---:|---|
| `01_weapons_usage.csv` | 1.227 | 41 | 208.065 | `d00a16d2239659e60800716bf5d22370d68fdb5bc64832e00cde0d2fe5aaa096` |
| `02_weapon_name_map.csv` | 2.599 | 2 | 103.687 | `8314ecd619bf67089dd02861b6ed09fdfeb903fdecac43b0fa9dbae1d1cd1006` |
| `03_sample_users.csv` | 4 | 7 | 282 | `e89e06988249dd51244e993e8d4d7a296a03708c7a4c98ca059498ccad8f5952` |
| `04_sample_user_weapons.csv` | 45 | 12 | 2.754 | `86d43b09251bcedae7d8b8819a40fef51ba5aa7cab845630c1a938074cb65873` |
| `05_issued_items_timeseries.csv` | 1.206 | 81 | 389.351 | `246be13202c9bf8c2f379249bd473ab90aea60d1b92dcf9936b5316a62cad586` |
| `06_users_detailed.csv` | 8.148 | 12 | 5.777.654 | `9588ea5fe613441f3f1833003ae8a3305bff6f82b927c43e0760a53ee9293f7e` |
| `07_users_cb.csv` | 375.591 | 6 | 18.910.137 | `27857225f22e923c99bb2330ef9fd119d21d792558dd34781092ec0e009b9f25` |
| **Tổng** | **388.820** | — | **25.391.930** | — |

## Ý nghĩa và giới hạn

- Các CSV là bảng raw phục vụ phân tích/nạp thử; không phải nội dung hướng dẫn của bộ 20 Markdown.
- Dữ liệu có trường định danh và hành vi như `openid`, `roleid`, nickname, hạng thành viên, lịch sử nạp và số trận. Phải xem toàn bộ thư mục là dữ liệu private.
- Nếu mở bằng Excel, nên nhập qua **Data → From Text/CSV** và đặt cột ID/text thành **Text** để tránh tự đổi kiểu.
- Nếu đưa vào Knowledge VNG, ưu tiên KB private chuyên dụng và kiểm thử dung lượng/parser trên bản tối thiểu trước; không mặc định nạp vào consumer tài liệu `Knowledge VNG AI`.

## Gate đã chạy

Lượt xác minh ngày 14/08/2026 kết thúc `PASS` với đúng 7 CSV, tổng 388.820 dòng, UTF-8 hợp lệ, record đầu/cuối khớp JSON nguồn và không có file `.partial`.
