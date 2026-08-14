# Review độc lập Task 02 — Ghi quy trình hai KB vào master

**Verdict:** APPROVED  
**Cho phép Task 3:** CÓ

## Tóm tắt

Nội dung hiện tại của `so-tay-tao-knowledge-base-v3.md` khớp đầy đủ với brief và Task 2 trong plan. Bốn snippet Markdown chuẩn trong plan đều xuất hiện đúng một lần, đúng vị trí; metadata phiên bản/ngày, hàng lịch sử, quy trình tám bước và cấu trúc 13 module đều đạt.

## Findings theo severity

### 🔴 Blocker

Không có.

### 🟡 Suggestion

Không có.

### 💭 Nit

Không có.

## Bằng chứng kiểm tra

- Metadata master tại dòng 3–4 là `Phiên bản: 3.1.1` và `Cập nhật: 07/08/2026`, đúng yêu cầu giữ ngày.
- Snippet `Hai KB, hai vai trò` từ plan xuất hiện đúng một lần tại dòng 198–205, trong marker `01-chuan-bi-noi-dung.md` (dòng 106–211), sau phần `Ảnh trong file Markdown: hai mục đích, hai đường dẫn` và trước cảnh báo số liệu. Nội dung giữ đúng hai vai trò KB, vai trò `LOCAL_ASSET`, thứ tự migration an toàn và yêu cầu tái kiểm chứng mapping.
- Snippet `Nạp một bộ Markdown có ảnh` xuất hiện đúng một lần tại dòng 905–911, trong marker `09-van-hanh-documents-wiki-graph.md` (dòng 871–964), ngay sau quy trình `Tải tệp lên`. Cả năm mục khớp nguyên văn plan.
- Quy trình mới trong phần `Ảnh trong chat` xuất hiện đúng một lần tại dòng 1098–1105, trong marker `11-chat-kiem-thu-va-bao-tri.md` (dòng 1054–1145). Có đúng tám bước liên tục theo thứ tự: asset local → KB asset → `image-map.json` → builder/13 file → chỉ nạp 13 MD → test ảnh → kiểm nguồn URI KB asset → giữ dependency. Hai bước cũ yêu cầu dùng cùng KB không còn trong master.
- Hàng lịch sử `3.1.1` khớp nguyên văn plan tại dòng 1363 và đứng ngay trên hàng `3.1.0` tại dòng 1364.
- Parser marker độc lập ghi nhận `13` marker mở, `13` marker đóng, tạo đúng `13` cặp; không có marker lồng, mồ côi hoặc chưa đóng. Tên marker là duy nhất và đúng thứ tự từ `00-gioi-thieu-va-quick-start.md` đến `12-ket-noi-google-drive.md`.
- Checker trích trực tiếp bốn fenced snippet `markdown` của Task 2 trong plan: cả bốn đều có đúng một bản khớp nguyên văn trong master và nằm lần lượt ở module 01, module 09, module 11 và Phụ lục E.

## Phạm vi review

Review này chỉ xác nhận trạng thái nội dung hiện tại theo brief/plan. Workspace không có lịch sử Git nên không thể tái dựng độc lập diff của implementer; điều này không ảnh hưởng kết luận về tính phù hợp của master hiện tại. Không chạy builder vì sẽ ghi lại artifact ngoài phạm vi Task 02. Review không sửa master, 13 module sinh, HTML, image map hoặc live KB.

## Kết luận

Task 02 đáp ứng tiêu chí chấp nhận và không có finding cần sửa. **Cho phép bắt đầu Task 3.**
