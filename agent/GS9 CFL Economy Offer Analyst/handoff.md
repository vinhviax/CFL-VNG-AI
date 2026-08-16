# Handoff — GS9 CFL Economy Offer Analyst

- **Local config:** `0.1-draft`
- **Web state:** Đã tạo và lưu config; chưa bind KB, chưa publish/share, sharing `0`, chưa chat/runtime/gold-set test
- **Web Agent ID:** `41524910-bec6-40ff-9b2a-96fa3e84a6e4`
- **Web actual — 14/08/2026:** Smart / `Hỏi đáp RAG`; `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; no-KB; image/audio Off; tools `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off
- **Source-bound tools:** Không có tool RAG/Wiki/data/CSDL/catalog active; document RAG, `Danh mục sản phẩm` and curated data tools remain conditional on separate audits
- **Evidence:** identity/config **Đã kiểm chứng**; behavior **Có điều kiện**; runtime/quality **Bị chặn–Chưa xác định**
- **Source of truth:** Web actual; planned baseline/System Prompt local được giữ để triển khai và test sau
- **Data dependency:** None; economy/item/offer audit required
- **Rollback:** Disable after Economy Owner approval if unsafe; do not delete automatically
- **Release gate:** Reproducible calculation tests and Economy Owner approval
