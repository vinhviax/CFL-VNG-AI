# Knowledge Base VNG — Tổng quan dự án

## Mục tiêu

Project đóng gói tài liệu đã kiểm chứng để tạo, vận hành và bảo trì Knowledge Base cùng Agent trên VNG AI. Root chính thức là:

`J:\My Drive\CFL\VNG AI\Knowledge Base VNG`

Phiên bản nội dung hiện hành là v3.3.0: 13 module Knowledge Base/Google Drive và 7 module Agent chuyên sâu.

## Kiến trúc local và Web

```text
so-tay-tao-knowledge-base-v3.md
            │
            ├── strict builder ──> knowledge/GS9 Knowledge VNG AI/*.md
            │                              │
            │                              └── Agent ──> Human
            │
49 PNG ─────┼──> HTML offline tự chứa
            │
            └──> knowledge/GS9 Knowledge VNG - Image Assets/*.png
                                      │
                                      └──> 49 URI MinIO trong image-map.json

agent/ + audit Agent ──> knowledge/GS9 CFL Knowledge Agent/*.md
                                      │
                                      └──> Human chọn, hiểu và dùng Agent
```

| Vai trò | Tên chính thức trên Web | ID | Inventory phát hành cuối |
|---|---|---|---|
| Consumer | `GS9 Knowledge VNG AI` | `cefadf09-4187-46ac-a765-591e3255a4a4` | 20 MD, 0 PNG |
| Asset host | `GS9 Knowledge VNG - Image Assets` | `6da8657c-dd96-4170-a698-074043475014` | 49 PNG, 0 MD |
| Agent meta-KB | `GS9 CFL Knowledge Agent` | `1d92448f-7ee2-46c4-b202-5efbe9cc5616` | 25 MD, 0 binary |

Ba KB cùng tenant `10012`. Prefix `GS9` là bắt buộc theo quy định công ty. Consumer và asset host giữ pipeline sổ tay/ảnh hiện hành; meta-KB Agent là corpus độc lập dành cho Human và không được bind mặc định vào Agent nghiệp vụ.

## Cây thư mục chuẩn

```text
Knowledge Base VNG/
├── knowledge/                         # mirror/dữ liệu các KB trên Web
│   ├── GS9 Knowledge VNG AI/          # 20 MD sinh + image-map.json
│   ├── GS9 Knowledge VNG - Image Assets/ # 49 PNG
│   ├── GS9 CFL Knowledge Agent/       # 25 MD Human-facing về 16 Agent
│   └── GS9 CFL .../                   # dữ liệu các KB CFL khác
├── agent/                             # thông tin Agent sẽ tạo trên Web
├── so-tay-tao-knowledge-base-v3.md    # master nghiệp vụ
├── so-tay-tao-knowledge-base.html     # artifact offline sinh tự động
├── scripts/                           # builder
├── tests/                             # test hồi quy
├── samples/                           # dữ liệu mẫu còn dùng
├── audit/                             # bằng chứng, snapshot, backup
├── docs/                              # kế hoạch/spec/report
├── docs human/                        # hướng dẫn dành cho người dùng
├── .gitignore                         # chặn credential/cache khỏi Git
├── NEXT_SESSION_PROMPT.md             # prompt chuyển phiên/máy
├── AGENTS.md
├── PROJECT.md
├── STATUS.md
├── HANDOFF.md
└── DECISIONS.md
```

`knowledge-vng/` trước đây là thư mục artifact gộp, chứa 20 Markdown, `image-map.json` và `assets/` với 49 PNG. Layout đó đã được thay bằng hai folder mang đúng tên KB Web; builder/test không còn tạo hoặc phụ thuộc `knowledge-vng/`.

`GS9 CFL Knowledge Agent` nằm ngoài pipeline builder sổ tay. Bộ 25 Markdown được quản lý trực tiếp như mirror của một meta-KB riêng và phải giữ đồng bộ với audit Web/config Agent có ngày.

## Repository và tính di động

- GitHub đích: `https://github.com/vinhviax/CFL-VNG-AI.git`.
- Branch chuẩn: `main`.
- Mục tiêu repository là giữ toàn bộ snapshot project để người dùng cá nhân tiếp tục trên máy khác, không phải public distribution.
- Dataset, audit, binary, HTML và backup được giữ trong Git theo phê duyệt hiện tại vì không file nào đạt `50 MiB`; chưa cần Git LFS.
- Credential/private key/`.env` không thuộc artifact project và luôn bị loại bởi `.gitignore`. Vùng key Item Profile đã nhận diện chỉ được đưa vào Git sau khi credential cũ bị revoke/rotate và file thay thế không còn chứa secret. Shortcut Google Drive `.gsheet` cũng bị loại vì không thể hash/clone; export dữ liệu thật vẫn được track.
- Trạng thái publish có ngày nằm trong `audit/github-publish-2026-08-14.md`, `STATUS.md` và `HANDOFF.md`.

## Hợp đồng artifact

- Master có đúng 20 cặp marker `MODULE`.
- Consumer local có 20 Markdown và một map; không có PNG.
- Asset host local có 49 PNG thật với signature PNG hợp lệ; không có Markdown.
- Map có 49 key khớp 49 tên PNG và 49 URI `minio://knowledge-base-prd/10012/exports/*.png` duy nhất.
- 20 module có 60 link MinIO và 60 `LOCAL_ASSET`; HTML không phụ thuộc tài nguyên remote khi đọc.
- Nội dung chỉ sửa tại master rồi build; folder consumer là mirror phát hành, không phải nơi biên tập trực tiếp.
- Meta-KB Agent có đúng 25 Markdown phẳng, gồm 6 trang hướng dẫn chung, 6 hồ sơ default, 10 hồ sơ custom và 3 trang governance; không có file ngoài Markdown hoặc folder con.

## Dữ liệu khác trong `knowledge/`

Các folder `GS9 CFL Data Daily`, `GS9 CFL Item Profile`, `GS9 CFL PUM` và `GS9 CFL Sentiment Feedback User` là dữ liệu của những KB khác trên Web. Không tự động nhập chúng vào `GS9 Knowledge VNG AI`, không đổi tên và không dọn nếu chưa xác định dependency.

Dữ liệu private có định danh/hành vi phải giữ phạm vi hẹp, không ghi giá trị cá nhân vào tài liệu bàn giao và không upload sang consumer dùng chung khi chưa có phê duyệt về quyền, retention và tối thiểu hóa dữ liệu.

## Bảo trì

Thay ảnh phải đi theo chuỗi asset host → map → strict build → Markdown → chat-test nguồn/ảnh. Trạng thái live thay đổi theo thời gian nằm trong `STATUS.md`; lý do quyết định bền vững nằm trong `DECISIONS.md`; audit chỉ mở khi cần chứng minh.
