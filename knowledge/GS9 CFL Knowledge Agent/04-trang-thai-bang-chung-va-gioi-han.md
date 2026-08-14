# Trạng thái, bằng chứng và giới hạn hiện tại

**Loại:** Governance  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** VNG AI Platform Owner  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Nguồn chuẩn cho mức độ chắc chắn  
**Mức bằng chứng:** Hỗn hợp; từng dòng có nhãn riêng  
**Nguồn chính:** `SRC-DEFAULT-AUDIT`, `SRC-CUSTOM-AUDIT`, `SRC-CUSTOM-UPDATE`

## Sáu Agent mặc định

**Đã kiểm chứng:** identity, mode/preset, model, retrieval, tool active và giới hạn UI-visible được audit chỉ-đọc.

**Bị chặn–Chưa xác định:** runtime behavior, chất lượng, latency, quota, retention, sharing/ACL, quyền thực thi menu, model availability và source permission thực tế.

Các caveat cấu hình:

- Quick Answer: system prompt yêu cầu context-only nhưng fallback cho phép general knowledge khi document list rỗng.
- Hybrid Researcher và Wiki Questioner: prompt nhắc `wiki_flag_issue`, UI không liệt kê tool này active.
- FPA Analyst: prompt nói pipeline đã scope source, UI vẫn chọn All KB.
- Tất cả sáu chọn All KB; không clone trực tiếp cho dữ liệu nhạy cảm.

## Mười custom Agent

**Đã kiểm chứng:** đã tạo đủ 10 identity/Web Agent ID; no-KB; sharing `0`; không publish/share; model `hosted_vllm/qwen3.6-35b`; reranker trống; temperature `0.7`; Thinking Off; image/audio Off.

**Đã kiểm chứng — cập nhật cấu hình cuối ngày 14/08/2026:**

- Planner, Release, Incident, KPI, Economy, Communications và Curator: `Hỏi người dùng`, `Suy nghĩ`, `Lập kế hoạch (todo)`.
- Player Voice: `Hỏi người dùng`, `Suy nghĩ`.
- GM: `Hỏi người dùng`, `Lập kế hoạch (todo)`.
- CS: Fast Answer, không có tab Tools.
- Chín Smart Agent: `20` loops, timeout `120s`, parallel Off.

Cập nhật này thay thế bảng tool/steps cũ trong audit tạo Agent. Các phần khác của audit vẫn là bằng chứng snapshot.

**Có điều kiện:** mục đích, prompt, planned RAG/Data/Wiki/SQL và approval behavior.

**Bị chặn–Chưa xác định:** grounding, citation, refusal, privacy behavior, tool orchestration, quality, latency và mọi test case vì chưa chat/gold-set/runtime test.

## Source tool chưa bật

Tại snapshot, không custom Agent nào có RAG semantic/keyword, Wiki, Data Analysis, SQL/database hoặc Product Catalog active. Basic tool không cung cấp dữ liệu nghiệp vụ. No-KB đồng nghĩa Agent chưa thể thực hiện workflow evidence-grounded như thiết kế.

## Mâu thuẫn tài liệu phải xử lý bằng source precedence

| Mâu thuẫn | Cách trình bày trong kho này |
|---|---|
| Custom README ghi `Web: Planned` | Dùng audit/config/handoff mới hơn: đã tạo nhưng chưa phát hành |
| Implementation plan vẫn có checkbox trống | Chỉ xem là ý định lịch sử, không dùng làm completion evidence |
| Planned model/tool khác Web actual | Tách hai bảng; Web actual là trạng thái đã lưu |
| `tests.md` có case/expected | Ghi `Chưa chạy`, không suy ra pass |
| Inventory count khác theo thời điểm | Ghi là snapshot có ngày, không gọi là live current vô thời hạn |

## Khi nào phải kiểm chứng lại

- trước khi bind hoặc đổi KB/data source;
- sau khi đổi model, temperature, reranker, tool, loops, timeout hoặc sharing;
- trước và sau runtime/gold-set test;
- trước publish/share hoặc mở cho nhóm người dùng mới;
- khi source audit thay đổi hoặc snapshot không còn đáp ứng freshness SLA của owner.

