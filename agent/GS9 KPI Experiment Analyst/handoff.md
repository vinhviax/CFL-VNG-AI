# Handoff — GS9 KPI Experiment Analyst

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `37da676c-59ce-4936-9314-5ac4cc3d1a45`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; `Lược đồ dữ liệu`, `Phân tích dữ liệu` and read-only `Truy vấn CSDL` remain conditional on metric/data audits
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **Data dependency:** None; metric/data audit required
- **Rollback:** Disable after Data Lead approval if unsafe; do not delete automatically
- **Release gate:** Gold calculations, SELECT-only enforcement, zero PII leakage and Data Lead approval
