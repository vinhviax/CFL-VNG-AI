# -*- coding: utf-8 -*-
"""Thay URI MinIO cu bang URI ban ket xuat (exports/) moi cho 21 file .md
tren Drive cong ty, dua theo comment LOCAL_ASSET lam neo khop dung anh.
Chi thay dung 1 URI ngay sau moi LOCAL_ASSET khop ten trong MAP.
"""
import json
import os
import re
import shutil

BASE = r"J:/.shortcut-targets-by-id/1MFx5oXxwi54JNZA3sRKa1LdFXnP-VHdG/VNGGames AI/knowledge/GS9 Knowledge VNG AI"
BACKUP_DIR = r"C:/Users/CPU13114/AppData/Local/Temp/claude/J--My-Drive-CFL-VNG-AI/6db794fa-82b3-429b-818b-cbe1f6658a3c/scratchpad/backup_doc_md"

PREFIX = "minio://knowledge-base-prd/10012/exports/"

MAP = {
    "image-01-tong-quan-danh-sach-knowledge.png": "4d3d44e1-d270-487a-9405-036833861e7f.png",
    "image-02-cau-hinh-tong-quan-document.png": "f762c7c4-60b4-48fe-bfd5-b48a5aba48b5.png",
    "image-03-cau-hinh-mo-hinh-vlm-asr.png": "b2de7c9e-728e-4795-bb23-78d32064620b.png",
    "image-04-xu-ly-parser-theo-dinh-dang.png": "ee32172f-2641-4918-aaae-a46cc07e4fd6.png",
    "image-05-xu-ly-phan-doan-cha-con.png": "908dc540-5d28-4053-9f1d-93dfe1eaa475.png",
    "image-06-chia-se-va-phan-quyen.png": "28669622-80e9-46d7-9e7c-0f9ff5c442be.png",
    "image-07-nguon-du-lieu-notion-drive-nas.png": "6739ab61-e3a0-401b-a9e9-8131a5199da9.png",
    "image-08-tai-tep-thu-muc-va-soan-thao.png": "ff3e10b8-4ba2-4181-9d5e-cb74e9408d42.png",
    "image-09-wiki-muc-luc-va-trang.png": "e0c4b33c-a656-43d3-ad06-5fff26ab7bee.png",
    "image-10-graph-cac-loai-node.png": "d32f50d0-5faf-4417-859e-9e076c8e5693.png",
    "image-11-faq-danh-sach-nhap-xuat-tim-kiem.png": "f1ece587-097c-4aac-a827-a564b298beb7.png",
    "image-12-faq-bieu-mau-them-qa.png": "3e2f81b5-022c-4d3f-a32f-f02526f4b513.png",
    "image-13-chat-hien-thi-anh-minio.png": "462923ab-4a3e-45b0-9f7c-1927b1a525f8.png",
    "image-14-chat-khong-hien-thi-duong-dan-tuong-doi.png": "302b1e4c-f35d-4aa3-ad9a-5c482985408d.png",
    "image-15-google-drive-xac-thuc-service-account.png": "64266508-8a5f-44c2-bb27-b6103bd9b1d6.png",
    "image-16-google-drive-chon-tai-nguyen.png": "a189c9b7-b453-4852-92ee-3fc4e27c61e8.png",
    "image-17-google-drive-lich-va-cach-dong-bo.png": "b86b4101-8e8d-42c0-b8cb-14aa26de03c3.png",
    "image-18-google-drive-loc-tep-va-tag.png": "667cfd07-ec8e-4106-8ed7-c6cd50c11c28.png",
    "image-19-google-drive-ghi-de-xu-ly.png": "0d0b7fca-af3f-470d-884a-e79bd171cad4.png",
    "image-20-google-drive-da-phuong-thuc-va-parser.png": "463a8a6f-5f35-4dcd-b564-749ba6e283df.png",
    "image-21-google-drive-parser-office-text.png": "04d66134-3b6b-4233-becc-a468d1c33c71.png",
    "image-22-google-drive-parser-media-web.png": "a2a0ab9c-e71f-49c0-9af0-e93eace1516b.png",
    "image-23-google-drive-dong-bo-xoa.png": "c2ec9f4c-a640-4908-aec2-7791fdfd0e78.png",
    "image-24-google-drive-parser-excel-tuy-chinh.png": "bd3e7580-e22d-417d-a1c6-9610417cfb48.png",
    "image-25-google-drive-dong-bo-thanh-cong.png": "dea09974-90cf-42ed-80f9-25d00dfb3f4e.png",
    "image-26-agent-tong-quan-danh-sach.png": "a0cd525e-8e7f-4642-a5b3-d19a93c3b7a0.png",
    "image-27-agent-thong-tin-co-ban-va-intent.png": "e688090a-3177-4577-a7aa-0249f1de4c45.png",
    "image-28-agent-cau-hinh-mo-hinh.png": "068b9def-31bb-421a-b67c-0bebf1383ed9.png",
    "image-29-agent-kho-tri-thuc.png": "959c8253-c708-4bec-b517-3517e309cbc4.png",
    "image-30-agent-cong-cu.png": "d67ec200-fb78-4e7b-a89a-e366f3292173.png",
    "image-31-agent-chien-luoc-truy-hoi.png": "889957f1-b7de-4ded-ad7d-62e987bd5ecc.png",
    "image-32-agent-cau-hinh-da-phuong-thuc.png": "e71d01e5-3862-48cd-b7bd-508c254f4b95.png",
    "image-33-agent-chat-nguon-va-anh.png": "ddd7572b-0986-4b38-84cf-933fbbd6614b.png",
    "image-34-agent-danh-gia-cau-tra-loi.png": "55775df7-5de4-4a76-8672-6ad94a02f973.png",
    "image-35-agent-che-do-va-preset.png": "10f70fc0-80fa-4587-98a4-0a0fcc26a2dd.png",
    "image-36-agent-system-prompt-va-bien.png": "33f9a9e4-4b45-455f-80da-37516ad8a414.png",
    "image-37-agent-intent-va-prompt-ghi-de.png": "27dc8f3a-2f22-4c48-837d-30df0203a58a.png",
    "image-38-agent-intent-trace-runtime.png": "bdf82a0f-afe2-408f-bfa7-7ea74c28f452.png",
    "image-39-agent-model-ab-va-request-info.png": "c29e63f2-8406-4385-8084-2e8f79aa3b3e.png",
    "image-40-agent-quota-timeout-va-loi-runtime.png": "c98c6de6-db2a-467e-b6d1-5ebfa52d2fde.png",
    "image-41-agent-test-kb-da-nguon.png": "d33d80ef-751f-46e4-9a0f-2ff89f2163b5.png",
    "image-42-agent-at-kho-tri-thuc-va-tep.png": "dcc18d1b-73ec-4807-8dfd-fc6c02742115.png",
    "image-43-agent-trace-cong-cu-truy-hoi.png": "9da4103a-78ec-48e5-ad58-8c31089ee9d4.png",
    "image-44-agent-ab-topk-threshold-rerank.png": "e765893c-39fc-41d7-a008-c18b0dffe725.png",
    "image-45-agent-tep-dinh-kem.png": "b7f1f751-d26f-4b4f-b8e1-cdd1b761bffc.png",
    "image-46-agent-image-analysis.png": "30c176a0-4903-4886-af09-badc6f5192f0.png",
    "image-47-agent-document-summarize.png": "c88ee1ea-6ca8-4668-ad78-43c7130e5921.png",
    "image-48-agent-lich-su-va-request-information.png": "21788a5d-919e-438f-bcc5-4386bf982fb7.png",
    "image-49-agent-chia-se-va-vong-doi.png": "e5c15742-730b-4e8f-9ea5-0f54001ff535.png",
    "image-50-them-tri-thuc-nut-tren-cau-tra-loi.png": "9b6fd721-0304-4c14-96a7-887e2a2dd0af.png",
    "image-51-them-tri-thuc-hop-thoai-tao-markdown.png": "18e869bc-0525-43a4-b4c2-fba41900a293.png",
    "image-52-them-tri-thuc-tai-lieu-ban-nhap-trong-kho.png": "8bf2c185-38cf-478d-a934-6fd0e006a57b.png",  # placeholder, overwritten below
}
# image-52 that gia tri dung tu doc-52 (khong phai bf2c... la URI CU); fix ngay:
MAP["image-52-them-tri-thuc-tai-lieu-ban-nhap-trong-kho.png"] = "85e5f4d5-8a21-4c75-9ffa-cdb5a0aa5ea7.png"

assert len(MAP) == 52, f"can dung 52, dang co {len(MAP)}"

PATTERN = re.compile(
    r'(<!--\s*LOCAL_ASSET:\s*\./(?P<fname>[A-Za-z0-9._-]+)\s*-->\s*\n!\[[^\]]*\]\()'
    r'(?P<uri>minio://[^)]*)'
    r'(\))'
)

os.makedirs(BACKUP_DIR, exist_ok=True)

total_replacements = 0
report = []
for name in sorted(os.listdir(BASE)):
    if not (name.startswith("doc-") and name.endswith(".md")):
        continue
    path = os.path.join(BASE, name)
    with open(path, "r", encoding="utf-8", newline="") as f:
        original = f.read()

    unmatched = []

    def _sub(m):
        global total_replacements
        fname = m.group("fname")
        new_uuid = MAP.get(fname)
        if new_uuid is None:
            unmatched.append(fname)
            return m.group(0)
        new_uri = PREFIX + new_uuid
        if new_uri == m.group("uri"):
            return m.group(0)
        total_replacements += 1
        return m.group(1) + new_uri + m.group(4)

    updated = PATTERN.sub(_sub, original)

    if unmatched:
        report.append(f"  CANH BAO {name}: khong tim thay trong MAP -> {unmatched}")

    if updated != original:
        shutil.copy2(path, os.path.join(BACKUP_DIR, name))
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(updated)
        os.replace(tmp, path)
        report.append(f"  DA SUA {name}")
    else:
        report.append(f"  khong doi {name}")

print("Tong so URI da thay:", total_replacements)
for line in report:
    print(line)
