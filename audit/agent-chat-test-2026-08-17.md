# Chat-test thật 3 Agent trên KB an toàn — 17/08/2026

**Loại:** chạy hội thoại thật trên `vnggames.ai/kb/chats`, tenant `10012`
**Phạm vi:** chỉ Agent gắn KB không chứa doanh thu và không chứa dữ liệu định danh
**Công cụ:** `claude-in-chrome` (Chrome thật, session người dùng)
**Mục đích:** vừa lấy dẫn chứng cho tài liệu thuyết trình, vừa mở gate chất lượng runtime (mục 4.2 HANDOFF)

---

## 0. Phát hiện chặn đường, xử lý trước khi test được

Lượt chạy đầu tiên của `Player Communications` **thất bại**. Cây suy luận trả về:

```
Gọi Search Knowledge Base thất bại
tool not found: search_knowledge_base (available: ask_user, thinking, todo_write)
```

**Gắn KB không tự động cho Agent quyền đọc KB.** Công cụ truy hồi (`Tìm theo ngữ nghĩa`, `Tìm theo từ khóa`) là một tập cấu hình riêng, và trước đây chúng bị mờ trên UI vì Agent chưa có KB nào trong phạm vi. Sau khi bind KB (DEC-060) chúng mới bật được — nhưng **không tự bật**.

Đã bật `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa` cho 3 Agent, giữ Wiki và SQL tắt theo quy ước:

| Agent | Số tool trước | Sau |
|---|---:|---:|
| `GS9 CFL Player Communications` | 3 | 5 |
| `GS9 CFL Economy Offer Analyst` | 3 | 5 |
| `GS9 CFL GM Policy Advisor` | 2 | 4 |

`GS9 CFL CS Copilot` ở chế độ `Trả lời nhanh` **không có tab Công cụ** — truy hồi chạy ngầm, không cần bật.

**Hệ quả cho quy trình:** dựng Agent mới phải có bước kiểm "đã bật công cụ truy hồi chưa", nếu không Agent nhìn thì có KB mà thực tế không đọc được.

---

## 1. Case 1 — `Player Communications` × `GS9 CFL Plan Version`

**Câu hỏi:** "Phiên bản 5.0 có những chế độ chơi và hệ thống mới nào? Soạn nháp một thông báo in-game ngắn giới thiệu chúng cho người chơi, kèm trích nguồn tài liệu."

**Chạy:** 31 bước / 5 phút 24 giây. Truy hồi: tìm ngữ nghĩa `Tìm thấy 1 kết quả`, tìm từ khoá `phiên bản 5.0|version 5.0|v5.0|5\.0` → `Tìm thấy 25 khớp`. Nhiều vòng đọc sâu tài liệu.

**Kết quả — 3 phần:**

1. Tổng hợp tính năng: `Parkour kỹ thuật`, `Boss thế giới Varanus`, `Rút buff Zombie tối thượng`, `Hiển thị buff đơn trong trận`, `Giao diện phối súng ngoài trận`, `Chế độ Thủ Công trên bản đồ Bão Sa Mạc`. Đối chiếu tay với bundle Plan V5 local: **khớp**, không có mục bịa.
2. Bản nháp thông báo in-game.
3. Bảng `Factual-claim Checklist` map từng khẳng định sang ảnh nguồn.

**Ảnh render thật trong câu trả lời** — xác nhận URI MinIO vá theo DEC-052/DEC-057 còn sống và luật trích dẫn ảnh (DEC-056) có tác dụng.

**Điểm mạnh đáng ghi:** trong bảng đối chiếu, **2/5 khẳng định để trống ô nguồn** (`Boss thế giới Varanus`, `Rút buff Zombie tối thượng`) — Agent tự thú nhận chỗ không có bằng chứng ảnh thay vì gán bừa. Đáng chú ý là hai ảnh này **có tồn tại** trong kho (`image-v5-06`, `image-v5-07`), tức là truy hồi bỏ sót chứ không phải kho thiếu.

**PII / số liệu nhạy cảm:** không có. Kho Plan Version không chứa dữ liệu người chơi hay doanh thu.

**Phân loại:** **Đã kiểm chứng** — Agent tra đúng kho, trả nội dung khớp nguồn, trích dẫn ảnh, tự đánh dấu chỗ thiếu bằng chứng.

---

## 2. Case 2 — `Knowledge Curator` × `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI`

**Câu hỏi:** "Tôi cần tra cứu chính sách xử phạt người chơi gian lận của CFL. Trợ lý nào phù hợp, nó đang gắn kho nào, và kho đó có thực sự chứa điều khoản xử phạt không?"

**Chạy:** 7 bước. Vòng 1 tìm ngữ nghĩa → `Không có kết quả`; tìm từ khoá → 12 khớp. Agent tự nhận xét `The initial retrieval results don't directly answer the question`, đổi truy vấn, vòng 2 → 2 kết quả từ 2 tệp, từ khoá → 4 khớp.

**Làm đúng — phần quan trọng nhất:**

> "3. Kho chứa điều khoản xử phạt gian lận không? — **Kết quả tra cứu: Không tìm thấy.** Tôi đã thực hiện cả hai phương pháp…"

Không bịa ra điều khoản. Với nghiệp vụ xử phạt, đây là hành vi bắt buộc và Agent vượt qua.

**Làm sai — hai lỗi:**

1. **Sai sự thật về chính hệ thống.** Khẳng định *"Hệ thống VNGGAMES AI hiện có 6 trợ lý mặc định (không có agent chuyên biệt mang tên 'CFL' hay 'CFL Agent')"*. Sai: 10 Agent custom `GS9 CFL *` tồn tại thật và được mô tả trong `doc-02` của chính KB nó đang gắn. Đây là lỗi **truy hồi bỏ sót**, không phải lỗi nội dung kho.
2. **Nội dung lỗi thời.** Liệt kê `Knowledge VNG - Image Assets` như KB đang tồn tại — KB này đã bị gỡ khỏi Web (danh sách 17/08/2026 chỉ còn 10 KB của người dùng + 1 KB được chia sẻ).

**PII / số liệu nhạy cảm:** không có.

**Phân loại:** **Có điều kiện** — an toàn ở phần từ chối bịa, nhưng không dùng được làm nguồn tra cứu về cấu hình hệ thống cho tới khi xử lý được lỗi truy hồi.

---

## 3. Case 3 — `CS Copilot` × `GS9 Knowledge VNG AI` (chế độ Trả lời nhanh)

**Câu hỏi:** "Một kho tri thức có thể nạp những định dạng tệp nào, và có mấy cách để đưa dữ liệu vào kho?" — câu này **có** đáp án trong kho đang gắn.

**Chạy:** 3 bước: `Query Understand` → tìm trong kho `Tìm thấy 1 kết quả` → suy luận. Hiển thị panel **`Nguồn tham khảo (1 tài liệu)`** — panel này không xuất hiện ở các Agent chế độ `Suy luận thông minh`.

**Kết quả: từ chối trả lời.** Lý luận nguyên văn:

> "I need to be careful not to invent anything about knowledge base formats or ingestion methods. I must strictly follow: *If sources are missing, conflicting or stale, do not use general knowledge. Say the answer is not established and draft an escalation.*"
>
> "Chẩn đoán ngắn gọn: … Thông tin này không có trong nguồn tài liệu được phê duyệt."

System Prompt của Agent này khoá phạm vi vào **nguồn chính sách CS đã duyệt**. Kho hướng dẫn nền tảng không thuộc loại nguồn đó, nên Agent từ chối — dù nội dung câu trả lời nằm ngay trong kho.

**Quan sát phụ:** phần thân câu trả lời không render trong ~90 giây theo dõi, chỉ thấy cây suy luận. Chưa rõ là Agent chủ động không xuất nội dung hay lỗi hiển thị.

**Phân loại:** **Đã kiểm chứng** ở mặt guardrail — hành vi đúng thiết kế. Đồng thời là bằng chứng trực tiếp rằng **kho tạm sai chuyên môn không thay được kho đúng** (DEC-060).

---

## 4. Kết luận gate chất lượng

| Agent | Truy hồi chạy | Không bịa | Không lộ PII | Dùng được cho việc thật |
|---|---|---|---|---|
| `Player Communications` | Đạt | Đạt | Đạt | **Đạt** cho việc soạn nháp, vẫn cần người duyệt |
| `Knowledge Curator` | Đạt | Đạt | Đạt | **Chưa** — sai sự thật về cấu hình hệ thống |
| `CS Copilot` | Đạt | Đạt | Đạt | **Chưa** — thiếu kho chính sách CS |

Ba Agent còn lại trong nhóm rủi ro (`Incident Triage` → PUM, `Player Voice Analyst` → Sentiment, `KPI Experiment Analyst` → Kho Tổng Hợp) **chưa test** trong lượt này vì người dùng giới hạn phạm vi ở KB an toàn.

**Gate 4.2 mở một phần:** lần đầu tiên có Agent đạt chat-test theo nghĩa đầy đủ (`Player Communications`). 13/16 Agent vẫn ở mức *Bị chặn–Chưa xác định*.

---

## 5. Việc phát sinh cần xử

1. **Lỗi truy hồi của `Knowledge Curator`** — kho có nội dung nhưng Agent lấy nhầm đoạn. Cần thử tăng Top K hoặc bật thêm `Thông tin tài liệu`, rồi test lại cùng câu hỏi.
2. **Nội dung lỗi thời trong meta-KB** — đã vá số đếm KB trong `KBCFL-10` ngày 17/08/2026. Cần đặt nhịp rà lại định kỳ, vì đây là lỗi tự sinh ra theo thời gian.
3. **Truy hồi bỏ sót ảnh ở Case 1** — 2 ảnh có trong kho nhưng không được gắn vào bảng đối chiếu.
4. **`CS Copilot` không render thân câu trả lời** — chưa xác định nguyên nhân.

---

## 6. Truy nguyên gốc lỗi thời ở Case 2 — ảnh chụp bị chuyển thành chữ tra cứu được

### 6.1 Đã kiểm chứng

Ba thông tin sai của `Knowledge Curator` khớp gần như từng ký tự với nội dung nhìn thấy trong ba ảnh nằm trong KB `GS9 Knowledge VNG AI`:

| Câu sai của Agent | Ảnh nguồn khớp |
|---|---|
| "hệ thống chỉ có 6 trợ lý mặc định, không có agent nào tên CFL" | `image-26-agent-tong-quan-danh-sach.png` — hiện `Tất cả agent 6 · Của tôi 0 · Mặc định 6` và đúng 6 tên |
| "Knowledge VNG - Image Assets (RAG + WIKI)" | `image-41-agent-test-kb-da-nguon.png` — dropdown chọn KB ngày 11/08/2026, có đúng nhãn `RAG` `WIKI` |
| "Drive CFL Viax (sync mỗi 15 phút, trạng thái Thành công)" | `image-25-google-drive-dong-bo-thanh-cong.png` |

**Cơ chế đã xác nhận bằng truy vấn trực tiếp vào chỉ mục** (`keyword_search` MCP, chuỗi `Drive CFL Viax`): nền tảng OCR nội dung ảnh **và** sinh mô tả ảnh **ngay lúc nạp**, lưu thành chunk văn bản tìm kiếm được. Bằng chứng nguyên văn:

- `image-25...png`, `chunk_type: "image_caption"` → *"…a connected data source: 'Drive CFL Viax' (Google Drive), marked as 'Đã kết nối'. Sync settings include: incremental sync, all files in folder, **every 15 minutes**… status 'Thành công'."*
- `image-25...png`, `chunk_type: "text"` → *"# Drive CFL Viax / Google Drive / Chế độ đồng bộ / Tăng dân / … / Lich / Môi 15 phút / Đã kết nối"*
- Chuỗi này còn xuất hiện ở `image-15-...png` và `image-33-...png`.

Tức là **ảnh minh hoạ giao diện đã trở thành nguồn dữ kiện chữ**, không cần Agent "nhìn ảnh" lúc trả lời.

### 6.2 Chưa kết luận

- **Chưa chứng minh tuyệt đối** rằng câu trả lời sai lấy đúng từ các chunk trên. Trùng chuỗi rất mạnh nhưng chưa có trace truy hồi chỉ đích danh chunk.
- KB **chưa phân tích xong** các tệp mới đồng bộ tại thời điểm test → trạng thái còn biến động.
- Giả thuyết cạnh tranh chưa loại trừ: Agent bịa, hoặc lấy từ ngữ cảnh hội thoại cũ.

**Phải test lại sau khi KB xử lý xong toàn bộ tệp.**

### 6.3 Điểm mấu chốt: lời tự nhận của Agent không dùng làm bằng chứng

Khi bị hỏi vặn *"có phải bạn tự đọc ảnh rồi tự chế ra không?"*, Agent quay ra nhận **đã bịa toàn bộ** và khẳng định `GS9 CFL PUM`, `GS9 CFL Data Daily`, `GS9 CFL Item Profile` "không hề tồn tại", `GS9 CFL Knowledge Agent` "rỗng (0 tài liệu)".

**Cả bốn khẳng định này đều sai** — bốn KB đó lần lượt có 7, 8, 8 và 8 tài liệu (đếm trên Web cùng ngày). Model nhận bừa theo hướng câu hỏi gợi ý.

→ **Quy tắc: không dùng lời Agent tự mô tả về chính nó làm bằng chứng, theo cả hai chiều.** Kiểm bằng API/UI.

### 6.4 Hướng xử lý

Đã làm tạm: gắn dòng cảnh báo "ảnh chụp một thời điểm, không phải danh mục hiện hành" cạnh 7 ảnh mang danh sách trong nguồn Human (`Agent-13`, `Agent-16` ×3, `KB-08` ×2, `KB-12`).

**Vá tạm này không giải quyết gốc** — không thể chụp lại ảnh mỗi lần hệ thống đổi, trong khi ảnh chỉ để minh hoạ giao diện. Người dùng đề xuất hướng gốc, cần thử:

1. **Tắt VLM / đọc ảnh ở các KB thuần hướng dẫn** (`GS9 Knowledge VNG AI`, `GS9 CFL Knowledge Agent`) — cắt đứt đường dữ liệu cũ lọt vào câu trả lời. **Chưa thử, chưa biết có tắt riêng từng KB được không, và tắt rồi ảnh có còn hiển thị trong câu trả lời không.**
2. **Giữ VLM ở KB nghiệp vụ** như `GS9 CFL Plan Version` — ở đó nội dung trong ảnh chính là thứ cần tra, Case 1 chứng minh chạy tốt.
3. Che phần danh sách khi chụp ảnh minh hoạ.

**Việc phải làm phiên sau:** thử tắt VLM trên một KB hướng dẫn, chạy lại đúng câu hỏi Case 2, so kết quả.

---

## 7. BẰNG CHỨNG MỚI (cuối phiên) — Agent truy hồi thẳng một tài liệu ảnh

Người dùng chạy lại Case 2 và cung cấp ảnh chụp cây suy luận: `docs KB/Asset/chat/case2-trace-lay-tai-lieu-anh.png`.

Cây 9 bước ghi rõ, theo thứ tự:

1. `Đang tìm trong kho tri thức: "CFL game chính sách xử phạt người chơi gian lận, CFL cheating penalty policy…"` → **Không có kết quả**
2. `Tìm theo từ khoá: "CFL|cheating|gian lận|xử phạt|penalty"` → **12 khớp**
3. `Đang tìm trong kho tri thức: "CFL Agent nào xử lý chính sách game, Các Agent mặc định và Agent CFL trên GS9…"` → **1 kết quả**
4. `Tìm theo từ khoá: "Agent.*CFL|CFL.*Agent|trợ lý.*CFL|CFL.*trợ lý"` → **6 khớp**
5. **`Lấy tài liệu: image-01-tong-quan-danh-sach-knowledge.png`**

**Bước 5 là bằng chứng trực tiếp:** Agent chủ động lấy **một tài liệu ảnh** làm nguồn trả lời, gọi đích danh tên tệp `.png`. Trước đó ta chỉ suy từ việc trùng chuỗi; nay có trace gọi thẳng.

Kết hợp với mục 6.1 (ảnh sinh chunk `image_caption` + `text` lúc nạp), **cơ chế đã rõ**: ảnh nằm trong kho là tài liệu tra cứu được như mọi tài liệu khác, và nội dung hiển thị bên trong ảnh trở thành dữ kiện.

**Nâng mức phân loại:** từ *Có điều kiện* lên **Đã kiểm chứng** cho mệnh đề "ảnh trong kho được truy hồi làm nguồn và nội dung trong ảnh trở thành dữ kiện trả lời".

**Vẫn còn biến số:** lượt chạy này dùng model **`deepseek-v4-flash`** (khác lượt trước, `hosted_vllm/qwen3.6-...`), và KB có thể đã phân tích thêm tệp. Khi test lại phải ghi rõ model đang dùng.

**Không đổi kết luận về hướng xử lý** — vẫn là: thử tắt VLM/đọc ảnh ở KB thuần hướng dẫn, giữ ở KB nghiệp vụ, rồi so kết quả.

---

## 8. GIẢ THUYẾT CẠNH TRANH MẠNH (phiên 5, máy công ty) — lúc test, ảnh có thể là nguồn DUY NHẤT

Trước khi chạy lại Case 2, đã đọc trực tiếp trạng thái phân tích tệp của `GS9 Knowledge VNG AI` trên Web (`Documents` → lọc theo `Trạng thái`).

**Số liệu đọc được:**

| Nhóm tệp | Số lượng | Trạng thái | Ngày cập nhật |
|---|---|---|---|
| Ảnh `.png` | 49 | **Hoàn tất** — đã index, mỗi ảnh có mô tả sinh sẵn hiển thị ngay dưới tên | 15–16/08/2026 |
| Markdown `doc-09` | 1 | Đang xử lý | 17/08/2026 |
| Markdown còn lại (`doc-00`→`doc-20` trừ `doc-09`) | 20 | **Chờ xử lý** | 17/08/2026 |

Tức là **toàn bộ 21 tài liệu chữ chưa vào chỉ mục, trong khi cả 49 ảnh đã vào**. Hàng đợi chạy tuần tự từng tệp một.

**Hệ quả với kết luận ở mục 6 và 7.** Mệnh đề "ảnh trong kho được truy hồi làm nguồn" vẫn đúng — trace bước `Lấy tài liệu: image-01-...png` là bằng chứng trực tiếp, không phụ thuộc trạng thái chỉ mục. **Nhưng** có một cách giải thích cạnh tranh chưa loại trừ được cho việc Agent trả lời sai:

> Không phải "Agent ưu tiên ảnh hơn chữ", mà có thể là **lúc chạy Case 2, ảnh là nguồn duy nhất tồn tại trong chỉ mục** — tài liệu chữ khi đó cũng đang ở trạng thái chờ xử lý như bây giờ.

Điều này khớp với chi tiết đã ghi ở mục 2: vòng tìm ngữ nghĩa đầu tiên trả **`Không có kết quả`**, và cả hai vòng chỉ moi được rất ít kết quả. Nếu 21 tài liệu chữ đã có trong chỉ mục thì câu hỏi về Agent và kho lẽ ra phải trúng `doc-02`, `doc-13`, `doc-16`.

**Chưa chứng minh** giả thuyết này, vì không có ảnh chụp trạng thái chỉ mục tại đúng thời điểm chạy Case 2 ngày 17/08. Ghi lại để không kết luận vội theo hướng đổ hết cho VLM.

**Hệ quả với cách test:** **không được chạy lại Case 2 khi 21 tài liệu chữ còn ở trạng thái Chờ xử lý.** Chạy lúc này chắc chắn tái hiện lỗi, nhưng vì lý do tầm thường (chữ chưa index), không phân biệt được hai giả thuyết. Phải đợi đủ hai điều kiện rồi mới chạy:

1. Bộ lọc `Chờ xử lý` và `Đang xử lý` của KB trả về **rỗng**.
2. Bộ lọc `Hoàn tất` đếm đủ **70** tài liệu (49 ảnh + 21 chữ).

Khi đó mới ghi model và chạy đúng câu hỏi Case 2.

**Quan sát phụ, củng cố mục 6.1:** trong danh sách `Hoàn tất`, phần mô tả của nhiều ảnh hiện thẳng nội dung sinh tự động — ví dụ `image-02` mô tả *"The document depicts a configuration modal window for a Knowledge…"*, `image-06` mô tả *"The document describes the 'Chia sẻ' (Share) configuration interface…"*. Đây là chữ tra cứu được, đúng như đã ghi ở mục 6.1. Một số ảnh khác có mô tả bắt đầu bằng chuỗi `![image-...](minio://...` — tức trường mô tả chứa cả cú pháp nhúng ảnh.
