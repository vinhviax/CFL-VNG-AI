# Hướng dẫn và quy ước — KB CS FAQ & Policy

> **Phiên bản:** draft-01 · **Trạng thái:** draft · **Hiệu lực:** chưa chốt
> **Mức:** P3 nội bộ phổ biến · **Chủ sở hữu:** *chưa gán — cần Trưởng nhóm CS* · **Nguồn:** soạn mới 15/08/2026

KB này gỡ bế tắc cho `GS9 CFL CS Copilot` — Agent duy nhất hiện **không có KB và không có tool nào**.

## Khác biệt quan trọng: KB này phải chọn `Loại: FAQ`

| | `Tài liệu` | **`FAQ`** ← chọn cái này |
|---|---|---|
| Đơn vị nội dung | đoạn văn bị cắt thành chunk | **một cặp hỏi–đáp = một đơn vị** |
| Truy hồi | khớp đoạn, có thể mất ngữ cảnh | khớp câu hỏi, trả nguyên câu trả lời |
| Hợp với | tài liệu tường thuật | câu hỏi lặp đi lặp lại của người chơi |

**Chọn sai không sửa được** — `Loại` khoá sau khi KB có nội dung. Nội dung CS về bản chất là hỏi–đáp lặp lại, nên `FAQ` đúng hơn.

Hệ quả: nội dung phải viết thành **cặp câu hỏi – câu trả lời**, không viết thành bài.

## Khuôn một mục FAQ

```markdown
### Q: <câu hỏi viết đúng như người chơi hay hỏi>

**Đáp:** <câu trả lời gửi được cho người chơi, không cần sửa>

- **Nhóm:** tài khoản | nạp thẻ | vật phẩm | lỗi kỹ thuật | xử phạt | sự kiện
- **Cần xác minh:** <thông tin CS phải hỏi trước khi trả lời, nếu có>
- **Chuyển tiếp khi:** <điều kiện phải đẩy lên GM hoặc kỹ thuật>
- **Nguồn:** <chính sách hoặc thông báo làm căn cứ>
```

Ba trường cuối là thứ phân biệt một FAQ dùng được với một FAQ gây hại: nếu thiếu `Chuyển tiếp khi`, Agent sẽ tự tin trả lời cả những ca đáng ra phải đẩy lên người.

## Quy tắc viết câu hỏi

1. **Viết đúng cách người chơi gõ**, kể cả sai chính tả phổ biến — đó là thứ retrieval phải khớp. Ví dụ hỏi "nạp tiền không nhận được đồ" chứ không phải "Sự cố giao dịch chưa hoàn tất".
2. **Một câu hỏi một mục.** Đừng gộp "nạp thẻ lỗi và mất đồ" vào một mục.
3. **Thêm biến thể cách hỏi** vào cùng mục nếu người chơi hay hỏi nhiều kiểu.
4. **Câu trả lời gửi được ngay**, không viết kiểu ghi chú nội bộ.
5. **Không hứa thời gian xử lý** nếu chính sách chưa quy định.

## Nhãn bắt buộc

| Nhãn | Giá trị |
|---|---|
| `type:` | `faq` hoặc `policy` |
| `status:` | `draft` / `approved` |

## Checklist trước khi nạp

- [ ] Đủ header
- [ ] Mọi mục có `Chuyển tiếp khi`
- [ ] Không chứa PII của người chơi thật trong ví dụ
- [ ] Không hứa mốc thời gian chưa được chính sách bảo chứng
- [ ] Trưởng nhóm CS đã duyệt câu trả lời

## Việc cần bạn cung cấp

Đây là KB **không bootstrap được từ dữ liệu** — phải lấy từ kinh nghiệm vận hành. Cần:

1. **Top 20–30 câu hỏi CS nhận nhiều nhất**, viết đúng như người chơi hỏi. Xuất từ hệ thống ticket nếu có; không thì nhóm CS liệt kê từ trí nhớ cũng được.
2. **Câu trả lời chuẩn** đang dùng cho từng câu đó.
3. **Ranh giới chuyển tiếp:** ca nào CS tự trả lời, ca nào đẩy GM, ca nào đẩy kỹ thuật.
4. **Chính sách nền:** hoàn tiền, đền bù, xử phạt — hiện chưa thấy tài liệu nào trong project.

Có mục 1 và 2 là tôi dựng được KB chạy thật. Mục 3 và 4 quyết định KB đó có an toàn để bật cho Agent hay không.

## Trạng thái

**Chưa có nội dung.** File này mới chỉ là format. `GS9 CFL CS Copilot` vẫn bế tắc cho tới khi có dữ liệu ở mục "Việc cần bạn cung cấp".
