# Bản đồ KB đích cho nghiệp vụ LiveOps CFL — thiết kế 15/08/2026

**Trạng thái:** Thiết kế, **chưa thực hiện**. Không mục nào trong tài liệu này được áp dụng lên Web nếu chưa có phê duyệt riêng.
**Bằng chứng nền:** `audit/business-kb-readonly-audit-2026-08-14.md`, `audit/agent-kb-binding-and-vi-descriptions-2026-08-14.md`, `audit/cfl-plan-v5-minio-uri-harvest-2026-08-15.md`
**Thay thế:** `agent/kb-allowlist-proposal-2026-08-14.md` (bản đó bind theo KB sẵn có; bản này bind theo bản đồ đích)

---

## 1. Vì sao cần bản đồ này

Dự án đã tạo 10 Agent live trước khi có bản đồ KB. Hệ quả đo được:

- 4/10 Agent không có nguồn nào phù hợp tồn tại → không phải lỗi bind, là lỗi quy hoạch.
- 2 Agent (`LiveOps Planner`, `Release Reviewer`) đang bind `GS9 Knowledge VNG AI` — đó là **sổ tay hướng dẫn dùng nền tảng VNG AI**, không phải tri thức về game. Bind vì đó là KB duy nhất sẵn có ở mức P3, không phải vì đúng việc. Đây là lỗi phân loại.
- `GS9 CFL Item Profile` trộn dữ liệu item-level (vô hại) với player-level (PII) trong cùng một kho → cả KB thành P0 → `Economy Offer Analyst` mất nguồn dù dữ liệu nó cần vẫn nằm đó.

Cả ba đều là triệu chứng của một nguyên nhân: **KB được vẽ theo nguồn dữ liệu, không theo mục đích tiêu thụ.**

---

## 2. Ràng buộc nền tảng (đã kiểm chứng, chi phối mọi quyết định)

| Ràng buộc | Hệ quả thiết kế |
|---|---|
| Share chỉ có ở **cấp KB**, không có cấp tài liệu | KB = **đơn vị phân quyền**. Trộn hai mức nhạy cảm trong một KB là mất quyền kiểm soát vĩnh viễn |
| Agent bind **cả KB**, không bind được một phần | KB = **đơn vị phạm vi truy hồi** |
| Không có TTL/expiry/auto-purge ở cấp KB | KB = **đơn vị vòng đời**; hết hạn phải xử lý bằng quy ước, không có cơ chế |
| `Chiến lược lập chỉ mục` **bị khoá sau khi KB có nội dung** | Phải chọn RAG / RAG+Wiki / Graph **ngay lúc tạo**. Sai là phải tạo KB mới và nạp lại |
| KB có `Loại`: `Tài liệu` hoặc `FAQ` | Chọn sai loại không sửa được sau |
| Có **nhãn (tag) ở cấp tài liệu** — endpoint `/tags`, bộ lọc `Danh mục tài liệu` trong UI | Đây là cơ chế duy nhất để phân biệt lát cắt bên trong một KB |
| Share KB vào space đồng thời mở KB đó cho **MCP connector** | Một đường truy cập song song với Agent binding, phải tính vào mô hình rủi ro |
| Mode `Trả lời nhanh` **không có tab Công cụ** | Agent mode này vẫn RAG được nhưng không cấu hình được tool truy hồi |
| Tool truy hồi bị khoá khi Agent chưa bind KB | Luôn bind KB trước, bật tool sau |

---

## 3. Bảy nguyên tắc quy hoạch

1. **Một KB = một (mức nhạy cảm × đối tượng đọc × nhịp cập nhật).** Không trộn ba trục này.
2. **Một tài liệu chỉ có đúng một KB là nguồn chuẩn.** Bản sao trong KB tổng hợp được phép nhưng phải khai báo là **dẫn xuất**, và **không Agent nào được bind đồng thời KB tổng hợp lẫn KB lẻ cấu thành nó** — đó mới là chỗ gây double-retrieval và hai `updated_at` mâu thuẫn.
3. **Không đổi tên KB đang chạy.** Quyết định của người dùng 15/08/2026: giữ nguyên mọi tên hiện có để không phá vỡ tham chiếu, thói quen và tài liệu cũ. Thay vào đó **mỗi KB phải có một dòng "bản chất"** ghi rõ nó là gì trong luồng — xem mục 5.1. Tên mới chỉ áp cho KB tạo mới.
4. **KB không có pipeline dựng lại + audit thì không được bind cho Agent.**
5. **Không dùng `Tất cả kho tri thức`** cho bất kỳ Agent nào.
6. **Dữ liệu định danh người chơi không bao giờ nằm trong KB được bind.** Không có ngoại lệ, không có "chỉ đọc là đủ".
7. **KB hướng-người-chơi và KB nội bộ không bao giờ chung một Agent** trừ khi System Prompt có guardrail đã duyệt.

---

## 4. Bốn trục phân loại

**Mức nhạy cảm**

| Mức | Định nghĩa | Ví dụ | Được bind? |
|---|---|---|---|
| **P0** | Định danh/hành vi người chơi | `openid`, `roleid`, `nickname`, lịch sử nạp | ❌ Không bao giờ |
| **P1** | Nội bộ mật | Doanh thu, ngân sách UA, kế hoạch chưa công bố | ⚠️ Chỉ Agent hướng nội bộ |
| **P2** | Nội bộ thường | Chỉ số tổng hợp, feedback đã ẩn danh | ✅ Có điều kiện |
| **P3** | Nội bộ phổ biến | Sổ tay nền tảng, tài liệu đã phát hành | ✅ Tự do |

**Đối tượng output:** `Human-only` · `Agent-nội-bộ` · `Agent-hướng-người-chơi`

**Nhịp cập nhật:** `static` · `versioned` · `periodic (D/W/M)` · `streaming` · `case-scoped`

**Vòng đời:** `permanent` · `rolling N tháng` · `theo phiên bản` · `theo vụ việc`

---

## 5. Bản đồ KB đích — 7 tầng

### 5.1 Bảng bản chất — tên giữ nguyên, ghi rõ nó là gì trong luồng

Đây là bảng tra cứu chính khi cần biết một KB đóng vai gì. **Không đổi tên KB**; cột "Bản chất" là thứ thay cho việc đổi tên.

| Tên đang chạy (giữ nguyên) | Tầng | Bản chất trong luồng | Vai trò dữ liệu | Ai được bind |
|---|---|---|---|---|
| `GS9 Knowledge VNG AI` | L0 | **Sổ tay dùng nền tảng VNG AI.** Không phải tri thức về game | nguồn chuẩn | chỉ `Knowledge Curator` |
| `GS9 Knowledge VNG - Image Assets` | L0 | **Kho ảnh cấp URI MinIO.** Dependency kỹ thuật, không phải corpus hỏi đáp | nguồn chuẩn | không Agent nào |
| `GS9 CFL Knowledge Agent` | L0 | **Meta-KB mô tả 16 Agent.** Dành cho người, không phải corpus nghiệp vụ | nguồn chuẩn | chỉ `Knowledge Curator` |
| `GS9 CFL Plan Version` | L2 | **Kế hoạch phiên bản sắp phát hành, nhiều phiên bản chung một kho.** Nội bộ, chưa chốt | nguồn chuẩn | Planner, Release Reviewer, Player Communications |
| `GS9 CFL PUM` | L4 | **Báo cáo kết quả theo tháng.** Nhìn về quá khứ, có doanh thu và ngân sách | nguồn chuẩn | Agent hướng nội bộ |
| `GS9 CFL Data Daily` | L4 | **Số liệu vận hành theo kỳ.** Chi tiết hơn, hạt mịn hơn PUM | nguồn chuẩn | Agent phân tích, **không chung Agent với KB tổng hợp** |
| `GS9 CFL Kho Dữ Liệu Tổng Hợp` | L4 | **Lăng kính toàn cảnh để xem Wiki.** Gom nhiều nguồn nhằm lấy góc nhìn rộng mà KB lẻ không cho được | **dẫn xuất** | `KPI Experiment Analyst` + bật tool Wiki |
| `GS9 CFL Sentiment Feedback User` | L5 | **Tiếng nói người chơi.** Free-text chưa quét PII | nguồn chuẩn | `Player Voice Analyst` sau khi quét PII |
| `GS9 CFL Item Profile` | L7 | **Kho cách ly.** Trộn item-level và player-level nên toàn bộ bị coi là P0 | nguồn chuẩn | **không ai** |
| `GS9 test knowledge base` | — | KB của người khác | — | không liên quan |

### L0 — Nền tảng & Meta (về hệ thống AI, không phải về game)

| KB | ID | Trạng thái | Mức | Nhịp | Chỉ mục |
|---|---|---|---|---|---|
| `GS9 Knowledge VNG AI` | `cefadf09-4187-46ac-a765-591e3255a4a4` | Giữ nguyên | P3 | static | RAG+Wiki |
| `GS9 Knowledge VNG - Image Assets` | `6da8657c-dd96-4170-a698-074043475014` | Giữ nguyên | P3 | static | asset host — **không bao giờ bind làm corpus hỏi đáp** |
| `GS9 CFL Knowledge Agent` | `1d92448f-7ee2-46c4-b202-5efbe9cc5616` | Giữ nguyên | P3 | static | RAG |

Tầng này **chỉ phục vụ `Knowledge Curator`**. Mọi Agent nghiệp vụ LiveOps bind vào đây là lỗi phân loại.

### L1 — Canon (sự thật về game, ổn định)

| KB | Trạng thái | Mức | Nhịp | Nguồn |
|---|---|---|---|---|
| `GS9 CFL Item Catalog` | **Tạo mới** | P1 | periodic-W | Tách từ Item Profile: `01_weapons_usage.csv`, `02_weapon_name_map.csv`, `05_issued_items_timeseries.csv`, `CFL ItemID.xlsx` |
| `GS9 CFL Glossary & Systems` | **Tạo mới** | P3 | static | Thuật ngữ chính thức VI/CN/EN, tên hệ thống, quy tắc viết. **Chưa có nguồn — cần soạn** |

`Glossary` là mắt xích thiếu quan trọng nhất cho `Player Communications` và `CS Copilot`: không có nó thì Agent tự chế tên hệ thống.

### L2 — Kế hoạch (hướng tương lai, chưa phát hành)

| KB | ID | Trạng thái | Mức | Nhịp |
|---|---|---|---|---|
| `GS9 CFL Plan Version` | `1452bc9a-c8b4-487b-b623-34e0b00a83e9` | Giữ, **bắt buộc gắn nhãn phiên bản** | P1 | versioned |
| `GS9 CFL Event Calendar & Brief` | **Tạo mới** | P1 | periodic-W | Lịch sự kiện, event spec, approval map. **Chưa có nguồn** |

### L3 — Vận hành (đang chạy)

| KB | Trạng thái | Mức | Nhịp |
|---|---|---|---|
| `GS9 CFL Runbook & Known Issues` | **Tạo mới** | P2 | rolling 12 tháng | Runbook sự cố, known issue, config dictionary, change ticket. **Chưa có nguồn** |

### L4 — Kết quả (hướng quá khứ, số liệu)

| KB | ID | Trạng thái | Mức | Nhịp | Vai trò |
|---|---|---|---|---|---|
| `GS9 CFL Kho Dữ Liệu Tổng Hợp` | `574d4d12-8421-4e6f-9628-d03f4f7fb475` | Giữ — **KB toàn cảnh, Wiki-first** | P2 | periodic-M | dẫn xuất |
| `GS9 CFL PUM` | `90484cd2-93fa-4d45-a37f-43c0d50430f2` | Giữ | P2 nội bộ | periodic-M | nguồn chuẩn |
| `GS9 CFL Data Daily` | `7be35c7c-c1fc-4538-bb1c-470f18378ae9` | **Giữ dùng bình thường** | P2 | periodic-M | nguồn chuẩn |

**Đính chính 15/08/2026 — `Kho Dữ Liệu Tổng Hợp` không phải trùng lặp nhầm.** Người dùng cố ý gom lại để **xem Wiki**: một KB tổng cho ra góc nhìn rộng mà từng KB lẻ không cho được, vì Wiki/Graph được sinh trên phạm vi toàn KB nên phạm vi khác thì kết quả khác. Đây là **lăng kính thứ hai có chủ đích**, không phải lỗi.

Hệ quả thiết kế:

- KB này là **dẫn xuất**, không phải nguồn chuẩn. Khi KB lẻ đổi, phải dựng lại KB tổng, nếu không `updated_at` sẽ lệch.
- **Bật nhóm tool Wiki** (`Tìm wiki`, `Đọc trang wiki`) cho Agent bind KB này — đó chính là lý do nó tồn tại. Đây là ngoại lệ có cơ sở với quy tắc "giữ Wiki Off".
- **Không Agent nào bind đồng thời KB tổng và KB lẻ cấu thành nó** (nguyên tắc 2).

**`Data Daily` giữ nguyên cách dùng hiện tại** — đính chính so với bản đầu. Không có bằng chứng nào cho thấy nó trùng nội dung `Kho Dữ Liệu Tổng Hợp`; trùng lặp đã kiểm chứng chỉ là `CFL ItemID.xlsx` giữa `Item Profile` và `Kho Dữ Liệu Tổng Hợp`. Đề xuất "hạ xuống staging" ở bản đầu là suy diễn quá tay, đã rút.

**PUM:** người dùng quyết định cả team được đọc doanh thu → hạ từ P1 xuống **P2 nội bộ**. Nhưng ràng buộc *"không để số liệu doanh thu lọt vào nội dung gửi người chơi"* **vẫn giữ nguyên** — đó là rủi ro đầu ra, không phải rủi ro phân quyền.

### L5 — Tiếng nói người chơi

| KB | ID | Trạng thái | Mức | Nhịp |
|---|---|---|---|---|
| `GS9 CFL Sentiment Feedback User` | *chưa lấy được ID* | **Giữ nguyên tên** (quyết định 15/08) | P2 | periodic-M |

**Điều kiện bind:** quét PII trong 85.365 dòng `Comment Message` trước. Cấm trả nguyên văn comment; chỉ tổng hợp theo `Topic`/`Sentiment`/`Emotion`.

### L6 — Dịch vụ người chơi

| KB | Trạng thái | Loại | Mức | Nhịp |
|---|---|---|---|---|
| `GS9 CFL CS FAQ & Policy` | **Tạo mới** | **`FAQ`**, không phải `Tài liệu` | P3 | rolling |
| `GS9 CFL GM Policy & Sanction` | **Tạo mới** | `Tài liệu` | P2 | static |

Chọn `Loại: FAQ` cho CS là quyết định không đảo ngược được — phải chốt lúc tạo.

### L7 — Cách ly (không bao giờ bind)

| KB | ID | Hành động |
|---|---|---|
| `GS9 CFL Item Profile` | `e99b635f-04ec-44ad-9bcc-f12cae587c7d` | **Bỏ share space**, giữ 4 file player-level, re-index để xoá PII khỏi description/summary, không bind |
| `GS9 test knowledge base` | `6f887ec5-dab1-4505-999f-fb99c2280da9` | Người khác sở hữu — bỏ qua |

---

## 6. Ánh xạ hiện trạng → đích

| Hành động | KB | Việc cụ thể |
|---|---|---|
| Giữ nguyên | Knowledge VNG AI, Image Assets, CFL Knowledge Agent, Kho Dữ Liệu Tổng Hợp, PUM | Chỉ siết ACL (G1) |
| Giữ tên, ghi bản chất | `Sentiment Feedback User` | Không đổi tên; ghi bản chất ở mục 5.1. Vẫn cần lấy ID còn thiếu |
| Giữ nguyên | `Data Daily` | Dùng bình thường; chỉ cấm bind chung Agent với KB tổng hợp |
| Tách | `Item Profile` → `Item Catalog` (mới) + phần P0 cách ly | G2, cần approval |
| Gắn nhãn | `Plan Version` | Bắt buộc `ver:v5` cho 41 tài liệu |
| Tạo mới | Glossary, Event Calendar & Brief, Runbook & Known Issues, CS FAQ, GM Policy | 5 KB — **đều chưa có nguồn** |
| Cách ly | `Item Profile` | Bỏ share, re-index |

**5/12 KB đích chưa tồn tại và chưa có nguồn.** Đây là công việc nội dung, không phải công việc cấu hình — và là lý do thật khiến 4 Agent bế tắc.

---

## 7. Quy ước đặt tên, nhãn, header

**Tên KB:** `GS9 CFL <Miền> [& <Miền phụ>]` — tiếng Anh cho miền, giữ prefix `GS9` bắt buộc.

**Nhãn tài liệu (bắt buộc):**

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

## 8. Chiến lược một-KB-nhiều-phiên-bản cho `Plan Version`

Bạn đã chốt: mọi phiên bản nằm chung một KB. Quyết định này **bắt buộc** kèm ba biện pháp, nếu thiếu sẽ hỏng.

### 8.1 Rủi ro trùng tên — phải xử lý TRƯỚC khi V6 lên

Bundle V5 hiện dùng tên `00-index-va-pham-vi.md` … `11-ghi-chu-va-truy-nguyen.md` và `image-01-….jpg` … `image-29-….jpg`. V6 sinh từ cùng converter sẽ ra **đúng những tên đó**. Hậu quả trong một KB dùng chung:

- 2 tài liệu cùng tên, khác nội dung → không phân biệt được trong `Nguồn tham khảo`
- Retrieval trộn V5 với V6 → Agent trả lời kế hoạch cũ cho câu hỏi về bản mới, **sai kiểu rất khó phát hiện**
- Registry ảnh trong file `10-danh-muc-hinh-anh.md` mất tính duy nhất

**Khắc phục:** đổi `convert_cfl_plan_html.py` để tiền tố mọi tên đầu ra bằng phiên bản. **Cập nhật 15/08/2026 (phiên 2, DEC-042):** quy ước đã chốt là `doc-v5-00-index-va-pham-vi.md`, `image-v5-01-….jpg` (giữ nguyên tiền tố loại tài liệu `doc-`/`image-` rồi mới chèn số phiên bản), không phải `V5-00-...`/`V5-image-01-...` như đề xuất ban đầu ở đây. Đã thực thi cục bộ cho 12 Markdown + 29 JPEG V5; script đã sửa `VERSION_TAG = "v5"` cho lần sinh sau. Với 41 tài liệu này, dùng nhãn `ver:v5` khi sync lên Web thay vì coi việc đổi tên là một lần upload/migration mới.

### 8.2 Ba biện pháp bắt buộc

1. **Nhãn `ver:` trên 100% tài liệu.** Không có nhãn = không được nạp.
2. **Header phiên bản trong nội dung** (mục 7) để chunk tự mang thông tin phiên bản.
3. **Câu bắt buộc trong System Prompt** của mọi Agent bind KB này:

```text
The Plan Version knowledge base contains MULTIPLE game versions in one store. Always state which version each fact comes from, taken from the version header in the retrieved chunk. If the user does not name a version, ask before answering. Never merge facts from two versions into one statement.
```

### 8.3 Rằng buộc kỹ thuật đã phát sinh

29 URI MinIO trong 12 file `.md` của V5 gắn cứng vào KB `1452bc9a…`. **Không được đổi KB đích cho Plan Version nữa** — dời là chết 29 link và phải chạy lại toàn bộ quy trình thu URI. Quyết định "một KB chung" vì vậy cũng là quyết định khoá.

---

## 9. Ma trận Agent × KB × tool (dẫn xuất từ bản đồ)

| Agent | KB chính | KB phụ | Tool nguồn | Trạng thái |
|---|---|---|---|---|
| `Knowledge Curator` | Knowledge VNG AI (L0) | CFL Knowledge Agent (L0) | semantic + keyword + doc info | ✅ **đang đúng** |
| `KPI Experiment Analyst` | Kho Dữ Liệu Tổng Hợp (L4) | — | semantic + keyword + doc info **+ Tìm wiki + Đọc trang wiki** | ✅ đúng KB; **bổ sung tool Wiki** |
| `Player Voice Analyst` | Sentiment Feedback User (L5) | — | semantic + keyword | ✅ đúng, chờ quét PII |
| `LiveOps Planner` | **Event Calendar & Brief (L2, mới)** | Plan Version (L2) | semantic + keyword + doc info | ⚠️ **bỏ bind Knowledge VNG AI** |
| `Release Reviewer` | **Runbook & Known Issues (L3, mới)** | Plan Version (L2) | semantic + keyword | ⚠️ **bỏ bind Knowledge VNG AI** |
| `Incident Triage` | **Runbook & Known Issues (L3, mới)** | PUM (L4) | semantic + keyword | ⚠️ PUM là giải pháp tạm |
| `Player Communications` | Plan Version (L2) | **Glossary (L1, mới)** | semantic + keyword + doc info | ❌ chờ guardrail + Glossary |
| `Economy Offer Analyst` | **Item Catalog (L1, mới)** | Kho Dữ Liệu Tổng Hợp (L4) | semantic + keyword | ❌ chờ G2 |
| `CS Copilot` | **CS FAQ & Policy (L6, mới)** | Runbook & Known Issues (L3) | RAG mặc định (mode Trả lời nhanh không có tab Công cụ) | ❌ chờ KB |
| `GM Policy Advisor` *(đổi tên 15/08)* | **GM Policy & Sanction (L6, mới)** | — | semantic + keyword | ❌ chờ KB; **tên + mô tả trên Web đã đổi 15/08**, System Prompt chưa |

**Giữ Off toàn bộ:** `Truy vấn CSDL`, `Phân tích dữ liệu`, `Lược đồ dữ liệu`, `Danh mục sản phẩm`, `Liệt kê đoạn` (chỉ bật khi debug rồi tắt).
**Nhóm Wiki:** mở khoá được sau khi kiểm chứng Wiki index có nội dung — `Plan Version` nay đã tự sinh Wiki (mục lục + 29 tóm tắt), nên điều kiện này đã đạt cho L2.

---

## 10. Đề xuất chỉnh lại mục đích Agent

### 10.1 Hai Agent đang bind sai tầng

`LiveOps Planner` và `Release Reviewer` bind `GS9 Knowledge VNG AI` = sổ tay dùng nền tảng AI. Không liên quan gì tới LiveOps game. **Đề xuất gỡ bind** khi KB L2/L3 sẵn sàng. Trong lúc chờ, giữ nguyên chứ không gỡ vội — gỡ thì Agent thành no-KB và mất luôn tool truy hồi.

### 10.2 `GM Case Investigator` → `GM Policy Advisor` — **đã duyệt 15/08/2026**

Vai trò "điều tra theo từng vụ" cần case-scoped view: bằng chứng của đúng một vụ, không phải kho toàn tenant. Nền tảng không có cơ chế đó, và **bind KB toàn tenant để điều tra một vụ là vi phạm least privilege**.

Đề xuất đổi thành **`GM Policy Advisor`**: trả lời về chính sách xử phạt, quy trình, tiền lệ — bind `GM Policy & Sanction`. Bằng chứng từng vụ nạp qua **tệp đính kèm trong hội thoại**, không qua KB.

### 10.3 `CS Copilot` — xác nhận lại mode

Mode `Trả lời nhanh` không có tab Công cụ nhưng **vẫn RAG được** (Agent mặc định `Quick Answer` chính là RAG Q&A). Nếu chỉ cần tra FAQ thì giữ mode này là đúng. Nếu cần suy luận nhiều bước thì phải đổi sang Smart — và đổi mode có thể reset cấu hình, cần kiểm chứng trước.

---

## 11. Thứ tự thực hiện có gate

| # | Việc | Gate | Phụ thuộc |
|---|---|---|---|
| 1 | Human duyệt bản đồ này | — | — |
| 2 | Siết ACL 5 KB xuống `Chỉ đọc` | G1 | Human |
| 3 | Gắn nhãn `ver:v5` cho 41 tài liệu Plan Version | — | KB xử lý xong |
| 4 | Sửa converter tiền tố `V5-` cho lần sinh sau | — | — |
| 5 | Chat-test `Incident Triage` × PUM | **G6** | #2 |
| 6 | Tách `Item Catalog`, cách ly `Item Profile` | G2 | Human |
| 7 | Soạn nội dung + tạo 5 KB còn thiếu | — | **cần nguồn từ các team** |
| 8 | Bind lại theo ma trận mục 9, mỗi Agent một audit | — | #7 |
| 9 | Gold-set eval từng Agent | — | #8 |

Bước 5 phải chạy trước mọi việc bind mở rộng — hiện **chưa có bằng chứng nào** cho thấy chuỗi bind + retrieval chạy đúng trên tenant này.

---

## 12. Quyết định của Human — 15/08/2026

| # | Câu hỏi | Quyết định | Hệ quả đã áp vào thiết kế |
|---|---|---|---|
| 1 | Nguồn cho 5 KB mới | **Chưa có, và chưa biết format** | Việc kế tiếp: soạn bộ template + tài liệu mẫu trước, rồi mới điền nội dung. Xem mục 14 |
| 2 | Ai đọc doanh thu | **Cả team đọc và sửa KB** | PUM hạ P1 → P2 nội bộ. Giữ nguyên cấm số liệu doanh thu ra nội dung người chơi. Rủi ro mới: xem 13 |
| 3 | Nhịp sự kiện | **Theo tháng** | `Event Calendar & Brief` nhịp `periodic-M`, khớp nhịp PUM |
| 4 | Hạ `Data Daily` | **Không hạ** | Đã rút đề xuất, giữ dùng bình thường |
| 5 | Đổi `GM Case Investigator` → `GM Policy Advisor` | **Đồng ý** | Đã đổi 4 file local; Web chưa đổi |
| 6 | Hai câu guardrail | **Duyệt cả hai** | Chốt nguyên văn ở mục 12.1; áp khi bind |
| 7 | `Kho Dữ Liệu Tổng Hợp` | **Là KB toàn cảnh để xem Wiki, có chủ đích** | Xếp loại dẫn xuất; **bật nhóm tool Wiki**; sửa nguyên tắc 2 |

### 12.1 Guardrail đã duyệt

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

## 13. Rủi ro của chính bản đồ này

- **Chi phí nội dung lớn hơn chi phí cấu hình.** 5 KB mới là việc soạn tài liệu, không phải việc bấm nút. Nếu không có người sở hữu nội dung thì bản đồ này nằm im.
- **Không đảo ngược được:** `Loại` KB và `Chiến lược lập chỉ mục` khoá sau khi có nội dung. Chọn sai phải tạo KB mới và nạp lại.
- **Bản đồ này chưa được kiểm chứng bằng runtime.** Mọi khuyến nghị bind vẫn là *Có điều kiện* cho tới khi G6 đạt.
- **Quyết định "cả team sửa được KB" phá hợp đồng DEC-001.** `GS9 Knowledge VNG AI` theo thiết kế chỉ được sửa ở master rồi strict build. Khi 6 người có quyền `Chỉnh sửa` trên Web, 20 module có thể bị sửa trực tiếp và lần build kế tiếp sẽ **ghi đè mất** thay đổi đó mà không cảnh báo. Đây là quyết định của người dùng, không phải lỗi — nhưng cần một biện pháp bù: **định kỳ chạy G5** (đối chiếu 20 module trên Web với master) để phát hiện lệch. Không có G5 thì không ai biết KB đã bị sửa ngoài quy trình.
- **KB tổng hợp là dẫn xuất nhưng không có pipeline dựng lại.** Hiện `Kho Dữ Liệu Tổng Hợp` được gom thủ công. Khi KB lẻ đổi mà quên dựng lại, Wiki toàn cảnh sẽ mô tả trạng thái cũ — sai theo kiểu khó phát hiện.

---

## 14. Việc kế tiếp: bộ template cho 5 KB còn thiếu

Người dùng xác nhận **chưa có nguồn và chưa có format**. Vì vậy bước đi được không phải "đi xin tài liệu" mà là **định nghĩa format trước**, rồi mới điền.

### 14.1 Hai KB bootstrap được từ dữ liệu đã có

Không phải cả 5 đều làm từ số không:

| KB | Bootstrap từ | Còn thiếu |
|---|---|---|
| `Glossary & Systems` | `02_weapon_name_map.csv` (id → display_name), `CFL ItemID.xlsx` (tên VI/CN), tên hệ thống trong Plan V5 | Quy tắc viết, thuật ngữ không phải vật phẩm |
| `Runbook & Known Issues` | PUM có root cause thật (bug V4.0, ping, FPS, verify SĐT) + `Player Voice` theo `Topic` | Quy trình xử lý, ngưỡng cảnh báo, người chịu trách nhiệm |

Ba KB còn lại (`Event Calendar & Brief`, `CS FAQ & Policy`, `GM Policy & Sanction`) phải soạn từ đầu vì là tri thức quy trình, không suy ra được từ dữ liệu.

### 14.2 Thứ tự ưu tiên theo mức gỡ bế tắc

| Ưu tiên | KB | Gỡ được | Ghi chú |
|---|---|---|---|
| 1 | `Glossary & Systems` | Chất lượng của `Player Communications` + `CS Copilot` | Bootstrap được, rẻ nhất |
| 2 | `CS FAQ & Policy` | `CS Copilot` — Agent đang trắng hoàn toàn | Phải chốt `Loại: FAQ` lúc tạo |
| 3 | `Runbook & Known Issues` | `Incident Triage` (bỏ phụ thuộc tạm vào PUM) + `Release Reviewer` | Bootstrap một phần |
| 4 | `Event Calendar & Brief` | `LiveOps Planner` | Nhịp tháng |
| 5 | `GM Policy & Sanction` | `GM Policy Advisor` | Cần GM Lead cung cấp chính sách |

### 14.3 Mỗi template gồm

1. **Cấu trúc thư mục + quy ước đặt tên file**
2. **Header bắt buộc** theo mục 7 (phiên bản, trạng thái, hiệu lực, mức, chủ sở hữu, nguồn)
3. **Khung nội dung** — các mục bắt buộc và tuỳ chọn, viết sao cho chunk hoá tốt
4. **Một tài liệu mẫu điền sẵn** bằng dữ liệu thật để làm chuẩn đối chiếu
5. **Checklist trước khi nạp** — không PII, có header, có nhãn, không link tương đối

Nguyên tắc viết chung cho mọi template: **một khái niệm một mục**, tiêu đề mang từ khoá người dùng thật sự gõ, không dùng bảng lồng nhau, không dùng đại từ trỏ ngược qua nhiều đoạn — vì chunk bị cắt sẽ mất ngữ cảnh.
