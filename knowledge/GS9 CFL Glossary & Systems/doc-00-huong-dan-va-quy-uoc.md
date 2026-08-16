# Hướng dẫn và quy ước — KB Glossary & Systems

> **Phiên bản:** draft-01 · **Trạng thái:** draft · **Hiệu lực:** chưa chốt
> **Mức:** P3 nội bộ phổ biến · **Chủ sở hữu:** *chưa gán* · **Nguồn:** soạn mới 15/08/2026

Đây vừa là trang mở đầu của KB, vừa là **format mẫu** cho 4 KB còn thiếu khác. Ai soạn nội dung cho `Event Calendar & Brief`, `Runbook & Known Issues`, `CS FAQ & Policy` hay `GM Policy & Sanction` đều theo đúng quy ước dưới đây.

## KB này là gì

Từ điển thuật ngữ chính thức: tên vũ khí, tên hệ thống, tên chế độ chơi, tiền tệ, và quy tắc viết. Đây là **nguồn chuẩn về cách gọi tên**, không phải nơi mô tả cơ chế gameplay.

Ai dùng: `Player Communications` (soạn patch note, thông báo), `CS Copilot` (trả lời người chơi). Không có nó thì Agent tự chế tên hệ thống — lỗi này không có cách nào phát hiện tự động.

## Header bắt buộc

Mọi file `.md` mở đầu bằng đúng khối này, không bỏ trường nào:

```markdown
> **Phiên bản:** draft-01 · **Trạng thái:** draft · **Hiệu lực:** chưa chốt
> **Mức:** P3 nội bộ phổ biến · **Chủ sở hữu:** <team> · **Nguồn:** <file gốc + ngày trích>
```

Header nằm trong nội dung nên **đi vào chunk và hiện ra trong `Nguồn tham khảo`** khi Agent trả lời. Đó là lý do nó bắt buộc: người đọc câu trả lời biết ngay thông tin còn draft hay đã chốt.

| Trường | Giá trị hợp lệ |
|---|---|
| `Trạng thái` | `draft` · `approved` · `published` |
| `Mức` | `P0` · `P1 nội bộ mật` · `P2 nội bộ thường` · `P3 nội bộ phổ biến` |
| `Hiệu lực` | ngày cụ thể, hoặc `chưa chốt` |

## Quy tắc viết để chunk hoá tốt

Nội dung sẽ bị cắt thành chunk rồi mới đưa cho model. Chunk bị cắt mà mất ngữ cảnh thì Agent trả lời sai. Vì vậy:

1. **Một khái niệm một mục.** Đừng nhồi ba thuật ngữ vào một đoạn.
2. **Tiêu đề mang từ khoá người dùng thật sự gõ.** Đặt `## Bậc phẩm chất` chứ không phải `## Phân loại mục 3.2`.
3. **Không dùng đại từ trỏ ngược qua nhiều đoạn.** Viết lại danh từ, đừng viết "nó", "cái này".
4. **Không dùng bảng lồng nhau.** Bảng phẳng, mỗi hàng tự đủ nghĩa.
5. **Mỗi bảng có câu dẫn ngay trước nó** nói bảng đó là gì — vì chunk có thể chỉ chứa bảng.
6. **Ảnh dùng URI MinIO**, không dùng đường dẫn tương đối. Đường dẫn tương đối không hoạt động trên Web.

## Nhãn bắt buộc khi nạp

| Nhãn | Giá trị cho KB này |
|---|---|
| `type:` | `glossary` |
| `status:` | `draft` / `approved` |

## Checklist trước khi nạp lên Web

- [ ] Có đủ khối header, không trường nào để trống
- [ ] Không chứa PII: `openid`, `roleid`, `nickname`, lịch sử nạp
- [ ] Không chứa số liệu doanh thu hoặc ngân sách
- [ ] Không còn link tương đối `](assets/...)`
- [ ] Đã gắn nhãn `type:` và `status:`
- [ ] Tên file có tiền tố số thứ tự để giữ trật tự đọc

## Cấu hình KB khi tạo — chốt một lần, không sửa được

| Trường | Giá trị | Vì sao |
|---|---|---|
| `Loại` | `Tài liệu` | Nội dung là định nghĩa có cấu trúc, không phải cặp hỏi–đáp |
| `Chiến lược lập chỉ mục` | RAG + Wiki | Wiki cho phép duyệt từ điển theo nhóm; **khoá sau khi có nội dung** |
| Chia sẻ | `Chỉ đọc` | Từ điển là nguồn chuẩn, không để sửa tự do |

## Trạng thái hiện tại

| File | Nguồn | Trạng thái |
|---|---|---|
| `00-huong-dan-va-quy-uoc.md` | soạn mới | draft |
| `01-thuat-ngu-vu-khi.md` | sinh từ `01_weapons_usage.csv` + `02_weapon_name_map.csv` | draft, **có phát hiện lỗi dữ liệu cần xử lý** |

Còn thiếu: thuật ngữ chế độ chơi, tiền tệ, sự kiện, giao diện; tên tiếng Việt/tiếng Trung của các dòng skin; quy tắc viết hoa và cách chèn tên vũ khí vào câu tiếng Việt.

**KB này chưa tồn tại trên Web.** Toàn bộ đang là bản nháp cục bộ, giống cách `GS9 CFL Plan Version` được dựng trước rồi mới upload.
