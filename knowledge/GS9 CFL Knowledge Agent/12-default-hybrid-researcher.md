# Default Agent — Hybrid Researcher

**Loại:** Default Agent  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Chưa xác định trong nguồn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Cấu hình UI đã audit; runtime chưa kiểm thử  
**Mức bằng chứng:** Đã kiểm chứng cho config; Có điều kiện cho routing  
**Nguồn chính:** `SRC-D-HYBRID`, `SRC-DEFAULT-AUDIT`

## Dùng khi

- Cần Wiki làm bản đồ khái niệm và raw chunk làm bằng chứng chi tiết.
- Cần fan-out Wiki + semantic + keyword, sau đó deep-read.

## Không dùng khi

- Chỉ có Wiki và không muốn chunk RAG: xem [Wiki Questioner](13-default-wiki-questioner.md).
- Cần SQL/Data Analysis/Catalog.
- Dữ liệu nhạy cảm chưa có allowlist; Agent đang All KB.

## Mục đích và đầu ra dự kiến

Mô tả UI: broad overview bằng Wiki/chunk, sau đó drill-in để trả lời chính xác có citation. Prompt coi Wiki là concept map và raw chunk là evidence cho quote, number và code; nếu hai lớp mâu thuẫn phải gắn cờ issue.

## Cấu hình Web đã kiểm chứng

| Trường | Giá trị |
|---|---|
| Mode / preset | `Suy luận thông minh` / `Kết hợp RAG + Wiki` |
| Model / reranker | `qwen3.6-plus` / `bge-reranker-v2-m3` |
| Temperature / Thinking | `0.7` / Off |
| KB / file type | `Tất cả kho tri thức` / `Tất cả loại tệp` |
| Retrieval | Tự động |
| Vector Top K | `10` |
| Keyword / vector threshold | `0.3` / `0.5` |
| Rerank Top K / threshold | `10` / `0.3` |
| Max loops / timeout | `40` / `120s` |
| Parallel tool calls | On |
| Image / audio | Off / Off |

**Nguồn:** `SRC-D-HYBRID`, `SRC-DEFAULT-AUDIT`; **as-of:** 14/08/2026.

## Tool hiệu lực

- Wiki: `Tìm Wiki`, `Đọc trang Wiki`, `Đọc tài liệu nguồn`.
- RAG: `Tìm theo ngữ nghĩa`, `Tìm theo từ khóa`, `Liệt kê đoạn`, `Thông tin tài liệu`.

Basic tools, SQL, Catalog, schema và Data Analysis không active.

## Static mismatch

**Đã kiểm chứng:** Prompt nhắc `wiki_flag_issue`, nhưng tool này không có trong danh sách active UI. Vì chưa runtime test, không biết Agent sẽ biểu diễn conflict thế nào.

## Cách dùng an toàn

1. Dùng khi cả Wiki và source document có governance rõ.
2. Kiểm tra raw source cho con số/quote; không dùng Wiki summary làm bằng chứng duy nhất.
3. Khi Wiki và raw source conflict, yêu cầu liệt kê cả hai; không để Agent tự chọn im lặng.
4. Kiểm tra source scope vì All KB và parallel fan-out có thể mở rộng retrieval.

## Runtime evidence và giới hạn

**Có điều kiện:** capability routing, parallel fan-out và mandatory deep-read.

**Bị chặn–Chưa xác định:** runtime flagging, citation, source precedence, ACL/share, quota và quality.

## Nguồn

- `agent/hybrid-researcher-config.md`
- `audit/default-agent-readonly-audit-2026-08-14.md`
- Xem [chooser](01-chon-agent-nhanh.md) và [safety gate](05-su-dung-an-toan-va-release-gate.md).

