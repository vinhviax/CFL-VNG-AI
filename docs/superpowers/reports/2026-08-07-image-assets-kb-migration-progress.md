# Tiến độ migration Knowledge VNG Image Assets

Ngày thực hiện: 07/08/2026  
Plan: `docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md`

**Trạng thái:** Đã đóng; 10/10 task hoàn tất. Đây là hồ sơ lịch sử, không phải task đang hoạt động.

| Task | Trạng thái | Bằng chứng / ghi chú |
|---|---|---|
| 1. Thêm test bảo vệ kiến trúc KB asset | Hoàn tất | Implementer PASS; reviewer APPROVED; test metadata, link local và magic bytes PNG đạt |
| 2. Ghi quy trình hai KB vào master | Hoàn tất | Master v3.1.1; kiến trúc 25 PNG / 13 MD và quy trình asset host → map → build → consumer đã được ghi |
| 3. Nạp 25 ảnh vào KB asset mới | Hoàn tất | Live inventory cuối: 25 PNG, 25 trạng thái **Hoàn tất**, 0 MD |
| 4. Thu thập 25 URI và cập nhật image map | Hoàn tất | 25 URI `.png` duy nhất; 14 payload JPEG gắn sai đuôi đã được transcode thành PNG thật, thay thế và audit |
| 5. Sinh lại và kiểm tra artifact local | Hoàn tất | Strict build đạt; 13 module, 36 link MinIO, 36 `LOCAL_ASSET`, HTML offline v3.1.1; baseline cuối 11/11 test |
| 6. Thay 13 Markdown trong KB sử dụng | Hoàn tất | 13 bản hiện hành **Hoàn tất**; retry file 11 và replacement cuối file 12 đều có audit |
| 7. Kiểm thử chat và nguồn MinIO mới | Hoàn tất | 3/3 trước cleanup PASS; hai lượt hậu-cleanup PASS; chat cuối xác minh cả URI ảnh và link đã rebase |
| 8. Gỡ 11 PNG khỏi KB sử dụng | Hoàn tất | Xóa từng ID sau gate chat; consumer còn đúng 13 MD, 0 PNG; asset KB vẫn 25 PNG; xem `task-08-consumer-png-cleanup.md` |
| 9. Ghi audit và cập nhật tài liệu bàn giao | Hoàn tất | Có audit migration tổng hợp; design spec đã đánh dấu triển khai; project/status/handoff đã cập nhật |
| 10. Verification cuối và bàn giao | Hoàn tất | Review vòng hai APPROVED; strict build và 11/11 test đạt; xem `task-10-final-verification.md` |

## Trạng thái live cuối đã quan sát

- `Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`): 25 PNG, 0 MD; 25/25 **Hoàn tất**.
- `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`): 13 MD, 0 PNG; 13/13 **Hoàn tất**.
- Chat cuối `2625ff6e-7e92-46d3-9fa4-eee81a1bf63c`: ảnh lọc tệp/tag render; 7 nguồn đều là Markdown; đoạn nguồn chứa đúng URI `minio://knowledge-base-prd/10012/exports/f0c0c37a-0e8c-44a2-ba64-abf67d5667ee.png` và link audit `../audit/...`.

## Quy tắc an toàn còn hiệu lực

- Không xóa KB `Knowledge VNG - Image Assets` hoặc bất kỳ PNG nào trong đó khi Markdown còn tham chiếu URI MinIO.
- Không nạp PNG độc lập trở lại `Knowledge VNG AI`; ảnh cho chat phải đi qua URI trong Markdown.
- Mọi thay đổi asset tiếp theo phải đi đúng thứ tự asset host → map → strict build → thay Markdown → chat test → cleanup consumer.
- Workspace không phải Git repository; checkpoint phục hồi là snapshot mapping, backup byte nguồn, audit ID và kết quả test.
