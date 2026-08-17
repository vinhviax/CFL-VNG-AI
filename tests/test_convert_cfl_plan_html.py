import hashlib
import importlib.util
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "convert_cfl_plan_html.py"
DEFAULT_SOURCE = Path(
    r"C:\Users\CPU13114\Downloads\CFL5_0- Plan Ver 5.0-14082026.html"
)
SOURCE = Path(os.environ.get("CFL_PLAN_V5_HTML", DEFAULT_SOURCE))
EXPECTED_SOURCE_SHA256 = (
    "593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038"
)
EXPECTED_MODULES = [
    "doc-v5-00-index-va-pham-vi.md",
    "doc-v5-01-tong-quan-phien-ban.md",
    "doc-v5-02-lich-trinh-phien-ban.md",
    "doc-v5-03-cach-choi-moi.md",
    "doc-v5-04-he-thong-moi.md",
    "doc-v5-05-nang-cao-chat-luong.md",
    "doc-v5-06-tiep-te-moi.md",
    "doc-v5-07-hoat-dong-tang-do-hoat-dong.md",
    "doc-v5-08-hoat-dong-thuong-mai-hoa.md",
    "doc-v5-09-ban-dia-hoa-va-phat-hanh.md",
    "doc-v5-10-danh-muc-hinh-anh.md",
    "doc-v5-11-ghi-chu-va-truy-nguyen.md",
]


def load_converter():
    spec = importlib.util.spec_from_file_location("convert_cfl_plan_html", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def normalize_text(value):
    return re.sub(r"\s+", " ", value).strip()


def tree_snapshot(root):
    return {
        path.relative_to(root).as_posix(): sha256_bytes(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


@unittest.skipUnless(SOURCE.exists(), f"Source HTML not available: {SOURCE}")
class ConvertCflPlanHtmlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.converter = load_converter()
        cls.source_bytes = SOURCE.read_bytes()
        cls.soup = BeautifulSoup(cls.source_bytes.decode("utf-8"), "html.parser")

    def test_source_contract_is_exactly_the_audited_file(self):
        self.assertEqual(sha256_bytes(self.source_bytes), EXPECTED_SOURCE_SHA256)

        inventory = self.converter.inspect_source(SOURCE)

        self.assertEqual(inventory["source_sha256"], EXPECTED_SOURCE_SHA256)
        self.assertEqual(inventory["section_count"], 9)
        self.assertEqual(inventory["group_count"], 29)
        self.assertEqual(inventory["item_count"], 115)
        self.assertEqual(inventory["figure_count"], 14)
        self.assertEqual(inventory["image_count"], 29)
        self.assertEqual(inventory["placeholder_count"], 2)
        self.assertEqual(inventory["dom_or_inline_hidden_element_count"], 0)
        self.assertEqual(inventory["css_hidden_empty_description_count"], 1)

    def test_conversion_has_complete_deterministic_shape(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "V5"
            self.converter.convert(SOURCE, output)

            self.assertEqual(
                sorted(path.name for path in output.glob("*.md")),
                EXPECTED_MODULES,
            )
            self.assertEqual(len(list(output.glob("*.jpg"))), 29)
            self.assertTrue((output / "source-manifest.json").is_file())

            first = tree_snapshot(output)
            self.converter.convert(SOURCE, output)
            second = tree_snapshot(output)
            self.assertEqual(first, second)

    def test_markdown_covers_all_semantic_source_text(self):
        selectors = [
            ".cover .tag",
            ".cover h1",
            ".cover h2",
            ".cover .meta .k",
            ".cover .meta .v",
            ".ov-slogan > div",
            ".ov-res .k",
            ".ov-res .v",
            ".viz h6",
            ".tl-bar > div",
            ".tl-lbl > span",
            ".sec-hd .no",
            ".sec-hd h3",
            ".sec-intro",
            ".kp .i",
            ".kp .x",
            ".grp-hd h4",
            ".grp-desc",
            ".item .t",
            ".item .d",
            ".item .hl li",
            ".shc",
            "figure figcaption",
            ".ph .c",
            ".ph .t",
            ".ph .s",
            ".fig-ph .code",
            ".fig-ph .tx",
            ".note h5",
            ".note li",
            "footer",
        ]
        expected = []
        for selector in selectors:
            for node in self.soup.select(selector):
                value = normalize_text(node.get_text(" ", strip=True))
                if value and value not in expected:
                    expected.append(value)

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "V5"
            self.converter.convert(SOURCE, output)
            corpus = normalize_text(
                "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in sorted(output.glob("*.md"))
                )
            )

        missing = [value for value in expected if value not in corpus]
        self.assertEqual(missing, [], f"Missing semantic source text: {missing[:5]}")

    def test_every_item_is_mapped_with_title_and_description(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "V5"
            self.converter.convert(SOURCE, output)
            manifest = json.loads(
                (output / "source-manifest.json").read_text(encoding="utf-8")
            )
            by_section = {
                entry["source_section_id"]: output / entry["file"]
                for entry in manifest["modules"]
                if entry.get("source_section_id")
            }

            seen = 0
            for section in self.soup.select("section[id]"):
                module_text = normalize_text(
                    by_section[section["id"]].read_text(encoding="utf-8")
                )
                for item in section.select(".item"):
                    title = normalize_text(item.select_one(".t").get_text(" ", strip=True))
                    description = normalize_text(
                        item.select_one(".d").get_text(" ", strip=True)
                    )
                    self.assertIn(title, module_text)
                    if description:
                        self.assertIn(description, module_text)
                    else:
                        self.assertIn("Không có mô tả trong nguồn HTML", module_text)
                    seen += 1

            self.assertEqual(seen, 115)

    def test_manifest_records_preserve_keyed_dom_data_and_order(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "V5"
            self.converter.convert(SOURCE, output)
            manifest = json.loads(
                (output / "source-manifest.json").read_text(encoding="utf-8")
            )

        expected_key_points = []
        expected_groups = []
        expected_items = []
        for section in self.soup.select("section[id]"):
            section_id = section["id"]
            for point_index, point in enumerate(
                section.select(":scope > .kp > div"), start=1
            ):
                expected_key_points.append(
                    {
                        "source_id": f"{section_id}-kp{point_index:02d}",
                        "source_section_id": section_id,
                        "code": normalize_text(point.select_one(":scope > .i").get_text()),
                        "text": normalize_text(point.select_one(":scope > .x").get_text()),
                    }
                )
            for group_index, group in enumerate(
                section.select(":scope > .grp"), start=1
            ):
                group_id = f"{section_id}-g{group_index:02d}"
                group_title = normalize_text(
                    group.select_one(":scope > .grp-hd h4").get_text()
                )
                description_node = group.select_one(":scope > .grp-bd > .grp-desc")
                figure_code_node = group.select_one(":scope > .grp-hd .fg")
                expected_groups.append(
                    {
                        "source_id": group_id,
                        "source_section_id": section_id,
                        "title": group_title,
                        "description": (
                            normalize_text(description_node.get_text())
                            if description_node
                            else ""
                        ),
                        "figure_code": (
                            normalize_text(figure_code_node.get_text())
                            if figure_code_node
                            else None
                        ),
                    }
                )
                for item_index, item in enumerate(
                    group.select(":scope > .grp-bd > .items > .item"), start=1
                ):
                    description = normalize_text(
                        item.select_one(":scope > .d").get_text()
                    )
                    expected_items.append(
                        {
                            "source_id": f"{group_id}-i{item_index:02d}",
                            "source_section_id": section_id,
                            "source_group_id": group_id,
                            "source_group": group_title,
                            "title": normalize_text(
                                item.select_one(":scope > .t").get_text()
                            ),
                            "description": description,
                            "description_status": (
                                "present_in_dom" if description else "empty_in_dom"
                            ),
                            "css_fallback": (
                                None if description else "Sẽ bổ sung chi tiết sau"
                            ),
                            "highlights": [
                                normalize_text(node.get_text())
                                for node in item.select(":scope > .hl > li")
                            ],
                        }
                    )

        self.assertEqual(manifest["records"]["key_points"], expected_key_points)
        self.assertEqual(manifest["records"]["groups"], expected_groups)
        self.assertEqual(manifest["records"]["items"], expected_items)

    def test_assets_manifest_and_links_are_valid(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "V5"
            self.converter.convert(SOURCE, output)
            manifest = json.loads(
                (output / "source-manifest.json").read_text(encoding="utf-8")
            )

            self.assertEqual(manifest["source"]["sha256"], EXPECTED_SOURCE_SHA256)
            self.assertEqual(manifest["coverage"]["sections"], 9)
            self.assertEqual(manifest["coverage"]["groups"], 29)
            self.assertEqual(manifest["coverage"]["items"], 115)
            self.assertEqual(manifest["coverage"]["figures"], 14)
            self.assertEqual(manifest["coverage"]["images"], 29)
            self.assertEqual(manifest["coverage"]["figure_placeholders"], 2)
            self.assertEqual(manifest["coverage"]["schedule_placeholders"], 1)
            self.assertEqual(len(manifest["assets"]), 29)
            self.assertEqual(manifest["coverage"]["figure_slots"], 15)
            self.assertEqual(manifest["coverage"]["key_points"], 20)
            self.assertEqual(manifest["coverage"]["group_descriptions"], 16)
            self.assertEqual(manifest["coverage"]["highlight_lists"], 35)
            self.assertEqual(manifest["coverage"]["highlight_bullets"], 91)
            self.assertEqual(
                manifest["coverage"]["dom_or_inline_hidden_elements"], 0
            )
            self.assertEqual(
                manifest["coverage"]["css_hidden_empty_descriptions"], 1
            )
            self.assertEqual(manifest["coverage"]["decoded_image_bytes"], 1872262)
            self.assertEqual(
                manifest["coverage"]["ordered_concatenated_image_sha256"],
                "69535d8f59b68a0b1cd99cd62e6a647c31f93e317cb36b1fe609169a848fdba4",
            )
            self.assertEqual(len(manifest["records"]["key_points"]), 20)
            self.assertEqual(len(manifest["records"]["groups"]), 29)
            self.assertEqual(len(manifest["records"]["items"]), 115)
            self.assertEqual(len(manifest["records"]["figures"]), 15)
            self.assertEqual(len(manifest["duplicate_descriptions"]), 3)
            self.assertEqual(
                {record["figure_code"] for record in manifest["records"]["figures"]},
                {f"FIG-{number:02d}" for number in range(15)},
            )

            for entry in manifest["assets"]:
                asset = output / entry["file"]
                payload = asset.read_bytes()
                self.assertTrue(payload.startswith(b"\xff\xd8\xff"), asset.name)
                self.assertEqual(len(payload), entry["bytes"])
                self.assertEqual(sha256_bytes(payload), entry["sha256"])
                self.assertGreater(entry["width"], 0)
                self.assertGreater(entry["height"], 0)

            widths = [entry["width"] for entry in manifest["assets"]]
            self.assertEqual(widths.count(720), 16)
            self.assertEqual(widths.count(1100), 13)

            item_records = manifest["records"]["items"]
            self.assertEqual(len({record["source_id"] for record in item_records}), 115)
            empty_record = next(
                record
                for record in item_records
                if record["title"] == "Đạo cụ lên kệ trên cửa hàng web"
            )
            self.assertEqual(empty_record["description"], "")
            self.assertEqual(empty_record["css_fallback"], "Sẽ bổ sung chi tiết sau")

            link_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
            all_link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
            for markdown in output.glob("*.md"):
                rendered = markdown.read_text(encoding="utf-8")
                h1_count = sum(1 for line in rendered.splitlines() if line.startswith("# "))
                self.assertEqual(h1_count, 1, markdown.name)
                for target in link_pattern.findall(rendered):
                    target = target.strip("<>")
                    self.assertTrue((markdown.parent / target).is_file(), target)
                for target in all_link_pattern.findall(rendered):
                    target = target.strip("<>")
                    if "://" not in target and not target.startswith("#"):
                        self.assertTrue((markdown.parent / target).is_file(), target)

            notes = (output / "doc-v5-11-ghi-chu-va-truy-nguyen.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("47", notes)
            self.assertIn("46", notes)
            self.assertIn("Sẽ bổ sung chi tiết sau", notes)


if __name__ == "__main__":
    unittest.main()
