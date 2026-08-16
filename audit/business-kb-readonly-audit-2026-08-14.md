# Audit read-only KB nghiệp vụ ứng viên — 14/08/2026

## Phạm vi và phương pháp

Mục tiêu: audit nội dung, owner, ACL, retention, sensitivity và freshness của các KB nghiệp vụ trên VNG AI để làm tiền đề cho allowlist bind KB vào 10 custom Agent LiveOps (theo backlog `STATUS.md` và DEC-034).

Hai nguồn bằng chứng, đều read-only:

1. **MCP KB connector** — `list_knowledge_bases`, `get_knowledge_base`, `list_documents`.
2. **UI** `https://vnggames.ai/kb/knowledge` — danh sách KB, badge, dialog `Chia sẻ` và `Tổng quan`.

Kỷ luật an toàn đã áp dụng:

- Không mutation. Mọi dialog cấu hình đóng bằng **Hủy**, không bấm **Lưu**.
- Ảnh danh sách trước và sau phiên audit giống nhau: `Tất cả 9`, `Tôi tạo 8`, `Được chia sẻ 1`, count tài liệu `25/49/16/1/20/9/7/8` và badge space không đổi.
- Không đọc nội dung file credential `keys CFL ItemID/keys/*.json`.
- Không ghi giá trị định danh cá nhân (openid, roleid, nickname, số tiền nạp cụ thể) vào audit này. Chỉ ghi tên cột, số dòng và mức độ nhạy cảm.

## Phát hiện 1 — Danh mục KB thực tế là 9, tài liệu project chỉ ghi 3

`PROJECT.md`, `STATUS.md` và `HANDOFF.md` chỉ ghi 3 KB (consumer, asset host, meta-KB Agent). Web actual có 9.

| # | KB | ID | Docs | Quyền sở hữu | Có trong tài liệu project? |
|---|---|---|---:|---|---|
| 1 | `GS9 CFL Knowledge Agent` | `1d92448f-7ee2-46c4-b202-5efbe9cc5616` | 25 | Của tôi | Có |
| 2 | `GS9 Knowledge VNG - Image Assets` | `6da8657c-dd96-4170-a698-074043475014` | 49 | Của tôi | Có |
| 3 | `GS9 Knowledge VNG AI` | `cefadf09-4187-46ac-a765-591e3255a4a4` | 20 | Của tôi | Có |
| 4 | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | `574d4d12-8421-4e6f-9628-d03f4f7fb475` | 16 | Của tôi | **Không** |
| 5 | `GS9 CFL PUM` | `90484cd2-93fa-4d45-a37f-43c0d50430f2` | 7 | Của tôi | Chỉ tên folder, không có ID |
| 6 | `GS9 CFL Data Daily` | `7be35c7c-c1fc-4538-bb1c-470f18378ae9` | 9 | Của tôi | Chỉ tên folder, không có ID |
| 7 | `GS9 CFL Item Profile` | `e99b635f-04ec-44ad-9bcc-f12cae587c7d` | 8 | Của tôi | Chỉ tên folder, không có ID |
| 8 | `GS9 CFL Sentiment Feedback User` | chưa ghi nhận | 1 | Của tôi | Chỉ tên folder, không có ID |
| 9 | `GS9 test knowledge base` | `6f887ec5-dab1-4505-999f-fb99c2280da9` | 0 | **Người khác** (shared-with-me) | **Không** |

Tồn đọng: ID của `GS9 CFL Sentiment Feedback User` chưa lấy được trong phiên này (row trên UI không điều hướng bằng click, và KB này ngoài phạm vi MCP — xem Phát hiện 6).

## Phát hiện 2 — ACL: 5 KB đang chia sẻ quyền **Chỉnh sửa** cho space `CFL Member`

Space `CFL Member` có **6 thành viên** (sidebar UI). Dialog `Chia sẻ` từng KB:

| KB | Chia sẻ tới | Quyền |
|---|---|---|
| `GS9 CFL Kho Dữ Liệu Tổng Hợp` | `CFL Member` | **Chỉnh sửa** |
| `GS9 Knowledge VNG AI` | `CFL Member` | **Chỉnh sửa** |
| `GS9 CFL Data Daily` | `CFL Member` | **Chỉnh sửa** |
| `GS9 CFL PUM` | `CFL Member` | **Chỉnh sửa** |
| `GS9 CFL Item Profile` | `CFL Member` | **Chỉnh sửa** |
| `GS9 CFL Knowledge Agent` | — | không chia sẻ |
| `GS9 Knowledge VNG - Image Assets` | — | không chia sẻ |
| `GS9 CFL Sentiment Feedback User` | — | không chia sẻ |

Chú giải UI trong dialog: *"Quyền Chỉnh sửa cho phép sửa nội dung; Chỉ đọc chỉ cho truy hồi và hỏi đáp."* Nghĩa là 5 KB trên đang cấp **quyền ghi** cho 6 người, không phải chỉ đọc.

Hệ quả cần xử lý:

- `GS9 Knowledge VNG AI` là consumer phát hành của 20 module sinh tự động. Sáu người có quyền sửa nội dung trên Web phá vỡ hợp đồng DEC-001 (chỉ sửa ở master rồi strict build). Web có thể drift khỏi master mà gate local 16 test không phát hiện, hoặc build local ghi đè im lặng thay đổi của người khác.
- `GS9 CFL Item Profile` chứa dữ liệu định danh player (Phát hiện 3) và đang mở quyền ghi cho 6 người.
- Câu `sharing 0` trong `STATUS.md`/`HANDOFF.md` chỉ đúng cho meta-KB `GS9 CFL Knowledge Agent`. Không được đọc thành "toàn bộ KB sharing 0".

Chưa xác định: danh tính 6 thành viên space và vai trò của họ. Audit này không ghi tên/email cá nhân; cần Human xác nhận danh sách có đúng least privilege.

## Phát hiện 3 — `Data Private Weapon` đã live trong `GS9 CFL Item Profile`

`DECISIONS.md` DEC-029 và `agent/liveops-custom-agent-catalog.md` (Boundary chung) ghi: **"Không dùng `Data Private Weapon`"**. `audit/cfm-private-weapon-export-2026-08-14.md` ghi: *"chưa upload JSON/CSV vào ... KB khác"*.

Web actual ngược lại. Đối chiếu byte-size và số dòng giữa audit export và KB live:

| File | Dòng (audit export) | Byte (audit export) | Local `knowledge/GS9 CFL Item Profile/` | Trên Web KB `e99b635f` |
|---|---:|---:|---|---|
| `01_weapons_usage.csv` | 1.227 | 208.065 | Có, khớp byte | Có, `file_size` khớp |
| `02_weapon_name_map.csv` | 2.599 | 103.687 | Có, khớp byte | Có, khớp |
| `03_sample_users.csv` | 4 | 282 | Có, khớp byte | Có, khớp |
| `04_sample_user_weapons.csv` | 45 | 2.754 | Có, khớp byte | Có, khớp |
| `05_issued_items_timeseries.csv` | 1.206 | 389.351 | Có, khớp byte | Có, khớp |
| `06_users_detailed.csv` | 8.148 | 5.777.654 | Có, khớp byte | Có, khớp |
| `07_users_cb.csv` | 375.591 | 18.910.137 | Có, khớp byte | Có, khớp |

Kết luận: **cùng một dataset**. 7/7 CSV của `Data Private Weapon` đã nằm trong mirror local `knowledge/GS9 CFL Item Profile/` và đã upload live, `parse_status` `completed`, đã sinh embedding, summary và bật `Sinh câu hỏi`.

Trường định danh/hành vi đang được index (đọc header, không đọc giá trị):

- `03_sample_users.csv`: `roleid`, `openid`, `nickname`, `membership_tier`, `cumulative_topup_thousand_vnd`, `ladder`, `matches`
- `04_sample_user_weapons.csv`: `openid`, `roleid`, `nickname`, `weapon_id`, `total`, `T1`–`T7`
- `06_users_detailed.csv`: `openid`, `roleid`, `nickname`, `membership_tier`, `cumulative_topup_thousand_vnd`, `tier_history`, `max_single_topup_vnd`, `transaction_count`, `last_topup_date`, `ladder`, `matches`, `weapon_summary`
- `07_users_cb.csv`: `openid`, `roleid`, `nickname`, `cumulative_topup_thousand_vnd`, `tier_history`, `matches`

Khối lượng bản ghi cấp player: 375.591 + 8.148 + 45 + 4 = **383.788 dòng**.

Vấn đề nghiêm trọng hơn việc upload: **PII đã lan sang metadata KB.** Trường `description`/summary do hệ thống tự sinh cho `06_users_detailed.csv` và `07_users_cb.csv` đã trích dẫn nickname thật và giá trị nạp cụ thể của người chơi. Metadata này không phải chunk nội dung — nó xuất hiện trong danh sách tài liệu và trong khối `Nguồn tham khảo` của bất kỳ Agent nào bind KB này. Audit này không sao chép các giá trị đó.

Trạng thái: **mâu thuẫn trực tiếp giữa DECISIONS/catalog và Web actual.** Cần Human quyết định phương án (siết quyền và giữ nguyên / tách KB item-level và player-level / xóa dữ liệu player). Không tự xóa, không tự bỏ share trong phiên audit này.

## Phát hiện 4 — Retention: không có control ở cấp KB

Dialog `Cấu hình Knowledge Base → Tổng quan` chỉ có: `Loại` (Tài liệu / FAQ), `Chiến lược lập chỉ mục` (`RAG (vector + từ khóa)` và `Wiki`, cả hai bị khóa khi KB đã có nội dung), `Tên`, `Mô tả`. Không có TTL, expiry, retention hay auto-purge.

Kết luận: retention là **Bị chặn–Chưa xác định** ở cấp policy. Dữ liệu tồn tại vô hạn tới khi xóa thủ công. Không thể đáp ứng yêu cầu retention bằng cấu hình; phải xử lý bằng quy ước vận hành có ngày và rà soát định kỳ.

## Phát hiện 5 — Freshness và toàn vẹn

- **Data Daily lệch mirror:** Web có 9 tài liệu, local mirror có 8. Web có thêm `CFL_082026.xlsx` (dữ liệu 01–09/08/2026) mà local không có. Local đang lệch sau Web.
- **Item Profile có nguồn sync ngoài:** `CFL ItemID.xlsx` vào KB qua `channel: google_drive` với `datasource_id` và `web_view_link` Google Sheets, `source_modified_at` 10/08/2026. Nội dung có thể đổi dưới chân Agent mà không qua build/audit nào. Local còn `cfm-sung-theo-thoi-gian.raw.json` (25.953.259 byte) chưa upload.
- **Trùng lặp có chủ đích:** `GS9 CFL Kho Dữ Liệu Tổng Hợp` (16 docs) = 8 xlsx Data Daily + 7 pdf PUM + 1 `CFL ItemID.xlsx`. Nếu bind cả KB tổng hợp và KB lẻ cho cùng một Agent sẽ có double-retrieval và khả năng dẫn hai nguồn cùng nội dung nhưng khác `updated_at`. KB tổng hợp **không** chứa 7 CSV player → sạch PII cấp player.
- **Dấu vết lỗi pipeline parse còn lưu:** `01_weapons_usage.csv` có `error_message` `"Task interrupted due to application restart"`; `CFL_082026.xlsx` có `"task stuck > 2h10m0s with no queued task, recovered by housekeeping"`. Cả hai vẫn `parse_status: completed`, nhưng độ đầy đủ chunk là **Có điều kiện** cho tới khi chat-test xác nhận.
- **Khác embedding model:** Item Profile dùng `3b3d08c9-9c57-49fe-a639-9ca73846fa10`; Data Daily, PUM và Kho tổng hợp dùng `56b60566-a978-49da-9372-588ad12dc5d6`. Cần lưu ý khi so sánh chất lượng retrieval giữa các KB.
- **Tag:** chỉ KB tổng hợp có tag (`PUM`, `Data`, `Source Item Ingame`). Bốn KB nghiệp vụ còn lại `tags: null` → không lọc được theo tag khi bind.

## Phát hiện 6 — Phạm vi MCP connector trùng khớp space `CFL Member`

MCP `list_knowledge_bases` trả về đúng 6 KB: 5 KB đã share cho `CFL Member` cộng `GS9 test knowledge base` (KB được share tới tôi từ space đó). Ba KB không share (`GS9 CFL Knowledge Agent`, `GS9 Knowledge VNG - Image Assets`, `GS9 CFL Sentiment Feedback User`) trả về `not found or not accessible` khi gọi trực tiếp bằng ID.

Kết luận: visibility của MCP connector = tập KB đã share vào space. Hệ quả cần tính vào bài toán quyền: **share một KB vào `CFL Member` đồng thời mở KB đó cho MCP connector**, tức là một đường truy cập dữ liệu song song với việc bind KB vào Agent. Trong phiên này MCP đã đọc được metadata PII của `GS9 CFL Item Profile` chỉ bằng quyền sẵn có.

## Phát hiện 7 — Phân loại sensitivity

| Mức | KB | Cơ sở |
|---|---|---|
| **P0 — định danh + tài chính cá nhân** | `GS9 CFL Item Profile` | 383.788 dòng cấp player với `openid`/`roleid`/`nickname`/lịch sử nạp/giao dịch; PII đã lan vào summary |
| **P1 — nội bộ mật, kinh doanh** | `GS9 CFL PUM` | MMR: revenue thực vs KPI, budget marketing, root cause sự cố, roadmap version chưa công bố, kết quả survey |
| **P1** | `GS9 CFL Data Daily` | DAU/NRU/revenue/CPI/CPN/LTV/ROAS/marketing cost theo ngày |
| **P1** | `GS9 CFL Kho Dữ Liệu Tổng Hợp` | Hợp của Data Daily + PUM + item catalog |
| **P2 — UGC free-text** | `GS9 CFL Sentiment Feedback User` | 1 xlsx, 85.365 dòng, cột `Source`, `Post Published Date`, `Post Message`, `Created Date`, `Comment Message`, `Topic`, `Feature`, `Sentiment`, `Emotion`, `Urgency`, `Like`, `Score`. Không có cột user ID — điểm cộng — nhưng free-text do người chơi viết có thể tự chứa PII |
| **P3 — tài liệu nội bộ vô hại** | `GS9 Knowledge VNG AI` | Sổ tay hướng dẫn nền tảng |
| **P3** | `GS9 CFL Knowledge Agent` | Meta-KB Human-facing về 16 Agent |
| **Ngoài phạm vi corpus** | `GS9 Knowledge VNG - Image Assets` | Asset host, DEC-024 |
| **Trống** | `GS9 test knowledge base` | 0 tài liệu; ứng viên KB test theo DEC-017 nhưng **không thuộc sở hữu của tôi** |

## Phân loại bằng chứng

- **Đã kiểm chứng:** danh mục 9 KB và ID (trừ Sentiment), count tài liệu, owner, quyền share từng KB, số thành viên space, badge Đa phương thức / Sinh câu hỏi, schema cột của dữ liệu local, số dòng, khớp byte giữa audit export và KB live, `parse_status`, `error_message`, `channel`, embedding model, tag, việc thiếu control retention.
- **Có điều kiện:** độ đầy đủ chunk của hai tài liệu từng lỗi pipeline; chất lượng retrieval của từng KB; mức độ PII thực tế trong free-text của KB Sentiment (chưa quét toàn bộ 85.365 dòng).
- **Bị chặn–Chưa xác định:** ID KB Sentiment; danh tính và vai trò 6 thành viên space `CFL Member`; owner thực của `GS9 test knowledge base`; policy retention ở cấp tenant; liệu 20 module trên Web còn khớp master hay đã bị sửa bởi thành viên có quyền Chỉnh sửa.

## Gate bắt buộc trước khi bind bất kỳ KB nào

| Mã | Việc | Cần Human approval |
|---|---|---|
| G1 | Hạ quyền share 5 KB từ `Chỉnh sửa` xuống `Chỉ đọc`; riêng `GS9 CFL Item Profile` xem xét bỏ share | Có |
| G2 | Quyết định phương án cho dữ liệu player trong `GS9 CFL Item Profile`, gồm cả xử lý PII đã lan vào description/summary (cần re-index sau khi loại cột định danh) | Có |
| G3 | Bổ sung 6 KB còn thiếu vào `PROJECT.md`/`STATUS.md` kèm ID và vai trò | Không |
| G4 | Đồng bộ mirror local Data Daily (thiếu `CFL_082026.xlsx`) | Không |
| G5 | Kiểm chứng 20 module trên Web còn khớp master, sau khi có G1 | Không |
| G6 | Chat-test grounding trên KB đã bind, xác nhận `Nguồn tham khảo` không lộ PII | Có |

## Đề xuất allowlist

Xem `agent/kb-allowlist-proposal-2026-08-14.md`.

## Bằng chứng liên quan

- `audit/cfm-private-weapon-export-2026-08-14.md` — export gốc của dataset player
- `audit/liveops-custom-agent-creation-2026-08-14.md` — trạng thái 10 Agent no-KB
- `agent/liveops-custom-agent-catalog.md` — boundary và ma trận tool hiện tại
- `DECISIONS.md` DEC-024, DEC-029, DEC-034
