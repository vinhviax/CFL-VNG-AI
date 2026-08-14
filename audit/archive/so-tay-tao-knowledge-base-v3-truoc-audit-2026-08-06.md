# Sổ tay Tạo Knowledge Base — VNGGames Studio 9

**Phiên bản:** v3.0 — 06/08/2026 (tái cấu trúc toàn bộ, hợp nhất mọi đính chính, loại bỏ mâu thuẫn nội bộ)
**Công cụ mô tả:** Knowledge Base tại `vnggames.ai/kb/knowledge` (nhãn BETA trên tool)
**Đối tượng đọc:** Team LiveOps / vận hành non-tech dựng KB cho AI và cho người đọc
**Nguồn của tài liệu:** Reverse-engineer bằng thao tác trực tiếp trên tool + ảnh chụp màn hình thật. **Không có tài liệu chính thức nào từ đội phát triển tool.** Mọi câu trong Phần II đều gắn nhãn nguồn bằng chứng.

---

## 🔍 Cách đọc tài liệu này

### Hai lớp nhãn — bắt buộc đọc trước

Mọi phát biểu về công cụ ở **Phần II** mang **2 nhãn**: một nhãn về *mức độ chắc chắn*, một nhãn về *nguồn bằng chứng*.

**Lớp 1 — Mức độ chắc chắn:**

| Nhãn | Nghĩa |
|---|---|
| ✅ | **Xác thực trực tiếp** — đã nhìn thấy/thao tác trên tool thật |
| 🚨 | **Phát hiện quan trọng** — đã xác thực, nhưng ảnh hưởng vận hành thật hoặc mâu thuẫn với chính mô tả của tool |
| ⚠️ | **Suy luận / xác thực một phần** — có cơ sở nhưng chưa kiểm chứng đầy đủ; luôn ghi rõ suy ra từ đâu |
| ❌ | **Chưa xác thực** — chưa có bằng chứng, chỉ liệt kê để biết cần kiểm tra |

**Lớp 2 — Nguồn bằng chứng** (quan trọng khi audit lại):

| Nhãn | Nghĩa |
|---|---|
| `[TT]` | Claude **thao tác trực tiếp** trên trình duyệt, tự đọc kết quả |
| `[Test]` | Có **số liệu đo được** từ phép test A/B trên tool |
| `[NSD]` | **Người dùng tự thao tác** và báo lại/gửi ảnh kết quả |
| `[Ảnh]` | Từ **ảnh chụp màn hình** người dùng cung cấp ở phiên trước — Claude chưa tự kiểm lại trong phiên thao tác trực tiếp |

> 🚨 **Ưu tiên audit:** Mọi mục gắn `[Ảnh]` là nhóm cần kiểm tra lại đầu tiên — đó là dữ liệu Claude **không tự tay xác minh**, chép lại từ ảnh của phiên làm việc trước.

### Ba nguyên tắc biên tập của tài liệu này

1. **Không bịa.** Không có số liệu/tên trường/hành vi nào được viết ra nếu chưa có ảnh hoặc test thật. Thiếu thông tin thì ghi ❌, không viết như đã biết.
2. **Sửa đè, không giữ song song.** Khi bằng chứng mới mâu thuẫn nội dung cũ → sửa thẳng, ghi rõ "đính chính" và lý do sai trước đó. Không để 2 phiên bản mâu thuẫn cùng tồn tại.
3. **Tách bạch mô tả của tool và hành vi thật của tool.** Nhiều chỗ tool ghi một đằng, chạy một nẻo (xem mục 6.2, 10.2, 12.3). Tài liệu luôn ghi cả hai và chỉ rõ cái nào là thật.

---

## 📋 Mục lục

**PHẦN I — CHUẨN BỊ (không phụ thuộc công cụ)**
- [1 — Dọn file trước khi mở tool](#1)
- [2 — Viết cho AI vs viết cho người đọc](#2)
- [3 — Chuyện gì xảy ra sau khi bấm Tạo](#3)
- [4 — Ví dụ nội dung chuẩn theo từng loại file](#4)

**PHẦN II — THAM CHIẾU CÔNG CỤ (phần cốt lõi, gắn nhãn bằng chứng)**
- [5 — Bản đồ toàn cảnh công cụ](#5)
- [6 — Tạo KB: chế độ Nhanh](#6)
- [7 — Tạo KB: chế độ Nâng cao → tab Tổng quan](#7)
- [8 — Tab Mô hình: model, VLM, ASR](#8)
- [9 — Tab Xử lý (1): Parser theo loại file](#9)
- [10 — Tab Xử lý (2): Phân đoạn / chunking](#10)
- [11 — Tab Chia sẻ và tab Nguồn dữ liệu](#11)
- [12 — Khóa cấu hình sau khi KB đã có nội dung](#12)
- [13 — Làm việc trong KB Tài liệu: Documents · Wiki · Graph](#13)
- [14 — Làm việc trong KB FAQ: nhập liệu và kiểm thử](#14)
- [15 — Chat hỏi đáp trên KB](#15)

**PHẦN III — VẬN HÀNH**
- [16 — Dựng KB FAQ cho LiveOps](#16)
- [17 — KB cho người đọc](#17)
- [18 — Duy trì KB](#18)

**PHẦN IV — PHỤ LỤC**
- [A — Bảng trạng thái xác thực tổng hợp](#pl-a)
- [B — Danh sách việc chưa xác thực (backlog test)](#pl-b)
- [C — Nhật ký các phép test đã thực hiện](#pl-c)
- [D — Lịch sử phiên bản](#pl-d)
- [E — Nguồn tham khảo ngoài](#pl-e)

---

## ⭐ Tóm tắt 10 điều quan trọng nhất về công cụ

Nếu chỉ đọc được 1 phút, đọc bảng này. Chi tiết ở mục tương ứng.

| # | Phát hiện | Mục |
|---|---|---|
| 1 | **Tài liệu và FAQ là hai luồng cấu hình gần như tách biệt** — khác số tab, khác khái niệm lập chỉ mục, khác số trường model | [5](#5) |
| 2 | 🚨 **ASR (giọng nói → chữ) chưa dùng được** — dropdown model rỗng, cảnh báo "liên hệ admin để thêm" | [8.4](#8) |
| 3 | 🚨 **"Theo cấu trúc" không tách được đoạn** kể cả trên PDF thật có `Chương X` / `PHẦN BỐN` — hạn chế thật của engine | [10.3](#10) |
| 4 | 🚨 **FAQ "Chỉ câu hỏi" trả về 0 kết quả tuyệt đối** nếu từ khóa chỉ nằm trong câu trả lời | [7.2](#7) |
| 5 | 🚨 **"Thay toàn bộ" xóa sạch dữ liệu cũ, không hoàn tác được** — luôn Xuất backup trước | [14.3](#14) |
| 6 | **"Soạn thảo trực tuyến"** cho phép viết tài liệu Markdown thẳng trên tool, không cần file | [13.2](#13) |
| 7 | 🚨 **"Nhập từ URL" bấm không có phản hồi** — nhiều khả năng chưa hoạt động | [13.1](#13) |
| 8 | **Cấu hình bị khóa khi KB đã có nội dung**, nhưng mở lại được bằng cách xóa hết tài liệu | [12](#12) |
| 9 | **Mặc định chunking là Cha-con, cha 32.768 / con 8.192 ký tự** — đơn vị là *ký tự*, không phải *từ* | [10.4](#10) |
| 10 | 🚨 **Banner "cấu hình khuyến nghị" của chế độ Nhanh ghi sai 1 dòng** ("sinh câu hỏi đang bật" — thực tế tắt) | [6.2](#6) |

---
---

# PHẦN I — CHUẨN BỊ

> Phần này **không nói về công cụ**. Đây là nguyên tắc làm nội dung, đúng bất kể dùng tool nào. Người vội có thể nhảy sang [Phần II](#5), nhưng bỏ qua Phần I là lý do phổ biến nhất khiến KB chạy sai.

## 1 — Dọn file trước khi mở tool {#1}

**Nguyên tắc:** Tool không sửa được tài liệu tệ. Nó chỉ nhân bản cái tệ đó lên với tốc độ cao hơn. **80% ca AI trả lời sai là do file nguồn, không phải do cấu hình.**

### 1.1 — Ba việc bắt buộc trước khi nạp

**a) Chia làm ba rổ: Sống · Chết · Không biết**

- **Sống** = còn dùng, còn đúng với bản game hiện tại
- **Chết** = nói về phiên bản cũ, event đã kết thúc, quy trình đã thay
- **Không biết** = không ai chắc

Chỉ nạp rổ **Sống**. Rổ Chết archive ra folder riêng — đừng xóa, nhưng đừng để vào KB.

**b) Tìm và xử lý thông tin mâu thuẫn**

Hai file cùng nói về cách xử lý X nhưng khác nhau ở bước 3? AI không biết cái nào đúng — nó sẽ chọn ngẫu nhiên, hoặc tệ hơn, trộn cả hai.

**Cách nhanh:** Gom file theo chủ đề, đọc chéo 5 phút, giữ một bản duy nhất.

**c) Tách file nhiều chủ đề thành nhiều file**

File `Tài liệu vận hành 2026.docx` dài 80 trang gộp cả maintenance, nạp thẻ, event, khiếu nại → tách thành 4 file. **Một file một chủ đề là nguyên tắc quan trọng nhất** của cả sổ tay này. Lý do kỹ thuật xem [mục 3](#3) và [mục 10](#10).

### 1.2 — Hai cảnh báo từ đời thực

**NYC MyCity Chatbot (2024):** Chạy trên Microsoft Azure AI, lấy dữ liệu từ 2.000+ trang web của thành phố, không cấu trúc, không kiểm chứng → tư vấn cho chủ doanh nghiệp những việc trái luật (từ chối voucher Section 8, từ chối tiền mặt, lấy tip nhân viên).

**Air Canada v. Moffatt (2024 BCCRT 149):** Chatbot tự bịa ra chính sách hoàn tiền không tồn tại → BC Civil Resolution Tribunal buộc hãng trả CA$812,02. Tribunal khẳng định: hãng chịu trách nhiệm cho mọi thông tin trên trang web, không phân biệt nội dung tĩnh hay do chatbot tạo ra.

Nguồn đầy đủ ở [Phụ lục E](#pl-e).

---

## 2 — Viết cho AI vs viết cho người đọc {#2}

**Nguyên tắc:** Con người có bộ lọc thường trực. AI không có.

| Viết để **AI** hiểu đúng | Viết để **người** dễ theo |
|---|---|
| Một đoạn = một chủ đề, không hơn | Có mở đầu, bối cảnh, ví dụ kể chuyện |
| Không lời dẫn, không câu chuyển ý | Heading và mục lục đủ để nhảy phần |
| Không tham chiếu "xem phần trên" | Tham chiếu chéo thoải mái |
| Viết dạng điều kiện: *nếu X thì làm Y* | Hình ảnh, sơ đồ giúp hiểu nhanh |
| Metadata bắt buộc: chủ đề, tag, ngày update, người phụ trách | |
| Số liệu tuyệt đối, không nói "như bình thường" | |

### Cách không phải viết hai lần

1. Viết bản gốc theo chuẩn AI (Markdown, một chủ đề một file, có metadata)
2. Bản cho người = bản gốc + lớp điều hướng (mục lục, sơ đồ, "đọc gì trước")
3. Chỉ sửa bản gốc, không bao giờ sửa bản người rồi quên sync

Chi tiết cách tổ chức bản cho người ở [mục 17](#17).

> ℹ️ **Cập nhật liên quan:** Tool có sẵn tính năng **Truy hồi theo ngữ cảnh** (mặc định BẬT) tự viết thêm dòng ngữ cảnh cho mỗi đoạn — làm thay một phần việc metadata thủ công. Xem [mục 10.6](#10). Metadata thủ công vẫn nên giữ.

---

## 3 — Chuyện gì xảy ra sau khi bấm Tạo {#3}

**Pipeline khái niệm** (áp dụng cho loại Tài liệu; FAQ bỏ qua bước đọc file và cắt đoạn vì dữ liệu vào đã ở dạng Q&A):

```
1. Nạp (bạn)     → Upload file / soạn trực tuyến / kết nối nguồn ngoài
   ↓
2. Đọc file      → Parser bóc chữ ra khỏi file            (chỉ Tài liệu)
   ↓
3. Cắt đoạn      → Chia theo cấu hình Phân đoạn            (chỉ Tài liệu)
   ↓
4. Mã hoá nghĩa  → Mỗi đoạn/câu hỏi thành vector
   ↓
5. Lưu           → Cất vào kho lập chỉ mục
   ↓
6. Hỏi & kiểm    → Chat với AI, đối chiếu với nguồn
```

> ✅ `[TT]` **Pipeline thật của tool có tên gọi riêng và 5 giai đoạn hiển thị được** — xem [mục 13.3](#13) để đối chiếu sơ đồ khái niệm ở trên với tên giai đoạn thật trên UI.

### Tại sao bước 3 quan trọng nhất (với loại Tài liệu)

Hệ thống không đưa cả file 80 trang cho AI đọc. Nó cắt file thành nhiều đoạn, rồi khi có câu hỏi chỉ lấy vài đoạn giống nghĩa nhất:

- **AI trả lời dựa trên vài đoạn, không phải cả tài liệu.** Thông tin bị chia đôi rơi vào hai đoạn → câu trả lời thiếu.
- **Đoạn trộn nhiều chủ đề không giống mạnh với chủ đề nào** → ít khi được chọn.
- **Heading là ranh giới cắt tự nhiên** — xem [mục 10](#10) để biết công cụ nhận diện điều này bằng cách nào (và ở đâu nó **không** nhận diện được).

**→ Đây là lý do [mục 1](#1) yêu cầu tách file theo chủ đề, và [mục 4](#4) yêu cầu dùng heading thật.**

---

## 4 — Ví dụ nội dung chuẩn theo từng loại file {#4}

### 4.1 — Markdown (ưu tiên số 1)

```markdown
<!-- Metadata: đặt ngay đầu file -->
chu_de:           Xử lý sự cố kết nối
tag:              ket-noi, timeout, server, lag
ap_dung_cho:      CrossFire Legends · client 3.x+
nguoi_phu_trach:  LiveOps · Studio 9
cap_nhat:         2026-08-05

# Người chơi không vào được game, báo Connection timeout

## Dấu hiệu nhận biết

Màn hình dừng ở bước đăng nhập, hiện chữ "Connection timeout"
kèm mã lỗi 4 chữ số ở góc dưới bên phải.

## Nguyên nhân đã ghi nhận

1. Mạng người chơi không ổn định
2. Tường lửa/diệt virus chặn kết nối của game
3. Server đang bảo trì
4. Client cũ hơn phiên bản tối thiểu đang yêu cầu

## Cách xử lý, theo thứ tự

1. Yêu cầu đọc mã lỗi. Nếu bắt đầu bằng 5, chuyển sang mục khác và dừng.
2. Kiểm tra khung bảo trì. Nếu đang bảo trì, trả lời theo mẫu và dừng.
3. Hướng dẫn đổi Wi-Fi sang 4G để loại trừ mạng nhà.
4. Hướng dẫn tắt phần mềm diệt virus, thử lại.
5. Nếu vẫn lỗi: tạo ticket kèm mã lỗi, ID game, giờ xảy ra, nhà mạng.

## Kết quả mong đợi

Người chơi vào được game. Nếu sau bước 5 vẫn không, cần đội kỹ thuật.

## Không áp dụng cho

Lỗi mất kết nối giữa trận — xem file dis-trong-tran.md
```

**Vì sao chuẩn:** Mỗi `##` heading trở thành một đoạn riêng. ✅ `[Test]` Đây **không phải suy đoán** — đã đo được: văn bản có 3 heading `#`/`##` ra đúng 3 phân đoạn ([mục 13.2](#13)), và mẫu Markdown 5 heading ra 3 đoạn ([mục 10.3](#10)).

### 4.2 — Excel / CSV

```
cau_hoi | tra_loi | nhom | tag | cap_nhat
"Nạp thẻ không nhận xu" | "Chờ 5 phút..." | thanh-toan | "nap;xu;thanh toan" | 2026-08-01
"Đổi mật khẩu thế nào" | "Cài đặt > Tài khoản..." | tai-khoan | "mat khau;bao mat" | 2026-07-20
```

**Lỗi phổ biến:** merge ô, header lỡ dòng, mỗi sheet cấu trúc khác, xen dòng trống → parser đọc lệch cột.

> ℹ️ Excel còn có khối cấu hình riêng "Parser Excel tùy chỉnh" — xem [mục 9.4](#9).

### 4.3 — Word

**Quy tắc duy nhất:** Dùng heading **style** thật (Styles → Heading 1, Heading 2), không bôi đậm tăng font. Kiểm tra bằng View → Navigation Pane: nếu cây mục lục hiện ra, bạn dùng heading đúng.

### 4.4 — PDF: ba trường hợp, không phải hai

| Thử bôi đen chữ trong PDF | Nghĩa là | Cách xử lý |
|---|---|---|
| **Bôi được, chữ đúng** | Có text-layer tốt | Nạp thoải mái |
| **Không bôi được** | Ảnh chụp/scan, không có text-layer | Cần OCR — parser MinerU tự làm, kết quả phụ thuộc độ nét |
| **Bôi được nhưng chữ ra sai/rác** | Text-layer tồn tại nhưng hỏng (font nhúng sai, encoding lỗi) | ✅ `[TT]` Bật **"Ép OCR toàn bộ PDF (scanned)"** trong "Phân tích lại với tùy chọn" — xem [mục 13.5](#13) |

**Thứ tự ưu tiên nguồn:** Markdown/Word gốc → PDF xuất từ Word → PDF scan.

### 4.5 — PowerPoint

Nguyên tắc thiết kế: **một slide, một ý**. Slide nhồi 300 chữ tạo đoạn dài trộn ý, ít khi được chọn. Phần **Ghi chú của người trình bày** là chỗ đặt bối cảnh mà slide không đủ chỗ.

🚨 `[TT]` **Nhưng "1 slide = 1 đoạn" KHÔNG đúng trên thực tế.** Đo trên 1 file PPTX xuất PDF, 37 slide, parser mặc định MinerU: ra **69 phân đoạn** ≈ **1,86 đoạn/slide**. Slide nhiều chữ/nhiều khối bị tách thêm. Đối chiếu Phân đoạn 1 khớp đúng slide 1 (tiêu đề + phụ đề), kèm ảnh logo giữ nguyên trong nội dung đoạn — do parser bảo toàn hình ảnh khi bóc chữ, **không phải** do VLM (VLM là bước riêng, xem [mục 8.3](#8)).

### 4.6 — JSON

```json
{
  "ten_event": "Giải đấu Hè 2026",
  "mo_ta": "5v5 loại trực tiếp",
  "ngay_bat_dau": "2026-08-15",
  "dieu_kien_tham_gia": "Cấp 20+, tài khoản xác thực SĐT"
}
```

Tên khoá phải có nghĩa: `ngay_bat_dau` chứ không `d1`.

### 4.7 — Hình ảnh

Screenshot bảng số, sơ đồ có nhãn: nạp được, nhưng **phải bật toggle Đa phương thức (VLM)** ở tab Mô hình ([mục 8.3](#8)) — mặc định tool để tắt. Ảnh nhân vật, key art không có chữ: đừng nạp.

### 4.8 — Email

Xoá tên, SĐT, email, ID giao dịch **trước** khi nạp. Một khi vào KB, thông tin có thể xuất hiện trong câu trả lời cho người khác.

### 4.9 — Âm thanh

🚨 **Hiện chưa dùng được.** Việc chuyển giọng nói thành văn bản là toggle ASR riêng ở tab Mô hình, mặc định tắt, và **chưa có model ASR nào được gán** ([mục 8.4](#8)). Kể cả khi admin thêm model, ghi âm nhiều người nói chen, nhiễu nền vẫn ra bản chữ sai nhiều — biên bản họp viết tay luôn là nguồn tốt hơn.

---
---

# PHẦN II — THAM CHIẾU CÔNG CỤ

> 🚨 **Đây là phần cốt lõi và là phần dễ sai nhất.** Mọi phát biểu đều gắn nhãn mức độ chắc chắn + nguồn bằng chứng. Nếu bạn thấy điều gì khác trên tool, **tool đúng, tài liệu sai** — báo lại để sửa.

## 5 — Bản đồ toàn cảnh công cụ {#5}

### 5.1 — Vòng đời một KB

```
[Tạo KB]  ──chọn──►  Nhanh  hoặc  Nâng cao
                        │
                        ├─ Loại: Tài liệu  hoặc  FAQ   ← KHÔNG đổi được sau khi tạo
                        │
                        ▼
              [Modal "Cấu hình Knowledge Base"]  (icon ⚙, sửa được sau này)
                 Tài liệu: Tổng quan · Mô hình · Xử lý · Chia sẻ · Nguồn dữ liệu
                 FAQ:      Tổng quan · Mô hình · Chia sẻ · Nguồn dữ liệu
                        │
                        ▼
              [Trang làm việc của KB]  (tab nội dung, khác hẳn tab cấu hình)
                 Tài liệu: Documents · Wiki · Graph
                 FAQ:      Documents (danh sách Q&A) · ...
                        │
                        ▼
              [Chat]  (icon 💬) — hỏi đáp trên KB đã nạp
```

⚠️ **Điểm gây nhầm nhất của tool:** có **hai bộ tab hoàn toàn khác nhau**. Tab trong *modal cấu hình* (Tổng quan/Mô hình/Xử lý/Chia sẻ/Nguồn dữ liệu) ≠ tab trên *trang làm việc* (Documents/Wiki/Graph). Nhiều tài liệu nội bộ cũ trộn hai thứ này làm một.

### 5.2 — Hai loại KB: bảng khác biệt tổng quan

✅ `[TT]` Chỉ có 2 lựa chọn ở trường **Loại**, dạng nút pill chọn 1: **Tài liệu** hoặc **FAQ**. Điểm quan trọng không nằm ở ô chọn này mà ở chỗ nó dẫn tới **hai luồng cấu hình gần như tách biệt**.

| | **Tài liệu** | **FAQ** |
|---|---|---|
| Mô tả trên tool | "KB Tài liệu nạp tệp" | "KB FAQ lưu cặp câu hỏi/trả lời" |
| Tab trong modal cấu hình | **5** — Tổng quan, Mô hình, **Xử lý**, Chia sẻ, Nguồn dữ liệu | **4** — Tổng quan, Mô hình, Chia sẻ, Nguồn dữ liệu |
| Khái niệm lập chỉ mục | **RAG + Wiki** (tick được cả hai) | **Chế độ lập chỉ mục** + **Cách index câu hỏi** |
| Có "Độ chi tiết Wiki"? | Có, nếu bật Wiki | Không |
| Số trường ở tab Mô hình | **3** (Chat/tóm tắt, Embedding, Tổng hợp Wiki) | **2** (Chat/tóm tắt, Embedding) |
| Có VLM / ASR? | Có (trong "Tùy chọn mô hình nâng cao") | ✅ `[TT]` **Không có** |
| Có tab Xử lý (parser + phân đoạn)? | Có | **Không** |
| Có công cụ "Kiểm tra tìm kiếm"? | ✅ `[TT]` **Không** | ✅ `[TT]` **Có** |
| Nạp dữ liệu bằng | Tải tệp/thư mục, Soạn thảo trực tuyến, (Nhập từ URL) | Thêm Q&A tay, Nhập file JSON/CSV/XLSX |

🚨 **Đính chính so với bản v2 cũ:** Bản cũ ghi "Tài liệu có 3 tab, FAQ có 2 tab". Con số đó **thiếu** — thực tế modal cấu hình còn có thêm tab **Chia sẻ** và **Nguồn dữ liệu** ở cả hai loại. Số đúng: Tài liệu 5, FAQ 4.

**Vì sao khác biệt này quan trọng:** Tài liệu cần parser để đọc file, cần phân đoạn để cắt file dài — FAQ không cần cả hai vì dữ liệu vào đã ở dạng câu hỏi/câu trả lời rời rạc. Tab Xử lý biến mất hoàn toàn khỏi luồng FAQ vì không có gì để "xử lý" theo nghĩa đó.

### 5.3 — Khi nào chọn loại nào

| Câu hỏi tự đặt | Nếu có → chọn |
|---|---|
| Tài liệu dài, nhiều nhánh, câu hỏi rất đa dạng? | **Tài liệu** |
| Nội dung thay đổi theo từng patch/event? | **Tài liệu** |
| Đã có sẵn bảng ticket CS với cột câu hỏi + trả lời? | **FAQ** |
| Sai một chữ = mất tiền hoặc uy tín? | **FAQ** |

**Không phải chọn một.** Tạo hai KB song song là bình thường: **FAQ cho những câu phải trả lời chuẩn từng chữ, Tài liệu cho phần còn lại.**

---

## 6 — Tạo KB: chế độ Nhanh {#6}

✅ `[TT]` Đã xem giao diện Nhanh cho cả Tài liệu và FAQ.

### 6.1 — Một form chung cho cả 2 loại

Khác với Nâng cao (nơi Tài liệu và FAQ có 2 luồng khác hẳn), chế độ **Nhanh** rút gọn cả hai về **đúng một form giống nhau**:

```
Tạo Knowledge Base                                    [ Nhanh ] Nâng cao
Tạo nhanh — chỉ chọn mô hình, phần còn lại dùng cấu hình khuyến nghị.

Loại *
KB Tài liệu nạp tệp; KB FAQ lưu cặp câu hỏi/trả lời.
                                    [ Tài liệu ]  [ FAQ ]
Tên *
Mô tả

Mô hình chat / tóm tắt *          [ Chọn mô hình ▾ ]
Mô hình Embedding *               [ Chọn mô hình ▾ ]
```

Form Nhanh **chỉ hỏi 4 thứ**: Loại, Tên, Mô tả, 2 model. Mọi khái niệm khác — RAG/Wiki, Độ chi tiết Wiki, Chế độ lập chỉ mục FAQ, Cách index câu hỏi, parser, phân đoạn, VLM, ASR — **bị ẩn** và tự nhận giá trị có sẵn.

✅ `[TT]` Chế độ Nhanh **không dùng sidebar tab**, chỉ là một form cuộn duy nhất.

✅ `[TT]` Lúc tạo KB mới, tooltip hướng dẫn hiện thông báo: *"Không đổi loại được sau khi tạo."* — Loại bị khóa ngay từ lúc tạo xong, không cần chờ có nội dung.

### 6.2 — 🚨 Banner "Đã áp dụng cấu hình khuyến nghị" — có 1 dòng ghi sai

`[Ảnh]` Cuộn xuống dưới form Nhanh có banner:

```
ⓘ Đã áp dụng cấu hình khuyến nghị
RAG, chunk cha-con, truy hồi theo ngữ cảnh và sinh câu hỏi đang bật.
Parser dùng Tự động; Wiki, VLM và ASR đang tắt.
                                              Cấu hình đầy đủ ngay >
```

🚨 **Đối chiếu banner với hành vi thật** (kiểm tra bằng cách tạo KB thật rồi mở Cấu hình đầy đủ xem từng toggle):

| Thông số | Mặc định thật | Banner ghi | Khớp? |
|---|---|---|---|
| Phân đoạn cha-con | **Cha-con** | "chunk cha-con" | ✅ |
| Truy hồi theo ngữ cảnh | **Bật** | "…đang bật" | ✅ |
| RAG | **Bật** | "RAG…đang bật" | ✅ |
| Wiki / VLM / ASR | **Tắt** | "…đang tắt" | ✅ |
| **Sinh câu hỏi** | **TẮT** | "sinh câu hỏi **đang bật**" | ❌ **SAI** |
| Parser | (xem ghi chú ⚠️ dưới) | "Parser dùng Tự động" | ⚠️ chưa chốt |

**Kết luận:** Đúng 1 dòng trong banner sai — **"sinh câu hỏi đang bật" là chữ ghi nhầm**, thực tế Sinh câu hỏi mặc định **TẮT** ở cả Nhanh và Nâng cao. Đây là lỗi copy của banner, không phải cấu hình riêng của chế độ Nhanh.

⚠️ `[TT]` **Điểm mới chưa chốt về Parser:** Banner ghi "Parser dùng Tự động", nhưng khi mở tab Xử lý của một KB tạo qua **Nâng cao mà không hề đụng vào tab Xử lý**, ô "Cấu hình parser" lại hiển thị **"Tùy chỉnh theo định dạng"** (không phải "Tự động"). Chưa rõ đây là mặc định thật của Nâng cao, hay UI hiển thị khác nhau giữa 2 chế độ tạo. → [Phụ lục B](#pl-b).

### 6.3 — Kết luận quan trọng: Nhanh và Nâng cao dùng chung một bộ mặc định

🚨 **Đính chính (ghi đè mọi suy luận trước):** Nhanh và Nâng cao **không phải hai bộ mặc định khác nhau**. Xác nhận bằng cách tạo KB thật ở cả hai chế độ rồi so từng toggle — giống nhau.

⚠️ **Ghi chú cho người đọc:** Không tin 100% chữ trong banner. Cách chắc chắn duy nhất để biết trạng thái thật của một KB là **mở "Cấu hình đầy đủ" và nhìn trực tiếp vào từng toggle**.

Có nút **"Cấu hình đầy đủ ngay"** trong banner — bấm vào chuyển thẳng sang Nâng cao. Hai chế độ chuyển đổi qua lại tự do (Nâng cao cũng có nút "Chuyển sang tạo nhanh").

---

## 7 — Tạo KB: chế độ Nâng cao → tab Tổng quan {#7}

## 7.1 — Loại **Tài liệu**: RAG và Wiki

✅ `[TT]` Đã bấm thử, xác nhận cả hai trạng thái tick/không tick.

```
Chiến lược lập chỉ mục *
Cách lập chỉ mục nội dung để truy hồi.

[✓] RAG (vector + từ khóa)          [✓] Wiki  NEW
    Tìm kiếm ngữ nghĩa + từ khóa         Tổng hợp tài liệu đã tải lên
    trên các đoạn. Mặc định cho          thành các trang wiki liên kết.
    hầu hết KB.
```

**Cả hai ô tick được đồng thời** — đây là checkbox, không phải chọn-một. Đã xác nhận bằng cách bấm Wiki khi RAG đang tick sẵn: cả hai cùng tick.

| Tiêu chí | RAG | Wiki |
|---|---|---|
| Cách dùng | Hỏi đáp, nhận câu trả lời kèm nguồn | Đọc trang đã tổng hợp, đi theo liên kết |
| Giữ file gốc? | Có | Không — viết lại thành trang mới |
| Mạnh nhất khi | Tra cứu nhanh, câu hỏi rời rạc | Onboarding, cần hiểu cả bức tranh |
| Rủi ro chính | Lấy thiếu đoạn nếu file cắt sai | Sai sót gốc bị viết lại thành câu khẳng định trôi chảy, khó phát hiện |

**Độ chi tiết Wiki — chỉ hiện khi bật Wiki:**

```
Độ chi tiết Wiki
Mức độ chia nhỏ tài liệu thành trang wiki.

[ Tập trung ]  [ Tiêu chuẩn ]  [ Toàn diện ]
                    ▲ mặc định
              "Số trang cân bằng."
```

✅ `[TT]` Ba mức, dạng pill chọn 1, mặc định **Tiêu chuẩn**. 🚨 **"Số trang cân bằng" là dòng caption mô tả mức Tiêu chuẩn — KHÔNG phải ô nhập số.** Đây là lỗi phổ biến nhất trong tài liệu nội bộ cũ; cần sửa nếu còn ai đang hướng dẫn "điền số trang wiki".

### ⚠️ Wiki khuếch đại chất lượng đầu vào — theo cả hai chiều

Wiki không chỉ hiển thị lại tài liệu, nó **viết lại**. File gốc mâu thuẫn sẽ được hoà thành một câu khẳng định nghe rất chắc chắn, và bạn không còn thấy dấu vết mâu thuẫn.

✅ `[TT]` **Chiều tốt — đã có bằng chứng thực tế.** Tạo KB "Test Doc RAG+Wiki" (RAG+Wiki cùng bật, Tiêu chuẩn), nạp chính file sổ tay này (Markdown có heading rõ, đã qua nhiều lượt đính chính). Trang Summary do Wiki sinh ra khớp **chính xác đến từng số liệu và cụm trích dẫn**, giữ nguyên cả những sắc thái tinh vi nhất — chi tiết ở [mục 13.4](#13).

**Kết luận cân bằng:** cảnh báo "Wiki khuếch đại cái sai" đúng với **nguồn bẩn/mâu thuẫn**; với **nguồn sạch có heading rõ**, Wiki khuếch đại theo chiều tích cực rất rõ. Điều kiện quyết định là chất lượng nguồn ([mục 1](#1)), không phải bản thân Wiki.

❌ Chưa test Wiki trên một nguồn cố ý có mâu thuẫn để thấy trực tiếp chiều xấu.

## 7.2 — Loại **FAQ**: Chế độ lập chỉ mục và Cách index câu hỏi

✅ `[TT]` FAQ **không có** RAG/Wiki. Phần lập chỉ mục nằm trong khối riêng **"Cấu hình FAQ"**:

```
Cấu hình FAQ
Chiến lược lập chỉ mục cho kho tri thức dạng FAQ.

Chế độ lập chỉ mục *
Nội dung nào được lập chỉ mục cho mục FAQ.
                                    [ Chỉ câu hỏi ]  [ Câu hỏi + trả lời ]
Cách index câu hỏi *
Cách lập chỉ mục nhiều câu hỏi của một mục.
                                    [ Gộp ]  [ Tách ]
```

Mặc định quan sát được: **Chỉ câu hỏi** + **Tách**.

### 🚨 Test A — Chế độ lập chỉ mục: chênh lệch là tuyệt đối, không phải tương đối

✅ `[Test]` **Cách test:** 2 KB FAQ giống hệt, cùng nạp 5 mục Q&A (bộ dữ liệu ở [mau-faq-test-cau-hinh.md](mau-faq-test-cau-hinh.md)), chỉ khác Chế độ lập chỉ mục. Đo bằng công cụ "Kiểm tra tìm kiếm" ([mục 14.4](#14)). Câu hỏi test: **"đổi tên cần bao nhiêu mảnh ngọc"** — từ khóa *"mảnh ngọc"* **chỉ nằm trong câu trả lời**, không có trong câu hỏi chuẩn lẫn biến thể.

| KB test | Chế độ lập chỉ mục | Ngưỡng 0.5 | Ngưỡng 0.0 |
|---|---|---|---|
| KB #1 | Chỉ câu hỏi | Không có mục khớp | **Vẫn không có mục khớp** |
| KB #2 | Câu hỏi + trả lời | **Khớp đúng, điểm 0.572** | — |

**Đối chứng kỹ thuật:** cùng công cụ, hỏi nguyên văn một câu hỏi chuẩn khác trong KB #1 → khớp điểm **1.000**. Chứng minh search hoạt động bình thường, "không có mục khớp" không phải lỗi kỹ thuật.

**Kết luận:** "Chỉ câu hỏi" **loại bỏ hoàn toàn** nội dung câu trả lời khỏi không gian tìm kiếm. Không phải "điểm thấp bị lọc" — mà là **câu trả lời không tham gia tính điểm chút nào** (bằng chứng: ngưỡng 0.0 vẫn ra 0 kết quả, không hiện candidate điểm thấp nào).

**Chọn thế nào:**
- Dùng **Chỉ câu hỏi** khi bạn viết đủ biến thể câu hỏi ([mục 16](#16)) và muốn match sạch, không nhiễu.
- Dùng **Câu hỏi + trả lời** khi câu trả lời chứa từ khóa đặc thù mà người dùng có thể gõ thẳng (mã lỗi, tên chính sách, tên vật phẩm).

### Test B — Cách index câu hỏi: khác biệt nhỏ, không có bên nào thắng rõ

✅ `[Test]` **Cách test:** 2 KB FAQ, cùng để Chế độ lập chỉ mục = Chỉ câu hỏi (cố định), chỉ đổi Gộp/Tách. Câu hỏi test: **"tài khoản bị đá ra khỏi game liên tục thì làm sao"** — từ vựng rất khác câu hỏi chuẩn, chỉ trùng 1 biến thể cụ thể.

| KB test | Cách index | Điểm (ngưỡng 0.0) | Trường "Khớp:" hiển thị |
|---|---|---|---|
| KB #3 | **Tách** | 0.718 | Chỉ đúng biến thể: *"bị đá ra khỏi game liên tục"* |
| KB #4 | **Gộp** | 0.738 | Câu hỏi chuẩn + biến thể gộp chung |

**Kết luận:** Cả hai đều match đúng — **không có trường hợp "không tìm thấy"** như Test A. Khác nhau ở **cơ chế**: Tách tính điểm trên biến thể khớp nhất (mỗi biến thể là 1 đơn vị độc lập); Gộp tính trên đại diện gộp của câu hỏi chuẩn + mọi biến thể.

⚠️ **Giới hạn của kết luận:** Gộp (0.738) nhỉnh hơn Tách (0.718) — **ngược với suy đoán ban đầu**, nhưng chênh lệch chỉ 0,02 trên **đúng 1 phép test**. Đủ để **bác bỏ** giả định "Tách chắc chắn chính xác hơn", **không đủ** để kết luận Gộp tốt hơn. Muốn chắc: lặp lại với nhiều câu hỏi thật từ ticket CS rồi lấy trung bình.

**Khuyến nghị thực dụng:** giữ mặc định **Tách** và đầu tư vào việc viết đủ biến thể — biến số đó ảnh hưởng lớn hơn nhiều so với lựa chọn Gộp/Tách.

---

## 8 — Tab Mô hình: model, VLM, ASR {#8}

### 8.1 — Ba vai trò model (loại Tài liệu)

| Trường | Vai trò (mô tả trên tool) | Có ở FAQ? |
|---|---|---|
| **Mô hình chat / tóm tắt** | "Sinh tóm tắt và trang wiki" | Có |
| **Mô hình Embedding** | "Vector hóa các đoạn cho tìm kiếm ngữ nghĩa" | Có |
| **Mô hình tổng hợp Wiki** | "Mô hình dùng để tổng hợp trang wiki" | **Không** |

✅ `[TT]` Doc và FAQ **dùng chung một pool model** cho Chat/tóm tắt + Embedding. Khác biệt duy nhất: Doc có thêm vai trò thứ 3 (Tổng hợp Wiki).

⚠️ Đáng chú ý: trường "Mô hình chat/tóm tắt" của **FAQ** vẫn ghi mô tả *"Sinh tóm tắt và trang wiki"* — dù FAQ không có Wiki. Nhiều khả năng là text UI dùng chung chưa viết riêng cho FAQ, **không nên suy ra rằng FAQ có sinh wiki**. Cần hỏi đội phát triển tool để chắc.

### 8.2 — 🚨 Danh sách model không ổn định giữa các lần mở

| Vai trò | Model quan sát được |
|---|---|
| Chat/tóm tắt · Tổng hợp Wiki | `qwen3.6-plus` · `gpt-oss-120b` · `hosted_vllm/qwen3.6-35b` · **`deepseek-v4-flash`** (không phải lúc nào cũng có) |
| Embedding | `text-embedding-3-large` · `text-embedding-3-small` · `qwen3-embed-8b` |
| VLM | `qwen3.6-plus` · `gpt-oss-120b` · `hosted_vllm/qwen3.6-35b` — 🚨 **không có `deepseek-v4-flash`** |

🚨 `[TT]` **Phát hiện:** Số model cho vai trò Chat/tóm tắt **dao động 3↔4 giữa các lần mở**:
- Lần mở khi tạo KB FAQ, và lần mở trên KB Tài liệu đã có nội dung: **4 model** (có deepseek).
- Lần mở khi tạo KB "Test Doc RAG+Wiki": **chỉ 3 model** (không có deepseek).

Chat/tóm tắt và Tổng hợp Wiki **luôn đồng bộ với nhau** (cùng có hoặc cùng thiếu deepseek trong một lần mở) → đúng là dùng chung 1 pool, chỉ là tổng số trong pool dao động.

⚠️ **Nguyên nhân chưa rõ** — có thể do rollout dần `deepseek-v4-flash`, hoặc lỗi tải danh sách. **Ý nghĩa vận hành:** nếu không thấy model mong muốn, tải lại trang / mở lại modal trước khi báo lỗi.

✅ `[TT]` **VLM là ngoại lệ ổn định:** pool VLM chỉ có 3 model, **không bao giờ thấy `deepseek-v4-flash`** kể cả khi Chat/tóm tắt của cùng KB đó đang có 4. → Muốn dùng model mới nhất để đọc ảnh: hiện chưa chọn được.

**Chọn độc lập:** Chat/tóm tắt và Tổng hợp Wiki dùng chung danh sách nhưng chọn riêng được. Ví dụ cấu hình thật đã thấy: Chat/tóm tắt `qwen3.6-plus`, Embedding `text-embedding-3-large`, Tổng hợp Wiki `hosted_vllm/qwen3.6-35b`.

### 8.3 — Đa phương thức (VLM) — đọc ảnh trong tài liệu

✅ `[Ảnh]` Nằm trong "Tùy chọn mô hình nâng cao" (bấm mở rộng dưới 3 dropdown chính).

| Tùy chọn | Mô tả trên tool | Mặc định |
|---|---|---|
| **Đa phương thức (VLM)** | "Trích xuất nội dung ảnh bằng mô hình thị giác" | **Tắt** |
| **Nhận dạng giọng nói (ASR)** | "Chuyển audio thành văn bản" | **Tắt** |

Khi bật VLM, hiện thêm 1 trường bắt buộc **Mô hình VLM** (3 model, xem 8.2).

**Ý nghĩa:** xử lý ảnh trong tài liệu (screenshot, sơ đồ, biểu đồ) **không tự động** — phải chủ động bật. VLM có model sẵn nên dùng được ngay.

### 8.4 — 🚨 ASR — bật được nhưng KHÔNG dùng được

```
Nhận dạng giọng nói (ASR)                                 [●───] BẬT
Chuyển audio thành văn bản.

Mô hình ASR *
Mô hình dùng để chuyển giọng nói thành chữ.
                                    [ Chọn mô hình ▾ ]
                                    ⚠ Chưa có model — liên hệ admin để thêm.
Ngôn ngữ
Để trống để tự động nhận dạng.
```

🚨 `[Ảnh]` **Đây là phát hiện vận hành cần báo admin:** dropdown Mô hình ASR **rỗng**, kèm cảnh báo *"Chưa có model — liên hệ admin để thêm."* Dù bật toggle, tính năng **chưa hoạt động**. Team định nạp file ghi âm sẽ bị chặn ngay ở đây — **không phải lỗi cấu hình của người dùng**.

⚠️ **Phân biệt hai trường "Ngôn ngữ" khác nhau:**
- Trường **Ngôn ngữ** dưới ASR → dùng cho nhận diện ngôn ngữ khi chuyển giọng nói thành chữ.
- Trường **Gợi ý ngôn ngữ** ở tab Xử lý ([mục 10.6](#10)) → dùng cho lập chỉ mục/embedding văn bản.
Hai trường độc lập, cấu hình riêng.

✅ `[TT]` Toàn bộ mục nâng cao VLM/ASR này **không xuất hiện** ở tab Mô hình của loại FAQ.

---

## 9 — Tab Xử lý (1): Parser theo loại file {#9}

> Chỉ áp dụng cho loại **Tài liệu**. FAQ không có tab Xử lý.

### 9.1 — Hai chế độ cấu hình parser

✅ `[TT]` Mục **Cấu hình parser**, mô tả: *"Tự động chọn engine khuyến nghị cho từng loại tệp. Tùy chỉnh cho phép bạn đổi từng định dạng."*

- **Tự động (khuyến nghị)** — tool tự chọn engine cho từng loại tệp
- **Tùy chỉnh theo định dạng** — mở bảng đầy đủ **14 nhóm định dạng** (tool hiển thị đúng chữ "14 nhóm định dạng"), tự chỉnh từng nhóm

⚠️ Xem ghi chú chưa chốt về giá trị mặc định của ô này ở [mục 6.2](#6).

### 9.2 — Sáu engine

`[Ảnh]` Mô tả nguyên văn từ tool (đã dịch):

| Engine | Mô tả | Đặc điểm |
|---|---|---|
| **Built-in** | Engine mặc định của DocReader cho định dạng phức tạp (Word, PDF, Excel, email, ảnh). Cân bằng chất lượng/tốc độ | Cân bằng, đa năng |
| **MinerU** | Độ chính xác cao nhất — layout, bảng, công thức và OCR qua dịch vụ MinerU tự host | Chất lượng cao nhất, **chậm nhất** |
| **LLM** | Trích xuất theo luật bởi một chat model, cấu hình riêng theo từng KB | Linh hoạt nhất, chất lượng tùy model |
| **markitdown** | Bộ chuyển đổi MarkItDown của Microsoft cho tài liệu Office và web | Cân bằng, cho Office/web |
| **liteparse** | Trích xuất văn bản nhanh theo đúng thứ tự đọc | Nhanh, chỉ thấy ở PDF |
| **Simple** | Trích xuất kiểu Go-native cho văn bản thuần | Nhanh, cho file text thuần |

🚨 **Điểm bản v1 ghi sai:** parser **không phải** "chỉ có 3 loại dùng chung". Thực tế có **6 engine**, và **mỗi nhóm định dạng có một tập con engine riêng** kèm một engine đặt sẵn.

### 9.3 — Bảng 14 nhóm định dạng

✅ `[TT]` **Cột "Đang chọn sẵn" đã được kiểm lại toàn bộ 14/14 nhóm trong phiên thao tác trực tiếp** (trên một KB Tài liệu chưa từng đụng vào tab Xử lý).
`[Ảnh]` Cột "Các engine chọn được" vẫn từ ảnh phiên trước, **chưa kiểm lại từng dropdown** → ưu tiên audit.

| # | Nhóm | Đuôi | Các engine chọn được `[Ảnh]` | Đang chọn sẵn ✅`[TT]` |
|---|---|---|---|---|
| 1 | Tài liệu PDF | `.pdf` | Built-in, MinerU, LLM, markitdown, liteparse | **MinerU** |
| 2 | Tài liệu Word | `.docx` `.doc` | Built-in, MinerU, LLM, markitdown | **MinerU** |
| 3 | Bài trình chiếu | `.pptx` `.ppt` | Built-in, MinerU, markitdown | **MinerU** |
| 4 | Bảng tính Excel | `.xlsx` `.xls` | Built-in, MinerU, LLM, markitdown | **Built-in** |
| 5 | Tệp CSV | `.csv` | Simple, LLM, markitdown | **Simple** |
| 6 | Markdown | `.md` `.markdown` | Built-in, Simple, LLM, markitdown | **Built-in** |
| 7 | Văn bản thuần | `.txt` | Simple, LLM | **Simple** |
| 8 | Tệp JSON | `.json` | Simple | **Simple** |
| 9 | Hình ảnh | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.tiff` `.webp` | Built-in, Simple, MinerU | **MinerU** |
| 10 | Tệp Email | `.msg` `.eml` | Built-in, LLM | **Built-in** |
| 11 | Sách điện tử | `.epub` | Built-in | **Built-in** |
| 12 | Trang web | `.html` `.htm` | Built-in, markitdown | **Built-in** |
| 13 | Lưu trữ web | `.mhtml` | Built-in | **Built-in** |
| 14 | **Âm thanh** | `.mp3` `.wav` `.m4a` `.flac` `.ogg` | ✅`[TT]` **chỉ có Simple** trong danh sách | 🚨 **Built-in** |

🚨 **Đính chính quan trọng — nhóm Âm thanh (dòng 14):** Bản v2 cũ ghi *"Không có mặc định — phải tự chọn Simple"*. **Sai.** Kiểm tra trực tiếp: ô này **đang hiển thị giá trị "Built-in"**, trong khi mở dropdown ra thì **danh sách chỉ có duy nhất một mục "Simple"**. Tức giá trị đang chọn **không nằm trong** danh sách chọn được — một điểm không nhất quán của UI.
⚠️ Chưa rõ engine nào thật sự chạy khi nạp file audio. Vì ASR chưa dùng được ([mục 8.4](#8)) nên điểm này hiện **chưa ảnh hưởng vận hành**, nhưng cần hỏi đội phát triển tool. → [Phụ lục B](#pl-b).

**Cách đọc bảng:** cột "Đang chọn sẵn" là engine tool tự đặt nếu bạn không đụng vào. Với đa số trường hợp, để nguyên là đúng. Chỉ đổi khi kết quả sai — cách phát hiện: sau khi nạp, hỏi AI một câu mà bạn biết chắc câu trả lời nằm ở đâu; nếu AI không tìm được, khả năng cao engine bóc chữ ra lỗi.

**Ghi chú theo nhóm:**
- **PDF/Word/PPTX** để MinerU là hợp lý (chất lượng cao nhất cho layout phức tạp). Đổi lại: **chậm hơn**.
- **Word phải dùng heading style thật** ([mục 4.3](#4)).
- **Excel** mặc định Built-in (nhanh, cân bằng); bảng có công thức/merge phức tạp thì cân nhắc MinerU.

### 9.4 — Parser Excel tùy chỉnh (khác với chọn engine)

✅ `[TT]` Ngoài dropdown engine, riêng nhóm Excel có thêm khối **"Parser Excel tùy chỉnh"** với 2 chế độ:

**Tự nhận diện** (mặc định) — *"Tự nhận diện đọc định dạng và phòng ban từ tên từng tệp."*
→ Hệ thống đọc **tên file** để đoán file khớp khuôn mẫu Excel nào đã cấu hình sẵn. Dùng khi kho có nhiều loại báo cáo Excel khác cấu trúc từ nhiều phòng ban.

**Thủ công** — *"Thủ công ghim một parser cho mọi tệp Excel trong kho tri thức này."*
→ Hiện thêm trường **"Định dạng parser"**. Đây **không phải** danh sách engine, mà là danh sách **khuôn mẫu định dạng Excel đã cấu hình sẵn**. `[Ảnh]` Giá trị quan sát được:
- **Không dùng** (mặc định) — đọc Excel như bảng thường
- **FPA · Monthly Performance**
- **FPA · Launching & Checkpoint**

⚠️ **Chưa xác thực:** khuôn mẫu "FPA · …" do tổ chức tự tạo hay có sẵn của tool, và có tạo thêm được không. **Theo yêu cầu, chủ đề này tạm gác lại** — chưa viết hướng dẫn tạo khuôn mẫu Excel.

---

## 10 — Tab Xử lý (2): Phân đoạn / chunking {#10}

✅ `[TT]` Mục **Phân đoạn**, mô tả: *"Điều khiển cách chia tài liệu trước khi embedding."* Chỉ có ở loại Tài liệu.

> Đây là mục thay thế hoàn toàn con số "200–500 từ" trong mọi tài liệu nội bộ cũ — **sai cả đơn vị lẫn giá trị**.

### 10.1 — Bốn chiến lược phân đoạn

✅ `[TT]` Mặc định = **Tự động**. Mô tả nguyên văn từng chiến lược:

| Chiến lược | Mô tả trên tool |
|---|---|
| **Tự động** (mặc định) | "Bộ phân tích chọn giữa chia theo tiêu đề, theo cấu trúc và theo độ dài cho mỗi tài liệu." |
| **Theo tiêu đề** | "Chia tại ranh giới tiêu đề Markdown; mỗi đoạn mang theo đường dẫn tiêu đề. Tốt cho Markdown có cấu trúc." |
| **Theo cấu trúc** | "Chia theo dấu hiệu cấu trúc: ngắt trang, mục đánh số, dấu hiệu chương, tiêu đề viết hoa. Lý tưởng cho PDF không có tiêu đề Markdown." |
| **Theo độ dài** | "Bỏ qua cấu trúc; chia đệ quy theo số ký tự và dấu phân tách — hành vi gốc." |

**Điều này xác nhận trực tiếp khuyến cáo ở [mục 1](#1) và [mục 3](#3):** heading thật sự được dùng làm cách cắt đoạn riêng, và mỗi đoạn cắt theo tiêu đề còn **mang theo "đường dẫn tiêu đề"** (breadcrumb, ví dụ `# Sổ tay ## Mục 10`) — giúp AI biết đoạn nằm ở đâu trong cấu trúc gốc.

🚨 **Nhưng đọc tiếp [mục 10.3](#10) trước khi tin vào mô tả của "Theo cấu trúc".**

### 10.2 — Công cụ "Xem trước phân đoạn"

✅ `[Ảnh]` Nút **Xem trước phân đoạn** có ở mọi chiến lược, mở modal riêng với **4 văn bản mẫu** dựng sẵn: **Tài liệu Markdown · Danh sách FAQ · Chương PDF · Văn xuôi**. Bấm **Chạy thử** để xem kết quả.

**Kết quả hiện 2 lớp:**
- *Lớp 1 — thống kê tổng:* số dòng, số ký tự, số tiêu đề Markdown, số ngắt trang, số dấu hiệu chương, ngôn ngữ tự nhận diện, và dòng `N đoạn · Ø trung bình · σ độ lệch chuẩn · min · max` (đơn vị ký tự).
- *Lớp 2 — từng đoạn:* số thứ tự (#0, #1…), số ký tự, **số token ước lượng**, khoảng vị trí ký tự trong văn bản gốc, **đường dẫn tiêu đề** (breadcrumb), nội dung đoạn đầy đủ.

🚨 **Giới hạn quan trọng của công cụ này** `[TT]`: nó **chỉ chạy trên văn bản dán tay / 4 mẫu có sẵn**, **không đọc được file đã tải lên KB**. Muốn xem file thật bị cắt thế nào, phải tải file lên rồi mở chi tiết tài liệu → "Xem phân đoạn" ([mục 13.3](#13)).

### 10.3 — 🚨 Benchmark thật: 3 chiến lược, kết quả gây bất ngờ

`[Ảnh]` **Test trên 4 văn bản mẫu:**

| Văn bản mẫu | Cấu trúc thật | **Theo tiêu đề** | **Theo cấu trúc** |
|---|---|---|---|
| Tài liệu Markdown | 5 heading `#`/`##`/`###` | ✅ **3 đoạn** — tách đúng | ❌ 1 đoạn (bỏ qua cả 5 heading) |
| Danh sách FAQ | Cặp `Q:`/`A:` | ❌ 1 đoạn (gộp 3 câu hỏi khác chủ đề) | ❌ 1 đoạn |
| Chương PDF | `CHAPTER ONE/TWO/THREE` viết hoa | ❌ 1 đoạn | 🚨 **1 đoạn** — mâu thuẫn mô tả |
| Văn xuôi | Không có gì | ❌ 1 đoạn (hợp lý) | ❌ 1 đoạn (hợp lý) |

**Kết luận 1 — "Theo tiêu đề" chỉ hiểu cú pháp `#`/`##` Markdown.** Không tự suy rộng ra các dấu hiệu heading mà mắt người nhận ra (CHAPTER X viết hoa, cặp Q/A). Với 3/4 mẫu có cấu trúc thật nhưng không phải Markdown, chiến lược này gộp tất cả vào 1 đoạn.

**Kết luận 2 — "Theo cấu trúc" thất bại ngay cả trên đúng loại dấu hiệu nó tuyên bố hỗ trợ.** Mô tả ghi *"…dấu hiệu chương, tiêu đề viết hoa"*, mẫu "Chương PDF" khớp 2/4 tiêu chí, nhưng kết quả **1 đoạn, 0 dấu hiệu chương được đếm**.

**Test bổ sung** `[Ảnh]`: một văn bản chứa 4 kiểu dấu hiệu cùng lúc (số Ả Rập `1.` `2.`, `Chương 3:`, `PHẦN BỐN:` viết hoa) → 785 ký tự, **0 dấu hiệu chương, 0 ngắt trang, 0 tiêu đề MD**, gộp **1 đoạn**.

### 🚨 Chốt hạ: test trên PDF THẬT — vẫn thất bại

✅ `[NSD]` Người dùng tự tạo KB "Test PDF cấu trúc", tự tải lên file PDF thật (`test-theo-cau-truc.pdf` — 4 trang, **ngắt trang thật**, font Unicode chuẩn, chứa đủ 4 kiểu dấu hiệu trên), đặt Chiến lược = **Theo cấu trúc**.

> **Kết quả xử lý thật (engine sản xuất, không phải sandbox preview): Tổng 1 phân đoạn.**
> Toàn bộ 4 phần — "1. Giai đoạn chuẩn bị", "2. Giai đoạn triển khai", "Chương 3: Giai đoạn tổng kết", "PHẦN BỐN: LƯU TRỮ DỮ LIỆU" — nằm chung trong **đúng 1 đoạn**.

**Kết luận dứt điểm:** Đây **không phải** hạn chế của riêng công cụ Xem trước khi mô phỏng bằng text dán tay. Ngay cả với **file PDF thật, ngắt trang thật, engine thật**, "Theo cấu trúc" **không nhận diện được** dấu hiệu chương/mục/viết hoa. **Đây là hạn chế (hoặc bug) thật của chiến lược này.**

⚠️ **Giới hạn còn lại của kết luận:** mới test 1 file PDF dựng bằng thư viện reportlab — có thể thiếu metadata/outline/font-hint mà MinerU dựa vào. **Nên thử thêm 1 PDF nghiệp vụ thật** (báo cáo có chương đánh số, xuất từ Word) để loại trừ hoàn toàn khả năng lỗi nằm ở cách tạo file test. → [Phụ lục B](#pl-b).

**Dữ liệu thực tế bổ sung** ✅`[TT]`: một báo cáo PDF nghiệp vụ thật đang chạy production (`CFL MMR GMT 2026.04.pdf`, **79 trang**, KB dùng chiến lược **Tự động**) → chỉ ra **2 phân đoạn**, đoạn 1 chiếm **68/79 trang**. Không phải phép so sánh 1-1 cho "Theo cấu trúc", nhưng cùng hướng: nhận diện cấu trúc trên PDF nghiệp vụ nhiều trang kém hiệu quả hơn kỳ vọng, kết quả nghiêng về cắt theo ngưỡng độ dài.

### "Theo độ dài" — hoạt động đúng thiết kế

✅ `[Ảnh]` Test trên văn xuôi tiếng Việt **14.746 ký tự** (không heading, không dấu hiệu chương), chế độ Cha-con:

- Ngôn ngữ tự nhận diện: **`vi`** ✅ (xác nhận để trống Gợi ý ngôn ngữ vẫn nhận đúng tiếng Việt)
- Kết quả: **2 đoạn con** — #0 = **8.192 ký tự** (kịch trần ngưỡng con), #1 = 6.554 ký tự (14.746 − 8.192, khớp chính xác)

✅ **Khớp hoàn toàn với cấu hình.** Văn bản < ngưỡng cha (32.768) nên vẫn nằm trong 1 khối cha; modal hiển thị **đơn vị đoạn con** (đơn vị dùng cho tìm kiếm/embedding thật) nên cắt tại ngưỡng con.

🚨 **Hệ quả cần biết:** ranh giới đoạn rơi **giữa một câu** — đoạn #0 kết thúc bằng *"…Đánh giá hiệu suất của đội vận hành"*, đoạn #1 bắt đầu bằng *"không nên chỉ dựa vào số liệu doanh thu…"*. Đúng thiết kế *"bỏ qua cấu trúc; chia đệ quy theo số ký tự và dấu phân tách"* — **số ký tự tuyệt đối được ưu tiên trước**, Dấu phân tách chỉ là tham khảo phụ. Với Cha-con (mặc định), tác động được giảm nhẹ vì đoạn cha vẫn được trả về kèm; với Thông thường thì mất ngữ cảnh rõ hơn.

**Bài học chung cho cả 3 chiến lược:** đừng chọn theo tên/mô tả. **Luôn kiểm tra kết quả cắt trên chính file thật** trước khi nạp hàng loạt.

### 10.4 — Cha-con vs Thông thường và số liệu thanh trượt

```
Phân đoạn cha-con
Phân đoạn hai cấp: đoạn con nhỏ khớp chính xác, nhưng
đoạn cha lớn được trả về để có ngữ cảnh phong phú hơn.
                                    [ Thông thường ]  [ Cha-con ]
```

🚨 **Mặc định thật là Cha-con**, ở **cả Nhanh và Nâng cao**. (Bản trước từng đính chính nhầm thành "Thông thường" do suy luận sai thứ tự ảnh chụp — nay đã xác nhận lại.)

**Khi ở chế độ Cha-con (mặc định):** `[Ảnh]`

| Thông số | Khoảng | Mặc định |
|---|---|---|
| Kích thước đoạn **cha** | 512 – 32.768 ký tự | **32.768** |
| Kích thước đoạn **con** | 64 – 8.192 ký tự | **8.192** |
| Chồng lấp cha | 0 – 4.096 ký tự | **0** (0 = dùng độ chồng lấp chính) |
| Chồng lấp con | 0 – 2.048 ký tự | **0** (0 ≈ 20% kích thước đoạn con) |

**Khi tự chuyển sang Thông thường:** `[Ảnh]`

| Thông số | Khoảng | Mặc định |
|---|---|---|
| Kích thước đoạn | 128 – 16.384 ký tự | **16.384** |
| Độ chồng lấp | 0 – 4.096 ký tự | **0** |

**Đơn vị luôn là KÝ TỰ, không phải TỪ**, ở cả hai chế độ.

✅ **Tóm lại, một KB mặc định (chưa ai chỉnh gì) đang chạy:** chế độ **Cha-con**, đoạn cha **32.768** / đoạn con **8.192** ký tự, chồng lấp **0**.

**Quan trọng:** 4 chiến lược phân đoạn và 2 chế độ cấu trúc (Thông thường/Cha-con) là **hai lựa chọn độc lập, kết hợp tự do** — cùng cặp số Cha-con xuất hiện y hệt bất kể đang chọn chiến lược nào.

❌ Chưa xác thực: hành vi khi văn bản vượt ngưỡng cha (>32.768 ký tự) — đoạn cha có cắt cứng tương tự đoạn con không.

### 10.5 — Sinh câu hỏi: mặc định TẮT

🚨 **Sinh câu hỏi mặc định TẮT cho cả Nhanh và Nâng cao.** Banner của chế độ Nhanh ghi ngược lại — đó là lỗi copy của banner, xem [mục 6.2](#6).

Khi bật, hiện thêm trường con **"Số câu hỏi mỗi đoạn"** — ✅ khoảng **1–10**, giá trị khi bật lần đầu: **3**.

### 10.6 — Tùy chọn nâng cao của Phân đoạn

```
Truy hồi theo ngữ cảnh                                    [●───] BẬT (mặc định)
Thêm tiêu đề ngữ cảnh do LLM viết vào mỗi đoạn để cải thiện truy hồi.

Giới hạn token                                        [ - ] 0 [ + ]     (0-8192, 0 = tắt)

Dấu phân tách
Ký tự mà bộ chia ưu tiên khi cắt. Dấu ưu tiên cao được thử trước.
  [ \n\n ×] [ \n ×] [ 。×] [ ! ×] [ ? ×] [ ； ×] [ ; ×]

Sinh câu hỏi                                              [───●] TẮT (mặc định)

Gợi ý ngôn ngữ                        [ + DE ]  [ + EN ]  [ + ZH ]
DE / EN / ZH. Để trống = tự nhận diện.
```

✅ **Xác nhận cả hai mặc định:** Truy hồi theo ngữ cảnh **BẬT**, Sinh câu hỏi **TẮT**.

**⚠️ Ràng buộc quan trọng:** ✅ Khi **Chiến lược = Theo độ dài**, hai trường sau bị **vô hiệu hóa**: **Giới hạn token** và **Gợi ý ngôn ngữ**.
*Vì sao hợp lý:* "Theo độ dài" bỏ qua cấu trúc, không phân tích ngữ nghĩa/ngôn ngữ, nên hai tham số này không có tác dụng.
*Ý nghĩa vận hành:* cần "Gợi ý ngôn ngữ" hoặc "Giới hạn token" thì **không thể** đồng thời dùng "Theo độ dài" — phải đổi qua Tự động / Theo tiêu đề / Theo cấu trúc.
❌ Chưa xác thực: "Truy hồi theo ngữ cảnh", "Dấu phân tách", "Sinh câu hỏi" có bị ảnh hưởng gì khi chọn Theo độ dài không.

**Ba điểm cho team tiếng Việt:**

1. **Truy hồi theo ngữ cảnh mặc định BẬT** — LLM tự viết thêm dòng ngữ cảnh cho mỗi đoạn trước khi lập chỉ mục. ✅ `[TT]` Đã thấy trực quan trên tài liệu thật: khối **"Ngữ cảnh tìm kiếm (LLM tạo)"** hiện ngay đầu mỗi phân đoạn ([mục 13.3](#13)) — tính năng chạy thật, không chỉ là mô tả UI.
2. **Dấu phân tách nghiêng về ngữ pháp CJK** (có `。`). Với tiếng Việt, các dấu `\n\n`, `\n`, `.`, `!`, `?`, `;` đều dùng bình thường.
3. **Gợi ý ngôn ngữ không có nút Tiếng Việt** — chỉ DE/EN/ZH. Nhưng **để trống (tự nhận diện) là lựa chọn đúng**: ✅ đã đo, tool nhận diện đúng `vi` trên văn bản 14.746 ký tự.

### 10.7 — Override cấu hình riêng cho từng lượt tải file

✅ `[TT]` Trong modal **"Tải tài liệu lên"**, bấm mở rộng **"Xử lý nâng cao"** hiện bộ tham số **giống hệt cấu hình Phân đoạn cấp KB**: Kích thước đoạn, Độ chồng đoạn, Giới hạn token, toggle Đoạn cha-con, Ký tự phân tách, Ngôn ngữ, toggle Đa phương thức (ảnh).

Mô tả trên tool: *"Ghi đè mặc định của KB cho lần tải này. Để 0 / để trống dùng mặc định KB."*

**Ý nghĩa vận hành:** không cần đổi cấu hình chung của cả KB khi chỉ vài file cần xử lý khác — override ngay lúc tải lên, không ảnh hưởng file khác.

⚠️ Ô "Ngôn ngữ" ở đây có placeholder `vd: en, vi` — khác với "Gợi ý ngôn ngữ" cấp KB (chỉ 3 nút DE/EN/ZH). Nhiều khả năng là ô nhập tay tự do; ❌ chưa test `vi` gõ tay có hoạt động không.

---

## 11 — Tab Chia sẻ và tab Nguồn dữ liệu {#11}

### 11.1 — Tab Chia sẻ

✅ `[TT]` Mô tả: *"Chia sẻ Knowledge Base này với các Space."*

```
Chọn space  [ Chọn space để chia sẻ ▾ ]   [ Chỉ đọc ▾ ]   [ Chia sẻ ]

Đã chia sẻ tới  0
    (Chưa chia sẻ tới space nào)

ⓘ Sau khi chia sẻ, thành viên space truy cập KB này theo quyền được gán.
  Quyền Chỉnh sửa cho phép sửa nội dung; Chỉ đọc chỉ cho truy hồi và hỏi đáp.
```

Hai mức quyền: **Chỉnh sửa** và **Chỉ đọc**.

### 11.2 — Tab Nguồn dữ liệu: Notion, Google Drive, NAS

🚨 **Đính chính lớn:** Bản trước ghi mục này "chưa xác thực, không có ảnh nào". Thực tế **có tồn tại**, tên là **"Nguồn dữ liệu"**, và hỗ trợ **3 dịch vụ, không phải 2**.

✅ `[TT]` **Vị trí:** modal Cấu hình KB (icon ⚙) → tab **"Nguồn dữ liệu"** (icon mây). Mô tả: *"Đồng bộ nội dung từ hệ thống bên ngoài theo lịch."* Khi trống, hiện nút **"+ Thêm nguồn dữ liệu đầu tiên"**, mở wizard **4 bước**: **1. Chọn loại → 2. Thông tin xác thực → 3. Tài nguyên → 4. Chiến lược.**

**Bước 1 — 3 loại nguồn:**

| Dịch vụ | Mô tả trên tool |
|---|---|
| **Notion** | "Đồng bộ trang và database từ Notion." |
| **Google Drive** | "Đồng bộ tệp và thư mục được chia sẻ với một service account của Google." |
| **NAS** | "Đồng bộ tệp từ ổ NAS qua giao thức SMB." |

**Bước 2 — thông tin xác thực** (✅ đã xem cấu trúc form, **không nhập dữ liệu thật**):

| Nguồn | Trường bắt buộc |
|---|---|
| **Notion** | Tên · **Integration Token** (placeholder `ntn_xxxx`) · nút "Kiểm tra kết nối" · link hướng dẫn `notion.so/my-integrations` |
| **Google Drive** | Tên · **Service account JSON** (dán toàn bộ JSON key) · Shared Drive ID (tùy chọn) · mục phụ "Quyền yêu cầu" |
| **NAS** | Tên · **Đường dẫn share** (UNC, vd `\\192.168.1.10\share\folder`) · **Tên đăng nhập** (`DOMAIN\user` hoặc `user@domain`) · **Mật khẩu** |

🚨 **Nhận xét vận hành quan trọng:** cả 3 phương thức đều đòi hỏi **thiết lập kỹ thuật cấp quản trị**, **không phải** "đăng nhập Google/Notion cá nhân bằng OAuth" như nhiều người mặc định nghĩ:
- **Google Drive** cần **service account của GCP** — phải tạo service account, lấy file JSON key, rồi **chia sẻ thư mục Drive đích với email của service account** (không phải email cá nhân).
- **Notion** cần **Integration Token** tạo ở trang dành cho lập trình viên — không phải nút "Đăng nhập bằng Notion".
- **NAS** cần tài khoản domain nội bộ + giao thức SMB — chỉ dùng được nếu tool truy cập được mạng nội bộ chứa NAS.

**→ Kết luận cho LiveOps:** khả năng cao **team IT/admin phải làm bước 2**. LiveOps không tự làm được nếu không có các thông tin kỹ thuật này.

❌ **Chưa xác thực — bước 3 (Tài nguyên) và bước 4 (Chiến lược):** chưa nhập thông tin xác thực thật nên chưa qua được bước 2. Chưa biết: chọn được từng folder hay lấy cả ổ; tần suất đồng bộ; xử lý khi file gốc bị xoá/sửa; chiến lược lập chỉ mục cho nguồn ngoài có giống nguồn upload tay không.

**Sáu câu hỏi cần trả lời khi có tài khoản kỹ thuật để test thật:**
1. Chọn được từng folder cụ thể, hay bắt buộc lấy cả tài khoản/ổ?
2. Đồng bộ tự động theo lịch hay phải bấm tay? Bao lâu một lần?
3. Xoá file ở nguồn thì KB có xoá theo không?
4. Sửa file ở nguồn thì bao lâu KB cập nhật?
5. File đồng bộ về có đi qua đúng pipeline parser/phân đoạn của KB không?
6. Có giới hạn dung lượng/số file mỗi lần đồng bộ không?

**Ba nguyên tắc đúng bất kể tool hoạt động thế nào:**
1. **Tạo folder riêng cho KB**, không trỏ vào folder làm việc chung.
2. **Kết nối bằng tài khoản dùng chung**, không phải tài khoản cá nhân.
3. **Tự động đồng bộ không thay được việc rà soát** — vẫn cần quy ước file nào là bản chốt.

**Nếu chưa dùng được nguồn ngoài — quy ước đặt tên khi nạp tay:**
```
[nhom]__[chu_de]__[ngay_cap_nhat].[duoi]
thanhtoan__xu-ly-loi-nap-the__2026-08-05.md
```
Update: nạp bản mới, xoá bản cũ **ngay trong cùng một lần làm việc**.

---

## 12 — Khóa cấu hình sau khi KB đã có nội dung {#12}

✅ `[TT]` Mở modal Cấu hình của một KB đã có nội dung, **hai banner cam** hiện cùng lúc ở tab Tổng quan:

> *"Kho tri thức này đã có nội dung — loại, indexing và mô hình embedding bị khóa."*
> *"Kho tri thức này đã có nội dung — chiến lược lập chỉ mục bị khóa. **Hãy xóa tài liệu để thay đổi.**"*

### Cái gì bị khóa, cái gì không

| Cấu hình | Khi KB đã có nội dung | Ghi chú |
|---|---|---|
| **Loại** (Tài liệu/FAQ) | 🔒 Khóa | Khóa **ngay từ lúc tạo xong**, không cần chờ có nội dung ([mục 6.1](#6)) |
| **Chiến lược lập chỉ mục** (RAG/Wiki hoặc Chế độ lập chỉ mục + Cách index) | 🔒 Khóa | Mở lại được — xem dưới |
| **Mô hình Embedding** | 🔒 Khóa | Cảnh báo riêng: *"Mô hình embedding bị khóa vì KB này đã có nội dung được lập chỉ mục."* |
| **Mô hình chat/tóm tắt** | ✅ **KHÔNG khóa** | Vẫn đổi được bình thường, không cảnh báo |
| **Mô hình tổng hợp Wiki** | ⚠️ Nhiều khả năng không khóa | Suy luận theo cùng logic với Chat/tóm tắt — chưa kiểm riêng |
| **Parser / Phân đoạn** (tab Xử lý) | ✅ **KHÔNG khóa** | Đổi được; áp dụng cho tài liệu nạp sau, hoặc dùng "Phân tích lại" cho tài liệu cũ ([mục 13.5](#13)) |

🚨 **Đính chính quan trọng: "khóa" KHÔNG có nghĩa "vĩnh viễn".** Banner ghi rõ *"Hãy xóa tài liệu để thay đổi"* — khóa **có điều kiện**, gắn với việc còn nội dung đã lập chỉ mục. **Xóa hết tài liệu/Q&A thì mở lại được.**

⚠️ **Ý nghĩa vận hành:** Nếu tạo KB FAQ với "Chỉ câu hỏi" rồi phát hiện cần "Câu hỏi + trả lời" sau khi đã nạp dữ liệu thật:
- Cách nhanh: tạo KB mới.
- Cách giữ nguyên KB: chấp nhận xóa hết dữ liệu, đổi cấu hình, nạp lại (nhớ **Xuất backup trước** — [mục 14.3](#14)).

**→ Vì vậy: quyết định Chế độ lập chỉ mục / Cách index / RAG-Wiki / Embedding TRƯỚC khi nạp dữ liệu production.** Dùng một KB test nhỏ để thử trước, như cách làm ở [mục 7.2](#7).

---

## 13 — Làm việc trong KB Tài liệu: Documents · Wiki · Graph {#13}

✅ `[TT]` Trang làm việc của KB loại Tài liệu có **3 tab nội dung**: **Documents**, **Wiki** (chỉ có nội dung nếu bật Wiki lúc tạo), **Graph**.

### 13.1 — Bốn cách nạp nội dung

✅ `[TT]` Nút tải lên (góc phải khung danh sách) mở dropdown **4 lựa chọn**:

| Lựa chọn | Trạng thái |
|---|---|
| **Tải tệp lên** | ✅ Hoạt động — mở hộp thoại chọn file của hệ điều hành |
| **Tải thư mục lên** | ✅ Tồn tại trong menu — ❌ chưa test hành vi thật |
| **Nhập từ URL** | 🚨 **Bấm không có phản hồi gì** — không mở modal, không toast lỗi. Chữ hiển thị nhạt hơn 3 mục còn lại. Nhiều khả năng **chưa hoạt động / đang phát triển** |
| **Soạn thảo trực tuyến** | ✅ Hoạt động tốt — xem 13.2 |

### 13.2 — ⭐ "Soạn thảo trực tuyến" — viết thẳng trên tool, không cần file

✅ `[TT]` Mở modal **"Tạo tri thức Markdown"**:

```
Tạo tri thức Markdown

Kho tri thức đích        [ Test Doc RAG+Wiki ▾ ]   ← đổi sang KB khác được
Tiêu đề tri thức                                 0/100
[__________________________________]

[ B I S <> H1 H2 H3 ☰ 1. ☑ " 📎 🔗 🖼 ⊞ ─ ]     ← toolbar định dạng
[ Nhập nội dung Markdown...                    ]

                    [Hủy] [Xem trước] [Lưu nháp] [Xuất bản]
```

- **Kho tri thức đích** — dropdown chọn KB, mặc định là KB đang mở, **đổi sang KB Tài liệu khác được**.
- **Toolbar đầy đủ:** đậm/nghiêng/gạch ngang, code, H1/H2/H3, danh sách gạch đầu dòng/số/checklist, trích dẫn, code block, link, ảnh, bảng, đường kẻ ngang.
- **Xem trước** — chuyển sang chế độ render Markdown thật.
- **Lưu nháp** — ❌ chưa test trạng thái nháp hiển thị thế nào trong danh sách.
- **Xuất bản** — ✅ đã test đầy đủ: hiện toast **"Đã xuất bản — bắt đầu lập chỉ mục"**, tài liệu xuất hiện ngay với tên `[Tiêu đề].md` (tool tự thêm `.md`), gắn nhãn nguồn **MANUAL** + icon bút chì (phân biệt với file tải lên).

✅ `[Test]` **Nội dung đi qua đúng pipeline như file tải lên:** văn bản test có 3 heading `#`/`##` → ra đúng **3 phân đoạn**, khớp ranh giới từng heading.

**⭐ Ý nghĩa vận hành lớn:** LiveOps **không cần tạo file rồi tải lên** — soạn thẳng trên tool là đủ. Đây là cách nhanh nhất để thêm một trang hướng dẫn ngắn mà không rời khỏi tool.

### 13.3 — Quy trình xử lý thật: 5 giai đoạn, xem tiến độ real-time

✅ `[TT]` Mở chi tiết một tài liệu đang xử lý, có khối **"Tiến trình xử lý"**:

```
Tiến trình xử lý       Đang hoàn tất       38.8s đã trôi · 4/5 giai đoạn
[████████████░░░░░░░░░░░░░░░░░░░░░░░░]

○ Phân tích tài liệu                                    Đang chờ
✓ Chia đoạn                                             8ms
✓ Vector hóa                                            1.8s
✓ Đa phương thức                                        1.2s
✓ Hậu xử lý (2 mục)                                     11ms
```

**5 giai đoạn thật:** Chia đoạn (chunking) → Vector hóa (embedding) → Đa phương thức (xử lý ảnh) → Hậu xử lý → Phân tích tài liệu.

⚠️ Việc "Phân tích tài liệu" chạy **sau cùng** (và nhiều khả năng là bước dành cho Wiki: tóm tắt + trích thực thể) là **suy luận từ quan sát thứ tự**, chưa xác nhận với đội phát triển tool.

**Xem kết quả cắt đoạn của file thật:** trong chi tiết tài liệu có 3 chế độ xem — **Xem trước** (render file gốc), **Toàn văn**, **Xem phân đoạn**. Chế độ "Xem phân đoạn" hiện từng đoạn kèm khối **"Ngữ cảnh tìm kiếm (LLM tạo)"** — đây là bằng chứng trực quan Truy hồi theo ngữ cảnh ([mục 10.6](#10)) chạy thật.

### 13.4 — Tab Wiki

✅ `[TT]` Cấu trúc Wiki sinh ra trên KB thật (3 tài liệu):

- **Mục lục** — trang chỉ mục tự động, tự cập nhật khi có trang mới
- **Nhật ký hoạt động**
- 2 cách xem: theo **Thư mục** hoặc theo **Loại**
- Tự phân loại trang vào thư mục theo chủ đề — quan sát được: *Configuration, Core, Data Processing, Entities, Features* (mỗi thư mục có số trang riêng)
- Một trang **"[tên file] - Summary"** cho mỗi tài liệu
- Khối **"Thực thể"** — tự trích thực thể có tên riêng thành trang riêng, liên kết qua lại (quan sát được **36 thực thể** với 3 tài liệu)

**Bằng chứng chất lượng** — đối chiếu trang Summary do Wiki sinh ra với chính nội dung sổ tay gốc:

| Wiki viết ra | Đối chiếu |
|---|---|
| *"Once a KB has content, the Type, Indexing Strategy, and Embedding Model are locked… The Chat/Summary Model remains editable"* | ✅ Đúng cả sắc thái "Chat/tóm tắt không bị khóa" ([mục 12](#12)) |
| *"By Structure:… Test Failure: Even on real PDFs with 'CHAPTER X' or 'PHẦN BỐN', it failed to split… This is a confirmed engine limitation."* | ✅ Giữ nguyên cả cụm tiếng Việt, khớp 100% [mục 10.3](#10) |
| *"Parent: 32,768 chars. Child: 8,192 chars."* | ✅ Đúng số tuyệt đối |
| *"VLM:… Uses the same pool as Chat (minus deepseek-v4-flash)."* | ✅ Bắt đúng chi tiết nhỏ nhất ([mục 8.2](#8)) |
| *"Question Only:… returns zero results."* | ✅ Đúng bản chất Test A ([mục 7.2](#7)) |

→ Với nguồn sạch, Wiki **không làm mất sắc thái**, kể cả các đính chính tinh vi.

### 13.5 — Quản lý tài liệu: danh mục, bộ lọc, menu từng tài liệu

**Danh mục tài liệu** ✅ `[TT]`: nút "+" cạnh "Danh mục tài liệu" mở đúng modal **"Quản lý thẻ"** giống hệt FAQ ([mục 14.2](#14)) — nhập tên + chọn 1 trong 7 màu + "Thêm thẻ". Đã test tạo tag thành công. **Hệ thống tag dùng chung logic cho cả 2 loại KB**, chỉ khác tên hiển thị ("Danh mục tài liệu" vs "Phân loại").

**Bộ lọc** ✅ `[TT]`: ô tìm theo tên · **Mọi định dạng** · **Mọi trạng thái** · **Mọi nguồn** · lọc theo ngày tải lên · chuyển xem lưới/danh sách.
Dropdown "Mọi định dạng" liệt kê theo **đuôi file thô**: PDF, DOCX, DOC, TXT, MD, MARKDOWN, EPUB, XLSX, XLS, CSV, PPTX, PPT, MSG, EML, HTML… ⚠️ Điểm nhỏ không nhất quán: `.md` và `.markdown` (cùng 1 nhóm parser ở [mục 9.3](#9)) hiện thành **2 dòng lọc riêng**.

**Menu từng tài liệu** ✅ `[TT]` (icon "⋮"):

```
✏  Sửa nội dung              (❌ chưa test — nhiều khả năng chỉ tài liệu nguồn MANUAL mới sửa được)
🔄 Phân tích lại              (chạy lại theo cấu hình hiện tại của KB)
⚙  Phân tích lại với tùy chọn
⇢  Chuyển                    (chuyển tài liệu sang KB khác)
🗑  Xóa
```

⭐ **"Phân tích lại" trả lời một câu hỏi tồn đọng lâu:** đổi Chiến lược phân đoạn **KHÔNG cần** xóa và tải lại file. Dùng "Phân tích lại" (theo cấu hình KB hiện tại) hoặc "Phân tích lại với tùy chọn" (ghi đè riêng cho lần chạy này).

**"Phân tích lại với tùy chọn"** mở đúng bộ tham số như "Xử lý nâng cao" lúc upload ([mục 10.7](#10)) — **cộng thêm 1 trường mới:**

- 🚨 **Ép OCR toàn bộ PDF (scanned)** — *"Render mọi trang PDF thành ảnh để OCR/VLM, bỏ qua nhận diện text-layer. Dùng cho PDF có text-layer rác/sai. Chỉ áp dụng cho tệp PDF."*
  → Đây là lời giải cho **trường hợp PDF thứ 3** ở [mục 4.4](#4): PDF bôi đen được nhưng chữ ra sai.

❌ Chưa test: kết quả thật trước/sau khi bấm "Phân tích lại".

### 13.6 — Tab Graph

✅ `[TT]` Đồ thị node **tương tác thật** (kéo/thu phóng được), có ô "Tìm node…", nút "Vừa khung" và "Ẩn mũi tên". Bảng chú giải **5 loại node**:

| Loại node | Màu | Ý nghĩa | Quan sát được |
|---|---|---|---|
| **Tóm tắt** | Xanh dương | 1 node/tài liệu — trang Summary | 3 |
| **Thực thể** | Xanh lá | Tên riêng được trích (công ty, sản phẩm, khái niệm có tên) | 36 |
| **Khái niệm** | Cam | Khái niệm/thuật ngữ chung | 26 |
| **Tổng hợp** | — | ⚠️ Suy luận: node tổng hợp xuyên nhiều tài liệu | **0** |
| **So sánh** | — | ⚠️ Suy luận: node so sánh giữa tài liệu/thực thể | **0** |

Node nối bằng cạnh thể hiện quan hệ được nhắc cùng nhau trong tài liệu.

❌ **Chưa xác thực:** "Tổng hợp" và "So sánh" là 2 loại node có thật trong chú giải nhưng **chưa quan sát được ví dụ nào** (đều 0) — ý nghĩa ghi ở bảng trên chỉ là suy luận từ tên gọi. Có thể cần nhiều tài liệu cùng chủ đề hơn để chúng xuất hiện.

---

## 14 — Làm việc trong KB FAQ: nhập liệu và kiểm thử {#14}

### 14.1 — Modal "Thêm Q&A" (nhập tay từng mục)

✅ `[TT]`

```
Thêm Q&A

Câu hỏi chuẩn *
Câu hỏi tương tự (0/10)
Câu hỏi loại trừ (0/10)
Câu trả lời (0/5) *
Phân loại                                    [ Chưa phân loại ▾ ]
                                                    [ Hủy ]  [ Lưu ]
```

| Trường | Giới hạn | Ghi chú |
|---|---|---|
| **Câu hỏi chuẩn** * | 1 | Tên trường thật. Sổ tay cũ gọi "Câu hỏi chính" — cùng một khái niệm |
| **Câu hỏi tương tự** | tối đa **10** | Tên thật cho khái niệm cũ gọi "Biến thể câu hỏi" |
| **Câu hỏi loại trừ** | tối đa **10** | 🚨 Chặn match thật — xem 14.1.1 |
| **Câu trả lời** * | tối đa **5** | ❌ Chưa rõ vì sao cho phép nhiều câu trả lời cho 1 mục |
| **Phân loại** | 1 | Tag tự tạo — xem 14.2 |

**Cách nhập:** gõ text rồi bấm nút "+" bên phải để biến thành chip. Không bấm "+" thì giá trị chưa được thêm.

#### 14.1.1 — 🚨 "Câu hỏi loại trừ" chặn match hoàn toàn

✅ `[Test]` Test trên mục "Vì sao tài khoản của tôi bị tạm khoá?":

1. **Trước khi thêm:** hỏi *"tôi quên mật khẩu nên không đăng nhập được"* → khớp mục này, điểm **0.707** (qua biến thể "không đăng nhập được nữa").
2. **Thêm chính câu đó vào "Câu hỏi loại trừ"**, lưu lại. Dòng Q&A hiện thêm nhãn **"1 phủ định"**.
3. **Hỏi lại đúng câu cũ** → **"Không có mục khớp"**, ngay cả ở ngưỡng **0.0**.

**Kết luận:** đây là cơ chế **chặn thật ở tầng truy hồi** — điểm rơi từ 0.707 xuống 0 tuyệt đối.
**Dùng khi nào:** loại trừ câu hỏi *nghe giống nhưng đáp án khác*. Ví dụ: "quên mật khẩu" nghe giống "bị khoá tài khoản" nhưng quy trình xử lý khác hẳn.

#### 14.1.2 — Hai toggle trên mỗi dòng Q&A

✅ `[Test]` Mỗi dòng Q&A có 2 toggle cam, nhãn không hiện trên UI. Xác định được nhờ **thanh hành động khối** (chọn nhiều mục → hiện nút Bật/Tắt/Đề xuất/Bỏ đề xuất) và test hành vi:

| Toggle | Tên | Khi TẮT | Ảnh hưởng tìm kiếm |
|---|---|---|---|
| Trái | **Đề xuất** | Dòng không đổi | ✅ Test: vẫn khớp **0.999** — **không ảnh hưởng** |
| Phải | **Kích hoạt** | Dòng hiện nhãn đỏ **"Đã tắt"** | ✅ Test: **"Không có mục khớp"** tuyệt đối |

**Kết luận: toggle "Kích hoạt" chính là trường `is_enabled`** trong file mẫu JSON/CSV — tắt là loại hẳn mục đó khỏi tìm kiếm, kể cả khớp nguyên văn 100%.

⚠️ **"Đề xuất" tồn tại như khái niệm riêng nhưng chưa rõ dùng để làm gì** — không ảnh hưởng search. Giả thuyết (chưa kiểm chứng): gắn cờ cho danh sách câu hỏi gợi ý hiển thị cho người dùng cuối. → [Phụ lục B](#pl-b).

### 14.2 — "Phân loại" là tag tự tạo, không phải preset

✅ `[TT]` Nút "+" cạnh "Phân loại (n)" ở sidebar mở modal **"Quản lý thẻ"**:

```
Quản lý thẻ
[ Ví dụ: Vận hành              ]  [ + Thêm thẻ ]
🔴 🟠 🟡 🟢 🔵 ⚪ ⬜   (7 màu)

⚪ Untagged                              ✏️  🗑
```

Nhập tên tùy ý, chọn màu, bấm "Thêm thẻ" → dùng được ngay ở dropdown "Phân loại" của mọi mục Q&A trong KB đó. **Tag do người dùng tự tạo riêng cho từng KB, không có preset chung của tổ chức.**

⚠️ **Điểm gây nhầm:** trạng thái chưa gán hiển thị là **"Chưa phân loại"** trong dropdown chọn, nhưng là **"Untagged"** (tiếng Anh) trong danh sách thẻ và ô giá trị đã chọn — hai chữ khác nhau cho **cùng một trạng thái**.

### 14.3 — Modal "Nhập Q&A" (nhập hàng loạt bằng file)

✅ `[TT]`

```
Nhập Q&A
[   ⇧  Kéo-thả tệp vào đây, hoặc  [Chọn tệp]  [⇣ Tệp mẫu ▾]   ]

Chế độ nhập
[ Thêm vào ]   Thay toàn bộ

Chọn tệp có ít nhất một dòng hợp lệ để nhập.
                                                    [ Hủy ]  [ Nhập ]
```

- Nút **"Tệp mẫu ▾"** tải mẫu trực tiếp từ tool — **3 định dạng: JSON, CSV, XLSX**, cả 3 cùng schema.
- Sau khi chọn file, modal hiện **xem trước** số mục và danh sách câu hỏi sẽ nhập.
- Nút **Nhập** bị khoá tới khi chọn được file hợp lệ.

**Schema file mẫu** ✅ `[TT]` (đọc nguyên văn nội dung cả 3 file mẫu):

| Trường trong file | Tương ứng modal "Thêm Q&A" | Ghi chú |
|---|---|---|
| `standard_question` | Câu hỏi chuẩn | |
| `similar_questions` (mảng) | Câu hỏi tương tự | Trong CSV nối nhiều giá trị bằng `##` |
| `negative_questions` (mảng) | Câu hỏi loại trừ | |
| `answers` (mảng) | Câu trả lời | |
| `tag_name` | Phân loại | |
| `is_enabled` (`TRUE`/`FALSE`) | Toggle **Kích hoạt** | ✅ Xác thực qua test hành vi (14.1.2) |

#### 🚨 "Thay toàn bộ" — XÓA SẠCH dữ liệu cũ, không hoàn tác được

✅ `[NSD]` Test thật: KB "Test B4 gộp" đang có **1 mục**, nhập file **2 mục hoàn toàn khác**, chọn **Thay toàn bộ**.

**Popup xác nhận trước khi chạy:**
```
⚠ Thay toàn bộ mục FAQ?
Thao tác này xoá 1 mục hiện có và nhập 2 mục thay thế.
Không thể hoàn tác.
                                          [ Hủy ]  [ Thay toàn bộ ]
```

**Kết quả:** KB chỉ còn đúng **2 mục** trong file mới. Mục cũ **biến mất hoàn toàn**.

🚨 **Cảnh báo vận hành:** đây là hành động **phá hủy dữ liệu**, tool ghi rõ "Không thể hoàn tác", **không có bước khôi phục**. Trước khi dùng trên KB thật: **bấm "Xuất" để backup dữ liệu hiện có ra file.**

⚠️ **Điểm nhỏ khó hiểu:** dòng tóm tắt sau khi nhập xong hiện *"Tổng 2 · 0 thêm mới · 2 bỏ qua"* — chữ "bỏ qua" gây hiểu lầm vì kết quả thật là 2 mục có trong KB. Nhiều khả năng là text dùng chung cho cả 2 chế độ, chưa viết riêng. **Không ảnh hưởng hành vi thật đã xác nhận ở trên.**

### 14.4 — Công cụ "Kiểm tra tìm kiếm" (chỉ có ở FAQ)

✅ `[TT]` Nút **"Kiểm tra tìm kiếm"** trên toolbar danh sách Q&A mở panel:

```
Kiểm tra tìm kiếm

Câu truy vấn      [ Nhập câu hỏi để thử truy hồi ]
Ngưỡng tương đồng                                          0.5
Số kết quả tối đa                                           10
                    [ 🔍 Tìm ]
```

- **Ngưỡng tương đồng** — thanh trượt 0–1, mặc định **0.5**. Kết quả điểm thấp hơn ngưỡng bị loại khỏi danh sách.
- **Số kết quả tối đa** — mặc định **10**.
- **Kết quả:** số thứ tự · câu hỏi chuẩn khớp · **điểm số** (vd `0.572`, hoặc `1.000` khi khớp nguyên văn) · dòng **"Khớp:"** cho biết đoạn văn bản thật sự dùng để tính điểm. Bấm mũi tên mở rộng xem toàn bộ câu trả lời + mọi biến thể.
- Không có kết quả → **"Không có mục khớp."**

⚠️ **Lưu ý vận hành:** ngưỡng mặc định 0.5 **có thể ẩn mất match yếu nhưng vẫn đúng**. Khi nghi ngờ FAQ "không tìm thấy gì", **hạ ngưỡng về 0** để phân biệt: không có candidate nào, hay có nhưng bị ngưỡng lọc.

✅ `[TT]` **Loại Tài liệu KHÔNG có công cụ này** — đã kiểm kỹ toolbar tab Documents của KB Tài liệu. Đây là tính năng **riêng của FAQ**. Cách gần nhất trên loại Tài liệu là dùng Chat và xem "Nguồn tham khảo" ([mục 15](#15)).

---

## 15 — Chat hỏi đáp trên KB {#15}

✅ `[TT]` Bấm icon 💬 ở đầu trang KB (cạnh ℹ và ⚙) mở khung **Trò chuyện**, tự gắn KB hiện tại làm nguồn tri thức (hiện thành tag, gỡ được bằng dấu ×, thêm KB khác vào cùng phiên chat được).

**Quy trình trả lời hiển thị công khai từng bước** — không phải hộp đen:

```
Nguồn tham khảo (N tài liệu)                         ▸
Hoàn tất N bước                                      ▾
  🔧 Đã gọi Query Understand
  🔍 Đang tìm trong kho tri thức: "…"        ← câu hỏi được viết lại/dịch sang tiếng Anh nội bộ
     Tìm thấy N kết quả
  💭 Suy nghĩ                                 ← khối lý luận trung gian, xem được toàn bộ

[Câu trả lời cuối — có markdown, heading, bullet]
```

- **"Nguồn tham khảo"** khi mở rộng liệt kê **từng tài liệu + số đoạn được dùng** (vd `so-tay-tao-knowledge-base-v2.md — 4 đoạn`, `Codex-101-….pdf — 6 đoạn`), kèm icon mở tài liệu gốc.
- Có ô chọn chế độ trả lời (quan sát được nhãn **"Quick Answer"**) và dropdown chọn **Mô hình** riêng cho phiên chat.
  ❌ Chưa rõ dropdown này mặc định dùng đúng "Mô hình chat/tóm tắt" đã cấu hình cho KB hay độc lập.
- Có nút **"Cuộc trò chuyện mới"** và **"Lịch sử"**.

✅ `[Test]` **Kiểm chứng chất lượng:** hỏi *"Chức năng 'Theo cấu trúc' trong phân đoạn có hoạt động tốt trên PDF thật không?"* trên KB đã nạp chính sổ tay này. Câu trả lời trích **đúng chính xác**: tên file test, số trang, các dấu hiệu đã thử, kết luận "hạn chế/bug thật của engine", dữ liệu bổ sung "79 trang… 68 trang dồn 1 đoạn", và khuyến nghị vận hành. **Không bịa, không lệch nghĩa, giữ đúng cả các đính chính tinh vi.**

---
---

# PHẦN III — VẬN HÀNH

## 16 — Dựng KB FAQ cho LiveOps {#16}

### 16.1 — Quyết định 2 lựa chọn cấu hình trước khi viết nội dung

Xem [mục 7.2](#7) để chọn **Chế độ lập chỉ mục** và **Cách index câu hỏi**.
Nhớ: sau khi nạp dữ liệu, hai thứ này **bị khóa** ([mục 12](#12)).

Nếu chưa chắc: dùng mặc định **Chỉ câu hỏi + Tách**, và viết đủ biến thể câu hỏi theo mẫu dưới — cách viết này tương thích tốt với cả 4 tổ hợp cấu hình.

### 16.2 — Lấy câu hỏi từ đâu (theo độ tin cậy)

1. **Ticket CS 90 ngày gần nhất** → 20 câu đầu thường chiếm phần lớn khối lượng
2. **Chat log của bot/kênh hỗ trợ** → câu bot trả lời sai = mục FAQ đang thiếu
3. **Bình luận fanpage lúc ra patch** → 48 giờ đầu lộ ra điều gì chưa nói rõ
4. **Giữ nguyên cách người chơi viết**, kể cả viết sai chính tả

### 16.3 — Mẫu một mục FAQ (đúng tên trường thật của tool)

🚨 **Đính chính:** bản trước ghi các trường "Nhóm / Tag / Không áp dụng / Người phụ trách / Cập nhật" như thể là trường của tool — **sai**. Modal "Thêm Q&A" thật chỉ có **5 trường** ([mục 14.1](#14)).

```
Câu hỏi chuẩn:
  Nạp thẻ rồi mà không thấy xu trong game thì làm sao?

Câu hỏi tương tự (tối đa 10):
  - nap the ko nhan xu
  - đã trừ tiền nhưng chưa có xu
  - mua gói xu bị lỗi

Câu hỏi loại trừ (tối đa 10 — CHẶN match hoàn toàn, xem mục 14.1.1):
  - nạp thẻ bị trừ tiền hai lần cho một lần mua

Câu trả lời (tối đa 5):
  Giao dịch thường hoàn tất trong 1-2 phút. Nếu quá 5 phút:
  1. Thoát hẳn game, mở lại
  2. Kiểm tra hòm thư trong game
  3. Nếu vẫn chưa có: gửi yêu cầu hỗ trợ kèm ID game, mã giao dịch

Phân loại: thanh-toan
```

**Phần Câu hỏi tương tự quyết định FAQ có dùng được hay không** — nên có 3–5 biến thể lấy từ ticket thật.

**Nếu cấu hình là "Câu hỏi + trả lời"**, nội dung câu trả lời cũng ảnh hưởng match → viết câu trả lời chứa cả những từ khóa người dùng có thể gõ thẳng (mã lỗi, tên chính sách, tên vật phẩm).

⚠️ **Người phụ trách / ngày cập nhật KHÔNG có trường riêng trong tool** (chỉ có "Phân loại"). Muốn theo dõi ai phụ trách, cập nhật khi nào → cần bảng theo dõi riêng ngoài tool ([mục 18](#18)).

### 16.4 — Hai điều đừng kỳ vọng ở FAQ

- **FAQ không xoá được rủi ro trả lời sai** — hệ thống vẫn phải ghép câu hỏi user vào một mục, việc ghép có thể sai.
- **FAQ không tự phủ câu hỏi mới** — ra event mà không thêm FAQ thì hỏi về event sẽ nhận câu trả lời cũ hoặc không có gì.

---

## 17 — KB cho người đọc {#17}

Phần này **không nằm trong tool**. Đây là cách tổ chức tài liệu để người mới tìm được thứ họ cần trong 2 phút — vẫn dùng đúng bộ file đã nạp cho AI.

### Lớp một — Cây phân loại, tối đa hai tầng

```
vanhanh/        Lịch bảo trì, quy trình phát hành, xử lý sự cố
thanhtoan/      Nạp thẻ, hoàn tiền, sai lệch giao dịch
taikhoan/       Đăng nhập, khoá, khôi phục, xác thực
gameplay/       Quy tắc, tính điểm, xử lý gian lận
event/          Từng event: điều kiện, phần thưởng, thời gian
noibo/          Onboarding, phân công, kênh liên hệ
```

Nếu một tài liệu không biết đặt vào folder nào → dấu hiệu nó nói về nhiều chủ đề, **tách nó ra**.

### Lớp hai — File mở đầu cho mỗi nhóm

```markdown
# Thanh toán — bắt đầu từ đâu

Người phụ trách: LiveOps · Studio 9
Rà soát lần cuối: 2026-08-05

## Nếu bạn đang trực ticket, đọc ba file này trước
1. xu-ly-loi-nap-the.md
2. chinh-sach-hoan-tien.md
3. cac-kenh-thanh-toan.md

## Việc thường bị làm sai trong nhóm này
- Hứa thời gian hoàn tiền ngắn hơn thực tế
- Trả lời ca quá 7 ngày như ca thường
```

**Mục "Việc thường bị làm sai"** là mục có giá trị nhất và hầu như không ai viết.

### Lớp ba — Năm quy ước để hai lớp không lệch nhau

| Quy ước | Vì sao |
|---|---|
| Chỉ sửa ở file gốc | Bản sửa ngoài gốc bị mất ở lần đồng bộ tiếp theo |
| Ngày cập nhật ghi **trong** file | Ngày của hệ điều hành thay đổi khi copy/đổi tên/đồng bộ |
| Một chủ đề một file | Đúng cho cả AI ([mục 3](#3), [10](#10)) và người |
| Không dùng chữ chỉ thời gian tương đối | "Hiện tại" vô nghĩa sau 6 tháng |
| Tên file không dấu | Tránh lỗi mã hoá, dễ tìm |

---

## 18 — Duy trì KB {#18}

**KB không có người phụ trách sẽ chết trong khoảng một quý, nhưng nó không báo cho ai — nó chỉ tiếp tục trả lời bằng thông tin của quý trước.**

| Việc | Tần suất | Ai |
|---|---|---|
| Thêm FAQ cho nội dung mới | Mỗi patch/event | LiveOps phụ trách event |
| Kiểm tra bằng câu hỏi thật | Hàng tuần, 10 câu | Người trực ticket |
| Rà soát nội dung theo nhóm | Hàng tháng | Người phụ trách nhóm |
| Dọn tài liệu chết | Hàng quý | Người phụ trách nhóm |
| Soát dữ liệu cá nhân | Hàng quý | Người quản lý KB |

### Khi AI trả lời sai — thứ tự truy nguyên

1. **Xem AI dẫn nguồn từ file nào** (Chat → "Nguồn tham khảo", [mục 15](#15)) — đúng file mà sai nội dung → vấn đề nội dung; sai file → vấn đề bước tìm.
2. **Mở file, đọc đúng đoạn được dẫn** — thường đoạn đó thật sự viết vậy, chỉ là lỗi thời.
3. **Nếu file đúng nhưng lấy sai đoạn** → nghi ngờ Chiến lược phân đoạn ([mục 10](#10)). Mở chi tiết tài liệu → "Xem phân đoạn" để nhìn cách cắt thật, rồi cân nhắc "Phân tích lại với tùy chọn" ([mục 13.5](#13)).
4. **Nếu hai file nói khác nhau về cùng một việc** → giữ một bản, gỡ bản còn lại.
5. **Với FAQ:** dùng "Kiểm tra tìm kiếm" ([mục 14.4](#14)), hạ ngưỡng về 0 để biết mục đó có được tính điểm không. Nếu vẫn 0 → kiểm tra toggle **Kích hoạt** và **Câu hỏi loại trừ**.

### Checklist rút gọn

**Trước khi mở tool:** Dọn Sống/Chết/Không biết · Xử lý mâu thuẫn · Tách file nhiều chủ đề · Xoá dữ liệu cá nhân

**Trong lúc tạo KB (Tài liệu):** Chọn RAG/Wiki · Nếu Wiki, chọn độ chi tiết · Kiểm tra parser (tab Xử lý) · Kiểm tra Chiến lược phân đoạn · Bật VLM nếu tài liệu có ảnh chứa chữ · *(ASR hiện chưa dùng được)*

**Trong lúc tạo KB (FAQ):** Chọn Chế độ lập chỉ mục · Chọn Cách index câu hỏi · **Chốt trước khi nạp — sau đó bị khóa**

**Sau khi tạo:** Hỏi 10 câu từ ticket thật · Thử câu KB không có (kiểm tra AI có bịa) · Kiểm tra "Nguồn tham khảo" có dẫn đúng file · Đưa cho người mới, bấm giờ 2 phút

**Trước mọi thao tác nguy hiểm:** Bấm **Xuất** để backup — đặc biệt trước khi dùng "Thay toàn bộ" ([mục 14.3](#14)) hoặc xóa tài liệu để mở khóa cấu hình ([mục 12](#12))

---
---

# PHẦN IV — PHỤ LỤC

## Phụ lục A — Bảng trạng thái xác thực tổng hợp {#pl-a}

> Bảng này đã **loại bỏ toàn bộ dòng trùng lặp và mâu thuẫn** của bản v2 cũ (v2 từng có 6 cặp dòng nói ngược nhau trong cùng một bảng do cập nhật chồng lớp).

### A.1 — Cấu trúc và luồng cấu hình

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Loại KB chỉ có 2 lựa chọn: Tài liệu / FAQ | ✅ | `[TT]` | [5.2](#5) |
| Modal cấu hình: Tài liệu 5 tab, FAQ 4 tab (gồm Chia sẻ + Nguồn dữ liệu) | ✅ | `[TT]` | [5.2](#5) |
| Trang làm việc có bộ tab riêng: Documents/Wiki/Graph | ✅ | `[TT]` | [13](#13) |
| Loại KB không đổi được sau khi tạo | ✅ | `[TT]` | [6.1](#6) |
| Chế độ Nhanh dùng 1 form chung, chỉ hỏi 4 thứ | ✅ | `[TT]` | [6.1](#6) |
| Nhanh và Nâng cao dùng **chung một bộ mặc định** | ✅ | `[TT]` | [6.3](#6) |
| Banner Nhanh sai dòng "sinh câu hỏi đang bật" (thực tế TẮT) | 🚨 | `[TT]` | [6.2](#6) |
| Giá trị mặc định thật của ô "Cấu hình parser" (Tự động hay Tùy chỉnh) | ⚠️ | `[TT]` | [6.2](#6) |

### A.2 — Tổng quan: RAG/Wiki và Cấu hình FAQ

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| RAG + Wiki là checkbox, tick được cả hai | ✅ | `[TT]` | [7.1](#7) |
| Độ chi tiết Wiki: 3 mức pill, "Số trang cân bằng" là caption không phải ô nhập | ✅ | `[TT]` | [7.1](#7) |
| Wiki trên nguồn sạch giữ chính xác từng số liệu/cụm trích dẫn | ✅ | `[TT]` | [13.4](#13) |
| Wiki trên nguồn có mâu thuẫn — chưa test chiều xấu | ❌ | — | [7.1](#7) |
| FAQ có Chế độ lập chỉ mục + Cách index câu hỏi (không có RAG/Wiki) | ✅ | `[TT]` | [7.2](#7) |
| **"Chỉ câu hỏi" → 0 kết quả tuyệt đối** khi từ khóa chỉ ở câu trả lời (cả ngưỡng 0.0); "Câu hỏi+trả lời" khớp 0.572 | ✅🚨 | `[Test]` | [7.2](#7) |
| Gộp vs Tách: cả hai đều match (Gộp 0.738 / Tách 0.718) — chưa đủ dữ liệu kết luận bên nào tốt hơn | ✅⚠️ | `[Test]` | [7.2](#7) |

### A.3 — Mô hình

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Tài liệu 3 trường model, FAQ 2 trường (không có Tổng hợp Wiki) | ✅ | `[TT]` | [8.1](#8) |
| Doc và FAQ dùng chung pool model cho Chat/tóm tắt + Embedding | ✅ | `[TT]` | [8.1](#8) |
| **Danh sách model Chat/tóm tắt dao động 3↔4** giữa các lần mở (`deepseek-v4-flash` lúc có lúc không) | 🚨 | `[TT]` | [8.2](#8) |
| Chat/tóm tắt và Tổng hợp Wiki luôn đồng bộ với nhau | ✅ | `[TT]` | [8.2](#8) |
| **Pool VLM chỉ 3 model, không bao giờ có `deepseek-v4-flash`** | 🚨 | `[TT]` | [8.2](#8) |
| VLM mặc định TẮT; khi bật hiện trường "Mô hình VLM" | ✅ | `[Ảnh]` | [8.3](#8) |
| ASR mặc định TẮT | ✅ | `[Ảnh]` | [8.4](#8) |
| **ASR chưa có model nào gán → tính năng KHÔNG dùng được** | 🚨 | `[Ảnh]` | [8.4](#8) |
| VLM/ASR không xuất hiện ở FAQ | ✅ | `[TT]` | [8.4](#8) |

### A.4 — Parser

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| 14 nhóm định dạng (tool ghi rõ "14 nhóm định dạng") | ✅ | `[TT]` | [9.3](#9) |
| Cột "engine đang chọn sẵn" của cả 14 nhóm | ✅ | `[TT]` | [9.3](#9) |
| Cột "các engine chọn được" của từng nhóm | ⚠️ | `[Ảnh]` | [9.3](#9) |
| 6 engine tồn tại (Built-in, MinerU, LLM, markitdown, liteparse, Simple) | ✅ | `[Ảnh]` | [9.2](#9) |
| **Nhóm Âm thanh: giá trị hiển thị "Built-in" nhưng danh sách chỉ có "Simple"** | 🚨 | `[TT]` | [9.3](#9) |
| Parser Excel tùy chỉnh: Tự nhận diện / Thủ công | ✅ | `[TT]` | [9.4](#9) |
| Khuôn mẫu "FPA · …" do đâu mà có, tạo thêm được không | ❌ | — | [9.4](#9) |

### A.5 — Phân đoạn

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| 4 chiến lược, mặc định **Tự động** | ✅ | `[TT]` | [10.1](#10) |
| Công cụ "Xem trước phân đoạn": 4 mẫu, thống kê 2 lớp, breadcrumb, ước lượng token | ✅ | `[Ảnh]` | [10.2](#10) |
| "Xem trước phân đoạn" **không đọc được file đã tải lên** | ✅ | `[TT]` | [10.2](#10) |
| "Theo tiêu đề" chỉ nhận cú pháp `#`/`##`, không suy rộng CHAPTER/Q&A | ✅ | `[Ảnh]` | [10.3](#10) |
| **"Theo cấu trúc" thất bại cả trên PDF THẬT** — hạn chế thật của engine | 🚨 | `[NSD]` | [10.3](#10) |
| PDF nghiệp vụ 79 trang (chiến lược Tự động) → 1 đoạn chiếm 68/79 trang | ⚠️ | `[TT]` | [10.3](#10) |
| "Theo độ dài" cắt đúng ngưỡng ký tự tuyệt đối, có thể cắt giữa câu | ✅ | `[Ảnh]` | [10.3](#10) |
| Tự nhận diện ngôn ngữ `vi` chính xác khi để trống Gợi ý ngôn ngữ | ✅ | `[Ảnh]` | [10.3](#10) |
| **Mặc định Cha-con: cha 32.768 / con 8.192 ký tự, chồng lấp 0** | ✅ | `[Ảnh]` | [10.4](#10) |
| Thông thường: 16.384 ký tự, chồng lấp 0 | ✅ | `[Ảnh]` | [10.4](#10) |
| Đơn vị là **ký tự**, không phải từ | ✅ | `[Ảnh]` | [10.4](#10) |
| Chiến lược và chế độ Cha-con/Thông thường là 2 lựa chọn độc lập | ✅ | `[Ảnh]` | [10.4](#10) |
| Hành vi khi văn bản vượt ngưỡng cha (>32.768) | ❌ | — | [10.4](#10) |
| Truy hồi theo ngữ cảnh mặc định BẬT (thấy khối "Ngữ cảnh tìm kiếm (LLM tạo)" trên tài liệu thật) | ✅ | `[TT]` | [10.6](#10) |
| Sinh câu hỏi mặc định TẮT; khi bật hiện "Số câu hỏi mỗi đoạn" (1–10, mặc định 3) | ✅ | `[Ảnh]` | [10.5](#10) |
| Chọn "Theo độ dài" → khoá Giới hạn token + Gợi ý ngôn ngữ | ✅ | `[Ảnh]` | [10.6](#10) |
| Override chunking riêng từng lượt tải ("Xử lý nâng cao") | ✅ | `[TT]` | [10.7](#10) |

### A.6 — Nguồn dữ liệu, Chia sẻ, Khóa cấu hình

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Tab "Nguồn dữ liệu" tồn tại, hỗ trợ **Notion / Google Drive / NAS**, wizard 4 bước | ✅ | `[TT]` | [11.2](#11) |
| Cả 3 nguồn đều cần thiết lập kỹ thuật cấp admin (không phải OAuth cá nhân) | ✅ | `[TT]` | [11.2](#11) |
| Bước 3 (Tài nguyên) và bước 4 (Chiến lược) của wizard | ❌ | — | [11.2](#11) |
| Tab "Chia sẻ" — chia sẻ tới Space, quyền Chỉnh sửa / Chỉ đọc | ✅ | `[TT]` | [11.1](#11) |
| Khóa Loại + Chiến lược lập chỉ mục + Embedding khi KB có nội dung | ✅ | `[TT]` | [12](#12) |
| **Khóa mở lại được bằng cách xóa hết tài liệu** (không vĩnh viễn) | 🚨 | `[TT]` | [12](#12) |
| Mô hình Chat/tóm tắt **KHÔNG** bị khóa | ✅ | `[TT]` | [12](#12) |
| Mô hình Tổng hợp Wiki có bị khóa không | ⚠️ | — | [12](#12) |

### A.7 — Bên trong KB Tài liệu

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Nút tải lên có **4 lựa chọn** | ✅ | `[TT]` | [13.1](#13) |
| **"Nhập từ URL" bấm không phản hồi** — nhiều khả năng chưa hoạt động | 🚨 | `[TT]` | [13.1](#13) |
| "Tải thư mục lên" — tồn tại, chưa test hành vi | ❌ | `[TT]` | [13.1](#13) |
| **"Soạn thảo trực tuyến"** tạo tài liệu `.md` thẳng trên tool, index qua đúng pipeline | ✅ | `[TT]`+`[Test]` | [13.2](#13) |
| "Lưu nháp" — chưa test trạng thái nháp | ❌ | — | [13.2](#13) |
| Quy trình xử lý 5 giai đoạn, tiến độ real-time | ✅ | `[TT]` | [13.3](#13) |
| Ý nghĩa chính xác từng giai đoạn (đặc biệt "Phân tích tài liệu") | ⚠️ | — | [13.3](#13) |
| Wiki: Mục lục + Nhật ký hoạt động + thư mục theo chủ đề + Thực thể | ✅ | `[TT]` | [13.4](#13) |
| Danh mục tài liệu dùng chung modal "Quản lý thẻ" với FAQ | ✅ | `[TT]` | [13.5](#13) |
| Bộ lọc: định dạng / trạng thái / nguồn / ngày; MD và MARKDOWN tách 2 dòng | ✅ | `[TT]` | [13.5](#13) |
| Menu tài liệu 5 mục; **"Phân tích lại" → không cần xóa/tải lại file** | ✅ | `[TT]` | [13.5](#13) |
| **"Ép OCR toàn bộ PDF (scanned)"** — cho PDF có text-layer rác/sai | ✅ | `[TT]` | [13.5](#13) |
| Kết quả thật trước/sau khi bấm "Phân tích lại" | ❌ | — | [13.5](#13) |
| "Sửa nội dung" trên tài liệu MANUAL | ❌ | — | [13.5](#13) |
| Graph: đồ thị tương tác, 5 loại node | ✅ | `[TT]` | [13.6](#13) |
| Node "Tổng hợp" / "So sánh" — chưa thấy ví dụ nào (đều 0) | ❌ | `[TT]` | [13.6](#13) |
| PPTX→PDF 37 slide → 69 phân đoạn (~1,86 đoạn/slide) | ✅ | `[TT]` | [4.5](#4) |

### A.8 — Bên trong KB FAQ

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Modal "Thêm Q&A": 5 trường (Câu hỏi chuẩn* / Tương tự 10 / Loại trừ 10 / Trả lời 5* / Phân loại) | ✅ | `[TT]` | [14.1](#14) |
| **"Câu hỏi loại trừ" chặn match hoàn toàn** (0.707 → 0 tuyệt đối) | ✅🚨 | `[Test]` | [14.1.1](#14) |
| Toggle **Kích hoạt** = `is_enabled`, tắt là loại hẳn khỏi tìm kiếm | ✅ | `[Test]` | [14.1.2](#14) |
| Toggle **Đề xuất** không ảnh hưởng tìm kiếm — mục đích thật chưa rõ | ⚠️ | `[Test]` | [14.1.2](#14) |
| "Phân loại" là tag tự tạo qua "Quản lý thẻ" (7 màu), không phải preset | ✅ | `[TT]` | [14.2](#14) |
| "Chưa phân loại" vs "Untagged" — 2 chữ cho cùng 1 trạng thái | ⚠️ | `[TT]` | [14.2](#14) |
| Modal "Nhập Q&A": JSON/CSV/XLSX cùng schema, có nút "Tệp mẫu" | ✅ | `[TT]` | [14.3](#14) |
| **"Thay toàn bộ" xóa sạch dữ liệu cũ, popup ghi "Không thể hoàn tác"** | ✅🚨 | `[NSD]` | [14.3](#14) |
| Vì sao "Câu trả lời" cho phép tối đa 5 | ❌ | — | [14.1](#14) |
| "Kiểm tra tìm kiếm": ngưỡng mặc định 0.5, tối đa 10 kết quả, có điểm + dòng "Khớp:" | ✅ | `[TT]` | [14.4](#14) |
| **"Kiểm tra tìm kiếm" KHÔNG có ở loại Tài liệu** | ✅ | `[TT]` | [14.4](#14) |

### A.9 — Chat

| Nội dung | Trạng thái | Nguồn | Mục |
|---|---|---|---|
| Chat hiện đủ bước agentic (Query Understand → tìm kho tri thức → Suy nghĩ) | ✅ | `[TT]` | [15](#15) |
| "Nguồn tham khảo" liệt kê từng tài liệu + số đoạn được dùng | ✅ | `[TT]` | [15](#15) |
| Chất lượng trả lời: chính xác đến từng số liệu khi đối chiếu nguồn | ✅ | `[Test]` | [15](#15) |
| Dropdown "Mô hình" trong chat có dùng đúng model đã cấu hình cho KB không | ❌ | — | [15](#15) |

---

## Phụ lục B — Backlog: việc chưa xác thực {#pl-b}

Sắp theo mức độ ảnh hưởng vận hành.

### B.1 — Ưu tiên cao (ảnh hưởng quyết định vận hành)

| # | Việc cần làm | Vì sao quan trọng | Mục |
|---|---|---|---|
| 1 | Test "Theo cấu trúc" trên **1 PDF nghiệp vụ thật** (báo cáo có chương đánh số, xuất từ Word) | Kết luận hiện tại dựa trên PDF dựng bằng reportlab — cần loại trừ khả năng lỗi nằm ở cách tạo file test | [10.3](#10) |
| 2 | **Bước 3–4 wizard Nguồn dữ liệu** (cần Integration Token / service account JSON / tài khoản NAS thật) | Quyết định LiveOps có tự đồng bộ Drive/Notion được không, hay phải nhờ IT | [11.2](#11) |
| 3 | Kết quả thật **trước/sau khi bấm "Phân tích lại"** | Đây là cách duy nhất sửa chunking cho tài liệu đã nạp — cần biết nó thực sự thay đổi gì | [13.5](#13) |
| 4 | Nhóm **Âm thanh**: engine nào thật sự chạy (hiển thị Built-in nhưng danh sách chỉ có Simple) | Mâu thuẫn UI; hiện chưa ảnh hưởng vì ASR chưa dùng được, nhưng cần hỏi đội phát triển | [9.3](#9) |

### B.2 — Ưu tiên trung bình

| # | Việc cần làm | Mục |
|---|---|---|
| 5 | Xác nhận lại **cột "các engine chọn được"** của cả 14 nhóm parser (mở từng dropdown) — dữ liệu này từ ảnh phiên trước | [9.3](#9) |
| 6 | Giá trị mặc định thật của ô "Cấu hình parser" (Tự động vs Tùy chỉnh theo định dạng) | [6.2](#6) |
| 7 | Hành vi thật của **"Tải thư mục lên"** | [13.1](#13) |
| 8 | **"Sửa nội dung"** trên tài liệu nguồn MANUAL — sửa xong có tự index lại không | [13.5](#13) |
| 9 | Trạng thái **"Lưu nháp"** hiển thị thế nào trong danh sách tài liệu | [13.2](#13) |
| 10 | Nút **"Xuất"** xuất ra định dạng gì, có dùng lại để nhập được không (quan trọng cho quy trình backup) | [14.3](#14) |
| 11 | Mục đích thật của toggle **"Đề xuất"** ở FAQ | [14.1.2](#14) |
| 12 | Hành vi khi văn bản **vượt ngưỡng đoạn cha** (>32.768 ký tự) | [10.4](#10) |
| 13 | Mô hình **Tổng hợp Wiki** có bị khóa khi KB có nội dung không | [12](#12) |

### B.3 — Ưu tiên thấp / cần hỏi đội phát triển tool

| # | Việc cần làm | Mục |
|---|---|---|
| 14 | Khuôn mẫu Excel **"FPA · …"** — do tổ chức tạo hay có sẵn; tạo thêm được không *(người dùng yêu cầu gác lại)* | [9.4](#9) |
| 15 | Vì sao trường **"Câu trả lời" cho phép tối đa 5** giá trị | [14.1](#14) |
| 16 | Ý nghĩa chính xác của 5 giai đoạn xử lý, đặc biệt **"Phân tích tài liệu"** và **"Hậu xử lý (2 mục)"** | [13.3](#13) |
| 17 | Node **"Tổng hợp"** / **"So sánh"** trên Graph sinh ra trong điều kiện nào | [13.6](#13) |
| 18 | Dropdown **"Mô hình"** trong khung chat có độc lập với cấu hình KB không | [15](#15) |
| 19 | Test Wiki trên **nguồn cố ý có mâu thuẫn** để thấy chiều xấu của "khuếch đại" | [7.1](#7) |
| 20 | Trường **Ngôn ngữ** trong "Xử lý nâng cao" có nhận `vi` gõ tay không | [10.7](#10) |

---

## Phụ lục C — Nhật ký các phép test đã thực hiện {#pl-c}

Ghi lại để audit có thể **lặp lại chính xác** từng phép test.

### C.1 — Test A/B trên FAQ (bộ dữ liệu: [mau-faq-test-cau-hinh.md](mau-faq-test-cau-hinh.md))

| Test | KB dùng | Biến thay đổi | Câu hỏi test | Kết quả |
|---|---|---|---|---|
| **A** — Chế độ lập chỉ mục | "Test 2 chỉ câu hỏi + tách" vs "Test A2 câu hỏi+trả lời" | Chỉ câu hỏi ↔ Câu hỏi+trả lời | "đổi tên cần bao nhiêu mảnh ngọc" | 0 kết quả (cả ngưỡng 0.0) ↔ **0.572** |
| **A-đối chứng** | "Test 2 chỉ câu hỏi + tách" | — | "Server bảo trì lúc nào?" (nguyên văn) | **1.000** — chứng minh search hoạt động |
| **B** — Cách index câu hỏi | "Test 2 chỉ câu hỏi + tách" vs "Test B4 gộp" | Tách ↔ Gộp | "tài khoản bị đá ra khỏi game liên tục thì làm sao" | **0.718** ↔ **0.738** |
| **C** — Câu hỏi loại trừ | "Test 2 chỉ câu hỏi + tách" | Thêm câu vào ô Loại trừ | "tôi quên mật khẩu nên không đăng nhập được" | **0.707** → **0 tuyệt đối** |
| **D** — Toggle Đề xuất | "Test 2 chỉ câu hỏi + tách" | Tắt toggle trái | Khớp nguyên văn | **0.999** — không đổi |
| **E** — Toggle Kích hoạt | "Test 2 chỉ câu hỏi + tách" | Tắt toggle phải | Khớp nguyên văn | **"Không có mục khớp"** |
| **F** — Thay toàn bộ | "Test B4 gộp" | Nhập file 2 mục, chế độ Thay toàn bộ | — | 1 mục cũ **bị xóa sạch**, còn đúng 2 mục mới |

### C.2 — Test phân đoạn trên loại Tài liệu

| Test | Nguồn | Cấu hình | Kết quả |
|---|---|---|---|
| Theo tiêu đề × 4 mẫu | 4 văn bản mẫu của "Xem trước phân đoạn" | Theo tiêu đề | Chỉ mẫu Markdown tách được (3 đoạn); 3 mẫu còn lại gộp 1 đoạn |
| Theo cấu trúc × 4 mẫu | như trên | Theo cấu trúc | **4/4 đều gộp 1 đoạn**, kể cả mẫu "Chương PDF" |
| Theo cấu trúc × 4 kiểu dấu hiệu | Văn bản dán tay 785 ký tự (`1.`, `2.`, `Chương 3:`, `PHẦN BỐN:`) | Theo cấu trúc | 0 dấu hiệu chương được đếm → **1 đoạn** |
| **Theo cấu trúc × PDF THẬT** | `test-theo-cau-truc.pdf` (4 trang, ngắt trang thật) | Theo cấu trúc, KB "Test PDF cấu trúc" | 🚨 **Tổng 1 phân đoạn** |
| Theo độ dài × văn bản dài | Văn xuôi tiếng Việt 14.746 ký tự | Theo độ dài, Cha-con | **2 đoạn con: 8.192 + 6.554**; nhận diện `vi` đúng |
| Soạn thảo trực tuyến | Văn bản 3 heading `#`/`##` | Mặc định KB | **3 phân đoạn** khớp ranh giới heading |
| PPTX thật | 37 slide xuất PDF, parser MinerU | Mặc định KB | **69 phân đoạn** (~1,86/slide) |
| PDF nghiệp vụ 79 trang | `CFL MMR GMT 2026.04.pdf` | Tự động (KB production) | **2 phân đoạn**, đoạn 1 = 68/79 trang |

### C.3 — Các KB test đã tạo trong quá trình làm tài liệu

| Tên KB | Loại | Cấu hình | Mục đích |
|---|---|---|---|
| Test 2 chỉ câu hỏi + tách | FAQ | Chỉ câu hỏi + Tách | Test A, B, C, D, E |
| Test A2 câu hỏi+trả lời | FAQ | Câu hỏi+trả lời + Tách | Đối chứng Test A |
| Test B4 gộp | FAQ | Chỉ câu hỏi + **Gộp** | Đối chứng Test B, và Test F |
| Test PDF cấu trúc | Tài liệu | Theo cấu trúc | Test "Theo cấu trúc" trên PDF thật |
| Test Doc RAG+Wiki | Tài liệu | **RAG + Wiki**, Tiêu chuẩn | Test Wiki, Graph, Chat, Soạn thảo trực tuyến, quản lý tài liệu |

> ⚠️ **Dọn dẹp:** các KB trên là KB test, nên xóa sau khi audit xong để tránh nhiễu danh sách KB thật.

### C.4 — File dữ liệu test kèm theo (cùng thư mục)

| File | Dùng cho |
|---|---|
| `mau-faq-test-cau-hinh.md` | Bộ 5 mục Q&A + hướng dẫn Test A và Test B |
| `mau-van-ban-theo-cau-truc.txt` | Văn bản 4 kiểu dấu hiệu cấu trúc (dán tay vào Xem trước) |
| `test-theo-cau-truc.pdf` | PDF thật 4 trang để test "Theo cấu trúc" |
| `test-thay-toan-bo.json` | 2 mục Q&A để test chế độ "Thay toàn bộ" |

---

## Phụ lục D — Lịch sử phiên bản {#pl-d}

| Bản | Ngày | Nội dung chính |
|---|---|---|
| **v3.0** | 06/08/2026 | **Tái cấu trúc toàn bộ**: chia 4 phần (Chuẩn bị / Tham chiếu công cụ / Vận hành / Phụ lục), đánh số lại 1–18 + phụ lục A–E. Thêm **hệ thống nhãn nguồn bằng chứng** `[TT]`/`[Test]`/`[NSD]`/`[Ảnh]`. **Sửa 3 lỗi cấu trúc** (mất tiêu đề mục Parser, tiêu đề rỗng ở mục Nguồn dữ liệu, mục lục thiếu). **Gỡ 6 cặp dòng mâu thuẫn** trong bảng trạng thái. **Đính chính mới:** số tab modal cấu hình là 5/4 (không phải 3/2); nhóm Âm thanh hiển thị Built-in dù danh sách chỉ có Simple. |
| v2.7 | 06/08/2026 | Test Chat thật, Danh mục tài liệu, bộ lọc, menu tài liệu ("Phân tích lại"), phát hiện "Ép OCR toàn bộ PDF". Xác nhận "Kiểm tra tìm kiếm" chỉ có ở FAQ. |
| v2.6 | 06/08/2026 | Chuyển sang điều khiển Chrome thật. Phát hiện nút tải lên có **4 lựa chọn**; "Soạn thảo trực tuyến" hoạt động; "Nhập từ URL" không phản hồi; 5 giai đoạn xử lý; tab Graph 5 loại node; PPTX 37 slide → 69 đoạn. |
| v2.5 | 06/08/2026 | Test KB Tài liệu RAG+Wiki thật: cấu trúc Wiki, độ chính xác trang Summary. Phát hiện danh sách model dao động 3↔4. |
| v2.4 | 06/08/2026 | Chốt "Thay toàn bộ" (xóa sạch, không hoàn tác). |
| v2.3 | 06/08/2026 | Chốt "Theo cấu trúc" trên PDF thật → hạn chế thật của engine. Phát hiện "Xử lý nâng cao" khi upload. |
| v2.2 | 06/08/2026 | Xác thực "Câu hỏi loại trừ", "Phân loại", 2 toggle Q&A, tab Nguồn dữ liệu (Drive/Notion/NAS), khóa cấu hình mở lại được, VLM thiếu deepseek. |
| v2.1 | 06/08/2026 | Test A/B FAQ (Chế độ lập chỉ mục, Cách index câu hỏi). Phát hiện 2 modal nhập liệu, "Kiểm tra tìm kiếm". |
| v2 | 06/08/2026 | Viết lại từ kiểm tra trực tiếp qua trình duyệt. Phát hiện Tài liệu và FAQ là 2 luồng cấu hình khác nhau. Số liệu thật cho chunking. |
| v1 | 05/08/2026 | Bản đầu, 13 mục, nhãn Khớp ảnh / Cần kiểm tra. |

---

## Phụ lục E — Nguồn tham khảo ngoài {#pl-e}

- **Moffatt v. Air Canada, 2024 BCCRT 149** — American Bar Association, tháng 2/2024:
  https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/
- **NYC MyCity Chatbot** — The Markup & THE CITY, tháng 3–4/2024:
  https://www.thecity.nyc/2024/04/02/malfunctioning-nyc-ai-chatbot-still-active-false-information/

⚠️ Cả hai vụ chỉ được báo chí theo dõi đến 2024. Nếu trích dẫn trong tài liệu chính thức, **nên kiểm tra lại diễn biến sau thời điểm đó**.

---

*Hết. Mọi sai lệch giữa tài liệu này và tool thật: **tool đúng, tài liệu sai** — vui lòng báo lại để cập nhật.*
