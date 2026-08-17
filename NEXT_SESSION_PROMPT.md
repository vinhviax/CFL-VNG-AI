Bạn đang tiếp quản dự án **Knowledge Base VNG**. Root project là folder `Knowledge Base VNG` nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), team GS9 dùng.

Hiện có **10 kho tri thức** và **16 trợ lý** (6 mặc định của nền tảng + 10 custom cho LiveOps). Cả 2 KB chính đã sync lên Web và có ảnh minh họa hoạt động.

Có file thuyết trình sẵn: `gioi-thieu-knowledge-base-va-agent.html` (10 phần, có ảnh chụp màn hình nhúng sẵn, mở bằng trình duyệt).

==================================================
1. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`.

HEAD phải là `4bbdbb0 docs: khôi phục sau sự cố Google Drive, thêm ảnh minh họa, ghi DEC-058/059` (đã push GitHub). Nếu working tree sạch thì phiên trước kết thúc gọn.

**Luôn xác nhận local khớp remote trước khi tin `git status`:**
```powershell
git fetch origin
git diff --stat origin/main HEAD
```
Phải rỗng tuyệt đối. Nếu KHÔNG rỗng — có thể Drive lại gây sự cố như 17/08 (xem mục 5).

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` → `STATUS.md`. `DECISIONS.md` (59 quyết định) tra khi cần hiểu vì sao.

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
3. TRẠNG THÁI HAI KB CHÍNH — ĐÃ SYNC XONG
==================================================

| KB | Local | Web | Ghi chú |
|---|---|---|---|
| `GS9 Knowledge VNG AI` | 20 doc + 49 ảnh | Đã sync | Chat-test ảnh ĐẠT |
| `GS9 CFL Knowledge Agent` | 8 doc | Đã sync (17/08) | Có bảng ai gắn kho nào |

`GS9 CFL Plan Version`: 12 doc + 29 ảnh, đã up bản mới lên Web (17/08).

==================================================
4. VIỆC ĐANG MỞ
==================================================

**4.1 Bốn Agent chưa gắn KB**
`CS Copilot`, `Economy Offer Analyst`, `GM Policy Advisor`, `Player Communications` — `kb_selection_mode: none`. Luật trích dẫn ảnh đã dán (DEC-056) nhưng vô tác dụng vì không có nguồn. Xem DEC-058 và bảng trong `AgentCFL-02-ma-tran-so-sanh-16-agent.md`.

**4.2 Gate chất lượng chưa chạy đầy đủ**
Chưa Agent nào chat-test đạt theo nghĩa đầy đủ (bộ câu hỏi mẫu, xác nhận nguồn, không lộ PII). Toàn bộ 16 Agent vẫn ở mức *Bị chặn–Chưa xác định* về chất lượng runtime.

**4.3 Chưa kiểm chứng**
- Converter Plan V5 với bố cục ảnh phẳng mới (DEC-054) — 6 test luôn skip vì HTML nguồn chỉ có trên máy công ty
- Hành vi connector khi đổi tên / di chuyển / xoá tệp
- Ảnh render 2 lần trong chat (lỗi nền tảng, xem mục 5) — chưa báo cho ai chịu trách nhiệm

==================================================
5. CẠM BẪY ĐÃ GẶP THẬT — ĐỌC KỸ, ĐẶC BIỆT MỤC ĐẦU
==================================================

**Google Drive mất kết nối rồi tự "Restore" ra layout cũ (DEC-059, sự cố 17/08/2026 — nghiêm trọng nhất từng gặp).** Drive rớt mount, rồi tự phục hồi nhưng trộn cấu trúc cũ (trước 15/08) chồng lên cấu trúc mới: thư mục `knowledge` thật bị đẩy thành `knowledge (1)`, `.git` mất lịch sử, hàng trăm file lệch nội dung, hàng chục thư mục rác chui vào.

Nếu tái diễn, làm theo đúng trình tự này:
1. **Không sửa gì trên Drive trước khi biết rõ.** Clone bản sạch từ GitHub ra một thư mục NGOÀI Drive để đối chiếu trước.
2. Nếu thấy thư mục thật bị đổi tên thành `<tên> (1)` — **đổi tên lại về đúng**, KHÔNG xoá rồi tạo mới (xoá-tạo-mới làm đứt kết nối Google Drive connector vì đổi ID; đổi tên thì giữ nguyên ID, an toàn).
3. Thay `.git` hỏng bằng bản sạch từ clone (`cp -r <clone>/.git .git`).
4. `git restore .` để đưa toàn bộ file tracked về đúng commit.
5. `git clean -f <thư_mục>/` để dọn file rác không được git theo dõi — nhưng **để ý `desktop.ini` nằm trong `.gitignore` nên `git clean -f` mặc định bỏ qua nó**, phải tự rà thêm bằng tay hoặc dùng `git clean -fx`.
6. Rà thủ công toàn cây thư mục tìm dấu hiệu Drive-duplicate: tên có `(1)`, `(2)`, `Copy of`, hoặc thư mục chỉ chứa mỗi `desktop.ini`.
7. **Xác nhận cuối bằng `git diff --stat origin/main HEAD` phải rỗng tuyệt đối** — không chỉ tin `git status` (nó có thể trống oan nếu `.git` đã bị thay bằng bản khác nhưng chưa fetch lại).

**Google Drive khoá file khi ghi.** File hay bị khoá ngay sau khi ghi. Dấu hiệu: `Invalid request code` (Bash) / `OSError: Errno 22` (Python) / `Incorrect function` (PowerShell), `stat` cho `Links: 0`. Không tool nào của agent vượt qua được — chỉ File Explorer ép tải về được.
→ **Ghi file qua file tạm rồi `os.replace`.** Ghi đè trực tiếp đã từng làm MẤT SẠCH nội dung một file nguồn (16/08).

**URI ảnh chết sau khi re-sync.** Nạp lại ảnh qua Google Drive connector là URI cũ chết toàn bộ. Lấy lại hàng loạt bằng trường `file_path` của API, ĐỪNG lấy URI trong `description` (chỉ 24/49 ảnh có, nhiều ảnh lại có 2 URI khó chọn). Dạng `file_path` (`minio://.../10012/<knowledge_id>/<uuid>.png`) đã kiểm chứng render đúng — DEC-052.

**MCP không thấy mọi KB.** `list_knowledge_bases` chỉ trả KB đã share vào space. Với KB chưa share, lấy token qua `/api/auth/token?sub_app=kb` rồi gọi `https://miniapp.vnggames.ai/kb/v1/api/...` kèm header `Authorization: Bearer` — gọi bằng cookie bị CORS chặn. `GET /kb/v1/api/agents` (trường `config.knowledge_bases`) dùng để lấy binding KB thật của Agent.

**Trang web dùng shadow DOM.** App KB chạy trong micro-frontend qiankun. Tool đọc trang thường KHÔNG thấy nội dung; phải qua `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`. Dialog cấu hình Agent lại render ở document chính. URL mở KB cần `?tenant_id=10012`.

**Ảnh render 2 lần trong chat.** Nền tảng tự render khi gặp `minio://` mà không đợi markdown khép kín → ảnh hiện 2 lần kèm ký tự `![`, `](`, `)` lộ ra. Lỗi nền tảng, KHÔNG phải lỗi tài liệu, đừng sửa nội dung.

**Trình duyệt in-app chưa đăng nhập.** Muốn thao tác trên `vnggames.ai` phải dùng `claude-in-chrome` (Chrome thật của người dùng, có sẵn session). Agent không được tự đăng nhập.

==================================================
6. LỆNH CHUẨN VÀ GATE
==================================================

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
python scripts\link_plan_v5_minio.py --check
```

Gate: strict build ra 20 module + 8 doc KB Agent, 60 link MinIO, HTML offline tự chứa, `Ran 30 tests`/`OK` (6 skip do thiếu HTML nguồn Plan V5). Không dùng `--allow-missing-minio` cho bản bàn giao.

==================================================
7. AN TOÀN
==================================================

- Không commit credential. `keys KB/` và `**/keys/` đã được `.gitignore` che.
- `GS9 CFL Item Profile` chứa dữ liệu người chơi. Đã đổi tên file theo quy ước (DEC-055) nhưng KHÔNG mở, KHÔNG đọc nội dung.
- Hai binding `Incident Triage → PUM` và `Player Voice Analyst → Sentiment Feedback User` từng bị đánh giá rủi ro, nay **người dùng xác nhận giữ nguyên** vì nền tảng chỉ dùng nội bộ (DEC-058). Đừng cảnh báo lại.
- Space `CFL Member` để quyền **Được chỉnh sửa** cho 6 người → mọi cấu hình Agent có thể bị người khác đổi bất cứ lúc nào. Đọc lại từ Web trước khi kết luận, đừng tin snapshot trong tài liệu.
- Không tự mutation live (đổi cấu hình Agent, xoá KB, share) nếu nhiệm vụ hiện tại chưa cho phép rõ.

==================================================
8. CÁCH LÀM VIỆC NGƯỜI DÙNG MONG MUỐN
==================================================

- **Trả lời ngắn gọn, đi thẳng vào việc.**
- Tài liệu trong `knowledge/` viết cho human đọc, không nhồi chi tiết kỹ thuật.
- Khi phát hiện điều gì mới: ghi vào `audit/` + `DECISIONS.md` + `docs KB/Dev`, rồi chỉ chắt phần "người dùng cần làm gì" sang `docs KB/Human`.
- Lấy trạng thái thật từ hệ thống (API/UI), đừng tin tài liệu cũ.
- Khi nghi ngờ có sự cố dữ liệu (mất file, Drive lỗi...) — kiểm chứng thật kỹ bằng nhiều lớp (git diff vs remote, đếm file, so nội dung), đừng chỉ báo cáo suông rồi kết luận vội. Người dùng đã nhắc thẳng: "tôi sợ nhiều khi bạn nhầm file cũ thành file mới rồi giữ lại file cũ xóa file mới".
