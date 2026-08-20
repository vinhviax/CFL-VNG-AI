Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root repo Git vẫn là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà). Xác nhận bằng `git rev-parse --show-toplevel`.

**⚠️ THAY ĐỔI LỚN NHẤT SO VỚI TRƯỚC — đọc kỹ trước khi làm gì:** từ 20/08/2026, thư mục `knowledge/` **không còn nằm trong repo này nữa**. Toàn bộ nội dung KB thật giờ nằm trên **Drive công ty**:

```
J:\.shortcut-targets-by-id\1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG\VNGGames AI\knowledge
```

ID thư mục (`1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG`) có thể khác trên máy khác — **xác nhận lại bằng cách mở Drive thật và soi đường dẫn**, đừng tin cứng giá trị này. Việc đọc/sửa file KB (`.md`, ảnh, `image-map.json`) từ nay làm trực tiếp trên đường dẫn Drive công ty đó, không phải trong `knowledge/` của repo (thư mục đó đã bị xoá khỏi repo local, **chưa commit** — xem mục 1 bên dưới).

Đọc theo thứ tự: `AGENTS.md` (đã có cảnh báo đổi kiến trúc ở đầu) → `HANDOFF.md` mục 4.10 (việc ưu tiên số 1) → `STATUS.md` (mục mới nhất 20/08 phiên 8) → `audit/session-2026-08-20-migration-va-relink-anh.md` (chi tiết đầy đủ những gì đã làm). `DECISIONS.md` từ DEC-075 tra khi cần hiểu vì sao.

==================================================
0. BỐI CẢNH — TẠI SAO CÓ THAY ĐỔI NÀY
==================================================

Người dùng quyết định 3 việc trong phiên 8 (20/08/2026):

1. **KB và Agent hiện tại KHÔNG phải bản cuối.** Team đang thu thập lại toàn bộ nguồn tài liệu qua Google Sheet `CFL Thu Thập Dữ Liệu` (Drive công ty, root `VNGGames AI/`) để dựng lại cấu trúc kho từ đầu. **Đừng đầu tư công sức lớn chỉnh sửa/tối ưu cấu trúc KB-Agent hiện tại** — sẽ bị thay.
2. **Chuyển toàn bộ nguồn dữ liệu KB sang Drive công ty** (`crossfirelegends@vng.com.vn`), thay vì Drive cá nhân trước đây.
3. **Đổi Service Account JSON** của connector `GS9 Knowledge VNG AI` sang key đọc Drive công ty, rồi resync toàn bộ.

Việc thứ 3 có hệ quả kỹ thuật lớn: **toàn bộ URI ảnh MinIO gốc bị chết**, dù `knowledge_id` mỗi tài liệu giữ nguyên (connector khớp theo tên file, chiến lược Ghi đè). Phần lớn công việc phiên 8 là xử lý hệ quả này.

==================================================
1. VIỆC ƯU TIÊN SỐ 1 — HOÀN TẤT RELINK, CHƯA XONG HẲN
==================================================

**Đã làm xong trong phiên 8 (đã kiểm chứng, không phải suy đoán):**

- Xác định URI `exports/` (bản kết xuất OCR/caption, lấy qua `read_source_document(knowledge_id, start_chunk_index=0, end_chunk_index=0)` — chunk 0 luôn có dòng `![<tên file>](minio://.../exports/<uuid>.<ext>)` ở đầu) **render đúng** khi nhúng vào `.md` và nạp lên Web. Đã thực nghiệm thật: sửa `doc-00`, nạp lên, ảnh hiện, xác nhận qua `read_network_requests` trả **200**.
- Lấy đủ **52/52 URI `exports/`** cho toàn bộ ảnh trong `GS9 Knowledge VNG AI` (`knowledge_base_id = cefadf09-4187-46ac-a765-591e3255a4a4`).
- Relink **63 lượt URI trong 20/21 file `.md`** trên Drive công ty (`doc-00` đã đúng từ bước thử nghiệm). Dùng comment `<!-- LOCAL_ASSET: ./image-NN-... -->` làm neo để khớp đúng ảnh, tránh thay nhầm chỗ chỉ nhắc chữ `minio://` trong văn bản giải thích (đã phát hiện 1 case thật trong `doc-01`). Đã sao lưu bản gốc trước khi sửa. Đã kiểm lại: không còn URI cũ nào sót trong 21 file.
- Script + bảng ánh xạ đầy đủ đã lưu tại `scripts/one-off/relink_images_2026-08-20.py` — dùng lại được nếu cần chạy lại hoặc đối chiếu.

**CHƯA làm — làm theo thứ tự này:**

1. **Hỏi người dùng: đã nạp 20 file `.md` vừa relink lên Web chưa?** Nếu chưa, đây là việc đầu tiên — không có ý nghĩa gì thêm nếu Web chưa có bản mới.
2. **Viết lại `image-map.json` trên Drive công ty** (`knowledge/GS9 Knowledge VNG AI/image-map.json`) với 52 URI `exports/` mới — bảng ánh xạ nằm sẵn trong `scripts/one-off/relink_images_2026-08-20.py` (biến `MAP`). **Làm việc này TRƯỚC khi ai chạy `build_handbook.py`** — nếu không, builder đọc map cũ (URI chết) và ghi đè mất công relink vừa làm.
3. **`GS9 CFL Plan Version` (29 ảnh) hoàn toàn CHƯA relink.** URI ảnh của KB này cũng đã chết theo cùng sự cố đổi Service Account, nhưng KB này **ngoài phạm vi MCP** — `list_knowledge_bases` không trả về nó (chỉ share KB vào không gian mới thấy được qua MCP). Hỏi người dùng có share được KB đó vào không gian MCP không; nếu không, phải làm thủ công qua trình duyệt (chậm hơn nhiều — 29 ảnh, không có API tiện lợi).
4. **Kiểm lại `get_document_info`/`list_documents` xem đã trả lại `file_path` (URI gốc) chưa** trước khi lặp lại quy trình `exports/` cho Plan Version — nếu công cụ đã phục hồi, dùng `file_path` thật thay vì `exports/` (đáng tin hơn, xem mục 3).

==================================================
2. VIỆC CẦN QUYẾT ĐỊNH — KHÔNG TỰ Ý LÀM
==================================================

**`knowledge/` trong repo local: xoá 153 file, CHƯA COMMIT.** `git status` sẽ cho thấy 153 file đứng `D` (working tree, chưa `git add`). `origin/main` vẫn còn nguyên `knowledge/` cũ — chưa ai push việc xoá này. Có bản sao lưu `knowledge-20260820T085450Z-1-001.zip` (164 MB) tại root, untracked — **đừng xoá file này**. Hỏi người dùng: commit chính thức việc xoá (`git rm -r knowledge/` rồi commit), hay khôi phục (`git checkout -- knowledge/`)? Đừng tự quyết.

**3 file untracked khác ở root** (`git status --short` sẽ thấy):
- `knowledge-20260820T085450Z-1-001.zip` — giữ lại, đây là bản sao lưu.
- `CFL Thu Thập Dữ Liệu.xlsx` — bản export cũ của Sheet, đã có bản sống trên Drive công ty. Hỏi trước khi xoá.
- `VNGGames AI.lnk` — shortcut Windows, không cần đưa vào git.

==================================================
3. RỦI RO CHƯA CHỨNG MINH — NHỚ KHI BÁO CÁO
==================================================

- **URI `exports/` là bản kết xuất phụ (sinh cho OCR/caption), không phải blob gốc của tài liệu.** Chưa có bằng chứng nó bền lâu dài — có thể bị sinh lại/đổi uuid nếu tài liệu được xử lý lại (vd bấm "Phân tích lại" trên Web). Đây là giải pháp chạy được ngay, không phải giải pháp đúng bài. Nếu công cụ MCP phục hồi trả lại `file_path` gốc, nên chuyển về dùng `file_path` thay vì `exports/`.
- **Nguyên nhân MCP mất trường `file_path`** (giữa phiên 8, công cụ `list_documents`/`get_document_info` đột ngột không còn trả trường này) **chưa được xác nhận chắc chắn** — chỉ có bằng chứng gián tiếp (một tool khác cùng server bị ngắt/thay thế cùng lúc). Không liên quan tới việc đổi Drive — đây là trùng hợp thời điểm, không phải nhân quả.
- **File `.md` trên Drive công ty dùng line ending LF**, khác quy ước CRLF ghi trong `AGENTS.md` cho repo Drive cá nhân. Đã xác nhận đây là trạng thái có từ trước (không phải do lần relink này gây ra), nhưng cần lưu ý nếu sau này đối chiếu diff giữa 2 vị trí.

==================================================
4. LỆNH KIỂM TRA ĐẦU PHIÊN
==================================================

```powershell
# 1. Repo Git vẫn đúng vị trí cũ
git rev-parse --show-toplevel
git status --short | head -20
git fetch origin
git diff --stat origin/main HEAD

# 2. Xác nhận đường dẫn Drive công ty còn đúng
ls "J:/.shortcut-targets-by-id/1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG/VNGGames AI/knowledge"
```

Nếu lệnh (2) báo lỗi đường dẫn không tồn tại, ID thư mục đã đổi trên máy này — hỏi người dùng mở Drive công ty ra soi lại đường dẫn thật, đừng đoán.

==================================================
5. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN (không đổi so với trước)
==================================================

- Trả lời ngắn gọn, đi thẳng vào việc. Hỏi gộp một lượt rồi làm, đừng hỏi lắt nhắt.
- Phân biệt rõ "đã kiểm chứng" / "chưa chứng minh" / "còn biến số" — đặc biệt quan trọng trong phiên này vì có nhiều suy đoán chưa kiểm chứng được (URI `exports/` có bền không, nguyên nhân MCP mất capability).
- Kiểm chứng thật bằng nhiều lớp, đừng báo cáo suông. Khi có thể, đối chiếu 2 nguồn độc lập trước khi kết luận (đã áp dụng đúng cách này khi lấy 52 URI — dùng cả `get_document_info` và `read_source_document` chunk 0, đối chiếu khớp uuid).
- Khi phát hiện điều mới: ghi vào `DECISIONS.md`, rồi chắt phần "người dùng cần làm gì" sang `docs KB/Human` nếu liên quan tới hướng dẫn thao tác (lưu ý: `docs KB/Human` vẫn còn trong repo, không bị ảnh hưởng bởi việc chuyển `knowledge/` — chỉ bản sinh/nạp lên Web mới chuyển vị trí).
