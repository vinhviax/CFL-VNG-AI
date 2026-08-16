# Handoff — GS9 CFL Player Voice Analyst

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `03bbab6e-1315-48ad-a05b-ad19fcb31796`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; privacy-audited data tools and taxonomy/runbook RAG remain conditional
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **Data dependency:** None; privacy, retention and dataset audit required
- **Rollback:** Disable after Privacy/Insights approval if unsafe; do not delete automatically
- **Release gate:** Zero PII leakage, cohort threshold tests and Insights Lead approval
