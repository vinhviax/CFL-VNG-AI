# Handoff — Knowledge Base VNG

**Cập nhật:** 16/08/2026 (phiên 3)
**Phiên bản:** 3.4.0 · **Test:** `Ran 30 tests` / `OK` (6 skip do thiếu HTML nguồn Plan V5 trên máy này)

---

## 1. Đọc gì trước

| Thứ tự | File | Vì sao |
|---|---|---|
| 1 | `AGENTS.md` | Quy tắc làm việc, ranh giới an toàn, bảng phân loại đối tượng đọc |
| 2 | File này | Trạng thái và việc đang mở |
| 3 | `STATUS.md` | Nhật ký theo phiên, chi tiết hơn |
| 4 | `DECISIONS.md` | 57 quyết định — tra khi không hiểu vì sao làm vậy |
| 5 | `PROJECT.md` | Cây thư mục chuẩn, hợp đồng artifact |

---

## 2. Kiến trúc nội dung — hiểu sai chỗ này là làm hỏng việc

Nội dung đi theo **ba tầng**, tách theo **đối tượng đọc** (DEC-053):

```
docs KB/Dev/      25 file · cơ chế, kết quả kiểm chứng, cấu hình
                  → cho Dev và Agent config. KHÔNG lên Web.

docs KB/Human/    29 file · hướng dẫn thao tác
                  → NGUỒN BUILD. Sửa nội dung ở đây.

knowledge/<KB>/   bản sinh bởi build_handbook.py
                  → lên Web. KHÔNG sửa tay, sẽ bị ghi đè.
```

**Quy ước tiền tố tên file** trong `docs KB/`, builder tự đổi sang `doc-` khi sinh (giữ DEC-042 vì regex đồng bộ khoá `^(doc|image)-`):

| Tiền tố nguồn | Dải số | Đổ về KB |
|---|---|---|
| `KB-NN-*` | 00–12 | `GS9 Knowledge VNG AI` |
| `Agent-NN-*` | 13–19 | `GS9 Knowledge VNG AI` |
| `AgentCFL-NN-*` | 00–05 | `GS9 CFL Knowledge Agent` |
| `KBCFL-NN-*` | 10–12 | `GS9 CFL Knowledge Agent` |

Thêm tính năng mới thì thêm tiền tố vào `HUMAN_SOURCE_PREFIXES` hoặc `SIMPLE_KB_TARGETS` trong `scripts/build_handbook.py` — **không tạo thư mục con**.

**Quy tắc phân loại một câu:** câu hỏi người dùng cuối đặt ra khi đang chat → Human. Câu hỏi chỉ người sửa hệ thống mới cần → Dev. Mã `DEC-xxx`, link `audit/`, cụm "đã/chưa kiểm chứng" **không được** xuất hiện trong `docs KB/Human` và `knowledge/`.

---

## 3. Trạng thái hai KB chính

| KB | Local | Web | Ghi chú |
|---|---|---|---|
| `GS9 Knowledge VNG AI` | 20 doc + 49 ảnh | **69 tài liệu, đã sync** | Chat-test ảnh ĐẠT |
| `GS9 CFL Knowledge Agent` | 8 doc | **0 tài liệu — chưa sync** | Việc mở số 1 |

`GS9 CFL Plan Version`: 12 doc + 29 ảnh, URI đã vá xong, **chưa up bản mới lên Web**.

---

## 4. Việc đang mở

### 4.1 Sync 2 KB lên Web — làm ngay
1. `knowledge/GS9 CFL Knowledge Agent` (8 file) — KB trên Web đang **trống**
2. `knowledge/GS9 CFL Plan Version/V5` (12 file `.md`) — URI ảnh đã vá, cần up lại

### 4.2 Chat-test luật trích dẫn ảnh của Agent
Đã chèn luật vào System Prompt của 10/10 Agent custom (DEC-056) nhưng **chưa test**. Nên thử `GS9 CFL Knowledge Curator` vì nó gắn `GS9 Knowledge VNG AI` (KB có ảnh). Hỏi câu buộc trả lời kèm hình, xem Agent có phát ra `![...](minio://...)` không.

### 4.3 Bốn Agent chưa gắn KB
`CS Copilot`, `Economy Offer Analyst`, `GM Policy Advisor`, `Player Communications` — `kb_selection_mode: none`. Luật trích dẫn ảnh đã dán nhưng vô tác dụng vì không có nguồn.

### 4.4 Gate chất lượng chưa chạy
**Chưa Agent nào chat-test đạt.** Toàn bộ 16 Agent vẫn ở mức *Bị chặn–Chưa xác định* về chất lượng runtime.

### 4.5 Chưa kiểm chứng
- Converter Plan V5 chạy với bố cục ảnh phẳng mới (DEC-054) — 6 test luôn skip vì HTML nguồn chỉ có trên máy công ty
- Hành vi connector khi **đổi tên / di chuyển / xoá** tệp

---

## 5. Cạm bẫy đã gặp thật

**Google Drive khoá file.** Project nằm trên Drive nên file hay bị khoá ngay sau khi ghi. Dấu hiệu: `Invalid request code` / `OSError: Errno 22` / `Incorrect function`, và `stat` cho `Links: 0`. Không tool nào của agent vượt qua được — chỉ File Explorer ép tải về được.
→ **Ghi file qua file tạm rồi `os.replace`.** Ghi đè trực tiếp đã từng làm **mất sạch nội dung một file nguồn** (16/08).

**URI ảnh chết sau khi re-sync.** Nạp lại ảnh qua connector là URI cũ chết toàn bộ. Lấy lại hàng loạt bằng trường `file_path` của API, đừng lấy URI trong `description` (chỉ 24/49 ảnh có, nhiều ảnh lại có 2 URI khó chọn).

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. Với KB chưa share (ví dụ `GS9 CFL Plan Version`), lấy token qua `/api/auth/token?sub_app=kb` rồi gọi `https://miniapp.vnggames.ai/kb/v1/api/...` kèm `Authorization: Bearer` — gọi bằng cookie bị CORS chặn.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun. Tool đọc trang thường không thấy nội dung; phải qua `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. Dialog cấu hình Agent thì lại render ở document chính.

**Ảnh render 2 lần trong chat.** Nền tảng tự render khi gặp `minio://` mà không đợi markdown khép kín → ảnh hiện 2 lần kèm ký tự `![`, `](`, `)` lộ ra. **Lỗi nền tảng, không phải lỗi tài liệu.**

---

## 6. Lệnh chuẩn

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

**Gate:** strict build ra 20 module + 8 doc KB Agent, 60 link MinIO, HTML offline tự chứa, `Ran 30 tests`/`OK`. Không dùng `--allow-missing-minio` cho bản bàn giao.

---

## 7. An toàn

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che (vá 16/08 — trước đó **không** được che).
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. Đã đổi tên file theo quy ước (DEC-055) nhưng **không mở, không đọc nội dung**.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` từng bị đánh giá rủi ro, nay **người dùng xác nhận giữ nguyên** vì nền tảng chỉ dùng nội bộ.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → mọi cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại trước khi kết luận.

---

## 8. Tài liệu thuyết trình

`gioi-thieu-knowledge-base-va-agent.html` — bản giới thiệu cho team, 10 phần: vấn đề, KB là gì, Agent là gì, cách phối hợp, quy trình 6 bước, 10 kho của CFL, 16 trợ lý, bảng binding, nguyên tắc an toàn, trạng thái. Tự chứa, mở bằng trình duyệt, in PDF được.

**Số liệu trong đó là ảnh chụp 16/08/2026** — nếu binding hay danh sách KB đổi thì phải cập nhật lại file này.
