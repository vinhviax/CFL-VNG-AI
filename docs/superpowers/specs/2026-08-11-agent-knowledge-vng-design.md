# Thiết kế kiểm thử và tài liệu Agent Knowledge VNG

**Ngày:** 11/08/2026  
**Trạng thái:** **Hoàn tất ngày 11/08/2026**; reviewer độc lập **APPROVED**  
**Phạm vi giao diện:** `https://vnggames.ai/kb/agents` và giao diện chat liên quan  
**Đích phân phối:** `Knowledge VNG AI` và `Knowledge VNG - Image Assets`, tenant `10012`

## 1. Mục tiêu

Bổ sung một hướng dẫn Agent đã được kiểm thử trên giao diện thật vào bộ sổ tay Knowledge VNG hiện hành. Hướng dẫn phải giải thích cách Agent trò chuyện với Human, sử dụng Knowledge Base để truy hồi thông tin, cấu hình từng tab, vận hành vòng đời Agent, kiểm thử chat và xử lý đánh giá câu trả lời.

Kết quả đích là một module Markdown mới trong `Knowledge VNG AI` và chín ảnh PNG minh họa mới trong `Knowledge VNG - Image Assets`. Không tạo Knowledge Base container thứ ba. Cụm từ “thêm một KB liên quan tới Agent” trong yêu cầu được thực hiện bằng một knowledge document Markdown mới dùng chung consumer hiện hành.

## 2. Phương án kiến trúc được chọn

Agent được bổ sung thành module thứ 14 của master hiện tại:

- Nguồn chuẩn duy nhất vẫn là `so-tay-tao-knowledge-base-v3.md`.
- Module sinh tự động mới là `knowledge-vng/13-tao-va-van-hanh-agent.md`.
- Builder tăng `EXPECTED_MODULE_COUNT` từ 13 lên 14.
- HTML offline được sinh lại từ master và chứa cả phần Agent cùng ảnh nhúng data URI.
- `Knowledge VNG AI` chuyển từ 13 Markdown lên 14 Markdown, không nhận PNG độc lập.
- `Knowledge VNG - Image Assets` chuyển từ 25 PNG lên 34 PNG, không nhận Markdown.

Phương án này giữ nguyên luồng nguồn chuẩn → strict build → Markdown phân phối, không tạo artifact sửa tay và không thêm pipeline thứ hai.

## 3. Artifact và tên file

### 3.1. Module Agent

Tên module: `13-tao-va-van-hanh-agent.md`.

Nội dung tối thiểu:

1. Agent là gì và quan hệ Human → Agent → KB → câu trả lời.
2. Tổng quan trang Trợ lý, phạm vi, tìm kiếm, list/grid, đánh dấu và Spaces.
3. Sáu tab của hộp Tạo trợ lý.
4. Hai chế độ chạy và năm preset.
5. System Prompt, biến khả dụng và Prompt theo intent.
6. Model, reranker, nhiệt độ và chế độ suy nghĩ.
7. Phạm vi KB, lọc loại tệp và truy hồi khi được nhắc.
8. Danh mục công cụ, vòng lặp, timeout và gọi song song.
9. Top K và các ngưỡng truy hồi/rerank.
10. Ảnh, âm thanh và điều kiện đa phương thức.
11. Tạo, sửa, nhân bản, đánh dấu, tắt/bật lại Agent test.
12. Giao diện Chat, tệp đính kèm, nhắc tri thức/tệp, model và nguồn tham khảo.
13. Đánh giá hữu ích/chưa hữu ích và hộp xử lý phản hồi.
14. Checklist kiểm thử, bảo trì, giới hạn và phân loại mức độ chắc chắn.

### 3.2. Ảnh mới

Chín PNG mới được đánh số liên tục:

1. `26-agent-tong-quan-danh-sach.png`
2. `27-agent-thong-tin-co-ban-va-intent.png`
3. `28-agent-cau-hinh-mo-hinh.png`
4. `29-agent-kho-tri-thuc.png`
5. `30-agent-cong-cu.png`
6. `31-agent-chien-luoc-truy-hoi.png`
7. `32-agent-cau-hinh-da-phuong-thuc.png`
8. `33-agent-chat-nguon-va-anh.png`
9. `34-agent-danh-gia-cau-tra-loi.png`

Mỗi file phải là PNG thật với magic bytes `89 50 4E 47 0D 0A 1A 0A`. Ảnh local nằm trong `knowledge-vng/assets/`; bản live nằm trong KB asset và cấp URI `minio://` duy nhất. Module chỉ dùng link MinIO hoạt động và comment `LOCAL_ASSET`; HTML offline dùng ảnh local.

## 4. Agent test và ranh giới an toàn

Tạo một Agent test riêng tên `Kiểm thử Agent Knowledge VNG 2026-08-11`. Nếu cần kiểm thử Nhân bản/Tắt, dùng bản sao tên `Kiểm thử Agent Knowledge VNG 2026-08-11 - Bản sao`.

Nguyên tắc:

- Không sửa, tắt hoặc nhân bản sáu Agent mặc định để làm test.
- Không xóa Agent hoặc dữ liệu live trong phạm vi triển khai này.
- Chỉ liên kết Agent test với `Knowledge VNG AI`; không liên kết trực tiếp `Knowledge VNG - Image Assets` làm nguồn hỏi đáp.
- Chỉ mutation trên Agent test, bản sao của nó, hai KB đã được chỉ định và chat/feedback do chính lượt test tạo ra.
- Không lưu token, credential, thông tin cá nhân hoặc dữ liệu không thuộc workspace.
- Nếu thao tác Tắt không có đường bật lại rõ ràng, dừng trước thao tác và ghi là chưa kiểm chứng thay vì để lại trạng thái khó phục hồi.

## 5. Cấu hình chuẩn để kiểm thử

Agent test dùng cấu hình nền sau:

- Chế độ chạy: `Suy luận thông minh`.
- Preset: `Hỏi đáp RAG`.
- Model: `deepseek-v4-flash` nếu còn khả dụng tại thời điểm test; nếu không, dùng model khả dụng được giao diện cung cấp và ghi tên/ngày trong audit.
- Reranker: `bge-reranker-v2-m3` nếu còn khả dụng.
- Nhiệt độ: `0,2` để giảm biến thiên khi đối chiếu.
- KB: `Kho tri thức đã chọn` → `Knowledge VNG AI`.
- Loại tệp: `MD`.
- `Chỉ truy hồi khi được nhắc`: tắt cho lượt kiểm thử tự động truy hồi; sau đó bật tạm thời để kiểm tra hành vi `@` và trả lại trạng thái tắt.
- Công cụ RAG: tìm ngữ nghĩa, tìm từ khóa, liệt kê đoạn và thông tin tài liệu; các công cụ khác chỉ bật khi test đúng chức năng tương ứng.
- Vòng lặp/timeout: giữ giá trị preset trừ khi test nút tăng/giảm; sau test trả về giá trị nền.
- Đa phương thức: bật tạm thời ảnh và âm thanh để kiểm tra điều khiển Chat; kết quả ASR phụ thuộc file/model phải được phân loại Có điều kiện nếu chưa có bằng chứng đầu-cuối.

System Prompt phải yêu cầu trả lời bằng ngôn ngữ của Human, dựa trên bằng chứng KB, nêu rõ khi không tìm thấy thông tin và không lộ ID nội bộ. Sáu intent được kiểm tra độc lập: Greeting, Chitchat, Follow-up, Image Analysis, Summarize và Document Analysis.

## 6. Ma trận kiểm thử live

### 6.1. Danh sách và vòng đời Agent

- Mở các phạm vi Tất cả, Của tôi, Mặc định, Được chia sẻ, Đã đánh dấu, Gần đây và Space hiện có.
- Thử tìm kiếm theo tên/mô tả và đổi list/grid.
- Tạo Agent test, mở chat, chỉnh sửa và lưu lại.
- Đánh dấu rồi bỏ đánh dấu Agent test.
- Nhân bản Agent test; kiểm tra tên, preset, model, KB và tool được sao chép.
- Chỉ thử Tắt/bật lại trên bản sao nếu giao diện cho thấy đường phục hồi rõ ràng.

### 6.2. Sáu tab tạo/chỉnh sửa

- Thông tin cơ bản: hai chế độ, năm preset, tên, emoji, mô tả, prompt, biến và intent.
- Cấu hình mô hình: bốn model đang hiển thị tại ngày khảo sát, reranker, nhiệt độ và switch suy nghĩ.
- Kho tri thức: ba phạm vi, chọn nhiều KB, lọc 12 loại tệp và switch `@`.
- Công cụ: từng nhóm công cụ, danh sách hiệu lực, vòng lặp, timeout và gọi song song.
- Chiến lược truy hồi: Top K vector, ngưỡng từ khóa/vector, Top K rerank và ngưỡng rerank.
- Đa phương thức: bật/tắt ảnh và âm thanh; xác nhận điều khiển tương ứng trong Chat.

### 6.3. Chat với Human

- Mở cuộc trò chuyện mới và lịch sử.
- Kiểm tra câu hỏi gợi ý.
- Chọn Agent, model, đính kèm tệp và nhắc KB/tệp.
- Gửi câu chào để kiểm tra intent không truy hồi.
- Gửi câu nghiệp vụ có đáp án trong `Knowledge VNG AI` để kiểm tra truy hồi và nguồn Markdown.
- Gửi câu không có trong KB để kiểm tra phản hồi không bịa.
- Gửi câu hỏi yêu cầu ảnh để kiểm tra URI MinIO và render.
- Nếu có file ảnh/âm thanh test an toàn, kiểm tra upload và phản hồi; nếu thiếu model/ASR phù hợp thì ghi Có điều kiện.

### 6.4. Đánh giá câu trả lời

- Tạo ít nhất một đánh giá Hữu ích và một Chưa hữu ích có bình luận ghi rõ đây là test nội bộ ngày 11/08/2026.
- Kiểm tra bộ lọc thời gian, Agent, loại phản hồi và Có bình luận.
- Kiểm tra Tổng quan và Hộp xử lý.
- Với phản hồi test chưa hữu ích, kiểm tra luồng Cần xử lý → Đang xem → Đã xử lý nếu các nút tồn tại và chỉ tác động bản ghi test.

## 7. Luồng ảnh và phân phối

1. Kiểm thử Agent và chụp đủ chín ảnh local.
2. Kiểm tra PNG signature, kích thước và nội dung không lộ credential.
3. Tạo snapshot `image-map.json` trước thay đổi trong `audit/`.
4. Upload chín PNG bằng **Thêm vào** vào `Knowledge VNG - Image Assets`.
5. Chờ 9/9 ảnh Hoàn tất; ghi knowledge ID và URI MinIO vào audit mới.
6. Mở rộng `image-map.json` từ 25 lên 34 ảnh; giữ metadata KB/tenant và thêm provenance `26-34`.
7. Cập nhật master, module marker, mục lục, lịch sử phiên bản và các tài liệu kiến trúc.
8. Nâng builder/test lên 14 module và 34 ảnh; chạy strict build.
9. Upload riêng `13-tao-va-van-hanh-agent.md` bằng **Thêm vào** vào `Knowledge VNG AI`.
10. Chờ tài liệu Hoàn tất, chat test nguồn/ảnh và kiểm tra inventory live.

Không dùng **Thay toàn bộ**. Không thay hoặc gỡ 13 Markdown cũ nếu byte/nội dung của chúng không đổi. Không upload PNG độc lập vào consumer và không xóa ảnh khỏi asset KB.

## 8. Thay đổi local dự kiến

- Sửa `so-tay-tao-knowledge-base-v3.md`, nâng phiên bản lên 3.2.0 và thêm module 13.
- Sinh `knowledge-vng/13-tao-va-van-hanh-agent.md` và cập nhật HTML offline.
- Thêm ảnh 26–34 vào `knowledge-vng/assets/`.
- Mở rộng `knowledge-vng/image-map.json`.
- Sửa `scripts/build_handbook.py` và `tests/test_build_handbook.py` từ 13 lên 14 module, 25 lên 34 ảnh.
- Cập nhật `AGENTS.md`, `PROJECT.md`, `DECISIONS.md`, `STATUS.md`, `HANDOFF.md` theo inventory mới.
- Tạo audit Agent ngày 11/08/2026, snapshot map trước thay đổi và JSON knowledge ID/URI cho chín ảnh cùng module mới.

Workspace hiện không phải Git repository, nên không thể tạo commit cho spec hoặc thay đổi. Việc kiểm chứng dựa trên file hiện hành, audit, output build/test và trạng thái live.

## 9. Xử lý lỗi và rollback

- Nếu bất kỳ ảnh nào không Hoàn tất, không cập nhật map/build bản bàn giao.
- Nếu URI trùng hoặc không kết thúc `.png`, dừng và sửa asset trước khi build.
- Nếu strict build/test thất bại, không upload module Agent.
- Nếu module live thất bại xử lý, giữ 13 Markdown cũ nguyên trạng và ghi audit; retry bằng parser khác chỉ khi có bằng chứng cụ thể.
- Nếu chat không đọc được module hoặc ảnh không render, không công nhận hoàn tất; giữ asset host và điều tra mapping/module.
- Snapshot map trước thay đổi và audit knowledge ID là checkpoint phục hồi; không sửa snapshot để khớp trạng thái mới.

## 10. Tiêu chí hoàn tất

Local:

- Master v3.2.0 có đúng 14 cặp marker module.
- Strict build báo `Build complete`, 14 module và HTML offline.
- Toàn bộ test hiện có kết thúc `OK`.
- Có đúng 34 PNG local hợp lệ, 34 URI MinIO duy nhất và metadata map đúng KB asset cùng tenant `10012`.
- Có 45 link ảnh MinIO hoạt động và 45 `LOCAL_ASSET` nếu mỗi ảnh Agent xuất hiện đúng một lần.
- Module Agent không có link ảnh local hoạt động; HTML nhúng ảnh và không phụ thuộc tài nguyên live.

Live:

- `Knowledge VNG - Image Assets`: 34 PNG, 0 MD; chín ảnh mới Hoàn tất.
- `Knowledge VNG AI`: 14 MD, 0 PNG; module Agent mới Hoàn tất.
- Agent test truy hồi được module Agent từ consumer, trả nguồn Markdown đúng và render ảnh MinIO.
- Không có Agent mặc định hoặc dữ liệu ngoài phạm vi bị sửa.
- Audit, `STATUS.md` và `HANDOFF.md` ghi ngày, bằng chứng, việc còn điều kiện và bước tiếp theo.
