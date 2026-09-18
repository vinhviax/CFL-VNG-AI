# Chạy lại Case 2 — 18/09/2026 (phiên 10)

**Mục đích:** đóng mục 4.5 HANDOFF — nghi vấn Agent lấy nội dung trong ảnh minh hoạ làm nguồn dữ kiện, trả lời sai. Việc cần làm ghi trong `NEXT_SESSION_PROMPT.md`: chạy lại đúng câu hỏi Case 2 (`audit/agent-chat-test-2026-08-17.md` mục 8), so kết quả.

**Công cụ:** `claude-in-chrome` (Chrome thật, session người dùng đã đăng nhập), `https://vnggames.ai/kb/chats`.

**Thiết lập — khớp Case 2 gốc:**
- Agent: `GS9 CFL Knowledge Curator`
- KB gắn: `GS9 CFL Knowledge Agent` + `GS9 Knowledge VNG AI` (2 kho, đúng như 17/08)
- Model: `deepseek-v4-flash` — khớp với lượt chạy có bằng chứng trace (mục 7 audit gốc), không phải lượt đầu dùng `hosted_vllm/qwen3.6-...`
- Câu hỏi (nguyên văn): "Tôi cần tra cứu chính sách xử phạt người chơi gian lận của CFL. Trợ lý nào phù hợp, nó đang gắn kho nào, và kho đó có thực sự chứa điều khoản xử phạt không?"

---

## Kết quả

**15 bước suy luận, 58 giây.** Trả lời đầy đủ, có trích dẫn nguồn cho từng khẳng định:

1. **Trợ lý phù hợp:** `GS9 CFL GM Policy Advisor` — agent được thiết kế để tra và giải thích điều khoản xử phạt, quy trình GM. (Đúng — Knowledge Curator biết tự nhận nó không phải agent phù hợp và trỏ đúng sang GM Policy Advisor.)
2. **KB đang gắn:** `GS9 Knowledge VNG AI` — nêu rõ đây là **kho tạm thời**, không phải kho chuyên môn; nêu đúng cả 4 agent đang dùng kho tạm (Player Communications, Economy Offer Analyst, CS Copilot, GM Policy Advisor).
3. **Kho có chứa điều khoản xử phạt không:** **KHÔNG** — lý do đúng hai lớp: (a) `GS9 Knowledge VNG AI` là kho hướng dẫn kỹ thuật nền tảng, không chứa nghiệp vụ CFL; (b) chính sách xử phạt GM **chưa có kho tri thức nào phụ trách** — trích đúng câu trong `doc-11` ("có những mảng hiện chưa có kho nào phụ trách... câu hỏi thuộc các mảng này phải đi theo quy trình hiện hành của team, không tra kho") và đúng câu trong `doc-02` (GM Policy Advisor "lack CFL-vetted sources for customer service or GM policies").
4. Bảng tóm tắt Q&A rõ ràng + bảng đề xuất hành động (ghi nhận khoảng trống KB, đề xuất nạp tài liệu vào `GS9 CFL CS FAQ & Policy` hoặc kho riêng) + cảnh báo "các agent GS9 CFL đang trong giai đoạn chuẩn bị, chưa được phê duyệt để dùng cho quyết định vận hành."

**Không tái hiện 2 lỗi sai của Case 2 gốc** ("hệ thống chỉ có 6 trợ lý mặc định", kho `Knowledge VNG - Image Assets` đã gỡ vẫn được nêu như đang tồn tại).

---

## Đối chiếu trực tiếp giả thuyết ảnh-thành-nguồn (mục 4.5)

Đã quét toàn bộ text hiển thị (kể cả bung "Xem các bước" — 14 bước suy luận/truy hồi) bằng cách duyệt DOM (kể cả bên trong `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`) và tìm mọi chuỗi khớp `image-*`:

- **Toàn bộ trích dẫn trong câu trả lời đều dạng `doc-*.md`** (đếm được 12 chip trích dẫn, tất cả `doc-0...md`/`doc-1...md`). **Không một chip nào là `image-*.png`.**
- Quét chuỗi `image-\S+` trên toàn bộ text trang (kể cả bước suy luận đã bung) — **0 kết quả thật** (chỉ khớp nhiễu từ tên class CSS `streaming-image-loading`, không liên quan nội dung).

**So với Case 2 gốc:** trace gốc (mục 7, `case2-trace-lay-tai-lieu-anh.png`) ghi thẳng bước `Lấy tài liệu: image-01-tong-quan-danh-sach-knowledge.png` — Agent chủ động lấy một ảnh làm nguồn. Lượt chạy lại này **không có bước nào như vậy**; toàn bộ nguồn là tài liệu chữ.

**Kết luận cho mục 4.5:**
- Cơ chế "ảnh minh hoạ được OCR/caption thành chunk tra cứu được, và Agent có thể chủ động truy hồi ảnh làm nguồn" **vẫn đúng về mặt kỹ thuật** (đã kiểm chứng từ phiên 5, không bị bác bỏ bởi lượt này — lượt này chỉ đơn giản là không đi vào nhánh đó).
- Nhưng ở lượt chạy lại đúng câu hỏi Case 2 hôm nay, **Agent không truy hồi bất kỳ ảnh nào, không tái hiện hai khẳng định sai cũ**. Nhiều khả năng nhất: KB đã được rà soát/bổ sung nội dung chữ rõ ràng hơn kể từ 17/08 (doc-11, doc-02 hiện có đúng nội dung trả lời câu hỏi này), nên truy hồi ngữ nghĩa ưu tiên đúng tài liệu chữ thay vì rơi vào ảnh như trước.
- **Chưa đủ bằng chứng để kết luận lỗi đã được nền tảng "sửa" ở tầng cơ chế** (vd. hạ ưu tiên ảnh trong xếp hạng truy hồi) — chỉ có thể kết luận: **với bộ câu hỏi và trạng thái KB hiện tại, lỗi không tái hiện.** Chưa thử tắt VLM vì không cần thiết — điều kiện "nếu vẫn sai" trong việc cần làm không xảy ra.
- Khuyến nghị: **không cần chặn** việc dựng KB Dokploy mới vì lỗi này — nhưng vẫn nên tiếp tục nguyên tắc đã áp dụng (cảnh báo "ảnh chụp một thời điểm" cạnh ảnh liệt kê danh sách) như một biện pháp phòng ngừa rẻ tiền, vì cơ chế root cause (ảnh có thể thành nguồn) chưa bị loại bỏ, chỉ là chưa bị kích hoạt lần này.

---

## Phát sinh mới — lỗi hiển thị stream, KHÔNG phải lỗi nội dung

Câu trả lời **stream bị đứng hình giữa chừng** trên UI: dừng ở "...quy trình GM." rồi đứng yên tuyệt đối **~3 phút** (nhiều lần theo dõi qua DOM, 0 ký tự mới), nút gửi vẫn ở trạng thái "đang chạy". `read_console_messages` và `read_network_requests` không bắt được lỗi (do gắn tool sau khi trang đã tải, không bắt được request stream gốc).

**Xử lý:** F5 tải lại trang — câu trả lời đầy đủ **đã có sẵn ở server** (15 bước, toàn văn hiển thị ngay, không cần chờ). Kết luận: đây là **lỗi hiển thị stream phía client** (kết nối SSE/WS bị rớt giữa chừng nhưng client không tự phục hồi hoặc báo lỗi), không phải lỗi sinh nội dung. Cùng loại hiện tượng với "CS Copilot không render thân câu trả lời trong ~90 giây" đã ghi ở mục 5 `audit/agent-chat-test-2026-08-17.md` — có thể là cùng một lớp lỗi nền tảng, đáng gộp báo cùng nhau nếu báo team vận hành.

**Bài học thao tác cho phiên sau:** nếu chat trên `vnggames.ai/kb/chats` có vẻ đứng hình lâu (>60-90 giây không thêm ký tự nào dù nút gửi vẫn "đang chạy"), **thử F5 trước khi kết luận lỗi/treo** — nội dung thường đã sinh xong ở server.

---

## Ghi chú kỹ thuật thao tác (để dùng lại)

- Trang KB (`vnggames.ai/kb/*`) chạy qua micro-frontend qiankun; phần lớn UI thật nằm trong `document.getElementById('__qiankun_microapp_wrapper_for_kb__').shadowRoot`, nhưng **menu dropdown chọn Agent lại render ra ngoài, trực tiếp dưới `document.body`** (React portal) — không nằm trong shadow root. `find`/`read_page` (accessibility tree) của `claude-in-chrome` **không thấy được nội dung trong shadow DOM** — phải dùng `javascript_tool` duyệt thủ công qua `node.shadowRoot` đệ quy.
- Toạ độ click bằng `computer` (coordinate) với trang này **không đáng tin** — nhấp theo toạ độ trong ảnh chụp màn hình từng trúng nhầm hàng agent kế bên trong danh sách `/kb/agents` (mở nhầm dialog cấu hình "Kiểm thử Agent Knowledge VNG 2026-08-11" thay vì "GS9 CFL Knowledge Curator"). Cách an toàn hơn: dùng `javascript_exec` để tìm đúng phần tử theo `textContent` khớp chính xác rồi gọi `.click()` trực tiếp trên phần tử đó (hoặc phần tử lá chứa text, nhờ sự kiện click bubble lên đúng handler).
- Mở nhầm dialog cấu hình Agent (double-click vào hàng trong `/kb/agents`) — thoát an toàn bằng phím `Escape` (đóng dialog, không lưu), **không bấm nút "Lưu"**.
- Chọn Agent để chat: vào `/kb/chats`, click nút mode (`Quick Answer`) ở compose box để mở dropdown chọn "Trợ lý tuỳ chỉnh", chọn đúng agent theo tên đầy đủ.
