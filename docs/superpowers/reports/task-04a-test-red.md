# Task 04A — PNG magic regression test

**Trạng thái:** RED CONFIRMED

## File đã sửa

- `tests/test_build_handbook.py`
- `docs/superpowers/reports/task-04a-test-red.md`

## Lệnh kiểm thử riêng

```powershell
python -m unittest -v tests.test_build_handbook.BuildHandbookTests.test_local_png_assets_have_png_signature
```

## Kết quả

- Exit code: `1`
- `Ran 1 test`
- `FAILED (failures=1)`
- Failure chỉ rõ file: `01-tong-quan-danh-sach-knowledge.png`
- Giá trị thực tế: `b'\xff\xd8\xff\xe0\x00\x10JF'`
- Giá trị mong đợi: `b'\x89PNG\r\n\x1a\n'`

## Nguyên nhân failure

File `01-tong-quan-danh-sach-knowledge.png` mang đuôi `.png` nhưng 8 byte đầu bắt đầu bằng magic bytes JPEG/JFIF, không phải signature PNG. Test vì vậy FAIL đúng mục tiêu hồi quy và nêu filename cần được sửa tại nguồn.

Không sửa asset, `knowledge-vng/image-map.json`, master hoặc dữ liệu live để làm test xanh.
