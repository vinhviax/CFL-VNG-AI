#!/usr/bin/env python3

"""Recover the missing handbook master from the released generated modules.

This is intentionally conservative: it refuses to overwrite an existing master
and writes only after a temporary round-trip reproduces every module, allowing
only the two path changes required by the new workspace layout.
"""

import json
import re
import tempfile
from pathlib import Path

import build_handbook


GENERATED_HEADER_RE = re.compile(
    r"\A<!-- GENERATED FILE - sửa nội dung tại so-tay-tao-knowledge-base-v3\.md -->\n\n"
)
LOCAL_ASSET_RE = re.compile(r"^<!-- LOCAL_ASSET: .*? -->\n?", re.MULTILINE)


def demote_headings(source):
    rendered = []
    fence = None
    for line in source.splitlines(keepends=True):
        marker = build_handbook._fence_marker(line)
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
        elif fence is None and re.match(r"^#{1,5}\s+", line):
            line = "#" + line
        rendered.append(line)
    return "".join(rendered)


def recover_module_body(rendered, uri_to_filename):
    body, replacements = GENERATED_HEADER_RE.subn("", rendered, count=1)
    if replacements != 1:
        raise ValueError("Module does not have the expected generated header")
    body = LOCAL_ASSET_RE.sub("", body)
    body = body.replace("](../audit/", "](audit/")

    def restore_image(match):
        source = match.group("src").strip().strip("<>")
        filename = uri_to_filename.get(source)
        if not filename:
            raise ValueError(f"Image URI is not present in image-map.json: {source}")
        path = (
            f"{build_handbook.KNOWLEDGE_DIR_NAME}/"
            f"{build_handbook.ASSET_KB_NAME}/{filename}"
        )
        return f"![{match.group('alt')}](<{path}>)"

    body = build_handbook.replace_images_outside_fences(body, restore_image)
    return demote_headings(body).strip()


def expected_after_layout_change(rendered):
    return (
        rendered.replace(
            "<!-- LOCAL_ASSET: assets/",
            f"<!-- LOCAL_ASSET: ../{build_handbook.ASSET_KB_NAME}/",
        )
        .replace("](../audit/", "](../../audit/")
    )


def main():
    root = Path(__file__).resolve().parents[1]
    master = root / "so-tay-tao-knowledge-base-v3.md"
    if master.exists():
        raise FileExistsError(f"Refusing to overwrite existing master: {master}")

    consumer = (
        root
        / build_handbook.KNOWLEDGE_DIR_NAME
        / build_handbook.CONSUMER_KB_NAME
    )
    image_map_path = consumer / "image-map.json"
    payload = json.loads(image_map_path.read_text(encoding="utf-8"))
    image_map = payload["images"]
    uri_to_filename = {uri: filename for filename, uri in image_map.items()}
    if len(uri_to_filename) != len(image_map):
        raise ValueError("image-map.json contains duplicate MinIO URIs")

    module_paths = sorted(consumer.glob("[0-1][0-9]-*.md"))
    if len(module_paths) != build_handbook.EXPECTED_MODULE_COUNT:
        raise ValueError(
            f"Expected {build_handbook.EXPECTED_MODULE_COUNT} modules, "
            f"found {len(module_paths)}"
        )

    blocks = []
    current = {}
    for module_path in module_paths:
        rendered = module_path.read_text(encoding="utf-8")
        current[module_path.name] = rendered
        body = recover_module_body(rendered, uri_to_filename)
        blocks.append(
            f"<!-- MODULE:{module_path.name} -->\n"
            f"{body}\n"
            "<!-- /MODULE -->"
        )

    intro = """# Sổ tay tạo và vận hành Knowledge Base & Agent

> Phiên bản: 3.3.0
> Cập nhật: 11/08/2026

Tài liệu chuẩn để tạo, kiểm thử và vận hành Knowledge Base cùng Agent trên VNG AI. Nội dung nghiệp vụ nằm trong 20 module dưới đây; các file Markdown phân phối và HTML offline được sinh bằng builder.
"""
    source = intro.rstrip() + "\n\n" + "\n\n".join(blocks) + "\n"

    temp_root = root / ".codex-tmp"
    temp_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as folder:
        outputs = build_handbook.write_modules(
            source,
            Path(folder),
            image_map,
            require_minio=True,
            source_root=root,
            local_asset_prefix=f"../{build_handbook.ASSET_KB_NAME}",
        )
        for output in outputs:
            actual = output.read_text(encoding="utf-8")
            expected = expected_after_layout_change(current[output.name])
            if actual != expected:
                raise ValueError(f"Round-trip mismatch for {output.name}")

    master.write_text(source, encoding="utf-8", newline="\n")
    print(f"Recovered {master}")
    print(f"- Modules: {len(module_paths)}")
    print(f"- Image mappings: {len(image_map)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
