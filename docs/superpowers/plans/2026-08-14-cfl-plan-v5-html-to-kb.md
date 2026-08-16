# CFL Plan Version 5 HTML-to-KB Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển toàn bộ nội dung có ý nghĩa trong `CFL5_0- Plan Ver 5.0-14082026.html` thành một bộ Knowledge Base Markdown có truy nguyên, ảnh tách riêng và kiểm chứng độ phủ tại `knowledge/GS9 Plan Version/V5`.

**Architecture:** Một bộ chuyển đổi Python đọc DOM tĩnh bằng BeautifulSoup, đối chiếu hợp đồng nguồn đã kiểm kê, ánh xạ từng section sang một tài liệu Markdown, giải mã ảnh data-URI sang JPEG và sinh manifest JSON. Bộ kiểm thử độc lập xác nhận số lượng, nội dung, liên kết, checksum và tính lặp lại trước khi bàn giao.

**Tech Stack:** Python 3.11, BeautifulSoup 4, Markdown, JSON, `unittest`.

## Global Constraints

- Chỉ đọc file HTML nguồn; không sửa hoặc di chuyển nguồn.
- Chỉ ghi vào script/test/plan/audit liên quan và `knowledge/GS9 Plan Version/V5`.
- Giữ nguyên câu chữ, số liệu, thuật ngữ và các bản ghi lặp của nguồn; không tự suy diễn hoặc “sửa” nội dung.
- Ghi rõ phần nào là placeholder hoặc thiếu mô tả thay vì tự bổ sung.
- Không truy cập Web VNG AI, không upload/publish/gán KB.
- Không đọc hoặc đưa credential, dữ liệu private, hay dữ liệu ngoài phạm vi vào đầu ra.

---

## Task 1: Khóa hợp đồng nguồn bằng kiểm thử thất bại

**Files:**

- Create: `tests/test_convert_cfl_plan_html.py`
- Test: `tests/test_convert_cfl_plan_html.py`

- [x] Viết fixture gọi bộ chuyển đổi trên bản sao tạm và xác nhận SHA-256 nguồn.
- [x] Khóa các số đã kiểm kê: 9 section, 29 group, 115 item, 14 figure, 29 ảnh, 2 placeholder.
- [x] Khóa hợp đồng đầu ra: 12 Markdown, 29 JPEG, 1 manifest JSON, đúng một H1 mỗi Markdown.
- [x] Kiểm tra mọi title/description/intro/key point/caption có mặt trong module tương ứng.
- [x] Kiểm tra ảnh có JPEG magic, checksum/byte count đúng manifest và mọi liên kết tương đối tồn tại.
- [x] Kiểm tra chạy lại cho kết quả byte-for-byte giống nhau.
- [x] Chạy test và ghi nhận RED vì script chưa tồn tại.

## Task 2: Xây bộ chuyển đổi xác định và có truy nguyên

**Files:**

- Create: `scripts/convert_cfl_plan_html.py`
- Modify: `tests/test_convert_cfl_plan_html.py`

- [x] Parse HTML UTF-8 và từ chối nguồn sai checksum/cấu trúc.
- [x] Trích overview, timeline, section intro, key point, group description, item title/description, figure caption và footer note.
- [x] Giải mã 29 ảnh data-URI sang `assets/` với tên thứ tự ổn định và slug dễ đọc.
- [x] Sinh 12 module Markdown theo section, có metadata nguồn và đường dẫn ảnh cục bộ.
- [x] Sinh `source-manifest.json` với checksum nguồn, keyed record, ánh xạ module/ảnh và bộ đếm độ phủ.
- [x] Không thêm timestamp biến động; dùng metadata xác định từ nguồn để bảo đảm idempotence.
- [x] Chạy test đến GREEN.

## Task 3: Sinh bộ Knowledge Base V5

**Files:**

- Create: `knowledge/GS9 Plan Version/V5/00-index-va-pham-vi.md`
- Create: `knowledge/GS9 Plan Version/V5/01-tong-quan-phien-ban.md`
- Create: `knowledge/GS9 Plan Version/V5/02-lich-trinh-phien-ban.md`
- Create: `knowledge/GS9 Plan Version/V5/03-cach-choi-moi.md`
- Create: `knowledge/GS9 Plan Version/V5/04-he-thong-moi.md`
- Create: `knowledge/GS9 Plan Version/V5/05-nang-cao-chat-luong.md`
- Create: `knowledge/GS9 Plan Version/V5/06-tiep-te-moi.md`
- Create: `knowledge/GS9 Plan Version/V5/07-hoat-dong-tang-do-hoat-dong.md`
- Create: `knowledge/GS9 Plan Version/V5/08-hoat-dong-thuong-mai-hoa.md`
- Create: `knowledge/GS9 Plan Version/V5/09-ban-dia-hoa-va-phat-hanh.md`
- Create: `knowledge/GS9 Plan Version/V5/10-danh-muc-hinh-anh.md`
- Create: `knowledge/GS9 Plan Version/V5/11-ghi-chu-va-truy-nguyen.md`
- Create: `knowledge/GS9 Plan Version/V5/source-manifest.json`
- Create: `knowledge/GS9 Plan Version/V5/assets/*.jpg`

- [x] Chạy bộ chuyển đổi trên file nguồn thật.
- [x] Xác nhận không có file thừa hoặc đầu ra ngoài destination.
- [x] Soát ngẫu nhiên các phần có số liệu/ràng buộc quan trọng và bản ghi trùng.
- [x] Xác nhận placeholder lịch trình và hình chưa có được ghi rõ là thiếu từ nguồn.

## Task 4: Audit và cập nhật tiến độ dự án

**Files:**

- Create: `audit/cfl-plan-v5-html-to-kb-2026-08-14.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`

- [x] Ghi nguồn, checksum, phạm vi, cấu trúc đầu ra và kết quả kiểm thử vào audit.
- [x] Ghi rõ đây là local KB, chưa upload/publish/bind trên Web.
- [x] Cập nhật STATUS và HANDOFF với đường dẫn, bộ đếm và lệnh tái tạo/xác minh.

## Task 5: Verification cuối

- [x] Chạy test chuyên biệt cho converter.
- [x] Chạy toàn bộ test suite của project.
- [x] Chạy kiểm tra liên kết Markdown/asset và secret-pattern trên phạm vi đầu ra mới.
- [x] Kiểm tra `git diff --check` và xem danh sách file thay đổi.
- [x] Chỉ tuyên bố hoàn tất khi mọi kiểm tra bắt buộc đều PASS.
