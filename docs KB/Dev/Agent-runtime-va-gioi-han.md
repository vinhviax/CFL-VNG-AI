# Agent — hành vi runtime và giới hạn

**Ngày kiểm chứng gốc:** 11–12/08/2026 (deep test + live test trên `https://vnggames.ai/kb/agents`).
**Bổ sung cấu hình:** 14/08/2026 (bind KB), 15/08/2026 (DEC-049, DEC-050).
**Đối tượng:** Dev và Agent config — người phải sửa hệ thống.

Ba mức phân loại dùng trong file này theo DEC-007:

| Mức | Nghĩa |
|---|---|
| **Đã kiểm chứng** | Có bằng chứng trực tiếp trong `audit/`, ghi ngày |
| **Có điều kiện** | Đúng trong phạm vi hẹp đã thử, chưa tổng quát |
| **Chưa xác định / Bị chặn** | Chưa ai thử, hoặc bị nền tảng/tenant chặn |

> **Cảnh báo nền tảng (DEC-022).** Đọc được một thiết lập trên màn hình **không** có nghĩa đã biết nó chạy ra sao. Mọi bảng cấu hình dưới đây là snapshot UI; hành vi runtime phải đo riêng.

---

## 1. Đường đi một lượt chat

Sơ đồ dưới ghép từ `doc-14`, `doc-15`, `doc-16` trong `so-tay-tao-knowledge-base-v3.md`.

```text
Human message
  → classifier gán Intent (nhãn theo lượt)
  → chọn prompt: System Prompt + prompt theo Intent (nếu có override)
  → KB scope (All / Selected / None) + lọc loại tệp + chip @ theo lượt
  → tools: semantic / keyword / list chunks / document info / wiki / data
  → candidate set
  → vector threshold + keyword threshold + Top K
  → reranker (nếu bật) → Top K rerank
  → context → chat model (+ reasoning nếu bật)
  → vòng lặp tool tới max loops hoặc timeout
  → answer + source chips
```

Bốn ranh giới dễ nhầm:

| Ranh giới | Sai lầm thường gặp | Sự thật |
|---|---|---|
| Model ↔ embedding | Đổi LLM để "sửa retrieval" | Đổi LLM không sửa embedding/chunk gốc |
| Reranker ↔ nội dung KB | Tắt reranker để "làm sạch KB" | Tắt reranker không thay nội dung KB |
| Intent ↔ retrieval | Intent quyết định có RAG hay không | Intent chỉ là nhãn mục đích của lượt; retrieval do scope/tool/switch quyết định |
| Answer đúng ↔ retrieval pass | Câu trả lời đúng nghĩa là truy hồi đạt | Model có thể đã biết sẵn; phải mở source chip |

---

## 2. Truy hồi (retrieval)

### 2.1 Giá trị baseline đã đo

**Đã kiểm chứng 11/08/2026** trên Agent test `Kiểm thử Agent Knowledge VNG 2026-08-11` (`3c644ac2-ab5f-4141-959d-f1fa13ce8c41`):

| Tham số | Giá trị | Ghi chú |
|---|---:|---|
| Vector Top K | 10 | Đã khôi phục sau A/B |
| Keyword threshold | 0,3 | |
| Vector threshold | 0,5 | |
| Rerank Top K | 5 | |
| Rerank threshold | 0,5 | |

Sáu Agent mặc định dùng bộ khác (đọc UI 14/08/2026, `audit/default-agent-readonly-audit-2026-08-14.md`): Top K vector `10`, keyword/vector `0,3`/`0,5`, rerank K/threshold `10`/`0,3`. Riêng `Data Analyst` dùng Top K vector `5` và rerank `5`/`0,3`.

Không có giá trị "đúng cho mọi KB". A/B **một biến**, giữ nguyên corpus và query.

### 2.2 Phạm vi KB và công tắc `@`

| Control | Giá trị quan sát | Trạng thái |
|---|---|---|
| KB scope | `Tất cả kho tri thức` / `Kho tri thức đã chọn` / `Không dùng kho tri thức` | **Đã kiểm chứng** 11/08 |
| Lọc loại tệp | PDF, DOCX, TXT, MD, CSV, XLSX, XLS, JSON, PPTX, HTML, MSG, EML | **Đã kiểm chứng** UI 11/08; danh sách tenant có thể đổi |
| `Chỉ truy hồi khi được nhắc` | Bật/tắt được; đã khôi phục tắt | **Đã kiểm chứng** |
| `@` KB/tệp trong composer | Dialog liệt kê 2 KB, 5 fixture TEST và 14 Markdown consumer tại thời điểm audit | **Đã kiểm chứng** UI |
| Gỡ chip `@` | Không còn phạm vi truy hồi | **Pass có điều kiện** |

`@` là **lựa chọn phạm vi**, không phải quyền vượt access control.

### 2.3 Tool truy hồi phụ thuộc KB — phát hiện 14/08/2026

**Đã kiểm chứng** (`audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md`):

- Agent **chưa bind KB** thì toàn bộ nhóm `TRUY HỒI TRI THỨC` bị mờ, chú thích `Cần có kho tri thức trong phạm vi`. Phải bind KB trước mới bật được tool.
- Nhóm Wiki có chú thích riêng `Cần kho tri thức đã bật Wiki`.
- Tab `Công cụ` hiển thị phạm vi dạng `n KB RAG · n KB Wiki` — dùng để xác nhận bind thành công **trước** khi lưu.
- Danh sách Agent **tự sắp lại sau mỗi lần lưu**: Agent vừa cập nhật nhảy lên đầu nhóm `Tôi tạo`. Hệ quả cho automation: không dùng lại tọa độ cũ, phải chụp lại danh sách trước mỗi lần bấm.

### 2.4 Cách thiết kế phép thử retrieval — bộ fixture ORCHID

Bộ fixture tại `audit/agent-deep-test-fixtures-2026-08-11/` là mẫu tham chiếu để dựng phép thử retrieval mới. Nguyên tắc: **mỗi file mang một oracle biết trước**, và ít nhất một file **cố ý mâu thuẫn**.

| File | Vai trò | Oracle |
|---|---|---|
| `TEST-orchid-canonical.md` | Nguồn chuẩn | ORCHID-731 · Nhóm Cam · SLA 4 giờ · P2 |
| `TEST-orchid-near-duplicate.md` | Gần trùng, mâu thuẫn có chủ đích | ORCHID-731 · Nhóm **Lam** · SLA **9 giờ** · P2 |
| `TEST-orchid-data.csv` | Hai record cùng mã, khác `record_status` | `canonical` và `conflicting-near-duplicate` |
| `TEST-orchid-attachment.pdf` | Kiểm đường attachment tách khỏi đường KB | Cùng oracle canonical |
| `TEST-kb-type-conflict.md` | Mâu thuẫn **liên KB** với consumer | Khẳng định sai "ba loại KB chính" |

Bốn loại query bắt buộc cho mọi bộ fixture:

| Loại query | Pass condition |
|---|---|
| **Canonical** | Trả đúng giá trị chuẩn + trích nguồn |
| **Conflict** | Nêu **cả hai** phía, chỉ ra nguồn chuẩn, giải thích căn cứ — không im lặng chọn một giá trị |
| **Exact identifier** | Mã/tên chính xác tìm được qua keyword search |
| **No-hit** | Kết luận thiếu nguồn, không nội suy |

Bảng quyết định khi có xung đột nguồn:

| Trạng thái nguồn | Hành vi mong muốn |
|---|---|
| Một canonical rõ, không xung đột | Trả lời + trích nguồn |
| Canonical + near-duplicate có nhãn | Trả canonical, cảnh báo mâu thuẫn |
| Hai nguồn đồng cấp mâu thuẫn | **Không tự quyết**; hỏi owner hoặc báo không xác định |
| Không nguồn nào chứa claim | No-hit có căn cứ |

Retrieval **không** tự biết tài liệu nào authoritative. Nhãn canonical phải nằm trong chính nội dung tài liệu, và prompt phải cấm "bỏ phiếu bằng số lượng chunk".

**Giới hạn công cụ local đã gặp:** PDF fixture được sinh từ dữ liệu tổng hợp; Poppler cục bộ không render được vì wrapper thiếu đường dẫn runtime. KB vẫn parse thành công và Agent phân tích được qua attachment. Đây là giới hạn visual QA local, **không** phải blocker ingest/chat.

---

## 3. Intent — thực tế quan sát được

Sáu Intent thấy trên UI ngày 11/08/2026. `Intent` là **nhãn mục đích của một lượt chat**, không phải KB, tool hay model.

| Intent | Công dụng | Bằng chứng 11/08/2026 | Trạng thái |
|---|---|---|---|
| Greeting Response | Chào hỏi | Phản hồi trực tiếp, không source chip | **Đã kiểm chứng** hành vi |
| Chitchat Response | Xã giao | Có trên UI | Cần test riêng theo prompt tenant |
| Follow-up Response | Hỏi tiếp trong session | Có trên UI | Test phải giữ session và source trước đó |
| Image Analysis Response | Đọc ảnh | Composer hiện preview nhưng request không mang ảnh; Agent nói không nhận được ảnh | **Có điều kiện / chưa pass** |
| Summarize Response | Tóm tắt | Tóm tắt `00-gioi-thieu-va-quick-start.md` đúng 5 gạch đầu dòng | **Pass** |
| Document Analysis Response | Phân tích tệp | PDF ORCHID → ORCHID-731, Nhóm Cam, 4 giờ, P2 | **Đã kiểm chứng** |

**Giới hạn quan trọng:** UI **không phơi bày nhãn classifier** trong trace. Quan sát greeting trả lời trực tiếp là quan sát **hành vi**, không phải bằng chứng nội bộ về thuật toán phân loại. Không khẳng định certainty hay cơ chế classifier.

Ở cấp Agent mặc định `Quick Answer`, tab `Hội thoại` lộ một tập nhãn classifier **khác** (đọc UI 14/08/2026): `greeting`, `summarize`, `kb_search`, `clarification`, `follow_up`, `image_only`, `doc_only`, `chitchat`; mặc định `kb_search`. Hai tập nhãn này **chưa được đối chiếu với nhau** — xem mục 7.

### Biến prompt quan sát được

| Trường | Biến |
|---|---|
| System Prompt (Suy luận thông minh) | `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}` |
| Prompt theo Intent | `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}` |

Một biến được UI gợi ý **không** bảo đảm nó có dữ liệu hữu ích trong mọi tình huống.

Cả 10 custom Agent CFL để `Prompt theo intent` **trống** (`Chọn intent`, dùng template mặc định) — **Đã kiểm chứng** 15/08/2026, kiểm mẫu trực tiếp trên `GS9 CFL Economy Offer Analyst` và `GS9 CFL CS Copilot`.

---

## 4. Model, reranker và quota

Bốn model thấy trên UI 11/08/2026: `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b`, `qwen3.6-plus`. Reranker thấy được: `bge-reranker-v2-m3`.

| Quan sát | Trạng thái |
|---|---|
| `hosted_vllm/qwen3.6-35b` trả lời canonical và no-hit | **Đã kiểm chứng** |
| `deepseek-v4-flash` trả lời canonical ở chat độc lập (5 bước/11 giây) | **Đã kiểm chứng** |
| `deepseek-v4-flash` và một lượt `qwen3.6-plus` trả `429 insufficient_quota` | **Có điều kiện** |
| Bốn model đều còn quota | **Chưa xác định** — không suy ra từ dropdown |
| Chất lượng tương đối giữa bốn model | **Chưa xác định** — xem mục 7 |

### Quy tắc quota

1. Gặp `429`/lỗi xác thực → **dừng model đó**, ghi **Bị chặn**, đổi model được phép. **Không retry vô hạn.**
2. Một model chuyển unavailable/429 giữa chu kỳ A/B → chu kỳ đó là **Bị chặn**, không lấp bằng số liệu model khác.
3. Không lưu request headers, token, service-account JSON hoặc diagnostic raw vào tài liệu/audit.

### Giới hạn vòng lặp và timeout

| Agent | Max loops | Timeout LLM | Parallel |
|---|---:|---:|---|
| Agent test 11/08 | 10 | 120 s | Off |
| `Smart Reasoning` (mặc định) | 50 | 120 s | Off |
| `Hybrid Researcher` (mặc định) | 40 | 120 s | **On** |
| `Wiki Questioner`, `Data Analyst` (mặc định) | 30 | 120 s | Off |
| 9 custom Agent CFL (Smart) | 20 | 120 s | Off |
| `GS9 CFL CS Copilot` (Trả lời nhanh) | — không có control | — | — |

`Chế độ suy nghĩ` (Thinking) làm tăng độ trễ và token/lượt. **DEC-050:** Thinking đang **Bật** trên các custom Agent CFL đã kiểm — trái baseline `Thinking Off` ghi từ 14/08. Mới đọc trực tiếp 2/10 (`CS Copilot`, `Knowledge Curator`); 8 Agent còn lại là *suy ra*.

---

## 5. Kết quả runtime đã đo — deep test 11/08/2026

Nguồn: `audit/agent-deep-test-2026-08-11.md`. Agent disposable `TEST - Agent Lifecycle Deep Audit 2026-08-11`, 2 KB, 10 tool.

| Case | Model | Quan sát | Phân loại |
|---|---|---|---|
| Canonical + conflict | `hosted_vllm/qwen3.6-35b` | 13 bước/17 s; keyword + semantic; 4 tệp nguồn; nêu Nhóm Cam/4 giờ và cảnh báo Nhóm Lam/9 giờ | **Đã kiểm chứng** |
| No-hit | `hosted_vllm/qwen3.6-35b` | 7 bước/8 s; kết luận không có chính sách nghỉ phép 2031 | **Đã kiểm chứng** |
| Canonical ngắn | `deepseek-v4-flash` | 5 bước/11 s; trả Nhóm Cam từ file canonical | **Đã kiểm chứng** |
| Greeting | `deepseek-v4-flash` | Phản hồi trực tiếp, không source chip | Đã kiểm chứng **hành vi**; không thấy nhãn classifier |
| PDF attachment | `deepseek-v4-flash` | Composer nhận PDF; trả đủ 4 trường oracle | **Đã kiểm chứng** |
| Image attachment | `deepseek-v4-flash` | Toast `Định dạng tệp không hỗ trợ` | **Bị chặn/có điều kiện** — không kết luận VLM hỏng |
| Audio/ASR | UI cấu hình | Tenant không cung cấp ASR model | **Bị chặn** |

Điểm gate quan trọng: câu trả lời canonical **đã giải thích** near-duplicate không phải nguồn chuẩn, thay vì im lặng chọn một giá trị. Đây là điều kiện bắt buộc cho tài liệu hướng dẫn đa nguồn.

---

## 6. Cạm bẫy đã gặp thật

| Cạm bẫy | Triệu chứng | Cách nhận biết / xử lý |
|---|---|---|
| Preset không đảm bảo Agent hợp lệ | Create bị validation `Bật ít nhất một công cụ…` | Kiểm tra tool set hiệu lực **sau** khi chọn preset |
| Tool RAG bị khóa | Nhóm `TRUY HỒI TRI THỨC` mờ | Chưa bind KB — bind trước, bật tool sau |
| `[[chunk#12]]` lộ trong answer | Hosted model trả handle chunk thay vì câu tổng hợp | Bằng chứng context **đã tới** model; lỗi ở lớp model/prompt, không phải `@` hỏng |
| Danh sách Agent cache tên cũ | Tên trên list khác tên trong dialog | Mở dialog mới thấy tên thật (phát hiện 15/08) |
| Bấm nhầm Agent | Mở sai Agent do list cuộn giữa lúc chụp và lúc bấm | Xác minh **tên + Agent ID trong dialog** trước mọi thao tác; sự cố này đã xảy ra 14/08, đã đóng bằng `Hủy` |
| Pipeline ingest kẹt ở hậu xử lý | Detail đủ 5 giai đoạn nhưng trạng thái tổng vẫn `Đang hoàn tất` | Bấm **Làm mới** một lần; **Phân tích lại** chỉ khi detail đã đủ 5 giai đoạn; **không** bấm **Hủy** (hủy pipeline chứ không đóng hộp) |
| Đổi LLM để sửa lỗi nguồn | Answer không có nguồn | Kiểm tool/KB/scope/retrieval **trước** model |
| Suy ra chất lượng model từ một lượt | "A nhanh hơn B" | Cần ≥3 lượt cùng query/corpus/quota tương đương |

---

## 7. Điều chưa được kết luận

> Mục này giữ nguyên tinh thần phần cùng tên trong `audit/agent-deep-test-2026-08-11.md`. Đây là danh sách **không được lấp bằng suy đoán**.

### 7.1 Bốn khoản gốc từ deep test 11/08/2026

1. **Không đánh giá được chất lượng tương đối của bốn model** khi chưa có cùng quota và ba lượt hoàn chỉnh mỗi model.
2. **Wiki / Data / Schema tools chưa có fixture Wiki hoặc data-source đủ điều kiện** để tuyên bố pass end-to-end. Mới quan sát trong catalog/cấu hình.
3. **Image Analysis và ASR chưa pass end-to-end** trên tenant hiện tại.
4. **Không xác nhận quyền share end-to-end**, cũng không xác nhận khôi phục sau khi xóa Agent.

### 7.2 Khoản phát sinh sau 11/08

5. **Chưa Agent CFL nào chat-test đạt.** Cả 10 custom Agent vẫn **Bị chặn–Chưa xác định** về grounding. Gate **G6** (chat-test xác nhận `Nguồn tham khảo` đúng và không lộ PII) chưa chạy tính đến 15/08/2026.
6. **Reranker và VLM vừa bật (DEC-049) chưa chat-test.** Bật control không chứng minh chất lượng.
7. **Thinking bật ngoài khai báo (DEC-050)** — mới xác minh 2/10 Agent; 8/10 là *suy ra*.
8. **Hai tập nhãn Intent chưa được đối chiếu**: sáu `*_Response` ở dropdown Agent, và tám nhãn classifier `greeting/summarize/kb_search/...` ở tab `Hội thoại` của `Quick Answer`. Chưa có bằng chứng chúng là cùng một cơ chế.
9. **Mâu thuẫn tĩnh trong prompt Agent mặc định chưa được runtime test:**
   - `Quick Answer`: system prompt cấm prior knowledge, nhưng **fallback prompt cho phép general knowledge** khi danh sách tài liệu rỗng.
   - `Hybrid Researcher` và `Wiki Questioner`: prompt nhắc `wiki_flag_issue` nhưng tool này **không** có trong danh sách hiệu lực.
   Cả hai là **Đã kiểm chứng (static)** nhưng **Có điều kiện** về hành vi thật.
10. **Quota tenant, retention và giới hạn backend thực tế không hiển thị trên UI** — **Bị chặn–Chưa xác định**.

### 7.3 Rủi ro làm mọi snapshot cấu hình có thể sai (DEC-049)

**Đây là rủi ro nền, ảnh hưởng toàn bộ file này.**

Ngày 15/08/2026, cả 10 custom Agent được chia sẻ vào space `CFL Member` với quyền **Được chỉnh sửa** cho 6 thành viên. Hệ quả:

- **Bất kỳ ai trong space cũng sửa được Agent.** Model, prompt, tool, KB scope, retrieval threshold đều nằm trong tầm sửa.
- **Mọi snapshot config trong `agent/GS9 CFL */config.md` có thể lệch bất cứ lúc nào.** Không có cơ chế khóa hay version lock được xác nhận.
- **Phải audit lại trước khi kết luận** bất kỳ điều gì về cấu hình hiện tại. Không trích snapshot cũ như trạng thái đang chạy.

Rủi ro song song ở tầng KB: bốn trong sáu KB đã bind (`GS9 Knowledge VNG AI` ×3 Agent, `GS9 CFL PUM`, `GS9 CFL Kho Dữ Liệu Tổng Hợp`) **vẫn** đang share quyền `Chỉnh sửa` cho cùng space đó. Gate **G1** (hạ xuống `Chỉ đọc`) chưa xong. Nội dung KB có thể bị sửa ngoài quy trình build → 20 module trên Web có còn khớp master hay không là **Bị chặn–Chưa xác định** (gate **G5**).

---

## 8. Chưa kiểm chứng

- Chất lượng tương đối của 4 model; chưa có bộ ba lượt/model với quota tương đương.
- Wiki tools, `Truy vấn CSDL`, `Phân tích dữ liệu`, `Lược đồ dữ liệu` end-to-end trên tenant CFL.
- Image Analysis / VLM `qwen3.6-plus` end-to-end sau khi bật ngày 15/08.
- ASR: tenant chưa cung cấp model.
- Grounding của cả 10 custom Agent CFL (G6 chưa chạy).
- Cơ chế classifier Intent nội bộ; UI không phơi bày nhãn.
- Ảnh hưởng thật của `Chế độ suy nghĩ` bật lên độ trễ và token/lượt trên tenant này.
- Cấu hình hiện tại của 8/10 custom Agent về model/reranker/temperature/Thinking — mới đọc trực tiếp 2/10, phần còn lại là *suy ra*.
- 20 module consumer trên Web có còn khớp master sau khi space `CFL Member` có quyền `Chỉnh sửa` hay không.
- Quota tenant, retention, giới hạn backend.

---

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `audit/agent-deep-test-2026-08-11.md` | Deep test, mục "Điều chưa được kết luận" |
| `audit/agent-live-test-2026-08-11.md` | Ma trận kiểm thử Agent, retrieval baseline |
| `audit/agent-deep-test-fixtures-2026-08-11/` | Bộ fixture ORCHID |
| `audit/default-agent-readonly-audit-2026-08-14.md` | Cấu hình 6 Agent mặc định |
| `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md` | Bind KB, phát hiện UI |
| `audit/business-kb-readonly-audit-2026-08-14.md` | Gate G1–G6 |
| `docs/superpowers/reports/2026-08-11-agent-final-verification.md` | Verdict APPROVED và mục có điều kiện |
| `docs/superpowers/plans/2026-08-11-agent-knowledge-vng-implementation-plan.md` | Kế hoạch kiểm thử gốc |
| `so-tay-tao-knowledge-base-v3.md` | `doc-14`, `doc-15`, `doc-16` |
| `DECISIONS.md` | DEC-007, DEC-022, DEC-049, DEC-050 |
