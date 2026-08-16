# Audit — Gắn URI MinIO cho bundle CFL Plan Version 5

**Ngày:** 15/08/2026
**Phạm vi:** đọc Web (read-only) + ghi 12 file Markdown local. **Không có mutation nào trên Web.**
**KB đích:** `GS9 CFL Plan Version` — `1452bc9a-c8b4-487b-b623-34e0b00a83e9`, tenant `10012`.

## Bối cảnh

Người dùng đã tự upload 29 ảnh `.jpg` lên KB ngày 14/08/2026, gỡ blocker `file_upload` ghi trong
`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`. Việc còn lại là lấy URI MinIO của từng ảnh và
nhúng vào 12 Markdown để chat trên Web render được ảnh (đường dẫn tương đối `assets/...` không hoạt động).

## Trạng thái Web đã kiểm chứng

- 29/29 tài liệu ảnh `Hoàn tất`.
- Wiki đã tự sinh: mục lục + `Tóm tắt (29)`; Graph 285 node.
- Chưa có Markdown nào trong KB.

## Cách lấy URI — đã kiểm chứng

1. Deep-link mở thẳng chi tiết: `.../kb/knowledge/<KB_ID>?tenant_id=10012&knowledge_id=<DOC_ID>`
2. Bấm **Toàn văn** (KHÔNG phải *Xem trước*).
3. `read_network_requests(urlPattern="file_path")` → `GET /kb/v1/api/files?file_path=minio://...` (URL-decode).

`knowledge_id` của 29 ảnh thu bằng deep-link `?q=image-NN` rồi mở dòng kết quả duy nhất.
Bản ghi ID: `scratchpad/plan-v5-knowledge-ids.json` (không đưa vào Git vì là dữ liệu tạm).

## Phát hiện quan trọng — mỗi ảnh sinh NHIỀU URI

Parser `MinerU` tách thêm ảnh con, nên `Toàn văn` nạp 2–10 URI cho một tài liệu.
Chọn nhầm thì ảnh vẫn hiển thị nhưng là bản cắt sai, **không có lỗi nào báo**.

**Quy tắc chọn:** URI có byte-size trùng khớp `source-manifest.json`.
Điều kiện đủ: 29 kích thước trong manifest **đều duy nhất** (đã kiểm: 29/29 unique).
**Thực nghiệm:** URI xuất hiện ĐẦU TIÊN trong log luôn là ảnh gốc.

Ví dụ `image-29-qbb95-bo-ngua.jpg` (local 21.122 byte, 720×720):

| URI | Bytes | Kết luận |
|---|---|---|
| `.../e6e45329-87e1-4ded-9515-247ff7c4cfde.jpg` | **21.122** | ảnh gốc — đã chọn |
| `.../86caa5d8-5b21-4c1c-bda9-d4367fb0824d.jpg` | 14.967 | bản MinerU cắt viền — loại |

### Mẫu đã kiểm chứng bằng byte-size (MCP `get_image`)

| Ảnh | Số URI trả về | Bytes đo được | Bytes manifest | Kết quả |
|---|---|---|---|---|
| image-02 | 3 | 92.979 | 92.979 | khớp |
| image-04 | 10 | 56.479 | 56.479 | khớp |
| image-24 | 6 (tích luỹ) | 62.368 | 62.368 | khớp |
| image-28 | 2 | 14.242 | 14.242 | khớp |
| image-29 | 2 | 21.122 | 21.122 | khớp |

5/29 kiểm chứng trực tiếp, phủ cả ca 2 URI, 3 URI, 10 URI và ca log tích luỹ.
24 ảnh còn lại áp dụng quy tắc "URI đầu tiên". **Phân loại: Có điều kiện** — chốt thành
*Đã kiểm chứng* sau khi chat-test render ảnh thật.

## Kết quả ghi vào bundle

- Tạo mới `knowledge/GS9 Plan Version/V5/image-map.json`: 29 mục, 29 URI duy nhất, tên khớp manifest 1-1.
- Chạy `python scripts\link_plan_v5_minio.py` → đổi **29 ảnh nhúng + 29 link registry** trên 7/12 file.
- Đếm lại trong 12 `.md`: **58 link `minio://`**, **29 comment `LOCAL_ASSET`**, **0 link tương đối còn sót**.
- Chạy lại script: `0 thay đổi` → idempotent đúng thiết kế.

## Sửa test

`tests/test_link_plan_v5_minio.py::test_bundle_currently_has_29_embeds_and_29_registry_links` khoá vào
trạng thái *trước* khi gắn link, nên sau thao tác một chiều sẽ đỏ vĩnh viễn. Đã sửa để đếm hợp đồng
29+29 ở **cả hai** dạng (`assets/...` và `minio://...`), giữ nguyên ý định kiểm tra.
Bổ sung `test_bundle_has_no_leftover_relative_image_links`.

Kết quả: `python -m unittest discover -s tests -p test_link_plan_v5_minio.py` → **Ran 7 tests, OK**.

## Gate chưa chạy được trên máy này

`tests/test_build_handbook.py` (10 lỗi) và `tests/test_convert_cfl_plan_html.py` (1 lỗi nạp module)
đều hỏng vì **thiếu package**, không liên quan thay đổi lần này:

```
ModuleNotFoundError: No module named 'markdown'
ModuleNotFoundError: No module named 'bs4'
```

Cần `pip install markdown beautifulsoup4` trên máy nhà rồi chạy lại full gate trước khi bàn giao.

## Việc còn lại

1. **Người dùng upload 12 file `.md`** trong `knowledge/GS9 Plan Version/V5/` lên cùng KB.
2. Chat-test một câu buộc trả lời kèm ảnh; xác nhận ảnh render thật và `Nguồn tham khảo` dùng đúng URI mới.
3. Nếu đạt → nâng kết luận quy tắc "URI đầu tiên" lên *Đã kiểm chứng* và cập nhật `STATUS.md` / `HANDOFF.md`.

## Cảnh báo bảo trì

12 file `.md` là artifact sinh từ `convert_cfl_plan_html.py`. Chạy lại converter sẽ ghi đè link MinIO
về `assets/...`; phải chạy lại `link_plan_v5_minio.py` sau đó.

Nguồn ghi "Tài liệu nội bộ, vui lòng không phổ biến ra ngoài" — giữ hạn chế này khi cấu hình chia sẻ KB.
KB hiện **chưa** share cho space nào (MCP connector trả `not found or not accessible`, đúng như mong đợi).
