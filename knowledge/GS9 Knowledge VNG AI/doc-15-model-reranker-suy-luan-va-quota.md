<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 15 - Agent: model, reranker, suy luận và quota {#15-model-reranker-suy-luan-va-quota}

## Bạn sẽ biết gì sau khi đọc

- Model chat và reranker khác nhau chỗ nào.
- Nên đặt nhiệt độ, số vòng lặp và timeout bao nhiêu.
- Cách so sánh hai model mà không rút ra kết luận sai.
- Gặp lỗi quota, timeout hay câu trả lời không nguồn thì kiểm tra gì trước.

## Model và reranker là hai lớp khác nhau

Model chat tổng hợp câu trả lời và điều phối công cụ. Reranker chấm lại độ liên quan của các ứng viên tìm được trước khi context đi vào model.

Hai lớp này độc lập: đổi model không sửa cách chia đoạn hay embedding của KB; tắt reranker không làm thay đổi nội dung KB.

Danh sách model tùy tenant. Các model thường thấy trên dropdown: `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b`, `qwen3.6-plus`, `gpt-5.4-mini`. Reranker thường thấy: `bge-reranker-v2-m3`.

Có tên trong dropdown **không** bảo đảm model còn quota. Sau khi lưu, phải chat thử một lượt để xác nhận model thật sự trả lời được.

<!-- LOCAL_ASSET: ./image-28-agent-cau-hinh-mo-hinh.png -->
![Cấu hình model, reranker, nhiệt độ và chế độ suy nghĩ](minio://knowledge-base-prd/10012/7a292f44-0841-47f9-9dd2-c534f3220765/2fafbaf8-836e-4970-b6e3-856f90031c2e.png)

*Ảnh 15.1 - Tab cấu hình model; danh sách model có thể khác theo tenant và theo quota còn lại.*

## Bảng control và giá trị nên đặt

| Control | Tác động | Giá trị khởi đầu | Dấu hiệu cần điều tra |
|---|---|---|---|
| Model chat | Suy luận, gọi tool, văn phong | Model đang chạy được trong chính tenant của bạn | `429`, timeout, tool quay vòng, câu trả lời không tổng hợp |
| Reranker | Chọn và xếp lại ứng viên | `bge-reranker-v2-m3` nếu tenant có | Nguồn đúng bị tụt hạng hoặc nguồn nhiễu vẫn còn |
| Nhiệt độ | Độ biến thiên đầu ra | `0,7` là giá trị preset; hạ về `0,2`–`0,3` khi cần câu trả lời nhất quán | Bám định dạng kém, mỗi lần chạy một kiểu |
| Chế độ suy nghĩ | Cho model suy nghĩ mở rộng | Chỉ bật khi use case thật sự cần | Token và độ trễ tăng nhưng câu trả lời không tốt hơn |
| Token sinh tối đa | Giới hạn độ dài đầu ra | Chỉ hiện ở chế độ **Trả lời nhanh**; `0` nghĩa là không giới hạn | Câu trả lời bị cắt giữa chừng |
| Số vòng lặp tối đa | Số vòng gọi tool | Thường đặt `20`; các Agent đang chạy nằm trong khoảng `10`–`50` | Vòng lặp dài mà không tiến gần bằng chứng |
| Timeout LLM | Chặn một lần gọi quá lâu | Thường `120` giây; một số Agent đặt `180` giây | Hết thời gian trước khi có câu trả lời |
| Gọi công cụ song song | Cho phép gọi nhiều tool cùng lúc | Tắt ở lần dựng đầu | Thứ tự nguồn đổi hoặc phát sinh lỗi đồng thời |

Giá trị số vòng lặp và timeout khác nhau giữa các Agent. Trước khi kết luận Agent của bạn đang chạy ở mức nào, mở tab **Công cụ** và đọc trực tiếp giá trị trên màn hình.

Ba tham số số vòng lặp, timeout và gọi song song chỉ có ở chế độ **Suy luận thông minh** và **Quy trình**. Chế độ **Trả lời nhanh** không có các trường này.

Lưu ý dễ nhầm: **Suy nghĩ** là tên một *tool* ở tab **Công cụ**. **Chế độ suy nghĩ** là *tham số cấp model* ở tab **Cấu hình mô hình**. Hai thứ trùng tên, bật tắt độc lập.

<!-- LOCAL_ASSET: ./image-39-agent-model-ab-va-request-info.png -->
![Đổi model trong khung chat](minio://knowledge-base-prd/10012/7f5d2f06-d0a4-49ce-86d1-d1a771f3ebfb/f7fbd79b-6a59-404b-86bf-0a186fc70e0f.png)

*Ảnh 15.2 - Model có thể đổi ngay trong khung chat; khi test phải ghi lại model thật của lượt đó.*

## Cách so sánh hai model cho đúng

1. Chọn ba câu cố định: một câu có đáp án rõ, một câu có nguồn mâu thuẫn, một câu ngoài phạm vi KB. Cố định KB, tool và chiến lược truy hồi.
2. Chạy ba lần với cùng một model nếu quota cho phép. Lưu câu trả lời, nguồn, số bước và lỗi.
3. Đổi **đúng một** biến mỗi lần. Không đổi đồng thời model, reranker và ngưỡng.
4. Gặp `429` hoặc lỗi xác thực thì dừng model đó và ghi lại là bị chặn. Không thử lại vô hạn.
5. Sau khi so sánh xong, khôi phục model, nhiệt độ, timeout, gọi song song và bộ tool về mức ban đầu.

Lưu mỗi lần chạy thành **một dòng ghi chép**, không phải một nhận xét chung. Cột tối thiểu: thời điểm, Agent và phiên bản cấu hình, model, reranker, nhiệt độ, chế độ suy nghĩ, bộ tool, phạm vi KB/file, câu hỏi, số bước, thời gian, câu trả lời, nguồn và lỗi.

Với câu có nhiều nguồn, chấm ba điểm riêng biệt, đừng gộp:

- **Truy hồi** — tài liệu chuẩn và tài liệu gần giống có được đưa vào ứng viên không.
- **Bám nguồn** — câu trả lời có chỉ đúng nguồn không.
- **Tổng hợp** — có nêu đúng giá trị chuẩn và có cảnh báo mâu thuẫn không.

## Luồng xử lý

```text
ứng viên truy hồi → lọc theo ngưỡng → reranker (nếu bật)
                         → Top K context → model chat / chế độ suy nghĩ
                         → gọi tool tới giới hạn vòng lặp và timeout → câu trả lời
```

## Điều không được kết luận

| Kết quả quan sát | Kết luận sai | Bước đúng |
|---|---|---|
| Model A nhanh hơn model B ở một lượt | A luôn tốt hơn | Lặp lại cùng câu hỏi và cùng corpus nếu quota cho phép |
| A trả lời được, B báo `429` | A chính xác hơn | Đây là khác biệt về khả dụng, không phải chất lượng |
| Cả hai đều có nguồn nhưng một câu sai | KB hỏng | So context, prompt và đầu ra của model trước |
| Cả hai đều không có nguồn | Model yếu | Kiểm phạm vi KB, tool và ngưỡng trước khi đổi model |

<!-- LOCAL_ASSET: ./image-40-agent-quota-timeout-va-loi-runtime.png -->
![Cảnh báo timeout và lỗi khi chạy](minio://knowledge-base-prd/10012/f8e2d14e-2826-4e25-887a-85ac424d6550/05fa29a3-589f-44b9-946d-2e9e5fd45c71.png)

*Ảnh 15.3 - Timeout và lỗi khi chạy là tín hiệu cần điều tra riêng, không quy cho KB.*

## Lập mốc hiệu năng có trách nhiệm

Không đặt cam kết thời gian phản hồi từ một lượt chạy trong môi trường thử nghiệm.

- Chạy cùng một câu ít nhất ba lần khi quota cho phép.
- Loại các lần lỗi hạ tầng khỏi số trung vị, nhưng vẫn ghi lại lỗi đó.
- Tách thời gian chờ nạp tài liệu ra khỏi thời gian Agent suy luận.
- Chỉ so sánh độ trễ khi model, phiên bản KB, bộ tool, tham số truy hồi, tệp đính kèm và quota tương đương nhau.
- Nếu giữa chu kỳ có model chuyển sang không khả dụng, coi chu kỳ đó là bị chặn. Không lấp bằng số liệu của model khác.

Khi chọn model cho môi trường thật:

- Ưu tiên model đang chạy tốt bộ câu hồi quy trong chính tenant của bạn, hơn là model chỉ "có tên" trong dropdown.
- Chuẩn bị sẵn một model dự phòng đã được phê duyệt và ghi rõ trong tài liệu vận hành, để người trực ca không phải đoán khi quota thay đổi.
- Không đổi model giữa lúc đang xử lý sự cố, trừ khi có lý do rõ ràng.
- Coi reranker là một thành phần phụ thuộc: khi nó không khả dụng, phải test lại truy hồi trước khi coi kết quả cũ vẫn đúng.
- Không đưa một model mới thành mặc định chỉ vì một buổi demo. Cần người phụ trách phê duyệt, có mốc so sánh trước — sau, có đường quay lui và xác nhận quota thực tế.

## Chẩn đoán theo triệu chứng

| Triệu chứng | Kiểm tra trước | Hành động đúng |
|---|---|---|
| `429 insufficient_quota` | Khả dụng và quota của model | Dừng model đó, đổi sang model được phép, ghi lại là bị chặn |
| Câu trả lời không có nguồn | Tool, phạm vi KB, chiến lược truy hồi | Không đổi model như bước đầu tiên |
| Nguồn đúng nhưng câu trả lời sai | Prompt, context, nhiệt độ, model | Mở nguồn đối chiếu rồi thử đổi một biến |
| Tool quay vòng | Số vòng lặp, prompt, bộ tool | Giảm tool và vòng lặp, nêu rõ tiêu chí dừng |
| Timeout | Chuỗi tool, model, gọi song song | Giữ lại thông tin lượt chạy, tăng timeout có lý do rồi chạy hồi quy |
| Lộ chuỗi `[[chunk#...]]` | Lớp tổng hợp của model và prompt | Thử model khác trước khi động vào file nguồn |
| Độ trễ tăng đột ngột | **Chế độ suy nghĩ** có đang bật không | Mở tab cấu hình model đọc giá trị thật |

Không lưu request header, token, file service account hay dữ liệu chẩn đoán thô vào tài liệu.

## Checklist

- [ ] Đã ghi model, reranker, nhiệt độ, chế độ suy nghĩ, timeout và gọi song song cho mỗi lần test.
- [ ] Có đủ câu đúng, câu mâu thuẫn, câu ngoài phạm vi trong cùng điều kiện.
- [ ] Dừng lại và ghi nhận khi gặp lỗi quota.
- [ ] Mỗi lần so sánh chỉ đổi một biến và khôi phục lại mức ban đầu.
- [ ] Không kết luận chất lượng model khi truy hồi hoặc quota không tương đương.
