# Luồng công việc của 10 custom Agent GS9

**Loại:** Hướng dẫn  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** LiveOps Lead và các owner chuyên môn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Thiết kế workflow; chưa phát hành runtime  
**Mức bằng chứng:** Có điều kiện  
**Nguồn chính:** `SRC-CUSTOM-CATALOG`, `SRC-CUSTOM-CONFIGS`, `SRC-CUSTOM-UPDATE`

## Vòng đời đề xuất

```text
Ý tưởng / mục tiêu
  ├─ LiveOps Planner ── event brief, lịch, dependency, risk, approval map
  ├─ Economy Offer Analyst ── giá, reward, source–sink, fairness
  ├─ KPI Experiment Analyst ── metric, baseline, cohort, measurement plan
  └─ Player Communications ── DRAFT notice/mail/push/localization
                ↓
       Release Reviewer ── preflight, blocker, rollback readiness
                ↓ Human Release Owner quyết định
          Vận hành live bởi hệ thống/Human ngoài Agent
                ↓
  ├─ Incident Triage ── facts, impact, timeline, hypotheses, next checks
  ├─ CS Copilot ── cited DRAFT reply và escalation
  └─ GM Case Investigator ── case-scoped evidence cho GM duyệt
                ↓
  ├─ Player Voice Analyst ── theme/sentiment trên dữ liệu ẩn danh
  ├─ KPI Experiment Analyst ── kết quả và hạn chế thống kê
  └─ Knowledge Curator ── postmortem, action items, DRAFT KB changes
```

Không mũi tên nào biểu thị Agent được phép publish, deploy, rollback, gửi tin, grant, compensate, sanction hoặc sửa KB.

## Handoff tối thiểu

| Từ | Sang | Gói bàn giao tối thiểu |
|---|---|---|
| Planner | Economy/KPI/Comms/Release | Brief version, region/platform, UTC + local time, owner, approved claims, dependencies |
| Economy | Planner/Release/KPI | IDs, price/reward calculation, assumptions, risks, approval status |
| KPI | Planner/Release/Curator | Metric definitions, dataset/view, freshness, filters, denominator, reproducible calculation |
| Communications | Release/Human publisher | DRAFT variants, claim checklist, glossary version, locale and approval state |
| Release | Human Release Owner | Blocking findings, required checks, rollback criteria, DRAFT recommendation |
| Incident | Incident Commander/CS/Curator | Fact/hypothesis split, timeline, impact, evidence gaps, next diagnostic check |
| CS | CS agent/GM | Cited reply draft, missing information, escalation reason; no broad player data |
| GM | Human GM | Approved case scope, evidence inventory, policy match, unresolved gaps |
| Player Voice | Product/LiveOps | Coverage, sample size, cohort protection, themes, uncertainty |
| Curator | Knowledge Owner | Source-backed draft, unresolved root cause, action owner requests, proposed KB changes |

## Ranh giới dữ liệu

- Chỉ chuyển dữ liệu tối thiểu cần cho workflow tiếp theo.
- Không đưa raw ticket, player identifier, secret hoặc credential vào meta-KB hay handoff phổ thông.
- GM chỉ nhận case-scoped record qua view đã phê duyệt; CS không tự chuyển dữ liệu sang GM ngoài quy trình.
- Player Voice chỉ dùng dữ liệu đã ẩn danh/tổng hợp và đạt cohort threshold.
- Tất cả nguồn nghiệp vụ vẫn đang chờ audit; không bind chỉ vì tên KB có vẻ phù hợp.

## Trạng thái hiện tại

Luồng trên là kiến trúc mục tiêu. Tại snapshot, basic tools đã lưu theo vai trò nhưng RAG/Wiki/Data/SQL/Catalog chưa bật, không có KB và chưa có test. Các handoff chưa được chứng minh bằng runtime.

