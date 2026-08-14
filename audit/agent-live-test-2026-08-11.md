# Audit Agent Knowledge VNG — 11/08/2026

**Bắt đầu:** 15:57 GMT+7, 11/08/2026  
**Trạng thái:** **Hoàn tất** — ma trận Agent, asset, module consumer, chat-test, inventory và review cuối đã đóng  
**Phạm vi:** trang Agents, Agent test chuyên dụng, chat/feedback test và hai KB được người dùng chỉ định.

## Ranh giới an toàn

- Chỉ mutation `Kiểm thử Agent Knowledge VNG 2026-08-11`, bản sao của nó, chat/feedback test và hai KB đã chỉ định.
- Không sửa, tắt, nhân bản hoặc xóa sáu Agent mặc định.
- Không dùng **Thay toàn bộ**; không xóa Agent, KB, Markdown hay ảnh.
- Agent test chỉ dùng `Knowledge VNG AI` làm nguồn truy hồi; không dùng KB asset làm nguồn hỏi đáp.
- Không lưu credential, token, private key hoặc dữ liệu cá nhân.

## Baseline trước mutation

### Local

| Hạng mục | Kết quả |
|---|---:|
| Master | v3.1.1; 13 cặp marker |
| Module sinh tự động | 13 |
| PNG local | 25 |
| Mapping / URI duy nhất | 25 / 25 |
| Kiểm thử | `Ran 11 tests`; `OK` |
| Git/worktree | Workspace không phải Git repository; dùng snapshot/audit làm checkpoint |

### Live lúc 15:56–15:57 GMT+7

| Vai trò | Knowledge Base | Inventory quan sát | Trạng thái |
|---|---|---|---|
| Asset host | `Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`) | 25 hàng `.png`, 0 `.md` | 25/25 **Hoàn tất** |
| Consumer | `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`) | 13 hàng `.md`, 0 PNG độc lập | 13/13 **Hoàn tất** |

Snapshot phục hồi: `audit/image-map-before-agent-extension-2026-08-11.json`.

## Đối tượng kiểm thử

| Đối tượng | Giá trị |
|---|---|
| Agent chính | `Kiểm thử Agent Knowledge VNG 2026-08-11` |
| Agent ID | `3c644ac2-ab5f-4141-959d-f1fa13ce8c41` |
| Bản sao | `Kiểm thử Agent Knowledge VNG 2026-08-11 - Bản sao` |
| Mô tả | `Agent test nội bộ dùng Knowledge VNG AI để kiểm chứng RAG, Intent, nguồn tham khảo và ảnh.` |
| KB truy hồi | Chỉ `Knowledge VNG AI`; loại tệp `MD` |
| KB asset | Không chọn làm corpus; chỉ cung cấp URI MinIO cho Markdown |

Sáu Agent mặc định `Quick Answer`, `Smart Reasoning`, `Hybrid Researcher`, `Wiki Questioner`, `Data Analyst` và `FPA Analyst` không bị mutation.

## Ma trận kiểm thử Agent

| Nhóm | Hạng mục | Kết quả | Trạng thái |
|---|---|---|---|
| Danh sách | Tất cả/Của tôi/Mặc định/Được chia sẻ/Đã đánh dấu/Gần đây/Space | Hiển thị đúng phạm vi và bộ đếm | Đã kiểm chứng |
| Danh sách | Tìm kiếm, list/grid, sao/bỏ sao | Hoạt động trên Agent test | Đã kiểm chứng |
| Chế độ chạy | Suy luận thông minh / Trả lời nhanh | Mô tả lần lượt là suy nghĩ nhiều bước và phản hồi trực tiếp; preset chỉ hiện ở lượt quan sát Suy luận thông minh | Đã kiểm chứng UI |
| Preset | RAG, Wiki, RAG + Wiki, Phân tích dữ liệu, Tùy chỉnh | Có năm lựa chọn | Đã kiểm chứng UI |
| Tạo mới | Sáu tab | Thông tin cơ bản, Mô hình, Kho tri thức, Công cụ, Truy hồi, Đa phương thức | Đã kiểm chứng |
| Chỉnh sửa | Tab Chia sẻ | Xuất hiện thêm khi sửa; Space `CFL Member`, vai trò Chỉ xem/Được chỉnh sửa | Quan sát; không gửi chia sẻ |
| Intent | Greeting/Chitchat/Follow-up | Trả lời trực tiếp hoặc theo ngữ cảnh | Pass |
| Intent | Document Analysis | Phân tích `00-gioi-thieu-va-quick-start.md` | Pass |
| Intent | Summarize | Tóm tắt cùng file đúng 5 gạch đầu dòng | Pass |
| Intent | Image Analysis | Composer hiện preview nhưng request không mang ảnh; Agent nói không nhận được ảnh | Có điều kiện/chưa pass |
| Model | Danh sách model | `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b`, `qwen3.6-plus` | Đã kiểm chứng UI |
| Model | Quota | deepseek và một lượt qwen3.6-plus trả `429 insufficient_quota` | Có điều kiện |
| Model | Hosted Qwen | Trả lời câu ngoài KB và không bịa | Pass |
| KB | Ba phạm vi và lọc loại tệp | All/selected/no KB; danh sách PDF, DOCX, TXT, MD, CSV, XLSX, XLS, JSON, PPTX, HTML, MSG, EML | Đã kiểm chứng |
| KB | `Chỉ truy hồi khi được nhắc` | Bật/tắt được; đã khôi phục tắt | Đã kiểm chứng |
| KB | `@` KB/tệp | Gỡ chip thì không có phạm vi; thêm `Knowledge VNG AI (13)` kích hoạt truy hồi | Pass có điều kiện |
| KB | Tổng hợp sau `@` | Hosted model lộ `[[chunk#12]]` thay vì câu tổng hợp | Có điều kiện model/prompt |
| Công cụ | Bộ hiệu lực | Suy nghĩ, Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu | Đã kiểm chứng |
| Công cụ | Giới hạn | 10 vòng; timeout 120 giây; song song bật/tắt được và để tắt | Đã kiểm chứng |
| Truy hồi | Giá trị | vector topK 10; keyword 0,3; vector 0,5; rerank topK 5; rerank 0,5 | Đã kiểm chứng/khôi phục |
| Đa phương thức | Ảnh/VLM | Bật tải ảnh, chọn `qwen3.6-plus`; lỗi ở bước truyền attachment | Có điều kiện |
| Đa phương thức | Audio/ASR | Picker báo chưa có model và yêu cầu liên hệ admin | Bị chặn theo tenant |
| Vòng đời | Tạo, sửa, lưu, mở lại | Giá trị lưu bền | Pass |
| Vòng đời | Nhân bản | Bản sao kế thừa model/KB/tool và được đổi tên | Pass |
| Vòng đời | Tắt/bật | Bản sao đã tắt rồi bật lại; trạng thái cuối bật | Pass |
| Vòng đời | Xóa | Không thao tác | Chưa kiểm chứng |
| Chat RAG | Google Drive | Dùng `12-ket-noi-google-drive.md`, hiện source chip và sáu ảnh | Pass |
| Chat ngoài KB | Chính sách nghỉ phép 2027 | Nói không tìm thấy, không bịa | Pass |
| Feedback | Helpful/Unhelpful + bình luận | Tạo đúng hai phản hồi test | Pass |
| Feedback | Thời gian/Agent/loại/bình luận/tìm kiếm | Các bộ lọc thu hẹp đúng dữ liệu | Pass |
| Feedback | Hộp xử lý | Mở được toàn bộ hội thoại liên quan | Pass |
| Feedback | Trạng thái | Chuyển phản hồi chưa hữu ích `Mới → Đang xem → Đã xử lý` | Pass |

## Cấu hình Agent chính sau kiểm thử

| Tab | Giá trị đáng chú ý |
|---|---|
| Thông tin cơ bản | Prompt preset RAG và prompt theo Intent để mặc định nếu không cần ghi đè |
| Mô hình | `hosted_vllm/qwen3.6-35b`; reranker `bge-reranker-v2-m3`; nhiệt độ đã thử ở `0,2` |
| Kho tri thức | Selected KB → `Knowledge VNG AI`; file type `MD`; chỉ truy hồi khi được nhắc = tắt |
| Công cụ | Suy nghĩ + bốn công cụ tìm/đọc tài liệu; 10 vòng; 120 giây; song song tắt |
| Truy hồi | 10 / 0,3 / 0,5 / 5 / 0,5 |
| Đa phương thức | Ảnh bật với VLM qwen; audio tắt vì không có ASR |

Biến System Prompt quan sát ở Suy luận thông minh: `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`. Biến cho Prompt theo Intent: `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`.

## Phiên chat và bằng chứng

- Intent, tài liệu và ảnh: `https://vnggames.ai/kb/chats/e3810c0c-692a-425a-bdbb-c8a5f3ce0c21?agent_id=3c644ac2-ab5f-4141-959d-f1fa13ce8c41`.
- RAG Google Drive và câu ngoài KB: `https://vnggames.ai/kb/chats/ff3f1910-ee11-482d-9577-20dff4b4b92b?agent_id=3c644ac2-ab5f-4141-959d-f1fa13ce8c41`.
- Module Agent sau phát hành: `https://vnggames.ai/kb/chats/2446f763-3758-4179-b67c-84ca561bfc64?agent_id=3c644ac2-ab5f-4141-959d-f1fa13ce8c41`.
- Ảnh `33-agent-chat-nguon-va-anh.png` ghi lại nguồn Markdown và ảnh render trong chat.
- Ảnh `34-agent-danh-gia-cau-tra-loi.png` ghi lại 2 feedback, tỷ lệ tích cực 50%, một mục Mới và một mục Đã xử lý.
- Ảnh audit `agent-final-chat-source-and-image-2026-08-11.png` ghi module 13 làm nguồn, ảnh tab Kho tri thức đã render và câu ngoài phạm vi được từ chối.

Hai bình luận test:

1. `Kiểm thử nội bộ 11/08/2026 — câu trả lời RAG đúng nguồn Markdown và hiển thị ảnh minh họa.`
2. `Kiểm thử nội bộ 11/08/2026 — UI nhận ảnh ở composer nhưng request không truyền ảnh tới Agent, nên Image Analysis trả không nhận được ảnh.`

## Kiểm chứng module Agent sau phát hành

| Phép thử | Kết quả | Trạng thái |
|---|---|---|
| Sáu tab + định nghĩa Intent + sáu Intent | Trả đúng sáu tab và sáu tên Intent; lượt siết nguồn gắn `13-tao-va-van-hanh-agent.md` cho từng phần | Pass |
| Mở nguồn tham khảo | Drawer mở đúng `13-tao-va-van-hanh-agent.md`, trạng thái pipeline **Xong** | Pass |
| Ảnh tab Kho tri thức | Câu trả lời hiển thị ảnh `Chọn phạm vi Knowledge Base và loại tệp`; DOM có ảnh visible, nguồn blob đã render; citation là module 13 | Pass |
| Câu ngoài phạm vi | Không đưa ra số ngày nghỉ phép 2027; nói KB không có dữ liệu và không suy đoán | Pass |

Agent vẫn chọn đúng `Knowledge VNG AI`, loại tệp `MD`, và switch `Chỉ truy hồi khi được nhắc` ở trạng thái tắt trước chat-test này.

## Mutation live đã thực hiện

1. Tạo Agent chính và bản sao; sửa/lưu, sao/bỏ sao, tắt/bật bản sao.
2. Tạo chat test và hai feedback test; chuyển feedback chưa hữu ích sang Đã xử lý.
3. Tải chín ảnh `26-agent-tong-quan-danh-sach.png` đến `34-agent-danh-gia-cau-tra-loi.png` vào `Knowledge VNG - Image Assets` bằng **Thêm tài liệu → Tải tệp lên**.
4. Không gửi chia sẻ, không xóa Agent, không xóa tài liệu/ảnh, không mutation sáu Agent mặc định.
5. Strict build sinh 14 module; upload duy nhất `13-tao-va-van-hanh-agent.md` vào `Knowledge VNG AI` bằng **Thêm tài liệu**. Pipeline báo **Xong** sau 9m46s; knowledge ID `957b9bcb-bdc5-41de-ba06-67e489eac1f0`; consumer đạt 14/14 Markdown **Hoàn tất**, 0 PNG.

## Toàn vẹn ảnh

Ảnh chụp từ browser ban đầu mang payload JPEG dù tên `.png` (`FF D8 FF E0`). Trước upload, cả chín file đã được transcode sang PNG thật và xác nhận magic bytes `89 50 4E 47 0D 0A 1A 0A`. Không có bản JPEG gắn sai đuôi nào được upload.

Inventory asset tăng từ 25 lên 34 ngay sau upload. Cả chín ảnh đã ở trạng thái **Hoàn tất**; pipeline chi tiết của ảnh cuối báo **Xong**, có tóm tắt, phân đoạn và hậu xử lý Wiki. Chín knowledge ID cùng chín URI `.png` thật, duy nhất đã được ghi tại `audit/agent-image-assets-knowledge-ids-2026-08-11.json`; `image-map.json` đã được mở rộng từ 25 lên 34 ánh xạ.

## Kết quả cuối và rollback

Asset, module và chat-test live đã qua gate. Nếu inventory/review cuối phát hiện sai lệch:

- dừng bước phụ thuộc;
- giữ nguyên 14 Markdown consumer hiện hành, không tự xóa module Agent để “rollback”;
- không xóa 25 ảnh nền hoặc 9 ảnh Agent khi Markdown còn tham chiếu;
- dùng `audit/image-map-before-agent-extension-2026-08-11.json` để đối chiếu mapping trước thay đổi;
- chỉ thay mapping bằng URI thật sau quy trình asset host → map → strict build → phát hành MD → chat-test.

Inventory cuối ghi nhận asset 34/34 PNG **Hoàn tất**, consumer 14/14 Markdown **Hoàn tất**. Reviewer độc lập `Avicenna` trả **APPROVED**, không có finding Critical/Major/Minor.
