<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 14 - Agent: chế độ, preset, prompt và Intent {#14-che-do-preset-prompt-va-intent}

## Khái niệm

Tab **Thông tin cơ bản** quyết định Agent được nhận diện thế nào và lựa chọn khởi đầu nào được áp dụng. UI đã quan sát có hai chế độ chạy:

- **Suy luận thông minh**: mô tả là suy nghĩ nhiều bước/phân tích sâu; hiển thị control **Loại trợ lý** (preset).
- **Trả lời nhanh**: mô tả là phản hồi trực tiếp; trong lượt quan sát control preset không còn hiển thị.

Năm preset dưới Suy luận thông minh là **Hỏi đáp RAG**, **Hỏi đáp Wiki**, **Kết hợp RAG + Wiki**, **Phân tích dữ liệu** và **Tùy chỉnh**. Preset điền System Prompt, gợi ý tool và phạm vi KB; nó là baseline để kiểm tra, không thay thế kiểm thử sau khi lưu.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/35-agent-che-do-va-preset.png -->
![Chế độ chạy và preset Hỏi đáp RAG](minio://knowledge-base-prd/10012/exports/a1ebe886-714d-4fc3-b3e9-d3cbe005cfbb.png)

*Ảnh 14.1 – Hai mode, preset và sáu tab của hộp Tạo trợ lý.*

## Bảng control

| Control | Mục đích | Thiết lập khởi đầu an toàn | Cần xác minh sau lưu |
|---|---|---|---|
| Tên/mô tả/icon | Nhận diện và tìm Agent | Tên nêu use case + owner | Không trùng Agent đang vận hành |
| Chế độ | Kiểu điều phối | Smart cho RAG/tool nhiều bước | Thời gian và trace phù hợp |
| Preset | Seed prompt/tool | RAG hoặc Tùy chỉnh cho Knowledge VNG | Không có tool thừa/thiếu |
| System Prompt | Luật chung của mọi lượt | Chỉ dùng nguồn, nêu nguồn, no-hit không bịa | Câu đúng/no-hit tuân thủ |
| Prompt Intent | Luật riêng cho một loại lượt | Để trống để dùng template nếu chưa test | Không phá luật chung |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/36-agent-system-prompt-va-bien.png -->
![System Prompt và biến UI gợi ý](minio://knowledge-base-prd/10012/exports/079fd918-899a-4c52-8ca7-7ec71d62b407.png)

*Ảnh 14.2 – System Prompt quan sát được và các biến chỉ nên dùng đúng cú pháp UI.*

System Prompt Smart Reasoning quan sát biến `{{knowledge_bases}}`, `{{current_time}}`, `{{language}}`. Prompt theo Intent gợi ý `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}`, `{{language}}`. Chỉ vì một biến được gợi ý không có nghĩa nó có dữ liệu hữu ích trong mọi tình huống; phải kiểm tra qua chat và source trace.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/37-agent-intent-va-prompt-ghi-de.png -->
![Intent và prompt theo Intent trong một cấu hình đã mở](minio://knowledge-base-prd/10012/exports/af8c66a4-3940-4c99-8a3e-bd4164a95aeb.png)

*Ảnh 14.3 – Prompt theo Intent là lớp ghi đè theo lượt; dùng template hoặc để trống khi chưa có case hồi quy.*

## SOP

1. Chọn mode theo độ phức tạp, sau đó chọn preset gần use case nhất.
2. Viết prompt chính theo năm phần: vai trò; dữ liệu được phép; quy tắc nguồn; no-hit/mâu thuẫn; định dạng câu trả lời.
3. Không nhét secret, token, dữ liệu HR nhạy cảm hoặc instruction trái chính sách vào prompt.
4. Chỉ thêm prompt Intent khi đã có một hành vi cần khác biệt rõ và một test case tái lập.
5. Mỗi lần sửa prompt, chạy cùng bộ câu cơ sở rồi lưu câu/nguồn trước–sau.

## Data flow

```text
Human message → classifier nhận Intent
  → System Prompt (luật chung)
  → nếu có: Prompt của Intent ghi đè/bổ sung cho lượt đó
  → tools + KB/file scope → model tổng hợp
```

`Intent` là **nhãn mục đích của một lượt chat**, không phải KB, tool hay model. Nó quyết định chọn prompt theo Intent và hướng điều phối; hành vi retrieval chỉ có thể được kết luận sau khi quan sát trace.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/27-agent-thong-tin-co-ban-va-intent.png -->
![Danh sách Intent và vùng prompt ghi đè](minio://knowledge-base-prd/10012/exports/431c4578-8b28-4d38-b1cc-1a27717a23c7.png)

*Ảnh 14.4 – Tab cơ bản chứa prompt chính, dropdown Intent và prompt chuyên biệt.*

| Intent UI | Công dụng kỳ vọng | Bằng chứng/giới hạn 11/08/2026 |
|---|---|---|
| Greeting Response | Chào hỏi | **Đã kiểm chứng:** phản hồi trực tiếp, không source chip |
| Chitchat Response | Hội thoại xã giao | Có trên UI; cần test riêng theo prompt tenant |
| Follow-up Response | Hỏi tiếp trong session | Có trên UI; test phải giữ session và source trước đó |
| Image Analysis Response | Đọc ảnh | Có trên UI; attachment ảnh bị từ chối ở test hiện tại |
| Summarize Response | Tóm tắt | Có trên UI; file/nguồn quyết định context thật |
| Document Analysis Response | Phân tích tệp | **Đã kiểm chứng** với PDF ORCHID attachment |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/38-agent-intent-trace-runtime.png -->
![Trace greeting thực tế](minio://knowledge-base-prd/10012/exports/75cca568-97e1-4f0c-a121-4e2f47a1d2be.png)

*Ảnh 14.5 – Greeting runtime trả lời trực tiếp; UI không hiển thị nhãn classifier nên đây là quan sát hành vi, không phải bằng chứng nội bộ về thuật toán.*

## Ma trận kiểm thử

| Biến đổi một lần | Input | Kỳ vọng quan sát |
|---|---|---|
| Smart ↔ Quick | cùng câu RAG | Trace/tool/độ sâu có thể khác; không tự suy chất lượng hơn |
| RAG preset ↔ Custom | ORCHID-731 | Kiểm tra tool, nguồn và no-hit thay vì chỉ nhìn câu văn |
| Prompt chính | no-hit 2031 | Nhận thiếu dữ liệu, không tạo chính sách |
| Greeting intent | lời chào | Phản hồi lịch sự, không truy hồi vô ích |
| Document intent | PDF attachment | Nhận tệp và trích đúng mã/owner/SLA |
| Intent prompt ghi đè | yêu cầu định dạng | Chỉ thay hành vi nhánh, không xóa quy tắc an toàn |

## Bằng chứng

- **Đã kiểm chứng:** UI có hai mode, năm preset và sáu Intent đúng tên trong bảng.
- **Đã kiểm chứng:** greeting được trả lời trực tiếp trong test Agent chuyên sâu.
- **Đã kiểm chứng:** System Prompt/Intent Prompt có các biến nêu trên trong UI.
- **Có điều kiện:** UI không phơi bày nhãn classifier trong trace; không khẳng định certainty hay thuật toán phân loại nội bộ.

## Quy tắc viết prompt vận hành

Một prompt production nên tách rõ **luật bất biến** và **hướng dẫn format**. Luật bất biến: chỉ dùng phạm vi nguồn được phép, trích nguồn khi đã retrieval, nêu thiếu dữ liệu/no-hit, nêu mâu thuẫn thay vì suy chọn. Hướng dẫn format: ngôn ngữ, độ dài, bảng hay bullet và câu hỏi làm rõ. Khi hai điều trái nhau, ưu tiên luật an toàn/nguồn; không dùng Intent prompt để vô hiệu hóa luật chung.

| Anti-pattern | Vì sao không ổn | Thay bằng |
|---|---|---|
| “Luôn trả lời tự tin” | Khuyến khích bịa khi no-hit | “Nếu không có nguồn phù hợp, nêu giới hạn và đề nghị thông tin cần thêm” |
| “Chỉ dùng KB” nhưng không nói nguồn | Human không kiểm chứng được | “Nêu tên nguồn/chunk cho claim quan trọng” |
| Prompt Intent sao chép toàn bộ System Prompt | Drift và khó A/B | Chỉ ghi phần khác biệt của intent |
| Cấm tool mơ hồ | Model không biết dừng ở đâu | Nêu tool được phép, tiêu chí gọi và tiêu chí dừng |

## Lỗi và giới hạn

- Preset có thể tạo cấu hình thiếu tool; Agent test ban đầu không tạo được cho tới khi bật ít nhất một tool. Kiểm tra validation trước khi kết luận preset hoàn chỉnh.
- Prompt càng dài không đồng nghĩa retrieval tốt hơn; luật xung đột hoặc ưu tiên nguồn phải ngắn, kiểm thử được.
- Không đặt “luôn trả lời” cùng với “chỉ trả lời khi có nguồn” nếu không mô tả nhánh no-hit.
- Lỗi `[[chunk#...]]` là lỗi tổng hợp/trình bày cần chẩn đoán prompt/model/context, không tự động sửa file nguồn.

## Checklist

- [ ] Mode và preset được ghi vào audit baseline.
- [ ] Prompt có luật nguồn, no-hit, xung đột và định dạng.
- [ ] Tất cả biến placeholder đúng cú pháp UI, không có secret.
- [ ] Sáu Intent được phân biệt bằng case, không chỉ tên.
- [ ] Mỗi prompt thay đổi có câu hồi quy và source trace.
