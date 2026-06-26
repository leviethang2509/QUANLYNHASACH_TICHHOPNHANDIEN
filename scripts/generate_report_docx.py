# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import datetime
import html
import os
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "report_assets"
ASSETS.mkdir(exist_ok=True)
HISTORY = ROOT / "LichSuQuaTrinhVietBaoCao.md"
DOCX = ROOT / "BaoCao_QuanLyNhaSach_NhanDienKhuonMat_LeVietThang_2224802010263.docx"
DRAWIO = ASSETS / "usecase_quan_ly_nha_sach.drawio"


def log(message):
    with HISTORY.open("a", encoding="utf-8") as file:
        file.write("\n## " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        file.write(message.rstrip() + "\n")


def font(size=28, bold=False):
    paths = [
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_center(draw, box, text, fnt, fill=(25, 25, 25)):
    x1, y1, x2, y2 = box
    lines = wrap(draw, text, fnt, x2 - x1 - 24)
    line_h = fnt.size + 6
    y = y1 + (y2 - y1 - len(lines) * line_h) / 2
    for line in lines:
        w = draw.textbbox((0, 0), line, font=fnt)[2]
        draw.text((x1 + (x2 - x1 - w) / 2, y), line, font=fnt, fill=fill)
        y += line_h


def arrow(draw, start, end, fill=(55, 90, 120), width=3):
    import math
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 12
    p1 = (end[0] - size * math.cos(angle - 0.45), end[1] - size * math.sin(angle - 0.45))
    p2 = (end[0] - size * math.cos(angle + 0.45), end[1] - size * math.sin(angle + 0.45))
    draw.polygon([end, p1, p2], fill=fill)


def make_usecase(path):
    width, height = 1800, 1120
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((width / 2, 50), "Sơ đồ Use Case tổng quát", font=font(46, True), fill=(30, 30, 30), anchor="mm")
    draw.rounded_rectangle((360, 120, 1440, 1020), radius=22, outline=(35, 80, 140), width=4, fill=(248, 251, 255))
    draw.text((900, 150), "Hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt", font=font(28, True), fill=(35, 80, 140), anchor="mm")

    actors = {
        "Khách vãng lai": (120, 260),
        "Người dùng": (120, 560),
        "Quản trị viên": (120, 860),
        "Face API/OCR": (1640, 400),
        "Gmail/Chatbox": (1640, 740),
    }
    for name, (x, y) in actors.items():
        draw.ellipse((x - 28, y - 70, x + 28, y - 14), outline=(25, 25, 25), width=3)
        draw.line((x, y - 14, x, y + 70), fill=(25, 25, 25), width=3)
        draw.line((x - 45, y + 20, x + 45, y + 20), fill=(25, 25, 25), width=3)
        draw.line((x, y + 70, x - 40, y + 130), fill=(25, 25, 25), width=3)
        draw.line((x, y + 70, x + 40, y + 130), fill=(25, 25, 25), width=3)
        draw.text((x, y + 160), name, font=font(28, True), fill=(25, 25, 25), anchor="mm")

    cases = [
        ("Xem/tìm kiếm sách", 560, 260),
        ("Đăng ký/đăng nhập", 860, 260),
        ("Cập nhật CMND/CCCD", 1160, 260),
        ("Xác thực khuôn mặt", 560, 480),
        ("Gửi yêu cầu mượn sách", 860, 480),
        ("Theo dõi lịch sử mượn", 1160, 480),
        ("Quản lý sách, danh mục, kho", 560, 700),
        ("Duyệt/từ chối/trả sách", 860, 700),
        ("Xem nhật ký hệ thống", 1160, 700),
        ("Gửi Gmail thông báo", 710, 900),
        ("Chatbox tư vấn sách", 1010, 900),
    ]
    centers = {}
    for text, x, y in cases:
        box = (x - 135, y - 55, x + 135, y + 55)
        draw.ellipse(box, fill="white", outline=(42, 111, 151), width=3)
        draw_center(draw, box, text, font(24))
        centers[text] = (x, y)

    for target in ["Xem/tìm kiếm sách"]:
        arrow(draw, (190, 330), (425, centers[target][1]), width=2)
    for target in ["Đăng ký/đăng nhập", "Cập nhật CMND/CCCD", "Xác thực khuôn mặt", "Gửi yêu cầu mượn sách", "Theo dõi lịch sử mượn"]:
        arrow(draw, (190, 630), (centers[target][0] - 135, centers[target][1]), width=2)
    for target in ["Quản lý sách, danh mục, kho", "Duyệt/từ chối/trả sách", "Xem nhật ký hệ thống"]:
        arrow(draw, (190, 930), (centers[target][0] - 135, centers[target][1]), width=2)
    for target in ["Cập nhật CMND/CCCD", "Xác thực khuôn mặt"]:
        arrow(draw, (1580, 470), (centers[target][0] + 135, centers[target][1]), width=2)
    for target in ["Gửi Gmail thông báo", "Chatbox tư vấn sách"]:
        arrow(draw, (1580, 810), (centers[target][0] + 135, centers[target][1]), width=2)
    image.save(path)


def make_flow(path, title, steps):
    width, height = 1800, 760
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    color = (36, 99, 140)
    draw.text((width / 2, 50), title, font=font(42, True), fill=(30, 30, 30), anchor="mm")
    columns = min(5, len(steps))
    box_w, box_h = 270, 110
    left = 120
    gap = (width - 2 * left - columns * box_w) / max(columns - 1, 1)
    boxes = []
    for index, step in enumerate(steps):
        row = index // columns
        col = index % columns
        if row % 2 == 1:
            col = columns - 1 - col
        x = left + col * (box_w + gap)
        y = 170 + row * 230
        box = (x, y, x + box_w, y + box_h)
        boxes.append(box)
        draw.rounded_rectangle(box, radius=18, fill=(246, 250, 252), outline=color, width=3)
        draw.ellipse((x - 22, y - 22, x + 28, y + 28), fill=color)
        draw.text((x + 3, y + 3), str(index + 1), font=font(24, True), fill="white", anchor="mm")
        draw_center(draw, box, step, font(23))
    for a, b in zip(boxes, boxes[1:]):
        start = (a[2], (a[1] + a[3]) / 2)
        end = (b[0], (b[1] + b[3]) / 2)
        if abs(start[1] - end[1]) > 20:
            start = ((a[0] + a[2]) / 2, a[3])
            end = ((b[0] + b[2]) / 2, b[1])
        arrow(draw, start, end, fill=color, width=3)
    image.save(path)


def make_drawio(path):
    path.write_text(
        """<mxfile host="app.diagrams.net"><diagram name="UseCase"><mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="sys" value="Hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fbff;strokeColor=#2a6f97;" vertex="1" parent="1"><mxGeometry x="210" y="80" width="720" height="560" as="geometry"/></mxCell><mxCell id="actor1" value="Người dùng" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;" vertex="1" parent="1"><mxGeometry x="60" y="240" width="40" height="80" as="geometry"/></mxCell><mxCell id="actor2" value="Quản trị viên" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;" vertex="1" parent="1"><mxGeometry x="60" y="470" width="40" height="80" as="geometry"/></mxCell><mxCell id="actor3" value="Face API/OCR" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;" vertex="1" parent="1"><mxGeometry x="1010" y="220" width="40" height="80" as="geometry"/></mxCell><mxCell id="actor4" value="Gmail/Chatbox" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;" vertex="1" parent="1"><mxGeometry x="1010" y="470" width="40" height="80" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>""",
        encoding="utf-8",
    )


def esc(value):
    return html.escape(str(value), quote=True)


def emu(px):
    return int(px * 9525)


class Docx:
    def __init__(self):
        self.body = []
        self.rels = []
        self.media = []
        self.next_rid = 1

    def p(self, text="", style=None, align=None, bold=False, italic=False, size=24):
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
        rpr.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
        self.body.append(f'<w:p><w:pPr>{"".join(ppr)}</w:pPr><w:r><w:rPr>{"".join(rpr)}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

    def heading(self, text, level=1):
        self.p(text, style=f"Heading{level}")

    def bullet(self, text):
        self.body.append(f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t>{esc(text)}</w:t></w:r></w:p>')

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def table(self, rows):
        parts = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblBorders><w:top w:val="single" w:sz="6"/><w:left w:val="single" w:sz="6"/><w:bottom w:val="single" w:sz="6"/><w:right w:val="single" w:sz="6"/><w:insideH w:val="single" w:sz="6"/><w:insideV w:val="single" w:sz="6"/></w:tblBorders></w:tblPr>']
        for row_index, row in enumerate(rows):
            parts.append("<w:tr>")
            for cell in row:
                shade = '<w:shd w:fill="D9EAF7"/>' if row_index == 0 else ""
                bold = "<w:b/>" if row_index == 0 else ""
                parts.append(f'<w:tc><w:tcPr>{shade}<w:tcW w:w="2400" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr>{bold}</w:rPr><w:t>{esc(cell)}</w:t></w:r></w:p></w:tc>')
            parts.append("</w:tr>")
        parts.append("</w:tbl>")
        self.body.append("".join(parts))
        self.p("")

    def image(self, path, caption, width_px=620):
        path = Path(path)
        if not path.exists():
            return
        image = Image.open(path)
        ratio = width_px / image.size[0]
        height_px = int(image.size[1] * ratio)
        rid = f"rId{self.next_rid}"
        self.next_rid += 1
        target = "media/" + path.name
        self.rels.append((rid, target))
        self.media.append((path, target))
        self.body.append(f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="{emu(width_px)}" cy="{emu(height_px)}"/><wp:docPr id="{self.next_rid}" name="{esc(path.name)}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="{esc(path.name)}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{emu(width_px)}" cy="{emu(height_px)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>''')
        self.p(caption, align="center", italic=True, size=22)

    def save(self, path):
        document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>{"".join(self.body)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1134" w:bottom="1440" w:left="1418" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>'''
        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:i/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr></w:style></w:styles>'''
        numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="-"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
        package_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
        doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rStyle" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
        for rid, target in self.rels:
            doc_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>')
        doc_rels.append("</Relationships>")
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>'''
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("[Content_Types].xml", content_types)
            zip_file.writestr("_rels/.rels", package_rels)
            zip_file.writestr("word/document.xml", document)
            zip_file.writestr("word/styles.xml", styles)
            zip_file.writestr("word/numbering.xml", numbering)
            zip_file.writestr("word/_rels/document.xml.rels", "".join(doc_rels))
            for source, target in self.media:
                zip_file.write(source, "word/" + target)


def build_report():
    make_drawio(DRAWIO)
    make_usecase(ASSETS / "usecase_quan_ly_nha_sach.png")
    make_flow(ASSETS / "workflow_muon_sach.png", "Quy trình người dùng mượn sách", ["Đăng nhập", "Cập nhật Gmail và CMND/CCCD", "Chọn sách cần mượn", "Xác thực khuôn mặt", "Gửi yêu cầu mượn", "Admin duyệt", "Gửi Gmail thông báo"])
    make_flow(ASSETS / "workflow_ocr_face.png", "Quy trình OCR CMND/CCCD và xác thực khuôn mặt", ["Tải ảnh mặt trước/sau", "Lưu ảnh giấy tờ", "Gọi Flask Face API", "OCR bằng PaddleOCR/Tesseract", "So khớp khuôn mặt", "Cập nhật hồ sơ định danh"])
    make_flow(ASSETS / "workflow_admin.png", "Quy trình admin xử lý mượn trả", ["Xem yêu cầu Pending", "Kiểm tra hồ sơ và tồn kho", "Duyệt hoặc từ chối", "Giảm tồn kho khi duyệt", "Xác nhận trả sách", "Tăng tồn kho và ghi log"])
    log("- Đã tạo lại sơ đồ use case, file draw.io và các ảnh quy trình bằng script UTF-8.")

    doc = Docx()
    doc.p("TRƯỜNG ĐẠI HỌC THỦ DẦU MỘT", align="center", bold=True, size=28)
    doc.p("KHOA CÔNG NGHỆ THÔNG TIN", align="center", bold=True, size=26)
    doc.p("")
    doc.p("BÁO CÁO ĐỒ ÁN", align="center", bold=True, size=34)
    doc.p("QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH", align="center", bold=True, size=32)
    doc.p("")
    doc.p("Sinh viên thực hiện: Lê Việt Thắng", align="center", bold=True)
    doc.p("MSSV: 2224802010263", align="center", bold=True)
    doc.p("Lớp: ........................................", align="center")
    doc.p("Giảng viên hướng dẫn: ........................................", align="center")
    doc.p("Bình Dương, tháng 05 năm 2026", align="center", bold=True)
    doc.page_break()

    doc.heading("LỜI CẢM ƠN", 1)
    doc.p("Em xin chân thành cảm ơn quý thầy cô đã hướng dẫn và tạo điều kiện trong quá trình thực hiện đề tài. Báo cáo này được xây dựng dựa trên source hệ thống quản lý nhà sách, kết hợp server nhận diện khuôn mặt, OCR CMND/CCCD và chatbox tư vấn sách nhằm hoàn thiện quy trình mượn trả sách an toàn hơn.")
    doc.page_break()

    doc.heading("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", 1)
    for _ in range(12):
        doc.p("........................................................................................................................")
    doc.page_break()

    doc.heading("MỤC LỤC", 1)
    for item in ["CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI", "CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ", "CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", "CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG", "CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ", "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "TÀI LIỆU THAM KHẢO", "PHỤ LỤC"]:
        doc.p(item)
    doc.page_break()

    doc.heading("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI", 1)
    doc.heading("1.1. Lý do chọn đề tài", 2)
    doc.p("Nhà sách không chỉ quản lý việc bán sách mà còn cần quản lý tồn kho, hồ sơ khách hàng, đơn hàng, đánh giá sản phẩm và nhu cầu mượn trả sách. Khi triển khai chức năng mượn sách, hệ thống cần xác định đúng người mượn, lưu hồ sơ định danh và theo dõi quá trình trả sách. Vì vậy, đề tài lựa chọn tích hợp nhận diện khuôn mặt và OCR CMND/CCCD vào hệ thống quản lý nhà sách nhằm nâng cao mức độ xác thực, giảm thao tác nhập liệu và hỗ trợ quản trị viên xử lý yêu cầu nhanh hơn.")
    doc.heading("1.2. Mục tiêu đề tài", 2)
    for item in ["Xây dựng website quản lý nhà sách có đầy đủ các chức năng cơ bản như quản lý sách, danh mục, đơn hàng, tài khoản và tồn kho.", "Tích hợp quy trình mượn trả sách có kiểm tra hồ sơ, tồn kho, xác thực khuôn mặt và gửi Gmail thông báo.", "Tích hợp OCR CMND/CCCD để hỗ trợ cập nhật thông tin định danh của người dùng.", "Xây dựng báo cáo kỹ thuật, sơ đồ use case, sơ đồ quy trình và ảnh minh họa theo đúng bố cục báo cáo."]:
        doc.bullet(item)
    doc.heading("1.3. Phạm vi thực hiện", 2)
    doc.p("Phạm vi đề tài tập trung vào hệ thống web ASP.NET MVC trong thư mục QLNhaSach và server Flask nhận diện/OCR/chatbox trong thư mục NHANDIENKHUONMAT-new07040226. Báo cáo không đi sâu huấn luyện lại mô hình AI mà mô tả cách tích hợp mô hình có sẵn vào nghiệp vụ mượn trả sách.")

    doc.heading("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ", 1)
    doc.heading("2.1. Công nghệ website", 2)
    doc.table([["Thành phần", "Công nghệ", "Vai trò"], ["Backend", "ASP.NET MVC 5, C#", "Xử lý nghiệp vụ, controller, view"], ["Runtime", ".NET Framework 4.8", "Nền tảng chạy ứng dụng"], ["ORM", "Entity Framework 6", "Ánh xạ dữ liệu"], ["CSDL", "SQL Server LocalDB - QLNhaSach", "Lưu dữ liệu sách, người dùng, đơn hàng, mượn trả"], ["Frontend", "Razor, HTML, CSS, JavaScript, jQuery, Bootstrap", "Xây dựng giao diện người dùng"], ["Mail", "Gmail SMTP/API", "Gửi thông báo trạng thái mượn trả"]])
    doc.heading("2.2. Công nghệ nhận diện khuôn mặt, OCR và chatbox", 2)
    doc.table([["Thành phần", "Công nghệ", "Vai trò"], ["Face API", "Flask", "Cung cấp API nhận diện, OCR, chatbox"], ["Nhận diện khuôn mặt", "InsightFace, ONNXRuntime", "Trích xuất embedding và so khớp khuôn mặt"], ["Liveness/action", "MediaPipe Face Landmarker", "Kiểm tra hành động khuôn mặt"], ["OCR", "PaddleOCR, pytesseract/Tesseract", "Đọc CMND/CCCD"], ["Xử lý ảnh", "OpenCV, NumPy, scikit-image", "Tiền xử lý ảnh và kiểm tra chất lượng"], ["Chatbox", "Flask blueprint, JSON knowledge base", "Tư vấn sách và hướng dẫn mượn"]])
    doc.heading("2.3. Cấu hình tích hợp", 2)
    for item in ["FaceAuthAPI: http://localhost:8000/api/face", "ChatboxWidgetUrl: http://localhost:8000/api/chatbox/widget.js", "FaceAuthMinConfidence: 0.75", "RentalMaxBorrowDays: 30", "SMTP Gmail: smtp.gmail.com, port 587, SSL."]:
        doc.bullet(item)

    doc.heading("CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 1)
    doc.heading("3.1. Tác nhân hệ thống", 2)
    doc.table([["Tác nhân", "Vai trò"], ["Khách vãng lai", "Xem trang chủ, danh mục, tìm kiếm và xem chi tiết sách"], ["Người dùng", "Đăng ký, đăng nhập, cập nhật hồ sơ, xác thực khuôn mặt, mượn sách"], ["Quản trị viên", "Quản lý sách, đơn hàng, người dùng, duyệt mượn/trả sách"], ["Face API/OCR", "Xác thực khuôn mặt và đọc giấy tờ định danh"], ["Gmail/Chatbox", "Gửi thông báo và tư vấn sách"]])
    doc.heading("3.2. Sơ đồ use case", 2)
    doc.image(ASSETS / "usecase_quan_ly_nha_sach.png", "Hình 3.1. Sơ đồ use case tổng quát của hệ thống")
    doc.heading("3.3. Quy trình mượn sách", 2)
    doc.image(ASSETS / "workflow_muon_sach.png", "Hình 3.2. Quy trình người dùng gửi yêu cầu mượn sách")
    doc.heading("3.4. Quy trình OCR và xác thực khuôn mặt", 2)
    doc.image(ASSETS / "workflow_ocr_face.png", "Hình 3.3. Quy trình OCR CMND/CCCD và xác thực khuôn mặt")
    doc.heading("3.5. Quy trình admin xử lý mượn trả", 2)
    doc.image(ASSETS / "workflow_admin.png", "Hình 3.4. Quy trình admin duyệt, trả sách và ghi log")

    doc.heading("CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG", 1)
    doc.heading("4.1. Cấu trúc source", 2)
    doc.table([["Thư mục", "Nội dung"], ["BaiTapLon", "Ứng dụng ASP.NET MVC, controller, view, cấu hình Web.config"], ["Mood", "Entity Framework model và lớp Draw xử lý dữ liệu"], ["Common", "Repository ghi log xác thực, geofence, mượn trả"], ["CommomSentMail", "Helper gửi Gmail SMTP"], ["Server Flask", "API nhận diện khuôn mặt, OCR CMND/CCCD và chatbox"]])
    doc.heading("4.2. Các controller/API chính", 2)
    doc.table([["Controller/API", "Chức năng"], ["UsersController", "Đăng ký, đăng nhập, hồ sơ người dùng, Facebook login"], ["ProductController", "Danh sách, tìm kiếm, chi tiết sách, đánh giá và file review"], ["RentalController", "Hồ sơ mượn, tạo yêu cầu mượn, duyệt/trả/hủy/quá hạn"], ["FaceAuthController", "OCR CMND/CCCD, đăng ký/xác thực khuôn mặt, challenge action"], ["LogsController", "Truy vấn log khuôn mặt, geofence, mượn trả"], ["Flask /api/face/*", "register, verify, authenticate, action-check, ocr-cmnd, health"], ["Flask /api/chatbox/*", "train, ask, widget.js"]])
    doc.heading("4.3. Ảnh giao diện ứng dụng", 2)
    doc.image(ASSETS / "screenshot_home.png", "Hình 4.1. Trang chủ hệ thống quản lý nhà sách")
    doc.image(ASSETS / "screenshot_product_list.png", "Hình 4.2. Màn hình danh sách sản phẩm sách")
    doc.p("Các màn hình yêu cầu phiên đăng nhập như hồ sơ người dùng, xác thực khuôn mặt, lịch sử mượn và quản trị mượn/trả cần được chụp bổ sung sau khi đăng nhập bằng tài khoản phù hợp. Trong lần tạo báo cáo này, hệ thống local truy cập được trang công khai và đã chụp các màn hình không yêu cầu session.")
    doc.heading("4.4. Gửi thông báo Gmail", 2)
    doc.p("Module gửi Gmail sử dụng SmtpClient với host smtp.gmail.com, port 587 và SSL. Hệ thống gửi thông báo khi người dùng tạo yêu cầu mượn, admin duyệt, từ chối, hủy, trả sách hoặc đánh dấu quá hạn. Lỗi SMTP được ghi chi tiết để hỗ trợ kiểm tra app password và email gửi.")

    doc.heading("CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ", 1)
    doc.heading("5.1. Kế hoạch kiểm thử", 2)
    doc.table([["Nhóm kiểm thử", "Trường hợp kiểm thử"], ["Tài khoản", "Đăng ký, đăng nhập, cập nhật hồ sơ"], ["OCR", "Ảnh rõ, ảnh mờ, thiếu mặt trước/mặt sau, ảnh không hợp lệ"], ["Khuôn mặt", "Đúng người, sai người, nhiều khuôn mặt, ảnh chất lượng thấp"], ["Mượn sách", "Còn tồn, hết tồn, thiếu hồ sơ, chưa xác thực"], ["Admin", "Duyệt, từ chối, trả sách, quá hạn"], ["Gmail", "Gửi thành công, sai app password, sai email gửi"], ["Chatbox", "Hỏi sách, giá, tồn kho, hướng dẫn mượn"]])
    doc.heading("5.2. Đánh giá kết quả", 2)
    doc.p("Hệ thống đáp ứng được định hướng đề tài: quản lý nhà sách kết hợp xác thực khuôn mặt và hồ sơ định danh cho quy trình mượn trả. Việc tách Face API thành server Flask giúp dễ nâng cấp mô hình nhận diện/OCR mà không ảnh hưởng trực tiếp đến ứng dụng ASP.NET MVC. Các log nghiệp vụ giúp quản trị viên theo dõi quá trình xác thực, mượn trả và gửi thông báo.")

    doc.heading("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 1)
    doc.p("Đề tài đã xây dựng được báo cáo và mô hình triển khai hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn trả sách. Hướng phát triển tiếp theo là hoàn thiện chụp ảnh toàn bộ quy trình sau khi đăng nhập, tối ưu OCR CMND/CCCD trong nhiều điều kiện ánh sáng, bổ sung dashboard thống kê mượn trả và chuẩn hóa tài liệu triển khai production.")
    doc.heading("TÀI LIỆU THAM KHẢO", 1)
    for item in ["Tài liệu ASP.NET MVC 5 và Entity Framework 6.", "Tài liệu Flask framework.", "Tài liệu InsightFace, MediaPipe, PaddleOCR và Tesseract OCR.", "Source code dự án QLNhaSach và server NHANDIENKHUONMAT-new07040226.", "Template.pdf và QuyTrinhVietBaoCao.md trong workspace."]:
        doc.bullet(item)
    doc.heading("PHỤ LỤC", 1)
    doc.heading("Phụ lục A. Kế hoạch thực hiện tháng 01 - 05/2026", 2)
    doc.table([["Tháng", "Nội dung chính", "Kết quả"], ["01/2026", "Khảo sát yêu cầu, phân tích source ASP.NET MVC và Flask API", "Tài liệu yêu cầu và kế hoạch"], ["02/2026", "Thiết kế use case, CSDL, luồng mượn trả, OCR và xác thực", "Bản thiết kế hệ thống"], ["03/2026", "Tích hợp hồ sơ định danh, OCR, xác thực khuôn mặt và tạo yêu cầu mượn", "Module mượn sách"], ["04/2026", "Hoàn thiện admin duyệt/trả, Gmail và chatbox", "Module quản trị và thông báo"], ["05/2026", "Kiểm thử, hoàn thiện báo cáo, chèn sơ đồ và ảnh quy trình", "Báo cáo hoàn chỉnh"]])
    doc.heading("Phụ lục B. File sinh kèm", 2)
    for item in ["report_assets/usecase_quan_ly_nha_sach.drawio", "report_assets/usecase_quan_ly_nha_sach.png", "report_assets/workflow_muon_sach.png", "report_assets/workflow_ocr_face.png", "report_assets/workflow_admin.png", "LichSuQuaTrinhVietBaoCao.md"]:
        doc.bullet(item)
    doc.save(DOCX)
    log("- Đã tạo lại file báo cáo DOCX bằng script UTF-8: `BaoCao_QuanLyNhaSach_NhanDienKhuonMat_LeVietThang_2224802010263.docx`.\n- Định dạng mặc định: Times New Roman, cỡ chữ 12, khổ A4, có phân trang theo chương, bảng biểu, sơ đồ use case, sơ đồ quy trình và ảnh chụp màn hình ứng dụng.\n- Ghi chú: chưa trích xuất trực tiếp được `Template.pdf` do thiếu công cụ đọc PDF local, nên bố cục được dựng theo mẫu báo cáo đồ án phổ biến và nội dung trong `QuyTrinhVietBaoCao.md`/source.")
    print(DOCX)


if __name__ == "__main__":
    build_report()
