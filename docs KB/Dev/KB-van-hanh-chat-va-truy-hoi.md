# KB — Vận hành Documents/Wiki/Graph, FAQ, chat kiểm thử và đánh giá truy hồi

Cách nạp và sửa nội dung, cách FAQ hoạt động, và cách đánh giá một câu trả lời bằng **nguồn truy hồi** thay vì bằng văn phong.

**Nguồn bằng chứng chính**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| [`audit/audit-knowledge-vng-2026-08-06.md`](../../audit/audit-knowledge-vng-2026-08-06.md) §8–§10, §13 | 06/08/2026 | Kiểm chứng live Documents, FAQ, chat, ảnh trong chat |
| [`audit/business-kb-readonly-audit-2026-08-14.md`](../../audit/business-kb-readonly-audit-2026-08-14.md) | 14/08/2026 | PII lan vào metadata; lỗi pipeline còn lưu; ACL |
| [`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`](../../audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md) | 14/08/2026 | Blocker upload tự động |
| `so-tay-tao-knowledge-base-v3.md` | — | Module `doc-09`, `doc-10`, `doc-11` |
| [`audit/archive/...-truoc-audit-2026-08-06.md`](../../audit/archive/so-tay-tao-knowledge-base-v3-truoc-audit-2026-08-06.md) §13–§15 | trước 06/08/2026 | **Master đã bị thay thế.** Chứa chi tiết pipeline chat, schema nhập FAQ, hành vi "Thay toàn bộ". Mọi mục lấy từ đây đánh dấu **(archive)**, giữ mức *Có điều kiện* |

**Phạm vi quan sát:** tenant `10012`.

---

## 1. Bốn cách nạp nội dung vào KB Tài liệu

Kiểm chứng 06/08/2026.

| Lựa chọn trong menu **Thêm tài liệu** | Trạng thái |
|---|---|
| **Tải tệp lên** | Hoạt động |
| **Tải thư mục lên** | Modal tồn tại; phép thử end-to-end **bị chặn** (§2) |
| **Nhập từ URL** | **Disabled** tại thời điểm kiểm tra |
| **Soạn thảo trực tuyến** | Hoạt động; tạo tài liệu nguồn `MANUAL` |

### Tải tệp lên

1. **Thêm tài liệu → Tải tệp lên**.
2. Chọn file hoặc kéo thả.
3. Mở **Xử lý nâng cao** nếu cần ghi đè parser/chunk cho riêng lượt nạp.
4. Tải lên, chờ trạng thái **Hoàn tất**.
5. Mở chi tiết file: xem tóm tắt, **Toàn văn** và **Xem phân đoạn**.

**Trạng thái `Hoàn tất` chỉ xác nhận pipeline kết thúc** — không xác nhận nội dung parse đúng. Xem [`KB-parser-va-xu-ly-file.md`](KB-parser-va-xu-ly-file.md) §9.

### Soạn thảo trực tuyến (archive §13.2)

Modal **Tạo tri thức Markdown** có: dropdown **Kho tri thức đích** (đổi sang KB Tài liệu khác được), Tiêu đề (0/100), toolbar định dạng đầy đủ, và bốn nút **Hủy / Xem trước / Lưu nháp / Xuất bản**.

**Xuất bản** hiện toast *"Đã xuất bản — bắt đầu lập chỉ mục"*; tài liệu xuất hiện với tên `[Tiêu đề].md` (tool tự thêm `.md`), gắn nhãn nguồn **MANUAL**. Nội dung đi qua **đúng pipeline như file tải lên**: văn bản test có 3 heading `#`/`##` ra đúng 3 phân đoạn.

---

## 2. Hai blocker upload đã ghi nhận

| Ngày | Blocker |
|---|---|
| 06/08/2026 | Modal Tải thư mục dùng input `multiple` + `webkitdirectory`. **API extension không gắn được** thư mục hoặc danh sách file vào input native. Bộ Aurora/Borealis phải nạp theo từng file — nên **không dùng làm bằng chứng** upload thư mục giữ cấu trúc |
| 14/08/2026 | Công cụ `file_upload` dùng whitelist đường dẫn **riêng, độc lập với quyền đọc file của agent**. Mọi đường dẫn tới file thật trong project đều bị từ chối, bất kể định dạng. Chỉ file trong scratchpad phiên làm việc được chấp nhận. Đã loại trừ giả thuyết độ dài đường dẫn, khoảng trắng, ký tự `:`, từ khóa tiếng Việt |

**Hệ quả vận hành:** upload hàng loạt phải do người thật thực hiện qua Explorer, hoặc đi đường Google Drive connector (DEC-046). Không mất thời gian chẩn đoán lại blocker 14/08 — kết luận đã chốt.

---

## 3. Lưu nháp — bản nháp KHÔNG phải nguồn chat

Kiểm chứng 06/08/2026.

Phép thử: tạo tài liệu `AUDIT-NHAP-20260806` chứa marker độc nhất `AUDIT-DRAFT-20260806`, bấm **Lưu nháp**.

- Toast *"Đã lưu bản nháp"*.
- Tài liệu xuất hiện trong danh sách với trạng thái **Bản nháp**.
- **Chat hỏi marker: không truy hồi được.**

Kết luận: **Lưu nháp** giữ nội dung chưa phát hành, không đưa vào index. Checklist phát hành bắt buộc có bước **Xuất bản** → chờ index → chạy câu hỏi xác nhận.

---

## 4. Sửa nội dung và Phân tích lại

Kiểm chứng 06/08/2026. Bảng so sánh đầy đủ và số chunk trước/sau nằm ở [`KB-phan-doan-chunking-va-embedding.md`](KB-phan-doan-chunking-va-embedding.md) §9. Tóm tắt hành vi:

| Thao tác | Áp cho | Tác động đã kiểm chứng |
|---|---|---|
| **Sửa nội dung** → **Xuất bản** | Tài liệu nguồn `MANUAL` | Kích hoạt lập chỉ mục lại thật. Số chunk 3 → 4 khi thêm marker; phục hồi nội dung gốc → về 3 |
| **Phân tích lại** | Mọi tài liệu | Tái chạy pipeline, tái sinh tóm tắt (đổi cách diễn đạt). **Không bảo đảm số chunk đổi** |

Nhãn menu chính xác cho tài liệu MANUAL là **Sửa nội dung** — không phải "Chỉnh sửa" hay tên khác.

Muốn đánh giá tác động: ghi ảnh hoặc số liệu trước/sau. Đừng dựa vào cảm giác.

---

## 5. Wiki và Graph khi vận hành

Kiểm chứng 06/08/2026.

### Wiki

Tab Wiki có **Mục lục** (trang chỉ mục tự cập nhật), **Nhật ký hoạt động**, hai cách xem (**Thư mục** / **Loại**), và tạo thư mục được. Node Graph có liên kết **Mở trong Wiki** khi node có trang liên quan.

Wiki xử lý nền: khi còn tài liệu đang xử lý, tab Wiki báo *"Đang xử lý 1 tài liệu…"*.

### Graph

Số node thay đổi liên tục trong cùng một ngày khi nguồn tiếp tục được xử lý: 66 → 93 → 159. Phân bố cuối ngày 06/08: Tóm tắt 22, Thực thể 66, Khái niệm 70, **Tổng hợp 0, So sánh 0**.

Chi tiết chú giải và kết luận về hai loại node chưa sinh được nằm ở [`KB-loai-kb-va-chien-luoc-index.md`](KB-loai-kb-va-chien-luoc-index.md) §5.

(archive §13.6) Đồ thị tương tác thật: kéo/thu phóng, ô "Tìm node…", nút "Vừa khung", "Ẩn mũi tên". Node nối bằng cạnh thể hiện quan hệ được nhắc cùng nhau trong tài liệu.

### Danh sách Documents và khả năng truy hồi có thể lệch pha

Cạm bẫy đã gặp thật, 06/08/2026: ba ảnh hiện `Đang hoàn tất` sau nhiều lần tải lại danh sách Documents, **dù chat đã truy hồi được đoạn nguồn và URI đầy đủ của chính chúng**. Lượt đối chiếu cuối ngày cho thấy hai trong ba đã tự chuyển `Hoàn tất`.

Đừng dùng riêng badge trạng thái làm gate phát hành.

---

## 6. Vận hành FAQ

### Thanh công cụ

Kiểm chứng 06/08/2026: **Chọn tất cả · Kiểm tra tìm kiếm · Xuất · Nhập · Thêm Q&A**.

### Cấu trúc một mục Q&A

| Trường | Giới hạn quan sát được |
|---|---|
| Câu hỏi chuẩn | 1, tối đa **200 ký tự** |
| Câu hỏi tương tự | tối đa **10** |
| Câu hỏi loại trừ | tối đa **10** |
| Câu trả lời | tối đa **5** |
| Phân loại | tag tự tạo, không phải preset |

### Kiểm tra tìm kiếm — công cụ chỉ FAQ mới có

| Tham số | Khoảng | Giá trị khi mở |
|---|---|---|
| Ngưỡng tương đồng | 0 – 1, bước 0,1 | **0,5** |
| Số kết quả tối đa | 1 – 50 | **10** |

Kết quả hiện: số thứ tự · câu hỏi chuẩn khớp · **điểm số** · dòng **"Khớp:"** cho biết đoạn văn bản thật sự dùng để tính điểm. Không có kết quả → *"Không có mục khớp."* (archive §14.4)

Hai phép thử đã chạy 06/08/2026:

- `"Server bảo trì lúc nào?"` ở ngưỡng 0 → trả về mục đúng, điểm **1,000**.
- Từ khóa **chỉ có trong câu trả lời** → **không tìm thấy** ở chế độ `Chỉ câu hỏi`, **kể cả ngưỡng 0**.

Điểm thứ hai là khác biệt về **phạm vi index**, không phải điểm similarity thấp. Đây là bằng chứng quyết định khi chọn giữa `Chỉ câu hỏi` và `Câu hỏi + trả lời`.

**Kỹ thuật chẩn đoán:** ngưỡng mặc định 0,5 có thể ẩn mất match yếu nhưng vẫn đúng. Khi nghi ngờ FAQ "không tìm thấy gì", **hạ ngưỡng về 0** để phân biệt: không có candidate nào, hay có nhưng bị ngưỡng lọc.

**KB Tài liệu KHÔNG có công cụ này.** Cách gần nhất là dùng Chat và mở **Nguồn tham khảo**.

### Xuất

Kiểm chứng 06/08/2026: nút **Xuất** tạo `faq_export_2026-08-06 (2).csv` gồm 5 dòng Q&A.

- Header dùng **tiếng Anh** — khác header tiếng Việt trong CSV mẫu của dự án.
- Trường nhiều giá trị nối bằng `##`.
- Chọn lại chính file xuất đó trong modal **Nhập**: hệ thống đọc đủ 5 mục và bật nút Nhập. Phép thử dừng ở preview để tránh tạo trùng.

Kết luận: **Xuất là bước backup thực dụng** trước mọi thao tác nhập.

### Nhập

Menu **Tệp mẫu** có **JSON, CSV, Excel** — cả ba cùng schema (archive §14.3):

| Trường trong file | Tương ứng modal Thêm Q&A |
|---|---|
| `standard_question` | Câu hỏi chuẩn |
| `similar_questions` (mảng) | Câu hỏi tương tự — trong CSV nối bằng `##` |
| `negative_questions` (mảng) | Câu hỏi loại trừ |
| `answers` (mảng) | Câu trả lời |
| `tag_name` | Phân loại |
| `is_enabled` (`TRUE`/`FALSE`) | Toggle Kích hoạt |

Live preview 06/08/2026 đọc đúng `3 mục` cho cả ba file mẫu của dự án (`mau-faq.json`, `.csv`, `.xlsx`); nút **Nhập** được bật. Mỗi lượt đóng bằng **Hủy**, danh sách FAQ giữ nguyên 5 mục.

### `Thay toàn bộ` là thao tác phá hủy dữ liệu

(archive §14.3, test thật của người dùng) KB có 1 mục, nhập file 2 mục khác hoàn toàn, chọn **Thay toàn bộ**. Popup xác nhận ghi nguyên văn *"Không thể hoàn tác."* Kết quả: KB chỉ còn đúng 2 mục mới; mục cũ **biến mất hoàn toàn**, không có bước khôi phục.

Quy trình bắt buộc trước khi nhập:

1. **Xuất backup** hiện tại.
2. Kiểm tra số mục trong file nguồn.
3. Xác nhận cách xử lý câu hỏi tương tự, loại trừ và nhiều câu trả lời.
4. Dùng chế độ **Thêm vào** khi đang thử.
5. Chỉ dùng **Thay toàn bộ** trong KB test hoặc khi đã có kế hoạch phục hồi.

Sau nhập: đối chiếu số mục, mở ngẫu nhiên ít nhất 5 mục, kiểm tra ký tự tiếng Việt / xuống dòng / dấu `##`, chạy bộ câu hỏi hồi quy ở **cùng** cấu hình index và ngưỡng, lưu file nguồn kèm ngày và người thực hiện.

*Điểm khó hiểu đã ghi nhận (archive):* dòng tóm tắt sau khi nhập hiện *"Tổng 2 · 0 thêm mới · 2 bỏ qua"* — chữ "bỏ qua" gây hiểu lầm vì kết quả thật là 2 mục có trong KB. Nhiều khả năng là text dùng chung cho cả hai chế độ.

---

## 7. Chat — quy trình trả lời hiển thị công khai

(archive §15) Bấm icon 💬 ở đầu trang KB mở khung **Trò chuyện**, tự gắn KB hiện tại làm nguồn (hiện thành tag, gỡ được bằng `×`, thêm KB khác vào cùng phiên được).

Các bước hiển thị — **không phải hộp đen**:

| Bước hiển thị | Ý nghĩa |
|---|---|
| `Nguồn tham khảo (N tài liệu)` | Mở rộng liệt kê **từng tài liệu + số đoạn được dùng**, kèm icon mở tài liệu gốc |
| `🔧 Đã gọi Query Understand` | Bước hiểu câu hỏi |
| `🔍 Đang tìm trong kho tri thức: "…"` | **Câu hỏi được viết lại / dịch sang tiếng Anh nội bộ** trước khi tìm |
| `Tìm thấy N kết quả` | Số candidate |
| `💭 Suy nghĩ` | Khối lý luận trung gian, xem được toàn bộ |
| Câu trả lời cuối | Có markdown, heading, bullet |

Khung chat còn có ô chọn chế độ trả lời (nhãn quan sát được: **Quick Answer**), dropdown chọn **Mô hình** riêng cho phiên chat, nút **Cuộc trò chuyện mới** và **Lịch sử**.

**Chưa rõ:** dropdown Mô hình trong chat có mặc định dùng đúng "Mô hình chat/tóm tắt" đã cấu hình cho KB hay độc lập.

### Quy trình kiểm thử chat

1. Chờ tài liệu ở trạng thái **Hoàn tất**.
2. Mở **Trò chuyện**.
3. Hỏi một câu có đáp án rõ trong nguồn.
4. Mở **Nguồn tham khảo** hoặc các bước truy hồi.
5. Kiểm tra file và đoạn được lấy có đúng không.
6. Đánh giá câu trả lời có giữ đúng **điều kiện, số liệu, ngoại lệ** không.
7. Hỏi lại bằng từ khác.
8. Hỏi một câu **ngoài phạm vi** để xem hệ thống có bịa hoặc kéo nguồn gần giống không.

---

## 8. Chẩn đoán theo lớp

Đây là bảng tra chính khi câu trả lời sai. Đi từ trên xuống, không đổi model trước.

| Hiện tượng | Kiểm tra trước |
|---|---|
| Không có nguồn đúng | File đã **Xuất bản** chưa, trạng thái, index, parser, chunking |
| Có nguồn nhưng thiếu đoạn quan trọng | Ranh giới chunk, heading, kích thước cha-con |
| Nguồn đúng nhưng trả lời sai | Model chat, prompt, nội dung mâu thuẫn trong chính nguồn |
| FAQ kéo nhầm mục | Biến thể, câu loại trừ, chế độ index, ngưỡng |
| Ảnh được mô tả nhưng không hiện | Loại đường dẫn ảnh trong Markdown (§9) |

Nguyên tắc: **nếu nguồn truy hồi sai, đừng đổi model chat.** Kiểm tra embedding, dữ liệu và chunking trước.

---

## 9. Ảnh trong chat

Tóm tắt ở đây phục vụ việc chẩn đoán chat. Hợp đồng ảnh đầy đủ (mapping, builder, `LOCAL_ASSET`, vòng đời KB asset) nằm ở [`KB-anh-va-uri-minio.md`](KB-anh-va-uri-minio.md).

Hai đường đã kiểm chứng 06/08/2026, kết quả trái ngược.

| Cách viết trong Markdown | Kết quả | Bằng chứng |
|---|---|---|
| Đường dẫn tương đối `![...](assets/ten-anh.png)` | **Không đạt.** Retriever tìm thấy nguồn và mô tả được ảnh, nhưng câu trả lời **không có thẻ `img`** | `audit/evidence/2026-08-06-chat-image-not-rendered.png` |
| URI nội bộ `![...](minio://knowledge-base-prd/.../ten-anh.png)` | **Đạt.** Retriever chuyển link thành image token; câu trả lời có thẻ ảnh, đúng alt, render đúng hình | `audit/evidence/2026-08-06-chat-image-minio-rendered.png` |

### Quy trình chuẩn cho bộ tài liệu có ảnh

1. Giữ ảnh cục bộ cho người đọc và HTML offline.
2. Upload ảnh **độc lập** để hệ thống sinh URI MinIO.
3. Lấy và lưu URI vào `image-map.json`.
4. Chạy builder thay ảnh cục bộ bằng URI MinIO trong file MD phân phối; giữ `<!-- LOCAL_ASSET: ... -->` để người bảo trì biết ảnh gốc.
5. Nạp file MD đã sửa.
6. Hỏi câu buộc trả lời kèm hình, xác nhận ảnh thật xuất hiện **và** nguồn dùng đúng URI mới.
7. **Không xóa ảnh nguồn** khi Markdown còn tham chiếu URI đó (DEC-005).

Build nghiêm ngặt dừng nếu một ảnh thật chưa có mapping MinIO. Ảnh nằm trong fenced code không được xem là tài nguyên cần mapping.

### Hai ghi chú đã chốt

- **DEC-041 (15/08/2026):** cú pháp `<!-- LOCAL_ASSET: <path> -->` + `![mô tả](minio://.../exports/<uuid>.<ext>)` được xác nhận **hoàn toàn đúng**. Hiện tượng **ảnh render hai lần trong chat** là hành vi không ổn định của model khi soạn câu trả lời, **không phải lỗi cú pháp hay cấu trúc KB**. Không sửa builder vì lý do này, không điều tra lại. Bằng chứng: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.
- **DEC-045 (15/08/2026):** ưu tiên MCP `list_documents` để thu URI MinIO hàng loạt (trả `file_path` cho toàn bộ tài liệu trong một lệnh) thay vì bắt network bằng browser. Điều kiện: KB phải được share vào space trước. Còn phải kiểm chứng dạng `file_path` cho **tài liệu ảnh** trước khi dùng làm nguồn ghi map.

---

## 10. Rủi ro khi đánh giá nguồn truy hồi

### PII đã lan vào metadata, không chỉ vào chunk

Phát hiện 14/08/2026 trên `GS9 CFL Item Profile`. Trường `description`/summary **do hệ thống tự sinh** cho hai CSV cấp player đã trích dẫn nickname thật và giá trị nạp cụ thể.

Metadata này **không phải chunk nội dung** — nó xuất hiện trong danh sách tài liệu **và trong khối `Nguồn tham khảo`** của bất kỳ Agent nào bind KB đó.

Hệ quả cho quy trình kiểm thử: khi chạy chat-test grounding, phải kiểm tra **cả khối Nguồn tham khảo**, không chỉ nội dung câu trả lời. Gate G6 trong audit KB nghiệp vụ yêu cầu đúng điều này và cần Human approval.

### Share KB vào space đồng thời mở KB đó cho MCP connector

Phát hiện 6, 14/08/2026: `list_knowledge_bases` trả về đúng tập KB đã share vào space `CFL Member`. Ba KB không share trả `not found or not accessible`.

Nghĩa là **share = mở thêm một đường truy cập dữ liệu song song** với việc bind KB vào Agent. Trong chính phiên audit đó, MCP đã đọc được metadata PII của `GS9 CFL Item Profile` chỉ bằng quyền sẵn có.

### Quyền `Chỉnh sửa` phá vỡ giả định "Web khớp master"

14/08/2026: 5 KB đang share quyền **Chỉnh sửa** cho space 6 thành viên. Chú giải UI: *"Quyền Chỉnh sửa cho phép sửa nội dung; Chỉ đọc chỉ cho truy hồi và hỏi đáp."*

Với `GS9 Knowledge VNG AI` — consumer phát hành của 20 module sinh tự động — điều này phá vỡ hợp đồng DEC-001. Web có thể drift khỏi master mà gate local không phát hiện, hoặc build local ghi đè im lặng thay đổi của người khác.

### Chất lượng reranker và VLM cấp Agent chưa được chat-test

DEC-049 (15/08/2026): 10 custom Agent đã bật `Mô hình xếp hạng lại` = `bge-reranker-v2-m3` và `Tải ảnh` + `Mô hình VLM` = `qwen3.6-plus`. Đây là cấu hình **cấp Agent**, không phải cấp KB.

Cả reranker lẫn VLM **chưa được chat-test** → chất lượng vẫn là *Bị chặn–Chưa xác định*. Đúng DEC-022: cấu hình UI không bằng hành vi runtime.

DEC-049 cũng ghi: quyền `Được chỉnh sửa` cho space 6 người nghĩa là **người khác sửa được Agent** — mọi snapshot config có thể lệch bất cứ lúc nào.

---

## 11. Bộ kiểm thử tối thiểu cho mỗi KB

| Loại câu hỏi | Số lượng |
|---|---:|
| Đúng nguyên văn | 5 |
| Diễn đạt tự nhiên hoặc không dấu | 5 |
| Cần điều kiện / ngoại lệ | 3 |
| Gần giống nhưng khác ý định | 3 |
| Ngoài phạm vi | 3 |
| Yêu cầu ảnh (nếu nội dung có ảnh) | 2 |

Ghi kết quả theo **ngày, model, cấu hình index/chunk và phiên bản nguồn**. Chạy lại toàn bộ sau khi đổi model, parser, chunking hoặc index.

---

## 12. Tiêu chí phát hành

Một KB sẵn sàng khi:

1. Nguồn đã có owner và phiên bản.
2. Cấu hình nền tảng được ghi lại (có ngày).
3. Các file đều **Hoàn tất** và nội dung phân đoạn đọc được.
4. Bộ câu hỏi đúng / gần đúng / loại trừ / ngoài phạm vi đã chạy.
5. **Nguồn truy hồi đúng** — không chỉ câu trả lời nghe hay.
6. Ảnh quan trọng đã được kiểm thử đến đầu ra chat.
7. Khối `Nguồn tham khảo` không lộ dữ liệu nhạy cảm.
8. Có backup và quy trình phục hồi.

### Quy trình vận hành một thay đổi

1. Lưu bản nguồn có phiên bản.
2. Sửa một nhóm nội dung.
3. Nạp hoặc Xuất bản.
4. Chờ **Hoàn tất**.
5. So sánh số chunk, tóm tắt và nguồn truy hồi.
6. Chạy bộ câu hỏi hồi quy.
7. Kiểm tra Wiki/Graph nếu đang dùng.
8. Ghi ngày, người thực hiện và kết quả.

---

## 13. Chưa kiểm chứng

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| Upload thư mục có giữ cấu trúc thư mục con không | **Bị chặn** | Không thực hiện được end-to-end (06/08 và 14/08/2026) |
| **Nhập từ URL** hoạt động thế nào | Bị chặn | Disabled tại thời điểm kiểm tra (06/08/2026) |
| Dropdown **Mô hình** trong khung chat có kế thừa model cấu hình của KB không | Chưa xác định | (archive §15) |
| Chế độ trả lời **Quick Answer** khác gì các chế độ còn lại | Chưa xác định | Chỉ quan sát nhãn |
| Điều kiện sinh node **Tổng hợp / So sánh** | Chưa xác định | Xem `KB-loai-kb-va-chien-luoc-index.md` §5 |
| Hành vi đồng bộ thêm/sửa/đổi tên/xóa/thu hồi quyền ở Notion, Drive, NAS | Chưa xác định | Notion và NAS chưa đi hết bước 3–4 vì thiếu credential test |
| Độ đầy đủ chunk của hai tài liệu từng lỗi pipeline | **Có điều kiện** | `01_weapons_usage.csv`, `CFL_082026.xlsx` — `parse_status: completed` nhưng có `error_message` (14/08/2026) |
| Chất lượng retrieval của từng KB nghiệp vụ | Có điều kiện | Hai embedding model khác nhau, chưa so sánh được |
| Chất lượng reranker `bge-reranker-v2-m3` và VLM cấp Agent | **Bị chặn** | Chưa chat-test (DEC-049) |
| 20 module trên Web còn khớp master hay đã bị sửa bởi thành viên có quyền Chỉnh sửa | Bị chặn | Gate G5, chờ G1 (14/08/2026) |
| Có phải mọi tenant thấy cùng bộ công cụ vận hành này | Chưa xác định | Toàn bộ quan sát trên tenant `10012` |
