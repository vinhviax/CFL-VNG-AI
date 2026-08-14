# Chọn Agent nhanh theo công việc

**Loại:** Hướng dẫn  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** Owner của Agent được chọn  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Hướng dẫn chọn; không cấp quyền sử dụng  
**Mức bằng chứng:** Có điều kiện  
**Nguồn chính:** `SRC-DEFAULT-AUDIT`, `SRC-CUSTOM-CATALOG`, `SRC-CUSTOM-UPDATE`

## Gate 1 — Agent có sẵn sàng không?

1. Nếu là custom Agent GS9: hiện **chưa sẵn sàng cho công việc thật** vì no-KB, sharing `0` và chưa test. Dùng hồ sơ Agent để chuẩn bị nguồn, test và phê duyệt; không coi prompt là bằng chứng chất lượng.
2. Nếu là Agent mặc định: audit chỉ chứng minh cấu hình UI. Kiểm tra dữ liệu được phép dùng trước khi chat vì cả sáu đang chọn `Tất cả kho tri thức`.
3. Nếu công việc có PII, case GM, dữ liệu người chơi, sanction, compensation, live config hoặc outbound message: phải dùng workflow được owner phê duyệt; không thay bằng một Agent mặc định cho tiện.

## Gate 2 — Chọn theo mục tiêu

| Nhu cầu | Agent phù hợp về thiết kế | Điều kiện bắt buộc |
|---|---|---|
| Hỏi đáp KB nhanh | [Quick Answer](10-default-quick-answer.md) | Kiểm tra fallback general knowledge và phạm vi All KB |
| RAG nhiều bước, evidence-first | [Smart Reasoning](11-default-smart-reasoning.md) | Nguồn phù hợp; runtime chưa được audit |
| Tổng quan Wiki rồi kiểm chứng raw chunk | [Hybrid Researcher](12-default-hybrid-researcher.md) | Wiki + RAG đáng tin; lưu ý thiếu `wiki_flag_issue` |
| Hỏi đáp chỉ trên Wiki | [Wiki Questioner](13-default-wiki-questioner.md) | Wiki đã xây đúng và nguồn gốc rõ ràng |
| Phân tích CSV/XLSX | [Data Analyst](14-default-data-analyst.md) | Dataset đã audit; chỉ `SELECT` theo prompt |
| Pipeline FPA cố định | [FPA Analyst](15-default-fpa-analyst.md) | Phải xác nhận source scoping; UI vẫn All KB |
| Lập event brief, lịch, checklist | [GS9 LiveOps Planner](20-custom-gs9-liveops-planner.md) | Chờ bind event/calendar/runbook đã audit và gold-set |
| Review change/config trước release | [GS9 Release Reviewer](21-custom-gs9-release-reviewer.md) | Chờ config dictionary/change ticket và Release Owner |
| Tổng hợp sự cố, timeline, severity | [GS9 Incident Triage](22-custom-gs9-incident-triage.md) | Shadow drill; không chạy remediation |
| KPI, cohort, experiment | [GS9 KPI Experiment Analyst](23-custom-gs9-kpi-experiment-analyst.md) | Metric dictionary + curated data; không dùng raw PII |
| Giá, reward, source–sink, offer | [GS9 Economy Offer Analyst](24-custom-gs9-economy-offer-analyst.md) | Item/economy/offer data đã audit |
| Feedback ẩn danh, theme, sentiment | [GS9 Player Voice Analyst](25-custom-gs9-player-voice-analyst.md) | Privacy, retention và cohort threshold đạt |
| Soạn reply/escalation CS | [GS9 CS Copilot](26-custom-gs9-cs-copilot.md) | FAQ/policy/known issue đã audit; Human gửi |
| Evidence bundle cho GM case | [GS9 GM Case Investigator](27-custom-gs9-gm-case-investigator.md) | Case ID, approved scope, least privilege, GM duyệt |
| Notice, mail, push, localization | [GS9 Player Communications](28-custom-gs9-player-communications.md) | Approved brief/claim/glossary; Human publish |
| Postmortem và đề xuất cập nhật KB | [GS9 Knowledge Curator](29-custom-gs9-knowledge-curator.md) | Evidence đã phê duyệt; Human cập nhật/publish |

## Không chọn theo tên hoặc preset đơn thuần

- Preset là cấu hình khởi đầu, không bảo đảm grounding hoặc chất lượng.
- Model giống nhau không làm hai Agent có cùng quyền hoặc dữ liệu.
- Tool xuất hiện trong planned baseline không có nghĩa tool đang bật trên Web.
- Không clone trực tiếp default Agent cho dữ liệu nhạy cảm; default đang dùng All KB.
- Không dùng custom Agent như thể đã RAG: tại snapshot, RAG/Wiki/Data/SQL/Catalog đều chưa hiệu lực.

## Khi không có Agent phù hợp

Tạm dừng, ghi rõ mục tiêu, owner, dữ liệu, hành động bị cấm, output mong muốn và tiêu chí pass. Trình owner thiết kế hoặc phát hành Agent mới; không mở rộng quyền của Agent gần giống mà không audit tác động.

