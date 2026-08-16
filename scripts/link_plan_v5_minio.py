#!/usr/bin/env python3
"""Thay link ảnh cục bộ trong bundle CFL Plan Version 5 bằng URI MinIO của KB Web.

Bối cảnh
--------
`knowledge/GS9 CFL Plan Version/V5/*.md` do `scripts/convert_cfl_plan_html.py` sinh ra và
dùng đường dẫn tương đối `image-v5-XX-*.jpg`. Đường dẫn tương đối KHÔNG hoạt động
khi Markdown được nạp vào Knowledge Base trên Web — chat sẽ không render được ảnh.
Script này đọc `image-map.json` (filename -> URI MinIO) rồi viết lại link cho đúng,
theo cùng convention của bộ sổ tay: giữ một comment `LOCAL_ASSET` để truy nguyên file
cục bộ, và dùng URI MinIO cho link mà Web thực sự đọc.

CẢNH BÁO: 12 file `.md` là artifact sinh. Nếu chạy lại `convert_cfl_plan_html.py`,
link MinIO sẽ bị ghi đè về đường dẫn tương đối và phải chạy lại script này.

Script idempotent: chạy nhiều lần cho cùng kết quả, không nhân đôi comment
`LOCAL_ASSET` và không sửa link đã là `minio://`.

Dùng
----
    python scripts/link_plan_v5_minio.py --check    # chỉ kiểm tra, không ghi
    python scripts/link_plan_v5_minio.py            # ghi vào 12 file .md

Định dạng `image-map.json` mong đợi (giống `image-map.json` của sổ tay):

    {
      "generated_at": "2026-08-__",
      "knowledge_base": "GS9 CFL Plan Version",
      "knowledge_base_id": "1452bc9a-c8b4-487b-b623-34e0b00a83e9",
      "tenant_id": "10012",
      "images": {
        "image-01-....jpg": "minio://knowledge-base-prd/10012/exports/<uuid>.jpg",
        ...
      }
    }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "knowledge" / "GS9 CFL Plan Version" / "V5"
# Từ 16/08/2026 ảnh nằm thẳng trong V5/, không còn thư mục assets/ riêng.
ASSETS = BUNDLE
MAP_PATH = BUNDLE / "image-map.json"

KB_NAME = "GS9 CFL Plan Version"
KB_ID = "1452bc9a-c8b4-487b-b623-34e0b00a83e9"
TENANT_ID = "10012"
# Chấp nhận cả hai dạng URI hợp lệ (DEC-052): dạng `exports/<uuid>` cũ và dạng
# `file_path` mới `<knowledge_id>/<uuid>` lấy qua API — cả hai đã kiểm chứng
# render đúng, nên chỉ khoá tới phần tenant.
URI_PREFIX = f"minio://knowledge-base-prd/{TENANT_ID}/"

# ![alt](name.jpg) hoặc ![alt](assets/name.jpg) — ảnh nhúng, sẽ render trong chat.
# Vẫn nhận dạng tiền tố `assets/` cũ để bundle sinh trước 16/08 chạy lại được.
EMBED_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?:assets/)?(?P<name>image-v5-[^)/]+)\)")
# [text](name.jpg)  — link tham chiếu trong registry ảnh (file 10)
LINK_RE = re.compile(
    r"(?<!!)\[(?P<text>[^\]]*)\]\((?:assets/)?(?P<name>image-v5-[^)/]+)\)"
)

LOCAL_ASSET_TMPL = "<!-- LOCAL_ASSET: {name} -->"


class MapError(RuntimeError):
    """image-map.json thiếu, sai định dạng hoặc không phủ đủ asset."""


def load_map(strict: bool = True) -> dict[str, str]:
    """Đọc và kiểm tra image-map.json. Trả về dict filename -> URI MinIO."""
    if not MAP_PATH.exists():
        raise MapError(
            f"Chưa có {MAP_PATH.relative_to(ROOT)}.\n"
            "Phải upload 29 ảnh lên KB Web, lấy URI MinIO từng ảnh rồi ghi map trước.\n"
            "Quy trình lấy URI: docs/superpowers/plans/2026-08-07-image-assets-kb-migration-plan.md (Task 4 Step 2)."
        )

    payload = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    images = payload.get("images")
    if not isinstance(images, dict) or not images:
        raise MapError("image-map.json phải có khóa 'images' là dict không rỗng.")

    if payload.get("knowledge_base_id") != KB_ID:
        raise MapError(
            f"knowledge_base_id phải là {KB_ID} ({KB_NAME}), "
            f"đang là {payload.get('knowledge_base_id')!r}."
        )

    on_disk = {p.name for p in sorted(ASSETS.glob("*.jpg"))}
    missing = sorted(on_disk - set(images))
    extra = sorted(set(images) - on_disk)
    if strict and missing:
        raise MapError(f"{len(missing)} asset chưa có URI: {missing[:5]}...")
    if extra:
        raise MapError(f"Map có {len(extra)} tên không tồn tại trong V5/: {extra[:5]}")

    bad = [u for u in images.values() if not u.startswith(URI_PREFIX)]
    if bad:
        raise MapError(f"{len(bad)} URI không đúng tiền tố {URI_PREFIX}: {bad[:3]}")

    dupes = len(images) - len(set(images.values()))
    if dupes:
        raise MapError(f"Có {dupes} URI bị trùng; mỗi ảnh phải có URI riêng.")

    return images


def rewrite_text(text: str, images: dict[str, str]) -> tuple[str, int, int, list[str]]:
    """Trả về (nội dung mới, số embed đã đổi, số link đã đổi, danh sách asset thiếu map)."""
    unmapped: list[str] = []
    embeds = 0
    links = 0

    def embed_sub(m: re.Match[str]) -> str:
        nonlocal embeds
        name = m.group("name")
        uri = images.get(name)
        if uri is None:
            unmapped.append(name)
            return m.group(0)
        embeds += 1
        return f"![{m.group('alt')}]({uri})"

    def link_sub(m: re.Match[str]) -> str:
        nonlocal links
        name = m.group("name")
        uri = images.get(name)
        if uri is None:
            unmapped.append(name)
            return m.group(0)
        links += 1
        # Registry hiển thị nguyên đường dẫn tương đối; sau khi đổi target sang MinIO
        # thì hiển thị tên file cho khỏi gây nhầm là còn dùng đường dẫn cục bộ.
        text_shown = m.group("text")
        if text_shown.startswith("assets/"):
            text_shown = name
        return f"[{text_shown}]({uri})"

    out_lines: list[str] = []
    for line in text.splitlines():
        embed_match = EMBED_RE.search(line)
        new_line = EMBED_RE.sub(embed_sub, line)
        new_line = LINK_RE.sub(link_sub, new_line)

        # Chèn comment truy nguyên ngay trước dòng ảnh nhúng, không nhân đôi.
        if embed_match and out_lines and out_lines[-1].strip().startswith("<!-- LOCAL_ASSET:"):
            out_lines.append(new_line)
            continue
        if embed_match:
            out_lines.append(LOCAL_ASSET_TMPL.format(name=embed_match.group("name")))
        out_lines.append(new_line)

    new_text = "\n".join(out_lines)
    if text.endswith("\n") and not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, embeds, links, unmapped


def main(argv: list[str] | None = None) -> int:
    # Console Windows mặc định cp1252 sẽ hiện mojibake với tiếng Việt.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="Chỉ kiểm tra và báo cáo, không ghi file.",
    )
    args = parser.parse_args(argv)

    try:
        images = load_map()
    except MapError as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2

    md_files = sorted(p for p in BUNDLE.glob("*.md"))
    if not md_files:
        print(f"LỖI: không thấy file .md nào trong {BUNDLE}", file=sys.stderr)
        return 2

    total_embeds = total_links = 0
    all_unmapped: list[str] = []
    changed: list[str] = []

    for path in md_files:
        original = path.read_text(encoding="utf-8")
        new_text, embeds, links, unmapped = rewrite_text(original, images)
        total_embeds += embeds
        total_links += links
        all_unmapped.extend(unmapped)
        if new_text != original:
            changed.append(path.name)
            if not args.check:
                path.write_text(new_text, encoding="utf-8")
        if embeds or links:
            print(f"  {path.name}: {embeds} ảnh nhúng, {links} link registry")

    if all_unmapped:
        print(
            f"LỖI: {len(all_unmapped)} tham chiếu không có URI: "
            f"{sorted(set(all_unmapped))[:5]}",
            file=sys.stderr,
        )
        return 1

    mode = "sẽ đổi" if args.check else "đã đổi"
    print(
        f"\n{mode}: {total_embeds} ảnh nhúng + {total_links} link registry "
        f"trên {len(changed)} file (tổng {len(md_files)} file .md)."
    )
    print(f"Ảnh có URI trong map: {len(images)}.")
    if args.check and changed:
        print("Chạy lại không có --check để ghi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
