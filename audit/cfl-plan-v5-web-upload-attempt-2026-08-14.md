# Audit tạm dừng — upload CFL Plan Version 5 lên Web KB — 14/08/2026

## Yêu cầu

Người dùng chỉ định rõ: đưa 12 Markdown + 29 JPEG tại `knowledge/GS9 Plan Version/V5/` (kèm `assets/`) vào KB Web đã có sẵn **`GS9 CFL Plan Version`**, ID `1452bc9a-c8b4-487b-b623-34e0b00a83e9`, và sửa lại link ảnh trong Markdown cho đúng URI MinIO.

## Baseline đã xác nhận trước khi thao tác

- KB `GS9 CFL Plan Version`: chủ sở hữu là người dùng, mô tả "Chứa các thông tin về Plan Version", **0 tài liệu**.
- Cấu hình (tab Tổng quan/Mô hình/Xử lý, đọc rồi đóng bằng Hủy, không lưu):
  - Loại: `Tài liệu`.
  - Chiến lược lập chỉ mục: `RAG (vector + từ khóa)` **và** `Wiki` cùng bật.
  - Model chat/tóm tắt: `deepseek-v4-flash`; Embedding: `text-embedding-3-large`; Model tổng hợp Wiki: `deepseek-v4-flash`.
  - Parser Hình ảnh (`.jpg .jpeg .png .gif .bmp .tiff .webp`): `MinerU`.
- Kết luận: KB đã cấu hình đúng để nhận cả Markdown và JPEG trong cùng một KB (không tách host ảnh riêng như hai KB sổ tay chính — đây là lựa chọn của người dùng, không phải mặc định của tôi).

## Việc đã làm

Mở hộp thoại "Tải tài liệu lên" trên đúng trang KB. Không chọn hoặc tải bất kỳ file nào thành công.

## Blocker kỹ thuật — chưa giải quyết được trong phiên này

Công cụ tự động hóa trình duyệt (`file_upload`, Claude in Chrome) dùng một whitelist đường dẫn **riêng, độc lập với quyền đọc file của agent** (Bash/Read đọc `J:\My Drive\CFL\VNG AI\Knowledge Base VNG` bình thường suốt phiên). Mọi đường dẫn tới file thật trong project — bất kể định dạng (`J:\...`, `J:/...`, `/j/...`, có hay không khoảng trắng) — đều bị từ chối. Chỉ file trong scratchpad phiên làm việc mới được chấp nhận qua bước kiểm tra quyền, nhưng đó không phải vị trí of file gốc.

Đã thử và loại trừ các giả thuyết: độ dài đường dẫn, khoảng trắng, số gạch ngang, ký tự `:` của drive letter, từ khóa tiếng Việt cụ thể — không giả thuyết nào giải thích nhất quán toàn bộ log lỗi. Không tốn thêm lượt thử; kết luận thực dụng: đây là giới hạn quyền truy cập file của riêng công cụ `file_upload`, không phải lỗi có thể tự sửa bằng cách đổi tên/đường dẫn.

**Không có mutation nào xảy ra.** KB vẫn 0 tài liệu tại thời điểm dừng. Hộp thoại "Tải tài liệu lên" có thể vẫn còn mở trên tab Chrome của phiên trước (không đáng tin cậy giữa hai phiên khác nhau — session mới nên tự mở lại).

## Bước tiếp theo khi tiếp tục

1. Con người tự chọn file qua Explorer (cách nhanh nhất, không cần thêm chẩn đoán):
   - Mở `https://vnggames.ai/kb/knowledge/1452bc9a-c8b4-487b-b623-34e0b00a83e9?tenant_id=10012`.
   - `Tải lên` → `Chọn tệp` → chọn cả 29 file `.jpg` trong `knowledge/GS9 Plan Version/V5/assets/` → xác nhận tải lên.
   - Chờ trạng thái từng ảnh chuyển `Hoàn tất`.
2. Sau khi 29 ảnh live, agent lấy URI MinIO cho từng ảnh bằng đúng quy trình đã dùng khi tách KB asset 07/08/2026 (xem `docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md`, Task 4 Step 2): mở chi tiết từng ảnh, bắt network request chứa `file_path=minio://knowledge-base-prd/10012/exports/<uuid>.jpg`, đối chiếu heading/checksum với `source-manifest.json` trước khi ghi mapping.
3. Ghi mapping vào `knowledge/GS9 Plan Version/V5/image-map.json` (file mới, chưa tồn tại).
4. Sửa 12 file `.md` local: thay `assets/image-XX-*.jpg` bằng URI MinIO, giữ traceability về file local.
5. Upload 12 Markdown đã sửa vào cùng KB (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`), lại cần con người chọn file qua Explorer vì lý do blocker trên, trừ khi tìm được cách khác (drag-drop, `/add-dir`, hoặc công cụ thay thế).
6. Chat-test 1 câu buộc trả lời kèm ảnh, xác nhận nguồn tham khảo dùng đúng URI mới.
7. Cập nhật audit/STATUS/HANDOFF với kết quả thật.

## Việc khác đang mở, không thuộc blocker này

Người dùng cũng yêu cầu: xác định Agent nào nên dùng KB nào và cần tool gì (mở rộng từ `agent/kb-allowlist-proposal-2026-08-14.md` sang toàn bộ 10 custom Agent, có tính đến KB Plan Version mới). Chưa bắt đầu việc này trong phiên. Người dùng tự nhận xử lý G1 (hạ quyền share 5 KB xuống Chỉ đọc) — không cần agent làm, chỉ theo dõi khi nào xong để mở khóa bind KB nghiệp vụ.
