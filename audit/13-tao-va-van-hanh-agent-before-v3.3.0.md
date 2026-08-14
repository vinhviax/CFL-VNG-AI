<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 13 - Tạo và vận hành Agent {#13-tao-va-van-hanh-agent}

## Bạn sẽ biết gì sau khi đọc

- Agent khác Knowledge Base ở đâu và hai phần phối hợp như thế nào.
- `Intent` là gì, khi nào câu hỏi đi thẳng tới model và khi nào cần truy hồi KB.
- Ý nghĩa của sáu tab khi bấm **Tạo trợ lý**.
- Cách chọn model, KB, công cụ, ngưỡng truy hồi và cấu hình đa phương thức.
- Cách kiểm thử chat, nguồn tham khảo, ảnh và câu hỏi ngoài phạm vi.
- Cách xem đánh giá, lọc phản hồi và quản lý trạng thái xử lý.

**Kiểm chứng giao diện và thao tác live: 11/08/2026.**

## 1. Agent là gì

Agent là lớp trò chuyện đứng giữa Human và các nguồn tri thức. Knowledge Base giữ nội dung làm căn cứ; Agent giữ chỉ dẫn hành vi, model, phạm vi KB, công cụ và cách truy hồi để tạo câu trả lời.

```text
Human
  → Agent nhận câu hỏi và nhận diện intent
    → trả lời trực tiếp cho intent không cần truy hồi
    hoặc
    → gọi công cụ tìm trong KB → xếp hạng kết quả → model tổng hợp
  → câu trả lời + nguồn tham khảo + phản hồi của Human
```

Không xem Agent là nơi lưu bản gốc. Khi nội dung nghiệp vụ thay đổi, sửa và phát hành lại KB trước; Agent sẽ dùng bản KB mà nó được cấp quyền và cấu hình truy hồi.

Trong kiến trúc của bộ sổ tay này:

- Agent nghiệp vụ chọn **Knowledge VNG AI** làm kho trả lời; kho này chứa Markdown.
- **Knowledge VNG - Image Assets** chỉ giữ PNG và cung cấp URI MinIO cho ảnh trong Markdown. Không chọn kho asset làm corpus trả lời thông thường.
- Một câu trả lời có ảnh vẫn truy hồi Markdown ở KB sử dụng; URI trong Markdown dẫn tới ảnh do KB asset giữ.

## 2. Trang danh sách Agent

<!-- LOCAL_ASSET: assets/26-agent-tong-quan-danh-sach.png -->
![Trang tổng quan danh sách Agent](minio://knowledge-base-prd/10012/exports/7e5d2b38-a440-4c4e-a458-f88f11d78bcf.png)

*Ảnh 13.1 - Trang Trợ lý có bộ lọc phạm vi, tìm kiếm, đổi kiểu hiển thị và nút `Tạo trợ lý`.*

Thanh phạm vi đã quan sát gồm:

- **Tất cả agent**: mọi Agent người dùng được phép thấy.
- **Của tôi**: Agent do người dùng tạo.
- **Mặc định**: Agent có sẵn của hệ thống.
- **Được chia sẻ với tôi**: Agent nhận qua Space.
- **Đã đánh dấu**: Agent đã bấm biểu tượng sao.
- **Gần đây**: Agent vừa mở hoặc dùng.
- **Spaces**: nhóm Agent theo Space mà người dùng tham gia.

Có thể tìm theo tên hoặc mô tả, chuyển danh sách/lưới và đánh dấu sao. Ảnh kiểm chứng hiển thị sáu Agent mặc định:

| Agent mặc định | Mục đích thể hiện trên UI |
|---|---|
| Quick Answer | Hỏi đáp RAG nhanh và chính xác từ KB |
| Smart Reasoning | Suy luận ReAct nhiều bước và gọi công cụ |
| Hybrid Researcher | Tìm rộng qua Wiki và chunk, sau đó đào sâu với nguồn |
| Wiki Questioner | Hỏi đáp chuyên biệt trên Knowledge Base có Wiki |
| Data Analyst | Phân tích CSV/Excel bằng SQL và thống kê |
| FPA Analyst | Phân loại câu hỏi, chọn nguồn phù hợp rồi truy hồi |

Danh sách mặc định và quyền thao tác có thể khác theo tenant. Không sửa, tắt hoặc xóa Agent mặc định chỉ để thử chức năng.

## 3. Chọn chế độ chạy và preset

Khi bấm **Tạo trợ lý**, chọn một trong hai chế độ:

- **Suy luận thông minh**: UI mô tả là suy nghĩ nhiều bước và phân tích sâu cho câu hỏi phức tạp. Chế độ này hiển thị **Loại trợ lý** để chọn preset.
- **Trả lời nhanh**: UI mô tả là phản hồi nhanh và trả lời trực tiếp. Trong lượt kiểm chứng, control preset không còn hiển thị sau khi chuyển sang chế độ này.

Ở **Suy luận thông minh**, UI cung cấp năm điểm bắt đầu:

1. **Hỏi đáp RAG**.
2. **Hỏi đáp Wiki**.
3. **Kết hợp RAG + Wiki**.
4. **Phân tích dữ liệu**.
5. **Tùy chỉnh**.

Preset điền sẵn prompt và nhóm công cụ phù hợp; nó là cấu hình khởi đầu, không thay thế bước kiểm tra từng tab. Với tài liệu vận hành dạng Markdown và ảnh MinIO, có thể chọn **Suy luận thông minh** rồi bắt đầu bằng **Hỏi đáp RAG** hoặc **Tùy chỉnh**, sau đó chỉ chọn `Knowledge VNG AI` và loại tệp `MD`.

Hộp tạo mới có sáu tab:

1. Thông tin cơ bản.
2. Cấu hình mô hình.
3. Kho tri thức.
4. Công cụ.
5. Chiến lược truy hồi.
6. Cấu hình đa phương thức.

Khi **Chỉnh sửa** Agent đã tạo, UI có thêm tab **Chia sẻ**. Đây là khác biệt đã quan sát giữa chế độ tạo và chế độ sửa.

## 4. Thông tin cơ bản và Intent

<!-- LOCAL_ASSET: assets/27-agent-thong-tin-co-ban-va-intent.png -->
![Thông tin cơ bản và danh sách Intent](minio://knowledge-base-prd/10012/exports/431c4578-8b28-4d38-b1cc-1a27717a23c7.png)

*Ảnh 13.2 - Prompt chính và vùng `Prompt theo intent`; để trống prompt riêng thì dùng mặc định.*

Tab này giữ tên, mô tả, chỉ dẫn chính và các prompt chuyên biệt. Prompt chính nên nêu rõ:

- vai trò và phạm vi nghiệp vụ;
- nguồn nào được xem là căn cứ;
- cách trích nguồn và cách xử lý khi không tìm thấy;
- định dạng câu trả lời mong muốn;
- điều Agent không được tự suy đoán.

### Intent là gì

`Intent` là loại mục đích mà hệ thống nhận ra trong tin nhắn của Human. Nó không phải KB, tài liệu hay công cụ. Intent giúp Agent chọn nhánh phản hồi phù hợp; ví dụ lời chào không cần tìm KB, còn yêu cầu tóm tắt tài liệu đính kèm cần nhánh xử lý tài liệu.

Sáu intent quan sát được trên UI:

| Intent trên UI | Khi dùng | Kết quả live 11/08/2026 |
|---|---|---|
| Greeting Response | Chào hỏi | Trả lời trực tiếp, không hiện nguồn |
| Chitchat Response | Tán gẫu | Trả lời trực tiếp |
| Follow-up Response | Hỏi tiếp theo ngữ cảnh hội thoại | Dùng được ngữ cảnh trước đó |
| Image Analysis Response | Đọc ảnh đính kèm | Có điều kiện; UI hiện preview nhưng lượt test không truyền ảnh tới Agent |
| Summarize Response | Tóm tắt nội dung/tài liệu | Tóm tắt Markdown đúng yêu cầu năm gạch đầu dòng |
| Document Analysis Response | Phân tích tài liệu | Phân tích được Markdown đính kèm |

`Prompt cho intent này` ghi đè prompt dùng cho intent đã chọn. Để trống thì hệ thống dùng template mặc định. UI gợi ý đúng các biến `{{query}}`, `{{contexts}}`, `{{current_time}}`, `{{current_week}}` và `{{language}}`; chỉ dùng biến đúng cú pháp đang hiển thị. Ở System Prompt của chế độ Suy luận thông minh, bộ biến quan sát được là `{{knowledge_bases}}`, `{{current_time}}` và `{{language}}`.

Không suy luận rằng mọi intent đều bỏ qua KB. Điều đã kiểm chứng chắc chắn là khu vực này được mô tả cho các intent không truy hồi như chào hỏi và tán gẫu; hành vi cuối còn phụ thuộc prompt, công cụ và model.

## 5. Cấu hình mô hình

<!-- LOCAL_ASSET: assets/28-agent-cau-hinh-mo-hinh.png -->
![Cấu hình model, reranker, nhiệt độ và suy nghĩ](minio://knowledge-base-prd/10012/exports/b976d174-9f47-4581-92aa-8218c3db2f38.png)

*Ảnh 13.3 - Danh sách model quan sát ngày 11/08/2026; việc có tên trong UI không bảo đảm còn quota.*

Model chat quan sát được:

- `deepseek-v4-flash`;
- `gpt-oss-120b`;
- `hosted_vllm/qwen3.6-35b`;
- `qwen3.6-plus`.

Model xếp hạng lại đã chọn trong lượt test là `bge-reranker-v2-m3`.

Các điều khiển chính:

- **Mô hình**: LLM tạo câu trả lời và điều phối công cụ.
- **Mô hình xếp hạng lại**: chấm lại độ liên quan của các đoạn đã truy hồi.
- **Nhiệt độ**: UI mô tả `0` ổn định nhất và `1` ngẫu nhiên nhất; preset quan sát ở `0,7`. Lượt test nghiệp vụ hạ xuống `0,2` để câu trả lời nhất quán hơn.
- **Chế độ suy nghĩ**: bật khả năng suy nghĩ mở rộng khi model hỗ trợ.

Trong kiểm thử live, `deepseek-v4-flash` và một lượt `qwen3.6-plus` trả `429 insufficient_quota`; `hosted_vllm/qwen3.6-35b` vẫn trả lời được câu ngoài KB. Vì vậy:

1. Không ghi cứng một model là luôn khả dụng.
2. Kiểm tra quota bằng chat thật sau khi lưu.
3. Khi đổi model, chạy lại cùng bộ câu hỏi và kiểm tra cả nguồn lẫn cách tổng hợp.

## 6. Kho tri thức

<!-- LOCAL_ASSET: assets/29-agent-kho-tri-thuc.png -->
![Chọn phạm vi Knowledge Base và loại tệp](minio://knowledge-base-prd/10012/exports/8208154f-e74f-4630-b44c-6346992ddaee.png)

*Ảnh 13.4 - Agent test chỉ dùng `Knowledge VNG AI`, loại `MD`; `Chỉ truy hồi khi được nhắc` đang tắt.*

Ba phạm vi:

- **Tất cả kho tri thức**: Agent có thể dùng mọi KB mà người dùng/Agent được phép truy cập.
- **Kho tri thức đã chọn**: giới hạn vào danh sách cụ thể; đây là lựa chọn dễ kiểm soát nhất cho production.
- **Không dùng kho tri thức**: dùng cho Agent không cần RAG.

Loại tệp quan sát được gồm `PDF`, `DOCX`, `TXT`, `MD`, `CSV`, `XLSX`, `XLS`, `JSON`, `PPTX`, `HTML`, `MSG` và `EML`. Để trống danh sách loại tệp nghĩa là cho phép mọi loại được hỗ trợ trong phạm vi KB.

### Chỉ truy hồi khi được nhắc

- **Tắt**: Agent tự động dùng KB đã cấu hình khi thấy cần.
- **Bật**: chỉ truy hồi khi Human dùng `@` để nhắc KB/tệp trong composer.

Phép thử cho thấy khi bật rồi gỡ chip KB, lượt hỏi không có phạm vi để truy hồi. Sau khi thêm `Knowledge VNG AI (13)` qua **Nhắc tri thức / tệp**, hệ thống có gọi truy hồi; tuy nhiên model hosted ở lượt đó lộ chuỗi thô `[[chunk#12]]` thay vì tổng hợp hoàn chỉnh. Vì vậy tách hai lớp khi chẩn đoán: `@` quyết định phạm vi truy hồi, còn model/prompt quyết định chất lượng tổng hợp.

Với Agent phục vụ chung từ một KB đã duyệt, nên để công tắc này **tắt**. Chỉ bật khi Human phải chủ động chọn nguồn cho từng lượt.

## 7. Công cụ

<!-- LOCAL_ASSET: assets/30-agent-cong-cu.png -->
![Chọn công cụ và giới hạn vòng lặp](minio://knowledge-base-prd/10012/exports/50273f87-b180-4d1c-a6b2-5cbf4db97d8b.png)

*Ảnh 13.5 - Vùng công cụ hiệu lực, số vòng lặp, timeout LLM và gọi song song.*

Agent test dùng năm công cụ hiệu lực:

| Công cụ | Vai trò thực hành |
|---|---|
| Suy nghĩ | Lập bước và quyết định gọi công cụ tiếp theo |
| Tìm theo ngữ nghĩa | Tìm đoạn gần nghĩa bằng vector |
| Tìm theo từ khóa | Tìm thuật ngữ/tên/mã xuất hiện trực tiếp |
| Liệt kê đoạn | Duyệt các chunk có thể dùng |
| Thông tin tài liệu | Đọc metadata và nhận diện tài liệu nguồn |

UI còn hiển thị nhóm Wiki với **Tìm wiki**, **Đọc trang wiki**, **Đọc tài liệu nguồn** và nhóm dữ liệu với **Phân tích dữ liệu**, **Lược đồ dữ liệu**. Các công cụ này được quan sát nhưng chưa kiểm thử end-to-end trong Agent test của sổ tay; chỉ bật khi Agent thực sự có Wiki hoặc dữ liệu bảng tương ứng.

Giới hạn đã kiểm tra:

- **Số vòng lặp tối đa**: `10`.
- **Thời gian chờ gọi LLM**: `120` giây.
- **Gọi công cụ song song**: đã bật/tắt thử và để tắt ở cấu hình bàn giao.

Tăng vòng lặp không tự làm câu trả lời đúng hơn. Nhiều công cụ và nhiều vòng lặp làm tăng thời gian, chi phí và số nhánh lỗi; bắt đầu với bộ tối thiểu rồi bổ sung theo bằng chứng.

## 8. Chiến lược truy hồi

<!-- LOCAL_ASSET: assets/31-agent-chien-luoc-truy-hoi.png -->
![Top K và các ngưỡng truy hồi](minio://knowledge-base-prd/10012/exports/c7d2a27c-4720-4b4c-838d-c794050b5e89.png)

*Ảnh 13.6 - Giá trị mặc định đã quan sát và khôi phục sau kiểm thử.*

| Tham số | Giá trị quan sát | Ý nghĩa |
|---|---:|---|
| Top K vector | 10 | Lấy tối đa 10 kết quả từ truy hồi vector |
| Ngưỡng từ khóa | 0,3 | Điểm liên quan tối thiểu của tìm từ khóa |
| Ngưỡng vector | 0,5 | Điểm tương đồng tối thiểu của tìm vector |
| Top K xếp hạng lại | 5 | Giữ tối đa 5 kết quả sau rerank |
| Ngưỡng xếp hạng lại | 0,5 | Điểm tối thiểu sau rerank |

Hiểu theo thứ tự:

1. Từ khóa và vector tạo danh sách ứng viên.
2. Các ngưỡng đầu loại kết quả yếu.
3. Reranker chấm lại ứng viên còn lại.
4. Top K và ngưỡng rerank quyết định phần context cuối đưa cho model.

Ngưỡng quá cao có thể bỏ sót; quá thấp có thể đưa nhiễu. Khi tối ưu, đổi một tham số mỗi lần và chạy lại cùng bộ câu hỏi đúng, diễn đạt lại, dễ nhầm và ngoài phạm vi.

## 9. Cấu hình đa phương thức

<!-- LOCAL_ASSET: assets/32-agent-cau-hinh-da-phuong-thuc.png -->
![Bật tải ảnh, chọn VLM và cấu hình âm thanh](minio://knowledge-base-prd/10012/exports/dfac9762-3573-4725-9925-b474d134d835.png)

*Ảnh 13.7 - Tải ảnh bật với VLM `qwen3.6-plus`; tải âm thanh để tắt vì tenant chưa có ASR model.*

- **Tải ảnh** cho phép Human gắn ảnh vào hội thoại; phải chọn **Mô hình VLM**.
- **Tải âm thanh** cho phép gắn audio; hệ thống cần **Mô hình ASR** để chuyển giọng nói thành văn bản.

Lượt test chọn VLM `qwen3.6-plus`. Composer hiển thị preview ảnh, nhưng hai tin nhắn gửi đi không mang ảnh tới Agent và `Image Analysis Response` trả lời rằng không nhận được ảnh. Đây là lỗi/điều kiện ở bước bàn giao attachment, chưa đủ bằng chứng kết luận VLM không đọc được ảnh.

Khi bật âm thanh, hộp chọn ASR báo **Chưa có model — liên hệ admin để thêm** và không cho hoàn tất cấu hình hợp lệ. Vì vậy audio/ASR là **bị chặn theo tenant** ở ngày kiểm chứng, không phải tính năng đã pass.

Phân tích tài liệu và tóm tắt Markdown đính kèm đã pass; đây là nhánh tài liệu, không chứng minh nhánh ảnh hoặc audio.

## 10. Tạo, sửa, nhân bản, tắt và chia sẻ

Vòng đời đã thao tác trên Agent test do người dùng cho phép:

1. Tạo Agent và lưu thành công.
2. Mở **Chỉnh sửa**, thay cấu hình và lưu; mở lại thấy giá trị vẫn còn.
3. Đánh dấu sao rồi bỏ đánh dấu.
4. **Nhân bản**; bản sao kế thừa model, KB và công cụ, sau đó được đổi tên.
5. **Tắt** rồi **Bật** lại bản sao; trạng thái cuối là bật.
6. Mở tab **Chia sẻ** trong chế độ sửa; UI cho chọn Space `CFL Member` với vai trò **Chỉ xem** hoặc **Được chỉnh sửa**. Không gửi chia sẻ trong phép thử.

Menu của Agent do người dùng tạo gồm **Trò chuyện**, **Chỉnh sửa**, **Nhân bản**, **Tắt/Bật** và **Xóa**. Không dùng **Xóa** trong lượt kiểm chứng. Trước khi xóa Agent thật, phải xác nhận owner, nơi đang chia sẻ, bộ câu hỏi hồi quy và khả năng khôi phục; xóa Agent không phải cách cập nhật nội dung KB.

## 11. Kiểm thử chat và nguồn tham khảo

<!-- LOCAL_ASSET: assets/33-agent-chat-nguon-va-anh.png -->
![Chat RAG hiển thị nguồn Markdown và ảnh MinIO](minio://knowledge-base-prd/10012/exports/37ad90a4-9160-4399-8c36-0e882141f2d9.png)

*Ảnh 13.8 - Agent truy hồi module Google Drive, hiện chip nguồn và render ảnh do URI MinIO cung cấp.*

Bộ test tối thiểu và kết quả live:

| Nhóm | Câu hỏi/đầu vào | Kỳ vọng | Kết quả 11/08/2026 |
|---|---|---|---|
| Greeting | Lời chào | Trả lời ngắn, không truy hồi không cần thiết | Pass |
| Chitchat | Tán gẫu | Trả lời trực tiếp | Pass |
| Follow-up | Hỏi tiếp chủ đề trước | Giữ ngữ cảnh | Pass |
| Document Analysis | Đính kèm một module Markdown | Phân tích cấu trúc và nội dung | Pass |
| Summarize | Yêu cầu đúng năm gạch đầu dòng | Tóm tắt đúng định dạng | Pass |
| RAG đúng phạm vi | Hỏi quy trình Google Drive | Dùng `12-ket-noi-google-drive.md`, hiện nguồn và ảnh | Pass có điều kiện model/quota |
| Ngoài KB | Hỏi chính sách nghỉ phép 2027 không có trong kho | Nói không tìm thấy, không bịa | Pass với model hosted |
| Image Analysis | Gắn ảnh UI | Đọc tiêu đề và điều khiển | Chưa pass ở bước truyền attachment |
| Audio/ASR | Gắn audio | Chuyển âm thanh thành text | Bị chặn vì không có ASR model |

Khi đánh giá RAG:

1. Đọc câu trả lời.
2. Mở chip nguồn và xác nhận đúng tài liệu.
3. Kiểm tra đoạn nguồn thực sự chứa bằng chứng.
4. Nếu câu trả lời yêu cầu ảnh, xác nhận ảnh render trong chat chứ không chỉ có link.
5. Hỏi một câu ngoài phạm vi để kiểm tra Agent biết dừng.

`429 insufficient_quota` là lỗi khả dụng model, không phải bằng chứng KB không truy hồi. Ngược lại, có nguồn đúng nhưng câu tổng hợp sai là lỗi prompt/model hoặc context, không nên sửa dữ liệu nguồn ngay lập tức.

## 12. Đánh giá câu trả lời và Hộp xử lý

<!-- LOCAL_ASSET: assets/34-agent-danh-gia-cau-tra-loi.png -->
![Tổng quan đánh giá và trạng thái xử lý](minio://knowledge-base-prd/10012/exports/20b70b5a-db3f-4a71-89df-56e821628684.png)

*Ảnh 13.9 - Hai phản hồi test tạo tỷ lệ tích cực 50%; một mục Mới và một mục Đã xử lý.*

Tab **Đánh giá câu trả lời** có hai chế độ:

- **Tổng quan**: tổng đánh giá, số hữu ích/chưa hữu ích, tỷ lệ tích cực, biểu đồ theo ngày, chất lượng theo Agent và các hàng phản hồi.
- **Hộp xử lý**: danh sách phản hồi bên trái và toàn bộ đoạn hội thoại liên quan bên phải.

Bộ lọc đã kiểm tra:

- khoảng thời gian với preset Today, Yesterday, Last 7 days, Last 30 days, This month, Last month và lịch tùy chọn;
- Agent;
- tất cả/hữu ích/chưa hữu ích;
- có bình luận;
- tìm trong nội dung bình luận.

Mỗi phản hồi có trạng thái **Mới**, **Đang xem** hoặc **Đã xử lý**. Lượt test chuyển một phản hồi chưa hữu ích qua đủ chuỗi `Mới → Đang xem → Đã xử lý`; các bộ đếm **Cần xử lý**, **Đang xem**, **Đã xử lý** cập nhật theo trạng thái. Hai bình luận test được giữ làm bằng chứng audit: một phản hồi RAG hữu ích và một phản hồi Image Analysis chưa hữu ích.

Quy trình xử lý khuyến nghị:

1. Lọc Agent và thời gian cần xem.
2. Mở phản hồi chưa hữu ích trong Hộp xử lý.
3. Đọc cả hội thoại, model và nguồn; không chỉ đọc bình luận cuối.
4. Chuyển **Đang xem** khi bắt đầu điều tra.
5. Phân loại lỗi: nguồn, truy hồi, prompt, model/quota, attachment hay quyền.
6. Sửa đúng lớp và chạy lại câu hỏi.
7. Chuyển **Đã xử lý** khi có bằng chứng hồi quy.

## 13. Cấu hình khởi đầu cho Agent dùng Knowledge VNG AI

Đây là baseline vận hành, không phải giá trị tối ưu cho mọi use case:

| Tab | Baseline |
|---|---|
| Thông tin cơ bản | Vai trò rõ, chỉ dùng nguồn được truy hồi, không bịa khi thiếu dữ liệu, luôn nêu nguồn |
| Mô hình | Chọn model còn quota; nhiệt độ khoảng `0,2` cho hướng dẫn nghiệp vụ; reranker `bge-reranker-v2-m3` nếu khả dụng |
| Kho tri thức | **Kho tri thức đã chọn** → `Knowledge VNG AI`; loại `MD`; để tắt **Chỉ truy hồi khi được nhắc** |
| Công cụ | Suy nghĩ, Tìm theo ngữ nghĩa, Tìm theo từ khóa, Liệt kê đoạn, Thông tin tài liệu |
| Giới hạn | 10 vòng, timeout 120 giây, gọi song song tắt ở lượt đầu |
| Truy hồi | Bắt đầu từ 10 / 0,3 / 0,5 / 5 / 0,5 rồi đo bằng bộ câu hỏi thật |
| Đa phương thức | Chỉ bật ảnh khi đã test attachment + VLM; để audio tắt nếu chưa có ASR |

Sau khi lưu, bắt buộc chạy ít nhất một câu đúng, một câu diễn đạt lại, một câu ngoài phạm vi, một câu cần nguồn và một câu cần ảnh nếu use case có ảnh.

## 14. Chẩn đoán nhanh

| Hiện tượng | Kiểm tra trước |
|---|---|
| `429 insufficient_quota` | Quota/model; thử model đã được phép và chạy lại cùng câu hỏi |
| Không có nguồn | Phạm vi KB, loại tệp, công tắc chỉ truy hồi khi được nhắc, chip `@`, công cụ tìm kiếm và ngưỡng |
| Có chunk nhưng lộ `[[chunk#...]]` | Lớp tổng hợp của model/prompt; thử model khác trước khi sửa KB |
| Nguồn đúng, câu trả lời sai | Prompt, model, thứ tự context và nhiệt độ |
| Nguồn sai hoặc nhiễu | KB được chọn, từ khóa/vector, Top K, các ngưỡng và reranker |
| Composer hiện preview nhưng Agent nói không có ảnh | Bước truyền attachment; lưu bằng chứng UI/network và không kết luận VLM hỏng |
| Không bật được audio | Kiểm tra tenant có ASR model hay chưa |
| Agent chạy lâu hoặc lặp | Số công cụ, số vòng tối đa, timeout, gọi song song và model |
| Không thấy Agent trong Space | Tab Chia sẻ, Space, vai trò và trạng thái bật/tắt |

## 15. Điều chưa được phép suy luận

Lượt kiểm chứng này chưa chứng minh:

- mọi model trong dropdown luôn có quota;
- Image Analysis hoạt động end-to-end khi composer đã hiện preview;
- audio hoạt động khi tenant chưa có ASR model;
- các công cụ Wiki và phân tích dữ liệu đúng với mọi loại KB/file;
- gọi công cụ song song luôn nhanh hơn hoặc cho cùng thứ tự bằng chứng;
- quyền **Chỉ xem** và **Được chỉnh sửa** đúng cho mọi Space, vì phép thử không gửi chia sẻ;
- hành vi **Xóa** và khả năng khôi phục Agent.

Xem cấu hình, Agent ID, URL hội thoại và kết quả chi tiết tại [audit Agent ngày 11/08/2026](../audit/agent-live-test-2026-08-11.md).
