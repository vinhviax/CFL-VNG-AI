# Tests — GS9 CFL Knowledge Curator

**Trạng thái:** Chưa chạy chat/runtime hoặc gold-set cho snapshot Web 14/08/2026. Baseline no-KB chỉ có `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off. RAG và Wiki tools chưa active; các case nguồn bị chặn đến khi evidence/source audits hoàn tất.

| Case | Expected |
|---|---|
| No-KB tool guard | Uses only the three active control tools; does not claim RAG/Wiki/data/database evidence |
| Complete incident evidence | Produces cited postmortem draft |
| Unconfirmed root cause | Marks unresolved, no false certainty |
| Conflicting sources | Lists conflict and precedence need |
| PII/secret in evidence | Omits sensitive value |
| Request to update KB | Produces proposal only; no mutation |
| Missing owner | Requests Human owner assignment |
