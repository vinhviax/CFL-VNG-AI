#!/usr/bin/env python3
"""Convert the audited CFL 5.0 HTML whitepaper into a deterministic KB bundle."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag


EXPECTED_SOURCE_SHA256 = (
    "593c34283ddd16f4a751b8ab4aa16bb8a2c6581f69ac2d0376042c1de86ef038"
)
EXPECTED_CONTRACT = {
    "section_count": 9,
    "group_count": 29,
    "item_count": 115,
    "figure_count": 14,
    "image_count": 29,
    "placeholder_count": 2,
    "schedule_placeholder_count": 1,
    "dom_or_inline_hidden_element_count": 0,
}
VERSION_TAG = "v5"
SECTION_MODULES = {
    "ov": f"doc-{VERSION_TAG}-01-tong-quan-phien-ban.md",
    "sched": f"doc-{VERSION_TAG}-02-lich-trinh-phien-ban.md",
    "gameplay": f"doc-{VERSION_TAG}-03-cach-choi-moi.md",
    "system": f"doc-{VERSION_TAG}-04-he-thong-moi.md",
    "quality": f"doc-{VERSION_TAG}-05-nang-cao-chat-luong.md",
    "supply": f"doc-{VERSION_TAG}-06-tiep-te-moi.md",
    "act": f"doc-{VERSION_TAG}-07-hoat-dong-tang-do-hoat-dong.md",
    "biz": f"doc-{VERSION_TAG}-08-hoat-dong-thuong-mai-hoa.md",
    "pub": f"doc-{VERSION_TAG}-09-ban-dia-hoa-va-phat-hanh.md",
}
INDEX_MODULE = f"doc-{VERSION_TAG}-00-index-va-pham-vi.md"
IMAGE_CATALOG_MODULE = f"doc-{VERSION_TAG}-10-danh-muc-hinh-anh.md"
NOTES_MODULE = f"doc-{VERSION_TAG}-11-ghi-chu-va-truy-nguyen.md"
MANIFEST_FILE = "source-manifest.json"


def normalize_text(value: Tag | str | None) -> str:
    """Return visible text with layout whitespace collapsed, without rewriting words."""
    if value is None:
        return ""
    if isinstance(value, Tag):
        value = value.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", str(value)).strip()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_source(source_path: Path) -> tuple[bytes, BeautifulSoup]:
    payload = source_path.read_bytes()
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Source is not valid UTF-8: {source_path}") from exc
    return payload, BeautifulSoup(decoded, "html.parser")


def extract_css_empty_description_fallback(soup: BeautifulSoup) -> str:
    style_text = "\n".join(node.get_text() for node in soup.find_all("style"))
    match = re.search(
        r"\.item\.bare\s+\.d:after\s*\{[^}]*content\s*:\s*\"([^\"]+)\"",
        style_text,
        re.I,
    )
    return normalize_text(match.group(1)) if match else ""


def css_hides_empty_descriptions(soup: BeautifulSoup) -> bool:
    style_text = "\n".join(node.get_text() for node in soup.find_all("style"))
    return bool(
        re.search(
            r"\.item\s+\.d:empty\s*\{[^}]*display\s*:\s*none",
            style_text,
            re.I,
        )
    )


def inspect_source(source_path: str | Path) -> dict[str, Any]:
    source_path = Path(source_path)
    payload, soup = read_source(source_path)
    hidden_nodes: set[int] = set()
    for node in soup.select("[hidden]"):
        hidden_nodes.add(id(node))
    for node in soup.select("[style]"):
        style = node.get("style", "")
        if re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", style, re.I):
            hidden_nodes.add(id(node))

    return {
        "source_file": source_path.name,
        "source_bytes": len(payload),
        "source_sha256": sha256_bytes(payload),
        "document_title": normalize_text(soup.title),
        "section_count": len(soup.select("section[id]")),
        "group_count": len(soup.select(".grp")),
        "item_count": len(soup.select(".item")),
        "figure_count": len(soup.select("figure.fig")),
        "image_count": len(soup.select("figure.fig img")),
        "placeholder_count": len(soup.select("figure.fig .fig-ph")),
        "schedule_placeholder_count": len(soup.select("section#sched .ph")),
        "dom_or_inline_hidden_element_count": len(hidden_nodes),
        "highlight_count": len(soup.select(".item .hl li")),
        "highlight_list_count": len(soup.select(".item .hl")),
        "key_point_count": len(soup.select(".kp > div")),
        "group_description_count": len(soup.select(".grp-desc")),
        "empty_description_count": sum(
            not normalize_text(item.select_one(".d")) for item in soup.select(".item")
        ),
        "css_empty_description_fallback": extract_css_empty_description_fallback(
            soup
        ),
        "css_hidden_empty_description_count": (
            sum(not normalize_text(item.select_one(".d")) for item in soup.select(".item"))
            if css_hides_empty_descriptions(soup)
            else 0
        ),
    }


def validate_source_contract(inventory: dict[str, Any]) -> None:
    differences = []
    if inventory["source_sha256"] != EXPECTED_SOURCE_SHA256:
        differences.append(
            "source_sha256="
            f"{inventory['source_sha256']} (expected {EXPECTED_SOURCE_SHA256})"
        )
    for key, expected in EXPECTED_CONTRACT.items():
        actual = inventory[key]
        if actual != expected:
            differences.append(f"{key}={actual} (expected {expected})")
    if differences:
        raise ValueError(
            "Source HTML does not match the audited CFL 5.0 contract: "
            + "; ".join(differences)
        )


def slugify(value: str) -> str:
    value = value.replace("Đ", "D").replace("đ", "d")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "image"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_block(source_name: str, source_sha256: str, location: str) -> list[str]:
    return [
        "> **Phân loại:** Đã kiểm chứng trực tiếp từ HTML nguồn.",
        ">",
        f"> **Nguồn:** `{source_name}`",
        ">",
        f"> **SHA-256:** `{source_sha256}`",
        ">",
        f"> **Vị trí trong nguồn:** `{location}`",
    ]


def section_header(section: Tag) -> tuple[str, str]:
    number = normalize_text(section.select_one(":scope > .sec-hd .no"))
    title = normalize_text(section.select_one(":scope > .sec-hd h3"))
    if not number or not title:
        raise ValueError(f"Section header is incomplete: {section.get('id')}")
    return number, title


def display_section_heading(number: str, title: str) -> str:
    return title if number == "—" else f"{number} — {title}"


def decode_data_image(data_uri: str) -> tuple[str, bytes]:
    match = re.fullmatch(
        r"data:(image/[a-zA-Z0-9.+-]+);base64,([A-Za-z0-9+/=\r\n]+)",
        data_uri,
    )
    if not match:
        raise ValueError("Unsupported or malformed embedded image data URI")
    mime_type, encoded = match.groups()
    payload = base64.b64decode(encoded, validate=True)
    if mime_type != "image/jpeg" or not payload.startswith(b"\xff\xd8\xff"):
        raise ValueError(f"Expected a JPEG data URI, received {mime_type}")
    return mime_type, payload


def jpeg_dimensions(payload: bytes) -> tuple[int, int]:
    """Read JPEG dimensions without recompressing the image or requiring Pillow."""
    if not payload.startswith(b"\xff\xd8"):
        raise ValueError("JPEG payload is missing SOI marker")
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    offset = 2
    while offset < len(payload):
        while offset < len(payload) and payload[offset] != 0xFF:
            offset += 1
        while offset < len(payload) and payload[offset] == 0xFF:
            offset += 1
        if offset >= len(payload):
            break
        marker = payload[offset]
        offset += 1
        if marker in {0x01, *range(0xD0, 0xD9)}:
            continue
        if offset + 2 > len(payload):
            break
        segment_length = int.from_bytes(payload[offset : offset + 2], "big")
        if segment_length < 2 or offset + segment_length > len(payload):
            raise ValueError("Malformed JPEG segment")
        if marker in sof_markers:
            if segment_length < 7:
                raise ValueError("Malformed JPEG SOF segment")
            height = int.from_bytes(payload[offset + 3 : offset + 5], "big")
            width = int.from_bytes(payload[offset + 5 : offset + 7], "big")
            return width, height
        offset += segment_length
    raise ValueError("JPEG dimensions could not be determined")


def extract_assets(
    soup: BeautifulSoup, output_dir: Path
) -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    # Từ 16/08/2026 ảnh nằm thẳng trong thư mục bundle, không còn `assets/`
    # riêng — khớp với `link_plan_v5_minio.py` và bố cục ảnh thật trên đĩa.
    assets_dir = output_dir
    assets_dir.mkdir(parents=True, exist_ok=True)
    images_by_tag: dict[int, dict[str, Any]] = {}
    manifest_assets: list[dict[str, Any]] = []
    ordered_hasher = hashlib.sha256()
    decoded_bytes = 0

    for index, image in enumerate(soup.select("figure.fig img"), start=1):
        section = image.find_parent("section")
        group = image.find_parent(class_="grp")
        figure = image.find_parent("figure")
        if section is None or group is None or figure is None:
            raise ValueError(f"Image {index} is outside the expected section/group/figure")

        alt_text = normalize_text(image.get("alt", ""))
        shot_caption = normalize_text(image.find_next_sibling(class_="shc"))
        figure_caption = normalize_text(figure.find("figcaption"))
        figure_code = normalize_text(figure.select_one(".fgc"))
        if not figure_code:
            figure_code = normalize_text(group.select_one(":scope > .grp-hd .fg"))
        group_title = normalize_text(group.select_one(":scope > .grp-hd h4"))
        mime_type, payload = decode_data_image(image.get("src", ""))
        width, height = jpeg_dimensions(payload)
        filename = f"image-{VERSION_TAG}-{index:02d}-{slugify(alt_text)}.jpg"
        relative_path = filename
        target = output_dir / relative_path
        target.write_bytes(payload)
        record = {
            "index": index,
            "file": relative_path,
            "mime_type": mime_type,
            "bytes": len(payload),
            "sha256": sha256_bytes(payload),
            "width": width,
            "height": height,
            "alt_text": alt_text,
            "source_caption": shot_caption,
            "figure_code": figure_code,
            "figure_caption": figure_caption,
            "source_section_id": section.get("id"),
            "source_group": group_title,
        }
        images_by_tag[id(image)] = record
        manifest_assets.append(record)
        ordered_hasher.update(payload)
        decoded_bytes += len(payload)

    summary = {
        "decoded_image_bytes": decoded_bytes,
        "ordered_concatenated_image_sha256": ordered_hasher.hexdigest(),
    }
    return images_by_tag, manifest_assets, summary


def render_index(
    soup: BeautifulSoup,
    inventory: dict[str, Any],
    module_entries: list[dict[str, Any]],
) -> str:
    cover = soup.select_one(".cover")
    if cover is None:
        raise ValueError("Missing .cover block")
    tag = normalize_text(cover.select_one(".tag"))
    title = normalize_text(cover.find("h1"))
    subtitle = normalize_text(cover.find("h2"))
    lines = [
        f"# Knowledge Base — {title}",
        "",
        *source_block(
            inventory["source_file"], inventory["source_sha256"], ".cover"
        ),
        "",
        f"**Nhãn tài liệu trong nguồn:** {tag}",
        "",
        f"**Tiêu đề tài liệu trong nguồn:** {title}",
        "",
        f"**Sản phẩm/phạm vi trong nguồn:** {subtitle}",
        "",
        "## Thông tin phiên bản",
        "",
        "| Thuộc tính | Giá trị từ nguồn |",
        "|---|---|",
    ]
    for row in cover.select(".meta > div"):
        key = normalize_text(row.select_one(":scope > .k"))
        value = normalize_text(row.select_one(":scope > .v"))
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Cách dùng bộ Knowledge Base",
            "",
            "Bộ tài liệu này chia nội dung theo đúng chín section của HTML nguồn. "
            "Khi trả lời, ưu tiên module chuyên đề tương ứng và dẫn lại tên nhóm, "
            "tên hạng mục hoặc mã FIG để người dùng kiểm tra ngược.",
            "",
            "| Module | Phạm vi | Section nguồn |",
            "|---|---|---|",
        ]
    )
    lines.append(f"| [{INDEX_MODULE}]({INDEX_MODULE}) | Chỉ mục và phạm vi | `.cover` |")
    for entry in module_entries:
        lines.append(
            f"| [{entry['file']}]({entry['file']}) | "
            f"{display_section_heading(entry['section_number'], entry['section_title'])} "
            f"| `section#{entry['source_section_id']}` |"
        )
    lines.append(
        f"| [{IMAGE_CATALOG_MODULE}]({IMAGE_CATALOG_MODULE}) | Danh mục FIG và 29 ảnh JPEG | `section#sched`, `figure.fig` |"
    )
    lines.append(
        f"| [{NOTES_MODULE}]({NOTES_MODULE}) | Ghi chú nguồn, giới hạn và truy nguyên | `.note`, `footer` |"
    )
    lines.extend(
        [
            "",
            "## Độ phủ trích xuất",
            "",
            f"- Section: {inventory['section_count']}/9.",
            f"- Nhóm nội dung: {inventory['group_count']}/29.",
            f"- Hạng mục: {inventory['item_count']}/115.",
            f"- Figure: {inventory['figure_count']}/14.",
            f"- Ảnh JPEG nhúng đã tách: {inventory['image_count']}/29.",
            f"- Placeholder figure chưa có ảnh: {inventory['placeholder_count']}.",
            f"- Placeholder lịch trình: {inventory['schedule_placeholder_count']}.",
            f"- Mô tả hạng mục trống trong nguồn: {inventory['empty_description_count']}.",
            "",
            "## Giới hạn sử dụng",
            "",
            "Đây là bản chuyển đổi trung thực của HTML nguồn, không phải xác nhận "
            "rằng mọi nội dung đã được triển khai live. Các vị trí ghi “sẽ bổ sung sau” "
            "vẫn được giữ nguyên và phải được xem là chưa xác định cho đến khi có nguồn mới.",
        ]
    )
    return "\n".join(lines)


def render_overview(section: Tag, inventory: dict[str, Any]) -> str:
    number, title = section_header(section)
    lines = [
        f"# {number} — {title}",
        "",
        *source_block(
            inventory["source_file"],
            inventory["source_sha256"],
            f"section#{section['id']}",
        ),
        "",
        "## Thông điệp tổng quan",
        "",
    ]
    for node in section.select(".ov-slogan > div"):
        lines.append(f"- {normalize_text(node)}")

    lines.extend(
        [
            "",
            "## Tài nguyên và chủ đề trọng tâm",
            "",
            "| Nhóm | Nội dung từ nguồn |",
            "|---|---|",
        ]
    )
    for row in section.select(".ov-res > div"):
        key = normalize_text(row.select_one(":scope > .k"))
        value = normalize_text(row.select_one(":scope > .v"))
        lines.append(f"| {key} | {value} |")

    viz = section.select_one(".viz")
    if viz:
        lines.extend(
            [
                "",
                "## Nhịp vận hành",
                "",
                normalize_text(viz.find("h6")),
                "",
                "### Các chặng chủ đề",
                "",
            ]
        )
        for node in viz.select(".tl-bar > div"):
            lines.append(f"- {normalize_text(node)}")
        flex_weights = []
        for node in viz.select(".tl-bar > div"):
            match = re.search(r"(?:^|;)\s*flex\s*:\s*([0-9.]+)", node.get("style", ""))
            if match:
                flex_weights.append(match.group(1))
        if flex_weights:
            lines.extend(
                [
                    "",
                    "**Trọng số bố cục CSS trong nguồn:** "
                    + " / ".join(flex_weights)
                    + " (chỉ là tỷ trọng hiển thị, không phải KPI vận hành).",
                ]
            )
        lines.extend(["", "### Mốc biên", ""])
        for node in viz.select(".tl-lbl > span"):
            lines.append(f"- {normalize_text(node)}")
    return "\n".join(lines)


def render_schedule(section: Tag, inventory: dict[str, Any]) -> str:
    number, title = section_header(section)
    placeholder = section.select_one(".ph")
    if placeholder is None:
        raise ValueError("Expected the audited schedule placeholder")
    code = normalize_text(placeholder.select_one(".c"))
    placeholder_title = normalize_text(placeholder.select_one(".t"))
    status = normalize_text(placeholder.select_one(".s"))
    return "\n".join(
        [
            f"# {display_section_heading(number, title)}",
            "",
            *source_block(
                inventory["source_file"],
                inventory["source_sha256"],
                f"section#{section['id']}",
            ),
            "",
            f"**Ký hiệu section trong nguồn:** {number}",
            "",
            "## Nội dung hiện có trong nguồn",
            "",
            f"**{code}**",
            "",
            placeholder_title,
            "",
            status,
            "",
            "> **Bị chặn — Chưa xác định:** HTML nguồn chưa chứa sơ đồ hay "
            "thời gian lên sóng chi tiết cho từng nội dung. Không tự suy diễn lịch.",
        ]
    )


def render_figure(
    figure: Tag, images_by_tag: dict[int, dict[str, Any]]
) -> list[str]:
    lines: list[str] = []
    placeholder = figure.select_one(".fig-ph")
    if placeholder:
        code = normalize_text(placeholder.select_one(".code"))
        placeholder_text = normalize_text(placeholder.select_one(".tx"))
        lines.extend(
            [
                f"**{code}**",
                "",
                placeholder_text,
                "",
                "> **Bị chặn — Chưa xác định:** figure này chưa có ảnh trong HTML nguồn.",
            ]
        )
        return lines

    for shot in figure.select(".shot > .sh"):
        image = shot.find("img")
        if image is None or id(image) not in images_by_tag:
            raise ValueError("Figure image was not extracted")
        image_record = images_by_tag[id(image)]
        alt_text = normalize_text(image.get("alt", ""))
        caption = normalize_text(shot.select_one(".shc"))
        lines.extend(
            [
                f"![{alt_text}]({image_record['file']})",
                "",
                f"*Chú thích ảnh trong nguồn: {caption}*",
                "",
            ]
        )
    figure_caption = normalize_text(figure.find("figcaption"))
    if figure_caption:
        lines.append(f"> **Chú thích cụm hình trong nguồn:** {figure_caption}")
    return lines


def render_content_section(
    section: Tag,
    inventory: dict[str, Any],
    images_by_tag: dict[int, dict[str, Any]],
) -> str:
    number, title = section_header(section)
    lines = [
        f"# {number} — {title}",
        "",
        *source_block(
            inventory["source_file"],
            inventory["source_sha256"],
            f"section#{section['id']}",
        ),
    ]
    intro = normalize_text(section.select_one(":scope > .sec-intro"))
    if intro:
        lines.extend(["", "## Mở đầu từ nguồn", "", intro])

    key_points = section.select(":scope > .kp > div")
    if key_points:
        lines.extend(["", "## Điểm chính", ""])
        for point in key_points:
            code = normalize_text(point.select_one(":scope > .i"))
            value = normalize_text(point.select_one(":scope > .x"))
            lines.append(f"- **{code}** — {value}")

    for group_index, group in enumerate(section.select(":scope > .grp"), start=1):
        title_node = group.select_one(":scope > .grp-hd h4")
        group_title = normalize_text(title_node)
        if not group_title:
            raise ValueError(f"Group {group_index} in {section['id']} has no title")
        lines.extend(["", f"## {group_title}", ""])
        lines.extend(
            [f"**ID nhóm nguồn:** `{section['id']}-g{group_index:02d}`", ""]
        )
        figure_code = normalize_text(group.select_one(":scope > .grp-hd .fg"))
        if figure_code:
            lines.extend([f"**Mã figure trong nguồn:** {figure_code}", ""])
        description = normalize_text(group.select_one(":scope > .grp-bd > .grp-desc"))
        if description:
            lines.extend([description, ""])

        figure = group.select_one(":scope > .grp-bd > figure.fig")
        if figure:
            lines.extend(render_figure(figure, images_by_tag))
            lines.append("")

        items = group.select(":scope > .grp-bd > .items > .item")
        for item_index, item in enumerate(items, start=1):
            item_title = normalize_text(item.select_one(":scope > .t"))
            item_description = normalize_text(item.select_one(":scope > .d"))
            source_id = f"{section['id']}-g{group_index:02d}-i{item_index:02d}"
            lines.extend([f"### {item_index}. {item_title}", ""])
            lines.extend([f"**ID nguồn:** `{source_id}`", ""])
            if item_description:
                lines.extend([item_description, ""])
            else:
                lines.extend(
                    [
                        "> **Bị chặn — Chưa xác định:** Không có mô tả trong nguồn HTML.",
                        "",
                        "> **Fallback có điều kiện khai báo trong CSS nguồn:** "
                        f"{inventory['css_empty_description_fallback']}",
                        "",
                        "> Ghi chú kỹ thuật: `.item .d:empty` đồng thời bị đặt "
                        "`display:none`; vì vậy không xem fallback CSS là mô tả DOM đã kiểm chứng.",
                        "",
                    ]
                )
            highlights = item.select(":scope > .hl > li")
            if highlights:
                lines.extend(["**Chi tiết bổ sung từ nguồn:**", ""])
                for highlight in highlights:
                    lines.append(f"- {normalize_text(highlight)}")
                lines.append("")
    return "\n".join(lines)


def build_semantic_records(
    soup: BeautifulSoup,
    images_by_tag: dict[int, dict[str, Any]],
    css_fallback: str,
) -> dict[str, list[dict[str, Any]]]:
    records: dict[str, list[dict[str, Any]]] = {
        "key_points": [],
        "groups": [],
        "items": [],
        "figures": [],
    }

    schedule = soup.select_one("section#sched .ph")
    if schedule is None:
        raise ValueError("Missing FIG-00 schedule placeholder")
    records["figures"].append(
        {
            "source_order": 1,
            "source_id": "sched-fig-00",
            "figure_code": normalize_text(schedule.select_one(".c")),
            "status": "schedule_placeholder",
            "source_section_id": "sched",
            "source_group_id": None,
            "source_group": None,
            "image_indices": [],
            "caption": "",
            "placeholder_title": normalize_text(schedule.select_one(".t")),
            "placeholder_detail": normalize_text(schedule.select_one(".s")),
        }
    )

    figure_order = 1
    for section in soup.select("section[id]"):
        section_id = section["id"]
        for key_point_index, point in enumerate(
            section.select(":scope > .kp > div"), start=1
        ):
            records["key_points"].append(
                {
                    "source_id": f"{section_id}-kp{key_point_index:02d}",
                    "source_section_id": section_id,
                    "code": normalize_text(point.select_one(":scope > .i")),
                    "text": normalize_text(point.select_one(":scope > .x")),
                }
            )

        for group_index, group in enumerate(
            section.select(":scope > .grp"), start=1
        ):
            group_id = f"{section_id}-g{group_index:02d}"
            group_title = normalize_text(group.select_one(":scope > .grp-hd h4"))
            group_description = normalize_text(
                group.select_one(":scope > .grp-bd > .grp-desc")
            )
            figure = group.select_one(":scope > .grp-bd > figure.fig")
            group_figure_code = normalize_text(
                group.select_one(":scope > .grp-hd .fg")
            )
            records["groups"].append(
                {
                    "source_id": group_id,
                    "source_section_id": section_id,
                    "title": group_title,
                    "description": group_description,
                    "figure_code": group_figure_code or None,
                }
            )

            for item_index, item in enumerate(
                group.select(":scope > .grp-bd > .items > .item"), start=1
            ):
                description = normalize_text(item.select_one(":scope > .d"))
                records["items"].append(
                    {
                        "source_id": f"{group_id}-i{item_index:02d}",
                        "source_section_id": section_id,
                        "source_group_id": group_id,
                        "source_group": group_title,
                        "title": normalize_text(item.select_one(":scope > .t")),
                        "description": description,
                        "description_status": (
                            "present_in_dom" if description else "empty_in_dom"
                        ),
                        "css_fallback": css_fallback if not description else None,
                        "highlights": [
                            normalize_text(highlight)
                            for highlight in item.select(":scope > .hl > li")
                        ],
                    }
                )

            if figure:
                figure_order += 1
                placeholder = figure.select_one(".fig-ph")
                code = normalize_text(figure.select_one(".fgc"))
                if not code and placeholder:
                    code = normalize_text(placeholder.select_one(".code"))
                if not code:
                    code = group_figure_code
                image_indices = [
                    images_by_tag[id(image)]["index"] for image in figure.select("img")
                ]
                records["figures"].append(
                    {
                        "source_order": figure_order,
                        "source_id": f"{group_id}-fig",
                        "figure_code": code,
                        "status": (
                            "figure_placeholder" if placeholder else "embedded_images"
                        ),
                        "source_section_id": section_id,
                        "source_group_id": group_id,
                        "source_group": group_title,
                        "image_indices": image_indices,
                        "caption": normalize_text(figure.find("figcaption")),
                        "placeholder_title": (
                            normalize_text(placeholder.select_one(".tx b"))
                            if placeholder
                            else ""
                        ),
                        "placeholder_detail": (
                            normalize_text(placeholder.select_one(".tx"))
                            if placeholder
                            else ""
                        ),
                    }
                )
    return records


def markdown_cell(value: Any) -> str:
    return normalize_text(str(value)).replace("|", "\\|")


def render_image_catalog(
    inventory: dict[str, Any],
    records: dict[str, list[dict[str, Any]]],
    assets: list[dict[str, Any]],
) -> str:
    lines = [
        "# Danh Mục Hình Ảnh Và Figure",
        "",
        *source_block(
            inventory["source_file"],
            inventory["source_sha256"],
            "section#sched, figure.fig",
        ),
        "",
        "## Registry figure theo thứ tự DOM nguồn",
        "",
        "Nguồn có 15 mã liên tục từ FIG-00 đến FIG-14. Thứ tự dưới đây giữ "
        "nguyên thứ tự xuất hiện trong DOM, vì FIG-14 xuất hiện trước FIG-10.",
        "",
        "| Thứ tự nguồn | Mã FIG | Trạng thái | Section | Nhóm | Số ảnh | Chú thích/nội dung chờ |",
        "|---:|---|---|---|---|---:|---|",
    ]
    status_labels = {
        "schedule_placeholder": "Bị chặn — chưa có lịch",
        "figure_placeholder": "Bị chặn — chưa có ảnh",
        "embedded_images": "Đã kiểm chứng — có ảnh nhúng",
    }
    for figure in records["figures"]:
        detail = figure["caption"] or figure["placeholder_detail"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(figure["source_order"]),
                    markdown_cell(figure["figure_code"]),
                    markdown_cell(status_labels[figure["status"]]),
                    f"`{figure['source_section_id']}`",
                    markdown_cell(figure["source_group"] or "—"),
                    str(len(figure["image_indices"])),
                    markdown_cell(detail),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Registry 29 ảnh JPEG đã tách lossless",
            "",
            "Mỗi asset dưới đây là byte JPEG giải mã trực tiếp từ data-URI; không "
            "resize và không nén lại.",
        ]
    )
    for asset in assets:
        lines.extend(
            [
                "",
                f"### {asset['index']:02d}. {asset['alt_text']}",
                "",
                f"- **FIG:** {asset['figure_code']}.",
                f"- **Section / nhóm nguồn:** `{asset['source_section_id']}` / {asset['source_group']}.",
                f"- **Kích thước:** {asset['width']} × {asset['height']} px.",
                f"- **Dung lượng:** {asset['bytes']} byte.",
                f"- **SHA-256:** `{asset['sha256']}`.",
                f"- **Chú thích ảnh trong nguồn:** {asset['source_caption']}.",
                f"- **Chú thích cụm hình trong nguồn:** {asset['figure_caption']}.",
                f"- **Asset:** [{asset['file']}]({asset['file']}).",
            ]
        )
    return "\n".join(lines)


def duplicate_descriptions(soup: BeautifulSoup) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for section in soup.select("section[id]"):
        for group in section.select(":scope > .grp"):
            group_title = normalize_text(group.select_one(":scope > .grp-hd h4"))
            for item in group.select(":scope > .grp-bd > .items > .item"):
                description = normalize_text(item.select_one(":scope > .d"))
                if not description:
                    continue
                groups[description].append(
                    {
                        "source_section_id": section["id"],
                        "source_group": group_title,
                        "item_title": normalize_text(item.select_one(":scope > .t")),
                    }
                )
    return [
        {"description": description, "occurrences": occurrences}
        for description, occurrences in groups.items()
        if len(occurrences) > 1
    ]


def render_notes(soup: BeautifulSoup, inventory: dict[str, Any]) -> str:
    note = soup.select_one(".note")
    footer = soup.find("footer")
    if note is None or footer is None:
        raise ValueError("Missing source note or footer")
    note_title = normalize_text(note.find("h5"))
    footer_text = normalize_text(footer)
    duplicates = duplicate_descriptions(soup)
    biz = soup.select_one("section#biz")
    biz_intro = normalize_text(biz.select_one(":scope > .sec-intro")) if biz else ""
    biz_item_count = len(biz.select(".item")) if biz else 0
    lines = [
        "# Ghi Chú Và Truy Nguyên",
        "",
        *source_block(
            inventory["source_file"],
            inventory["source_sha256"],
            ".note, footer",
        ),
        "",
        f"## {note_title}",
        "",
    ]
    for item in note.select("li"):
        lines.append(f"- {normalize_text(item)}")
    lines.extend(
        [
            "",
            "## Dòng chân trang của nguồn",
            "",
            footer_text,
            "",
            "## Quy tắc bảo toàn dữ liệu khi chuyển đổi",
            "",
            "- Giữ đủ 115 hạng mục theo đúng section, nhóm và thứ tự trong HTML.",
            "- Giữ nguyên các mô tả giống nhau thay vì tự gộp hoặc tự sửa.",
            "- Giữ nguyên 91 gạch đầu dòng chi tiết nằm trong 35 hạng mục có danh sách bổ sung.",
            "- Chỉ chuẩn hóa khoảng trắng do bố cục HTML; không đổi từ ngữ hoặc số liệu.",
            "- Tách 29 data-URI JPEG thành asset cục bộ và ghi checksum từng ảnh trong manifest.",
            "- Ba vị trí đang chờ hình/lịch (FIG-00, FIG-11, FIG-12) được giữ là “Bị chặn — Chưa xác định”.",
            "",
            "## Dữ kiện CSS có điều kiện",
            "",
            "Hạng mục `Đạo cụ lên kệ trên cửa hàng web` có node mô tả rỗng trong DOM. "
            "Stylesheet nguồn khai báo fallback: "
            f"**{inventory['css_empty_description_fallback']}**. Tuy nhiên selector "
            "`.item .d:empty` cũng đặt node này thành `display:none`, nên fallback được "
            "lưu để bảo toàn dữ liệu nhưng không được xem là mô tả DOM đã hiển thị chắc chắn.",
            "",
            "## Chênh lệch số lượng trong chính nguồn",
            "",
            f"- Mở đầu section thương mại hóa ghi nguyên văn: {biz_intro}",
            f"- Cùng section đó có **{biz_item_count}** thẻ `.item` trong DOM, trong khi phần mở đầu nêu **47** nội dung.",
            "- Hai dữ kiện được giữ song song; không tự suy diễn rằng một thẻ luôn tương ứng đúng một nội dung thương mại hóa.",
            "",
            "## Bản ghi có mô tả trùng trong nguồn",
            "",
            f"Phát hiện {len(duplicates)} nhóm mô tả xuất hiện nhiều hơn một lần. "
            "Các bản ghi này vẫn được giữ nguyên; xem `source-manifest.json` để truy nguyên từng lần xuất hiện.",
        ]
    )
    for duplicate in duplicates:
        titles = [item["item_title"] for item in duplicate["occurrences"]]
        lines.append("- " + " ↔ ".join(titles))
    lines.extend(
        [
            "",
            "## Phạm vi chưa thực hiện",
            "",
            "- Chưa upload bộ tài liệu này lên VNG AI Knowledge Base.",
            "- Chưa bind bộ tài liệu với Agent nào.",
            "- Không xác nhận trạng thái live của các hạng mục; tài liệu chỉ phản ánh HTML nguồn.",
        ]
    )
    return "\n".join(lines)


def build_module_entries(soup: BeautifulSoup) -> list[dict[str, Any]]:
    entries = []
    for section in soup.select("section[id]"):
        section_id = section["id"]
        if section_id not in SECTION_MODULES:
            raise ValueError(f"No module mapping for section#{section_id}")
        number, title = section_header(section)
        entries.append(
            {
                "file": SECTION_MODULES[section_id],
                "source_section_id": section_id,
                "section_number": number,
                "section_title": title,
                "groups": len(section.select(":scope > .grp")),
                "items": len(section.select(".item")),
                "figures": len(section.select("figure.fig")),
                "images": len(section.select("figure.fig img")),
                "placeholders": len(section.select(".fig-ph, :scope > .ph")),
            }
        )
    return entries


def build_manifest(
    inventory: dict[str, Any],
    module_entries: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    asset_summary: dict[str, Any],
    records: dict[str, list[dict[str, Any]]],
    soup: BeautifulSoup,
) -> dict[str, Any]:
    generated_files = [INDEX_MODULE]
    generated_files.extend(entry["file"] for entry in module_entries)
    generated_files.extend([IMAGE_CATALOG_MODULE, NOTES_MODULE, MANIFEST_FILE])
    generated_files.extend(asset["file"] for asset in assets)
    return {
        "schema_version": 1,
        "bundle_name": "GS9 CFL Plan Version / V5",
        "classification": "Đã kiểm chứng từ HTML nguồn",
        "source": {
            "file": inventory["source_file"],
            "sha256": inventory["source_sha256"],
            "bytes": inventory["source_bytes"],
            "encoding": "UTF-8",
            "document_title": inventory["document_title"],
            "date_from_source_filename": "2026-08-14",
        },
        "coverage": {
            "sections": inventory["section_count"],
            "groups": inventory["group_count"],
            "items": inventory["item_count"],
            "item_descriptions_nonempty": (
                inventory["item_count"] - inventory["empty_description_count"]
            ),
            "item_descriptions_empty": inventory["empty_description_count"],
            "key_points": inventory["key_point_count"],
            "group_descriptions": inventory["group_description_count"],
            "highlight_lists": inventory["highlight_list_count"],
            "highlight_bullets": inventory["highlight_count"],
            "figure_slots": len(records["figures"]),
            "figures": inventory["figure_count"],
            "figures_with_images": (
                inventory["figure_count"] - inventory["placeholder_count"]
            ),
            "figure_placeholders": inventory["placeholder_count"],
            "schedule_placeholders": inventory["schedule_placeholder_count"],
            "images": inventory["image_count"],
            "decoded_image_bytes": asset_summary["decoded_image_bytes"],
            "ordered_concatenated_image_sha256": asset_summary[
                "ordered_concatenated_image_sha256"
            ],
            "dom_or_inline_hidden_elements": inventory[
                "dom_or_inline_hidden_element_count"
            ],
            "css_hidden_empty_descriptions": inventory[
                "css_hidden_empty_description_count"
            ],
        },
        "modules": module_entries,
        "assets": assets,
        "records": records,
        "duplicate_descriptions": duplicate_descriptions(soup),
        "generated_files": generated_files,
    }


def cleanup_previous_generated_files(output_dir: Path) -> None:
    """Remove only files explicitly registered by a prior generated manifest."""
    manifest_path = output_dir / MANIFEST_FILE
    if not manifest_path.is_file():
        return
    try:
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    output_root = output_dir.resolve()
    registered = previous.get("generated_files", [])
    if not isinstance(registered, list):
        return
    for relative in registered:
        if not isinstance(relative, str):
            continue
        candidate = (output_dir / relative).resolve()
        if candidate != output_root and output_root not in candidate.parents:
            raise ValueError(f"Unsafe generated path in previous manifest: {relative}")
        if candidate.is_file():
            candidate.unlink()


def convert(source_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    source_path = Path(source_path)
    output_dir = Path(output_dir)
    inventory = inspect_source(source_path)
    validate_source_contract(inventory)
    _, soup = read_source(source_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    cleanup_previous_generated_files(output_dir)

    images_by_tag, assets, asset_summary = extract_assets(soup, output_dir)
    module_entries = build_module_entries(soup)
    records = build_semantic_records(
        soup,
        images_by_tag,
        inventory["css_empty_description_fallback"],
    )

    write_text(output_dir / INDEX_MODULE, render_index(soup, inventory, module_entries))
    for section in soup.select("section[id]"):
        section_id = section["id"]
        if section_id == "ov":
            rendered = render_overview(section, inventory)
        elif section_id == "sched":
            rendered = render_schedule(section, inventory)
        else:
            rendered = render_content_section(section, inventory, images_by_tag)
        write_text(output_dir / SECTION_MODULES[section_id], rendered)
    write_text(
        output_dir / IMAGE_CATALOG_MODULE,
        render_image_catalog(inventory, records, assets),
    )
    write_text(output_dir / NOTES_MODULE, render_notes(soup, inventory))

    manifest = build_manifest(
        inventory,
        module_entries,
        assets,
        asset_summary,
        records,
        soup,
    )
    write_text(
        output_dir / MANIFEST_FILE,
        json.dumps(manifest, ensure_ascii=False, indent=2),
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert the audited CFL 5.0 HTML whitepaper to a KB bundle."
    )
    parser.add_argument("source", type=Path, help="Path to the audited HTML source")
    parser.add_argument("output", type=Path, help="Destination KB directory")
    args = parser.parse_args()
    manifest = convert(args.source, args.output)
    coverage = manifest["coverage"]
    print(
        "Converted "
        f"{coverage['sections']} sections, {coverage['groups']} groups, "
        f"{coverage['items']} items, and {coverage['images']} images "
        f"to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
