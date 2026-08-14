# Handoff — GS9 Incident Triage

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `43a43154-ef15-40c3-99bb-678c3be733ed`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; document RAG and read-only `Truy vấn CSDL` remain conditional on separate source audits
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **KB dependency:** None; incident sources require audit
- **Rollback:** Disable after Incident Commander approval if unsafe; do not delete automatically
- **Release gate:** Shadow-mode incident drills, zero autonomous action and Incident Commander approval
