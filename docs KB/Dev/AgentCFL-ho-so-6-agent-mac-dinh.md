# AgentCFL — hồ sơ chi tiết 6 Agent mặc định

**Ngày kiểm chứng:** 14/08/2026 (audit chỉ-đọc UI, không mutation, không chat-test).
**Đối tượng:** Dev và Agent config.
**Quan hệ với file khác:** `Agent-ho-so-16-agent-cfl.md` mục 2 là **bảng tổng hợp** 6 Agent này. File hiện tại là **hồ sơ từng Agent**: mục đích, ranh giới dùng/không dùng, biến prompt, mâu thuẫn tĩnh và điều chưa kiểm chứng riêng của từng Agent. Không chép lại bảng tổng hợp.

Tham số cấu hình không lặp ở đây:

| Cần tra | Đọc file |
|---|---|
| Model, temperature, reranker, `Chế độ suy nghĩ` | `Agent-cau-hinh-va-tham-so.md` mục 2–5 |
| Top K, ngưỡng vector/keyword/rerank, vòng lặp, timeout, parallel | `Agent-cau-hinh-va-tham-so.md` mục 6 · `Agent-kho-tri-thuc-va-tool.md` mục 2 |
| Danh mục tool và điều kiện bật | `Agent-kho-tri-thuc-va-tool.md` mục 3 |
| Mode, preset, `Prompt theo intent` | `Agent-preset-prompt-va-intent.md` |

---

## 0. Ba điều đúng cho cả sáu

1. **Cả sáu để `Tất cả kho tri thức`.** Đây là ranh giới bảo mật rộng nhất có thể. Hệ quả trực tiếp: **không nhân bản Agent mặc định để làm việc trên dữ liệu nhạy cảm** — bản sao kế thừa phạm vi này (DEC-034).
2. **Không có panel `Chia sẻ`.** Không kết luận được public/private, ai dùng được, ai sửa được. **Bị chặn–Chưa xác định**.
3. **Không Agent nào chat-test.** Mọi mô tả hành vi trong file này đọc từ System Prompt và mô tả UI, nên ở mức **Có điều kiện** (DEC-022: cấu hình UI không bằng hành vi runtime).

---

## 1. `Quick Answer`

**Mô tả UI:** `Knowledge base RAG Q&A for fast and accurate answers`.

**Prompt định vị:** trợ lý hỏi đáp trên context truy hồi, giữ nguyên marker/link ảnh, trả Markdown theo `{{language}}`, báo khi không tìm thấy.

| Dùng khi | Không dùng khi |
|---|---|
| Cần câu trả lời nhanh từ KB, không cần điều phối tool nhiều bước | Công việc cần allowlist KB hoặc least privilege |
| Chấp nhận được giới hạn của mode `Trả lời nhanh` và kiểm lại nguồn thủ công | Câu trả lời tuyệt đối không được fallback sang general knowledge |
| | Cần Wiki, SQL, Data Analysis, Catalog hoặc action tool |

**Riêng của Agent này** (không Agent mặc định nào khác có):

- `Max output tokens` = `0`; UI giải thích là không giới hạn.
- Tab `Hội thoại`: multi-turn Bật, giữ `5` lượt, query rewrite Bật. Nếu bỏ trống rewrite model thì dùng chính model chat.
- `Chiến lược dự phòng` = `Mô hình tự sinh`.
- `Phân tích bảng dữ liệu` Tắt.
- Không có tab `Công cụ` → **0 tool**.

**Biến prompt nhìn thấy:** `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`.

**Rewrite classifier** phân loại câu hỏi thành: `greeting`, `summarize`, `kb_search`, `clarification`, `follow_up`, `image_only`, `doc_only`, `chitchat`. Mặc định rơi về `kb_search`. Output của rewrite là JSON gồm câu hỏi đã viết lại, intent và mô tả ảnh.

> **Mâu thuẫn tĩnh — Đã kiểm chứng (static), runtime Có điều kiện.**
> System Prompt cấm dùng prior knowledge. Fallback prompt lại **cho phép** general knowledge khi danh sách tài liệu rỗng. Hai nhánh đối nghịch nhau trong cùng một Agent. Chưa chat-test nên **không biết nhánh nào thắng**. Đây là rủi ro trả lời không nguồn cao nhất trong 6 Agent mặc định.

**Chưa kiểm chứng riêng:** grounding thực tế, citation, render ảnh, ACL/share, quota, retention, latency, nhánh fallback nào chạy.

---

## 2. `Smart Reasoning`

**Mô tả UI:** `ReAct reasoning framework with multi-step thinking and tool calling`.

**Prompt định vị:** Progressive Agentic RAG, Evidence-First. Yêu cầu: truy hồi mới cho mỗi câu hỏi mới, fan-out semantic + keyword, đọc full chunk/FAQ, **không** fallback general knowledge khi KB không có bằng chứng.

| Dùng khi | Không dùng khi |
|---|---|
| Cần RAG nhiều bước, evidence-first trên tài liệu/chunk | Cần Wiki, SQL, Data Analysis hoặc Catalog — không tool nào trong nhóm này active |
| Cần fan-out rồi đọc sâu trước khi tổng hợp | Cần dữ liệu allowlist nhạy cảm (đang All KB) |

**Biến prompt:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`. Không có per-intent override.

**Đối lập với `Quick Answer`:** Agent này prompt **cấm hẳn** fallback general knowledge, không có nhánh cho phép. Về mặt tĩnh, đây là Agent mặc định an toàn nhất cho câu hỏi phải có nguồn.

**Cảnh báo dùng:** không lấy số vòng lặp hoặc số tool gọi ra làm bằng chứng chất lượng. `50` loops là trần cao nhất trong 6 Agent, không phải chỉ dấu Agent "suy nghĩ kỹ hơn".

**Chưa kiểm chứng riêng:** grounding runtime, thứ tự gọi tool thực tế, source permission, sharing, quota, retention, latency, chất lượng câu trả lời.

---

## 3. `Hybrid Researcher`

**Mô tả UI:** lấy tổng quan rộng bằng Wiki/chunk rồi đào sâu để trả lời chính xác có citation.

**Prompt định vị:** Wiki là **concept map**; raw chunk là **evidence** cho quote, số liệu và code. Khi hai lớp mâu thuẫn thì phải gắn cờ issue.

| Dùng khi | Không dùng khi |
|---|---|
| Cần Wiki làm bản đồ khái niệm và raw chunk làm bằng chứng chi tiết | Chỉ có Wiki, không muốn chunk RAG — dùng `Wiki Questioner` |
| Cần fan-out Wiki + semantic + keyword rồi deep-read | Cần SQL / Data Analysis / Catalog |

**Riêng của Agent này:** là Agent mặc định **duy nhất bật `Gọi song song`** (14/08/2026), và là Agent duy nhất có đủ cả 3 tool Wiki + 4 tool RAG chunk cùng lúc.

Hệ quả của parallel + All KB: phạm vi truy hồi mở rộng nhanh hơn các Agent khác. Kiểm tra source scope trước khi hỏi.

> **Mâu thuẫn tĩnh — Đã kiểm chứng.** Prompt nhắc `wiki_flag_issue` nhưng tool này **không** có trong danh sách tool hiệu lực trên UI. Cơ chế "gắn cờ khi Wiki và raw source mâu thuẫn" vì vậy **không có đường thực thi**. Chưa runtime test nên chưa biết Agent biểu diễn conflict bằng cách nào — hoặc có im lặng chọn một bên không.

**Chưa kiểm chứng riêng:** capability routing, parallel fan-out có thật sự chạy song song, deep-read bắt buộc, cách biểu diễn conflict, source precedence, citation, ACL/share, quota.

---

## 4. `Wiki Questioner`

**Mô tả UI:** Agent chuyên trả lời từ KB dạng Wiki.

**Prompt định vị:** dùng trang `index` cho overview, trang `log` cho timeline; đọc trang Wiki trước khi trả lời; đi theo link 1–2 hop; chỉ đọc tài liệu nguồn khi Wiki thiếu quote hoặc raw data. Workflow đặt tên là Search–Read–Expand.

| Dùng khi | Không dùng khi |
|---|---|
| Câu hỏi hợp với Wiki đã có trang và link được quản trị tốt | Cần raw chunk RAG làm nguồn chính |
| Cần đi theo link 1–2 hop | Cần SQL / Data Analysis / Catalog |
| | Wiki chưa có owner hoặc chưa truy được về nguồn gốc |

> **Hai vấn đề tĩnh:**
> - `wiki_flag_issue` — cùng vấn đề với `Hybrid Researcher`: prompt nhắc, UI không có tool.
> - **External MCP** — prompt cho phép gọi external MCP nếu được expose. Audit **không chứng minh** external MCP nào đang active. Mức: **Bị chặn–Chưa xác định**. Đây là bề mặt tấn công tiềm năng cần đóng lại trước khi phát hành: nếu một MCP server nào đó được expose sau này, prompt đã sẵn sàng gọi nó mà không cần sửa gì.

**Cảnh báo dùng:** Wiki là lớp dẫn xuất. Không coi graph/link trong Wiki là authority. Wiki stale hoặc mâu thuẫn thì dừng và báo owner, không tự hoà giải.

**Chưa kiểm chứng riêng:** workflow Search–Read–Expand có chạy đúng thứ tự không, hành vi theo link, external MCP.

---

## 5. `Data Analyst`

**Prompt định vị:** lấy schema trước khi viết SQL; **chỉ cho phép `SELECT`**; cấm `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`; tự sửa query khi lỗi; trả insight kèm bảng kết quả.

| Dùng khi | Không dùng khi |
|---|---|
| Phân tích CSV/XLSX đã audit bằng schema + phân tích kiểu DuckDB | Cần query database trực tiếp, RAG tài liệu, Wiki hoặc Catalog |
| Cần insight có query/calculation tái lập | Dataset có raw PII, secret, hoặc quyền/retention chưa rõ |
| | Cần ghi hoặc thay đổi production data |

**Riêng của Agent này:**

- Là Agent mặc định duy nhất có temperature `0.3` (5 Agent còn lại `0.7`).
- Là Agent mặc định duy nhất **lọc loại tệp**: `Tất cả kho tri thức` nhưng chỉ `CSV`, `XLSX`. Lọc loại tệp là lớp thu hẹp phạm vi duy nhất đang được dùng trong 6 Agent mặc định.
- Là Agent mặc định duy nhất hạ Top K xuống `5` (vector và rerank).
- SQL chạy **bên trong luồng Data Analysis**, không phải qua tool `Truy vấn CSDL`.

> **Cảnh báo quan trọng.** `SELECT`-only là **ràng buộc trong prompt**, không phải ràng buộc kỹ thuật đã được chứng minh. Audit **không chạy một query nào**. Không suy ra runtime enforcement từ câu chữ trong prompt. Vẫn phải review SQL mà Agent sinh ra.

**Yêu cầu tối thiểu với output:** bắt Agent ghi rõ dataset, kỳ, timezone, filter, cohort, mẫu số, đơn vị và query/calculation. Bắt phân biệt `missing` với `0` — đây là lỗi phân tích tốn kém nhất và Agent không tự tránh.

**Chưa kiểm chứng riêng:** query enforcement, cô lập giữa các file, độ chính xác tính toán, quota, retention, ACL, hành vi privacy.

---

## 6. `FPA Analyst`

**Mô tả UI:** pipeline cố định — hiểu câu hỏi → định tuyến tới nguồn phù hợp → truy hồi.

**Prompt định vị:** chỉ trả lời từ nội dung truy hồi; giữ chính xác số liệu, kỳ và đơn vị; **không coi missing là zero**; query source inventory khi user hỏi về nguồn.

| Dùng khi | Không dùng khi |
|---|---|
| Cần workflow FPA cố định để route nguồn và báo cáo hiệu suất | Cần **bảo đảm** về source scope |
| Có quyền hợp lệ với Catalog/database và tự review được số liệu/kỳ/đơn vị | Cần Wiki hoặc tool Data Analysis cho CSV/XLSX |
| | Việc nhạy cảm chưa qua review least-privilege |

**Riêng của Agent này:**

- Agent mặc định duy nhất ở mode `Quy trình` (workflow cố định tên `fpa`).
- Agent mặc định duy nhất **bật `Chế độ suy nghĩ`**.
- Agent mặc định duy nhất hạ ngưỡng vector xuống `0.3` (5 Agent còn lại `0.5`) → cửa truy hồi rộng hơn, nhiễu vào context nhiều hơn.
- Agent mặc định duy nhất có tool `Truy vấn CSDL` và `Danh mục sản phẩm` cùng lúc. Đây là Agent mặc định có bề mặt quyền lớn nhất.
- Timeout `180s` — dài nhất; vòng lặp `10` — ngắn nhất. Pipeline cố định nên cần ít vòng nhưng mỗi vòng nặng hơn.

> **Mâu thuẫn tĩnh — Có điều kiện.** Prompt nói pipeline đã hiểu câu hỏi và **thu hẹp scope nguồn**, nhưng UI vẫn để `Tất cả kho tri thức`. Chỉ runtime hoặc source-drawer evidence mới chứng minh được scoping thật. Trong lúc chưa có bằng chứng, **coi như Agent đang tra toàn bộ KB**.

> **Cảnh báo quyền.** Không suy ra `Truy vấn CSDL` là read-only chỉ từ prompt. Phải kiểm tra policy của chính tool và backend. Đây là Agent duy nhất trong 6 Agent mặc định có đường ghi tiềm năng vào database.

**Chưa kiểm chứng riêng:** routing của fixed pipeline, quyền database hiệu lực, source scoping thật, quota, sharing, retention, chất lượng tính toán. Audit **không chạy DB test và không chạy chat test**.

---

## 7. Bảng tra nhanh bốn mâu thuẫn tĩnh

Cả bốn đều **Đã kiểm chứng ở mức đọc prompt**, và cả bốn đều **chưa runtime test**.

| Agent | Mâu thuẫn | Rủi ro nếu nhánh xấu thắng |
|---|---|---|
| `Quick Answer` | Prompt cấm prior knowledge · fallback prompt cho phép general knowledge khi document list rỗng | Trả lời không nguồn, đọc như có nguồn |
| `Hybrid Researcher` | Prompt nhắc `wiki_flag_issue` · tool không active | Mâu thuẫn Wiki ↔ raw source bị nuốt im lặng |
| `Wiki Questioner` | Cùng vấn đề `wiki_flag_issue` · thêm external MCP được prompt cho phép nhưng chưa xác định | Như trên, cộng bề mặt gọi tool ngoài không kiểm soát |
| `FPA Analyst` | Prompt nói đã scope nguồn · UI vẫn All KB | Tưởng least-privilege trong khi đang tra toàn bộ KB |

Bốn mục này nên là bốn test case đầu tiên khi G6 (chat-test grounding) được chạy.

---

## Chưa kiểm chứng — toàn nhóm

- **Chất lượng grounding của cả 6.** Gate G6 chưa chạy. Toàn bộ hành vi ở mức **Bị chặn–Chưa xác định**.
- **Sharing / ACL.** Không có panel Chia sẻ → không biết ai dùng được, ai sửa được.
- **Quyền thực thi menu.** Menu chỉ có `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`. **Không thấy `Xóa`** — chưa xác nhận là bị chặn hay chỉ ẩn.
- **Quota, retention, latency, model availability** cho cả 6.
- **Owner nghiệp vụ.** Nguồn audit **không ghi** owner cho bất kỳ Agent mặc định nào. Đây là khoảng trống governance: sáu Agent có quyền tra toàn bộ KB nhưng không ai đứng tên.

## Nguồn

| Nguồn | Nội dung |
|---|---|
| `audit/default-agent-readonly-audit-2026-08-14.md` | Audit chỉ-đọc tổng, 14/08/2026 |
| `agent/quick-answer-config.md` | `SRC-D-QUICK` |
| `agent/smart-reasoning-config.md` | `SRC-D-SMART` |
| `agent/hybrid-researcher-config.md` | `SRC-D-HYBRID` |
| `agent/wiki-questioner-config.md` | `SRC-D-WIKI` |
| `agent/data-analyst-config.md` | `SRC-D-DATA` |
| `agent/fpa-analyst-config.md` | `SRC-D-FPA` |
| `knowledge/GS9 CFL Knowledge Agent/doc-10`→`doc-15` | Hồ sơ meta-KB viết tay, nguồn trực tiếp của file này |
| `DECISIONS.md` | DEC-007, DEC-022, DEC-034 |
