# -*- coding: utf-8 -*-
from pathlib import Path
import datetime
import html
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "BaoCaoMau.docx"
OUTPUT = ROOT / "BaoCaoMauSua.docx"
BACKUP = ROOT / "BaoCaoMauSua.before_template_update.docx"
HISTORY = ROOT / "LichSuQuaTrinhVietBaoCao.md"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def log(message):
    with HISTORY.open("a", encoding="utf-8") as file:
        file.write("\n## " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        file.write(message.rstrip() + "\n")


TITLE_MAP = {
    "NGUYỄN THANH LÂMNGÀNH KỸ THUẬT PHẦN MỀM": "LÊ VIỆT THẮNGNGÀNH KỸ THUẬT PHẦN MỀM",
    "XÂY DỰNG WEBSITE BÁN SÁCH BẰNG ASP.NET CORE": "QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH",
    "ThS.Nguyễn Thiện Thanh": "........................................",
    "ThS. Nguyễn Thiện Thanh": "........................................",
    "Nguyễn Thanh Lâm": "Lê Việt Thắng",
    "1234": "2224802010263",
    "Hà Nội – Năm 2024": "Hà Nội – Năm 2026",
    "Hà Nội – Năm  2024": "Hà Nội – Năm 2026",
    "Trang này đặt phiếu giao đề tài vào đây": "Trang này đặt phiếu giao đề tài hoặc nhiệm vụ đồ án theo mẫu của khoa",
    "(BÁO CÁO NÊN LÀM TỪ 50 đến 80 TRANG)": "(BÁO CÁO ĐƯỢC CẬP NHẬT THEO MẪU, GIỮ CẤU TRÚC VÀ CHUẨN HÓA THEO DỰ ÁN QLNHASACH)",
    "HTCSDL": "API",
    "Hệ thống cơ sở dữ liệu": "Application Programming Interface",
    "CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG1": "CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG1",
    "1.2 Khảo sát hệ thống1": "1.2 Khảo sát hệ thống quản lý nhà sách1",
    "1.2.1 Tổng quan về hệ thống1": "1.2.1 Tổng quan về hệ thống QLNhaSach1",
    "1.3.1 Hoạt động bán hàng2": "1.3.1 Hoạt động bán sách và mượn/trả sách2",
    "1.3.2 Báo cáo, thống kê3": "1.3.2 Ghi log, thông báo và thống kê3",
    "1.3.3 Cập nhật thông tin hệ thống4": "1.3.3 Cập nhật hồ sơ, OCR và xác thực khuôn mặt4",
    "2.2.2 Đánh giá sản phẩm14": "2.2.2 Đánh giá sách và xem file review14",
    "2.2.4 Thêm vào danh sách yêu thích17": "2.2.4 Quản lý sách yêu thích17",
    "2.2.5 Mua hàng18": "2.2.5 Đặt hàng và gửi yêu cầu mượn sách18",
    "2.2.7 Đơn hàng của tôi20": "2.2.7 Lịch sử đơn hàng và lịch sử mượn sách20",
    "2.2.11 Quản lý khách hàng25": "2.2.11 Quản lý người dùng và hồ sơ định danh25",
    "2.2.13 Quản lý nhân viên29": "2.2.13 Quản lý xác thực khuôn mặt, OCR và Gmail29",
    "2.2.14 Thống kê31": "2.2.14 Nhật ký hệ thống, mượn/trả và chatbox31",
    "5.1 Mô hình kiến trúc dự án76": "5.1 Mô hình kiến trúc dự án76",
    "5.1.1 Giới thiệu về kiến trúc onion76": "5.1.1 Giới thiệu kiến trúc ASP.NET MVC kết hợp Flask API76",
    "5.1.2 Các lớp trong kiến trúc onion76": "5.1.2 Các lớp trong kiến trúc hệ thống76",
    "5.1.3 Ưu nhược điểm của kiến trúc onion77": "5.1.3 Ưu nhược điểm của kiến trúc tách MVC và Flask77",
    "5.2.1 ASP.NET Core78": "5.2.1 ASP.NET MVC 5 và .NET Framework78",
}


REPLACEMENTS = [
    ("ASP.NET Core", "ASP.NET MVC 5"),
    ("Asp.Net Core", "ASP.NET MVC 5"),
    ("asp.net core", "ASP.NET MVC 5"),
    ("website bán sách", "website quản lý nhà sách tích hợp mượn/trả sách"),
    ("Website bán sách", "Website quản lý nhà sách tích hợp mượn/trả sách"),
    ("bán sách", "quản lý nhà sách"),
    ("mua hàng", "đặt hàng hoặc gửi yêu cầu mượn sách"),
    ("giỏ hàng", "giỏ hàng và quy trình mượn sách"),
    ("nhân viên", "quản trị viên"),
    ("khách hàng", "người dùng"),
    ("Authors", "Users"),
    ("AuthorProducts", "RentalRequests"),
    ("Banners", "Slides"),
    ("Brands", "StoreLocations"),
    ("CategoryProducts", "ProductFavorites"),
    ("Comments", "ProductReviews"),
    ("Customers", "Users"),
    ("Employees", "FaceAuthLogs"),
    ("FavouriteProducts", "ProductFavorites"),
    ("Images", "FaceSamples"),
    ("Products", "Sanphams"),
    ("UserClaims", "FaceAuthLogs"),
    ("Roles", "Quyens"),
    ("RoleClaims", "RentalLogs"),
    ("UserRoles", "GeofenceLogs"),
    ("UserLogins", "FaceRentalTokens"),
    ("UserTokens", "FaceRentalTokens"),
    ("Provinces", "StoreLocations"),
    ("Districts", "RentalLogs"),
    ("Wards", "GeofenceLogs"),
    ("Authors của dự án", "Users của dự án"),
    ("Products của dự án", "Sanphams của dự án"),
    ("Onion", "MVC kết hợp API phụ trợ"),
    ("onion", "MVC kết hợp API phụ trợ"),
]


SECTION_MARKERS = {
    "front": [
        "LỜI NÓI ĐẦU",
        "DANH MỤC CÁC TỪ VIẾT TẮT",
        "DANH MỤC CÁC HÌNH ẢNH",
        "MỤC LỤC",
    ],
    "chapter1": ["CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG", "MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG"],
    "chapter2": ["CHƯƠNG 2. PHÂN TÍCH CÁC YÊU CẦU", "PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG"],
    "chapter3": ["CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU", "THIẾT KẾ CƠ SỞ DỮ LIỆU"],
    "chapter4": ["CHƯƠNG 4. THIẾT KẾ CÁC CHỨC NĂNG", "THIẾT KẾ CÁC CHỨC NĂNG"],
    "chapter5": ["CHƯƠNG 5. THIẾT KẾ GIAO DIỆN", "THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT"],
    "chapter6": ["CHƯƠNG 6. KIỂM THỬ HỆ THỐNG", "KIỂM THỬ HỆ THỐNG"],
    "chapter7": ["CHƯƠNG 7. TỔNG KẾT", "TỔNG KẾT VÀ ĐÁNH GIÁ"],
    "refs": ["TÀI LIỆU THAM KHẢO"],
}


POOLS = {
    "front": [
        "Báo cáo được cập nhật theo mẫu gốc, giữ nguyên cấu trúc trình bày nhưng thay nội dung sang đề tài quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn/trả sách.",
        "Đề tài sử dụng source ASP.NET MVC trong thư mục QLNhaSach và source Flask trong thư mục NHANDIENKHUONMAT-new07040226 làm căn cứ phân tích, thiết kế, cài đặt và kiểm thử.",
        "Các phần danh mục hình, mục lục và bảng biểu được điều chỉnh để phản ánh các module: người dùng, sản phẩm, mượn/trả, Face API, OCR CMND/CCCD, Gmail và chatbox.",
    ],
    "chapter1": [
        "Hệ thống quản lý nhà sách cần hỗ trợ nghiệp vụ bán sách, quản lý tồn kho, quản lý người dùng và mở rộng quy trình mượn/trả sách có định danh rõ ràng.",
        "Điểm khác biệt của đề tài là yêu cầu xác thực khuôn mặt trước khi mượn sách, OCR CMND/CCCD để chuẩn hóa hồ sơ và gửi Gmail thông báo theo trạng thái xử lý.",
        "Người dùng có thể đăng ký, đăng nhập, cập nhật hồ sơ, xem sách, đánh giá, yêu thích, đặt hàng, gửi yêu cầu mượn và theo dõi lịch sử mượn/trả.",
        "Quản trị viên quản lý sách, danh mục, kho, hóa đơn, người dùng, yêu cầu mượn/trả, log xác thực, log nghiệp vụ và cấu hình thông báo.",
        "Yêu cầu phi chức năng gồm giao diện dễ dùng, dữ liệu nhất quán, log đầy đủ, API phản hồi JSON rõ ràng và hệ thống hiển thị lỗi thân thiện khi dịch vụ phụ trợ không sẵn sàng.",
    ],
    "chapter2": [
        "Tác nhân chính gồm khách vãng lai, người dùng thành viên, quản trị viên, Flask Face API/OCR, Gmail và chatbox tư vấn sách.",
        "Use case xem sản phẩm cho phép người dùng duyệt danh sách sách, tìm kiếm, xem chi tiết, đánh giá và kiểm tra tồn kho trước khi đặt hàng hoặc mượn sách.",
        "Use case cập nhật hồ sơ định danh yêu cầu người dùng bổ sung họ tên, Gmail, CMND/CCCD và có thể dùng OCR để đọc thông tin từ ảnh giấy tờ.",
        "Use case xác thực khuôn mặt gồm đăng ký mẫu mặt, action challenge chống thao tác sai quy trình và so khớp khuôn mặt trước khi mượn sách.",
        "Use case quản trị mượn/trả cho phép admin duyệt, từ chối, hủy, xác nhận trả, đánh dấu quá hạn, cập nhật tồn kho và ghi log.",
        "Chatbox hỗ trợ người dùng hỏi về tên sách, giá, tồn kho và hướng dẫn mượn sách thông qua endpoint Flask.",
    ],
    "chapter3": [
        "Cơ sở dữ liệu QLNhaSach lưu thông tin người dùng, sách, danh mục, đơn hàng, kho, yêu cầu mượn/trả, đánh giá, yêu thích và nhật ký hệ thống.",
        "Bảng RentalRequests lưu user, sách, số lượng, trạng thái, ngày yêu cầu, ngày mượn, hạn trả, ngày trả thực tế và ghi chú xử lý.",
        "Bảng FaceAuthLogs lưu lịch sử đăng ký/xác thực khuôn mặt, action, purpose, result, confidence, request_id và mã lỗi nếu có.",
        "Bảng RentalLogs lưu lịch sử nghiệp vụ mượn/trả như Request, Cancel, Approve, Reject, Return và Overdue.",
        "Các bảng ProductReviews và ProductFavorites mở rộng trải nghiệm người dùng bằng đánh giá và danh sách sách yêu thích.",
        "Dữ liệu phụ trợ phía Flask gồm face_db.pkl để lưu embedding khuôn mặt và chatbox_knowledge.json để lưu tri thức tư vấn sách.",
    ],
    "chapter4": [
        "BaiTapLon là project ASP.NET MVC chứa controller, view và cấu hình Web.config; Mood chứa model Entity Framework; Common chứa repository ghi log.",
        "UsersController xử lý đăng ký, đăng nhập, hồ sơ người dùng và luồng đăng ký khuôn mặt thông qua view RegisterFace.",
        "ProductController xử lý danh sách sách, tìm kiếm, chi tiết, đánh giá và điểm bắt đầu của quy trình mượn sách.",
        "FaceAuthController nhận ảnh upload, validate file, lưu tạm, gọi Flask API, đọc JSON, kiểm tra confidence và ghi FaceAuthLogs.",
        "RentalController tạo yêu cầu mượn, kiểm tra faceToken, tồn kho, hồ sơ định danh và cho phép admin cập nhật trạng thái mượn/trả.",
        "GmailNotificationService gửi thông báo theo sự kiện Request, ApproveSuccess, Reject, Cancel, Return và Overdue.",
        "Flask app.py cung cấp các endpoint /api/face/register, /verify, /authenticate, /action-check, /ocr-cmnd và các endpoint chatbox.",
    ],
    "chapter5": [
        "Giao diện website được xây dựng bằng Razor View, HTML, CSS, JavaScript, Bootstrap và jQuery, phù hợp với mô hình ASP.NET MVC.",
        "Các màn hình chính gồm trang chủ, danh sách sách, chi tiết sách, đăng nhập, hồ sơ người dùng, đăng ký khuôn mặt, OCR giấy tờ và danh sách mượn/trả.",
        "Cấu hình tích hợp quan trọng trong Web.config gồm FaceAuthAPI, ChatboxWidgetUrl, FaceAuthMinConfidence, FaceAuthRentalTokenMinutes, RentalMaxBorrowDays và GmailNotificationsEnabled.",
        "Flask server chạy ở port 8000, nhận multipart/form-data, xử lý ảnh bằng OpenCV, nhận diện bằng InsightFace và action-check bằng MediaPipe.",
        "Chatbox được nhúng qua widget.js và gọi /api/chatbox/ask để trả lời câu hỏi về sách, giá, tồn kho và hướng dẫn mượn.",
        "Khi triển khai local cần chạy SQL Server/LocalDB, website ASP.NET MVC và Flask server song song.",
    ],
    "chapter6": [
        "Kiểm thử tài khoản gồm đăng ký hợp lệ, đăng ký trùng, đăng nhập đúng/sai và cập nhật hồ sơ người dùng.",
        "Kiểm thử OCR gồm ảnh rõ, ảnh mờ, thiếu mặt trước/mặt sau, ảnh sai giấy tờ và kiểm tra khả năng chỉnh tay thông tin.",
        "Kiểm thử nhận diện gồm đăng ký mẫu mặt, xác thực đúng người, sai người, ảnh nhiều khuôn mặt, ảnh kém sáng và action challenge.",
        "Kiểm thử mượn/trả gồm mượn khi còn tồn, hết tồn, thiếu hồ sơ, chưa xác thực, quá số ngày mượn, admin duyệt, trả và đánh dấu quá hạn.",
        "Kiểm thử Gmail gồm cấu hình đúng, sai app password, tắt thông báo và ghi nhận lỗi SMTP vào log.",
        "Kiểm thử chatbox gồm hỏi tên sách, giá, tồn kho, hướng dẫn mượn và tình huống server chatbox mất kết nối.",
    ],
    "chapter7": [
        "Đề tài đã chuẩn hóa hệ thống quản lý nhà sách theo hướng có xác thực khuôn mặt, OCR hồ sơ định danh, Gmail thông báo và chatbox tư vấn.",
        "Việc tách Flask Face API thành dịch vụ riêng giúp website ASP.NET MVC dễ nâng cấp mô hình nhận diện, OCR và action-check mà không phá vỡ nghiệp vụ web.",
        "Hạn chế còn lại là OCR phụ thuộc chất lượng ảnh, nhận diện phụ thuộc ánh sáng/camera và Gmail phụ thuộc cấu hình app password.",
        "Hướng phát triển gồm dashboard thống kê mượn/trả, tối ưu OCR, triển khai production cho Flask API, bảo mật embedding và nâng cấp chatbox theo dữ liệu thực tế.",
    ],
    "refs": [
        "Tài liệu ASP.NET MVC 5, Entity Framework 6, Flask, InsightFace, MediaPipe, PaddleOCR, Tesseract OCR và source code QLNhaSach.",
    ],
}


SHORT_REPLACEMENTS = {
    "DN_01": "DN_01",
    "DN_02": "DN_02",
    "DN_03": "DN_03",
    "XSP_01": "XS_01",
    "MH_01": "MS_01",
    "AGH_01": "XT_01",
    "QLSP_01": "QLS_01",
    "QLNV_01": "QLXT_01",
    "GD_01": "GD_01",
    "U": "U",
    "F": "F",
    "ID": "ID",
    "STT": "STT",
    "CBHD": "CBHD",
    "Sinh viên": "Sinh viên",
    "Mã số sinh viên": "Mã số sinh viên",
    ":": ":",
}


def apply_replacements(text):
    updated = text
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    return updated


def detect_section(text, current):
    upper = text.upper()
    for section, markers in SECTION_MARKERS.items():
        if any(marker in upper for marker in markers):
            return section
    return current


def looks_like_heading(text):
    stripped = text.strip()
    return (
        stripped in TITLE_MAP
        or stripped.isupper()
        or bool(re.match(r"^(\d+(\.\d+)*|CHƯƠNG|Hình|Bảng|TÀI LIỆU|MỤC LỤC|DANH MỤC|LỜI NÓI)", stripped))
    )


def transform_text(text, section, counter):
    stripped = text.strip()
    if not stripped:
        return text
    if re.fullmatch(r"[-–—_.\s]+", stripped):
        return stripped
    if stripped in TITLE_MAP:
        return TITLE_MAP[stripped]
    if stripped in SHORT_REPLACEMENTS:
        return SHORT_REPLACEMENTS[stripped]

    updated = apply_replacements(stripped)

    if "Lời đầu tiên em xin" in stripped:
        return (
            "Lời đầu tiên em xin chân thành cảm ơn quý thầy cô trong khoa công nghệ thông tin đã hỗ trợ em trong quá trình học tập, rèn luyện và thực hiện đề tài. "
            "Em xin gửi lời cảm ơn đến giảng viên hướng dẫn đã góp ý, định hướng và giúp em hoàn thiện báo cáo quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn/trả sách."
        )
    if "Thông qua đồ án tốt nghiệp này" in stripped:
        return (
            "Thông qua đồ án tốt nghiệp này, em đã vận dụng kiến thức về ASP.NET MVC, Entity Framework, SQL Server, Flask API, nhận diện khuôn mặt, OCR CMND/CCCD, Gmail và chatbox. "
            "Quá trình thực hiện giúp em hiểu rõ hơn cách kết hợp nghiệp vụ web với dịch vụ AI phụ trợ trong một hệ thống thực tế."
        )

    if looks_like_heading(updated):
        return updated

    # Table cells and very short labels should stay compact after project-term updates.
    if len(stripped) <= 25:
        return updated

    pool = POOLS.get(section) or POOLS["chapter1"]
    return pool[counter % len(pool)]


def paragraph_text(pnode):
    return "".join((t.text or "") for t in pnode.findall(".//w:t", NS)).strip()


def set_paragraph_text(pnode, value):
    text_nodes = pnode.findall(".//w:t", NS)
    if not text_nodes:
        return
    text_nodes[0].text = value
    text_nodes[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for node in text_nodes[1:]:
        node.text = ""


def update_document_xml(xml_bytes):
    root = ET.fromstring(xml_bytes)
    section = "front"
    counters = {key: 0 for key in POOLS}
    changed = 0

    for pnode in root.findall(".//w:p", NS):
        original = paragraph_text(pnode)
        if not original:
            continue
        section = detect_section(original, section)
        new_text = transform_text(original, section, counters.get(section, 0))
        if not looks_like_heading(original) and len(original.strip()) > 25:
            counters[section] = counters.get(section, 0) + 1
        if new_text != original:
            set_paragraph_text(pnode, new_text)
            changed += 1

    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return xml, changed


def copy_and_update_docx():
    if OUTPUT.exists():
        shutil.copy2(OUTPUT, BACKUP)

    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        document_xml, changed = update_document_xml(zin.read("word/document.xml"))
        with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = document_xml
                zout.writestr(item, data)

    with zipfile.ZipFile(OUTPUT, "r") as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
        text = " ".join(html.unescape(x) for x in re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml))
        checks = {
            "media": len([n for n in names if n.startswith("word/media/")]),
            "tables": xml.count("<w:tbl>"),
            "changed": changed,
            "has_project_title": "QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH" in text,
            "has_old_student": "Nguyễn Thanh Lâm" in text or "NGUYỄN THANH LÂM" in text,
            "has_old_aspnet_core": "ASP.NET Core" in text or "Asp.Net Core" in text,
        }
    return checks


def main():
    checks = copy_and_update_docx()
    log(
        "- Đã cập nhật `BaoCaoMauSua.docx` trực tiếp từ nền `BaoCaoMau.docx`, giữ cấu trúc/media/bảng của báo cáo mẫu.\n"
        f"- Số đoạn văn bản đã thay đổi: {checks['changed']}.\n"
        f"- Media giữ lại: {checks['media']}; bảng giữ lại: {checks['tables']}.\n"
        "- Cách làm: không dựng lại tài liệu trắng, chỉ thay câu chữ theo từng đoạn/section để phù hợp dự án QLNhaSach + Flask."
    )
    print(checks)


if __name__ == "__main__":
    main()
