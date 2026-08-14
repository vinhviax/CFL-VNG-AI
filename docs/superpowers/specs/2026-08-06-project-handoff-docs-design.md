# Thiết kế bộ tài liệu bối cảnh và bàn giao dự án Knowledge Base VNG

Ngày chốt thiết kế: 06/08/2026  
Phạm vi: `J:\My Drive\AI\Knowledge Base VNG`

## Bối cảnh

Dự án đã hoàn thiện bản sổ tay nguồn, 12 module Markdown dùng để nạp vào Knowledge VNG, bản HTML chạy hoàn toàn offline, bộ mẫu FAQ/DOC, ảnh minh họa và nhật ký kiểm chứng giao diện thật. Agent tiếp theo cần hiểu nhanh ba lớp thông tin khác nhau: dự án là gì, trạng thái hiện tại ra sao và phải làm việc theo quy tắc nào.

## Mục tiêu

Tạo một bộ tài liệu ở thư mục gốc để agent mới có thể:

1. Xác định đúng nguồn chuẩn và các artifact sinh tự động.
2. Nắm được những gì đã hoàn tất, bằng chứng kiểm tra và phần còn tồn đọng.
3. Tiếp tục công việc mà không sửa nhầm file sinh tự động hoặc tác động dữ liệu ngoài phạm vi test.
4. Biết chính xác lệnh build, test và các bước cập nhật tài liệu bàn giao sau mỗi phiên làm việc.

## Các phương án đã cân nhắc

### Phương án A — Ba file tối thiểu

Chỉ dùng `AGENTS.md`, `STATUS.md` và `HANDOFF.md`. Số file ít nhưng phần tổng quan dự án, quyết định kiến trúc và trạng thái dễ bị trộn lẫn, khiến tài liệu nhanh dài và khó cập nhật độc lập.

### Phương án B — Năm file chuyên trách

Dùng `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `HANDOFF.md` và `DECISIONS.md`. Mỗi file có một trách nhiệm rõ ràng, giảm trùng lặp và cho phép agent đọc theo nhu cầu. Đây là phương án được chọn.

### Phương án C — Một file bàn giao duy nhất

Đơn giản khi mở lần đầu nhưng có nguy cơ trở thành tài liệu nguyên khối, lặp lại nội dung sổ tay và khó phân biệt thông tin ổn định với ảnh chụp trạng thái theo thời điểm.

## Thiết kế được chọn

### `AGENTS.md` — Cách làm việc

Áp dụng cho toàn workspace. File này quy định thứ tự đọc, nguồn chuẩn, vùng được phép sửa, quy tắc an toàn với Knowledge VNG, lệnh build/test và tiêu chí hoàn tất. Nội dung tập trung vào chỉ dẫn bắt buộc, không kể lại lịch sử dự án.

### `PROJECT.md` — Dự án là gì

Mô tả mục tiêu, đối tượng sử dụng, các đầu ra, luồng sinh artifact, cây thư mục và chiến lược ảnh. Đây là thông tin tương đối ổn định, chỉ đổi khi phạm vi hoặc kiến trúc dự án thay đổi.

### `STATUS.md` — Dự án đang ở đâu

Ghi ảnh chụp trạng thái có ngày: phiên bản, số lượng artifact, kết quả build/test, trạng thái hai KB test, các phép thử live và backlog còn lại. Mọi dữ liệu có thể thay đổi trên giao diện phải kèm ngày kiểm chứng.

### `HANDOFF.md` — Agent kế tiếp làm gì

Là điểm vào nhanh nhất. File nêu thứ tự đọc, tình trạng phiên bàn giao, các việc tiếp theo theo ưu tiên, quy trình bắt đầu/kết thúc một phiên và các bẫy thường gặp. File không sao chép toàn bộ trạng thái; nó liên kết sang `STATUS.md` và nhật ký audit.

### `DECISIONS.md` — Vì sao dự án làm như hiện tại

Lưu các quyết định bền vững: master Markdown là nguồn chuẩn, chia 12 module, HTML một file offline, ảnh dùng hai đường dẫn local/MinIO, chỉ thử trên KB test và giữ nguồn ảnh còn được tham chiếu. Mỗi quyết định có ngày, trạng thái và hệ quả bảo trì.

## Luồng đọc và nguồn dữ liệu

Agent mới bắt đầu ở `HANDOFF.md`, sau đó đọc `STATUS.md`, `PROJECT.md`, `DECISIONS.md` và tuân thủ `AGENTS.md`. Khi cần chi tiết nghiệp vụ, agent đọc `so-tay-tao-knowledge-base-v3.md`; khi cần bằng chứng live, agent đọc `audit/audit-knowledge-vng-2026-08-06.md`.

Nguồn chuẩn của nội dung sổ tay vẫn là `so-tay-tao-knowledge-base-v3.md`. Năm file bàn giao không trở thành nguồn thay thế và không được dùng để sửa trực tiếp 12 module sinh trong `knowledge-vng/`.

## Quy tắc đồng bộ

- Thay đổi nội dung sổ tay: sửa master, cập nhật ảnh/map nếu cần, chạy build và test, rồi cập nhật `STATUS.md` cùng `HANDOFF.md`.
- Thay đổi quyết định kiến trúc hoặc chính sách: cập nhật `DECISIONS.md`, sau đó điều chỉnh `AGENTS.md` nếu quy trình làm việc bị ảnh hưởng.
- Kết quả kiểm chứng live mới: cập nhật audit trước, rồi tóm tắt trạng thái mới trong `STATUS.md` với ngày cụ thể.
- Khi bàn giao: ghi rõ việc đã làm, việc chưa làm, bằng chứng và bước tiếp theo trong `HANDOFF.md`; không ghi trạng thái suy đoán như sự thật.

## Kiểm chứng

Bộ tài liệu đạt yêu cầu khi:

1. Cả năm file tồn tại ở thư mục gốc và liên kết chéo tới các file thật.
2. Các số liệu khớp với workspace: phiên bản 3.0.1, 12 module, 14 ảnh, 14 mapping MinIO và 7 test tự động.
3. Không có chỉ dẫn sửa trực tiếp artifact sinh tự động.
4. Backlog giữ đúng bốn nhóm chưa xác thực và không biến chúng thành kết luận đã kiểm chứng.
5. Build nghiêm ngặt và toàn bộ test hiện có chạy thành công sau khi tạo tài liệu.

## Phê duyệt

Người dùng đã chỉ dẫn chấp thuận toàn bộ lựa chọn mặc định trước đó. Vì vậy phương án B và các quy ước đặt tên ở trên được xem là đã phê duyệt để triển khai trong cùng phiên.
