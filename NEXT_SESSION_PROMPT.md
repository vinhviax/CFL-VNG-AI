Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root project là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), team GS9 dùng.

Hiện có **10 kho tri thức** và **16 trợ lý** (6 mặc định của nền tảng + 10 custom cho LiveOps).

Hai KB chính do agent quản lý nội dung:
- `GS9 Knowledge VNG AI` — hướng dẫn dùng chính nền tảng VNG AI (20 doc + 49 ảnh)
- `GS9 CFL Knowledge Agent` — hướng dẫn về Agent và KB của riêng CFL (8 doc)

Tám KB còn lại là dữ liệu nghiệp vụ CFL (Plan Version, PUM, Data Daily, Item Profile, Kho Dữ Liệu Tổng Hợp, Glossary, CS FAQ, Sentiment).

==================================================
1. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`.

HEAD phải là `b79aed7 feat: tách nội dung theo đối tượng đọc, vá URI ảnh, cấu hình 10 Agent` (đã push lên GitHub). Nếu working tree sạch thì phiên trước đã kết thúc gọn.

Rồi đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` → `STATUS.md`. `DECISIONS.md` (57 quyết định) tra khi cần hiểu vì sao.

CẢNH BÁO ĐÃ TỪNG XẢY RA: nếu `git status` cho thấy TOÀN BỘ file tracked là `D` và mọi thứ hiện lại như `??` — đó là `.git/index` hỏng do Google Drive sync xen vào lúc git ghi `index.lock`. KHÔNG mất dữ liệu. Sửa:
```powershell
rm .git/index.lock    # nếu còn
git reset -q
git status --short --branch
```

==================================================
2. KIẾN TRÚC NỘI DUNG — HIỂU SAI CHỖ NÀY LÀ LÀM HỎNG VIỆC
==================================================

Nội dung đi theo BA TẦNG, tách theo ĐỐI TƯỢNG ĐỌC (DEC-053):

```
docs KB/Dev/      25 file · cơ chế, kết quả kiểm chứng, cấu hình
                  → cho Dev và Agent config. KHÔNG lên Web.

docs KB/Human/    29 file · hướng dẫn thao tác
                  → NGUỒN BUILD. Sửa nội dung ở đây.

knowledge/<KB>/   bản sinh bởi scripts/build_handbook.py
                  → lên Web. KHÔNG sửa tay, sẽ bị ghi đè.
```

Quy ước tiền tố tên file trong `docs KB/`, builder tự đổi sang `doc-` khi sinh (giữ DEC-042 vì regex đồng bộ khoá `^(doc|image)-`):

| Tiền tố nguồn | Dải số | Đổ về KB |
|---|---|---|
| `KB-NN-*` | 00–12 | `GS9 Knowledge VNG AI` |
| `Agent-NN-*` | 13–19 | `GS9 Knowledge VNG AI` |
| `AgentCFL-NN-*` | 00–05 | `GS9 CFL Knowledge Agent` |
| `KBCFL-NN-*` | 10–12 | `GS9 CFL Knowledge Agent` |

Thêm tính năng mới thì thêm tiền tố vào `HUMAN_SOURCE_PREFIXES` hoặc `SIMPLE_KB_TARGETS` trong `scripts/build_handbook.py` — KHÔNG tạo thư mục con.

**Quy tắc phân loại một câu:** câu hỏi người dùng cuối đặt ra khi đang chat → Human. Câu hỏi chỉ người sửa hệ thống mới cần → Dev. Mã `DEC-xxx`, link `audit/`, cụm "đã/chưa kiểm chứng", `Mức bằng chứng` KHÔNG được xuất hiện trong `docs KB/Human` và `knowledge/`.

Người dùng đã nói rõ: **sẽ còn đổi cấu trúc, nội dung, Agent và binding trong tương lai** — mỗi lần đổi phải giữ đúng ba tầng này.

==================================================
3. VIỆC ĐANG MỞ
==================================================

**3.1 Sync 2 KB lên Web — ưu tiên cao nhất**
- `knowledge/GS9 CFL Knowledge Agent` (8 file) — KB trên Web đang **0 tài liệu**
- `knowledge/GS9 CFL Plan Version/V5` (12 file `.md`) — URI ảnh đã vá, cần up lại

**3.2 Chat-test luật trích dẫn ảnh của Agent**
Đã chèn luật vào System Prompt 10/10 Agent custom (DEC-056) nhưng CHƯA test. Nên thử `GS9 CFL Knowledge Curator` vì nó gắn `GS9 Knowledge VNG AI` (KB có ảnh). Hỏi câu buộc trả lời kèm hình, xem Agent có phát ra `![...](minio://...)` không.

**3.3 Bốn Agent chưa gắn KB**
`CS Copilot`, `Economy Offer Analyst`, `GM Policy Advisor`, `Player Communications` — `kb_selection_mode: none`, câu trả lời không có nguồn CFL nào bảo chứng.

**3.4 Gate chất lượng chưa chạy**
Chưa Agent nào chat-test đạt. Toàn bộ 16 Agent vẫn ở mức *Bị chặn–Chưa xác định* về chất lượng runtime.

**3.5 Chưa kiểm chứng**
- Converter Plan V5 với bố cục ảnh phẳng mới (DEC-054) — 6 test luôn skip vì HTML nguồn chỉ có trên máy công ty
- Hành vi connector khi đổi tên / di chuyển / xoá tệp

==================================================
4. CẠM BẪY ĐÃ GẶP THẬT — ĐỌC KỸ
==================================================

**Google Drive khoá file.** Project nằm trên Drive nên file hay bị khoá ngay sau khi ghi. Dấu hiệu: `Invalid request code` (Bash) / `OSError: Errno 22` (Python) / `Incorrect function` (PowerShell), và `stat` cho `Links: 0`. Không tool nào của agent vượt qua được — chỉ File Explorer ép tải về được.
→ **Ghi file qua file tạm rồi `os.replace`.** Ghi đè trực tiếp đã từng làm MẤT SẠCH nội dung một file nguồn (16/08). Khôi phục được nhờ bản đã build trong `knowledge/`.

**URI ảnh chết sau khi re-sync.** Nạp lại ảnh qua Google Drive connector là URI cũ chết toàn bộ. Lấy lại hàng loạt bằng trường `file_path` của API, ĐỪNG lấy URI trong `description` (chỉ 24/49 ảnh có, nhiều ảnh lại có 2 URI khó chọn). Dạng `file_path` (`minio://.../10012/<knowledge_id>/<uuid>.png`) đã kiểm chứng render đúng — DEC-052.

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. Với KB chưa share (ví dụ `GS9 CFL Plan Version`), lấy token qua `/api/auth/token?sub_app=kb` rồi gọi `https://miniapp.vnggames.ai/kb/v1/api/...` kèm header `Authorization: Bearer` — gọi bằng cookie bị CORS chặn.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun. Tool đọc trang thường KHÔNG thấy nội dung; phải qua `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. Riêng dialog cấu hình Agent lại render ở document chính. URL mở KB cần `?tenant_id=10012`, thiếu là ra trang lỗi.

**Ảnh render 2 lần trong chat.** Nền tảng tự render khi gặp `minio://` mà không đợi markdown khép kín → ảnh hiện 2 lần kèm ký tự `![`, `](`, `)` lộ ra. Lỗi nền tảng, KHÔNG phải lỗi tài liệu, đừng sửa nội dung.

**Trình duyệt in-app chưa đăng nhập.** Muốn thao tác trên `vnggames.ai` phải dùng `claude-in-chrome` (Chrome thật của người dùng, có sẵn session). Agent không được tự đăng nhập.

==================================================
5. LỆNH CHUẨN VÀ GATE
==================================================

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

Gate: strict build ra 20 module + 8 doc KB Agent, 60 link MinIO, HTML offline tự chứa, `Ran 30 tests`/`OK` (6 skip do thiếu HTML nguồn Plan V5). Không dùng `--allow-missing-minio` cho bản bàn giao.

==================================================
6. AN TOÀN
==================================================

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che (vá 16/08 — trước đó KHÔNG được che, một lệnh `git add -A` là lọt service-account key).
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. Đã đổi tên file theo quy ước (DEC-055) nhưng KHÔNG mở, KHÔNG đọc nội dung.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` từng bị đánh giá rủi ro, nay **người dùng xác nhận giữ nguyên** vì nền tảng chỉ dùng nội bộ. Đừng cảnh báo lại.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → mọi cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại từ Web trước khi kết luận, đừng tin snapshot trong tài liệu.
- Không tự mutation live (đổi cấu hình Agent, xoá KB, share) nếu nhiệm vụ hiện tại chưa cho phép rõ.

==================================================
7. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- **Trả lời ngắn gọn.** Người dùng đã nhắc: nói dài quá khó hiểu. Đi thẳng vào việc.
- Tài liệu trong `knowledge/` viết cho human đọc, không nhồi chi tiết kỹ thuật.
- Khi phát hiện điều gì mới: ghi vào `audit/` + `DECISIONS.md` + `docs KB/Dev`, rồi chỉ chắt phần "người dùng cần làm gì" sang `docs KB/Human`.
- Lấy trạng thái thật từ hệ thống (API/UI), đừng tin tài liệu cũ — đã có nhiều lần tài liệu ghi sai so với thực tế.

==================================================
8. TÀI LIỆU THUYẾT TRÌNH
==================================================

`gioi-thieu-knowledge-base-va-agent.html` — bản giới thiệu cho team, 10 phần: vấn đề, KB là gì, Agent là gì, cách phối hợp, quy trình 6 bước, 10 kho của CFL, 16 trợ lý, bảng binding, nguyên tắc an toàn, trạng thái. Tự chứa, mở bằng trình duyệt, in PDF được.

Số liệu trong đó là ảnh chụp 16/08/2026 — nếu binding hay danh sách KB đổi thì phải cập nhật lại file này.
