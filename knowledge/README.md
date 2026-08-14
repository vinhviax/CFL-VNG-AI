# Knowledge trên VNG AI

Mỗi folder con tương ứng một Knowledge Base đang được quản lý trên Web và giữ nguyên tên chính thức của KB đó.

- `GS9 Knowledge VNG AI`: mirror phát hành của consumer; 20 Markdown sinh tự động và `image-map.json`.
- `GS9 Knowledge VNG - Image Assets`: 49 PNG cấp URI MinIO cho ảnh trong sổ tay.
- Các folder `GS9 CFL ...`: dữ liệu của các KB CFL khác; không tự động trộn vào consumer tài liệu.

Không sửa trực tiếp 20 module trong consumer. Nội dung sổ tay được sửa tại `../so-tay-tao-knowledge-base-v3.md` rồi sinh bằng `../scripts/build_handbook.py`.
