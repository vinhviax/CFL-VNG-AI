# KB — Parser và xử lý file

Parser nào có cho định dạng nào, MinerU dùng khi nào, OCR / VLM / ASR đứng ở đâu trong pipeline, và những mâu thuẫn UI đã ghi nhận.

**Nguồn bằng chứng chính**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| [`audit/audit-knowledge-vng-2026-08-06.md`](../../audit/audit-knowledge-vng-2026-08-06.md) §5, §4 | 06/08/2026 | Ma trận parser khi **upload tay**; trạng thái VLM/ASR |
| [`audit/audit-google-drive-connector-2026-08-07.md`](../../audit/audit-google-drive-connector-2026-08-07.md) | 07/08/2026 | Ma trận parser trong **wizard Google Drive** |
| [`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`](../../audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md) | 14/08/2026 | Parser Hình ảnh = `MinerU` trên một KB thật |
| [`audit/business-kb-readonly-audit-2026-08-14.md`](../../audit/business-kb-readonly-audit-2026-08-14.md) | 14/08/2026 | `parse_status` / `error_message` của tài liệu live |
| `so-tay-tao-knowledge-base-v3.md` | — | Module `doc-05`, `doc-06`, `doc-08`, `doc-12` |
| [`audit/archive/so-tay-tao-knowledge-base-v3-truoc-audit-2026-08-06.md`](../../audit/archive/so-tay-tao-knowledge-base-v3-truoc-audit-2026-08-06.md) §8.2–8.4, §9.4 | trước 06/08/2026 | **Master lưu trữ, đã bị thay thế.** Chứa tên parser Excel tùy chỉnh và pool model VLM. Mục lấy từ đây đánh dấu **(archive)**, giữ mức *Có điều kiện* |

**Phạm vi quan sát:** tenant `10012`. Danh sách parser **phụ thuộc tenant** — parser tiền tố `FPA ·` là parser do chính tenant test đăng ký, không phải mặc định sản phẩm (§5).

---

## 1. Parser là gì trong pipeline này

Parser là bộ đọc chuyển file thành nội dung văn bản để hệ thống chia chunk và lập chỉ mục. Đổi parser → nội dung chunk đổi → kết quả truy hồi đổi, dù file nguồn không thay đổi một byte.

Parser chỉ tồn tại ở **KB Tài liệu**, trong tab **Cài đặt → Xử lý**. KB FAQ không có tab Xử lý (kiểm chứng 06/08/2026).

Tên engine quan sát được trên UI: **Built-in, Simple, MinerU, LLM, markitdown, liteparse**. Không định dạng nào có đủ cả sáu.

| Engine | Cách hiểu thực dụng (để chọn bài test, **không** phải cam kết kỹ thuật nội bộ) |
|---|---|
| **Built-in** | Bộ đọc tích hợp của hệ thống |
| **Simple** | Trích xuất đơn giản; phù hợp văn bản ít bố cục |
| **MinerU** | Hướng tới tài liệu có bố cục, bảng, hình phức tạp |
| **LLM** | Dùng model diễn giải cấu trúc; tốn thời gian, có thể tạo cách viết khác nguồn |
| **markitdown** | Chuyển nhiều định dạng sang Markdown |
| **liteparse** | Lựa chọn riêng, chỉ quan sát được ở PDF |

---

## 2. Ma trận parser khi upload tay

Quan sát trực tiếp trong dropdown tab **Xử lý**, ngày **06/08/2026**, tenant `10012`.

| Nhóm file | Lựa chọn thấy trong dropdown |
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
| Audio | UI hiển thị `Built-in` đang chọn, **nhưng dropdown chỉ có `Simple`** |

### Hai mâu thuẫn UI đã ghi nhận

1. **PPT/PPTX không có Built-in.** Đây là đính chính so với tài liệu cũ. Nếu code hoặc doc nào giả định PPT dùng Built-in, giả định đó sai với UI ngày 06/08/2026.
2. **Audio: giá trị hiển thị ≠ tập lựa chọn.** UI cho thấy `Built-in` là giá trị đang chọn, nhưng mở dropdown chỉ thấy `Simple`. Chưa xác định giá trị nào thực sự chạy ở runtime — đúng tinh thần DEC-022: cấu hình UI không bằng hành vi runtime.

---

## 3. Ma trận parser trong wizard Google Drive khác với upload tay

Quan sát ngày **07/08/2026**, trong bước **Chiến lược** của wizard nguồn dữ liệu Google Drive.

| Loại | Parser đang hiển thị trong lượt test |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in; kèm chọn `Tự nhận diện` hoặc `Thủ công` |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

**Đây không phải cùng một tập lựa chọn với §2.** Ví dụ PowerPoint hiện `MinerU` ở đây trong khi upload tay có `MinerU, markitdown`; Markdown hiện `Built-in` trong khi upload tay có bốn lựa chọn. Không sao chép bảng này thành bảng kia.

Không có bằng chứng nào cho rằng nguồn ngoài dùng **cùng** parser với upload tay. Module `doc-08` ghi rõ đây là điều **không được suy luận** cho tới khi có ma trận nhiều chu kỳ.

Phần connector đầy đủ (xác thực, chọn tài nguyên, lịch, chế độ, xung đột, regex, tag, đồng bộ xóa) nằm ở [`KB-google-drive-connector.md`](KB-google-drive-connector.md).

---

## 4. MinerU

| Quan sát | Ngày | Nguồn |
|---|---|---|
| Có trong dropdown của PDF, Word, PPT/PPTX, Excel, Images khi upload tay | 06/08/2026 | Audit §5 |
| Là parser hiển thị cho PDF/Word/PowerPoint và Ảnh trong wizard Google Drive | 07/08/2026 | Module `doc-08`, `doc-12` |
| Là parser **đang lưu** cho nhóm Hình ảnh (`.jpg .jpeg .png .gif .bmp .tiff .webp`) trên KB thật `GS9 CFL Plan Version` (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`) | 14/08/2026 | Audit CFL Plan V5 |

Đó là toàn bộ những gì đã kiểm chứng về MinerU. **Không có bằng chứng nội bộ nào** trong project về chất lượng đầu ra MinerU so với các engine khác — chưa ai chạy A/B trên cùng một file. Mô tả "hướng tới tài liệu có bố cục phức tạp" ở §1 là cách hiểu để chọn bài test, không phải kết quả đo.

---

## 5. Parser tùy chỉnh của tenant — tiền tố `FPA ·`

Kiểm chứng 07/08/2026, trong wizard Google Drive.

Nhóm Excel có thêm một khối riêng, **tách khỏi dropdown engine ở §2**, với hai chế độ (archive §9.4):

| Chế độ | Mô tả trên tool |
|---|---|
| **Tự nhận diện** (mặc định) | *"Tự nhận diện đọc định dạng và phòng ban từ tên từng tệp."* — hệ thống đọc **tên file** để đoán khuôn mẫu Excel nào đã cấu hình sẵn |
| **Thủ công** | *"Thủ công ghim một parser cho mọi tệp Excel trong kho tri thức này."* — hiện thêm trường **Định dạng parser** |

Trường **Định dạng parser** **không phải** danh sách engine, mà là danh sách **khuôn mẫu định dạng Excel đã cấu hình sẵn**. Giá trị quan sát được (archive):

- `Không dùng` (mặc định) — đọc Excel như bảng thường
- `FPA · Monthly Performance`
- `FPA · Launching & Checkpoint`

**Master hiện hành (caption Ảnh 08.11 / 12.9, kiểm chứng 07/08/2026) kết luận: các parser tiền tố `FPA ·` là cấu hình riêng của tenant test, không phải mặc định chung.** Tenant khác gần như chắc chắn không có các parser này, hoặc có bộ khác hoàn toàn.

*Mâu thuẫn nguồn cần biết:* bản archive (trước 06/08/2026) ghi mục này ở trạng thái **chưa xác thực** — chưa rõ khuôn mẫu `FPA ·` do tổ chức tự tạo hay có sẵn của tool, và có tạo thêm được không. Master hiện hành khẳng định là cấu hình tenant nhưng **không dẫn bằng chứng mới** cho việc "ai tạo ra chúng". Coi phần "tenant-specific" là **Có điều kiện**: đủ chắc để không hard-code, chưa đủ chắc để giải thích cơ chế đăng ký parser.

Quy tắc dùng:

- Chỉ chọn parser tùy chỉnh khi cấu trúc workbook **đúng với** cấu trúc parser đó yêu cầu.
- Không chọn chỉ vì tên nghe phù hợp.
- Nếu không chắc: dùng `Tự nhận diện` hoặc cấu hình mặc định đã kiểm thử.
- Không viết code hoặc tài liệu hard-code tên parser `FPA ·` như một hằng số nền tảng.

---

## 6. OCR, VLM và ASR

Ba thứ này nằm ở ba nơi khác nhau, dễ nhầm.

| Tính năng | Ở đâu | Trạng thái đã kiểm chứng |
|---|---|---|
| **VLM** (đọc nội dung hình ảnh) | Tab **Mô hình** của KB Tài liệu | 06/08/2026: đang **bật** trên KB test, model `hosted_vllm/qwen3.6-35b` |
| **ASR** (âm thanh → văn bản) | Tab **Mô hình**, sau khi bật toggle | 06/08/2026: bật toggle làm hiện **Mô hình ASR** + **Ngôn ngữ**; **dropdown model rỗng** |
| **Ép OCR toàn bộ PDF** | Bước Chiến lược của wizard nguồn dữ liệu (cấp nguồn, không phải cấp KB) | 07/08/2026: chỉ quan sát control, chưa chạy đối chứng |
| **Đa phương thức** | Bước Chiến lược của wizard nguồn dữ liệu | 07/08/2026: chỉ quan sát control |

VLM và ASR nằm trong khối **"Tùy chọn mô hình nâng cao"** của tab Mô hình, bấm mở rộng dưới ba dropdown chính. Khối này **không xuất hiện ở loại FAQ** (archive §8.3–8.4).

| Tùy chọn | Mô tả trên tool | Mặc định (archive) |
|---|---|---|
| Đa phương thức (VLM) | "Trích xuất nội dung ảnh bằng mô hình thị giác" | **Tắt** |
| Nhận dạng giọng nói (ASR) | "Chuyển audio thành văn bản" | **Tắt** |

### VLM

Trạng thái "đang bật" trên KB test **chỉ chứng minh cấu hình hiện hữu**. Không suy ra VLM mặc định bật cho KB mới — archive ghi mặc định là Tắt, nhưng đó là nguồn đã bị thay thế, giữ mức *Có điều kiện*.

Ý nghĩa: xử lý ảnh trong tài liệu (screenshot, sơ đồ, biểu đồ) **không tự động** — phải chủ động bật và chọn **Mô hình VLM**.

**Pool VLM hẹp hơn pool chat** (archive §8.2): chỉ có `qwen3.6-plus`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b` — **không bao giờ thấy** `deepseek-v4-flash`, kể cả khi vai trò Chat/tóm tắt của cùng KB đó đang liệt kê 4 model.

Đã kiểm chứng: VLM xử lý được ảnh giao diện và sinh tóm tắt. Giới hạn đã ghi nhận: **OCR có thể đọc sai tên thương hiệu hoặc chữ nhỏ**. Vì vậy mọi ảnh phải đi kèm caption văn bản — không để một quy trình quan trọng chỉ tồn tại trong ảnh.

### ASR

Kết luận đúng là: **chưa chọn được model ASR trong môi trường đã kiểm thử (06/08/2026)**. Không được viết thành "sản phẩm không hỗ trợ ASR".

Ghi chú thay đổi giữa hai lượt quan sát: bản archive (trước 06/08/2026) ghi dropdown ASR rỗng **kèm** cảnh báo nguyên văn *"Chưa có model — liên hệ admin để thêm."* Audit 06/08/2026 xác nhận dropdown vẫn rỗng nhưng **dòng cảnh báo đó không còn xuất hiện**. UI đã đổi; tình trạng không dùng được thì chưa.

### Ép OCR toàn bộ PDF

Chỉ dùng cho PDF scan hoặc PDF có text-layer hỏng. Bật cho PDF có text-layer tốt là lãng phí thời gian xử lý mà không thêm thông tin.

---

## 7. Ghi đè parser ở cấp lượt nạp và cấp nguồn

| Vị trí | Control | Ngày kiểm chứng |
|---|---|---|
| Modal **Tải tệp lên** / **Tải thư mục lên** | Mục **Xử lý nâng cao** — ghi đè parser/chunk cho riêng lượt nạp | 06/08/2026 |
| Wizard nguồn dữ liệu, bước Chiến lược | Ghi đè parser theo loại tệp + ghi đè chunking + toggle đa phương thức/ASR/OCR | 07/08/2026 |
| Menu chi tiết tài liệu | **Phân tích lại với tùy chọn nâng cao** | 06/08/2026 |

Khuyến nghị đã ghi trong module `doc-08` / `doc-12`: giữ giá trị `0` hoặc để trống ở lượt đầu để kế thừa cấu hình KB. Chỉ ghi đè khi đã có bộ câu hỏi đối chứng để đo trước/sau.

---

## 8. Quy trình A/B parser

Cần thiết vì không có bảng xếp hạng chất lượng nào được kiểm chứng trong project này.

1. Chọn **một file đại diện** có heading, bảng, chú thích ảnh và **một mã độc nhất** (marker) để tra được trong chat.
2. Giữ nguyên mọi cấu hình khác — chỉ đổi parser.
3. Xử lý bằng parser A. Ghi **số chunk** và nội dung một vài chunk.
4. Dùng **Phân tích lại với tùy chọn nâng cao**, hoặc một KB test riêng, để chạy parser B.
5. Hỏi câu dựa vào **bảng**, **heading** và **caption ảnh** — ba chỗ parser hay làm hỏng nhất.
6. Chọn parser theo khả năng giữ đúng cấu trúc và dữ kiện, **không** theo độ dài tóm tắt.

### Dấu hiệu parser chưa phù hợp

- Heading bị nối vào đoạn trước.
- Cột bảng bị đảo hoặc mất tên cột.
- Text trong ảnh được đọc nhưng gắn sai khu vực.
- Một PDF dài chỉ thành một khối duy nhất, khó truy hồi.
- Tóm tắt nghe hợp lý nhưng **mã, số và ngoại lệ biến mất**.

---

## 9. Cạm bẫy đã gặp thật

### `Hoàn tất` không đồng nghĩa "parse đúng"

Trạng thái **Hoàn tất** chỉ xác nhận pipeline kết thúc. Phải mở chunk và chat để kiểm tra nội dung (06/08/2026).

Bằng chứng cụ thể từ audit KB nghiệp vụ 14/08/2026: hai tài liệu vẫn ở `parse_status: completed` nhưng mang `error_message`:

| Tài liệu | `error_message` |
|---|---|
| `01_weapons_usage.csv` | `Task interrupted due to application restart` |
| `CFL_082026.xlsx` | `task stuck > 2h10m0s with no queued task, recovered by housekeeping` |

Độ đầy đủ chunk của hai file này là **Có điều kiện** cho tới khi chat-test xác nhận.

### Trạng thái xử lý có thể treo lâu rồi tự chuyển

06/08/2026: ba ảnh (`04-...`, `09-...`, `11-...`) hiện `Đang hoàn tất` sau nhiều lần tải lại danh sách Documents — dù chat **đã** truy hồi được đoạn nguồn và URI đầy đủ của chính chúng. Lượt đối chiếu cuối ngày cho thấy hai trong ba đã tự chuyển sang `Hoàn tất`.

Nghĩa là: danh sách Documents và khả năng truy hồi thực tế có thể **lệch pha**. Đừng dùng riêng badge trạng thái làm gate.

### File `.png` phải có payload PNG thật

DEC-014: `.png` phải có magic bytes `89 50 4E 47 0D 0A 1A 0A`. Không đổi đuôi JPEG thành `.png`.

Lý do liên quan trực tiếp tới parser: **parser/VLM suy ra MIME và đường dẫn xuất từ nội dung thật**, nên file gắn sai đuôi sẽ sinh URI có đuôi `.jpg` — làm hỏng mapping ảnh. Nếu phát hiện sai, transcode sang PNG thật, giữ nguyên tên và kích thước, rồi kiểm tra lại signature trước khi upload.

### Upload thư mục bị chặn về mặt tự động hóa

06/08/2026: modal có input `multiple` + `webkitdirectory`, nhưng API extension **không gắn được** thư mục hoặc danh sách file vào input native.

14/08/2026: công cụ `file_upload` dùng whitelist đường dẫn **riêng, độc lập với quyền đọc file của agent**. Mọi đường dẫn tới file thật trong project đều bị từ chối, bất kể định dạng đường dẫn. Chỉ file trong scratchpad phiên làm việc được chấp nhận. Đã loại trừ các giả thuyết: độ dài đường dẫn, khoảng trắng, ký tự `:` của drive letter, từ khóa tiếng Việt.

Hệ quả vận hành: **upload hàng loạt phải do người thật thực hiện qua Explorer**, hoặc đi đường Google Drive connector (DEC-046).

---

## 10. Markdown vẫn cần cấu trúc tốt

Parser không thay thế việc viết heading. Với Markdown: một `#` cho tên tài liệu, `##` cho từng ý định người dùng thường hỏi. Cách này bền hơn việc dựa vào ký hiệu trang trí hoặc chữ in đậm.

---

## 11. Chưa kiểm chứng

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| Chất lượng đầu ra giữa các engine (MinerU vs Built-in vs LLM vs markitdown vs liteparse) | Chưa xác định | Chưa có lượt A/B nào trên cùng một file trong project |
| Parser nào **thực sự** chạy cho Audio | Chưa xác định | UI hiển thị `Built-in`, dropdown chỉ có `Simple` (06/08/2026) |
| `liteparse` làm gì khác các engine PDF còn lại | Chưa xác định | Chỉ quan sát tên trong dropdown |
| Nguồn ngoài (Drive/Notion/NAS) có dùng **cùng** parser với upload tay không | Chưa xác định | Hai ma trận §2 và §3 khác nhau; chưa test đối chứng |
| Parser `FPA ·` áp dụng đúng trên mọi bộ dữ liệu Excel | Chưa xác định | Chỉ quan sát danh sách; chưa chạy file thật qua parser tùy chỉnh |
| Hành vi thật của **Ép OCR toàn bộ PDF** | Chưa xác định | Mới quan sát control (07/08/2026) |
| Model ASR khả dụng ở tenant khác | Chưa xác định | Dropdown rỗng trên tenant `10012` ngày 06/08/2026 |
| Có phải mọi tenant thấy cùng 6 engine này | Chưa xác định | Danh sách parser đã chứng minh là phụ thuộc tenant (§5) |
| Upload thư mục có giữ cấu trúc thư mục con không | Bị chặn | Phép thử end-to-end không thực hiện được (06/08 và 14/08/2026) |
