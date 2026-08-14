# Verification cuối — Agent Knowledge VNG 11/08/2026

**Trạng thái:** **APPROVED**  
**Phạm vi:** module Agent thứ 14, chín ảnh Agent, hai KB hiện hành, Agent/chat/feedback test và artifact local v3.2.0.

## Kết quả chính

- Master v3.2.0 có đúng 14 cặp marker; module Agent được sinh bởi builder, không sửa tay.
- `Knowledge VNG - Image Assets`: 34 PNG, 0 MD; 34/34 **Hoàn tất**.
- `Knowledge VNG AI`: 14 MD, 0 PNG; 14/14 **Hoàn tất**.
- Agent test chỉ dùng consumer làm KB trả lời; module 13 mở đúng nguồn, ảnh Agent render và câu ngoài phạm vi không bị bịa.

## Verification local

| Gate | Bằng chứng | Kết quả |
|---|---|---|
| Strict build | `python scripts\build_handbook.py` | `Build complete`; 14 module; HTML offline |
| Test hồi quy | `python -m unittest discover -s tests -v` | `Ran 11 tests`; `OK` |
| Module | 14 `.md`; 13 module nền vẫn tồn tại | Pass |
| Ảnh local | 34 PNG; 25 ảnh nền vẫn tồn tại; toàn bộ signature PNG hợp lệ | Pass |
| Map | 34 key, 34 URI `.png` MinIO duy nhất, đúng tenant `10012` | Pass |
| Liên kết ảnh | 45 MinIO + 45 `LOCAL_ASSET`; active local link trong generated module = 0 theo test | Pass |
| Module Agent | Một H1, chín MinIO, chín `LOCAL_ASSET` | Pass |
| HTML offline | Có mục Agent, chín ảnh data URI, ảnh mở zoom được | Pass |
| Secret scan | Không thấy payload private key/token theo pattern vật liệu bí mật | Pass |

## Verification live

| Hạng mục | Bằng chứng | Kết quả |
|---|---|---|
| Chín ảnh Agent | 9 knowledge ID + 9 URI duy nhất; pipeline từng ảnh **Xong** | Pass |
| Module Agent | `957b9bcb-bdc5-41de-ba06-67e489eac1f0`; parser mặc định; pipeline **Xong** sau 9m46s | Pass |
| Inventory asset | 34 hàng PNG, 34 trạng thái **Hoàn tất**, không có hàng MD | Pass |
| Inventory consumer | 14 hàng MD, 14 trạng thái **Hoàn tất**, không có hàng PNG | Pass |
| Nguồn module mới | Drawer mở đúng `13-tao-va-van-hanh-agent.md` | Pass |
| Sáu tab và Intent | Trả đúng định nghĩa, sáu Intent, sáu tab; citation từng phần là module 13 trong lượt siết nguồn | Pass |
| Ảnh Agent | Ảnh `Chọn phạm vi Knowledge Base và loại tệp` visible trong chat và có citation module 13 | Pass |
| Ngoài phạm vi | Không đưa ra số ngày nghỉ phép 2027; nói KB không có dữ liệu | Pass |
| An toàn Agent | Sáu Agent mặc định không mutation; Agent test/bản sao hoạt động; switch yêu cầu `@` đã trả về tắt | Pass |

## Mục có điều kiện hoặc chưa kiểm chứng

- `Image Analysis Response`: composer từng hiện preview nhưng request test không truyền ảnh tới Agent; chưa chứng minh lỗi VLM.
- Audio/ASR: bị chặn vì tenant không có ASR model.
- `deepseek-v4-flash` và một lượt `qwen3.6-plus`: gặp `429 insufficient_quota`; hosted Qwen dùng được cho gate cuối.
- Một lượt `@Knowledge VNG AI` với hosted model lộ handle `[[chunk#12]]`; đây là vấn đề model/prompt sau retrieval, không phải bằng chứng switch `@` không hoạt động.
- Chia sẻ chỉ quan sát role; không gửi chia sẻ. Xóa Agent không được thao tác.

## Bằng chứng

- [Audit Agent](../../../audit/agent-live-test-2026-08-11.md)
- [Snapshot inventory live cuối](../../../audit/final-agent-live-inventory-2026-08-11.json)
- [Chín ID/URI ảnh Agent](../../../audit/agent-image-assets-knowledge-ids-2026-08-11.json)
- [ID module Agent](../../../audit/agent-markdown-knowledge-id-2026-08-11.json)
- [Ảnh chat nguồn và ảnh Agent](../../../audit/agent-final-chat-source-and-image-2026-08-11.png)
- [Kế hoạch triển khai](../plans/2026-08-11-agent-knowledge-vng-implementation-plan.md)

## Review độc lập

Reviewer `Avicenna` chạy ở chế độ chỉ đọc và trả verdict **APPROVED**:

- Critical: không có.
- Major: không có.
- Minor: không có.

Reviewer đối chiếu được 14 module, 34 PNG thật, 34 URI duy nhất, 45 MinIO/`LOCAL_ASSET`, 0 active local image link và 11 test; không phát hiện credential hoặc mâu thuẫn sự thật mang tính chặn.
