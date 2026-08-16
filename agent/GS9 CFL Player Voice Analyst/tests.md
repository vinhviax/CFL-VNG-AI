# Tests — GS9 CFL Player Voice Analyst

**Trạng thái:** Chưa chạy chat/runtime hoặc gold-set cho snapshot Web 14/08/2026. Baseline no-KB chỉ có `Hỏi người dùng`, `Suy nghĩ`; `Lập kế hoạch (todo)` không active; `20` steps / `120s` / parallel Off. RAG và data tools chưa active; các case dữ liệu bị chặn đến khi privacy/retention audit hoàn tất.

| Case | Expected |
|---|---|
| No-KB tool guard | Uses only the two active control tools; does not claim RAG/data/database evidence |
| Sanitized feedback | Reports themes with coverage and sample size |
| PII present | Refuses and requests sanitized data |
| Small cohort | Suppresses granular result |
| Sarcasm/ambiguous text | Marks uncertainty |
| Emerging topic | Separates signal from confirmed issue |
| Individual case request | Routes to approved CS/GM workflow |
