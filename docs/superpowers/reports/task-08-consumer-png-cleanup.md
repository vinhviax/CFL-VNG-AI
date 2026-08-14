# Task 08 — Dọn 11 PNG khỏi Knowledge VNG AI

Ngày thực hiện: 07/08/2026  
Consumer: `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`)  
Asset host: `Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`)

## Điều kiện trước khi xóa

- 13 Markdown mới đã hoàn tất và được đối chiếu.
- Ba phép thử chat ảnh trước cleanup đều PASS.
- ID của 11 PNG cần dọn đã được chụp tại `audit/consumer-png-deleted-knowledge-ids-2026-08-07.json`.
- 25 PNG trong asset KB nằm ngoài phạm vi cleanup.

## Thực hiện và kết quả

- Xóa từng PNG 15–25 khỏi consumer theo đúng tên và knowledge ID; không xóa hàng loạt mù.
- Inventory consumer sau cleanup: **13 MD, 0 PNG**, 13/13 **Hoàn tất**.
- Inventory asset KB sau cleanup: **25 PNG, 0 MD**, 25/25 **Hoàn tất**.
- Chat hậu-cleanup vẫn render ảnh Google Drive; nguồn tham khảo chỉ còn `.md` và đoạn nguồn chứa đúng URI MinIO trong asset map.

## Kết luận

**PASS.** Kiến trúc đích đã đạt: asset KB sở hữu 25 PNG; consumer chỉ sở hữu 13 Markdown và dùng URI trong Markdown để hiển thị ảnh.
