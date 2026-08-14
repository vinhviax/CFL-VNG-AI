# Nguồn, quyền sở hữu và truy nguyên

**Loại:** Governance  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** VNG AI Platform Owner và owner từng Agent  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Source register chuẩn của mirror  
**Mức bằng chứng:** Đã kiểm chứng cho đường dẫn và phạm vi nguồn  
**Nguồn chính:** Các nguồn trong bảng dưới

## Source precedence

1. Audit Web có ngày và phần `Web actual` cho trạng thái UI-visible.
2. Per-Agent `config.md`/`handoff.md` cho snapshot chi tiết khi không mâu thuẫn với audit/cập nhật mới hơn.
3. Catalog, `STATUS.md`, `HANDOFF.md` cho tổng hợp liên Agent.
4. Per-Agent `README.md` cho mục đích, người dùng và business owner.
5. Planned baseline/System Prompt cho thiết kế dự kiến, không phải runtime.
6. `tests.md` cho acceptance criteria, không phải kết quả test.
7. Implementation plan cho ý định lịch sử, không phải completion evidence.

## Nguồn dùng chung

| Source ID | Đường dẫn local | Phạm vi | Owner nguồn / ngày |
|---|---|---|---|
| `SRC-AGENT-INDEX` | `agent/README.md` | Quy ước artifact và boundary chung | Agent Knowledge Steward / 14-08-2026 |
| `SRC-DEFAULT-AUDIT` | `audit/default-agent-readonly-audit-2026-08-14.md` | Sáu default, config-only audit | VNG AI Platform evidence / 14-08-2026 |
| `SRC-CUSTOM-AUDIT` | `audit/liveops-custom-agent-creation-2026-08-14.md` | Creation, identity, common config ban đầu | Agent rollout evidence / 14-08-2026 |
| `SRC-CUSTOM-CATALOG` | `agent/liveops-custom-agent-catalog.md` | Ten-Agent inventory, purpose, boundary | Agent Knowledge Steward / 14-08-2026 |
| `SRC-CUSTOM-UPDATE` | `audit/liveops-custom-agent-multitool-and-agent-kb-2026-08-14.md` | Web audit sau lưu: role-based basic tools, badge và `20/120s` cho chín Smart Agent | VNG AI Web operator / 14-08-2026 |
| `SRC-CUSTOM-CONFIGS` | `agent/GS9 */config.md` | Planned baseline, prompt, Web ID và snapshot | Từng business owner / 14-08-2026 |
| `SRC-CUSTOM-HANDOFFS` | `agent/GS9 */handoff.md` | Dependency, rollback, release gate | Từng business owner / 14-08-2026 |
| `SRC-CUSTOM-TESTS` | `agent/GS9 */tests.md` | Test design; chưa có execution result | Từng business owner / chưa chạy |
| `SRC-STATUS` | `STATUS.md`; `HANDOFF.md` | Workspace summary, không thay per-Agent source | Knowledge Owner / 14-08-2026 |

`SRC-CUSTOM-UPDATE` là bằng chứng cụ thể cho lần cấu hình multi-tool ngày 14/08/2026 và chỉ thay phần tool/steps/timeout cũ của custom Agent. Các identity, no-KB, model, sharing và boundary khác tiếp tục dùng `SRC-CUSTOM-AUDIT`, `SRC-CUSTOM-CONFIGS` và `SRC-CUSTOM-HANDOFFS`.

## Nguồn per default Agent

| Profile | Source ID | Đường dẫn local | Operational owner |
|---|---|---|---|
| Quick Answer | `SRC-D-QUICK` | `agent/quick-answer-config.md` | Chưa xác định trong nguồn |
| Smart Reasoning | `SRC-D-SMART` | `agent/smart-reasoning-config.md` | Chưa xác định trong nguồn |
| Hybrid Researcher | `SRC-D-HYBRID` | `agent/hybrid-researcher-config.md` | Chưa xác định trong nguồn |
| Wiki Questioner | `SRC-D-WIKI` | `agent/wiki-questioner-config.md` | Chưa xác định trong nguồn |
| Data Analyst | `SRC-D-DATA` | `agent/data-analyst-config.md` | Chưa xác định trong nguồn |
| FPA Analyst | `SRC-D-FPA` | `agent/fpa-analyst-config.md` | Chưa xác định trong nguồn |

## Owner per custom Agent

| Agent | Business owner | Source files |
|---|---|---|
| LiveOps Planner | LiveOps Lead | `agent/GS9 LiveOps Planner/{README,config,tests,handoff}.md` |
| Release Reviewer | Release Owner | `agent/GS9 Release Reviewer/{README,config,tests,handoff}.md` |
| Incident Triage | Incident Commander | `agent/GS9 Incident Triage/{README,config,tests,handoff}.md` |
| KPI Experiment Analyst | Product/Data Analytics Lead | `agent/GS9 KPI Experiment Analyst/{README,config,tests,handoff}.md` |
| Economy Offer Analyst | Economy/Product Owner | `agent/GS9 Economy Offer Analyst/{README,config,tests,handoff}.md` |
| Player Voice Analyst | Player Insights Lead | `agent/GS9 Player Voice Analyst/{README,config,tests,handoff}.md` |
| CS Copilot | CS Lead | `agent/GS9 CS Copilot/{README,config,tests,handoff}.md` |
| GM Case Investigator | GM Lead | `agent/GS9 GM Case Investigator/{README,config,tests,handoff}.md` |
| Player Communications | Communications/Marketing Lead | `agent/GS9 Player Communications/{README,config,tests,handoff}.md` |
| Knowledge Curator | Knowledge Owner / LiveOps Lead | `agent/GS9 Knowledge Curator/{README,config,tests,handoff}.md` |

## Quy tắc trích nguồn trong profile

Mỗi bảng cấu hình hoặc trạng thái phải ghi `Nguồn` và `As-of`. Đường dẫn ngoài folder mirror được giữ ở dạng code literal để bản upload không tạo broken link. Link Markdown trong mirror chỉ dùng cho 25 trang nội bộ.

Khi nguồn thay đổi, ghi SHA-256 hoặc diff trong artifact audit phát hành, cập nhật trang phụ thuộc và thêm mục vào [lịch sử thay đổi](92-lich-su-thay-doi.md).
