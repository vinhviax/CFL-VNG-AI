import importlib.util
import base64
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_handbook.py"
CONSUMER_DIR = ROOT / "knowledge" / "GS9 Knowledge VNG AI"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_handbook", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BuildHandbookTests(unittest.TestCase):
    def test_archived_master_is_out_of_the_build_path(self):
        """Master cũ là bản lưu trữ, không còn là nguồn build.

        Từ 16/08/2026 builder đọc `docs KB/Human` (DEC-053); nhánh master chỉ
        chạy khi thư mục đó rỗng. Ngày 17/08/2026 master được dời vào
        `audit/archive/` (DEC-066). Gate nay kiểm đúng hai điều còn ý nghĩa:
        master không nằm ở root nữa, và nguồn thật sinh đủ module — thay cho
        các assert khoá chuỗi số đếm trên một file đã hết vai trò.
        """
        self.assertFalse(
            (ROOT / "so-tay-tao-knowledge-base-v3.md").exists(),
            "master cũ phải nằm ở audit/archive/, không còn ở root",
        )
        self.assertTrue(
            (ROOT / "audit" / "archive" / "so-tay-tao-knowledge-base-v3.md").is_file(),
            "bản lưu trữ master phải còn để các tài liệu Dev truy nguyên được",
        )

        human_dir = ROOT / "docs KB" / "Human"
        sources = sorted(
            path
            for pattern in ("KB-*.md", "Agent-*.md")
            for path in human_dir.glob(pattern)
        )
        builder = load_builder()
        self.assertEqual(len(sources), builder.EXPECTED_MODULE_COUNT)

    def test_project_layout_uses_exact_web_knowledge_base_names(self):
        builder = load_builder()

        self.assertEqual(builder.KNOWLEDGE_DIR_NAME, "knowledge")
        self.assertEqual(builder.CONSUMER_KB_NAME, "GS9 Knowledge VNG AI")
        self.assertFalse(hasattr(builder, "ASSET_KB_NAME"))

    def test_local_png_assets_have_png_signature(self):
        expected_signature = b"\x89PNG\r\n\x1a\n"

        for asset_path in sorted(CONSUMER_DIR.glob("image-*.png")):
            with asset_path.open("rb") as asset_file:
                actual_signature = asset_file.read(8)

            self.assertEqual(
                actual_signature,
                expected_signature,
                f"{asset_path.name} does not have a PNG signature",
            )

    def test_project_image_map_covers_all_merged_assets(self):
        payload = json.loads(
            (CONSUMER_DIR / "image-map.json").read_text(encoding="utf-8")
        )
        assets = {path.name for path in CONSUMER_DIR.glob("image-*.png")}
        images = payload["images"]

        self.assertEqual(
            payload["knowledge_base"],
            "GS9 Knowledge VNG AI",
        )
        self.assertEqual(
            payload["knowledge_base_id"],
            "cefadf09-4187-46ac-a765-591e3255a4a4",
        )
        self.assertEqual(payload["tenant_id"], "10012")
        self.assertEqual(set(images), assets)
        self.assertEqual(len(images), 52)
        self.assertEqual(len(set(images.values())), 52)
        # Đã kiểm chứng 16/08/2026 (doc-02, DEC-052): dạng file_path
        # ("minio://.../10012/<knowledge_id>/<uuid>.png") render đúng trong
        # Document preview, y hệt dạng "exports/" cũ. Chấp nhận cả hai.
        for name, uri in images.items():
            self.assertTrue(name.startswith("image-"))
            self.assertTrue(uri.startswith("minio://knowledge-base-prd/10012/"))
            self.assertTrue(uri.endswith(".png"))

    def test_generated_project_modules_have_no_active_local_image_links(self):
        for module_path in sorted(CONSUMER_DIR.glob("*.md")):
            rendered = module_path.read_text(encoding="utf-8")
            in_fence = False
            active_lines = []
            for line in rendered.splitlines():
                stripped = line.lstrip()
                if stripped.startswith("```") or stripped.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if not in_fence:
                    active_lines.append(line)
            active = "\n".join(active_lines)
            self.assertNotIn("](assets/", active, module_path.name)

    def test_extract_modules_promotes_each_module_to_one_h1(self):
        builder = load_builder()
        source = """
# Master
<!-- MODULE:00-first.md -->
## 00 - First
### Child
<!-- /MODULE -->
<!-- MODULE:01-second.md -->
## 01 - Second
### Child
<!-- /MODULE -->
"""

        modules = builder.extract_modules(source)

        self.assertEqual([item.name for item in modules], ["00-first.md", "01-second.md"])
        self.assertEqual(modules[0].body.count("\n# ") + modules[0].body.startswith("# "), 1)
        self.assertIn("## Child", modules[0].body)

    def test_write_modules_uses_minio_image_and_records_local_asset(self):
        builder = load_builder()
        self.assertTrue(hasattr(builder, "write_modules"), "write_modules must exist")
        source = """
<!-- MODULE:00-first.md -->
## 00 - First
![Màn hình](knowledge-vng/assets/screen.png)
<!-- /MODULE -->
"""
        with tempfile.TemporaryDirectory() as folder:
            outputs = builder.write_modules(
                source,
                Path(folder),
                {"screen.png": "minio://bucket/screen.png"},
                require_minio=True,
            )

            rendered = outputs[0].read_text(encoding="utf-8")

        self.assertIn("<!-- LOCAL_ASSET: assets/screen.png -->", rendered)
        self.assertIn("![Màn hình](minio://bucket/screen.png)", rendered)
        self.assertNotIn("](knowledge-vng/assets/", rendered)

    def test_write_modules_accepts_angle_wrapped_asset_paths_with_spaces(self):
        builder = load_builder()
        source = """
<!-- MODULE:00-first.md -->
## 00 - First
![Màn hình](<knowledge/GS9 Knowledge VNG - Image Assets/screen.png>)
<!-- /MODULE -->
"""
        with tempfile.TemporaryDirectory() as folder:
            outputs = builder.write_modules(
                source,
                Path(folder),
                {"screen.png": "minio://bucket/screen.png"},
                require_minio=True,
                local_asset_prefix="../GS9 Knowledge VNG - Image Assets",
            )

            rendered = outputs[0].read_text(encoding="utf-8")

        self.assertIn(
            "<!-- LOCAL_ASSET: ../GS9 Knowledge VNG - Image Assets/screen.png -->",
            rendered,
        )
        self.assertIn("![Màn hình](minio://bucket/screen.png)", rendered)

    def test_write_modules_ignores_image_examples_inside_fenced_code(self):
        builder = load_builder()
        source = """
<!-- MODULE:00-first.md -->
## 00 - First
![Real image](knowledge-vng/assets/screen.png)

```markdown
![Example only](minio://bucket/example.png)
```
<!-- /MODULE -->
"""
        with tempfile.TemporaryDirectory() as folder:
            outputs = builder.write_modules(
                source,
                Path(folder),
                {"screen.png": "minio://bucket/screen.png"},
                require_minio=True,
            )

            rendered = outputs[0].read_text(encoding="utf-8")

        self.assertIn("![Real image](minio://bucket/screen.png)", rendered)
        self.assertIn("![Example only](minio://bucket/example.png)", rendered)
        self.assertNotIn("LOCAL_ASSET: assets/example.png", rendered)

    def test_write_modules_rebases_master_relative_document_links(self):
        builder = load_builder()
        source = """
<!-- MODULE:00-first.md -->
## 00 - First
Xem [audit](audit/evidence.md).
<!-- /MODULE -->
"""
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evidence = root / "audit" / "evidence.md"
            evidence.parent.mkdir(parents=True)
            evidence.write_text("evidence", encoding="utf-8")
            output_dir = root / "knowledge" / "GS9 Knowledge VNG AI"

            outputs = builder.write_modules(
                source,
                output_dir,
                {},
                require_minio=False,
                source_root=root,
            )
            rendered = outputs[0].read_text(encoding="utf-8")

        self.assertIn("](../../audit/evidence.md)", rendered)
        self.assertNotIn("](audit/evidence.md)", rendered)

    def test_build_offline_html_embeds_images_and_interactions(self):
        builder = load_builder()
        self.assertTrue(hasattr(builder, "build_offline_html"), "build_offline_html must exist")
        source = """
# Sổ tay

Mở đầu.

## 00 - Quick start

![Màn hình](<knowledge/GS9 Knowledge VNG - Image Assets/screen.png>)
"""
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            asset = (
                root
                / "knowledge"
                / "GS9 Knowledge VNG - Image Assets"
                / "screen.png"
            )
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png)
            output = root / "handbook.html"

            builder.build_offline_html(source, root, output)
            rendered = output.read_text(encoding="utf-8")

        self.assertIn("data:image/png;base64,", rendered)
        self.assertIn('id="search"', rendered)
        self.assertIn('id="sidebar"', rendered)
        self.assertIn('id="printButton"', rendered)
        self.assertIn("@media (max-width: 940px)", rendered)
        self.assertIn("prefers-reduced-motion", rendered)
        self.assertIn("IntersectionObserver", rendered)
        self.assertIn('class="skip-link"', rendered)
        self.assertIn("overflow-wrap:anywhere", rendered)
        self.assertIn(".doc-section,.intro-card{min-width:0", rendered)
        self.assertIn(".table-wrap{max-width:100%;overflow-x:auto", rendered)
        self.assertNotIn('src="http', rendered.lower())
        self.assertNotIn('<script src=', rendered.lower())
        self.assertNotIn('<link rel="stylesheet"', rendered.lower())
        self.assertNotIn("—", rendered)
        self.assertNotIn("–", rendered)

    def test_build_offline_html_uses_version_from_source(self):
        builder = load_builder()
        source = """
# Sổ tay

> Phiên bản: 9.8.7
> Cập nhật: 01/02/2030

## 00 - Quick start

Nội dung kiểm thử.
"""
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root / "handbook.html"

            builder.build_offline_html(source, root, output)
            rendered = output.read_text(encoding="utf-8")

        self.assertIn("Sổ tay vận hành · Phiên bản 9.8.7", rendered)
        self.assertIn("Cập nhật 01/02/2030", rendered)
        self.assertIn("Dữ liệu giao diện được kiểm chứng ngày 01/02/2030", rendered)
        self.assertNotIn("Sổ tay vận hành · Phiên bản 3.0", rendered)
        self.assertNotIn("Cập nhật 06/08/2026", rendered)

    def test_build_project_creates_twenty_modules_including_agent_deep_split(self):
        builder = load_builder()
        self.assertTrue(hasattr(builder, "build_project"), "build_project must exist")
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        blocks = []
        module_names = [f"doc-{index:02d}-module.md" for index in range(13)]
        module_names.extend(
            [
                "doc-13-tong-quan-va-kien-truc.md",
                "doc-14-che-do-preset-prompt-va-intent.md",
                "doc-15-model-reranker-suy-luan-va-quota.md",
                "doc-16-kho-tri-thuc-cong-cu-va-truy-hoi.md",
                "doc-17-da-phuong-thuc-va-tep-dinh-kem.md",
                "doc-18-chat-nguon-lich-su-va-danh-gia.md",
                "doc-19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md",
                "doc-20-thiet-ke-danh-muc-kho.md",
            ]
        )
        bodies = {}
        for index, module_name in enumerate(module_names):
            bodies[module_name] = (
                f"## {index:02d} - Module\n"
                "![Màn hình](<knowledge/GS9 Knowledge VNG AI/image-screen.png>)\n"
            )

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            consumer_dir = root / "knowledge" / "GS9 Knowledge VNG AI"
            consumer_dir.mkdir(parents=True)
            (consumer_dir / "image-screen.png").write_bytes(png)
            (consumer_dir / "image-map.json").write_text(
                '{"images":{"image-screen.png":"minio://bucket/image-screen.png"}}',
                encoding="utf-8",
            )
            human_dir = root / "docs KB" / "Human"
            (human_dir / "KB").mkdir(parents=True)
            (human_dir / "Agent").mkdir(parents=True)
            (human_dir / "_master-header.txt").write_text(
                "# Sổ tay\n\n", encoding="utf-8"
            )
            for module_name, body in bodies.items():
                index = int(module_name.split("-")[1])
                sub = "Agent" if 13 <= index < 20 else "KB"
                (human_dir / sub / module_name).write_text(body, encoding="utf-8")

            result = builder.build_project(root, require_minio=True)

            self.assertEqual(len(result["modules"]), 21)
            self.assertEqual(
                result["modules"][-1].name,
                "doc-20-thiet-ke-danh-muc-kho.md",
            )
            self.assertTrue(result["html"].exists())
            self.assertEqual(len(list(consumer_dir.glob("*.md"))), 21)
            self.assertFalse((root / "knowledge-vng").exists())

    def test_live_project_has_exact_agent_deep_split_and_sixty_image_pairs(self):
        expected_modules = {
            "doc-00-gioi-thieu-va-quick-start.md",
            "doc-01-chuan-bi-noi-dung.md",
            "doc-02-tao-kb-nhanh-va-nang-cao.md",
            "doc-03-tai-lieu-rag-wiki.md",
            "doc-04-faq-va-lap-chi-muc.md",
            "doc-05-mo-hinh-vlm-asr.md",
            "doc-06-parser-va-xu-ly-file.md",
            "doc-07-phan-doan-chunking.md",
            "doc-08-chia-se-va-nguon-du-lieu.md",
            "doc-09-van-hanh-documents-wiki-graph.md",
            "doc-10-van-hanh-faq.md",
            "doc-11-chat-kiem-thu-va-bao-tri.md",
            "doc-12-ket-noi-google-drive.md",
            "doc-13-tong-quan-va-kien-truc.md",
            "doc-14-che-do-preset-prompt-va-intent.md",
            "doc-15-model-reranker-suy-luan-va-quota.md",
            "doc-16-kho-tri-thuc-cong-cu-va-truy-hoi.md",
            "doc-17-da-phuong-thuc-va-tep-dinh-kem.md",
            "doc-18-chat-nguon-lich-su-va-danh-gia.md",
            "doc-19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md",
            "doc-20-thiet-ke-danh-muc-kho.md",
        }
        module_paths = sorted(CONSUMER_DIR.glob("doc-*.md"))
        self.assertEqual({path.name for path in module_paths}, expected_modules)

        rendered = "\n".join(path.read_text(encoding="utf-8") for path in module_paths)
        # Đã kiểm chứng 16/08/2026 (doc-02, DEC-052): dạng file_path
        # ("minio://.../10012/<knowledge_id>/<uuid>.png") render đúng, thay
        # thế toàn bộ 49 URI "exports/" cũ đã chết sau khi ảnh được re-sync
        # qua Google Drive connector. Đếm theo tiền tố chung, không khoá dạng.
        # Cập nhật 18/08/2026 (DEC-071/072): 61 → 64 sau khi doc-11 build
        # được với 3 ảnh mới image-50/51/52 (tính năng "Thêm vào tri thức").
        self.assertEqual(rendered.count("minio://knowledge-base-prd/10012/"), 64)
        self.assertEqual(
            rendered.count("<!-- LOCAL_ASSET: ./image-"),
            64,
        )

    def test_agent_modules_are_operational_guides_without_dev_content(self):
        """Module Agent phải là hướng dẫn thao tác, không lẫn nội dung Dev.

        Từ 16/08/2026 nội dung tách theo đối tượng đọc: `docs KB/Human` chỉ
        hướng dẫn người dùng, mọi chi tiết kiểm chứng nằm ở `docs KB/Dev`.
        Cấu trúc heading cố định cũ (gồm `Bằng chứng`, `Data flow`) không còn
        áp dụng; gate nay kiểm đúng thứ khiến tài liệu dùng được.
        """
        dev_only_markers = [
            "DEC-0",
            "audit/",
            "## Bằng chứng",
            "Chưa được phép suy luận",
            "Bị chặn–Chưa xác định",
        ]
        for module_number in range(13, 20):
            matches = list(CONSUMER_DIR.glob(f"doc-{module_number:02d}-*.md"))
            self.assertEqual(
                len(matches), 1, f"missing or ambiguous module {module_number:02d}"
            )
            name = matches[0].name
            rendered = matches[0].read_text(encoding="utf-8")

            self.assertIn("Bạn sẽ biết gì sau khi đọc", rendered, name)
            self.assertIn("Checklist", rendered, name)
            self.assertIn("minio://", rendered, f"{name}: phải có ít nhất một ảnh")
            for marker in dev_only_markers:
                self.assertNotIn(marker, rendered, f"{name}: lẫn nội dung Dev — {marker}")

    def test_count_h1_ignores_markdown_inside_fenced_code(self):
        builder = load_builder()
        self.assertTrue(hasattr(builder, "count_h1"), "count_h1 must exist")
        source = """# Tài liệu

```markdown
# Ví dụ nằm trong code
## Mục con trong code
```

## Mục thật
"""

        self.assertEqual(builder.count_h1(source), 1)


if __name__ == "__main__":
    unittest.main()
