# Agent: tổng quan và kiến trúc

**Phạm vi:** Agent là gì trên nền tảng VNG AI, các loại Agent đang tồn tại, và sáu tab của hộp `Tạo trợ lý`.
**Ngày kiểm chứng gần nhất trong file này:** 15/08/2026.
**Đọc kèm:** `Agent-cau-hinh-va-tham-so.md` · `Agent-preset-prompt-va-intent.md` · `Agent-kho-tri-thuc-va-tool.md`.

---

## 1. Agent làm gì bên trong

Agent **không lưu tri thức**. Nó là lớp điều phối một lượt chat: nhận câu hỏi, phân loại Intent, quyết định có gọi truy hồi hay không, chọn công cụ, lọc/xếp hạng ứng viên rồi giao context cho model tổng hợp.

```text
Human → Agent nhận lượt chat → phân loại Intent
      ├─ nhánh trả lời trực tiếp (ví dụ lời chào)
      └─ nhánh suy luận: System Prompt → tools → KB/file scope
                          → ngưỡng + Top K → reranker
                          → context → model → câu trả lời + nguồn + feedback
```

Hệ quả vận hành: **nội dung sai thì sửa KB, không sửa câu trả lời của Agent.** Agent chỉ dùng bản KB mà nó được bind và được cấu hình truy hồi (kiểm chứng 11/08/2026, `audit/13-tao-va-van-hanh-agent-before-v3.3.0.md` mục 1).

### Năm lớp và ai sở hữu

| Lớp | Chủ sở hữu | Control phải kiểm | Sai ở lớp này biểu hiện thế nào |
|---|---|---|---|
| Nội dung | Owner KB | Markdown, phiên bản, URI ảnh MinIO | Nguồn sai hoặc thiếu bằng chứng |
| Truy hồi | Owner Agent | KB scope, loại file, `@`, tool, ngưỡng, reranker | Không có nguồn, hoặc nguồn nhiễu |
| Hành vi | Owner Agent | mode, preset, System Prompt, Intent, model | Nguồn đúng nhưng tổng hợp sai |
| Giao tiếp | Human | chat mới, lịch sử, feedback, Request Information | Không tái hiện được lỗi |
| Quyền/vòng đời | Owner + Space admin | bật/tắt, chia sẻ, audit, rollback | Người sai quyền thấy hoặc **sửa được** Agent |

Nguồn: `so-tay-tao-knowledge-base-v3.md` khối `doc-13`, kiểm chứng 11/08/2026.

### Nguyên tắc xuyên suốt — DEC-022

**Cấu hình UI đọc được KHÔNG bằng hành vi runtime đã kiểm chứng.** Mở dialog và đọc `Chế độ suy nghĩ: Bật` chỉ chứng minh *giá trị đang lưu*, không chứng minh model thực sự suy nghĩ mở rộng, không chứng minh retrieval chạy, không chứng minh reranker có tác dụng.

Ba mức phân loại dùng thống nhất trong toàn bộ tài liệu Dev (DEC-007):

- **Đã kiểm chứng** — có bằng chứng trực tiếp, ghi ngày.
- **Có điều kiện** — đúng trong phạm vi hẹp đã thử.
- **Bị chặn – Chưa xác định** — chưa ai thử, hoặc bị chặn bởi tenant/quota/quyền.

---

## 2. Các loại Agent đang tồn tại

Tại 15/08/2026 tenant `10012` có **6 Agent mặc định** + **10 Agent custom GS9 CFL** (danh sách 14/08/2026 hiển thị `Tất cả 18`, `Của tôi 12`, `Mặc định 6` — con số `Của tôi 12` gồm cả 2 Agent kiểm thử ngày 11/08).

### 2.1 Sáu Agent mặc định

| Agent | Mục đích trên UI | Mode | Ngày kiểm chứng | Nguồn |
|---|---|---|---|---|
| `Quick Answer` | Hỏi đáp RAG nhanh và chính xác từ KB | `Trả lời nhanh` | 14/08/2026 | `audit/default-agent-readonly-audit-2026-08-14.md` |
| `Smart Reasoning` | Suy luận ReAct nhiều bước và gọi công cụ | `Suy luận thông minh` / preset `Hỏi đáp RAG` | 14/08/2026 | như trên |
| `Hybrid Researcher` | Fan-out Wiki + chunk rồi đào sâu có trích dẫn | `Suy luận thông minh` / `Kết hợp RAG + Wiki` | 14/08/2026 | như trên |
| `Wiki Questioner` | Hỏi đáp chuyên biệt trên KB có Wiki | `Suy luận thông minh` / `Hỏi đáp Wiki` | 14/08/2026 | như trên |
| `Data Analyst` | Phân tích CSV/Excel bằng SQL + thống kê | `Suy luận thông minh` / `Phân tích dữ liệu` | 14/08/2026 | như trên |
| `FPA Analyst` | Phân loại câu hỏi → chọn nguồn → truy hồi | **`Quy trình`** (workflow cố định `fpa`) | 14/08/2026 | như trên |

**Ba điểm phải nhớ về Agent mặc định:**

1. **Cả sáu đều để `Tất cả kho tri thức`.** Không clone trực tiếp Agent mặc định cho việc nghiệp vụ nhạy cảm — bản sao sẽ kế thừa scope All KB (kết luận của audit 14/08/2026).
2. UI cho biết **không sửa được tên/mô tả**; các tham số cấu hình vẫn có nút Lưu. Nhìn thấy menu không chứng minh quyền thực thi.
3. **Không có tab/panel Chia sẻ nào hiển thị** cho Agent mặc định trong phạm vi UI đã xem → quyền public/private là *Bị chặn – Chưa xác định*.

### 2.2 Mười Agent custom GS9 CFL

| Agent | Web Agent ID | Mode | Ngày kiểm chứng ID |
|---|---|---|---|
| `GS9 CFL LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` | Suy luận thông minh | 14/08 tạo · 15/08 xác minh lại |
| `GS9 CFL Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | Suy luận thông minh | như trên |
| `GS9 CFL Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` | Suy luận thông minh | như trên |
| `GS9 CFL KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | Suy luận thông minh | như trên |
| `GS9 CFL Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | Suy luận thông minh | như trên |
| `GS9 CFL Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | Suy luận thông minh | như trên |
| `GS9 CFL CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | **Trả lời nhanh** | như trên |
| `GS9 CFL GM Policy Advisor` | `01d42d42-dd08-4907-9d4a-913142bc554c` | Suy luận thông minh | như trên |
| `GS9 CFL Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | Suy luận thông minh | như trên |
| `GS9 CFL Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | Suy luận thông minh | như trên |

**Đổi tên và đổi vai trò đã xảy ra:**

- 15/08/2026 — cả 10 Agent đổi tiền tố `GS9 ` → `GS9 CFL ` trên Web, đã đọc trực tiếp trong từng dialog (DEC-048, DEC-049).
- 15/08/2026 — `GS9 GM Case Investigator` đổi mục đích thành `GS9 CFL GM Policy Advisor`: từ điều tra case-scoped (không khả thi, vi phạm least privilege) sang tra cứu chính sách/quy trình/tiền lệ; bằng chứng vụ việc đi qua tệp đính kèm hội thoại thay vì KB (DEC-039).
- **Cạm bẫy đã gặp thật:** danh sách Agent trên UI **cache tên cũ**. Phải mở dialog mới thấy tên thật (15/08/2026).

### 2.3 Trạng thái chất lượng: chưa Agent nào đạt

**Tính đến 15/08/2026, không một Agent nào trong 10 Agent custom đã chat-test đạt.** Gate G6 (chat-test xác nhận `Nguồn tham khảo` đúng và không lộ PII) chưa chạy. Chất lượng grounding của cả 10 là **Bị chặn – Chưa xác định**.

Ngoại lệ duy nhất, và không được suy rộng: 14/08/2026 có **một** chat test đạt trên Agent mặc định `Quick Answer` khi nhắc KB `GS9 CFL Knowledge Agent` — Agent chọn đúng `GS9 LiveOps Planner`/`GS9 Release Reviewer`, nêu đúng bộ tool và Human gate, UI hiện `Nguồn tham khảo (15 tài liệu)`. Đây là **luồng hỏi đáp meta-KB**, không phải bằng chứng runtime cho 10 Agent custom (`audit/liveops-custom-agent-multitool-and-agent-kb-2026-08-14.md`).

---

## 3. Sáu tab của hộp `Tạo trợ lý`

Kiểm chứng 11/08/2026 trên hộp tạo mới:

| # | Tab | Quyết định điều gì | Tài liệu chi tiết |
|---|---|---|---|
| 1 | Thông tin cơ bản | Tên, mô tả, System Prompt, Prompt theo Intent | `Agent-preset-prompt-va-intent.md` |
| 2 | Cấu hình mô hình | Model chat, reranker, nhiệt độ, chế độ suy nghĩ | `Agent-cau-hinh-va-tham-so.md` |
| 3 | Kho tri thức | Phạm vi KB, loại tệp, công tắc `Chỉ truy hồi khi được nhắc` | `Agent-kho-tri-thuc-va-tool.md` |
| 4 | Công cụ | Tool hiệu lực, số vòng lặp, timeout LLM, gọi song song | `Agent-kho-tri-thuc-va-tool.md` |
| 5 | Chiến lược truy hồi | Top K, ngưỡng keyword/vector, Top K + ngưỡng rerank | `Agent-kho-tri-thuc-va-tool.md` |
| 6 | Cấu hình đa phương thức | Tải ảnh + VLM, tải âm thanh + ASR | mục 4 file này |

### Tập tab thay đổi theo mode và theo thao tác

Đây là điểm hay bị nhầm. Sáu tab ở trên là tập của **chế độ tạo mới, mode Suy luận thông minh**. Thực tế:

| Tình huống | Khác biệt tab đã quan sát | Ngày |
|---|---|---|
| Chỉnh sửa Agent đã tạo | **Thêm tab `Chia sẻ`** | 11/08/2026 |
| Mode `Trả lời nhanh` | **Không có tab `Công cụ`**; thay bằng tab `Hội thoại` (multi-turn, query rewrite, `Mẫu ngữ cảnh`); cũng không có control preset `Loại trợ lý` | 14/08 (Quick Answer) · 15/08 (CS Copilot) |
| Mode `Quy trình` (FPA Analyst) | Có tab `Các bước` ghi workflow cố định `fpa`, không sửa được tại đây | 14/08/2026 |
| Agent chưa bind KB | Tab `Công cụ` vẫn có, nhưng nhóm `TRUY HỒI TRI THỨC` **bị mờ** với chú thích `Cần có kho tri thức trong phạm vi` | 14/08/2026 |

Tab `Công cụ` hiển thị phạm vi KB dạng `n KB RAG · n KB Wiki` — dùng nó để xác nhận bind thành công **trước khi bấm Lưu** (phát hiện 14/08/2026).

---

## 4. Tab 6 — Cấu hình đa phương thức

| Trường | Giá trị quan sát | Ngày | Nguồn |
|---|---|---|---|
| `Tải ảnh` (10 Agent custom) | **Bật** | 15/08/2026 | DEC-049; đọc trực tiếp trên CS Copilot + Knowledge Curator, 8 Agent còn lại *suy ra* |
| `Mô hình VLM` | `qwen3.6-plus` | 15/08/2026 | như trên |
| `Tải âm thanh` | Off | 15/08/2026 | như trên |
| `Tải ảnh`/`Tải âm thanh` (6 Agent mặc định) | Off / Off | 14/08/2026 | `audit/default-agent-readonly-audit-2026-08-14.md` |
| `Mô hình ASR` | **Không có model** — UI báo *Chưa có model, liên hệ admin để thêm* | 11/08/2026 | `audit/13-...before-v3.3.0.md` mục 9 |

**Trạng thái thật của nhánh ảnh:** *Bị chặn / Có điều kiện*, không phải "đã hoạt động". Ngày 11/08/2026 composer hiển thị preview ảnh nhưng hai tin nhắn gửi đi **không mang ảnh tới Agent**; `Image Analysis Response` trả lời rằng không nhận được ảnh. Một đường test khác cho toast `Định dạng tệp không hỗ trợ`. Đây là lỗi ở bước bàn giao attachment, **chưa đủ bằng chứng kết luận VLM không đọc được ảnh** — và ngược lại, bật toggle không chứng minh VLM đọc được ảnh.

**Rủi ro mới do DEC-049:** bật `Tải ảnh` cho cả 10 Agent mở thêm bề mặt đưa ảnh chứa **PII người chơi** (ảnh chụp màn hình ticket, log, tài khoản) vào hội thoại. Phải nhắc điều này trong mọi hướng dẫn sử dụng cho Human.

**Tách hai đường xử lý tệp khi chẩn đoán** (11/08/2026):

```text
KB file:     file → parser/chunk/index → retrieval tools → context → answer
Attachment:  Human file → upload validation → request/session → Intent/VLM/ASR
                                                → model → answer
```

Hai đường gặp nhau ở model nhưng khác validation, quyền, model và timing. Luôn hỏi *"file đã tới request chưa?"* trước *"model đọc đúng chưa?"*.

---

## 5. Vòng đời và chia sẻ

Vòng đời đã thao tác thật trên Agent kiểm thử ngày 11/08/2026: tạo → chỉnh sửa và lưu (mở lại giá trị còn) → đánh dấu sao → nhân bản (bản sao kế thừa model, KB, tool) → tắt rồi bật lại. **Không thao tác Xóa** — hành vi xóa và khả năng khôi phục vẫn *Chưa xác định*.

Menu của Agent do người dùng tạo: `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt/Bật`, `Xóa`.
Menu của Agent mặc định (14/08/2026): `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt` — không có `Xóa`.

### DEC-049 — chia sẻ space và hệ quả nghiêm trọng

15/08/2026 người dùng đã chia sẻ **cả 10 Agent custom** vào space `CFL Member` với quyền **`Được chỉnh sửa`** (đọc trực tiếp trên `GS9 CFL CS Copilot`; sidebar `SPACES · CFL Member 10` xác nhận đủ 10).

> **Hệ quả bắt buộc phải hiểu:** quyền `Được chỉnh sửa` cho một space 6 thành viên nghĩa là **người khác sửa được Agent bất cứ lúc nào**. Mọi snapshot cấu hình trong tài liệu này — kể cả bảng trong `Agent-cau-hinh-va-tham-so.md` — **có thể lệch bất cứ lúc nào**. Trước khi kết luận bất cứ điều gì về một Agent, phải audit lại chính Agent đó, không đọc lại tài liệu.

Đây cũng là lý do mọi dòng trong tài liệu Agent phải có **ngày**: giá trị không có ngày là giá trị vô nghĩa.

Song song, **KB cũng đang chia sẻ quyền `Chỉnh sửa`** cho space `CFL Member`: 4/6 KB đã bind (`GS9 Knowledge VNG AI` ×3 Agent, `GS9 CFL PUM`, `GS9 CFL Kho Dữ Liệu Tổng Hợp`) vẫn ở trạng thái này tại 14/08/2026 — gate G1 chưa xong. Nội dung KB có thể bị sửa ngoài quy trình build.

---

## 6. Cạm bẫy đã gặp thật

| Hiện tượng | Điều đã thực sự xảy ra | Cách xử lý đúng |
|---|---|---|
| Bấm vào Agent trong danh sách, mở ra **sai Agent** | 14/08/2026: danh sách cuộn giữa lúc chụp ảnh và lúc bấm → mở nhầm `Kiểm thử Agent Knowledge VNG 2026-08-11` | Đóng ngay bằng `Hủy`. Từ đó: **xác minh tên + Agent ID trong dialog trước mọi thao tác** |
| Danh sách nhảy vị trí sau mỗi lần lưu | Agent vừa cập nhật nhảy lên đầu nhóm `Tôi tạo` | Chụp lại danh sách trước **mỗi** lần bấm; không tái dùng tọa độ cũ |
| Danh sách hiển thị tên cũ dù đã đổi | UI cache tên ở trang list (15/08/2026) | Mở dialog để đọc tên thật |
| `429 insufficient_quota` | Lỗi khả dụng model (11/08/2026, `deepseek-v4-flash` và một lượt `qwen3.6-plus`) | Đây **không** phải bằng chứng KB hỏng. Đổi model được phép, ghi blocker |
| Câu trả lời lộ chuỗi thô `[[chunk#12]]` | Context đã tới model nhưng lớp tổng hợp hỏng (11/08/2026) | Chẩn đoán prompt/model trước; **không sửa file nguồn** |
| Composer hiện preview ảnh nhưng Agent nói không có ảnh | Lỗi bàn giao attachment (11/08/2026) | Lưu bằng chứng UI/network; không kết luận VLM hỏng |

---

## 7. Chưa kiểm chứng

Danh sách này là **ranh giới của tài liệu**, không phải danh sách việc cần làm.

- **Chất lượng runtime của toàn bộ 16 Agent** (6 mặc định + 10 custom). Chưa Agent nào chat-test đạt. Gate G6 mở. *Bị chặn – Chưa xác định*.
- **Hành vi `Xóa` Agent** và khả năng khôi phục — chưa ai thử (11/08/2026 chủ động không thử).
- **Quyền `Chỉ xem` vs `Được chỉnh sửa`** thực sự cho phép/chặn thao tác gì trong space — phép thử 11/08 không gửi chia sẻ; DEC-049 đã đặt quyền `Được chỉnh sửa` nhưng chưa test hiệu lực thật của quyền đó.
- **Trạng thái public/private của 6 Agent mặc định** — không có panel Share hiển thị (14/08/2026).
- **Quota tenant, retention, giới hạn token/chi phí thực tế** — UI không phơi bày. Mọi con số loop/timeout trong tài liệu chỉ là *limit nhìn thấy trong config*.
- **Nhánh ảnh end-to-end** — bật `Tải ảnh` + VLM `qwen3.6-plus` (15/08/2026) hoàn toàn chưa được chat-test. Bằng chứng gần nhất (11/08/2026) là **thất bại** ở bước attachment.
- **Nhánh audio/ASR** — *Bị chặn*: tenant chưa có model ASR (11/08/2026).
- **Hiệu lực thật của phân loại Intent** — UI không hiển thị nhãn classifier trong trace; mọi kết luận về Intent là quan sát hành vi, không phải bằng chứng nội bộ.
- **Danh sách Agent mặc định theo tenant khác** — có thể khác; bảng mục 2.1 chỉ đúng cho tenant `10012`.
