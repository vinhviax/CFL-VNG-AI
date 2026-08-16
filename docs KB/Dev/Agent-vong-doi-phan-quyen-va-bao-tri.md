# Agent — vòng đời, phân quyền, release gate và bảo trì

**Ngày kiểm chứng gốc:** 11–12/08/2026 (vòng đời, UI chia sẻ).
**Bổ sung:** 14/08/2026 (gate G1–G6, bind KB), 15/08/2026 (DEC-049 chia sẻ thật vào space).
**Đối tượng:** Dev và Agent config.

---

## 1. Hai vòng đời tách rời

> **Agent config và nội dung KB có vòng đời riêng. Rollback Agent không thay thế rollback KB.**

```text
draft config → test Agent → evidence/audit → publish/share (nếu được phê duyệt)
      ↘ clone disposable → disable/enable → audit → delete đúng resource TEST

KB master → strict build → consumer Markdown → Agent retrieval
      ↑ rollback source/MD là việc KHÁC với rollback Agent config
```

Agent có thể tiếp tục tồn tại khi Markdown bị thay. Đổi nội dung phải đi theo đường `master → build → consumer → chat test`, **không** dùng Delete Agent như biện pháp "làm mới nội dung".

---

## 2. Thao tác vòng đời — trạng thái đã kiểm chứng

Menu Agent user-owned: `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`/`Bật`, `Xóa` — **Đã kiểm chứng** 11/08/2026.
Menu Agent **mặc định** chỉ có `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt` — không thấy `Xóa` (đọc UI 14/08/2026).

| Thao tác | Đã thực hiện live | Bằng chứng | Guardrail |
|---|---|---|---|
| Tạo Agent disposable | Có | `TEST - Agent Lifecycle Deep Audit 2026-08-11` | Tên `TEST -`, mô tả ghi rõ sẽ xóa sau audit |
| Clone | Có | Bản sao kế thừa model/KB/tool, đổi tên được | Kiểm cấu hình bản sao trước khi dùng |
| Disable → Enable | Có | Toast `Đã tắt trợ lý` / `Đã bật trợ lý`; trạng thái cuối = bật | Chỉ toggle trên clone, không toggle Agent đang phục vụ Human |
| Edit / Save | Có | Giá trị lưu bền sau mở lại | Lưu baseline, A/B một biến, restore |
| Xóa Agent TEST | Có (12/08) | Xóa đúng 2 Agent TEST; còn 8 Agent gồm đủ 6 mặc định | Bốn xác nhận (mục 2.2) |
| Xóa Agent production | **Không test** | — | Export/backup config, kiểm sharing, có rollback |
| Khôi phục sau Delete | **Chưa xác định** | UI không hứa hẹn, chưa test | Không suy luận |

### 2.1 Validation khi tạo

Create lần đầu bị chặn bởi validation `Bật ít nhất một công cụ…`. Sau khi chọn tool mới create thành công.

**Kết luận:** preset/mode **không** tự đảm bảo Agent hợp lệ nếu tool set rỗng. Luôn kiểm tool set hiệu lực sau khi chọn preset.

### 2.2 Bốn xác nhận trước Delete

Trước khi bấm Delete, phải đủ **cả bốn**:

1. Đúng **tên hiển thị**.
2. Đúng **owner**.
3. Đúng **mục đích** (`TEST`, không phải default/production).
4. **Audit/backup đã tồn tại**.

Thiếu một xác nhận → **không bấm Delete**.

Hộp xác nhận UI ghi đúng tên tài nguyên và cảnh báo xóa đoạn dữ liệu — **Đã kiểm chứng** 12/08/2026 khi dọn `13-tao-va-van-hanh-agent.md`.

Sau cleanup: reload danh sách, đối chiếu count và tên để chắc không còn resource TEST ngoài ý muốn.

---

## 3. Chia sẻ và phân quyền

### 3.1 Tab Chia sẻ

Tab `Chia sẻ` chỉ xuất hiện khi **sửa** Agent, không có khi tạo mới — **Đã kiểm chứng** 11/08/2026.

| Role | Ý nghĩa quan sát | Trạng thái 11/08 |
|---|---|---|
| `Chỉ xem` | Role chọn được khi chia sẻ Space | **Có điều kiện** — chưa test quyền end-to-end |
| `Được chỉnh sửa` | Role chọn được khi chia sẻ Space | **Có điều kiện** — chưa test quyền end-to-end |

Audit 11/08 chỉ **quan sát** UI, không gửi lời mời và không add Agent vào Space.

### 3.2 Trạng thái thật sau 15/08/2026 — DEC-049

Người dùng đã thực hiện chia sẻ thật. Đây là mutation live, khác hoàn toàn với trạng thái quan sát ở 11/08.

| Hạng mục | Giá trị | Trạng thái |
|---|---|---|
| Space | `CFL Member` | **Đã kiểm chứng** — sidebar `SPACES · CFL Member 10` |
| Số Agent được share | 10/10 custom Agent CFL | **Đã kiểm chứng** |
| Quyền | **Được chỉnh sửa** | **Đã kiểm chứng** — đọc trực tiếp trên `GS9 CFL CS Copilot` |
| Số thành viên space | 6 | **Đã kiểm chứng** (`audit/business-kb-readonly-audit-2026-08-14.md`) |
| Danh tính và vai trò 6 thành viên | — | **Bị chặn–Chưa xác định** |

### 3.3 Rủi ro DEC-049 — bắt buộc đọc

> **Quyền `Được chỉnh sửa` cho một space 6 người nghĩa là bất kỳ ai trong space cũng sửa được Agent.**

Hệ quả cụ thể:

| Hệ quả | Chi tiết |
|---|---|
| Mọi snapshot config có thể lệch | `agent/GS9 CFL */config.md` là ảnh chụp tại một thời điểm. Model, prompt, tool, KB scope, threshold đều nằm trong tầm sửa của 6 người. |
| Không kết luận từ snapshot cũ | **Phải audit lại trước khi kết luận** bất kỳ điều gì về cấu hình đang chạy. |
| Không có version lock được xác nhận | Không có cơ chế khóa cấu hình nào được kiểm chứng trên UI. |
| Drift không để lại dấu vết đã biết | Chưa xác định UI có log ai sửa gì, lúc nào. |

Rủi ro song song ở tầng KB: bốn trong sáu KB đã bind (`GS9 Knowledge VNG AI` ×3 Agent, `GS9 CFL PUM`, `GS9 CFL Kho Dữ Liệu Tổng Hợp`) **vẫn** share quyền `Chỉnh sửa` cho cùng space. Nội dung KB có thể bị sửa ngoài quy trình build → không bảo đảm 20 module trên Web còn khớp master.

Rủi ro thứ ba: `Tải ảnh` được bật cùng đợt (DEC-049) → mở thêm bề mặt đưa ảnh chứa PII người chơi vào hội thoại, cho cả 6 thành viên space. Chi tiết ở `Agent-da-phuong-thuc-va-chat.md`.

### 3.4 Phân vai vận hành

| Vai trò | Quyết định | Không được tự ý làm |
|---|---|---|
| Owner nội dung | Canonical source, phiên bản, mâu thuẫn nghiệp vụ | Đổi model/quyền để che lỗi nguồn |
| Owner Agent | Prompt, KB scope, tool, bộ regression | Sửa master KB trực tiếp trong module generated |
| Space/admin | Quyền truy cập, provisioning model/ASR | Cấp rộng quyền chỉ để thử một lỗi |
| Reviewer | Xem evidence, source, rollback | Phê duyệt chỉ dựa trên screenshot câu trả lời |
| Human dùng Agent | Feedback, làm rõ | Được coi là owner dữ liệu KB một cách mặc định |

---

## 4. Release gate

### 4.1 Gate G1–G6 — bắt buộc trước khi bind bất kỳ KB nào

Nguồn: `audit/business-kb-readonly-audit-2026-08-14.md`.

| Mã | Việc | Cần Human approval | Trạng thái 15/08/2026 |
|---|---|---|---|
| **G1** | Hạ quyền share 5 KB từ `Chỉnh sửa` xuống `Chỉ đọc`; riêng `GS9 CFL Item Profile` xem xét bỏ share | **Có** | **Chưa xong** — người dùng tự xử lý |
| **G2** | Quyết định phương án cho dữ liệu player trong `GS9 CFL Item Profile`, gồm PII đã lan vào description/summary (cần re-index sau khi loại cột định danh) | **Có** | Chưa xong |
| **G3** | Bổ sung 6 KB còn thiếu vào `PROJECT.md`/`STATUS.md` kèm ID và vai trò | Không | — |
| **G4** | Đồng bộ mirror local Data Daily (thiếu `CFL_082026.xlsx`) | Không | — |
| **G5** | Kiểm chứng 20 module trên Web còn khớp master, **sau khi có G1** | Không | Bị chặn bởi G1 |
| **G6** | **Chat-test grounding trên KB đã bind, xác nhận `Nguồn tham khảo` không lộ PII** | **Có** | **Chưa chạy** |

**Thực tế đã xảy ra:** 6/10 Agent đã bind KB ngày 14/08 **trước khi G1 xong**. Audit ghi rõ bind không làm rủi ro nặng thêm, nhưng nội dung KB vẫn có thể bị sửa ngoài quy trình build. Đây là nợ kỹ thuật phải đóng.

### 4.2 Gate nội dung KB — thứ tự bắt buộc

Đã chạy đủ và **Đã kiểm chứng** trong đợt v3.3.0 (11–12/08/2026):

```text
asset host (ảnh Hoàn tất 15/15)
  → lấy URI MinIO thật từ trang detail từng ảnh
  → cập nhật image map
  → strict build (python scripts/build_handbook.py)
  → unit test (python -m unittest discover -s tests)
  → nạp consumer Markdown từng module một
  → chờ trạng thái Hoàn tất
  → chat-test: nội dung + source drawer + ảnh render
  → chỉ khi pass mới nạp module kế tiếp
```

Quy tắc rút ra: **nạp từng module một, chat-test xong mới nạp module kế**. Không nạp chồng. Không xóa bản legacy trước khi bản thay thế pass chat-test.

### 4.3 Gate phát hành Agent

| Bước | Điều kiện pass |
|---|---|
| Cấu hình lưu thành công | **Không** đủ để coi là phát hành |
| Định danh version/audit | Mỗi thay đổi quan trọng có một mốc audit ghi ngày |
| Bộ regression | Canonical + conflict + exact identifier + no-hit |
| Owner chịu trách nhiệm | Có tên người quay lại baseline khi source/answer regress |
| Rollback path | Backup config + backup nội dung, tách riêng |

> Agent **không** có "phát hành tự động an toàn" chỉ vì nút Lưu thành công.

---

## 5. Trạng thái phát hành hiện tại — 15/08/2026

| Hạng mục | Trạng thái |
|---|---|
| 6 Agent mặc định | Không mutation trong mọi audit; audit chỉ-đọc 14/08 |
| 10 custom Agent CFL | Đã tạo, đã đổi tên `GS9 CFL`, đã share space |
| Bind KB | **6/10 đã bind**, 4/10 chưa (`Player Communications`, `GM Policy Advisor`, `Economy Offer Analyst`, `CS Copilot`) |
| Chat-test | **0/10 đạt** — chưa Agent nào chat-test đạt. G6 chưa chạy |
| Grounding | **Bị chặn–Chưa xác định** cho cả 10 |
| Reranker + VLM vừa bật | **Chưa chat-test** |

Phân loại chuẩn áp cho cả 10 Agent CFL:

- Identity và config UI-visible → **Đã kiểm chứng** (ngày 15/08, và chỉ 2/10 đọc trực tiếp cho model/Thinking).
- Behavior mô tả trong System Prompt → **Có điều kiện**.
- Runtime, grounding, chất lượng, latency → **Bị chặn–Chưa xác định**.

---

## 6. Lịch bảo trì

| Chu kỳ | Việc làm | Output tối thiểu |
|---|---|---|
| Sau thay KB/Markdown | Chạy canonical, conflict, no-hit; mở source và ảnh | Audit ghi ngày, source pass/fail |
| Sau đổi model/prompt/tool | A/B **một** biến; restore nếu không đạt | Config diff + kết quả hồi quy |
| Hàng tuần | Xem feedback chưa xử lý, trend quota/error | Owner và trạng thái Hộp xử lý |
| Hàng tháng | Rà soát quyền Space, Agent đã tắt, Agent TEST cũ | Danh sách giữ/xóa có phê duyệt |
| Trước xóa/retire | Backup config và evidence, xác nhận exact target | Rollback plan + người duyệt |

**Bổ sung cho môi trường DEC-049:** vì 6 người sửa được Agent, thêm một chu kỳ **rà soát drift cấu hình** — đọc lại dialog từng Agent và so với `config.md` — trước mỗi lần kết luận về hành vi.

Reranker phải được coi là **dependency**, không phải tùy chọn: khi nó mất khả dụng, test lại retrieval trước khi coi answer cũ còn tương đương.

---

## 7. Rollback

| Loại | Cách làm | Không được làm |
|---|---|---|
| Rollback cấu hình Agent | Khôi phục từ snapshot `config.md` + audit ngày tương ứng | Không dùng Delete Agent để "làm mới" |
| Rollback nội dung KB | `master → strict build → consumer → chat-test` lại | Không tự xóa module để rollback |
| Rollback ảnh | Đối chiếu `audit/image-map-before-*.json` | Không thay mapping bằng URI suy đoán |
| Khi ingest lỗi | Giữ module đã hoàn tất, audit lỗi, **không** đụng bản legacy | Không nạp chồng module kế tiếp |

Backup byte-for-byte trước khi thay thế module là bắt buộc. Ví dụ đã làm: `audit/13-tao-va-van-hanh-agent-before-v3.3.0.md`, SHA-256 `489FDBB1E9E6C541D5B035C6EDFBD32ABE5F08BAE9034F604A3E97473F65D8B7`.

---

## 8. Cạm bẫy đã gặp thật

| Cạm bẫy | Nhận biết / xử lý |
|---|---|
| Danh sách Agent **cache tên cũ** | Tên trên list khác tên trong dialog. Mở dialog mới thấy tên thật (15/08) |
| Danh sách tự sắp lại sau mỗi lần lưu | Agent vừa cập nhật nhảy lên đầu nhóm `Tôi tạo`. Chụp lại danh sách trước mỗi lần bấm; không tái dùng tọa độ |
| Bấm nhầm Agent | Đã xảy ra 14/08 — mở nhầm `Kiểm thử Agent Knowledge VNG 2026-08-11`. Đã đóng bằng `Hủy`, không sửa gì. Quy tắc: xác minh **tên + Agent ID trong dialog** trước mọi thao tác |
| `AGENTS.md` giữ checklist cũ | Reviewer chặn vì file còn ghi 14 phần trong khi thực tế 20. Sửa riêng, build lại, chạy lại test |
| Xóa nhầm Agent | Tên TEST độc nhất + owner + ID + ảnh/audit trước Delete. Mơ hồ thì dừng |
| Drift cấu hình | Baseline export + test matrix + A/B một biến |
| Gộp nhiều thay đổi | Không gộp content change với nhiều config change trong cùng một lần |
| Chia sẻ sai phạm vi | Xem UI trước; chỉ gửi khi rõ quyền, đích và role |

---

## 9. Chưa kiểm chứng

- **Quyền `Chỉ xem` và `Được chỉnh sửa` end-to-end** — chưa test một tài khoản khác thực sự làm được gì trong từng role.
- **Khôi phục sau Delete Agent** — UI không hứa hẹn, chưa test.
- **UI có log ai sửa Agent, lúc nào** hay không.
- **Danh tính và vai trò 6 thành viên space `CFL Member`**.
- **G1, G2, G5, G6** đều chưa hoàn tất tính đến 15/08/2026.
- **20 module trên Web có còn khớp master** sau khi space có quyền `Chỉnh sửa` (phụ thuộc G1 → G5).
- **Policy retention ở cấp tenant**.
- **Menu `Xóa` trên Agent mặc định** — không thấy trên UI, nhưng chưa xác nhận là bị chặn hay chỉ ẩn.
- **Owner thực của `GS9 test knowledge base`**.

---

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `so-tay-tao-knowledge-base-v3.md` khối `doc-19` | Vòng đời, phân quyền, quan sát và bảo trì |
| `audit/agent-live-test-2026-08-11.md` | Ma trận vòng đời, tab Chia sẻ |
| `audit/agent-deep-test-2026-08-11.md` | Clone/disable/enable, cleanup, backup SHA-256 |
| `audit/business-kb-readonly-audit-2026-08-14.md` | Gate G1–G6, quyền share KB, space `CFL Member` |
| `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md` | Bind KB, G1 chưa xong, nợ tài liệu |
| `audit/default-agent-readonly-audit-2026-08-14.md` | Menu và giới hạn 6 Agent mặc định |
| `DECISIONS.md` | DEC-034, DEC-039, DEC-048, DEC-049, DEC-050 |
