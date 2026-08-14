# Audit kiểm thử Agent chuyên sâu — 11/08/2026

> Trạng thái: đang hoàn thiện phát hành v3.3.0.  
> Phạm vi: UI `https://vnggames.ai/kb/agents`, Agent disposable và KB TEST được tạo riêng; không gọi private API, không lưu credential/token/private key.

## Mục tiêu và guardrail

- Kiểm thử vận hành lẫn kỹ thuật cho Agent trước khi tách module 13 cũ thành 13–19.
- Giữ nguyên sáu Agent mặc định, Agent test cũ và consumer production trong giai đoạn audit.
- Chỉ tạo resource mang tiền tố `TEST -`; chỉ xóa sau khi bằng chứng đã lưu.
- Dùng dữ liệu tổng hợp ORCHID, không dùng dữ liệu nhân sự/khách hàng thật.
- Request Information chỉ được mở trên UI; các giá trị định danh và URL định danh đã bị che trong ảnh xuất bản.

## Baseline

| Hạng mục | Giá trị trước v3.3.0 | Trạng thái |
|---|---|---|
| Asset host | 34 PNG, 0 Markdown | Đã kiểm chứng trước upload ảnh 35–49 |
| Consumer | 14 Markdown, 0 PNG | Đã kiểm chứng trước rollout |
| Module Agent cũ | `13-tao-va-van-hanh-agent.md`, knowledge ID `957b9bcb-bdc5-41de-ba06-67e489eac1f0` | Đã sao lưu byte-for-byte |
| Backup Markdown cũ | `audit/13-tao-va-van-hanh-agent-before-v3.3.0.md` | SHA-256 `489FDBB1E9E6C541D5B035C6EDFBD32ABE5F08BAE9034F604A3E97473F65D8B7` |
| Backup image map | `audit/image-map-before-agent-deep-split-2026-08-11.json` | SHA-256 `95F3D44EBDD116779B8A0C8EC57AB0E842FF8A625B33F7A7BDB2C3B48C1787F7` |

## Fixture tổng hợp

KB disposable: `TEST - Agent Deep Audit 2026-08-11` (ID `af9b245f-e282-48fd-bf00-ca1bdce0dbc2`).

| File | Dữ liệu oracle | Kết quả ingest |
|---|---|---|
| `TEST-orchid-canonical.md` | ORCHID-731, Nhóm Cam, SLA 4 giờ, P2 | Hoàn tất |
| `TEST-orchid-near-duplicate.md` | Cố ý mâu thuẫn: Nhóm Lam, SLA 9 giờ | Hoàn tất |
| `TEST-kb-type-conflict.md` | Cố ý mâu thuẫn số loại KB consumer | Hoàn tất |
| `TEST-orchid-data.csv` | Hai record canonical/conflicting | Hoàn tất |
| `TEST-orchid-attachment.pdf` | ORCHID-731, Nhóm Cam, SLA 4 giờ | Hoàn tất |

Fixture nằm tại [agent-deep-test-fixtures-2026-08-11](agent-deep-test-fixtures-2026-08-11/). PDF được sinh từ dữ liệu tổng hợp; công cụ Poppler cục bộ không render được vì wrapper thiếu đường dẫn runtime, nhưng file được KB parse thành công và được Agent phân tích qua attachment. Đây là giới hạn visual QA local, không phải blocker ingest/chat.

## Cấu hình Agent disposable

Agent `TEST - Agent Lifecycle Deep Audit 2026-08-11` được tạo với:

- Smart Reasoning; model `hosted_vllm/qwen3.6-35b`; reranker `bge-reranker-v2-m3`.
- Hai KB: KB TEST và `Knowledge VNG AI`.
- Tool đã chọn: Suy nghĩ, Lập kế hoạch (todo), Hỏi người dùng, Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu, Truy vấn CSDL, Phân tích dữ liệu, Lược đồ dữ liệu.
- Max loops 10; timeout 120 giây; gọi công cụ song song tắt ở baseline.

Create lần đầu bị validation “Bật ít nhất một công cụ…”; sau khi chọn tool, create thành công. Đây là bằng chứng preset/mode không tự đảm bảo Agent hợp lệ nếu tool set rỗng.

## Kết quả chat và truy hồi

| Case | Model | Kết quả quan sát | Phân loại |
|---|---|---|---|
| Canonical + conflict | `hosted_vllm/qwen3.6-35b` | 13 bước/17 giây; keyword và semantic search; 4 tệp nguồn; nêu Nhóm Cam/4 giờ và cảnh báo Nhóm Lam/9 giờ | Đã kiểm chứng |
| No-hit | `hosted_vllm/qwen3.6-35b` | 7 bước/8 giây; semantic + keyword; kết luận không có chính sách nghỉ phép 2031 | Đã kiểm chứng |
| Canonical ngắn | `deepseek-v4-flash` | 5 bước/11 giây; trả Nhóm Cam từ `TEST-orchid-canonical.md` | Đã kiểm chứng |
| Greeting | `deepseek-v4-flash` | Phản hồi trực tiếp, không source chip | Đã kiểm chứng về hành vi; không nhìn thấy nhãn classifier nội bộ |
| PDF attachment | `deepseek-v4-flash` | Composer nhận PDF; trả ORCHID-731, Nhóm Cam, 4 giờ, P2 | Đã kiểm chứng |
| Image attachment | `deepseek-v4-flash` | Toast `Định dạng tệp không hỗ trợ` | Bị chặn/có điều kiện; không kết luận VLM hỏng |
| Audio/ASR | UI cấu hình | Tenant không cung cấp ASR model | Bị chặn |
| `@` KB/tệp | UI composer | Dialog liệt kê 2 KB, 5 file TEST và 14 Markdown consumer ở thời điểm audit | Đã kiểm chứng UI; hiệu quả tùy config/model |

Nguồn của canonical query gồm canonical MD, near-duplicate MD, CSV và PDF. Answer đã giải thích near-duplicate không phải nguồn chuẩn thay vì im lặng chọn một giá trị. Đây là gate bắt buộc cho tài liệu hướng dẫn đa nguồn.

## Intent, model, tool và Request Information

- UI có hai mode: Smart Reasoning và Quick Reply; Smart hiển thị năm preset RAG, Wiki, RAG + Wiki, Data Analysis, Custom.
- Sáu Intent thấy được: Greeting Response, Chitchat Response, Follow-up Response, Image Analysis Response, Summarize Response, Document Analysis Response.
- Bốn model thấy được: `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b`, `qwen3.6-plus`; không suy ra tất cả đều còn quota.
- System Prompt UI gợi ý `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`; prompt Intent gợi ý `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`.
- Request Information UI hiển thị request/message/session ID, POST, URL và thời gian. Không sao chép JSON, payload hay định danh vào tài liệu phát hành; ảnh asset 48 che các giá trị này.

## Vòng đời và quyền

- Clone `TEST - Agent Lifecycle Deep Audit 2026-08-11 (Copy)` được tạo.
- Clone đã Disable (toast `Đã tắt trợ lý`) và Enable lại (toast `Đã bật trợ lý`); trạng thái cuối trước cleanup là enabled.
- Menu Agent user-owned có Chat, Edit, Clone, Disable/Enable, Delete.
- UI share cho phép chọn Space và role Chỉ xem/Được chỉnh sửa; audit không gửi lời mời/không add Agent vào Space, nên role end-to-end là **Có điều kiện**.

## Bằng chứng ảnh

Ảnh 35–49 là screenshot UI thực, PNG thật; ảnh 48 được tạo bản che định danh trước khi dùng. Hậu kiểm phát hành đã hoàn tất; 14 raw JPEG trung gian trong `tmp/agent-deep-screens-2026-08-11` được xóa ngày 14/08/2026 sau khi xác nhận asset PNG tương ứng đã có trong asset host local. Map knowledge ID/URI của 15/15 asset nằm tại `audit/agent-deep-image-assets-knowledge-ids-2026-08-11.json`.

## Điều chưa được kết luận

- Không đánh giá chất lượng tương đối của bốn model khi chưa có cùng quota và ba lượt hoàn chỉnh mỗi model.
- Wiki/Data/Schema tools chưa có fixture Wiki/data-source đủ điều kiện để tuyên bố pass end-to-end.
- Image Analysis và ASR chưa pass end-to-end trên tenant hiện tại.
- Không xác nhận quyền share end-to-end hay khôi phục sau xóa Agent.

## Rollback và cleanup dự kiến

1. Nếu ảnh không hoàn tất hoặc không lấy được URI UI hợp lệ: dừng trước strict build, không xóa 34 asset cũ.
2. Nếu Markdown 14–19 fail: giữ module đã hoàn tất, audit lỗi; không đụng module 13 cũ.
3. Chỉ upload module 13 mới sau khi 14–19 có source/ảnh; chỉ xóa live module 13 cũ sau chat-test module mới.
4. Sau audit/live verification, xóa đúng KB TEST và hai Agent `TEST - Agent Lifecycle…`; không xóa hai Agent test cũ.

## Theo dõi pipeline asset sau upload

**Quan sát lúc 20:20 11/08/2026.** Asset host hiển thị đủ 49 PNG. Trong 15 ảnh mới, các ảnh 35, 36, 37, 38, 41, 45, 47 và 48 hiển thị **Hoàn tất**; các ảnh 39, 40, 42, 43, 44, 46 và 49 vẫn hiển thị **Đang hoàn tất** dù chi tiết của từng ảnh đã có đủ các bước Phân tích tài liệu, Chia đoạn, Vector hóa, Đa phương thức và Hậu xử lý.

Đã bấm **Làm mới** đúng một lần trên từng job 39, 40, 42, 43, 44 và 46 sau khi quan sát trạng thái này; trạng thái danh sách chưa đổi trong lần kiểm tra tiếp theo. Job 49 đã được làm mới một lần trước đó với cùng kết quả. Không bấm **Hủy** vì nút này hủy pipeline, không chỉ đóng hộp. Chưa chọn **Phân tích lại** và chưa cập nhật map/strict build khi chưa có URI MinIO hợp lệ cho 15/15 ảnh.

Sau khi lưu quan sát trên, nút **Phân tích lại** được dùng đúng một lần cho bảy ảnh 39, 40, 42, 43, 44, 46 và 49. Đây là retry có căn cứ: UI của từng job đã cho thấy năm bước xử lý hoàn tất nhưng trạng thái tổng không chuyển. UI phản hồi `Đang xử lý` cho ảnh 39 và `Chờ xử lý` cho sáu ảnh còn lại. Không có ảnh nào bị xóa, không có pipeline nào bị hủy và 8 ảnh hoàn tất không bị chạm tới. Cần chờ chu kỳ mới rồi kiểm tra lại 15/15 trước khi lấy URI/map.

**Theo dõi lúc 20:37 11/08/2026.** Sau retry, ảnh 44 và 49 đã chuyển **Hoàn tất**, nên tổng số ảnh mới hoàn tất là 10/15. Năm ảnh 39, 40, 42, 43 và 46 vẫn ở **Đang hoàn tất**. Đã mở chi tiết từng job và dùng **Làm mới** ở chu kỳ retry; detail của cả năm vẫn cho thấy các bước con đã kết thúc, không có thông báo lỗi UI. Đây là trạng thái bị chặn ở hậu xử lý của asset host; không có căn cứ để chạy thêm lần **Phân tích lại**, và không tiếp tục build/map bằng URI suy đoán.

**Theo dõi lúc 20:56 11/08/2026.** Ảnh 39, 40 và 42 đã tự chuyển **Hoàn tất** trong chu kỳ host tiếp theo, đưa tổng lên 13/15. Hai ảnh còn lại 43 và 46 vẫn dừng ở **Đang hoàn tất** sau làm mới chi tiết. Vì lần reanalysis thứ nhất đã chứng minh có thể gỡ kẹt từng phần nhưng hai job này vẫn lặp cùng trạng thái, sẽ chạy **Phân tích lại** lần thứ hai có kiểm soát chỉ cho 43 và 46, sau đó chờ một chu kỳ mới; không retry hàng loạt, không hủy và không sửa mapping trước khi đủ 15/15.

**Theo dõi lúc 21:24 11/08/2026.** Ảnh 43 đã chuyển **Hoàn tất**; ảnh 46 vẫn hiển thị **Đang hoàn tất** trong danh sách sau lần bấm **Làm mới** đúng một lần của chu kỳ hiện tại. Vì vậy tổng là **14/15** và chưa có cơ sở chạy thêm **Phân tích lại** hoặc suy đoán URI MinIO. Không bấm **Hủy**, không thay đổi map và không chạy strict build.

**Kiểm chứng cấu hình tạm lúc 21:24 11/08/2026.** Trên đúng Agent disposable `TEST - Agent Lifecycle Deep Audit 2026-08-11`, tab **Kho tri thức** cho phép thêm `Knowledge VNG - Image Assets` vào hai KB baseline và lưu thành công (thẻ Agent hiển thị 3 KB). Ngay sau đó đã bỏ chính KB asset và lưu lại; thẻ Agent trở về đúng **2** KB / **10** tool baseline. Đây chỉ là kiểm chứng UI về phạm vi KB, không phải bằng chứng URI MinIO và không thay đổi hai Agent test hiện hữu hoặc sáu Agent mặc định.

**Theo dõi lúc 21:34 11/08/2026.** Ảnh 46 vẫn **Đang hoàn tất** sau lần làm mới danh sách của chu kỳ này; mọi ảnh 35–45 và 47–49 đã **Hoàn tất**, nên gate vẫn là 14/15. Không có thao tác hủy, retry mới, map hay build.

**Thử đường nguồn qua Agent lúc 21:34 11/08/2026.** Chỉ trên Agent disposable, đã gắn tạm KB asset (3 KB), mở Chat và hỏi mô tả của `35-agent-che-do-va-preset.png`. Agent trả về **“Trợ lý cần bạn làm rõ”**, nói không thấy tệp trong danh sách tài liệu gần đây; giao diện không xuất source drawer hay URI MinIO. Đã bấm **Bỏ qua**, gỡ KB asset và lưu lại baseline **2 KB / 10 tool**. Kết luận: việc chọn KB asset và luồng Request Information được **Đã kiểm chứng**; suy luận rằng UI Chat là kênh xuất URI MinIO là **Bị chặn/Chưa xác định**. Không dùng dữ liệu nội bộ, API riêng hoặc suy đoán URI thay thế.

**Asset gate lúc 22:17 11/08/2026 — Đã kiểm chứng.** Job 46 đã đổi sang **Xong** ở detail (lần #3, đủ năm giai đoạn) và sau điều hướng/làm mới danh sách cũng hiển thị **Hoàn tất**. Vì vậy ảnh 35–49 là **15/15 Hoàn tất** trong asset host. Mở trang detail UI riêng của từng ảnh, đọc đúng asset đã render và chọn duy nhất `file_path=minio` có đuôi `.png` cho từng filename. Kết quả gồm 15 URI duy nhất được lưu tại `audit/agent-deep-image-assets-knowledge-ids-2026-08-11.json`; không gọi private API, không dùng URI suy đoán và không chọn các bản `.jpg` hậu xử lý.

**Gate local lúc 22:17 11/08/2026 — Đã kiểm chứng.** Sau khi map có đủ 49 ảnh, strict `python scripts\\build_handbook.py` hoàn tất với 20 module và HTML offline. `python -m unittest discover -s tests -v` đạt `Ran 13 tests` / `OK`. Kiểm tra contract chính xác đếm 60 URI `minio://knowledge-base-prd/10012/exports/` và 60 `<!-- LOCAL_ASSET: assets/`; các số 65/61 khi grep thô gồm ví dụ code fence/chú thích, không phải link hoặc metadata phát hành.

**Consumer rollout lúc 22:17 11/08/2026 — Đang xử lý.** Module `14-che-do-preset-prompt-va-intent.md` đã được nạp bằng **Thêm tài liệu → Tải tệp lên**, UI xác nhận `1 thành công / 0 lỗi` và tóm tắt đã lập chỉ mục đúng nội dung. Detail cho thấy 5/5 giai đoạn nhưng trạng thái vẫn **Đang hoàn tất** sau một lần **Làm mới**. Không bấm Hủy, chưa nạp chồng module 15–19 và chưa động tới module 13 cũ.

**Consumer module 14 lúc 22:32 11/08/2026 — Đã kiểm chứng.** Module 14 đã đổi **Hoàn tất**. Chat trực tiếp trên `Knowledge VNG AI` hỏi năm preset Smart Reasoning và vai trò Intent: trả đúng năm preset, giải thích Intent là nhãn điều phối theo lượt chat, có `Nguồn tham khảo (8 tài liệu)` và source drawer chứa chính `14-che-do-preset-prompt-va-intent.md` (2 đoạn). Mở tài liệu từ source drawer hiển thị năm ảnh của module 14 bằng blob render từ nội dung MinIO. Đây là pass source và ảnh; các nguồn cũ xuất hiện đồng thời là kết quả multi-source bình thường, không làm mất nguồn module 14.

**Consumer module 15 lúc 22:32 11/08/2026 — Đang xử lý.** Đã nạp `15-model-reranker-suy-luan-va-quota.md` qua **Thêm tài liệu → Tải tệp lên**, UI xác nhận `1 thành công / 0 lỗi`. Sau polling có trạng thái **Đang hoàn tất**, chưa xác nhận final nên chưa chat-test và chưa nạp module 16.

**Consumer module 15 lúc 22:51 11/08/2026 — Đã kiểm chứng.** Module 15 đã **Hoàn tất**. Chat hỏi vị trí của `bge-reranker-v2-m3` và xử lý `429 insufficient_quota` trả đúng: reranker nằm sau retrieval/filter và trước Top K; quota 429 phải dừng, ghi blocked, không retry vô hạn. Source drawer chứa `15-model-reranker-suy-luan-va-quota.md` (1 đoạn); mở nguồn render ba ảnh module 15. Đây là pass source/ảnh.

**Consumer module 16 lúc 22:51 11/08/2026 — Đang xử lý.** Đã nạp `16-kho-tri-thuc-cong-cu-va-truy-hoi.md` qua **Thêm tài liệu → Tải tệp lên`; UI hiển thị `Chờ xử lý` rồi `Đang hoàn tất` trong polling. Chưa có final/chat-test nên chưa nạp module 17.

**Consumer module 16 lúc 23:12 11/08/2026 — Đã kiểm chứng.** Module 16 đã **Hoàn tất**. Chat hỏi hành vi `Chỉ truy hồi khi được nhắc` và vị trí reranker: câu trả lời đúng rằng không có `@` thì không kỳ vọng tự RAG, và reranker nằm sau candidate/filter/threshold trước Top K. Source drawer chứa module 16; mở nguồn render bảy ảnh (scope, tools, retrieval, multi-KB, `@`, trace và A/B). Đây là pass source/ảnh.

**Consumer module 17 lúc 23:12 11/08/2026 — Đang xử lý.** Đã nạp `17-da-phuong-thuc-va-tep-dinh-kem.md` qua **Thêm tài liệu → Tải tệp lên**. Polling đi từ `Chờ xử lý` sang `Đang hoàn tất`; chưa có final/chat-test nên module 18 chưa được nạp.

**Consumer module 17 lúc 23:32 11/08/2026 — Đã kiểm chứng.** Module 17 đã **Hoàn tất**. Chat trả đúng rằng KB corpus và chat attachment có validation/quyền/model/timing khác nhau, nên không suy ra attachment từ parse KB; tenant thiếu ASR phải ghi **Bị chặn**, không workaround. Source drawer chứa module 17; mở nguồn render bốn ảnh attachment/đa phương thức. Đây là pass source/ảnh.

**Consumer module 18 lúc 23:32 11/08/2026 — Đang xử lý.** Đã nạp `18-chat-nguon-lich-su-va-danh-gia.md` qua **Thêm tài liệu → Tải tệp lên**. Polling đi từ `Chờ xử lý` qua `Đang xử lý` đến `Đang hoàn tất`; chưa có final/chat-test nên module 19 chưa được nạp.

**Consumer module 18 lúc 23:53 11/08/2026 — Đã kiểm chứng.** Module 18 đã **Hoàn tất**. Chat trả đúng rằng feedback chỉ chuyển **Đã xử lý** sau điều tra và bằng chứng hồi quy; Request Information phải che Request/Message/Session ID và URL định danh. Source drawer chứa module 18; mở nguồn render ba ảnh chat/source/feedback. Đây là pass source/ảnh.

**Consumer module 19 lúc 23:53 11/08/2026 — Đang xử lý.** Đã nạp `19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md` qua **Thêm tài liệu → Tải tệp lên**. Polling đã tới **Đang hoàn tất**; chưa có final/chat-test nên chưa nạp module 13 tổng quan mới và không động tới module 13 cũ.

**Consumer module 19 lúc 00:12 12/08/2026 — Đã kiểm chứng.** Module 19 đã **Hoàn tất**. Chat trả đúng bốn xác nhận trước delete (tên, owner, mục đích TEST, audit/backup) và tách rollback cấu hình Agent khỏi rollback nội dung KB. Source drawer chứa module 19; mở nguồn render ảnh vòng đời/chia sẻ. Đây là pass source/ảnh.

**Consumer module 13 mới lúc 00:12 12/08/2026 — Đang xử lý.** Đã nạp `13-agent-tong-quan-va-kien-truc.md` qua **Thêm tài liệu → Tải tệp lên**; consumer tạm có 21 Markdown và UI hiển thị `Chờ xử lý`. Bản cũ `13-tao-va-van-hanh-agent.md` vẫn còn nguyên. Chỉ sau khi module 13 mới Hoàn tất và pass source/ảnh mới được xóa chính xác bản cũ.

**Consumer module 13 mới ngày 12/08/2026 — Đã kiểm chứng.** UI đã chuyển `13-agent-tong-quan-va-kien-truc.md` sang **Hoàn tất**. Chat hỏi ranh giới Agent–Knowledge Base và vị trí Intent trả lời đúng: Agent là lớp điều phối, KB giữ nội dung có thể truy hồi, và Intent là bước phân loại sớm sau khi nhận lượt chat. `Nguồn tham khảo (6 tài liệu)` có chính `13-agent-tong-quan-va-kien-truc.md` (**3 đoạn**); mở nguồn render ảnh hero `Trang danh sách và nút Tạo trợ lý`. Đây là pass nội dung/source/ảnh của bản thay thế.

**Checkpoint cleanup legacy.** Backup nguyên byte `audit/13-tao-va-van-hanh-agent-before-v3.3.0.md` (SHA-256 `489FDBB1E9E6C541D5B035C6EDFBD32ABE5F08BAE9034F604A3E97473F65D8B7`) đã tồn tại trước rollout. Bản live được phép dọn sau checkpoint này là đúng tên `13-tao-va-van-hanh-agent.md`, knowledge ID `957b9bcb-bdc5-41de-ba06-67e489eac1f0`; không phải module 13 mới và không liên quan asset host.

**Consumer legacy cleanup ngày 12/08/2026 — Đã kiểm chứng.** Hộp xác nhận UI ghi đúng `"13-tao-va-van-hanh-agent.md"` và cảnh báo xóa đoạn dữ liệu. Sau xác nhận, danh sách `Knowledge VNG AI` là **20** Markdown: không còn bản legacy, còn `13-agent-tong-quan-va-kien-truc.md`, không có hàng PNG và cả 20 hàng Markdown đều **Hoàn tất**. Không xóa asset host.

**Hậu kiểm no-hit ngày 12/08/2026 — Đã kiểm chứng.** Câu hỏi `Chính sách nghỉ phép năm 2031 của Agent là gì?` trả lời rõ không có thông tin trong Knowledge Base, phân loại no-hit và không tạo chính sách tưởng tượng. Câu trả lời vẫn có source chip do corpus chứa chính quy tắc kiểm thử no-hit; điều này không phải bằng chứng rằng một chính sách 2031 tồn tại.

**Cleanup TEST ngày 12/08/2026 — Đã kiểm chứng.** Đã xóa qua hộp xác nhận đúng tên KB `TEST - Agent Deep Audit 2026-08-11` (ID `af9b245f-e282-48fd-bf00-ca1bdce0dbc2`) và hai Agent disposable `TEST - Agent Lifecycle Deep Audit 2026-08-11` cùng `(Copy)`. Hậu kiểm danh sách Agent: còn 8 Agent, gồm đủ sáu Agent mặc định và hai Agent test hiện hữu `Kiểm thử Agent Knowledge VNG 2026-08-11`/`- Bản sao`; không còn Agent lifecycle TEST. Hai KB phát hành vẫn hiện diện.

**Inventory asset host ngày 12/08/2026 — Đã kiểm chứng.** `Knowledge VNG - Image Assets` hiển thị `Tất cả tài liệu 49`. Lọc trạng thái **Hoàn tất** vẫn cho toàn bộ danh sách 49 (không có hàng PNG chưa hoàn tất); lọc định dạng **MD** cho 0 hàng. Vì vậy asset host là **49 PNG, 0 Markdown, 49/49 Hoàn tất**. Đây là hậu kiểm UI, không suy đoán URI và không xóa asset nào.

**Reviewer độc lập ngày 12/08/2026 — APPROVED.** Lượt review đọc-only ban đầu chặn vì `AGENTS.md` còn ghi giữ marker của 14 phần. Đã tái tạo bằng invariant một dòng, xác định đây là checklist cũ sót lại, sửa riêng thành 20 phần, rồi strict build và toàn bộ 13 test lại **OK**. Reviewer kiểm tra lại và xác nhận 20 module, 49 PNG/signature, 49 URI MinIO duy nhất, 60 ảnh MinIO hoạt động, 60 `LOCAL_ASSET` và không còn instruction 14 phần. Reviewer không sửa file và không truy cập live UI.
