# Audit chuẩn hóa workspace — 14/08/2026

## Phạm vi

Chuẩn hóa local project tại `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`. Không mở trình duyệt, không upload, không đổi cấu hình và không mutation tài nguyên live.

## Kết luận về `knowledge-vng/`

`knowledge-vng/` là folder artifact gộp cũ, không phải một file. Trước khi workspace được di chuyển, folder này chứa:

- 20 Markdown sinh tự động;
- `image-map.json`;
- `assets/` với 49 PNG.

Layout hiện hành tách đúng theo tên KB trên Web:

- `knowledge/GS9 Knowledge VNG AI/`: 20 Markdown + map;
- `knowledge/GS9 Knowledge VNG - Image Assets/`: 49 PNG.

Builder và test không còn tạo hoặc phụ thuộc folder `knowledge-vng/`.

## Phục hồi core

Trong lần di chuyển, master `so-tay-tao-knowledge-base-v3.md` và HTML offline không còn ở root mới hoặc các root cũ. Trước mọi lần build, 20 module consumer cùng map được backup nguyên byte tại:

`audit/workspace-normalization-prebuild-2026-08-14.zip`

SHA-256: `E67C0DADA29C286E8D295E1796B8C28FC35EE8313F3E5538524310A406042299`

Master được phục hồi cơ học từ 20 module: bỏ generated header/`LOCAL_ASSET`, đổi link MinIO ngược về asset local theo map duy nhất, hạ heading về cấp trong master và bọc lại đúng 20 marker `MODULE`. Dry-run sinh lại 20/20 module khớp bản backup sau khi chỉ quy đổi đường dẫn local/audit sang độ sâu folder mới.

Sau đó sửa ba SOP đang hoạt động nhưng còn số liệu/layout cũ:

- `01-chuan-bi-noi-dung.md`;
- `09-van-hanh-documents-wiki-graph.md`;
- `11-chat-kiem-thu-va-bao-tri.md`.

Các sửa đổi có chủ đích là 14 → 20 Markdown, 34 → 49 PNG, tên KB có prefix `GS9` và đường dẫn mới dưới `knowledge/`. Không thay các kết quả kiểm thử lịch sử có ghi rõ “tại thời điểm test”.

Năm file context cũ được backup trước khi viết lại tại `audit/workspace-docs-before-normalization-2026-08-14.zip`, SHA-256 `33F3556EF13C92BEEEB16A4F1F74C010DB6E74BB1AC9EC9CD428FF4726808B44`.

## Thay đổi builder/test

- Consumer output/map: `knowledge/GS9 Knowledge VNG AI/`.
- Asset local: `knowledge/GS9 Knowledge VNG - Image Assets/`.
- `LOCAL_ASSET`: `../GS9 Knowledge VNG - Image Assets/<file>.png`.
- Hỗ trợ Markdown image target bọc `<...>` để đường dẫn có khoảng trắng hợp lệ.
- Bổ sung test khóa tên Web, layout mới, đường dẫn có khoảng trắng và cấm SOP master dùng layout/count cũ.

## Dọn dẹp

Đã chuyển 6 fixture cũ từ `audit-upload-folder/` sang `audit/archive/audit-upload-folder-2026-08-06/` để vẫn truy nguyên được.

Đã gửi 5 folder đã xác minh vào Windows Recycle Bin, tổng 39 file/1.778.642 byte:

- `.codex-tmp/`;
- `outputs/` — chứa output kiểm tra và một XLSX trùng SHA-256 với `samples/faq/mau-faq.xlsx`;
- `tmp/` — 14 raw JPEG có đủ 14 PNG phát hành tương ứng;
- `scripts/__pycache__/`;
- `tests/__pycache__/`.

Các mục này có thể khôi phục từ Recycle Bin. Không xóa hay di chuyển file trong `knowledge/`, `samples/`, dữ liệu CFL hoặc credential hiện hữu.

## Verification

```text
Build complete
- 20 modules: 125,609 bytes
- Offline HTML: 30,859,005 bytes

Ran 16 tests in 1.199s
OK
```

Kiểm kê sau build:

- consumer: 20 MD + 1 JSON, 0 PNG;
- asset host: 49 PNG, 0 MD;
- 49 key/49 URI MinIO duy nhất;
- 60 MinIO + 60 `LOCAL_ASSET`;
- không có folder `knowledge-vng/`, `tmp/`, `outputs/` hoặc `audit-upload-folder/` ở root.

## Trạng thái live

Không có thao tác live trong đợt chuẩn hóa này. Ba module local được sửa SOP cần quy trình phát hành/chat-test riêng nếu muốn cập nhật nội dung trên Web; snapshot live gần nhất vẫn là audit ngày 12/08/2026.
