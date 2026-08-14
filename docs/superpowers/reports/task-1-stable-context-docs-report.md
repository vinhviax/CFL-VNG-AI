# Báo cáo Task 1 — Tài liệu bối cảnh và quy tắc ổn định

## Nội dung đã tạo

- [AGENTS.md](../../../AGENTS.md): quy tắc áp dụng toàn workspace, thứ tự đọc bắt đầu từ `HANDOFF.md`, nguồn chuẩn, vùng sửa, an toàn live, quy trình master → build → test → audit/status, lệnh và tiêu chí hoàn tất.
- [PROJECT.md](../../../PROJECT.md): mục tiêu, đối tượng dùng, năm nhóm đầu ra, luồng master → 12 module/HTML, cây thư mục, chiến lược ảnh, hai KB test/tenant và giới hạn phạm vi.
- [DECISIONS.md](../../../DECISIONS.md): tám quyết định DEC-001 đến DEC-008, mỗi quyết định có ngày 06/08/2026, trạng thái và hệ quả bảo trì.

Không file nào trên nhận vai trò nguồn nghiệp vụ: nguồn chuẩn vẫn là [so-tay-tao-knowledge-base-v3.md](../../../so-tay-tao-knowledge-base-v3.md).

## Kiểm tra đã chạy

- Đọc master để đối chiếu phiên bản `3.0.1`, ngày `06/08/2026`, 12 module, quy tắc phân loại trạng thái và chiến lược ảnh.
- Đọc [scripts/build_handbook.py](../../../scripts/build_handbook.py) để xác nhận luồng sinh 12 module/HTML và điều kiện build MinIO.
- Đọc [knowledge-vng/image-map.json](../../../knowledge-vng/image-map.json) để xác nhận 14 mapping URI MinIO cho `Test Doc RAG+Wiki`; không dùng file này làm bằng chứng cho KB FAQ.
- Đọc [audit/audit-knowledge-vng-2026-08-06.md](../../../audit/audit-knowledge-vng-2026-08-06.md) để đối chiếu hai KB test được phép thao tác, định danh route đã quan sát và các ràng buộc an toàn live.
- Đọc brief và thiết kế bàn giao để kiểm tra phân vai: chỉ dẫn ở `AGENTS.md`, bối cảnh ổn định ở `PROJECT.md`, lý do quyết định ở `DECISIONS.md`.
- Kiểm tra filesystem/JSON sau khi ghi: đủ 4 file thuộc Task 1; `MODULES=12`, `ASSETS=14`, `MINIO_MAPPINGS=14`, master `3.0.1`/`06/08/2026`, `DECISIONS=8` và cả ba tài liệu bối cảnh đều dẫn chiếu master.
- Chạy `python -m unittest discover -s tests -v`: 7/7 test đạt, kết thúc `Ran 7 tests` và `OK`. Test dùng thư mục tạm; không ghi module hoặc HTML của workspace.
- Kiểm tra các liên kết Markdown của bốn file Task 1: chỉ có 2 target chưa tồn tại là `AGENTS.md → HANDOFF.md` và `AGENTS.md → STATUS.md`; đây là hai file thuộc Task 2 theo contract, không phải link sai đường dẫn.

## File đã thay đổi

- `AGENTS.md` (tạo mới)
- `PROJECT.md` (tạo mới)
- `DECISIONS.md` (tạo mới)
- `docs/superpowers/reports/task-1-stable-context-docs-report.md` (tạo mới)

## Tự rà soát

- `AGENTS.md` chỉ chứa quy tắc và quy trình; không sao chép nội dung nghiệp vụ của sổ tay.
- `PROJECT.md` chỉ mô tả bối cảnh/cấu trúc ổn định; trạng thái live được dẫn chiếu về audit có ngày.
- `DECISIONS.md` chỉ ghi quyết định, trạng thái và hệ quả bảo trì.
- Cả ba file đều khẳng định master là nguồn chuẩn và cấm sửa trực tiếp 12 module/HTML sinh tự động.

## Lo ngại và phụ thuộc

- `HANDOFF.md` và `STATUS.md` chưa tồn tại ở thời điểm Task 1; hai liên kết chưa phân giải của `AGENTS.md` là contract cho Task 2. Task 1 không có quyền tạo chúng.
- Đã chạy đầy đủ `python -m unittest discover -s tests -v`: 7/7 test đạt. Chỉ strict project build `python scripts\build_handbook.py` chưa chạy trong Task 1, vì lệnh này sẽ ghi lại 12 module và HTML — ngoài phạm vi ownership của Task 1.

## Sửa theo review và kiểm tra sau sửa

- Audit hiện ghi type, KB ID và tenant `10012` cho từng KB test, với nguồn quan sát là route của phiên audit 06/08/2026.
- `PROJECT.md` hiện liệt kê từng KB cùng type, ID, tenant và liên kết audit; đã bỏ nhận định sai rằng `image-map.json` xác nhận KB FAQ.
- Đã rà soát lại report để tách rõ full unittest đã chạy/đạt khỏi strict project build chưa chạy.
