# Audit phiên 20/08/2026 — Chuyển kiến trúc sang Drive công ty, đứt URI ảnh, relink 52 ảnh

## Bối cảnh

Người dùng quyết định: (1) KB và Agent hiện tại **không phải bản cuối** — sẽ dựng lại sau khi thu thập xong tài liệu team; (2) chuyển toàn bộ nguồn dữ liệu KB từ Google Drive cá nhân sang **Drive công ty** (`crossfirelegends@vng.com.vn`); (3) từ nay làm việc trực tiếp trên cây `J:\.shortcut-targets-by-id\1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG\VNGGames AI\knowledge`, không còn dùng `knowledge/` trong repo Drive cá nhân.

## Việc đã làm

### 1. Thu thập nguồn tài liệu team

Tạo Google Sheet `CFL Thu Thập Dữ Liệu` (owner `crossfirelegends@vng.com.vn`, ID `1hXyIgACbmSxfeHVHMoyQfXp6ytuQ3Mlp3X9fD5J68t8`), đặt tại root `VNGGames AI/` trên Drive công ty. 4 sheet: `HuongDan`, `LoaiDoc` (9 loại tài liệu + bảng "Loại file — Data hay Docs?"), `ThuThapDoc` (bảng điền, người dùng đã tự mở rộng thêm cột "Link tài liệu đã apply"), `TuDien`. Người dùng đang tự chỉnh sửa trực tiếp trên Web, không qua agent.

Đã sửa định dạng bảng "Loại file" cho khớp style bảng gốc (header nền navy chữ trắng, tiêu đề Arial 14 đậm, nhãn cột B đậm) — làm trên bản `.xlsx` export rồi để người dùng tự tải lên lại.

### 2. Xoá `knowledge/` khỏi repo local — **CHƯA COMMIT**

Người dùng tự tay xoá thư mục `knowledge/` (153 file, 9 kho) khỏi `J:\My Drive\CFL\VNG AI\Knowledge Base VNG\knowledge`. Xác nhận qua `git status --short`: toàn bộ 153 file đứng `D` (deleted, working tree), **chưa `git add`, chưa commit**. `git diff --stat origin/main HEAD` rỗng — nghĩa là commit gần nhất (`7062ccf`) vẫn còn nguyên trên remote, chưa ai push việc xoá này.

**Có bản sao lưu:** file `knowledge-20260820T085450Z-1-001.zip` (164 MB, tạo 15:56 hôm nay) nằm ngay tại root project, **untracked**, chưa bị git hay ai xoá. Đây rất có thể là bản Drive tự xuất khi người dùng tải xuống trước khi xoá. **Đừng xoá file zip này** cho tới khi xác nhận không cần phục hồi.

Hai file khác cũng untracked ở root: `CFL Thu Thập Dữ Liệu.xlsx` (bản export cũ, đã có bản sống trên Drive công ty — có thể xoá) và `VNGGames AI.lnk` (shortcut Windows, không cần vào git).

### 3. Đổi Service Account JSON của connector `GS9 Knowledge VNG AI` sang key công ty

Người dùng vào **Cấu hình Knowledge Base → Nguồn dữ liệu → Sửa nguồn dữ liệu**, dán JSON service account mới (quyền đọc Drive công ty), rồi đồng bộ lại. Xác nhận qua Web: mỗi tài liệu hiện có `Thời gian tải lên` mới (vd `21:31:45 20/8/2026`), khớp đúng thời điểm resync.

**Hệ quả xác nhận được:** `knowledge_id` của từng tài liệu **giữ nguyên** (do connector khớp theo tên file, dùng chiến lược Ghi đè — không tạo document mới), nhưng nội dung/URI lưu trữ bị nạp lại. Các file `.md` cục bộ hết hiện ảnh, đúng như người dùng quan sát.

### 4. Công cụ MCP mất khả năng trả `file_path` — không liên quan tới việc đổi Drive

Đầu phiên, `list_documents`/`get_document_info` (namespace `0ea6d139-...`) trả đủ `file_path` (URI MinIO gốc, dạng `minio://.../<knowledge_id>/<uuid>.ext`). Giữa phiên, có system-reminder báo một tool khác cùng server (`faq_search`) bị ngắt và thay bằng `database_query`/`list_faq_entries`. Sau mốc đó, `get_document_info`/`list_documents` không còn trả `file_path` trong bất kỳ lần gọi nào (đã thử nhiều knowledge_id, nhiều batch). Đây là thay đổi phía server MCP, **trùng thời điểm nhưng không phải do đổi Drive.**

Đã thử và loại các hướng sau để lấy lại URI gốc:
- Gọi thẳng endpoint `miniapp.vnggames.ai/kb/v1/api/knowledge-bases/{id}/files?file_path=...` qua JS injection trong trang — bị chặn CORS.
- Mở URL đó trực tiếp trên trình duyệt — `401 Unauthorized: missing authentication`.
- Đọc localStorage lấy bearer token để tự gọi API — **không thử**, vì đây đúng loại việc `HANDOFF.md` cảnh báo không nên làm (trích token xác thực qua JS injection).

### 5. Phát hiện và xác nhận đường vòng: URI `exports/`

Khi đọc nội dung tài liệu qua `read_source_document`, phần mô tả ảnh (sinh cho OCR/caption) luôn nhúng sẵn một dòng `![<tên file>](minio://knowledge-base-prd/10012/exports/<uuid>.<ext>)` ở đầu chunk 0 — đây là bản kết xuất do nền tảng tự sinh, khác `file_path` gốc (`<knowledge_id>/<uuid>`).

**Đã kiểm chứng bằng thực nghiệm thật, không suy đoán:**
1. Sửa `doc-00-gioi-thieu-va-quick-start.md` trên Drive công ty, thay URI ảnh `image-01` bằng URI `exports/` tương ứng.
2. Nạp lên Web (tự động qua sync định kỳ, không cần thao tác thủ công).
3. Mở tài liệu vừa nạp: **ảnh hiện đúng vị trí**. Xác nhận thêm qua `read_network_requests` — request `GET .../files?file_path=minio%3A%2F%2F...exports%2F4d3d44e1-...` trả **200**, đúng và duy nhất trong lần tải trang đó (không phải cache).

**Rủi ro chưa được chứng minh, cần ghi rõ:** URI `exports/` là bản kết xuất phụ, không phải blob gốc của tài liệu. Chưa có bằng chứng nó bền lâu dài — có thể bị sinh lại/đổi uuid nếu tài liệu được xử lý lại (vd bấm "Phân tích lại"). Coi đây là giải pháp tạm chạy được, không phải giải pháp đúng bài.

### 6. Lấy đủ 52/52 URI `exports/` cho `GS9 Knowledge VNG AI`, relink 21 file `.md`

Với mỗi ảnh trong 52 ảnh của kho `GS9 Knowledge VNG AI` (`knowledge_base_id = cefadf09-4187-46ac-a765-591e3255a4a4`):
- Thử `get_document_info` theo lô 10-14 ID — khi trường `description` tình cờ chứa dòng `![<tên đúng file>](minio://.../exports/...)` ở đầu thì lấy trực tiếp.
- Khi không có (description bị cắt hoặc không nhúng embed), fallback bằng `read_source_document(knowledge_id, start_chunk_index=0, end_chunk_index=0)` — chunk 0 luôn có dòng embed self-reference ở đầu, xác nhận qua đối chiếu 2 nguồn khớp uuid tuyệt đối (case `image-16`).

Kết quả: bảng ánh xạ đầy đủ 52 cặp `tên file → uuid exports/`.

**Áp dụng vào 21 file `.md`:** viết script Python, dùng comment `<!-- LOCAL_ASSET: ./image-NN-... -->` làm neo (comment luôn đứng ngay trước dòng `![alt](minio://...)` tương ứng) để khớp đúng URI cần thay, tránh thay nhầm các chỗ chỉ nhắc chữ `minio://` trong văn bản giải thích (đã phát hiện 1 case thật trong `doc-01`: câu ví dụ `(minio://knowledge-base-prd/.../ten-anh.png)` là placeholder minh hoạ, không phải ảnh thật — script đã bỏ qua đúng).

- Sao lưu từng file gốc trước khi sửa (`scratchpad/backup_doc_md/`).
- Ghi qua file tạm + `os.replace`.
- Kết quả: **63 URI được thay trong 20/21 file** (`doc-00` không đổi vì đã sửa tay từ bước thử nghiệm, đã đúng từ trước). Không có cảnh báo tên ảnh không khớp bảng.
- Kiểm lại: `grep` không còn URI dạng `<knowledge_id>/<uuid>` (cũ) nào trong 21 file; đúng 52 URI `exports/` duy nhất xuất hiện xuyên suốt.

**Phát hiện phụ:** file `.md` trên Drive công ty dùng **line ending LF**, không phải CRLF như quy ước ghi trong `AGENTS.md`/`HANDOFF.md` cho repo Drive cá nhân. Đã xác nhận qua so sánh với bản backup trước khi sửa — LF đã có từ trước, không phải do script gây ra. Có thể do quá trình copy sang Drive công ty làm mất định dạng CRLF gốc.

## Việc CHƯA làm — treo lại cho phiên sau

1. **`image-map.json` trên Drive công ty chưa được viết lại** với 52 URI mới. Nếu ai chạy `build_handbook.py` trước khi cập nhật file này, nó sẽ đọc map cũ (URI gốc đã chết) và ghi đè lên các file `.md` vừa relink — **mất công vừa làm**. Cảnh báo rõ cho phiên sau.
2. **`GS9 CFL Plan Version` (29 ảnh) — hoàn toàn chưa relink.** KB này không nằm trong phạm vi mà MCP nhìn thấy được (`list_knowledge_bases` chỉ trả 6 KB, không có Plan Version) — không thể lặp lại quy trình lấy URI qua MCP như đã làm với `GS9 Knowledge VNG AI`. Cần: (a) người dùng share KB đó vào không gian MCP, hoặc (b) tìm đường khác (duyệt qua trình duyệt từng ảnh — chậm, 29 ảnh).
3. **Chưa xác nhận người dùng đã nạp 20 file `.md` vừa sửa lên Web.** Việc relink chỉ có ý nghĩa sau khi đồng bộ; hiện tại vẫn là thay đổi cục bộ trên Drive công ty.
4. **`knowledge/` trong repo local vẫn ở trạng thái xoá chưa commit.** Cần người dùng xác nhận: có muốn `git rm -r knowledge/` và commit chính thức, hay giữ nguyên trạng thái làm việc (working tree khác HEAD) — hiện tại rất dễ nhầm lẫn nếu ai chạy lệnh git không kiểm tra kỹ trước.
5. **Chưa dọn 3 file untracked ở root**: file zip backup (giữ lại), `CFL Thu Thập Dữ Liệu.xlsx` cũ (có thể xoá, đã có bản sống trên Drive công ty), `VNGGames AI.lnk` (không cần thiết trong git).

## Mức bằng chứng

| Việc | Mức bằng chứng |
|---|---|
| Ảnh `exports/` render đúng khi nhúng vào `.md` thật, nạp lên Web | **Đã kiểm chứng** — thực nghiệm 1 ảnh, xác nhận qua network request 200 |
| 52/52 URI thu thập đúng tên file | **Đã kiểm chứng** — đối chiếu 2 nguồn độc lập cho ít nhất 1 case, không có cảnh báo lệch tên ở 51 case còn lại |
| URI `exports/` bền vững lâu dài | **Chưa chứng minh** — chỉ là suy đoán dựa trên tên thư mục |
| Nguyên nhân MCP mất `file_path` | **Chưa chứng minh chắc chắn** — có bằng chứng gián tiếp (tool khác cùng server đổi cùng lúc), không có xác nhận trực tiếp từ phía nền tảng |
| 20/21 file `.md` đã relink đúng, không sót URI cũ | **Đã kiểm chứng** bằng grep toàn bộ cây |
