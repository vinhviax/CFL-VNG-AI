# Handoff — Knowledge Base VNG

**Cập nhật:** 14/08/2026  
**Trạng thái:** Đã chuẩn hóa workspace và đường dẫn builder; rollout v3.3.0 vẫn đóng; 10 custom Agent đã có basic tool theo vai trò; meta-KB `GS9 CFL Knowledge Agent` đã phát hành 25/25 Markdown và chat-test đạt; GitHub handoff đã publish lên `main`, không có mutation live đang chạy.

## Điểm vào phiên tiếp theo

Root duy nhất:

`J:\My Drive\CFL\VNG AI\Knowledge Base VNG`

Đọc theo thứ tự: `AGENTS.md` → `HANDOFF.md` → `STATUS.md` → `PROJECT.md` → `DECISIONS.md`. Chỉ mở audit liên quan khi cần bằng chứng.

## Tiếp tục từ GitHub trên máy khác

Repository: `https://github.com/vinhviax/CFL-VNG-AI.git`  
Branch: `main`

Clone mới:

```powershell
git clone https://github.com/vinhviax/CFL-VNG-AI.git
Set-Location .\CFL-VNG-AI
git status --short --branch
```

Nếu đã clone:

```powershell
git pull --ff-only origin main
git status --short --branch
```

Sau đó dùng nguyên prompt trong `NEXT_SESSION_PROMPT.md`. Root trên máy mới là kết quả `git rev-parse --show-toplevel`, không giả định còn ổ `J:`.

Snapshot Git đầu tiên: `1502d798debe46674cb5271fc92bd0c6240f2452`. Sau lần push đầu, local HEAD và `origin/main` khớp chính xác, upstream là `origin/main` và working tree sạch. Commit handoff cuối chỉ cập nhật tài liệu tiến độ/audit; trên máy mới luôn lấy trạng thái chuẩn bằng `git pull --ff-only origin main`.

## Cấu trúc cần giữ

| Khu vực | Vai trò |
|---|---|
| `knowledge/` | Mirror/dữ liệu của các KB đang quản lý trên Web |
| `knowledge/GS9 Knowledge VNG AI/` | 20 Markdown sinh + `image-map.json`; không PNG |
| `knowledge/GS9 Knowledge VNG - Image Assets/` | 49 PNG; không Markdown |
| `knowledge/GS9 CFL Knowledge Agent/` | 25 Markdown Human-facing về 6 default + 10 custom Agent; không binary/folder con |
| `agent/` | Artifact audit read-only của 6 Agent mặc định và catalog/config/test/handoff quản trị của 10 custom Agent LiveOps |

Ba tên `GS9 ...` là tên chính thức trên Web theo quy định công ty; không đổi lại tên cũ.

`knowledge-vng/` là layout gộp cũ, không phải file. Trước đây nó chứa 20 module, map và folder 49 ảnh. Builder/test hiện không còn phụ thuộc hoặc tái tạo layout đó.

## Trạng thái core

- Master: `so-tay-tao-knowledge-base-v3.md`, v3.3.0, 20 marker module.
- Consumer: 20 MD + map 49 URI duy nhất.
- Asset host: 49 PNG thật.
- Module: 60 MinIO + 60 `LOCAL_ASSET` trỏ sang `../GS9 Knowledge VNG - Image Assets/`.
- HTML offline tự chứa đã sinh lại.
- Verification mới nhất: strict build PASS; `Ran 16 tests`; `OK`.
- Đối chiếu vòng phục hồi: 20/20 module khớp backup sau quy đổi path. Sau đó ba module `01`, `09`, `11` được sửa có chủ đích để dùng 20 MD/49 PNG và layout/tên `GS9`; chưa upload live.
- Custom Agent: 10/10 đã tạo; list count `18/12/6/0` theo thứ tự Tất cả/Của tôi/Mặc định/shared-with-me. Tất cả no-KB, sharing `0`, image/audio Off và chưa chat/runtime test.
- Web actual chung là `hosted_vllm/qwen3.6-35b`, temperature `0.7`, Thinking Off, reranker trống. Planned baseline/System Prompt local được giữ nguyên nhưng Web actual là nguồn chuẩn cho trạng thái đang lưu.
- Tool actual: bảy Smart Agent dùng Ask + Think + Todo; Player Voice dùng Ask + Think; GM dùng Ask + Todo; CS Copilot giữ Fast Answer và không có Tools tab. Chín Smart Agent có `20` loop, timeout `120s`, parallel Off.
- Agent meta-KB: ID `1d92448f-7ee2-46c4-b202-5efbe9cc5616`, tenant `10012`, 25/25 Markdown Hoàn tất, sharing 0, model `hosted_vllm/qwen3.6-35b`, embedding `text-embedding-3-large`. Chat test đã trả lời đúng Agent/tool/Human gate và mở được nguồn hồ sơ tương ứng.

## Lệnh chuẩn

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

Không dùng `--allow-missing-minio` cho bản bàn giao.

## Lưu ý an toàn

- Nội dung nghiệp vụ chỉ sửa ở master; không sửa trực tiếp module/HTML.
- Không xóa asset KB hoặc PNG còn được Markdown tham chiếu.
- Không mutation live, upload dữ liệu private, gửi chia sẻ hoặc xóa Agent/KB nếu chưa được giao rõ ràng.
- Không bind KB nghiệp vụ cho 10 custom Agent trước audit nội dung/quyền; không publish/share hoặc chạy gold-set Agent nếu chưa có chỉ định mới. Chat test đã thực hiện chỉ trên meta-KB bằng prompt tổng hợp vô hại.
- Có credential hiện hữu trong vùng dữ liệu một KB CFL khác; chưa được dọn vì chưa xác định dependency. Không đọc, sao chép hoặc đưa credential đó vào audit.
- Git handoff publish toàn bộ project theo phê duyệt người dùng nhưng `.gitignore` loại credential/private key/`.env`. Không dùng `git add -f`, không public fork/mirror và không đưa file key đã nhận diện vào lịch sử Git.
- `Test Doc RAG+Wiki` cũ đã bị xóa; test Documents/Wiki/Graph mới cần KB test được phép.

## Bằng chứng mới nhất

- `audit/default-agent-readonly-audit-2026-08-14.md`
- `agent/README.md` và sáu file `agent/*-config.md` — cấu hình UI-visible của 6 Agent mặc định, chỉ-đọc
- `audit/liveops-custom-agent-creation-2026-08-14.md`
- `audit/liveops-custom-agent-multitool-and-agent-kb-2026-08-14.md`
- `agent/liveops-custom-agent-catalog.md` và 10 folder `agent/GS9 .../` — planned baseline cùng Web actual/ID/handoff của custom Agent
- `knowledge/GS9 CFL Knowledge Agent/` — 25 Markdown đã review độc lập và upload live
- `audit/workspace-normalization-2026-08-14.md`
- `audit/workspace-normalization-prebuild-2026-08-14.zip`
- `audit/workspace-docs-before-normalization-2026-08-14.zip`
- `audit/final-live-inventory-2026-08-12.json`
- `audit/agent-deep-test-2026-08-11.md`
- `docs/superpowers/reports/2026-08-12-agent-v3.3-rollout.md`
- `audit/github-publish-2026-08-14.md`
- `NEXT_SESSION_PROMPT.md`

## Việc tiếp theo chỉ khi được giao

- Audit các KB nghiệp vụ ứng viên rồi trình allowlist/quyền cho từng Agent; không tự bind KB CFL khác hoặc `Data Private Weapon`.
- Chỉ chạy gold-set/runtime Agent, publish/share hoặc thay đổi cấu hình Web khi có chỉ định mới; mọi action gửi tin/live mutation vẫn cần Human approval.
- Khi Agent Web actual thay đổi, cập nhật đồng thời `agent/`, meta-KB local, upload Web và audit; không coi meta-KB là corpus nghiệp vụ của Agent.
- Tiếp tục backlog connector/retrieval/ASR trong `STATUS.md` khi có quyền và fixture test.
- Rà soát credential theo quy trình thay thế/rotation trước khi di chuyển hoặc xóa.
