# Audit cấu hình multi-tool và KB GS9 CFL Knowledge Agent — 14/08/2026

## Phạm vi và nguyên tắc

- Mục tiêu: cấu hình tool theo vai trò cho 10 Agent GS9 custom, cập nhật mirror local và tạo KB hướng dẫn Human về 6 Agent mặc định + 10 Agent custom.
- Trình duyệt: trình duyệt tích hợp Codex, phiên VNGGames AI đã đăng nhập.
- Chỉ dùng UI công khai; không dùng private API, cookie, local storage, session storage hoặc credential.
- Không sửa 6 Agent mặc định. Không share, publish, clone, tắt, xóa hoặc gắn dữ liệu nghiệp vụ chưa được audit.
- `Data Private Weapon`, ảnh asset, file credential/system metadata và raw player data nằm ngoài phạm vi.

## Audit nguồn và quyết định binding

### Đã kiểm chứng

- `GS9 Knowledge VNG AI`: tài liệu nền tảng VNG AI, không phải corpus nghiệp vụ game cho toàn bộ Agent.
- `GS9 Knowledge VNG - Image Assets`: asset host; không dùng làm RAG corpus.
- `GS9 CFL Data Daily`: có nội dung KPI tổng hợp phù hợp nhất với KPI Analyst, nhưng Web ACL, retention, freshness và ingestion completeness chưa được xác minh đầy đủ.
- `GS9 CFL PUM`, `GS9 CFL Item Profile`, `GS9 CFL Sentiment Feedback User`: có rủi ro dữ liệu cá nhân, credential/system metadata hoặc nội dung nhạy cảm; không bind as-is.
- Danh sách Web tại thời điểm audit hiển thị `GS9 CFL Data Daily`, `GS9 CFL PUM`, `GS9 CFL Item Profile` thuộc Space `CFL Member`; chỉ nhãn/khả năng truy cập hiện tại không chứng minh quyền dùng cho từng Agent.

### Quyết định

- Không bind bất kỳ KB nghiệp vụ nào trong lần cấu hình này.
- Không bật RAG-4, Wiki-3, Data-2, `Truy vấn CSDL` hoặc `Danh mục sản phẩm` khi chưa có source owner, ACL, retention, sensitivity, freshness và gold-set test.
- KB `GS9 CFL Knowledge Agent` là meta-KB cho Human hiểu/chọn/dùng Agent; không mặc nhiên là dữ liệu nghiệp vụ cho các Agent LiveOps/CS/GM/Product/Data/Marketing.

## Tool surface đã kiểm chứng

| Nhóm | Tool UI | Điều kiện |
|---|---|---|
| Điều phối không cần KB | `Suy nghĩ`; `Lập kế hoạch (todo)`; `Hỏi người dùng` | Có thể bật khi Agent ở Smart mode. |
| RAG-4 | `Tìm theo ngữ nghĩa`; `Tìm theo từ khóa`; `Liệt kê đoạn`; `Thông tin tài liệu` | Cần KB đã chọn và được audit. |
| Wiki-3 | `Tìm wiki`; `Đọc trang wiki`; `Đọc tài liệu nguồn` | Cần KB đã bật Wiki và nguồn được phép. |
| Data-2 | `Lược đồ dữ liệu`; `Phân tích dữ liệu` | Cần bảng/CSV/XLSX đã được curate. |
| Database | `Truy vấn CSDL` | Cần view read-only, allowlist và phạm vi dữ liệu riêng. |
| Catalog | `Danh mục sản phẩm` | Cần catalog read-only đã kiểm chứng game/region/environment. |

`Suy nghĩ` là tên một tool; khác với model-level `Thinking/Chế độ suy nghĩ`, hiện vẫn Off trên 10 Agent custom.

## Snapshot trước mutation

- Chín Smart Agent: chỉ `Hỏi người dùng` (badge 1), no-KB, loop 20, timeout 120 giây, parallel Off.
- `GS9 CS Copilot`: Fast Answer; không có tab Tools và không có explicit tool badge.
- Cả 10: `hosted_vllm/qwen3.6-35b`, temperature 0.7, Thinking Off, reranker trống, image/audio Off, sharing 0, chưa runtime/gold-set test.

## Cấu hình đã lưu và mở lại kiểm chứng

| Agent | ID | Mode | Tool hiệu lực sau lưu | Badge | Bằng chứng |
|---|---|---|---|---:|---|
| GS9 LiveOps Planner | `99ce5c68-e722-47fb-beab-c496433eb3d4` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 Release Reviewer | `d4ec2736-bc1f-4fde-806f-2ade904d13b4` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 Incident Triage | `43a43154-ef15-40c3-99bb-678c3be733ed` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 KPI Experiment Analyst | `37da676c-59ce-4936-9314-5ac4cc3d1a45` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 Economy Offer Analyst | `41524910-bec6-40ff-9b2a-96fa3e84a6e4` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 Player Voice Analyst | `03bbab6e-1315-48ad-a05b-ad19fcb31796` | Smart | `Hỏi người dùng`; `Suy nghĩ` | 2 | Đã cập nhật trợ lý; list badge 2 |
| GS9 CS Copilot | `9ad150d4-6de8-48f5-a2c2-22c008cb3ae5` | Fast Answer | Không có Tools tab/explicit tool | 0 | Giữ nguyên theo mode; list không có badge tool |
| GS9 GM Case Investigator | `01d42d42-dd08-4907-9d4a-913142bc554c` | Smart | `Hỏi người dùng`; `Lập kế hoạch (todo)` | 2 | Đã cập nhật trợ lý; list badge 2 |
| GS9 Player Communications | `4b8e6d78-9217-4dbb-8ab3-919628a48440` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |
| GS9 Knowledge Curator | `2dd80249-7db3-4a63-812a-6eff8fa1d2f6` | Smart | `Hỏi người dùng`; `Suy nghĩ`; `Lập kế hoạch (todo)` | 3 | Đã cập nhật trợ lý; list badge 3 |

Parallel tool calling vẫn Off. Không bật tool gửi, publish, deploy, sửa cấu hình live, account action, sanction, compensation hoặc KB mutation.

## KB GS9 CFL Knowledge Agent

### Đã tạo trên Web

- Tên: `GS9 CFL Knowledge Agent`
- ID: `1d92448f-7ee2-46c4-b202-5efbe9cc5616`
- Tenant hiển thị trong URL: `10012`
- Loại: Tài liệu
- Chiến lược: RAG (vector + từ khóa), quick recommended configuration
- Chat/tóm tắt: `hosted_vllm/qwen3.6-35b`
- Embedding: `text-embedding-3-large`
- Wiki: Off khi tạo nhanh
- Chia sẻ: 0 Space; trạng thái `Của tôi`
- Mô tả: `Cẩm nang cấu hình, vai trò, công cụ, giới hạn và cách sử dụng 6 Agent mặc định cùng 10 Agent GS9 custom.`

### Upload

- Nguồn local: `knowledge/GS9 CFL Knowledge Agent/`.
- Inventory local: đúng 25 Markdown phẳng; 6 trang hướng dẫn chung, 6 hồ sơ default, 10 hồ sơ custom, 3 trang governance; không có non-MD/folder con.
- Validation local: 25 H1 duy nhất, 0 link nội bộ hỏng, 0 pattern secret độ tin cậy cao và không còn folder legacy.
- Review độc lập: PASS sau khi `SRC-CUSTOM-UPDATE` được nối tới audit Web cụ thể này.
- Upload UI: chọn đúng 25 tệp; toast `25 thành công / 0 lỗi`.
- Trạng thái xử lý cuối: `25/25 Hoàn tất`, 0 Đang xử lý, 0 Chờ xử lý, 0 lỗi.

### Chat test Human-facing

- Agent chat: `Quick Answer`; KB được nhắc: `GS9 CFL Knowledge Agent`.
- Prompt tổng hợp vô hại: hỏi Agent nào dùng cho lập kế hoạch LiveOps và kiểm tra phát hành, tool đang bật và bước cần Human phê duyệt.
- Kết quả: chọn đúng `GS9 LiveOps Planner` và `GS9 Release Reviewer`; nêu đúng Ask + Think + Todo, các source-bound tool chưa bật, LiveOps Lead/Event Owner và Release Owner là Human gate.
- Nguồn: UI hiển thị `Nguồn tham khảo (15 tài liệu)`; danh sách có `20-custom-gs9-liveops-planner.md` và `21-custom-gs9-release-reviewer.md`.
- Kết luận runtime: luồng hỏi đáp meta-KB cho trường hợp chọn Agent này **Đã kiểm chứng**. Không suy rộng thành gold-set/runtime pass cho 10 custom Agent.

## Phân loại kết luận

- **Đã kiểm chứng:** UI tool active sau lưu, badge list, ID Agent/KB, model/embedding KB, sharing 0, no-KB trên Agent, inventory 25/25 và chat test chọn Agent/citation nêu trên.
- **Có điều kiện:** RAG/Data/Wiki/SQL/Catalog chỉ sau audit nguồn + ACL + test; runtime usefulness của basic multi-tool cần gold-set.
- **Bị chặn–Chưa xác định:** quota/retention hiệu lực, dữ liệu backend của Product Catalog/Database, runtime accuracy, effective access theo từng Human/Space và lịch sử audit cấp nền tảng.

## Human approval gate

- Mọi gửi/publish/schedule, sửa event/config/live service, account action, sanction, compensation, grant item, thay data/KB và thao tác vận hành live đều cần Human phê duyệt ngoài Agent.
- Human đã giao rõ việc tạo/đổi tên meta-KB và upload 25 Markdown trong task này; đó là mutation KB duy nhất. Không gửi/publish/share, sửa live service, account action, sanction, compensation hoặc grant item.
