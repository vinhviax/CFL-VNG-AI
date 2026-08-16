# KB — Quy hoạch nghiệp vụ 7 tầng và ranh giới giữa các Knowledge Base

**Đối tượng:** Dev và người cấu hình Agent. Người cần biết *một tài liệu thuộc KB nào và vì sao*.
**Ngày viết:** 16/08/2026.
**Trạng thái tổng thể:** bản đồ đích là **thiết kế đã chốt, chưa thực hiện trên Web** (spec 15/08/2026, DEC-036). Không mục nào ở đây là mô tả trạng thái Web hiện tại.

**Nguồn:**

| Nguồn | Ngày | Vai trò |
|---|---|---|
| `docs/superpowers/specs/2026-08-15-kb-architecture-design.md` | 15/08/2026 | Bản đồ 7 tầng — nguồn chuẩn |
| `DECISIONS.md` DEC-036, 037, 038, 040, 044 | 15/08/2026 | Luật bền vững |
| `PROJECT.md` mục "Quy hoạch KB nghiệp vụ LiveOps" | 15/08/2026 | Ràng buộc project |
| `agent/kb-allowlist-proposal-2026-08-14.md` | 14/08/2026 | **Bản nháp cũ, đã bị thay thế** (DEC-036) — chỉ giữ làm bằng chứng lịch sử |
| `audit/business-kb-readonly-audit-2026-08-14.md` | 14/08/2026 | Bằng chứng read-only về 9 KB thật trên Web |

---

## 1. Vấn đề mà bản đồ này giải quyết

Dự án tạo 10 custom Agent **trước** khi có bản đồ KB. Hệ quả đo được (spec mục 1, 15/08/2026):

- 4/10 Agent không có nguồn nào phù hợp tồn tại. Đây là lỗi **quy hoạch**, không phải lỗi bind.
- 2 Agent (`LiveOps Planner`, `Release Reviewer`) bind `GS9 Knowledge VNG AI` — đó là sổ tay dùng nền tảng VNG AI, không phải tri thức về game. Bind vì đó là KB P3 duy nhất sẵn có. Đây là lỗi **phân loại**.
- `GS9 CFL Item Profile` trộn dữ liệu item-level (vô hại) với player-level (PII) trong cùng một kho → cả KB thành P0 → `Economy Offer Analyst` mất nguồn dù dữ liệu nó cần vẫn nằm đó.

Một nguyên nhân chung: **KB được vẽ theo nguồn dữ liệu, không theo mục đích tiêu thụ.**

DEC-036 (15/08/2026) chốt hướng ngược lại: ranh giới KB vẽ theo **(mức nhạy cảm × đối tượng đọc × nhịp cập nhật)**, và quy hoạch phải đi **trước** việc bind.

---

## 2. Ràng buộc nền tảng chi phối mọi ranh giới

Đây là các ràng buộc của VNG AI, không phải lựa chọn thiết kế. Trạng thái: **Đã kiểm chứng** qua audit UI/MCP 14–15/08/2026 (`audit/business-kb-readonly-audit-2026-08-14.md`, `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md`).

| Ràng buộc nền tảng | Hệ quả lên ranh giới KB |
|---|---|
| Share chỉ có ở **cấp KB**, không có cấp tài liệu | KB = **đơn vị phân quyền**. Trộn hai mức nhạy cảm trong một KB là mất quyền kiểm soát vĩnh viễn |
| Agent bind **cả KB**, không bind được một phần | KB = **đơn vị phạm vi truy hồi** |
| Không có TTL/expiry/auto-purge ở cấp KB | KB = **đơn vị vòng đời**; hết hạn phải xử lý bằng quy ước |
| `Chiến lược lập chỉ mục` **bị khoá sau khi KB có nội dung** | Chọn RAG / RAG+Wiki / Graph **ngay lúc tạo**. Sai là phải tạo KB mới và nạp lại |
| KB có `Loại`: `Tài liệu` hoặc `FAQ`, không đổi được sau | Chọn sai loại = tạo lại KB |
| Có **nhãn (tag) cấp tài liệu** — endpoint `/tags`, bộ lọc `Danh mục tài liệu` | Cơ chế **duy nhất** để phân biệt lát cắt bên trong một KB |
| Share KB vào space đồng thời mở KB đó cho **MCP connector** | Một đường truy cập song song với Agent binding, phải tính vào mô hình rủi ro |
| Mode `Trả lời nhanh` **không có tab Công cụ** | Agent mode này vẫn RAG được nhưng không cấu hình được tool truy hồi |
| Tool truy hồi bị khoá khi Agent chưa bind KB | Luôn bind KB trước, bật tool sau |

---

## 3. Bốn trục phân loại

**Mức nhạy cảm** — trục quyết định nhất, vì share nằm ở cấp KB.

| Mức | Định nghĩa | Ví dụ | Được bind? |
|---|---|---|---|
| **P0** | Định danh/hành vi người chơi | `openid`, `roleid`, `nickname`, lịch sử nạp | Không bao giờ |
| **P1** | Nội bộ mật | Doanh thu, ngân sách UA, kế hoạch chưa công bố | Chỉ Agent hướng nội bộ |
| **P2** | Nội bộ thường | Chỉ số tổng hợp, feedback đã ẩn danh | Có điều kiện |
| **P3** | Nội bộ phổ biến | Sổ tay nền tảng, tài liệu đã phát hành | Tự do |

**Đối tượng output:** `Human-only` · `Agent-nội-bộ` · `Agent-hướng-người-chơi`
**Nhịp cập nhật:** `static` · `versioned` · `periodic (D/W/M)` · `streaming` · `case-scoped`
**Vòng đời:** `permanent` · `rolling N tháng` · `theo phiên bản` · `theo vụ việc`

### Bảy nguyên tắc quy hoạch

1. **Một KB = một (mức nhạy cảm × đối tượng đọc × nhịp cập nhật).** Không trộn ba trục.
2. **Một tài liệu chỉ có đúng một KB là nguồn chuẩn.** Bản sao trong KB tổng hợp được phép nhưng phải khai báo là **dẫn xuất**, và **không Agent nào bind đồng thời KB tổng hợp lẫn KB lẻ cấu thành nó** — đó mới là chỗ gây double-retrieval và hai `updated_at` mâu thuẫn.
3. **Không đổi tên KB đang chạy** (DEC-037). Thay bằng "dòng bản chất" ở mục 5.
4. **KB không có pipeline dựng lại + audit thì không được bind cho Agent.**
5. **Không dùng `Tất cả kho tri thức`** cho bất kỳ Agent nào.
6. **Dữ liệu định danh người chơi không bao giờ nằm trong KB được bind.** Không ngoại lệ.
7. **KB hướng-người-chơi và KB nội bộ không chung một Agent** trừ khi System Prompt có guardrail đã duyệt.

---

## 4. Bản đồ 7 tầng

```text
L0  Nền tảng & Meta        về hệ thống AI, KHÔNG phải về game
    ├── GS9 Knowledge VNG AI              cefadf09-4187-46ac-a765-591e3255a4a4   P3  static
    ├── GS9 Knowledge VNG - Image Assets  6da8657c-dd96-4170-a698-074043475014   P3  asset host
    └── GS9 CFL Knowledge Agent           1d92448f-7ee2-46c4-b202-5efbe9cc5616   P3  static
                    └── chỉ Knowledge Curator được bind

L1  Canon                  sự thật về game, ổn định
    ├── GS9 CFL Item Catalog          [TẠO MỚI]  P1  periodic-W  tách từ Item Profile
    └── GS9 CFL Glossary & Systems    [TẠO MỚI]  P3  static      chưa có nguồn

L2  Kế hoạch               hướng tương lai, chưa phát hành
    ├── GS9 CFL Plan Version          1452bc9a-c8b4-487b-b623-34e0b00a83e9  P1  versioned
    └── GS9 CFL Event Calendar & Brief [TẠO MỚI] P1  periodic-M  chưa có nguồn

L3  Vận hành               đang chạy
    └── GS9 CFL Runbook & Known Issues [TẠO MỚI] P2  rolling 12 tháng  chưa có nguồn

L4  Kết quả                hướng quá khứ, số liệu
    ├── GS9 CFL Kho Dữ Liệu Tổng Hợp  574d4d12-8421-4e6f-9628-d03f4f7fb475  P2  periodic-M  DẪN XUẤT
    ├── GS9 CFL PUM                   90484cd2-93fa-4d45-a37f-43c0d50430f2  P2  periodic-M
    └── GS9 CFL Data Daily            7be35c7c-c1fc-4538-bb1c-470f18378ae9  P2  periodic-M

L5  Tiếng nói người chơi
    └── GS9 CFL Sentiment Feedback User   [CHƯA LẤY ĐƯỢC ID]  P2  periodic-M

L6  Dịch vụ người chơi
    ├── GS9 CFL CS FAQ & Policy       [TẠO MỚI]  Loại=FAQ       P3  rolling
    └── GS9 CFL GM Policy & Sanction  [TẠO MỚI]  Loại=Tài liệu  P2  static

L7  Cách ly                KHÔNG BAO GIỜ BIND
    ├── GS9 CFL Item Profile          e99b635f-04ec-44ad-9bcc-f12cae587c7d  P0
    └── GS9 test knowledge base       6f887ec5-dab1-4505-999f-fb99c2280da9  của người khác
```

**5/12 KB đích chưa tồn tại và chưa có nguồn** (spec mục 6, 15/08/2026). Đây là công việc **nội dung**, không phải công việc cấu hình — và là lý do thật khiến 4 Agent bế tắc.

### Ghi chú theo tầng

- **L0** chỉ phục vụ `Knowledge Curator`. Mọi Agent nghiệp vụ LiveOps bind vào đây là lỗi phân loại.
- **L0 / Image Assets** là asset host cấp URI MinIO. **Không bao giờ bind làm corpus hỏi đáp.** Local đã gộp 49 PNG vào cùng thư mục `GS9 Knowledge VNG AI` (DEC-043); KB Web tách riêng **vẫn chưa xoá**, chờ Phase 3 hoàn tất và chat-test đạt (DEC-005, DEC-043).
- **L1 / Glossary** là mắt xích thiếu quan trọng nhất cho `Player Communications` và `CS Copilot`: không có nó thì Agent tự chế tên hệ thống.
- **L2 / Plan Version** dùng **một KB cho mọi phiên bản** (quyết định người dùng 15/08). Xem mục 7.
- **L4 / Kho Dữ Liệu Tổng Hợp** là **dẫn xuất có chủ đích** (DEC-038): gom nhiều KB lẻ để xem Wiki/Graph ở góc nhìn toàn cảnh mà KB lẻ không cho được — vì Wiki/Graph sinh trên phạm vi toàn KB nên phạm vi khác thì kết quả khác. **Không phải trùng lặp nhầm.**
- **L4 / PUM** hạ từ P1 xuống **P2 nội bộ** (DEC-038, cả team được đọc doanh thu). Ràng buộc *"không để số liệu doanh thu lọt vào nội dung gửi người chơi"* **giữ nguyên** — đó là rủi ro đầu ra, không phải rủi ro phân quyền.
- **L4 / Data Daily** giữ dùng bình thường (DEC-038). Đề xuất "hạ xuống staging" ở bản spec đầu tiên đã bị rút vì là suy diễn quá tay.
- **L5** chỉ bind sau khi quét PII trong 85.365 dòng `Comment Message`. Cấm trả nguyên văn comment; chỉ tổng hợp theo `Topic`/`Sentiment`/`Emotion`.
- **L6 / CS FAQ** phải chốt `Loại: FAQ` **lúc tạo** — không đảo ngược được.

---

## 5. Bảng bản chất — thay cho việc đổi tên (DEC-037)

DEC-037 (15/08/2026) cấm đổi tên KB đang chạy, để không phá vỡ tham chiếu, thói quen và tài liệu cũ. Thay vào đó mỗi KB có một **dòng bản chất**. Khi cần biết một KB đóng vai gì, **tra bảng này, không suy từ tên**.

| Tên đang chạy (giữ nguyên) | Tầng | Bản chất trong luồng | Vai trò dữ liệu | Ai được bind |
|---|---|---|---|---|
| `GS9 Knowledge VNG AI` | L0 | **Sổ tay dùng nền tảng VNG AI.** Không phải tri thức về game | nguồn chuẩn | chỉ `Knowledge Curator` |
| `GS9 Knowledge VNG - Image Assets` | L0 | **Kho ảnh cấp URI MinIO.** Dependency kỹ thuật, không phải corpus hỏi đáp | nguồn chuẩn | không Agent nào |
| `GS9 CFL Knowledge Agent` | L0 | **Meta-KB mô tả 16 Agent.** Dành cho người | nguồn chuẩn | chỉ `Knowledge Curator` |
| `GS9 CFL Plan Version` | L2 | **Kế hoạch phiên bản sắp phát hành, nhiều phiên bản chung một kho.** Nội bộ, chưa chốt | nguồn chuẩn | Planner, Release Reviewer, Player Communications |
| `GS9 CFL PUM` | L4 | **Báo cáo kết quả theo tháng.** Nhìn về quá khứ, có doanh thu và ngân sách | nguồn chuẩn | Agent hướng nội bộ |
| `GS9 CFL Data Daily` | L4 | **Số liệu vận hành theo kỳ.** Hạt mịn hơn PUM | nguồn chuẩn | Agent phân tích, **không chung Agent với KB tổng hợp** |
| `GS9 CFL Kho Dữ Liệu Tổng Hợp` | L4 | **Lăng kính toàn cảnh để xem Wiki** | **dẫn xuất** | `KPI Experiment Analyst` + bật tool Wiki |
| `GS9 CFL Sentiment Feedback User` | L5 | **Tiếng nói người chơi.** Free-text chưa quét PII | nguồn chuẩn | `Player Voice Analyst` sau khi quét PII |
| `GS9 CFL Item Profile` | L7 | **Kho cách ly.** Trộn item-level và player-level nên toàn bộ bị coi là P0 | nguồn chuẩn | **không ai** |
| `GS9 test knowledge base` | — | KB của người khác | — | không liên quan |

**Lưu ý phiên 16/08/2026** (kiểm trực tiếp cây thư mục lúc 17:34):

- Hai thư mục local **đã có nội dung thật**, không còn là chỗ trống: `knowledge/GS9 CFL Glossary & Systems/` (3 Markdown `doc-00`→`doc-02`) và `knowledge/GS9 CFL CS FAQ & Policy/` (1 Markdown `doc-00`). Đây là hai KB nháp theo DEC-047, tương ứng **L1 / Glossary & Systems** và **L6 / CS FAQ & Policy** — hai trong 5 KB mà spec 15/08 xếp là "Tạo mới, chưa có nguồn". Nghĩa là **việc soạn nội dung đã bắt đầu**, đúng thứ tự ưu tiên 1 và 2 ở mục 10.
- KB test `Test` (`d7295a59-03b1-496c-86eb-9ecaa3364aa7`) dùng cho thực nghiệm sync ở DEC-051 **chỉ tồn tại trên Web**, không có thư mục mirror trong `knowledge/`. Nó là KB disposable theo tinh thần DEC-027, không thuộc bản đồ đích.

Cả ba đều **chưa nằm trong bảng bản chất của spec 15/08**, nên bảng trên còn thiếu.

Cập nhật tiến độ 5 KB "tạo mới": **2/5 đã có bản nháp local** (`Glossary & Systems`, `CS FAQ & Policy`); 3 KB còn lại (`Event Calendar & Brief`, `Runbook & Known Issues`, `GM Policy & Sanction`) chưa có thư mục local nào. `Item Catalog` là việc **tách** từ `Item Profile` (G2), không phải soạn mới, và cũng chưa bắt đầu.

---

## 6. Ranh giới giữa các KB — ba nhầm lẫn hay gặp

### 6.1 "Sổ tay nền tảng" ≠ "tri thức về game"

`GS9 Knowledge VNG AI` dạy cách **dùng VNG AI**. Nó không biết gì về CrossFire Legends. Bind nó cho `LiveOps Planner` không sai kỹ thuật nhưng sai nghiệp vụ: Agent sẽ trả lời câu hỏi về event bằng kiến thức về nút bấm trên nền tảng AI.

Cách nhận biết: hỏi *"tài liệu này mô tả sản phẩm nào?"*. Nếu câu trả lời là "VNG AI" thì đó là L0.

### 6.2 "KB tổng hợp" ≠ "KB lẻ gộp lại cho tiện"

`Kho Dữ Liệu Tổng Hợp` tồn tại vì **Wiki/Graph sinh theo phạm vi KB**. Một KB tổng cho ra góc nhìn mà từng KB lẻ không cho được. Hệ quả bắt buộc:

- Nó là **dẫn xuất**: KB lẻ đổi thì phải dựng lại KB tổng, nếu không `updated_at` lệch.
- **Bật nhóm tool Wiki** (`Tìm wiki`, `Đọc trang wiki`) cho Agent bind nó — đó chính là lý do nó tồn tại. Đây là ngoại lệ **có cơ sở** với quy tắc "giữ Wiki Off".
- **Không Agent nào bind đồng thời KB tổng và KB lẻ cấu thành nó.**

Trùng lặp **đã kiểm chứng** duy nhất là `CFL ItemID.xlsx` nằm ở cả `Item Profile` và `Kho Dữ Liệu Tổng Hợp`, hai `datasource_id` khác nhau nhưng cùng `external_id` Google Sheets (audit 14/08/2026).

### 6.3 "Mức nhạy cảm của KB" = mức của tài liệu nhạy cảm nhất trong đó

Vì share ở cấp KB, một file player-level kéo cả KB xuống P0. `Item Profile` là ví dụ sống: 4 file item-level vô hại bị khoá cùng 4 file player-level (`03_sample_users.csv`, `04_sample_user_weapons.csv`, `06_users_detailed.csv` 8.148 dòng, `07_users_cb.csv` 375.591 dòng).

Cách xử lý duy nhất là **tách KB** (G2): tạo `GS9 CFL Item Catalog` chỉ chứa nhóm item-level. Chỉ đổi quyền là **không đủ** — PII đã lan vào description/summary tự sinh, phải xoá và nạp lại bản đã loại `nickname` rồi re-index.

---

## 7. Chiến lược một-KB-nhiều-phiên-bản cho `Plan Version`

Quyết định người dùng: mọi phiên bản (V5, V6, …) nằm chung một KB. Quyết định này **bắt buộc** kèm ba biện pháp.

**Rủi ro trùng tên.** V6 sinh từ cùng converter sẽ ra đúng tên file của V5 → 2 tài liệu cùng tên khác nội dung, retrieval trộn V5 với V6, Agent trả kế hoạch cũ cho câu hỏi về bản mới. **Sai kiểu rất khó phát hiện.**

**Khắc phục đã chốt (DEC-042, 15/08/2026):** tiền tố phiên bản chèn sau tiền tố loại — `doc-v5-00-index-va-pham-vi.md`, `image-v5-01-….jpg`. Đã thực thi cục bộ cho 12 Markdown + 29 JPEG V5; `convert_cfl_plan_html.py` đã đặt `VERSION_TAG = "v5"` cho lần sinh sau.

**Ba biện pháp bắt buộc:**

1. **Nhãn `ver:` trên 100% tài liệu.** Không có nhãn = không được nạp.
2. **Header phiên bản trong nội dung** (mục 8) để chunk tự mang thông tin phiên bản.
3. **Guardrail G-A trong System Prompt** của mọi Agent bind KB này (DEC-040).

**Ràng buộc khoá:** 29 URI MinIO trong 12 file `.md` của V5 gắn cứng vào KB `1452bc9a…`. **Không được đổi KB đích cho Plan Version nữa** — dời là chết 29 link và phải chạy lại toàn bộ quy trình thu URI.

### Hai guardrail đã duyệt (DEC-040, 15/08/2026)

**G-A — chống trộn phiên bản.** Áp cho **mọi** Agent bind `GS9 CFL Plan Version`:

```text
The Plan Version knowledge base contains MULTIPLE game versions in one store. Always state which version each fact comes from, taken from the version header in the retrieved chunk. If the user does not name a version, ask before answering. Never merge facts from two versions into one statement.
```

**G-B — kế hoạch nội bộ không phải brief đã duyệt.** Áp riêng cho `GS9 CFL Player Communications`:

```text
The Plan Version knowledge base is an INTERNAL planning document, not an approved brief. Never quote it verbatim in player-facing copy. Never treat a planned item as confirmed for release. If an item is marked pending, placeholder, or lacks a confirmed date, state that it is unconfirmed and stop; request an approved brief instead.
```

Cả hai là **mutation live** khi áp lên Web, thực hiện cùng lúc với thao tác bind.

---

## 8. Nhãn và header bắt buộc

**Nhãn tài liệu:**

| Nhãn | Giá trị | Áp dụng |
|---|---|---|
| `ver:` | `v5`, `v6` … | L2 Plan |
| `type:` | `brief`, `runbook`, `report`, `policy`, `catalog`, `glossary` | tất cả |
| `period:` | `2026-08` | L4 |
| `status:` | `draft`, `approved`, `published` | L2, L6 |

**Header bắt buộc trong mọi Markdown:**

```markdown
> **Phiên bản:** V5 · **Trạng thái:** draft · **Hiệu lực:** chưa chốt
> **Mức:** P1 nội bộ · **Chủ sở hữu:** <team> · **Nguồn:** <file gốc + SHA-256>
```

Header nằm trong nội dung nên **đi vào chunk và xuất hiện trong `Nguồn tham khảo`** — đây là lớp phòng vệ chính khi nhiều phiên bản chung một KB.

---

## 9. Ma trận Agent × KB × tool

Dẫn xuất từ bản đồ, spec mục 9 (15/08/2026). Trạng thái là **thiết kế**, không phải Web actual.

| Agent | KB chính | KB phụ | Tool nguồn | Trạng thái |
|---|---|---|---|---|
| `Knowledge Curator` | Knowledge VNG AI (L0) | CFL Knowledge Agent (L0) | semantic + keyword + doc info | đang đúng |
| `KPI Experiment Analyst` | Kho Dữ Liệu Tổng Hợp (L4) | — | semantic + keyword + doc info **+ Tìm wiki + Đọc trang wiki** | đúng KB; bổ sung tool Wiki |
| `Player Voice Analyst` | Sentiment Feedback User (L5) | — | semantic + keyword | đúng, chờ quét PII |
| `LiveOps Planner` | **Event Calendar & Brief (L2, mới)** | Plan Version (L2) | semantic + keyword + doc info | bỏ bind Knowledge VNG AI |
| `Release Reviewer` | **Runbook & Known Issues (L3, mới)** | Plan Version (L2) | semantic + keyword | bỏ bind Knowledge VNG AI |
| `Incident Triage` | **Runbook & Known Issues (L3, mới)** | PUM (L4) | semantic + keyword | PUM là giải pháp tạm |
| `Player Communications` | Plan Version (L2) | **Glossary (L1, mới)** | semantic + keyword + doc info | chờ guardrail G-B + Glossary |
| `Economy Offer Analyst` | **Item Catalog (L1, mới)** | Kho Dữ Liệu Tổng Hợp (L4) | semantic + keyword | chờ G2 |
| `CS Copilot` | **CS FAQ & Policy (L6, mới)** | Runbook & Known Issues (L3) | RAG mặc định (mode `Trả lời nhanh` không có tab Công cụ) | chờ KB |
| `GM Policy Advisor` | **GM Policy & Sanction (L6, mới)** | — | semantic + keyword | chờ KB |

**Giữ Off toàn bộ:** `Truy vấn CSDL`, `Phân tích dữ liệu`, `Lược đồ dữ liệu`, `Danh mục sản phẩm`, `Liệt kê đoạn` (chỉ bật khi debug rồi tắt).

**Đổi vai trò `GM Case Investigator` → `GM Policy Advisor`** (DEC-039, duyệt 15/08/2026): vai trò "điều tra theo từng vụ" cần case-scoped view. Nền tảng không có cơ chế đó, và bind KB toàn tenant để điều tra một vụ là **vi phạm least privilege**. Bằng chứng từng vụ nạp qua **tệp đính kèm trong hội thoại**, không qua KB. Tên + mô tả trên Web đã đổi 15/08; System Prompt chưa.

---

## 10. Ánh xạ hiện trạng → đích, và thứ tự có gate

| Hành động | KB | Việc cụ thể |
|---|---|---|
| Giữ nguyên | Knowledge VNG AI, Image Assets, CFL Knowledge Agent, Kho Dữ Liệu Tổng Hợp, PUM | Chỉ siết ACL (G1) |
| Giữ tên, ghi bản chất | `Sentiment Feedback User` | Vẫn cần lấy ID còn thiếu |
| Giữ nguyên | `Data Daily` | Chỉ cấm bind chung Agent với KB tổng hợp |
| Tách | `Item Profile` → `Item Catalog` (mới) + phần P0 cách ly | G2, cần approval |
| Gắn nhãn | `Plan Version` | Bắt buộc `ver:v5` cho 41 tài liệu |
| Tạo mới | Glossary, Event Calendar & Brief, Runbook & Known Issues, CS FAQ, GM Policy | 5 KB — **đều chưa có nguồn** |
| Cách ly | `Item Profile` | Bỏ share, re-index |

**Thứ tự thực hiện:**

| # | Việc | Gate | Phụ thuộc |
|---|---|---|---|
| 1 | Human duyệt bản đồ | — | — |
| 2 | Siết ACL 5 KB xuống `Chỉ đọc` | G1 | Human |
| 3 | Gắn nhãn `ver:v5` cho 41 tài liệu Plan Version | — | KB xử lý xong |
| 4 | Converter tiền tố phiên bản cho lần sinh sau | — | đã xong 15/08 (DEC-042) |
| 5 | Chat-test `Incident Triage` × PUM | **G6** | #2 |
| 6 | Tách `Item Catalog`, cách ly `Item Profile` | G2 | Human |
| 7 | Soạn nội dung + tạo 5 KB còn thiếu | — | **cần nguồn từ các team** |
| 8 | Bind lại theo ma trận mục 9, mỗi Agent một audit | — | #7 |
| 9 | Gold-set eval từng Agent | — | #8 |

Bước 5 phải chạy **trước** mọi việc bind mở rộng. Tính đến 16/08/2026, **chưa có bằng chứng nào** cho thấy chuỗi bind + retrieval chạy đúng trên tenant này (G6 chưa chạy — `STATUS.md`).

**Ưu tiên soạn nội dung** (spec mục 14.2): 1. `Glossary & Systems` (bootstrap được từ `02_weapon_name_map.csv`, `CFL ItemID.xlsx`, tên hệ thống trong Plan V5 — rẻ nhất) → 2. `CS FAQ & Policy` (Agent đang trắng hoàn toàn) → 3. `Runbook & Known Issues` (bootstrap một phần từ root cause trong PUM) → 4. `Event Calendar & Brief` → 5. `GM Policy & Sanction`.

---

## 11. Quan hệ với bản allowlist 14/08/2026

`agent/kb-allowlist-proposal-2026-08-14.md` **đã bị thay thế** bởi bản đồ này (DEC-036). Khác biệt bản chất:

| | Allowlist 14/08 | Bản đồ 7 tầng 15/08 |
|---|---|---|
| Cách tiếp cận | Bind theo **KB sẵn có** | Bind theo **bản đồ đích** |
| `LiveOps Planner` | `GS9 Knowledge VNG AI` (P3, vì đó là thứ đang có) | Event Calendar & Brief (L2, phải tạo) |
| `GM Case Investigator` | không bind, để mở | đổi vai trò thành `GM Policy Advisor` (DEC-039) |
| KB tổng hợp | tránh vì sợ trùng lặp | dùng có chủ đích cho Wiki (DEC-038) |

Bản cũ vẫn hữu ích ở hai chỗ chưa bị thay thế: mô tả chi tiết điều kiện bind cứng **C1** (tài liệu nội bộ, cấm phổ biến ra ngoài) và **C2** (kế hoạch chưa chốt: FIG-00 chưa có sơ đồ, FIG-11/FIG-12 chưa có ảnh, một mô tả DOM rỗng, section thương mại hoá ghi 47 nội dung nhưng DOM có 46 item, ba cặp mô tả trùng).

---

## Chưa kiểm chứng và rủi ro còn lại

**Chưa kiểm chứng (tính đến 16/08/2026):**

- **Toàn bộ bản đồ chưa được kiểm chứng bằng runtime.** Mọi khuyến nghị bind vẫn ở mức *Có điều kiện* cho tới khi G6 đạt. Chưa có một lượt chat-test nào chứng minh chuỗi bind → retrieval → `Nguồn tham khảo` chạy đúng trên tenant `10012`.
- **ID của `GS9 CFL Sentiment Feedback User` chưa lấy được.** Không thể tham chiếu chắc chắn KB này bằng ID.
- **5 KB đích chưa tồn tại**, chưa có nguồn và chưa có format. Chưa biết ai sở hữu nội dung.
- **Chưa quét PII** cho 85.365 dòng `Comment Message` của L5.
- **G1–G6 đều chưa đóng** ngoài phần audit đọc. G3 (ghi 6 KB còn thiếu kèm ID vào `PROJECT.md`/`STATUS.md`) và G4 (mirror Data Daily thiếu `doc-CFL_082026.xlsx`) vẫn mở.

**Rủi ro còn lại:**

- **Chi phí nội dung lớn hơn chi phí cấu hình.** 5 KB mới là việc soạn tài liệu. Không có người sở hữu nội dung thì bản đồ nằm im.
- **Không đảo ngược được:** `Loại` KB và `Chiến lược lập chỉ mục` khoá sau khi có nội dung.
- **Quyết định "cả team sửa được KB" phá hợp đồng DEC-001.** Khi 6 người có quyền `Chỉnh sửa` trên Web, 20 module có thể bị sửa trực tiếp và lần build kế tiếp **ghi đè mất** thay đổi đó mà không cảnh báo. Biện pháp bù: định kỳ chạy **G5** (đối chiếu 20 module trên Web với master). Không có G5 thì không ai biết KB đã bị sửa ngoài quy trình.
- **KB tổng hợp là dẫn xuất nhưng không có pipeline dựng lại.** Hiện gom thủ công. Quên dựng lại → Wiki toàn cảnh mô tả trạng thái cũ, sai theo kiểu khó phát hiện.
- **Share KB vào space mở luôn đường MCP.** Mọi phân tích rủi ro chỉ tính Agent binding là thiếu một cửa.
- **DEC-049 (15/08/2026):** 10 Agent được share vào space `CFL Member` quyền `Được chỉnh sửa` — người khác sửa được Agent, nên mọi snapshot cấu hình có thể lệch bất cứ lúc nào; phải audit lại trước khi kết luận.
- **Bảng bản chất đã lạc hậu so với cây thư mục.** Spec 15/08 xếp `Glossary & Systems` và `CS FAQ & Policy` là "chưa có nguồn", nhưng 16/08 cả hai đã có bản nháp local (3 MD và 1 MD). KB test `Test` (DEC-051) cũng không có mục nào trong bảng. Ai tra bảng để quyết định bind sẽ thấy một bức tranh cũ hơn thực tế.
- **Bản nháp local không đồng nghĩa KB đã sẵn sàng bind.** Bốn file Markdown mới chưa qua audit nội dung, chưa có header bắt buộc theo mục 8, chưa nạp lên Web và chưa chat-test. Nguyên tắc 4 (*"KB không có pipeline dựng lại + audit thì không được bind"*) vẫn chặn.
