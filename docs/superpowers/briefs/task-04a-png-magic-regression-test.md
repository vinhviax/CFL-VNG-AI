# Task 04A — Regression test cho định dạng asset PNG

## Bối cảnh đã xác minh

- Ảnh 01–14 mang đuôi `.png` nhưng magic bytes là JPEG/JFIF.
- Ảnh 15–25 là PNG thật.
- KB asset vì vậy sinh nhiều URI `.jpg` cho ảnh 01 thay vì một URI `.png` gốc duy nhất.

## Phạm vi sở hữu

- Chỉ sửa `tests/test_build_handbook.py` và report task này.
- Không sửa asset, image map, master hoặc live KB.
- Không hoàn tác thay đổi ngoài phạm vi.

## Yêu cầu RED

1. Thêm một test tích hợp tên rõ ràng `test_local_png_assets_have_png_signature`.
2. Với mọi file `knowledge-vng/assets/*.png`, đọc 8 byte đầu và so sánh với signature PNG `b"\x89PNG\r\n\x1a\n"`.
3. Failure phải nêu filename gây sai để sửa được tại nguồn.
4. Chạy riêng test mới và xác nhận nó **FAIL** đúng vì ít nhất ảnh `01` là JPEG.
5. Không sửa production data để làm test xanh.
6. Dùng `apply_patch` cho chỉnh sửa text.

## Báo cáo

Tạo `docs/superpowers/reports/task-04a-test-red.md` với trạng thái `RED CONFIRMED`, file đã sửa, lệnh/kết quả và nguyên nhân failure.
