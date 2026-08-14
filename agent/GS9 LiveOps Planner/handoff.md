# Handoff — GS9 LiveOps Planner

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `99ce5c68-e722-47fb-beab-c496433eb3d4`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; RAG document tools remain conditional on the business-source allowlist audit
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **KB dependency:** None; business KB audit required
- **Rollback:** If created incorrectly, disable only after Human approval; do not delete automatically
- **Release gate:** KB allowlist, gold-set tests and LiveOps Lead approval
