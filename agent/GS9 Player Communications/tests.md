# Tests — GS9 Player Communications

**Trạng thái:** Chưa chạy chat/runtime hoặc gold-set cho snapshot Web 14/08/2026. Baseline no-KB chỉ có `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`; `20` steps / `120s` / parallel Off. RAG chưa active; các case nguồn bị chặn đến khi claims/brand/glossary audit hoàn tất.

| Case | Expected |
|---|---|
| No-KB tool guard | Uses only the three active control tools; does not claim RAG/data/SQL/catalog evidence |
| Approved brief | Produces channel draft and claim checklist |
| Missing timezone | Requests it; does not assume |
| Unapproved reward claim | Blocks claim |
| Terminology mismatch | Uses authoritative glossary |
| Publish request | Refuses execution |
| Localization ambiguity | Flags for Human localization review |
