<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3.md -->

# 19 - Agent: vòng đời, phân quyền, quan sát và bảo trì {#19-vong-doi-phan-quyen-quan-sat-va-bao-tri}

## Khái niệm

Vòng đời Agent gồm tạo, cấu hình, test, phát hành, sửa, nhân bản, tắt/bật, chia sẻ và xóa. Nội dung KB có vòng đời riêng: Agent có thể tiếp tục tồn tại khi Markdown bị thay; vì thế rollback Agent không thay thế rollback KB. Thao tác destructive hoặc quyền phải được kiểm soát theo owner và bằng chứng trước/sau.

<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/49-agent-chia-se-va-vong-doi.png -->
![Menu vòng đời và UI chia sẻ](minio://knowledge-base-prd/10012/exports/0874930a-485f-4b72-ad9b-cff1ec240324.png)

*Ảnh 19.1 – Menu Agent user-owned có Chat, Edit, Clone, Disable/Enable và Delete; UI chia sẻ chỉ được quan sát, không gửi lời mời trong audit.*

## Bảng control

| Thao tác | Đã thực hiện live | Điều kiện/guardrail |
|---|---|---|
| Tạo Agent disposable | Có | Đặt tên `TEST -`, mô tả rõ xóa sau audit |
| Clone | Có | Kiểm tra bản sao có cấu hình dự kiến trước khi dùng |
| Disable → Enable | Có | Toast xác nhận; kiểm tra trạng thái cuối là enabled |
| Edit | Có ở phạm vi config test | Lưu baseline, A/B một biến, restore |
| Delete Agent test | Được phép sau audit | Xác nhận đúng tên, owner và không phải default/production |
| Chia sẻ Space/role | Chỉ xem UI | Không gửi invitation hoặc add vào Space khi chưa có uỷ quyền |
| Delete Agent production | Không test | Export/backup config, kiểm tra sharing và rollback trước |

| Role trong UI chia sẻ | Ý nghĩa đã quan sát | Trạng thái |
|---|---|---|
| Chỉ xem | Role có thể chọn khi chia sẻ Space | **Có điều kiện:** không test quyền end-to-end |
| Được chỉnh sửa | Role có thể chọn khi chia sẻ Space | **Có điều kiện:** không test quyền end-to-end |

## SOP

1. Tạo Agent `TEST - <mục đích> - <ngày>`; tuyệt đối không đổi sáu Agent mặc định để thử UI.
2. Lưu ảnh/cấu hình baseline trước clone hoặc A/B; ghi model, KB, tool, threshold, version KB.
3. Test functional rồi clone disposable; test disable/enable trên clone để không phá session baseline.
4. Chỉ mở tab Chia sẻ và đọc role/Space nếu chưa được cấp quyền gửi chia sẻ.
5. Khi release, phân công owner, bộ regression, cadence review và kênh tiếp nhận feedback.
6. Khi retire test resource, lưu audit trước; xóa đúng resource `TEST` theo tên/ID, xác minh không đụng default/existing test.
7. Sau bất kỳ xóa/thay thế nào, đối chiếu inventory, source drawer và ảnh MinIO; nếu fail, rollback theo backup đã lưu.

## Data flow

```text
draft config → test Agent → evidence/audit → publish/share (nếu được phê duyệt)
      ↘ clone disposable → disable/enable → audit → delete exact TEST resource

KB master → strict build → consumer Markdown → Agent retrieval
                 ↑ rollback source/MD khác với rollback Agent config
```

## Ma trận kiểm thử

| Nhóm | Test | Pass | Không được làm |
|---|---|---|---|
| Create | Agent TEST có KB/tool hợp lệ | Tạo thành công, có chat | Không dùng Agent default |
| Clone | Clone Agent TEST | Bản sao xuất hiện, cấu hình cần thiết có mặt | Không clone production để thử |
| Toggle | Disable rồi Enable clone | Có hai toast, trạng thái cuối Enabled | Không toggle Agent đang phục vụ Human |
| Share | Mở UI role | Thấy Space/Chỉ xem/Được chỉnh sửa | Không gửi share/invite |
| Delete | Xóa exact TEST sau audit | Resource biến mất, audit còn | Không xóa khi tên/owner mơ hồ |
| Maintenance | Re-run regression sau KB rollout | Mỗi module mới có source/ảnh | Không gộp content change với nhiều config change |

## Bằng chứng

- **Đã kiểm chứng:** Agent `TEST - Agent Lifecycle Deep Audit 2026-08-11` được tạo với 2 KB và tool set; clone được tạo.
- **Đã kiểm chứng:** clone đã Disable (toast “Đã tắt trợ lý”) rồi Enable (toast “Đã bật trợ lý”); trạng thái cuối là bật trước cleanup.
- **Đã kiểm chứng:** menu user-owned hiển thị Chat, Edit, Clone, Disable/Enable, Delete.
- **Có điều kiện:** tab Chia sẻ hiển thị Space/roles nhưng audit không gửi chia sẻ, nên không tuyên bố role end-to-end.
- **Chưa xác định:** khôi phục sau Delete Agent không được suy luận nếu UI không hứa hẹn và chưa test.

## Lịch bảo trì khuyến nghị

| Chu kỳ | Việc làm | Output tối thiểu |
|---|---|---|
| Sau thay KB/Markdown | Chạy canonical, conflict, no-hit; mở source/ảnh | Audit ngày, source pass/fail |
| Sau đổi model/prompt/tool | A/B một biến; restore nếu không đạt | Config diff và kết quả hồi quy |
| Hàng tuần | Xem feedback chưa xử lý, quota/error trend | Owner và trạng thái Hộp xử lý |
| Hàng tháng | Rà soát quyền Space, Agent tắt, Agent TEST cũ | Danh sách giữ/xóa có phê duyệt |
| Trước xóa/retire | Backup config/evidence, xác nhận exact target | Rollback plan và người duyệt |

Agent không có “phát hành tự động an toàn” chỉ vì nút lưu thành công. Mỗi lần thay đổi quan trọng phải có một định danh version/audit, một bộ regression và một owner chịu trách nhiệm quay lại baseline khi source/answer regress.

## Phân vai vận hành

| Vai trò | Quyết định | Không được tự ý làm |
|---|---|---|
| Owner nội dung | Canonical source, phiên bản, mâu thuẫn nghiệp vụ | Đổi model/quyền để che lỗi nguồn |
| Owner Agent | Prompt, KB scope, tool, regression | Sửa master KB trực tiếp trong generated module |
| Space/admin | Quyền truy cập, model/ASR provisioning | Cấp rộng quyền chỉ để test một lỗi |
| Reviewer | Xem evidence, source, rollback | Phê duyệt chỉ dựa trên screenshot câu trả lời |
| Human dùng Agent | Feedback/clarification | Được xem là owner của dữ liệu KB tự động |

Trước delete, dùng “bốn xác nhận”: đúng tên hiển thị; đúng owner; đúng mục đích `TEST`; và audit/backup đã tồn tại. Nếu một xác nhận thiếu, không bấm Delete. Delete là thao tác cuối lifecycle, không phải biện pháp làm mới nội dung; nội dung cần đổi đi theo master → build → consumer → chat test.

Sau cleanup, reload danh sách và đối chiếu count/đúng tên để đảm bảo không còn resource TEST ngoài ý muốn và không ảnh hưởng Agent đang tồn tại.
Nếu lịch sử chat test cần giữ làm audit, lưu bằng chứng đã che trước cleanup thay vì giữ Agent TEST vô thời hạn.

## Lỗi và giới hạn

| Rủi ro | Kiểm soát |
|---|---|
| Xóa nhầm Agent | Tên TEST độc nhất, owner, ID, ảnh/audit trước delete; dừng nếu mơ hồ |
| Drift cấu hình | Baseline/export mô tả + test matrix + A/B một biến |
| KB update làm Agent regress | Publish Markdown theo thứ tự asset → map → strict build → consumer → chat source test |
| Chia sẻ sai phạm vi | Xem UI trước; chỉ gửi khi có quyền/đích/rõ role |
| Quan sát thiếu context | Lưu source, model, KB chips và Request Information đã che |

## Checklist

- [ ] Agent production/default không bị dùng làm đối tượng test phá huỷ.
- [ ] Clone/toggle/delete chỉ trên resource `TEST` được định danh chính xác.
- [ ] Chia sẻ chỉ quan sát cho đến khi có phê duyệt gửi thật.
- [ ] Có owner, regression set, lịch review và đường rollback.
- [ ] Audit được cập nhật trước STATUS/HANDOFF và trước cleanup TEST.
