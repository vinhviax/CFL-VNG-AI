<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 13 - Agent: tổng quan và kiến trúc {#13-agent-tong-quan-va-kien-truc}

**Phạm vi và ngày kiểm chứng: 11/08/2026.** Module này là điểm vào ngắn cho cả vận hành và kỹ thuật; các control chi tiết nằm ở module 14–19.

## Khái niệm

Agent là lớp điều phối cuộc hội thoại giữa Human, model, Knowledge Base (KB), công cụ và tệp đính kèm. KB là nơi giữ nội dung có thể truy hồi; Agent giữ cấu hình để quyết định **có dùng nguồn nào**, gọi công cụ nào và trả lời theo hướng dẫn nào. Vì vậy sửa quy trình nghiệp vụ phải bắt đầu từ Markdown nguồn/KB, không phải sửa câu trả lời tạm thời của Agent.

```text
Human → Agent nhận lượt chat → phân loại Intent
      ├─ nhánh trả lời trực tiếp (ví dụ lời chào)
      └─ nhánh suy luận: prompt → tools → KB/file → rerank → model tổng hợp
                                                        ↓
                              câu trả lời + nguồn + feedback + Request Information
```

Trong gói Knowledge VNG, Agent nghiệp vụ dùng **Knowledge VNG AI** làm corpus: Markdown chứa SOP và URI ảnh MinIO. **Knowledge VNG - Image Assets** chỉ là host 49 PNG; không chọn nó làm KB hỏi đáp phổ thông. Một ảnh render trong câu trả lời vẫn được truy hồi từ Markdown consumer rồi theo URI tới asset host.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/26-agent-tong-quan-danh-sach.png -->
![Trang danh sách và nút Tạo trợ lý](minio://knowledge-base-prd/10012/exports/7e5d2b38-a440-4c4e-a458-f88f11d78bcf.png)

*Ảnh 13.1 – Danh sách Agent, bộ lọc phạm vi và điểm bắt đầu tạo Agent.*

## Bảng control

| Lớp | Chủ sở hữu vận hành | Control phải kiểm tra | Sai ở lớp này thường biểu hiện |
|---|---|---|---|
| Nội dung | Owner KB | Markdown, phiên bản, nguồn và ảnh MinIO | Nguồn sai hoặc thiếu bằng chứng |
| Truy hồi | Owner Agent | KB, loại file, `@`, tool, threshold, reranker | Không có nguồn hoặc nguồn nhiễu |
| Hành vi | Owner Agent | preset, System Prompt, Intent, model | Có nguồn đúng nhưng tổng hợp sai |
| Giao tiếp | Human/owner | chat mới, lịch sử, feedback, Request Information | Không tái hiện được lỗi |
| Quyền và vòng đời | Owner/Space admin | bật/tắt, chia sẻ, audit, rollback | Người không đúng quyền thấy hoặc sửa Agent |

| Thuật ngữ UI | Ý nghĩa vận hành |
|---|---|
| **Trợ lý/Agent** | Cấu hình chat có thể dùng lại, không phải bản gốc tri thức |
| **Intent** | Lớp phân loại lượt chat để chọn prompt ghi đè và hành vi truy hồi |
| **Nguồn** | File/chunk được UI hiển thị làm căn cứ; phải mở kiểm chứng khi đánh giá |
| **Request Information** | Hộp UI cho ID, method, URL và thời điểm request; dùng đối chiếu hỗ trợ, không chứa credential |
| **Preset** | Cấu hình khởi đầu, không phải một bảo đảm chất lượng |

## SOP

1. Xác định use case, Human, dữ liệu được phép dùng và tiêu chí câu trả lời đạt.
2. Chọn hoặc tạo Agent thử nghiệm; không cấu hình thử trực tiếp trên Agent mặc định.
3. Chọn **Knowledge VNG AI** hoặc KB có chủ đích; không nạp PNG độc lập vào consumer.
4. Thiết lập prompt, model, công cụ và retrieval; lưu baseline bằng ảnh/audit trước A/B.
5. Chạy ít nhất một câu đúng, một câu mâu thuẫn, một no-hit, một follow-up và một attachment phù hợp.
6. Mở source drawer và Request Information, phân loại lỗi theo lớp trước khi sửa.
7. Chỉ phát hành/chia sẻ sau khi test hồi quy; giữ bản sao cấu hình và đường rollback.

## Data flow

```text
Agent config
  → phân loại Intent
  → prompt chính hoặc prompt Intent ghi đè
  → lựa chọn KB/file + tool
  → semantic/keyword/wiki/data retrieval
  → ngưỡng + Top K + reranker
  → context cho LLM → trả lời, source chips, feedback
```

Điểm quan trọng: Intent không tự chứng minh một lượt chat sẽ hoặc sẽ không gọi KB. Nó là lớp định tuyến; kết quả thực tế còn phụ thuộc System Prompt, tool đã bật, KB/file được chọn, model và quota.

## Ma trận kiểm thử

| Tình huống | Câu/đầu vào mẫu | Kỳ vọng | Chỉ dấu pass |
|---|---|---|---|
| Greeting | “Xin chào, bạn giúp gì?” | Phản hồi trực tiếp, phù hợp | Không bịa nguồn |
| RAG chuẩn | ORCHID-731 owner/SLA | Nêu Nhóm Cam, 4 giờ và nguồn | Source chip canonical/PDF/CSV |
| Xung đột | Hỏi cùng mã có near-duplicate | Nêu Nhóm Lam/9 giờ là mâu thuẫn | Không âm thầm chọn một giá trị |
| No-hit | Chính sách nghỉ phép 2031 | Nói không có trong KB | Không tạo chính sách tưởng tượng |
| File đính kèm | PDF ORCHID tổng hợp | Phân tích mã/owner/SLA | Kết quả khớp attachment |

## Bằng chứng

- **Đã kiểm chứng:** trang Agent có danh sách, tìm kiếm, phạm vi và nút Tạo trợ lý; create dialog có sáu tab.
- **Đã kiểm chứng:** Agent test dùng đồng thời KB TEST và Knowledge VNG AI đã trả về canonical ORCHID-731, chỉ ra tài liệu near-duplicate mâu thuẫn và có nguồn.
- **Đã kiểm chứng:** no-hit “chính sách nghỉ phép năm 2031” kết luận không có thông tin sau semantic và keyword search.
- **Có điều kiện:** tenant/model/quyền có thể thay đổi danh sách Agent, tool, model và tốc độ.

Chi tiết truy vết nằm tại [audit Agent chuyên sâu 11/08](../../audit/agent-deep-test-2026-08-11.md).

## Lỗi và giới hạn

- Không biến Agent thành kho lưu bản gốc hoặc kênh thay Markdown nguồn.
- Khi model bị quota/429, không suy luận KB hỏng: phân biệt lỗi model với lỗi retrieval.
- Không lấy source chip là bằng chứng đủ nếu chưa mở đúng file/chunk và so với câu trả lời.
- Không dùng asset host làm corpus thường xuyên; ảnh phải đi theo Markdown consumer.

## Checklist

- [ ] Use case, KB phạm vi và owner được nêu rõ.
- [ ] Agent test tách biệt Agent mặc định/production.
- [ ] Có câu đúng, mâu thuẫn, no-hit và attachment phù hợp.
- [ ] Có source drawer và Request Information cho một lượt quan trọng.
- [ ] Kết luận được gắn **Đã kiểm chứng**, **Có điều kiện** hoặc **Bị chặn/Chưa xác định**.
