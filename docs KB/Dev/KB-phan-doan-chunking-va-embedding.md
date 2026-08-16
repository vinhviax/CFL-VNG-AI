# KB — Phân đoạn (chunking) và embedding

Bốn chiến lược phân đoạn, chế độ cha-con, các tham số thật, model embedding, và kết quả benchmark đã chạy.

**Nguồn bằng chứng chính**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| [`audit/audit-knowledge-vng-2026-08-06.md`](../../audit/audit-knowledge-vng-2026-08-06.md) §6, §9 | 06/08/2026 | Trạng thái phân đoạn của KB test; phép thử Phân tích lại và Sửa nội dung |
| [`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`](../../audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md) | 14/08/2026 | Embedding `text-embedding-3-large` trên KB thật |
| [`audit/business-kb-readonly-audit-2026-08-14.md`](../../audit/business-kb-readonly-audit-2026-08-14.md) Phát hiện 5 | 14/08/2026 | Hai KB nghiệp vụ dùng hai embedding model khác nhau |
| `so-tay-tao-knowledge-base-v3.md` | — | Module `doc-07`, `doc-08`, `doc-09` |
| [`audit/archive/so-tay-tao-knowledge-base-v3-truoc-audit-2026-08-06.md`](../../audit/archive/so-tay-tao-knowledge-base-v3-truoc-audit-2026-08-06.md) §10, §8.2, §12, §13.3 | trước 06/08/2026 | **Bản master lưu trữ, đã bị thay thế.** Chứa các con số khoảng/mặc định và benchmark chiến lược mà master hiện hành không lặp lại |

**Cách đọc nguồn archive.** Bản archive là master **trước** đợt audit 06/08/2026 và mang hệ nhãn bằng chứng riêng (`[TT]` quan sát trực tiếp, `[Ảnh]`, `[NSD]` người dùng tự chạy). Một số khẳng định trong đó **đã bị audit 06/08 đính chính** (ví dụ: PPT/PPTX có Built-in — sai). Mọi mục lấy từ archive trong file này được đánh dấu **(archive)** và giữ ở mức *Có điều kiện* cho tới khi có lượt kiểm chứng mới.

**Phạm vi quan sát:** tenant `10012`.

---

## 1. Chunk là gì trong hệ thống này

Chunk (phân đoạn) là đơn vị nội dung dùng cho tìm kiếm và embedding. Mục **Phân đoạn** nằm ở tab **Cài đặt → Xử lý**, mô tả trên UI: *"Điều khiển cách chia tài liệu trước khi embedding."* **Chỉ có ở loại Tài liệu** — FAQ không có tab Xử lý.

Chunk quá lớn mang nhiều chủ đề. Chunk quá nhỏ mất điều kiện và ngoại lệ. Không có cấu hình tốt tuyệt đối — phụ thuộc cấu trúc nguồn và dạng câu hỏi.

**Đơn vị luôn là KÝ TỰ, không phải TỪ** (archive §10.4). Mọi tài liệu nội bộ cũ ghi "200–500 từ" là sai cả đơn vị lẫn giá trị.

---

## 2. Bốn chiến lược phân đoạn (archive)

Mô tả nguyên văn trên UI:

| Chiến lược | Mô tả trên tool |
|---|---|
| **Tự động** (mặc định) | "Bộ phân tích chọn giữa chia theo tiêu đề, theo cấu trúc và theo độ dài cho mỗi tài liệu." |
| **Theo tiêu đề** | "Chia tại ranh giới tiêu đề Markdown; mỗi đoạn mang theo đường dẫn tiêu đề. Tốt cho Markdown có cấu trúc." |
| **Theo cấu trúc** | "Chia theo dấu hiệu cấu trúc: ngắt trang, mục đánh số, dấu hiệu chương, tiêu đề viết hoa. Lý tưởng cho PDF không có tiêu đề Markdown." |
| **Theo độ dài** | "Bỏ qua cấu trúc; chia đệ quy theo số ký tự và dấu phân tách — hành vi gốc." |

KB test trong audit 06/08/2026 đang ở **Tự động**.

### Benchmark đã chạy — đừng tin mô tả (archive §10.3)

Test trên 4 văn bản mẫu của công cụ **Xem trước phân đoạn**:

| Văn bản mẫu | Cấu trúc thật | Theo tiêu đề | Theo cấu trúc |
|---|---|---|---|
| Tài liệu Markdown | 5 heading `#`/`##`/`###` | **3 đoạn** — tách đúng | 1 đoạn (bỏ qua cả 5 heading) |
| Danh sách FAQ | Cặp `Q:`/`A:` | 1 đoạn (gộp 3 câu khác chủ đề) | 1 đoạn |
| Chương PDF | `CHAPTER ONE/TWO/THREE` viết hoa | 1 đoạn | **1 đoạn — mâu thuẫn mô tả** |
| Văn xuôi | Không có gì | 1 đoạn (hợp lý) | 1 đoạn (hợp lý) |

Hai kết luận:

1. **"Theo tiêu đề" chỉ hiểu cú pháp `#`/`##` Markdown.** Không suy rộng ra dấu hiệu heading mà mắt người nhận ra (CHAPTER X viết hoa, cặp Q/A).
2. **"Theo cấu trúc" thất bại ngay trên đúng loại dấu hiệu nó tuyên bố hỗ trợ.** Test bổ sung với văn bản chứa 4 kiểu dấu hiệu cùng lúc (`1.`, `2.`, `Chương 3:`, `PHẦN BỐN:`) cho **0 dấu hiệu chương, 0 ngắt trang, 0 tiêu đề MD**, gộp 1 đoạn.

**Kiểm chứng trên file thật, không phải sandbox:** người dùng tự tạo KB `Test PDF cấu trúc`, tải lên PDF thật 4 trang có ngắt trang thật, font Unicode chuẩn, chứa đủ 4 kiểu dấu hiệu, đặt Chiến lược = **Theo cấu trúc**. Kết quả engine sản xuất: **tổng 1 phân đoạn**. Cả 4 phần nằm chung một đoạn.

Đây là **hạn chế (hoặc bug) thật của chiến lược**, không phải giới hạn của công cụ preview.

*Giới hạn của kết luận:* mới test 1 file PDF dựng bằng reportlab — có thể thiếu metadata/outline/font-hint. Dữ liệu cùng hướng: một báo cáo PDF nghiệp vụ thật 79 trang (`CFL MMR GMT 2026.04.pdf`, KB dùng chiến lược **Tự động**) chỉ ra **2 phân đoạn**, đoạn 1 chiếm **68/79 trang**.

### "Theo độ dài" hoạt động đúng thiết kế (archive)

Test trên văn xuôi tiếng Việt 14.746 ký tự, chế độ Cha-con:

- Ngôn ngữ tự nhận diện: `vi` — xác nhận để trống **Gợi ý ngôn ngữ** vẫn nhận đúng tiếng Việt.
- Kết quả: 2 đoạn con — #0 = **8.192 ký tự** (kịch trần ngưỡng con), #1 = 6.554 ký tự (`14.746 − 8.192`, khớp chính xác).

**Hệ quả cần biết:** ranh giới đoạn rơi **giữa một câu**. Số ký tự tuyệt đối được ưu tiên trước; **Dấu phân tách chỉ là tham khảo phụ**. Chế độ Cha-con giảm nhẹ tác động vì đoạn cha vẫn được trả về kèm; chế độ Thông thường mất ngữ cảnh rõ hơn.

---

## 3. Cha-con và Thông thường

Hai chế độ cấu trúc, **độc lập** với 4 chiến lược ở §2 — kết hợp tự do. Cùng cặp số Cha-con xuất hiện y hệt bất kể đang chọn chiến lược nào (archive §10.4).

### Chế độ Cha-con (archive: là mặc định ở cả Nhanh và Nâng cao)

| Thông số | Khoảng | Mặc định |
|---|---|---|
| Kích thước đoạn **cha** | 512 – 32.768 ký tự | **32.768** |
| Kích thước đoạn **con** | 64 – 8.192 ký tự | **8.192** |
| Chồng lấp cha | 0 – 4.096 ký tự | **0** (0 = dùng độ chồng lấp chính) |
| Chồng lấp con | 0 – 2.048 ký tự | **0** (0 ≈ 20% kích thước đoạn con) |

### Chế độ Thông thường (archive)

| Thông số | Khoảng | Mặc định |
|---|---|---|
| Kích thước đoạn | 128 – 16.384 ký tự | **16.384** |
| Độ chồng lấp | 0 – 4.096 ký tự | **0** |

### Cơ chế

- **Chunk con** khớp chính xác phần nhỏ có từ ngữ liên quan → dùng cho tìm kiếm/embedding.
- **Chunk cha** được trả về kèm để câu trả lời có ngữ cảnh rộng hơn.

Lợi ích chỉ có thật khi chunk cha chứa **đúng** ngữ cảnh của chunk con. Nếu một file trộn nhiều chủ đề trong cùng section, tăng kích thước cha chỉ kéo thêm nhiễu.

---

## 4. Trạng thái quan sát được trên KB test

Kiểm chứng **06/08/2026**, KB `Test Doc RAG+Wiki` (`8902e4d0-4884-4be7-a54b-1d193bf8506a`), tenant `10012`.

| Thiết lập | Giá trị quan sát |
|---|---|
| Chiến lược | Tự động |
| Chế độ | Cha-con |
| Kích thước cha | 32.768 ký tự |
| Kích thước con | 8.192 ký tự |
| Chồng lấp cha / con | 0 / 0 |
| Truy hồi theo ngữ cảnh | **Bật** |
| Sinh câu hỏi | **Tắt** |
| Giới hạn token | 0 |
| Dấu phân cách | dòng trống, dòng mới, `。`, `！`, `？`, `;`, `；` |
| Gợi ý ngôn ngữ | Có nút **DE / EN / ZH**; ô để trống |

**Cảnh báo bắt buộc.** Đây là **trạng thái hiện hữu của một KB test**, không phải mặc định sản phẩm. Audit 06/08 ghi rõ: không được viết thành mặc định nếu chưa tạo KB trắng đối chứng. Bản archive **có** khẳng định đây là mặc định — nhưng đó là nguồn đã bị thay thế, giữ ở mức *Có điều kiện*.

Lưu ý KB này đã bị người dùng xóa (DEC-017). ID trên chỉ là bằng chứng lịch sử, không dùng làm dependency hay đích mutation.

---

## 5. Tùy chọn nâng cao của Phân đoạn

| Tùy chọn | Mô tả trên UI (archive) | Trạng thái KB test 06/08 |
|---|---|---|
| **Truy hồi theo ngữ cảnh** | "Thêm tiêu đề ngữ cảnh do LLM viết vào mỗi đoạn để cải thiện truy hồi." | Bật |
| **Giới hạn token** | Khoảng 0–8192; `0` = tắt | 0 |
| **Dấu phân tách** | "Ký tự mà bộ chia ưu tiên khi cắt. Dấu ưu tiên cao được thử trước." | 7 dấu, xem §4 |
| **Sinh câu hỏi** | Khi bật hiện thêm **Số câu hỏi mỗi đoạn**, khoảng 1–10, giá trị khi bật lần đầu = 3 | Tắt |
| **Gợi ý ngôn ngữ** | Ba nút DE / EN / ZH. Để trống = tự nhận diện | Để trống |

**Truy hồi theo ngữ cảnh chạy thật, không chỉ là mô tả UI.** Bằng chứng trực quan (archive §13.3): mở chi tiết tài liệu → **Xem phân đoạn**, mỗi đoạn có khối **"Ngữ cảnh tìm kiếm (LLM tạo)"** ở đầu.

### Ràng buộc đã ghi nhận (archive §10.6)

Khi **Chiến lược = Theo độ dài**, hai trường bị **vô hiệu hóa**: **Giới hạn token** và **Gợi ý ngôn ngữ**. Nghĩa là cần một trong hai thì không thể đồng thời dùng "Theo độ dài" — phải đổi sang Tự động / Theo tiêu đề / Theo cấu trúc.

### Ba điểm cho nội dung tiếng Việt

1. Bộ dấu phân tách nghiêng về ngữ pháp CJK (có `。`, `！`, `？`, `；`). Với tiếng Việt, `\n\n`, `\n`, `.`, `!`, `?`, `;` dùng bình thường.
2. **Gợi ý ngôn ngữ không có nút Tiếng Việt** — chỉ DE/EN/ZH.
3. Để trống là lựa chọn đúng: đã đo, tool nhận diện đúng `vi` trên văn bản 14.746 ký tự.

---

## 6. Công cụ Xem trước phân đoạn có giới hạn nghiêm trọng

(archive §10.2) Nút **Xem trước phân đoạn** có ở mọi chiến lược, mở modal với 4 văn bản mẫu dựng sẵn: **Tài liệu Markdown · Danh sách FAQ · Chương PDF · Văn xuôi**.

Kết quả hiện 2 lớp:

- **Thống kê tổng:** số dòng, số ký tự, số tiêu đề Markdown, số ngắt trang, số dấu hiệu chương, ngôn ngữ tự nhận diện, và dòng `N đoạn · Ø trung bình · σ độ lệch chuẩn · min · max` (đơn vị ký tự).
- **Từng đoạn:** số thứ tự, số ký tự, số token ước lượng, khoảng vị trí trong văn bản gốc, đường dẫn tiêu đề (breadcrumb), nội dung đầy đủ.

**Giới hạn:** công cụ này **chỉ chạy trên văn bản dán tay hoặc 4 mẫu có sẵn — không đọc được file đã tải lên KB.** Muốn biết file thật bị cắt thế nào, phải tải lên rồi mở chi tiết tài liệu → **Xem phân đoạn**.

---

## 7. Ghi đè phân đoạn ở ba cấp

| Cấp | Vị trí | Ghi chú |
|---|---|---|
| KB | Cài đặt → Xử lý → Phân đoạn | Áp cho tài liệu nạp sau; tài liệu cũ cần **Phân tích lại** |
| Lượt tải | Modal Tải tài liệu lên → **Xử lý nâng cao** | Bộ tham số giống hệt cấp KB. UI ghi: *"Ghi đè mặc định của KB cho lần tải này. Để 0 / để trống dùng mặc định KB."* |
| Nguồn ngoài | Wizard nguồn dữ liệu → bước Chiến lược | Ghi đè kích thước đoạn, độ chồng, giới hạn token, đoạn cha-con, ký tự phân tách, ngôn ngữ (07/08/2026) |

Khuyến nghị: giữ `0` / để trống ở lượt đầu để kế thừa cấu hình KB. Chỉ ghi đè khi đã có bộ câu hỏi đối chứng.

*Chi tiết đáng ngờ (archive §10.7):* ô "Ngôn ngữ" ở cấp lượt tải có placeholder `vd: en, vi` — khác với "Gợi ý ngôn ngữ" cấp KB (chỉ 3 nút DE/EN/ZH). Chưa test `vi` gõ tay có hoạt động không.

---

## 8. Cấu hình phân đoạn KHÔNG bị khóa

Khác với loại KB và Embedding. Bảng khóa đầy đủ nằm ở [`KB-loai-kb-va-chien-luoc-index.md`](KB-loai-kb-va-chien-luoc-index.md) §2. Riêng cho chunking:

| Cấu hình | Khi KB đã có nội dung |
|---|---|
| Parser / Phân đoạn (tab Xử lý) | **Không khóa** — đổi được, áp cho tài liệu nạp sau hoặc dùng Phân tích lại |
| Mô hình chat / tóm tắt | **Không khóa** |
| Mô hình Embedding | **Khóa** |

(archive §12) Banner khóa ghi *"Hãy xóa tài liệu để thay đổi"* — nghĩa là khóa **có điều kiện**, không vĩnh viễn. Xóa hết nội dung đã lập chỉ mục thì mở lại được. Đây là suy đọc từ chữ trên banner; **chưa ai chạy thử đường xóa-hết-rồi-đổi trên tenant này**.

---

## 9. Phân tích lại vs Sửa nội dung + Xuất bản

Hai thao tác này cho kết quả khác nhau. Cả hai kiểm chứng 06/08/2026.

| | **Phân tích lại** | **Sửa nội dung + Xuất bản** (tài liệu MANUAL) |
|---|---|---|
| Tài liệu thử | `03-so-sanh-aurora-borealis.md` | `Test soạn thảo trực tuyến.md` |
| Chuỗi trạng thái | Chờ xử lý → Đang hoàn tất → Hoàn tất | Chờ xử lý → Đang hoàn tất → Hoàn tất |
| Số chunk trước → sau | 1 → **1** (không đổi) | 3 → **4** (thêm marker), rồi phục hồi nội dung gốc → **3** |
| Tóm tắt | Sinh lại, **đổi cách diễn đạt** | Chứa marker mới |
| Thời gian tải lên | Không đổi | — |

**Kết luận:** Phân tích lại tái chạy pipeline và tái sinh tóm tắt, nhưng **không bảo đảm số chunk thay đổi** nếu cấu hình hoặc nội dung không tạo ranh giới khác. Trong phép thử đó, thay đổi duy nhất là độ chi tiết Wiki (Tiêu chuẩn → Toàn diện) — thứ không ảnh hưởng ranh giới chunk.

Ngược lại, **Sửa nội dung + Xuất bản thực sự kích hoạt lập chỉ mục lại** và số chunk phản ứng theo nội dung — cả chiều tăng lẫn chiều giảm.

Muốn đánh giá thay đổi: ghi ảnh hoặc số liệu trước/sau. Đừng dựa vào cảm giác.

---

## 10. Năm giai đoạn của pipeline xử lý (archive §13.3)

Mở chi tiết một tài liệu đang xử lý có khối **"Tiến trình xử lý"** với tiến độ real-time:

| # | Giai đoạn | Thời gian mẫu quan sát được |
|---|---|---|
| 1 | Chia đoạn (chunking) | 8ms |
| 2 | Vector hóa (embedding) | 1.8s |
| 3 | Đa phương thức (xử lý ảnh) | 1.2s |
| 4 | Hậu xử lý | 11ms |
| 5 | Phân tích tài liệu | chạy sau cùng |

Việc "Phân tích tài liệu" chạy sau cùng và nhiều khả năng phục vụ Wiki (tóm tắt + trích thực thể) là **suy luận từ thứ tự quan sát**, chưa xác nhận với đội phát triển.

Ý nghĩa vận hành: embedding chỉ là **một trong năm** giai đoạn. Một tài liệu đứng lâu ở "Đang hoàn tất" không nhất thiết đang kẹt ở embedding.

---

## 11. Model Embedding

### Pool model quan sát được (archive §8.2)

| Vai trò | Model |
|---|---|
| Embedding | `text-embedding-3-large` · `text-embedding-3-small` · `qwen3-embed-8b` |
| Chat / tóm tắt · Tổng hợp Wiki | `qwen3.6-plus` · `gpt-oss-120b` · `hosted_vllm/qwen3.6-35b` · `deepseek-v4-flash` (không phải lúc nào cũng có) |
| VLM | `qwen3.6-plus` · `gpt-oss-120b` · `hosted_vllm/qwen3.6-35b` — **không có** `deepseek-v4-flash` |

Doc và FAQ dùng chung pool model cho Chat/tóm tắt + Embedding. Khác biệt duy nhất: Doc có thêm vai trò thứ ba (Tổng hợp Wiki).

### Cảnh báo bắt buộc — danh sách model không ổn định

Ba tầng cảnh báo, cả ba đều có bằng chứng:

1. **Số model dao động giữa các lần mở** (archive §8.2). Vai trò Chat/tóm tắt lúc thấy 4 model, lúc chỉ 3 — `deepseek-v4-flash` có/không tùy lần mở. Nguyên nhân chưa rõ; có thể là rollout dần hoặc lỗi tải danh sách. Vận hành: nếu không thấy model mong muốn, **tải lại trang / mở lại modal trước khi báo lỗi**.
2. **Có model hiện trong dropdown nhưng backend không chấp nhận.** 06/08/2026: `deepseek-v4-flash` chọn được ở KB FAQ nhưng lưu thất bại với lỗi `LLM model not found`. KB FAQ test phải chuyển sang `qwen3.6-plus`.
3. **Danh sách có thể đổi bất cứ lúc nào.** Không viết quy trình hay code phụ thuộc vĩnh viễn vào một tên model. Chọn model **đang lưu được trong chính KB đó**, ghi ngày kiểm tra.

### Embedding trên KB thật

| KB | Embedding | Ngày | Nguồn |
|---|---|---|---|
| `GS9 CFL Plan Version` (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`) | `text-embedding-3-large` | 14/08/2026 | Audit CFL Plan V5 |
| `GS9 CFL Item Profile` | model id `3b3d08c9-9c57-49fe-a639-9ca73846fa10` | 14/08/2026 | Audit KB nghiệp vụ |
| `GS9 CFL Data Daily`, `GS9 CFL PUM`, `GS9 CFL Kho Dữ Liệu Tổng Hợp` | model id `56b60566-a978-49da-9372-588ad12dc5d6` | 14/08/2026 | Audit KB nghiệp vụ |

**Hai KB nghiệp vụ đang dùng hai embedding model khác nhau.** Phải tính tới điều này khi so sánh chất lượng retrieval giữa các KB — kết quả không so sánh trực tiếp được.

MCP `list_documents` / metadata KB trả về **UUID model**, không phải tên model. Chưa có bảng ánh xạ UUID → tên trong project.

### Vì sao Embedding phải chốt trước

Đổi embedding = đổi toàn bộ không gian vector = phải lập chỉ mục lại toàn bộ nội dung. Đó là lý do UI khóa trường này khi KB đã có nội dung. Chốt bằng KB test trước khi nạp dữ liệu lớn.

---

## 12. Đo ảnh hưởng của phân đoạn bằng truy hồi thật

Không kết luận chiến lược nào "tốt nhất" chỉ bằng preview. Với mỗi cấu hình, đo:

- Số chunk được tạo.
- Heading / đường dẫn cấu trúc đi cùng chunk.
- Chunk chứa điều kiện, ngoại lệ và kết quả có bị tách không.
- Câu hỏi diễn đạt khác từ nguồn có truy hồi đúng không.
- Câu gần giống nhưng ngoài phạm vi có bị kéo nhầm không.

### Bộ câu hỏi kiểm thử chunk cho mỗi tài liệu

1. Câu có đáp án nằm trọn trong một mục.
2. Câu cần ghép điều kiện và ngoại lệ trong cùng mục.
3. Câu cần liên kết hai mục xa nhau.
4. Câu dùng từ đồng nghĩa, không trùng từ nguồn.
5. Câu cùng từ khóa nhưng khác phạm vi.

**Xem phần nguồn truy hồi trước khi đánh giá văn phong câu trả lời.** Chi tiết quy trình ở [`KB-van-hanh-chat-va-truy-hoi.md`](KB-van-hanh-chat-va-truy-hoi.md).

---

## 13. Chưa kiểm chứng

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| Cấu hình phân đoạn **mặc định** của KB trắng mới tạo | Chưa xác định | Archive khẳng định Cha-con 32.768/8.192/0/0 là mặc định; audit 06/08 từ chối kết luận này khi chưa có KB trắng đối chứng |
| Hành vi khi văn bản **vượt ngưỡng cha** (>32.768 ký tự) | Chưa xác định | Đoạn cha có cắt cứng tương tự đoạn con không |
| "Theo cấu trúc" có hoạt động trên PDF nghiệp vụ thật xuất từ Word không | Có điều kiện | Mới test 1 PDF dựng bằng reportlab; kết quả 1 đoạn |
| Ảnh hưởng của "Theo độ dài" lên **Truy hồi theo ngữ cảnh**, **Dấu phân tách**, **Sinh câu hỏi** | Chưa xác định | Chỉ xác nhận Giới hạn token và Gợi ý ngôn ngữ bị vô hiệu hóa |
| Ô "Ngôn ngữ" cấp lượt tải có nhận `vi` gõ tay không | Chưa xác định | Placeholder gợi ý `vd: en, vi` nhưng chưa test |
| Đổi cấu hình phân đoạn rồi Phân tích lại có thực sự đổi số chunk không | Chưa xác định | Phép thử 06/08 chỉ đổi độ chi tiết Wiki, không đổi tham số chunk |
| Xóa hết tài liệu có mở khóa lại Embedding không | Chưa xác định | Chỉ đọc được chữ trên banner (archive §12) |
| Ánh xạ UUID embedding model → tên model | Chưa xác định | Metadata KB nghiệp vụ chỉ trả UUID (14/08/2026) |
| Chất lượng retrieval giữa `text-embedding-3-large`, `-small`, `qwen3-embed-8b` | Chưa xác định | Chưa có lượt A/B nào |
| Có phải mọi tenant thấy cùng pool embedding này | Chưa xác định | Toàn bộ quan sát trên tenant `10012` |
