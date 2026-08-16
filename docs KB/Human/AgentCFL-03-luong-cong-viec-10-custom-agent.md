# Luồng công việc của 10 trợ lý GS9 CFL

Đọc xong phần này bạn biết trợ lý nào đứng ở khâu nào, và khi chuyển việc sang khâu sau thì phải mang theo những gì.

## Bốn giai đoạn

**1. Chuẩn bị sự kiện**

- `LiveOps Planner` — brief sự kiện, lịch, dependency, rủi ro, ai duyệt cái gì.
- `Economy Offer Analyst` — giá, phần thưởng, dòng vào – dòng ra, tính công bằng.
- `KPI Experiment Analyst` — chỉ số cần theo dõi, mốc so sánh, cohort, cách đo.
- `Player Communications` — nháp thông báo, thư trong game, push, bản dịch.

**2. Trước khi phát hành**

- `Release Reviewer` — kiểm tra trước phát hành, liệt kê vấn đề chặn, đánh giá khả năng rollback.
- Sau đó **Release Owner là người quyết định**. Việc đưa lên live do hệ thống và con người thực hiện, không phải trợ lý.

**3. Khi đang chạy live**

- `Incident Triage` — tách sự thật khỏi giả thuyết, dựng dòng thời gian, đề xuất mức độ, gợi ý bước kiểm tra tiếp theo.
- `CS Copilot` — nháp trả lời có trích nguồn và đề xuất chuyển cấp.
- `GM Policy Advisor` — chỉ ra điều khoản áp dụng kèm mã điều khoản cho GM được phân quyền.

**4. Sau sự kiện**

- `Player Voice Analyst` — chủ đề và cảm xúc trên dữ liệu đã ẩn danh.
- `KPI Experiment Analyst` — kết quả thực tế và giới hạn của phép đo.
- `Knowledge Curator` — postmortem, bài học, việc cần làm, đề xuất sửa kho tri thức.

Không khâu nào trong luồng này cho phép trợ lý tự phát hành, tự triển khai, tự rollback, tự gửi tin, tự tặng thưởng, tự bồi thường, tự chế tài hay tự sửa kho tri thức.

## Bàn giao giữa các khâu

Khi chuyển kết quả từ trợ lý này sang trợ lý khác hoặc sang người, mang theo tối thiểu:

| Từ | Sang | Phải mang theo |
|---|---|---|
| `LiveOps Planner` | Economy, KPI, Communications, Release | Phiên bản brief, khu vực và nền tảng, giờ theo UTC và giờ địa phương, người chịu trách nhiệm, các cam kết đã duyệt, dependency |
| `Economy Offer Analyst` | Planner, Release, KPI | Mã vật phẩm, cách tính giá và phần thưởng, giả định đã dùng, rủi ro, trạng thái phê duyệt |
| `KPI Experiment Analyst` | Planner, Release, Curator | Định nghĩa chỉ số, bộ dữ liệu, độ tươi dữ liệu, bộ lọc, mẫu số, cách tính để người khác dựng lại được |
| `Player Communications` | Release, người phát hành | Các biến thể nháp, danh sách cam kết cần kiểm, phiên bản thuật ngữ, ngôn ngữ, trạng thái duyệt |
| `Release Reviewer` | Release Owner | Vấn đề chặn, các bước kiểm bắt buộc, điều kiện rollback, khuyến nghị dạng nháp |
| `Incident Triage` | Incident Commander, CS, Curator | Phần nào là sự thật phần nào là giả thuyết, dòng thời gian, phạm vi ảnh hưởng, chỗ còn thiếu bằng chứng, bước kiểm tiếp theo |
| `CS Copilot` | Nhân viên CS, GM | Nháp trả lời có trích nguồn, thông tin còn thiếu, lý do chuyển cấp — không kèm dữ liệu người chơi ngoài phạm vi |
| `GM Policy Advisor` | GM được phân quyền | Điều khoản áp dụng kèm mã, cách ánh xạ vào tình huống, chỗ chính sách còn trống hoặc mâu thuẫn |
| `Player Voice Analyst` | Product, LiveOps | Độ phủ dữ liệu, cỡ mẫu, ngưỡng bảo vệ nhóm nhỏ, các chủ đề, mức không chắc chắn |
| `Knowledge Curator` | Knowledge Owner | Bản nháp có dẫn nguồn, nguyên nhân gốc còn bỏ ngỏ, đề nghị phân công, các thay đổi kho tri thức đề xuất |

## Ranh giới dữ liệu khi bàn giao

- Chỉ chuyển đúng phần dữ liệu mà khâu sau cần. Không chuyển cả gói cho tiện.
- Không đưa ticket thô, định danh người chơi, khoá bí mật hay thông tin đăng nhập vào bất kỳ bản bàn giao nào.
- GM chỉ nhận hồ sơ trong phạm vi vụ việc đã được duyệt. CS không tự chuyển dữ liệu sang GM ngoài quy trình.
- `Player Voice Analyst` chỉ làm việc trên dữ liệu đã ẩn danh và đủ lớn để không lần ra được cá nhân.
- Đừng gắn một kho tri thức cho trợ lý chỉ vì tên kho nghe có vẻ hợp. Nguồn phải được chủ sở hữu duyệt trước.

## Luồng này là mục tiêu, chưa phải hiện trạng

Các khâu ở trên mô tả cách 10 trợ lý được thiết kế để phối hợp. Việc bàn giao thực tế giữa chúng chưa được chạy thử đầy đủ, nên khi dùng hãy tự kiểm lại đầu vào và đầu ra ở mỗi khâu thay vì tin rằng khâu trước đã làm đúng.
