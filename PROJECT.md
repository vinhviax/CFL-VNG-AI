# Knowledge Base VNG — Tổng quan dự án

## Mục tiêu

Project đóng gói tài liệu đã kiểm chứng để tạo, vận hành và bảo trì Knowledge Base cùng Agent trên VNG AI. Root chính thức là:

`J:\My Drive\VNGGames AI\Knowledge Base VNG Source`

Phiên bản nội dung hiện hành là v3.3.0: 13 module Knowledge Base/Google Drive và 7 module Agent chuyên sâu.

**Cập nhật 18/09/2026 (DEC-082):** project đã chuyển sang tài khoản Google Drive mới. `knowledge/` nằm trở lại trong repo (thay thế kiến trúc DEC-076 dùng shortcut sang Drive công ty), nhưng **chỉ phần text/ảnh nhẹ được git theo dõi** — xem `AGENTS.md` mục "Phạm vi git của knowledge/".

## Kiến trúc local và Web

**Tái cấu trúc 15/08/2026 (DEC-043/044):** hai vai trò consumer + asset host đã gộp vật lý cục bộ thành một thư mục. Web KB `GS9 Knowledge VNG - Image Assets` vẫn còn nguyên trạng cho tới khi Phase 3 (Google Drive connector sync) hoàn tất và chat-test đạt.

```text
docs KB/Human/{KB,Agent}-NN-*.md
            │
            ├── strict builder ──> knowledge/GS9 Knowledge VNG AI/doc-NN-*.md
            │                              │                    (cùng thư mục)
            │                              │                    image-NN-*.png
49 PNG ─────┴──> HTML offline tự chứa      │
                                           └── Agent ──> Human
                                      │
                                      └──> 49 URI MinIO trong image-map.json

agent/ + audit Agent ──> knowledge/GS9 CFL Knowledge Agent/doc-NN-*.md
                                      │
                                      └──> Human chọn, hiểu và dùng Agent
```

| Vai trò | Tên chính thức trên Web | ID | Inventory phát hành cuối |
|---|---|---|---|
| KB nền tảng (KB + Agent, kèm ảnh) | `GS9 Knowledge VNG AI` | `cefadf09-4187-46ac-a765-591e3255a4a4` | 20 MD (`doc-00`→`doc-19`) + 49 PNG (`image-01`→`image-49`) = 69, cùng thư mục local |
| Asset host (Web, chưa retire) | `GS9 Knowledge VNG - Image Assets` | `6da8657c-dd96-4170-a698-074043475014` | 49 PNG, 0 MD — không còn thư mục local riêng, Web chưa đổi |
| Agent meta-KB | `GS9 CFL Knowledge Agent` | `1d92448f-7ee2-46c4-b202-5efbe9cc5616` | 28 MD (`doc-00`→`doc-92`, gồm 3 trang cấu trúc KB CFL mới `doc-30`–`doc-32`), 0 binary |

Ba KB cùng tenant `10012`. Prefix `GS9` là bắt buộc theo quy định công ty. Meta-KB Agent là corpus độc lập dành cho Human và không được bind mặc định vào Agent nghiệp vụ.

## Cây thư mục chuẩn

```text
Knowledge Base VNG/
├── docs KB/                           # nguồn nội dung, tách theo ĐỐI TƯỢNG ĐỌC (16/08/2026)
│   ├── Dev/                           # cơ chế, kết quả kiểm chứng — KHÔNG lên Web
│   │   ├── KB-*.md                    # tính năng Knowledge Base
│   │   ├── Agent-*.md                 # tính năng Agent
│   │   └── _QUY-UOC-VIET-FILE-DEV.md
│   └── Human/                         # hướng dẫn người dùng — nguồn build ra knowledge/
│       ├── KB-NN-*.md                 # → doc-NN-*.md trong GS9 Knowledge VNG AI
│       ├── Agent-NN-*.md              # → doc-NN-*.md trong GS9 Knowledge VNG AI
│       └── _QUY-UOC-VIET-FILE-HUMAN.md
├── knowledge/                         # mirror/dữ liệu các KB trên Web
│   ├── GS9 Knowledge VNG AI/          # 20 doc-NN-*.md sinh + 49 image-NN-*.png + image-map.json
│   ├── GS9 CFL Knowledge Agent/       # 28 doc-NN-*.md về 16 Agent + cấu trúc KB CFL
│   ├── GS9 CFL Plan Version/V5/       # 12 doc-v5-NN-*.md + 29 image-v5-NN-*.jpg (cùng thư mục)
│   └── GS9 CFL .../                   # dữ liệu các KB CFL khác
├── agent/                             # config chi tiết từng Agent, cho Dev đọc
├── so-tay-tao-knowledge-base.html     # artifact offline sinh tự động — KHÔNG theo dõi bằng git (DEC-066)
├── scripts/                           # builder
├── tests/                             # test hồi quy
├── samples/                           # dữ liệu mẫu còn dùng
├── audit/                             # bằng chứng, snapshot, backup
├── docs/                              # kế hoạch/spec/report
├── .gitignore                         # chặn credential/cache khỏi Git
├── NEXT_SESSION_PROMPT.md             # prompt chuyển phiên/máy
├── AGENTS.md
├── PROJECT.md
├── STATUS.md
├── HANDOFF.md
└── DECISIONS.md
```

**Tách nội dung theo đối tượng đọc (16/08/2026).** `docs KB/Dev` và `docs KB/Human` là ma trận hai chiều: trục dọc là ai đọc, trục ngang là tính năng nào (tiền tố tên file `KB-`, `Agent-`; thêm tính năng mới thì thêm tiền tố, không tạo thư mục con). Quy tắc phân loại: câu hỏi mà người dùng cuối đặt ra khi đang chat thì thuộc Human; câu hỏi chỉ người sửa hệ thống mới cần thì thuộc Dev. Chi tiết kiểm chứng, mã `DEC-xxx`, link `audit/` không được xuất hiện trong `docs KB/Human`.

Khi build, tiền tố tính năng được đổi thành `doc-` để giữ quy ước đặt tên trên Web (DEC-042) — regex đồng bộ khoá vào `^(doc|image)-`. Master cũ `so-tay-tao-knowledge-base-v3.md` **đã hết vai trò nguồn build** và nằm ở `audit/archive/` từ 17/08/2026 (DEC-066): builder chỉ đọc tới nó khi `docs KB/Human` rỗng, điều không còn xảy ra. Giữ bản lưu trữ vì nhiều tài liệu trong `docs KB/Dev` trích dẫn nó làm nguồn truy nguyên.

`docs human/` (layout cũ, 2 file hướng dẫn rời) đã bị xoá — nội dung thuộc về `docs KB/Human`.

`knowledge-vng/` trước đây là thư mục artifact gộp (layout tiền nhiệm 07/08/2026). `knowledge/GS9 Knowledge VNG - Image Assets/` là layout tiền nhiệm thứ hai (12/08→15/08/2026): asset host tách riêng khỏi consumer. Cả hai layout cũ đã bị thay bằng một thư mục `GS9 Knowledge VNG AI/` gộp module + ảnh (DEC-043); builder/test không còn tạo hoặc phụ thuộc layout cũ nào.

`GS9 CFL Knowledge Agent` nằm ngoài pipeline builder sổ tay. Bộ 28 Markdown được quản lý trực tiếp như mirror của một meta-KB riêng và phải giữ đồng bộ với audit Web/config Agent có ngày.

## Repository và tính di động

- GitHub đích: `https://github.com/vinhviax/CFL-VNG-AI.git`.
- Branch chuẩn: `main`.
- Mục tiêu repository là giữ toàn bộ snapshot project để người dùng cá nhân tiếp tục trên máy khác, không phải public distribution.
- Dataset, audit, binary, HTML và backup được giữ trong Git theo phê duyệt hiện tại vì không file nào đạt `50 MiB`; chưa cần Git LFS.
- Credential/private key/`.env` không thuộc artifact project và luôn bị loại bởi `.gitignore`. Vùng key Item Profile đã nhận diện chỉ được đưa vào Git sau khi credential cũ bị revoke/rotate và file thay thế không còn chứa secret. Shortcut Google Drive `.gsheet` cũng bị loại vì không thể hash/clone; export dữ liệu thật vẫn được track.
- Trạng thái publish có ngày nằm trong `audit/github-publish-2026-08-14.md`, `STATUS.md` và `HANDOFF.md`.

## Hợp đồng artifact

- `docs KB/Human` có đúng 21 file nguồn (`KB-00`→`KB-12`, `Agent-13`→`Agent-19`, `KB-20`); builder đổi tiền tố sang `doc-` khi sinh. Dải `KB-NN` kín 00–12 nên chủ đề KB thêm mới đánh số từ 20 trở đi để không đụng dải `Agent-13`→`Agent-19`.
- `GS9 Knowledge VNG AI` local có 21 Markdown (`doc-00`→`doc-19`, `doc-20`), **52 PNG** (`image-01`→`image-52`) và một map — cùng một thư mục (DEC-043). *(Đếm lại 18/09/2026: 21 md + 52 png + `image-map.json` = 74 file.)*
- Map có **52 key** khớp 52 tên PNG `image-NN-...` và 52 URI `minio://knowledge-base-prd/10012/exports/...` duy nhất (chuyển sang dạng `exports/` từ DEC-078/080). Dạng URI hiện dùng là `file_path` lấy qua MCP `list_documents` (DEC-052); dạng `exports/` cũ vẫn hợp lệ.
- 20 module có 60 link MinIO và 60 `LOCAL_ASSET` dạng `./image-NN-...` (cùng thư mục); HTML không phụ thuộc tài nguyên remote khi đọc.
- Nội dung chỉ sửa tại `docs KB/Human` rồi build; folder `GS9 Knowledge VNG AI` là mirror phát hành, không phải nơi biên tập trực tiếp.
- Tài liệu trong `GS9 Knowledge VNG AI` không được chứa `DEC-xxx`, link `audit/`, hay nhãn mức bằng chứng — test hồi quy kiểm điều này cho 7 module Agent.
- Meta-KB Agent có **8 Markdown** phẳng trên đĩa (đếm 18/09/2026; con số "28" ở bản cũ là sai), gồm 6 trang hướng dẫn chung, 6 hồ sơ default, 10 hồ sơ custom, 3 trang cấu trúc KB CFL (`doc-30`–`doc-32`) và 3 trang governance; không có file ngoài Markdown hoặc folder con.

## Dữ liệu khác trong `knowledge/`

Các folder `GS9 CFL Data Daily`, `GS9 CFL Item Profile`, `GS9 CFL PUM` và `GS9 CFL Sentiment Feedback User` là dữ liệu của những KB khác trên Web.

**Kiểm kê thật 18/09/2026 (đầu phiên 10) — `knowledge/` có 354 file, 2,75 GB, 12 thư mục.** Hai thư mục dưới đây **chưa từng được mô tả trong tài liệu trước đó**:

| Thư mục | Thực tế | Git |
|---|---|---|
| `H5 Promotion/` | 6 file, **1,74 GB** — 3 zip minigame H5 (649 / 570 / 503 MB) + 2 xlsx timeline & item quà | Loại trừ (vượt 100 MB/file) |
| `Kho Tài Liệu Chưa Tích Hợp/` | 181 file, **895 MB** — tài liệu nguồn team gửi, chưa xử lý: `Event/`, `Function/`, `Localize/`, `Membership/`, và `gs9-metric-playbook.docx` | Loại trừ |
| `Keys Drive/` | service-account key của connector | Loại trừ (credential) |
 Không tự động nhập chúng vào `GS9 Knowledge VNG AI` và không dọn nếu chưa xác định dependency.

**Cập nhật cuối phiên 10 (18/09/2026) — thêm 2 thư mục nhẹ, tổng nay 14 thư mục:**
- `gs9-metric-playbook.docx` đã **chuyển ra khỏi** `Kho Tài Liệu Chưa Tích Hợp/` (còn 180 file, 895 MB) sang kho riêng mới `GS9 CFL Metric Playbook/doc-00-metric-playbook.docx` (1 file, 529 KB, **có** git theo dõi).
- `GS9 Dokploy VNG AI/` — kho mới, 6 file Markdown (`doc-00`→`doc-05`), viết tay trực tiếp không qua builder, **có** git theo dõi.
- Cả hai kho mới **chưa lên Web**, chưa trỏ Google Drive connector — xem `HANDOFF.md` mục 4.12/4.13.

**Cập nhật 15/08/2026 (phiên 2):** theo yêu cầu người dùng, tên file trong `GS9 CFL PUM`, `GS9 CFL Data Daily` và `GS9 CFL Sentiment Feedback User` đã thêm tiền tố `doc-` (giữ nguyên phần tên gốc, `desktop.ini` không đổi). Người dùng xác nhận các thư mục này liên kết với Google Drive và chủ động chấp nhận việc đổi tên sẽ khiến Web tự đồng bộ theo.

**Cập nhật 16/08/2026:** `GS9 CFL Item Profile` trước đó đã bị đổi tên bằng gạch dưới (`doc_01_...`), vừa trái DEC-047 vừa sai dấu phân cách nên regex sync `^(doc|image)-` không khớp. Theo chỉ định của người dùng, 7 file `.csv` nay đã đổi sang đúng quy ước `doc-NN-slug`; `doc_CFL ItemID.gsheet` giữ nguyên tên vì là shortcut Drive, không phải artifact nạp lên KB. Thao tác **chỉ đổi tên, không mở và không đọc nội dung** — boundary P0 với dữ liệu người chơi vẫn giữ nguyên.

Dữ liệu private có định danh/hành vi phải giữ phạm vi hẹp, không ghi giá trị cá nhân vào tài liệu bàn giao và không upload sang consumer dùng chung khi chưa có phê duyệt về quyền, retention và tối thiểu hóa dữ liệu.

## Quy hoạch KB nghiệp vụ LiveOps (15/08/2026)

Ba KB ở bảng trên (`Knowledge VNG AI`, `Image Assets`, `CFL Knowledge Agent`) là tầng nền tảng/meta, phục vụ vận hành chính project này. Toàn bộ KB nghiệp vụ CFL khác (`GS9 CFL Plan Version`, `PUM`, `Data Daily`, `Kho Dữ Liệu Tổng Hợp`, v.v.) và ma trận Agent × KB × tool nay theo bản đồ kiến trúc 7 tầng tại `docs/superpowers/specs/2026-08-15-kb-architecture-design.md` — không theo `agent/kb-allowlist-proposal-2026-08-14.md` (giữ làm bằng chứng lịch sử). Đọc tài liệu đó trước khi bind KB mới cho bất kỳ Agent nào.

## Bảo trì

Thay ảnh phải đi theo chuỗi asset host → map → strict build → Markdown → chat-test nguồn/ảnh. Trạng thái live thay đổi theo thời gian nằm trong `STATUS.md`; lý do quyết định bền vững nằm trong `DECISIONS.md`; audit chỉ mở khi cần chứng minh.
