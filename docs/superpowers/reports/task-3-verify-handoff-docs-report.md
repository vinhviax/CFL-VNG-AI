# Task 3 — Báo cáo kiểm chứng bộ tài liệu bàn giao

**Trạng thái:** DONE

**Thư mục kiểm chứng:** `J:\My Drive\AI\Knowledge Base VNG`  
**Phạm vi thay đổi:** chỉ chạy build nghiêm ngặt để tái sinh 12 module/HTML và tạo báo cáo này. Không sửa năm file bàn giao, master, audit, image map, script hoặc test.

## 1. Năm file bàn giao ở thư mục gốc

Lệnh chính xác:

```powershell
$required = @('AGENTS.md','PROJECT.md','STATUS.md','HANDOFF.md','DECISIONS.md')
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath $_ -PathType Leaf) })
"HANDOFF_FILES=$($required.Count)"
"MISSING_HANDOFF_FILES=$($missing.Count)"
$missing | ForEach-Object { "MISSING=$_" }
if ($missing.Count -gt 0) { exit 1 }
```

Exit code: `0`  
Kết quả: `HANDOFF_FILES=5`, `MISSING_HANDOFF_FILES=0`.

## 2. Link Markdown tương đối trong năm file

Lệnh chính xác:

```powershell
$handoffFiles = @('AGENTS.md','PROJECT.md','STATUS.md','HANDOFF.md','DECISIONS.md')
$broken = [System.Collections.Generic.List[string]]::new()
$linkCount = 0
foreach ($file in $handoffFiles) {
  $content = Get-Content -LiteralPath $file -Raw
  $matches = [regex]::Matches($content, '(?<image>!)?\[[^\]]*\]\((?<target>[^)]+)\)')
  $base = Split-Path -Parent $file
  if ([string]::IsNullOrEmpty($base)) { $base = (Get-Location).Path }
  foreach ($match in $matches) {
    if ($match.Groups['image'].Success) { continue }
    $target = $match.Groups['target'].Value.Trim()
    if ($target.StartsWith('<') -and $target.EndsWith('>')) { $target = $target.Substring(1, $target.Length - 2) }
    $target = $target -replace '#.*$', ''
    if ([string]::IsNullOrWhiteSpace($target)) { continue }
    if ($target -match '^(https?://|minio://|mailto:)') { continue }
    $linkCount++
    $resolved = Join-Path -Path $base -ChildPath $target
    if (-not (Test-Path -LiteralPath $resolved)) { $broken.Add("$file -> $target") }
  }
}
"RELATIVE_MARKDOWN_LINKS=$linkCount"
"BROKEN_LINKS=$($broken.Count)"
$broken
if ($broken.Count -gt 0) { exit 1 }
```

Exit code: `0`  
Kết quả: `RELATIVE_MARKDOWN_LINKS=30`, `BROKEN_LINKS=0`. Không có link hỏng.

## 3. Đối chiếu filesystem và JSON

Lệnh chính xác:

```powershell
$modules = @(Get-ChildItem -LiteralPath 'knowledge-vng' -File -Filter '*.md')
$assets = @(Get-ChildItem -LiteralPath 'knowledge-vng\assets' -File)
$map = Get-Content -LiteralPath 'knowledge-vng\image-map.json' -Raw | ConvertFrom-Json
$mappings = @($map.images.PSObject.Properties)
$masterLines = @(Get-Content -LiteralPath 'so-tay-tao-knowledge-base-v3.md').Count
$assetNames = @($assets.Name | Sort-Object)
$mappingNames = @($mappings.Name | Sort-Object)
$unmappedAssets = @($assetNames | Where-Object { $_ -notin $mappingNames })
$missingAssets = @($mappingNames | Where-Object { $_ -notin $assetNames })
"MODULES=$($modules.Count)"
"ASSETS=$($assets.Count)"
"MINIO_MAPPINGS=$($mappings.Count)"
"MASTER_LINES=$masterLines"
"UNMAPPED_ASSETS=$($unmappedAssets.Count)"
"MISSING_MAPPED_ASSETS=$($missingAssets.Count)"
$unmappedAssets | ForEach-Object { "UNMAPPED_ASSET=$_" }
$missingAssets | ForEach-Object { "MISSING_MAPPED_ASSET=$_" }
if ($modules.Count -ne 12 -or $assets.Count -ne 14 -or $mappings.Count -ne 14 -or $masterLines -ne 1078 -or $unmappedAssets.Count -ne 0 -or $missingAssets.Count -ne 0) { exit 1 }
```

Exit code: `0`  
Kết quả: `MODULES=12`, `ASSETS=14`, `MINIO_MAPPINGS=14`, `MASTER_LINES=1078`, `UNMAPPED_ASSETS=0`, `MISSING_MAPPED_ASSETS=0`.

## 4. Đối chiếu thiết kế, audit và backlog

Đã đọc `docs/superpowers/specs/2026-08-06-project-handoff-docs-design.md` và `audit/audit-knowledge-vng-2026-08-06.md`.

Lệnh chính xác:

```powershell
$statusBacklog = @((Get-Content -LiteralPath 'STATUS.md') | Where-Object { $_ -match '^\| P[1-4] \|' })
$handoffBacklog = @((Get-Content -LiteralPath 'HANDOFF.md') | Where-Object { $_ -match '^\| P[1-4] \|' })
$auditBacklog = @((Get-Content -LiteralPath 'audit\audit-knowledge-vng-2026-08-06.md') | Where-Object { $_ -match '^([1-4])\. ' } | Select-Object -Last 4)
$forbiddenDirectives = @((Get-Content -LiteralPath 'AGENTS.md','PROJECT.md','STATUS.md','HANDOFF.md','DECISIONS.md') | Where-Object { $_ -match '(?i)(sửa trực tiếp|chỉnh sửa trực tiếp)' -and $_ -notmatch '(?i)(không sửa trực tiếp|không chỉnh sửa trực tiếp)' })
"STATUS_BACKLOG_ROWS=$($statusBacklog.Count)"
"HANDOFF_BACKLOG_ROWS=$($handoffBacklog.Count)"
"AUDIT_UNVERIFIED_BACKLOG_ITEMS=$($auditBacklog.Count)"
"DIRECT_GENERATED_ARTIFACT_EDIT_DIRECTIVES=$($forbiddenDirectives.Count)"
$statusBacklog
$handoffBacklog
$auditBacklog
$forbiddenDirectives
if ($statusBacklog.Count -ne 4 -or $handoffBacklog.Count -ne 4 -or $auditBacklog.Count -ne 4 -or $forbiddenDirectives.Count -ne 0) { exit 1 }
```

Exit code: `0`  
Kết quả: `STATUS_BACKLOG_ROWS=4`, `HANDOFF_BACKLOG_ROWS=4`, `AUDIT_UNVERIFIED_BACKLOG_ITEMS=4`, `DIRECT_GENERATED_ARTIFACT_EDIT_DIRECTIVES=0`.

Xác nhận bằng đọc và đối chiếu:

- Số liệu trạng thái `v3.0.1`, 12 module, 14 ảnh/mapping và 7 test phù hợp với thiết kế và audit.
- Snapshot Graph `159/159` cùng `13/14` ảnh hoàn tất trong `STATUS.md` phù hợp với cập nhật đối chiếu cuối trong audit.
- Bốn backlog P1–P4 ở `STATUS.md` và `HANDOFF.md` vẫn là Bị chặn hoặc Chưa xác định, tương ứng bốn mục tại audit.
- Các chỉ dẫn đều cấm sửa trực tiếp module/HTML sinh tự động; không phát hiện chỉ dẫn ngược lại.

## 5. Build nghiêm ngặt

Lệnh chính xác:

```powershell
python scripts\build_handbook.py
```

Exit code: `0`  
Output:

```text
Build complete
- 12 modules: 47,042 bytes
- Offline HTML: 2,379,085 bytes
```

## 6. Kiểm tra HTML sau build

Lệnh chính xác:

```powershell
$html = Get-Content -LiteralPath 'so-tay-tao-knowledge-base.html' -Raw
$htmlBytes = (Get-Item -LiteralPath 'so-tay-tao-knowledge-base.html').Length
$dataUris = [regex]::Matches($html, 'data:image/').Count
$externalScripts = [regex]::Matches($html, '(?i)<script\s+[^>]*\bsrc\s*=').Count
$httpSources = [regex]::Matches($html, '(?i)src\s*=\s*["'']http').Count
$externalStylesheets = [regex]::Matches($html, '(?i)<link\s+[^>]*rel\s*=\s*["'']stylesheet').Count
"HTML_BYTES=$htmlBytes"
"IMAGE_DATA_URIS=$dataUris"
"EXTERNAL_SCRIPT_SRC=$externalScripts"
"HTTP_SRC=$httpSources"
"EXTERNAL_STYLESHEET_LINKS=$externalStylesheets"
if ($dataUris -ne 14 -or $externalScripts -ne 0 -or $httpSources -ne 0 -or $externalStylesheets -ne 0) { exit 1 }
```

Exit code: `0`  
Kết quả: `HTML_BYTES=2379085`, `IMAGE_DATA_URIS=14`, `EXTERNAL_SCRIPT_SRC=0`, `HTTP_SRC=0`, `EXTERNAL_STYLESHEET_LINKS=0`.

## 7. Test hồi quy

Lệnh chính xác:

```powershell
python -m unittest discover -s tests -v
```

Exit code: `0`  
Kết quả: `Ran 7 tests in 0.412s`, `OK`; 7/7 test đạt.

## Sai lệch và lo ngại

Không có sai lệch so với các tiêu chí của Task 3. Không có link hỏng, không có lỗi build/test và không có file/dòng cần controller xử lý.

## 8. Fixes sau review — bằng chứng bổ sung

### A. External runtime dependency của HTML

Checker này chỉ xem runtime resource-bearing tags/CSS. Liên kết tham khảo `<a href>` không được tính là dependency.

Lệnh chính xác:

```powershell
$html = Get-Content -LiteralPath 'so-tay-tao-knowledge-base.html' -Raw
$isExternal = { param([string]$value) $value -match '^(?i:(?:https?:)?//)' }
$getAttribute = {
  param([string]$tag, [string]$name)
  $pattern = ('(?is)\b{0}\s*=\s*(?:"(?<v>[^"]*)"|''(?<v>[^'']*)''|(?<v>[^\s>]+))' -f [regex]::Escape($name))
  $match = [regex]::Match($tag, $pattern)
  if ($match.Success) { return $match.Groups['v'].Value }
  return $null
}
$resourceExternal = [System.Collections.Generic.List[string]]::new()
foreach ($tag in [regex]::Matches($html, '(?is)<(?:script|img|iframe|source|audio|video)\b[^>]*>')) {
  $value = & $getAttribute $tag.Value 'src'
  if ($null -ne $value -and (& $isExternal $value)) { $resourceExternal.Add($tag.Value) }
}
$posterExternal = [System.Collections.Generic.List[string]]::new()
foreach ($tag in [regex]::Matches($html, '(?is)<video\b[^>]*>')) {
  $value = & $getAttribute $tag.Value 'poster'
  if ($null -ne $value -and (& $isExternal $value)) { $posterExternal.Add($tag.Value) }
}
$linkCounts = [ordered]@{ stylesheet = 0; preload = 0; modulepreload = 0; font = 0 }
foreach ($tag in [regex]::Matches($html, '(?is)<link\b[^>]*>')) {
  $rel = (& $getAttribute $tag.Value 'rel')
  $href = (& $getAttribute $tag.Value 'href')
  if ($null -eq $rel -or $null -eq $href -or -not (& $isExternal $href)) { continue }
  foreach ($kind in $linkCounts.Keys) {
    if ($rel -match "(?i)(^|\s)$kind(\s|$)") { $linkCounts[$kind]++ }
  }
}
$cssImports = [regex]::Matches($html, '(?is)@import\s+(?:url\(\s*)?["'']?(?:https?:)?//').Count
$cssUrls = [regex]::Matches($html, '(?is)url\(\s*["'']?(?:https?:)?//').Count
$dataUris = [regex]::Matches($html, 'data:image/').Count
"IMAGE_DATA_URIS=$dataUris"
"EXTERNAL_RESOURCE_TAG_SRC=$($resourceExternal.Count)"
"EXTERNAL_VIDEO_POSTER=$($posterExternal.Count)"
"EXTERNAL_LINK_STYLESHEET=$($linkCounts['stylesheet'])"
"EXTERNAL_LINK_PRELOAD=$($linkCounts['preload'])"
"EXTERNAL_LINK_MODULEPRELOAD=$($linkCounts['modulepreload'])"
"EXTERNAL_LINK_FONT=$($linkCounts['font'])"
"EXTERNAL_CSS_IMPORTS=$cssImports"
"EXTERNAL_CSS_URLS=$cssUrls"
$resourceExternal
$posterExternal
if ($dataUris -ne 14 -or $resourceExternal.Count -ne 0 -or $posterExternal.Count -ne 0 -or ($linkCounts.Values | Measure-Object -Sum).Sum -ne 0 -or $cssImports -ne 0 -or $cssUrls -ne 0) { exit 1 }
```

Exit code: `0`  
Output:

```text
IMAGE_DATA_URIS=14
EXTERNAL_RESOURCE_TAG_SRC=0
EXTERNAL_VIDEO_POSTER=0
EXTERNAL_LINK_STYLESHEET=0
EXTERNAL_LINK_PRELOAD=0
EXTERNAL_LINK_MODULEPRELOAD=0
EXTERNAL_LINK_FONT=0
EXTERNAL_CSS_IMPORTS=0
EXTERNAL_CSS_URLS=0
```

Kết luận phạm vi chính xác: không có external runtime dependency theo các resource-bearing tags/CSS đã kiểm tra.

### B. Parse và đối chiếu backlog có cấu trúc

Tập trạng thái chấp nhận được là ba giá trị phân loại xuất hiện trong tài liệu: `Bị chặn/Chưa xác định`, `Bị chặn`, `Chưa xác định`.

Lệnh chính xác:

```powershell
$allowedStatuses = @('Bị chặn/Chưa xác định','Bị chặn','Chưa xác định')
$parseBacklog = {
  param([string]$path)
  $rows = [System.Collections.Generic.List[object]]::new()
  foreach ($line in Get-Content -LiteralPath $path -Encoding utf8) {
    if ($line -match '^\|\s*(P[1-4])\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|') {
      $rows.Add([pscustomobject]@{ Code = $matches[1]; Title = $matches[2].Trim(); Status = $matches[3].Trim() })
    }
  }
  return @($rows)
}
$statusRows = @(& $parseBacklog 'STATUS.md')
$handoffRows = @(& $parseBacklog 'HANDOFF.md')
$statusCodes = @($statusRows.Code | Sort-Object -Unique)
$handoffCodes = @($handoffRows.Code | Sort-Object -Unique)
$expectedCodes = @('P1','P2','P3','P4')
$statusCodeDiff = @(Compare-Object $expectedCodes $statusCodes)
$handoffCodeDiff = @(Compare-Object $expectedCodes $handoffCodes)
$statusCanonical = @($statusRows | ForEach-Object { "$($_.Code)|$($_.Title)|$($_.Status)" } | Sort-Object)
$handoffCanonical = @($handoffRows | ForEach-Object { "$($_.Code)|$($_.Title)|$($_.Status)" } | Sort-Object)
$backlogDiff = @(Compare-Object $statusCanonical $handoffCanonical)
$invalidStatuses = @($statusRows + $handoffRows | Where-Object { $_.Status -notin $allowedStatuses })
$audit = Get-Content -LiteralPath 'audit\audit-knowledge-vng-2026-08-06.md' -Raw -Encoding utf8
$section12 = [regex]::Match($audit, '(?s)## 12\. Mục bị chặn hoặc chưa xác định\r?\n(?<body>.*?)(?=\r?\n## 13\.)').Groups['body'].Value
$auditPatterns = [ordered]@{
  AUDIT_UPLOAD_FOLDER = '(?i)Upload thư mục thật'
  AUDIT_SYNTHESIS_COMPARISON_NODE = '(?i)node Tổng hợp/So sánh'
  AUDIT_CONNECTOR_STEP_3_4 = '(?i)Bước 3[-–]4.*credential'
  AUDIT_SYNC_BEHAVIOR = '(?i)Hành vi đồng bộ.*Notion, Drive, NAS'
}
"STATUS_PARSED_ROWS=$($statusRows.Count)"
"HANDOFF_PARSED_ROWS=$($handoffRows.Count)"
"STATUS_CODE_SET=$($statusCodes -join ',')"
"HANDOFF_CODE_SET=$($handoffCodes -join ',')"
"STATUS_CODE_DIFF=$($statusCodeDiff.Count)"
"HANDOFF_CODE_DIFF=$($handoffCodeDiff.Count)"
"BACKLOG_COMPARE_OBJECT_DIFF=$($backlogDiff.Count)"
"INVALID_BACKLOG_STATUSES=$($invalidStatuses.Count)"
foreach ($entry in $auditPatterns.GetEnumerator()) {
  $count = [regex]::Matches($section12, $entry.Value).Count
  "$($entry.Key)=$count"
}
$statusRows | ForEach-Object { "STATUS_ROW=$($_.Code)|$($_.Title)|$($_.Status)" }
$handoffRows | ForEach-Object { "HANDOFF_ROW=$($_.Code)|$($_.Title)|$($_.Status)" }
$backlogDiff
$invalidStatuses
$allPatternsPresent = @($auditPatterns.Values | ForEach-Object { [regex]::IsMatch($section12, $_) }) -notcontains $false
if ($statusRows.Count -ne 4 -or $handoffRows.Count -ne 4 -or $statusCodeDiff.Count -ne 0 -or $handoffCodeDiff.Count -ne 0 -or $backlogDiff.Count -ne 0 -or $invalidStatuses.Count -ne 0 -or -not $allPatternsPresent) { exit 1 }
```

Exit code: `0`  
Output:

```text
STATUS_PARSED_ROWS=4
HANDOFF_PARSED_ROWS=4
STATUS_CODE_SET=P1,P2,P3,P4
HANDOFF_CODE_SET=P1,P2,P3,P4
STATUS_CODE_DIFF=0
HANDOFF_CODE_DIFF=0
BACKLOG_COMPARE_OBJECT_DIFF=0
INVALID_BACKLOG_STATUSES=0
AUDIT_UPLOAD_FOLDER=1
AUDIT_SYNTHESIS_COMPARISON_NODE=1
AUDIT_CONNECTOR_STEP_3_4=1
AUDIT_SYNC_BEHAVIOR=1
STATUS_ROW=P1|Upload thư mục thật và cấu trúc thư mục con|Bị chặn/Chưa xác định
STATUS_ROW=P2|Điều kiện sinh node Tổng hợp/So sánh|Chưa xác định
STATUS_ROW=P3|Bước 3–4 connector khi có credential test|Bị chặn
STATUS_ROW=P4|Ma trận đồng bộ thêm/sửa/đổi tên/xóa/quyền ở Notion/Drive/NAS sau khi connector hoạt động|Chưa xác định
HANDOFF_ROW=P1|Upload thư mục thật và cấu trúc thư mục con|Bị chặn/Chưa xác định
HANDOFF_ROW=P2|Điều kiện sinh node Tổng hợp/So sánh|Chưa xác định
HANDOFF_ROW=P3|Bước 3–4 connector khi có credential test|Bị chặn
HANDOFF_ROW=P4|Ma trận đồng bộ thêm/sửa/đổi tên/xóa/quyền ở Notion/Drive/NAS sau khi connector hoạt động|Chưa xác định
```

Kết luận: hai bảng cùng có đúng P1–P4; `Compare-Object` của bộ `code|title|status` bằng 0; mọi status thuộc tập cho phép; section 12 audit có đủ bốn nội dung riêng biệt.

### C. Guard cấm sửa artifact sinh

Danh sách dòng xuất chỉ gồm các dòng trong năm tài liệu nhắc literal `knowledge-vng/*.md` hoặc `so-tay-tao-knowledge-base.html` cùng động từ sửa/chỉnh sửa/thay đổi. Mọi dòng dạng directive đó phải có phủ định `không` hoặc mô tả artifact sinh tự động. Ngoài ra checker xác nhận guard rõ ràng ở `AGENTS.md`, `STATUS.md` và `HANDOFF.md`; guard của `STATUS.md` dùng mô tả “12 module hoặc HTML sinh tự động” thay vì literal filename.

Lệnh chính xác:

```powershell
$docs = @('AGENTS.md','PROJECT.md','STATUS.md','HANDOFF.md','DECISIONS.md')
$artifactReference = '(?i)(knowledge-vng/\*\.md|so-tay-tao-knowledge-base\.html)'
$editVerb = '(?i)(sửa|chỉnh sửa|thay đổi)'
$directiveLines = [System.Collections.Generic.List[object]]::new()
foreach ($doc in $docs) {
  $lineNumber = 0
  foreach ($line in Get-Content -LiteralPath $doc -Encoding utf8) {
    $lineNumber++
    if ($line -match $artifactReference -and $line -match $editVerb) {
      $directiveLines.Add([pscustomobject]@{ File = $doc; Line = $lineNumber; Text = $line })
    }
  }
}
$unsafeDirectives = @($directiveLines | Where-Object {
  $_.Text -notmatch '(?i)\bkhông\b' -and $_.Text -notmatch '(?i)(artifact|module|HTML)\s+sinh\s+tự\s+động'
})
$guardPatterns = @{
  'AGENTS.md' = '(?i)knowledge-vng/\*\.md.*sinh tự động.*không sửa trực tiếp'
  'STATUS.md' = '(?i)không sửa trực tiếp 12 module hoặc HTML sinh tự động'
  'HANDOFF.md' = '(?i)không sửa trực tiếp.*knowledge-vng/\*\.md.*so-tay-tao-knowledge-base\.html.*artifact sinh tự động'
}
$missingGuards = [System.Collections.Generic.List[string]]::new()
foreach ($entry in $guardPatterns.GetEnumerator()) {
  $hasGuard = @(Get-Content -LiteralPath $entry.Key -Encoding utf8 | Where-Object { $_ -match $entry.Value }).Count -gt 0
  if (-not $hasGuard) { $missingGuards.Add($entry.Key) }
}
"ARTIFACT_EDIT_REFERENCE_LINES=$($directiveLines.Count)"
"UNSAFE_ARTIFACT_EDIT_DIRECTIVES=$($unsafeDirectives.Count)"
"MISSING_EXPLICIT_ARTIFACT_GUARDS=$($missingGuards.Count)"
$directiveLines | ForEach-Object { "ARTIFACT_DIRECTIVE=$($_.File):$($_.Line):$($_.Text)" }
$unsafeDirectives | ForEach-Object { "UNSAFE_DIRECTIVE=$($_.File):$($_.Line):$($_.Text)" }
$missingGuards | ForEach-Object { "MISSING_GUARD=$_" }
if ($directiveLines.Count -eq 0 -or $unsafeDirectives.Count -ne 0 -or $missingGuards.Count -ne 0) { exit 1 }
```

Exit code: `0`  
Output:

```text
ARTIFACT_EDIT_REFERENCE_LINES=3
UNSAFE_ARTIFACT_EDIT_DIRECTIVES=0
MISSING_EXPLICIT_ARTIFACT_GUARDS=0
ARTIFACT_DIRECTIVE=AGENTS.md:18:- `knowledge-vng/*.md` là 12 module sinh tự động; không sửa trực tiếp.
ARTIFACT_DIRECTIVE=AGENTS.md:19:- `so-tay-tao-knowledge-base.html` là HTML sinh tự động; không sửa trực tiếp.
ARTIFACT_DIRECTIVE=HANDOFF.md:64:- Không sửa trực tiếp `knowledge-vng/*.md` hoặc `so-tay-tao-knowledge-base.html`: đây là artifact sinh tự động.
```

Kết luận phạm vi chính xác: không có directive cho phép sửa trực tiếp artifact sinh trong các dòng filename-literal đã xuất; ba guard rõ ràng bắt buộc tại `AGENTS.md`, `STATUS.md` và `HANDOFF.md` đều hiện diện.

## 9. Re-review fix — kiểm chứng thay thế A–C

Mục này thay thế bằng chứng ở mục 8 cho ba finding Important. Các checker dưới đây dùng `python` standard library; không sửa file nào ngoài report này.

### 9.1 HTML parser: external runtime dependency đầy đủ

`html.parser` duyệt mọi tag/attribute. Checker xem `src`, `srcset` (từng candidate), `poster`, `data`, `xlink:href`, `background`, `archive`, `codebase`, và `href` trên mọi tag trừ `a`/`area`; đồng thời quét CSS trong `<style>`/`style` và script inline. URL `http(s)` hoặc protocol-relative (`//`) trong các resource-bearing location là lỗi. `<a href>` và `<area href>` tham khảo được loại trừ có chủ đích.

Lệnh chính xác:

```powershell
@'
from html.parser import HTMLParser
from pathlib import Path
import re

html = Path('so-tay-tao-knowledge-base.html').read_text(encoding='utf-8')
EXTERNAL = re.compile(r'^(?:https?:)?//', re.I)
CSS_IMPORT = re.compile(r'@import\s+(?:url\(\s*)?["\']?(?:https?:)?//', re.I)
CSS_URL = re.compile(r'url\(\s*["\']?(?:https?:)?//', re.I)
SCRIPT_URL = re.compile(r'(?:https?:)?//', re.I)
NETWORK_PRIMITIVE = re.compile(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\b|\bimport\s*\(', re.I)
RESOURCE_ATTRS = ('src', 'poster', 'data', 'xlink:href', 'background', 'archive', 'codebase')

class DependencyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.counts = {f'EXTERNAL_{name.upper().replace(":", "_").replace("-", "_")}': 0 for name in RESOURCE_ATTRS}
        self.counts.update({
            'EXTERNAL_SRCSET': 0,
            'EXTERNAL_NON_ANCHOR_HREF': 0,
            'EXTERNAL_CSS_IMPORT': 0,
            'EXTERNAL_CSS_URL': 0,
            'EXTERNAL_SCRIPT_URL': 0,
            'SCRIPT_NETWORK_PRIMITIVE': 0,
        })
        self.in_style = False
        self.in_script = False
        self.style_text = []
        self.script_text = []
    def inspect_css(self, text):
        self.counts['EXTERNAL_CSS_IMPORT'] += len(CSS_IMPORT.findall(text))
        self.counts['EXTERNAL_CSS_URL'] += len(CSS_URL.findall(text))
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attr in RESOURCE_ATTRS:
            value = attrs.get(attr)
            if not value:
                continue
            values = value.split() if attr == 'archive' else [value]
            self.counts[f'EXTERNAL_{attr.upper().replace(":", "_").replace("-", "_")}'] += sum(bool(EXTERNAL.match(item)) for item in values)
        srcset = attrs.get('srcset')
        if srcset:
            for candidate in srcset.split(','):
                url = candidate.strip().split(maxsplit=1)[0] if candidate.strip() else ''
                self.counts['EXTERNAL_SRCSET'] += bool(EXTERNAL.match(url))
        href = attrs.get('href')
        if href and tag not in ('a', 'area'):
            self.counts['EXTERNAL_NON_ANCHOR_HREF'] += bool(EXTERNAL.match(href))
        style = attrs.get('style')
        if style:
            self.inspect_css(style)
        if tag == 'style':
            self.in_style = True
            self.style_text = []
        if tag == 'script':
            self.in_script = True
            self.script_text = []
    def handle_data(self, data):
        if self.in_style:
            self.style_text.append(data)
        if self.in_script:
            self.script_text.append(data)
    def handle_endtag(self, tag):
        if tag == 'style' and self.in_style:
            self.inspect_css(''.join(self.style_text))
            self.in_style = False
        if tag == 'script' and self.in_script:
            script = ''.join(self.script_text)
            self.counts['EXTERNAL_SCRIPT_URL'] += len(SCRIPT_URL.findall(script))
            self.counts['SCRIPT_NETWORK_PRIMITIVE'] += len(NETWORK_PRIMITIVE.findall(script))
            self.in_script = False

parser = DependencyParser()
parser.feed(html)
parser.close()
print(f'IMAGE_DATA_URIS={html.count("data:image/")}')
for key, value in parser.counts.items():
    print(f'{key}={value}')
total = sum(parser.counts.values())
print(f'EXTERNAL_RUNTIME_DEPENDENCY_TOTAL={total}')
if html.count('data:image/') != 14 or total != 0:
    raise SystemExit(1)
'@ | python -
```

Exit code: `0`  
Output:

```text
IMAGE_DATA_URIS=14
EXTERNAL_SRC=0
EXTERNAL_POSTER=0
EXTERNAL_DATA=0
EXTERNAL_XLINK_HREF=0
EXTERNAL_BACKGROUND=0
EXTERNAL_ARCHIVE=0
EXTERNAL_CODEBASE=0
EXTERNAL_SRCSET=0
EXTERNAL_NON_ANCHOR_HREF=0
EXTERNAL_CSS_IMPORT=0
EXTERNAL_CSS_URL=0
EXTERNAL_SCRIPT_URL=0
SCRIPT_NETWORK_PRIMITIVE=0
EXTERNAL_RUNTIME_DEPENDENCY_TOTAL=0
```

Kết luận phạm vi chính xác: không có external runtime dependency theo mọi resource-bearing attribute/CSS/script inline đã kiểm tra; external `<a href>`/`<area href>` tham khảo không nằm trong phạm vi dependency và được phép.

### 9.2 Audit section 12: heading boundary, ordinal và pattern chính xác

Checker cắt từ heading `## 12.` đến heading `##` kế tiếp, parse mọi numbered top-level item (`^\d+\.`), bắt buộc đúng bốn item có ordinal `1,2,3,4`; bốn pattern nội dung được kiểm tra mỗi pattern đúng một lần. Chuẩn hóa Unicode chỉ để đối sánh không phụ thuộc console, còn output giữ nguyên văn audit.

Lệnh chính xác:

```powershell
@'
from pathlib import Path
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
def folded(value):
    decomposed = unicodedata.normalize('NFD', value).replace('\u0111', 'd').replace('\u0110', 'D')
    return ''.join(char for char in decomposed if unicodedata.category(char) != 'Mn').casefold()

audit = Path('audit/audit-knowledge-vng-2026-08-06.md').read_text(encoding='utf-8')
section = re.search(r'^## 12\..*?\n(?P<body>.*?)(?=^##\s+|\Z)', audit, re.M | re.S)
if not section:
    raise SystemExit(1)
body = section.group('body')
items = [(int(match.group('ordinal')), re.sub(r'\s+', ' ', match.group('text')).strip())
         for match in re.finditer(r'^(?P<ordinal>\d+)\.\s+(?P<text>.*?)(?=^\d+\.\s+|\Z)', body, re.M | re.S)]
patterns = {
    'AUDIT_UPLOAD_FOLDER': r'upload thu muc that',
    'AUDIT_SYNTHESIS_COMPARISON_NODE': r'node tong hop/so sanh',
    'AUDIT_CONNECTOR_STEP_3_4': r'buoc 3-4.*credential',
    'AUDIT_SYNC_BEHAVIOR': r'hanh vi dong bo.*notion, drive, nas',
}
normalized_body = folded(body)
print(f'AUDIT_SECTION12_TOP_LEVEL_ITEMS={len(items)}')
print('AUDIT_SECTION12_ORDINALS=' + ','.join(str(ordinal) for ordinal, _ in items))
for ordinal, text in items:
    print(f'AUDIT_SECTION12_ITEM={ordinal}|{text}')
pattern_counts = {}
for name, pattern in patterns.items():
    pattern_counts[name] = len(re.findall(pattern, normalized_body, re.S))
    print(f'{name}={pattern_counts[name]}')
if len(items) != 4 or [ordinal for ordinal, _ in items] != [1, 2, 3, 4] or any(count != 1 for count in pattern_counts.values()):
    raise SystemExit(1)
'@ | python -
```

Exit code: `0`  
Output:

```text
AUDIT_SECTION12_TOP_LEVEL_ITEMS=4
AUDIT_SECTION12_ORDINALS=1,2,3,4
AUDIT_SECTION12_ITEM=1|Upload thư mục thật và cấu trúc thư mục con sau upload.
AUDIT_SECTION12_ITEM=2|Điều kiện sinh node Tổng hợp/So sánh.
AUDIT_SECTION12_ITEM=3|Bước 3-4 của nguồn dữ liệu ngoài khi có credential.
AUDIT_SECTION12_ITEM=4|Hành vi đồng bộ thêm/sửa/đổi tên/xóa/quyền ở Notion, Drive, NAS. Các mục này phải tiếp tục mang nhãn Bị chặn/Chưa xác định trong tài liệu chính.
AUDIT_UPLOAD_FOLDER=1
AUDIT_SYNTHESIS_COMPARISON_NODE=1
AUDIT_CONNECTOR_STEP_3_4=1
AUDIT_SYNC_BEHAVIOR=1
```

### 9.3 Guard: phủ định rõ ràng trên cùng dòng

Checker lấy mọi dòng trong năm docs có generated target literal (`knowledge-vng/*.md`, filename HTML) hoặc cụm `12 module ... HTML sinh tự động`, đồng thời có edit verb. Một dòng bị unsafe nếu không có `không` hoặc `cấm` gắn với edit verb trên chính dòng đó; cụm “sinh tự động” không được dùng làm điều kiện an toàn. Nó cũng assert ba guard bắt buộc tại `AGENTS.md`, `STATUS.md`, `HANDOFF.md`.

Lệnh chính xác:

```powershell
@'
from pathlib import Path
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
def folded(value):
    decomposed = unicodedata.normalize('NFD', value).replace('\u0111', 'd').replace('\u0110', 'D')
    return ''.join(char for char in decomposed if unicodedata.category(char) != 'Mn').casefold()

docs = ['AGENTS.md', 'PROJECT.md', 'STATUS.md', 'HANDOFF.md', 'DECISIONS.md']
generated_target = re.compile(r'knowledge-vng/\*\.md|so-tay-tao-knowledge-base\.html|12 module.*html sinh tu dong', re.I)
edit_verb = re.compile(r'sua|chinh sua|thay doi', re.I)
clear_negation = re.compile(r'(?:khong|cam).{0,40}(?:sua|chinh sua|thay doi)|(?:sua|chinh sua|thay doi).{0,40}(?:khong|cam)', re.I)
directives = []
for doc in docs:
    for line_number, line in enumerate(Path(doc).read_text(encoding='utf-8').splitlines(), start=1):
        normalized = folded(line)
        if generated_target.search(normalized) and edit_verb.search(normalized):
            directives.append((doc, line_number, line, bool(clear_negation.search(normalized))))
unsafe = [entry for entry in directives if not entry[3]]
required_guards = {
    'AGENTS.md': lambda line: 'knowledge-vng/*.md' in folded(line) and 'khong sua truc tiep' in folded(line),
    'STATUS.md': lambda line: 'khong sua truc tiep 12 module hoac html sinh tu dong' in folded(line),
    'HANDOFF.md': lambda line: 'knowledge-vng/*.md' in folded(line) and 'so-tay-tao-knowledge-base.html' in folded(line) and 'khong sua truc tiep' in folded(line),
}
missing_guards = [doc for doc, predicate in required_guards.items() if not any(predicate(line) for line in Path(doc).read_text(encoding='utf-8').splitlines())]
print(f'GENERATED_TARGET_EDIT_LINES={len(directives)}')
print(f'UNSAFE_GENERATED_TARGET_EDIT_LINES={len(unsafe)}')
print(f'MISSING_REQUIRED_GUARD_LINES={len(missing_guards)}')
for doc, line_number, line, _ in directives:
    print(f'GENERATED_TARGET_EDIT_LINE={doc}:{line_number}:{line}')
for doc, line_number, line, _ in unsafe:
    print(f'UNSAFE_GENERATED_TARGET_EDIT_LINE={doc}:{line_number}:{line}')
for doc in missing_guards:
    print(f'MISSING_REQUIRED_GUARD={doc}')
if not directives or unsafe or missing_guards:
    raise SystemExit(1)
'@ | python -
```

Exit code: `0`  
Output:

```text
GENERATED_TARGET_EDIT_LINES=4
UNSAFE_GENERATED_TARGET_EDIT_LINES=0
MISSING_REQUIRED_GUARD_LINES=0
GENERATED_TARGET_EDIT_LINE=AGENTS.md:18:- `knowledge-vng/*.md` là 12 module sinh tự động; không sửa trực tiếp.
GENERATED_TARGET_EDIT_LINE=AGENTS.md:19:- `so-tay-tao-knowledge-base.html` là HTML sinh tự động; không sửa trực tiếp.
GENERATED_TARGET_EDIT_LINE=STATUS.md:54:- Chỉ sửa nội dung sổ tay tại [so-tay-tao-knowledge-base-v3.md](so-tay-tao-knowledge-base-v3.md); không sửa trực tiếp 12 module hoặc HTML sinh tự động.
GENERATED_TARGET_EDIT_LINE=HANDOFF.md:64:- Không sửa trực tiếp `knowledge-vng/*.md` hoặc `so-tay-tao-knowledge-base.html`: đây là artifact sinh tự động.
```

Kết luận re-review: ba finding đã được kiểm chứng lại bằng parser/assertion chặt hơn; không có check hợp lệ nào fail, nên trạng thái report vẫn là `DONE` (không phải `BLOCKED`).
