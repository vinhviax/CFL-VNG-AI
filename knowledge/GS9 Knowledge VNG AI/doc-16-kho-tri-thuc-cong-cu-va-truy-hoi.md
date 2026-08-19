<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 16 - Agent: kho tri thức, công cụ và truy hồi {#16-kho-tri-thuc-cong-cu-va-truy-hoi}

## Bạn sẽ biết gì sau khi đọc

- Chọn phạm vi KB và lọc loại tệp cho đúng.
- Công tắc **Chỉ truy hồi khi được nhắc** và cách dùng `@` trong khung chat.
- Bật tool nào, theo điều kiện gì.
- Đặt Top K và ngưỡng truy hồi bao nhiêu, và kiểm tra theo thứ tự nào khi nguồn sai.

## Chọn kho tri thức là control bảo mật

Tab **Kho tri thức** xác định corpus mà Agent được phép tìm. Đây là ranh giới dữ liệu, không chỉ là tiện lợi.

| Phạm vi | Nghĩa là gì | Dùng khi nào |
|---|---|---|
| **Tất cả kho tri thức** | Agent dùng được mọi KB mà nó có quyền truy cập | Hạn chế dùng cho nghiệp vụ |
| **Kho tri thức đã chọn** | Giới hạn vào danh sách cụ thể | Lựa chọn đúng cho môi trường thật |
| **Không dùng kho tri thức** | Agent không cần truy hồi | Agent chỉ soạn thảo hoặc điều phối |

Với Agent Knowledge VNG, chọn rõ **Knowledge VNG AI**. Kho ảnh chỉ giữ PNG để Markdown tham chiếu, không dùng làm corpus hỏi đáp.

Nếu bạn nhân bản một Agent mặc định, bản sao sẽ kế thừa phạm vi **Tất cả kho tri thức**. Kiểm và thu hẹp lại ngay sau khi nhân bản.

<!-- LOCAL_ASSET: ./image-29-agent-kho-tri-thuc.png -->
![Phạm vi KB và lọc loại tệp](minio://knowledge-base-prd/10012/152c62ab-1025-4903-a34c-e2c8e8214d25/2f7f5de5-3379-406b-9b3a-e5cc43aa9305.png)

*Ảnh 16.1 - Chọn KB là control bảo mật và chất lượng, không chỉ là tiện lợi.*

> **Ảnh chụp một thời điểm, không phải danh mục hiện hành.** Tên kho, tên trợ lý, tên nguồn dữ liệu và các con số đếm nhìn thấy trong ảnh là của lúc chụp màn hình để viết hướng dẫn này. Chúng đổi liên tục. Xem ảnh để biết **giao diện nằm ở đâu**, đừng lấy ảnh để biết **hệ thống đang có gì** — mở thẳng hệ thống mà xem.

### Lọc loại tệp

Loại tệp thường có trên giao diện: `MD`, `PDF`, `CSV`, `DOCX`, `TXT`, `XLSX`, `XLS`, `JSON`, `PPTX`, `HTML`, `MSG`, `EML`. Danh sách có thể khác theo tenant.

Để trống danh sách nghĩa là cho phép mọi loại được hỗ trợ trong phạm vi KB. Thu hẹp loại tệp là cách rẻ nhất để giảm nhiễu, nên làm trước khi động vào ngưỡng.

### Công tắc Chỉ truy hồi khi được nhắc

| Trạng thái | Hành vi |
|---|---|
| **Tắt** | Agent tự dùng KB đã cấu hình khi thấy cần |
| **Bật** | Chỉ truy hồi khi bạn dùng `@` (**Nhắc tri thức / tệp**) trong khung chat |

Khi công tắc đang bật mà bạn không gõ `@`, đừng kỳ vọng Agent tự tìm trong KB.

`@` là lựa chọn **phạm vi**, không phải quyền vượt qua kiểm soát truy cập. Bạn chỉ nhắc được KB và tệp mà mình vốn đã có quyền.

## Công cụ

| Nhóm | Tool | Điều kiện bật |
|---|---|---|
| **Điều phối, không cần KB** | Suy nghĩ · Lập kế hoạch (todo) · Hỏi người dùng | Bật được ngay ở chế độ Suy luận thông minh |
| **Truy hồi tài liệu** | Tìm theo ngữ nghĩa · Tìm theo từ khóa · Liệt kê đoạn · Thông tin tài liệu | Cần đã chọn KB |
| **Wiki** | Tìm wiki · Đọc trang wiki · Đọc tài liệu nguồn | Cần KB đã bật Wiki và Wiki có nội dung thật |
| **Dữ liệu** | Lược đồ dữ liệu · Phân tích dữ liệu | Cần bảng, CSV hoặc XLSX đã chuẩn hóa |
| **Cơ sở dữ liệu** | Truy vấn CSDL | Cần view chỉ đọc và danh sách cho phép |
| **Danh mục** | Danh mục sản phẩm | Cần catalog chỉ đọc đã kiểm tra đúng game, region, môi trường |

Hai điều hay gặp khi cấu hình lần đầu:

- Khi Agent **chưa chọn KB**, cả nhóm **Truy hồi tri thức** bị mờ với chú thích *Cần có kho tri thức trong phạm vi*. Chọn KB trước, mới bật được tool.
- Tab **Công cụ** hiển thị phạm vi dạng `n KB RAG · n KB Wiki`. Dùng dòng này để xác nhận đã gắn KB thành công **trước khi bấm Lưu**.

Nhãn `WIKI` trong dropdown chỉ cho biết KB có bật Wiki, **không** chứng minh Wiki đã có nội dung. Chỉ bật nhóm tool Wiki khi đã mở Wiki của KB đó và thấy có trang thật.

Nguyên tắc quyền tối thiểu: nhóm điều phối bật được ngay; nhóm truy hồi, Wiki, dữ liệu, CSDL và danh mục chỉ bật sau khi đã rà nguồn và quyền. Trước khi bật một tool gắn với nguồn dữ liệu, phải trả lời được sáu câu: ai sở hữu nguồn, quyền truy cập ra sao, dữ liệu giữ bao lâu, mức nhạy cảm thế nào, cập nhật đến đâu, và có bộ câu hỏi chuẩn để kiểm chưa.

<!-- LOCAL_ASSET: ./image-30-agent-cong-cu.png -->
![Công cụ, số vòng lặp, timeout và gọi song song](minio://knowledge-base-prd/10012/0e90211a-e678-4c4e-bc9f-103cb0fc9a06/0af752a5-9ef3-4c50-a65b-d19002c00109.png)

*Ảnh 16.2 - Bộ tool có hiệu lực phải được kiểm lại sau khi chọn preset.*

## Chiến lược truy hồi

<!-- LOCAL_ASSET: ./image-31-agent-chien-luoc-truy-hoi.png -->
![Chiến lược truy hồi: Top K, ngưỡng và reranker](minio://knowledge-base-prd/10012/735dfe79-76f4-4c34-a22d-413ce015281f/02701d3a-ef3c-4099-882f-00291192a93a.png)

*Ảnh 16.3 - Chiến lược truy hồi là lớp lọc ứng viên trước context; mỗi lần chỉ đổi một tham số.*

```text
Từ khóa + vector tạo danh sách ứng viên
  → ngưỡng từ khóa / ngưỡng vector loại kết quả yếu
  → reranker chấm lại ứng viên còn lại
  → Top K xếp hạng lại + ngưỡng xếp hạng lại quyết định context cuối
  → context → model
```

Giá trị khởi đầu thường gặp:

| Tham số | Giá trị thường dùng |
|---|---|
| Top K vector | `10` (một số Agent phân tích dữ liệu đặt `5`) |
| Ngưỡng từ khóa | `0,3` |
| Ngưỡng vector | `0,5` |
| Top K xếp hạng lại | `5`–`10` |
| Ngưỡng xếp hạng lại | `0,3`–`0,5` |

Giá trị mặc định của hộp tạo mới và giá trị đang lưu trên từng Agent có thể khác nhau. Trước khi kết luận Agent của bạn đang chạy ở mức nào, mở tab **Chiến lược truy hồi** và đọc giá trị thật trên màn hình.

### Quy tắc chỉnh ngưỡng

- Ngưỡng quá cao gây bỏ sót. Ngưỡng quá thấp kéo nhiễu vào context.
- Đổi **một** tham số mỗi lần, giữ nguyên corpus và câu hỏi.
- Chạy lại đủ bốn loại câu: đúng, diễn đạt lại, dễ nhầm và ngoài phạm vi.
- Không có giá trị đúng cho mọi KB. Ghi lại ảnh hưởng tới câu ngoài phạm vi, không chỉ ghi câu đúng.
- Nếu nguồn nhiễu, giảm phạm vi và lọc loại tệp trước; đừng động vào ngưỡng ngay.

<!-- LOCAL_ASSET: ./image-41-agent-test-kb-da-nguon.png -->
![Chọn nhiều KB cho một Agent](minio://knowledge-base-prd/10012/580d4822-45bd-4dea-8ab0-74a3146f6a03/13fd8fde-ec78-4eff-96ab-a8451a394017.png)

*Ảnh 16.4 - Một Agent có thể gắn nhiều KB; giữ danh sách gọn giúp quan sát nguồn dễ hơn.*

> **Ảnh chụp một thời điểm, không phải danh mục hiện hành.** Tên kho, tên trợ lý, tên nguồn dữ liệu và các con số đếm nhìn thấy trong ảnh là của lúc chụp màn hình để viết hướng dẫn này. Chúng đổi liên tục. Xem ảnh để biết **giao diện nằm ở đâu**, đừng lấy ảnh để biết **hệ thống đang có gì** — mở thẳng hệ thống mà xem.

## Baseline cho Agent hỏi đáp Knowledge VNG AI

Khởi đầu thực dụng:

- Phạm vi: **Kho tri thức đã chọn** = `Knowledge VNG AI`.
- Loại tệp: chỉ `MD`.
- Công tắc **Chỉ truy hồi khi được nhắc**: tắt, để Agent tự truy hồi.
- Tool: bật **Tìm theo ngữ nghĩa** và **Tìm theo từ khóa**.
- Reranker: bật nếu tenant có.

Sau đó chọn một câu hỏi từ mỗi chủ đề quan trọng, một câu diễn đạt lại và một câu cố ý không có trong sổ tay. Nếu nguồn nhiễu, thu hẹp phạm vi hoặc lọc tệp trước. Nếu nguồn quá ít, hạ ngưỡng hoặc tăng Top K từng bước và ghi lại ảnh hưởng tới câu ngoài phạm vi.

## Các bước cấu hình

1. Bắt đầu bằng **Kho tri thức đã chọn** với loại tệp tối thiểu. Chỉ nới rộng khi có case chứng minh cần.
2. Bật tìm theo ngữ nghĩa và tìm theo từ khóa cho tài liệu hỗn hợp. Giữ **Liệt kê đoạn** và **Thông tin tài liệu** cho việc dò lỗi.
3. Chỉ bật tool Wiki khi KB đã có Wiki thật. Chỉ bật tool dữ liệu khi có CSV, XLSX hoặc bảng tương thích.
4. Chuẩn bị bốn câu để đánh giá: một câu có tài liệu chuẩn, một câu có tài liệu gần giống dễ nhầm, một câu tra mã hoặc tên chính xác, một câu ngoài phạm vi.
5. Khi nguồn sai, kiểm tra theo thứ tự ở mục dưới. Đừng sửa prompt trước.

<!-- LOCAL_ASSET: ./image-42-agent-at-kho-tri-thuc-va-tep.png -->
![Nhắc KB hoặc tệp bằng @](minio://knowledge-base-prd/10012/bbd47e33-6458-4ccf-b811-9838ec41e0bb/7bf33d67-fecb-4df3-9463-2bc4c5dd67cf.png)

*Ảnh 16.5 - Hộp thoại hiển thị cả KB và từng tệp có thể nhắc trong khung chat.*

> **Ảnh chụp một thời điểm, không phải danh mục hiện hành.** Tên kho, tên trợ lý, tên nguồn dữ liệu và các con số đếm nhìn thấy trong ảnh là của lúc chụp màn hình để viết hướng dẫn này. Chúng đổi liên tục. Xem ảnh để biết **giao diện nằm ở đâu**, đừng lấy ảnh để biết **hệ thống đang có gì** — mở thẳng hệ thống mà xem.

## Ma trận kiểm thử

| Trường hợp | Thay đổi duy nhất | Kỳ vọng |
|---|---|---|
| Phạm vi | Chọn 1 KB ↔ chọn 2 KB ↔ không dùng KB | Nguồn chỉ xuất hiện trong phạm vi cho phép |
| Lọc loại tệp | MD ↔ PDF ↔ CSV | File đúng được hoặc không được vào ứng viên theo bộ lọc |
| `@` | Bật/tắt **Chỉ truy hồi khi được nhắc** | Không gõ `@` thì không tự truy hồi khi công tắc bật |
| Tool | Ngữ nghĩa ↔ từ khóa ↔ cả hai | Cả mã chính xác và câu diễn đạt lại đều có đường tìm |
| Top K | `3` ↔ `10` | Mâu thuẫn còn được phát hiện hay bị cắt mất |
| Ngưỡng vector | `0,3` ↔ `0,7` | Độ bao phủ và độ nhiễu thay đổi; không đánh giá chỉ bằng văn phong |
| Reranker | Tắt ↔ bật | Ghi lại thứ tự và danh sách nguồn cuối cùng |

<!-- LOCAL_ASSET: ./image-43-agent-trace-cong-cu-truy-hoi.png -->
![Kết quả truy hồi hiển thị nhiều tệp nguồn](minio://knowledge-base-prd/10012/6150e91c-cdc2-4008-9158-afea73bae00f/826ac8c4-1be0-4bef-93f6-c3c607314386.png)

*Ảnh 16.6 - Lượt chạy dùng cả tìm theo từ khóa và ngữ nghĩa rồi hiển thị các tệp nguồn tìm được.*

## Khi nhiều nguồn nói khác nhau

Truy hồi không tự biết tài liệu nào là chuẩn. Tài liệu chuẩn phải mang nhãn rõ ngay trong nội dung, và prompt phải yêu cầu Agent hiển thị mâu thuẫn thay vì "bỏ phiếu" theo số lượng đoạn tìm được.

| Trạng thái nguồn | Hành vi mong muốn |
|---|---|
| Một nguồn chuẩn rõ ràng, không xung đột | Trả lời và trích nguồn |
| Nguồn chuẩn cộng bản gần giống đã gắn nhãn | Trả lời theo bản chuẩn, cảnh báo mâu thuẫn |
| Hai nguồn ngang cấp mâu thuẫn | Không tự quyết; hỏi lại người phụ trách hoặc báo chưa xác định |
| Nguồn không chứa điều được hỏi | Trả lời là không có thông tin, không suy diễn |

<!-- LOCAL_ASSET: ./image-44-agent-ab-topk-threshold-rerank.png -->
![So sánh Top K, ngưỡng và reranker](minio://knowledge-base-prd/10012/272e938d-ac79-447e-ad78-e748ca0fb92c/d940ba5c-7dbe-443b-94b0-30ea1c9b9e18.png)

*Ảnh 16.7 - Các control này phải được so sánh từng biến một và khôi phục lại mức ban đầu.*

## Nguồn sai hoặc không có nguồn: kiểm theo thứ tự

Dừng ở lớp đầu tiên tìm ra vấn đề.

1. **Phạm vi KB** — Agent đã chọn KB chưa, đúng KB chưa?
2. **`@` và chip** — công tắc **Chỉ truy hồi khi được nhắc** có đang bật, bạn đã chọn chip chưa?
3. **Loại tệp** — file đúng có nằm trong bộ lọc không?
4. **Tool** — **Tìm theo ngữ nghĩa** và **Tìm theo từ khóa** đã bật chưa?
5. **Ngưỡng và Top K** — có đang quá cao gây bỏ sót không?
6. **Reranker** — có đẩy nguồn đúng tụt hạng không?

Đừng sửa prompt trước. Đừng đổi model trước. Đó là hai bước tốn công nhất và ít khi là nguyên nhân.

| Hiện tượng | Lớp cần kiểm | Không được kết luận |
|---|---|---|
| Không có nguồn nào | Phạm vi → `@` → loại tệp → tool → ngưỡng | "Model yếu" |
| Có đoạn nhưng lộ `[[chunk#...]]` | Lớp tổng hợp của model và prompt | "KB hỏng" — không sửa file nguồn |
| Nguồn đúng, câu trả lời sai | Prompt, thứ tự context, nhiệt độ | "Truy hồi hỏng" |
| Nguồn sai hoặc nhiễu | KB đã chọn, Top K, ngưỡng, reranker | "Cần thêm tài liệu" |
| Tool truy hồi bị mờ | Agent chưa chọn KB | "Tool bị lỗi" |
| Nhóm Wiki bị mờ | KB chưa bật Wiki | "Nền tảng không có Wiki" |
| Nguồn đến từ KB không được phép | Phạm vi đang là **Tất cả kho tri thức** | Kiểm ngay, đây là sự cố dữ liệu |

## Kiểm chứng một câu trả lời, năm bước

1. Đọc câu trả lời.
2. Mở chip nguồn, xác nhận đúng tài liệu.
3. Mở đoạn nguồn, xác nhận nó thật sự chứa bằng chứng cho câu trả lời.
4. Nếu câu trả lời cần ảnh, xác nhận ảnh **hiện ra** trong chat chứ không chỉ có đường dẫn.
5. Hỏi thêm một câu ngoài phạm vi để kiểm tra Agent biết dừng.

## Checklist

- [ ] Phạm vi **Kho tri thức đã chọn** ghi rõ, đúng nghiệp vụ Agent phục vụ.
- [ ] Bộ lọc loại tệp khớp use case; có test PDF hoặc CSV nếu đã bật.
- [ ] Chỉ bật bộ tool tối thiểu; các tool có điều kiện đã kiểm nguồn trước khi bật.
- [ ] Đã test `@`, câu có tài liệu chuẩn, câu mâu thuẫn, câu tra mã chính xác và câu ngoài phạm vi.
- [ ] Đã mở nguồn đối chiếu trước khi đổi prompt hoặc model.
