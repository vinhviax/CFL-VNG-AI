# Quy tắc cập nhật và kiểm tra mirror Agent

**Loại:** Governance  
**Owner nội dung:** Agent Knowledge Steward  
**Owner nghiệp vụ:** VNG AI Platform Owner  
**Snapshot Web:** 14/08/2026  
**Trạng thái sử dụng:** Checklist bắt buộc trước phát hành  
**Mức bằng chứng:** Quy tắc validation  
**Nguồn chính:** `SRC-AGENT-INDEX`, `SRC-DEFAULT-AUDIT`, `SRC-CUSTOM-AUDIT`

## Cấu trúc

- Folder phải có đúng `25` file `.md`, không có file loại khác và không có folder con.
- Tên file phải khớp danh sách tại [trang giới thiệu](00-gioi-thieu-va-pham-vi.md).
- Có đúng sáu profile `10`–`15` và mười profile `20`–`29`.
- Mỗi file có một H1 duy nhất; toàn corpus không trùng H1.
- Mọi link Markdown nội bộ phải resolve trong folder.

## Metadata và nội dung

- Mọi file có đủ: Loại, Owner nội dung, Owner nghiệp vụ, Snapshot Web, Trạng thái sử dụng, Mức bằng chứng, Nguồn chính.
- Chỉ dùng ba evidence label: `Đã kiểm chứng`, `Có điều kiện`, `Bị chặn–Chưa xác định`.
- Mọi claim cấu hình/trạng thái hiện tại có source ID và ngày snapshot.
- Profile custom tách `Web actual`, `Planned baseline` và `Runtime evidence`.
- Mọi test custom mặc định là `Chưa chạy`; chỉ đổi khi có ngày, runner, result và audit artifact.
- Không mô tả no-KB Agent là grounded, production-ready hoặc đã phát hành.
- Không copy `Web: Planned` từ README custom làm trạng thái hiện tại; dùng source precedence.

## Đối chiếu cấu hình

- Default matrix phải khớp `SRC-DEFAULT-AUDIT`: model, temperature, scope, tools, Top K/threshold, loop/timeout/parallel và caveat.
- Custom common state phải là qwen3.6-35b, temperature `0.7`, Thinking Off, reranker trống, no-KB, image/audio Off, sharing `0`, untested.
- Custom role-based tool phải khớp `SRC-CUSTOM-UPDATE`.
- Chín Smart custom phải là `20` loops, `120s`, parallel Off; CS không có Tools/steps/timeout.
- RAG/Wiki/Data/SQL/Catalog của custom phải ghi `Conditional — chưa enabled`.
- Web Agent ID phải là UUID duy nhất và chỉ xuất hiện trong field identity/source phù hợp.

## Safety

- Không credential, token, cookie/session, secret, PII, raw player record hoặc dữ liệu private.
- Mỗi custom profile có prohibited actions, Human gate, release gate và rollback.
- Không khuyến nghị clone default Agent cho dữ liệu nhạy cảm vì All KB.
- Meta-KB phải được mô tả tách biệt với operational game corpus.

## Quy trình cập nhật

1. Chụp/audit Web read-only; không suy ra runtime từ config.
2. So sánh source mới với source register và ghi phần thay đổi.
3. Cập nhật profile canonical trước, sau đó chooser/matrix/guidance.
4. Chạy validation cấu trúc, H1, links, source labels, forbidden data và invariants.
5. Reviewer nghiệp vụ xác nhận purpose/gate; Platform Owner xác nhận Web actual.
6. Ghi [lịch sử thay đổi](92-lich-su-thay-doi.md) và artifact audit.

## Điều kiện fail

Fail phát hành nếu thiếu profile, link hỏng, actual/planned bị trộn, test chưa chạy bị ghi pass, có secret/PII, source không có ngày, tool custom bị mô tả sai, hoặc claim sẵn sàng vượt quá bằng chứng.

