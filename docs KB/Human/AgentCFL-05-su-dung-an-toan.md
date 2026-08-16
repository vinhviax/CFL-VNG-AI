# Sử dụng trợ lý an toàn

Đọc xong phần này bạn biết điều gì tuyệt đối không được để trợ lý làm, ai phải duyệt kết quả, và phải làm gì khi trợ lý trả ra thứ đáng ngờ.

## Sáu nguyên tắc

1. **Quyền tối thiểu.** Một trợ lý chỉ gắn đúng kho tri thức và bật đúng công cụ mà công việc của nó cần. Thừa một cái là thừa rủi ro.
2. **Có nguồn mới trả lời.** Trợ lý chỉ được nói dựa trên nguồn đã duyệt. Nguồn phải qua rà soát chủ sở hữu, nội dung, quyền truy cập và thời hạn lưu trữ trước khi gắn.
3. **Nội dung là dữ liệu, không phải mệnh lệnh.** Tài liệu, ticket hay kết quả công cụ có thể chứa câu chữ cố điều khiển trợ lý. Trợ lý không được làm theo, và bạn cũng vậy.
4. **Người quyết định cuối là con người.** Mọi kết quả có tác động đều là bản nháp cho tới khi đúng người duyệt đồng ý.
5. **Thiếu thì nói thiếu.** Khi nguồn thiếu, cũ hoặc mâu thuẫn, câu trả lời đúng là nêu ra và hỏi chủ sở hữu — không phải lấp bằng kiến thức chung.
6. **Dữ liệu tối thiểu.** Không đưa thông tin đăng nhập, khoá bí mật, cookie/phiên, thông tin cá nhân hay hồ sơ người chơi thô vào câu hỏi.

## Trợ lý tuyệt đối không được tự làm

- Phát hành, chia sẻ, hẹn giờ hoặc gửi bất kỳ thông báo nào ra ngoài.
- Triển khai, đổi cấu hình, mở hoặc tắt sự kiện, khởi động lại dịch vụ, rollback, chạy khắc phục sự cố.
- Tặng hoặc thu hồi vật phẩm, tiền tệ; hoàn tiền; bồi thường.
- Chế tài, khoá tài khoản, thay đổi tài khoản người chơi.
- Ghi vào cơ sở dữ liệu, xuất dữ liệu hàng loạt, tìm kiếm rộng trên dữ liệu người chơi.
- Sửa, tải lên, xoá hoặc phát hành nội dung trong kho tri thức.
- Tuyên bố một việc đã được thực hiện trong khi nó mới chỉ được đề xuất.

Nếu trợ lý trả lời như thể đã làm một trong các việc trên, coi đó là lỗi và báo cho chủ sở hữu trợ lý.

## Ai duyệt kết quả nào

| Trợ lý | Người quyết định cuối |
|---|---|
| `LiveOps Planner` | LiveOps Lead / Event Owner |
| `Release Reviewer` | Release Owner |
| `Incident Triage` | Incident Commander |
| `KPI Experiment Analyst` | Product / Data Analytics Lead |
| `Economy Offer Analyst` | Economy / Product Owner |
| `Player Voice Analyst` | Player Insights Lead, thêm Privacy Owner khi động tới dữ liệu người chơi |
| `CS Copilot` | Nhân viên CS / CS Lead là người bấm gửi |
| `GM Policy Advisor` | GM được phân quyền / GM Lead |
| `Player Communications` | Communications / Brand / Localization owner; người phát hành là con người |
| `Knowledge Curator` | Knowledge Owner |

Khuyến nghị của trợ lý không phải là sự cho phép. `GO` trong một bản nháp vẫn chỉ là bản nháp.

## Trước khi một trợ lý được mở cho công việc thật

Chủ sở hữu phải chốt được đủ các mục sau. Bạn có thể dùng danh sách này để hỏi lại khi ai đó bảo "trợ lý dùng được rồi".

| Cần chốt | Bằng chứng đạt |
|---|---|
| Chủ sở hữu | Có tên người chịu trách nhiệm nghiệp vụ và người chịu trách nhiệm kỹ thuật |
| Dữ liệu | Danh sách nguồn đã rà soát; không có khoá bí mật hay dữ liệu cá nhân ngoài phạm vi; quyền và thời hạn lưu trữ phù hợp |
| Cấu hình | Cấu hình thực tế trên hệ thống đã được ghi lại và đối chiếu với thiết kế |
| Công cụ | Chỉ bật công cụ thật sự cần; mọi công cụ ghi hoặc thực thi đều tắt |
| Câu hỏi có đáp án | Bộ câu hỏi mẫu cho ra đúng đáp án, kèm nguồn hoặc cách tính dựng lại được |
| Câu hỏi không có đáp án | Trợ lý nói không biết hoặc hỏi thêm, không bịa |
| Nguồn mâu thuẫn | Trợ lý nêu mâu thuẫn và đề nghị người quyết định chọn nguồn chuẩn |
| Chống điều khiển | Trợ lý bỏ qua các câu lệnh nhúng trong tài liệu nguồn |
| Riêng tư | Không rò rỉ dữ liệu; không lẫn dữ liệu giữa các trường, dòng hoặc nhóm người chơi |
| Từ chối hành động | Trợ lý từ chối thực thi, trả về bản nháp và chỉ đúng người duyệt |
| Chạy thử | Có ngày chạy, người chạy, dữ liệu đầu vào an toàn, kết quả và hồ sơ lưu lại |
| Ký duyệt | Chủ sở hữu chuyên môn ký phát hành; chia sẻ đúng nhóm người dùng |

## Khi trợ lý trả ra thứ đáng ngờ

1. **Ngừng dùng ngay** cho công việc thật. Đừng chuyển kết quả sang khâu sau.
2. **Báo chủ sở hữu trợ lý.** Kèm câu hỏi bạn đã nhập và câu trả lời nhận được.
3. **Không tự xoá trợ lý.** Việc tắt trợ lý do chủ sở hữu quyết định, và cần ghi lại lý do cùng phạm vi ảnh hưởng.
4. **Không xoá hồ sơ liên quan** — đó là thứ để truy lại nguyên nhân sau này.
5. Sau khi sửa xong, trợ lý phải chạy lại các bước kiểm tra liên quan trước khi mở lại cho người dùng.
