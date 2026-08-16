# Audit — Lỗi ảnh render hai lần trong chat KB `GS9 CFL Plan Version`

**Ngày:** 15/08/2026
**Phạm vi:** điều tra read-only, **không mutation nào**. Không sửa file `.md`, không sửa KB, không sửa Agent.
**Trạng thái kết luận:** **ĐÃ ĐÓNG 15/08/2026.** Không phải lỗi nội dung. Xem mục "Kết luận cuối" ở cuối file.

## Kết luận cuối — cú pháp hiện tại ĐÚNG, lỗi do model

Người dùng chạy thêm hai phép thử và chốt:

1. KB **chỉ chứa `.md`** có link ảnh, không upload ảnh vào KB đó → **vẫn duplicate**. Loại bỏ nghi phạm "gộp ảnh chung KB".
2. Chat lại lần nữa trên cùng dữ liệu → **hiển thị bình thường, mỗi ảnh đúng một lần, không còn mảnh cú pháp thừa**.

→ **Cú pháp đang dùng là ĐÚNG và giữ nguyên:**

```markdown
![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/10012/exports/<uuid>.png)
```

→ Hiện tượng nhân đôi là **hành vi không ổn định của model khi soạn câu trả lời** (đôi lúc tự xuất ra `![url](url)` khiến bộ render chèn ảnh ở cả hai vị trí), **không phải lỗi của file Markdown, không phải lỗi cấu trúc KB**.

**Hệ quả:**
- KHÔNG sửa 12 file `.md` của Plan V5. Chúng đã đúng.
- KHÔNG sửa `build_handbook.py`, `convert_cfl_plan_html.py`, `link_plan_v5_minio.py` về mặt cú pháp ảnh.
- File thí nghiệm `audit/test-fixtures/doc-test-cu-phap-anh.md` không cần chạy nữa; giữ lại làm tài liệu tham khảo nếu sau này nghi ngờ tái diễn.
- Nếu muốn giảm tần suất: cân nhắc thêm một câu vào System Prompt của Agent bind KB có ảnh, đại ý *"khi trích dẫn ảnh, xuất tham chiếu ảnh đúng một lần, không lặp URI"*. Đây là giảm nhẹ, không phải sửa gốc.

---

## Phần dưới đây là quá trình điều tra, giữ làm bằng chứng lịch sử


## Hiện tượng

Người dùng chat trên KB `GS9 CFL Plan Version` (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`), câu hỏi *"Trong Version 5 mới sẽ có những hoạt động gì mới"*. Câu trả lời hiển thị:

- `Nguồn tham khảo (6 tài liệu)`, `Hoàn tất 3 bước` — chuỗi truy hồi chạy bình thường
- **Mỗi ảnh hiện HAI lần**, hai bản giống hệt nhau
- Ba mảnh cú pháp markdown rơi lại thành **chữ literal**: `![` · `](` · `)`

Thứ tự render thực tế:

```
![          ← chữ literal
[ẢNH 1]
](          ← chữ literal
[ẢNH 2]
)           ← chữ literal
```

## Suy luận từ ba mảnh literal

Markdown **không được parse**. Và giữa `![` với `](` lại có ảnh — tức **cả ô alt text lẫn ô URL đều bị thay bằng `<img>`**.

Chỉ một cấu hình đầu vào cho ra kết quả đó: chuỗi tới bộ render chat có dạng

```
![minio://knowledge-base-prd/10012/exports/<uuid>.jpg](minio://knowledge-base-prd/10012/exports/<uuid>.jpg)
```

Nghĩa là bộ render chat quét toàn văn, thấy `minio://` ở đâu thì chèn `<img>` vào đó — chèn xong thì cú pháp markdown vỡ và `![`, `](`, `)` rơi lại thành chữ. Để có hai ảnh thì phải có **hai** URI, tức URI đã lọt vào ô alt text.

## Đã loại trừ — file `.md` local KHÔNG hỏng

| Kiểm tra | Kết quả |
|---|---|
| Số embed `![alt](minio://...)` | **29** — đúng thiết kế |
| Số link registry `[text](minio://...)` | **29** — đúng thiết kế |
| URI `minio://` lọt vào ô alt text | **0 trường hợp** |
| Link lồng nhau `](...](` | **0 trường hợp** |
| Mẫu alt text | `'Hoạt động chủ đề Halloween'`, `'AN94-Smilodon'`, `'Giao diện phối súng ngoài trận (bản tiếng Việt)'` — đều là chú thích tiếng Việt, không phải URI |

Lệnh kiểm chứng dùng regex trên cả 12 file, không phải đọc mẫu.

## Đã loại trừ — nội dung lưu trên Web KHÔNG hỏng

Mở trang chi tiết `07-hoat-dong-tang-do-hoat-dong.md` (`knowledge_id=a1deaca7-f217-4b0a-8acb-344b2142ddbc`), tab `Toàn văn`:

- Ảnh `image-17-hoat-dong-chu-de-halloween.jpg` render **đúng một lần**
- Kèm caption bên dưới, không có mảnh cú pháp literal nào
- Trạng thái tài liệu `Hoàn tất`

Vậy bản lưu và bản render ở trang tài liệu đều đúng. Lỗi chỉ xuất hiện ở **bộ render của chat**.

## Bằng chứng phụ — 29 URI MinIO là ĐÚNG

Các ảnh thực tế hiện trong câu trả lời chat khớp đúng nội dung được hỏi (ảnh chủ đề Halloween, ảnh lịch nổi bật hoạt động). Kết hợp với `Nguồn tham khảo (6 tài liệu)`, điều này chứng minh:

- Chuỗi bind + truy hồi + phân giải URI MinIO **chạy thật**
- `image-map.json` ánh xạ **đúng** — không phải map sai ảnh

Đây là bằng chứng vận hành đầu tiên cho quy tắc "URI đầu tiên = ảnh gốc" ngoài phép đo byte-size. Tuy nhiên gate G6 **chưa đạt** vì tiêu chí G6 gồm cả việc câu trả lời hiển thị đúng.

## Mảnh bằng chứng còn thiếu

**Chưa đọc được text chunk thô.** Tab `Xem phân đoạn` của tài liệu 07 không cuộn thêm được để tới chunk chứa ảnh — panel bị kẹt, page cuộn thay vì panel. Cần đọc chunk này để phân biệt hai giả thuyết:

- **(a)** Parser lúc nạp đã viết lại markdown, thay alt text bằng đường dẫn ảnh
- **(b)** Parser giữ nguyên, chính LLM tự soạn `![url](url)` khi viết câu trả lời

Cách phân biệt: nếu chunk thô vẫn còn alt text tiếng Việt → giả thuyết (b); nếu chunk đã thành `![minio://...](minio://...)` → giả thuyết (a).

## Nghi phạm số một

Bộ sổ tay `GS9 Knowledge VNG AI` dùng **đúng y hệt** định dạng này:

```markdown
<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/14-....png -->
![Câu trả lời có mô tả ảnh nhưng không render ảnh khi Markdown dùng đường dẫn tương đối](minio://knowledge-base-prd/10012/exports/227784d8-....png)
```

Và chat render ảnh **bình thường** hồi 06/08/2026 — bằng chứng `audit/evidence/2026-08-06-chat-image-minio-rendered.png`.

Khác biệt cấu trúc duy nhất giữa hai KB:

| | Sổ tay | Plan V5 |
|---|---|---|
| Ảnh | KB riêng `GS9 Knowledge VNG - Image Assets` | **Cùng KB** với Markdown |
| KB tiêu thụ | chỉ chứa 20 Markdown, 0 ảnh | 12 Markdown **+ 29 JPEG** |

Khi ảnh và Markdown chung một kho, truy hồi kéo về cả chunk Markdown *lẫn* chính tài liệu ảnh. Đây là nghi phạm hàng đầu.

## Phép thử đối chứng cần chạy — rẻ và dứt điểm

Hỏi một câu buộc trả lời kèm ảnh trên **KB sổ tay `GS9 Knowledge VNG AI`** (cùng định dạng markdown, nhưng ảnh ở KB riêng):

| Kết quả | Kết luận | Việc phải làm |
|---|---|---|
| Sổ tay **cũng** nhân đôi | Lỗi phía nền tảng, không liên quan file hay quyết định gộp KB | Báo lỗi nền tảng. **Không sửa 12 file** |
| Sổ tay **bình thường** | Nguyên nhân là gộp ảnh + Markdown chung một KB | Tách ảnh sang KB riêng theo pattern sổ tay, HOẶC bỏ cú pháp `![]()` dùng URI trần |

**Chạy phép thử này TRƯỚC khi sửa 12 file.** Nếu nguyên nhân nằm ở nền tảng mà lại đi sửa file thì vừa mất công vừa phá thứ đang đúng.

## Ảnh hưởng tới quyết định đã chốt

Nếu phép thử cho kết quả "gộp chung KB là nguyên nhân", điều này **xung đột với quyết định của người dùng** là để mọi phiên bản Plan trong cùng một KB và để ảnh chung Markdown. Khi đó phải đưa lại cho người dùng quyết định: chấp nhận tách KB ảnh, hay đổi định dạng nhúng ảnh.

Lưu ý ràng buộc đã khoá: 29 URI MinIO gắn cứng vào KB `1452bc9a...`. Tách ảnh sang KB mới = upload lại 29 ảnh = 29 URI mới = chạy lại toàn bộ quy trình thu URI.
