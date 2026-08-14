# Hướng dẫn thiết kế Knowledge Base cho LiveOps game

> Tài liệu tham khảo dành cho LiveOps, Game Operations, CS, GM và các nhóm phối hợp vận hành game.  
> Cập nhật: 07/08/2026  
> Hướng dẫn thao tác công cụ chi tiết: [Sổ tay tạo và vận hành Knowledge Base](../so-tay-tao-knowledge-base-v3.md)

## 1. Mục tiêu

Knowledge Base cho LiveOps giúp tập trung kiến thức đang nằm rải rác trong tài liệu sự kiện, SOP, ticket, bảng cấu hình và kinh nghiệm của người trực ca. Khi được tổ chức đúng, KB có thể hỗ trợ:

- Tra cứu nhanh quy tắc và thông số sự kiện.
- Hướng dẫn xử lý sự cố theo đúng thứ tự.
- Chuẩn hóa câu trả lời của CS hoặc GM.
- Hỗ trợ onboarding và bàn giao ca trực.
- Giữ nguồn tham khảo, điều kiện và ngoại lệ đi cùng câu trả lời.
- Hiển thị hình minh họa như ảnh màn hình cấu hình hoặc dashboard khi nguồn ảnh được chuẩn bị đúng.

KB không thay thế hệ thống giám sát realtime, ticket system, kho cấu hình hay hệ thống lưu trữ bí mật. Dữ liệu thay đổi liên tục chỉ nên đưa vào KB khi đã có quy trình cập nhật và xác nhận độ mới.

## 2. Kiến trúc khuyến nghị

Với mỗi game, nên bắt đầu bằng hai KB riêng:

### 2.1. KB Tài liệu — kiến thức vận hành đầy đủ

KB Tài liệu là nguồn bối cảnh và quy trình chi tiết. Nội dung phù hợp gồm:

- Đặc tả và lịch vận hành sự kiện.
- Runbook mở, đóng hoặc rollback sự kiện.
- SOP xử lý sự cố.
- Patch notes, release notes và known issues.
- Reward table, item ID, currency và giới hạn economy.
- Quy trình payment, cộng bù và hoàn trả.
- Ma trận escalation và checklist bàn giao ca.
- Tài liệu onboarding cho thành viên mới.

Nên bật **RAG** để hỏi đáp theo đoạn nguồn. Chỉ bật **Wiki** khi tài liệu đã sạch, heading rõ, không có phiên bản mâu thuẫn và có người kiểm tra nội dung tổng hợp sau cập nhật.

### 2.2. KB FAQ — lớp trả lời nhanh và được kiểm soát

KB FAQ dùng cho các câu hỏi lặp lại, trong đó mỗi ý định cần một câu trả lời ngắn và nhất quán. Nội dung phù hợp gồm:

- Thời gian bắt đầu hoặc kết thúc sự kiện.
- Server, platform hoặc region được áp dụng.
- Điều kiện nhận quà.
- Lý do chưa nhận được phần thưởng.
- Thời hạn sử dụng vật phẩm sự kiện.
- Trường hợp được cộng bù hoặc chuyển cấp.
- Mã lỗi phổ biến và hướng xử lý ngắn.
- Mẫu trả lời chuẩn cho CS hoặc GM.

FAQ nên có câu hỏi chuẩn, các cách hỏi tương tự lấy từ ticket thật, câu hỏi loại trừ cho ý định dễ nhầm và câu trả lời ghi rõ phạm vi áp dụng.

## 3. LiveOps có thể dùng KB cho những bài toán nào?

| Nhóm nội dung | Ví dụ | Loại KB phù hợp |
|---|---|---|
| Vận hành sự kiện | Thời gian, server áp dụng, nhiệm vụ, reward, reset | Tài liệu |
| Runbook/SOP | Mở event, đóng event, rollback, kiểm tra config | Tài liệu |
| Xử lý sự cố | Không nhận quà, leaderboard sai, server lag | Tài liệu |
| Patch và release | Nội dung phiên bản, thay đổi config, known issues | Tài liệu |
| Economy/config | Item ID, currency, reward table, giới hạn mua | Tài liệu |
| Onboarding trực ca | Trách nhiệm, công cụ, escalation, bàn giao | Tài liệu + Wiki |
| Câu hỏi người chơi | “Sự kiện kết thúc lúc nào?” | FAQ |
| Câu trả lời CS chuẩn | Mẫu trả lời, điều kiện hỗ trợ, chuyển cấp | FAQ |
| Mã lỗi phổ biến | Mã lỗi, nguyên nhân, cách xử lý ngắn | FAQ hoặc cả hai |

Ví dụ câu hỏi có thể dùng trong chat:

- Sự kiện Summer Festival áp dụng cho server nào?
- Nếu người chơi hoàn thành nhiệm vụ nhưng chưa nhận quà thì kiểm tra theo thứ tự nào?
- Ai chịu trách nhiệm escalation khi leaderboard không cập nhật?
- Cho tôi bảng reward của mốc 1–10.
- Soạn câu trả lời ticket cho người chơi chưa nhận được quà sự kiện.
- Hiển thị ảnh màn hình cấu hình leaderboard.

## 4. Khi nào chọn Tài liệu, khi nào chọn FAQ?

### Chọn Tài liệu khi

- Nội dung dài hoặc có nhiều heading.
- Cần giải thích bối cảnh, nguyên nhân và lý do.
- Có quy trình nhiều bước.
- Có bảng reward, item, server hoặc timeline.
- Có nhiều điều kiện và ngoại lệ.
- Người dùng cần xem nguồn để kiểm tra lại.
- Người đọc cần hiểu toàn bộ chủ đề, không chỉ một câu trả lời.

Ví dụ:

- SOP xử lý sự cố không nhận quà.
- Thông số sự kiện Summer Festival.
- Quy trình rollback leaderboard.
- Hướng dẫn mở và đóng event.
- Patch notes phiên bản 3.5.
- Ma trận escalation LiveOps.

### Chọn FAQ khi

- Một câu hỏi tương ứng với một câu trả lời được kiểm soát.
- Câu trả lời phải ngắn và nhất quán.
- Câu hỏi xuất hiện lặp lại trong ticket.
- Có nhiều cách diễn đạt cùng một ý định.
- Cần câu hỏi loại trừ để tránh trả lời nhầm.
- Dữ liệu nguồn đang có dạng bảng Q&A, CSV hoặc Excel.

Ví dụ:

- Sự kiện kết thúc lúc nào?
- Server mới có tham gia sự kiện không?
- Vì sao tôi chưa nhận được quà?
- Quà sự kiện có gửi qua thư không?
- Vật phẩm sự kiện có hết hạn không?
- Trường hợp nào được hỗ trợ cộng bù?

### Dùng cả hai khi

Một vấn đề vừa cần câu trả lời chuẩn, vừa cần quy trình chi tiết.

Ví dụ với tình huống **không nhận được quà sự kiện**:

- **FAQ:** câu trả lời ngắn cho CS hoặc người chơi, điều kiện đủ để được hỗ trợ và thời điểm cần chuyển cấp.
- **Tài liệu:** quy trình nội bộ kiểm tra event ID, player ID, eligibility, log, mailbox, inventory và cách cộng bù.

FAQ là lớp trả lời nhanh; Tài liệu là nguồn bối cảnh và quy trình đầy đủ. Không nên sao chép nguyên một SOP dài vào FAQ.

## 5. Cây nội dung gợi ý

```text
[GAME] LIVEOPS - DOCUMENTS
├── 00-tong-quan-va-lien-he.md
├── 01-lich-va-quy-tac-su-kien.md
├── 02-runbook-mo-dong-event.md
├── 03-xu-ly-su-co.md
├── 04-payment-va-hoan-tra.md
├── 05-reward-va-economy.md
├── 06-release-va-patch-notes.md
└── 07-escalation-va-ban-giao-ca.md

[GAME] LIVEOPS - FAQ
├── Sự kiện
├── Phần thưởng
├── Thanh toán
├── Tài khoản
├── Lỗi kỹ thuật
└── Chính sách hỗ trợ
```

Không nên trộn nhiều game vào cùng một KB nếu chúng cùng dùng các từ như “server”, “event”, “gói tháng” nhưng có quy định khác nhau. Tách theo game giúp giảm nguy cơ truy hồi nhầm.

## 6. Metadata tối thiểu cho nội dung LiveOps

Mỗi tài liệu hoặc FAQ cần ghi rõ:

- Tên game.
- Môi trường: Production, Staging hoặc Test.
- Platform và region áp dụng.
- Server hoặc nhóm server áp dụng.
- Event ID hoặc mã cấu hình liên quan.
- Thời gian bắt đầu và kết thúc kèm múi giờ.
- Phiên bản và ngày hiệu lực.
- Owner nghiệp vụ.
- Trạng thái: Draft, Active hoặc Superseded.
- Ngày kiểm tra gần nhất.

Ví dụ metadata đầu tài liệu:

```markdown
Game: Example Game
Môi trường: Production
Region: VN
Event ID: SUMMER_2026
Hiệu lực: 2026-08-10 10:00 ICT đến 2026-08-24 23:59 ICT
Owner: LiveOps Team
Phiên bản: 1.2
Trạng thái: Active
Kiểm tra gần nhất: 2026-08-09
```

## 7. Quy tắc nội dung FAQ LiveOps

- Câu hỏi chuẩn chỉ mô tả một ý định chính.
- Câu hỏi tương tự lấy từ cách người chơi hoặc CS thực sự diễn đạt, kể cả viết tắt và không dấu.
- Câu hỏi loại trừ dùng cho trường hợp gần giống nhưng phải đi sang quy trình khác.
- Câu trả lời phải nêu phạm vi, điều kiện, ngoại lệ và thời điểm chuyển cấp.
- Nếu người dùng thường tìm bằng event ID, item ID hoặc error code chỉ xuất hiện trong câu trả lời, cân nhắc index **Câu hỏi + trả lời**.
- Giữ **Tách** làm điểm xuất phát, sau đó đánh giá bằng bộ ticket thật.
- Trước khi nhập thay toàn bộ FAQ, luôn xuất backup và thử chế độ thêm vào trong KB test.

## 8. Nội dung không nên đưa vào KB

- Password, token hoặc service-account JSON.
- Dữ liệu cá nhân của người chơi.
- Link chứa credential hoặc session bí mật.
- Hai phiên bản quy định mâu thuẫn cùng mang trạng thái Active.
- Trạng thái realtime nếu không có quy trình đồng bộ.
- Suy đoán chưa được xác nhận nhưng được viết như kết luận chắc chắn.

## 9. Lộ trình triển khai đề xuất

### Giai đoạn 1 — Chuẩn hóa nguồn

1. Chọn một game và một owner nghiệp vụ.
2. Thu thập 10–20 tài liệu LiveOps quan trọng nhất.
3. Loại bỏ bản cũ hoặc đánh dấu Superseded.
4. Bổ sung metadata, heading, điều kiện và ngoại lệ.

### Giai đoạn 2 — Dựng KB Tài liệu

1. Tạo KB Tài liệu test.
2. Bật RAG; bật Wiki khi nguồn đã đủ sạch.
3. Nạp một nhóm tài liệu nhỏ trước.
4. Chờ trạng thái Hoàn tất và kiểm tra nguồn truy hồi.
5. Mở rộng sang toàn bộ bộ tài liệu sau khi mẫu nhỏ đạt.

### Giai đoạn 3 — Dựng KB FAQ

1. Lấy 30–50 câu hỏi xuất hiện nhiều nhất từ ticket.
2. Chuẩn hóa thành câu hỏi chuẩn, biến thể, loại trừ và câu trả lời.
3. Nhập vào KB FAQ test.
4. Chạy Kiểm tra tìm kiếm với câu đúng, câu diễn đạt lại, câu gần giống và câu ngoài phạm vi.
5. Chốt ngưỡng vận hành từ dữ liệu kiểm thử, không từ một câu hỏi đơn lẻ.

### Giai đoạn 4 — Phát hành và duy trì

1. Chỉ định owner nghiệp vụ và owner kỹ thuật.
2. Ghi phiên bản cấu hình KB và phiên bản nguồn.
3. Chạy bộ câu hỏi hồi quy sau mỗi thay đổi lớn.
4. Kiểm tra ảnh quan trọng đến đầu ra chat.
5. Lưu backup và quy trình phục hồi.
6. Định kỳ loại bỏ hoặc lưu trữ nội dung hết hiệu lực.

## 10. Checklist trước khi phát hành

- [ ] Nội dung có owner và ngày hiệu lực.
- [ ] Không còn hai phiên bản Active mâu thuẫn.
- [ ] Mọi file đã ở trạng thái Hoàn tất.
- [ ] Câu hỏi đúng và câu diễn đạt lại lấy được nguồn phù hợp.
- [ ] Câu gần giống nhưng sai ý định không kéo nhầm câu trả lời.
- [ ] Câu ngoài phạm vi không khiến hệ thống tự suy diễn.
- [ ] Điều kiện, số liệu và ngoại lệ trong câu trả lời khớp nguồn.
- [ ] Hình ảnh quan trọng hiển thị đúng trong chat nếu có sử dụng.
- [ ] Có backup và cách phục hồi.
- [ ] Có lịch xem lại nội dung sau khi sự kiện hoặc phiên bản kết thúc.

## Kết luận

Đối với LiveOps, KB Tài liệu nên được xây trước để tạo nguồn vận hành đáng tin cậy. KB FAQ được xây tiếp từ các câu hỏi ticket lặp lại nhằm chuẩn hóa câu trả lời cho CS, GM hoặc người chơi. Khi một chủ đề vừa có câu trả lời ngắn vừa có SOP chi tiết, hãy dùng cả hai KB và giữ vai trò của chúng tách biệt.
