<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 16 - Agent: kho tri thức, công cụ và truy hồi {#16-kho-tri-thuc-cong-cu-va-truy-hoi}

## Khái niệm

Tab **Kho tri thức** xác định corpus mà Agent được phép tìm. UI có ba phạm vi: tất cả KB được phép, KB đã chọn và không dùng KB. Với Agent Knowledge VNG, chọn rõ **Knowledge VNG AI**; asset host chỉ giữ PNG để Markdown tham chiếu. UI cho lọc theo loại tệp như `MD`, `PDF`, `CSV`, `DOCX`, `TXT`, `XLSX`, `XLS`, `JSON`, `PPTX`, `HTML`, `MSG`, `EML` (danh sách tenant có thể đổi).

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/29-agent-kho-tri-thuc.png -->
![Phạm vi KB và lọc loại tệp](minio://knowledge-base-prd/10012/exports/8208154f-e74f-4630-b44c-6346992ddaee.png)

*Ảnh 16.1 – Chọn KB là control bảo mật và chất lượng, không chỉ là tiện lợi.*

`Chỉ truy hồi khi được nhắc` thay đổi thời điểm Agent được phép dùng KB. Khi bật, Human chọn KB hoặc tệp qua **Nhắc tri thức / tệp** (`@`) trong composer; không có `@` thì không nên kỳ vọng RAG tự chạy. Khi tắt, Agent có thể tự gọi retrieval trong phạm vi cấu hình.

## Bảng control

| Nhóm | UI/giá trị quan sát | Vai trò | Rủi ro khi cấu hình sai |
|---|---|---|---|
| KB scope | All / Selected / None | Biên dữ liệu Agent thấy | Leaky scope hoặc không có nguồn |
| File types | MD/PDF/CSV… | Thu hẹp corpus theo use case | Bỏ sót file đúng hoặc kéo nhiễu |
| `@` | KB/tệp trong composer | Scope theo từng lượt | Human tưởng đã truy hồi nhưng chưa chọn chip |
| Semantic search | Tìm theo ngữ nghĩa | Recall cho câu diễn đạt lại | Gần nghĩa nhưng sai chủ đề |
| Keyword search | Tìm theo từ khóa | Mã, tên, thuật ngữ | Bỏ sót biến thể/đồng nghĩa |
| List chunks / Document info | Duyệt/đọc metadata | Debug candidate và nguồn | Tool thừa làm loop dài |
| Wiki/data tools | Wiki, SQL, Data Analysis, Schema | Chỉ cho KB/file tương thích | Kết luận sai vì tool không có dữ liệu |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/30-agent-cong-cu.png -->
![Công cụ, loops, timeout và parallel](minio://knowledge-base-prd/10012/exports/50273f87-b180-4d1c-a6b2-5cbf4db97d8b.png)

*Ảnh 16.2 – Tool set hiệu lực phải được kiểm tra sau preset.*

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/31-agent-chien-luoc-truy-hoi.png -->
![Chiến lược truy hồi: Top K, ngưỡng và reranker](minio://knowledge-base-prd/10012/exports/c7d2a27c-4720-4b4c-838d-c794050b5e89.png)

*Ảnh 16.3 – Retrieval strategy là lớp lọc candidate trước context; chỉ thay một tham số trong mỗi lần A/B.*

## SOP

1. Bắt đầu bằng **Selected KB** và loại file tối thiểu; nới rộng chỉ khi testcase chứng minh cần.
2. Bật semantic + keyword cho tài liệu hỗn hợp; giữ List chunks/Document info cho trace kỹ thuật.
3. Chỉ bật Wiki tools khi KB đã có Wiki phù hợp; chỉ bật data tools khi CSV/XLSX/table tương thích.
4. Chọn một canonical, một near duplicate, một tên/mã exact và một no-hit để đánh giá.
5. Khi nguồn sai: kiểm tra scope → `@`/chip → file type → tool → threshold/Top K → reranker; đừng sửa prompt trước.

## Data flow

```text
KB scope + file filter + @ per-turn
     → tools: semantic / keyword / chunks / document info / wiki / data
     → candidate set
     → vector/keyword thresholds + Top K
     → reranker (nếu bật) → context → answer + source chips
```

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/41-agent-test-kb-da-nguon.png -->
![Hai KB trong Agent test](minio://knowledge-base-prd/10012/exports/464611ad-8b6b-44e6-a2d8-1bdfefc8e856.png)

*Ảnh 16.4 – Agent test được giới hạn vào KB TEST tổng hợp và Knowledge VNG AI để quan sát xung đột có kiểm soát.*

## Ma trận kiểm thử

| Case | Thay đổi duy nhất | Kỳ vọng |
|---|---|---|
| Scope | Selected KB TEST ↔ Selected TEST + consumer ↔ None | Source chỉ xuất hiện trong scope cho phép |
| Type filter | MD ↔ PDF ↔ CSV | File đúng được/không được candidate theo filter |
| `@` | bật/tắt “chỉ khi được nhắc” | Không `@` không tự retrieval khi công tắc bật |
| Tool | semantic ↔ keyword ↔ cả hai | Mã ORCHID exact và diễn đạt lại đều có đường tìm |
| Top K | 3 ↔ 10 | Conflict còn bị phát hiện hay bị cắt mất |
| Vector threshold | 0,3 ↔ 0,7 | Recall/nhiễu thay đổi, không đánh giá chỉ bằng câu văn |
| Reranker | tắt ↔ bật | Thứ tự/candidate cuối và nguồn phải được ghi |

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/42-agent-at-kho-tri-thuc-va-tep.png -->
![Nhắc KB hoặc tệp bằng @](minio://knowledge-base-prd/10012/exports/f4c5d9ed-91e6-4110-ad20-6e1a08a25dd4.png)

*Ảnh 16.5 – Dialog hiển thị cả KB và từng tệp có thể nhắc trong composer.*

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/43-agent-trace-cong-cu-truy-hoi.png -->
![Trace tools và source từ bốn file ORCHID](minio://knowledge-base-prd/10012/exports/79ffdb8a-ae3c-4b06-af4e-40d765ccbb7e.png)

*Ảnh 16.6 – Runtime dùng keyword/semantic rồi hiển thị các file canonical, near-duplicate, CSV và PDF.*

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/44-agent-ab-topk-threshold-rerank.png -->
![A/B Top K, threshold và rerank](minio://knowledge-base-prd/10012/exports/33d4048f-735b-464e-8dcc-2e8b714fdc0a.png)

*Ảnh 16.7 – Các control phải được A/B một biến và khôi phục baseline, không chỉnh đồng thời.*

## Bằng chứng

- **Đã kiểm chứng:** Agent test có thể chọn đồng thời KB TEST và Knowledge VNG AI; dialog `@` liệt kê 2 KB cùng 5 fixture và 14 Markdown consumer tại thời điểm test.
- **Đã kiểm chứng:** query ORCHID dùng keyword + semantic, tìm 8 matches/5 kết quả từ 4 tệp và nêu xung đột Nhóm Cam/4 giờ với Nhóm Lam/9 giờ.
- **Đã kiểm chứng:** no-hit sau semantic/keyword không bịa chính sách.
- **Có điều kiện:** Wiki/Data/Schema tools chỉ được quan sát trong catalog/cấu hình; kết quả end-to-end phụ thuộc Wiki hoặc data source tương thích.

## Quy tắc ưu tiên và xung đột nguồn

Retrieval không tự biết tài liệu nào là authoritative. Với data đa nguồn, tài liệu canonical phải mang nhãn/metadata rõ trong chính nội dung; prompt cần yêu cầu Agent hiển thị mâu thuẫn và không “bỏ phiếu” bằng số lượng chunk. Trong fixture ORCHID, canonical MD, PDF và record CSV đầu khớp Nhóm Cam/4 giờ; near-duplicate và record CSV thứ hai cố ý ghi Nhóm Lam/9 giờ. Test pass khi Agent đưa cả hai phía, nêu nguồn chuẩn/nhãn conflict và giải thích căn cứ chọn giá trị chuẩn.

| Trạng thái nguồn | Hành vi mong muốn |
|---|---|
| Một nguồn canonical rõ, không xung đột | Trả lời và trích nguồn |
| Canonical + near duplicate có nhãn | Trả lời canonical, cảnh báo mâu thuẫn |
| Hai nguồn đồng cấp mâu thuẫn | Không tự quyết; hỏi Human/owner hoặc báo không xác định |
| Source không có claim cần hỏi | No-hit có căn cứ, không nội suy |

## Baseline retrieval cho Knowledge VNG AI

Khởi đầu thực dụng là: scope **Selected** = `Knowledge VNG AI`; loại `MD`; `@` tắt nếu Agent phải tự RAG; semantic và keyword đều bật; reranker bật khi tenant khả dụng. Sau đó chọn một query từ mỗi module quan trọng, một query diễn đạt lại và một query cố ý không có trong sổ tay. Nếu source bị nhiễu, giảm scope/lọc file trước; nếu source quá ít, hạ threshold hoặc tăng Top K từng bước và ghi lại ảnh hưởng đến no-hit.

## Lỗi và giới hạn

- `[[chunk#...]]` lộ ra là bằng chứng context tới model, nhưng không phải câu trả lời đạt; giữ trace và chẩn đoán model/prompt.
- Nhiều nguồn không tự cho biết nguồn nào là canonical: đặt nhãn nguồn, prompt quy tắc xung đột và test near duplicate.
- `@` là lựa chọn scope, không phải quyền vượt qua access control.
- Top K/threshold không có giá trị “đúng cho mọi KB”; thay một biến và giữ corpus/query cố định.

## Checklist

- [ ] Scope Selected KB được ghi rõ, không gồm asset host.
- [ ] Lọc loại file khớp use case, có test PDF/CSV nếu bật.
- [ ] Tool catalog tối thiểu và các tool điều kiện được gắn nhãn.
- [ ] Có test `@`, canonical, conflict, exact identifier và no-hit.
- [ ] Có source trace trước khi đổi prompt/model.
