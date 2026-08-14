# Trạng thái Knowledge Base VNG

**Ngày snapshot:** 14/08/2026  
**Phiên bản:** 3.3.0  
**Giai đoạn:** Workspace đã chuẩn hóa; 10 custom Agent LiveOps đã có basic tool theo vai trò; meta-KB `GS9 CFL Knowledge Agent` đã phát hành 25/25 Markdown; GitHub handoff đã publish lên `main`, không có mutation live đang chạy.

## Kết quả hiện tại

- Root chính thức: `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`.
- `knowledge/` quản lý mirror/dữ liệu của các KB trên Web; `agent/` quản lý artifact cấu hình/test/handoff của Agent.
- Tên chính thức hiện tại: `GS9 Knowledge VNG AI`, `GS9 Knowledge VNG - Image Assets` và `GS9 CFL Knowledge Agent`; giữ nguyên chính xác tên trên Web.
- Consumer local: 20 Markdown + `image-map.json`, không có PNG.
- Asset host local: 49 PNG, không có Markdown.
- Master v3.3.0 đã được phục hồi từ 20 module phát hành sau khi file bị thất lạc trong lần di chuyển. Dry-run vòng lặp so sánh 20/20 module không có sai lệch ngoài hai thay đổi đường dẫn có chủ đích.
- Builder/test đã chuyển khỏi `knowledge-vng/` sang hai folder tên KB Web.
- Gate mới nhất: strict build PASS; 20 module; HTML offline tự chứa; `Ran 16 tests`, `OK`.
- Ba module local `01`, `09`, `11` có sửa SOP có chủ đích để thay 14/34 và layout cũ bằng 20/49 cùng tên/path `GS9`; chưa phát hành live trong đợt chuẩn hóa này.
- Audit chỉ-đọc 14/08/2026 của 6 Agent mặc định VNG AI đã hoàn tất; bằng chứng tổng ở `audit/default-agent-readonly-audit-2026-08-14.md` và bản ghi từng Agent ở `agent/*-config.md`.
- Đã tạo và lưu cấu hình 10 custom Agent LiveOps trên Web. Snapshot sau tạo: `Tất cả 18`, `Của tôi 12`, `Mặc định 6`, shared-with-me `0`. Cả 10 chưa bind KB, sharing `0`, chưa publish/share và chưa chat/runtime test; bằng chứng tại `audit/liveops-custom-agent-creation-2026-08-14.md`.
- Web actual chung: preset `Hỏi đáp RAG`, model `hosted_vllm/qwen3.6-35b`, reranker trống, temperature `0.7`, Thinking Off, KB `Không dùng kho tri thức`, image/audio Off. Planner, Release, Incident, KPI, Economy, Communications và Curator có `Hỏi người dùng` + `Suy nghĩ` + `Lập kế hoạch (todo)`; Player Voice có Ask + Think; GM có Ask + Todo; `GS9 CS Copilot` là Fast Answer không có Tools tab. Chín Smart Agent giữ `20` loop, `120s`, parallel Off.
- Identity/config UI-visible của 10 Agent là **Đã kiểm chứng**; behavior từ prompt là **Có điều kiện**; runtime/quality là **Bị chặn–Chưa xác định**.
- Local meta-KB có đúng 25 Markdown phẳng tại `knowledge/GS9 CFL Knowledge Agent/`: 6 hướng dẫn chung, 6 hồ sơ Agent mặc định, 10 hồ sơ Agent custom và 3 trang governance; không có binary/folder con/link hỏng/pattern secret độ tin cậy cao.
- Web meta-KB `GS9 CFL Knowledge Agent` (`1d92448f-7ee2-46c4-b202-5efbe9cc5616`) có 25/25 Markdown `Hoàn tất`, sharing 0. Chat test dùng Quick Answer đã chọn đúng LiveOps Planner + Release Reviewer, nêu đúng tool/Human gate và hiển thị `Nguồn tham khảo (15 tài liệu)`, gồm hai hồ sơ Agent tương ứng.
- Git handoff đích là `https://github.com/vinhviax/CFL-VNG-AI.git`, branch `main`. Người dùng đã phê duyệt publish toàn bộ project để dùng cá nhân; credential/private key/cache là ngoại lệ bắt buộc và được chặn bằng `.gitignore`.
- Prompt chuyển máy/phiên nằm tại `NEXT_SESSION_PROMPT.md`; audit publish nằm tại `audit/github-publish-2026-08-14.md`.
- Snapshot commit `1502d798debe46674cb5271fc92bd0c6240f2452` đã push thành công; `origin/main` khớp local HEAD tại gate sau push. Commit handoff cuối tiếp tục cập nhật tài liệu trạng thái này.

## Snapshot live cuối đã kiểm chứng

| Vai trò | KB | Inventory |
|---|---|---|
| Consumer | `GS9 Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`) | 20 MD, 0 PNG; 20/20 Hoàn tất |
| Asset host | `GS9 Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`) | 49 PNG, 0 MD; 49/49 Hoàn tất |
| Agent meta-KB | `GS9 CFL Knowledge Agent` (`1d92448f-7ee2-46c4-b202-5efbe9cc5616`) | 25 MD, 0 binary; 25/25 Hoàn tất; sharing 0 |

Snapshot live này kế thừa kiểm chứng rollout ngày 12/08/2026; việc đổi prefix theo quy định công ty không phải một lần upload hoặc migration mới.

## Việc đã chuẩn hóa local

- Khôi phục master và sinh lại HTML offline.
- Vòng phục hồi ban đầu giữ nguyên nội dung 20 module; sau đó sửa đúng ba SOP đang hoạt động còn count/path cũ. Không đổi các kết quả lịch sử có ghi rõ thời điểm test.
- Có backup nguyên byte trước build tại `audit/workspace-normalization-prebuild-2026-08-14.zip`.
- Có backup năm file context cũ tại `audit/workspace-docs-before-normalization-2026-08-14.zip`.
- Các cache, ảnh tạm đã phát hành, output trùng và fixture audit upload cũ được dọn/lưu trữ theo audit chuẩn hóa workspace.

## Backlog

- Upload folder thật và kiểm tra folder con.
- Xác định điều kiện sinh node Tổng hợp/So sánh.
- Kiểm thử Google Drive nhiều chu kỳ: thêm, sửa, đổi tên, di chuyển, xóa và quyền.
- Kiểm chứng Notion/NAS bằng credential test quyền tối thiểu.
- Kiểm chứng Image Analysis, audio/ASR và quota model khi tenant đủ điều kiện.
- Audit nội dung, owner, ACL, retention và dữ liệu nhạy cảm của từng KB nghiệp vụ trước khi đề xuất allowlist cho 10 Agent; không bind chỉ dựa trên tên KB.
- Lập và chạy gold-set/chat/runtime test riêng cho từng Agent chỉ khi được giao; planned baseline có thể khác Web actual và Web actual là nguồn chuẩn cho trạng thái đang lưu.
- Khi thay tool, ID, mode hoặc quyền Agent, cập nhật `agent/`, 25 Markdown meta-KB và Web KB theo cùng một audit có ngày; không trình bày planned claim như Web actual.
- Rà soát credential hiện hữu trong dữ liệu của các KB CFL khác; không tự xóa khi chưa xác định dependency và phương án thay thế.
- Trên máy tiếp theo, xác minh `git status --short --branch` sạch và chạy `git pull --ff-only origin main` trước khi làm việc.

## Quy tắc giữ nguyên

- Không xóa 49 PNG/asset KB khi Markdown còn tham chiếu URI MinIO.
- Không dùng asset host làm corpus hỏi đáp thông thường.
- Không sửa trực tiếp module hoặc HTML; sửa master rồi strict build.
- Không upload dữ liệu private vào consumer dùng chung khi chưa có phê duyệt rõ ràng.
- Không dùng meta-KB Agent như corpus nghiệp vụ game và không tự gán KB CFL khác cho custom Agent khi chưa audit owner/ACL/retention/sensitivity/freshness.
