<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 18 - Agent: chat, nguồn, lịch sử và đánh giá {#18-chat-nguon-lich-su-va-danh-gia}

## Khái niệm

Chat là bề mặt Human nhìn thấy, còn source chips, history, feedback và Request Information là bề mặt quan sát để vận hành. Một câu trả lời “nghe hợp lý” chỉ là giả thuyết: phải mở nguồn, kiểm xem chunk/tài liệu có thật sự chứa claim hay không, rồi mới đánh giá Agent/KB. Chat mới tạo một session; follow-up phải được kiểm thử trong cùng history, không giả định Agent nhớ giữa session.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/33-agent-chat-nguon-va-anh.png -->
![Câu trả lời RAG, nguồn và ảnh trong Markdown](minio://knowledge-base-prd/10012/exports/37ad90a4-9160-4399-8c36-0e882141f2d9.png)

*Ảnh 18.1 – Câu trả lời cần kiểm tra cả source chip và ảnh render, không chỉ phần văn bản.*

## Bảng control

| UI | Mục đích | SOP kiểm chứng |
|---|---|---|
| Cuộc trò chuyện mới | Cô lập testcase/session | Đặt một query, ghi điều kiện cấu hình |
| Lịch sử | Mở lại hội thoại/follow-up | Không dùng history để suy luận persistent memory chưa kiểm chứng |
| Source chip / Xem file | Căn cứ retrieval | Mở đúng file, đối chiếu claim/chunk |
| Hữu ích/Chưa hữu ích | Tín hiệu Human | Gắn feedback vào testcase, không phải phán quyết nguyên nhân |
| Hộp xử lý | Điều tra feedback | Chuyển Mới → Đang xem → Đã xử lý có bằng chứng hồi quy |
| Request Information | Metadata request qua UI | Lưu ngày/method/ID đã che; không trích credential/private payload |

## SOP

1. Mở **Cuộc trò chuyện mới**, ghi Agent, model, KB chips, tools/retrieval baseline.
2. Gửi query; chờ status hoàn tất, không chụp khi UI còn `Đang tải` nếu muốn ghi answer cuối.
3. Mở source từng nguồn quan trọng; xác minh file, tên/chunk và fact.
4. Bấm **Thông tin request** khi cần trao đổi hỗ trợ hoặc tái hiện; che Request/Message/Session ID và URL định danh trước khi phân phối ảnh.
5. Đánh giá Hữu ích/Chưa hữu ích kèm nhận xét ngắn, liên kết test case.
6. Trong Hộp xử lý, phân loại: nguồn, retrieval, prompt, model/quota, attachment hoặc quyền; hồi quy rồi đóng.

## Data flow

```text
session/chat → response + sources
             → Human feedback (useful/not useful + comment)
             → evaluation overview → processing inbox
             → investigate with source + Request Information
             → fix correct layer → regression → resolved
```

Lịch sử giúp tái hiện ngữ cảnh conversation; nó không thay audit cấu hình vì model, quota hoặc Agent setting có thể đổi sau đó.

## Ma trận kiểm thử

| Case | Thao tác | Điều cần chứng minh |
|---|---|---|
| Chat mới | canonical ORCHID | Source canonical/PDF/CSV và answer đúng |
| Follow-up | “Owner là ai?” sau query ORCHID | Có/không dùng context được ghi rõ |
| Conflict | request nêu cảnh báo | Source near-duplicate được lộ, không che mâu thuẫn |
| No-hit | chính sách 2031 | Có kết luận thiếu nguồn, không hallucinate |
| Source drawer | mở file | Claim tồn tại trong nguồn thật |
| Request info | mở UI | Có request metadata, không lưu data nhạy cảm |
| Feedback | useful/not useful | Có đối tượng Hộp xử lý và mô tả nguyên nhân |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/34-agent-danh-gia-cau-tra-loi.png -->
![Tổng quan feedback và Hộp xử lý](minio://knowledge-base-prd/10012/exports/20b70b5a-db3f-4a71-89df-56e821628684.png)

*Ảnh 18.2 – Evaluation cần được vận hành như queue điều tra, không chỉ dashboard tỷ lệ.*

## Bằng chứng

- **Đã kiểm chứng:** canonical RAG hiển thị tool trace, source buttons cho canonical MD, near-duplicate MD, CSV và PDF; answer nêu mâu thuẫn có chủ đích.
- **Đã kiểm chứng:** no-hit kết luận không có information sau semantic/keyword search.
- **Đã kiểm chứng:** response có nút Sao chép, Thêm vào tri thức, Hữu ích, Chưa hữu ích và Thông tin request.
- **Đã kiểm chứng:** Request Information UI hiện Request ID, Message ID, Session ID, method POST, URL và thời gian gửi; ảnh phân phối đã che các định danh.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/48-agent-lich-su-va-request-information.png -->
![Request Information đã che định danh](minio://knowledge-base-prd/10012/exports/124e6dfd-7a1a-4c1a-92aa-6b02ad216b57.png)

*Ảnh 18.3 – Chỉ dùng thông tin UI để định vị request; các giá trị định danh đã được che trước khi nạp asset KB.*

## Kịch bản triage feedback

Khi Human bấm **Chưa hữu ích**, điều tra theo đường ngắn nhất: (1) mở conversation và xác định expectation; (2) mở source chip; (3) phân loại no source/source sai/source đúng answer sai; (4) kiểm tra Agent config snapshot; (5) sửa đúng một lớp; (6) chạy lại query gốc và query diễn đạt lại; (7) ghi hành động rồi mới chuyển **Đã xử lý**. Không đóng feedback chỉ vì response mới nghe trôi chảy.

| Loại feedback | Dấu hiệu | Owner thường xử lý | Bằng chứng đóng ticket |
|---|---|---|---|
| Thiếu nguồn | Không có chip hoặc no-hit sai | Owner Agent/KB | Scope/tool/index đã kiểm tra + source mới đúng |
| Nguồn sai | Chip không chứa claim | Owner KB/retrieval | Query hồi quy chọn đúng file/chunk |
| Tổng hợp sai | Chip đúng nhưng conclusion sai | Owner prompt/model | Answer mới + source không đổi/đúng |
| Attachment fail | Composer/toast/request bất thường | Owner Agent/tenant admin | Test file synthetic pass hoặc blocker có căn cứ |
| Quyền | Không thấy Agent/KB | Space/owner admin | Role/scope được xác minh theo phê duyệt |

## Quy tắc hiển thị nguồn và hình ảnh

Với Markdown có ảnh, source drawer phải mở đúng Markdown, còn UI chat phải render ảnh qua URI MinIO; hai kiểm tra này khác nhau. Link local `assets/...` có thể chạy trong HTML offline nhưng không phải đường phát hành cho chat. Nếu response nêu ảnh mà chỉ có URL hoặc placeholder, đánh dấu render chưa pass. Nếu ảnh render nhưng source Markdown sai, không chấp nhận answer chỉ vì visual đẹp.

Gói evidence tối thiểu cho một incident gồm: query đã che dữ liệu nhạy cảm, thời điểm, Agent/model, KB chips, answer, source drawer, trạng thái file, Request Information đã che và câu hồi quy sau sửa. Nếu không có đủ, trạng thái là **Đang xem** thay vì **Đã xử lý**.

Khi feedback nêu claim nghiệp vụ, liên hệ owner nội dung để xác nhận canonical source; không buộc model chọn câu trả lời theo phản hồi đơn lẻ.
Một source không còn truy hồi được sau update cần được coi là regression có owner, không chỉ là feedback UI.

## Lỗi và giới hạn

- Source đúng không đồng nghĩa answer đúng: model có thể tổng hợp sai hoặc ưu tiên sai; kiểm tra cả hai.
- Answer đúng không đồng nghĩa retrieval pass: có thể model đã biết sẵn; bắt buộc kiểm tra source khi use case yêu cầu grounded answer.
- Feedback là chỉ dấu Human; không tự suy ra root cause từ thumbs-down.
- Không sao chép JSON request, private URL có ID, credential hoặc browser storage vào audit/workspace.
- `[[chunk#...]]` phải được coi là lỗi format/answer; nó vẫn có thể hữu ích cho kỹ thuật viên xác nhận chunk tồn tại.

## Checklist

- [ ] Có chat mới và follow-up được đánh dấu khác session.
- [ ] Mỗi claim quan trọng có source được mở kiểm tra.
- [ ] No-hit và conflict có outcome rõ ràng.
- [ ] Request Information được che ID/URL trước khi dùng ảnh.
- [ ] Feedback có trạng thái, owner điều tra và test hồi quy trước khi đóng.
