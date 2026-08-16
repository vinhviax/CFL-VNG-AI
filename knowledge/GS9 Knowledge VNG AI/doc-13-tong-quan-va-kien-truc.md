<!-- GENERATED FILE - sửa nội dung tại docs KB/Human/ -->

# 13 - Agent: tổng quan và kiến trúc {#13-agent-tong-quan-va-kien-truc}

## Bạn sẽ biết gì sau khi đọc

- Agent là gì và khác Knowledge Base ở chỗ nào.
- Sáu tab trong hộp **Tạo trợ lý** quyết định điều gì.
- Thứ tự các bước từ lúc dựng Agent tới lúc phát hành.
- Khi câu trả lời sai thì đi tìm nguyên nhân ở lớp nào trước.

## Agent là gì

Agent là lớp điều phối một lượt chat giữa bạn, model, Knowledge Base (KB), công cụ và tệp đính kèm.

Agent **không lưu tri thức**. KB mới là nơi giữ nội dung có thể truy hồi. Agent chỉ giữ cấu hình để quyết định dùng nguồn nào, gọi công cụ nào và trả lời theo hướng dẫn nào.

Hệ quả quan trọng: **nội dung sai thì sửa KB, không sửa câu trả lời của Agent.**

```text
Human → Agent nhận lượt chat → phân loại Intent
      ├─ nhánh trả lời trực tiếp (ví dụ lời chào)
      └─ nhánh suy luận: prompt → tools → KB/file → rerank → model tổng hợp
                                                        ↓
                              câu trả lời + nguồn + feedback + Request Information
```

Agent nghiệp vụ chọn kho tri thức chứa nội dung nghiệp vụ làm nguồn trả lời. Ảnh và tài liệu Markdown để chung một kho được: ảnh vẫn hiện trong câu trả lời vì Markdown tham chiếu tới liên kết nội bộ của ảnh đó.

<!-- LOCAL_ASSET: ./image-26-agent-tong-quan-danh-sach.png -->
![Trang danh sách và nút Tạo trợ lý](minio://knowledge-base-prd/10012/5267ca6e-9ffc-4091-ba24-89d4b0075e80/7cda390e-4f99-43c0-8e92-279519831e71.png)

*Ảnh 13.1 - Danh sách Agent, bộ lọc phạm vi và điểm bắt đầu tạo Agent.*

## Sáu tab của hộp Tạo trợ lý

| # | Tab | Quyết định điều gì |
|---|---|---|
| 1 | Thông tin cơ bản | Tên, mô tả, chế độ chạy, System Prompt, prompt theo Intent |
| 2 | Cấu hình mô hình | Model chat, reranker, nhiệt độ, chế độ suy nghĩ |
| 3 | Kho tri thức | Phạm vi KB, loại tệp, công tắc *Chỉ truy hồi khi được nhắc* |
| 4 | Công cụ | Tool được bật, số vòng lặp, timeout LLM, gọi song song |
| 5 | Chiến lược truy hồi | Top K, ngưỡng từ khóa/vector, Top K và ngưỡng xếp hạng lại |
| 6 | Cấu hình đa phương thức | Tải ảnh + VLM, tải âm thanh + ASR |

Tập tab thay đổi theo chế độ chạy:

- Chế độ **Trả lời nhanh** không có tab **Công cụ**; thay bằng tab **Hội thoại** và cũng không có control chọn preset.
- Khi mở lại Agent đã tạo, có thêm tab **Chia sẻ**.
- Khi Agent chưa chọn KB, nhóm tool **Truy hồi tri thức** bị mờ với chú thích *Cần có kho tri thức trong phạm vi*. Chọn KB trước, mới bật được tool.

## Năm lớp và ai chịu trách nhiệm

Dùng bảng này để biết lỗi thuộc lớp nào trước khi sửa.

| Lớp | Người phụ trách | Control phải kiểm tra | Sai ở lớp này thường biểu hiện |
|---|---|---|---|
| Nội dung | Owner KB | Markdown, phiên bản, nguồn và ảnh | Nguồn sai hoặc thiếu bằng chứng |
| Truy hồi | Owner Agent | KB, loại file, `@`, tool, ngưỡng, reranker | Không có nguồn hoặc nguồn nhiễu |
| Hành vi | Owner Agent | preset, System Prompt, Intent, model | Có nguồn đúng nhưng tổng hợp sai |
| Giao tiếp | Người dùng / owner | chat mới, lịch sử, feedback, Request Information | Không tái hiện được lỗi |
| Quyền và vòng đời | Owner / Space admin | bật/tắt, chia sẻ, rà soát, rollback | Người không đúng quyền thấy hoặc sửa Agent |

## Thuật ngữ trên giao diện

| Thuật ngữ | Ý nghĩa khi vận hành |
|---|---|
| **Trợ lý / Agent** | Cấu hình chat có thể dùng lại, không phải bản gốc tri thức |
| **Intent** | Nhãn phân loại lượt chat, dùng để chọn prompt ghi đè và hướng xử lý |
| **Nguồn** | File hoặc đoạn được hiển thị làm căn cứ; phải mở ra kiểm tra khi đánh giá |
| **Request Information** | Hộp hiển thị ID, method, URL và thời điểm request; dùng để đối chiếu khi cần hỗ trợ |
| **Preset** | Cấu hình khởi đầu, không phải bảo đảm chất lượng |

## Các bước dựng và vận hành một Agent

1. Xác định use case, người dùng, dữ liệu được phép dùng và tiêu chí thế nào là câu trả lời đạt.
2. Tạo một Agent thử nghiệm riêng. Không cấu hình thử trực tiếp trên Agent mặc định hoặc Agent đang chạy thật.
3. Chọn KB có chủ đích, đúng phạm vi nghiệp vụ mà Agent phục vụ.
4. Thiết lập prompt, model, công cụ và chiến lược truy hồi. Chụp lại màn hình cấu hình làm mốc trước khi thử nghiệm A/B.
5. Chạy tối thiểu năm loại câu: một câu có đáp án rõ, một câu có hai tài liệu mâu thuẫn, một câu ngoài phạm vi KB, một câu hỏi tiếp và một tệp đính kèm.
6. Mở khung nguồn và Request Information, phân loại lỗi theo lớp trước khi sửa bất cứ thứ gì.
7. Chỉ phát hành hoặc chia sẻ sau khi chạy lại bộ câu hồi quy. Giữ bản sao cấu hình và cách quay lui.

## Luồng xử lý một câu hỏi

```text
Agent config
  → phân loại Intent
  → prompt chính hoặc prompt Intent ghi đè
  → lựa chọn KB/file + tool
  → tìm theo ngữ nghĩa / từ khóa / wiki / dữ liệu
  → ngưỡng + Top K + reranker
  → context cho model → trả lời, chip nguồn, feedback
```

Intent chỉ là lớp định tuyến. Nó không tự quyết định một lượt chat có gọi KB hay không. Kết quả thật còn phụ thuộc System Prompt, tool đã bật, KB/file được chọn, model và quota.

## Bộ câu kiểm thử tối thiểu

| Tình huống | Đầu vào mẫu | Kỳ vọng | Dấu hiệu đạt |
|---|---|---|---|
| Chào hỏi | "Xin chào, bạn giúp gì?" | Phản hồi trực tiếp, phù hợp | Không bịa nguồn |
| Hỏi đáp chuẩn | Một câu có đáp án rõ trong KB | Trả lời đúng và nêu nguồn | Chip nguồn trỏ đúng tài liệu |
| Xung đột | Câu mà KB có hai tài liệu nói khác nhau | Nêu rõ đây là mâu thuẫn | Không âm thầm chọn một giá trị |
| Ngoài phạm vi | Một chính sách không hề có trong KB | Nói không có thông tin | Không tạo nội dung tưởng tượng |
| Tệp đính kèm | Một PDF quen thuộc | Phân tích đúng nội dung tệp | Kết quả khớp tệp đã gửi |

## Lỗi và giới hạn cần nhớ

- Không biến Agent thành nơi lưu bản gốc hoặc kênh thay cho Markdown nguồn.
- Khi model báo lỗi quota hoặc `429`, đừng vội kết luận KB hỏng. Lỗi model và lỗi truy hồi là hai chuyện khác nhau.
- Chip nguồn chưa phải bằng chứng. Phải mở đúng file và đúng đoạn, so với câu trả lời.
- Ảnh chỉ hiện trong câu trả lời khi có Markdown tham chiếu tới nó. Nạp ảnh vào kho mà không có tài liệu nào trỏ tới thì Agent không có cớ để đưa ảnh ra.
- Danh sách Agent trên trang danh sách có thể hiển thị chậm hoặc nhảy vị trí sau mỗi lần lưu. Mở dialog và xác nhận đúng tên Agent trước mọi thao tác.

## Checklist trước khi phát hành

- [ ] Use case, phạm vi KB và người phụ trách đã nêu rõ.
- [ ] Agent thử nghiệm tách khỏi Agent mặc định và Agent đang chạy thật.
- [ ] Đã chạy đủ câu đúng, câu mâu thuẫn, câu ngoài phạm vi và tệp đính kèm.
- [ ] Đã mở khung nguồn và Request Information cho ít nhất một lượt quan trọng.
- [ ] Có bản sao cấu hình và đường quay lui khi cần.
