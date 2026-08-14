# Ma trận so sánh 16 Agent

**Loại:** Hướng dẫn  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Owner ghi trên từng hồ sơ  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** So sánh; không thay release gate  
**Mức bằng chứng:** Cấu hình Đã kiểm chứng; hành vi Có điều kiện  
**Nguồn chính:** `SRC-DEFAULT-AUDIT`, `SRC-CUSTOM-AUDIT`, `SRC-CUSTOM-UPDATE`

## Agent mặc định

| Agent | Mục tiêu | Mode / model | Scope và tool hiệu lực | Giới hạn thấy được | Caveat chính |
|---|---|---|---|---|---|
| [Quick Answer](10-default-quick-answer.md) | Q&A nhanh | Fast Answer / `gpt-5.4-mini` | All KB, all files; không tab Tools | max output `0`; history `5` | Fallback có thể dùng general knowledge |
| [Smart Reasoning](11-default-smart-reasoning.md) | RAG evidence-first nhiều bước | Smart / `gpt-5.4-mini` | All KB; semantic, keyword, chunks, document info | `50` loops / `120s` | Runtime chưa test |
| [Hybrid Researcher](12-default-hybrid-researcher.md) | Wiki + raw-chunk research | Smart / `qwen3.6-plus` | All KB; 3 Wiki + 4 RAG tools | `40` / `120s`; parallel On | Prompt nhắc tool flag không active |
| [Wiki Questioner](13-default-wiki-questioner.md) | Wiki Q&A | Smart / `qwen3.6-plus` | All KB; Wiki search/read/source | `30` / `120s` | External MCP và flag tool chưa xác định |
| [Data Analyst](14-default-data-analyst.md) | CSV/XLSX + DuckDB | Smart / `gpt-5.4-mini` | All KB nhưng CSV/XLSX; schema + analysis | `30` / `120s` | Prompt-only `SELECT`; chưa chạy query audit |
| [FPA Analyst](15-default-fpa-analyst.md) | Pipeline FPA cố định | Workflow / `qwen3.6-plus` | All KB; Catalog, Ask, RAG, DB query | `10` / `180s` | Prompt nói scoped nhưng UI vẫn All KB |

## Custom Agent GS9

Tất cả custom Agent dùng `hosted_vllm/qwen3.6-35b`, temperature `0.7`, Thinking Off, reranker trống, no-KB, image/audio Off, sharing `0`, chưa publish/share và chưa runtime test.

| Agent | Workflow | Mode | Basic tool hiệu lực | Human gate | Sẵn sàng |
|---|---|---|---|---|---|
| [LiveOps Planner](20-custom-gs9-liveops-planner.md) | Event brief/calendar/risk | Smart | Ask + Think + Todo | LiveOps Lead | Chưa |
| [Release Reviewer](21-custom-gs9-release-reviewer.md) | Preflight và rollback readiness | Smart | Ask + Think + Todo | Release Owner | Chưa |
| [Incident Triage](22-custom-gs9-incident-triage.md) | Timeline/severity/hypothesis | Smart | Ask + Think + Todo | Incident Commander | Chưa |
| [KPI Experiment Analyst](23-custom-gs9-kpi-experiment-analyst.md) | KPI/cohort/experiment | Smart | Ask + Think + Todo | Data Analytics Lead | Chưa |
| [Economy Offer Analyst](24-custom-gs9-economy-offer-analyst.md) | Price/reward/source–sink | Smart | Ask + Think + Todo | Economy Owner | Chưa |
| [Player Voice Analyst](25-custom-gs9-player-voice-analyst.md) | Aggregate feedback | Smart | Ask + Think | Player Insights Lead | Chưa |
| [CS Copilot](26-custom-gs9-cs-copilot.md) | Ticket/reply/escalation draft | Fast Answer | Không tab Tools | CS Lead | Chưa |
| [GM Case Investigator](27-custom-gs9-gm-case-investigator.md) | Case-scoped evidence | Smart | Ask + Todo | GM Lead | Chưa |
| [Player Communications](28-custom-gs9-player-communications.md) | Channel/localization draft | Smart | Ask + Think + Todo | Communications Lead | Chưa |
| [Knowledge Curator](29-custom-gs9-knowledge-curator.md) | Postmortem/KB proposal | Smart | Ask + Think + Todo | Knowledge Owner | Chưa |

Chín Smart Agent đều có `20` loops, timeout `120s`, parallel Off. Basic tool `Suy nghĩ` không đồng nghĩa với công tắc model Thinking; công tắc này đang Off.

## Khác biệt quan trọng

| Default | Custom GS9 |
|---|---|
| Cấu hình sẵn, dùng All KB | Đã tạo nhưng no-KB và chưa phát hành |
| Tool nguồn có thể active | Chỉ basic tools theo vai trò; source tools chưa active |
| Owner nghiệp vụ không được ghi trong nguồn audit | Có owner và Human gate theo workflow |
| Không được thiết kế riêng cho ranh giới dữ liệu GS9 | Thiết kế least-privilege nhưng chưa được chứng minh runtime |

