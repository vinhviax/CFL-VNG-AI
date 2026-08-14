# Thiết kế KB lưu ảnh riêng cho Knowledge VNG

**Ngày:** 07/08/2026  
**Trạng thái:** Đã triển khai và kiểm chứng ngày 07/08/2026  
**KB lưu ảnh:** `Knowledge VNG - Image Assets` — ID `6da8657c-dd96-4170-a698-074043475014`, tenant `10012`  
**KB sử dụng:** `Knowledge VNG AI` — ID `cefadf09-4187-46ac-a765-591e3255a4a4`, tenant `10012`

## Bối cảnh

Bộ phân phối có 13 file Markdown và 25 ảnh local. Markdown dùng URI `minio://` để Knowledge VNG render ảnh trong chat; HTML offline dùng ảnh local. KB từng giữ 14 ảnh cũ là `Test Doc RAG+Wiki` đã bị xóa. Mười một ảnh Google Drive mới hiện đang nằm trực tiếp trong `Knowledge VNG AI`, làm KB sử dụng có 24 tài liệu thay vì chỉ 13 file Markdown.

Không được giả định URI từ KB đã xóa sẽ tồn tại bền vững. Toàn bộ 25 ảnh phải được chuyển sang một KB asset ổn định và toàn bộ URI phải được cấp lại từ KB đó.

## Mục tiêu

- `Knowledge VNG - Image Assets` giữ đúng 25 ảnh nguồn và tồn tại lâu dài.
- `Knowledge VNG AI` cuối cùng chỉ giữ đúng 13 file Markdown.
- Cả 13 Markdown chỉ dùng URI MinIO đang thuộc KB asset mới; không dùng đường dẫn `assets/...` làm liên kết ảnh hoạt động.
- HTML offline tiếp tục nhúng 25 ảnh local và không phụ thuộc Internet.
- Master ghi rõ quy trình hai KB để agent hoặc human sau này không upload PNG vào KB sử dụng.
- Việc thay link và dọn ảnh chỉ diễn ra theo thứ tự an toàn, không tạo khoảng thời gian Markdown trỏ vào ảnh đã bị xóa.

## Ngoài phạm vi

- Không chuyển sang Google Drive hoặc URL HTTPS làm nơi host ảnh trong lượt này.
- Không thay nội dung nghiệp vụ của 13 module ngoài phần hướng dẫn lưu và nạp ảnh.
- Không xóa KB asset hoặc ảnh trong KB asset sau khi phát hành.
- Không thay model, parser, chunking, Wiki hoặc Graph của `Knowledge VNG AI` ngoài yêu cầu tối thiểu để xử lý lại file được thay.

## Kiến trúc

```text
knowledge-vng/assets/*.png
        │
        │ upload một lần
        ▼
Knowledge VNG - Image Assets
        │
        │ 25 URI minio://
        ▼
knowledge-vng/image-map.json
        │
        │ strict build
        ├──────────────► knowledge-vng/00–12.md
        │                         │
        │                         │ upload chỉ Markdown
        │                         ▼
        │                Knowledge VNG AI
        │
        └──────────────► so-tay-tao-knowledge-base.html
                          dùng ảnh local/data URI
```

KB asset là nơi sở hữu vòng đời ảnh. KB sử dụng chỉ tiêu thụ URI qua Markdown. Hai KB cùng tenant `10012`, nhưng không phụ thuộc vào việc ảnh xuất hiện như tài liệu trong KB sử dụng.

## Quy tắc nội dung phải được ghi vào master

Master `so-tay-tao-knowledge-base-v3.md` phải nói rõ:

1. Ảnh local và ảnh MinIO có hai vai trò khác nhau.
2. KB asset giữ ảnh; KB sử dụng chỉ nhận Markdown.
3. Không upload thư mục `assets/` hoặc các PNG cùng gói Markdown vào KB sử dụng.
4. Mọi Markdown phân phối phải dùng URI `minio://` đã kiểm chứng; `LOCAL_ASSET` chỉ là metadata để dựng HTML offline.
5. Không xóa ảnh hoặc KB asset khi còn Markdown tham chiếu.
6. Khi chuyển nơi lưu ảnh, thứ tự bắt buộc là: tạo host mới → upload ảnh → lấy URI → cập nhật mapping → build → thay Markdown → kiểm thử chat → xóa ảnh ở host cũ/KB sử dụng.
7. Nếu KB asset cũ bị xóa, phải coi toàn bộ mapping liên quan là cần tái kiểm chứng, kể cả khi một số link vẫn tạm thời render.

Nội dung này phải xuất hiện trong các module sinh liên quan:

- `01-chuan-bi-noi-dung.md`: giải thích hai đường ảnh và hai vai trò KB.
- `09-van-hanh-documents-wiki-graph.md`: checklist nạp một bộ Markdown có ảnh; chỉ nạp MD vào KB sử dụng.
- `11-chat-kiem-thu-va-bao-tri.md`: quy trình host, kiểm thử và cấm xóa asset.

Không sửa trực tiếp ba module này; sửa master rồi để builder sinh lại.

## Dòng dữ liệu và di chuyển live

1. Xác nhận `Knowledge VNG - Image Assets` đang trống và đúng tenant/owner.
2. Upload 25 file trong `knowledge-vng/assets/` vào KB asset.
3. Với từng ảnh, lấy URI MinIO đầy đủ và đối chiếu chính xác theo tên file.
4. Lưu snapshot mapping cũ vào audit trước khi thay; cập nhật `knowledge-vng/image-map.json` thành 25 URI mới và provenance của KB asset.
5. Bổ sung test hồi quy cho hai điều kiện: mapping phủ đủ 25 asset và không module nào có liên kết ảnh hoạt động dạng `assets/...`.
6. Chạy strict build để sinh lại 13 Markdown và HTML offline; không dùng `--allow-missing-minio`.
7. Trong `Knowledge VNG AI`, thay từng file Markdown bằng bản mới. Chỉ gỡ bản cũ sau khi bản mới cùng tên đã có chunk/vector và mở được.
8. Kiểm thử chat ít nhất ba nhóm ảnh: ảnh giao diện tổng quan, ảnh chứng minh đường tương đối không render, và ảnh Google Drive.
9. Mở nguồn tham khảo để xác nhận chunk Markdown dùng URI thuộc KB asset mới, không phải URI cũ hoặc `assets/...`.
10. Chỉ sau khi toàn bộ 13 Markdown đã qua kiểm thử mới xóa 11 PNG hiện nằm trong `Knowledge VNG AI`.
11. Xác nhận trạng thái cuối: KB asset có 25 ảnh; KB sử dụng có 13 Markdown và không có PNG.

## An toàn và phục hồi

- Không xóa 11 PNG trong `Knowledge VNG AI` trước khi 25 URI mới và 13 Markdown mới đã được kiểm thử.
- Không dùng thao tác xóa hàng loạt nếu không thể phân biệt chính xác PNG và Markdown.
- Mỗi lần thay Markdown phải phân biệt bản mới/bản cũ bằng dung lượng, thời gian tải lên và trạng thái xử lý.
- Nếu bất kỳ ảnh nào không render từ URI mới, dừng việc dọn PNG; giữ nguyên trạng thái live và sửa mapping trước.
- Asset local trong workspace là nguồn phục hồi; không xóa hoặc đổi tên trong lượt di chuyển.
- Workspace hiện không phải Git repository, nên audit có ngày, snapshot mapping và kết quả test là hồ sơ phục hồi bắt buộc thay cho commit.

## Kiểm thử và tiêu chí chấp nhận

### Local

- `python scripts\build_handbook.py` trả exit code `0`, báo `Build complete` và đúng 13 module.
- `python -m unittest discover -s tests -v` đạt toàn bộ test hiện có và test mới.
- `image-map.json` có đúng 25 tên asset và 25 URI MinIO duy nhất thuộc KB asset mới.
- Mỗi ảnh trong module có một `LOCAL_ASSET` comment và một liên kết MinIO; không có liên kết ảnh hoạt động dạng `assets/...` ngoài code fence minh họa.
- HTML offline mở được và hiển thị đủ ảnh khi không có Internet.

### Live

- Câu hỏi về ít nhất ba ảnh trả lời kèm đúng hình.
- Nguồn tham khảo của câu trả lời chứa Markdown mới và URI MinIO mới.
- `Knowledge VNG AI` cuối cùng có 13 Markdown, không có PNG.
- `Knowledge VNG - Image Assets` có 25 ảnh và được ghi là dependency không được xóa.

## Tài liệu dự án cần cập nhật sau khi hoàn tất

- `audit/audit-google-drive-connector-2026-08-07.md` hoặc một audit di chuyển ảnh riêng có đầy đủ KB ID, mapping và bằng chứng chat.
- `AGENTS.md`, `PROJECT.md`, `DECISIONS.md`, `STATUS.md` và `HANDOFF.md` phải ghi kiến trúc hai KB, trạng thái 25/25 mapping và quy tắc không xóa KB asset.
- `knowledge-vng/image-map.json` phải ghi provenance duy nhất là `Knowledge VNG - Image Assets` cho ảnh 01–25.

## Trạng thái cuối mong đợi

```text
Knowledge VNG - Image Assets
└── 25 PNG (dependency lâu dài)

Knowledge VNG AI
└── 13 Markdown (00–12)
```

Không còn ảnh độc lập trong KB sử dụng; file `12-ket-noi-google-drive.md` vận hành giống các file `00–11`.

## Kết quả triển khai

- Asset KB đạt 25 PNG, 0 MD; consumer đạt 13 MD, 0 PNG.
- 25 URI MinIO mới đã được ghi vào `knowledge-vng/image-map.json` và strict build đã sinh 13 module cùng HTML offline.
- Ba phép thử chat trước cleanup và một phép thử hậu-cleanup đều render ảnh; nguồn hậu-cleanup chỉ còn Markdown.
- Audit tổng hợp: `audit/audit-image-assets-migration-2026-08-07.md`.
