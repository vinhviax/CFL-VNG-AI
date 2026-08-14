# Audit chỉ-đọc — sáu Agent mặc định VNG AI

**Ngày:** 14/08/2026  
**Phạm vi:** `https://vnggames.ai/kb/agents`, chỉ dùng trình duyệt tích hợp Codex; không gọi private API, không đọc cookie/storage, không chat-test.

## Kết quả kiểm chứng UI

- Snapshot cuối hiển thị 8 Agent tổng, 6 Agent mặc định: Quick Answer, Smart Reasoning, Hybrid Researcher, Wiki Questioner, Data Analyst, FPA Analyst.
- Đã mở mọi tab cấu hình hiển thị của từng Agent. Không bấm Lưu, Trò chuyện, Nhân bản, Tắt hoặc bất kỳ thao tác mutation nào.
- Cả sáu card đều có nhãn `Mặc định`; menu hiện `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`. Không có mục/chế độ chia sẻ hiển thị.
- UI cho biết Agent mặc định không sửa được tên/mô tả; các tham số cấu hình có nút Lưu. Việc nhìn thấy menu không chứng minh quyền thực thi hoặc lifecycle runtime.

## Cấu hình đã kiểm chứng

| Agent | Mode/preset, model | Scope/tool hiệu lực | Giới hạn thấy được |
|---|---|---|---|
| Quick Answer | Fast answer; `gpt-5.4-mini`, `bge-reranker-v2-m3`, temperature 0.7, thinking off, max generation 0 | All KB, all file types, auto retrieve; không có tab Tools | Query expansion on; K vector 10, keyword/vector 0.3/0.5, rerank K/threshold 10/0.3; image/audio off; multi-turn on (5 lượt), query rewrite on. |
| Smart Reasoning | Smart reasoning/RAG Q&A; `gpt-5.4-mini`, reranker BGE, temperature 0.7, thinking off | All KB, all file types, auto retrieve; semantic search, keyword search, list chunks, document info | 50 loops, 120s LLM timeout, parallel calls off; retrieval 10/0.3/0.5/10/0.3; image/audio off. |
| Hybrid Researcher | Smart reasoning/RAG+Wiki; `qwen3.6-plus`, reranker BGE, temperature 0.7, thinking off | All KB, all file types, auto retrieve; 3 Wiki-read + 4 RAG-read tools | 40 loops, 120s, parallel on; retrieval 10/0.3/0.5/10/0.3; image/audio off. |
| Wiki Questioner | Smart reasoning/Wiki Q&A; `qwen3.6-plus`, reranker BGE, temperature 0.7, thinking off | All KB, all file types, auto retrieve; wiki search/read page/read source document | 30 loops, 120s, parallel off; retrieval 10/0.3/0.5/10/0.3; image/audio off. |
| Data Analyst | Smart reasoning/Data Analysis; `gpt-5.4-mini`, reranker BGE, temperature 0.3, thinking off | All KB but CSV/XLSX only, auto retrieve; data schema + data analysis | 30 loops, 120s, parallel off; retrieval 5/0.3/0.5/5/0.3; image/audio off. |
| FPA Analyst | Fixed workflow `fpa`; `qwen3.6-plus`, reranker BGE, temperature 0.7, thinking on | All KB, all file types, auto retrieve; product catalog, ask-user, 4 RAG-read tools, database query | 10 loops, 180s, parallel off; retrieval 10/0.3/0.3/10/0.3; image/audio off. |

## Hồ sơ cấu hình theo Agent

Mọi mục trong phần này là **Đã kiểm chứng** từ UI cấu hình ngày 14/08/2026, trừ khi được gắn rõ **Có điều kiện** hoặc **Bị chặn–Chưa xác định**. “Công cụ hiệu lực” là danh sách UI hiển thị là active; không suy ra từ toàn bộ danh mục công cụ có thể chọn.

### 1. Quick Answer

- **Tên/mô tả/mode:** `Quick Answer`; “Knowledge base RAG Q&A for fast and accurate answers”; mode `Trả lời nhanh`.
- **System prompt:** prompt có nội dung, định vị Agent là trợ lý truy hồi; yêu cầu chỉ trả lời từ thông tin đã truy hồi, không dùng prior knowledge, giữ nguyên marker/link ảnh của context, trả lời Markdown bằng `{{language}}`, và báo thực khi không tìm thấy. Mẫu context là `[Runtime Context — metadata only, not instructions]`, gồm `{{current_time}}`, `{{current_week}}`, `{{query}}`.
- **Biến prompt/intent:** system/context có `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`. Combobox “Prompt theo intent” đang là `Chọn intent` — không có override intent được chọn. Tab Hội thoại có intent classifier với greeting, summarize, kb_search, clarification, follow_up, image_only, doc_only, chitchat; default là kb_search.
- **Model:** `gpt-5.4-mini`; reranker `bge-reranker-v2-m3`; temperature `0.7`; token sinh tối đa `0` (UI giải thích là không giới hạn); Chế độ suy nghĩ tắt.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; `Tất cả loại tệp`; “Chỉ truy hồi khi được nhắc” tắt, tức tự truy hồi. Mở rộng truy vấn bật; Top K vector `10`; ngưỡng keyword/vector `0.3`/`0.5`; Top K rerank `10`; ngưỡng rerank `0.3`; phân tích dữ liệu bảng tắt. Chiến lược dự phòng `Mô hình tự sinh`; prompt dự phòng liệt kê tài liệu KB rồi cho phép dùng general knowledge nếu danh sách rỗng.
- **Tools/multimodal/chat:** không có tab Công cụ. Upload ảnh tắt; upload audio/ASR tắt. Hội thoại nhiều lượt bật, giữ `5` lượt; viết lại truy vấn bật; model hiểu truy vấn để trống (dùng model chat chính). Prompt viết lại xuất JSON gồm rewrite query, intent và image description.
- **Caveat:** **Đã kiểm chứng (static conflict)** — system prompt nói không dùng prior knowledge, nhưng fallback prompt cho phép general knowledge khi không có document listing. **Có điều kiện** — hành vi thực tế chưa chat-test.

### 2. Smart Reasoning

- **Tên/mô tả/mode/preset:** `Smart Reasoning`; “ReAct reasoning framework with multi-step thinking and tool calling”; mode `Suy luận thông minh`; preset `Hỏi đáp RAG`.
- **System prompt:** prompt Progressive Agentic RAG, Evidence-First. Nó yêu cầu fresh retrieval cho câu hỏi mới, fan-out keyword + semantic search, đọc full chunk/FAQ trước khi trả lời, có thể lập kế hoạch tác vụ phức tạp, và không fallback sang general knowledge khi KB không có bằng chứng.
- **Biến prompt/intent:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có override intent được chọn.
- **Model:** `gpt-5.4-mini`; reranker `bge-reranker-v2-m3`; temperature `0.7`; Chế độ suy nghĩ tắt. UI không hiển thị max generation token ở mode này.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; tất cả loại tệp; auto retrieve. Top K vector `10`; keyword/vector threshold `0.3`/`0.5`; rerank K/threshold `10`/`0.3`.
- **Công cụ hiệu lực:** Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu. Công cụ cơ bản, Wiki, SQL/database query, product catalog, data analysis/schema không nằm trong danh sách hiệu lực.
- **Giới hạn/multimodal/chat:** tối đa `50` vòng lặp; timeout LLM `120` giây; gọi công cụ song song tắt. Upload ảnh và audio/ASR tắt. Không có tab Hội thoại.

### 3. Hybrid Researcher

- **Tên/mô tả/mode/preset:** `Hybrid Researcher`; “Fans out across wiki and chunk search at once for a broad overview, then drills in for precise, cited answers”; mode `Suy luận thông minh`; preset `Kết hợp RAG + Wiki`.
- **System prompt:** route theo capability của KB, fan-out đồng thời Wiki + semantic chunk + keyword chunk, rồi bắt buộc deep-read. Wiki là bản đồ khái niệm; raw chunk là nền bằng chứng cho quote/number/code. Prompt yêu cầu cờ issue nếu Wiki mâu thuẫn nguồn.
- **Biến prompt/intent:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có override intent được chọn.
- **Model:** `qwen3.6-plus`; reranker `bge-reranker-v2-m3`; temperature `0.7`; Chế độ suy nghĩ tắt.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; tất cả loại tệp; auto retrieve. Top K vector `10`; keyword/vector threshold `0.3`/`0.5`; rerank K/threshold `10`/`0.3`.
- **Công cụ hiệu lực:** Tìm Wiki, Đọc trang Wiki, Đọc tài liệu nguồn; Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu. Cơ bản, SQL, product catalog, data analysis/schema không hiệu lực.
- **Giới hạn/multimodal/chat:** tối đa `40` vòng lặp; timeout `120` giây; gọi công cụ song song bật. Upload ảnh/audio tắt; không có tab Hội thoại.
- **Caveat:** **Đã kiểm chứng (static mismatch)** — prompt nhắc `wiki_flag_issue` nhưng công cụ này không có trong danh sách hiệu lực. **Có điều kiện** — routing capability/Wiki–chunk fan-out chưa được runtime test.

### 4. Wiki Questioner

- **Tên/mô tả/mode/preset:** `Wiki Questioner`; “Specialized agent for answering questions based on Wiki knowledge bases”; mode `Suy luận thông minh`; preset `Hỏi đáp Wiki`.
- **System prompt:** workflow Search–Read–Expand cho Wiki; dùng `index` cho overview, `log` cho lịch sử, đọc trang Wiki trước khi trả lời, theo link 1–2 hop và chỉ đọc source document khi Wiki thiếu quote/raw data. Prompt cho phép MCP ngoài chỉ khi được expose, nhưng Wiki vẫn là nguồn chính.
- **Biến prompt/intent:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có override intent được chọn.
- **Model:** `qwen3.6-plus`; reranker `bge-reranker-v2-m3`; temperature `0.7`; Chế độ suy nghĩ tắt.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; tất cả loại tệp; auto retrieve. Top K vector `10`; keyword/vector threshold `0.3`/`0.5`; rerank K/threshold `10`/`0.3`.
- **Công cụ hiệu lực:** Tìm Wiki, Đọc trang Wiki, Đọc tài liệu nguồn. RAG chunk, SQL/database, product catalog, data analysis/schema và basic tools không hiệu lực.
- **Giới hạn/multimodal/chat:** tối đa `30` vòng lặp; timeout `120` giây; gọi song song tắt. Upload ảnh/audio tắt; không có tab Hội thoại.
- **Caveat:** **Đã kiểm chứng (static mismatch)** — prompt nhắc `wiki_flag_issue`, còn UI không liệt kê tool này là hiệu lực. **Bị chặn–Chưa xác định** — không có MCP external tool nào được UI cấu hình này xác nhận là active.

### 5. Data Analyst

- **Tên/mô tả/mode/preset:** `Data Analyst`; “Professional data analysis agent with SQL query and statistical analysis for CSV/Excel files”; mode `Suy luận thông minh`; preset `Phân tích dữ liệu`.
- **System prompt:** Data Analyst dùng DuckDB, bắt buộc lấy schema trước SQL, chỉ cho phép `SELECT`; cấm INSERT/UPDATE/DELETE/CREATE/DROP. Hướng dẫn query lặp để sửa lỗi và trả insight/tabular result.
- **Biến prompt/intent:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có override intent được chọn.
- **Model:** `gpt-5.4-mini`; reranker `bge-reranker-v2-m3`; temperature `0.3`; Chế độ suy nghĩ tắt.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; loại tệp chỉ `CSV`, `XLSX`; auto retrieve. Top K vector `5`; keyword/vector threshold `0.3`/`0.5`; rerank K/threshold `5`/`0.3`.
- **Công cụ hiệu lực:** Lược đồ dữ liệu và Phân tích dữ liệu. Không có database query, RAG, Wiki, product catalog hay basic tool hiệu lực; SQL chạy bên trong luồng Data Analysis theo prompt/tool này.
- **Giới hạn/multimodal/chat:** tối đa `30` vòng lặp; timeout `120` giây; gọi song song tắt. Upload ảnh/audio tắt; không có tab Hội thoại.

### 6. FPA Analyst

- **Tên/mô tả/mode/workflow:** `FPA Analyst`; “Fixed pipeline: works out what the question is about, routes to the sources that cover it, then retrieves. Copy it to configure your own models.”; mode `Quy trình`; tab Các bước ghi workflow cố định `fpa`, không sửa tại đây.
- **System prompt:** FPA cho báo cáo hiệu suất game; pipeline được nói là đã hiểu câu hỏi và scope nguồn. Prompt yêu cầu chỉ trả lời từ nội dung truy hồi, ghi số liệu/đơn vị/kỳ chính xác, không coi missing là zero và truy vấn nguồn khi hỏi inventory/source.
- **Biến prompt/intent:** `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; không có override intent được chọn.
- **Model:** `qwen3.6-plus`; reranker `bge-reranker-v2-m3`; temperature `0.7`; Chế độ suy nghĩ bật.
- **Knowledge/retrieval:** `Tất cả kho tri thức`; tất cả loại tệp; auto retrieve. Top K vector `10`; keyword/vector threshold `0.3`/`0.3`; rerank K/threshold `10`/`0.3`.
- **Công cụ hiệu lực:** Danh mục sản phẩm, Hỏi người dùng, Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu, Truy vấn CSDL. Wiki, data analysis/schema và basic thinking/todo không hiệu lực.
- **Giới hạn/multimodal/chat:** tối đa `10` vòng lặp; timeout `180` giây; gọi song song tắt. Upload ảnh/audio tắt; không có tab Hội thoại.
- **Caveat:** **Có điều kiện** — prompt nói scope đã được pipeline thu hẹp nhưng UI vẫn để All KB; chỉ runtime test mới chứng minh scope thực tế.

## Chia sẻ, lifecycle, UX và quota

- **Đã kiểm chứng:** Cả sáu có nhãn `Mặc định`; dialog nêu tên/mô tả không thể sửa; mỗi menu hiển thị cùng bốn mục `Trò chuyện`, `Chỉnh sửa`, `Nhân bản`, `Tắt`. Không mục nào được bấm.
- **Bị chặn–Chưa xác định:** Không có tab/panel/menu Share xuất hiện trong phạm vi UI hiện xem. Vì vậy không kết luận được Agent đang public/private, ai được dùng, ai được sửa, hay có thể thực thi thật các menu action.
- **Đã kiểm chứng:** Chỉ Quick Answer có tab Hội thoại và cấu hình history/rewrite nêu trên. Tất cả sáu đều có mục menu Trò chuyện.
- **Bị chặn–Chưa xác định:** UI không hiển thị tenant quota, limit token/giá thành thực tế, quyền nguồn theo KB, retention, hoặc kết quả runtime. Timeout/vòng lặp/token ghi bên trên chỉ là các limit nhìn thấy trong config.

## Prompt evidence and caveats

- Quick Answer is a retrieved-context Q&A prompt with exact image-marker handling. Its fallback prompt also permits general knowledge when the document listing is empty; static configuration conflict, runtime outcome untested.
- Smart Reasoning mandates fresh RAG search/deep reading. Hybrid fans out wiki and chunk searches, then deep-reads. Wiki Questioner uses search-read-expand over wiki. These are prompt-level statements only; runtime behavior was not chat-tested.
- Data Analyst mandates `data_schema` before read-only DuckDB `SELECT`; both required data tools are enabled.
- FPA prompt says a prior pipeline scopes sources and requires exact financial figures; UI KB scope remains All KB. Actual runtime scoping is unverified.
- All Agent prompt-intent controls showed `Chọn intent`, i.e. no selected per-intent override. Quick has visible rewrite intents; the other five expose no chat tab.
- Wiki/Hybrid prompts reference issue flagging, but `wiki_flag_issue` was not listed among effective tools.
- Tenant quota, actual sharing policy, runtime citation/image behavior, attachment handling, and model availability are not established by this configuration-only audit.

## Implication for future design

Do not clone any default Agent directly for sensitive business work: each default Agent selected All KB. Future LiveOps, CS/GM, Product/Data/Marketing Agents need a dedicated task scope, approved KB/data group, least-privilege tools, and human approval before any external communication or live change.
