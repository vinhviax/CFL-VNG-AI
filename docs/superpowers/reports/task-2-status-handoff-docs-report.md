# Báo cáo Task 2 — Status và handoff documents

**Ngày:** 06/08/2026  
**Phạm vi được sở hữu:** `STATUS.md`, `HANDOFF.md` và báo cáo này.

## Nội dung đã tạo

- `STATUS.md`: snapshot ngày 06/08/2026, tóm tắt baseline, inventory artifact, dẫn chiếu evidence audit, trạng thái hai KB test, Graph/ảnh có thể đổi, bốn nhóm backlog và ưu tiên phiên sau.
- `HANDOFF.md`: nêu rõ baseline hoàn tất/không có tác vụ triển khai mở; thứ tự đọc, lệnh kiểm tra đầu phiên, bốn việc theo ưu tiên, điều kiện quyền/credential, checklist trước-sau chỉnh sửa và các bẫy về artifact sinh/ảnh MinIO.
- Cả hai file liên kết tới tài liệu vận hành, master và audit theo contract; trạng thái live được tách khỏi quy ước bền vững.

## Sửa theo reviewer

- Tách việc kiểm tra lại ảnh `11-faq-danh-sach-nhap-xuat-tim-kiem.png` và trạng thái Wiki thành mục **Theo dõi đầu phiên (không phải backlog)** ở cả hai file.
- Đồng bộ backlog theo cùng một bảng và cùng nhãn: P1 upload thư mục/cấu trúc con; P2 điều kiện node Tổng hợp/So sánh; P3 bước 3–4 connector khi có credential test; P4 ma trận đồng bộ sau khi connector hoạt động.
- Không còn gộp connector và đồng bộ: P4 nêu rõ phụ thuộc hoàn tất P3.
- Làm rõ trong `HANDOFF.md` rằng builder là thao tác ghi tái sinh 12 module/HTML; nhiệm vụ chỉ đọc phải dùng báo cáo gần nhất và các check filesystem/liên kết không ghi. Build chỉ được chạy khi scope cho phép ghi artifact hoặc khi thay đổi nguồn cần tái sinh; test chỉ chạy khi verification nằm trong scope.
- Chuẩn hóa taxonomy cho dòng ảnh hướng dẫn trong `STATUS.md` thành **Đã kiểm chứng ngày 06/08/2026; trạng thái live có thể thay đổi**.
- Đổi checklist sau sửa thành câu có điều kiện: nếu thay đổi nội dung sổ tay thì chỉ sửa master và giữ đủ 12 cặp marker `MODULE`.

## Kiểm tra đã chạy

- Đọc và đối chiếu: brief Task 2, `AGENTS.md`, `PROJECT.md`, `DECISIONS.md`, `audit/audit-knowledge-vng-2026-08-06.md`, master, thiết kế bàn giao và `tests/test_build_handbook.py`.
- Đối chiếu trực tiếp workspace: master v3.0.1 ngày 06/08/2026 có 1.078 dòng; có 12 module Markdown, 14 ảnh local, 14 mapping MinIO và HTML offline 2.379.085 byte; source test định nghĩa 7 test.
- Đã chạy `python -m unittest discover -s tests -v`: `Ran 7 tests` và `OK`.
- Kiểm tra liên kết Markdown nội bộ trong ba file tạo mới: tất cả target hợp lệ. Không chạy build nghiêm ngặt vì lệnh này ghi lại 12 module và HTML sinh tự động, nằm ngoài ba file được giao sở hữu; kết quả build được ghi trong STATUS là evidence từ audit ngày 06/08/2026.
- Focused check sau sửa reviewer: đối chiếu hai bảng backlog từng cột, xác nhận P1–P4 có thứ tự và nhãn giống hệt; xác nhận ảnh/Wiki chỉ nằm trong mục theo dõi đầu phiên, không mang mã backlog.
- Focused check whole-project review: xác nhận liên kết nội bộ hợp lệ, P1–P4 tiếp tục khớp, taxonomy ảnh đúng nguyên văn, hướng dẫn read-only không chạy build và checklist master dùng câu điều kiện. Không chạy build hoặc Git.

## File đã đổi

- `STATUS.md` — tạo mới.
- `HANDOFF.md` — tạo mới.
- `docs/superpowers/reports/task-2-status-handoff-docs-report.md` — tạo mới.

Không sửa master, artifact sinh, ảnh, mapping MinIO, audit, test hoặc tài liệu vận hành khác.

## Tự rà soát

- Có đủ bốn backlog bắt buộc và đều giữ nhãn chưa xác thực/bị chặn.
- P3 và P4 được tách thành hai hạng mục tuần tự, không còn gộp connector với đồng bộ.
- Có đầy đủ ID và tenant của hai KB test, snapshot Graph 159/159 và tình trạng còn một ảnh đang xử lý.
- `HANDOFF.md` dẫn tới `STATUS.md`, `PROJECT.md`, `DECISIONS.md`, `AGENTS.md`, master và audit.
- `STATUS.md` dẫn về audit/evidence thay vì sao chép đầy đủ bằng chứng.

## Lo ngại còn lại

- Trạng thái `Đang hoàn tất` của ảnh FAQ và thông báo Wiki là trạng thái live có thể đã thay đổi sau 06/08/2026; chưa kiểm tra live lại trong Task 2.
- Bốn hạng mục backlog vẫn cần điều kiện kỹ thuật hoặc credential test để kiểm chứng.
