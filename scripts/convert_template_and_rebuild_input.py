# -*- coding: utf-8 -*-
from pathlib import Path
import datetime as _dt
import json
import re
import shutil
import textwrap
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "QLNhaSach_BaoCao"
INPUTS = WORKSPACE / "00_inputs"
TEMPLATE = INPUTS / "BaoCaoMau.docx"
TEMPLATE_FALLBACK = ROOT / "BaoCaoMau.docx"

MD_DIR = WORKSPACE / "01_template_markdown"
MEDIA_DIR = MD_DIR / "media"
CHAPTER_DIR = MD_DIR / "chapters"
KB_DIR = WORKSPACE / "03_knowledge_base"
HISTORY_DIR = WORKSPACE / "13_history"
LOG_DIR = WORKSPACE / "11_logs"
VALIDATION_DIR = WORKSPACE / "10_validation"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def now():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    for path in [
        INPUTS,
        MD_DIR,
        MEDIA_DIR,
        CHAPTER_DIR,
        KB_DIR,
        HISTORY_DIR,
        LOG_DIR,
        VALIDATION_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def next_version(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    match = re.match(r"^(.*)_v(\d+)$", stem)
    if match:
        base = match.group(1)
        start = int(match.group(2)) + 1
    else:
        base = stem
        start = 2
    index = start
    while True:
        candidate = parent / f"{base}_v{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def slugify(value: str, fallback: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value).strip("-")
    return value[:70] or fallback


def repair_vietnamese_mojibake(value: str) -> str:
    """Fix common UTF-8 text that was previously decoded as Windows-1252."""
    if not value:
        return value
    markers = ("Ã", "á»", "áº", "Ä", "Æ", "â€“", "â€œ", "â€")
    if not any(marker in value for marker in markers):
        return value
    try:
        fixed = value.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return value
    return fixed


def copy_template_if_needed():
    if TEMPLATE.exists():
        return
    if TEMPLATE_FALLBACK.exists():
        shutil.copy2(TEMPLATE_FALLBACK, TEMPLATE)
        return
    raise FileNotFoundError("Khong tim thay BaoCaoMau.docx trong 00_inputs hoac thu muc goc.")


def read_zip_text(zf, name):
    try:
        return zf.read(name).decode("utf-8")
    except KeyError:
        return ""


def read_relationships(zf):
    rels = {}
    text = read_zip_text(zf, "word/_rels/document.xml.rels")
    if not text:
        return rels
    root = ET.fromstring(text)
    for rel in root.findall("rel:Relationship", NS):
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            rels[rid] = target
    return rels


def extract_media(zf, media_base: Path):
    media_base.mkdir(parents=True, exist_ok=True)
    copied = {}
    for name in zf.namelist():
        if name.startswith("word/media/") and not name.endswith("/"):
            out = media_base / Path(name).name
            out.write_bytes(zf.read(name))
            copied[name] = out
            copied[name.replace("word/", "")] = out
            copied[name.replace("word/", "../")] = out
    return copied


def paragraph_style(paragraph):
    node = paragraph.find("w:pPr/w:pStyle", NS)
    if node is None:
        return ""
    return node.attrib.get(f"{{{NS['w']}}}val", "")


def paragraph_text(paragraph):
    parts = []
    for node in paragraph.iter():
        if node.tag == f"{{{NS['w']}}}t" and node.text:
            parts.append(node.text)
        elif node.tag == f"{{{NS['w']}}}tab":
            parts.append("\t")
        elif node.tag == f"{{{NS['w']}}}br":
            parts.append("\n")
    return repair_vietnamese_mojibake("".join(parts).strip())


def paragraph_images(paragraph, rels, media_files):
    images = []
    for blip in paragraph.findall(".//a:blip", NS):
        rid = blip.attrib.get(f"{{{NS['r']}}}embed")
        target = rels.get(rid or "")
        if not target:
            continue
        normalized = target
        if not normalized.startswith("word/") and not normalized.startswith("media/"):
            normalized = f"word/{normalized}"
        media_path = media_files.get(normalized) or media_files.get(target)
        if media_path:
            rel_path = media_path.relative_to(MD_DIR).as_posix()
            images.append(f"![Hinh minh hoa]({rel_path})")
    return images


def table_to_markdown(table):
    rows = []
    for tr in table.findall("w:tr", NS):
        cells = []
        for tc in tr.findall("w:tc", NS):
            text = " ".join(t.strip() for t in tc.itertext() if t and t.strip())
            text = repair_vietnamese_mojibake(text)
            text = re.sub(r"\s+", " ", text).replace("|", "\\|")
            cells.append(text)
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    max_cols = max(len(row) for row in rows)
    rows = [row + [""] * (max_cols - len(row)) for row in rows]
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join(["---"] * max_cols) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows[1:]]
    return "\n".join([header, sep] + body)


def style_to_heading(style):
    compact = style.lower().replace(" ", "")
    match = re.search(r"heading(\d+)|tocheading(\d+)", compact)
    if match:
        level = int(match.group(1) or match.group(2))
        return max(1, min(level, 6))
    if compact in {"title", "titlestyle"}:
        return 1
    return 0


def convert_docx_to_markdown():
    output_media = next_version(MEDIA_DIR / "BaoCaoMau_v1")
    full_md = next_version(MD_DIR / "BaoCaoMau_converted_v1.md")
    with zipfile.ZipFile(TEMPLATE) as zf:
        rels = read_relationships(zf)
        media_files = extract_media(zf, output_media)
        document_xml = read_zip_text(zf, "word/document.xml")
        app_xml = read_zip_text(zf, "docProps/app.xml")

    document = ET.fromstring(document_xml)
    body = document.find("w:body", NS)
    lines = [
        "---",
        "source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx",
        f"converted_at: {now()}",
        "converter: scripts/convert_template_and_rebuild_input.py",
        "---",
        "",
    ]

    app_pages = ""
    if app_xml:
        app_root = ET.fromstring(app_xml)
        for child in app_root.iter():
            if child.tag.endswith("Pages") and child.text:
                app_pages = child.text
                break
    if app_pages:
        lines.extend([f"> So trang docProps/app.xml: {app_pages}", ""])

    for child in list(body):
        if child.tag == f"{{{NS['w']}}}p":
            text = paragraph_text(child)
            images = paragraph_images(child, rels, media_files)
            heading = style_to_heading(paragraph_style(child))
            if text:
                if heading:
                    lines.append(f"{'#' * heading} {text}")
                else:
                    lines.append(text)
                lines.append("")
            for image in images:
                lines.append(image)
                lines.append("")
        elif child.tag == f"{{{NS['w']}}}tbl":
            md_table = table_to_markdown(child)
            if md_table:
                lines.append(md_table)
                lines.append("")

    content = "\n".join(lines).replace("\r\n", "\n")
    full_md.write_text(content, encoding="utf-8")
    chapters = split_chapters(content, full_md.stem)
    return full_md, output_media, chapters, app_pages


def split_chapters(content, stem):
    chapter_paths = []
    current_title = "front_matter"
    current_lines = []
    chapter_index = 0

    def flush():
        nonlocal chapter_index, current_lines, current_title
        if not "".join(current_lines).strip():
            return
        chapter_index += 1
        name = f"{chapter_index:02d}_{slugify(current_title, 'chuong')}.md"
        out = next_version(CHAPTER_DIR / name)
        out.write_text("\n".join(current_lines).strip() + "\n", encoding="utf-8")
        chapter_paths.append(out)

    for line in content.splitlines():
        if line.startswith("# ") and current_lines:
            flush()
            current_title = line[2:].strip()
            current_lines = [line]
        else:
            if line.startswith("# "):
                current_title = line[2:].strip()
            current_lines.append(line)
    flush()
    return chapter_paths


def load_text(path: Path, missing=""):
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace").strip()
    return missing


def load_json(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def scan_source_facts():
    controller_files = sorted((ROOT / "BaiTapLon").glob("**/*Controller.cs"))
    controllers = []
    action_pattern = re.compile(r"public\s+(?:async\s+)?(?:ActionResult|JsonResult|PartialViewResult|FileResult|ContentResult|Task<[^>]+>)\s+([A-Za-z0-9_]+)\s*\(")
    for file in controller_files:
        if "\\obj\\" in str(file):
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        actions = sorted(set(action_pattern.findall(text)))
        controllers.append(
            {
                "path": str(file.relative_to(ROOT)).replace("\\", "/"),
                "name": file.stem,
                "actions": actions[:40],
            }
        )

    dbsets = []
    for file in [ROOT / "Mood" / "EF2" / "QuanLySachDBContext.cs", ROOT / "Mood" / "EF2" / "LogDbContext.cs"]:
        if file.exists():
            text = file.read_text(encoding="utf-8", errors="ignore")
            for model, name in re.findall(r"DbSet<([^>]+)>\s+([A-Za-z0-9_]+)\s*\{", text):
                dbsets.append({"context": file.stem, "model": model, "dbset": name})

    services = []
    for file in sorted((ROOT / "BaiTapLon" / "Services").glob("*.cs")):
        services.append(str(file.relative_to(ROOT)).replace("\\", "/"))
    for file in sorted((ROOT / "Common").glob("**/*Repository.cs")):
        services.append(str(file.relative_to(ROOT)).replace("\\", "/"))

    migrations = [str(p.relative_to(ROOT)).replace("\\", "/") for p in sorted((ROOT / "sql" / "migrations").glob("*.sql"))]
    tests = [str(p.relative_to(ROOT)).replace("\\", "/") for p in sorted((ROOT / "Tests").glob("*.cs"))]
    flask_routes = []
    flask_app = ROOT / "face_auth_api" / "app.py"
    if flask_app.exists():
        text = flask_app.read_text(encoding="utf-8", errors="ignore")
        for route, methods in re.findall(r"@app\.route\(['\"]([^'\"]+)['\"](?:,\s*methods\s*=\s*(\[[^\]]+\]))?", text):
            flask_routes.append({"route": route, "methods": methods or "['GET']"})
        for method, route in re.findall(r"@app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]", text):
            flask_routes.append({"route": route, "methods": f"['{method.upper()}']"})
    return {
        "controllers": controllers,
        "dbsets": dbsets,
        "services": services,
        "migrations": migrations,
        "tests": tests,
        "flask_routes": flask_routes,
    }


def bullet(items, formatter=str):
    return "\n".join(f"- {formatter(item)}" for item in items)


def build_full_input(converted_md: Path, media_dir: Path, chapters, pages):
    kb = load_json(KB_DIR / "knowledge_base_v1.json")
    source = scan_source_facts()
    controller_inventory = load_text(WORKSPACE / "02_source_analysis" / "code_inventory" / "controller_action_inventory_v1.md")
    database_inventory = load_text(WORKSPACE / "02_source_analysis" / "database" / "database_context_inventory_v1.md")
    workflows = load_text(KB_DIR / "business_workflows_v1.md")
    functional_requirements = load_text(WORKSPACE / "07_tables" / "functional_requirements_v1.md")
    database_tables = load_text(WORKSPACE / "07_tables" / "database_tables_v1.md")

    controller_lines = []
    for item in source["controllers"]:
        actions = ", ".join(item["actions"][:18]) if item["actions"] else "(khong tim thay action public)"
        controller_lines.append(f"- `{item['name']}` (`{item['path']}`): {actions}")

    dbset_lines = [f"- `{x['context']}.{x['dbset']}` -> `{x['model']}`" for x in source["dbsets"]]
    flask_lines = [f"- `{x['route']}` methods={x['methods']}" for x in source["flask_routes"]]

    content = f"""# FULL INPUT v1 - Bao cao QLNhaSach theo source code

Thoi diem tao: {now()} Asia/Bangkok

Nguon template da chuyen Markdown: `{converted_md.relative_to(ROOT).as_posix()}`

Thu muc media template: `{media_dir.relative_to(ROOT).as_posix()}`

So chuong Markdown da tach: {len(chapters)}

So trang template ghi trong DOCX metadata: {pages or "khong doc duoc"}

## 1. Muc tieu bao cao

Viet lai bao cao tot nghiep/thuc tap bang tieng Viet cho de tai:

**Xay dung website quan ly nha sach ket hop nhan dien khuon mat, xac thuc vi tri va quan ly muon tra sach**

Bao cao phai bam sat source code hien co, khong mo ta tinh nang khong co bang chung trong controller, service, Entity Framework model, migration SQL hoac Flask API.

## 2. Pham vi source code bat buoc phan tich

- `BaiTapLon`: ung dung ASP.NET MVC, controller, view, cau hinh, admin area.
- `Mood`: Entity Framework model va cac lop Draw xu ly du lieu.
- `Common`: repository dung chung, dac biet la ghi nhat ky.
- `CommomMail`, `CommomSentMail`: ho tro email.
- `face_auth_api`: Flask API cho nhan dien khuon mat, OCR va API phu tro.
- `sql`, `db.sql`, `sql_15_2.sql`: database schema va migration.
- `Tests`: test cho FaceAuth, Geofence, Rental.

## 3. Thong tin du an tu knowledge base

Ten du an: `{kb.get("project_name", "QLNhaSach")}`

Tieu de bao cao: `{kb.get("report_title", "")}`

Mo ta: {kb.get("project_description", "")}

### Cong nghe

{bullet(kb.get("technologies", []))}

### Module chinh

{bullet(kb.get("modules", []))}

### Tac nhan

{bullet(kb.get("actors", []))}

### Use case cot loi

{bullet(kb.get("core_use_cases", []))}

## 4. Bang chung cu tu source code

### Controller va action quet truc tiep

{chr(10).join(controller_lines)}

### DbSet/Entity Framework quet truc tiep

{chr(10).join(dbset_lines)}

### Service, repository va integration

{bullet(source["services"])}

### Flask Face API routes

{chr(10).join(flask_lines) if flask_lines else "- Chua tim thay route Flask bang regex."}

### Migration SQL

{bullet(source["migrations"])}

### Test hien co

{bullet(source["tests"])}

## 5. Workflow nghiep vu phai viet trong bao cao

{workflows}

## 6. Yeu cau chuc nang da lap bang

{functional_requirements}

## 7. Phan tich database da co

{database_inventory}

## 8. Bang database da lap

{database_tables}

## 9. Controller inventory da co

{controller_inventory}

## 10. Quy tac viet lai bao cao

- Giu cau truc chuong cua template Markdown neu co the.
- Van phong: tieng Viet hoc thuat, ro rang, dung thuat ngu nhat quan.
- Khong dung placeholder hoac noi dung chung chung.
- Chi mo ta tinh nang khi co bang chung trong source code/inventory o tren.
- Uu tien cac luong: dang ky/dang nhap, MFA khuon mat, OCR CMND/CCCD, yeu thich, gio hang, don hang, muon sach, geofence, admin duyet muon/tra, Gmail notification, log va thong ke.
- Giai thich kien truc ASP.NET MVC ket hop Entity Framework, SQL Server LocalDB va Flask Face API.
- Tao bang yeu cau, bang API/controller, bang database, bang test case dua tren thong tin that.
- Tao UML/Draw.io bang nhan tieng Viet, khong tao so do generic.
- Tong do dai ban bao cao cuoi nen kiem soat de khong vuot qua 120 trang khi xuat DOCX/PDF.

## 11. Dau ra mong muon cho buoc tiep theo

- Markdown bao cao moi trong `QLNhaSach_BaoCao/06_report_markdown`.
- Knowledge base cap nhat neu phat hien sai lech.
- UML/Draw.io/images trong `QLNhaSach_BaoCao/05_uml`.
- DOCX/PDF xuat trong `QLNhaSach_BaoCao/09_exports`.
- Log va validation day du trong `QLNhaSach_BaoCao/11_logs` va `QLNhaSach_BaoCao/10_validation`.
"""
    output = next_version(INPUTS / "FULL_INPUT_QLNhaSach_SRC_CODE_v1.md")
    output.write_text(content, encoding="utf-8")
    return output, source


def write_history(converted_md, media_dir, chapters, full_input, source):
    history = next_version(HISTORY_DIR / "006_convert_template_va_dung_full_input_v1.md")
    chapter_list = "\n".join(f"- `{p.relative_to(ROOT).as_posix()}`" for p in chapters)
    content = f"""# 006 - Convert BaoCaoMau va dung full input theo source code

Thoi diem: {now()} Asia/Bangkok

## Da thuc hien

1. Chuyen `QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx` sang Markdown.
2. Trich media cua template sang thu muc rieng.
3. Tach Markdown theo Heading 1 thanh cac chuong rieng.
4. Dung lai full input bao cao dua tren knowledge base, inventory va source code hien tai.
5. Khong ghi de file goc.

## File ket qua

- Markdown template: `{converted_md.relative_to(ROOT).as_posix()}`
- Media: `{media_dir.relative_to(ROOT).as_posix()}`
- Full input moi: `{full_input.relative_to(ROOT).as_posix()}`

## Cac chuong da tach

{chapter_list}

## Thong ke source quet truc tiep

- Controllers: {len(source["controllers"])}
- DbSet: {len(source["dbsets"])}
- Services/repositories: {len(source["services"])}
- Flask routes: {len(source["flask_routes"])}
- SQL migrations: {len(source["migrations"])}
- Tests: {len(source["tests"])}

## Ghi chu

May hien tai khong co `pandoc` va chua co `python-docx`, nen script dung parser DOCX bang thu vien chuan Python. Markdown giu duoc van ban, heading, bang va anh; cac dinh dang Word phuc tap co the can soat lai khi xuat bao cao cuoi.
"""
    history.write_text(content, encoding="utf-8")

    log = LOG_DIR / "execution_log.md"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n## {now()}\n\n")
        f.write("- Convert `00_inputs/BaoCaoMau.docx` sang Markdown bang parser DOCX noi bo.\n")
        f.write(f"- Tao `{converted_md.relative_to(ROOT).as_posix()}`.\n")
        f.write(f"- Tao `{full_input.relative_to(ROOT).as_posix()}`.\n")
        f.write(f"- Ghi history `{history.relative_to(ROOT).as_posix()}`.\n")
    return history


def write_validation(converted_md, media_dir, chapters, full_input, source):
    validation = next_version(VALIDATION_DIR / "convert_template_full_input_validation_v1.md")
    md_text = converted_md.read_text(encoding="utf-8", errors="replace")
    word_count = len(re.findall(r"\w+", md_text, flags=re.UNICODE))
    estimated_pages = max(1, round(word_count / 380))
    checks = [
        ("Template DOCX ton tai", TEMPLATE.exists()),
        ("Markdown template da tao", converted_md.exists() and converted_md.stat().st_size > 0),
        ("Media dir da tao", media_dir.exists()),
        ("Co chapter Markdown", len(chapters) > 0),
        ("Full input da tao", full_input.exists() and full_input.stat().st_size > 0),
        ("Quet duoc controller", len(source["controllers"]) > 0),
        ("Quet duoc DbSet", len(source["dbsets"]) > 0),
        ("Quet duoc Flask route", len(source["flask_routes"]) > 0),
        ("Uoc luong Markdown duoi 120 trang", estimated_pages <= 120),
    ]
    lines = [
        "# Validation - Convert template va full input",
        "",
        f"Thoi diem: {now()} Asia/Bangkok",
        "",
        "| Hang muc | Ket qua |",
        "|---|---|",
    ]
    for name, ok in checks:
        lines.append(f"| {name} | {'OK' if ok else 'CAN KIEM TRA'} |")
    lines.extend(
        [
            "",
            "## File chinh",
            "",
            f"- `{converted_md.relative_to(ROOT).as_posix()}`",
            f"- `{full_input.relative_to(ROOT).as_posix()}`",
            f"- `{media_dir.relative_to(ROOT).as_posix()}`",
            "",
            "## Do dai Markdown",
            "",
            f"- So tu uoc tinh: {word_count}",
            f"- So trang uoc tinh voi 380 tu/trang: {estimated_pages}",
            "- Ghi chu: so trang metadata trong DOCX co the khong chinh xac neu Word chua cap nhat truong thong ke.",
        ]
    )
    validation.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return validation


def main():
    ensure_dirs()
    copy_template_if_needed()
    converted_md, media_dir, chapters, pages = convert_docx_to_markdown()
    full_input, source = build_full_input(converted_md, media_dir, chapters, pages)
    history = write_history(converted_md, media_dir, chapters, full_input, source)
    validation = write_validation(converted_md, media_dir, chapters, full_input, source)
    print(json.dumps({
        "converted_markdown": str(converted_md.relative_to(ROOT)),
        "media_dir": str(media_dir.relative_to(ROOT)),
        "chapters": len(chapters),
        "full_input": str(full_input.relative_to(ROOT)),
        "history": str(history.relative_to(ROOT)),
        "validation": str(validation.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
