# Nhật ký kiểm chứng Knowledge VNG - 06/08/2026

Trạng thái: Đã hoàn tất phần kiểm chứng có thể thực hiện  
Phạm vi: `https://vnggames.ai/kb/knowledge`  
Nguồn đối chiếu: `so-tay-tao-knowledge-base-v3.md`  
Nguyên tắc: Chỉ ghi trên KB test; không xóa KB có sẵn; không dùng credential thật trong tài liệu.

## 1. Môi trường và dữ liệu test

- Giao diện tiếng Việt, nhãn **KNOWLEDGE BASE BETA**.
- Có 8 KB mang tên thử nghiệm tại thời điểm bắt đầu.
- Hai KB dùng chính; identifier được quan sát từ route trong phiên audit ngày 06/08/2026:
  - `Test Doc RAG+Wiki` - loại Tài liệu; KB ID `8902e4d0-4884-4be7-a54b-1d193bf8506a`; tenant `10012`.
  - `Test 2 chỉ câu hỏi + tách` - loại FAQ; KB ID `73de52af-6511-468e-94bb-cca61c670b31`; tenant `10012`.
- Dữ liệu mới tạo gồm bộ Aurora/Borealis, tài liệu test ảnh, một bản nháp và 14 ảnh hướng dẫn.

## 2. Kết quả cấu trúc giao diện

| Hạng mục | Kết quả | Trạng thái |
|---|---|---|
| Cài đặt Tài liệu | Tổng quan, Mô hình, Xử lý, Chia sẻ, Nguồn dữ liệu | Đã kiểm chứng |
| Cài đặt FAQ | Tổng quan, Mô hình, Chia sẻ, Nguồn dữ liệu; không có Xử lý | Đã kiểm chứng |
| Trang làm việc | Documents, Wiki, Graph xuất hiện ở cả Tài liệu và FAQ | Đã kiểm chứng |
| Wiki/Graph của FAQ | Chỉ hiện “Wiki chưa được bật”; FAQ không có control bật Wiki | Khung giao diện dùng chung |
| Loại KB | Bị khóa sau khi tạo | Đã kiểm chứng |
| Embedding khi đã có nội dung | Hiển thị khóa | Đã kiểm chứng |

## 3. RAG, Wiki và Graph

- RAG và Wiki là checkbox độc lập, bật đồng thời được.
- Ba mức Wiki: **Tập trung, Tiêu chuẩn, Toàn diện**.
- Caption của Tiêu chuẩn: “Số trang cân bằng.”
- Wiki có Mục lục, Nhật ký hoạt động, xem theo Thư mục/Loại và tạo thư mục.
- Graph có chú giải: Tóm tắt, Thực thể, Khái niệm, Tổng hợp, So sánh.

### Phép thử Tổng hợp/So sánh

1. Nạp tài liệu Aurora, Borealis và một tài liệu so sánh hai hệ thống.
2. Chuyển độ chi tiết Wiki từ Tiêu chuẩn sang Toàn diện.
3. Chạy Phân tích lại tài liệu so sánh.
4. Mở Graph và kiểm tra số node.

Kết quả sau cùng: 93/93 node, gồm Tóm tắt 9, Thực thể 42, Khái niệm 41, Tổng hợp 0, So sánh 0. Không tìm thấy thao tác tạo tay hai loại node. Điều kiện sinh Tổng hợp/So sánh chưa xác định.

## 4. Model, VLM và ASR

| Hạng mục | Kết quả |
|---|---|
| Chat model ở Tài liệu | `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b`, `qwen3.6-plus` |
| `deepseek-v4-flash` ở FAQ | UI cho chọn nhưng lưu lỗi `LLM model not found` |
| VLM ở KB test | Đang bật, `hosted_vllm/qwen3.6-35b`; không suy ra mặc định |
| ASR | Bật toggle làm hiện model/ngôn ngữ; dropdown model rỗng |
| Cảnh báo ASR cũ | Không còn thấy dòng “liên hệ admin” |

FAQ test được chuyển sang `qwen3.6-plus` để tiếp tục kiểm thử.

## 5. Parser

| Nhóm | Các lựa chọn quan sát trực tiếp |
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
| Audio | UI hiển thị Built-in; dropdown chỉ có Simple |

Đính chính quan trọng: PPT/PPTX không có Built-in trong dropdown. Audio vẫn có mâu thuẫn giá trị hiển thị/lựa chọn.

## 6. Phân đoạn

Trạng thái quan sát trong KB Tài liệu:

- Tự động, Cha-con.
- Cha 32.768 ký tự, con 8.192 ký tự.
- Chồng lấp 0/0.
- Truy hồi theo ngữ cảnh bật.
- Sinh câu hỏi tắt.
- Giới hạn token 0.
- Dấu phân cách: dòng trống, dòng mới, `。`, `！`, `？`, `;`, `；`.
- Gợi ý ngôn ngữ DE/EN/ZH; ô để trống.

Đây là trạng thái hiện hữu, không được ghi thành mặc định sản phẩm nếu chưa tạo KB trắng đối chứng.

## 7. Chia sẻ và nguồn dữ liệu

- Chia sẻ qua Space với quyền **Chỉnh sửa** hoặc **Chỉ đọc**.
- Connector quan sát được: Notion, Google Drive, NAS.
- Wizard: Chọn loại, Thông tin xác thực, Tài nguyên, Chiến lược.
- Notion: Tên, Integration Token, kiểm tra kết nối.
- Google Drive: Tên, Service account JSON, Shared Drive ID tùy chọn.
- NAS: Tên, UNC share, username, password.
- Không có credential test nên chưa đi được bước 3-4.

## 8. FAQ

### Cấu trúc và tìm kiếm

- Thêm Q&A: câu hỏi chuẩn tối đa 200 ký tự; câu tương tự 0/10; loại trừ 0/10; trả lời 0/5; phân loại.
- Kiểm tra tìm kiếm: ngưỡng 0-1, bước 0,1, mở ra ở 0,5; số kết quả 1-50, mở ra ở 10.
- “Server bảo trì lúc nào?” ở ngưỡng 0 trả về mục đúng, điểm 1,000.
- Từ khóa chỉ có trong câu trả lời không tìm thấy ở chế độ Chỉ câu hỏi, kể cả ngưỡng 0.

### Mâu thuẫn index bị khóa

Banner nói index bị khóa khi có nội dung. Thao tác thật:

1. Chuyển Chỉ câu hỏi sang Câu hỏi + trả lời, lưu thành công.
2. Mở lại, giá trị được giữ.
3. Chuyển về Chỉ câu hỏi + Tách, lưu thành công.

Kết luận: loại và Embedding vẫn khóa; hai control index FAQ còn hoạt động.

### Xuất và nhập lại

- Nút Xuất tạo `faq_export_2026-08-06 (2).csv`, 5 dòng Q&A.
- Header tiếng Anh; trường nhiều giá trị nối bằng `##`.
- Chọn chính file xuất trong modal Nhập: hệ thống đọc đủ 5 mục và bật nút Nhập.
- Dừng ở preview để không tạo trùng.
- Menu mẫu có JSON, CSV, Excel.

## 9. Documents và thao tác nội dung

### Menu thêm tài liệu

- Tải tệp lên.
- Tải thư mục lên.
- Nhập từ URL - disabled.
- Soạn thảo trực tuyến.

### Upload thư mục

Modal có input `multiple` + `webkitdirectory` và Xử lý nâng cao. API extension không gắn được thư mục hoặc danh sách file vào input native. Phép thử chọn thư mục thật bị chặn kỹ thuật. Bộ Aurora/Borealis được upload theo file, nên không dùng làm bằng chứng giữ cấu trúc thư mục.

### Lưu nháp

- Tạo `AUDIT-NHAP-20260806`, marker `AUDIT-DRAFT-20260806`.
- Bấm **Lưu nháp**, toast “Đã lưu bản nháp”.
- Tài liệu có trạng thái Bản nháp.
- Chat hỏi marker không truy hồi được bản nháp.

### Sửa nội dung MANUAL

- Tài liệu `Test soạn thảo trực tuyến.md`, nguồn MANUAL.
- Nhãn menu đúng là **Sửa nội dung**.
- Trước sửa: 3 chunk.
- Thêm marker `AUDIT-MANUAL-EDIT-20260806`, Xuất bản: trạng thái Chờ xử lý, Đang hoàn tất, Hoàn tất; tóm tắt chứa marker; 4 chunk.
- Phục hồi chính xác nội dung gốc và Xuất bản lại: marker biến mất, trở về 3 chunk.

### Phân tích lại

- Tài liệu `03-so-sanh-aurora-borealis.md` trước: 1 chunk.
- Đổi Wiki Tiêu chuẩn sang Toàn diện, lưu thành công.
- Bấm Phân tích lại: Hoàn tất, Chờ xử lý, Đang hoàn tất, Hoàn tất.
- Sau: vẫn 1 chunk; thời gian tải lên giữ nguyên; tóm tắt đổi cách diễn đạt.

## 10. Ảnh trong chat

### Test đường dẫn tương đối - không đạt

- MD dùng `![...](assets/codex-agentic-loop-example.png)`.
- Ảnh được upload riêng.
- Chat tìm thấy nguồn và mô tả ảnh, nhưng không có thẻ `img` trong câu trả lời.
- Bằng chứng: `audit/evidence/2026-08-06-chat-image-not-rendered.png`.

### Test URI MinIO - đạt

- Lấy link nội bộ ảnh: `minio://knowledge-base-prd/.../codex-agentic-loop-example.png`.
- Tạo MD mới dùng chính URI đó.
- Retriever chuyển link thành image token.
- Câu trả lời có thẻ ảnh, alt “Sơ đồ Codex Agentic Loop” và render đúng hình.
- Bằng chứng: `audit/evidence/2026-08-06-chat-image-minio-rendered.png`.

Kết luận đóng gói:

1. Giữ ảnh cục bộ cho người đọc và HTML offline.
2. Upload ảnh độc lập để hệ thống tạo URI MinIO.
3. Chèn URI MinIO vào file MD phân phối.
4. Giữ ảnh nguồn trong KB khi MD còn tham chiếu.

## 11. Tác động còn lại trên KB test

- `Test Doc RAG+Wiki`: Wiki đang ở mức Toàn diện; có bộ Aurora/Borealis, tài liệu test ảnh, ảnh hướng dẫn và một bản nháp.
- `Test 2 chỉ câu hỏi + tách`: model chat là `qwen3.6-plus`; index đã phục hồi về Chỉ câu hỏi + Tách.
- Tài liệu MANUAL đã phục hồi đúng nội dung gốc.
- Không xóa ảnh đang cung cấp URI MinIO cho bộ tài liệu cuối.

## 12. Mục bị chặn hoặc chưa xác định

1. Upload thư mục thật và cấu trúc thư mục con sau upload.
2. Điều kiện sinh node Tổng hợp/So sánh.
3. Bước 3-4 của nguồn dữ liệu ngoài khi có credential.
4. Hành vi đồng bộ thêm/sửa/đổi tên/xóa/quyền ở Notion, Drive, NAS.

Các mục này phải tiếp tục mang nhãn Bị chặn/Chưa xác định trong tài liệu chính.

## 13. Đóng gói ảnh cho 12 module

- Đã tải 14 ảnh hướng dẫn lên `Test Doc RAG+Wiki` như các nguồn độc lập.
- Mở các đoạn nguồn được retriever trả về và lấy URI đầy đủ có alt trùng tên file.
- Mapping được lưu tại `knowledge-vng/image-map.json`.
- Bộ build thay ảnh cục bộ bằng URI `minio://` trong 12 file MD phân phối, đồng thời giữ `LOCAL_ASSET` trong comment để người bảo trì biết ảnh gốc.
- Build nghiêm ngặt dừng nếu một ảnh thật chưa có mapping MinIO; ví dụ ảnh nằm trong fenced code không được xem là tài nguyên cần mapping.
- Ở lượt kiểm tra ban đầu, ba ảnh `04-xu-ly-parser-theo-dinh-dang.png`, `09-wiki-muc-luc-va-trang.png` và `11-faq-danh-sach-nhap-xuat-tim-kiem.png` vẫn hiện `Đang hoàn tất` ở danh sách Documents sau nhiều lần tải lại, dù chat đã truy hồi được đoạn nguồn và URI đầy đủ.
- Lượt đối chiếu cuối cùng cùng ngày xác nhận `04-xu-ly-parser-theo-dinh-dang.png` và `09-wiki-muc-luc-va-trang.png` đã chuyển sang `Hoàn tất`; chỉ còn `11-faq-danh-sach-nhap-xuat-tim-kiem.png` hiện `Đang hoàn tất`. Tab Wiki đồng thời báo “Đang xử lý 1 tài liệu…”. Đây là trạng thái nền có thể tiếp tục thay đổi, nên nhật ký giữ cả ảnh chụp ban đầu và kết quả đối chiếu sau.
- Cùng lượt đối chiếu cuối, Graph hiển thị 159/159 node: Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0, So sánh 0. Kết quả này thay ảnh chụp số lượng 93 node nếu cần mô tả trạng thái hiện tại, nhưng không thay đổi kết luận rằng điều kiện sinh Tổng hợp/So sánh chưa xác định.

## 14. Kiểm tra artifact cuối

### HTML offline

- Không có stylesheet, script hoặc font bên ngoài; 14 ảnh được nhúng thành data URI.
- Desktop: sidebar cố định, tìm kiếm, nội dung và viewer ảnh hoạt động.
- Tìm `MinIO`: bộ đếm đổi từ 25 xuống 6 mục.
- Mobile 390 x 844: menu mở/đóng đúng `aria-expanded`; sau sửa lỗi, `document.scrollWidth = clientWidth = 375`, không còn tràn ngang.
- Viewer ảnh mở đúng alt text và đóng được.

### Bộ mẫu FAQ

- JSON và CSV dùng đúng schema của template tải từ menu **Tệp mẫu**.
- XLSX được nhập từ template chính thức, giữ nguyên 6 cột, điền 3 mục tiếng Việt, kiểm tra lại range `FAQ!A1:F4`, không có lỗi công thức và đã render để kiểm tra chữ không bị cắt.
- File CSV do tool xuất vẫn là bằng chứng live re-import: đọc đủ 5 mục ở preview.
- Live preview trong modal **Nhập** đọc đúng `3 mục` cho từng file `mau-faq.json`, `mau-faq.csv` và `mau-faq.xlsx`; ba câu hỏi hiển thị đúng ở danh sách xem trước và nút **Nhập** được bật.
- Sau mỗi lượt kiểm tra, modal được đóng bằng **Hủy**. Không bấm **Nhập**; danh sách FAQ vẫn giữ nguyên 5 mục.

### Build và kiểm tra hồi quy

- Nguồn chuẩn được chốt ở phiên bản `3.0.1`; builder lấy phiên bản và ngày cập nhật trực tiếp từ metadata của MD thay vì hardcode trong hero/sidebar HTML.
- Regression test `test_build_offline_html_uses_version_from_source` đã được chạy theo chu trình đỏ-xanh và giữ builder không tái phát lỗi lệch phiên bản.
- Build nghiêm ngặt tạo đúng 12 module với 14 liên kết ảnh MinIO và một HTML offline có 14 ảnh data URI, không có stylesheet/script ngoài.
- Toàn bộ 7 test tự động đạt; completion audit độc lập đạt với `ERROR_COUNT=0`.
