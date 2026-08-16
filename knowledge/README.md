# Knowledge trên VNG AI

Mỗi folder con thường tương ứng một Knowledge Base đang được quản lý trên Web và giữ nguyên tên chính thức của KB đó. Các bộ local-only phải được ghi rõ, không mặc định là đã upload.

- `GS9 Knowledge VNG AI`: mirror phát hành của consumer; 20 Markdown sinh tự động và `image-map.json`.
- `GS9 Knowledge VNG - Image Assets`: 49 PNG cấp URI MinIO cho ảnh trong sổ tay.
- Các folder `GS9 CFL ...`: dữ liệu của các KB CFL khác; không tự động trộn vào consumer tài liệu.
- `GS9 CFL Plan Version/V5`: bộ chuyển đổi local-only từ HTML kế hoạch CFL 5.0; gồm 12 Markdown, 29 JPEG và `source-manifest.json`; chưa upload/bind trên Web.

Không sửa trực tiếp 20 module trong consumer. Nội dung sổ tay được sửa tại `../so-tay-tao-knowledge-base-v3.md` rồi sinh bằng `../scripts/build_handbook.py`.
