# KB — Loại KB và chiến lược lập chỉ mục

Cơ chế chọn loại Knowledge Base (Tài liệu / FAQ), bật RAG / Wiki / Graph, và khác biệt giữa hai chế độ tạo Nhanh và Nâng cao.

**Nguồn bằng chứng chính**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| [`audit/audit-knowledge-vng-2026-08-06.md`](../../audit/audit-knowledge-vng-2026-08-06.md) | 06/08/2026 | Kiểm chứng live toàn bộ UI Knowledge Base trên tenant `10012` |
| [`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`](../../audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md) | 14/08/2026 | Baseline cấu hình một KB nghiệp vụ thật |
| [`audit/business-kb-readonly-audit-2026-08-14.md`](../../audit/business-kb-readonly-audit-2026-08-14.md) | 14/08/2026 | 9 KB nghiệp vụ: cấu hình, ACL, retention |
| `so-tay-tao-knowledge-base-v3.md` | — | Module `doc-00`, `doc-02`, `doc-03`, `doc-04` |

**Phạm vi quan sát:** toàn bộ khẳng định dưới đây quan sát trên tenant `10012`, giao diện `https://vnggames.ai/kb/knowledge`, nhãn **KNOWLEDGE BASE BETA**. Tenant khác có thể khác — đặc biệt danh sách model và parser tùy chỉnh.

---

## 1. Hai loại KB

Kiểm chứng 06/08/2026.

| | **Tài liệu** | **FAQ** |
|---|---|---|
| Đơn vị nội dung | File / nội dung soạn trực tuyến, được parse và chia chunk | Từng mục Q&A độc lập |
| Tab trong **Cài đặt** | Tổng quan, Mô hình, **Xử lý**, Chia sẻ, Nguồn dữ liệu | Tổng quan, Mô hình, Chia sẻ, Nguồn dữ liệu — **không có Xử lý** |
| Tab trang làm việc | Documents, Wiki, Graph | Documents, Wiki, Graph (Wiki/Graph là khung dùng chung, xem §4) |
| Cấu hình đặc thù | RAG / Wiki, parser, phân đoạn, VLM, ASR | Chế độ index câu hỏi, Gộp/Tách, Kiểm tra tìm kiếm, Nhập/Xuất |
| Công cụ đo chất lượng | Chat + xem nguồn truy hồi | **Kiểm tra tìm kiếm** (ngưỡng 0–1) + chat |

Vì FAQ không có tab **Xử lý**, mọi nội dung về parser và chunking chỉ áp cho KB Tài liệu. Xem [`KB-parser-va-xu-ly-file.md`](KB-parser-va-xu-ly-file.md) và [`KB-phan-doan-chunking-va-embedding.md`](KB-phan-doan-chunking-va-embedding.md).

### Chọn loại nào

| Tình huống | Chọn | Lý do |
|---|---|---|
| Hướng dẫn dài, SOP, chính sách, tài liệu dự án | Tài liệu | Cần parser, phân đoạn, truy hồi theo nội dung |
| Onboarding đọc theo chủ đề liên kết | Tài liệu + Wiki | Wiki tổng hợp thành trang có liên kết |
| Câu trả lời phải quản lý theo từng mục | FAQ | Mỗi Q&A là một đơn vị độc lập |
| Đã có sẵn bảng câu hỏi + biến thể + trả lời | FAQ | Nhập JSON / CSV / Excel |
| Vừa có quy định cứng vừa có tài liệu giải thích | Hai KB | FAQ giữ câu chuẩn; Tài liệu giữ bối cảnh |

---

## 2. Cái gì bị khóa và khi nào

Kiểm chứng 06/08/2026, xác nhận lại 14/08/2026 trên KB nghiệp vụ.

| Thiết lập | Trạng thái | Bằng chứng |
|---|---|---|
| **Loại KB** (Tài liệu / FAQ) | Khóa **ngay sau khi tạo** | Audit 06/08 §2 |
| **Chiến lược lập chỉ mục** (RAG / Wiki) | Khóa khi KB đã có nội dung | Audit 06/08 §2; audit nghiệp vụ 14/08 Phát hiện 4 |
| **Model Embedding** | Khóa khi KB đã có nội dung | Audit 06/08 §2 |
| **Chế độ index FAQ** (Chỉ câu hỏi / Câu hỏi + trả lời) | Banner nói khóa, **thực tế vẫn lưu được** | Audit 06/08 §8 |
| **Gộp / Tách** của FAQ | Banner nói khóa, **thực tế vẫn lưu được** | Audit 06/08 §8 |

**Cạm bẫy đã gặp thật — mâu thuẫn banner FAQ.** Banner trên KB FAQ đã có nội dung cảnh báo cấu hình lập chỉ mục bị khóa. Thao tác live 06/08/2026: chuyển `Chỉ câu hỏi` → `Câu hỏi + trả lời`, lưu thành công, mở lại giá trị được giữ; chuyển ngược về `Chỉ câu hỏi + Tách`, lưu thành công. Kết luận: **loại KB và Embedding thật sự khóa; hai control index FAQ thì không.** Đừng bắt người dùng xóa toàn bộ FAQ chỉ để đổi hai lựa chọn này — nhưng phải chạy lại **Kiểm tra tìm kiếm** sau mỗi lần đổi.

**Hệ quả thiết kế:** loại KB và Embedding là hai quyết định một chiều. Chốt chúng trên KB test trước khi nạp dữ liệu thật.

---

## 3. RAG và Wiki là hai checkbox độc lập

Kiểm chứng 06/08/2026.

Trong tab **Tổng quan** của KB Tài liệu, `RAG (vector + từ khóa)` và `Wiki` **không loại trừ nhau** — bật đồng thời được. Baseline KB thật `GS9 CFL Plan Version` (14/08/2026) bật cả hai.

| Nhu cầu | RAG | Wiki |
|---|---|---|
| Hỏi đáp nhanh, xem nguồn gốc | Phù hợp | Hỗ trợ gián tiếp |
| Đọc theo mục lục, hiểu bức tranh tổng | Không phải đầu ra chính | Phù hợp |
| Kiểm soát câu chữ gốc | Dễ đối chiếu đoạn nguồn | Nội dung **đã bị viết lại** |
| Phụ thuộc chất lượng nguồn | Cao | Rất cao (có bước tổng hợp lại) |

### Ba mức chi tiết Wiki

| Mức | Ghi chú |
|---|---|
| Tập trung | — |
| Tiêu chuẩn | Caption quan sát được: "Số trang cân bằng." Đây là **mô tả**, không phải ô nhập số trang |
| Toàn diện | Đã dùng trong phép thử Graph 06/08 |

Wiki trong trang làm việc có: **Mục lục**, **Nhật ký hoạt động**, xem theo **Thư mục** hoặc **Loại**, tạo thư mục, và liên kết `Mở trong Wiki` từ node Graph.

---

## 4. FAQ hiển thị Wiki/Graph nhưng không có chức năng thật

Kiểm chứng 06/08/2026.

KB FAQ vẫn hiện đủ ba tab `Documents / Wiki / Graph`. Bấm Wiki hoặc Graph chỉ nhận thông báo:

> Wiki chưa được bật. Bật Wiki trong cài đặt Knowledge Base (chiến lược lập chỉ mục) để tự động tổng hợp trang wiki từ tài liệu.

Nhưng **cấu hình FAQ không có control bật Wiki**. Đây là khung giao diện dùng chung giữa hai loại KB, không phải bằng chứng FAQ hỗ trợ Wiki/Graph. Không viết tài liệu hướng dẫn người dùng "bật Wiki cho FAQ".

---

## 5. Graph — năm loại node, hai loại chưa sinh được

Kiểm chứng 06/08/2026.

Chú giải Graph có: **Tóm tắt, Thực thể, Khái niệm, Tổng hợp, So sánh**.

| Mốc đo trong cùng ngày 06/08/2026 | Tổng | Tóm tắt | Thực thể | Khái niệm | Tổng hợp | So sánh |
|---|---:|---:|---:|---:|---:|---:|
| Sau khi nạp bộ Aurora/Borealis, Wiki = Toàn diện, chạy Phân tích lại | 93/93 | 9 | 42 | 41 | **0** | **0** |
| Lượt đối chiếu cuối ngày, sau khi các nguồn ảnh hoàn tất | 159/159 | 22 | 66 | 70 | **0** | **0** |

Hai kết luận tách bạch:

1. **Graph có cập nhật liên tục** — số node đổi từ 66 → 93 → 159 khi nguồn tiếp tục được xử lý. Con số cụ thể là ảnh chụp thời điểm, không phải giới hạn.
2. **Điều kiện sinh node Tổng hợp / So sánh: chưa xác định.** Cả khi đã có tài liệu so sánh trực tiếp hai hệ thống và Wiki ở mức Toàn diện, hai loại này vẫn bằng 0. Không tìm thấy thao tác tạo tay trong menu node hoặc canvas.

Không viết khẳng định kiểu "cứ có hai tài liệu liên quan là sinh node So sánh".

---

## 6. Chế độ Nhanh và Nâng cao

Kiểm chứng 06/08/2026.

| | **Nhanh** | **Nâng cao** |
|---|---|---|
| Trường hiển thị | Loại, Tên, Mô tả, Mô hình chat/tóm tắt, Mô hình Embedding | Toàn bộ tab cấu hình theo loại KB |
| RAG / Wiki | Ẩn, nhận cấu hình khuyến nghị | Hiển thị, chọn được |
| Parser, phân đoạn, VLM, ASR | Ẩn | Hiển thị |
| Cấu hình index FAQ | Ẩn | Hiển thị |
| Dùng khi | Tạo KB test nhanh | Cần kiểm soát đầy đủ từ đầu |

**Cạm bẫy đã gặp thật — banner tóm tắt nói sai.** Trong một phép thử tạo KB, banner của chế độ Nhanh ghi "sinh câu hỏi đang bật", nhưng mở cấu hình thật thì **Sinh câu hỏi** đang tắt. Đây là ca điển hình của DEC-022: banner là bản tóm tắt UI, trạng thái từng control trong **Cài đặt** mới là bằng chứng.

Dù dùng chế độ nào, luôn mở lại **Cài đặt** và chụp trạng thái từng tab trước khi nạp dữ liệu.

### Quy trình tạo an toàn

1. Tạo KB test bằng **Nâng cao**.
2. Chốt **loại KB** và **Embedding** — hai thứ khóa được.
3. Với Tài liệu: quyết định RAG, Wiki hoặc cả hai.
4. Với FAQ: chọn phạm vi index và cách xử lý biến thể câu hỏi.
5. Đặt tên có môi trường + mục đích, ví dụ `TEST - Payment FAQ - 2026Q3`.
6. Lưu, mở lại từng tab, chụp trạng thái.
7. Nạp một mẫu nhỏ đại diện, kiểm thử, rồi mới mở rộng.

---

## 7. Baseline một KB nghiệp vụ thật

Đọc read-only ngày 14/08/2026 trên KB `GS9 CFL Plan Version`, ID `1452bc9a-c8b4-487b-b623-34e0b00a83e9`, tenant `10012`. Mọi dialog đóng bằng **Hủy**, không lưu.

| Thiết lập | Giá trị |
|---|---|
| Loại | `Tài liệu` |
| Chiến lược lập chỉ mục | `RAG (vector + từ khóa)` **và** `Wiki` — cùng bật |
| Model chat / tóm tắt | `deepseek-v4-flash` |
| Model Embedding | `text-embedding-3-large` |
| Model tổng hợp Wiki | `deepseek-v4-flash` |
| Parser Hình ảnh (`.jpg .jpeg .png .gif .bmp .tiff .webp`) | `MinerU` |
| Số tài liệu tại thời điểm đọc | 0 |

**Cảnh báo model.** Danh sách model có thể đổi, và **có model hiện trong dropdown nhưng backend không chấp nhận**. Bằng chứng 06/08/2026: `deepseek-v4-flash` chọn được trong UI của KB FAQ nhưng lưu thất bại với lỗi `LLM model not found`; KB FAQ test phải chuyển sang `qwen3.6-plus` để tiếp tục.

**Mâu thuẫn nguồn cần lưu ý:** cùng tên model `deepseek-v4-flash` bị backend từ chối ở KB **FAQ** ngày 06/08/2026, nhưng lại là giá trị đang lưu của KB **Tài liệu** `GS9 CFL Plan Version` ngày 14/08/2026.

Manh mối một phần từ bản master lưu trữ trước 06/08/2026 (`audit/archive/...-truoc-audit-2026-08-06.md` §8.2): **số model của vai trò Chat/tóm tắt dao động 3↔4 giữa các lần mở modal**, `deepseek-v4-flash` có/không tùy lần. Nguyên nhân chưa rõ — có thể là rollout dần, có thể là lỗi tải danh sách.

Điều đó **không giải thích** vì sao lưu thất bại với lỗi `LLM model not found`, và cũng không chứng minh model này đã ổn định vào 14/08. Không suy diễn. Quy tắc thực dụng: nếu không thấy model mong muốn thì tải lại trang trước khi báo lỗi; chỉ chọn model **đã lưu được trong chính KB đó** và ghi ngày kiểm tra.

---

## 8. Không có control retention ở cấp KB

Kiểm chứng 14/08/2026 (audit KB nghiệp vụ, Phát hiện 4).

Dialog `Cấu hình Knowledge Base → Tổng quan` chỉ có: `Loại`, `Chiến lược lập chỉ mục`, `Tên`, `Mô tả`. **Không có TTL, expiry, retention hay auto-purge.**

Hệ quả: dữ liệu tồn tại vô hạn tới khi xóa thủ công. Yêu cầu retention không thể đáp ứng bằng cấu hình — phải xử lý bằng quy ước vận hành có ngày và rà soát định kỳ.

---

## 9. Ranh giới KB — vẽ trước khi bind

DEC-036 (15/08/2026): quy hoạch KB theo bản đồ 7 tầng phải đi **trước** việc bind KB cho Agent. Ranh giới KB vẽ theo **(mức nhạy cảm × đối tượng đọc × nhịp cập nhật)**, không theo nguồn dữ liệu.

Các quyết định liên quan đã chốt:

| DEC | Ngày | Nội dung áp cho loại/ranh giới KB |
|---|---|---|
| DEC-037 | 15/08 | **Không đổi tên KB đang chạy trên Web.** Mỗi KB có một dòng "bản chất" ghi vai trò thật; tên mới chỉ áp cho KB tạo mới |
| DEC-038 | 15/08 | `GS9 CFL Kho Dữ Liệu Tổng Hợp` là **KB dẫn xuất có chủ đích** (gom nhiều KB lẻ để xem Wiki/Graph toàn cảnh), không phải trùng lặp nhầm. **Không Agent nào được bind đồng thời KB tổng hợp và KB lẻ cấu thành nó** |
| DEC-043 | 15/08 | Gộp ảnh + tài liệu vào **cùng một KB** (bỏ khái niệm asset host riêng ở mức local) |
| DEC-051 | 16/08 | DEC-043 được xác nhận đúng bằng thực nghiệm 3 vòng sync Google Drive: ảnh vẫn sống khi tài liệu khác được sửa và re-ingest, ở **cả** chế độ Tăng dần và Toàn bộ |

**Lý do kỹ thuật của DEC-051 là suy ra, không xác minh bằng log connector:** link ảnh nhúng là URI MinIO tĩnh, không phải tham chiếu động vào document ảnh trong KB. Kết luận dựa trên quan sát UI, không phải log hệ thống.

---

## 10. Chưa kiểm chứng

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| Điều kiện sinh node **Tổng hợp** và **So sánh** trong Graph | Chưa xác định | Đã thử tài liệu so sánh trực tiếp + Wiki Toàn diện, vẫn 0/0 (06/08/2026) |
| Cấu hình **mặc định** của một KB trắng mới tạo | Chưa xác định | Mọi giá trị ghi trong tài liệu này là trạng thái KB đã có nội dung, không phải mặc định sản phẩm |
| Khác biệt giữa **Tập trung / Tiêu chuẩn / Toàn diện** ở đầu ra thật | Chưa xác định | Chỉ quan sát caption UI và một lượt đổi Tiêu chuẩn → Toàn diện |
| Vì sao `deepseek-v4-flash` lưu lỗi ở FAQ (06/08) nhưng đang chạy ở KB Tài liệu (14/08) | Chưa xác định | Hai nguồn khác ngày, khác loại KB; không đủ dữ liệu để kết luận |
| Chuyện gì xảy ra khi **bật Wiki sau** khi KB đã có nội dung | Chưa xác định | Control bị khóa khi có nội dung; chưa test đường xóa hết nội dung rồi bật lại |
| Policy retention ở **cấp tenant** | Bị chặn | Cấp KB đã xác nhận không có; cấp tenant không đọc được (14/08/2026) |
| Có phải mọi tenant đều thấy cùng bộ chiến lược index này | Chưa xác định | Toàn bộ quan sát nằm trên tenant `10012` |
