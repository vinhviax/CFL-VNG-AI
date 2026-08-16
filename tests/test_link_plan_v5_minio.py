"""Test cho scripts/link_plan_v5_minio.py — đổi link ảnh cục bộ sang URI MinIO."""

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "link_plan_v5_minio.py"
BUNDLE = ROOT / "knowledge" / "GS9 CFL Plan Version" / "V5"
# Tu 16/08/2026 anh nam thang trong V5/.
ASSETS = BUNDLE


def load_module():
    spec = importlib.util.spec_from_file_location("link_plan_v5_minio", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LinkPlanV5MinioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()
        cls.uri = cls.mod.URI_PREFIX + "11111111-2222-3333-4444-555555555555.jpg"
        cls.images = {"image-v5-01-abc.jpg": cls.uri}

    def test_embed_gets_minio_uri_and_local_asset_comment(self):
        text = "![Giao diện phối súng](image-v5-01-abc.jpg)\n"
        out, embeds, links, unmapped = self.mod.rewrite_text(text, self.images)

        self.assertEqual((embeds, links, unmapped), (1, 0, []))
        self.assertIn(f"![Giao diện phối súng]({self.uri})", out)
        self.assertIn("<!-- LOCAL_ASSET: image-v5-01-abc.jpg -->", out)
        self.assertNotIn("](image-v5-", out)

    def test_registry_link_target_changes_and_text_becomes_filename(self):
        text = "- **Asset:** [image-v5-01-abc.jpg](image-v5-01-abc.jpg).\n"
        out, embeds, links, unmapped = self.mod.rewrite_text(text, self.images)

        self.assertEqual((embeds, links, unmapped), (0, 1, []))
        self.assertIn(f"[image-v5-01-abc.jpg]({self.uri})", out)
        self.assertNotIn("](image-v5-", out)
        # Link registry không phải ảnh nhúng nên không thêm comment truy nguyên.
        self.assertNotIn("LOCAL_ASSET", out)

    def test_rewrite_is_idempotent(self):
        text = "![alt](image-v5-01-abc.jpg)\n"
        once, _, _, _ = self.mod.rewrite_text(text, self.images)
        twice, embeds, links, unmapped = self.mod.rewrite_text(once, self.images)

        self.assertEqual(once, twice)
        self.assertEqual((embeds, links, unmapped), (0, 0, []))
        self.assertEqual(twice.count("LOCAL_ASSET"), 1)

    def test_unmapped_asset_is_reported_and_left_untouched(self):
        text = "![alt](image-v5-99-khong-co-trong-map.jpg)\n"
        out, embeds, links, unmapped = self.mod.rewrite_text(text, self.images)

        self.assertEqual((embeds, links), (0, 0))
        self.assertEqual(unmapped, ["image-v5-99-khong-co-trong-map.jpg"])
        self.assertIn("](image-v5-99-khong-co-trong-map.jpg)", out)

    def test_bundle_currently_has_29_embeds_and_29_registry_links(self):
        """Hợp đồng nội dung: 29 ảnh, mỗi ảnh nhúng 1 lần và vào registry 1 lần.

        Đếm được ở CẢ HAI trạng thái của bundle — trước khi gắn link thì tham chiếu
        là `image-v5-...`, sau khi chạy link_plan_v5_minio.py thì là `minio://...`.
        Việc gắn link là thao tác một chiều nên test không được khoá vào trạng thái đầu.
        """
        names = {p.name for p in ASSETS.glob("*.jpg")}
        self.assertEqual(len(names), 29)

        fake = {
            name: self.mod.URI_PREFIX + f"{i:08d}-0000-0000-0000-000000000000.jpg"
            for i, name in enumerate(sorted(names), start=1)
        }

        embeds = links = 0
        unmapped: list[str] = []
        for path in sorted(BUNDLE.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            _, e, l, u = self.mod.rewrite_text(text, fake)
            embeds += e + len(re.findall(r"!\[[^\]]*\]\(minio://[^)]+\)", text))
            links += l + len(re.findall(r"(?<!!)\[[^\]]*\]\(minio://[^)]+\)", text))
            unmapped.extend(u)

        self.assertEqual(unmapped, [], "mọi tham chiếu ảnh phải khớp một file trong V5/")
        self.assertEqual(embeds, 29)
        self.assertEqual(links, 29)

    def test_bundle_has_no_leftover_relative_image_links(self):
        """Sau khi gắn link, không còn `](image-v5-...)` nào — Web không đọc được đường dẫn tương đối."""
        if not (BUNDLE / "image-map.json").exists():
            self.skipTest("chưa có image-map.json nên bundle vẫn ở trạng thái trước khi gắn link")
        leftover = [
            path.name
            for path in sorted(BUNDLE.glob("*.md"))
            if re.search(r"\]\(image-v5-", path.read_text(encoding="utf-8"))
        ]
        self.assertEqual(leftover, [])

    def test_map_targets_the_plan_version_kb_id(self):
        self.assertEqual(self.mod.KB_ID, "1452bc9a-c8b4-487b-b623-34e0b00a83e9")
        # DEC-052: chấp nhận cả `exports/<uuid>` cũ lẫn `<knowledge_id>/<uuid>`
        # lấy qua API — cả hai đã kiểm chứng render đúng, nên chỉ khoá tới tenant.
        self.assertEqual(self.mod.URI_PREFIX, "minio://knowledge-base-prd/10012/")

    def test_bundle_uris_match_map_and_are_valid_minio(self):
        """29 ảnh trong bundle phải trỏ đúng URI đang có trong map."""
        images = json.loads((BUNDLE / "image-map.json").read_text(encoding="utf-8"))["images"]
        self.assertEqual(len(images), 29)
        for name, uri in images.items():
            self.assertTrue(name.startswith("image-v5-"), name)
            self.assertTrue(uri.startswith(self.mod.URI_PREFIX), uri)

        rendered = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(BUNDLE.glob("doc-v5-*.md"))
        )
        for uri in images.values():
            self.assertIn(uri, rendered, f"URI vắng mặt trong bundle: {uri}")
        # Không còn URI lạ ngoài map.
        used = set(re.findall(r"minio://knowledge-base-prd/10012/[^)\s]+", rendered))
        self.assertEqual(used - set(images.values()), set())


if __name__ == "__main__":
    unittest.main()
