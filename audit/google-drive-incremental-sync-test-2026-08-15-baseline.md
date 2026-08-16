# Baseline test đồng bộ "Tăng dần" — KB `Test`

**Ngày:** 15/08/2026 · **KB ID:** `d7295a59-03b1-496c-86eb-9ecaa3364aa7`
**Trạng thái:** Sau lượt sync đầu tiên (Toàn bộ + Ghi đè + Mọi tệp), cả 4 file `Hoàn tất`.

## Mốc trước khi sync tăng dần

| File | `knowledge_id` (document ID trong KB) | Ghi chú |
|---|---|---|
| `C.png` | `aa308f81-fa83-4098-bac0-235c0fbe5ec9` | Tóm tắt tự sinh chứa 2 URI MinIO (xem dưới) |
| `D.png` | `2852c79a-e3c0-4393-ae78-16db25650541` | Tóm tắt không lộ URI trực tiếp |
| `a.md` | `4b48546d-6fd4-4ee9-bbb8-19362fd17c53` | Không đổi trong suốt bài test |
| `b.md` | `136f2601-cf49-4898-99d5-bb8b8f1bb7e8` | Sẽ sửa nội dung (không đổi link ảnh) ở vòng test tăng dần |

## URI MinIO của `C.png` (2 URI — giống hiện tượng MinerU tách ảnh con ở Plan V5)

- `minio://knowledge-base-prd/10012/exports/13b88b2e-a43d-485a-b255-173d37a476cf.png` ← người dùng đã chọn URI này gắn vào `a.md`
- `minio://knowledge-base-prd/10012/exports/9b816769-9333-46ac-9694-48e7971939c8.jpg`

## URI MinIO của `D.png` (người dùng tự lấy qua UI, agent không tìm được qua caption)

- `minio://knowledge-base-prd/10012/exports/9aa0a0d8-0905-43ef-b7d1-7da9f23f1c68.png` ← đã gắn vào `b.md`

## MỚI — vòng test 2: `a.md` và `b.md` đã gắn URI thật (không còn link tương đối)

Người dùng đã tự sửa `a.md`/`b.md` để nhúng URI MinIO thật (thay vì `C.png`/`D.png` tương đối) — đúng cú pháp chuẩn `<!-- LOCAL_ASSET: ... --> + minio://...`. Agent đã sửa phần văn xuôi của cả 2 file (không đụng dòng ảnh):

- `a.md` = nhóm **đối chứng** (không sửa gì thêm sau vòng này) — ảnh C.
- `b.md` = nhóm **thử nghiệm** (sửa nội dung xung quanh, giữ nguyên dòng ảnh) — ảnh D.

**Mục tiêu vòng test này:** xác định gộp ảnh + tài liệu chung một KB (kiến trúc đã chọn, DEC-043) có an toàn khi sửa nội dung tài liệu mà không đụng ảnh hay không — đây là câu hỏi quyết định có tách ảnh ra KB riêng (asset host, kiến trúc cũ) hay tiếp tục gộp chung.

**Việc tiếp theo:** người dùng chuyển "Tăng dần", sync lại → agent so sánh:
1. Ảnh C trong `a.md` còn hiển thị đúng không (nhóm đối chứng).
2. Ảnh D trong `b.md` còn hiển thị đúng không (nhóm thử nghiệm, nội dung xung quanh đã đổi).
3. ID tài liệu (`knowledge_id`) của `C.png`/`D.png` có đổi không.
4. `e.md` (nếu người dùng đã thêm) có xuất hiện.

## Phát hiện quan trọng khi lấy mốc

- **Google Drive connector KHÔNG tự resolve link ảnh tương đối trong Markdown.** Nội dung `b.md` sau khi ingest vẫn còn nguyên `![Ảnh test D](D.png)` — không đổi thành `minio://...`. Nghĩa là quy trình gắn URI thủ công (`link_plan_v5_minio.py`) vẫn cần thiết cho nội dung đưa vào KB qua connector; connector không tự làm việc này.
- `D.png` không lộ URI MinIO trong tóm tắt của chính nó (khác `C.png`) — không tìm được cách lấy URI trực tiếp qua UI cho ảnh không tự lộ URI trong caption. Menu "..." của tài liệu chỉ có Phân tích lại / Chuyển / Xóa, không có "Sao chép link".
- **Dùng `knowledge_id` (document ID nội bộ của KB) làm chỉ số so sánh chính** thay vì cố lấy URI MinIO cho mọi file — vì đây mới là chỉ số phản ánh trực tiếp "connector có tạo lại tài liệu hay không" khi sync tăng dần.

## Việc tiếp theo

1. Người dùng thêm `e.md` (nội dung tùy ý) vào `knowledge/Test/`.
2. Người dùng sửa nội dung `b.md` — **không đụng dòng `![Ảnh test D](D.png)`**.
3. Chuyển "Chế độ đồng bộ" sang **Tăng dần**, chạy sync.
4. Agent mở lại 4 tài liệu cũ, so `knowledge_id` với bảng trên:
   - `a.md`, `C.png`, `D.png` không đổi (kỳ vọng) → xác nhận tăng dần bỏ qua file không sửa.
   - `b.md` đổi hay giữ nguyên `knowledge_id`? (cả hai đều là dữ liệu hữu ích)
   - `e.md` xuất hiện với `knowledge_id` mới.

## Vòng 2 — Tăng dần, thêm đoạn văn bản vào `b.md` (16/08/2026)

**Thao tác:** Agent thêm đoạn văn bản mới ("Sửa lần 2...") vào cuối `b.md`, giữ nguyên dòng ảnh D (`minio://.../9aa0a0d8-0905-43ef-b7d1-7da9f23f1c68.png`). Người dùng chạy sync với cấu hình **Tăng dần + Ghi đè + Mọi tệp**.

**Kết quả (quan sát qua UI, người dùng xác nhận):**
- `b.md` được re-ingest: nội dung xem trước hiển thị đúng đoạn "Sửa lần 2" mới, thời gian tải lên cập nhật thành `Aug 16, 2026, 4:40:37 AM`.
- Ảnh D vẫn hiển thị đúng trong `b.md` sau khi re-ingest — link MinIO không bị mất dù nội dung xung quanh (không đụng dòng ảnh) đã đổi.
- Kết luận của người dùng, agent đồng ý: đồng bộ Tăng dần chỉ update lại tài liệu có thay đổi thực sự (`b.md`), và việc sửa nội dung xung quanh một ảnh đã gắn URI MinIO không làm mất link ảnh đó, kể cả khi ảnh và tài liệu cùng chung một KB.
- **Hạn chế xác minh:** không lấy được `knowledge_id` qua MCP tool (`list_knowledge_bases` không thấy KB `Test`; tra thẳng bằng ID mốc cũng lỗi "not found or not accessible") — KB test dường như nằm ngoài phạm vi công cụ MCP hiện có. Kết luận trên dựa trên quan sát UI (thời gian tải lên, nội dung xem trước, ảnh hiển thị), không dựa trên so sánh `knowledge_id` trực tiếp như kế hoạch ban đầu.

**Việc tiếp theo (vòng 3 — Toàn bộ):** người dùng sẽ chuyển "Chế độ đồng bộ" sang **Toàn bộ** và sync lại, để so sánh hành vi: đồng bộ Toàn bộ có re-ingest lại *mọi* file (kể cả `a.md`, `C.png`, `D.png` không đổi) hay không, và ảnh có còn giữ nguyên ở cả 4 tài liệu sau đó không.

## Vòng 3a — Toàn bộ, không file nào đổi nội dung (16/08/2026)

**Thao tác:** Chạy sync với cấu hình Toàn bộ + Ghi đè + Mọi tệp, nhưng chưa sửa file nào cả (từ trạng thái cuối vòng 2).

**Kết quả:** Người dùng quan sát "ghi đè không có hiệu lực" — không thấy dấu hiệu re-ingest rõ ràng. Diễn giải hợp lý: connector Google Drive vẫn dựa trên cơ chế phát hiện thay đổi (hash/mtime) ở tầng nguồn trước khi quyết định tải lại, kể cả khi chế độ đồng bộ đặt là "Toàn bộ" — "Toàn bộ" ở đây có nghĩa là *liệt kê lại toàn bộ tài nguyên đã chọn mỗi lần chạy* (theo mô tả UI), không đồng nghĩa với *bắt buộc re-ingest nội dung không đổi*.

## Vòng 3b — Toàn bộ, thêm `e.md` mới + sửa nội dung `a.md` và `b.md` (giữ nguyên dòng ảnh) (16/08/2026)

**Thao tác:** Agent thêm file mới `e.md` (không tham chiếu ảnh) và thêm đoạn văn bản mới vào cả `a.md` (ảnh C) và `b.md` (ảnh D), giữ nguyên dòng ảnh trong cả hai. Chạy sync Toàn bộ + Ghi đè + Mọi tệp.

**Kết quả (xác nhận qua UI):**
- `e.md` được ingest thành công, đầy đủ pipeline (Phân tích tài liệu → Chia đoạn → Vector hóa → Đa phương thức → Hậu xử lý), tải lên lúc `Aug 16, 2026, 5:05:44 AM`, xuất hiện trong danh sách tài liệu KB `Test` (tổng số tài liệu tăng từ 4 lên 5).
- `b.md` hiển thị đúng nội dung "Sửa lần 3" mới thêm; ảnh D vẫn còn nguyên trong tài liệu.
- Danh sách tài liệu vẫn còn đủ `C.png`/`D.png` như các tài liệu độc lập, không bị xoá hay tạo trùng.

**Kết luận của người dùng, agent xác nhận hợp lý:** Link ảnh MinIO nhúng trong `a.md`/`b.md` là URI tĩnh trỏ thẳng vào MinIO, không phải tham chiếu động vào document `C.png`/`D.png` trong KB — nên ảnh "sống" hay "chết" trong `a.md`/`b.md` không phụ thuộc vào việc `C.png`/`D.png` có được re-sync hay không, mà phụ thuộc vào (a) object đó còn tồn tại trên MinIO, và (b) pipeline ingest của connector không sửa/chuẩn hoá lại dòng ảnh khi re-ingest tài liệu chứa nó. Qua cả 2 chế độ (Tăng dần ở vòng 2, Toàn bộ ở vòng 3b) và 3 lần sửa nội dung (`b.md` x2, `a.md` x1) không sửa dòng ảnh, ảnh vẫn giữ nguyên đúng ở mọi lần — không có trường hợp nào ảnh bị mất hay đổi link.

**Hạn chế còn lại:** Không xác minh được bằng `knowledge_id` (MCP tool không truy cập được KB `Test`), chỉ dựa trên quan sát UI (nội dung xem trước, ảnh render, danh sách tài liệu). Chưa test case biên: sửa trực tiếp nội dung `C.png`/`D.png` (đổi caption/tóm tắt) trong khi `a.md`/`b.md` không đổi — nằm ngoài phạm vi câu hỏi gốc (DEC-043) nên không bắt buộc trước khi kết luận.

## Kết luận cuối — DEC-043 được xác nhận đúng bằng thực nghiệm

Gộp ảnh + tài liệu chung một KB (DEC-043) **an toàn** khi tài liệu khác trong cùng KB được sửa nội dung và sync lại — cả ở chế độ Tăng dần lẫn Toàn bộ — miễn là dòng ảnh (URI MinIO) không bị đụng tới trong lần sửa. Xem [DEC-051](../DECISIONS.md) để biết quyết định chính thức áp dụng cho `GS9 Knowledge VNG AI`.
