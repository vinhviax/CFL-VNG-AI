# Task 04A — Review PNG magic regression test

**Kết luận:** APPROVED  
**Cho phép bước transcode:** CÓ

## Đánh giá

Không có blocker, suggestion bắt buộc hoặc nit ảnh hưởng đến bước tiếp theo.

- Test có đúng tên `test_local_png_assets_have_png_signature`.
- Test duyệt toàn bộ `knowledge-vng/assets/*.png`, đọc đúng 8 byte đầu và so sánh với PNG signature `b"\x89PNG\r\n\x1a\n"`.
- Assertion dùng `asset_path.name`, nên failure nêu rõ filename cần sửa tại nguồn.
- Không có thay đổi implementation hoặc production data trong phạm vi review này.

## Kiểm chứng RED độc lập

Lệnh đã chạy:

```powershell
python -m unittest -v tests.test_build_handbook.BuildHandbookTests.test_local_png_assets_have_png_signature
```

Kết quả:

- Exit code: `1`
- `Ran 1 test`
- `FAILED (failures=1)`
- Failure nêu rõ `01-tong-quan-danh-sach-knowledge.png does not have a PNG signature`.
- Giá trị thực tế là `b'\xff\xd8\xff\xe0\x00\x10JF'`, khác PNG signature mong đợi.
- Kiểm tra thêm 12 byte đầu cho kết quả `FF-D8-FF-E0-00-10-4A-46-49-46-00-01`, xác nhận file mang magic JPEG/JFIF dù có đuôi `.png`.

Regression test vì vậy đang RED đúng nguyên nhân và đủ rõ filename. Task 04A được phê duyệt; có thể chuyển sang bước transcode asset.
