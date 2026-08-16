# Agent — đa phương thức, tệp đính kèm và bề mặt chat

**Ngày kiểm chứng gốc:** 11–12/08/2026.
**Bổ sung:** 15/08/2026 (DEC-049 bật `Tải ảnh` + VLM trên 10 custom Agent CFL).
**Đối tượng:** Dev và Agent config.

---

## 1. Hai đường xử lý tệp — không suy ra lẫn nhau

Đây là điều dễ sai nhất khi debug.

| | Đường KB corpus | Đường attachment trong chat |
|---|---|---|
| Vòng đời | Lâu dài, tái sử dụng mọi lượt | Đúng **một** request |
| Xử lý | parser → chunk → index → retrieval tools | upload validation → request/session → Intent/VLM/ASR hoặc document reader |
| Điều kiện | Trạng thái tài liệu **Hoàn tất** | Client chấp nhận định dạng + tenant có model tương ứng |
| Bằng chứng | Source chip / source drawer | Filename + size hiện ở composer |

```text
KB file:     file → parser/chunk/index → retrieval tools → context → answer
Attachment:  Human file → upload validation → request/session
                → Intent / VLM / ASR / document reader → model → answer
```

Hai path chỉ gặp nhau ở model. Chúng có **validation, quyền, model và timing khác nhau**.

**Quy tắc chẩn đoán:** hỏi *"file đã tới request chưa?"* trước *"model đọc đúng chưa?"*.

Hai suy luận sai bị cấm:

- ❌ "PDF trong KB parse được → PDF attachment chắc chắn chạy."
- ❌ "Composer hiện preview ảnh → VLM đã nhận bytes."

---

## 2. Ma trận loại tệp — trạng thái 11/08/2026

| Loại | Đường đi | Test đã làm | Trạng thái |
|---|---|---|---|
| Markdown | KB → index → retrieval | Canonical / near-duplicate ORCHID | **Đã kiểm chứng** |
| PDF | KB **và** attachment | `TEST-orchid-attachment.pdf` (1,7 KB) | **Đã kiểm chứng cả hai đường** |
| CSV | KB → data/retrieval | Hai record ORCHID | **Đã kiểm chứng** qua RAG; data tool E2E **có điều kiện** |
| Ảnh | attachment → VLM / Image Intent | PNG UI có sẵn | **Bị chặn/có điều kiện** |
| Audio | attachment → ASR → text | Chỉ kiểm tra UI | **Bị chặn** |

### Chi tiết PDF attachment — Đã kiểm chứng

Composer nhận PDF 1,7 KB và hiển thị kích thước trước khi gửi. `deepseek-v4-flash` trả đúng cả bốn trường oracle: `ORCHID-731`, Nhóm Cam, SLA 4 giờ, priority P2.

### Chi tiết ảnh — hai lượt quan sát khác nhau

| Ngày | Quan sát | Kết luận được phép |
|---|---|---|
| 11/08 (live test) | Composer hiện preview nhưng **request không mang ảnh**; Agent nói không nhận được ảnh | Lỗi ở bước truyền attachment |
| 11/08 (deep test) | Toast `Định dạng tệp không hỗ trợ` với model test | Client từ chối; **không** kết luận VLM hỏng |

Hai lượt này khác nhau ở lớp thất bại (transmission vs client validation). Cả hai đều **chưa** chứng minh VLM lỗi.

### Chi tiết audio — Bị chặn theo tenant

Picker ASR báo chưa có model và yêu cầu liên hệ admin. Đây là **Bị chặn ở tầng provisioning tenant**, không phải lỗi cấu hình Agent. Không workaround bằng cách đưa credential hoặc model riêng vào workspace.

---

## 3. Thay đổi 15/08/2026 — bật `Tải ảnh` + VLM (DEC-049)

Người dùng thực hiện mutation live trên cả 10 custom Agent CFL:

| Control | Giá trị sau 15/08 | Trạng thái |
|---|---|---|
| `Tải ảnh` | **Bật** | **Đã kiểm chứng** UI (đọc trực tiếp trên `CS Copilot` và `Knowledge Curator`; 8 Agent còn lại *suy ra*) |
| `Mô hình VLM` | `qwen3.6-plus` | như trên |
| `Tải âm thanh` | Off | như trên |

### Rủi ro phải nêu trong mọi hướng dẫn sử dụng

> **Bật `Tải ảnh` mở thêm một bề mặt đưa ảnh chứa PII người chơi vào hội thoại.**

Cụ thể với CFL:

- Ảnh chụp màn hình ticket CS, ảnh hồ sơ tài khoản, ảnh giao dịch, ảnh chat trong game đều có thể chứa tên, ID người chơi, số điện thoại, email, thông tin thanh toán.
- Ảnh đi qua session chat, không qua quy trình audit nội dung như KB corpus. Không có bước duyệt trước.
- 10 Agent này đang share vào space `CFL Member` quyền `Được chỉnh sửa` — bề mặt này mở cho cả 6 thành viên.
- Retention của ảnh đính kèm ở cấp tenant là **Bị chặn–Chưa xác định**.

Kiểm soát tối thiểu đề nghị: cấm đính kèm ảnh chứa dữ liệu định danh người chơi; nếu nghiệp vụ bắt buộc, che định danh trước khi tải lên và xác nhận nơi lưu/retention với admin.

**Chất lượng VLM sau khi bật vẫn là `Bị chặn–Chưa xác định`** — chưa chat-test lượt nào. Bật control không chứng minh nó chạy.

---

## 4. Quy tắc dữ liệu cho tệp đính kèm

Bốn câu hỏi trước mỗi lần upload:

| Câu hỏi | Lý do |
|---|---|
| Corpus lâu dài hay context một lượt? | Chọn đúng đường KB hoặc attachment |
| Có PII / secret / credential không? | Ngăn rò rỉ qua chat và qua audit |
| Có fact oracle để chấm không? | Phân biệt parse lỗi với model tổng hợp lỗi |
| Tenant/model có VLM hoặc ASR không? | Tránh kết luận sai từ control rỗng |

Không dùng để kiểm thử: hợp đồng, thông tin cá nhân, credential, key, log nội bộ, file có retention chưa rõ. Dùng fixture synthetic có oracle rõ (mã, owner, SLA).

Ba điểm phải kiểm khi test attachment:

1. Filename và size **xuất hiện ở composer**.
2. Query nêu đúng **attachment**, không phải nguồn KB khác.
3. Answer **không** chỉ lặp lại dữ liệu từ KB đã bind.

---

## 5. Nguồn tham khảo trong chat

### 5.1 Bề mặt UI của một response

**Đã kiểm chứng 11/08/2026:** response có các nút `Sao chép`, `Thêm vào tri thức`, `Hữu ích`, `Chưa hữu ích`, `Thông tin request`.

| Bề mặt | Mục đích | SOP kiểm chứng |
|---|---|---|
| Source chip / `Xem file` | Căn cứ retrieval | Mở đúng file, đối chiếu claim với chunk |
| Source drawer | Xem nội dung nguồn | Kiểm tên file **và** số đoạn được trích |
| Ảnh render trong answer | Nội dung Markdown có ảnh | Kiểm ảnh render qua URI MinIO, không phải placeholder |
| `Thông tin request` | Metadata request | Che ID và URL trước khi phân phối ảnh |

### 5.2 Hai kiểm tra tách rời cho Markdown có ảnh

Đây là hai điều **khác nhau**, phải kiểm riêng:

1. **Source drawer mở đúng Markdown** — đúng file, đúng số đoạn.
2. **UI chat render ảnh qua URI MinIO** — blob thật, không phải URL trần hay placeholder.

Nếu response nêu ảnh mà chỉ có URL hoặc placeholder → **render chưa pass**. Nếu ảnh render nhưng source Markdown sai → **không chấp nhận answer** chỉ vì visual đẹp.

Link local `assets/...` chạy được trong HTML offline nhưng **không** phải đường phát hành cho chat.

### 5.3 Bằng chứng đã đo

Chuỗi 8 lần chat-test module 14→19 và 13 mới (11–12/08/2026) đều pass cả nội dung, source và ảnh:

| Module | Số đoạn trong source drawer | Ảnh render |
|---|---:|---:|
| `14-che-do-preset-prompt-va-intent.md` | 2 | 5 |
| `15-model-reranker-suy-luan-va-quota.md` | 1 | 3 |
| `16-kho-tri-thuc-cong-cu-va-truy-hoi.md` | — | 7 |
| `17-da-phuong-thuc-va-tep-dinh-kem.md` | — | 4 |
| `18-chat-nguon-lich-su-va-danh-gia.md` | — | 3 |
| `19-vong-doi-phan-quyen-...md` | — | có |
| `13-agent-tong-quan-va-kien-truc.md` | 3 | hero |

Lượt module 14 hiển thị `Nguồn tham khảo (8 tài liệu)`. Các nguồn cũ xuất hiện đồng thời là **kết quả multi-source bình thường**, không làm mất nguồn module mới.

### 5.4 Hai bẫy lý luận về nguồn

| Bẫy | Sự thật |
|---|---|
| "Có source chip → answer đúng" | Model có thể tổng hợp sai hoặc ưu tiên sai chunk. Phải mở nguồn kiểm claim. |
| "Answer đúng → retrieval pass" | Model có thể đã biết sẵn. Bắt buộc kiểm source khi use case yêu cầu grounded answer. |

Trường hợp thật: câu hỏi no-hit `Chính sách nghỉ phép năm 2031 của Agent là gì?` vẫn **có source chip**, vì corpus chứa chính quy tắc kiểm thử no-hit. Source chip đó **không** phải bằng chứng rằng chính sách 2031 tồn tại.

Handle `[[chunk#...]]` lộ ra là lỗi format/answer. Nó vẫn hữu ích cho kỹ thuật viên xác nhận chunk tồn tại, nhưng không được tính là answer đạt.

---

## 6. Lịch sử hội thoại và session

| Điểm | Trạng thái |
|---|---|
| Chat mới tạo một session mới | **Đã kiểm chứng** |
| Follow-up phải test **trong cùng history** | Quy tắc bắt buộc |
| Agent nhớ **giữa** các session | **Chưa kiểm chứng** — không giả định persistent memory |
| `Quick Answer` giữ lịch sử `5` lượt (UI 14/08) | **Đã kiểm chứng** UI |
| Custom Agent CFL baseline: giữ tối đa `3` lượt, tắt khi luồng có dữ liệu cá nhân | Thiết kế trong `config.md`, **chưa** xác minh Web actual |

Lịch sử giúp tái hiện ngữ cảnh conversation. Nó **không** thay audit cấu hình: model, quota hoặc setting Agent có thể đã đổi sau đó.

### `Thông tin request`

UI hiển thị Request ID, Message ID, Session ID, method `POST`, URL và thời gian gửi — **Đã kiểm chứng** 11/08/2026.

Quy tắc phân phối: **che Request/Message/Session ID và URL định danh trước khi dùng ảnh**. Không sao chép JSON request, private URL có ID, credential hoặc browser storage vào audit/workspace. Ảnh asset 48 trong bộ phát hành đã được che trước khi nạp.

---

## 7. Đánh giá câu trả lời (feedback)

### 7.1 Vòng đời

```text
session/chat → response + sources
  → Human feedback (Hữu ích / Chưa hữu ích + bình luận)
  → tổng quan đánh giá → Hộp xử lý
  → điều tra bằng source + Thông tin request
  → sửa đúng một lớp → hồi quy → Đã xử lý
```

**Đã kiểm chứng 11/08/2026:** hai feedback test được tạo; các bộ lọc (thời gian, Agent, loại, bình luận, tìm kiếm) thu hẹp đúng dữ liệu; Hộp xử lý mở được toàn bộ hội thoại liên quan; trạng thái chuyển `Mới → Đang xem → Đã xử lý`. Ảnh `34-agent-danh-gia-cau-tra-loi.png` ghi 2 feedback, tỷ lệ tích cực 50%.

### 7.2 Kịch bản triage — 7 bước

1. Mở conversation, xác định expectation của Human.
2. Mở source chip.
3. Phân loại: **không có nguồn** / **nguồn sai** / **nguồn đúng nhưng answer sai**.
4. Kiểm tra snapshot cấu hình Agent tại thời điểm đó.
5. Sửa **đúng một lớp**.
6. Chạy lại query gốc **và** query diễn đạt lại.
7. Ghi hành động, rồi mới chuyển **Đã xử lý**.

Không đóng feedback chỉ vì response mới nghe trôi chảy.

### 7.3 Bảng phân loại và bằng chứng đóng ticket

| Loại | Dấu hiệu | Owner | Bằng chứng đóng |
|---|---|---|---|
| Thiếu nguồn | Không có chip, hoặc no-hit sai | Owner Agent/KB | Scope/tool/index đã kiểm + source mới đúng |
| Nguồn sai | Chip không chứa claim | Owner KB/retrieval | Query hồi quy chọn đúng file/chunk |
| Tổng hợp sai | Chip đúng, conclusion sai | Owner prompt/model | Answer mới + source không đổi/đúng |
| Attachment fail | Composer/toast/request bất thường | Owner Agent + tenant admin | Test file synthetic pass, hoặc blocker có căn cứ |
| Quyền | Không thấy Agent/KB | Space/admin | Role/scope xác minh theo phê duyệt |

### 7.4 Gói bằng chứng tối thiểu

Một incident cần đủ: query đã che dữ liệu nhạy cảm · thời điểm · Agent/model · KB chips · answer · source drawer · trạng thái file · `Thông tin request` đã che · câu hồi quy sau sửa.

**Thiếu bất kỳ mục nào → trạng thái là `Đang xem`, không phải `Đã xử lý`.**

Một nguồn không còn truy hồi được sau update là **regression có owner**, không chỉ là feedback UI.

---

## 8. Cạm bẫy đã gặp thật

| Cạm bẫy | Nhận biết |
|---|---|
| Chat khi tài liệu còn `Đang hoàn tất` | Nguồn thiếu hoặc sai. Chờ **Hoàn tất** rồi mới test parser/source |
| Chụp ảnh khi UI còn `Đang tải` | Ghi nhầm answer trung gian thành answer cuối |
| Dùng feedback thumbs-down làm root cause | Feedback là chỉ dấu Human, không phải chẩn đoán |
| Sửa parser KB khi attachment fail | Hai đường xử lý khác nhau — đừng sửa nhầm lớp |
| Coi `Định dạng tệp không hỗ trợ` là "VLM hỏng" | Đó là lỗi client validation; VLM chưa được chạm tới |
| Lưu Request Information chưa che | Rò ID/URL định danh vào tài liệu phát hành |

---

## 9. Chưa kiểm chứng

- **Image Analysis / VLM `qwen3.6-plus` end-to-end** sau khi bật `Tải ảnh` ngày 15/08 — chưa lượt chat nào.
- **ASR** — tenant chưa cung cấp model. Bị chặn ở tầng provisioning.
- **Data tool E2E cho CSV** — mới đọc CSV qua RAG, chưa qua `Phân tích dữ liệu`/`Lược đồ dữ liệu`.
- **Retention của ảnh và tệp đính kèm** ở cấp tenant.
- **Persistent memory giữa các session** — không có bằng chứng, không giả định.
- **Số lượt lịch sử thật (Web actual)** của 10 custom Agent CFL — `config.md` ghi baseline `3` nhưng chưa đọc trực tiếp trên Web.
- **Feedback loop trên 10 Agent CFL** — chưa có lượt chat nào nên chưa có feedback nào.
- Danh sách loại tệp UI liệt kê **không** bảo đảm parser/VLM/ASR đều khả dụng trên mọi tenant/model.

---

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `so-tay-tao-knowledge-base-v3.md` khối `doc-17` | Đa phương thức và tệp đính kèm |
| `so-tay-tao-knowledge-base-v3.md` khối `doc-18` | Chat, nguồn, lịch sử và đánh giá |
| `audit/agent-live-test-2026-08-11.md` | Ma trận Intent, feedback, ảnh bằng chứng |
| `audit/agent-deep-test-2026-08-11.md` | PDF/ảnh/audio attachment, chuỗi chat-test module |
| `DECISIONS.md` | DEC-049 (bật Tải ảnh + VLM), DEC-050 |
