#!/usr/bin/env python3

import argparse
import base64
import html
import json
import mimetypes
import os
import re
from collections import namedtuple
from pathlib import Path

import markdown


Module = namedtuple("Module", "name body")
EXPECTED_MODULE_COUNT = 21
KNOWLEDGE_DIR_NAME = "knowledge"
CONSUMER_KB_NAME = "GS9 Knowledge VNG AI"
HUMAN_SOURCE_DIR_NAME = "docs KB/Human"
HUMAN_SOURCE_SUBDIRS = ("KB", "Agent")
# Tiền tố tính năng dùng cho tên file nguồn của sổ tay nền tảng.
HUMAN_SOURCE_PREFIXES = ("KB", "Agent")

# KB phụ sinh thẳng từ nguồn Human, không qua pipeline module/ảnh của sổ tay.
# Mỗi mục: tiền tố tên file nguồn -> tên thư mục KB trong `knowledge/`.
SIMPLE_KB_TARGETS = {
    "AgentCFL": "GS9 CFL Knowledge Agent",
    "KBCFL": "GS9 CFL Knowledge Agent",
}
LEGACY_GENERATED_MODULE_NAMES = (
    "13-tao-va-van-hanh-agent.md",
    "00-gioi-thieu-va-quick-start.md",
    "01-chuan-bi-noi-dung.md",
    "02-tao-kb-nhanh-va-nang-cao.md",
    "03-tai-lieu-rag-wiki.md",
    "04-faq-va-lap-chi-muc.md",
    "05-mo-hinh-vlm-asr.md",
    "06-parser-va-xu-ly-file.md",
    "07-phan-doan-chunking.md",
    "08-chia-se-va-nguon-du-lieu.md",
    "09-van-hanh-documents-wiki-graph.md",
    "10-van-hanh-faq.md",
    "11-chat-kiem-thu-va-bao-tri.md",
    "12-ket-noi-google-drive.md",
    "13-agent-tong-quan-va-kien-truc.md",
    "14-che-do-preset-prompt-va-intent.md",
    "15-model-reranker-suy-luan-va-quota.md",
    "16-kho-tri-thuc-cong-cu-va-truy-hoi.md",
    "17-da-phuong-thuc-va-tep-dinh-kem.md",
    "18-chat-nguon-lich-su-va-danh-gia.md",
    "19-vong-doi-phan-quyen-quan-sat-va-bao-tri.md",
)
MODULE_RE = re.compile(
    r"<!-- MODULE:(?P<name>[^>]+) -->\s*(?P<body>.*?)\s*<!-- /MODULE -->",
    re.DOTALL,
)
IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")
DOCUMENT_LINK_RE = re.compile(
    r"(?<!!)\[(?P<label>[^\]]+)\]\("
    r"(?P<target><[^>]+>|[^)\s]+)(?P<suffix>[^)]*)\)"
)
ARCHIVED_AGENT_BLOCK_RE = re.compile(
    r"<!-- ARCHIVED_AGENT_MODULE_V3_2:.*?\n-->", re.DOTALL
)


def _fence_marker(line):
    stripped = line.lstrip()
    if stripped.startswith("```"):
        return "```"
    if stripped.startswith("~~~"):
        return "~~~"
    return None


def replace_images_outside_fences(source, replacement):
    rendered = []
    fence = None
    for line in source.splitlines(keepends=True):
        marker = _fence_marker(line)
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
        elif fence is None:
            line = IMAGE_RE.sub(replacement, line)
        rendered.append(line)
    return "".join(rendered)


def find_images_outside_fences(source):
    matches = []
    fence = None
    for line in source.splitlines():
        marker = _fence_marker(line)
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
        elif fence is None:
            matches.extend(IMAGE_RE.finditer(line))
    return matches


def rebase_master_relative_links(source, source_root, output_dir):
    source_root = Path(source_root).resolve()
    output_dir = Path(output_dir).resolve()

    def replace_link(match):
        raw_target = match.group("target")
        wrapped = raw_target.startswith("<") and raw_target.endswith(">")
        target = raw_target[1:-1] if wrapped else raw_target
        if (
            target.startswith(("#", "/", "\\", "../"))
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)
        ):
            return match.group(0)

        path_text, marker, fragment = target.partition("#")
        source_target = (source_root / path_text).resolve()
        output_target = (output_dir / path_text).resolve()
        if not source_target.exists() or output_target.exists():
            return match.group(0)

        rebased = Path(os.path.relpath(source_target, output_dir)).as_posix()
        if marker:
            rebased += f"#{fragment}"
        if wrapped:
            rebased = f"<{rebased}>"
        return f"[{match.group('label')}]({rebased}{match.group('suffix')})"

    rendered = []
    fence = None
    for line in source.splitlines(keepends=True):
        marker = _fence_marker(line)
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
        elif fence is None:
            line = DOCUMENT_LINK_RE.sub(replace_link, line)
        rendered.append(line)
    return "".join(rendered)


def promote_headings_outside_fences(source):
    """Nâng mọi heading lên một cấp, bỏ qua nội dung trong code fence.

    `extract_modules` hạ heading một cấp vì master dùng `##` cho tiêu đề
    module. Nguồn trong `docs KB/Human` đã viết ở đúng cấp hiển thị cuối
    (`#` là tiêu đề bài), nên phải nâng trước để bù lại phép hạ đó.

    Heading nằm trong code fence là nội dung mẫu cho người đọc chép theo,
    không phải cấu trúc tài liệu — giữ nguyên.
    """
    rendered = []
    fence = None
    for line in source.splitlines(keepends=True):
        marker = _fence_marker(line)
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
        elif fence is None and re.match(r"^#{1,5}\s", line):
            line = "#" + line
        rendered.append(line)
    return "".join(rendered)


def human_source_to_module_name(filename):
    """Đổi tên nguồn Human sang tên tài liệu trên Web.

    Nguồn dùng tiền tố tính năng cho người soạn dễ nhận ra file thuộc phần nào
    (`KB-00-....md`, `Agent-13-....md`). Tài liệu trên Web phải giữ tiền tố
    `doc-` theo quy ước đặt tên (DEC-042) vì regex đồng bộ khoá vào
    `^(doc|image)-`. Hàm này chỉ thay tiền tố, giữ nguyên số và phần slug.
    """
    for prefix in HUMAN_SOURCE_PREFIXES:
        if filename.startswith(f"{prefix}-"):
            return "doc-" + filename[len(prefix) + 1 :]
    return filename


def load_source_from_dirs(root):
    """Ghép các file nguồn theo function thành một chuỗi master.

    Nguồn nằm phẳng trong `docs KB/Human/`, đặt tên `<TínhNăng>-<NN>-<slug>.md`.
    Mỗi file là thân của một module; hàm này bọc lại bằng marker
    `<!-- MODULE:... -->` để phần còn lại của builder dùng nguyên logic cũ.
    Thư mục con theo tính năng và tên `doc-*.md` cũ vẫn được nhận để các bố cục
    trước đây không làm gãy build.
    """
    root = Path(root)
    human_dir = root / HUMAN_SOURCE_DIR_NAME
    header_file = human_dir / "_master-header.txt"
    header = header_file.read_text(encoding="utf-8") if header_file.exists() else ""

    patterns = [f"{prefix}-*.md" for prefix in HUMAN_SOURCE_PREFIXES]
    patterns.append("doc-*.md")
    search_dirs = [human_dir] + [human_dir / sub for sub in HUMAN_SOURCE_SUBDIRS]

    found = {}
    for source_dir in search_dirs:
        if not source_dir.is_dir():
            continue
        for pattern in patterns:
            for path in source_dir.glob(pattern):
                module_name = human_source_to_module_name(path.name)
                found.setdefault(module_name, path)

    if not found:
        # Chưa dựng xong nguồn Human — quay về master gốc để build vẫn chạy.
        # Master đã ngừng là nguồn build từ 16/08/2026 (DEC-053) và được dời vào
        # `audit/archive/` ngày 17/08/2026 (DEC-066). Vẫn dò cả vị trí cũ ở root
        # để bản sao chưa cập nhật của repo không gãy build.
        legacy_candidates = (
            root / "audit" / "archive" / "so-tay-tao-knowledge-base-v3.md",
            root / "so-tay-tao-knowledge-base-v3.md",
        )
        for legacy_master in legacy_candidates:
            if legacy_master.exists():
                return legacy_master.read_text(encoding="utf-8")
        raise ValueError(
            f"Không tìm thấy nguồn nào trong {human_dir} và cũng không có master gốc."
        )

    parts = []
    for module_name in sorted(found):
        path = found[module_name]
        body = path.read_text(encoding="utf-8")
        if path.name != module_name:
            # Chỉ nguồn Human (tên có tiền tố tính năng) mới cần bù cấp heading;
            # file `doc-*.md` cũ vốn đã ở dạng master nên giữ nguyên.
            body = promote_headings_outside_fences(body)
        parts.append(f"<!-- MODULE:{module_name} -->\n{body}<!-- /MODULE -->\n")

    return header + "\n".join(parts)


def extract_modules(source: str):
    modules = []
    for match in MODULE_RE.finditer(source):
        body = re.sub(
            r"^(#{2,6})(\s+)",
            lambda heading: heading.group(1)[1:] + heading.group(2),
            match.group("body").strip(),
            flags=re.MULTILINE,
        )
        modules.append(Module(match.group("name").strip(), body))
    return modules


def count_h1(source):
    count = 0
    fence = None
    for line in source.splitlines():
        stripped = line.lstrip()
        marker = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else None
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence is None and re.match(r"^#\s+", line):
            count += 1
    return count


def write_modules(
    source,
    output_dir,
    image_map,
    require_minio=True,
    source_root=None,
    local_asset_prefix="assets",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    modules = extract_modules(source)
    missing = set()
    rendered_modules = []

    for module in modules:
        def replace_image(match):
            source_path = match.group("src").strip()
            if source_path.startswith("<") and source_path.endswith(">"):
                source_path = source_path[1:-1]
            filename = Path(source_path.replace("\\", "/")).name
            local = f"{local_asset_prefix.rstrip('/')}/{filename}"
            uri = image_map.get(filename)
            if uri:
                return (
                    f"<!-- LOCAL_ASSET: {local} -->\n"
                    f"![{match.group('alt')}]({uri})"
                )
            missing.add(filename)
            return f"![{match.group('alt')}]({local})"

        body = replace_images_outside_fences(module.body, replace_image)
        if source_root is not None:
            body = rebase_master_relative_links(body, source_root, output_dir)
        rendered_modules.append(Module(module.name, body))

    if require_minio and missing:
        raise ValueError("Missing MinIO mappings: " + ", ".join(sorted(missing)))

    outputs = []
    for module in rendered_modules:
        target = output_dir / module.name
        target.write_text(
            "<!-- GENERATED FILE - sửa nội dung tại "
            "docs KB/Human/ -->\n\n"
            + module.body.rstrip()
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        outputs.append(target)
    return outputs


def _slugify(value):
    table = str.maketrans(
        "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ",
        "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd",
    )
    value = value.lower().translate(table)
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "section"


def _markdown_html(source):
    return markdown.markdown(
        source,
        extensions=["extra", "tables", "fenced_code", "attr_list", "sane_lists", "toc"],
        output_format="html5",
    )


def _embed_images(rendered, root):
    def replace(match):
        src = html.unescape(match.group("src"))
        if src.startswith("data:"):
            return match.group(0)
        if src.startswith(("http://", "https://", "minio://")):
            raise ValueError(f"Offline HTML cannot embed remote image: {src}")
        target = (Path(root) / src).resolve()
        try:
            target.relative_to(Path(root).resolve())
        except ValueError as exc:
            raise ValueError(f"Image escapes build root: {src}") from exc
        if not target.exists():
            raise FileNotFoundError(f"Missing image: {src}")
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        payload = base64.b64encode(target.read_bytes()).decode("ascii")
        data = f"data:{mime};base64,{payload}"
        return match.group(0).replace(match.group("src"), data)

    return re.sub(
        r'<img(?P<before>[^>]*?)src="(?P<src>[^"]+)"(?P<after>[^>]*)>',
        replace,
        rendered,
    )


def _split_sections(source):
    source = ARCHIVED_AGENT_BLOCK_RE.sub("", source)
    source = source.replace("—", "-").replace("–", "-")
    source = re.sub(r"<!-- /?MODULE(?::[^>]*)? -->", "", source)
    source = re.sub(r"^#\s+.*?\n", "", source, count=1)
    heading = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(heading.finditer(source))
    if not matches:
        return source.strip(), []
    intro = source[: matches[0].start()].strip()
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        title = re.sub(r"\s*\{#[^}]+\}\s*$", "", match.group(1)).strip()
        sections.append((title, source[match.start() : end].strip()))
    return intro, sections


def _source_metadata(source, label, fallback="không ghi"):
    match = re.search(
        rf"^>\s*{re.escape(label)}:\s*(.*?)\s*$",
        source,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else fallback


def build_offline_html(source, root, output):
    version = html.escape(_source_metadata(source, "Phiên bản"))
    updated_at = html.escape(_source_metadata(source, "Cập nhật"))
    intro, sections = _split_sections(source)
    nav = []
    cards = []
    used = set()
    for number, (title, block) in enumerate(sections, start=1):
        section_id = _slugify(title)
        base = section_id
        suffix = 2
        while section_id in used:
            section_id = f"{base}-{suffix}"
            suffix += 1
        used.add(section_id)
        rendered = _embed_images(_markdown_html(block), root)
        rendered = re.sub(
            r'<h2(?: id="[^"]+")?>',
            f'<h2 id="{section_id}">',
            rendered,
            count=1,
        )
        nav.append(
            f'<a href="#{section_id}"><span>{number:02d}</span>{html.escape(title)}</a>'
        )
        label = "Chương" if re.match(r"^\d{2}\s+-", title) else "Tham chiếu"
        cards.append(
            f'<section class="doc-section" data-title="{html.escape(title.lower())}">'
            f'<div class="section-label">{label}</div>{rendered}</section>'
        )

    intro_html = _embed_images(_markdown_html(intro), root)
    css = r"""
:root {
  --ink:#191b1f;--muted:#656970;--line:#ddd7d0;--paper:#faf8f5;--panel:#fff;
  --soft:#f2eee9;--accent:#ef5b2a;--accent-dark:#9e3513;--accent-soft:#fff0e8;
  --shadow:0 14px 42px rgba(35,28,23,.09);--radius:12px;--topbar:64px;--sidebar:304px;
}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:88px}
body{margin:0;color:var(--ink);background:var(--paper);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:16px;line-height:1.72;text-rendering:optimizeLegibility}
a{color:var(--accent-dark);text-underline-offset:3px;overflow-wrap:anywhere}a:hover{color:var(--accent)}
:focus-visible{outline:3px solid rgba(239,91,42,.34);outline-offset:3px}
.skip-link{position:fixed;left:12px;top:-60px;z-index:110;padding:9px 13px;color:#fff;background:#1d1f23;border-radius:8px}.skip-link:focus{top:10px}
.progress{position:fixed;inset:0 auto auto 0;z-index:100;width:0;height:3px;background:var(--accent);transition:width 80ms linear}
.topbar{position:fixed;inset:0 0 auto 0;z-index:80;height:var(--topbar);display:flex;align-items:center;gap:18px;padding:0 24px;background:rgba(250,248,245,.96);border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}
.brand{display:flex;align-items:center;gap:11px;min-width:245px;font-weight:760}.brand-mark{display:grid;place-items:center;width:32px;height:32px;color:#fff;background:var(--accent);border-radius:8px;font-size:13px;letter-spacing:.04em}
.top-search{position:relative;flex:1;max-width:720px}.top-search input{width:100%;height:40px;padding:0 90px 0 14px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:9px;font:inherit}.search-meta{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:12px;pointer-events:none}
button{font:inherit}.button{min-height:38px;padding:0 13px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:9px;cursor:pointer;font-weight:650}.button:hover{border-color:var(--accent);color:var(--accent-dark)}.menu-button{display:none}
.sidebar{position:fixed;inset:var(--topbar) auto 0 0;z-index:70;width:var(--sidebar);overflow:auto;padding:24px 18px 32px;background:#f4f0eb;border-right:1px solid var(--line)}
.sidebar-label{margin:0 10px 10px;color:var(--muted);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.nav-list{display:grid;gap:3px}.nav-list a{display:grid;grid-template-columns:28px 1fr;gap:8px;align-items:start;padding:8px 10px;color:#474b51;border-left:3px solid transparent;border-radius:0 7px 7px 0;text-decoration:none;font-size:13px;line-height:1.35}.nav-list a span{color:#9a9289;font-variant-numeric:tabular-nums}.nav-list a:hover,.nav-list a.active{color:var(--accent-dark);background:var(--accent-soft);border-left-color:var(--accent)}
.sidebar-note{margin:22px 8px 0;padding:13px;border:1px solid #e7c8b8;border-radius:9px;background:#fff8f3;color:#6f3a23;font-size:12px;line-height:1.5}
main{margin-left:var(--sidebar);padding-top:var(--topbar)}.hero{padding:56px clamp(28px,6vw,88px) 42px;color:#fff;background:#202226;border-bottom:4px solid var(--accent)}.hero-inner{max-width:1040px;margin:0 auto}.eyebrow{margin-bottom:18px;color:#ffcab4;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.hero h1{max-width:820px;margin:0;font-size:clamp(36px,5vw,68px);line-height:1.02;letter-spacing:-.045em}.hero p{max-width:760px;margin:20px 0 0;color:#d9dade;font-size:18px;line-height:1.6}.hero-meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}.hero-meta span{padding:7px 10px;color:#f1f1f2;background:#2e3136;border:1px solid #45484e;border-radius:7px;font-size:12px}
.content-shell{min-width:0;max-width:1120px;margin:0 auto;padding:44px clamp(24px,5vw,74px) 100px}.doc-section,.intro-card{min-width:0}.intro-card{margin-bottom:28px;padding:24px 28px;background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:var(--radius)}
.doc-section{position:relative;margin:0 0 28px;padding:clamp(26px,4vw,48px);background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}.doc-section[hidden]{display:none}.section-label{margin-bottom:10px;color:var(--accent-dark);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
h2,h3,h4,h5,h6{color:#202226;line-height:1.24;text-wrap:balance}h2{margin:0 0 24px;font-size:clamp(28px,3.5vw,42px);letter-spacing:-.035em}h3{margin:34px 0 12px;padding-top:4px;font-size:24px;letter-spacing:-.02em}h4{margin:26px 0 10px;font-size:19px}p,ul,ol{max-width:820px}li+li{margin-top:5px}
blockquote{margin:22px 0;padding:15px 18px;color:#5d392a;background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 9px 9px 0}blockquote p{margin:0}
code{padding:.12em .34em;color:#8d2f10;background:#f5ebe6;border:1px solid #eedbd1;border-radius:5px;font-family:Consolas,"SFMono-Regular",monospace;font-size:.9em}pre{max-width:100%;overflow:auto;margin:20px 0;padding:19px;color:#f3f3f3;background:#202226;border-radius:9px;line-height:1.58}pre code{display:block;padding:0;color:inherit;background:transparent;border:0}
.table-wrap{max-width:100%;overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:9px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.5}th{color:#4a2a1e;background:var(--accent-soft);text-align:left}th,td{padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fbfaf8}
img{display:block;max-width:100%;height:auto;margin:22px auto 10px;border:1px solid #d8d2cc;border-radius:9px;box-shadow:0 10px 28px rgba(31,25,21,.12);cursor:zoom-in}img+em{display:block;max-width:820px;margin:0 auto 26px;color:var(--muted);font-size:13px;text-align:center}hr{margin:34px 0;border:0;border-top:1px solid var(--line)}
.empty{display:none;padding:42px;text-align:center;color:var(--muted)}.empty.visible{display:block}.image-viewer{position:fixed;inset:0;z-index:120;display:none;place-items:center;padding:28px;background:rgba(18,19,21,.88)}.image-viewer.open{display:grid}.image-viewer img{max-width:min(1500px,95vw);max-height:88vh;margin:0;border:0;cursor:zoom-out}.image-viewer button{position:absolute;top:18px;right:20px;color:#fff;background:#292b30;border-color:#555}.scrim{display:none}
@media (max-width: 940px){:root{--sidebar:0px}.topbar{padding:0 14px;gap:10px}.brand{min-width:0}.brand-name{display:none}.menu-button{display:inline-flex}.print-button{display:none}.sidebar{width:min(330px,88vw);transform:translateX(-102%);transition:transform 180ms ease;box-shadow:16px 0 38px rgba(0,0,0,.14)}body.nav-open .sidebar{transform:translateX(0)}.scrim{position:fixed;inset:var(--topbar) 0 0 0;z-index:65;background:rgba(24,24,24,.35)}body.nav-open .scrim{display:block}main{margin-left:0}.hero{padding-top:42px}}
@media (max-width:620px){.top-search input{padding-right:14px}.search-meta{display:none}.hero{padding:36px 20px 32px}.hero p{font-size:16px}.content-shell{padding:24px 14px 70px}.doc-section,.intro-card{padding:22px 18px;border-radius:9px}h2{font-size:29px}h3{font-size:21px}th,td{min-width:150px;padding:9px 10px}}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}*,*::before,*::after{transition-duration:.01ms!important;animation-duration:.01ms!important}}
@media print{@page{margin:16mm}body{background:#fff;font-size:10.5pt}.topbar,.sidebar,.scrim,.progress,.image-viewer{display:none!important}main{margin:0;padding:0}.hero{padding:0 0 18px;color:#000;background:#fff;border-bottom:2px solid #444}.hero p,.eyebrow{color:#333}.hero-meta span{color:#333;background:#fff;border-color:#aaa}.content-shell{max-width:none;padding:18px 0 0}.doc-section,.intro-card{break-inside:avoid-page;padding:0 0 16px;border:0;box-shadow:none}a{color:#000;text-decoration:none}img{max-height:200mm;box-shadow:none}}
"""
    script = r"""
(()=>{
const body=document.body,search=document.getElementById('search'),sections=[...document.querySelectorAll('.doc-section')],meta=document.getElementById('searchMeta'),empty=document.getElementById('emptyState'),menu=document.getElementById('menuButton'),scrim=document.getElementById('scrim'),progress=document.getElementById('progress'),viewer=document.getElementById('imageViewer'),viewerImage=document.getElementById('viewerImage'),closeViewer=document.getElementById('closeViewer');
const normalize=v=>v.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
document.querySelectorAll('table').forEach(table=>{const wrap=document.createElement('div');wrap.className='table-wrap';table.parentNode.insertBefore(wrap,table);wrap.appendChild(table)});
search.addEventListener('input',()=>{const query=normalize(search.value.trim());let shown=0;sections.forEach(section=>{const match=!query||normalize(section.textContent).includes(query);section.hidden=!match;if(match)shown+=1});meta.textContent=`${shown} mục`;empty.classList.toggle('visible',shown===0)});
const closeMenu=()=>{body.classList.remove('nav-open');menu.setAttribute('aria-expanded','false')};menu.addEventListener('click',()=>{const open=!body.classList.contains('nav-open');body.classList.toggle('nav-open',open);menu.setAttribute('aria-expanded',String(open))});scrim.addEventListener('click',closeMenu);document.querySelectorAll('.nav-list a').forEach(link=>link.addEventListener('click',closeMenu));document.getElementById('printButton').addEventListener('click',()=>window.print());
const updateProgress=()=>{const root=document.documentElement,max=root.scrollHeight-root.clientHeight;progress.style.width=max>0?`${Math.min(100,root.scrollTop/max*100)}%`:'0%'};document.addEventListener('scroll',updateProgress,{passive:true});updateProgress();
const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(!entry.isIntersecting)return;document.querySelectorAll('.nav-list a').forEach(link=>link.classList.remove('active'));const heading=entry.target.querySelector('h2'),link=heading&&document.querySelector(`.nav-list a[href="#${heading.id}"]`);if(link)link.classList.add('active')})},{rootMargin:'-20% 0px -68% 0px',threshold:0});sections.forEach(section=>observer.observe(section));
document.querySelectorAll('.doc-section img,.intro-card img').forEach(image=>{image.tabIndex=0;const open=()=>{viewerImage.src=image.src;viewerImage.alt=image.alt;viewer.classList.add('open');closeViewer.focus()};image.addEventListener('click',open);image.addEventListener('keydown',event=>{if(event.key==='Enter')open()})});const hideViewer=()=>viewer.classList.remove('open');closeViewer.addEventListener('click',hideViewer);viewer.addEventListener('click',event=>{if(event.target===viewer||event.target===viewerImage)hideViewer()});document.addEventListener('keydown',event=>{if(event.key==='Escape'){hideViewer();closeMenu()}});
})();
"""
    document = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Sổ tay Knowledge Base - VNGGames</title><style>{css}</style></head>
<body><a class="skip-link" href="#main-content">Đến nội dung chính</a><div class="progress" id="progress" aria-hidden="true"></div>
<header class="topbar"><button class="button menu-button" id="menuButton" aria-expanded="false" aria-controls="sidebar">Mục lục</button><div class="brand"><span class="brand-mark">KB</span><span class="brand-name">VNGGames Knowledge</span></div><label class="top-search"><span hidden>Tìm trong sổ tay</span><input id="search" type="search" placeholder="Tìm tên nút, khái niệm hoặc lỗi..." autocomplete="off"><span class="search-meta" id="searchMeta">{len(sections)} mục</span></label><button class="button print-button" id="printButton">In tài liệu</button></header>
<aside class="sidebar" id="sidebar" aria-label="Mục lục"><p class="sidebar-label">Nội dung</p><nav class="nav-list">{''.join(nav)}</nav><div class="sidebar-note">Bản offline. Ảnh, CSS và JavaScript đều nằm trong file này. Dữ liệu giao diện được kiểm chứng ngày {updated_at}.</div></aside><div class="scrim" id="scrim" aria-hidden="true"></div>
<main id="main-content"><section class="hero"><div class="hero-inner"><div class="eyebrow">Sổ tay vận hành · Phiên bản {version}</div><h1>Tạo và vận hành Knowledge Base &amp; Agent</h1><p>Hướng dẫn dựa trên kiểm chứng giao diện thật: từ xây Knowledge Base, parser, chunking và nguồn dữ liệu đến cấu hình Agent, truy hồi, công cụ, attachment, quan sát và bảo trì.</p><div class="hero-meta"><span>VNGGames</span><span>Studio 9 kiểm chứng</span><span>Cập nhật {updated_at}</span><span>{EXPECTED_MODULE_COUNT} module</span></div></div></section><div class="content-shell"><section class="intro-card">{intro_html}</section><div id="sections">{''.join(cards)}</div><div class="empty" id="emptyState"><strong>Không tìm thấy nội dung phù hợp.</strong><br>Thử từ khóa ngắn hơn hoặc dùng tên nút trên giao diện.</div></div></main>
<div class="image-viewer" id="imageViewer" role="dialog" aria-modal="true" aria-label="Xem ảnh lớn"><button class="button" id="closeViewer">Đóng</button><img id="viewerImage" alt=""></div><script>{script}</script></body></html>"""
    document = document.replace("—", "-").replace("–", "-")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    return output


def build_simple_kbs(root):
    """Sinh các KB phụ từ nguồn Human, không qua pipeline module/ảnh.

    Khác `write_modules`: các KB này là tài liệu văn bản thuần, không nhúng
    ảnh nên không cần `image-map.json` và không kiểm URI MinIO. Vẫn ghi header
    `GENERATED FILE` để không ai sửa nhầm vào bản sinh, và vẫn buộc đúng một H1
    mỗi tài liệu.

    Chỉ xoá bản sinh cũ mang đúng header đó; file người dùng tự đặt vào thư mục
    KB không bao giờ bị đụng tới.
    """
    root = Path(root)
    human_dir = root / HUMAN_SOURCE_DIR_NAME
    results = {}

    # Nhiều tiền tố có thể cùng đổ về một KB (ví dụ `AgentCFL-` và `KBCFL-`).
    # Gom theo KB trước rồi mới ghi, nếu không bước dọn của tiền tố sau sẽ xoá
    # mất bản sinh của tiền tố trước.
    by_kb = {}
    for prefix, kb_name in SIMPLE_KB_TARGETS.items():
        for path in human_dir.glob(f"{prefix}-*.md"):
            by_kb.setdefault(kb_name, []).append((prefix, path))

    for kb_name, sources in by_kb.items():
        sources = sorted(sources, key=lambda pair: pair[1].name)

        target_dir = root / KNOWLEDGE_DIR_NAME / kb_name
        target_dir.mkdir(parents=True, exist_ok=True)

        written = []
        for prefix, path in sources:
            target_name = "doc-" + path.name[len(prefix) + 1 :]
            body = path.read_text(encoding="utf-8")
            if count_h1(body) != 1:
                raise ValueError(f"{path.name} must contain exactly one H1")
            target = target_dir / target_name
            target.write_text(
                f"<!-- GENERATED FILE - sửa nội dung tại {HUMAN_SOURCE_DIR_NAME}/ -->\n\n"
                + body.rstrip()
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            written.append(target)

        keep = {path.name for path in written}
        for stale in target_dir.glob("doc-*.md"):
            if stale.name in keep:
                continue
            if stale.read_text(encoding="utf-8").startswith(
                "<!-- GENERATED FILE - sửa nội dung tại "
            ):
                stale.unlink()

        results[kb_name] = written

    return results


def build_project(root, require_minio=True):
    root = Path(root).resolve()
    knowledge_dir = root / KNOWLEDGE_DIR_NAME
    module_dir = knowledge_dir / CONSUMER_KB_NAME
    image_map_file = module_dir / "image-map.json"
    html_output = root / "so-tay-tao-knowledge-base.html"
    source = load_source_from_dirs(root)
    extracted = extract_modules(source)
    if len(extracted) != EXPECTED_MODULE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_MODULE_COUNT} modules, found {len(extracted)}"
        )

    image_map = {}
    if image_map_file.exists():
        payload = json.loads(image_map_file.read_text(encoding="utf-8"))
        image_map = payload.get("images", payload)
    modules = write_modules(
        source,
        module_dir,
        image_map,
        require_minio=require_minio,
        source_root=root,
        local_asset_prefix=".",
    )

    # The v3.3 split replaces the former generated all-in-one Agent module.
    # Remove only this exact generated artifact after a successful write; never
    # prune arbitrary user files from the module directory.
    for legacy_name in LEGACY_GENERATED_MODULE_NAMES:
        legacy = module_dir / legacy_name
        if legacy.exists() and legacy.read_text(encoding="utf-8").startswith(
            "<!-- GENERATED FILE - sửa nội dung tại "
        ):
            legacy.unlink()

    for module in modules:
        rendered = module.read_text(encoding="utf-8")
        if count_h1(rendered) != 1:
            raise ValueError(f"{module.name} must contain exactly one H1")
        images = find_images_outside_fences(rendered)
        if not images:
            raise ValueError(f"{module.name} must contain at least one image")
        if require_minio and not any(
            image.group("src").startswith("minio://") for image in images
        ):
            raise ValueError(f"{module.name} must contain a MinIO image")

    build_offline_html(source, root, html_output)
    offline = html_output.read_text(encoding="utf-8").lower()
    forbidden = ['src="http', '<script src=', '<link rel="stylesheet"']
    for token in forbidden:
        if token in offline:
            raise ValueError(f"Offline HTML contains forbidden resource: {token}")
    if "data:image/" not in offline:
        raise ValueError("Offline HTML does not contain embedded images")

    simple_kbs = build_simple_kbs(root)
    return {"modules": modules, "html": html_output, "simple_kbs": simple_kbs}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-missing-minio",
        action="store_true",
        help="Build a local preview before every image has a MinIO mapping.",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    result = build_project(root, require_minio=not args.allow_missing_minio)
    module_bytes = sum(path.stat().st_size for path in result["modules"])
    print("Build complete")
    print(f"- {EXPECTED_MODULE_COUNT} modules: {module_bytes:,} bytes")
    print(f"- Offline HTML: {result['html'].stat().st_size:,} bytes")
    for kb_name, written in result.get("simple_kbs", {}).items():
        print(f"- {kb_name}: {len(written)} tài liệu")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
