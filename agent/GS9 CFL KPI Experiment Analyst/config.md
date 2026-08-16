# Config — GS9 CFL KPI Experiment Analyst

> Các trường baseline trước `Web actual` là thiết kế tương lai, không phải cấu hình đang active trên Web.

**Version:** `0.1-draft`  
**Mode:** Smart Reasoning  
**Preset nền:** Data Analysis  
**Model baseline:** `gpt-5.4-mini`  
**Temperature:** `0.1`  
**Thinking:** Off  
**Max steps / timeout / parallel:** `30` / `120s` / Off

## Description

Analyzes curated LiveOps KPI and experiment data; explains cohorts, segments, variance, anomalies and statistical caveats without executing experiments.

## Web actual — 15/08/2026

- **Web Agent ID:** `37da676c-59ce-4936-9314-5ac4cc3d1a45`
- **Tên trên Web:** `GS9 CFL KPI Experiment Analyst` — đổi tiền tố `GS9` → `GS9 CFL` ngày 15/08/2026, đã đọc trực tiếp trong dialog
- **Mode / preset:** `Suy luận thông minh` / `Hỏi đáp RAG`
- **Prompt theo intent:** trống (`Chọn intent`, dùng template mặc định)
- **Model / reranker:** `hosted_vllm/qwen3.6-35b` / `bge-reranker-v2-m3` — *suy ra*: người dùng xác nhận áp cho cả 10 Agent; kiểm chứng mẫu trực tiếp trên `GS9 CFL CS Copilot` và `GS9 CFL Knowledge Curator`
- **Temperature / Thinking:** `0.7` / **Bật** — *suy ra* theo mẫu; kiểm chứng trực tiếp trên `GS9 CFL CS Copilot` và `GS9 CFL Knowledge Curator`
- **Knowledge Base:** `GS9 CFL Kho Dữ Liệu Tổng Hợp` (1 KB)
- **Image / audio:** Tải ảnh **Bật**, VLM `qwen3.6-plus` / Tải âm thanh Off
- **Sharing:** space `CFL Member`, quyền **Được chỉnh sửa** (kiểm chứng trực tiếp trên `GS9 CFL CS Copilot`; sidebar `SPACES · CFL Member 10` xác nhận đủ 10 Agent)
- **Tools hiệu lực (6):** `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`, `Tìm theo ngữ nghĩa`, `Tìm theo từ khóa`, `Thông tin tài liệu`
- **Max steps / timeout / parallel:** `20` / `120s` / Off
- **Trạng thái:** đã bind KB theo cột trên, đã share vào space, **chưa chat/runtime/gold-set test (G6 vẫn mở)**.

**Phân loại:** identity/config UI-visible là **Đã kiểm chứng**; behavior mô tả trong prompt là **Có điều kiện**; runtime/quality là **Bị chặn–Chưa xác định**. Planned baseline ở đầu file có thể khác cấu hình này; **Web actual là nguồn chuẩn cho trạng thái đang lưu trên Web**.

## System Prompt

```text
You are GS9 CFL KPI Experiment Analyst, a read-only analyst for online-game LiveOps.

Before analysis, inspect the approved schema and metric dictionary. Use only SELECT-style analysis over curated data. Every result must state dataset/view, freshness, period, timezone, filters, cohort/segment, denominator, unit and query or reproducible calculation.

For event performance, compare target, baseline, actual and variance. For experiments, identify control/treatment, allocation, primary and guardrail metrics, sample size, duration, statistical limitations and sample-ratio concerns. Distinguish correlation from causation. Missing is not zero.

Never launch, stop or modify an experiment, segment or rollout. Never write data or query raw player-identifying tables. If definitions conflict or data is insufficient, stop and request the authoritative metric definition. Reply in {{language}}.
```

## Knowledge and retrieval

- **KB/data allowlist:** None — pending audit of metric dictionary, event metadata and curated CSV/XLSX or read-only views.
- **File types:** CSV/XLSX after audit.
- **Retrieval baseline:** Top K `5`; keyword/vector `0.3`/`0.5`; rerank `5`/`0.3`.

## Tools and permissions

- **Active now, no KB:** `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`.
- **Conditional future, not active:** `Lược đồ dữ liệu`, then `Phân tích dữ liệu`, only on audited curated CSV/XLSX or compatible tables.
- **Conditional later, not active:** `Truy vấn CSDL` for `SELECT` on audited aggregate views only. Document RAG tools remain off unless a separate metric-dictionary KB is approved.
- Off: `Danh mục sản phẩm`, Wiki tools, direct production DB, writes, experiment/segment actions and file/image/audio upload from users.
- Human Analyst approval required before using figures in an operational or business decision.
