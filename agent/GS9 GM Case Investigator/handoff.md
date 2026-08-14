# Handoff — GS9 GM Case Investigator

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `01d42d42-dd08-4907-9d4a-913142bc554c`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; case-policy RAG and case-scoped read-only `Truy vấn CSDL` remain conditional on separate audits
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **Data dependency:** None; case-scoped view and policy audit required
- **Rollback:** Disable after GM Lead approval if unsafe; do not delete automatically
- **Release gate:** Row/field isolation, zero cross-player leakage and GM Lead approval
