# GS9 CFL Knowledge Agent — giới thiệu và phạm vi

**Loại:** Hướng dẫn  
**Owner nội dung:** Knowledge Owner / Agent Knowledge Steward  
**Owner nghiệp vụ:** VNG AI Platform Owner và owner ghi trên từng Agent  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Tài liệu tra cứu; không phải corpus nghiệp vụ game  
**Mức bằng chứng:** Đã kiểm chứng, Có điều kiện và Bị chặn–Chưa xác định được ghi riêng  
**Nguồn chính:** `SRC-DEFAULT-AUDIT`, `SRC-CUSTOM-AUDIT`, `SRC-CUSTOM-UPDATE`

## Mục đích

Kho này giúp Human:

- hiểu sáu Agent mặc định và mười custom Agent GS9;
- so sánh và chọn đúng Agent theo công việc;
- biết dữ liệu, công cụ và hành động nào được phép;
- phân biệt cấu hình Web đã nhìn thấy, thiết kế dự kiến và hành vi runtime chưa kiểm thử;
- tìm owner, release gate, rollback và nguồn bằng chứng.

Đây là **meta-KB về Agent**. Không đưa event brief, dữ liệu người chơi, metric, policy GM/CS, catalog vật phẩm hoặc nội dung vận hành game vào đây. Những nguồn đó phải nằm trong corpus nghiệp vụ riêng, được audit owner, ACL, retention và dữ liệu nhạy cảm trước khi bind.

## Trạng thái nhanh ngày 14/08/2026

- Sáu Agent mặc định đã được audit UI chỉ-đọc; không chat/runtime test.
- Mười custom Agent đã được tạo nhưng đều no-KB, sharing `0`, chưa publish/share và chưa chạy gold-set/runtime test.
- Chín custom Smart Agent dùng model `hosted_vllm/qwen3.6-35b`, temperature `0.7`, Thinking Off, reranker trống, image/audio Off, `20` loops, timeout `120s`, parallel Off. Chúng chỉ có các basic tool theo vai trò; RAG, Wiki, Data, SQL và Catalog chưa bật.
- `GS9 CS Copilot` dùng Fast Answer, cùng model/temperature/no-KB, không có tab Tools và không có steps/timeout.
- Vì chưa có nguồn nghiệp vụ và chưa test, mười custom Agent **chưa sẵn sàng phát hành cho công việc thật**.

## Ba lớp phải đọc tách biệt

| Lớp | Ý nghĩa | Có thể kết luận |
|---|---|---|
| Web actual | Cấu hình UI-visible tại snapshot | Identity, model, mode, tool, KB, giới hạn nhìn thấy |
| Planned baseline | Thiết kế trong `agent/<Agent>/config.md` | Mục tiêu triển khai, không phải trạng thái đang chạy |
| Runtime evidence | Kết quả chat/gold-set có ngày và bằng chứng | Hiện chưa có cho 16 Agent trong phạm vi audit này |

## Nhãn bằng chứng

- **Đã kiểm chứng:** nhìn thấy trực tiếp trên UI hoặc được ghi trong audit có ngày.
- **Có điều kiện:** mô tả từ prompt/baseline; chỉ đúng khi nguồn, tool, quyền và runtime đáp ứng.
- **Bị chặn–Chưa xác định:** chưa có quyền, dữ liệu hoặc test để kết luận.

Không đổi nhãn `Có điều kiện` thành `Đã kiểm chứng` chỉ vì System Prompt mô tả đúng hành vi mong muốn.

## Điểm vào

- [Chọn Agent nhanh](01-chon-agent-nhanh.md)
- [Ma trận so sánh 16 Agent](02-ma-tran-so-sanh-16-agent.md)
- [Luồng công việc 10 custom Agent](03-luong-cong-viec-10-custom-agent.md)
- [Trạng thái, bằng chứng và giới hạn](04-trang-thai-bang-chung-va-gioi-han.md)
- [Sử dụng an toàn và release gate](05-su-dung-an-toan-va-release-gate.md)
- [Nguồn, quyền sở hữu và truy nguyên](90-nguon-quyen-so-huu-va-truy-nguyen.md)

## Hồ sơ Agent mặc định

- [Quick Answer](10-default-quick-answer.md)
- [Smart Reasoning](11-default-smart-reasoning.md)
- [Hybrid Researcher](12-default-hybrid-researcher.md)
- [Wiki Questioner](13-default-wiki-questioner.md)
- [Data Analyst](14-default-data-analyst.md)
- [FPA Analyst](15-default-fpa-analyst.md)

## Hồ sơ custom Agent

- [GS9 LiveOps Planner](20-custom-gs9-liveops-planner.md)
- [GS9 Release Reviewer](21-custom-gs9-release-reviewer.md)
- [GS9 Incident Triage](22-custom-gs9-incident-triage.md)
- [GS9 KPI Experiment Analyst](23-custom-gs9-kpi-experiment-analyst.md)
- [GS9 Economy Offer Analyst](24-custom-gs9-economy-offer-analyst.md)
- [GS9 Player Voice Analyst](25-custom-gs9-player-voice-analyst.md)
- [GS9 CS Copilot](26-custom-gs9-cs-copilot.md)
- [GS9 GM Case Investigator](27-custom-gs9-gm-case-investigator.md)
- [GS9 Player Communications](28-custom-gs9-player-communications.md)
- [GS9 Knowledge Curator](29-custom-gs9-knowledge-curator.md)

## Thuật ngữ tối thiểu

| Thuật ngữ | Nghĩa trong kho này |
|---|---|
| KB / corpus | Nguồn được Agent truy hồi; không đồng nghĩa với prompt |
| Tool hiệu lực | Tool UI cho thấy đang bật, không phải toàn bộ tool có thể chọn |
| Thinking | Công tắc suy luận mở rộng của model; khác basic tool `Suy nghĩ` |
| DRAFT | Đầu ra để Human rà soát, không phải hành động đã thực hiện |
| Human gate | Vai trò phải phê duyệt trước publish, gửi, thay đổi live hoặc quyết định nhạy cảm |
| No-KB | Agent không có nguồn nghiệp vụ để grounding/RAG tại snapshot |
