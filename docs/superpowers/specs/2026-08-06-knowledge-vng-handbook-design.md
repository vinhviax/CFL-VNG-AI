# Thiết kế bộ Sổ tay Knowledge Base VNGGames

Ngày chốt thiết kế: 06/08/2026  
Trạng thái: Đã được người dùng duyệt theo toàn bộ phương án mặc định  
Phạm vi: Sổ tay tổng, HTML offline, 10–12 tài liệu Knowledge có ảnh, bộ mẫu và nhật ký kiểm chứng

## 1. Mục tiêu

Bộ đầu ra phải phục vụ đồng thời ba nhu cầu:

1. Một tài liệu nguồn đầy đủ và có thể bảo trì lâu dài.
2. Một trang HTML dễ đọc để giới thiệu Knowledge Base và cách dùng Knowledge VNG cho người mới.
3. Một bộ tài liệu nhỏ, độc lập, tối ưu để nạp vào Knowledge VNG và để con người đọc theo từng chủ đề.

Mọi mô tả hành vi của Knowledge VNG phải dựa trên kiểm thử giao diện thật tại `https://vnggames.ai/kb/knowledge`. Điều chưa thể kiểm thử phải được ghi rõ nguyên nhân và không được trình bày như sự thật đã xác nhận.

## 2. Kiến trúc nguồn nội dung

`so-tay-tao-knowledge-base-v3.md` là nguồn nội dung chuẩn duy nhất.

- File tổng chứa toàn bộ kiến thức, quy trình, cảnh báo, trạng thái xác thực và liên kết đến audit.
- Bộ 12 file nhỏ là bản phân phối theo chủ đề, được trích từ nguồn chuẩn và có phần mở đầu riêng để mỗi file vẫn hiểu được khi đứng độc lập.
- HTML là lớp trình bày dành cho con người, rút gọn và diễn giải từ nguồn chuẩn; không được tự bổ sung tuyên bố kỹ thuật chưa có trong file tổng.
- Nhật ký audit được tách riêng để tài liệu vận hành không bị lẫn chi tiết thử nghiệm.

## 3. Cấu trúc đầu ra

```text
so-tay-tao-knowledge-base-v3.md
so-tay-tao-knowledge-base.html
knowledge-vng/
  00-gioi-thieu-va-quick-start.md
  01-chuan-bi-noi-dung.md
  02-tao-kb-nhanh-va-nang-cao.md
  03-tai-lieu-rag-wiki.md
  04-faq-va-lap-chi-muc.md
  05-mo-hinh-vlm-asr.md
  06-parser-va-xu-ly-file.md
  07-phan-doan-chunking.md
  08-chia-se-va-nguon-du-lieu.md
  09-van-hanh-documents-wiki-graph.md
  10-van-hanh-faq.md
  11-chat-kiem-thu-va-bao-tri.md
  assets/
    ...anh PNG/WebP da cat va che du lieu...
samples/
  faq/
  document/
audit/
  audit-knowledge-vng-2026-08-06.md
```

Tên tài liệu chung: **Sổ tay tạo và vận hành Knowledge Base — VNGGames**. Studio 9 được ghi là đơn vị biên soạn/kiểm chứng, không giới hạn đối tượng đọc chỉ trong Studio 9.

## 4. Quy tắc cho 12 file Knowledge

Mỗi file phải:

- có đúng một tiêu đề cấp 1;
- mở đầu bằng mục “Bạn sẽ biết gì sau khi đọc”;
- giải thích thuật ngữ trước khi dùng;
- có quy trình theo thứ tự thao tác và cảnh báo đặt ngay trước bước nguy hiểm;
- tránh phụ thuộc vào số thứ tự chương của file tổng;
- ghi “Kiểm chứng giao diện: 06/08/2026” với các mục phụ thuộc phiên bản tool;
- có từ khóa tự nhiên, tên nút tiếng Việt đúng như giao diện và biến thể người dùng có thể hỏi;
- không chứa nhật ký thử nghiệm dài, tên KB test hoặc dữ liệu nội bộ không cần thiết;
- dùng liên kết tương đối ổn định tới ảnh trong `assets/` nếu phép kiểm thử xác nhận tool giữ và hiển thị được ảnh.

## 5. Chiến lược hình ảnh

Ảnh là yêu cầu bắt buộc cho cả HTML và bộ file Knowledge.

### 5.1 Mục đích

- giúp người đọc nhận ra đúng màn hình và đúng nút;
- giúp câu trả lời chat của Knowledge VNG có thể hiển thị ảnh minh họa như ví dụ người dùng cung cấp;
- giảm mô tả dài cho các cấu hình nhiều trường.

### 5.2 Tiêu chuẩn ảnh

- chỉ chụp vùng giao diện cần thiết;
- che tên người dùng, tenant, token, dữ liệu nguồn và thông tin nội bộ không cần thiết;
- ưu tiên PNG cho ảnh giao diện và WebP khi cần giảm dung lượng;
- tên file dùng chữ thường, không dấu, có tiền tố theo module;
- mỗi ảnh có alt text mô tả ý nghĩa, không dùng alt text chung chung như “ảnh 1”;
- ngay trước hoặc sau ảnh phải có câu giải thích để câu trả lời vẫn hữu ích nếu ảnh không được render.

### 5.3 Phép kiểm thử bắt buộc

Trước khi chốt cách đóng gói, phải thử trên KB test:

1. Markdown tham chiếu ảnh tương đối và tải cả thư mục MD + ảnh.
2. Markdown tham chiếu một URL HTTPS ổn định nếu cách 1 không hoạt động.
3. Ảnh nhúng trong tài liệu nguồn mà tool chắc chắn hỗ trợ, dùng làm phương án dự phòng nếu Markdown không truyền được ảnh vào câu trả lời.
4. Hỏi câu có chủ đích để xác nhận ảnh xuất hiện trong câu trả lời chat, không chỉ xuất hiện ở phần xem tài liệu.

Chỉ phương án vượt qua đủ chuỗi **nguồn → lập chỉ mục → chat → ảnh hiển thị** mới được dùng làm chuẩn. Nếu tool không hỗ trợ ảnh từ Markdown, bộ MD vẫn giữ ảnh để con người đọc và đi kèm định dạng bổ sung đã kiểm thử để Knowledge VNG trả ảnh.

## 6. HTML offline

`so-tay-tao-knowledge-base.html` phải là một file duy nhất:

- không Google Fonts, CDN, framework hoặc tài nguyên mạng;
- CSS, JavaScript và ảnh đều nhúng trong file;
- có mục giới thiệu, quick start, bản đồ chọn Document/FAQ, quy trình tạo và vận hành, cảnh báo, mục tra cứu và phần “đã kiểm chứng/chưa kiểm chứng”;
- responsive cho màn hình desktop và điện thoại;
- có tìm kiếm nội dung, điều hướng theo mục và nút in;
- không yêu cầu server cục bộ để mở.

## 7. Audit và mức độ bằng chứng

Mỗi kết luận được phân loại:

- **Đã kiểm chứng:** quan sát hoặc thao tác thành công trên giao diện thật.
- **Đã kiểm chứng có điều kiện:** hành vi phụ thuộc model, quyền, dữ liệu hoặc cấu hình cụ thể.
- **Mâu thuẫn giao diện:** nhãn/cảnh báo nói một điều nhưng hành vi thực tế khác.
- **Bị chặn:** không thể hoàn tất do credential, quyền, file picker hoặc dữ liệu mẫu chưa đủ.
- **Suy luận:** chỉ dùng trong audit, không đưa thành hướng dẫn chắc chắn.

Audit riêng phải ghi ngày, KB test, hành động, kết quả quan sát, tác động dữ liệu và trạng thái phục hồi.

## 8. Phạm vi tác động trên hệ thống

- Chỉ thử thao tác ghi trên KB có tên rõ ràng là KB test.
- Không đưa bộ tài liệu cuối vào KB vận hành chính thức trong giai đoạn này.
- Không xóa KB test có sẵn.
- Dữ liệu do quá trình audit tạo mới chỉ được xóa sau khi đã sao lưu và xác minh; không đụng tới dữ liệu có sẵn nếu không cần thiết.
- Với thao tác phá hủy như “Thay toàn bộ”, phải Xuất backup trước và chỉ thực hiện trong KB test chuyên biệt.

## 9. Tiêu chí hoàn tất

Công việc chỉ hoàn tất khi:

1. Mọi tuyên bố liên quan tool trong file tổng có trạng thái bằng chứng.
2. Các mâu thuẫn đã quan sát được sửa trong nội dung chính.
3. File tổng không còn tham chiếu sai phiên bản, tiêu đề hoặc file v2.
4. HTML mở offline, không phát sinh request mạng và không có liên kết điều hướng hỏng.
5. Có đúng 10–12 file Knowledge độc lập, liên kết ảnh hợp lệ và không trùng lặp mâu thuẫn.
6. Có bộ mẫu FAQ/Document đã được tool nhận diện.
7. Ít nhất một đường đi ảnh đã được kiểm thử đến câu trả lời chat; nếu không khả thi, giới hạn được ghi rõ cùng phương án dự phòng đã kiểm thử.
8. Kiểm tra tự động xác nhận heading, liên kết tương đối, asset tồn tại, tài nguyên HTML offline và các cụm từ lỗi thời đã được loại bỏ.

