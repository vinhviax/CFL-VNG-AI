# Agent — đoạn prompt bắt Agent trả kèm hình ảnh

**Ngày soạn:** 16/08/2026 · **Trạng thái:** **đã áp lên 10/10 Agent custom**, chưa chat-test

## Đã triển khai — 16/08/2026

Agent chèn đoạn luật (bản tiếng Anh) vào cuối `System Prompt`, ngay trước `Reply in {{language}}.`, cho cả 10 Agent `GS9 CFL *` qua giao diện Web. Xác minh bằng cách mở lại từng Agent và đọc ngược giá trị `System Prompt`:

| Agent | Độ dài prompt sau khi chèn | Có luật ảnh |
|---|---:|---|
| `GS9 CFL Knowledge Curator` | 1518 | ✅ |
| `GS9 CFL KPI Experiment Analyst` | 1480 | ✅ |
| `GS9 CFL LiveOps Planner` | 1693 | ✅ |
| `GS9 CFL Release Reviewer` | 1519 | ✅ |
| `GS9 CFL Incident Triage` | 1515 | ✅ |
| `GS9 CFL Economy Offer Analyst` | 1491 | ✅ |
| `GS9 CFL Player Voice Analyst` | 1468 | ✅ |
| `GS9 CFL GM Policy Advisor` | 1702 | ✅ |
| `GS9 CFL Player Communications` | 1457 | ✅ |
| `GS9 CFL CS Copilot` | 1441 | ✅ |

Cả 10 prompt gốc đều kết thúc bằng `Reply in {{language}}.` nên chèn được đúng vị trí, không phải nối vào cuối.

**Cảnh báo về `GS9 CFL CS Copilot`:** đây là Agent **duy nhất không gắn kho tri thức nào** (xác nhận trực tiếp trên danh sách Agent — không có badge KB, khác 9 Agent còn lại). Đoạn luật đã dán nhưng **hiện chưa có tác dụng** vì không có nguồn truy hồi nào để lấy URI ảnh. Nó sẽ tự có hiệu lực khi Agent này được bind KB.

**Binding đã xác minh:** `GS9 CFL Knowledge Curator` gắn `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI` — do gắn KB có ảnh nên đây là Agent phù hợp nhất để chat-test luật này.

## Vấn đề

Agent mô tả hình bằng lời nhưng không trả ra link ảnh, nên người dùng không thấy hình trong câu trả lời.

Nguyên nhân: tài liệu nguồn có nhúng URI `minio://` nhưng prompt hệ thống không yêu cầu Agent giữ lại và phát ra URI đó. Mô hình coi URI là nhiễu và lược đi khi tóm tắt.

Điều kiện cần trước khi đoạn prompt này có tác dụng:

1. Tài liệu trong KB phải **đã nhúng URI `minio://` còn sống**. Prompt không tự tạo ra được ảnh.
2. Agent phải **bind KB** chứa tài liệu đó.
3. Nên bật `Tải ảnh` + VLM để Agent đọc được nội dung ảnh (đã bật cho 10 Agent custom theo DEC-049).

## Đoạn prompt bổ sung (tiếng Anh, khớp prompt hiện có)

Chèn vào cuối `System Prompt`, trước câu `Reply in {{language}}.`:

```text
When a retrieved source contains an image reference in the form ![alt](minio://...), reproduce that exact markdown image line in your answer at the point where it illustrates your explanation. Copy the URI character for character. Never invent, shorten, guess or reconstruct an image URI, and never present an image that does not appear in the retrieved sources. If several images are relevant, include each one next to the step or claim it supports rather than grouping them at the end. If no retrieved source contains an image, answer normally and do not mention that images are missing.
```

## Bản tiếng Việt (dùng nếu Agent viết prompt bằng tiếng Việt)

```text
Khi nguồn truy hồi có tham chiếu ảnh dạng ![mô tả](minio://...), hãy chép nguyên dòng markdown đó vào câu trả lời, đặt đúng chỗ mà nó minh họa cho nội dung. Chép URI chính xác từng ký tự. Tuyệt đối không tự bịa, rút gọn, đoán hay dựng lại URI ảnh, và không đưa ra ảnh không có trong nguồn truy hồi. Nếu có nhiều ảnh liên quan, đặt từng ảnh cạnh bước hoặc luận điểm mà nó minh họa, không dồn hết xuống cuối. Nếu nguồn không có ảnh nào thì trả lời bình thường, không cần nói là thiếu ảnh.
```

## Vì sao viết như vậy

| Câu trong prompt | Chặn lỗi gì |
|---|---|
| `reproduce that exact markdown image line` | Mô hình hay diễn giải thành *"xem hình bên dưới"* thay vì phát ra link |
| `Copy the URI character for character` | URI là UUID; sai một ký tự là ảnh chết |
| `Never invent, shorten, guess or reconstruct` | Chặn mô hình bịa URI trông hợp lệ — lỗi này khó phát hiện vì link vẫn đúng định dạng |
| `next to the step or claim it supports` | Chặn thói quen dồn hết ảnh xuống cuối, mất liên kết với nội dung |
| `do not mention that images are missing` | Chặn câu thừa *"tài liệu không có hình minh họa"* ở mọi câu trả lời không liên quan ảnh |

## Cách kiểm chứng sau khi dán

1. Hỏi câu **buộc** phải có hình: *"Tab Tổng quan của KB Tài liệu có những gì? Cho tôi xem hình minh họa."*
2. Xác nhận ảnh **hiện thật trong câu trả lời**, không chỉ là mô tả bằng lời.
3. Đối chiếu URI trong câu trả lời với URI trong tài liệu nguồn — phải trùng khít.
4. Hỏi một câu **không** liên quan ảnh, xác nhận Agent không chèn ảnh bừa và không than phiền thiếu ảnh.

## Chưa kiểm chứng

| Hạng mục | Trạng thái |
|---|---|
| Đoạn prompt này có làm Agent phát ra URI hay không | **Chưa chat-test** — soạn ngày 16/08/2026, chưa dán lên Agent nào |
| Nền tảng có render `minio://` thành ảnh trong câu trả lời của Agent không | Đã kiểm chứng ở **chat KB**; chưa kiểm chứng riêng ở **chat Agent** |
| Hành vi khi Agent bind nhiều KB và ảnh nằm ở KB khác với tài liệu | Chưa thử |
| Ảnh hưởng tới độ dài câu trả lời và quota token | Chưa đo |

## Ghi chú cấu hình phát hiện khi soạn

`agent/GS9 CFL CS Copilot/config.md` (và 3 file config khác) **tự mâu thuẫn**: dòng `Knowledge Base` ghi `Không dùng kho tri thức`, nhưng dòng `Trạng thái` ngay dưới lại ghi *"đã bind KB theo cột trên"*. Câu trạng thái là template dùng chung, chưa sửa theo từng Agent.

Nếu Agent thật sự chưa bind KB thì đoạn prompt trên **không có tác dụng** — không có nguồn truy hồi thì không có URI nào để trả về. Phải xác minh binding trên Web trước khi kết luận prompt hỏng.
