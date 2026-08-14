# Task 2: Ghi trạng thái và bàn giao phiên tiếp theo

## Global constraints

- Thư mục đích chính xác: `J:\My Drive\AI\Knowledge Base VNG`.
- Nguồn nội dung chuẩn duy nhất: `so-tay-tao-knowledge-base-v3.md`, phiên bản `3.0.1`, cập nhật `06/08/2026`.
- Không sửa trực tiếp 12 file sinh trong `knowledge-vng/` hoặc HTML sinh tự động.
- Giữ nguyên 14 ảnh local và 14 URI trong `knowledge-vng/image-map.json`.
- Không thay đổi hoặc xóa dữ liệu ngoài hai KB test được ghi trong audit.
- Mọi trạng thái live phải có ngày kiểm chứng và liên kết bằng chứng.
- Workspace không phải Git repository; không tạo commit hay worktree.

## Files

- Create: `STATUS.md`
- Create: `HANDOFF.md`
- Read: `audit/audit-knowledge-vng-2026-08-06.md`
- Read: `so-tay-tao-knowledge-base-v3.md`
- Read: `tests/test_build_handbook.py`
- Read: `docs/superpowers/specs/2026-08-06-project-handoff-docs-design.md`

## Interfaces

- Consumes: kết quả audit ngày 06/08/2026, số lượng artifact và kết quả kiểm tra hiện có.
- Produces: ảnh chụp trạng thái có ngày và hướng dẫn tiếp tục có thứ tự ưu tiên.

## Required facts

- Master: phiên bản `3.0.1`, cập nhật `06/08/2026`, 1.078 dòng.
- Output: 12 module Markdown, 14 ảnh local, 14 mapping MinIO, HTML offline 2.379.085 byte trước lượt build kiểm chứng cuối.
- Test tự động hiện có: 7.
- Graph cuối ngày 06/08/2026: 159/159 node; Tóm tắt 22, Thực thể 66, Khái niệm 70, Tổng hợp 0, So sánh 0.
- Chỉ còn `11-faq-danh-sach-nhap-xuat-tim-kiem.png` hiển thị `Đang hoàn tất`; chat vẫn truy hồi được chunk/URI và Wiki báo đang xử lý một tài liệu.
- FAQ test đã phục hồi về model `qwen3.6-plus`, chế độ `Chỉ câu hỏi + Tách`.
- Document test đang dùng Wiki mức `Toàn diện`; tài liệu MANUAL đã phục hồi đúng nội dung gốc.
- Document KB: `Test Doc RAG+Wiki`, ID `8902e4d0-4884-4be7-a54b-1d193bf8506a`, tenant `10012`.
- FAQ KB: `Test 2 chỉ câu hỏi + tách`, ID `73de52af-6511-468e-94bb-cca61c670b31`, tenant `10012`.

## Required work

1. Tạo `STATUS.md` với ngày trạng thái, tóm tắt hoàn tất, inventory artifact, snapshot live, bằng chứng kiểm tra, bốn nhóm backlog và ưu tiên tiếp theo. Phân biệt rõ trạng thái có thể thay đổi với kết luận bền vững.
2. Tạo `HANDOFF.md` với trạng thái `baseline hoàn tất, không có tác vụ triển khai đang mở`; thứ tự đọc; lệnh kiểm tra đầu phiên; bốn việc tiếp theo theo mức ưu tiên; điều kiện cần quyền/credential; checklist trước/sau chỉnh sửa; bẫy không sửa file sinh và không xóa nguồn ảnh MinIO.
3. `HANDOFF.md` phải trỏ tới `STATUS.md`, `PROJECT.md`, `DECISIONS.md`, `AGENTS.md`, master và audit. `STATUS.md` phải trỏ tới audit/evidence thay vì sao chép toàn bộ bằng chứng.
4. Bốn backlog phải giữ nguyên trạng thái chưa xác thực:
   - Upload thư mục thật và cấu trúc thư mục con.
   - Điều kiện sinh node Tổng hợp/So sánh.
   - Bước 3–4 của connector khi có credential.
   - Hành vi đồng bộ thêm/sửa/đổi tên/xóa/quyền ở Notion, Drive, NAS.

## Report contract

Viết báo cáo đầy đủ tại `docs/superpowers/reports/task-2-status-handoff-docs-report.md`, gồm: nội dung đã tạo, kiểm tra đã chạy, file đã đổi, tự rà soát và mọi lo ngại. Trong phản hồi cuối chỉ ghi trạng thái, tóm tắt kiểm tra, lo ngại và đường dẫn báo cáo.
