# Gắn kho tri thức tạm cho 4 Agent chưa có nguồn — 17/08/2026

**Loại:** mutation live trên Web `vnggames.ai/kb/agents`, tenant `10012`
**Người yêu cầu:** người dùng (phiên 17/08/2026)
**Công cụ:** `claude-in-chrome` (Chrome thật, session sẵn có)

## 1. Bối cảnh

DEC-058 (16/08/2026) ghi nhận 4/10 Agent custom ở `kb_selection_mode: none`:
`CS Copilot`, `Economy Offer Analyst`, `GM Policy Advisor`, `Player Communications`.

Nguyên nhân gốc **không phải thiếu quyền mà là thiếu nguồn** — KB nghiệp vụ tương ứng
chưa có nội dung thật hoặc chưa tồn tại:

| Agent | KB nghiệp vụ đích | Trạng thái nguồn 17/08/2026 |
|---|---|---|
| `CS Copilot` | `GS9 CFL CS FAQ & Policy` | chỉ có `doc-00-huong-dan-va-quy-uoc.md` (file định dạng), chưa có nội dung |
| `Economy Offer Analyst` | `GS9 CFL Item Catalog` | chưa tồn tại; chờ tách khỏi `GS9 CFL Item Profile` (dữ liệu P0) |
| `GM Policy Advisor` | `GS9 CFL GM Policy & Sanction` | chưa tồn tại, chưa có thư mục local |
| `Player Communications` | `GS9 CFL Event Calendar & Brief` | chưa tồn tại, chưa có thư mục local |

Người dùng quyết định: **hoãn soạn nội dung, gắn tạm KB gần đúng nhất hiện có**, phần
thiếu ghi lại chuẩn bị sau.

## 2. Trạng thái trước khi sửa — đọc trực tiếp từ Web

Mở dialog cấu hình từng Agent, tab `Kho tri thức`. Cả 4 đều ở
**`Không dùng kho tri thức`** (nút được tô cam), khớp với DEC-058.

Agent ID đọc được trong dialog: `GS9 CFL Player Communications` =
`4b8e6d78-9217-4dbb-8ab3-919628a48440`.

## 3. Thay đổi đã thực hiện

Mỗi Agent: đổi sang `Kho tri thức đã chọn` → chọn đúng một KB → `Lưu`.
Cả 4 lần đều nhận toast **`Đã cập nhật trợ lý`**.

| Agent | KB đã gắn | Lý do chọn |
|---|---|---|
| `GS9 CFL Player Communications` | `GS9 CFL Plan Version` | nội dung sự kiện/kế hoạch là thứ cần soạn thông báo |
| `GS9 CFL Economy Offer Analyst` | `GS9 CFL Data Daily` | có số liệu nạp/kinh tế theo ngày, gần nghiệp vụ nhất |
| `GS9 CFL CS Copilot` | `GS9 Knowledge VNG AI` | fallback nền tảng, không có nguồn CS nào gần đúng |
| `GS9 CFL GM Policy Advisor` | `GS9 Knowledge VNG AI` | fallback nền tảng, không có nguồn GM nào gần đúng |

Không đụng bất kỳ trường nào khác: mode chạy, model, tool, prompt, chia sẻ,
`Loại tệp hỗ trợ` (giữ `Tất cả loại tệp`), `Chỉ truy hồi khi được nhắc` (giữ Tắt).

## 4. Xác minh sau khi sửa — đọc lại trực tiếp, không tin toast

Mở lại dialog `Kho tri thức` của cả 4 Agent:

| Agent | Chế độ đọc được | KB đọc được |
|---|---|---|
| `GS9 CFL Player Communications` | `Kho tri thức đã chọn` | `GS9 CFL Plan Version` |
| `GS9 CFL Economy Offer Analyst` | `Kho tri thức đã chọn` | `GS9 CFL Data Daily` |
| `GS9 CFL CS Copilot` | `Kho tri thức đã chọn` | `GS9 Knowledge VNG AI` |
| `GS9 CFL GM Policy Advisor` | `Kho tri thức đã chọn` | `GS9 Knowledge VNG AI` |

**Kết luận: Đã kiểm chứng** ở mức cấu hình. Chất lượng runtime vẫn
**Bị chặn–Chưa xác định** — chưa chat-test Agent nào.

## 5. Việc còn treo sau lượt này

Bốn KB nghiệp vụ vẫn cần soạn nội dung thật; khi có, phải đổi binding từ KB tạm
sang KB đúng:

1. `GS9 CFL CS FAQ & Policy` — cần top câu hỏi CS, câu trả lời chuẩn, ranh giới
   chuyển cấp GM/kỹ thuật, chính sách hoàn tiền/đền bù.
2. `GS9 CFL GM Policy & Sanction` — cần bảng điều khoản xử phạt, quy trình, tiền lệ.
3. `GS9 CFL Event Calendar & Brief` — cần lịch sự kiện, brief đã duyệt, mẫu thông báo.
4. `GS9 CFL Item Catalog` — cần tách khỏi `GS9 CFL Item Profile`, phải rà dữ liệu P0
   trước khi tách.

## 6. Ghi chú kỹ thuật gặp trong lượt này

- **Dialog cấu hình Agent render ở document chính**, nhưng danh sách Agent nằm trong
  shadow DOM qiankun — `read_page` không thấy danh sách, chỉ thấy dialog.
- **Toạ độ ảnh chụp không khớp toạ độ click.** Viewport thật `2080x1032`, ảnh chụp trả về
  `1568x778`; phải nhân toạ độ đọc từ ảnh với `1.3265`. Không nhân thì click lệch sang
  Agent khác — đã từng mở nhầm dialog `FPA Analyst`.
- **Phím `Escape` đóng cả dialog, mất thay đổi chưa lưu.** Muốn đóng dropdown chọn KB thì
  click vào vùng trống trong dialog, đừng bấm Escape.
- Sau khi đóng dialog, thao tác gõ đầu tiên vào ô tìm kiếm hay bị nuốt — cần tách thành
  lượt riêng hoặc gõ lại.
