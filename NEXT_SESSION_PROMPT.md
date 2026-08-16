# Prompt phiên tiếp theo — cập nhật 15/08/2026 (phiên 2 kết thúc, đang chờ kết quả test đồng bộ tăng dần)

Copy toàn bộ khối dưới đây vào phiên agent mới:

```text
Bạn đang tiếp quản dự án Knowledge Base VNG. Root project là folder `Knowledge Base VNG`, nằm trong `\My Drive\CFL\VNG AI\` (ổ đĩa tùy máy: `J:` ở máy công ty, `G:` ở máy nhà).

LƯU Ý: `VNG AI` là workspace chung, về sau chứa thêm project khác. Root của project này luôn là `VNG AI\Knowledge Base VNG`. Xác nhận bằng `git rev-parse --show-toplevel`. KHÔNG đọc/sửa các folder anh em nằm cạnh nó.

QUAN TRỌNG: Prompt này cung cấp bối cảnh, KHÔNG tự cấp quyền mutation. Việc đầu tiên của phiên này là ĐỌC và XÁC NHẬN trạng thái — vẫn hỏi người dùng trước khi làm gì tiếp.

==================================================
0. DỰ ÁN NÀY LÀ GÌ — TÓM TẮT 30 GIÂY
==================================================

Xây và vận hành Knowledge Base + Agent trên nền tảng VNG AI (`vnggames.ai`, tenant `10012`) cho nghiệp vụ LiveOps game CrossFire Legends (CFL/CFM VN), do team GS9 dùng.

Ba mảng:
1. **Bộ sổ tay v3.3.0** — 20 Markdown hướng dẫn dùng chính nền tảng VNG AI, tên `doc-00`→`doc-19`, đã gộp chung thư mục với 49 ảnh `image-01`→`image-49`.
2. **10 custom Agent LiveOps** — tên đã đổi `GS9 CFL ...`, đã share space `CFL Member` quyền Chỉnh sửa, 6 đã bind KB, chưa Agent nào chat-test đạt.
3. **Quy hoạch kiến trúc KB 7 tầng** — bản đồ đã chốt 15/08; đang thực thi tái cấu trúc tên/KB theo kế hoạch.

**PHIÊN TRƯỚC (phiên 2, 15/08) ĐÃ LÀM XONG:** Phase 1+2 của kế hoạch tái cấu trúc (đổi tên toàn bộ + gộp KB nền tảng), đổi tên 10 custom Agent, xác minh Web actual toàn bộ Agent, và đang chạy dở một thử nghiệm quan trọng về hành vi đồng bộ Google Drive (mục 1 dưới đây) — **đây là việc ưu tiên số 1 của phiên này.**

==================================================
1. VIỆC ƯU TIÊN SỐ 1 — TEST ĐỒNG BỘ TĂNG DẦN, ĐANG CHỜ KẾT QUẢ VÒNG 2
==================================================

Đọc kỹ: `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md` trước khi làm gì khác.

**Câu hỏi cần trả lời:** gộp ảnh + tài liệu chung một KB (đã chọn, DEC-043) có an toàn khi một tài liệu khác trong cùng KB được sửa nội dung và sync tăng dần hay không? Kết quả quyết định GIỮ hay HOÀN TÁC kiến trúc gộp — ảnh hưởng trực tiếp `GS9 Knowledge VNG AI` (đã gộp 49 ảnh + 20 module) và toàn bộ cách làm Phase 3 sau này.

**Đã làm (vòng 1 — sync Toàn bộ):**
- Tạo KB test `Test` (`d7295a59-03b1-496c-86eb-9ecaa3364aa7`) với 4 file: `C.png`, `D.png`, `a.md` (gắn ảnh C), `b.md` (gắn ảnh D).
- Sync lần 1: Toàn bộ + Ghi đè + Mọi tệp → cả 4 `Hoàn tất`.
- **Phát hiện quan trọng:** Google Drive connector KHÔNG tự resolve link ảnh tương đối trong Markdown khi sync. Người dùng phải tự lấy URI MinIO qua UI và nhúng tay vào file — giống hệt quy trình thủ công cũ (`link_plan_v5_minio.py`), connector không tự làm thay.
- Đã ghi `knowledge_id` (ID tài liệu nội bộ) của cả 4 file làm mốc so sánh — xem bảng trong file audit trên.
- Người dùng đã tự nhúng URI MinIO thật vào `a.md` (ảnh C) và `b.md` (ảnh D).
- Agent đã sửa văn xuôi: `a.md` = nhóm ĐỐI CHỨNG (không sửa gì nữa), `b.md` = nhóm THỬ NGHIỆM (sửa nội dung quanh ảnh, không đụng dòng ảnh).

**Đang chờ (vòng 2 — sync Tăng dần):** người dùng sẽ chuyển "Chế độ đồng bộ" sang Tăng dần và sync lại (có thể đã làm xong khi bạn đọc prompt này — HỎI NGƯỜI DÙNG TRẠNG THÁI HIỆN TẠI TRƯỚC). Khi có kết quả:
1. Mở lại 4 tài liệu trong KB `Test`, so `knowledge_id` với mốc đã ghi trong file audit — đổi hay giữ nguyên.
2. Ảnh C (`a.md`, không sửa) và ảnh D (`b.md`, có sửa nội dung quanh) còn hiển thị đúng không.
3. `e.md` (nếu người dùng đã thêm) có xuất hiện với ID mới.
4. **Ghi kết luận thành DEC mới.** Nếu ảnh mất/đổi khi tài liệu khác trong KB được sync lại (dù không đụng dòng ảnh) → phải bàn lại việc tách ảnh ra KB riêng, ảnh hưởng `GS9 Knowledge VNG AI`. Nếu ảnh vẫn ổn → DEC-043 được xác nhận đúng bằng thực nghiệm.
5. Cập nhật `docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` phần Phase 3 theo kết quả.

==================================================
2. VIỆC PHẢI LÀM ĐẦU TIÊN
==================================================

Read-only: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`.

HEAD vẫn là `a2285e6 docs: record GitHub handoff` — CHƯA commit gì từ phiên 1 hoặc phiên 2. Toàn bộ là file local (rất nhiều: đổi tên ~150 file + nội dung mới).

CẢNH BÁO ĐÃ TỪNG XẢY RA: nếu `git status` cho thấy TOÀN BỘ file tracked staged là `D` VÀ mọi thứ hiện lại như `??` — đó là `.git/index` hỏng do Google Drive sync xen vào lúc git ghi `index.lock`. KHÔNG mất dữ liệu. Sửa:
```powershell
rm .git/index.lock    # nếu còn
git reset -q
git status --short --branch
```
Không dùng `git checkout --`, `git clean`, `git add .`.

Đọc theo thứ tự: AGENTS.md → HANDOFF.md → STATUS.md → PROJECT.md → DECISIONS.md (đặc biệt DEC-041→050, tất cả thêm ngày 15/08 phiên 2).
Rồi đọc: `audit/google-drive-incremental-sync-test-2026-08-15-baseline.md` (việc ưu tiên số 1, xem mục 1).

Phản hồi đầu tiên: xác nhận root, đã đọc governance, trạng thái Git thật, và hỏi người dùng đã sync vòng 2 (Tăng dần) chưa.

==================================================
3. GATE VÀ LỆNH CHUẨN
==================================================

29 test, ba nhóm — KHÔNG đổi từ phiên trước:
- `tests/test_build_handbook.py` — 16 test, gate sổ tay (đã cập nhật cho tên `doc-`/`image-` gộp)
- `tests/test_convert_cfl_plan_html.py` — 6 test, converter Plan V5 (skip trên máy nhà, thiếu source HTML)
- `tests/test_link_plan_v5_minio.py` — 7 test, script gắn URI

```powershell
python -m unittest discover -s tests -v
python scripts\build_handbook.py          # strict build 20 module + HTML offline
```
Không dùng `--allow-missing-minio` cho bản bàn giao. Nếu thiếu package: `pip install markdown beautifulsoup4` (đã cài ở máy này, có thể không cần lại).

==================================================
4. HẠ TẦNG TRÊN WEB — SỐ LIỆU THẬT SAU PHIÊN 2
==================================================

Tenant `10012`. **QUAN TRỌNG: tên KB local đã đổi ở phiên 2, và một số KB đã có bằng chứng người dùng tự sync qua Google Drive connector (Phase 3 thật đã bắt đầu ngoài ý muốn ban đầu — CẦN HỎI LẠI người dùng xem đã chủ động làm Phase 3 cho bao nhiêu KB).**

| KB (tên Web) | ID | Số tài liệu Web (đã quan sát 15/08) | Ghi chú |
|---|---|---|---|
| GS9 Knowledge VNG AI | cefadf09-4187-46ac-a765-591e3255a4a4 | **69** — khớp local (20 doc + 49 image gộp) | Có bằng chứng đã Phase 3 sync |
| GS9 Knowledge VNG - Image Assets | 6da8657c-dd96-4170-a698-074043475014 | 49 PNG (chưa xác minh lại phiên này) | Còn tồn tại riêng trên Web, chưa xóa (đúng theo DEC-005) |
| GS9 CFL Knowledge Agent | 1d92448f-7ee2-46c4-b202-5efbe9cc5616 | **28** — khớp local (25 cũ + 3 file mới `doc-30/31/32`) | Đã sync qua Drive, tên `doc-NN-...` đúng |
| GS9 CFL Plan Version | 1452bc9a-c8b4-487b-b623-34e0b00a83e9 | **41** — khớp local (12 doc-v5 + 29 image-v5) | Có bằng chứng đã Phase 3 sync |
| GS9 CFL Kho Dữ Liệu Tổng Hợp | 574d4d12-8421-4e6f-9628-d03f4f7fb475 | 97 (tăng từ 16) | Người dùng đang tự gom thêm — hỏi lại phạm vi |
| GS9 CFL Data Daily | 7be35c7c-c1fc-4538-bb1c-470f18378ae9 | 8, tên `doc-CFL_MMYYYY.xlsx` | Đã đổi tên local phiên 2, thiếu `doc-CFL_082026.xlsx` (G4 cũ) |
| GS9 CFL PUM | 90484cd2-93fa-4d45-a37f-43c0d50430f2 | 7, tên `doc-CFL MMR GMT ...pdf` | Đã đổi tên local phiên 2 |
| GS9 CFL Item Profile | e99b635f-04ec-44ad-9bcc-f12cae587c7d | 10 | **P0 CÁCH LY — KHÔNG đổi tên, KHÔNG đụng** |
| GS9 CFL Sentiment Feedback User | (xem KB list) | 1 | Đã đổi tên local `doc-Feedback User Sentiment SS4.xlsx` |
| GS9 CFL Glossary & Systems | (xem KB list) | 3, trạng thái **"ĐANG TEST"** trên Web | Người dùng có vẻ đang thử publish — hỏi lại |
| GS9 CFL CS FAQ & Policy | (xem KB list) | 1, trạng thái **"ĐANG TEST"** trên Web | Người dùng có vẻ đang thử publish — hỏi lại |
| **Test** (mới, chỉ để thử nghiệm) | **d7295a59-03b1-496c-86eb-9ecaa3364aa7** | 4 (`a.md`, `b.md`, `C.png`, `D.png`) | Xem mục 1 — KB test đồng bộ, KHÔNG phải KB nghiệp vụ thật |
| GS9 test knowledge base | 6f887ec5-dab1-4505-999f-fb99c2280da9 | 0, người khác sở hữu | Không liên quan |

Ràng buộc nền tảng đã kiểm chứng (không đổi):
- Share CHỈ ở cấp KB → KB = đơn vị phân quyền
- Agent bind CẢ KB → KB = đơn vị phạm vi truy hồi
- KHÔNG có TTL/expiry → KB = đơn vị vòng đời
- `Loại` (Tài liệu/FAQ) và `Chiến lược lập chỉ mục` **KHOÁ sau khi KB có nội dung**
- Mode `Trả lời nhanh` không có tab Công cụ, không có control `Loại trợ lý` (vẫn RAG được)
- Tool truy hồi khoá khi Agent chưa bind KB → bind trước, bật tool sau
- **MỚI phiên 2:** Google Drive connector KHÔNG tự resolve link ảnh tương đối trong Markdown khi sync — vẫn cần lấy URI + nhúng tay.
- Chế độ đồng bộ Drive: `Toàn bộ` (liệt kê lại hết mỗi lần) vs `Tăng dần` (chỉ lấy mục đổi từ lần trước, qua cursor connector) — hành vi thật của Tăng dần đang được test (mục 1).
- Xung đột: `Ghi đè` vs `Bỏ qua nếu đã có`. Phạm vi tệp trong thư mục: `Mọi tệp` vs `Chỉ tệp mới nhất` (cẩn thận với KB nhiều file theo tháng như PUM/Data Daily — luôn chọn `Mọi tệp`).

==================================================
5. CÚ PHÁP NHÚNG ẢNH — ĐÃ CHỐT, ĐỪNG ĐIỀU TRA LẠI
==================================================

CÚ PHÁP CHUẨN, GIỮ NGUYÊN:
```markdown
<!-- LOCAL_ASSET: <đường dẫn cục bộ tới file ảnh> -->
![Mô tả cụ thể của ảnh](minio://knowledge-base-prd/10012/exports/<uuid>.<ext>)
```
- `LOCAL_ASSET` là comment, không render trên Web.
- `minio://.../exports/<uuid>.<ext>` mới là thứ Web đọc.
- Phần trong `![...]` là mô tả nội dung, KHÔNG phải tên file, KHÔNG phải URI.

TUYỆT ĐỐI KHÔNG: sửa cú pháp ảnh trong `build_handbook.py`/`convert_cfl_plan_html.py`/`link_plan_v5_minio.py`; điều tra lại nguyên nhân duplicate (đã kết luận là hành vi model, không phải lỗi cú pháp). Bằng chứng: `audit/cfl-plan-v5-chat-image-double-render-2026-08-15.md`.

**MỚI phiên 2 — phát hiện về ảnh đa-URI:** một ảnh có thể sinh NHIỀU URI khi qua parser (`C.png` trong KB test sinh 2 URI: 1 `.png` + 1 `.jpg`). Đây là hiện tượng đã biết từ Plan V5 ("MinerU tách ảnh con"). Quy tắc chọn vẫn là: URI đầu tiên xuất hiện / khớp đúng định dạng gốc = ảnh thật.

==================================================
6. KẾ HOẠCH TÁI CẤU TRÚC — PHASE 1+2 ĐÃ XONG, PHASE 3 ĐANG DỞ
==================================================

`docs/superpowers/plans/2026-08-15-kb-restructure-and-naming.md` — đọc lại nếu cần chi tiết kỹ thuật.

**Phase 1 (đổi tên) + Phase 2 (gộp KB + soạn nội dung mới): ĐÃ XONG, đã qua hash-check bảo toàn nội dung.**
- Quy ước đã CHỐT (không phải hỏi lại): `doc-`/`image-` cho tài liệu thường; `doc-v5-`/`image-v5-` cho Plan Version (chống trùng khi V6 lên).
- `GS9 Knowledge VNG AI` local đã gộp 20 module (`doc-00`→`doc-19`) + 49 ảnh (`image-01`→`image-49`) vào MỘT thư mục. `build_handbook.py` đã sửa (`local_asset_prefix = "."`, bỏ `ASSET_KB_NAME`).
- `GS9 CFL Knowledge Agent` local có 28 file: 25 cũ đổi tên `doc-` + 3 file MỚI đã soạn (`doc-30-cau-truc-kb-cfl.md`, `doc-31-ban-chat-tung-kb.md`, `doc-32-quy-uoc-dat-ten-va-nhung-anh.md`).
- Plan V5: 12 Markdown + 29 JPEG đã đổi tên `doc-v5-`/`image-v5-`. `convert_cfl_plan_html.py` đã sửa (`VERSION_TAG = "v5"`) cho lần sinh sau (cần source HTML, chỉ có ở máy công ty).
- **NỢ CHƯA XONG:** 4 file trong meta-KB (`doc-00`, `doc-01`, `doc-02`, `doc-26`) còn link chết trỏ tên cũ `27-custom-gs9-gm-case-investigator.md` — chưa sửa vì cần đổi nhãn hiển thị (nội dung), ngoài phạm vi việc đổi tên. Cần giao riêng nếu muốn sửa.
- 5 KB khác ngoài kế hoạch gốc cũng đã đổi tên `doc-` theo yêu cầu người dùng (DEC-047): `GS9 CFL PUM`, `GS9 CFL Data Daily`, `GS9 CFL Sentiment Feedback User`, `GS9 CFL Glossary & Systems`, `GS9 CFL CS FAQ & Policy`. `GS9 CFL Item Profile` loại trừ hoàn toàn (P0).

**Phase 3 (Google Drive connector sync lên Web):** kế hoạch gốc nói "agent chưa làm, cần go-ahead" — nhưng **bằng chứng cho thấy người dùng đã tự làm việc này ngoài lề cho ít nhất 3 KB** (số liệu Web khớp local ở mục 4). Cần hỏi lại người dùng phạm vi đã sync thật, và xem việc test đồng bộ tăng dần (mục 1) ảnh hưởng gì tới các KB đã sync đó (đặc biệt `GS9 Knowledge VNG AI` — đã gộp ảnh, đúng kịch bản đang test).

==================================================
7. BẢN ĐỒ KIẾN TRÚC KB 7 TẦNG
==================================================

`docs/superpowers/specs/2026-08-15-kb-architecture-design.md` — nguồn chuẩn cho việc bind Agent. Thay vai trò của `agent/kb-allowlist-proposal-2026-08-14.md` (giữ làm bằng chứng lịch sử, KHÔNG xóa).

Bảy tầng: L0 Nền tảng & Meta · L1 Canon · L2 Kế hoạch · L3 Vận hành · L4 Kết quả · L5 Tiếng nói người chơi · L6 Dịch vụ · L7 Cách ly.
Nguyên tắc: ranh giới KB vẽ theo (mức nhạy cảm × đối tượng đọc × nhịp cập nhật), KHÔNG theo nguồn dữ liệu.

QUYẾT ĐỊNH ĐÃ CHỐT (DEC-036→040, KHÔNG tự đảo lại):
- KHÔNG đổi tên KB đang chạy. Mỗi KB có một dòng "bản chất" ở mục 5.1 spec.
- `Kho Dữ Liệu Tổng Hợp` là KB DẪN XUẤT có chủ đích để xem Wiki/Graph toàn cảnh — BẬT nhóm tool Wiki cho Agent bind nó; không Agent nào bind đồng thời KB tổng hợp và KB lẻ cấu thành.
- `Data Daily` giữ dùng bình thường, KHÔNG hạ cấp.
- `PUM` hạ P1→P2 nội bộ (cả team đọc doanh thu), NHƯNG cấm số liệu doanh thu lọt vào nội dung gửi người chơi.
- Nhịp sự kiện LiveOps THEO THÁNG.
- Guardrail G-A (chống trộn phiên bản) và G-B (kế hoạch nội bộ ≠ brief duyệt) đã duyệt nguyên văn ở mục 12.1 spec, áp khi bind Plan Version. CHƯA áp lên Web.

5/12 KB đích CHƯA TỒN TẠI: `Item Catalog`, `Glossary & Systems` (đã bootstrap, đang "ĐANG TEST" trên Web), `Event Calendar & Brief`, `Runbook & Known Issues`, `CS FAQ & Policy` (đang "ĐANG TEST" trên Web, mới có format), `GM Policy & Sanction`. Đây là việc SOẠN NỘI DUNG.

==================================================
8. 10 CUSTOM AGENT — TRẠNG THÁI THẬT (đã xác minh trực tiếp 15/08 phiên 2)
==================================================

Tất cả đã đổi tên `GS9 CFL ...` trên Web. Xác minh bằng cách MỞ DIALOG từng Agent (không suy từ danh sách — danh sách có lúc hiện cache tên cũ).

| Agent | Agent ID | KB / tool | Mode / Preset | Ghi chú |
|---|---|---|---|---|
| GS9 CFL Knowledge Curator | 2dd80249-7db3-4a63-812a-6eff8fa1d2f6 | 2 KB (L0) / 6 | Smart / Hỏi đáp RAG | Đúng, không cần đổi preset (theo bản đồ kiến trúc mục 9, KHÔNG cần Wiki) |
| GS9 CFL KPI Experiment Analyst | 37da676c-59ce-4936-9314-5ac4cc3d1a45 | Kho Tổng Hợp / 6 | Smart / Hỏi đáp RAG | **Cần bật tay 2 tool `Tìm Wiki` + `Đọc trang Wiki`** qua tab Công cụ (ĐỪNG đổi preset — sẽ ghi đè System Prompt). Việc mở, chưa làm. |
| GS9 CFL Player Voice Analyst | 03bbab6e-1315-48ad-a05b-ad19fcb31796 | Sentiment / 4 | Smart / Hỏi đáp RAG | Đúng, chờ quét PII |
| GS9 CFL LiveOps Planner | 99ce5c68-e722-47fb-beab-c496433eb3d4 | Knowledge VNG AI / 6 | Smart / Hỏi đáp RAG | **BIND SAI TẦNG L0** — chờ KB Event Calendar (L2) tạo xong mới gỡ, đừng gỡ vội (mất tool) |
| GS9 CFL Release Reviewer | d4ec2736-bc1f-4fde-806f-2ade904d13b4 | Knowledge VNG AI / 5 | Smart / Hỏi đáp RAG | **BIND SAI TẦNG L0** — tương tự, chờ Runbook (L3) |
| GS9 CFL Incident Triage | 43a43154-ef15-40c3-99bb-678c3be733ed | CFL PUM / 5 | Smart / Hỏi đáp RAG | Đúng tạm |
| GS9 CFL Player Communications | 4b8e6d78-9217-4dbb-8ab3-919628a48440 | không bind / 3 | Smart / Hỏi đáp RAG | Chờ Glossary + guardrail G-B |
| GS9 CFL Economy Offer Analyst | 41524910-bec6-40ff-9b2a-96fa3e84a6e4 | không bind / 3 | Smart / Hỏi đáp RAG | Chờ tách Item Catalog |
| GS9 CFL CS Copilot | 9ad150d4-6de8-48f5-a2c2-22c008cb3ae5 | không bind / 0 | **Trả lời nhanh** (không có control preset) | Chờ nội dung CS FAQ |
| GS9 CFL GM Policy Advisor | 01d42d42-dd08-4907-9d4a-913142bc554c | không bind / 2 | Smart / Hỏi đáp RAG | Đổi vai trò xong 15/08 phiên 1, tên đổi xong phiên 2 |

**Xác nhận thêm ngày 15/08 (đã đọc trực tiếp, không suy đoán):**
- **`Prompt theo intent` để trống ở CẢ 10 Agent** — dùng template mặc định, đừng thêm khi chưa có chat-test (G6) xác nhận cần.
- **Cả 10 Agent: reranker `bge-reranker-v2-m3` đã bật, `Chế độ suy nghĩ` (Thinking) đang BẬT** (trái baseline cũ ghi Off — CHƯA rõ có chủ đích hay không, hỏi lại người dùng — xem DEC-050). Tải ảnh Bật + VLM `qwen3.6-plus`, tải âm thanh Off.
- **Cả 10 Agent đã share space `CFL Member` quyền `Được chỉnh sửa`** (6 người sửa được Agent — snapshot config có thể lệch bất cứ lúc nào).
- Basic tool + tool phụ thuộc KB của 6 Agent đã bind: xem `agent/liveops-custom-agent-catalog.md` mục "Ma trận tool active hiện tại" (đã cập nhật 15/08).

System Prompt giữ tiếng Anh CÓ CHỦ ĐÍCH (kết thúc `Reply in {{language}}`) — ĐỪNG tự dịch. Mô tả Agent là tiếng Việt.
Sharing đã đổi từ `0` sang space `CFL Member`. Chưa Agent nào chat-test đạt (G6 vẫn mở).

HÀNH VI UI: danh sách Agent TỰ SẮP LẠI/CACHE TÊN CŨ sau mỗi lần lưu → xác minh tên + Agent ID **bằng cách mở dialog trực tiếp**, đừng tin tên hiển thị trong danh sách.

**Nợ chưa xử lý:** meta-KB Web (`GS9 CFL Knowledge Agent`) đã sync qua Drive (28 tài liệu, xem mục 4) — CẦN KIỂM TRA lại xem hồ sơ GM đã đúng tên `doc-27-custom-gs9-gm-policy-advisor.md` (Policy Advisor) hay vẫn còn nội dung `Case Investigator` cũ, vì trước đó (trước khi Drive sync) đây là một khoản nợ đã biết.

==================================================
9. HAI KB NHÁP — ĐÃ ĐỔI TÊN, MỘT SỐ ĐANG "ĐANG TEST" TRÊN WEB
==================================================

`knowledge/GS9 CFL Glossary & Systems/` — 3 file, đã đổi tên `doc-00/01/02`. `doc-01-thuat-ngu-vu-khi.md` sinh từ dữ liệu Item Profile thật, phát hiện 3 lỗi dữ liệu nguồn: `Whtie`→`White` (15 dòng), phẩm chất RỖNG (24 dòng), hai hệ `A/B/C` vs hệ màu lẫn lộn (100 dòng). `doc-02-thuat-ngu-he-thong-va-che-do.md` rút 146 tiêu đề Plan V5; `Weapon Laboratory` CHƯA có tên tiếng Việt. **Trên Web đang ở trạng thái "ĐANG TEST" (3 tài liệu)** — hỏi lại người dùng ý định.

`knowledge/GS9 CFL CS FAQ & Policy/` — 1 file format, đã đổi tên `doc-00`. CHƯA CÓ NỘI DUNG THẬT. **Trên Web đang "ĐANG TEST" (1 tài liệu)**. Cần người dùng cung cấp: top 20–30 câu hỏi CS viết đúng như người chơi gõ + câu trả lời chuẩn + ranh giới chuyển tiếp GM/kỹ thuật + chính sách hoàn tiền/đền bù.

==================================================
10. BOUNDARY AN TOÀN
==================================================

Không tự thực hiện nếu chưa có yêu cầu rõ: tạo/sửa/publish/share/xóa Agent hoặc KB; đổi tool/model/prompt/quota (ngoại lệ: bật 2 tool Wiki cho KPI Experiment Analyst nếu người dùng xác nhận — xem mục 8); bind KB mới trước khi đối chiếu bản đồ 7 tầng; gửi tin/in-game mail/push/patch note; grant item, compensation, sanction; database write; commit/push Git.

**BLOCKER P0 — `GS9 CFL Item Profile`:** dữ liệu player (`openid`/`roleid`/`nickname`/lịch sử nạp), PII đã lan vào description/summary. KHÔNG bind, KHÔNG mở, KHÔNG đọc mẫu, KHÔNG sync, KHÔNG đổi tên (loại trừ hoàn toàn khỏi mọi việc đổi tên phiên 2). Người dùng từng đề cập ý định gom "tất cả KB tên GS9 CFL" vào Kho Dữ Liệu Tổng Hợp — ĐÃ CẢNH BÁO rủi ro PII, người dùng nói "đều là nội bộ nên đừng sợ" nhưng CHƯA xác nhận có cố ý gộp cả Item Profile hay không. Hỏi lại nếu liên quan.

Có service-account key trong `knowledge/GS9 CFL Item Profile/keys CFL ItemID/keys/` — `.gitignore` đã chặn, không đọc, không tự xóa, **và tuyệt đối không đưa vào phạm vi sync Drive**.

ACL: nhiều KB đang share quyền `Được chỉnh sửa` cho space `CFL Member` (nay 11 người, tăng từ 6). Rủi ro: sửa trực tiếp trên Web sẽ bị lần build kế tiếp GHI ĐÈ mà không cảnh báo → cần chạy G5 định kỳ (đối chiếu 20 module Web với master).

Phân loại kết luận: Đã kiểm chứng / Có điều kiện / Bị chặn–Chưa xác định. Web actual luôn là nguồn chuẩn khi khác planned baseline.

==================================================
11. MẸO THAO TÁC WEB — ĐỌC ĐỂ ĐỠ MẤT THỜI GIAN (cập nhật phiên 2)
==================================================

Nội dung KB/Agent nằm trong iframe cross-origin (`miniapp.vnggames.ai`) → `find`/`read_page` KHÔNG thấy, chỉ click theo tọa độ.

**MỚI phiên 2 — độ phân giải screenshot có thể ĐỔI GIỮA CÁC LẦN CHỤP trong cùng phiên** (đã gặp 1568x580 rồi tự đổi sang 1568x707 không báo trước) — toạ độ tính từ ảnh cũ sẽ SAI hoàn toàn sau khi độ phân giải đổi. Cách xử lý: **luôn tính tọa độ từ ảnh chụp MỚI NHẤT, không tái sử dụng tọa độ từ lượt trước**, đặc biệt sau khi điều hướng trang hoặc đổi bộ lọc.

**MỚI phiên 2 — danh sách KB/Agent có thể đổi thứ tự động (theo "Gần đây"/hoạt động) giữa các lần tải trang** — click vào một hàng theo tọa độ nhớ từ trước có thể trúng hàng khác. Cách an toàn nhất: dùng ô tìm kiếm lọc còn đúng 1 kết quả rồi mới click (đã dùng thành công nhiều lần cho danh sách Agent và KB).

Deep-link hữu ích:
- Lọc tài liệu: `...?tenant_id=10012&q=<từ khóa>` → còn 1 dòng, click an toàn hơn nhiều
- Mở chi tiết: `...?tenant_id=10012&knowledge_id=<DOC_ID>`

`read_network_requests` KHÔNG trả response body (đã thử lại phiên 2, xác nhận vẫn không lấy được JSON của `/v1/api/knowledge-bases` dù request 200 OK) — chỉ dùng để tìm URL/endpoint tham khảo, không dùng để đọc dữ liệu.

ĐÃ LOẠI TRỪ, đừng thử lại: gọi API `miniapp.vnggames.ai/kb/v1/api/...` bằng navigate top-level → `Unauthorized`; chạy JS đọc `localStorage` để tự gắn Bearer → **bị chặn, KHÔNG lách**; mở `miniapp.vnggames.ai/kb/` top-level → app kẹt skeleton.

VẪN DÙNG ĐƯỢC: MCP `get_image(url=minio://...)` để tải ảnh; MCP `list_documents`/`list_knowledge_bases` CHỈ thấy KB đã share vào space (KB `Test` KHÔNG share nên MCP không thấy — đọc qua trình duyệt).

**Cách lấy ID tài liệu nhanh:** mở tài liệu trong KB, đọc URL sau `&knowledge_id=` — đây là ID nội bộ ổn định, dùng để so sánh "tài liệu có bị tạo lại hay không" qua các lần sync, kể cả khi không lấy được URI MinIO trực tiếp.

Menu "..." trên một tài liệu chỉ có: Phân tích lại / Phân tích lại với tùy chọn / Chuyển / Xóa — KHÔNG có "Sao chép link"/URI.

==================================================
12. VIỆC ĐANG MỞ NGOÀI KẾ HOẠCH CHÍNH
==================================================

1. **Việc ưu tiên số 1: kết quả test đồng bộ tăng dần (mục 1)** — quyết định kiến trúc gộp ảnh+tài liệu.
2. Hỏi lại phạm vi Phase 3 thật người dùng đã tự làm (mục 4, 6).
3. Bật 2 tool Wiki cho `KPI Experiment Analyst` (mục 8) — chờ xác nhận.
4. Hỏi người dùng `Chế độ suy nghĩ` (Thinking) bật trên 10 Agent có chủ đích không (DEC-050).
5. Sửa 4 file meta-KB còn link chết trỏ `27-custom-gs9-gm-case-investigator.md` (mục 6) — cần giao riêng, là đổi nội dung/nhãn.
6. Kiểm tra hồ sơ GM trên Web meta-KB đã đúng `Policy Advisor` sau khi Drive sync chưa (mục 8).
7. Đồng bộ meta-KB Web (nếu chưa) — hồ sơ GM.
8. Chat-test grounding (gate G6) — chưa Agent nào đạt.
9. Thu thập nội dung CS FAQ từ người dùng.
10. Soạn tiếp Glossary hoặc Runbook.
11. Bind Plan Version cho Planner/Release Reviewer/Player Communications — sau khi guardrail G-A/G-B áp.
12. Commit/push nếu người dùng yêu cầu (CHƯA commit gì qua cả 2 phiên).

Không có mutation live nào agent tự khởi tạo đang chạy dở — chỉ có việc TEST (mục 1) đang chờ hành động của người dùng (sync vòng 2). Khi có nhiều lựa chọn hợp lý thì hỏi lại, đừng tự chọn.
```
