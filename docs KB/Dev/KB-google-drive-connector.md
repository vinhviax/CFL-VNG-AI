# KB — Google Drive connector

Hành vi thật của Google Drive connector: hai trục cấu hình hay bị nhầm lẫn, cơ chế phát hiện thay đổi, và những gì nó **không** làm.

**Đọc kèm:** [`KB-anh-va-uri-minio.md`](KB-anh-va-uri-minio.md) — connector không tự xử lý ảnh, phải gắn URI thủ công.

---

## 1. Hai trục cấu hình độc lập — chỗ hay nhầm nhất

Màn hình **Chiến lược** có hai thiết lập riêng biệt. Chúng trả lời hai câu hỏi khác nhau và **không thay thế nhau**.

| Trục | Giá trị | Trả lời câu hỏi |
|---|---|---|
| **Chế độ đồng bộ** | `Tăng dần` / `Toàn bộ` | Lần chạy này connector **liệt kê những tài nguyên nào** từ nguồn? |
| **Chiến lược xung đột** | `Ghi đè` / `Bỏ qua nếu đã có` | Khi một tài nguyên **đã tồn tại trong KB**, làm gì với nó? |

Nhầm lẫn điển hình: nghĩ `Toàn bộ + Ghi đè` sẽ ép nạp lại mọi thứ. **Không đúng.** Xem mục 3.

### Chế độ đồng bộ

| Chế độ | Cơ chế |
|---|---|
| **Tăng dần** | Dựa vào **cursor** mà connector lưu từ lần chạy trước; chỉ xét phần thay đổi kể từ cursor đó |
| **Toàn bộ** | **Liệt kê lại từ đầu** toàn bộ tài nguyên đã chọn mỗi lần chạy; không dùng cursor |

Diễn giải "Toàn bộ = liệt kê lại toàn bộ tài nguyên đã chọn mỗi lần chạy" lấy từ mô tả trên UI, đối chiếu với quan sát vòng test 3a (16/08/2026).

### Chiến lược xung đột

| Giá trị | Hành vi |
|---|---|
| **Ghi đè** | Bản trong KB bị thay bằng bản từ Drive. Dùng khi Drive là nguồn chuẩn |
| **Bỏ qua nếu đã có** | Giữ bản đang có trong KB |

Khuyến nghị của sổ tay (`doc-12`): **Tăng dần** cho vận hành thường xuyên; chỉ dùng **Toàn bộ** khi cần quét lại có chủ đích. Sau khi đổi chiến lược, luôn chạy bộ câu hỏi đối chứng.

---

## 2. Phát hiện then chốt — CẢ HAI chế độ đều chỉ nạp lại tệp thực sự thay đổi

**Đã kiểm chứng 16/08/2026 — DEC-051.** Bằng chứng: `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`.

### Vòng test 3a — bằng chứng trực tiếp

Cấu hình: **Toàn bộ + Ghi đè + Mọi tệp**. Thao tác: **không sửa file nào cả**.

Kết quả: người dùng quan sát **"ghi đè không có hiệu lực"** — không thấy dấu hiệu re-ingest rõ ràng.

### Diễn giải

Connector vẫn dựa trên cơ chế **phát hiện thay đổi ở tầng nguồn** (hash hoặc mtime) trước khi quyết định tải lại — **kể cả khi chế độ đồng bộ đặt là "Toàn bộ"**.

> "Toàn bộ" nghĩa là *liệt kê lại toàn bộ tài nguyên đã chọn*, **không** đồng nghĩa với *bắt buộc re-ingest nội dung không đổi*.

Hệ quả thực tế: không có cách nào (đã biết) để ép re-ingest một file không đổi chỉ bằng cách đổi hai thiết lập này. Muốn ép nạp lại, phải làm file thực sự đổi ở nguồn, hoặc dùng **Phân tích lại** trên từng tài liệu trong KB.

**Phân loại:** cơ chế hash/mtime là **suy ra hợp lý**, không xác minh bằng log connector. Cái đã quan sát trực tiếp là *sync Toàn bộ trên dữ liệu không đổi thì không thấy hiệu lực*.

---

## 3. Kết quả ba vòng test Tăng dần vs Toàn bộ

KB test `Test` (`d7295a59-03b1-496c-86eb-9ecaa3364aa7`): `C.png`, `D.png`, `a.md` (nhúng ảnh C qua URI MinIO), `b.md` (nhúng ảnh D).

| Vòng | Ngày | Chế độ | Thao tác nguồn | Kết quả quan sát |
|---|---|---|---|---|
| 1 | 15/08 | Toàn bộ + Ghi đè | Sync lần đầu | 4 file **Hoàn tất** |
| 2 | 16/08 | **Tăng dần** + Ghi đè | Thêm đoạn văn vào `b.md`, giữ nguyên dòng ảnh D | Chỉ `b.md` re-ingest: nội dung mới đúng, thời gian tải lên cập nhật `Aug 16, 2026, 4:40:37 AM`. Ảnh D **vẫn hiển thị đúng** |
| 3a | 16/08 | **Toàn bộ** + Ghi đè | **Không sửa gì** | Không có hiệu lực re-ingest |
| 3b | 16/08 | **Toàn bộ** + Ghi đè | Thêm `e.md` mới; sửa nội dung `a.md` và `b.md`, giữ nguyên dòng ảnh cả hai | `e.md` ingest đủ pipeline (Phân tích tài liệu → Chia đoạn → Vector hóa → Đa phương thức → Hậu xử lý), tải lên `Aug 16, 2026, 5:05:44 AM`, KB tăng 4 → 5 tài liệu. `b.md` hiện đúng "Sửa lần 3". `C.png`/`D.png` vẫn nguyên, không bị xoá hay tạo trùng. Ảnh C và D **vẫn còn** |

### Kết luận

1. **Tăng dần** chỉ update tài liệu có thay đổi thực sự — đúng như kỳ vọng.
2. **Toàn bộ** cũng chỉ nạp lại tệp thực sự thay đổi — **trái với kỳ vọng thông thường**.
3. Sửa nội dung xung quanh một ảnh đã gắn URI MinIO **không làm mất link ảnh**, ở cả hai chế độ, kể cả khi ảnh và tài liệu cùng chung một KB (DEC-051).
4. File mới trong phạm vi sync được ingest bình thường.

### Giới hạn xác minh

Kế hoạch ban đầu là so sánh `knowledge_id` trước/sau để biết chắc connector có tạo lại tài liệu hay không. **Không thực hiện được**: MCP không truy cập được KB `Test` (`list_knowledge_bases` không thấy KB; tra thẳng bằng ID trả `not found or not accessible`) — có thể vì phạm vi KB đăng ký cho MCP server giới hạn ở KB production.

Toàn bộ kết luận trên dựa vào **quan sát UI**: nội dung xem trước, ảnh render, danh sách tài liệu, timestamp tải lên. Không có log hệ thống.

---

## 4. Connector KHÔNG tự resolve link ảnh tương đối

**Đã kiểm chứng 15/08/2026.**

Nội dung `b.md` sau khi ingest qua connector **vẫn còn nguyên**:

```markdown
![Ảnh test D](D.png)
```

Không đổi thành `minio://...`, dù `D.png` nằm cùng thư mục nguồn và cũng đã được ingest vào cùng KB.

**Hệ quả:** quy trình gắn URI thủ công (thu URI → ghi `image-map.json` → chạy `link_plan_v5_minio.py` hoặc tương đương) **vẫn cần thiết** cho nội dung đưa vào KB qua connector. Connector không làm việc này thay bạn.

Đây là kiểm chứng độc lập thứ ba cho sự thật ở mục 1 của [`KB-anh-va-uri-minio.md`](KB-anh-va-uri-minio.md).

---

## 5. Thiết lập kết nối — chuỗi đã kiểm chứng

**Đã kiểm chứng 07/08/2026** — `audit/audit-google-drive-connector-2026-08-07.md`.

1. Tạo hoặc chọn Google Cloud project dành cho connector.
2. **Bật Google Drive API** trong đúng project đó.
3. Tạo service account riêng; tạo key JSON ở tab **Keys** (key do Google sinh).
4. Chia sẻ đúng thư mục nguồn cho `client_email` của service account, quyền **Viewer**.
5. Trong Knowledge VNG: chọn Google Drive, dán **toàn bộ** service-account JSON; để trống Shared Drive ID nếu nguồn nằm ở My Drive.
6. **Kiểm tra kết nối** → chọn tài nguyên → cấu hình chiến lược → **Tạo & đồng bộ ngay**.

### Lỗi đã gặp thật

| Triệu chứng | Nguyên nhân gốc đã xác nhận | Cách sửa |
|---|---|---|
| `connection validation failed` ở bước Kiểm tra kết nối | Google Drive API chưa được bật trong project | Enable API. Connector đi tiếp ngay — **không cần tạo lại service account hoặc JSON key** |

---

## 6. Bước Tài nguyên

Quan sát được ngày 07/08/2026:

- Hiển thị cây thư mục và tệp mà service account có quyền đọc.
- Chọn được **một tệp riêng** hoặc **cả thư mục**. Chọn thư mục thì tệp mới thêm vào thư mục cũng thuộc phạm vi đồng bộ.
- **Dấu trừ màu cam** ở thư mục cha = chỉ một phần con được chọn.
- Mục có nhãn **Hiện chưa hỗ trợ** sẽ không được xử lý.

---

## 7. Bước Chiến lược — các nhóm cấu hình khác

### Lịch

Đơn vị: phút, giờ, hằng ngày, hằng tuần, hằng tháng.

Khuyến nghị `doc-12`: 15 phút để test; Giờ hoặc Hằng ngày cho phần lớn nguồn vận hành.

### Lọc tệp và tag

- Thêm được **nhiều regex** tên tệp; tệp khớp **một trong** các mẫu sẽ được đồng bộ.
- Để trống mẫu = nhận mọi tệp hợp lệ trong phạm vi đã chọn.
- Dùng `(?i)` để không phân biệt hoa/thường.
- Có **tag mặc định** và **rule gắn tag theo đường dẫn**; rule hỗ trợ capture từ regex.
- Sổ tay khuyến nghị: thử ít nhất một tên khớp và một tên không khớp trước production; rule theo đường dẫn chỉ dùng khi cấu trúc thư mục ổn định.

### Ghi đè xử lý (chunking cấp nguồn)

Giá trị `0` ở kích thước đoạn, độ chồng đoạn và giới hạn token = **dùng mặc định của KB**. Cùng nhóm còn có đoạn cha-con, ký tự phân tách và ngôn ngữ.

Khuyến nghị lượt đầu: giữ tất cả ở `0`, để trống ký tự phân tách.

### Đa phương thức và parser

Toggle quan sát được: đa phương thức ảnh (VLM), ASR, sinh câu hỏi, ép OCR toàn bộ PDF scanned.

Parser quan sát được ngày 07/08/2026 (**có thể đổi theo tenant**):

| Loại tệp | Parser |
|---|---|
| PDF, Word, PowerPoint | MinerU |
| Excel | Built-in; tự nhận diện hoặc thủ công |
| CSV, TXT, JSON | Simple |
| Markdown | Built-in |
| Ảnh | MinerU |
| Email, EPUB, HTML/HTM, MHTML, âm thanh | Built-in |

Khi chọn Excel **Thủ công**, tenant test hiển thị `Không dùng` và hai parser tiền tố `FPA`. **Đây là cấu hình riêng của tenant test, không phải mặc định chung của sản phẩm.** Không chọn parser tuỳ chỉnh chỉ vì tên nghe phù hợp — workbook phải đúng cấu trúc parser yêu cầu.

Lưu ý liên quan ảnh: parser ảnh là **MinerU**, chính là parser tách ảnh con gây ra hiện tượng "một ảnh nhiều URI" (mục 5 của [`KB-anh-va-uri-minio.md`](KB-anh-va-uri-minio.md)).

### Đồng bộ xóa

UI mô tả: bật control này sẽ **gỡ tri thức khi tệp nguồn đã bị xoá**.

Lượt 07/08/2026 **chỉ quan sát control, chưa thực hiện phép thử xoá đối chứng**. Sổ tay khuyến nghị: **tắt trong lượt thử đầu**; chỉ bật sau khi đã thử bằng tệp không quan trọng, có backup và xác nhận được cách phục hồi.

---

## 8. Xác nhận lượt đồng bộ thành công

Card nguồn dữ liệu sau khi tạo hiển thị: Trạng thái, Chế độ đồng bộ, Phạm vi, Lịch, Đồng bộ gần nhất, Kết quả.

Lượt đã kiểm chứng 07/08/2026: **Đã kết nối** · **Tăng dần** · **Một tệp** · **Mỗi 15 phút** · **Vừa xong** · **Thành công**.

Card báo Thành công **chưa đủ**. Sổ tay yêu cầu tiếp:

1. Mở Documents, xác nhận tài liệu đã xuất hiện.
2. Chờ trạng thái xử lý hoàn tất.
3. Mở chunk để kiểm tra nội dung parser.
4. Hỏi câu đúng, gần đúng, loại trừ và ngoài phạm vi.
5. **Kiểm tra nguồn truy hồi**, không chỉ đánh giá câu trả lời nghe hợp lý.

Pipeline ingest quan sát được (vòng test 3b, 16/08/2026): Phân tích tài liệu → Chia đoạn → Vector hóa → Đa phương thức → Hậu xử lý.

---

## 9. Cảnh báo bảo mật — phạm vi sync

**DEC-046, 15/08/2026.** Mỗi KB trỏ đúng **một** thư mục con của `knowledge/`:

| KB | Thư mục nguồn |
|---|---|
| `GS9 Knowledge VNG AI` | `knowledge/GS9 Knowledge VNG AI/` |
| `GS9 CFL Knowledge Agent` | `knowledge/GS9 CFL Knowledge Agent/` |
| `GS9 CFL Plan Version` | `knowledge/GS9 CFL Plan Version/` |
| `GS9 CFL Item Profile` | **không sync** |

> **TUYỆT ĐỐI không trỏ vào root project.**

Root project chứa `audit/`, `docs/`, `scripts/`, `tests/`, `.git/` và **service-account key** tại `knowledge/GS9 CFL Item Profile/keys CFL ItemID/keys/`. Không được để lọt vào phạm vi sync.

Quy tắc bảo mật khác (audit 07/08/2026):

- JSON key là secret. Không đưa vào Drive nguồn, KB, Markdown, ảnh chụp hoặc Git.
- Chỉ cấp **Viewer** cho đúng thư mục cần đồng bộ. Không chia sẻ toàn bộ My Drive.
- Không chọn thư mục `keys` hoặc bất kỳ vùng chứa credential nào ở bước Tài nguyên.

---

## 10. Chưa kiểm chứng

Danh sách này gộp backlog 07/08/2026, mục "Chưa được phép suy luận" của `doc-12`, và giới hạn còn lại sau ba vòng test 15–16/08/2026.

### Vòng đời tệp nguồn

- **Đổi tên tệp** trên Drive rồi sync — KB tạo tài liệu mới hay đổi tên bản cũ. DEC-046 ghi rõ hành vi đổi tên khi sync (135 file đổi tên trong phiên 15/08) **chưa được kiểm chứng trên nền tảng**; bắt buộc thử trên 2–3 file trước khi sync toàn bộ.
- **Di chuyển tệp** sang thư mục khác.
- **Xoá tệp** ở nguồn — kể cả hành vi của **Đồng bộ xóa** end-to-end. Chưa thử một lần nào.
- **Thu hồi quyền** của service account giữa chừng.

### Phạm vi và cấu hình

- **Shared Drive.** Mọi lượt test đều dùng My Drive, trường Shared Drive ID để trống. Không suy ra Shared Drive hành xử giống My Drive.
- **Regex lọc tệp, rule gắn tag, parser tuỳ chỉnh** đúng cho **mọi loại dữ liệu**. Mới quan sát giao diện, chưa chạy trên dữ liệu đối chứng có ca khớp và ca không khớp.
- **Parser tuỳ chỉnh của tenant** (nhóm `FPA`) — chưa chạy trên workbook thật.
- **Nhiều chu kỳ dài.** Ba vòng test là ba lần chạy thủ công trên 4–5 file. Chưa quan sát connector chạy theo lịch qua nhiều chu kỳ, chưa test drift của cursor Tăng dần.

### Liên quan ảnh

- **Sửa đúng dòng ảnh** trong Markdown rồi sync. Mọi vòng test đều cố ý giữ nguyên dòng ảnh.
- **Sửa nội dung/caption của chính tài liệu ảnh** (`C.png`/`D.png`) trong khi Markdown không đổi (DEC-051 ghi là case biên, ngoài phạm vi).
- **Ảnh nạp qua connector có sinh URI MinIO theo cùng cơ chế upload tay không** — chưa thu URI cho ảnh đến từ connector.

### Xác minh

- **Không đọc được `knowledge_id`** qua MCP cho KB test → mọi kết luận về "connector có tạo lại tài liệu hay không" là suy từ UI, không phải từ ID.
- **Cơ chế hash/mtime** ở mục 2 là suy luận, chưa có log connector xác nhận.

### Nguồn khác

- **Notion và NAS**, bước 3–4: chưa kiểm chứng.

---

## Nguồn

- `audit/audit-google-drive-connector-2026-08-07.md`
- `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md`
- `so-tay-tao-knowledge-base-v3.md`, khối `MODULE:doc-12-ket-noi-google-drive.md`
- `DECISIONS.md`: DEC-046, DEC-051
