# Đề xuất allowlist KB cho 10 custom Agent LiveOps — 14/08/2026

**Trạng thái:** Đề xuất, **chưa thực hiện**. Cả 10 Agent hiện vẫn `Không dùng kho tri thức`, sharing `0`, không có tool phụ thuộc nguồn nào active.
**Bằng chứng nền:** `audit/business-kb-readonly-audit-2026-08-14.md`
**Yêu cầu:** Mọi mục trong tài liệu này cần Human approval trước khi áp dụng. Không tự bind.

## Cập nhật cùng ngày — bổ sung KB `GS9 CFL Plan Version`

Sau khi viết bản đầu, KB Web `GS9 CFL Plan Version` (`1452bc9a-c8b4-487b-b623-34e0b00a83e9`) được xác nhận tồn tại, cấu hình đúng (`Loại: Tài liệu`, RAG+Wiki, parser ảnh `MinerU`) nhưng **còn 0 tài liệu** — bundle 12 Markdown + 29 ảnh đang chờ upload (`audit/cfl-plan-v5-web-upload-attempt-2026-08-14.md`). KB này đổi lựa chọn tốt nhất cho ba Agent dưới đây vì nó là nguồn kế hoạch phiên bản kế tiếp thật, không phải chỉ tài liệu nền tảng. Khuyến nghị được đánh dấu **có điều kiện: chỉ hiệu lực sau khi 12 Markdown lên KB và chat-test grounding đạt** — chưa được tính vào Phase 1 vì nội dung chưa live.

### Điều kiện bind cứng cho `GS9 CFL Plan Version`

Bundle này khác mọi KB khác trong project ở hai điểm, nên có điều kiện riêng, áp dụng cho **bất kỳ** Agent nào được bind vào nó:

**C1 — Tài liệu nội bộ.** Footer nguồn ghi nguyên văn: "Tài liệu nội bộ, vui lòng không phổ biến ra ngoài", đối tượng là "Đồng nghiệp phát hành / marketing của nhóm dự án · Đội phát hành bản địa bên ngoài". Hệ quả: KB không được share ra space rộng; Agent không được trích nguyên văn vào nội dung hướng ra người chơi; mọi output dùng nguồn này phải gắn nhãn nội bộ và đi qua Human approval.

**C2 — Kế hoạch chưa chốt, không phải sự thật đã phát hành.** Bundle giữ nguyên các điểm bất toàn của nguồn: FIG-00 chưa có sơ đồ lịch trình chi tiết; FIG-11 và FIG-12 chưa có ảnh; một hạng mục có mô tả DOM rỗng (`Đạo cụ lên kệ trên cửa hàng web`); section thương mại hóa mở đầu ghi 47 nội dung nhưng DOM có 46 item; ba cặp mô tả trùng dưới title khác nhau. Agent tuyệt đối không được trình bày các mục này như đã xác nhận lên sóng, và phải nêu rõ khi một hạng mục còn chờ chốt.

**Xung đột phát hiện được với `GS9 Player Communications`.** System Prompt hiện tại của Agent này yêu cầu *"Use only approved event briefs, schedules, claims, brand rules, channel limits and glossary"*. Plan V5 **không phải approved brief** — nó là tài liệu kế hoạch nội bộ. Bind thẳng mà không sửa prompt sẽ khiến Agent coi kế hoạch chưa duyệt như nguồn hợp lệ để soạn nội dung ra-người-chơi. Trước khi bind, chèn guardrail sau vào System Prompt (đề xuất, cần Human duyệt câu chữ):

```text
The Plan Version knowledge base is an INTERNAL planning document, not an approved brief. Never quote it verbatim in player-facing copy. Never treat a planned item as confirmed for release. If an item is marked pending, placeholder, or lacks a confirmed date, state that it is unconfirmed and stop; request an approved brief instead.
```

Với `GS9 LiveOps Planner` và `GS9 Release Reviewer`, rủi ro thấp hơn vì output của hai vai trò này hướng nội bộ, không ra người chơi — nhưng C1 và C2 vẫn áp dụng nguyên vẹn.

## Nguyên tắc đề xuất

1. **Không bind `GS9 CFL Item Profile` ở trạng thái hiện tại.** KB này là P0: 383.788 dòng cấp player có `openid`/`roleid`/`nickname`/lịch sử nạp, đang share quyền `Chỉnh sửa` cho 6 người, và PII đã lan vào description/summary nên sẽ hiện trong `Nguồn tham khảo` của Agent.
2. **Chọn KB tổng hợp hoặc KB lẻ, không cả hai** cho cùng một Agent, để tránh double-retrieval và hai nguồn cùng nội dung khác `updated_at`.
3. **Không dùng `Tất cả kho tri thức`** (boundary hiện hành).
4. **Tool nguồn tối thiểu theo mức sensitivity:**
   - P1/P2: `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa`. Không bật `Đọc tài liệu nguồn`.
   - P3: thêm `Thông tin tài liệu` và `Đọc tài liệu nguồn` được phép.
   - `Liệt kê đoạn` chỉ bật khi debug grounding, tắt lại sau.
   - `Tìm Wiki` / `Đọc trang Wiki`: chỉ sau khi kiểm chứng Wiki index thực có nội dung (chiến lược Wiki đang bật nhưng chưa test).
   - `Lược đồ dữ liệu` / `Phân tích dữ liệu` / `Truy vấn CSDL` / `Danh mục sản phẩm`: giữ **Off** cho cả 10 Agent trong Phase 1.
5. **Giữ nguyên gate hành động:** không Agent nào được bật tool gửi tin, publish, sửa config, rollback, grant item, compensation, sanction, account mutation hay database write.

## Điều kiện tiên quyết

Phase 1 chỉ bắt đầu sau khi **G1** và **G3** trong audit hoàn tất:

- **G1** — hạ quyền share 5 KB từ `Chỉnh sửa` xuống `Chỉ đọc`. Lý do: `Chỉ đọc` đủ cho retrieval và hỏi đáp; `Chỉnh sửa` cho 6 người là quyền ghi không cần thiết, và với `GS9 Knowledge VNG AI` nó phá vỡ hợp đồng "chỉ sửa ở master rồi strict build" (DEC-001).
- **G3** — ghi 6 KB còn thiếu vào `PROJECT.md`/`STATUS.md` kèm ID.

**G2** (phương án dữ liệu player) là điều kiện riêng cho `GS9 Economy Offer Analyst`.

## Bảng allowlist đề xuất — Phase 1

| Agent | KB đề xuất | Mức | Tool nguồn bật | Ghi chú |
|---|---|---|---|---|
| `GS9 LiveOps Planner` | `GS9 Knowledge VNG AI`; **+ `GS9 CFL Plan Version` khi live (có điều kiện)** | P3 | semantic + keyword + doc info | Plan Version là nguồn lịch trình/nội dung phiên bản kế tiếp thật — khớp trực tiếp vai trò lập event brief/calendar hơn bất kỳ KB nào khác đang có. Chưa bind được vì KB còn 0 tài liệu. Phase 1 tạm chỉ có nền tảng platform |
| `GS9 Release Reviewer` | `GS9 Knowledge VNG AI`; **+ `GS9 CFL Plan Version` khi live (có điều kiện)** | P3 | semantic + keyword | Plan Version cho biết nội dung/hệ thống mới sắp phát hành — hữu ích để review trước khi ra mắt. Vẫn chưa có config dictionary hay change ticket dạng KB |
| `GS9 Incident Triage` | `GS9 CFL PUM` | P1 | semantic + keyword | PUM có root cause thật (bug V4.0, ping, FPS, verify SĐT), mitigation và timeline theo tháng — đúng nhu cầu triage. Không có runbook/monitoring snapshot |
| `GS9 KPI Experiment Analyst` | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | P1 | semantic + keyword + doc info | Chọn KB tổng hợp thay vì bind cả Data Daily + PUM, theo nguyên tắc 2. Chỉ số liệu tổng hợp, không có player-level |
| `GS9 Economy Offer Analyst` | **Hoãn.** Đề xuất tạo KB mới `GS9 CFL Item Catalog` | P1 | semantic + keyword | Xem mục "Phương án tách Item Profile" bên dưới. Không bind `GS9 CFL Item Profile` |
| `GS9 Player Voice Analyst` | `GS9 CFL Sentiment Feedback User` | P2 | semantic + keyword | Cần quét PII trong free-text trước (85.365 dòng `Comment Message`). Cấm trả lời nguyên văn comment; chỉ tổng hợp theo `Topic`/`Sentiment`/`Emotion` |
| `GS9 CS Copilot` | **Chưa bind** | — | — | Không có KB FAQ/CS policy/known issue nào tồn tại. Cần soạn KB mới; đây là gap nội dung, không phải gap quyền. Lưu ý mode `Trả lời nhanh` không có tab Tools |
| `GS9 GM Case Investigator` | **Không bind** | — | — | Vai trò cần case-scoped view theo từng vụ. Không tồn tại nguồn như vậy; bind KB toàn tenant sẽ vượt phạm vi least privilege |
| `GS9 Player Communications` | **`GS9 CFL Plan Version` (khi live) là nguồn chính thay cho PUM**; PUM chỉ còn phụ | P1 | semantic + keyword + doc info | Đổi so với bản đầu: Plan Version chứa nguyên văn nội dung/hình ảnh phiên bản sắp phát hành — đúng việc soạn patch note/notice hơn PUM (PUM là báo cáo kết quả tháng trước, không phải nội dung sắp ra). Cần `Thông tin tài liệu` để trích đúng tên hệ thống/mốc thời gian. Vẫn thiếu brand guideline/glossary/approved claims — nêu rõ hạn chế trong System Prompt. Bundle ghi "tài liệu nội bộ, không phổ biến ra ngoài" — cấm trích nguyên văn ra ngoài phạm vi nội bộ |
| `GS9 Knowledge Curator` | `GS9 Knowledge VNG AI` + `GS9 CFL Knowledge Agent` | P3 | semantic + keyword + doc info | Hai KB P3, không xung đột nội dung. Cần cân nhắc: meta-KB Agent hiện không share space, bind vào Agent là lần đầu KB này ra khỏi phạm vi Human-only |

Tổng kết Phase 1 (chỉ tính KB đã live): **7 Agent được bind**, 1 hoãn (`Economy Offer Analyst`), 2 không bind (`CS Copilot`, `GM Case Investigator`). Ba Agent (Planner, Release Reviewer, Player Communications) có khuyến nghị bổ sung/thay đổi gắn với `GS9 CFL Plan Version`, hiệu lực sau khi KB đó có nội dung và qua chat-test — xem mục cập nhật ở đầu file.

## Phương án tách `GS9 CFL Item Profile` (cần approval — G2)

8 tài liệu hiện tại chia làm hai nhóm rạch ròi:

**Nhóm item-level — không có PII, bind được:**

- `01_weapons_usage.csv` — cột `id`, `name`, `pham`, `fam`, `loai`, `tot`, ma trận `M_T1..M_T7` theo nhóm
- `02_weapon_name_map.csv` — `id`, `display_name`
- `05_issued_items_timeseries.csv` — `id`, `name`, phân loại, `tot`, chuỗi theo tháng/tuần
- `CFL ItemID.xlsx` — catalog ItemID, tên VI/CN, group, type, quality, version, giá Xu CF và VND

**Nhóm player-level — P0, không bind:**

- `03_sample_users.csv` (4 dòng), `04_sample_user_weapons.csv` (45 dòng), `06_users_detailed.csv` (8.148 dòng), `07_users_cb.csv` (375.591 dòng)

Đề xuất:

1. Tạo KB mới `GS9 CFL Item Catalog`, chỉ nạp nhóm item-level, không share space hoặc share `Chỉ đọc`, rồi bind cho `GS9 Economy Offer Analyst`.
2. Giữ `GS9 CFL Item Profile` làm KB private cho nhóm player-level: **bỏ share space**, không bind cho bất kỳ Agent nào.
3. Xử lý PII đã lan vào description/summary của `06_users_detailed.csv` và `07_users_cb.csv`. Chỉ đổi quyền là không đủ — summary đã sinh vẫn còn nickname và giá trị nạp. Cần xóa và nạp lại phiên bản đã loại `nickname` (và cân nhắc hash `openid`/`roleid`) rồi re-index.
4. Lưu ý `CFL ItemID.xlsx` đang sync từ Google Drive: nếu dùng cho Agent, phải ghi nhận datasource và tần suất sync vào audit, vì nội dung đổi được mà không qua build nào.

Cảnh báo phụ: `CFL ItemID.xlsx` hiện tồn tại ở **hai** KB (`GS9 CFL Item Profile` và `GS9 CFL Kho Dữ Liệu Tổng Hợp`) với hai `datasource_id` khác nhau nhưng cùng `external_id` Google Sheets. Nếu bind cả `Item Catalog` mới và KB tổng hợp cho hai Agent khác nhau thì chấp nhận được; bind cho cùng một Agent thì vi phạm nguyên tắc 2.

## Phase 2 — chỉ khi có nguồn mới

| Agent | Nguồn còn thiếu | Việc cần làm |
|---|---|---|
| `GS9 CS Copilot` | FAQ, CS policy, known issue, script escalation | Soạn KB mới; cân nhắc `Loại: FAQ` thay vì `Tài liệu` |
| `GS9 GM Case Investigator` | Case-scoped view, policy xử phạt | Thiết kế cơ chế nạp bằng chứng theo từng case; không dùng KB toàn tenant |
| `GS9 LiveOps Planner` | Event spec, calendar, runbook, approval map | Chuẩn hóa từ tài liệu vận hành hiện có |
| `GS9 Release Reviewer` | Config dictionary, change ticket | Cần nguồn từ team kỹ thuật |
| `GS9 Player Communications` | Brand guideline, glossary, approved claims | Cần nguồn từ team marketing/legal |
| `GS9 Incident Triage` | Runbook, monitoring snapshot | Bổ sung sau PUM |

## Thứ tự thực hiện đề xuất

1. Human duyệt G1 → hạ quyền share 5 KB xuống `Chỉ đọc`.
2. G3 + G4 → cập nhật tài liệu project và đồng bộ mirror Data Daily.
3. G5 → đối chiếu 20 module Web với master sau khi quyền đã siết.
4. Bind Phase 1 cho **một** Agent trước (đề xuất `GS9 Incident Triage` với PUM: P1, một KB, nội dung rõ ràng, dễ đánh giá grounding).
5. G6 → chat-test Agent đó, xác nhận `Nguồn tham khảo` đúng và không lộ PII.
6. Nếu đạt, bind 6 Agent còn lại của Phase 1, mỗi Agent một audit có ngày.
7. G2 → quyết định phương án Item Profile, rồi mới xử lý `Economy Offer Analyst`.

Sau mỗi bước bind, cập nhật đồng thời `agent/`, meta-KB `GS9 CFL Knowledge Agent` và audit theo DEC-034. Không trình bày planned claim như Web actual.
