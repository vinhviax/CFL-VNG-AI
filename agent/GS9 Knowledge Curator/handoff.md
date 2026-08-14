# Handoff — GS9 Knowledge Curator

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `2dd80249-7db3-4a63-812a-6eff8fa1d2f6`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; document RAG and Wiki tools remain conditional on separate evidence/source audits
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **KB dependency:** None; evidence and Wiki audit required
- **Rollback:** Disable after Knowledge Owner approval if unsafe; do not delete automatically
- **Release gate:** Evidence classification, no-false-root-cause and no-publish tests
