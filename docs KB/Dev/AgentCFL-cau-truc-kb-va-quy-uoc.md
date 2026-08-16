# AgentCFL — cấu trúc KB và quy ước: bản đối chiếu với meta-KB

**Ngày viết:** 16/08/2026. **Đối tượng:** Dev và Agent config.

File này **cố tình ngắn**. Ba trang `doc-30`→`doc-32` trong `knowledge/GS9 CFL Knowledge Agent/` là bản rút gọn 15/08/2026 của những tài liệu đã có bản đầy đủ và mới hơn trong `docs KB/Dev/`. Chép lại sẽ tạo hai nguồn cùng nội dung khác ngày — đúng cái lỗi mà DEC-038 cấm.

File này làm ba việc: **chỉ đường**, **ghi ba điểm meta-KB có mà nơi khác chưa có**, và **ghi hai sai số** phát hiện khi đối chiếu.

---

## 1. Bản đầy đủ nằm ở đâu

| Trang meta-KB | Nội dung | Bản canonical, đầy đủ hơn |
|---|---|---|
| `doc-30-cau-truc-kb-cfl.md` | Bản đồ 7 tầng L0–L7, 7 nguyên tắc quy hoạch, ràng buộc nền tảng | `KB-quy-hoach-nghiep-vu-7-tang.md` mục 2–4 |
| `doc-31-ban-chat-tung-kb.md` | Bảng "bản chất" từng KB, lý do không đổi tên KB | `KB-quy-hoach-nghiep-vu-7-tang.md` mục 5 (DEC-037) |
| `doc-32` phần đặt tên | Tiền tố `doc-` / `image-`, chèn số phiên bản `doc-v5-NN-` | `KB-quy-uoc-dat-ten-va-hop-dong-artifact.md` mục 4 (DEC-042, DEC-047) |
| `doc-32` phần nhúng ảnh | Cú pháp `LOCAL_ASSET` + URI `minio://`, ảnh render hai lần | `KB-anh-va-uri-minio.md` mục 3 và 6 (DEC-041) |
| `doc-32` phần ba biện pháp cho KB nhiều phiên bản | Nhãn `ver:vN`, header phiên bản trong nội dung, guardrail G-A | `KB-quy-hoach-nghiep-vu-7-tang.md` mục 7 và 8 (DEC-040) |

**Nguồn gốc chung của cả ba trang:** `docs/superpowers/specs/2026-08-15-kb-architecture-design.md`. Khi hai bản lệch nhau, spec và các file `KB-*.md` thắng — chúng được cập nhật tiếp sau 15/08, ba trang meta-KB thì không.

---

## 2. Ba điểm meta-KB có mà file Dev khác chưa ghi

### 2.1 Hai Agent đang bind sai tầng — có chủ đích, có hạn chót

`doc-31` ghi thẳng: `LiveOps Planner` và `Release Reviewer` **hiện bind vào `GS9 Knowledge VNG AI` (tầng L0)**, trong khi L0 là sổ tay nền tảng, **không liên quan tri thức LiveOps game**. Lý do: đó từng là KB duy nhất sẵn có lúc bind ngày 14/08.

Đây là **lỗi phân loại đã biết**, không phải cấu hình đúng. Điều kiện gỡ: khi KB đúng tầng L2 (`Event Calendar & Brief`) và L3 (`Runbook & Known Issues`) sẵn sàng thì phải **gỡ bind L0 ra**, không giữ song song.

`Agent-ho-so-16-agent-cfl.md` mục 3.1 ghi hai Agent này là "Có KB · chưa chat-test" mà **không đánh dấu là bind sai tầng**. Đọc riêng bảng đó dễ tưởng cấu hình đã đúng. Ghi chú này bổ khuyết cho chỗ đó.

Hệ quả thực tế phải lường trước khi chạy G6: hai Agent lập kế hoạch LiveOps đang truy hồi trên corpus nói về **cách dùng nền tảng VNG AI**. Câu trả lời sẽ trôi về hướng dẫn công cụ thay vì nội dung game, và nó sẽ trông như một lỗi model trong khi thật ra là lỗi bind.

### 2.2 Cột "Ai được bind" là quy tắc, không phải trạng thái

`doc-31` nói rõ điều mà bảng bản chất dễ bị đọc nhầm: cột **"Ai được bind" mô tả quy tắc mong muốn**, không mô tả Web hiện tại. Hai thứ này đang lệch nhau ở ít nhất hai Agent (mục 2.1). Khi rà bind, đối chiếu **cả hai chiều**: KB nào đang bị bind bởi Agent không được phép, và Agent nào chưa bind được KB mà quy tắc cho phép.

### 2.3 Lý do kỹ thuật của việc chèn số phiên bản vào tên file

`doc-32` nêu lý do đầy đủ nhất trong các bản: converter sinh **cùng một dải tên** `00`–`11` và `01`–`29` cho **mọi** phiên bản. Không chèn `v5`/`v6`, V6 sẽ sinh trùng tên hệt V5 **trong cùng một KB**. Hậu quả kép:

1. Hai tài liệu cùng tên khác nội dung → không phân biệt được trong `Nguồn tham khảo` khi chat trích nguồn.
2. Retrieval trộn V5 với V6 → Agent trả lời kế hoạch cũ cho câu hỏi về bản mới, **không có dấu hiệu nào cho thấy nó nhầm**.

Đây là ràng buộc kỹ thuật của converter, không phải sở thích đặt tên. Ghi lại vì nó là lập luận cần có khi ai đó đề nghị bỏ tiền tố phiên bản cho gọn.

---

## 3. Hai sai số trong meta-KB — không chép sang

| Sai số | Chi tiết | Bản đúng |
|---|---|---|
| Đếm KB chưa tồn tại | `doc-30` và `doc-31` đều viết **"5 KB đích chưa tồn tại"** nhưng `doc-31` liệt kê **6 tên**: `Item Catalog`, `Glossary & Systems`, `Event Calendar & Brief`, `Runbook & Known Issues`, `CS FAQ & Policy`, `GM Policy & Sanction` | Đúng là **5 KB cần soạn mới**. `Item Catalog` là việc **tách** từ `Item Profile` (gate G2), không phải soạn nội dung mới — nên nó không nằm cùng nhóm. Xem `KB-quy-hoach-nghiep-vu-7-tang.md` mục 10 |
| Tiến độ soạn nội dung | Cả hai trang ghi 5 KB đều "chưa có nguồn" (trạng thái 15/08) | Đến 16/08 đã có **2/5 bản nháp local**: `GS9 CFL Glossary & Systems` (3 file) và `GS9 CFL CS FAQ & Policy` (1 file). Xem `KB-quy-hoach-nghiep-vu-7-tang.md` mục 5, ghi chú phiên 16/08 |

---

## Chưa kiểm chứng

- **Ba trang `doc-30`→`doc-32` có được cập nhật tiếp hay không.** Chúng là bản viết tay, không sinh từ builder, nên sẽ **không** tự đồng bộ khi các file `KB-*.md` đổi. Nếu giữ chúng trên Web, chúng sẽ lệch dần. Quyết định giữ hay bỏ chưa có.
- **Việc gỡ bind L0 khỏi hai Agent** — chưa có ngày, chưa có người phụ trách.

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `knowledge/GS9 CFL Knowledge Agent/doc-30`→`doc-32` | Ba trang meta-KB được đối chiếu trong file này |
| `docs/superpowers/specs/2026-08-15-kb-architecture-design.md` | Bản đồ kỹ thuật gốc (DEC-036) |
| `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` | Cơ sở quy ước đặt tên |
| `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md` | Kết luận cú pháp ảnh đúng, không đổi |
| `DECISIONS.md` | DEC-036, DEC-037, DEC-038, DEC-040, DEC-041, DEC-042, DEC-047 |
