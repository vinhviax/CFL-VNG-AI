# Hồ sơ 16 Agent — 6 mặc định + 10 custom CFL

**Ngày kiểm chứng:** 14/08/2026 (6 Agent mặc định, audit chỉ-đọc) · 14–15/08/2026 (10 custom Agent CFL).
**Đối tượng:** Dev và Agent config. File này là **chỉ mục tra cứu**, không chép nguyên văn từng hồ sơ.

> **Cảnh báo trước khi dùng bảng trong file này (DEC-049).** 10 custom Agent đang share vào space `CFL Member` với quyền **Được chỉnh sửa** cho 6 người. Bất kỳ ai cũng sửa được Agent, nên **mọi giá trị dưới đây có thể đã lệch**. Phải mở dialog trên Web và đọc lại trước khi kết luận. Chi tiết: `Agent-vong-doi-phan-quyen-va-bao-tri.md`.

---

## 1. Tóm tắt trạng thái sẵn sàng

| Nhóm | Số lượng | Đã bind KB | Chat-test đạt |
|---|---:|---:|---:|
| Agent mặc định VNG AI | 6 | Tất cả dùng `Tất cả kho tri thức` (mặc định nền tảng) | 0/6 |
| Custom Agent CFL | 10 | **6/10** | **0/10** |

> **Chưa Agent nào chat-test đạt.** Gate **G6** (chat-test grounding, xác nhận `Nguồn tham khảo` đúng và không lộ PII) chưa chạy tính đến 15/08/2026. Toàn bộ 16 Agent ở mức **Bị chặn–Chưa xác định** về chất lượng runtime.

### Binding KB thật — đọc từ API ngày 16/08/2026

Lấy trực tiếp từ `GET /kb/v1/api/agents`, trường `config.kb_selection_mode` và `config.knowledge_bases`. Đây là **Web actual**, không phải thiết kế:

| Agent custom | `kb_selection_mode` | KB đang gắn |
|---|---|---|
| `Knowledge Curator` | `selected` | `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI` |
| `KPI Experiment Analyst` | `selected` | `GS9 CFL Kho Dữ Liệu Tổng Hợp` |
| `Incident Triage` | `selected` | **`GS9 CFL PUM`** |
| `Player Voice Analyst` | `selected` | **`GS9 CFL Sentiment Feedback User`** |
| `LiveOps Planner` | `selected` | `GS9 Knowledge VNG AI` |
| `Release Reviewer` | `selected` | `GS9 Knowledge VNG AI` |
| `CS Copilot` | `none` | — |
| `Economy Offer Analyst` | `none` | — |
| `GM Policy Advisor` | `none` | — |
| `Player Communications` | `none` | — |

**Hai binding từng bị đánh giá là rủi ro — nay đã được chấp nhận (16/08/2026):**

1. `Incident Triage` → `GS9 CFL PUM` (chứa dữ liệu doanh thu)
2. `Player Voice Analyst` → `GS9 CFL Sentiment Feedback User` (chứa phản hồi người dùng)

Hồ sơ Agent cũ và audit 14/08 từng ghi hai cặp này là *"chặn"* / *"không bind as-is"*. Người dùng xác nhận **giữ nguyên**, lý do: nền tảng chỉ dùng nội bộ. Các đánh giá "chặn" trước đó không còn hiệu lực cho hai cặp này.

Vẫn giữ nguyên tắc chung khi bind kho mới: chỉ gắn kho mà công việc của Agent thật sự cần, không gắn thừa.

**Bốn Agent `kb_selection_mode: none`** trả lời hoàn toàn không có nguồn CFL nào — kết quả của chúng không có gì bảo chứng. Con số *"6/10 đã bind"* ở bảng trên khớp với dữ liệu API này.

**Phạm vi thật hẹp hơn tên gọi:** `Incident Triage` chỉ có report tháng, chưa có runbook sự cố. `LiveOps Planner` và `Release Reviewer` gắn kho hướng dẫn nền tảng, chưa gắn kho nghiệp vụ LiveOps. Đừng suy từ tên Agent ra phạm vi dữ liệu.

Phân loại áp cho mọi hàng trong file này:

| Lớp | Mức |
|---|---|
| Identity, ID, cấu hình UI-visible | **Đã kiểm chứng** (ngày ghi ở tiêu đề mỗi bảng) |
| Behavior mô tả trong System Prompt | **Có điều kiện** |
| Runtime, grounding, chất lượng, latency, quota | **Bị chặn–Chưa xác định** |

---

## 2. Sáu Agent mặc định VNG AI

Audit chỉ-đọc UI ngày **14/08/2026**. Không mutation. Nguồn chi tiết: `audit/default-agent-readonly-audit-2026-08-14.md` và 6 file `agent/<tên>-config.md`.

| Agent | Vai trò (mô tả UI) | Mode / preset | Model | KB scope | Tool hiệu lực | Loops / timeout | Sẵn sàng |
|---|---|---|---|---|---:|---|---|
| `Quick Answer` | RAG Q&A nhanh | `Trả lời nhanh` | `gpt-5.4-mini` | Tất cả KB · mọi loại tệp | **0** (không có tab Công cụ) | — | Config OK · **chưa chat-test** |
| `Smart Reasoning` | ReAct, suy luận nhiều bước + tool calling | `Suy luận thông minh` / `Hỏi đáp RAG` | `gpt-5.4-mini` | Tất cả KB · mọi loại tệp | **4** — semantic, keyword, liệt kê đoạn, thông tin tài liệu | 50 / 120 s | Config OK · **chưa chat-test** |
| `Hybrid Researcher` | Fan-out Wiki + chunk rồi đào sâu, trả lời có trích dẫn | `Suy luận thông minh` / `Kết hợp RAG + Wiki` | `qwen3.6-plus` | Tất cả KB · mọi loại tệp | **7** — 3 Wiki + 4 RAG chunk | 40 / 120 s · **parallel On** | Config OK · **chưa chat-test** |
| `Wiki Questioner` | Hỏi đáp trên KB dạng Wiki | `Suy luận thông minh` / `Hỏi đáp Wiki` | `qwen3.6-plus` | Tất cả KB · mọi loại tệp | **3** — tìm Wiki, đọc trang Wiki, đọc tài liệu nguồn | 30 / 120 s | Config OK · **chưa chat-test** |
| `Data Analyst` | Phân tích dữ liệu CSV/Excel bằng SQL + thống kê | `Suy luận thông minh` / `Phân tích dữ liệu` | `gpt-5.4-mini` · temp `0.3` | Tất cả KB · **chỉ `CSV`, `XLSX`** | **2** — lược đồ dữ liệu, phân tích dữ liệu | 30 / 120 s | Config OK · **chưa chat-test** |
| `FPA Analyst` | Pipeline cố định: hiểu câu hỏi → định tuyến nguồn → truy hồi | `Quy trình` (workflow `fpa`) | `qwen3.6-plus` · **Thinking Bật** | Tất cả KB · mọi loại tệp | **7** — danh mục sản phẩm, hỏi người dùng, 4 RAG chunk, `Truy vấn CSDL` | 10 / 180 s | Config OK · **chưa chat-test** |

Điểm chung đã kiểm chứng:

- Reranker `bge-reranker-v2-m3` trên cả 6.
- Temperature `0.7` trên 5 Agent; `Data Analyst` là `0.3`.
- `Prompt theo intent` = `Chọn intent` trên cả 6 — không có override intent nào được chọn.
- Upload ảnh và audio/ASR **tắt** trên cả 6.
- Chỉ `Quick Answer` có tab `Hội thoại` (multi-turn bật, giữ `5` lượt, query rewrite bật).
- Cả 6 có nhãn `Mặc định`; menu chỉ có `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt` — **không thấy `Xóa`**.
- **Không có panel Share** → không kết luận được public/private, ai dùng, ai sửa. **Bị chặn–Chưa xác định**.

### Ba mâu thuẫn tĩnh trong prompt Agent mặc định

Đây là phát hiện **Đã kiểm chứng (static)** từ việc đọc prompt, nhưng hành vi runtime **Có điều kiện**:

| Agent | Mâu thuẫn |
|---|---|
| `Quick Answer` | System prompt cấm prior knowledge, nhưng **fallback prompt cho phép general knowledge** khi danh sách tài liệu rỗng |
| `Hybrid Researcher` | Prompt nhắc `wiki_flag_issue` nhưng tool này **không** có trong danh sách hiệu lực |
| `Wiki Questioner` | Cùng vấn đề `wiki_flag_issue` |
| `FPA Analyst` | Prompt nói pipeline đã thu hẹp scope nguồn, nhưng UI vẫn để `Tất cả kho tri thức` — scope thật chỉ runtime test mới chứng minh |

---

## 3. Mười custom Agent CFL

Web actual ngày **15/08/2026**. Nguồn: 10 thư mục `agent/GS9 CFL */`, `audit/liveops-custom-agent-creation-2026-08-14.md`, `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md`.

### 3.1 Bảng hồ sơ

| Agent | Vai trò | KB đã bind | Tool | Sẵn sàng |
|---|---|---|---:|---|
| `GS9 CFL LiveOps Planner` | Lập kế hoạch event/chiến dịch LiveOps từ lịch, spec, runbook đã duyệt; sinh checklist, rủi ro, dependency, điểm phê duyệt | `GS9 Knowledge VNG AI` (1) | 6 | Có KB · **chưa chat-test** |
| `GS9 CFL Release Reviewer` | Rà soát change request và bằng chứng cấu hình trước phát hành; sinh preflight report, blocking issue, đánh giá rollback | `GS9 Knowledge VNG AI` (1) | 5 | Có KB · **chưa chat-test** |
| `GS9 CFL Incident Triage` | Phân loại sự cố live bằng runbook, known issue, tác động người chơi, snapshot monitoring, thay đổi gần đây | `GS9 CFL PUM` (1) | 5 | Có KB · **chưa chat-test** |
| `GS9 CFL KPI Experiment Analyst` | Phân tích KPI và thử nghiệm LiveOps; giải thích cohort, segment, phương sai, bất thường, caveat thống kê | `GS9 CFL Kho Dữ Liệu Tổng Hợp` (1) | 6 | Có KB · **chưa chat-test** |
| `GS9 CFL Player Voice Analyst` | Phân tích phản hồi người chơi đã ẩn danh/tổng hợp: chủ đề, sentiment, pain point, feature request | `GS9 CFL Sentiment Feedback User` (1) | 4 | Có KB · **chưa chat-test** |
| `GS9 CFL Knowledge Curator` | Biến bằng chứng event/sự cố thành draft postmortem, bài học, action item, đề xuất cập nhật KB | `GS9 Knowledge VNG AI` + `GS9 CFL Knowledge Agent` (2) | 6 | Có KB · **chưa chat-test** |
| `GS9 CFL Economy Offer Analyst` | Rà soát đề xuất kinh tế và gói ưu đãi theo bằng chứng item, tiền tệ, phần thưởng, giá, hiệu quả lịch sử | **Không bind** | 3 | **Chặn** — thiếu KB hợp lệ |
| `GS9 CFL Player Communications` | Soạn nội dung hướng ra người chơi và biến thể bản địa hóa từ brief/claim/lịch/thuật ngữ đã duyệt | **Không bind** | 3 | **Chặn** — chờ KB nguồn |
| `GS9 CFL GM Policy Advisor` | Tra cứu và giải thích chính sách xử phạt, quy trình, tiền lệ cho GM được phân quyền | **Không bind** | 2 | **Chặn** — chờ KB chính sách |
| `GS9 CFL CS Copilot` | Phân loại ticket và soạn draft trả lời/escalation cho CS dựa trên chính sách đã duyệt | **Không bind** | 0 | **Chặn** — thiếu KB, mode không có tab Công cụ |

### 3.2 Cấu hình chung — Web actual 15/08/2026

| Trường | Giá trị | Mức xác minh |
|---|---|---|
| Mode | 9 Agent `Suy luận thông minh`; `CS Copilot` là `Trả lời nhanh` | **Đã kiểm chứng** |
| Preset | `Hỏi đáp RAG` cho 9 Smart; `CS Copilot` **không có control `Loại trợ lý`** | **Đã kiểm chứng** |
| Model | `hosted_vllm/qwen3.6-35b` | Đọc trực tiếp 2/10; 8/10 ***suy ra*** |
| Reranker | `bge-reranker-v2-m3` | Đọc trực tiếp 2/10; 8/10 ***suy ra*** |
| Temperature | `0.7` | Đọc trực tiếp 2/10; 8/10 ***suy ra*** |
| `Chế độ suy nghĩ` | **Bật** (trái baseline `Off` ghi 14/08 — DEC-050) | Đọc trực tiếp 2/10; 8/10 ***suy ra*** |
| `Prompt theo intent` | Trống (`Chọn intent`) | **Đã kiểm chứng**, kiểm mẫu 2 Agent |
| Max steps / timeout / parallel | `20` / `120s` / Off cho 9 Smart; `CS Copilot` không có control | **Đã kiểm chứng** |
| Tải ảnh / VLM | **Bật** / `qwen3.6-plus` | Đọc trực tiếp 2/10; 8/10 ***suy ra*** |
| Tải âm thanh | Off | như trên |
| Chia sẻ | Space `CFL Member`, quyền **Được chỉnh sửa** | **Đã kiểm chứng** (đọc trên `CS Copilot`; sidebar `SPACES · CFL Member 10`) |
| Phạm vi KB | `Kho tri thức đã chọn` cho cả 6 Agent có bind — **không** dùng `Tất cả kho tri thức` | **Đã kiểm chứng** |

Hai Agent được đọc trực tiếp: `GS9 CFL CS Copilot` và `GS9 CFL Knowledge Curator`. Tám Agent còn lại ghi *suy ra* theo mẫu trong chính `config.md` của chúng.

### 3.3 Web Agent ID

| Agent | ID |
|---|---|
| `GS9 CFL LiveOps Planner` | `99ce5c68-e722-47fb-beab-c496433eb3d4` |
| `GS9 CFL Release Reviewer` | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` |
| `GS9 CFL Incident Triage` | `43a43154-ef15-40c3-99bb-678c3be733ed` |
| `GS9 CFL KPI Experiment Analyst` | `37da676c-59ce-4936-9314-5ac4cc3d1a45` |
| `GS9 CFL Economy Offer Analyst` | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` |
| `GS9 CFL Player Voice Analyst` | `03bbab6e-1315-48ad-a05b-ad19fcb31796` |
| `GS9 CFL CS Copilot` | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` |
| `GS9 CFL GM Policy Advisor` | `01d42d42-dd08-4907-9d4a-913142bc554c` |
| `GS9 CFL Player Communications` | `4b8e6d78-9217-4dbb-8ab3-919628a48440` |
| `GS9 CFL Knowledge Curator` | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` |

Xác minh **tên + ID trong dialog** trước mọi thao tác. Danh sách Agent trên UI từng **cache tên cũ** (phát hiện 15/08).

### 3.4 Ma trận tool đang bật

| Tool | Số Agent bật |
|---|---:|
| `Hỏi người dùng` | 9 (mọi Smart Agent) |
| `Suy nghĩ` | 8 (trừ `GM Policy Advisor`, `CS Copilot`) |
| `Lập kế hoạch (todo)` | 8 (trừ `Player Voice Analyst`, `CS Copilot`) |
| `Tìm theo ngữ nghĩa` | 6 (đúng nhóm có bind KB) |
| `Tìm theo từ khóa` | 6 (đúng nhóm có bind KB) |
| `Thông tin tài liệu` | 3 — `Knowledge Curator`, `KPI Experiment Analyst`, `LiveOps Planner` |

**Giữ Off có chủ đích trên cả 10:** `Liệt kê đoạn`, `Truy vấn CSDL`, `Danh mục sản phẩm`, `Phân tích dữ liệu`, `Lược đồ dữ liệu`, và toàn bộ nhóm Wiki (`Tìm wiki`, `Đọc trang wiki`, `Đọc tài liệu nguồn`) — Wiki index chưa được kiểm chứng có nội dung.

Chiến lược truy hồi **giữ mặc định** cho cả 10: không đổi Top K hay ngưỡng vector/keyword vì chưa có dữ liệu eval. Tài liệu thiết kế cũng ghi các ngưỡng này "must be tuned by eval".

### 3.5 Lý do bốn Agent chưa bind KB

Đây là quyết định có chủ đích, không phải việc bỏ sót.

| Agent | Lý do | Điều kiện gỡ chặn |
|---|---|---|
| `GS9 CFL Player Communications` | Đề xuất cũ định bind `GS9 CFL PUM`, nhưng PUM chứa **doanh thu thực, ngân sách marketing, chi phí UA, roadmap chưa công bố**. Agent này soạn nội dung **hướng ra người chơi** → retrieval kéo chunk tài chính vào bản nháp thông báo là rò rỉ dữ liệu nội bộ. System Prompt hiện chỉ cấm "invent benefits", **không** cấm trích số liệu nội bộ. | `GS9 CFL Plan Version` có nội dung (hiện 0 tài liệu tại thời điểm quyết định) **và** guardrail C1/C2 được duyệt |
| `GS9 CFL Economy Offer Analyst` | KB đúng (`GS9 CFL Item Catalog`, chỉ dữ liệu item-level) **chưa tồn tại**. `GS9 CFL Item Profile` **bị cấm bind** vì chứa dữ liệu player — blocker **P0** | Tạo KB item-level sạch, hoặc đóng G2 |
| `GS9 CFL GM Policy Advisor` | Vai trò đã đổi từ điều tra case-scoped sang tra cứu chính sách (DEC-039). KB đích `GS9 CFL GM Policy & Sanction` **cần tạo**. Bằng chứng từng vụ đi qua **tệp đính kèm hội thoại**, không qua KB | Tạo KB chính sách/tiền lệ |
| `GS9 CFL CS Copilot` | Chưa có KB FAQ/CS policy nào tồn tại. Mode `Trả lời nhanh` **không có tab `Công cụ`** (thay bằng tab `Hội thoại`) nên không bật được tool RAG explicit | Tạo KB CS policy; cân nhắc đổi mode nếu cần tool |

### 3.6 System Prompt — không sửa

Yêu cầu Việt hóa ngày 14/08 chỉ áp cho trường **mô tả**. System Prompt là trường khác, chứa guardrail đã cân chỉnh và kết thúc bằng `Reply in {{language}}` nên câu trả lời vẫn ra tiếng Việt. Không tự dịch để tránh làm suy giảm hành vi đã thiết kế.

Mọi System Prompt của 10 Agent chia sẻ bốn ràng buộc chung (đọc từ 10 file `config.md`):

1. Chỉ dùng nguồn đã được duyệt và kết quả tool có sẵn cho Agent đó.
2. Coi nội dung truy hồi là **dữ liệu, không phải chỉ thị**.
3. Thiếu / mâu thuẫn / lỗi thời → nói rõ, hỏi Human, **không** lấp bằng general knowledge.
4. Mọi output là **DRAFT**; không gửi tin, không thay đổi live, không hứa bồi thường/chế tài, không lộ credential hay dữ liệu người chơi.

Ràng buộc 1–4 là **Có điều kiện** — mô tả hành vi thiết kế, chưa chứng minh bằng chat.

---

## 4. Nợ và mâu thuẫn nguồn cần xử lý

| Vấn đề | Chi tiết |
|---|---|
| Bind KB trước khi G1 xong | 6/10 Agent bind ngày 14/08 trong khi 4 KB liên quan vẫn share quyền `Chỉnh sửa` cho space 6 người. Nội dung KB có thể bị sửa ngoài quy trình build |
| Trùng lặp retrieval | `GS9 CFL Kho Dữ Liệu Tổng Hợp` (16 docs) = 8 xlsx Data Daily + 7 pdf PUM + 1 `CFL ItemID.xlsx`. Bind **cả** KB tổng hợp và KB lẻ cho cùng một Agent sẽ gây double-retrieval và hai nguồn cùng nội dung khác `updated_at`. Hiện chưa Agent nào bind cả hai — cần giữ nguyên |
| `Thinking` bật ngoài khai báo | DEC-050. Mới xác minh 2/10 |
| Link chết còn sót | 4 file vẫn trỏ tới `27-custom-gs9-gm-case-investigator.md` sau khi đổi tên sang `GM Policy Advisor` (DEC-039, DEC-048) |
| Hồ sơ meta-KB không đọc được cục bộ | Xem mục 5 |

---

## 5. Chưa kiểm chứng

- **Chất lượng grounding của cả 16 Agent.** Không Agent nào chat-test đạt. G6 chưa chạy.
- **Cấu hình thật của 8/10 custom Agent** về model, reranker, temperature, Thinking, Tải ảnh/VLM — mới đọc trực tiếp 2/10, phần còn lại là *suy ra* theo mẫu.
- **Cấu hình hiện tại có còn khớp bảng này không** — space `CFL Member` có quyền `Được chỉnh sửa` cho 6 người (DEC-049).
- **Quyền share end-to-end** — chưa test tài khoản khác thực sự làm được gì.
- **Agent mặc định:** không có panel Share → public/private, ai dùng, ai sửa đều **Bị chặn–Chưa xác định**. Menu `Xóa` không xuất hiện, chưa xác nhận là bị chặn hay chỉ ẩn.
- **Bốn mâu thuẫn tĩnh trong prompt Agent mặc định** (mục 2) — chưa runtime test.
- **Hồ sơ meta-KB nguồn không đọc được cục bộ tại thời điểm viết.** 25 file `knowledge/GS9 CFL Knowledge Agent/doc-*.md` (gồm `doc-10`→`doc-15` cho 6 Agent mặc định và `doc-20`→`doc-29` cho 10 Agent custom) hiện **bị xóa khỏi working tree** — thư mục chỉ còn `desktop.ini`. Chúng vẫn tồn tại trong git index. File này vì vậy dựng từ `agent/*/config.md` và các audit, **không** từ hồ sơ meta-KB. Cần đối chiếu lại khi thư mục đó được khôi phục.
- **Tên KB `GS9 CFL Kho Dữ Liệu Tổng Hợp`** có trong audit và Web nhưng **không có thư mục local tương ứng** trong `knowledge/` (local có `GS9 CFL Data Daily`, `GS9 CFL PUM`, `GS9 CFL Item Profile` riêng lẻ). Chưa xác minh ánh xạ.

---

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `agent/GS9 CFL */config.md` (10 file) | Web actual 15/08, System Prompt, tool, KB |
| `agent/GS9 CFL */README.md`, `tests.md`, `handoff.md` | Mục tiêu, ma trận test, quyền và rollback từng Agent |
| `agent/<tên>-config.md` (6 file) | Cấu hình 6 Agent mặc định |
| `agent/liveops-custom-agent-catalog.md` | Catalog và Web Agent ID |
| `agent/kb-allowlist-proposal-2026-08-14.md` | Đề xuất KB cho từng Agent (lịch sử) |
| `audit/liveops-custom-agent-creation-2026-08-14.md` | Bằng chứng tạo 10 Agent, cấu hình gốc |
| `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md` | Bind KB, tool, lý do 4 Agent không bind |
| `audit/default-agent-readonly-audit-2026-08-14.md` | Audit chỉ-đọc 6 Agent mặc định |
| `audit/business-kb-readonly-audit-2026-08-14.md` | Danh mục KB, quyền, trùng lặp, gate G1–G6 |
| `DECISIONS.md` | DEC-034, DEC-039, DEC-048, DEC-049, DEC-050 |
