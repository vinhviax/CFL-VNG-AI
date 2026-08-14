# Tiến độ mở rộng Agent Knowledge VNG — 11/08/2026

**Trạng thái:** **Hoàn tất**  
**Đặc tả:** [Thiết kế Agent](../specs/2026-08-11-agent-knowledge-vng-design.md)  
**Kế hoạch:** [Implementation plan](../plans/2026-08-11-agent-knowledge-vng-implementation-plan.md)  
**Audit live:** [Agent live test](../../../audit/agent-live-test-2026-08-11.md)

## Tiến độ theo gate

| Gate | Trạng thái | Bằng chứng hiện tại |
|---|---|---|
| Baseline và checkpoint | Hoàn tất | 25 PNG asset, 13 MD consumer, strict build v3.1.1 và snapshot map trước mở rộng |
| Kiểm thử bề mặt Agent | Hoàn tất | Danh sách, hai chế độ, năm preset, sáu tab tạo và tab Chia sẻ khi sửa |
| Intent và Chat | Hoàn tất có điều kiện | Greeting/Chitchat/Follow-up/Document/Summarize pass; Image Analysis lỗi truyền attachment; ASR thiếu model |
| Vòng đời Agent | Hoàn tất | Tạo, sửa/lưu, sao/bỏ sao, nhân bản, tắt/bật; không xóa, không gửi chia sẻ |
| Feedback | Hoàn tất | Hai feedback test, bộ lọc, Hộp xử lý và Mới → Đang xem → Đã xử lý |
| Chín PNG local | Hoàn tất | 26–34 đã transcode thành PNG thật và kiểm tra signature |
| Upload asset live | Hoàn tất | Inventory 34 PNG; 9/9 ảnh Agent **Hoàn tất**; 9 knowledge ID và 9 URI `.png` duy nhất đã ghi audit |
| Master/builder/test | Hoàn tất | Strict build sinh 14 module và HTML offline; 34 URI, 45 link/`LOCAL_ASSET`; `Ran 11 tests`, `OK` |
| Upload module Agent | Hoàn tất | `13-tao-va-van-hanh-agent.md` Xong sau 9m46s; consumer 14/14 MD Hoàn tất; knowledge ID đã ghi audit |
| Chat test module mới | Hoàn tất | Sáu tab/Intent dùng đúng nguồn module 13; ảnh Kho tri thức render; câu nghỉ phép 2027 bị từ chối, không bịa |

## Kết quả live Agent đáng chú ý

- Agent chính: `Kiểm thử Agent Knowledge VNG 2026-08-11`, ID `3c644ac2-ab5f-4141-959d-f1fa13ce8c41`.
- Agent chỉ bind `Knowledge VNG AI`, file type `MD`; không dùng KB asset làm corpus.
- RAG Google Drive mở đúng nguồn `12-ket-noi-google-drive.md` và render ảnh MinIO.
- Câu ngoài KB được từ chối đúng với model hosted.
- `deepseek-v4-flash` và một lượt `qwen3.6-plus` gặp `429 insufficient_quota`.
- `@Knowledge VNG AI` kích hoạt retrieval khi switch yêu cầu nhắc được bật; một lượt hosted model lộ handle `[[chunk#12]]`.
- Composer hiện preview ảnh nhưng không chuyển attachment tới Agent; audio bị chặn vì tenant chưa có ASR model.

## TDD và local checkpoint

Hai test mục tiêu đã thất bại đúng lý do trước implementation:

1. Map 25 key không phủ chín PNG mới.
2. Builder kỳ vọng 13 module nhưng fixture yêu cầu 14.

Sau đó `EXPECTED_MODULE_COUNT` được nâng lên 14 và unit test fixture 14 module đã xanh. Test map được giữ đỏ cho tới khi có đủ URI live thật; chưa dùng placeholder và chưa chạy strict build bàn giao.

## Bước tiếp theo

Không còn gate bắt buộc. Chỉ tiếp tục các mục backlog trong `STATUS.md` khi người dùng cấp điều kiện/quyền tương ứng.
