# KB — Phương pháp kiểm chứng và phân loại độ tin cậy bằng chứng

**Đối tượng:** Dev và người viết tài liệu/audit cho project. Người cần biết *tôi được phép khẳng định điều này ở mức nào, và phải kèm gì*.
**Ngày viết:** 16/08/2026.
**Cách kiểm chứng:** đọc `DECISIONS.md` (DEC-007, 008, 010, 017, 022, 027), `AGENTS.md`, và đối chiếu cách 19 file trong `audit/` áp dụng phân loại trên thực tế.

**Chồng lấn:** đây là tài liệu **phương pháp**, không phải tài liệu nội dung. Kết quả áp dụng phương pháp này nằm rải trong các file `KB-*` và `Agent-*` khác — mỗi file đều có mục "Chưa kiểm chứng" ở cuối chính là sản phẩm của luật ở đây.

---

## 1. Vì sao project này cần một thang đo riêng

Toàn bộ tri thức trong project đến từ **quan sát một nền tảng do bên khác vận hành**. Không có mã nguồn VNG AI, không có log hệ thống, không có tài liệu API chính thức. Thứ duy nhất có là: màn hình UI, phản hồi MCP, kết quả chat, và file trên đĩa.

Ba đặc tính của loại tri thức đó:

- **Hết hạn được.** Nền tảng đổi mà không báo. Một khẳng định đúng hôm nay sai tuần sau.
- **Nhìn thấy ≠ chạy đúng.** Đọc được một thiết lập trên màn hình không có nghĩa là đã biết nó hoạt động ra sao.
- **Không đầy đủ.** Rất nhiều câu hỏi không trả lời được bằng UI, và im lặng dễ bị đọc nhầm thành "không có vấn đề".

Nếu viết tài liệu theo lối khẳng định phẳng, cả ba đặc tính trên biến mất khỏi trang giấy và người đọc sau sẽ hành động như thể mọi dòng đều chắc chắn như nhau. **DEC-007 (06/08/2026)** sinh ra để chặn đúng chuyện đó.

---

## 2. Ba mức phân loại (DEC-007)

DEC-007 nguyên văn: *"Phân biệt Đã kiểm chứng, Có điều kiện và Bị chặn/Chưa xác định. Trạng thái live luôn có ngày và liên kết bằng chứng; không suy diễn thành hướng dẫn chắc chắn."*

| Mức | Nghĩa | Điều kiện để dùng | Phải kèm gì |
|---|---|---|---|
| **Đã kiểm chứng** | Có bằng chứng trực tiếp, quan sát được | Đã tự tay thấy/chạy/đọc kết quả | **Ngày** + cách quan sát + đường dẫn bằng chứng |
| **Có điều kiện** | Đúng trong phạm vi hẹp đã thử, không suy rộng được | Đã thử nhưng mẫu nhỏ, môi trường đặc thù, hoặc chỉ đúng khi có tiền đề | Ngày + **phạm vi đã thử** + tiền đề chưa kiểm |
| **Bị chặn — Chưa xác định** | Chưa ai thử, hoặc thử mà không tiếp cận được | Không có bằng chứng | Ngày + **lý do chặn** + việc cần làm để gỡ |

Ba mức này **không phải thang tự tin chủ quan**. Chúng phân theo *loại bằng chứng đang có*, không theo *cảm giác chắc chắn*. Một khẳng định có thể rất hợp lý nhưng vẫn là "Chưa xác định" nếu chưa ai thử.

### 2.1 Đọc thang đo theo chiều ngược lại

Cách dùng hữu ích nhất khi đọc tài liệu cũ:

- Gặp **Đã kiểm chứng** → tin, nhưng kiểm ngày. Cũ quá thì chạy lại.
- Gặp **Có điều kiện** → đọc kỹ phạm vi. Việc bạn định làm có nằm trong phạm vi đó không?
- Gặp **Bị chặn — Chưa xác định** → **đây là chỗ nguy hiểm nhất**, không phải chỗ ít quan trọng nhất. Nó nghĩa là chưa ai biết, nên đừng giả định là an toàn.

---

## 3. Bốn luật bổ trợ

### 3.1 Cấu hình UI không bằng hành vi runtime (DEC-022, 11/08/2026)

Luật quan trọng nhất khi làm việc với Agent. Nguyên văn: *"Với Agent, cấu hình Intent/prompt/model/switch trong UI và hành vi runtime là hai lớp bằng chứng riêng."*

| Đọc được từ UI | Chỉ chat-test mới chứng minh |
|---|---|
| Model nào được chọn | Model đó có thực sự được gọi không |
| Tool nào bật | Tool đó có được dùng khi trả lời không |
| KB nào bind | Retrieval có lấy đúng chunk không |
| Reranker/VLM bật | Chất lượng xếp hạng, ảnh có đọc được không |

Hệ quả bắt buộc: *"Chỉ kết luận Intent, retrieval, VLM hoặc ASR hoạt động khi chat test chứng minh; lỗi quota, attachment, raw chunk hoặc thiếu model phải ghi là Có điều kiện/Bị chặn, không suy rộng thành mặc định."*

Ví dụ sống — **DEC-049 (15/08/2026)**: người dùng bật `bge-reranker-v2-m3` và VLM `qwen3.6-plus` cho cả 10 Agent, Agent đã xác minh read-only trên UI. Kết luận được ghi là: identity/config **Đã kiểm chứng**, nhưng *"reranker và VLM đều chưa được chat-test nên chất lượng vẫn là Bị chặn–Chưa xác định"*. Hai lớp, hai mức, cùng một sự việc.

### 3.2 Ghi nhận trạng thái thật, không tự sửa

**DEC-050 (15/08/2026)** là ví dụ mẫu mực. Khi xác minh cấu hình, phát hiện `Chế độ suy nghĩ` đang **BẬT** trên 2 Agent — trái với baseline "Thinking Off" ghi từ 14/08. Cách xử lý:

1. **Ghi nhận trạng thái thật**, không tự tắt.
2. Ghi rõ mới kiểm **2/10 Agent**; phần còn lại *"suy ra theo mẫu và phải ghi rõ là suy ra cho tới khi kiểm đủ"*.
3. Không đảo trạng thái khi chưa có chỉ định người dùng.

Ba việc này tương ứng ba luật: không mutation ngoài phạm vi, không suy rộng mẫu nhỏ, và tách rõ *quan sát* khỏi *suy luận*.

### 3.3 Bằng chứng lịch sử không cấp quyền hiện tại

**DEC-017 (07/08/2026):** `Test Doc RAG+Wiki` đã bị người dùng xoá, *"chỉ còn là bằng chứng lịch sử trong audit 06/08/2026"*. Hệ quả: *"Không dùng KB/ID đó như dependency hay đích mutation."*

Nguyên tắc rút ra: một audit cũ chứng minh **điều gì đã đúng vào ngày đó**, không chứng minh **điều gì được phép làm hôm nay**. Cùng tinh thần ở **DEC-006** — KB trong audit cũ *"không tự động cấp quyền mutation"*.

Khi đọc audit cũ, tách hai câu hỏi: *"lúc đó thế nào?"* (audit trả lời được) và *"giờ tôi làm được gì?"* (audit không trả lời).

### 3.4 Artifact thử nghiệm phải audit trước khi dọn

**DEC-027 (12/08/2026):** KB/Agent disposable dùng để kiểm thử *"chỉ tồn tại để kiểm thử và phải được audit trước cleanup"* — chỉ xoá sau khi rollout đã chứng minh, và giữ backup legacy.

Lý do: nếu xoá đồ thử nghiệm trước khi ghi lại kết quả, bằng chứng biến mất cùng với nó và kết luận trở thành lời kể không kiểm chứng được.

---

## 4. Quy trình đóng một khẳng định

### 4.1 Bốn bước

```text
1. QUAN SÁT   thấy gì, bằng cách nào (UI / MCP / chạy lệnh / đọc file)
       │
2. GHI        chép nguyên trạng vào audit/ — kể cả thứ trái kỳ vọng
       │
3. PHÂN LOẠI  gán một trong ba mức + ngày + phạm vi
       │
4. LAN TOẢ    cập nhật STATUS.md và HANDOFF.md (DEC-008)
```

**DEC-008 (06/08/2026)** khoá thứ tự bước 2→4: *"Cập nhật audit trước, rồi `STATUS.md` và `HANDOFF.md` với việc đã làm, tồn đọng, bằng chứng và bước tiếp theo."* `AGENTS.md` nhắc lại ở mục "Kết thúc phiên".

Audit trước, tài liệu sống sau. Ngược lại thì tài liệu sống thành khẳng định không có gốc.

### 4.2 Gate là dạng đặc biệt của "Đã kiểm chứng"

Với thứ đo được bằng lệnh, project không dùng lời văn mà dùng **gate**: một điều kiện nhị phân chạy được, có kết quả in ra.

**DEC-010 (07/08/2026)** là ví dụ: giai đoạn bổ sung 11 ảnh Google Drive *"chỉ được công nhận chat-ready khi đủ mapping và strict build đạt"*. Không phải "trông có vẻ ổn" mà là "strict build không ném lỗi".

Cùng tinh thần, gate bàn giao hiện hành (`AGENTS.md`, 15/08/2026) là một chuỗi số đếm được: 20 module, 49 PNG/URI, 60 MinIO + 60 `LOCAL_ASSET`, `Ran 29 tests`/`OK`. Chi tiết ở `KB-pipeline-build-va-kiem-thu.md` mục 7.3.

**Ưu điểm của gate:** không cãi được, và người sau chạy lại được.
**Giới hạn của gate:** chỉ phủ được thứ đo bằng máy. Chất lượng câu trả lời của Agent không có gate.

---

## 5. Phân loại này trông thế nào trong `audit/`

19 file `.md` trong `audit/` là nơi phương pháp được áp dụng thật. Ba khuôn mẫu lặp lại:

### 5.1 Khuôn "bảng ba cột" — cho danh mục hạng mục

`audit/audit-google-drive-connector-2026-08-07.md` mục 6 chia rành mạch cái đã thử và cái chưa:

| Hạng mục | Trạng thái |
|---|---|
| Xác thực service account và My Drive | Đã kiểm chứng |
| Bước 3 – chọn tài nguyên | Đã kiểm chứng |
| Tạo nguồn và lượt đồng bộ đầu tiên | Đã kiểm chứng, kết quả Thành công |
| Incremental/full qua nhiều chu kỳ | Chưa xác định |
| Regex, tag, parser tùy chỉnh trên dữ liệu đối chứng | Chưa xác định |
| Sửa, đổi tên, di chuyển, xóa, thu hồi quyền | Chưa xác định |

Giá trị của bảng này lộ ra 8 ngày sau: kế hoạch 15/08 định đổi tên 135 file rồi sync — **đúng dòng "Chưa xác định"**. Nhờ có bảng, rủi ro được nhận diện trước khi làm, và kế hoạch chèn bước "thử 2–3 file trước". Một ô "Chưa xác định" ghi đúng chỗ đã chặn được một sự cố diện rộng.

### 5.2 Khuôn "ba đoạn tổng kết" — cho audit tổng hợp

`audit/business-kb-readonly-audit-2026-08-14.md` kết bằng ba đoạn, mỗi đoạn một mức:

- **Đã kiểm chứng:** danh mục 9 KB và ID, count tài liệu, owner, quyền share, số thành viên space, schema cột, số dòng, `parse_status`, `channel`, embedding model, tag, việc thiếu control retention.
- **Có điều kiện:** độ đầy đủ chunk của hai tài liệu từng lỗi pipeline; chất lượng retrieval từng KB; mức độ PII thực tế trong free-text (chưa quét toàn bộ 85.365 dòng).
- **Bị chặn–Chưa xác định:** ID KB Sentiment; danh tính 6 thành viên space; owner thực của `GS9 test knowledge base`; policy retention cấp tenant; liệu 20 module trên Web còn khớp master hay đã bị sửa.

Đây là khuôn nên chép lại cho mọi audit mới. Nó buộc người viết phải quyết định từng hạng mục thuộc mức nào, thay vì để lẫn lộn trong văn xuôi.

### 5.3 Khuôn "caveat kép" — khi một sự việc có hai lớp bằng chứng

`audit/default-agent-readonly-audit-2026-08-14.md` dùng cách viết tinh nhất, đúng theo DEC-022:

> **Đã kiểm chứng (static conflict)** — system prompt nói không dùng prior knowledge, nhưng fallback prompt cho phép general knowledge khi không có document listing. **Có điều kiện** — hành vi thực tế chưa chat-test.

Một câu, hai mức. Phần *đọc được từ cấu hình* là Đã kiểm chứng; phần *nó chạy ra sao* là Có điều kiện. Cùng file còn có mẫu phân biệt **Đã kiểm chứng (static mismatch)** — prompt nhắc một tool không có trong danh sách hiệu lực.

File này cũng mở đầu bằng một câu khai báo mặc định rất đáng chép:

> Mọi mục trong phần này là **Đã kiểm chứng** từ UI cấu hình ngày 14/08/2026, trừ khi được gắn rõ **Có điều kiện** hoặc **Bị chặn–Chưa xác định**.

Khai báo mặc định một lần ở đầu, rồi chỉ đánh dấu ngoại lệ — gọn hơn gắn nhãn từng dòng.

### 5.4 Khuôn "kết luận kèm giới hạn xác minh"

**DEC-051 (16/08/2026)** cho thấy cách viết một kết luận **tích cực** mà vẫn trung thực. Kết luận: gộp ảnh + tài liệu chung một KB là **an toàn** qua 3 vòng sync. Nhưng ngay sau đó:

- **Lý do kỹ thuật là suy ra**, không xác minh bằng log connector.
- **Giới hạn xác minh:** không so sánh được `knowledge_id` qua MCP; *"kết luận dựa trên quan sát UI … không phải log hệ thống"*.
- **Chưa test** case sửa trực tiếp nội dung/caption của chính file ảnh.

Ba dòng đó biến một khẳng định "an toàn" thành một khẳng định **dùng được**: người sau biết chính xác nó phủ tới đâu.

---

## 6. Những lỗi phân loại đã gặp thật

### 6.1 Suy diễn quá tay rồi phải rút

Bản đầu của bản đồ kiến trúc đề xuất hạ `GS9 CFL Data Daily` xuống staging vì nghi trùng nội dung với `Kho Dữ Liệu Tổng Hợp`. Spec 15/08 tự đính chính: *"Không có bằng chứng nào cho thấy nó trùng nội dung … Đề xuất 'hạ xuống staging' ở bản đầu là suy diễn quá tay, đã rút."*

Trùng lặp **đã kiểm chứng** duy nhất là `CFL ItemID.xlsx` giữa `Item Profile` và `Kho Dữ Liệu Tổng Hợp`. Từ một trùng lặp có bằng chứng, bản đầu suy ra một trùng lặp không có bằng chứng.

**Dấu hiệu nhận biết:** khi một khuyến nghị hành động (hạ cấp, xoá, gỡ bind) dựa trên chữ "có vẻ" hoặc "chắc là", đó là suy diễn chứ không phải kết luận.

### 6.2 Đọc im lặng thành phủ định

`audit/default-agent-readonly-audit-2026-08-14.md` xử lý đúng: *"Không có tab/panel/menu Share xuất hiện trong phạm vi UI hiện xem. Vì vậy **không kết luận được** Agent đang public/private."*

Không thấy nút Share **không** nghĩa là không có chia sẻ. Nó nghĩa là không nhìn thấy. Ghi thành "Bị chặn–Chưa xác định", không ghi thành "không được chia sẻ".

### 6.3 Suy rộng từ mẫu nhỏ

DEC-050: kiểm 2/10 Agent rồi *"phần còn lại suy ra theo mẫu"*. Cách xử lý đúng là **gắn nhãn "suy ra"** ngay tại chỗ, không để nó trôi thành sự thật ở tài liệu kế tiếp.

Tương tự, khi thấy `Image attachment` bị chặn trên một Agent (`audit/agent-deep-test-2026-08-11.md`), kết luận được ghi là *"Bị chặn/có điều kiện; không kết luận VLM hỏng"* — một lần thất bại trên một đường không đủ để kết luận cả tính năng.

### 6.4 Khẳng định hết hạn sau sáu phút — ca gặp trực tiếp

Trong lúc viết chính bộ tài liệu này, ngày 16/08/2026:

- **17:34** — đo hợp đồng artifact: 60 link MinIO / 60 `LOCAL_ASSET`. Bộ test `Ran 29 tests … OK (skipped=6)`. Ghi vào tài liệu là **Đã kiểm chứng**.
- **17:37** — một tác nhân ngoài phiên sửa tay `doc-02-tao-kb-nhanh-va-nang-cao.md`, đổi URI ảnh sang dạng `<doc_id>/<uuid>` không khớp `image-map.json`.
- **17:40** — chạy lại: `AssertionError: 59 != 60`. Hợp đồng vỡ.

Khẳng định "Đã kiểm chứng" lúc 17:34 **không sai** — nó đúng vào thời điểm đó, và có ngày giờ nên truy được. Đó chính là lý do luật bắt ghi ngày: một khẳng định có mốc thời gian thì khi hết hạn nó **tự tố cáo mình**, còn một khẳng định không mốc thì sai âm thầm mãi mãi.

Cách xử lý đã áp dụng, đúng theo 3.2: ghi nhận trạng thái thật, truy nguyên bằng mtime, **không hoàn tác** thay đổi của người khác, báo lại cho người có thẩm quyền quyết định.

Ca này cũng cho thấy giá trị của **gate chạy được** (4.2) so với lời văn: không ai phải tranh luận hợp đồng còn đúng không — chạy lệnh là biết.

### 6.5 Tài liệu mô tả trạng thái repo hết hạn trong ngày

Ngày 16/08/2026, ba file trong chính thư mục `docs KB/Dev/` được viết buổi sáng đã sai vào buổi chiều: mã `build_handbook.py` được thêm nhánh fallback, thư mục KB được khôi phục, bộ test từ đỏ 4 lỗi chuyển sang `OK`. Chi tiết ở `KB-pipeline-build-va-kiem-thu.md` mục 8.

**Bài học:** khẳng định về *trạng thái repo* có hạn dùng ngắn hơn nhiều so với khẳng định về *cơ chế*. Khi viết, tách hai loại: cơ chế thì mô tả kỹ, trạng thái thì kèm lệnh để người đọc tự chạy lại.

---

## 7. Nguyên tắc làm việc (`AGENTS.md`)

Thang đo bằng chứng chỉ là một nửa. Nửa kia là các ranh giới hành động — cũng là cơ chế bảo vệ bằng chứng.

### 7.1 Ranh giới mutation

`AGENTS.md` mục "An toàn":

- **Không mutation live, gửi chia sẻ, xoá KB/Agent hoặc upload dữ liệu private** nếu nhiệm vụ hiện tại chưa cho phép rõ ràng.
- **Không tự share KB vào space hoặc tự cấu hình sync** — đó là thay đổi quyền, cần người dùng thực hiện hoặc cho phép rõ (DEC-045, DEC-046).
- Không xoá PNG còn được Markdown tham chiếu (DEC-005).
- Meta-KB Agent **không tự động** thành corpus nghiệp vụ; chỉ bind sau audit nội dung, owner, ACL, retention, freshness.

Liên hệ với phương pháp: mutation không được phép **phá bằng chứng**. Đó là lý do DEC-027 bắt audit trước khi cleanup và DEC-005 cấm xoá asset còn được tham chiếu.

### 7.2 Ranh giới credential

- Không lưu credential, token, private key hoặc service-account mới trong project/audit.
- Nếu phát hiện credential hiện hữu: **không đọc nội dung và không tự xoá** khi chưa xác định dependency.
- `.gitignore` bảo vệ vùng key đã nhận diện; không `git add -f`, không force-push (DEC-035).
- Google Drive connector: mỗi KB trỏ đúng **một** thư mục con của `knowledge/`, tuyệt đối không trỏ root project (DEC-046).

Lưu ý cách diễn đạt "không đọc nội dung": nó có nghĩa là **liệt kê tên file thì được, mở file thì không**. Ranh giới nằm ở nội dung, không ở sự tồn tại.

### 7.3 Ranh giới dữ liệu người chơi

- `Data Private Weapon` và dữ liệu định danh/hành vi không tự động trộn vào consumer tài liệu (DEC-029).
- `GS9 CFL Item Profile` là boundary P0: không đổi tên, không mở, không đọc (DEC-047).
- Audit/handoff *"chỉ ghi schema, count và checksum, không ghi giá trị cá nhân cụ thể"* (DEC-029).

Câu cuối là một quy tắc viết bằng chứng: **mô tả hình dạng dữ liệu, không chép dữ liệu**. Nhờ vậy audit vẫn kiểm chứng được mà không trở thành bản sao của dữ liệu nhạy cảm.

### 7.4 Thứ tự đọc khi vào phiên

`AGENTS.md`: đọc `HANDOFF.md`, `STATUS.md`, `PROJECT.md`, `DECISIONS.md`. *"Chỉ mở audit/report liên quan khi cần bằng chứng có ngày."*

Phân vai bốn tài liệu:

| Tài liệu | Trả lời câu hỏi |
|---|---|
| `HANDOFF.md` | Phiên trước dừng ở đâu, tôi làm gì tiếp |
| `STATUS.md` | Trạng thái live hiện tại, có ngày |
| `PROJECT.md` | Kiến trúc và hợp đồng artifact |
| `DECISIONS.md` | **Vì sao** làm thế, luật bền vững |
| `audit/*` | Bằng chứng thô — mở khi cần chứng minh |

Ba tài liệu đầu **đổi theo thời gian**. `DECISIONS.md` chỉ **nới thêm**, các mục cũ được đánh dấu "Được thay thế" chứ không bị xoá — nên vẫn tra ngược được vì sao một quyết định cũ từng đúng.

---

## 8. Checklist trước khi viết một khẳng định

```text
[ ] Khẳng định này là CƠ CHẾ hay TRẠNG THÁI?
       cơ chế    -> mô tả kỹ, ít hết hạn
       trạng thái -> bắt buộc kèm ngày + lệnh kiểm chứng lại

[ ] Bằng chứng đến từ đâu?
       chạy lệnh / đọc file   -> Đã kiểm chứng
       UI hoặc MCP đọc được   -> Đã kiểm chứng ở lớp cấu hình
                                 nhưng runtime là lớp riêng (DEC-022)
       suy ra từ mã           -> ghi rõ "suy luận từ mã"
       chưa thử               -> Bị chặn — Chưa xác định

[ ] Có ngày chưa?

[ ] Có mã DEC để tra ngược chưa?

[ ] Có đường dẫn audit/ chưa? (khi có)

[ ] Phạm vi đã thử có bị viết rộng hơn thực tế không?
       "2/10 Agent"  KHÔNG PHẢI  "các Agent"

[ ] Im lặng có bị đọc thành phủ định không?
       "không thấy X"  KHÔNG PHẢI  "không có X"

[ ] Cuối file đã có mục "Chưa kiểm chứng" / "Rủi ro còn lại" chưa?
```

---

## Chưa kiểm chứng và rủi ro còn lại

**Chưa kiểm chứng:**

- **Không có công cụ nào kiểm tự động việc gắn nhãn.** Phân loại hoàn toàn phụ thuộc kỷ luật người viết. Không có test, lint hay gate nào bắt được một khẳng định thiếu nhãn hoặc gắn nhãn sai mức.
- **Chưa rà lại toàn bộ nhãn cũ theo ngày.** Nhiều khẳng định "Đã kiểm chứng" từ 06–07/08/2026 chưa được chạy lại; không biết còn đúng không. Chưa có quy ước về **hạn dùng** của một nhãn.
- **G6 (chat-test bind + retrieval) chưa chạy.** Đây là gate duy nhất chuyển các khuyến nghị bind từ *Có điều kiện* sang *Đã kiểm chứng*. Chừng nào chưa chạy, toàn bộ ma trận Agent × KB vẫn là thiết kế.
- **Chưa kiểm chứng chính phương pháp này có được tuân thủ đều không.** Quan sát trong tài liệu này dựa trên 4 file audit đọc kỹ trong tổng số 19 file `.md` của `audit/`, cộng với danh sách đếm số lần xuất hiện của các cụm từ phân loại. Đây là **mẫu**, không phải rà soát toàn bộ.

**Rủi ro còn lại:**

- **Nhãn dễ trở thành nghi thức.** Gắn "Đã kiểm chứng" cho mọi thứ vì quen tay sẽ làm thang đo mất nghĩa. Dấu hiệu cảnh báo: một tài liệu dài mà mục "Chưa kiểm chứng" ở cuối chỉ có một hai gạch đầu dòng.
- **"Bị chặn — Chưa xác định" dễ bị đọc thành "không quan trọng".** Thực tế đây là danh sách rủi ro. Sự cố đổi tên khi sync (5.1) chỉ tránh được vì có người đọc kỹ ô "Chưa xác định".
- **Ngày ghi trong tài liệu là ngày viết, không phải ngày kiểm chứng.** Hai thứ này thường trùng nhưng không phải luôn luôn; khi một khẳng định được chép lại từ tài liệu cũ, ngày gốc dễ bị thay bằng ngày mới. Chưa có quy ước phân biệt.
- **Thay đổi mã ngày 16/08/2026 chưa có mã DEC.** Nhánh fallback của `load_source_from_dirs`, `ASSETS = BUNDLE` và dòng marker mới đều là quyết định kiến trúc nhưng không tra ngược được vào `DECISIONS.md`. Đây chính là loại lỗ hổng mà DEC-008 định chặn.
- **Ba tài liệu Dev viết sáng 16/08 đã sai vào chiều cùng ngày.** Không có cơ chế nào đánh dấu một file Dev là "có thể đã cũ" ngoài dòng ngày ở đầu file. Người đọc phải tự so ngày và tự chạy lại lệnh.
