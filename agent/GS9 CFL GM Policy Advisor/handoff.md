# Handoff — GS9 CFL GM Policy Advisor

> **Đổi tên và đổi vai trò 15/08/2026** từ `GS9 GM Case Investigator`. Tên, mô tả và System Prompt trên Web **đã áp đủ cùng ngày**.

- **Local config:** `0.2-draft`
- **Web state:** Đã tạo dưới tên cũ; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `01d42d42-dd08-4907-9d4a-913142bc554c`
- **Tên trên Web:** `GS9 CFL GM Policy Advisor` — khớp local từ 15/08/2026. **Không còn lệch nào giữa local và Web** ngoài việc chưa bind KB
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active
- **Evidence:** identity/config **Đã kiểm chứng** tại 14/08/2026; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; System Prompt local nay trùng khớp Web
- **Data dependency:** KB `GS9 CFL GM Policy & Sanction` chưa tồn tại. Không còn phụ thuộc case-scoped view — bằng chứng vụ việc chuyển sang tệp đính kèm hội thoại
- **Thay đổi so với bản 0.1:** bỏ `Truy vấn CSDL` khỏi lộ trình; bỏ yêu cầu case-scoped read-only view
- **Rollback:** Disable after GM Lead approval if unsafe; do not delete automatically
- **Release gate:** Chỉ trích dẫn điều khoản có mã; tách bạch POLICY vs CASE EVIDENCE; zero cross-player leakage; GM Lead approval

## Việc cần làm để Agent này chạy được

1. Tạo KB `GS9 CFL GM Policy & Sanction` (L6, `Loại: Tài liệu`, P2) — **chưa có nguồn**.
2. ~~Áp tên/mô tả/System Prompt lên Web~~ — **xong toàn bộ 15/08/2026**.
3. Bind KB, bật `Tìm theo ngữ nghĩa` + `Tìm theo từ khóa`.
4. Chat-test theo `tests.md`, đặc biệt case tách bạch POLICY vs CASE EVIDENCE.
