<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 17 - Agent: đa phương thức và tệp đính kèm {#17-da-phuong-thuc-va-tep-dinh-kem}

## Khái niệm

Agent có hai đường xử lý khác nhau cần tách biệt khi kiểm thử:

1. **Tài liệu trong KB**: file đã upload, parser/index hoàn tất, được tools truy hồi như corpus.
2. **Tệp đính kèm trong chat**: file đi cùng đúng một request Human; model/Intent xử lý tệp đó trong phiên chat.

Không suy luận PDF trong KB parse được thì PDF attachment chắc chắn hoạt động, hoặc composer nhận ảnh thì VLM đã nhận bytes. MD, PDF và CSV fixture ORCHID đều được KB TEST xử lý hoàn tất; PDF attachment cũng được Agent đọc đúng. Nhánh image/ASR vẫn có điều kiện tenant/model.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/32-agent-cau-hinh-da-phuong-thuc.png -->
![Tab cấu hình đa phương thức](minio://knowledge-base-prd/10012/exports/dfac9762-3573-4725-9925-b474d134d835.png)

*Ảnh 17.1 – Control tải ảnh, VLM và audio/ASR cần cấu hình riêng với retrieval tài liệu.*

## Bảng control

| Loại input | Đường đi | Test đã làm | Trạng thái 11/08/2026 |
|---|---|---|---|
| Markdown | upload KB → index → retrieval | Canonical/near-duplicate | **Đã kiểm chứng** |
| PDF | upload KB hoặc attachment | ORCHID PDF | **Đã kiểm chứng** cả hai đường |
| CSV | upload KB → data/retrieval | Hai record ORCHID | **Đã kiểm chứng** đọc qua RAG; data tool E2E có điều kiện |
| Ảnh | attachment → VLM/Image Intent | PNG UI hiện có | **Bị chặn/có điều kiện:** client báo định dạng không hỗ trợ với model test |
| Audio | attachment → ASR → text | Chỉ kiểm tra UI | **Bị chặn:** tenant chưa có ASR model |

| Control | Câu hỏi vận hành | Không được kết luận chỉ từ UI |
|---|---|---|
| Tải ảnh | Có VLM/model tương thích? client nhận file? | VLM đọc được ảnh chỉ vì toggle bật |
| Image Analysis Intent | Có prompt nhánh hợp lý? | Attachment đã truyền thành công |
| Tải âm thanh | Có ASR model và ngôn ngữ? | Audio được transcript/đưa vào context |
| Document/Summarize Intent | Tệp có đúng request hay chỉ KB source? | Model tuân thủ khung trả lời |

## SOP

1. Xác định file dùng làm corpus lâu dài hay attachment một lượt; không thay thế nhau.
2. Với KB, chờ status **Hoàn tất** rồi test parser/source; không chat ngay khi còn chờ xử lý.
3. Với attachment, dùng một PDF/CSV/MD tổng hợp không nhạy cảm, hỏi những fact biết trước.
4. Với ảnh, chọn file an toàn, kiểm tra UI nhận tệp, model VLM/Intent và response; lưu lỗi client/server tách biệt.
5. Với audio, nếu dropdown ASR báo không có model thì dừng, ghi blocker; không cố đưa credential/model riêng vào workspace.
6. Xóa attachment/chat test nếu chính sách retention yêu cầu; fixture tổng hợp và audit không chứa thông tin thật.

## Data flow

```text
KB file:      file → parser/chunk/index → retrieval tools → context → answer
Attachment:   Human file → upload validation → request/session → Intent/VLM/ASR or document reader
                                                   → model → answer
```

Hai path gặp nhau ở model nhưng có validation, quyền, model và timing khác nhau. Chẩn đoán đúng phải hỏi “file có tới request chưa?” trước “model đọc đúng chưa?”.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/45-agent-tep-dinh-kem.png -->
![PDF nằm trong composer trước khi gửi](minio://knowledge-base-prd/10012/exports/c8f2a63c-944e-479a-a116-fbbe29438d2e.png)

*Ảnh 17.2 – Composer xác nhận PDF đã được đính kèm và hiển thị kích thước trước khi gửi.*

## Ma trận kiểm thử

| Tình huống | Input | Câu hỏi/kiểm tra | Pass condition |
|---|---|---|---|
| MD corpus | `TEST-orchid-canonical.md` | owner/SLA | Nguồn canonical + Nhóm Cam/4 giờ |
| PDF corpus | `TEST-orchid-attachment.pdf` trong KB | owner/SLA | Có thể truy hồi cùng dữ liệu chuẩn |
| CSV corpus | `TEST-orchid-data.csv` | so sánh hai record | Nêu record canonical và conflicting |
| PDF attachment | cùng PDF trong composer | mã/owner/SLA | ORCHID-731, Nhóm Cam, 4 giờ |
| Image attachment | PNG UI an toàn | mô tả nội dung | Ghi client/server error nếu bị chặn |
| Audio attachment | audio chỉ khi có ASR | transcript | Chỉ pass khi ASR/tenant hoạt động |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/46-agent-image-analysis.png -->
![Ảnh đính kèm bị từ chối ở client](minio://knowledge-base-prd/10012/exports/7aff3c1c-13cd-4788-9b17-251f7c94de12.png)

*Ảnh 17.3 – Bằng chứng lỗi “Định dạng tệp không hỗ trợ” với đường test này; không dùng nó để kết luận VLM hỏng.*

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/47-agent-document-summarize.png -->
![Document Analysis PDF trả về fact mong đợi](minio://knowledge-base-prd/10012/exports/c993f9f0-e66c-4692-83d7-11a5b85ad5fb.png)

*Ảnh 17.4 – Agent phân tích attachment PDF và nêu đúng mã, owner, SLA, priority.*

## Bằng chứng

- **Đã kiểm chứng:** KB TEST xử lý 3 MD, CSV và PDF hoàn tất; câu RAG đã dùng 4 tệp ORCHID để đối chiếu.
- **Đã kiểm chứng:** PDF attachment 1,7 KB được composer nhận; `deepseek-v4-flash` trả ORCHID-731, Nhóm Cam, SLA 4 giờ, priority P2.
- **Đã kiểm chứng:** Image upload theo đường test hiện hành cho toast `Định dạng tệp không hỗ trợ`.
- **Bị chặn:** audio/ASR không hoàn tất vì UI báo chưa có model ASR cho tenant.
- **Có điều kiện:** file type được UI liệt kê không bảo đảm parser/VLM/ASR đều khả dụng trên mọi tenant/model.

## Quy tắc dữ liệu và riêng tư attachment

Attachment đi qua session chat nên không nên dùng để kiểm thử với hợp đồng, thông tin cá nhân, credential, key, log nội bộ hoặc file có retention chưa rõ. Tạo fixture synthetic có oracle rõ (mã, owner, SLA) và kiểm tra: filename/size xuất hiện ở composer; query nêu đúng attachment; answer không chỉ lặp dữ liệu từ KB khác. Nếu attachment có nội dung nhạy cảm hợp lệ trong vận hành, áp dụng chính sách dữ liệu của tổ chức và xác nhận nơi lưu/retention trước khi upload.

| Câu hỏi trước upload | Lý do |
|---|---|
| Đây là corpus lâu dài hay context một lượt? | Chọn đường KB hoặc attachment |
| Có PII/secret/credential không? | Ngăn rò rỉ qua chat/audit |
| Có fact oracle để chấm không? | Phân biệt parse lỗi với model tổng hợp lỗi |
| Model/tenant có VLM hoặc ASR không? | Tránh kết luận sai từ control rỗng |

## Tóm tắt và phân tích tài liệu

Hai Intent **Summarize Response** và **Document Analysis Response** không thay thế kiểm chứng nguồn. Tóm tắt tốt phải giữ rõ phạm vi, dữ kiện chưa chắc và mâu thuẫn; phân tích tốt phải chỉ ra file/đoạn đang nói tới. Khi Human đính kèm PDF, yêu cầu model trả mã/owner/SLA là case oracle; khi Human chỉ yêu cầu “tóm tắt”, thêm constraint về số bullet, ngôn ngữ và việc không thêm fact ngoài file.

## Lỗi và giới hạn

| Hiện tượng | Lớp cần kiểm tra trước | Hành động |
|---|---|---|
| Tệp không hiện composer | Upload validation/client | Ghi định dạng/kích thước/model, không gọi lại private API |
| Tệp hiện nhưng answer nói không thấy | Attachment transmission/Intent | Lưu Request Information và test tệp tổng hợp khác |
| PDF KB có source nhưng attachment fail | Hai đường xử lý khác nhau | Không sửa parser KB vội |
| Không có ASR model | Tenant provisioning | Gắn nhãn Bị chặn và yêu cầu admin qua kênh chuẩn |
| CSV trả lời sai | Data/retrieval/prompt | Kiểm tra record, tool và source before model judgement |

## Checklist

- [ ] Phân biệt corpus KB với attachment per-turn.
- [ ] Tệp test không nhạy cảm, có oracle fact rõ ràng.
- [ ] PDF/CSV/MD được kiểm tra status trước chat.
- [ ] Image/ASR chỉ tuyên bố pass khi có response end-to-end.
- [ ] Audit ghi model, loại file, lỗi/toast và Request Information phù hợp.
