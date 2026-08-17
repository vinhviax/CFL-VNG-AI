# Sổ tay tạo và vận hành Knowledge Base & Agent

> Phiên bản: 3.3.0
> Cập nhật: 11/08/2026

Tài liệu chuẩn để tạo, kiểm thử và vận hành Knowledge Base cùng Agent trên VNG AI. Nội dung nghiệp vụ nằm trong 20 module dưới đây; các file Markdown phân phối và HTML offline được sinh bằng builder.

<!-- MODULE:doc-00-gioi-thieu-va-quick-start.md -->
## 00 - Giới thiệu và quick start {#00-gioi-thieu-va-quick-start}

### Bạn sẽ biết gì sau khi đọc

- Knowledge Base giải quyết việc gì.
- Khi nào chọn **Tài liệu**, khi nào chọn **FAQ**.
- Luồng tối thiểu từ tạo kho đến câu trả lời đã kiểm thử.

**Kiểm chứng giao diện: 06/08/2026.**

### Knowledge Base là gì

Knowledge Base, viết tắt là KB, là kho nội dung có cấu trúc để hệ thống tìm và dùng làm nguồn khi trả lời. Knowledge VNG hiện có hai loại chính:

- **Tài liệu:** nạp file hoặc soạn nội dung dài; hệ thống phân tích file, chia đoạn và có thể tạo Wiki/Graph.
- **FAQ:** lưu từng mục câu hỏi và câu trả lời; có công cụ kiểm tra tìm kiếm, nhập và xuất dữ liệu.

Hai loại này phục vụ hai bài toán khác nhau. Không cần ép toàn bộ tri thức vào một KB duy nhất.

![Trang danh sách Knowledge Base và nút tạo Knowledge Base mới](<knowledge/GS9 Knowledge VNG AI/image-01-tong-quan-danh-sach-knowledge.png>)

*Ảnh 00.1 - Trang Knowledge hiển thị danh sách kho và nút `Knowledge Base mới`.*

### Chọn loại nào

| Tình huống | Chọn | Lý do |
|---|---|---|
| Hướng dẫn dài, SOP, chính sách, tài liệu dự án | Tài liệu | Cần parser, phân đoạn và truy hồi theo nội dung |
| Onboarding cần đọc theo chủ đề liên kết | Tài liệu + Wiki | Wiki tổng hợp thành các trang có liên kết |
| Câu trả lời phải được quản lý theo từng mục | FAQ | Mỗi Q&A là một đơn vị độc lập |
| Có sẵn bảng câu hỏi, biến thể và câu trả lời | FAQ | Nhập JSON, CSV hoặc Excel thuận tiện |
| Vừa có quy định cứng vừa có tài liệu giải thích | Hai KB | FAQ cho câu chuẩn; Tài liệu cho bối cảnh |

### Quick start 8 bước

1. Xác định người dùng sẽ hỏi gì và ai chịu trách nhiệm nội dung.
2. Chọn **Tài liệu** hoặc **FAQ** trước khi nạp dữ liệu.
3. Chuẩn hóa nguồn: bỏ bản cũ, chia chủ đề, đặt heading rõ.
4. Tạo KB test và chọn model đang dùng được.
5. Mở **Cài đặt** để kiểm tra lại cấu hình thật, kể cả khi dùng chế độ Nhanh.
6. Nạp một bộ nhỏ đại diện trước, chờ trạng thái **Hoàn tất**.
7. Dùng **Trò chuyện** hoặc **Kiểm tra tìm kiếm** để chạy câu hỏi đúng, câu hỏi diễn đạt lại, câu ngoài phạm vi và câu dễ nhầm.
8. Chỉ mở rộng dữ liệu sau khi đã xem nguồn truy hồi và sửa được lỗi.

### Bản đồ màn hình

Knowledge VNG có hai bộ tab khác nhau:

- **Trong Cài đặt:**
  - Tài liệu: **Tổng quan, Mô hình, Xử lý, Chia sẻ, Nguồn dữ liệu**.
  - FAQ: **Tổng quan, Mô hình, Chia sẻ, Nguồn dữ liệu**.
- **Trong trang làm việc:** **Documents, Wiki, Graph** xuất hiện ở cả hai loại. Với FAQ được kiểm thử, Wiki và Graph chỉ hiện thông báo chưa bật chứ chưa có chức năng thật.

Đừng nhầm tab **Xử lý** trong Cài đặt với tab **Documents** ở trang làm việc.

### Ba nguyên tắc trước khi dùng thật

1. **Thử trên KB test.** Không dùng thao tác nhập thay toàn bộ trên kho đang phục vụ người dùng.
2. **Đo bằng câu hỏi thật.** Một file được xử lý thành công chưa chứng minh câu trả lời đúng.
3. **Giữ bản nguồn và bản xuất.** KB là lớp phân phối, không thay thế kho lưu trữ có phiên bản.
<!-- /MODULE -->

<!-- MODULE:doc-01-chuan-bi-noi-dung.md -->
## 01 - Chuẩn bị nội dung nguồn {#01-chuan-bi-noi-dung}

### Bạn sẽ biết gì sau khi đọc

- Cách làm sạch file trước khi nạp.
- Cấu trúc Markdown thân thiện với người đọc và hệ thống truy hồi.
- Cách chuẩn bị ảnh để vừa đọc offline vừa hiển thị trong chat Knowledge VNG.

**Kiểm chứng giao diện: 06/08/2026.**

### Chất lượng nguồn quyết định giới hạn câu trả lời

Parser và model có thể giúp trích xuất, nhưng không tự giải quyết được tài liệu mâu thuẫn, thiếu ngữ cảnh hoặc đã lỗi thời. Trước khi nạp, hãy trả lời bốn câu:

1. Đây có phải bản đang hiệu lực không?
2. Mỗi chủ đề có một nơi chịu trách nhiệm rõ không?
3. Thuật ngữ, mã lỗi, thời gian và phạm vi áp dụng có được viết trực tiếp không?
4. Người đọc có thể hiểu một mục khi nó bị tách ra khỏi phần trước không?

### Checklist dọn file

- Xóa bản nháp, bản trùng và thông tin đã hết hiệu lực.
- Tách file quá dài theo nhóm chức năng hoặc hành trình người dùng.
- Đặt một tiêu đề cấp 1 cho mỗi file; dùng tiêu đề cấp 2-3 cho các phần.
- Viết đủ chủ ngữ và phạm vi. Tránh các câu như “làm như trên”, “trường hợp này”, “phiên bản mới”.
- Đưa điều kiện áp dụng, ngoại lệ và kết quả mong đợi vào cùng mục với quy trình.
- Với bảng, lặp lại tên đối tượng trong hàng thay vì dựa hoàn toàn vào vị trí cột.
- Ghi ngày hiệu lực và chủ sở hữu nội dung nếu tài liệu thay đổi thường xuyên.

### Mẫu Markdown cho KB Tài liệu

```markdown
# Người chơi không vào được game, báo Connection timeout

Ngày hiệu lực: 2026-08-06
Chủ sở hữu: LiveOps

# Dấu hiệu nhận biết

- Mã lỗi: CONNECTION_TIMEOUT
- Xảy ra sau khi bấm Đăng nhập.

# Nguyên nhân đã ghi nhận

1. Máy chủ đang bảo trì.
2. Kết nối đến cụm đăng nhập bị gián đoạn.

# Cách xử lý, theo thứ tự

1. Kiểm tra trang trạng thái vận hành.
2. Nếu không có sự cố chung, yêu cầu người chơi đổi mạng và thử lại.

# Kết quả mong đợi

Người chơi vào được màn hình chọn máy chủ.

# Không áp dụng cho

Không dùng quy trình này cho lỗi INVALID_TOKEN.
```

### Ảnh trong file Markdown: hai mục đích, hai đường dẫn

Đường dẫn tương đối như sau hữu ích khi con người mở bộ file trên máy:

```markdown
![Màn hình cấu hình](assets/02-cau-hinh-tong-quan-document.png)
```

Tuy nhiên, phép thử trực tiếp cho thấy chat Knowledge VNG **không render ảnh** từ đường dẫn tương đối, dù file MD và ảnh đều đã được nạp riêng.

![Câu trả lời có mô tả ảnh nhưng không render ảnh khi Markdown dùng đường dẫn tương đối](<knowledge/GS9 Knowledge VNG AI/image-14-chat-khong-hien-thi-duong-dan-tuong-doi.png>)

*Ảnh 01.1 - Trường hợp không đạt: câu trả lời có phần “Hình minh họa” nhưng DOM không có ảnh.*

Đường đi đã kiểm thử thành công là:

1. Nạp ảnh như một tài liệu độc lập vào KB Tài liệu có VLM.
2. Chờ ảnh ở trạng thái **Hoàn tất**.
3. Lấy URI nội bộ dạng `minio://knowledge-base-prd/.../ten-anh.png` từ nội dung nguồn mà hệ thống tạo.
4. Chèn URI đó vào Markdown:

   ```markdown
   ![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/.../ten-anh.png)
   ```

5. Nạp hoặc phân tích lại file Markdown.
6. Hỏi câu buộc trả lời kèm hình và xác nhận ảnh thật xuất hiện trong câu trả lời.

**Lưu ý vận hành:** URI `minio://` gắn với tài nguyên trong hệ thống. Không xóa ảnh nguồn nếu các file Knowledge đang tham chiếu URI đó. Bộ 20 file phân phối của dự án dùng cả ảnh cục bộ để con người đọc và ảnh MinIO để chat có thể render.

Trước khi upload bộ ảnh vào KB asset, kiểm tra định dạng thật: file đuôi `.png` phải có payload PNG với 8 magic bytes `89 50 4E 47 0D 0A 1A 0A`; không chỉ đổi đuôi JPEG thành `.png`. Parser/VLM có thể suy ra MIME và đường dẫn xuất từ nội dung thật, nên file sai định dạng có thể sinh URI đuôi `.jpg`. Nếu phát hiện sai, transcode sang PNG thật, giữ nguyên tên file và kích thước ảnh khi phù hợp, rồi kiểm tra lại trước khi upload.

### Hai KB, hai vai trò

- **KB asset** giữ 49 ảnh PNG độc lập và cấp URI `minio://`. Đây là dependency lâu dài, không dùng làm KB hỏi đáp cho human.
- **KB sử dụng** chỉ nhận 20 file Markdown đã chứa URI MinIO. Không upload folder ảnh hoặc PNG cùng bộ Markdown vào KB này.

Trong dự án này, KB asset là `GS9 Knowledge VNG - Image Assets`; KB sử dụng là `GS9 Knowledge VNG AI`. `LOCAL_ASSET` trong file sinh chỉ giúp builder tìm ảnh local để dựng HTML offline, không phải liên kết ảnh mà Knowledge VNG chat sử dụng.

Khi đổi nơi lưu ảnh, làm đúng thứ tự: tạo host mới → upload ảnh → lấy URI → cập nhật mapping → build → thay Markdown → kiểm thử chat → xóa ảnh ở nơi cũ. Nếu KB asset cũ bị xóa, phải tái kiểm chứng toàn bộ mapping liên quan dù một số link vẫn tạm thời render.

### Không viết điều chưa có bằng chứng như số liệu

Các câu “80% lỗi AI đến từ file nguồn”, “KB không có owner sẽ chết sau một quý” hoặc các tỷ lệ tương tự không được dùng nếu không có dữ liệu đo và nguồn trích dẫn. Có thể viết dưới dạng rủi ro vận hành, không biến thành thống kê.
<!-- /MODULE -->

<!-- MODULE:doc-02-tao-kb-nhanh-va-nang-cao.md -->
## 02 - Tạo KB bằng chế độ Nhanh và Nâng cao {#02-tao-kb-nhanh-va-nang-cao}

### Bạn sẽ biết gì sau khi đọc

- Khác biệt giữa **Nhanh** và **Nâng cao**.
- Những lựa chọn cần chốt trước khi có nội dung.
- Cách tránh tin nhầm banner tóm tắt cấu hình.

**Kiểm chứng giao diện: 06/08/2026.**

### Chế độ Nhanh

Form Nhanh hỏi các trường chính:

- **Loại:** Tài liệu hoặc FAQ.
- **Tên** và **Mô tả**.
- **Mô hình chat / tóm tắt**.
- **Mô hình Embedding**.

Các lựa chọn RAG/Wiki, parser, phân đoạn, VLM, ASR hoặc cách lập chỉ mục FAQ được ẩn và nhận cấu hình khuyến nghị. Chế độ này phù hợp để tạo KB test nhanh, nhưng không thay thế bước mở lại **Cài đặt** để kiểm tra.

### Chế độ Nâng cao

Chế độ Nâng cao hiển thị toàn bộ tab cấu hình theo loại KB. Với Tài liệu, tab **Tổng quan** cho thấy loại và chiến lược RAG/Wiki; với FAQ, tab này có cấu hình lập chỉ mục câu hỏi.

![Tab Tổng quan của KB Tài liệu với loại, RAG, Wiki, tên và mô tả](<knowledge/GS9 Knowledge VNG AI/image-02-cau-hinh-tong-quan-document.png>)

*Ảnh 02.1 - Tab Tổng quan của KB Tài liệu đã có nội dung; một số lựa chọn bị khóa.*

### Những gì bị khóa và khi nào

**Đã kiểm chứng:** loại KB bị khóa sau khi tạo. Khi KB Tài liệu đã có nội dung, loại, chiến lược lập chỉ mục và model Embedding hiển thị vô hiệu hóa; giao diện yêu cầu xóa tài liệu nếu muốn thay đổi cấu trúc này.

**Mâu thuẫn giao diện ở FAQ:** banner cũng nói cấu hình lập chỉ mục bị khóa khi có nội dung, nhưng hai lựa chọn **Chỉ câu hỏi / Câu hỏi + trả lời** và **Gộp / Tách** vẫn bấm, lưu và giữ giá trị sau khi mở lại. Vì vậy:

- Không hướng dẫn người dùng phải xóa toàn bộ FAQ chỉ để đổi hai lựa chọn này.
- Sau mỗi lần đổi, chạy lại **Kiểm tra tìm kiếm** vì không có bảo đảm kết quả cũ giữ nguyên.
- Coi loại KB và Embedding là lựa chọn nền tảng cần chốt trước.

### Cảnh báo về banner cấu hình khuyến nghị

Trong phép thử tạo KB trước đó, banner Nhanh ghi “sinh câu hỏi đang bật” nhưng khi mở cấu hình thật, **Sinh câu hỏi** ở trạng thái tắt. Đây là ví dụ cho nguyên tắc: banner là bản tóm tắt; trạng thái từng control trong **Cài đặt** mới là bằng chứng vận hành.

### Quy trình tạo an toàn

1. Tạo KB test bằng Nâng cao nếu cần kiểm soát đầy đủ ngay từ đầu.
2. Chọn loại KB và Embedding.
3. Với Tài liệu, quyết định bật RAG, Wiki hoặc cả hai.
4. Với FAQ, chọn phạm vi nội dung được index và cách xử lý biến thể câu hỏi.
5. Đặt tên có môi trường và mục đích, ví dụ `TEST - Payment FAQ - 2026Q3`.
6. Lưu cấu hình, mở lại từng tab và chụp trạng thái trước khi nạp dữ liệu.
7. Nạp một mẫu nhỏ, kiểm thử, rồi mới mở rộng.

### Đừng dùng tên model như một quy tắc cố định

Danh sách model có thể đổi, và có model hiện trong dropdown nhưng backend không chấp nhận. Hãy chọn model đang lưu được trong chính KB, ghi ngày kiểm tra và tránh viết quy trình phụ thuộc vĩnh viễn vào một tên model.
<!-- /MODULE -->

<!-- MODULE:doc-03-tai-lieu-rag-wiki.md -->
## 03 - KB Tài liệu, RAG và Wiki {#03-tai-lieu-rag-wiki}

### Bạn sẽ biết gì sau khi đọc

- RAG và Wiki khác nhau ở đầu ra nào.
- Cách bật đồng thời RAG và Wiki.
- Giới hạn của Wiki và Graph đã quan sát được.

**Kiểm chứng giao diện: 06/08/2026.**

### Thuật ngữ

- **RAG:** tìm các đoạn liên quan trong nguồn và đưa chúng vào ngữ cảnh trả lời.
- **Wiki:** tổng hợp nội dung đã nạp thành các trang có cấu trúc và liên kết.
- **Graph:** biểu diễn các node và quan hệ được sinh từ nội dung.

### RAG và Wiki có thể bật cùng lúc

Trong tab **Tổng quan** của KB Tài liệu, RAG và Wiki là hai checkbox độc lập, không phải lựa chọn loại trừ. Khi bật Wiki, giao diện có ba mức chi tiết:

- **Tập trung**
- **Tiêu chuẩn** - caption quan sát được là “Số trang cân bằng.”
- **Toàn diện**

Caption “Số trang cân bằng” là mô tả, không phải trường nhập số trang.

| Nhu cầu | RAG | Wiki |
|---|---|---|
| Hỏi đáp nhanh và xem nguồn | Phù hợp | Có thể hỗ trợ gián tiếp |
| Đọc theo mục lục, hiểu bức tranh | Không phải đầu ra chính | Phù hợp |
| Kiểm soát câu chữ gốc | Dễ đối chiếu đoạn nguồn | Nội dung đã được tổng hợp lại |
| Phụ thuộc chất lượng nguồn | Cao | Rất cao vì có bước viết lại |

### Wiki trong trang làm việc

Tab Wiki của KB Tài liệu đã kiểm thử có:

- **Mục lục** và **Nhật ký hoạt động**.
- Cách xem theo **Thư mục** hoặc **Loại**.
- Khả năng tạo thư mục để tổ chức trang.
- Liên kết từ node Graph sang **Mở trong Wiki** khi node có trang liên quan.

![Tab Wiki với mục lục và trang tổng hợp](<knowledge/GS9 Knowledge VNG AI/image-09-wiki-muc-luc-va-trang.png>)

*Ảnh 03.1 - Wiki là lớp nội dung tổng hợp, tách với danh sách file gốc.*

### FAQ cũng hiện tab Wiki/Graph nhưng chưa có chức năng thật

Ở KB FAQ được kiểm thử, **Documents, Wiki, Graph** đều xuất hiện. Khi bấm Wiki hoặc Graph, trang chỉ báo:

> Wiki chưa được bật. Bật Wiki trong cài đặt Knowledge Base (chiến lược lập chỉ mục) để tự động tổng hợp trang wiki từ tài liệu.

FAQ không có control bật Wiki trong cấu hình. Vì vậy đây là khung giao diện dùng chung, không phải bằng chứng FAQ hỗ trợ Wiki/Graph.

### Graph và các loại node

Chú giải Graph quan sát được gồm **Tóm tắt, Thực thể, Khái niệm, Tổng hợp, So sánh**.

![Graph với chú giải năm loại node](<knowledge/GS9 Knowledge VNG AI/image-10-graph-cac-loai-node.png>)

*Ảnh 03.2 - Chú giải có Tổng hợp và So sánh, nhưng KB test vẫn chưa sinh được hai loại node này.*

Ngay sau phép thử nạp bộ Aurora/Borealis, chuyển Wiki sang **Toàn diện** và chạy **Phân tích lại**, Graph ghi nhận 93 node: Tóm tắt 9, Thực thể 42, Khái niệm 41, Tổng hợp 0, So sánh 0. Ở lượt đối chiếu cuối cùng cùng ngày, sau khi các nguồn tiếp tục được xử lý, Graph hiển thị 159/159 node: Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0, So sánh 0. Vì vậy 93 chỉ là ảnh chụp tại một thời điểm, không phải giới hạn cố định. Không tìm thấy nút tạo tay hai loại node này.

**Kết luận:** giao diện định nghĩa hai loại node, nhưng điều kiện sinh chúng chưa được xác định. Không viết hướng dẫn khẳng định “cứ có hai tài liệu liên quan là sinh node So sánh”.

### Khi nên bật Wiki

- Nguồn đã được làm sạch, heading rõ và không có hai phiên bản mâu thuẫn.
- Người đọc cần đi theo chủ đề, không chỉ hỏi từng câu rời rạc.
- Có người kiểm tra trang tổng hợp sau mỗi đợt cập nhật lớn.

Nếu ưu tiên tuyệt đối việc trích đúng câu chữ gốc, hãy bắt đầu với RAG và kiểm tra nguồn trước khi bật Wiki.
<!-- /MODULE -->

<!-- MODULE:doc-04-faq-va-lap-chi-muc.md -->
## 04 - KB FAQ và lập chỉ mục {#04-faq-va-lap-chi-muc}

### Bạn sẽ biết gì sau khi đọc

- Hai cấu hình lập chỉ mục của FAQ.
- Tác động của **Chỉ câu hỏi** và **Câu hỏi + trả lời**.
- Cách chọn **Gộp** hoặc **Tách** mà không suy đoán.

**Kiểm chứng giao diện: 06/08/2026.**

### Cấu trúc một mục FAQ

Form **Thêm Q&A** quan sát được có:

- 1 **Câu hỏi chuẩn**, tối đa 200 ký tự.
- Tối đa 10 **Câu hỏi tương tự**.
- Tối đa 10 **Câu hỏi loại trừ**.
- Tối đa 5 **Câu trả lời**.
- **Phân loại**.

![Biểu mẫu Thêm Q&A với câu hỏi chuẩn, biến thể, loại trừ và câu trả lời](<knowledge/GS9 Knowledge VNG AI/image-12-faq-bieu-mau-them-qa.png>)

*Ảnh 04.1 - Mỗi mục FAQ có thể chứa nhiều biến thể và nhiều câu trả lời.*

### Chế độ lập chỉ mục

| Chế độ | Nội dung tham gia tìm kiếm | Dùng khi |
|---|---|---|
| **Chỉ câu hỏi** | Câu hỏi chuẩn và biến thể | Muốn match tập trung, đã viết đủ cách hỏi |
| **Câu hỏi + trả lời** | Câu hỏi và nội dung trả lời | Người dùng có thể gõ mã lỗi, tên vật phẩm hoặc thuật ngữ chỉ có trong câu trả lời |

Phép kiểm thử dùng một từ khóa chỉ tồn tại trong câu trả lời:

- Ở **Chỉ câu hỏi**, không có kết quả kể cả khi ngưỡng bằng 0.
- Ở **Câu hỏi + trả lời**, mục đúng được tìm thấy.

Đây là khác biệt về phạm vi index, không chỉ là điểm similarity thấp.

### Cách index câu hỏi

| Cách | Cơ chế hiển thị đã quan sát | Ý nghĩa vận hành |
|---|---|---|
| **Tách** | Biến thể khớp có thể hiện riêng | Dễ biết cách hỏi nào kéo được mục |
| **Gộp** | Câu hỏi chuẩn và biến thể nằm trong đại diện gộp | Có thể thay đổi điểm theo toàn bộ cụm câu hỏi |

Một phép thử cho điểm Gộp 0,738 và Tách 0,718. Chênh lệch một mẫu không đủ để kết luận Gộp tốt hơn. Giữ **Tách** làm điểm xuất phát là hợp lý, sau đó đo trên ticket thật.

### Banner nói bị khóa, control vẫn lưu được

Trên FAQ đã có nội dung, giao diện cảnh báo index bị khóa. Thao tác thật vẫn đổi và lưu được cả hai cặp lựa chọn. Đây là **mâu thuẫn giao diện**.

Quy trình khi đổi:

1. Ghi lại cấu hình hiện tại.
2. Đổi một biến tại một thời điểm.
3. Lưu và mở lại để xác nhận giá trị được giữ.
4. Chạy bộ câu hỏi kiểm thử ở cùng ngưỡng.
5. Nếu kết quả xấu đi, phục hồi cấu hình cũ.

### Viết câu hỏi tốt

- Câu hỏi chuẩn mô tả ý định chính, không cố nhồi mọi từ khóa.
- Câu hỏi tương tự lấy từ cách người dùng nói thật: viết tắt, không dấu, tên màn hình cũ.
- Câu hỏi loại trừ dành cho ý định gần giống nhưng phải đi sang quy trình khác.
- Câu trả lời ghi rõ phạm vi, bước làm, ngoại lệ và thời điểm cần chuyển cấp.

### Không để FAQ trở thành kho câu trả lời mâu thuẫn

Nếu hai mục có câu hỏi gần nhau nhưng trả lời khác, thêm điều kiện phân biệt vào câu hỏi chuẩn và câu trả lời. Dùng **Kiểm tra tìm kiếm** để xem cả hai mục có cùng xuất hiện ở ngưỡng vận hành hay không.
<!-- /MODULE -->

<!-- MODULE:doc-05-mo-hinh-vlm-asr.md -->
## 05 - Model, VLM và ASR {#05-mo-hinh-vlm-asr}

### Bạn sẽ biết gì sau khi đọc

- Vai trò của model chat, Embedding, Wiki, VLM và ASR.
- Những gì đang bị khóa hoặc chưa hoạt động đầy đủ.
- Cách chọn model mà không phụ thuộc vào danh sách nhất thời.

**Kiểm chứng giao diện: 06/08/2026.**

### Các vai trò model

- **Chat / tóm tắt:** tạo tóm tắt, câu trả lời và nội dung tổng hợp.
- **Embedding:** biến nội dung thành vector để tìm tương đồng; thay model có thể làm thay đổi toàn bộ không gian tìm kiếm.
- **Tổng hợp Wiki:** dùng cho quá trình tạo trang Wiki ở KB Tài liệu.
- **VLM:** đọc nội dung hình ảnh.
- **ASR:** chuyển âm thanh thành văn bản.

![Tab Mô hình với model chat, Embedding, Wiki, VLM và ASR](<knowledge/GS9 Knowledge VNG AI/image-03-cau-hinh-mo-hinh-vlm-asr.png>)

*Ảnh 05.1 - Tab Mô hình của KB Tài liệu; cấu hình trong ảnh là trạng thái của KB test, không phải mặc định sản phẩm.*

### Trạng thái đã quan sát

Trong KB Tài liệu, dropdown chat tại thời điểm kiểm tra có:

- `gpt-oss-120b`
- `hosted_vllm/qwen3.6-35b`
- `qwen3.6-plus`

Trong FAQ, UI từng hiển thị thêm `deepseek-v4-flash`, nhưng backend từ chối lưu với lỗi `LLM model not found`. Đây là mâu thuẫn UI/backend và là lý do không coi “có trong dropdown” đồng nghĩa “dùng được”.

### Embedding

Khi KB đã có nội dung, model Embedding hiển thị khóa. Điều này hợp lý về vận hành vì đổi embedding cần lập chỉ mục lại toàn bộ nội dung. Hãy chốt model bằng KB test trước khi nạp dữ liệu lớn.

### VLM

Trong KB Tài liệu test, VLM đang bật và dùng `hosted_vllm/qwen3.6-35b`. Trạng thái này chỉ chứng minh cấu hình hiện hữu. Không suy ra VLM mặc định bật cho KB mới.

VLM đã xử lý được ảnh giao diện và tạo tóm tắt, nhưng OCR có thể đọc sai tên thương hiệu hoặc chữ nhỏ. Ảnh phải đi kèm caption văn bản; đừng để một quy trình quan trọng chỉ tồn tại trong ảnh.

### ASR

Khi bật toggle ASR, giao diện hiện thêm **Mô hình ASR** và **Ngôn ngữ**. Dropdown model quan sát được đang rỗng. Dòng cảnh báo cũ “Chưa có model - liên hệ admin” không còn xuất hiện trong giao diện hiện tại.

Kết luận đúng là: **chưa chọn được model ASR trong môi trường đã kiểm thử**. Không khẳng định toàn bộ sản phẩm không hỗ trợ ASR ở mọi môi trường.

### Cách chọn và ghi nhận model

1. Mở dropdown trong chính loại KB cần dùng.
2. Chọn model, bấm **Lưu** và xác nhận không có toast lỗi.
3. Mở lại tab để xem model có được giữ không.
4. Chạy cùng một bộ câu hỏi và ghi độ đúng, nguồn truy hồi, độ trễ.
5. Ghi tên model kèm ngày kiểm thử trong hồ sơ vận hành, không hard-code vào hướng dẫn dài hạn.

### Khi model lỗi

- Nếu UI cho chọn nhưng lưu lỗi, đổi sang model đã lưu được và ghi bằng chứng UI/backend.
- Nếu câu trả lời kém nhưng nguồn truy hồi đúng, kiểm tra model chat và prompt.
- Nếu nguồn truy hồi sai, ưu tiên kiểm tra embedding, dữ liệu và chunking trước khi đổi model chat.
<!-- /MODULE -->

<!-- MODULE:doc-06-parser-va-xu-ly-file.md -->
## 06 - Parser và xử lý file {#06-parser-va-xu-ly-file}

### Bạn sẽ biết gì sau khi đọc

- Parser là gì và vì sao cùng một file có thể cho kết quả khác.
- Ma trận lựa chọn parser theo định dạng ở giao diện hiện tại.
- Cách kiểm thử parser bằng nội dung thật, không chỉ nhìn trạng thái Hoàn tất.

**Kiểm chứng giao diện: 06/08/2026.**

### Parser là gì

Parser là bộ đọc và chuyển file thành nội dung để hệ thống lập chỉ mục. Tên engine trên giao diện gồm **Built-in, Simple, MinerU, LLM, markitdown, liteparse**. Không phải định dạng nào cũng có đủ mọi engine.

![Tab Xử lý với cấu hình parser theo từng định dạng file](<knowledge/GS9 Knowledge VNG AI/image-04-xu-ly-parser-theo-dinh-dang.png>)

*Ảnh 06.1 - Các lựa chọn parser thay đổi theo từng nhóm file.*

### Ma trận quan sát trực tiếp

| Nhóm file | Các lựa chọn thấy trong dropdown |
|---|---|
| PDF | Built-in, MinerU, LLM, markitdown, liteparse |
| Word | Built-in, MinerU, LLM, markitdown |
| PPT/PPTX | MinerU, markitdown |
| Excel | Built-in, MinerU, LLM, markitdown |
| CSV | Simple, LLM, markitdown |
| Markdown | Built-in, Simple, LLM, markitdown |
| TXT | Simple, LLM |
| JSON | Simple |
| Images | Built-in, Simple, MinerU |
| Email | Built-in, LLM |
| EPUB | Built-in |
| HTML | Built-in, markitdown |
| MHTML | Built-in |
| Audio | UI hiển thị Built-in đang chọn, nhưng dropdown chỉ có Simple |

Hai điểm cần ghi nhớ:

- PPT/PPTX **không có Built-in** trong dropdown đã kiểm tra.
- Audio có mâu thuẫn giữa giá trị đang hiển thị và lựa chọn có thể chọn.

### Hiểu tên engine theo hướng thực dụng

- **Built-in:** bộ đọc tích hợp của hệ thống.
- **Simple:** trích xuất đơn giản, phù hợp nội dung văn bản ít bố cục.
- **MinerU:** hướng tới tài liệu có bố cục, bảng hoặc hình phức tạp.
- **LLM:** dùng model để diễn giải cấu trúc; có thể tốn thời gian và tạo cách viết khác nguồn.
- **markitdown:** chuyển nhiều định dạng sang Markdown.
- **liteparse:** lựa chọn riêng quan sát được cho PDF.

Các mô tả trên giúp chọn bài test; không phải cam kết kỹ thuật nội bộ của từng engine.

### Quy trình A/B parser

1. Chọn một file đại diện có heading, bảng, chú thích ảnh và một mã độc nhất.
2. Giữ nguyên mọi cấu hình khác.
3. Xử lý bằng parser A, ghi số đoạn và nội dung một số đoạn.
4. Dùng **Phân tích lại với tùy chọn nâng cao** hoặc một KB test riêng để thử parser B.
5. Hỏi câu dựa vào bảng, heading và caption ảnh.
6. Chọn parser theo khả năng giữ đúng cấu trúc và dữ kiện, không theo độ dài tóm tắt.

### Dấu hiệu parser chưa phù hợp

- Heading bị nối vào đoạn trước.
- Cột bảng bị đảo hoặc mất tên cột.
- Text trong ảnh được đọc nhưng gắn sai khu vực.
- Một PDF dài chỉ thành một khối khó truy hồi.
- Tóm tắt nghe hợp lý nhưng mã, số và ngoại lệ biến mất.

### File Markdown vẫn cần cấu trúc tốt

Parser không thay thế việc viết heading. Với Markdown, đặt một `#` cho tên tài liệu và dùng `##` cho các ý định người dùng thường hỏi. Đây là cách bền vững hơn việc dựa vào ký hiệu trang trí hoặc chữ in đậm.
<!-- /MODULE -->

<!-- MODULE:doc-07-phan-doan-chunking.md -->
## 07 - Phân đoạn và chunking {#07-phan-doan-chunking}

### Bạn sẽ biết gì sau khi đọc

- Chunk là gì, chế độ cha-con dùng để làm gì.
- Cấu hình đang quan sát được trong KB test.
- Cách đo ảnh hưởng của phân đoạn bằng truy hồi thật.

**Kiểm chứng giao diện: 06/08/2026.**

### Chunk là gì

Chunk, hay phân đoạn, là đơn vị nội dung được dùng cho tìm kiếm. Chunk quá lớn dễ mang nhiều chủ đề; chunk quá nhỏ dễ mất điều kiện và ngoại lệ. Cấu hình tốt phụ thuộc cấu trúc nguồn và dạng câu hỏi.

### Trạng thái hiện hữu đã kiểm tra

Trong KB Tài liệu test:

- Chiến lược: **Tự động**.
- Chế độ: **Cha-con**.
- Kích thước cha: **32.768 ký tự**.
- Kích thước con: **8.192 ký tự**.
- Chồng lấp cha/con: **0 / 0**.
- **Truy hồi theo ngữ cảnh:** bật.
- **Sinh câu hỏi:** tắt.
- **Giới hạn token:** 0.
- Dấu phân cách hiển thị gồm dòng trống, dòng mới, `。`, `！`, `？`, `;`, `；`.
- Gợi ý ngôn ngữ có nút **DE, EN, ZH**; ô hiện để trống.

Đây là trạng thái của KB test, không phải cam kết mặc định cho mọi KB mới.

![Tab Xử lý với chế độ phân đoạn cha-con và các kích thước](<knowledge/GS9 Knowledge VNG AI/image-05-xu-ly-phan-doan-cha-con.png>)

*Ảnh 07.1 - Giao diện cấu hình chunk cha-con trong KB Tài liệu.*

### Hiểu chế độ cha-con

- **Chunk con** giúp tìm đúng phần nhỏ có từ ngữ liên quan.
- **Chunk cha** cung cấp bối cảnh rộng hơn cho câu trả lời.

Lợi ích chỉ có thật khi chunk cha chứa đúng ngữ cảnh của chunk con. Nếu file trộn nhiều chủ đề trong cùng section, tăng kích thước có thể kéo thêm nhiễu.

### Các chiến lược và điều cần đo

Giao diện có các lựa chọn phân đoạn khác nhau theo cấu hình. Không nên kết luận một chiến lược “tốt nhất” nếu chỉ nhìn preview. Với mỗi chiến lược, đo:

- Số chunk được tạo.
- Heading hoặc đường dẫn cấu trúc đi cùng chunk.
- Chunk chứa điều kiện, ngoại lệ và kết quả có bị tách không.
- Câu hỏi diễn đạt khác từ nguồn có truy hồi đúng không.
- Câu gần giống nhưng ngoài phạm vi có bị kéo nhầm không.

### Phép thử Phân tích lại đã thực hiện

Tài liệu `03-so-sanh-aurora-borealis.md` có 1 chunk trước khi chạy. Sau khi đổi độ chi tiết Wiki từ **Tiêu chuẩn** sang **Toàn diện** và bấm **Phân tích lại**:

- Trạng thái đi qua **Chờ xử lý, Đang hoàn tất, Hoàn tất**.
- Số chunk vẫn là 1.
- Thời gian tải lên không đổi.
- Tóm tắt được sinh lại và thay đổi cách diễn đạt.

Kết luận: **Phân tích lại** có thể tái xử lý và tái sinh tóm tắt, nhưng không bảo đảm số chunk thay đổi nếu cấu hình hoặc nội dung không tạo ranh giới khác.

### Bộ câu hỏi kiểm thử chunk

Với mỗi tài liệu, chuẩn bị ít nhất:

1. Câu hỏi có đáp án nằm trọn trong một mục.
2. Câu cần ghép điều kiện và ngoại lệ trong cùng mục.
3. Câu cần liên kết hai mục xa nhau.
4. Câu dùng từ đồng nghĩa, không trùng từ nguồn.
5. Câu có cùng từ khóa nhưng khác phạm vi.

Xem phần nguồn truy hồi trước khi đánh giá văn phong câu trả lời.
<!-- /MODULE -->

<!-- MODULE:doc-08-chia-se-va-nguon-du-lieu.md -->
## 08 - Chia sẻ và nguồn dữ liệu {#08-chia-se-va-nguon-du-lieu}

### Bạn sẽ biết gì sau khi đọc

- Cách chia sẻ KB qua Space và hai mức quyền.
- Các nguồn Notion, Google Drive, NAS và yêu cầu credential.
- Cách kết nối Google Drive bằng service account, chọn tài nguyên và cấu hình đồng bộ.
- Phần nào đã kiểm chứng, phần nào vẫn cần test qua nhiều chu kỳ.

**Kiểm chứng giao diện: 06-07/08/2026.**

### Chia sẻ qua Space

Tab **Chia sẻ** cho phép chọn Space và gán quyền:

- **Chỉnh sửa:** thành viên có thể thay đổi nội dung theo quyền hệ thống.
- **Chỉ đọc:** thành viên dùng để đọc, truy hồi hoặc hỏi đáp nhưng không sửa nội dung.

![Tab Chia sẻ với lựa chọn Space và quyền Chỉnh sửa hoặc Chỉ đọc](<knowledge/GS9 Knowledge VNG AI/image-06-chia-se-va-phan-quyen.png>)

*Ảnh 08.1 - Chia sẻ là quyết định quyền truy cập, không phải cách nạp dữ liệu.*

Trước khi chia sẻ:

1. Đặt owner của KB và owner nội dung.
2. Kiểm tra tài liệu có dữ liệu hạn chế không.
3. Cấp **Chỉ đọc** theo mặc định; chỉ cấp **Chỉnh sửa** cho nhóm vận hành.
4. Dùng một tài khoản hoặc thành viên đại diện để xác nhận quyền thật.

### Nguồn dữ liệu ngoài

Tab **Nguồn dữ liệu** quan sát được có ba connector:

- **Notion**
- **Google Drive**
- **NAS**

![Tab Nguồn dữ liệu với Notion, Google Drive và NAS](<knowledge/GS9 Knowledge VNG AI/image-07-nguon-du-lieu-notion-drive-nas.png>)

*Ảnh 08.2 - Khi chưa cấu hình, trang hiện nút thêm nguồn dữ liệu đầu tiên.*

Wizard có bốn bước:

1. Chọn loại.
2. Thông tin xác thực.
3. Tài nguyên.
4. Chiến lược.

### Trường xác thực đã quan sát

| Nguồn | Trường chính |
|---|---|
| Notion | Tên, Integration Token, kiểm tra kết nối |
| Google Drive | Tên, Service account JSON, Shared Drive ID tùy chọn |
| NAS | Tên, UNC share, username, password |

### Google Drive - chuẩn bị quyền và xác thực

Google Drive connector dùng scope chỉ đọc `drive.readonly`. Quy trình đã kiểm chứng ngày 07/08/2026:

1. Tạo hoặc chọn một Google Cloud project.
2. Bật **Google Drive API** trong đúng project.
3. Tạo service account riêng; không cần gán Google Cloud role chỉ để đọc tài nguyên Drive đã được chia sẻ.
4. Trong tab **Keys**, tạo key loại JSON. Google tự sinh `private_key`; không thêm key thủ công.
5. Chia sẻ đúng thư mục nguồn cho `client_email` của service account với quyền **Viewer**.
6. Trong Knowledge VNG, dán nguyên JSON. Để trống **Shared Drive ID** khi nguồn nằm trong My Drive.
7. Bấm **Kiểm tra kết nối** trước khi đi tiếp.

![Màn hình xác thực Google Drive bằng service-account JSON](<knowledge/GS9 Knowledge VNG AI/image-15-google-drive-xac-thuc-service-account.png>)

*Ảnh 08.3 - Không chụp hoặc lưu nội dung JSON key; ảnh chỉ ghi nhận các trường cấu hình.*

Lỗi tổng quát `connection validation failed` đã xuất hiện khi Drive API chưa được bật. Sau khi Enable API trong đúng project, cùng service account và key đi tiếp được; không cần tạo lại credential.

### Google Drive - chọn tài nguyên

![Cây chọn thư mục và tệp Google Drive](<knowledge/GS9 Knowledge VNG AI/image-16-google-drive-chon-tai-nguyen.png>)

*Ảnh 08.4 - Có thể chọn một tệp hoặc thư mục; dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

Trạng thái quan sát được:

- ✓ màu cam: đã chọn.
- − màu cam ở thư mục: chọn một phần nội dung con.
- vòng tròn trắng: chưa chọn.
- **Hiện chưa hỗ trợ:** connector thấy tài nguyên nhưng chưa hỗ trợ loại đó.

Chọn thư mục khi muốn tệp mới trong thư mục thuộc phạm vi đồng bộ. Chọn một tệp để thử nghiệm hẹp. Không chọn thư mục chứa credential như `keys`.

### Google Drive - lịch, chế độ và xung đột

![Lịch và cách đồng bộ Google Drive](<knowledge/GS9 Knowledge VNG AI/image-17-google-drive-lich-va-cach-dong-bo.png>)

*Ảnh 08.5 - Lượt test dùng Tăng dần, Ghi đè và mỗi 15 phút.*

| Control | Lựa chọn đã quan sát | Cách dùng |
|---|---|---|
| Lịch | Phút, Giờ, Hằng ngày, Hằng tuần, Hằng tháng | Chọn theo nhịp cập nhật nguồn; 15 phút phù hợp test, không phải mặc định bắt buộc |
| Chế độ | Tăng dần, Toàn bộ | Tăng dần cho vận hành; Toàn bộ khi cần quét lại có chủ đích |
| Xung đột | Ghi đè, Bỏ qua nếu đã có | Ghi đè khi Drive là nguồn chuẩn; Bỏ qua để giữ bản hiện có trong KB |

### Google Drive - lọc tệp và tag

![Regex lọc tệp và gắn tag](<knowledge/GS9 Knowledge VNG AI/image-18-google-drive-loc-tep-va-tag.png>)

*Ảnh 08.6 - Có thể thêm nhiều regex tên tệp, tag mặc định và rule tag theo đường dẫn.*

- Để trống regex để nhận mọi tệp hợp lệ trong phạm vi đã chọn.
- Khi có nhiều mẫu, tệp khớp một trong các regex sẽ được đồng bộ.
- `(?i)` cho phép không phân biệt hoa/thường.
- Rule tag theo đường dẫn có thể dùng capture regex như `$1` hoặc `${name}`.
- Trước khi dùng production, thử một tệp khớp và một tệp không khớp.

### Google Drive - ghi đè xử lý

![Ghi đè chunking cho nguồn Google Drive](<knowledge/GS9 Knowledge VNG AI/image-19-google-drive-ghi-de-xu-ly.png>)

*Ảnh 08.7 - Giá trị 0 dùng mặc định KB; chỉ ghi đè khi có bộ câu hỏi đối chứng.*

Nguồn có thể ghi đè kích thước đoạn, độ chồng, giới hạn token, đoạn cha-con, ký tự phân tách và ngôn ngữ. Khuyến nghị giữ `0` hoặc để trống ở lượt đầu để kế thừa cấu hình KB.

![Đa phương thức, ASR, OCR và parser theo loại tệp](<knowledge/GS9 Knowledge VNG AI/image-20-google-drive-da-phuong-thuc-va-parser.png>)

*Ảnh 08.8 - Các toggle và parser kế thừa yêu cầu model/cấu hình tương ứng của KB.*

- Bật đa phương thức khi cần phân tích hình và đã có VLM.
- Bật ASR cho âm thanh khi có model ASR khả dụng.
- Chỉ ép OCR toàn bộ PDF khi tài liệu là scan hoặc text-layer hỏng.
- Sinh câu hỏi là tùy chọn bổ sung, không thay thế nội dung nguồn tốt.

### Google Drive - parser theo loại tệp

![Parser cho Office, CSV, Markdown và văn bản](<knowledge/GS9 Knowledge VNG AI/image-21-google-drive-parser-office-text.png>)

![Parser cho JSON, ảnh, email, ebook và web](<knowledge/GS9 Knowledge VNG AI/image-22-google-drive-parser-media-web.png>)

*Ảnh 08.9-08.10 - Danh sách parser quan sát trong wizard ngày 07/08/2026.*

| Loại | Parser đang hiển thị trong lượt test |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in; Tự nhận diện hoặc Thủ công |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

Danh sách parser có thể phụ thuộc tenant và thay đổi theo thời điểm.

![Chọn parser Excel tùy chỉnh](<knowledge/GS9 Knowledge VNG AI/image-24-google-drive-parser-excel-tuy-chinh.png>)

*Ảnh 08.11 - Các parser có tiền tố FPA là cấu hình riêng của tenant test, không phải mặc định chung.*

Khi Excel để **Thủ công**, dropdown có thể hiện parser do tenant đăng ký. Chỉ chọn parser tùy chỉnh khi cấu trúc workbook đúng với parser đó; nếu không, dùng Tự nhận diện hoặc cấu hình mặc định đã kiểm thử.

### Google Drive - đồng bộ xóa

![Tùy chọn đồng bộ xóa](<knowledge/GS9 Knowledge VNG AI/image-23-google-drive-dong-bo-xoa.png>)

*Ảnh 08.12 - UI mô tả bật control sẽ gỡ tri thức khi nguồn đã bị xóa.*

Khuyến nghị để **tắt** trong lượt thử đầu. Chỉ bật sau khi đã thử bằng tệp không quan trọng và xác nhận quy trình backup/phục hồi. Lượt ngày 07/08/2026 mới quan sát control, chưa thử xóa end-to-end.

### Kết quả kết nối và đồng bộ đầu tiên

![Google Drive đã kết nối và đồng bộ thành công](<knowledge/GS9 Knowledge VNG AI/image-25-google-drive-dong-bo-thanh-cong.png>)

*Ảnh 08.13 - Card nguồn hiển thị Đã kết nối và Kết quả Thành công.*

Lượt kiểm chứng hiển thị:

- Chế độ: **Tăng dần**.
- Phạm vi: **Một tệp**.
- Lịch: **Mỗi 15 phút**.
- Đồng bộ gần nhất: **Vừa xong**.
- Kết quả: **Thành công**.

Kết quả này xác nhận wizard bước 3-4 và lượt đồng bộ đầu tiên trong điều kiện test. Sau đó vẫn phải mở Documents, kiểm tra trạng thái xử lý, nội dung chunk và chat bằng câu hỏi đối chứng.

### Phần chưa xác định sau lượt Google Drive đầu tiên

Chưa khẳng định:

- Tăng dần và Toàn bộ cho kết quả ra sao qua nhiều chu kỳ.
- Regex, tag theo đường dẫn hoặc parser tùy chỉnh áp dụng đúng trên mọi bộ dữ liệu.
- Sửa, đổi tên, di chuyển, xóa hoặc thu hồi quyền ở Drive phản ánh thế nào vào KB.
- Đồng bộ xóa có thể phục hồi bằng quy trình nào.
- Shared Drive hoạt động giống My Drive; lượt test này để trống Shared Drive ID.
- Notion và NAS đi hết bước 3-4; hai connector này vẫn thiếu credential test.

### Không tự suy luận hành vi đồng bộ

Cho đến khi có ma trận nhiều chu kỳ, không khẳng định:

- file bị xóa ở nguồn sẽ tự bị xóa trong KB;
- quyền xem ở Notion/Drive được giữ nguyên sau đồng bộ;
- cập nhật xảy ra ngay lập tức;
- mọi định dạng trong nguồn ngoài dùng cùng parser với upload tay.

Khi có credential test, cần chạy ma trận: thêm file, sửa file, đổi tên, di chuyển, xóa, thu hồi quyền và lỗi kết nối.

### Bảo mật credential

- Không chụp token hoặc JSON key vào tài liệu hướng dẫn.
- Không đặt credential trong file Markdown của KB.
- Dùng tài khoản dịch vụ có quyền tối thiểu.
- Với Drive, ưu tiên Viewer trên đúng thư mục; không chia sẻ toàn bộ My Drive.
- Ghi người sở hữu credential và quy trình xoay vòng ngoài KB nội dung.
<!-- /MODULE -->

<!-- MODULE:doc-09-van-hanh-documents-wiki-graph.md -->
## 09 - Vận hành Documents, Wiki và Graph {#09-van-hanh-documents-wiki-graph}

### Bạn sẽ biết gì sau khi đọc

- Các cách thêm nội dung vào KB Tài liệu.
- Hành vi của Lưu nháp, Sửa nội dung và Phân tích lại.
- Giới hạn đã biết của upload thư mục và Graph.

**Kiểm chứng giao diện: 06/08/2026.**

### Menu Thêm tài liệu

Menu quan sát được có:

- **Tải tệp lên**
- **Tải thư mục lên**
- **Nhập từ URL** - đang disabled
- **Soạn thảo trực tuyến**

![Menu thêm tài liệu với tải tệp, tải thư mục, nhập URL và soạn trực tuyến](<knowledge/GS9 Knowledge VNG AI/image-08-tai-tep-thu-muc-va-soan-thao.png>)

*Ảnh 09.1 - `Nhập từ URL` đang vô hiệu hóa tại thời điểm kiểm tra.*

### Tải tệp lên

1. Bấm **Thêm tài liệu > Tải tệp lên**.
2. Chọn file hoặc kéo thả.
3. Mở **Xử lý nâng cao** nếu cần ghi đè parser/chunk cho lượt nạp.
4. Bấm tải lên và chờ **Hoàn tất**.
5. Mở chi tiết file để xem tóm tắt, toàn văn và phân đoạn.

Trạng thái Hoàn tất chỉ xác nhận pipeline kết thúc; vẫn phải kiểm tra nội dung phân đoạn và chat.

### Nạp một bộ Markdown có ảnh

1. Xác nhận KB asset có đủ 49 ảnh PNG đã được kiểm tra định dạng thật và mọi file đều có mapping MinIO.
2. Chạy build nghiêm ngặt.
3. Chỉ chọn đúng 20 file `.md` trong `knowledge/GS9 Knowledge VNG AI/` để nạp vào KB sử dụng.
4. Không chọn `knowledge/GS9 Knowledge VNG - Image Assets/` và không nạp PNG cùng bộ Markdown.
5. Sau khi xử lý xong, hỏi câu buộc trả lời kèm ảnh và mở nguồn tham khảo để kiểm tra URI.

### Tải thư mục lên

Modal thật dùng input `multiple` và `webkitdirectory`, có **Xử lý nâng cao**. Tuy nhiên extension không gắn được thư mục vào hộp chọn native, nên phép thử end-to-end “chọn thư mục thật rồi xác nhận cấu trúc” bị chặn.

Các file Aurora/Borealis được nạp riêng để tiếp tục test nội dung, không được dùng làm bằng chứng upload thư mục giữ cấu trúc thư mục con.

### Soạn thảo trực tuyến, Lưu nháp và Xuất bản

Phép thử tạo tài liệu `AUDIT-NHAP-20260806`:

- Bấm **Lưu nháp** hiện toast “Đã lưu bản nháp”.
- Tài liệu xuất hiện với trạng thái **Bản nháp**.
- Chat hỏi mã độc nhất trong bản nháp không truy hồi được nội dung đó.

Kết luận vận hành: dùng **Lưu nháp** để giữ nội dung chưa phát hành; cần **Xuất bản** và chờ lập chỉ mục nếu muốn chat sử dụng.

### Sửa nội dung tài liệu MANUAL

Với tài liệu tạo bằng Soạn thảo trực tuyến, menu chi tiết có nhãn chính xác **Sửa nội dung**.

Phép thử:

1. Tài liệu gốc có 3 chunk.
2. Thêm marker kiểm thử và bấm **Xuất bản**.
3. Toast báo bắt đầu lập chỉ mục; trạng thái đi qua Chờ xử lý, Đang hoàn tất, Hoàn tất.
4. Tóm tắt có marker và số chunk thành 4.
5. Phục hồi đúng nội dung gốc, Xuất bản lại; marker biến mất và số chunk trở về 3.

Do đó, **Sửa nội dung + Xuất bản** thực sự kích hoạt lập chỉ mục lại.

### Phân tích lại

**Phân tích lại** giữ tài liệu trong KB và chạy pipeline lần nữa. Trong test Aurora/Borealis, thời gian tải lên không đổi, tóm tắt đổi cách diễn đạt, số chunk giữ nguyên. Ghi ảnh hoặc số liệu trước/sau nếu muốn đánh giá thay đổi; đừng dựa vào cảm giác.

### Wiki và Graph sau cập nhật

Sau khi nạp thêm ảnh và tài liệu, Graph tăng từ 66 lên 93 node. Ở lượt đối chiếu cuối cùng, Graph tiếp tục tăng lên 159 node khi các nguồn nền tiếp tục hoàn tất; phân bố lúc đó là Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0 và So sánh 0. Số node thay đổi chứng minh Graph tiếp tục được cập nhật, nhưng **Tổng hợp** và **So sánh** vẫn bằng 0 ngay cả khi có tài liệu so sánh rõ và Wiki ở mức Toàn diện.

Không có nút tạo tay hai node này trong menu node hoặc hướng dẫn canvas đã quan sát. Điều kiện sinh vẫn là backlog.

### Quy trình vận hành một thay đổi

1. Lưu bản nguồn có phiên bản.
2. Sửa một nhóm nội dung.
3. Nạp hoặc Xuất bản.
4. Chờ Hoàn tất.
5. So sánh số chunk, tóm tắt và nguồn truy hồi.
6. Chạy bộ câu hỏi hồi quy.
7. Kiểm tra Wiki/Graph nếu đang dùng.
8. Ghi ngày, người thực hiện và kết quả.
<!-- /MODULE -->

<!-- MODULE:doc-10-van-hanh-faq.md -->
## 10 - Vận hành FAQ {#10-van-hanh-faq}

### Bạn sẽ biết gì sau khi đọc

- Cách thêm, kiểm tra, nhập và xuất FAQ.
- Cách dùng ngưỡng tìm kiếm.
- Quy trình backup trước thao tác thay toàn bộ.

**Kiểm chứng giao diện: 06/08/2026.**

### Thanh công cụ FAQ

Trang Documents của FAQ đã kiểm tra có:

- **Chọn tất cả**
- **Kiểm tra tìm kiếm**
- **Xuất**
- **Nhập**
- **Thêm Q&A**

![Danh sách FAQ với các nút kiểm tra tìm kiếm, xuất, nhập và thêm Q&A](<knowledge/GS9 Knowledge VNG AI/image-11-faq-danh-sach-nhap-xuat-tim-kiem.png>)

*Ảnh 10.1 - Trang vận hành FAQ tập trung vào từng mục Q&A và chất lượng tìm kiếm.*

### Thêm Q&A bằng tay

1. Bấm **Thêm Q&A**.
2. Viết câu hỏi chuẩn rõ ý định.
3. Thêm biến thể từ ticket thật.
4. Thêm câu loại trừ nếu có ý định gần giống.
5. Viết câu trả lời và phạm vi áp dụng.
6. Gán phân loại.
7. Lưu và chạy **Kiểm tra tìm kiếm** ngay.

### Kiểm tra tìm kiếm

Modal quan sát được có:

- Ngưỡng từ **0 đến 1**, bước **0,1**, giá trị mở ra là **0,5**.
- Số kết quả tối đa từ **1 đến 50**, giá trị mở ra là **10**.

Câu đối chứng “Server bảo trì lúc nào?” ở ngưỡng 0 trả về mục chính xác với điểm 1,000. Từ khóa chỉ nằm trong câu trả lời không trả kết quả ở chế độ Chỉ câu hỏi, kể cả ngưỡng 0.

Không đặt ngưỡng chỉ từ một câu hỏi. Thu thập:

- câu đúng nguyên văn;
- câu diễn đạt lại;
- câu gần giống nhưng phải loại trừ;
- câu ngoài phạm vi;
- câu có mã lỗi hoặc tên riêng.

Chọn ngưỡng cân bằng bỏ sót và kéo nhầm theo rủi ro nghiệp vụ.

### Xuất FAQ

Nút **Xuất** đã tạo file CSV gồm 5 dòng Q&A. Header file xuất dùng tiếng Anh và một số trường nhiều giá trị nối bằng `##`.

Chính file CSV xuất đó được chọn lại trong modal **Nhập**; hệ thống đọc đủ 5 mục và bật nút Nhập. Phép thử dừng ở preview để tránh tạo trùng.

Kết luận: **Xuất** là bước backup thực dụng trước khi nhập thay toàn bộ, dù header của file xuất khác header tiếng Việt trong CSV mẫu.

### Nhập và file mẫu

Menu tải file mẫu có **JSON, CSV, Excel**. Bộ mẫu dự án nằm trong `samples/faq/` và được chuẩn hóa từ template của tool.

Trước khi nhập:

1. Xuất backup hiện tại.
2. Kiểm tra số mục trong file nguồn.
3. Xác nhận cách xử lý câu hỏi tương tự, loại trừ và nhiều câu trả lời.
4. Dùng chế độ thêm vào nếu đang thử.
5. Chỉ dùng **Thay toàn bộ** trong KB test hoặc khi đã có kế hoạch phục hồi.

### Sau nhập

- Đối chiếu số mục.
- Mở ngẫu nhiên ít nhất 5 mục.
- Kiểm tra ký tự tiếng Việt, xuống dòng và dấu phân cách `##`.
- Chạy bộ câu hỏi hồi quy ở cùng cấu hình index và ngưỡng.
- Lưu file nguồn cùng ngày nhập và người thực hiện.
<!-- /MODULE -->

<!-- MODULE:doc-11-chat-kiem-thu-va-bao-tri.md -->
## 11 - Chat, kiểm thử và bảo trì {#11-chat-kiem-thu-va-bao-tri}

### Bạn sẽ biết gì sau khi đọc

- Cách đánh giá một câu trả lời bằng nguồn, không chỉ bằng văn phong.
- Cách làm ảnh xuất hiện trong chat Knowledge VNG.
- Cách duy trì KB mà không mất khả năng phục hồi.

**Kiểm chứng giao diện: 06/08/2026.**

### Quy trình kiểm thử chat

1. Chờ tài liệu ở trạng thái **Hoàn tất**.
2. Mở **Trò chuyện**.
3. Hỏi một câu có đáp án rõ trong nguồn.
4. Mở **Nguồn tham khảo** hoặc các bước truy hồi.
5. Kiểm tra file và đoạn được lấy có đúng không.
6. Đánh giá câu trả lời có giữ đúng điều kiện, số liệu và ngoại lệ không.
7. Hỏi lại bằng từ khác.
8. Hỏi một câu ngoài phạm vi để kiểm tra hệ thống có bịa hoặc kéo nguồn gần giống không.

### Chẩn đoán theo lớp

| Hiện tượng | Kiểm tra trước |
|---|---|
| Không có nguồn đúng | File đã xuất bản, trạng thái, index, parser, chunking |
| Có nguồn nhưng thiếu đoạn quan trọng | Ranh giới chunk, heading, kích thước cha-con |
| Nguồn đúng nhưng trả lời sai | Model chat, prompt, nội dung mâu thuẫn |
| FAQ kéo nhầm mục | Biến thể, câu loại trừ, chế độ index, ngưỡng |
| Ảnh được mô tả nhưng không hiện | Loại đường dẫn ảnh trong Markdown |

### Ảnh trong chat: kết quả kiểm thử

Khi Markdown dùng đường dẫn tương đối `assets/...`, retriever tìm thấy file và nội dung ảnh, nhưng câu trả lời chỉ ghi mô tả và không có thẻ ảnh.

Khi Markdown dùng URI nội bộ `minio://...`, retriever chuyển liên kết thành ảnh và câu trả lời hiển thị đúng hình.

![Câu trả lời Knowledge VNG hiển thị ảnh khi nguồn Markdown dùng URI MinIO](<knowledge/GS9 Knowledge VNG AI/image-13-chat-hien-thi-anh-minio.png>)

*Ảnh 11.1 - Trường hợp đạt: ảnh xuất hiện trực tiếp trong câu trả lời chat.*

Quy trình chuẩn cho bộ Knowledge có ảnh:

1. Giữ ảnh local trong `knowledge/GS9 Knowledge VNG - Image Assets/` để dựng HTML offline.
2. Nạp ảnh một lần vào KB asset có vòng đời ổn định.
3. Lấy và lưu URI MinIO trong `knowledge/GS9 Knowledge VNG AI/image-map.json`.
4. Chạy builder để sinh liên kết MinIO vào 20 file phân phối.
5. Chỉ nạp 20 file MD vào KB sử dụng; không nạp PNG vào KB sử dụng.
6. Hỏi câu có chủ đích “trả lời kèm hình minh họa”.
7. Xác nhận ảnh thật xuất hiện và nguồn Markdown dùng URI của KB asset.
8. Không xóa KB asset hoặc ảnh độc lập khi còn Markdown tham chiếu.

### Bản nháp không phải nguồn chat

Phép thử mã độc nhất trong tài liệu **Bản nháp** không được truy hồi. Vì vậy checklist phát hành phải có bước **Xuất bản**, chờ index và chạy câu hỏi xác nhận.

### Bộ kiểm thử tối thiểu

Mỗi KB nên có một file kiểm thử gồm:

- 5 câu hỏi đúng nguyên văn.
- 5 câu diễn đạt tự nhiên hoặc không dấu.
- 3 câu cần điều kiện/ngoại lệ.
- 3 câu gần giống nhưng không cùng ý định.
- 3 câu ngoài phạm vi.
- 2 câu yêu cầu ảnh nếu nội dung có ảnh.

Ghi kết quả theo ngày, model, cấu hình index/chunk và phiên bản nguồn.

### Bảo trì

- Chỉ định owner nghiệp vụ và owner kỹ thuật.
- Ghi phiên bản, ngày hiệu lực và lịch xem lại cho nguồn.
- Xuất FAQ trước thay đổi lớn; giữ file gốc của KB Tài liệu ngoài hệ thống.
- Sau khi đổi model, parser, chunking hoặc index, chạy lại toàn bộ câu hỏi hồi quy.
- Khi thêm hoặc thay ảnh, kiểm tra lại định dạng thật trước khi upload; nếu cần transcode, giữ nguyên tên và kích thước ảnh khi phù hợp.
- Không xóa ảnh độc lập nếu MD còn tham chiếu URI MinIO của ảnh đó.
- Ghi các mục chưa kiểm chứng riêng, không trộn thành hướng dẫn chắc chắn.

### Tiêu chí phát hành

Một KB sẵn sàng khi:

1. Nguồn đã có owner và phiên bản.
2. Cấu hình nền tảng được ghi lại.
3. Các file đều Hoàn tất và nội dung phân đoạn đọc được.
4. Bộ câu hỏi đúng, gần đúng, loại trừ và ngoài phạm vi đã chạy.
5. Nguồn truy hồi đúng, không chỉ câu trả lời nghe hay.
6. Ảnh quan trọng đã được kiểm thử đến đầu ra chat.
7. Có backup và quy trình phục hồi.
<!-- /MODULE -->

<!-- MODULE:doc-12-ket-noi-google-drive.md -->
## 12 - Kết nối Google Drive {#12-ket-noi-google-drive}

### Bạn sẽ biết gì sau khi đọc

- Cách tạo quyền đọc tối thiểu bằng service account.
- Cách chọn đúng thư mục hoặc tệp trên Google Drive.
- Cách chọn lịch, chế độ, xung đột, filter, tag và parser.
- Cách nhận biết lượt đồng bộ đầu tiên đã thành công.
- Phần nào vẫn phải kiểm thử trước khi dùng production.

**Kiểm chứng giao diện và lượt đồng bộ đầu tiên: 07/08/2026.**

### 1. Chuẩn bị Google Cloud và quyền Drive

1. Tạo hoặc chọn Google Cloud project dành cho connector.
2. Bật **Google Drive API** trong đúng project.
3. Tạo service account riêng và tạo key JSON trong tab **Keys**.
4. Chia sẻ đúng thư mục nguồn cho `client_email` với quyền **Viewer**.
5. Không đưa JSON key vào Drive, KB, Markdown hoặc ảnh chụp.

![Nhập service-account JSON cho Google Drive](<knowledge/GS9 Knowledge VNG AI/image-15-google-drive-xac-thuc-service-account.png>)

*Ảnh 12.1 - Dán nguyên JSON; để trống Shared Drive ID khi nguồn nằm trong My Drive.*

Nếu **Kiểm tra kết nối** trả về `connection validation failed`, kiểm tra Drive API trước. Trong phép thử thực tế, kết nối đi tiếp ngay sau khi Enable API; không cần tạo lại key.

### 2. Chọn tài nguyên

![Chọn thư mục hoặc tệp Google Drive](<knowledge/GS9 Knowledge VNG AI/image-16-google-drive-chon-tai-nguyen.png>)

*Ảnh 12.2 - Dấu trừ ở thư mục cha nghĩa là chỉ một phần con được chọn.*

- Chọn thư mục để tệp mới trong thư mục thuộc phạm vi đồng bộ.
- Chọn một tệp để thử nghiệm hẹp.
- Mục có nhãn **Hiện chưa hỗ trợ** sẽ không được xử lý.
- Không chọn thư mục `keys` hoặc vùng chứa credential.

### 3. Chọn lịch và cách đồng bộ

![Lịch, chế độ và chiến lược xung đột](<knowledge/GS9 Knowledge VNG AI/image-17-google-drive-lich-va-cach-dong-bo.png>)

*Ảnh 12.3 - Lượt test dùng Tăng dần, Ghi đè và mỗi 15 phút.*

| Cấu hình | Khuyến nghị ban đầu |
|---|---|
| Lịch | 15 phút để test; Giờ hoặc Hằng ngày cho phần lớn nguồn vận hành |
| Chế độ | **Tăng dần** cho vận hành thường xuyên |
| Xung đột | **Ghi đè** khi Drive là nguồn chuẩn; Bỏ qua khi cần giữ bản đang có trong KB |

Chỉ dùng **Toàn bộ** khi cần quét lại có chủ đích. Sau khi đổi chiến lược, luôn chạy bộ câu hỏi đối chứng.

### 4. Lọc tệp và tag

![Regex lọc tên tệp và gắn tag](<knowledge/GS9 Knowledge VNG AI/image-18-google-drive-loc-tep-va-tag.png>)

*Ảnh 12.4 - Để trống regex để đồng bộ mọi tệp hợp lệ trong phạm vi.*

- Nhiều regex hoạt động theo điều kiện khớp một trong các mẫu.
- Dùng `(?i)` để không phân biệt hoa/thường.
- Thử ít nhất một tên khớp và một tên không khớp trước production.
- Tag mặc định nên mô tả nguồn/nghiệp vụ; rule theo đường dẫn chỉ dùng khi cấu trúc thư mục ổn định.

### 5. Giữ mặc định xử lý ở lượt đầu

![Ghi đè chunking ở cấp nguồn](<knowledge/GS9 Knowledge VNG AI/image-19-google-drive-ghi-de-xu-ly.png>)

*Ảnh 12.5 - Giá trị 0 dùng cấu hình mặc định của KB.*

Giữ kích thước đoạn, độ chồng và token ở `0`; để trống ký tự phân tách nếu chưa có lý do kiểm thử rõ ràng. Chỉ bật đoạn cha-con khi nội dung cần giữ ngữ cảnh cha lớn hơn.

![Đa phương thức, ASR, OCR và parser](<knowledge/GS9 Knowledge VNG AI/image-20-google-drive-da-phuong-thuc-va-parser.png>)

*Ảnh 12.6 - VLM, ASR và OCR cần model/cấu hình tương ứng.*

- Đa phương thức: bật khi cần đọc hình và KB có VLM.
- ASR: bật cho âm thanh khi có model ASR khả dụng.
- Ép OCR toàn bộ PDF: chỉ dùng cho scan hoặc text-layer hỏng.
- Sinh câu hỏi: tùy chọn bổ sung, không sửa được nguồn viết kém.

### 6. Chọn parser đúng loại tệp

![Parser cho Office, CSV, Markdown và text](<knowledge/GS9 Knowledge VNG AI/image-21-google-drive-parser-office-text.png>)

![Parser cho media, email, ebook và web](<knowledge/GS9 Knowledge VNG AI/image-22-google-drive-parser-media-web.png>)

*Ảnh 12.7-12.8 - Parser quan sát được ngày 07/08/2026; danh sách có thể đổi theo tenant.*

| Loại | Parser quan sát được |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

![Parser Excel tùy chỉnh](<knowledge/GS9 Knowledge VNG AI/image-24-google-drive-parser-excel-tuy-chinh.png>)

*Ảnh 12.9 - Các parser có tiền tố FPA là cấu hình riêng của tenant test.*

Excel **Thủ công** có thể liệt kê parser do tenant đăng ký. Không chọn parser tùy chỉnh chỉ vì tên nghe phù hợp; workbook phải đúng cấu trúc mà parser yêu cầu.

### 7. Thận trọng với đồng bộ xóa

![Bật hoặc tắt đồng bộ xóa](<knowledge/GS9 Knowledge VNG AI/image-23-google-drive-dong-bo-xoa.png>)

*Ảnh 12.10 - UI mô tả bật control sẽ gỡ tri thức khi tệp nguồn bị xóa.*

Để **tắt trong lượt thử đầu**. Chỉ bật sau khi thử bằng tệp không quan trọng, có backup và đã xác nhận cách phục hồi. Lượt ngày 07/08/2026 chưa thử hành vi xóa end-to-end.

### 8. Tạo nguồn và xác nhận thành công

Bấm **Tạo & đồng bộ ngay**. Card nguồn phải cho biết trạng thái, chế độ, phạm vi, lịch, thời điểm gần nhất và kết quả.

![Google Drive đã kết nối và đồng bộ thành công](<knowledge/GS9 Knowledge VNG AI/image-25-google-drive-dong-bo-thanh-cong.png>)

*Ảnh 12.11 - Lượt test hiển thị Đã kết nối và Kết quả Thành công.*

Lượt đã kiểm chứng dùng **Tăng dần**, phạm vi **Một tệp**, lịch **Mỗi 15 phút** và kết quả **Thành công**. Sau đó vẫn phải:

1. Mở Documents và xác nhận tài liệu đã xuất hiện.
2. Chờ trạng thái xử lý hoàn tất.
3. Mở chunk để kiểm tra nội dung parser.
4. Hỏi câu đúng, gần đúng, loại trừ và ngoài phạm vi.
5. Kiểm tra nguồn truy hồi, không chỉ đánh giá câu trả lời nghe hợp lý.

### Chưa được phép suy luận

Một lượt thành công chưa chứng minh:

- Tăng dần và Toàn bộ đúng qua nhiều chu kỳ.
- Regex, tag và parser tùy chỉnh đúng cho mọi dữ liệu.
- Sửa, đổi tên, di chuyển, xóa hoặc thu hồi quyền phản ánh đúng vào KB.
- Shared Drive giống My Drive; lượt test này không điền Shared Drive ID.

Xem bằng chứng chi tiết tại [audit Google Drive ngày 07/08/2026](audit/audit-google-drive-connector-2026-08-07.md).
<!-- /MODULE -->

<!-- MODULE:doc-13-agent-tong-quan-va-kien-truc.md -->
## 13 - Agent: tổng quan và kiến trúc {#13-agent-tong-quan-va-kien-truc}

**Phạm vi và ngày kiểm chứng: 11/08/2026.** Module này là điểm vào ngắn cho cả vận hành và kỹ thuật; các control chi tiết nằm ở module 14–19.

### Khái niệm

Agent là lớp điều phối cuộc hội thoại giữa Human, model, Knowledge Base (KB), công cụ và tệp đính kèm. KB là nơi giữ nội dung có thể truy hồi; Agent giữ cấu hình để quyết định **có dùng nguồn nào**, gọi công cụ nào và trả lời theo hướng dẫn nào. Vì vậy sửa quy trình nghiệp vụ phải bắt đầu từ Markdown nguồn/KB, không phải sửa câu trả lời tạm thời của Agent.

```text
Human → Agent nhận lượt chat → phân loại Intent
      ├─ nhánh trả lời trực tiếp (ví dụ lời chào)
      └─ nhánh suy luận: prompt → tools → KB/file → rerank → model tổng hợp
                                                        ↓
                              câu trả lời + nguồn + feedback + Request Information
```

Trong gói Knowledge VNG, Agent nghiệp vụ dùng **Knowledge VNG AI** làm corpus: Markdown chứa SOP và URI ảnh MinIO. **Knowledge VNG - Image Assets** chỉ là host 49 PNG; không chọn nó làm KB hỏi đáp phổ thông. Một ảnh render trong câu trả lời vẫn được truy hồi từ Markdown consumer rồi theo URI tới asset host.

![Trang danh sách và nút Tạo trợ lý](<knowledge/GS9 Knowledge VNG AI/image-26-agent-tong-quan-danh-sach.png>)

*Ảnh 13.1 – Danh sách Agent, bộ lọc phạm vi và điểm bắt đầu tạo Agent.*

### Bảng control

| Lớp | Chủ sở hữu vận hành | Control phải kiểm tra | Sai ở lớp này thường biểu hiện |
|---|---|---|---|
| Nội dung | Owner KB | Markdown, phiên bản, nguồn và ảnh MinIO | Nguồn sai hoặc thiếu bằng chứng |
| Truy hồi | Owner Agent | KB, loại file, `@`, tool, threshold, reranker | Không có nguồn hoặc nguồn nhiễu |
| Hành vi | Owner Agent | preset, System Prompt, Intent, model | Có nguồn đúng nhưng tổng hợp sai |
| Giao tiếp | Human/owner | chat mới, lịch sử, feedback, Request Information | Không tái hiện được lỗi |
| Quyền và vòng đời | Owner/Space admin | bật/tắt, chia sẻ, audit, rollback | Người không đúng quyền thấy hoặc sửa Agent |

| Thuật ngữ UI | Ý nghĩa vận hành |
|---|---|
| **Trợ lý/Agent** | Cấu hình chat có thể dùng lại, không phải bản gốc tri thức |
| **Intent** | Lớp phân loại lượt chat để chọn prompt ghi đè và hành vi truy hồi |
| **Nguồn** | File/chunk được UI hiển thị làm căn cứ; phải mở kiểm chứng khi đánh giá |
| **Request Information** | Hộp UI cho ID, method, URL và thời điểm request; dùng đối chiếu hỗ trợ, không chứa credential |
| **Preset** | Cấu hình khởi đầu, không phải một bảo đảm chất lượng |

### SOP

1. Xác định use case, Human, dữ liệu được phép dùng và tiêu chí câu trả lời đạt.
2. Chọn hoặc tạo Agent thử nghiệm; không cấu hình thử trực tiếp trên Agent mặc định.
3. Chọn **Knowledge VNG AI** hoặc KB có chủ đích; không nạp PNG độc lập vào consumer.
4. Thiết lập prompt, model, công cụ và retrieval; lưu baseline bằng ảnh/audit trước A/B.
5. Chạy ít nhất một câu đúng, một câu mâu thuẫn, một no-hit, một follow-up và một attachment phù hợp.
6. Mở source drawer và Request Information, phân loại lỗi theo lớp trước khi sửa.
7. Chỉ phát hành/chia sẻ sau khi test hồi quy; giữ bản sao cấu hình và đường rollback.

### Data flow

```text
Agent config
  → phân loại Intent
  → prompt chính hoặc prompt Intent ghi đè
  → lựa chọn KB/file + tool
  → semantic/keyword/wiki/data retrieval
  → ngưỡng + Top K + reranker
  → context cho LLM → trả lời, source chips, feedback
```

Điểm quan trọng: Intent không tự chứng minh một lượt chat sẽ hoặc sẽ không gọi KB. Nó là lớp định tuyến; kết quả thực tế còn phụ thuộc System Prompt, tool đã bật, KB/file được chọn, model và quota.

### Ma trận kiểm thử

| Tình huống | Câu/đầu vào mẫu | Kỳ vọng | Chỉ dấu pass |
|---|---|---|---|
| Greeting | “Xin chào, bạn giúp gì?” | Phản hồi trực tiếp, phù hợp | Không bịa nguồn |
| RAG chuẩn | ORCHID-731 owner/SLA | Nêu Nhóm Cam, 4 giờ và nguồn | Source chip canonical/PDF/CSV |
| Xung đột | Hỏi cùng mã có near-duplicate | Nêu Nhóm Lam/9 giờ là mâu thuẫn | Không âm thầm chọn một giá trị |
| No-hit | Chính sách nghỉ phép 2031 | Nói không có trong KB | Không tạo chính sách tưởng tượng |
| File đính kèm | PDF ORCHID tổng hợp | Phân tích mã/owner/SLA | Kết quả khớp attachment |

### Bằng chứng

- **Đã kiểm chứng:** trang Agent có danh sách, tìm kiếm, phạm vi và nút Tạo trợ lý; create dialog có sáu tab.
- **Đã kiểm chứng:** Agent test dùng đồng thời KB TEST và Knowledge VNG AI đã trả về canonical ORCHID-731, chỉ ra tài liệu near-duplicate mâu thuẫn và có nguồn.
- **Đã kiểm chứng:** no-hit “chính sách nghỉ phép năm 2031” kết luận không có thông tin sau semantic và keyword search.
- **Có điều kiện:** tenant/model/quyền có thể thay đổi danh sách Agent, tool, model và tốc độ.

Chi tiết truy vết nằm tại [audit Agent chuyên sâu 11/08](audit/agent-deep-test-2026-08-11.md).

### Lỗi và giới hạn

- Không biến Agent thành kho lưu bản gốc hoặc kênh thay Markdown nguồn.
- Khi model bị quota/429, không suy luận KB hỏng: phân biệt lỗi model với lỗi retrieval.
- Không lấy source chip là bằng chứng đủ nếu chưa mở đúng file/chunk và so với câu trả lời.
- Không dùng asset host làm corpus thường xuyên; ảnh phải đi theo Markdown consumer.

### Checklist

- [ ] Use case, KB phạm vi và owner được nêu rõ.
- [ ] Agent test tách biệt Agent mặc định/production.
- [ ] Có câu đúng, mâu thuẫn, no-hit và attachment phù hợp.
- [ ] Có source drawer và Request Information cho một lượt quan trọng.
- [ ] Kết luận được gắn **Đã kiểm chứng**, **Có điều kiện** hoặc **Bị chặn/Chưa xác định**.
<!-- /MODULE -->

<!-- MODULE:doc-14-che-do-preset-prompt-va-intent.md -->
## 14 - Agent: chế độ, preset, prompt và Intent {#14-che-do-preset-prompt-va-intent}

### Khái niệm

Tab **Thông tin cơ bản** quyết định Agent được nhận diện thế nào và lựa chọn khởi đầu nào được áp dụng. UI đã quan sát có hai chế độ chạy:

- **Suy luận thông minh**: mô tả là suy nghĩ nhiều bước/phân tích sâu; hiển thị control **Loại trợ lý** (preset).
- **Trả lời nhanh**: mô tả là phản hồi trực tiếp; trong lượt quan sát control preset không còn hiển thị.

Năm preset dưới Suy luận thông minh là **Hỏi đáp RAG**, **Hỏi đáp Wiki**, **Kết hợp RAG + Wiki**, **Phân tích dữ liệu** và **Tùy chỉnh**. Preset điền System Prompt, gợi ý tool và phạm vi KB; nó là baseline để kiểm tra, không thay thế kiểm thử sau khi lưu.

![Chế độ chạy và preset Hỏi đáp RAG](<knowledge/GS9 Knowledge VNG AI/image-35-agent-che-do-va-preset.png>)

*Ảnh 14.1 – Hai mode, preset và sáu tab của hộp Tạo trợ lý.*

### Bảng control

| Control | Mục đích | Thiết lập khởi đầu an toàn | Cần xác minh sau lưu |
|---|---|---|---|
| Tên/mô tả/icon | Nhận diện và tìm Agent | Tên nêu use case + owner | Không trùng Agent đang vận hành |
| Chế độ | Kiểu điều phối | Smart cho RAG/tool nhiều bước | Thời gian và trace phù hợp |
| Preset | Seed prompt/tool | RAG hoặc Tùy chỉnh cho Knowledge VNG | Không có tool thừa/thiếu |
| System Prompt | Luật chung của mọi lượt | Chỉ dùng nguồn, nêu nguồn, no-hit không bịa | Câu đúng/no-hit tuân thủ |
| Prompt Intent | Luật riêng cho một loại lượt | Để trống để dùng template nếu chưa test | Không phá luật chung |

![System Prompt và biến UI gợi ý](<knowledge/GS9 Knowledge VNG AI/image-36-agent-system-prompt-va-bien.png>)

*Ảnh 14.2 – System Prompt quan sát được và các biến chỉ nên dùng đúng cú pháp UI.*

System Prompt Smart Reasoning quan sát biến `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`. Prompt theo Intent gợi ý `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`. Chỉ vì một biến được gợi ý không có nghĩa nó có dữ liệu hữu ích trong mọi tình huống; phải kiểm tra qua chat và source trace.

![Intent và prompt theo Intent trong một cấu hình đã mở](<knowledge/GS9 Knowledge VNG AI/image-37-agent-intent-va-prompt-ghi-de.png>)

*Ảnh 14.3 – Prompt theo Intent là lớp ghi đè theo lượt; dùng template hoặc để trống khi chưa có case hồi quy.*

### SOP

1. Chọn mode theo độ phức tạp, sau đó chọn preset gần use case nhất.
2. Viết prompt chính theo năm phần: vai trò; dữ liệu được phép; quy tắc nguồn; no-hit/mâu thuẫn; định dạng câu trả lời.
3. Không nhét secret, token, dữ liệu HR nhạy cảm hoặc instruction trái chính sách vào prompt.
4. Chỉ thêm prompt Intent khi đã có một hành vi cần khác biệt rõ và một test case tái lập.
5. Mỗi lần sửa prompt, chạy cùng bộ câu cơ sở rồi lưu câu/nguồn trước–sau.

### Data flow

```text
Human message → classifier nhận Intent
  → System Prompt (luật chung)
  → nếu có: Prompt của Intent ghi đè/bổ sung cho lượt đó
  → tools + KB/file scope → model tổng hợp
```

`Intent` là **nhãn mục đích của một lượt chat**, không phải KB, tool hay model. Nó quyết định chọn prompt theo Intent và hướng điều phối; hành vi retrieval chỉ có thể được kết luận sau khi quan sát trace.

![Danh sách Intent và vùng prompt ghi đè](<knowledge/GS9 Knowledge VNG AI/image-27-agent-thong-tin-co-ban-va-intent.png>)

*Ảnh 14.4 – Tab cơ bản chứa prompt chính, dropdown Intent và prompt chuyên biệt.*

| Intent UI | Công dụng kỳ vọng | Bằng chứng/giới hạn 11/08/2026 |
|---|---|---|
| Greeting Response | Chào hỏi | **Đã kiểm chứng:** phản hồi trực tiếp, không source chip |
| Chitchat Response | Hội thoại xã giao | Có trên UI; cần test riêng theo prompt tenant |
| Follow-up Response | Hỏi tiếp trong session | Có trên UI; test phải giữ session và source trước đó |
| Image Analysis Response | Đọc ảnh | Có trên UI; attachment ảnh bị từ chối ở test hiện tại |
| Summarize Response | Tóm tắt | Có trên UI; file/nguồn quyết định context thật |
| Document Analysis Response | Phân tích tệp | **Đã kiểm chứng** với PDF ORCHID attachment |

![Trace greeting thực tế](<knowledge/GS9 Knowledge VNG AI/image-38-agent-intent-trace-runtime.png>)

*Ảnh 14.5 – Greeting runtime trả lời trực tiếp; UI không hiển thị nhãn classifier nên đây là quan sát hành vi, không phải bằng chứng nội bộ về thuật toán.*

### Ma trận kiểm thử

| Biến đổi một lần | Input | Kỳ vọng quan sát |
|---|---|---|
| Smart ↔ Quick | cùng câu RAG | Trace/tool/độ sâu có thể khác; không tự suy chất lượng hơn |
| RAG preset ↔ Custom | ORCHID-731 | Kiểm tra tool, nguồn và no-hit thay vì chỉ nhìn câu văn |
| Prompt chính | no-hit 2031 | Nhận thiếu dữ liệu, không tạo chính sách |
| Greeting intent | lời chào | Phản hồi lịch sự, không truy hồi vô ích |
| Document intent | PDF attachment | Nhận tệp và trích đúng mã/owner/SLA |
| Intent prompt ghi đè | yêu cầu định dạng | Chỉ thay hành vi nhánh, không xóa quy tắc an toàn |

### Bằng chứng

- **Đã kiểm chứng:** UI có hai mode, năm preset và sáu Intent đúng tên trong bảng.
- **Đã kiểm chứng:** greeting được trả lời trực tiếp trong test Agent chuyên sâu.
- **Đã kiểm chứng:** System Prompt/Intent Prompt có các biến nêu trên trong UI.
- **Có điều kiện:** UI không phơi bày nhãn classifier trong trace; không khẳng định certainty hay thuật toán phân loại nội bộ.

### Quy tắc viết prompt vận hành

Một prompt production nên tách rõ **luật bất biến** và **hướng dẫn format**. Luật bất biến: chỉ dùng phạm vi nguồn được phép, trích nguồn khi đã retrieval, nêu thiếu dữ liệu/no-hit, nêu mâu thuẫn thay vì suy chọn. Hướng dẫn format: ngôn ngữ, độ dài, bảng hay bullet và câu hỏi làm rõ. Khi hai điều trái nhau, ưu tiên luật an toàn/nguồn; không dùng Intent prompt để vô hiệu hóa luật chung.

| Anti-pattern | Vì sao không ổn | Thay bằng |
|---|---|---|
| “Luôn trả lời tự tin” | Khuyến khích bịa khi no-hit | “Nếu không có nguồn phù hợp, nêu giới hạn và đề nghị thông tin cần thêm” |
| “Chỉ dùng KB” nhưng không nói nguồn | Human không kiểm chứng được | “Nêu tên nguồn/chunk cho claim quan trọng” |
| Prompt Intent sao chép toàn bộ System Prompt | Drift và khó A/B | Chỉ ghi phần khác biệt của intent |
| Cấm tool mơ hồ | Model không biết dừng ở đâu | Nêu tool được phép, tiêu chí gọi và tiêu chí dừng |

### Lỗi và giới hạn

- Preset có thể tạo cấu hình thiếu tool; Agent test ban đầu không tạo được cho tới khi bật ít nhất một tool. Kiểm tra validation trước khi kết luận preset hoàn chỉnh.
- Prompt càng dài không đồng nghĩa retrieval tốt hơn; luật xung đột hoặc ưu tiên nguồn phải ngắn, kiểm thử được.
- Không đặt “luôn trả lời” cùng với “chỉ trả lời khi có nguồn” nếu không mô tả nhánh no-hit.
- Lỗi `[[chunk#...]]` là lỗi tổng hợp/trình bày cần chẩn đoán prompt/model/context, không tự động sửa file nguồn.

### Checklist

- [ ] Mode và preset được ghi vào audit baseline.
- [ ] Prompt có luật nguồn, no-hit, xung đột và định dạng.
- [ ] Tất cả biến placeholder đúng cú pháp UI, không có secret.
- [ ] Sáu Intent được phân biệt bằng case, không chỉ tên.
- [ ] Mỗi prompt thay đổi có câu hồi quy và source trace.
<!-- /MODULE -->

<!-- MODULE:doc-15-model-reranker-suy-luan-va-quota.md -->
## 15 - Agent: model, reranker, suy luận và quota {#15-model-reranker-suy-luan-va-quota}

### Khái niệm

Model chat tổng hợp answer và có thể điều phối tool; reranker chấm lại độ liên quan của ứng viên retrieval trước khi context đi vào model. Hai lớp này khác nhau: đổi LLM không sửa embedding/chunk gốc; tắt reranker không thay nội dung KB. Trong UI 11/08/2026, bốn model thấy được là `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b` và `qwen3.6-plus`; reranker thấy được là `bge-reranker-v2-m3`.

![Cấu hình model, reranker, temperature và reasoning](<knowledge/GS9 Knowledge VNG AI/image-28-agent-cau-hinh-mo-hinh.png>)

*Ảnh 15.1 – Tab cấu hình model; danh sách là snapshot UI, không cam kết quota còn hiệu lực.*

### Bảng control

| Control | Tác động | Baseline test | Dấu hiệu cần điều tra |
|---|---|---|---|
| Chat model | Suy luận, tool calling, văn phong | `hosted_vllm/qwen3.6-35b` có phản hồi ở test | 429, timeout, tool loop hoặc answer không tổng hợp |
| Reranker | Chọn/xếp lại candidate | `bge-reranker-v2-m3` nếu tenant khả dụng | Nguồn đúng bị tụt hoặc nguồn nhiễu còn lại |
| Temperature | Độ biến thiên đầu ra | A/B một biến, ví dụ 0,2 ↔ 0,7 | Tính lặp và bám định dạng giảm |
| Reasoning | Quyền suy nghĩ mở rộng khi model hỗ trợ | Chỉ bật khi use case cần | Token/độ trễ tăng nhưng answer không tốt hơn |
| Max loops | Số vòng tool tối đa | 10 trong Agent test | Loop dài, không tiến gần bằng chứng |
| Timeout LLM | Chặn một call quá lâu | 120 giây trong Agent test | Hết thời gian trước câu trả lời |
| Tool song song | Có thể gọi nhiều tool đồng thời | A/B, khôi phục baseline | Thứ tự/nguồn khác hoặc lỗi đồng thời |

![A/B model trong composer và menu model](<knowledge/GS9 Knowledge VNG AI/image-39-agent-model-ab-va-request-info.png>)

*Ảnh 15.2 – Model có thể đổi cho chat; test phải ghi model thật ở lượt đó.*

### SOP

1. Chọn một query canonical, một conflict và một no-hit; cố định KB/tool/retrieval.
2. Chạy ba lần cùng model nếu quota cho phép; lưu answer, nguồn, số bước và lỗi.
3. Đổi **một** model hoặc **một** control mỗi lần; không đồng thời đổi prompt/reranker/threshold.
4. Dừng ngay model nhận `429`/quota hoặc lỗi xác thực; ghi **Bị chặn**, không retry vô hạn.
5. Sau A/B, phục hồi model, temperature, timeout, parallel và tool baseline trước test khác.

### Data flow

```text
retrieval candidates → filters/threshold → reranker (nếu bật)
                         → Top K context → chat model/reasoning
                         → tool calls đến max loops/timeout → answer
```

Không suy luận model nào “thông minh hơn” chỉ từ một câu, đặc biệt khi candidate/context khác, quota khác hoặc Agent chạy tools khác nhau.

### Ma trận kiểm thử

| Trục | Case | Điều ghi nhận |
|---|---|---|
| 4 model | ORCHID canonical + no-hit | Có/không trả lời, nguồn, latency, lỗi quota |
| Temperature | 0,2 và 0,7 với cùng query | Độ bám format, không dùng để đo facts đơn lẻ |
| Reranker | tắt/bật khi có canonical + near duplicate | Thứ tự nguồn, có bỏ sót mâu thuẫn không |
| Reasoning | tắt/bật nếu UI/model hỗ trợ | Số bước, tool và answer cuối |
| Timeout | baseline và giá trị thử | Có abort/timeout rõ ràng; sau đó khôi phục |
| Parallel | tắt/bật cùng tools | Độ trễ, nguồn và lỗi đồng thời |

### Bằng chứng

- **Đã kiểm chứng:** `hosted_vllm/qwen3.6-35b` trả lời canonical/no-hit trong test chuyên sâu; `deepseek-v4-flash` cũng trả lời canonical ở chat độc lập.
- **Đã kiểm chứng:** UI trình bày bốn model và reranker nêu trên; Agent test dùng max loops 10 và timeout 120 giây.
- **Có điều kiện:** không đủ quota/quyền để kết luận cả bốn model đều chạy ba lượt hoặc có chất lượng tương đương.

![Timeout/cảnh báo runtime là tín hiệu vận hành](<knowledge/GS9 Knowledge VNG AI/image-40-agent-quota-timeout-va-loi-runtime.png>)

*Ảnh 15.3 – Timeout/lỗi runtime cần được ghi như tín hiệu điều tra, không bị gán nhầm cho KB.*

### Diễn giải kết quả A/B

Lưu mỗi lần chạy thành một hàng audit thay vì một nhận xét chung. Cột tối thiểu: thời điểm, Agent/version config, model, reranker, temperature, reasoning, tool set, KB/file scope, query cố định, số bước, thời gian, answer, source và lỗi. Với câu có nhiều nguồn, chấm ba điểm riêng: **retrieval** có đưa canonical và near-duplicate vào không; **grounding** có chỉ đúng nguồn không; **synthesis** có nêu đúng Nhóm Cam/4 giờ và cảnh báo Nhóm Lam/9 giờ không.

| Kết quả | Không được kết luận | Bước kế tiếp |
|---|---|---|
| Model A nhanh hơn Model B một lượt | A luôn tốt hơn | Lặp query/corpus giống nhau nếu quota cho phép |
| A có answer nhưng B 429 | A chính xác hơn | Ghi khác biệt khả dụng/quota; không chấm chất lượng |
| Cả hai có source nhưng một answer sai | KB hỏng | So context, prompt, model output trước |
| Không source ở cả hai | Model yếu | So scope/tools/threshold trước model |

### Baseline hiệu năng có trách nhiệm

Không đặt SLA chat từ một lượt ở môi trường test. Để lập baseline, chạy cùng query ít nhất ba lần khi quota cho phép, loại kết quả bị lỗi hạ tầng khỏi median nhưng vẫn ghi lỗi, và tách thời gian chờ ingestion khỏi thời gian Agent suy luận. Chỉ so sánh latency khi model, KB version, tool set, retrieval parameter, attachment và quota tương đương. Nếu một model chuyển sang unavailable/429 giữa chu kỳ, chu kỳ đó là **Bị chặn**, không được lấp bằng số liệu của model khác.

Quy tắc chọn model cho production: ưu tiên model đang pass bộ regression trong chính tenant hơn model “có tên” trong dropdown; giữ fallback được phê duyệt; ghi ngày và lỗi quota; và tránh đổi model trong lúc xử lý một incident trừ khi có lý do rõ. Reranker cũng cần được coi là dependency: khi nó mất khả dụng, test retrieval lại trước khi coi answer cũ còn tương đương.

Không chuyển một model mới thành default chỉ từ demo: cần owner phê duyệt, baseline trước/sau, rollback path và xác nhận quota thực tế.
Ghi rõ model fallback trong runbook để người trực ca không phải đoán khi quota thay đổi.

### Lỗi và giới hạn

| Triệu chứng | Chẩn đoán trước | Hành động đúng |
|---|---|---|
| `429 insufficient_quota` | Khả dụng model/quota | Dừng model, đổi model được phép, ghi blocker |
| Answer không có nguồn | Tool/KB/scope/retrieval trước model | Không đổi LLM như bước đầu tiên |
| Source đúng nhưng câu sai | Prompt, context, temperature, model | Kiểm tra source và thử A/B cô lập |
| Tool quay vòng | Loops, prompt, tool set | Giảm tools/loops và buộc tiêu chí dừng |
| Timeout | Tool chain, model, parallel | Giữ trace, tăng timeout có lý do rồi hồi quy |

Không lưu request headers, token, service-account JSON hoặc internal diagnostic raw vào tài liệu/audit.

### Checklist

- [ ] Ghi model/reranker/temperature/reasoning/timeout/parallel cho mỗi test.
- [ ] Có canonical, conflict, no-hit cùng điều kiện.
- [ ] Dừng khi quota/429 và phân loại Bị chặn.
- [ ] A/B chỉ đổi một biến và khôi phục baseline.
- [ ] Không kết luận chất lượng model nếu retrieval hoặc quota không tương đương.
<!-- /MODULE -->

<!-- MODULE:doc-16-kho-tri-thuc-cong-cu-va-truy-hoi.md -->
## 16 - Agent: kho tri thức, công cụ và truy hồi {#16-kho-tri-thuc-cong-cu-va-truy-hoi}

### Khái niệm

Tab **Kho tri thức** xác định corpus mà Agent được phép tìm. UI có ba phạm vi: tất cả KB được phép, KB đã chọn và không dùng KB. Với Agent Knowledge VNG, chọn rõ **Knowledge VNG AI**; asset host chỉ giữ PNG để Markdown tham chiếu. UI cho lọc theo loại tệp như `MD`, `PDF`, `CSV`, `DOCX`, `TXT`, `XLSX`, `XLS`, `JSON`, `PPTX`, `HTML`, `MSG`, `EML` (danh sách tenant có thể đổi).

![Phạm vi KB và lọc loại tệp](<knowledge/GS9 Knowledge VNG AI/image-29-agent-kho-tri-thuc.png>)

*Ảnh 16.1 – Chọn KB là control bảo mật và chất lượng, không chỉ là tiện lợi.*

`Chỉ truy hồi khi được nhắc` thay đổi thời điểm Agent được phép dùng KB. Khi bật, Human chọn KB hoặc tệp qua **Nhắc tri thức / tệp** (`@`) trong composer; không có `@` thì không nên kỳ vọng RAG tự chạy. Khi tắt, Agent có thể tự gọi retrieval trong phạm vi cấu hình.

### Bảng control

| Nhóm | UI/giá trị quan sát | Vai trò | Rủi ro khi cấu hình sai |
|---|---|---|---|
| KB scope | All / Selected / None | Biên dữ liệu Agent thấy | Leaky scope hoặc không có nguồn |
| File types | MD/PDF/CSV… | Thu hẹp corpus theo use case | Bỏ sót file đúng hoặc kéo nhiễu |
| `@` | KB/tệp trong composer | Scope theo từng lượt | Human tưởng đã truy hồi nhưng chưa chọn chip |
| Semantic search | Tìm theo ngữ nghĩa | Recall cho câu diễn đạt lại | Gần nghĩa nhưng sai chủ đề |
| Keyword search | Tìm theo từ khóa | Mã, tên, thuật ngữ | Bỏ sót biến thể/đồng nghĩa |
| List chunks / Document info | Duyệt/đọc metadata | Debug candidate và nguồn | Tool thừa làm loop dài |
| Wiki/data tools | Wiki, SQL, Data Analysis, Schema | Chỉ cho KB/file tương thích | Kết luận sai vì tool không có dữ liệu |

![Công cụ, loops, timeout và parallel](<knowledge/GS9 Knowledge VNG AI/image-30-agent-cong-cu.png>)

*Ảnh 16.2 – Tool set hiệu lực phải được kiểm tra sau preset.*

![Chiến lược truy hồi: Top K, ngưỡng và reranker](<knowledge/GS9 Knowledge VNG AI/image-31-agent-chien-luoc-truy-hoi.png>)

*Ảnh 16.3 – Retrieval strategy là lớp lọc candidate trước context; chỉ thay một tham số trong mỗi lần A/B.*

### SOP

1. Bắt đầu bằng **Selected KB** và loại file tối thiểu; nới rộng chỉ khi testcase chứng minh cần.
2. Bật semantic + keyword cho tài liệu hỗn hợp; giữ List chunks/Document info cho trace kỹ thuật.
3. Chỉ bật Wiki tools khi KB đã có Wiki phù hợp; chỉ bật data tools khi CSV/XLSX/table tương thích.
4. Chọn một canonical, một near duplicate, một tên/mã exact và một no-hit để đánh giá.
5. Khi nguồn sai: kiểm tra scope → `@`/chip → file type → tool → threshold/Top K → reranker; đừng sửa prompt trước.

### Data flow

```text
KB scope + file filter + @ per-turn
     → tools: semantic / keyword / chunks / document info / wiki / data
     → candidate set
     → vector/keyword thresholds + Top K
     → reranker (nếu bật) → context → answer + source chips
```

![Hai KB trong Agent test](<knowledge/GS9 Knowledge VNG AI/image-41-agent-test-kb-da-nguon.png>)

*Ảnh 16.4 – Agent test được giới hạn vào KB TEST tổng hợp và Knowledge VNG AI để quan sát xung đột có kiểm soát.*

### Ma trận kiểm thử

| Case | Thay đổi duy nhất | Kỳ vọng |
|---|---|---|
| Scope | Selected KB TEST ↔ Selected TEST + consumer ↔ None | Source chỉ xuất hiện trong scope cho phép |
| Type filter | MD ↔ PDF ↔ CSV | File đúng được/không được candidate theo filter |
| `@` | bật/tắt “chỉ khi được nhắc” | Không `@` không tự retrieval khi công tắc bật |
| Tool | semantic ↔ keyword ↔ cả hai | Mã ORCHID exact và diễn đạt lại đều có đường tìm |
| Top K | 3 ↔ 10 | Conflict còn bị phát hiện hay bị cắt mất |
| Vector threshold | 0,3 ↔ 0,7 | Recall/nhiễu thay đổi, không đánh giá chỉ bằng câu văn |
| Reranker | tắt ↔ bật | Thứ tự/candidate cuối và nguồn phải được ghi |

![Nhắc KB hoặc tệp bằng @](<knowledge/GS9 Knowledge VNG AI/image-42-agent-at-kho-tri-thuc-va-tep.png>)

*Ảnh 16.5 – Dialog hiển thị cả KB và từng tệp có thể nhắc trong composer.*

![Trace tools và source từ bốn file ORCHID](<knowledge/GS9 Knowledge VNG AI/image-43-agent-trace-cong-cu-truy-hoi.png>)

*Ảnh 16.6 – Runtime dùng keyword/semantic rồi hiển thị các file canonical, near-duplicate, CSV và PDF.*

![A/B Top K, threshold và rerank](<knowledge/GS9 Knowledge VNG AI/image-44-agent-ab-topk-threshold-rerank.png>)

*Ảnh 16.7 – Các control phải được A/B một biến và khôi phục baseline, không chỉnh đồng thời.*

### Bằng chứng

- **Đã kiểm chứng:** Agent test có thể chọn đồng thời KB TEST và Knowledge VNG AI; dialog `@` liệt kê 2 KB cùng 5 fixture và 14 Markdown consumer tại thời điểm test.
- **Đã kiểm chứng:** query ORCHID dùng keyword + semantic, tìm 8 matches/5 kết quả từ 4 tệp và nêu xung đột Nhóm Cam/4 giờ với Nhóm Lam/9 giờ.
- **Đã kiểm chứng:** no-hit sau semantic/keyword không bịa chính sách.
- **Có điều kiện:** Wiki/Data/Schema tools chỉ được quan sát trong catalog/cấu hình; kết quả end-to-end phụ thuộc Wiki hoặc data source tương thích.

### Quy tắc ưu tiên và xung đột nguồn

Retrieval không tự biết tài liệu nào là authoritative. Với data đa nguồn, tài liệu canonical phải mang nhãn/metadata rõ trong chính nội dung; prompt cần yêu cầu Agent hiển thị mâu thuẫn và không “bỏ phiếu” bằng số lượng chunk. Trong fixture ORCHID, canonical MD, PDF và record CSV đầu khớp Nhóm Cam/4 giờ; near-duplicate và record CSV thứ hai cố ý ghi Nhóm Lam/9 giờ. Test pass khi Agent đưa cả hai phía, nêu nguồn chuẩn/nhãn conflict và giải thích căn cứ chọn giá trị chuẩn.

| Trạng thái nguồn | Hành vi mong muốn |
|---|---|
| Một nguồn canonical rõ, không xung đột | Trả lời và trích nguồn |
| Canonical + near duplicate có nhãn | Trả lời canonical, cảnh báo mâu thuẫn |
| Hai nguồn đồng cấp mâu thuẫn | Không tự quyết; hỏi Human/owner hoặc báo không xác định |
| Source không có claim cần hỏi | No-hit có căn cứ, không nội suy |

### Baseline retrieval cho Knowledge VNG AI

Khởi đầu thực dụng là: scope **Selected** = `Knowledge VNG AI`; loại `MD`; `@` tắt nếu Agent phải tự RAG; semantic và keyword đều bật; reranker bật khi tenant khả dụng. Sau đó chọn một query từ mỗi module quan trọng, một query diễn đạt lại và một query cố ý không có trong sổ tay. Nếu source bị nhiễu, giảm scope/lọc file trước; nếu source quá ít, hạ threshold hoặc tăng Top K từng bước và ghi lại ảnh hưởng đến no-hit.

### Lỗi và giới hạn

- `[[chunk#...]]` lộ ra là bằng chứng context tới model, nhưng không phải câu trả lời đạt; giữ trace và chẩn đoán model/prompt.
- Nhiều nguồn không tự cho biết nguồn nào là canonical: đặt nhãn nguồn, prompt quy tắc xung đột và test near duplicate.
- `@` là lựa chọn scope, không phải quyền vượt qua access control.
- Top K/threshold không có giá trị “đúng cho mọi KB”; thay một biến và giữ corpus/query cố định.

### Checklist

- [ ] Scope Selected KB được ghi rõ, không gồm asset host.
- [ ] Lọc loại file khớp use case, có test PDF/CSV nếu bật.
- [ ] Tool catalog tối thiểu và các tool điều kiện được gắn nhãn.
- [ ] Có test `@`, canonical, conflict, exact identifier và no-hit.
- [ ] Có source trace trước khi đổi prompt/model.
<!-- /MODULE -->

<!-- MODULE:doc-17-da-phuong-thuc-va-tep-dinh-kem.md -->
## 17 - Agent: đa phương thức và tệp đính kèm {#17-da-phuong-thuc-va-tep-dinh-kem}

### Khái niệm

Agent có hai đường xử lý khác nhau cần tách biệt khi kiểm thử:

1. **Tài liệu trong KB**: file đã upload, parser/index hoàn tất, được tools truy hồi như corpus.
2. **Tệp đính kèm trong chat**: file đi cùng đúng một request Human; model/Intent xử lý tệp đó trong phiên chat.

Không suy luận PDF trong KB parse được thì PDF attachment chắc chắn hoạt động, hoặc composer nhận ảnh thì VLM đã nhận bytes. MD, PDF và CSV fixture ORCHID đều được KB TEST xử lý hoàn tất; PDF attachment cũng được Agent đọc đúng. Nhánh image/ASR vẫn có điều kiện tenant/model.

![Tab cấu hình đa phương thức](<knowledge/GS9 Knowledge VNG AI/image-32-agent-cau-hinh-da-phuong-thuc.png>)

*Ảnh 17.1 – Control tải ảnh, VLM và audio/ASR cần cấu hình riêng với retrieval tài liệu.*

### Bảng control

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

### SOP

1. Xác định file dùng làm corpus lâu dài hay attachment một lượt; không thay thế nhau.
2. Với KB, chờ status **Hoàn tất** rồi test parser/source; không chat ngay khi còn chờ xử lý.
3. Với attachment, dùng một PDF/CSV/MD tổng hợp không nhạy cảm, hỏi những fact biết trước.
4. Với ảnh, chọn file an toàn, kiểm tra UI nhận tệp, model VLM/Intent và response; lưu lỗi client/server tách biệt.
5. Với audio, nếu dropdown ASR báo không có model thì dừng, ghi blocker; không cố đưa credential/model riêng vào workspace.
6. Xóa attachment/chat test nếu chính sách retention yêu cầu; fixture tổng hợp và audit không chứa thông tin thật.

### Data flow

```text
KB file:      file → parser/chunk/index → retrieval tools → context → answer
Attachment:   Human file → upload validation → request/session → Intent/VLM/ASR or document reader
                                                   → model → answer
```

Hai path gặp nhau ở model nhưng có validation, quyền, model và timing khác nhau. Chẩn đoán đúng phải hỏi “file có tới request chưa?” trước “model đọc đúng chưa?”.

![PDF nằm trong composer trước khi gửi](<knowledge/GS9 Knowledge VNG AI/image-45-agent-tep-dinh-kem.png>)

*Ảnh 17.2 – Composer xác nhận PDF đã được đính kèm và hiển thị kích thước trước khi gửi.*

### Ma trận kiểm thử

| Tình huống | Input | Câu hỏi/kiểm tra | Pass condition |
|---|---|---|---|
| MD corpus | `TEST-orchid-canonical.md` | owner/SLA | Nguồn canonical + Nhóm Cam/4 giờ |
| PDF corpus | `TEST-orchid-attachment.pdf` trong KB | owner/SLA | Có thể truy hồi cùng dữ liệu chuẩn |
| CSV corpus | `TEST-orchid-data.csv` | so sánh hai record | Nêu record canonical và conflicting |
| PDF attachment | cùng PDF trong composer | mã/owner/SLA | ORCHID-731, Nhóm Cam, 4 giờ |
| Image attachment | PNG UI an toàn | mô tả nội dung | Ghi client/server error nếu bị chặn |
| Audio attachment | audio chỉ khi có ASR | transcript | Chỉ pass khi ASR/tenant hoạt động |

![Ảnh đính kèm bị từ chối ở client](<knowledge/GS9 Knowledge VNG AI/image-46-agent-image-analysis.png>)

*Ảnh 17.3 – Bằng chứng lỗi “Định dạng tệp không hỗ trợ” với đường test này; không dùng nó để kết luận VLM hỏng.*

![Document Analysis PDF trả về fact mong đợi](<knowledge/GS9 Knowledge VNG AI/image-47-agent-document-summarize.png>)

*Ảnh 17.4 – Agent phân tích attachment PDF và nêu đúng mã, owner, SLA, priority.*

### Bằng chứng

- **Đã kiểm chứng:** KB TEST xử lý 3 MD, CSV và PDF hoàn tất; câu RAG đã dùng 4 tệp ORCHID để đối chiếu.
- **Đã kiểm chứng:** PDF attachment 1,7 KB được composer nhận; `deepseek-v4-flash` trả ORCHID-731, Nhóm Cam, SLA 4 giờ, priority P2.
- **Đã kiểm chứng:** Image upload theo đường test hiện hành cho toast `Định dạng tệp không hỗ trợ`.
- **Bị chặn:** audio/ASR không hoàn tất vì UI báo chưa có model ASR cho tenant.
- **Có điều kiện:** file type được UI liệt kê không bảo đảm parser/VLM/ASR đều khả dụng trên mọi tenant/model.

### Quy tắc dữ liệu và riêng tư attachment

Attachment đi qua session chat nên không nên dùng để kiểm thử với hợp đồng, thông tin cá nhân, credential, key, log nội bộ hoặc file có retention chưa rõ. Tạo fixture synthetic có oracle rõ (mã, owner, SLA) và kiểm tra: filename/size xuất hiện ở composer; query nêu đúng attachment; answer không chỉ lặp dữ liệu từ KB khác. Nếu attachment có nội dung nhạy cảm hợp lệ trong vận hành, áp dụng chính sách dữ liệu của tổ chức và xác nhận nơi lưu/retention trước khi upload.

| Câu hỏi trước upload | Lý do |
|---|---|
| Đây là corpus lâu dài hay context một lượt? | Chọn đường KB hoặc attachment |
| Có PII/secret/credential không? | Ngăn rò rỉ qua chat/audit |
| Có fact oracle để chấm không? | Phân biệt parse lỗi với model tổng hợp lỗi |
| Model/tenant có VLM hoặc ASR không? | Tránh kết luận sai từ control rỗng |

### Tóm tắt và phân tích tài liệu

Hai Intent **Summarize Response** và **Document Analysis Response** không thay thế kiểm chứng nguồn. Tóm tắt tốt phải giữ rõ phạm vi, dữ kiện chưa chắc và mâu thuẫn; phân tích tốt phải chỉ ra file/đoạn đang nói tới. Khi Human đính kèm PDF, yêu cầu model trả mã/owner/SLA là case oracle; khi Human chỉ yêu cầu “tóm tắt”, thêm constraint về số bullet, ngôn ngữ và việc không thêm fact ngoài file.

### Lỗi và giới hạn

| Hiện tượng | Lớp cần kiểm tra trước | Hành động |
|---|---|---|
| Tệp không hiện composer | Upload validation/client | Ghi định dạng/kích thước/model, không gọi lại private API |
| Tệp hiện nhưng answer nói không thấy | Attachment transmission/Intent | Lưu Request Information và test tệp tổng hợp khác |
| PDF KB có source nhưng attachment fail | Hai đường xử lý khác nhau | Không sửa parser KB vội |
| Không có ASR model | Tenant provisioning | Gắn nhãn Bị chặn và yêu cầu admin qua kênh chuẩn |
| CSV trả lời sai | Data/retrieval/prompt | Kiểm tra record, tool và source before model judgement |

### Checklist

- [ ] Phân biệt corpus KB với attachment per-turn.
- [ ] Tệp test không nhạy cảm, có oracle fact rõ ràng.
- [ ] PDF/CSV/MD được kiểm tra status trước chat.
- [ ] Image/ASR chỉ tuyên bố pass khi có response end-to-end.
- [ ] Audit ghi model, loại file, lỗi/toast và Request Information phù hợp.
<!-- /MODULE -->

<!-- MODULE:doc-18-chat-nguon-lich-su-va-danh-gia.md -->
## 18 - Agent: chat, nguồn, lịch sử và đánh giá {#18-chat-nguon-lich-su-va-danh-gia}

### Khái niệm

Chat là bề mặt Human nhìn thấy, còn source chips, history, feedback và Request Information là bề mặt quan sát để vận hành. Một câu trả lời “nghe hợp lý” chỉ là giả thuyết: phải mở nguồn, kiểm xem chunk/tài liệu có thật sự chứa claim hay không, rồi mới đánh giá Agent/KB. Chat mới tạo một session; follow-up phải được kiểm thử trong cùng history, không giả định Agent nhớ giữa session.

![Câu trả lời RAG, nguồn và ảnh trong Markdown](<knowledge/GS9 Knowledge VNG AI/image-33-agent-chat-nguon-va-anh.png>)

*Ảnh 18.1 – Câu trả lời cần kiểm tra cả source chip và ảnh render, không chỉ phần văn bản.*

### Bảng control

| UI | Mục đích | SOP kiểm chứng |
|---|---|---|
| Cuộc trò chuyện mới | Cô lập testcase/session | Đặt một query, ghi điều kiện cấu hình |
| Lịch sử | Mở lại hội thoại/follow-up | Không dùng history để suy luận persistent memory chưa kiểm chứng |
| Source chip / Xem file | Căn cứ retrieval | Mở đúng file, đối chiếu claim/chunk |
| Hữu ích/Chưa hữu ích | Tín hiệu Human | Gắn feedback vào testcase, không phải phán quyết nguyên nhân |
| Hộp xử lý | Điều tra feedback | Chuyển Mới → Đang xem → Đã xử lý có bằng chứng hồi quy |
| Request Information | Metadata request qua UI | Lưu ngày/method/ID đã che; không trích credential/private payload |

### SOP

1. Mở **Cuộc trò chuyện mới**, ghi Agent, model, KB chips, tools/retrieval baseline.
2. Gửi query; chờ status hoàn tất, không chụp khi UI còn `Đang tải` nếu muốn ghi answer cuối.
3. Mở source từng nguồn quan trọng; xác minh file, tên/chunk và fact.
4. Bấm **Thông tin request** khi cần trao đổi hỗ trợ hoặc tái hiện; che Request/Message/Session ID và URL định danh trước khi phân phối ảnh.
5. Đánh giá Hữu ích/Chưa hữu ích kèm nhận xét ngắn, liên kết test case.
6. Trong Hộp xử lý, phân loại: nguồn, retrieval, prompt, model/quota, attachment hoặc quyền; hồi quy rồi đóng.

### Data flow

```text
session/chat → response + sources
             → Human feedback (useful/not useful + comment)
             → evaluation overview → processing inbox
             → investigate with source + Request Information
             → fix correct layer → regression → resolved
```

Lịch sử giúp tái hiện ngữ cảnh conversation; nó không thay audit cấu hình vì model, quota hoặc Agent setting có thể đổi sau đó.

### Ma trận kiểm thử

| Case | Thao tác | Điều cần chứng minh |
|---|---|---|
| Chat mới | canonical ORCHID | Source canonical/PDF/CSV và answer đúng |
| Follow-up | “Owner là ai?” sau query ORCHID | Có/không dùng context được ghi rõ |
| Conflict | request nêu cảnh báo | Source near-duplicate được lộ, không che mâu thuẫn |
| No-hit | chính sách 2031 | Có kết luận thiếu nguồn, không hallucinate |
| Source drawer | mở file | Claim tồn tại trong nguồn thật |
| Request info | mở UI | Có request metadata, không lưu data nhạy cảm |
| Feedback | useful/not useful | Có đối tượng Hộp xử lý và mô tả nguyên nhân |

![Tổng quan feedback và Hộp xử lý](<knowledge/GS9 Knowledge VNG AI/image-34-agent-danh-gia-cau-tra-loi.png>)

*Ảnh 18.2 – Evaluation cần được vận hành như queue điều tra, không chỉ dashboard tỷ lệ.*

### Bằng chứng

- **Đã kiểm chứng:** canonical RAG hiển thị tool trace, source buttons cho canonical MD, near-duplicate MD, CSV và PDF; answer nêu mâu thuẫn có chủ đích.
- **Đã kiểm chứng:** no-hit kết luận không có information sau semantic/keyword search.
- **Đã kiểm chứng:** response có nút Sao chép, Thêm vào tri thức, Hữu ích, Chưa hữu ích và Thông tin request.
- **Đã kiểm chứng:** Request Information UI hiện Request ID, Message ID, Session ID, method POST, URL và thời gian gửi; ảnh phân phối đã che các định danh.

![Request Information đã che định danh](<knowledge/GS9 Knowledge VNG AI/image-48-agent-lich-su-va-request-information.png>)

*Ảnh 18.3 – Chỉ dùng thông tin UI để định vị request; các giá trị định danh đã được che trước khi nạp asset KB.*

### Kịch bản triage feedback

Khi Human bấm **Chưa hữu ích**, điều tra theo đường ngắn nhất: (1) mở conversation và xác định expectation; (2) mở source chip; (3) phân loại no source/source sai/source đúng answer sai; (4) kiểm tra Agent config snapshot; (5) sửa đúng một lớp; (6) chạy lại query gốc và query diễn đạt lại; (7) ghi hành động rồi mới chuyển **Đã xử lý**. Không đóng feedback chỉ vì response mới nghe trôi chảy.

| Loại feedback | Dấu hiệu | Owner thường xử lý | Bằng chứng đóng ticket |
|---|---|---|---|
| Thiếu nguồn | Không có chip hoặc no-hit sai | Owner Agent/KB | Scope/tool/index đã kiểm tra + source mới đúng |
| Nguồn sai | Chip không chứa claim | Owner KB/retrieval | Query hồi quy chọn đúng file/chunk |
| Tổng hợp sai | Chip đúng nhưng conclusion sai | Owner prompt/model | Answer mới + source không đổi/đúng |
| Attachment fail | Composer/toast/request bất thường | Owner Agent/tenant admin | Test file synthetic pass hoặc blocker có căn cứ |
| Quyền | Không thấy Agent/KB | Space/owner admin | Role/scope được xác minh theo phê duyệt |

### Quy tắc hiển thị nguồn và hình ảnh

Với Markdown có ảnh, source drawer phải mở đúng Markdown, còn UI chat phải render ảnh qua URI MinIO; hai kiểm tra này khác nhau. Link local `assets/...` có thể chạy trong HTML offline nhưng không phải đường phát hành cho chat. Nếu response nêu ảnh mà chỉ có URL hoặc placeholder, đánh dấu render chưa pass. Nếu ảnh render nhưng source Markdown sai, không chấp nhận answer chỉ vì visual đẹp.

Gói evidence tối thiểu cho một incident gồm: query đã che dữ liệu nhạy cảm, thời điểm, Agent/model, KB chips, answer, source drawer, trạng thái file, Request Information đã che và câu hồi quy sau sửa. Nếu không có đủ, trạng thái là **Đang xem** thay vì **Đã xử lý**.

Khi feedback nêu claim nghiệp vụ, liên hệ owner nội dung để xác nhận canonical source; không buộc model chọn câu trả lời theo phản hồi đơn lẻ.
Một source không còn truy hồi được sau update cần được coi là regression có owner, không chỉ là feedback UI.

### Lỗi và giới hạn

- Source đúng không đồng nghĩa answer đúng: model có thể tổng hợp sai hoặc ưu tiên sai; kiểm tra cả hai.
- Answer đúng không đồng nghĩa retrieval pass: có thể model đã biết sẵn; bắt buộc kiểm tra source khi use case yêu cầu grounded answer.
- Feedback là chỉ dấu Human; không tự suy ra root cause từ thumbs-down.
- Không sao chép JSON request, private URL có ID, credential hoặc browser storage vào audit/workspace.
- `[[chunk#...]]` phải được coi là lỗi format/answer; nó vẫn có thể hữu ích cho kỹ thuật viên xác nhận chunk tồn tại.

### Checklist

- [ ] Có chat mới và follow-up được đánh dấu khác session.
- [ ] Mỗi claim quan trọng có source được mở kiểm tra.
- [ ] No-hit và conflict có outcome rõ ràng.
- [ ] Request Information được che ID/URL trước khi dùng ảnh.
- [ ] Feedback có trạng thái, owner điều tra và test hồi quy trước khi đóng.
<!-- /MODULE -->

<!-- MODULE:doc-19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md -->
## 19 - Agent: vòng đời, phân quyền, quan sát và bảo trì {#19-vong-doi-phan-quyen-quan-sat-va-bao-tri}

### Khái niệm

Vòng đời Agent gồm tạo, cấu hình, test, phát hành, sửa, nhân bản, tắt/bật, chia sẻ và xóa. Nội dung KB có vòng đời riêng: Agent có thể tiếp tục tồn tại khi Markdown bị thay; vì thế rollback Agent không thay thế rollback KB. Thao tác destructive hoặc quyền phải được kiểm soát theo owner và bằng chứng trước/sau.

![Menu vòng đời và UI chia sẻ](<knowledge/GS9 Knowledge VNG AI/image-49-agent-chia-se-va-vong-doi.png>)

*Ảnh 19.1 – Menu Agent user-owned có Chat, Edit, Clone, Disable/Enable và Delete; UI chia sẻ chỉ được quan sát, không gửi lời mời trong audit.*

### Bảng control

| Thao tác | Đã thực hiện live | Điều kiện/guardrail |
|---|---|---|
| Tạo Agent disposable | Có | Đặt tên `TEST -`, mô tả rõ xóa sau audit |
| Clone | Có | Kiểm tra bản sao có cấu hình dự kiến trước khi dùng |
| Disable → Enable | Có | Toast xác nhận; kiểm tra trạng thái cuối là enabled |
| Edit | Có ở phạm vi config test | Lưu baseline, A/B một biến, restore |
| Delete Agent test | Được phép sau audit | Xác nhận đúng tên, owner và không phải default/production |
| Chia sẻ Space/role | Chỉ xem UI | Không gửi invitation hoặc add vào Space khi chưa có uỷ quyền |
| Delete Agent production | Không test | Export/backup config, kiểm tra sharing và rollback trước |

| Role trong UI chia sẻ | Ý nghĩa đã quan sát | Trạng thái |
|---|---|---|
| Chỉ xem | Role có thể chọn khi chia sẻ Space | **Có điều kiện:** không test quyền end-to-end |
| Được chỉnh sửa | Role có thể chọn khi chia sẻ Space | **Có điều kiện:** không test quyền end-to-end |

### SOP

1. Tạo Agent `TEST - <mục đích> - <ngày>`; tuyệt đối không đổi sáu Agent mặc định để thử UI.
2. Lưu ảnh/cấu hình baseline trước clone hoặc A/B; ghi model, KB, tool, threshold, version KB.
3. Test functional rồi clone disposable; test disable/enable trên clone để không phá session baseline.
4. Chỉ mở tab Chia sẻ và đọc role/Space nếu chưa được cấp quyền gửi chia sẻ.
5. Khi release, phân công owner, bộ regression, cadence review và kênh tiếp nhận feedback.
6. Khi retire test resource, lưu audit trước; xóa đúng resource `TEST` theo tên/ID, xác minh không đụng default/existing test.
7. Sau bất kỳ xóa/thay thế nào, đối chiếu inventory, source drawer và ảnh MinIO; nếu fail, rollback theo backup đã lưu.

### Data flow

```text
draft config → test Agent → evidence/audit → publish/share (nếu được phê duyệt)
      ↘ clone disposable → disable/enable → audit → delete exact TEST resource

KB master → strict build → consumer Markdown → Agent retrieval
                 ↑ rollback source/MD khác với rollback Agent config
```

### Ma trận kiểm thử

| Nhóm | Test | Pass | Không được làm |
|---|---|---|---|
| Create | Agent TEST có KB/tool hợp lệ | Tạo thành công, có chat | Không dùng Agent default |
| Clone | Clone Agent TEST | Bản sao xuất hiện, cấu hình cần thiết có mặt | Không clone production để thử |
| Toggle | Disable rồi Enable clone | Có hai toast, trạng thái cuối Enabled | Không toggle Agent đang phục vụ Human |
| Share | Mở UI role | Thấy Space/Chỉ xem/Được chỉnh sửa | Không gửi share/invite |
| Delete | Xóa exact TEST sau audit | Resource biến mất, audit còn | Không xóa khi tên/owner mơ hồ |
| Maintenance | Re-run regression sau KB rollout | Mỗi module mới có source/ảnh | Không gộp content change với nhiều config change |

### Bằng chứng

- **Đã kiểm chứng:** Agent `TEST - Agent Lifecycle Deep Audit 2026-08-11` được tạo với 2 KB và tool set; clone được tạo.
- **Đã kiểm chứng:** clone đã Disable (toast “Đã tắt trợ lý”) rồi Enable (toast “Đã bật trợ lý”); trạng thái cuối là bật trước cleanup.
- **Đã kiểm chứng:** menu user-owned hiển thị Chat, Edit, Clone, Disable/Enable, Delete.
- **Có điều kiện:** tab Chia sẻ hiển thị Space/roles nhưng audit không gửi chia sẻ, nên không tuyên bố role end-to-end.
- **Chưa xác định:** khôi phục sau Delete Agent không được suy luận nếu UI không hứa hẹn và chưa test.

### Lịch bảo trì khuyến nghị

| Chu kỳ | Việc làm | Output tối thiểu |
|---|---|---|
| Sau thay KB/Markdown | Chạy canonical, conflict, no-hit; mở source/ảnh | Audit ngày, source pass/fail |
| Sau đổi model/prompt/tool | A/B một biến; restore nếu không đạt | Config diff và kết quả hồi quy |
| Hàng tuần | Xem feedback chưa xử lý, quota/error trend | Owner và trạng thái Hộp xử lý |
| Hàng tháng | Rà soát quyền Space, Agent tắt, Agent TEST cũ | Danh sách giữ/xóa có phê duyệt |
| Trước xóa/retire | Backup config/evidence, xác nhận exact target | Rollback plan và người duyệt |

Agent không có “phát hành tự động an toàn” chỉ vì nút lưu thành công. Mỗi lần thay đổi quan trọng phải có một định danh version/audit, một bộ regression và một owner chịu trách nhiệm quay lại baseline khi source/answer regress.

### Phân vai vận hành

| Vai trò | Quyết định | Không được tự ý làm |
|---|---|---|
| Owner nội dung | Canonical source, phiên bản, mâu thuẫn nghiệp vụ | Đổi model/quyền để che lỗi nguồn |
| Owner Agent | Prompt, KB scope, tool, regression | Sửa master KB trực tiếp trong generated module |
| Space/admin | Quyền truy cập, model/ASR provisioning | Cấp rộng quyền chỉ để test một lỗi |
| Reviewer | Xem evidence, source, rollback | Phê duyệt chỉ dựa trên screenshot câu trả lời |
| Human dùng Agent | Feedback/clarification | Được xem là owner của dữ liệu KB tự động |

Trước delete, dùng “bốn xác nhận”: đúng tên hiển thị; đúng owner; đúng mục đích `TEST`; và audit/backup đã tồn tại. Nếu một xác nhận thiếu, không bấm Delete. Delete là thao tác cuối lifecycle, không phải biện pháp làm mới nội dung; nội dung cần đổi đi theo master → build → consumer → chat test.

Sau cleanup, reload danh sách và đối chiếu count/đúng tên để đảm bảo không còn resource TEST ngoài ý muốn và không ảnh hưởng Agent đang tồn tại.
Nếu lịch sử chat test cần giữ làm audit, lưu bằng chứng đã che trước cleanup thay vì giữ Agent TEST vô thời hạn.

### Lỗi và giới hạn

| Rủi ro | Kiểm soát |
|---|---|
| Xóa nhầm Agent | Tên TEST độc nhất, owner, ID, ảnh/audit trước delete; dừng nếu mơ hồ |
| Drift cấu hình | Baseline/export mô tả + test matrix + A/B một biến |
| KB update làm Agent regress | Publish Markdown theo thứ tự asset → map → strict build → consumer → chat source test |
| Chia sẻ sai phạm vi | Xem UI trước; chỉ gửi khi có quyền/đích/rõ role |
| Quan sát thiếu context | Lưu source, model, KB chips và Request Information đã che |

### Checklist

- [ ] Agent production/default không bị dùng làm đối tượng test phá huỷ.
- [ ] Clone/toggle/delete chỉ trên resource `TEST` được định danh chính xác.
- [ ] Chia sẻ chỉ quan sát cho đến khi có phê duyệt gửi thật.
- [ ] Có owner, regression set, lịch review và đường rollback.
- [ ] Audit được cập nhật trước STATUS/HANDOFF và trước cleanup TEST.
<!-- /MODULE -->
