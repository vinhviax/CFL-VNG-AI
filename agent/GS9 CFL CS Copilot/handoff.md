# Handoff — GS9 CFL CS Copilot

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5`
- **Web actual — 14/08/2026:** Fast Answer / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; không có tab Tools, `0` explicit tools, không có steps/timeout
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; automatic Fast Answer retrieval remains conditional on an audited selected CS KB
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **KB dependency:** None; CS sources require audit
- **Rollback:** Disable after CS Lead approval if unsafe; do not delete automatically
- **Release gate:** Grounded reply, escalation and privacy tests; CS Lead approval
