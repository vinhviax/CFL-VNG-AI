# Agent: kho tri thức, truy hồi và công cụ

**Phạm vi:** tab `Kho tri thức`, tab `Công cụ` và tab `Chiến lược truy hồi` — bind KB, lọc loại tệp, ngưỡng truy hồi, danh mục tool và nguyên tắc least privilege.
**Ngày kiểm chứng gần nhất:** 15/08/2026.
**Nguyên tắc nền:** DEC-022 — bind được KB và bật được tool **không** chứng minh Agent truy hồi đúng.

---

## 1. Chọn KB là control bảo mật, không phải tiện lợi

### Ba phạm vi

| Phạm vi | Nghĩa | Dùng khi nào |
|---|---|---|
| `Tất cả kho tri thức` | Agent dùng được **mọi** KB mà nó được phép truy cập | Hạn chế dùng cho nghiệp vụ. Cả 6 Agent mặc định đang ở mức này |
| `Kho tri thức đã chọn` | Giới hạn vào danh sách cụ thể | **Lựa chọn đúng cho production.** Cả 6 Agent custom có bind đều dùng mức này |
| `Không dùng kho tri thức` | Agent không cần RAG | 4/10 Agent custom đang ở mức này (do chưa có nguồn hợp lệ) |

**Kết luận của audit 14/08/2026, dành riêng cho thiết kế tương lai:** *không clone trực tiếp bất kỳ Agent mặc định nào cho việc nghiệp vụ nhạy cảm* — cả sáu đều chọn `Tất cả kho tri thức`, và bản clone sẽ kế thừa scope đó.

### Loại tệp

Loại tệp quan sát được trên UI (11/08/2026, danh sách có thể đổi theo tenant):
`PDF` · `DOCX` · `TXT` · `MD` · `CSV` · `XLSX` · `XLS` · `JSON` · `PPTX` · `HTML` · `MSG` · `EML`

Để trống danh sách = cho phép **mọi** loại được hỗ trợ trong phạm vi KB. Thu hẹp loại tệp là cách rẻ nhất để giảm nhiễu trước khi động vào ngưỡng.

Ví dụ đang chạy: `Data Analyst` giới hạn chỉ `CSV`, `XLSX` (14/08/2026). Agent kiểm thử ngày 11/08 giới hạn chỉ `MD`.

### Công tắc `Chỉ truy hồi khi được nhắc`

| Trạng thái | Hành vi |
|---|---|
| **Tắt** | Agent tự động dùng KB đã cấu hình khi thấy cần |
| **Bật** | Chỉ truy hồi khi Human dùng `@` (`Nhắc tri thức / tệp`) trong composer |

Phép thử 11/08/2026: bật công tắc rồi gỡ chip KB → lượt hỏi **không có phạm vi để truy hồi**. Sau khi thêm `Knowledge VNG AI (13)` qua `@` → hệ thống **có** gọi truy hồi; nhưng model ở lượt đó lộ chuỗi thô `[[chunk#12]]` thay vì tổng hợp hoàn chỉnh.

Bài học tách lớp: **`@` quyết định phạm vi truy hồi; model/prompt quyết định chất lượng tổng hợp.** Hai lỗi khác nhau, đừng gộp.

`@` là lựa chọn **scope**, không phải quyền vượt access control.

Trạng thái hiện tại: cả 6 Agent mặc định đều để công tắc này **Tắt** (auto retrieve, 14/08/2026).

---

## 2. Chiến lược truy hồi — thứ tự lọc

```text
Từ khóa + vector tạo danh sách ứng viên
  → ngưỡng keyword / ngưỡng vector loại kết quả yếu
  → reranker chấm lại ứng viên còn lại
  → Top K rerank + ngưỡng rerank quyết định context cuối
  → context → model
```

### Giá trị mặc định và giá trị đang chạy

| Tham số | Mặc định quan sát 11/08 | Quick Answer | Smart / Hybrid / Wiki | Data Analyst | FPA Analyst |
|---|---:|---:|---:|---:|---:|
| Top K vector | `10` | `10` | `10` | `5` | `10` |
| Ngưỡng từ khóa | `0,3` | `0.3` | `0.3` | `0.3` | `0.3` |
| Ngưỡng vector | `0,5` | `0.5` | `0.5` | `0.5` | **`0.3`** |
| Top K xếp hạng lại | `5` | `10` | `10` | `5` | `10` |
| Ngưỡng xếp hạng lại | `0,5` | `0.3` | `0.3` | `0.3` | `0.3` |

Cột "mặc định quan sát 11/08" lấy từ Agent kiểm thử; năm cột còn lại là 6 Agent mặc định, kiểm chứng 14/08/2026. Hai bộ giá trị **không giống nhau** ở Top K rerank và ngưỡng rerank — dropdown mặc định của hộp tạo mới không trùng cấu hình Agent mặc định.

`Quick Answer` còn có hai control riêng của mode `Trả lời nhanh` (14/08/2026): `Mở rộng truy vấn` **Bật**, `Phân tích bảng dữ liệu` Tắt, và `Chiến lược dự phòng` = `Mô hình tự sinh`.

### 10 Agent custom: giữ nguyên mặc định, có lý do

Không đổi Top K hay ngưỡng vector/keyword cho bất kỳ Agent custom nào (14/08/2026). Lý do ghi rõ: **chưa có dữ liệu eval**; chính tài liệu thiết kế cũng ghi các ngưỡng này *"must be tuned by eval"*. Đổi ngưỡng khi chưa có bộ câu hỏi chuẩn là đoán mò có ghi chép.

### Quy tắc chỉnh ngưỡng

- Ngưỡng **quá cao** → bỏ sót. Ngưỡng **quá thấp** → đưa nhiễu vào context.
- **Đổi một tham số mỗi lần.** Giữ cố định corpus và query.
- Chạy lại đủ bốn loại câu: đúng · diễn đạt lại · dễ nhầm (near-duplicate) · ngoài phạm vi (no-hit).
- Không có giá trị "đúng cho mọi KB". Ghi lại ảnh hưởng lên **no-hit**, không chỉ lên câu đúng.
- Nếu nguồn nhiễu: **giảm scope / lọc loại tệp trước**, đừng động vào ngưỡng ngay.

### Xung đột nguồn — retrieval không biết cái nào là chuẩn

| Trạng thái nguồn | Hành vi mong muốn |
|---|---|
| Một nguồn canonical rõ, không xung đột | Trả lời và trích nguồn |
| Canonical + near-duplicate có nhãn | Trả lời theo canonical, **cảnh báo mâu thuẫn** |
| Hai nguồn đồng cấp mâu thuẫn | **Không tự quyết**; hỏi Human/owner hoặc báo không xác định |
| Nguồn không chứa claim được hỏi | No-hit có căn cứ, không nội suy |

Tài liệu canonical phải mang **nhãn/metadata rõ trong chính nội dung**; prompt phải yêu cầu Agent hiển thị mâu thuẫn và **không "bỏ phiếu" bằng số lượng chunk**.

---

## 3. Danh mục tool

Sáu nhóm tool đã kiểm chứng trên UI (14/08/2026):

| Nhóm | Tool | Điều kiện bật |
|---|---|---|
| **Điều phối, không cần KB** | `Suy nghĩ` · `Lập kế hoạch (todo)` · `Hỏi người dùng` | Bật được ngay khi Agent ở mode Smart |
| **RAG-4** | `Tìm theo ngữ nghĩa` · `Tìm theo từ khóa` · `Liệt kê đoạn` · `Thông tin tài liệu` | **Cần KB đã chọn và đã audit** |
| **Wiki-3** | `Tìm wiki` · `Đọc trang wiki` · `Đọc tài liệu nguồn` | Cần KB **đã bật Wiki** và nguồn được phép |
| **Data-2** | `Lược đồ dữ liệu` · `Phân tích dữ liệu` | Cần bảng/CSV/XLSX đã được curate |
| **Database** | `Truy vấn CSDL` | Cần view read-only, allowlist, phạm vi dữ liệu riêng |
| **Catalog** | `Danh mục sản phẩm` | Cần catalog read-only đã kiểm chứng game/region/environment |

> **`Suy nghĩ` là tên một TOOL.** Khác hoàn toàn với tham số cấp model `Chế độ suy nghĩ` / Thinking ở tab `Cấu hình mô hình`. Hai thứ trùng tên, khác lớp, bật/tắt độc lập. Xem `Agent-cau-hinh-va-tham-so.md` mục 4.

### Hành vi UI: tool truy hồi bị khóa theo KB

Phát hiện 14/08/2026, quan trọng cho mọi người cấu hình lần đầu:

- Khi Agent **chưa bind KB**, toàn bộ nhóm `TRUY HỒI TRI THỨC` **bị mờ** với chú thích `Cần có kho tri thức trong phạm vi`. **Bắt buộc bind KB trước, mới bật được tool.**
- Nhóm Wiki có chú thích riêng: `Cần kho tri thức đã bật Wiki`.
- Tab `Công cụ` hiển thị phạm vi KB dạng `n KB RAG · n KB Wiki` → dùng để **xác nhận bind thành công trước khi bấm Lưu**.
- Cả 9 KB trong dropdown đều hiển thị nhãn `RAG` và `WIKI` — nhãn này **không** chứng minh Wiki index có nội dung.

---

## 4. Least privilege — DEC-034

**Nguyên tắc:** basic tool được phép dùng khi Agent chưa có KB. RAG / Wiki / Data / SQL / Catalog **chỉ bật sau khi audit nguồn và quyền**.

Sáu điều kiện phải có trước khi bật một tool source-bound: **source owner · ACL · retention · sensitivity · freshness · gold-set test**. Thiếu một điều là chưa đủ.

Ba tool **không được bật** cho bất kỳ Agent custom nào tính đến 15/08/2026: `Truy vấn CSDL`, `Danh mục sản phẩm`, và toàn bộ nhóm Wiki. Lý do: chưa có view read-only/allowlist cho database, chưa kiểm chứng catalog, và **Wiki index chưa được kiểm chứng có nội dung**.

`Liệt kê đoạn`, `Phân tích dữ liệu`, `Lược đồ dữ liệu` cũng đang Off trên cả 10.

### Tại sao meta-KB không phải chìa khóa mở tool

KB `GS9 CFL Knowledge Agent` (`1d92448f-7ee2-46c4-b202-5efbe9cc5616`) là **meta-KB cho Human** hiểu/chọn/dùng 16 Agent. Nó **không** mặc nhiên là dữ liệu nghiệp vụ. DEC-034 ghi rõ: *không bind meta-KB hay KB CFL nghiệp vụ vào Agent chỉ để mở khóa tool.*

---

## 5. Trạng thái bind KB và tool — Web actual 15/08/2026

| Agent | KB đã bind | Số tool | Tool hiệu lực |
|---|---|---:|---|
| `GS9 CFL Knowledge Curator` | `GS9 Knowledge VNG AI` + `GS9 CFL Knowledge Agent` | 6 | Ask · Think · Todo · Semantic · Keyword · Doc info |
| `GS9 CFL LiveOps Planner` | `GS9 Knowledge VNG AI` | 6 | Ask · Think · Todo · Semantic · Keyword · Doc info |
| `GS9 CFL KPI Experiment Analyst` | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | 6 | Ask · Think · Todo · Semantic · Keyword · Doc info |
| `GS9 CFL Release Reviewer` | `GS9 Knowledge VNG AI` | 5 | Ask · Think · Todo · Semantic · Keyword |
| `GS9 CFL Incident Triage` | `GS9 CFL PUM` | 5 | Ask · Think · Todo · Semantic · Keyword |
| `GS9 CFL Player Voice Analyst` | `GS9 CFL Sentiment Feedback User` | 4 | Ask · Think · Semantic · Keyword |
| `GS9 CFL Economy Offer Analyst` | **Không bind** | 3 | Ask · Think · Todo |
| `GS9 CFL Player Communications` | **Không bind** | 3 | Ask · Think · Todo |
| `GS9 CFL GM Policy Advisor` | **Không bind** | 2 | Ask · Todo |
| `GS9 CFL CS Copilot` | **Không bind** | 0 | Không có tab `Công cụ` (mode `Trả lời nhanh`) |

Bằng chứng: mỗi lần lưu có toast `Đã cập nhật trợ lý`; hàng danh sách sau lưu hiển thị đúng số KB và số tool; mọi Agent ID đối chiếu khớp `agent/liveops-custom-agent-catalog.md` **trước khi** sửa (14/08/2026), xác minh lại 15/08/2026.

Cả 6 Agent có bind đều dùng `Kho tri thức đã chọn` — **không Agent nào dùng `Tất cả kho tri thức`**. Đúng boundary.

### Bốn Agent không bind — lý do cụ thể, không phải "chưa làm"

| Agent | Lý do không bind |
|---|---|
| `GS9 CFL Player Communications` | Đề xuất ban đầu là bind `GS9 CFL PUM`. **Từ chối có chủ đích:** PUM chứa doanh thu thực, ngân sách marketing, chi phí UA, roadmap chưa công bố; Agent này lại soạn nội dung **hướng ra người chơi**. Retrieval kéo một chunk số liệu tài chính vào bản nháp thông báo = **rò rỉ dữ liệu nội bộ**. System Prompt hiện chỉ cấm "invent benefits", **không cấm trích số liệu nội bộ**. Nguồn đúng là `GS9 CFL Plan Version`, hiện 0 tài liệu tại thời điểm quyết định |
| `GS9 CFL Economy Offer Analyst` | KB đúng (`GS9 CFL Item Catalog`, chỉ dữ liệu item-level) **chưa tồn tại**. `GS9 CFL Item Profile` **bị cấm bind** vì chứa dữ liệu người chơi — blocker P0 |
| `GS9 CFL GM Policy Advisor` | Ban đầu cần case-scoped view theo từng vụ — không nguồn nào phù hợp. Sau DEC-039, KB đích là `GS9 CFL GM Policy & Sanction` (L6), **cần tạo** |
| `GS9 CFL CS Copilot` | Chưa có KB FAQ/CS policy nào tồn tại |

Đây là mẫu ra quyết định nên lặp lại: **thà để Agent không bind còn hơn bind một KB sai loại dữ liệu.**

### Kết quả audit nguồn (14/08/2026)

| KB | Kết luận |
|---|---|
| `GS9 Knowledge VNG AI` | Tài liệu nền tảng VNG AI — **không** phải corpus nghiệp vụ game cho mọi Agent |
| `GS9 Knowledge VNG - Image Assets` | Asset host (PNG + URI MinIO). **Không dùng làm RAG corpus** |
| `GS9 CFL Data Daily` | Có KPI tổng hợp phù hợp KPI Analyst, nhưng ACL/retention/freshness/ingestion completeness **chưa xác minh đủ** |
| `GS9 CFL PUM` · `GS9 CFL Item Profile` · `GS9 CFL Sentiment Feedback User` | Có rủi ro dữ liệu cá nhân, credential/system metadata hoặc nội dung nhạy cảm — **không bind as-is** |

Lưu ý: `GS9 CFL PUM` và `GS9 CFL Sentiment Feedback User` **về sau vẫn được bind** (cho `Incident Triage` và `Player Voice Analyst`). Đây là một điểm cần đối chiếu — xem mục "Chưa kiểm chứng".

Nhãn Space hiện tại **không** chứng minh quyền dùng cho từng Agent. `GS9 CFL Data Daily`, `GS9 CFL PUM`, `GS9 CFL Item Profile` hiển thị thuộc space `CFL Member` — đó là nhãn, không phải phê duyệt.

---

## 6. Blocker đang mở: G1 — KB chia sẻ quyền `Chỉnh sửa`

Tại 14/08/2026, **4 trong 6 KB vừa bind** vẫn đang chia sẻ quyền `Chỉnh sửa` cho space `CFL Member` (6 thành viên): `GS9 Knowledge VNG AI` (×3 Agent), `GS9 CFL PUM`, `GS9 CFL Kho Dữ Liệu Tổng Hợp`.

Nghĩa là **nội dung KB có thể bị sửa ngoài quy trình build**. Việc bind không làm rủi ro này nặng thêm, nhưng nó chưa được đóng. Người dùng tự xử lý việc hạ quyền.

Cộng thêm DEC-049: **cả 10 Agent cũng đang share quyền `Được chỉnh sửa`** cho cùng space. Nghĩa là cả **nội dung** lẫn **cấu hình** đều có thể thay đổi mà không qua quy trình. Trước khi kết luận bất cứ điều gì, audit lại.

---

## 7. Chẩn đoán: nguồn sai hoặc không có nguồn

Kiểm **theo đúng thứ tự này**, dừng ở lớp đầu tiên tìm ra vấn đề:

1. **KB scope** — Agent có bind KB không? Đúng KB không?
2. **`@` / chip** — công tắc `Chỉ truy hồi khi được nhắc` đang bật? Human đã chọn chip chưa?
3. **Loại tệp** — file đúng có nằm trong bộ lọc không?
4. **Tool** — `Tìm theo ngữ nghĩa` / `Tìm theo từ khóa` đã bật chưa?
5. **Ngưỡng + Top K** — quá cao gây bỏ sót?
6. **Reranker** — có đẩy nguồn đúng tụt hạng không?

**Đừng sửa prompt trước.** Đừng đổi model trước. Đó là hai bước tốn nhất và ít khi là nguyên nhân.

| Hiện tượng | Lớp cần kiểm | Không được kết luận |
|---|---|---|
| Không có nguồn nào | Scope → `@` → loại tệp → tool → ngưỡng | "Model yếu" |
| Có chunk nhưng lộ `[[chunk#...]]` | Lớp tổng hợp model/prompt | "KB hỏng" — **không sửa file nguồn** |
| Nguồn đúng, câu trả lời sai | Prompt, thứ tự context, nhiệt độ | "Retrieval hỏng" |
| Nguồn sai hoặc nhiễu | KB đã chọn, Top K, ngưỡng, reranker | "Cần thêm tài liệu" |
| Tool truy hồi bị mờ, không bật được | Agent chưa bind KB | "Tool bị lỗi" |
| Nhóm Wiki bị mờ | KB chưa bật Wiki | "Nền tảng không có Wiki" |
| Nguồn từ KB không được phép | Scope đang là `Tất cả kho tri thức` | — kiểm ngay, đây là sự cố dữ liệu |

Kiểm chứng một câu trả lời RAG, năm bước: đọc câu trả lời → mở chip nguồn xác nhận đúng tài liệu → **mở đoạn nguồn xác nhận nó thực sự chứa bằng chứng** → nếu cần ảnh, xác nhận ảnh **render** trong chat chứ không chỉ có link → hỏi một câu ngoài phạm vi để kiểm Agent biết dừng.

---

## 8. Human approval gate

Không tool nào trong 16 Agent được phép tự thực hiện các việc sau. Mọi việc này cần **Human phê duyệt ngoài Agent**:

gửi/publish/schedule tin nhắn · sửa event/config/live service · account action · sanction · compensation · grant item · thay đổi data/KB · mọi thao tác vận hành live.

Tính đến 15/08/2026 **không tool gửi, publish, deploy, sửa cấu hình live, account action hay KB mutation nào được bật** trên bất kỳ Agent nào.

---

## 9. Chưa kiểm chứng

- **Toàn bộ chất lượng truy hồi của 10 Agent custom.** Chưa Agent nào chat-test đạt; gate G6 (xác nhận `Nguồn tham khảo` đúng và không lộ PII) **chưa chạy**. *Bị chặn – Chưa xác định*.
- **Tác dụng của reranker `bge-reranker-v2-m3`** vừa bật 15/08/2026 cho cả 10 Agent — chưa test. Có thể đổi hoàn toàn thứ tự nguồn so với mọi quan sát trước đó (DEC-049).
- **Mâu thuẫn cần đối chiếu:** audit 14/08 xếp `GS9 CFL PUM` và `GS9 CFL Sentiment Feedback User` vào nhóm "có rủi ro dữ liệu cá nhân/nhạy cảm — không bind as-is", nhưng cùng ngày hai KB này **đã được bind** cho `Incident Triage` và `Player Voice Analyst`. Các audit không ghi lại bước phê duyệt trung gian nào giữa hai kết luận. Cần xác minh trước khi coi hai binding này là đã qua audit đầy đủ.
- **Wiki index có nội dung hay không.** Cả 9 KB hiển thị nhãn `WIKI` trong dropdown, nhưng nhãn ≠ nội dung. Đây là lý do toàn bộ Wiki-3 đang Off.
- **Hành vi end-to-end của Wiki-3, Data-2, `Truy vấn CSDL`, `Danh mục sản phẩm`** — chỉ quan sát trong catalog/cấu hình; chưa chạy thật trên bất kỳ Agent nào của dự án.
- **ACL, retention, freshness, ingestion completeness** của `GS9 CFL Data Daily` và các KB nghiệp vụ khác — chưa xác minh đủ (14/08/2026).
- **Dữ liệu backend thật của Product Catalog / Database** — *Bị chặn – Chưa xác định*.
- **Effective access theo từng Human/Space** — nhãn Space không chứng minh quyền dùng.
- **Giá trị ngưỡng tối ưu cho từng KB** — chưa có eval, chưa có gold-set. Mọi ngưỡng hiện tại là mặc định nền tảng, giữ nguyên có chủ đích.
- **Gate G1 chưa đóng** — 4/6 KB đã bind vẫn share quyền `Chỉnh sửa` cho space 6 người (14/08/2026).
- **Tính ổn định của bảng mục 5** — cả 10 Agent share quyền `Được chỉnh sửa` (DEC-049); bind KB và tool có thể bị người khác đổi bất cứ lúc nào.
