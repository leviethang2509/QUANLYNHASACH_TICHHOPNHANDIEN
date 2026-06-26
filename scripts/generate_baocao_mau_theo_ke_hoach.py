# -*- coding: utf-8 -*-
from pathlib import Path
import datetime
import html
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "QLNhaSach_BaoCao"
TEMPLATE = ROOT / "BaoCaoMau.docx"
OUTPUT = WORKSPACE / "09_exports" / "docx" / "BaoCaoMauTheoKeHoach.docx"
ARCHIVE = WORKSPACE / "12_archive" / "BaoCaoMauTheoKeHoach.before_update.docx"
HISTORY = WORKSPACE / "13_history" / "005_tao_baocao_mau_theo_ke_hoach.md"
LOG = WORKSPACE / "11_logs" / "execution_log.md"
KNOWLEDGE = WORKSPACE / "03_knowledge_base" / "knowledge_base_v1.json"

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def now_text():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def escape(value):
    return html.escape(str(value), quote=True)


def text_to_runs(text):
    lines = str(text).splitlines() or [""]
    runs = []
    for index, line in enumerate(lines):
        if index:
            runs.append("<w:br/>")
        runs.append(f'<w:t xml:space="preserve">{escape(line)}</w:t>')
    return "".join(runs)


def paragraph(text="", style=None, bold=False, italic=False, align=None):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')

    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")

    return (
        "<w:p>"
        f"<w:pPr>{''.join(ppr)}</w:pPr>"
        f"<w:r><w:rPr>{''.join(rpr)}</w:rPr>{text_to_runs(text)}</w:r>"
        "</w:p>"
    )


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def table(rows):
    xml = [
        "<w:tbl>",
        "<w:tblPr>",
        '<w:tblStyle w:val="TableGrid"/>',
        "<w:tblBorders>",
        '<w:top w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        '<w:left w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        '<w:right w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="auto"/>',
        "</w:tblBorders>",
        "</w:tblPr>",
    ]
    for row_index, row in enumerate(rows):
        xml.append("<w:tr>")
        for cell in row:
            shade = '<w:shd w:fill="D9EAF7"/>' if row_index == 0 else ""
            bold = "<w:b/>" if row_index == 0 else ""
            xml.append(
                "<w:tc>"
                f"<w:tcPr>{shade}<w:tcW w:w=\"2600\" w:type=\"dxa\"/></w:tcPr>"
                f"<w:p><w:r><w:rPr>{bold}</w:rPr><w:t xml:space=\"preserve\">{escape(cell)}</w:t></w:r></w:p>"
                "</w:tc>"
            )
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


def load_knowledge():
    if not KNOWLEDGE.exists():
        return {}
    return json.loads(KNOWLEDGE.read_text(encoding="utf-8"))


def replace_text_fragments(xml):
    replacements = {
        "XÂY DỰNG WEBSITE BÁN SÁCH BẰNG ASP.NET CORE": "XÂY DỰNG WEBSITE QUẢN LÝ NHÀ SÁCH KẾT HỢP NHẬN DIỆN KHUÔN MẶT, XÁC THỰC VỊ TRÍ VÀ QUẢN LÝ MƯỢN TRẢ SÁCH",
        "XÂY DỰNG WEBSITE BÁN SÁCH": "XÂY DỰNG WEBSITE QUẢN LÝ NHÀ SÁCH",
        "ASP.NET Core": "ASP.NET MVC 5",
        "Asp.Net Core": "ASP.NET MVC 5",
        "website bán sách": "website quản lý nhà sách",
        "Website bán sách": "Website quản lý nhà sách",
        "bán sách": "quản lý nhà sách",
        "mua hàng": "đặt hàng và mượn sách",
        "khách hàng": "người dùng",
        "nhân viên": "quản trị viên",
        "Nguyễn Thanh Lâm": "Lê Việt Thắng",
        "1234": "2224802010263",
        "Năm 2024": "Năm 2026",
    }
    for old, new in replacements.items():
        xml = xml.replace(escape(old), escape(new))
        xml = xml.replace(old, new)
    return xml


def build_plan_appendix(knowledge):
    modules = knowledge.get("modules", [])
    use_cases = knowledge.get("core_use_cases", [])
    entities = knowledge.get("database_entities", [])
    services = knowledge.get("important_services", [])

    parts = [
        page_break(),
        paragraph("PHẦN CẬP NHẬT THEO KẾ HOẠCH BÁO CÁO", style="Heading1", bold=True),
        paragraph(
            "Nội dung dưới đây được bổ sung từ kế hoạch trong thư mục QLNhaSach_BaoCao. "
            "Mục tiêu là điều chỉnh báo cáo mẫu theo đúng cấu trúc và nghiệp vụ thực tế của dự án QLNhaSach.",
            italic=True,
        ),
        paragraph("1. Thông tin đề tài", style="Heading2", bold=True),
        table(
            [
                ["Mục", "Nội dung"],
                ["Tên dự án", knowledge.get("project_name", "QLNhaSach")],
                ["Tên báo cáo", knowledge.get("report_title", "Xây dựng website quản lý nhà sách")],
                ["Mô tả", knowledge.get("project_description", "")],
                ["Thư mục quản lý", "QLNhaSach_BaoCao"],
            ]
        ),
        paragraph("2. Cấu trúc hệ thống được dùng để viết báo cáo", style="Heading2", bold=True),
        table(
            [
                ["Thành phần", "Vai trò"],
                ["BaiTapLon", "Ứng dụng ASP.NET MVC, controller, view, cấu hình Web.config và khu vực quản trị."],
                ["Mood", "Entity Framework models và các lớp Draw xử lý truy vấn/nghiệp vụ dữ liệu."],
                ["Common", "Repository dùng chung, đặc biệt là ghi và truy vấn log."],
                ["face_auth_api", "Flask API hỗ trợ nhận diện khuôn mặt, OCR CMND/CCCD và chatbox."],
                ["sql", "Script tạo database và migration bổ sung bảng nghiệp vụ mới."],
            ]
        ),
        paragraph("3. Các module chính", style="Heading2", bold=True),
        table([["STT", "Module"]] + [[str(i + 1), item] for i, item in enumerate(modules)]),
        paragraph("4. Các use case cốt lõi", style="Heading2", bold=True),
        table([["STT", "Use case"]] + [[str(i + 1), item] for i, item in enumerate(use_cases)]),
        paragraph("5. Các bảng dữ liệu cần mô tả trong báo cáo", style="Heading2", bold=True),
        table([["STT", "Bảng/Entity"]] + [[str(i + 1), item] for i, item in enumerate(entities)]),
        paragraph("6. Service và lớp nghiệp vụ quan trọng", style="Heading2", bold=True),
        table([["STT", "Service/Repository"]] + [[str(i + 1), item] for i, item in enumerate(services)]),
        paragraph("7. Nội dung cần ưu tiên khi chỉnh báo cáo", style="Heading2", bold=True),
        table(
            [
                ["Nhóm nội dung", "Yêu cầu chỉnh sửa"],
                ["Chương yêu cầu", "Mô tả đúng bài toán quản lý nhà sách, người dùng, quản trị viên, mượn/trả sách, OCR và nhận diện khuôn mặt."],
                ["Chương phân tích", "Dùng các actor và use case thực tế: khách vãng lai, người dùng, quản trị viên, Face API, Gmail service."],
                ["Chương database", "Tập trung Users, Sanphams, Orders, RentalRequests, StoreLocations, ProductFavorites, ProductReviews và các bảng log."],
                ["Chương thiết kế", "Giải thích kiến trúc ASP.NET MVC kết hợp Entity Framework, Flask Face API, Gmail notification và geofence."],
                ["Chương kiểm thử", "Bổ sung test case cho đăng nhập, MFA khuôn mặt, OCR CMND/CCCD, kiểm tra vị trí, mượn/trả sách và yêu thích."],
            ]
        ),
        paragraph("8. Nhật ký và thư mục đầu ra", style="Heading2", bold=True),
        paragraph(
            "Mọi file sinh ra trong quá trình viết báo cáo được lưu trong QLNhaSach_BaoCao. "
            "Mỗi quy trình có lịch sử riêng tại QLNhaSach_BaoCao/13_history và log tổng tại QLNhaSach_BaoCao/11_logs/execution_log.md."
        ),
    ]
    return "".join(parts)


def write_history():
    content = f"""# 005 - Tao BaoCaoMauTheoKeHoach

Thoi diem: {now_text()} Asia/Bangkok

## Muc tieu

Copy bao cao mau `BaoCaoMau.docx`, sau do sua lai noi dung theo ke hoach da luu trong `QLNhaSach_BaoCao`.

## Da thuc hien

1. Tao file ket qua:
   - `09_exports/docx/BaoCaoMauTheoKeHoach.docx`
2. Cap nhat mot so cum noi dung/tua de chinh trong XML cua DOCX neu tim thay.
3. Chen phan `PHAN CAP NHAT THEO KE HOACH BAO CAO` vao cuoi tai lieu.
4. Noi dung chen them duoc lay tu:
   - `03_knowledge_base/knowledge_base_v1.json`
   - cac inventory va workflow da tao trong workspace.

## Ghi chu

File mau goc `BaoCaoMau.docx` khong bi thay doi.
"""
    HISTORY.write_text(content, encoding="utf-8")

    with LOG.open("a", encoding="utf-8") as file:
        file.write(f"\n## {now_text()}\n\n")
        file.write("- Tao `09_exports/docx/BaoCaoMauTheoKeHoach.docx` tu `BaoCaoMau.docx`.\n")
        file.write("- Chen phan cap nhat noi dung theo ke hoach vao cuoi bao cao.\n")
        file.write("- Ghi lich su tai `13_history/005_tao_baocao_mau_theo_ke_hoach.md`.\n")


def update_docx():
    if not TEMPLATE.exists():
        raise FileNotFoundError(TEMPLATE)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        shutil.copy2(OUTPUT, ARCHIVE)

    knowledge = load_knowledge()
    appendix = build_plan_appendix(knowledge)

    temp_output = OUTPUT.with_suffix(".tmp.docx")
    with zipfile.ZipFile(TEMPLATE, "r") as zin, zipfile.ZipFile(temp_output, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                xml = replace_text_fragments(xml)
                sect_match = re.search(r"<w:sectPr[\s\S]*?</w:sectPr>", xml)
                if sect_match:
                    xml = xml[: sect_match.start()] + appendix + xml[sect_match.start() :]
                else:
                    xml = xml.replace("</w:body>", appendix + "</w:body>")
                data = xml.encode("utf-8")
            elif item.filename == "docProps/core.xml":
                xml = data.decode("utf-8")
                xml = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>BaoCaoMauTheoKeHoach - QLNhaSach</dc:title>", xml)
                xml = re.sub(r"<dc:subject>.*?</dc:subject>", "<dc:subject>Bao cao quan ly nha sach theo ke hoach</dc:subject>", xml)
                data = xml.encode("utf-8")
            zout.writestr(item, data)

    temp_output.replace(OUTPUT)
    write_history()


if __name__ == "__main__":
    update_docx()
    print(str(OUTPUT))
