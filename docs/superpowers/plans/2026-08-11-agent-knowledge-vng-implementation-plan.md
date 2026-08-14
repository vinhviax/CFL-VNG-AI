# Kế hoạch triển khai tài liệu Agent Knowledge VNG

> **Dành cho agent thực thi:** BẮT BUỘC dùng kỹ năng `executing-plans` để thực hiện tuần tự từng task và dừng tại các gate an toàn. Đánh dấu checkbox ngay sau khi có bằng chứng.

**Mục tiêu:** Kiểm thử có kiểm soát toàn bộ bề mặt Agent đang khả dụng, bổ sung module Markdown thứ 14 vào `Knowledge VNG AI`, bổ sung chín ảnh PNG thật vào `Knowledge VNG - Image Assets`, rồi xác minh Agent truy hồi đúng nội dung/nguồn/ảnh.

**Kiến trúc:** Giữ nguyên một master duy nhất (`so-tay-tao-knowledge-base-v3.md`) và pipeline hai KB hiện hành. Ảnh UI Agent được lưu local, upload vào KB asset, ánh xạ thành URI MinIO, rồi builder sinh module `13-tao-va-van-hanh-agent.md` và HTML offline. Consumer chỉ nhận module Markdown mới; Agent test chỉ dùng consumer làm nguồn tri thức.

**Công nghệ:** Markdown, JSON, Python `unittest`, `scripts/build_handbook.py`, PowerShell, Chrome đã đăng nhập và Knowledge VNG UI.

**Đặc tả:** `docs/superpowers/specs/2026-08-11-agent-knowledge-vng-design.md`.

## Ràng buộc toàn cục

- Chỉ sửa nội dung nghiệp vụ tại `so-tay-tao-knowledge-base-v3.md`; không sửa trực tiếp module hoặc HTML sinh tự động.
- Chỉ mutation Agent test `Kiểm thử Agent Knowledge VNG 2026-08-11`, bản sao của nó, hai KB được chỉ định và các chat/feedback do lượt test tạo ra.
- Không sửa, tắt, nhân bản hoặc xóa sáu Agent mặc định.
- Không xóa Agent, tài liệu, ảnh hoặc KB trong kế hoạch này. Chỉ dùng **Thêm vào**, không dùng **Thay toàn bộ**.
- Agent test chỉ liên kết `Knowledge VNG AI`; không dùng `Knowledge VNG - Image Assets` làm nguồn hỏi đáp.
- Không upload PNG vào consumer và không upload Markdown vào asset KB.
- Không đưa credential, token, dữ liệu cá nhân hoặc khóa bí mật vào ảnh, audit hay prompt.
- Nếu nút **Tắt** không cho thấy đường bật lại chắc chắn, dừng trước mutation và ghi `Chưa kiểm chứng`.
- Nếu upload ảnh, strict build, xử lý module hoặc chat test chưa đạt gate tương ứng, không đi tiếp sang bước phụ thuộc.
- Không dùng `--allow-missing-minio` cho artifact bàn giao.
- Workspace không phải Git repository; không khởi tạo Git. Snapshot, audit và output kiểm thử là checkpoint phục hồi.
- Mọi sửa file văn bản dùng `apply_patch`; ảnh nhị phân được lưu từ API chụp màn hình của trình duyệt.

---

### Task 1: Chốt baseline và checkpoint trước mutation

**Files:**
- Read: `HANDOFF.md`
- Read: `STATUS.md`
- Read: `PROJECT.md`
- Read: `DECISIONS.md`
- Read: `so-tay-tao-knowledge-base-v3.md`
- Read: `knowledge-vng/image-map.json`
- Create: `audit/image-map-before-agent-extension-2026-08-11.json`
- Create: `audit/agent-live-test-2026-08-11.md`
- Modify: `docs/superpowers/specs/2026-08-11-agent-knowledge-vng-design.md`

**Gate:** Baseline local và live khớp handoff: 13 MD ở consumer, 25 PNG ở asset KB, không có migration đang chạy.

- [x] **Bước 1: Xác nhận lại file vận hành và nguồn chuẩn**

Đọc đủ năm file nêu trên và kiểm tra rằng không có thay đổi mới ghi đè phạm vi Agent đã duyệt.

- [x] **Bước 2: Chạy kiểm tra baseline chỉ-đọc**

```powershell
python -m unittest discover -s tests -v
```

Kỳ vọng: `Ran 11 tests` và `OK`.

```powershell
@'
from pathlib import Path
import json

root = Path('.')
assets = sorted((root / 'knowledge-vng' / 'assets').glob('*.png'))
modules = sorted((root / 'knowledge-vng').glob('*.md'))
mapping = json.loads((root / 'knowledge-vng' / 'image-map.json').read_text(encoding='utf-8'))
print('modules', len(modules))
print('assets', len(assets))
print('mapped', len(mapping['images']))
print('unique_uris', len(set(mapping['images'].values())))
'@ | python -
```

Kỳ vọng: `13`, `25`, `25`, `25`.

- [x] **Bước 3: Xác nhận inventory live trước mutation**

Mở đúng hai KB theo ID trong `AGENTS.md`; ghi thời gian, số lượng, định dạng và trạng thái xử lý vào audit. Kỳ vọng:

- `Knowledge VNG - Image Assets`: 25 PNG, 0 MD; 25/25 Hoàn tất.
- `Knowledge VNG AI`: 13 MD, 0 PNG; 13/13 Hoàn tất.

- [x] **Bước 4: Lưu snapshot map nguyên byte**

Dùng `Copy-Item -LiteralPath` từ `knowledge-vng/image-map.json` sang `audit/image-map-before-agent-extension-2026-08-11.json`; sau đó so SHA-256 hai file. Không chỉnh snapshot sau bước này.

- [x] **Bước 5: Tạo audit Agent và cập nhật trạng thái đặc tả**

Audit phải có các phần: phạm vi, cấu hình môi trường, ma trận test, kết quả từng tab/nút, mutation đã thực hiện, ảnh bằng chứng, live IDs/URIs, điểm chưa xác định và rollback. Đổi trạng thái đặc tả thành `Đã duyệt ngày 11/08/2026; đang triển khai`.

---

### Task 2: Kiểm thử danh sách Agent và sáu tab cấu hình

**Files:**
- Create: `knowledge-vng/assets/26-agent-tong-quan-danh-sach.png`
- Create: `knowledge-vng/assets/27-agent-thong-tin-co-ban-va-intent.png`
- Create: `knowledge-vng/assets/28-agent-cau-hinh-mo-hinh.png`
- Create: `knowledge-vng/assets/29-agent-kho-tri-thuc.png`
- Create: `knowledge-vng/assets/30-agent-cong-cu.png`
- Create: `knowledge-vng/assets/31-agent-chien-luoc-truy-hoi.png`
- Create: `knowledge-vng/assets/32-agent-cau-hinh-da-phuong-thuc.png`
- Modify: `audit/agent-live-test-2026-08-11.md`
- Live target: `https://vnggames.ai/kb/agents`

**Interfaces:** Đọc trạng thái UI đã đăng nhập, tạo duy nhất Agent test và lưu bảy ảnh giao diện không lộ thông tin nhạy cảm.

- [x] **Bước 1: Kiểm thử bề mặt danh sách**

Mở lần lượt `Tất cả`, `Của tôi`, `Mặc định`, `Được chia sẻ`, `Đã đánh dấu`, `Gần đây` và Space hiện có. Kiểm tra tìm kiếm tên/mô tả, chuyển list/grid, menu từng Agent và trạng thái đánh dấu. Ghi `Đã kiểm chứng`, `Có điều kiện` hoặc `Chưa xác định` cho từng mục.

- [x] **Bước 2: Chụp ảnh tổng quan danh sách**

Chụp vùng đủ thể hiện tab/phạm vi, tìm kiếm, list/grid và thẻ Agent thành `26-agent-tong-quan-danh-sach.png`.

- [x] **Bước 3: Mở Tạo trợ lý và kiểm tra tab Thông tin cơ bản**

Kiểm tra hai chế độ chạy, năm preset, tên, emoji, mô tả, System Prompt, biến khả dụng và sáu intent:

`Greeting`, `Chitchat`, `Follow-up`, `Image Analysis`, `Summarize`, `Document Analysis`.

Không suy diễn hành vi runtime chỉ từ nhãn; mô tả rõ phần nào mới là cấu hình. Chụp `27-agent-thong-tin-co-ban-va-intent.png`.

- [x] **Bước 4: Kiểm tra Cấu hình mô hình**

Ghi chính xác danh sách model/reranker hiển thị tại thời điểm test, nhiệt độ, chế độ suy nghĩ và giá trị mặc định. Chụp `28-agent-cau-hinh-mo-hinh.png`.

- [x] **Bước 5: Kiểm tra Kho tri thức**

Ghi ba phạm vi KB, cách chọn một/nhiều KB, bộ lọc loại file và switch `Chỉ truy hồi khi được nhắc`. Chụp `29-agent-kho-tri-thuc.png`.

- [x] **Bước 6: Kiểm tra Công cụ**

Ghi các nhóm tool, tool đang bật theo preset, vòng lặp, timeout và gọi song song. Chỉ thay đổi điều khiển trên Agent test. Chụp `30-agent-cong-cu.png`.

- [x] **Bước 7: Kiểm tra Chiến lược truy hồi**

Ghi Top K vector, ngưỡng từ khóa/vector, Top K rerank và ngưỡng rerank; phân biệt giá trị mặc định UI với khuyến nghị vận hành. Chụp `31-agent-chien-luoc-truy-hoi.png`.

- [x] **Bước 8: Kiểm tra Cấu hình đa phương thức**

Kiểm tra switch ảnh/âm thanh và điều kiện để control tương ứng xuất hiện trong Chat. Không tuyên bố ASR/vision đầu-cuối nếu chưa có file test và phản hồi. Chụp `32-agent-cau-hinh-da-phuong-thuc.png`.

- [x] **Bước 9: Xác thực bảy PNG đầu**

```powershell
@'
from pathlib import Path
signature = b'\x89PNG\r\n\x1a\n'
paths = sorted(Path('knowledge-vng/assets').glob('2[6-9]-*.png')) + sorted(Path('knowledge-vng/assets').glob('3[0-2]-*.png'))
for path in paths:
    assert path.read_bytes().startswith(signature), path
    print(path.name, path.stat().st_size)
assert len(paths) == 7, len(paths)
'@ | python -
```

Kỳ vọng: đúng bảy file, mỗi file có payload PNG thật và dung lượng lớn hơn 0.

---

### Task 3: Tạo Agent test và kiểm thử vòng đời an toàn

**Files:**
- Modify: `audit/agent-live-test-2026-08-11.md`
- Live entity: `Kiểm thử Agent Knowledge VNG 2026-08-11`
- Conditional live entity: `Kiểm thử Agent Knowledge VNG 2026-08-11 - Bản sao`

**Cấu hình nền:** Suy luận thông minh; Hỏi đáp RAG; `deepseek-v4-flash` nếu còn khả dụng; `bge-reranker-v2-m3` nếu còn khả dụng; nhiệt độ `0,2`; KB được chọn là `Knowledge VNG AI`; loại file `MD`; truy hồi khi được nhắc tắt.

- [x] **Bước 1: Tạo Agent test bằng cấu hình nền**

System Prompt phải yêu cầu trả lời theo ngôn ngữ Human, chỉ dựa trên bằng chứng KB khi là câu nghiệp vụ, nói rõ khi không tìm thấy, trích nguồn khi có và không lộ ID nội bộ. Ghi ID/URL Agent và giá trị thực tế nếu model/reranker dự kiến không còn khả dụng.

- [x] **Bước 2: Kiểm tra tạo, chỉnh sửa và lưu**

Sửa mô tả bằng một dấu hiệu test vô hại, lưu, mở lại và xác nhận persistence. Trả mô tả về nội dung chuẩn sau test.

- [x] **Bước 3: Kiểm tra đánh dấu và bỏ đánh dấu**

Chỉ tác động Agent test; xác nhận nó xuất hiện rồi biến mất khỏi phạm vi `Đã đánh dấu`.

- [x] **Bước 4: Kiểm tra Nhân bản**

Nhân bản Agent test, đặt tên đúng hậu tố `- Bản sao`, rồi đối chiếu preset, model, KB, tool và retrieval. Không xóa bản sao trong phạm vi này.

- [x] **Bước 5: Gate Tắt/bật lại**

Chỉ bấm **Tắt** trên bản sao nếu trước mutation đã xác định chắc chắn control bật lại và phạm vi tìm thấy Agent đã tắt. Nếu không, ghi `Chưa kiểm chứng — dừng trước mutation`. Nếu có, thực hiện tắt → tìm → bật lại và ghi bằng chứng trạng thái cuối là hoạt động.

---

### Task 4: Kiểm thử Chat, Intent, nguồn, ảnh và đánh giá câu trả lời

**Files:**
- Create: `knowledge-vng/assets/33-agent-chat-nguon-va-anh.png`
- Create: `knowledge-vng/assets/34-agent-danh-gia-cau-tra-loi.png`
- Modify: `audit/agent-live-test-2026-08-11.md`

- [x] **Bước 1: Kiểm tra các control Chat**

Mở chat mới bằng Agent test; kiểm tra Agent picker, model, upload file, ảnh, nhắc KB/file, gửi tin và lịch sử. Đọc tài liệu file-upload của công cụ browser trước khi upload file test.

- [x] **Bước 2: Kiểm thử sáu Intent độc lập**

Dùng sáu prompt phân biệt rõ Greeting, Chitchat, Follow-up, Image Analysis, Summarize và Document Analysis. Với intent cần file/ảnh, chỉ dùng asset test vô hại trong workspace. Ghi prompt, phản hồi tóm tắt, có/không truy hồi và mức chắc chắn; không đưa toàn bộ hội thoại dài vào audit.

- [x] **Bước 3: Kiểm thử truy hồi KB tự động**

Hỏi một câu có đáp án chắc chắn trong 13 module hiện hành, mở nguồn tham khảo và xác nhận nguồn là Markdown của `Knowledge VNG AI`. Hỏi một câu ngoài KB để kiểm tra Agent không bịa.

- [x] **Bước 4: Kiểm thử truy hồi chỉ khi được nhắc**

Bật tạm switch `Chỉ truy hồi khi được nhắc`, so sánh cùng câu hỏi không có `@` và có `@Knowledge VNG AI`, sau đó trả switch về tắt. Ghi bằng chứng hành vi thay vì suy luận từ nhãn.

- [x] **Bước 5: Kiểm thử ảnh từ module hiện hành**

Yêu cầu câu trả lời kèm hình minh họa từ một module đang có ảnh; xác nhận ảnh render và nguồn Markdown mở được. Chụp `33-agent-chat-nguon-va-anh.png` sao cho thấy câu hỏi, phần trả lời, nguồn và ảnh nhưng không lộ dữ liệu nhạy cảm.

- [x] **Bước 6: Tạo phản hồi Hữu ích và Chưa hữu ích**

Trên chính hai câu trả lời test, tạo một phản hồi Hữu ích và một Chưa hữu ích. Bình luận phải ghi rõ `Kiểm thử nội bộ 11/08/2026` để không bị hiểu là feedback người dùng thật.

- [x] **Bước 7: Kiểm tra trang Đánh giá câu trả lời**

Kiểm tra bộ lọc thời gian, Agent, loại phản hồi, có bình luận, Tổng quan và Hộp xử lý. Với feedback test chưa hữu ích, kiểm tra `Cần xử lý → Đang xem → Đã xử lý` nếu control tồn tại và chỉ tác động bản ghi test. Chụp `34-agent-danh-gia-cau-tra-loi.png`.

- [x] **Bước 8: Xác thực đủ chín ảnh**

```powershell
@'
from pathlib import Path
signature = b'\x89PNG\r\n\x1a\n'
paths = sorted(Path('knowledge-vng/assets').glob('*.png'))
new = [p for p in paths if 26 <= int(p.name.split('-', 1)[0]) <= 34]
assert len(paths) == 34, len(paths)
assert len(new) == 9, len(new)
for path in new:
    data = path.read_bytes()
    assert data.startswith(signature), path
    assert len(data) > 0, path
    print(path.name, len(data))
'@ | python -
```

Kỳ vọng: 34 PNG tổng cộng, đúng chín file mới và tất cả có signature hợp lệ.

---

### Task 5: Upload chín ảnh vào KB asset và thu URI MinIO

**Files:**
- Read: `knowledge-vng/assets/26-agent-tong-quan-danh-sach.png` đến `34-agent-danh-gia-cau-tra-loi.png`
- Create: `audit/agent-image-assets-knowledge-ids-2026-08-11.json`
- Modify: `audit/agent-live-test-2026-08-11.md`
- Live target: `Knowledge VNG - Image Assets` (`6da8657c-dd96-4170-a698-074043475014`, tenant `10012`)

- [x] **Bước 1: Xác nhận đúng KB và inventory trước upload**

Kỳ vọng ngay trước mutation: 25 PNG, 0 MD, tất cả Hoàn tất.

- [x] **Bước 2: Upload đúng chín PNG bằng Thêm vào**

Chọn chính xác file 26–34. Không chọn 25 ảnh cũ, không đổi parser/chunking và không bấm Hủy khi pipeline đang chạy.

- [x] **Bước 3: Chờ xử lý hoàn tất**

Kỳ vọng: 9/9 Hoàn tất; inventory 34 PNG, 0 MD. Nếu bất kỳ file nào lỗi, dừng trước cập nhật map và ghi bằng chứng/retry có kiểm soát.

- [x] **Bước 4: Thu knowledge ID và URI MinIO**

Với từng file, đối chiếu tên → knowledge ID → URI duy nhất kết thúc `.png`. Tạo JSON chứa ngày, KB, KB ID, tenant, chín record và trạng thái. Kiểm tra không URI nào trùng nhau hoặc trùng 25 URI cũ.

---

### Task 6: Viết test thất bại cho hợp đồng 14 module/34 ảnh

**Files:**
- Modify: `tests/test_build_handbook.py`
- Test: `tests/test_build_handbook.py`

**TDD gate:** Phải quan sát test thất bại vì implementation vẫn đang ở 13 module/25 mapping trước khi sửa builder/master/map.

- [x] **Bước 1: Nâng assertion inventory ảnh từ 25 lên 34**

Thay hai assertion hiện hành:

```python
self.assertEqual(len(images), 34)
self.assertEqual(len(set(images.values())), 34)
```

- [x] **Bước 2: Đổi test build thành 14 module có Agent**

Đổi tên test thành:

```python
def test_build_project_creates_fourteen_modules_including_agent_guide(self):
```

Trong fixture, tạo thêm marker/module `13-tao-va-van-hanh-agent.md` có một H1 và một ảnh hợp lệ; đổi assertions `13` thành `14`; assert danh sách output có `13-tao-va-van-hanh-agent.md`.

- [x] **Bước 3: Chạy test mục tiêu và xác nhận đỏ đúng lý do**

```powershell
python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb
python -m unittest discover -s tests -v -k fourteen_modules_including_agent_guide
```

Kỳ vọng: test map thất bại vì map còn 25; test builder thất bại vì `EXPECTED_MODULE_COUNT` còn 13. Nếu thất bại do cú pháp/fixture, sửa test trước khi đi tiếp.

---

### Task 7: Mở rộng image map và builder

**Files:**
- Modify: `knowledge-vng/image-map.json`
- Modify: `scripts/build_handbook.py`
- Test: `tests/test_build_handbook.py`

- [x] **Bước 1: Thêm metadata provenance 26–34 và chín mapping**

Giữ nguyên `knowledge_base`, `knowledge_base_id`, `tenant_id`, `purpose`, provenance `01-25` và toàn bộ 25 URI cũ. Thêm provenance `26-34` mô tả ảnh Agent ngày 11/08/2026 và chín filename → URI từ audit. Cập nhật `generated_at` theo ngày kiểm chứng.

- [x] **Bước 2: Nâng số module builder**

Trong `scripts/build_handbook.py`:

```python
EXPECTED_MODULE_COUNT = 14
```

Không nới lỏng validation H1, ảnh hoặc MinIO.

- [x] **Bước 3: Chạy riêng test map**

```powershell
python -m unittest discover -s tests -v -k project_image_map_covers_all_assets_from_dedicated_asset_kb
```

Kỳ vọng: `OK`, 34 key khớp 34 asset và 34 URI duy nhất.

- [x] **Bước 4: Xác nhận gate project theo thứ tự thực thi thực tế**

```powershell
python -m unittest discover -s tests -v -k fourteen_modules_including_agent_guide
```

Fixture 14 module đã xanh. Trong thứ tự thực thi thực tế, master 14 marker được viết trước khi live map mở khóa; vì vậy không chạy strict project build với map thiếu để tránh ghi artifact dở dang. Strict build chỉ được chạy sau khi 9/9 ảnh hoàn tất và map đủ 34 URI.

```powershell
python scripts\build_handbook.py
```

Kết quả gate: không có artifact bàn giao nào được sinh bằng placeholder hoặc `--allow-missing-minio`.

---

### Task 8: Viết module Agent vào master v3.2.0

**Files:**
- Modify: `so-tay-tao-knowledge-base-v3.md`
- Generated later: `knowledge-vng/13-tao-va-van-hanh-agent.md`
- Generated later: `so-tay-tao-knowledge-base.html`

- [x] **Bước 1: Nâng metadata và mục lục**

Đổi phiên bản thành `3.2.0`, ngày cập nhật `11/08/2026`, thêm mục `Tạo và vận hành Agent` vào mục lục và đổi các câu vận hành nói `13 module` thành `14 module` khi chúng mô tả trạng thái hiện hành.

- [x] **Bước 2: Thêm đúng một cặp marker module 13**

Chèn sau module Google Drive và trước phụ lục:

```markdown
<!-- MODULE:13-tao-va-van-hanh-agent.md -->
# Tạo và vận hành Agent
...
<!-- /MODULE -->
```

- [x] **Bước 3: Viết nội dung dựa trên bằng chứng live**

Module phải bao phủ đủ 14 nhóm nội dung trong đặc tả: mô hình Human–Agent–KB; danh sách; sáu tab; chế độ/preset; prompt/intent; model; KB; tool; retrieval; multimodal; vòng đời; Chat; feedback; checklist/bảo trì/giới hạn. Mỗi kết luận chưa có test đầu-cuối phải được gắn `Có điều kiện` hoặc `Chưa xác định`.

- [x] **Bước 4: Gắn đủ chín ảnh theo kiến trúc MinIO/local**

Mỗi ảnh 26–34 xuất hiện đúng một lần trong module theo mẫu hiện hành: link hoạt động là URI MinIO và comment `LOCAL_ASSET` trỏ filename local. Không tạo active link `assets/...` trong module.

- [x] **Bước 5: Thêm lịch sử phiên bản**

Thêm dòng 3.2.0 ngày 11/08/2026 mô tả module Agent, chín ảnh và kiểm thử live.

- [x] **Bước 6: Kiểm tra marker trước build**

```powershell
@'
from pathlib import Path
text = Path('so-tay-tao-knowledge-base-v3.md').read_text(encoding='utf-8')
print(text.count('<!-- MODULE:'), text.count('<!-- /MODULE -->'))
assert text.count('<!-- MODULE:') == 14
assert text.count('<!-- /MODULE -->') == 14
assert '<!-- MODULE:13-tao-va-van-hanh-agent.md -->' in text
'@ | python -
```

Kỳ vọng: `14 14`.

---

### Task 9: Strict build và xác minh artifact local

**Files:**
- Generated: `knowledge-vng/*.md`
- Generated: `so-tay-tao-knowledge-base.html`
- Modify if needed: source/master, builder, tests (không sửa generated trực tiếp)

- [x] **Bước 1: Chạy strict build**

```powershell
python scripts\build_handbook.py
```

Kỳ vọng: `Build complete`, `14 modules`, HTML offline; không dùng cờ nới lỏng.

- [x] **Bước 2: Chạy toàn bộ test**

```powershell
python -m unittest discover -s tests -v
```

Kỳ vọng: `Ran 11 tests` và `OK` nếu chỉ cập nhật test hiện hành.

- [x] **Bước 3: Kiểm tra inventory và số link**

```powershell
@'
from pathlib import Path
import json, re

root = Path('.')
modules = sorted((root / 'knowledge-vng').glob('*.md'))
assets = sorted((root / 'knowledge-vng' / 'assets').glob('*.png'))
payload = json.loads((root / 'knowledge-vng' / 'image-map.json').read_text(encoding='utf-8'))
text = '\n'.join(p.read_text(encoding='utf-8') for p in modules)
print('modules', len(modules))
print('assets', len(assets))
print('map', len(payload['images']))
print('unique_uris', len(set(payload['images'].values())))
print('minio_links', len(re.findall(r'!\[[^\]]*\]\(minio://', text)))
print('local_asset', text.count('LOCAL_ASSET:'))
assert len(modules) == 14
assert len(assets) == 34
assert len(payload['images']) == 34
assert len(set(payload['images'].values())) == 34
assert len(re.findall(r'!\[[^\]]*\]\(minio://', text)) == 45
assert text.count('LOCAL_ASSET:') == 45
'@ | python -
```

Kỳ vọng: `14`, `34`, `34`, `34`, `45`, `45`.

- [x] **Bước 4: Kiểm tra module Agent và HTML offline**

Xác nhận module có đúng một H1, chín MinIO link/chín `LOCAL_ASSET`, không có active local image link. Mở HTML offline, kiểm tra mục lục Agent, chín ảnh nhúng data URI, zoom ảnh và không có request ảnh live.

---

### Task 10: Cập nhật kiến trúc, quyết định và trạng thái local trước upload MD

**Files:**
- Modify: `AGENTS.md`
- Modify: `PROJECT.md`
- Modify: `DECISIONS.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`
- Modify: `audit/agent-live-test-2026-08-11.md`
- Create: `docs/superpowers/reports/2026-08-11-agent-knowledge-vng-progress.md`

- [x] **Bước 1: Cập nhật các con số kiến trúc bền vững**

Ghi master v3.2.0, 14 module, 34 PNG, 34 URI, 45 link/`LOCAL_ASSET`; thêm vai trò Agent test và nguyên tắc chỉ bind consumer. Không đưa trạng thái xử lý tạm thời vào `AGENTS.md`, `PROJECT.md` hoặc `DECISIONS.md`.

- [x] **Bước 2: Ghi quyết định về Intent và mức chắc chắn**

Ghi rõ Intent là tuyến xử lý/prompt chuyên biệt theo loại yêu cầu; lựa chọn trong UI không tự chứng minh phân loại runtime. Phân biệt `Đã kiểm chứng`, `Có điều kiện`, `Chưa xác định`.

- [x] **Bước 3: Ghi trạng thái có ngày**

`STATUS.md`, `HANDOFF.md`, audit và progress report phải chỉ ra phần local đã đạt, inventory asset live, MD Agent chưa/đã upload, các test bị chặn và bước tiếp theo. Không trình bày đích 14 MD là live nếu upload chưa hoàn tất.

---

### Task 11: Upload module Agent vào consumer

**Files:**
- Read: `knowledge-vng/13-tao-va-van-hanh-agent.md`
- Create: `audit/agent-markdown-knowledge-id-2026-08-11.json`
- Modify: `audit/agent-live-test-2026-08-11.md`
- Live target: `Knowledge VNG AI` (`cefadf09-4187-46ac-a765-591e3255a4a4`, tenant `10012`)

**Gate trước mutation:** strict build và toàn bộ test đều xanh; asset KB đã có 34 PNG Hoàn tất; module có chín URI MinIO đúng.

- [x] **Bước 1: Xác nhận inventory consumer trước upload**

Kỳ vọng: 13 MD, 0 PNG, tất cả Hoàn tất; không có file trùng tên `13-tao-va-van-hanh-agent.md`.

- [x] **Bước 2: Upload duy nhất module Agent bằng Thêm vào**

Không chọn 13 module cũ, HTML, JSON hay ảnh. Giữ parser mặc định trừ khi có lỗi cụ thể và audit chứng minh cần retry.

- [x] **Bước 3: Chờ trạng thái Hoàn tất**

Kỳ vọng: 14 MD, 0 PNG; module mới Hoàn tất. Nếu lỗi, giữ nguyên 13 MD cũ, audit lỗi và chỉ retry có kiểm soát.

- [x] **Bước 4: Ghi knowledge ID**

Tạo JSON gồm ngày, KB/ID/tenant, filename, knowledge ID, parser thực tế, trạng thái và thời gian hoàn tất.

---

### Task 12: Kiểm chứng Agent truy hồi chính module Agent

**Files:**
- Modify: `audit/agent-live-test-2026-08-11.md`
- Modify: `docs/superpowers/reports/2026-08-11-agent-knowledge-vng-progress.md`

- [x] **Bước 1: Làm mới cấu hình/phiên Chat nếu cần**

Xác nhận Agent test vẫn trỏ consumer và không bị đổi sang KB asset; mở chat mới để tránh lịch sử cũ ảnh hưởng.

- [x] **Bước 2: Hỏi câu chỉ module Agent mới trả lời đầy đủ**

Ví dụ: yêu cầu liệt kê sáu tab Tạo trợ lý và giải thích Intent. Xác nhận nội dung khớp module mới và nguồn tham khảo mở đúng `13-tao-va-van-hanh-agent.md`.

- [x] **Bước 3: Hỏi câu buộc trả lời kèm ảnh Agent**

Xác nhận ít nhất một ảnh 26–34 render trong câu trả lời và nguồn là module Agent. Nếu nguồn đúng nhưng ảnh không render, không công nhận hoàn tất; kiểm tra URI/module trước.

- [x] **Bước 4: Kiểm tra câu ngoài phạm vi**

Xác nhận Agent nói không đủ dữ liệu thay vì bịa, theo System Prompt.

---

### Task 13: Xác minh cuối, reviewer độc lập và bàn giao

**Files:**
- Create: `audit/final-agent-live-inventory-2026-08-11.json`
- Create: `docs/superpowers/reports/2026-08-11-agent-final-verification.md`
- Modify: `audit/agent-live-test-2026-08-11.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`

- [x] **Bước 1: Chạy lại strict build và toàn bộ test**

```powershell
python scripts\build_handbook.py
python -m unittest discover -s tests -v
```

Kỳ vọng cuối: `Build complete`, 14 module, `Ran 11 tests`, `OK`.

- [x] **Bước 2: Chụp inventory live cuối**

Ghi JSON có ngày/giờ và từng KB:

- Asset: 34 PNG, 0 MD; 34/34 Hoàn tất.
- Consumer: 14 MD, 0 PNG; 14/14 Hoàn tất.

- [x] **Bước 3: Rà soát an toàn và hồi quy**

Xác nhận 25 ảnh cũ và 13 MD cũ vẫn tồn tại; không Agent mặc định nào bị sửa; Agent test/bản sao ở trạng thái hoạt động; switch `Chỉ truy hồi khi được nhắc` đã trả về tắt; không có credential trong workspace/audit.

- [x] **Bước 4: Yêu cầu reviewer độc lập**

Reviewer đối chiếu đặc tả, plan, diff file, output build/test, inventory live, chat source/ảnh và các mục `Có điều kiện`. Chỉ chấp nhận khi không còn lỗi nghiêm trọng/chính.

- [x] **Bước 5: Cập nhật STATUS và HANDOFF cuối**

Ghi kết quả thật, evidence links, những gì còn chưa kiểm chứng (nếu có), quy tắc bảo trì Agent/ảnh và nhiệm vụ mở tiếp theo. Không ghi `Hoàn tất` nếu bất kỳ gate live bắt buộc nào chưa đạt.

## Tiêu chí hoàn tất tổng

- Master v3.2.0 có đúng 14 cặp marker; module Agent là artifact sinh tự động.
- Có đúng 34 PNG thật local, 34 URI MinIO duy nhất, 45 link ảnh MinIO và 45 `LOCAL_ASSET`.
- Strict build và 11 test thành công.
- Asset KB có 34 PNG/0 MD; consumer có 14 MD/0 PNG; tất cả Hoàn tất.
- Agent test truy hồi module Agent, mở đúng nguồn Markdown và render ít nhất một ảnh Agent.
- Không sửa sáu Agent mặc định, không xóa dữ liệu, không để mutation thử nghiệm ở trạng thái khó phục hồi.
- Audit, snapshot, ID/URI JSON, final inventory, `STATUS.md` và `HANDOFF.md` đầy đủ và nhất quán.
