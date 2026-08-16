# So sánh 16 trợ lý

Đọc xong phần này bạn thấy được điểm mạnh, giới hạn và điểm cần cẩn thận của từng trợ lý, đặt cạnh nhau.

## Sáu trợ lý mặc định

| Trợ lý | Làm gì | Tra được nguồn nào | Điểm cần cẩn thận |
|---|---|---|---|
| `Quick Answer` | Hỏi đáp nhanh một lượt trên kho tri thức, có nhớ vài lượt hội thoại gần nhất | Toàn bộ kho tri thức, mọi loại tệp | Khi không tìm thấy tài liệu, có thể trả lời bằng kiến thức chung thay vì nói "không có" |
| `Smart Reasoning` | Tra cứu nhiều bước, tìm theo ngữ nghĩa và từ khoá rồi đọc sâu đoạn tài liệu | Toàn bộ kho tri thức, mọi loại tệp | Không tra được Wiki, không chạy SQL, không phân tích file bảng |
| `Hybrid Researcher` | Kết hợp Wiki để lấy tổng quan và đoạn tài liệu gốc để lấy dẫn chứng | Toàn bộ kho tri thức, mọi loại tệp | Khi Wiki và tài liệu gốc lệch nhau, hãy yêu cầu trợ lý nêu cả hai; đừng để nó tự chọn một bên |
| `Wiki Questioner` | Hỏi đáp trên Wiki: tìm trang, đọc trang, đi theo liên kết một hai bước | Toàn bộ kho tri thức, mọi loại tệp | Chỉ hữu ích khi Wiki được quản trị tốt; không đọc đoạn tài liệu gốc làm nguồn chính |
| `Data Analyst` | Đọc lược đồ rồi phân tích file CSV / Excel bằng truy vấn và thống kê | Toàn bộ kho tri thức nhưng chỉ file CSV và XLSX | Trợ lý chỉ được đọc, không được ghi; vẫn nên xem lại truy vấn nó viết ra |
| `FPA Analyst` | Quy trình cố định: hiểu câu hỏi, định tuyến nguồn, truy hồi rồi báo cáo hiệu suất | Toàn bộ kho tri thức, thêm danh mục sản phẩm và truy vấn CSDL | Quy trình nói là đã thu hẹp nguồn, nhưng phạm vi cấu hình vẫn để mở — tự kiểm tra kỳ, đơn vị và nguồn số liệu |

Điểm chung của cả sáu:

- Đều đặt phạm vi ở **toàn bộ kho tri thức**, nên đừng nhập dữ liệu nhạy cảm và đừng nhân bản chúng cho việc nhạy cảm.
- Đều tắt tải ảnh và tải âm thanh.
- Chỉ `Quick Answer` có hội thoại nhiều lượt; các trợ lý còn lại không giữ ngữ cảnh lượt trước.

## Mười trợ lý riêng của GS9 CFL

| Trợ lý | Việc chính | Trợ lý hỏi lại được không | Người duyệt kết quả |
|---|---|---|---|
| `LiveOps Planner` | Brief sự kiện, lịch, dependency, rủi ro | Có, và lập được danh sách việc | LiveOps Lead |
| `Release Reviewer` | Kiểm tra trước phát hành, mức sẵn sàng rollback | Có, và lập được danh sách việc | Release Owner |
| `Incident Triage` | Dòng thời gian, mức độ, giả thuyết nguyên nhân | Có, và lập được danh sách việc | Incident Commander |
| `KPI Experiment Analyst` | KPI, cohort, kết quả thử nghiệm | Có, và lập được danh sách việc | Data Analytics Lead |
| `Economy Offer Analyst` | Giá, phần thưởng, dòng vào – dòng ra, gói ưu đãi | Có, và lập được danh sách việc | Economy Owner |
| `Player Voice Analyst` | Chủ đề và cảm xúc trên phản hồi đã ẩn danh | Có | Player Insights Lead |
| `CS Copilot` | Phân loại ticket, nháp trả lời, đề xuất chuyển cấp | Trả lời một lượt, không có công cụ phụ | CS Lead |
| `GM Policy Advisor` | Tra và giải thích điều khoản xử phạt, quy trình | Có, và lập được danh sách việc | GM Lead |
| `Player Communications` | Thông báo, thư trong game, push, bản địa hoá | Có, và lập được danh sách việc | Communications Lead |
| `Knowledge Curator` | Postmortem, bài học, đề xuất sửa kho tri thức | Có, và lập được danh sách việc | Knowledge Owner |

Cả mười đều dùng chung một mô hình và chưa được ký duyệt phát hành. Khác biệt thật giữa chúng nằm ở **kho tri thức được gắn** và **quy tắc trong hướng dẫn hệ thống**, không nằm ở mô hình.

### Trợ lý nào đang gắn kho nào

| Trợ lý | Kho tri thức đang gắn |
|---|---|
| `Knowledge Curator` | `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI` |
| `KPI Experiment Analyst` | `GS9 CFL Kho Dữ Liệu Tổng Hợp` |
| `Incident Triage` | `GS9 CFL PUM` |
| `Player Voice Analyst` | `GS9 CFL Sentiment Feedback User` |
| `LiveOps Planner` | `GS9 Knowledge VNG AI` |
| `Release Reviewer` | `GS9 Knowledge VNG AI` |
| `CS Copilot` | **chưa gắn kho nào** |
| `Economy Offer Analyst` | **chưa gắn kho nào** |
| `GM Policy Advisor` | **chưa gắn kho nào** |
| `Player Communications` | **chưa gắn kho nào** |

Bốn trợ lý chưa gắn kho vẫn trả lời được, nhưng câu trả lời **không dựa trên nguồn nào của CFL** — đừng dùng kết quả của chúng làm căn cứ.

Hai kho `PUM` và `Sentiment Feedback User` chứa số liệu kinh doanh và phản hồi người chơi. Chúng được gắn có chủ đích cho công việc nội bộ, nhưng khi bạn sao chép kết quả ra ngoài nhóm thì vẫn nên tự lọc: bỏ số liệu chi tiết và thông tin nhận dạng người chơi.

Sáu trợ lý còn lại cũng cần đọc kỹ cột bên phải: phạm vi thật của chúng hẹp hơn tên gọi nhiều. `Incident Triage` chỉ tra được report tháng, chưa có runbook sự cố. `LiveOps Planner` và `Release Reviewer` đang gắn kho hướng dẫn nền tảng, chưa gắn kho nghiệp vụ LiveOps.

Bảng này là ảnh chụp một thời điểm. Kho gắn cho trợ lý đổi được bất cứ lúc nào, nên trước khi tin một câu trả lời quan trọng, hãy mở trợ lý ra xem nó đang gắn kho nào.

Lưu ý một điểm dễ nhầm: công cụ tên `Suy nghĩ` trong danh sách công cụ **không phải** là công tắc `Chế độ suy nghĩ` của mô hình. Đó là hai thứ khác nhau, bật tắt độc lập.

## Khác biệt cốt lõi giữa hai nhóm

| Trợ lý mặc định | Trợ lý riêng GS9 CFL |
|---|---|
| Cấu hình sẵn, mở phạm vi ra toàn bộ kho tri thức | Chỉ gắn đúng kho tri thức được duyệt cho vai trò đó |
| Không có chủ sở hữu nghiệp vụ cụ thể | Mỗi trợ lý có chủ sở hữu và người duyệt rõ ràng |
| Không thiết kế riêng cho ranh giới dữ liệu GS9 | Thiết kế theo nguyên tắc quyền tối thiểu |
| Dùng được ngay cho tra cứu thường ngày | Đang chuẩn bị, chưa dùng cho quyết định vận hành |
