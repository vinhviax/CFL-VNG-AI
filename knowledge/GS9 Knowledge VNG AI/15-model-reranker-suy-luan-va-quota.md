<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 15 - Agent: model, reranker, suy luận và quota {#15-model-reranker-suy-luan-va-quota}

## Khái niệm

Model chat tổng hợp answer và có thể điều phối tool; reranker chấm lại độ liên quan của ứng viên retrieval trước khi context đi vào model. Hai lớp này khác nhau: đổi LLM không sửa embedding/chunk gốc; tắt reranker không thay nội dung KB. Trong UI 11/08/2026, bốn model thấy được là `deepseek-v4-flash`, `gpt-oss-120b`, `hosted_vllm/qwen3.6-35b` và `qwen3.6-plus`; reranker thấy được là `bge-reranker-v2-m3`.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/28-agent-cau-hinh-mo-hinh.png -->
![Cấu hình model, reranker, temperature và reasoning](minio://knowledge-base-prd/10012/exports/b976d174-9f47-4581-92aa-8218c3db2f38.png)

*Ảnh 15.1 – Tab cấu hình model; danh sách là snapshot UI, không cam kết quota còn hiệu lực.*

## Bảng control

| Control | Tác động | Baseline test | Dấu hiệu cần điều tra |
|---|---|---|---|
| Chat model | Suy luận, tool calling, văn phong | `hosted_vllm/qwen3.6-35b` có phản hồi ở test | 429, timeout, tool loop hoặc answer không tổng hợp |
| Reranker | Chọn/xếp lại candidate | `bge-reranker-v2-m3` nếu tenant khả dụng | Nguồn đúng bị tụt hoặc nguồn nhiễu còn lại |
| Temperature | Độ biến thiên đầu ra | A/B một biến, ví dụ 0,2 ↔ 0,7 | Tính lặp và bám định dạng giảm |
| Reasoning | Quyền suy nghĩ mở rộng khi model hỗ trợ | Chỉ bật khi use case cần | Token/độ trễ tăng nhưng answer không tốt hơn |
| Max loops | Số vòng tool tối đa | 10 trong Agent test | Loop dài, không tiến gần bằng chứng |
| Timeout LLM | Chặn một call quá lâu | 120 giây trong Agent test | Hết thời gian trước câu trả lời |
| Tool song song | Có thể gọi nhiều tool đồng thời | A/B, khôi phục baseline | Thứ tự/nguồn khác hoặc lỗi đồng thời |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/39-agent-model-ab-va-request-info.png -->
![A/B model trong composer và menu model](minio://knowledge-base-prd/10012/exports/3deae3c9-9c14-473f-ada3-cc64bfa4a8e3.png)

*Ảnh 15.2 – Model có thể đổi cho chat; test phải ghi model thật ở lượt đó.*

## SOP

1. Chọn một query canonical, một conflict và một no-hit; cố định KB/tool/retrieval.
2. Chạy ba lần cùng model nếu quota cho phép; lưu answer, nguồn, số bước và lỗi.
3. Đổi **một** model hoặc **một** control mỗi lần; không đồng thời đổi prompt/reranker/threshold.
4. Dừng ngay model nhận `429`/quota hoặc lỗi xác thực; ghi **Bị chặn**, không retry vô hạn.
5. Sau A/B, phục hồi model, temperature, timeout, parallel và tool baseline trước test khác.

## Data flow

```text
retrieval candidates → filters/threshold → reranker (nếu bật)
                         → Top K context → chat model/reasoning
                         → tool calls đến max loops/timeout → answer
```

Không suy luận model nào “thông minh hơn” chỉ từ một câu, đặc biệt khi candidate/context khác, quota khác hoặc Agent chạy tools khác nhau.

## Ma trận kiểm thử

| Trục | Case | Điều ghi nhận |
|---|---|---|
| 4 model | ORCHID canonical + no-hit | Có/không trả lời, nguồn, latency, lỗi quota |
| Temperature | 0,2 và 0,7 với cùng query | Độ bám format, không dùng để đo facts đơn lẻ |
| Reranker | tắt/bật khi có canonical + near duplicate | Thứ tự nguồn, có bỏ sót mâu thuẫn không |
| Reasoning | tắt/bật nếu UI/model hỗ trợ | Số bước, tool và answer cuối |
| Timeout | baseline và giá trị thử | Có abort/timeout rõ ràng; sau đó khôi phục |
| Parallel | tắt/bật cùng tools | Độ trễ, nguồn và lỗi đồng thời |

## Bằng chứng

- **Đã kiểm chứng:** `hosted_vllm/qwen3.6-35b` trả lời canonical/no-hit trong test chuyên sâu; `deepseek-v4-flash` cũng trả lời canonical ở chat độc lập.
- **Đã kiểm chứng:** UI trình bày bốn model và reranker nêu trên; Agent test dùng max loops 10 và timeout 120 giây.
- **Có điều kiện:** không đủ quota/quyền để kết luận cả bốn model đều chạy ba lượt hoặc có chất lượng tương đương.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/40-agent-quota-timeout-va-loi-runtime.png -->
![Timeout/cảnh báo runtime là tín hiệu vận hành](minio://knowledge-base-prd/10012/exports/875e9309-46ee-4901-800f-c88d92367724.png)

*Ảnh 15.3 – Timeout/lỗi runtime cần được ghi như tín hiệu điều tra, không bị gán nhầm cho KB.*

## Diễn giải kết quả A/B

Lưu mỗi lần chạy thành một hàng audit thay vì một nhận xét chung. Cột tối thiểu: thời điểm, Agent/version config, model, reranker, temperature, reasoning, tool set, KB/file scope, query cố định, số bước, thời gian, answer, source và lỗi. Với câu có nhiều nguồn, chấm ba điểm riêng: **retrieval** có đưa canonical và near-duplicate vào không; **grounding** có chỉ đúng nguồn không; **synthesis** có nêu đúng Nhóm Cam/4 giờ và cảnh báo Nhóm Lam/9 giờ không.

| Kết quả | Không được kết luận | Bước kế tiếp |
|---|---|---|
| Model A nhanh hơn Model B một lượt | A luôn tốt hơn | Lặp query/corpus giống nhau nếu quota cho phép |
| A có answer nhưng B 429 | A chính xác hơn | Ghi khác biệt khả dụng/quota; không chấm chất lượng |
| Cả hai có source nhưng một answer sai | KB hỏng | So context, prompt, model output trước |
| Không source ở cả hai | Model yếu | So scope/tools/threshold trước model |

## Baseline hiệu năng có trách nhiệm

Không đặt SLA chat từ một lượt ở môi trường test. Để lập baseline, chạy cùng query ít nhất ba lần khi quota cho phép, loại kết quả bị lỗi hạ tầng khỏi median nhưng vẫn ghi lỗi, và tách thời gian chờ ingestion khỏi thời gian Agent suy luận. Chỉ so sánh latency khi model, KB version, tool set, retrieval parameter, attachment và quota tương đương. Nếu một model chuyển sang unavailable/429 giữa chu kỳ, chu kỳ đó là **Bị chặn**, không được lấp bằng số liệu của model khác.

Quy tắc chọn model cho production: ưu tiên model đang pass bộ regression trong chính tenant hơn model “có tên” trong dropdown; giữ fallback được phê duyệt; ghi ngày và lỗi quota; và tránh đổi model trong lúc xử lý một incident trừ khi có lý do rõ. Reranker cũng cần được coi là dependency: khi nó mất khả dụng, test retrieval lại trước khi coi answer cũ còn tương đương.

Không chuyển một model mới thành default chỉ từ demo: cần owner phê duyệt, baseline trước/sau, rollback path và xác nhận quota thực tế.
Ghi rõ model fallback trong runbook để người trực ca không phải đoán khi quota thay đổi.

## Lỗi và giới hạn

| Triệu chứng | Chẩn đoán trước | Hành động đúng |
|---|---|---|
| `429 insufficient_quota` | Khả dụng model/quota | Dừng model, đổi model được phép, ghi blocker |
| Answer không có nguồn | Tool/KB/scope/retrieval trước model | Không đổi LLM như bước đầu tiên |
| Source đúng nhưng câu sai | Prompt, context, temperature, model | Kiểm tra source và thử A/B cô lập |
| Tool quay vòng | Loops, prompt, tool set | Giảm tools/loops và buộc tiêu chí dừng |
| Timeout | Tool chain, model, parallel | Giữ trace, tăng timeout có lý do rồi hồi quy |

Không lưu request headers, token, service-account JSON hoặc internal diagnostic raw vào tài liệu/audit.

## Checklist

- [ ] Ghi model/reranker/temperature/reasoning/timeout/parallel cho mỗi test.
- [ ] Có canonical, conflict, no-hit cùng điều kiện.
- [ ] Dừng khi quota/429 và phân loại Bị chặn.
- [ ] A/B chỉ đổi một biến và khôi phục baseline.
- [ ] Không kết luận chất lượng model nếu retrieval hoặc quota không tương đương.
