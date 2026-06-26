# -*- coding: utf-8 -*-
from pathlib import Path
import copy
import datetime as dt
import html
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
WS = ROOT / "QLNhaSach_BaoCao"
TEMPLATE = WS / "00_inputs" / "BaoCaoMau.docx"
INPUT = WS / "00_inputs" / "FULL_INPUT_QLNhaSach_SRC_CODE_v6.md"
OUT_DIR = WS / "09_exports" / "docx"
HISTORY = WS / "13_history"
LOGS = WS / "11_logs"
VALIDATION = WS / "10_validation"

OUTPUT = OUT_DIR / "BaoCao_QLNhaSach_LeVietThang_2224802010263_Synced_v1.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"

ET.register_namespace("w", W)
ET.register_namespace("r", R)
ET.register_namespace("a", A)
ET.register_namespace("wp", WP)
ET.register_namespace("pic", PIC)


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def q(ns, tag):
    return f"{{{ns}}}{tag}"


def ensure_dirs():
    for path in [OUT_DIR, HISTORY, LOGS, VALIDATION]:
        path.mkdir(parents=True, exist_ok=True)


def repair_text(value):
    if not value:
        return value
    if any(marker in value for marker in ("Ã", "á»", "áº", "Ä", "Æ", "â€", "â€“")):
        try:
            return value.encode("cp1252").decode("utf-8")
        except UnicodeError:
            return value
    return value


def replace_report_text(value):
    replacements = {
        "NGUYỄN THANH LÂM": "LÊ VIỆT THẮNG",
        "Nguyễn Thanh Lâm": "Lê Việt Thắng",
        "Nguyễn Thanh Lâm": "Lê Việt Thắng",
        "1234": "2224802010263",
        "XÂY DỰNG WEBSITE BÁN SÁCH BẰNG ASP.NET CORE": "XÂY DỰNG WEBSITE QUẢN LÝ NHÀ SÁCH KẾT HỢP NHẬN DIỆN KHUÔN MẶT, XÁC THỰC VỊ TRÍ VÀ QUẢN LÝ MƯỢN TRẢ SÁCH",
        "XÂY DỰNG WEBSITE BÁN SÁCH": "XÂY DỰNG WEBSITE QUẢN LÝ NHÀ SÁCH",
        "ASP.NET Core": "ASP.NET MVC 5",
        "Asp.Net Core": "ASP.NET MVC 5",
        "website bán sách": "website quản lý nhà sách",
        "Website bán sách": "Website quản lý nhà sách",
        "bán sách": "quản lý nhà sách",
        "khách hàng": "người dùng",
        "nhân viên": "quản trị viên",
        "Năm 2024": "Năm 2026",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def paragraph_text(p):
    return "".join((t.text or "") for t in p.findall(".//" + q(W, "t"))).strip()


def set_paragraph_text(p, value):
    texts = p.findall(".//" + q(W, "t"))
    if not texts:
        run = p.find(q(W, "r"))
        if run is None:
            run = ET.SubElement(p, q(W, "r"))
        t = ET.SubElement(run, q(W, "t"))
        t.text = value
        return
    texts[0].text = value
    texts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for node in texts[1:]:
        node.text = ""


def para(text="", style=None, bold=False, italic=False):
    p = ET.Element(q(W, "p"))
    if style:
        ppr = ET.SubElement(p, q(W, "pPr"))
        ET.SubElement(ppr, q(W, "pStyle"), {q(W, "val"): style})
    r = ET.SubElement(p, q(W, "r"))
    if bold or italic:
        rpr = ET.SubElement(r, q(W, "rPr"))
        if bold:
            ET.SubElement(rpr, q(W, "b"))
        if italic:
            ET.SubElement(rpr, q(W, "i"))
    t = ET.SubElement(r, q(W, "t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return p


def table(rows):
    tbl = ET.Element(q(W, "tbl"))
    tbl_pr = ET.SubElement(tbl, q(W, "tblPr"))
    ET.SubElement(tbl_pr, q(W, "tblStyle"), {q(W, "val"): "TableGrid"})
    borders = ET.SubElement(tbl_pr, q(W, "tblBorders"))
    for name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        ET.SubElement(borders, q(W, name), {q(W, "val"): "single", q(W, "sz"): "6", q(W, "space"): "0", q(W, "color"): "auto"})
    for row_index, row in enumerate(rows):
        tr = ET.SubElement(tbl, q(W, "tr"))
        for cell in row:
            tc = ET.SubElement(tr, q(W, "tc"))
            tc_pr = ET.SubElement(tc, q(W, "tcPr"))
            ET.SubElement(tc_pr, q(W, "tcW"), {q(W, "w"): "2800", q(W, "type"): "dxa"})
            if row_index == 0:
                ET.SubElement(tc_pr, q(W, "shd"), {q(W, "fill"): "D9EAF7"})
            p = ET.SubElement(tc, q(W, "p"))
            r = ET.SubElement(p, q(W, "r"))
            if row_index == 0:
                rpr = ET.SubElement(r, q(W, "rPr"))
                ET.SubElement(rpr, q(W, "b"))
            t = ET.SubElement(r, q(W, "t"))
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            t.text = str(cell)
    return tbl


def image_paragraph(rel_id, name, cx=5486400, cy=2600000):
    p = ET.Element(q(W, "p"))
    r = ET.SubElement(p, q(W, "r"))
    drawing = ET.SubElement(r, q(W, "drawing"))
    inline = ET.SubElement(drawing, q(WP, "inline"), {"distT": "0", "distB": "0", "distL": "0", "distR": "0"})
    ET.SubElement(inline, q(WP, "extent"), {"cx": str(cx), "cy": str(cy)})
    ET.SubElement(inline, q(WP, "effectExtent"), {"l": "0", "t": "0", "r": "0", "b": "0"})
    ET.SubElement(inline, q(WP, "docPr"), {"id": str(abs(hash(rel_id)) % 100000), "name": name})
    ET.SubElement(inline, q(WP, "cNvGraphicFramePr"))
    graphic = ET.SubElement(inline, q(A, "graphic"))
    graphic_data = ET.SubElement(graphic, q(A, "graphicData"), {"uri": PIC})
    pic = ET.SubElement(graphic_data, q(PIC, "pic"))
    nv = ET.SubElement(pic, q(PIC, "nvPicPr"))
    ET.SubElement(nv, q(PIC, "cNvPr"), {"id": "0", "name": name})
    ET.SubElement(nv, q(PIC, "cNvPicPr"))
    blip_fill = ET.SubElement(pic, q(PIC, "blipFill"))
    ET.SubElement(blip_fill, q(A, "blip"), {q(R, "embed"): rel_id})
    stretch = ET.SubElement(blip_fill, q(A, "stretch"))
    ET.SubElement(stretch, q(A, "fillRect"))
    sp_pr = ET.SubElement(pic, q(PIC, "spPr"))
    xfrm = ET.SubElement(sp_pr, q(A, "xfrm"))
    ET.SubElement(xfrm, q(A, "off"), {"x": "0", "y": "0"})
    ET.SubElement(xfrm, q(A, "ext"), {"cx": str(cx), "cy": str(cy)})
    prst = ET.SubElement(sp_pr, q(A, "prstGeom"), {"prst": "rect"})
    ET.SubElement(prst, q(A, "avLst"))
    return p


def add_svg_relationships(tmp_dir):
    rels_path = tmp_dir / "word" / "_rels" / "document.xml.rels"
    rels_root = ET.parse(rels_path).getroot()
    existing_ids = [r.attrib.get("Id", "") for r in rels_root.findall(q(REL, "Relationship"))]
    max_id = 0
    for rid in existing_ids:
        m = re.match(r"rId(\d+)$", rid)
        if m:
            max_id = max(max_id, int(m.group(1)))

    media_dir = tmp_dir / "word" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    image_map = {
        "system": WS / "05_uml" / "images" / "illustration_system_architecture_v1.svg",
        "face": WS / "05_uml" / "images" / "illustration_flask_face_api_v1.svg",
        "ocr": WS / "05_uml" / "images" / "illustration_ocr_cmnd_v1.svg",
        "search": WS / "05_uml" / "images" / "illustration_search_engine_v1.svg",
    }
    rel_map = {}
    for key, src in image_map.items():
        if not src.exists():
            continue
        dst_name = f"qlnhasach_{key}_v1.svg"
        shutil.copy2(src, media_dir / dst_name)
        max_id += 1
        rid = f"rId{max_id}"
        ET.SubElement(rels_root, q(REL, "Relationship"), {
            "Id": rid,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            "Target": f"media/{dst_name}",
        })
        rel_map[key] = rid
    ET.ElementTree(rels_root).write(rels_path, encoding="utf-8", xml_declaration=True)

    content_types_path = tmp_dir / "[Content_Types].xml"
    ct_root = ET.parse(content_types_path).getroot()
    has_svg = any(x.attrib.get("Extension") == "svg" for x in ct_root.findall(q(CT, "Default")))
    if not has_svg:
        ET.SubElement(ct_root, q(CT, "Default"), {"Extension": "svg", "ContentType": "image/svg+xml"})
        ET.ElementTree(ct_root).write(content_types_path, encoding="utf-8", xml_declaration=True)
    return rel_map


def synced_sections(rel_map):
    return {
        "MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG": [
            para("Nội dung cập nhật theo mã nguồn QLNhaSach", "Heading2", True),
            para("Đề tài được đồng bộ thành hệ thống quản lý nhà sách kết hợp nhận diện khuôn mặt, xác thực vị trí và quản lý mượn trả sách. Phạm vi chức năng không chỉ dừng ở bán sách trực tuyến mà còn bao gồm quy trình mượn/trả, OCR CMND/CCCD, geofence, nhật ký hệ thống và dashboard quản trị."),
            table([
                ["Nhóm chức năng", "Nội dung được triển khai trong source code"],
                ["Tài khoản và bảo mật", "Đăng ký, đăng nhập, MFA khuôn mặt, đăng ký mẫu mặt, challenge liveness."],
                ["Sản phẩm/sách", "Xem danh mục, tìm kiếm, gợi ý tên sách, chi tiết sách, file đọc thử, video, đánh giá."],
                ["Mượn/trả sách", "Kiểm tra hồ sơ CMND/CCCD, tồn kho, vị trí geofence, xác thực mặt và gửi yêu cầu mượn."],
                ["Quản trị", "Quản lý sách, danh mục, đơn hàng, người dùng, nhập hàng, vị trí nhà sách, log và thống kê."],
            ]),
            para("Hình minh họa kiến trúc tổng quan", italic=True),
            image_paragraph(rel_map["system"], "illustration_system_architecture_v1.svg") if "system" in rel_map else para("Xem hình: QLNhaSach_BaoCao/05_uml/images/illustration_system_architecture_v1.svg"),
        ],
        "PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG": [
            para("Bổ sung danh mục use case đồng bộ với source code", "Heading2", True),
            para("Danh mục use case được mở rộng từ FULL_INPUT v6 và các controller thực tế. Các tác nhân chính gồm khách vãng lai, người dùng đã đăng nhập, quản trị viên, Flask Face API, Gmail Service và SQL Server."),
            table([
                ["Tác nhân", "Use case tiêu biểu"],
                ["Khách vãng lai", "Xem trang chủ, tìm kiếm sách, xem chi tiết, lưu yêu thích cục bộ, đăng ký và đăng nhập."],
                ["Người dùng", "MFA khuôn mặt, OCR CMND/CCCD, yêu thích, giỏ hàng, đặt hàng, mượn sách có kiểm tra vị trí và xác thực mặt."],
                ["Quản trị viên", "Quản lý sách/danh mục/tồn kho, đơn hàng, người dùng, mượn/trả, nhập hàng, vị trí nhà sách, log và thống kê."],
                ["Hệ thống ngoài", "Flask Face API xử lý ảnh và Gmail Service gửi thông báo trạng thái."],
            ]),
            para("Sơ đồ liên quan", "Heading3", True),
            para("Các sơ đồ đã xuất để chỉnh sửa trong Draw.io: use_case_day_du_v2.drawio, sequence_face_login_v2.drawio, sequence_ocr_cmnd_v2.drawio, sequence_search_engine_v2.drawio, activity_search_engine_v2.drawio."),
        ],
        "THIẾT KẾ CƠ SỞ DỮ LIỆU": [
            para("Cập nhật phân tích dữ liệu theo chức năng mới", "Heading2", True),
            para("Cơ sở dữ liệu sử dụng Entity Framework qua QuanLySachDBContext cho dữ liệu nghiệp vụ và LogDbContext cho nhật ký. Các bảng bổ sung quan trọng gồm RentalRequests, StoreLocations, ProductFavorites, ProductReviews, FaceAuthLogs, GeofenceLogs và RentalLogs."),
            table([
                ["Nhóm bảng", "Vai trò"],
                ["Users/Quyens", "Lưu tài khoản, vai trò, thông tin CMND/CCCD và dữ liệu phục vụ mượn sách."],
                ["Sanphams/Categories", "Quản lý sách, danh mục, tồn kho, ảnh, file đọc thử và video giới thiệu."],
                ["Orders/Order_Detail", "Lưu đơn hàng và chi tiết sản phẩm đặt mua."],
                ["RentalRequests", "Lưu yêu cầu mượn/trả, trạng thái duyệt, ngày mượn và ngày trả."],
                ["FaceAuthLogs/GeofenceLogs/RentalLogs", "Lưu bằng chứng xác thực, kiểm tra vị trí và thay đổi trạng thái mượn/trả."],
            ]),
        ],
        "THIẾT KẾ CÁC CHỨC NĂNG CỦA HỆ THỐNG": [
            para("Thiết kế chức năng nhận diện khuôn mặt và OCR", "Heading2", True),
            para("ASP.NET MVC không xử lý ảnh trực tiếp mà gọi Flask Face API thông qua FaceAuthApiClient. API Flask sử dụng OpenCV để đọc ảnh, MediaPipe để phát hiện landmark khuôn mặt, histogram HSV để tạo descriptor, pytesseract để OCR CMND/CCCD và JSON profile để lưu mẫu khuôn mặt theo user_id."),
            para("Hình minh họa Flask Face API", italic=True),
            image_paragraph(rel_map["face"], "illustration_flask_face_api_v1.svg") if "face" in rel_map else para("Xem hình: illustration_flask_face_api_v1.svg"),
            para("Hình minh họa OCR CMND/CCCD", italic=True),
            image_paragraph(rel_map["ocr"], "illustration_ocr_cmnd_v1.svg") if "ocr" in rel_map else para("Xem hình: illustration_ocr_cmnd_v1.svg"),
            table([
                ["Endpoint Flask", "Mục đích"],
                ["/api/face/register", "Đăng ký mẫu khuôn mặt cho người dùng."],
                ["/api/face/verify, /api/face/authenticate", "So khớp ảnh hiện tại với mẫu đã lưu."],
                ["/api/face/action-check", "Kiểm tra hành động sống như quay mặt, há miệng, cười, nhìn lên/xuống."],
                ["/api/face/ocr-cmnd", "Đọc ảnh CMND/CCCD và trích xuất trường định danh."],
            ]),
        ],
        "THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT": [
            para("Thiết kế tìm kiếm và trải nghiệm tra cứu sách", "Heading2", True),
            para("Search engine của hệ thống là cơ chế tìm kiếm nội bộ bằng ProductController, SanphamDraw, Entity Framework/LINQ và SQL Server. Chức năng ListName trả gợi ý autocomplete, còn Search trả danh sách kết quả có phân trang bằng X.PagedList."),
            para("Hình minh họa search engine nội bộ", italic=True),
            image_paragraph(rel_map["search"], "illustration_search_engine_v1.svg") if "search" in rel_map else para("Xem hình: illustration_search_engine_v1.svg"),
            table([
                ["Thành phần", "Vai trò trong tìm kiếm"],
                ["ProductController.ListName", "Trả JSON gợi ý tên sách khi người dùng nhập từ khóa."],
                ["ProductController.Search", "Nhận keyWord, page, pagesize và render view kết quả."],
                ["SanphamDraw.getByKeyWord", "Lọc dữ liệu bằng Contains trên tên sách, tác giả, thể loại hoặc thông tin liên quan."],
                ["X.PagedList", "Phân trang danh sách sản phẩm để giao diện dễ theo dõi."],
            ]),
        ],
        "KIỂM THỬ HỆ THỐNG": [
            para("Bổ sung kiểm thử theo chức năng mở rộng", "Heading2", True),
            table([
                ["Mã", "Kịch bản", "Kết quả mong đợi"],
                ["TC-FACE-01", "Đăng nhập MFA với ảnh đúng mẫu và challenge hợp lệ", "Tạo USER_SESSION, ghi FaceAuthLogs thành công."],
                ["TC-FACE-02", "Xác thực khuôn mặt sai hoặc không có profile", "Từ chối đăng nhập/mượn sách, trả thông báo phù hợp."],
                ["TC-OCR-01", "Tải ảnh CMND/CCCD mặt trước và mặt sau", "Trích xuất số giấy tờ, họ tên, ngày sinh, địa chỉ và cập nhật hồ sơ."],
                ["TC-GEOFENCE-01", "Người dùng ở ngoài bán kính nhà sách", "Không cho gửi yêu cầu mượn, ghi GeofenceLogs."],
                ["TC-SEARCH-01", "Tìm sách theo tên/tác giả", "Hiển thị danh sách kết quả, gợi ý sách mới và tổng số kết quả."],
                ["TC-RENTAL-01", "Gửi yêu cầu mượn đủ điều kiện", "Tạo RentalRequest Pending, ghi RentalLogs và gửi email nếu cấu hình cho phép."],
            ]),
        ],
        "TỔNG KẾT VÀ ĐÁNH GIÁ": [
            para("Đánh giá sau khi đồng bộ với source code", "Heading2", True),
            para("Báo cáo sau khi cập nhật phản ánh đúng phạm vi hệ thống QLNhaSach: quản lý nhà sách, bán hàng, mượn/trả sách, nhận diện khuôn mặt, OCR CMND/CCCD, kiểm tra vị trí, thông báo Gmail, nhật ký và thống kê. Các sơ đồ PlantUML/Draw.io đi kèm được đặt trong QLNhaSach_BaoCao/05_uml để tiếp tục chỉnh sửa hoặc xuất ảnh khi hoàn thiện bản nộp cuối."),
        ],
    }


def insert_sections(body, rel_map):
    sections = synced_sections(rel_map)
    children = list(body)
    insertions = []
    for index, child in enumerate(children):
        if child.tag != q(W, "p"):
            continue
        text = replace_report_text(repair_text(paragraph_text(child))).upper()
        for heading, nodes in sections.items():
            if heading in text:
                insertions.append((index + 1, nodes))
                break
    for index, nodes in reversed(insertions):
        for node in reversed(nodes):
            body.insert(index, copy.deepcopy(node))
    return len(insertions)


def update_document_xml(tmp_dir, rel_map):
    doc_path = tmp_dir / "word" / "document.xml"
    tree = ET.parse(doc_path)
    root = tree.getroot()
    body = root.find(".//" + q(W, "body"))

    for p in root.findall(".//" + q(W, "p")):
        text = paragraph_text(p)
        if not text:
            continue
        repaired = replace_report_text(repair_text(text))
        if repaired != text:
            set_paragraph_text(p, repaired)

    inserted = insert_sections(body, rel_map)
    tree.write(doc_path, encoding="utf-8", xml_declaration=True)
    return inserted


def zip_dir(src_dir, out_file):
    if out_file.exists():
        stem = out_file.stem
        suffix = out_file.suffix
        i = 2
        while (out_file.parent / f"{stem}_v{i}{suffix}").exists():
            i += 1
        out_file = out_file.parent / f"{stem}_v{i}{suffix}"
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in src_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(src_dir).as_posix())
    return out_file


def main():
    ensure_dirs()
    if not TEMPLATE.exists():
        raise FileNotFoundError(TEMPLATE)
    tmp_dir = WS / "12_archive" / "tmp_synced_docx"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)
    with zipfile.ZipFile(TEMPLATE) as zf:
        zf.extractall(tmp_dir)

    rel_map = add_svg_relationships(tmp_dir)
    inserted = update_document_xml(tmp_dir, rel_map)
    out = zip_dir(tmp_dir, OUTPUT)
    shutil.rmtree(tmp_dir)

    hist = HISTORY / "008_dong_bo_bao_cao_mau_theo_full_input_v6.md"
    hist.write_text(f"""# 008 - Đồng bộ báo cáo mẫu theo FULL_INPUT v6

Thời điểm: {now()} Asia/Bangkok

## Kết quả

- File Word mới: `{out.relative_to(ROOT).as_posix()}`
- Nguồn: `QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx`
- Input đồng bộ: `{INPUT.relative_to(ROOT).as_posix()}`
- Số vị trí chương đã chèn nội dung: {inserted}

## Nội dung đã sửa

- Sinh viên: Lê Việt Thắng
- MSSV: 2224802010263
- Đề tài: Xây dựng website quản lý nhà sách kết hợp nhận diện khuôn mặt, xác thực vị trí và quản lý mượn trả sách
- Chèn nội dung theo từng phần: yêu cầu hệ thống, use case, cơ sở dữ liệu, Face API/OCR, search engine, kiểm thử, tổng kết.
""", encoding="utf-8")

    with (LOGS / "execution_log.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {now()}\n\n")
        f.write(f"- Tạo DOCX đồng bộ theo FULL_INPUT v6: `{out.relative_to(ROOT).as_posix()}`.\n")
        f.write(f"- Chèn nội dung vào {inserted} vị trí chương/phần liên quan.\n")

    ok = out.exists() and out.stat().st_size > 0 and inserted >= 5
    (VALIDATION / "synced_report_docx_validation_v1.md").write_text(f"""# Validation - DOCX đồng bộ FULL_INPUT v6

Thời điểm: {now()} Asia/Bangkok

| Hạng mục | Kết quả |
|---|---|
| File DOCX mới tồn tại | {'OK' if out.exists() else 'CẦN KIỂM TRA'} |
| File có dung lượng | {'OK' if out.exists() and out.stat().st_size > 0 else 'CẦN KIỂM TRA'} |
| Chèn theo chương liên quan | {'OK' if inserted >= 5 else 'CẦN KIỂM TRA'} |
| Nhúng SVG minh họa | {'OK' if len(rel_map) >= 4 else 'CẦN KIỂM TRA'} |

File: `{out.relative_to(ROOT).as_posix()}`
""", encoding="utf-8")

    print(out.relative_to(ROOT))
    print(f"inserted_sections={inserted}")


if __name__ == "__main__":
    main()
