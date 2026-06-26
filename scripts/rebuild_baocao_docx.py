# -*- coding: utf-8 -*-
from pathlib import Path
import datetime
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FLASK_ROOT = Path(r"D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226")
ASSETS = ROOT / "report_assets"
HISTORY = ROOT / "LichSuQuaTrinhVietBaoCao.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_report_docx import Docx, make_drawio, make_flow, make_usecase  # noqa: E402


def log(message):
    with HISTORY.open("a", encoding="utf-8") as file:
        file.write("\n## " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        file.write(message.rstrip() + "\n")


def ensure_assets():
    ASSETS.mkdir(exist_ok=True)
    make_drawio(ASSETS / "usecase_quan_ly_nha_sach.drawio")
    make_usecase(ASSETS / "usecase_quan_ly_nha_sach.png")
    make_flow(
        ASSETS / "workflow_muon_sach.png",
        "Quy trình người dùng mượn sách",
        [
            "Đăng nhập",
            "Cập nhật Gmail và CMND/CCCD",
            "Chọn sách cần mượn",
            "Xác thực khuôn mặt",
            "Gửi yêu cầu mượn",
            "Admin duyệt",
            "Gửi Gmail thông báo",
        ],
    )
    make_flow(
        ASSETS / "workflow_ocr_face.png",
        "Quy trình OCR CMND/CCCD và xác thực khuôn mặt",
        [
            "Tải ảnh mặt trước/sau",
            "Lưu ảnh giấy tờ",
            "Gọi Flask Face API",
            "OCR bằng PaddleOCR/Tesseract",
            "So khớp khuôn mặt",
            "Cập nhật hồ sơ định danh",
        ],
    )
    make_flow(
        ASSETS / "workflow_admin.png",
        "Quy trình admin xử lý mượn trả",
        [
            "Xem yêu cầu Pending",
            "Kiểm tra hồ sơ và tồn kho",
            "Duyệt hoặc từ chối",
            "Giảm tồn kho khi duyệt",
            "Xác nhận trả sách",
            "Tăng tồn kho và ghi log",
        ],
    )


def p_many(doc, paragraphs):
    for text in paragraphs:
        doc.p(text)


def bullets(doc, items):
    for item in items:
        doc.bullet(item)


def numbered(doc, items):
    for index, item in enumerate(items, start=1):
        doc.p(f"{index}. {item}")


def caption(doc, text):
    doc.p(text, align="center", italic=True, size=22)


def page_break(doc):
    doc.page_break()


def add_front_matter(doc):
    doc.p("TRƯỜNG ĐẠI HỌC THỦ DẦU MỘT", align="center", bold=True, size=28)
    doc.p("KHOA CÔNG NGHỆ THÔNG TIN", align="center", bold=True, size=26)
    doc.p("")
    doc.p("BÁO CÁO ĐỒ ÁN", align="center", bold=True, size=34)
    doc.p(
        "QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH",
        align="center",
        bold=True,
        size=32,
    )
    doc.p("")
    doc.p("Sinh viên thực hiện: Lê Việt Thắng", align="center", bold=True, size=26)
    doc.p("MSSV: 2224802010263", align="center", bold=True, size=26)
    doc.p("Lớp: ........................................", align="center", size=24)
    doc.p("Giảng viên hướng dẫn: ........................................", align="center", size=24)
    doc.p("")
    doc.p("Bình Dương, tháng 05 năm 2026", align="center", bold=True, size=26)
    page_break(doc)

    doc.heading("LỜI CẢM ƠN", 1)
    p_many(
        doc,
        [
            "Em xin chân thành cảm ơn quý thầy cô Khoa Công nghệ thông tin đã truyền đạt kiến thức nền tảng và tạo điều kiện để em thực hiện đề tài. Em cũng xin cảm ơn giảng viên hướng dẫn đã góp ý trong quá trình phân tích, triển khai và hoàn thiện báo cáo.",
            "Báo cáo này được xây dựng dựa trên source hệ thống quản lý nhà sách QLNhaSach và source Flask nhận diện khuôn mặt, OCR CMND/CCCD, chatbox tư vấn sách. Trong quá trình thực hiện, em đã cố gắng trình bày rõ nghiệp vụ, công nghệ, cách tích hợp và kết quả kiểm thử. Do kinh nghiệm còn hạn chế, báo cáo khó tránh khỏi thiếu sót; em mong nhận được góp ý để tiếp tục hoàn thiện hệ thống.",
        ],
    )
    page_break(doc)

    doc.heading("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", 1)
    for _ in range(14):
        doc.p("........................................................................................................................")
    doc.p("Điểm: ..............................", align="right")
    doc.p("Chữ ký giảng viên: ..............................", align="right")
    page_break(doc)

    doc.heading("MỤC LỤC", 1)
    for item in [
        "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI",
        "1.1. Lý do chọn đề tài",
        "1.2. Mục tiêu đề tài",
        "1.3. Phạm vi và phương pháp thực hiện",
        "CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ",
        "CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG",
        "CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG",
        "CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ",
        "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN",
        "TÀI LIỆU THAM KHẢO",
        "PHỤ LỤC",
    ]:
        doc.p(item)
    page_break(doc)

    doc.heading("DANH MỤC HÌNH", 1)
    for item in [
        "Hình 3.1. Sơ đồ use case tổng quát của hệ thống",
        "Hình 3.2. Quy trình người dùng gửi yêu cầu mượn sách",
        "Hình 3.3. Quy trình OCR CMND/CCCD và xác thực khuôn mặt",
        "Hình 3.4. Quy trình admin xử lý mượn/trả sách",
        "Hình 4.1. Trang chủ hệ thống quản lý nhà sách",
        "Hình 4.2. Màn hình danh sách sản phẩm sách",
        "Hình 4.3. Màn hình đăng nhập hệ thống",
        "Hình 4.4. Màn hình danh sách mượn/trả sách",
    ]:
        doc.p(item)
    doc.heading("DANH MỤC BẢNG", 1)
    for item in [
        "Bảng 2.1. Công nghệ sử dụng phía website ASP.NET MVC",
        "Bảng 2.2. Công nghệ sử dụng phía Flask Face API/OCR/chatbox",
        "Bảng 3.1. Tác nhân và vai trò",
        "Bảng 3.2. Mô tả bảng dữ liệu chính",
        "Bảng 4.1. Cấu trúc source",
        "Bảng 4.2. Controller/service chính",
        "Bảng 4.3. Endpoint Flask và chức năng",
        "Bảng 5.1. Kịch bản kiểm thử",
    ]:
        doc.p(item)
    page_break(doc)


def add_chapter_1(doc):
    doc.heading("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI", 1)
    doc.heading("1.1. Lý do chọn đề tài", 2)
    p_many(
        doc,
        [
            "Nhà sách là môi trường có nhiều nghiệp vụ lặp lại như quản lý danh mục sách, tồn kho, đơn hàng, người dùng, phản hồi và thống kê. Khi mở rộng thêm chức năng mượn/trả sách, hệ thống cần giải quyết thêm bài toán định danh người mượn, theo dõi trạng thái xử lý, hạn trả và lịch sử thao tác.",
            "Nếu chỉ dựa vào tài khoản và mật khẩu, quá trình mượn sách vẫn có rủi ro người dùng mượn hộ, khai báo thiếu thông tin hoặc nhập sai giấy tờ. Vì vậy, đề tài lựa chọn tích hợp nhận diện khuôn mặt, OCR CMND/CCCD và gửi Gmail thông báo vào hệ thống quản lý nhà sách. Cách tiếp cận này giúp tăng độ tin cậy khi xác thực, giảm thao tác nhập liệu hồ sơ và giúp quản trị viên theo dõi quy trình mượn/trả rõ ràng hơn.",
        ],
    )
    doc.heading("1.2. Mục tiêu đề tài", 2)
    bullets(
        doc,
        [
            "Xây dựng báo cáo kỹ thuật cho hệ thống quản lý nhà sách trên nền tảng ASP.NET MVC.",
            "Mô tả đầy đủ quy trình mượn/trả sách có kiểm tra đăng nhập, hồ sơ định danh, tồn kho, xác thực khuôn mặt và thời hạn mượn.",
            "Trình bày cách website ASP.NET MVC tích hợp với Flask Face API để đăng ký khuôn mặt, xác thực khuôn mặt, kiểm tra hành động và OCR CMND/CCCD.",
            "Trình bày cơ chế gửi Gmail thông báo khi người dùng tạo yêu cầu mượn, admin duyệt, từ chối, hủy, trả sách hoặc đánh dấu quá hạn.",
            "Bổ sung chatbox tư vấn sách, giá, tồn kho và hướng dẫn mượn sách dựa trên module Flask `sales_chatbox`.",
            "Hoàn thiện sơ đồ use case, sơ đồ quy trình, bảng công nghệ, bảng endpoint, test case và phụ lục triển khai.",
        ],
    )
    doc.heading("1.3. Phạm vi thực hiện", 2)
    p_many(
        doc,
        [
            "Phạm vi hệ thống gồm source website `QLNhaSach` và source Flask tại `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226`. Website quản lý nhà sách được xây dựng theo mô hình ASP.NET MVC, sử dụng Entity Framework 6 và SQL Server LocalDB. Server Flask đóng vai trò dịch vụ phụ trợ cho nhận diện khuôn mặt, OCR CMND/CCCD và chatbox.",
            "Báo cáo tập trung vào phân tích, thiết kế, tích hợp và kiểm thử ứng dụng. Phần AI được trình bày ở mức ứng dụng thư viện/mô hình có sẵn như InsightFace, MediaPipe, PaddleOCR và Tesseract; đề tài không tự huấn luyện mô hình nhận diện khuôn mặt từ đầu.",
        ],
    )
    doc.heading("1.4. Phương pháp thực hiện", 2)
    numbered(
        doc,
        [
            "Khảo sát source hiện có, xác định controller, model, service, cấu hình và bảng dữ liệu chính.",
            "Phân tích nghiệp vụ người dùng, quản trị viên, Face API/OCR, Gmail và chatbox.",
            "Thiết kế sơ đồ use case, quy trình mượn sách, quy trình OCR/xác thực khuôn mặt và quy trình admin xử lý mượn/trả.",
            "Đối chiếu cấu hình trong `Web.config` với endpoint thực tế của Flask.",
            "Xây dựng kế hoạch kiểm thử theo từng nhóm chức năng và ghi nhận tiêu chí nghiệm thu.",
        ],
    )
    doc.heading("1.5. Bố cục báo cáo", 2)
    p_many(
        doc,
        [
            "Báo cáo gồm năm chương chính. Chương 1 trình bày tổng quan đề tài. Chương 2 trình bày cơ sở lý thuyết và công nghệ. Chương 3 phân tích và thiết kế hệ thống. Chương 4 mô tả triển khai hệ thống theo source thực tế. Chương 5 trình bày kiểm thử, đánh giá, hạn chế và hướng phát triển.",
        ],
    )
    page_break(doc)


def add_chapter_2(doc):
    doc.heading("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ", 1)
    doc.heading("2.1. Công nghệ phía website quản lý nhà sách", 2)
    doc.table(
        [
            ["Thành phần", "Công nghệ", "Vai trò"],
            ["Backend web", "ASP.NET MVC 5, C#", "Xử lý controller, view và nghiệp vụ quản lý nhà sách"],
            ["Runtime", ".NET Framework 4.8", "Nền tảng chạy ứng dụng web"],
            ["ORM", "Entity Framework 6", "Ánh xạ bảng dữ liệu sang model C#"],
            ["CSDL", "SQL Server LocalDB", "Lưu người dùng, sách, đơn hàng, mượn/trả và log"],
            ["Frontend", "Razor, HTML, CSS, JavaScript", "Hiển thị giao diện người dùng và quản trị"],
            ["UI", "Bootstrap, jQuery, jQuery Validation", "Hỗ trợ bố cục, tương tác và validate dữ liệu"],
            ["Phân trang", "X.PagedList", "Phân trang danh sách sản phẩm, hóa đơn và log"],
            ["Mail", "Gmail SMTP/API", "Gửi thông báo trạng thái mượn/trả"],
        ]
    )
    caption(doc, "Bảng 2.1. Công nghệ sử dụng phía website ASP.NET MVC")

    doc.heading("2.2. Công nghệ phía Flask Face API/OCR/chatbox", 2)
    doc.table(
        [
            ["Thành phần", "Công nghệ", "Vai trò"],
            ["API server", "Flask 3", "Cung cấp endpoint `/api/face/*` và `/api/chatbox/*`"],
            ["Nhận diện khuôn mặt", "InsightFace, ONNXRuntime", "Trích xuất embedding và so khớp khuôn mặt"],
            ["Kiểm tra hành động", "MediaPipe Face Landmarker", "Phát hiện quay trái/phải, nhìn lên/xuống, mở miệng, cười"],
            ["Xử lý ảnh", "OpenCV, NumPy, scikit-image", "Đọc ảnh, kiểm tra chất lượng và tính toán chỉ số ảnh"],
            ["OCR", "PaddleOCR, pytesseract/Tesseract", "Đọc thông tin CMND/CCCD"],
            ["Lưu mẫu mặt", "`face_db.pkl`", "Lưu embedding khuôn mặt theo user"],
            ["Chatbox", "Flask blueprint, JSON knowledge base", "Tư vấn sách, giá, tồn kho và hướng dẫn mượn"],
            ["Kết nối dữ liệu", "pyodbc", "Đọc dữ liệu sản phẩm để huấn luyện chatbox"],
        ]
    )
    caption(doc, "Bảng 2.2. Công nghệ sử dụng phía Flask Face API/OCR/chatbox")

    doc.heading("2.3. Nhận diện khuôn mặt và xác thực", 2)
    p_many(
        doc,
        [
            "Nhận diện khuôn mặt trong đề tài được triển khai theo hướng so khớp 1:1. Khi đăng ký, Flask phát hiện khuôn mặt, trích xuất embedding và lưu theo `user_id`. Khi xác thực, ảnh mới được trích xuất embedding và so khớp với embedding đã đăng ký. Kết quả trả về gồm `success`, `confidence`, `request_id`, `user_id` và các mã lỗi nếu có.",
            "Website ASP.NET MVC vẫn áp dụng ngưỡng riêng `FaceAuthMinConfidence=0.75`. Nhờ vậy, Flask có thể thay đổi mô hình hoặc cách tính điểm, còn website vẫn giữ một quy tắc chấp nhận thống nhất ở tầng nghiệp vụ.",
        ],
    )
    doc.heading("2.4. OCR CMND/CCCD", 2)
    p_many(
        doc,
        [
            "OCR CMND/CCCD giúp người dùng cập nhật hồ sơ định danh nhanh hơn. Server Flask nhận ảnh mặt trước/mặt sau, kiểm tra định dạng ảnh, dùng PaddleOCR hoặc Tesseract để đọc text, sau đó parse các trường như số giấy tờ, họ tên, ngày sinh, địa chỉ, ngày cấp và nơi cấp.",
            "Khi ảnh giấy tờ có khuôn mặt, hệ thống có thể so khớp khuôn mặt trên giấy tờ với mẫu khuôn mặt đã đăng ký để tăng độ tin cậy. Nếu ảnh mờ, sai giấy tờ hoặc thiếu thông tin, hệ thống trả mã lỗi để website hiển thị hướng dẫn cho người dùng.",
        ],
    )
    doc.heading("2.5. Gmail và chatbox", 2)
    p_many(
        doc,
        [
            "Gmail được dùng để thông báo trạng thái mượn/trả sách cho người dùng. Các sự kiện chính gồm tạo yêu cầu mượn, duyệt mượn, từ chối, hủy, trả sách và quá hạn. Lỗi gửi mail được ghi log để quản trị viên kiểm tra cấu hình SMTP hoặc app password.",
            "Chatbox được nhúng qua `ChatboxWidgetUrl` và gọi API `/api/chatbox/ask`. Module chatbox có thể huấn luyện từ database sản phẩm qua `/api/chatbox/train`, lưu tri thức vào `chatbox_knowledge.json` và ghi lịch sử hội thoại vào `chatbox_history.md`.",
        ],
    )
    page_break(doc)


def add_chapter_3(doc):
    doc.heading("CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 1)
    doc.heading("3.1. Tác nhân hệ thống", 2)
    doc.table(
        [
            ["Tác nhân", "Vai trò"],
            ["Khách vãng lai", "Xem trang chủ, danh mục, tìm kiếm và xem chi tiết sách"],
            ["Người dùng", "Đăng ký, đăng nhập, cập nhật hồ sơ, OCR CMND/CCCD, xác thực khuôn mặt, mượn sách"],
            ["Quản trị viên", "Quản lý sách, người dùng, đơn hàng, tồn kho, duyệt/trả sách và xem log"],
            ["Face API/OCR", "Đăng ký khuôn mặt, xác thực, kiểm tra hành động và OCR giấy tờ"],
            ["Gmail SMTP/API", "Gửi thông báo trạng thái mượn/trả"],
            ["Chatbox", "Tư vấn sách, giá, tồn kho và hướng dẫn mượn"],
        ]
    )
    caption(doc, "Bảng 3.1. Tác nhân và vai trò")

    doc.heading("3.2. Use case tổng quát", 2)
    p_many(
        doc,
        [
            "Các use case chính của hệ thống gồm xem/tìm kiếm sách, đăng ký/đăng nhập, cập nhật hồ sơ CMND/CCCD, đăng ký mẫu khuôn mặt, xác thực khuôn mặt, gửi yêu cầu mượn, theo dõi lịch sử mượn, admin duyệt/từ chối/trả sách, gửi Gmail thông báo, chatbox tư vấn và xem nhật ký hệ thống.",
        ],
    )
    doc.image(ASSETS / "usecase_quan_ly_nha_sach.png", "Hình 3.1. Sơ đồ use case tổng quát của hệ thống")

    doc.heading("3.3. Ràng buộc nghiệp vụ", 2)
    bullets(
        doc,
        [
            "Người dùng phải đăng nhập trước khi gửi yêu cầu mượn sách.",
            "Người dùng phải có Gmail nhận thông báo, họ tên và thông tin CMND/CCCD.",
            "Người dùng phải xác thực khuôn mặt thành công trước khi gửi yêu cầu mượn.",
            "Token xác thực khuôn mặt khi mượn chỉ có hạn 3 phút và gắn với đúng user/sản phẩm.",
            "Không cho mượn nếu sách hết tồn kho hoặc người dùng đang có yêu cầu còn hiệu lực với cùng sách.",
            "Khi admin duyệt mượn, hệ thống giảm tồn kho; khi xác nhận trả sách, hệ thống tăng tồn kho.",
            "Mọi thao tác mượn/trả, xác thực và gửi thông báo cần được ghi log.",
        ],
    )

    doc.heading("3.4. Thiết kế dữ liệu chính", 2)
    doc.table(
        [
            ["Bảng/model", "Vai trò"],
            ["Users", "Lưu tài khoản, hồ sơ người dùng, thông tin liên hệ và định danh"],
            ["Sanphams", "Lưu thông tin sách/sản phẩm, giá, hình ảnh, danh mục và tồn kho"],
            ["Orders, Order_Detail", "Lưu đơn hàng và chi tiết đơn hàng"],
            ["RentalRequests", "Lưu yêu cầu mượn, trạng thái, số lượng, ngày mượn, hạn trả và ngày trả thực tế"],
            ["RentalLogs", "Lưu lịch sử thao tác mượn/trả như Request, Cancel, Approve, Return, Overdue"],
            ["FaceAuthLogs", "Lưu lịch sử đăng ký/xác thực khuôn mặt, confidence, request_id, lỗi"],
            ["GeofenceLogs", "Lưu log kiểm tra vị trí cửa hàng nếu dùng chức năng geofence"],
            ["ProductReviews", "Lưu đánh giá và file review sản phẩm"],
            ["ProductFavorites", "Lưu sách yêu thích của người dùng"],
            ["StoreLocations", "Lưu vị trí cửa hàng"],
        ]
    )
    caption(doc, "Bảng 3.2. Mô tả bảng dữ liệu chính")

    doc.heading("3.5. Quy trình xử lý", 2)
    doc.image(ASSETS / "workflow_muon_sach.png", "Hình 3.2. Quy trình người dùng gửi yêu cầu mượn sách")
    doc.image(ASSETS / "workflow_ocr_face.png", "Hình 3.3. Quy trình OCR CMND/CCCD và xác thực khuôn mặt")
    doc.image(ASSETS / "workflow_admin.png", "Hình 3.4. Quy trình admin xử lý mượn/trả sách")

    doc.heading("3.6. Luồng xác thực khuôn mặt khi mượn sách", 2)
    numbered(
        doc,
        [
            "Người dùng chọn sách, số lượng và số ngày mượn.",
            "Website kiểm tra tồn kho, hồ sơ định danh và yêu cầu mượn đang còn hiệu lực.",
            "Website yêu cầu người dùng thực hiện action challenge như quay trái, quay phải, mở miệng hoặc cười.",
            "MVC gửi frame webcam sang `/api/face/action-check`.",
            "Khi `action_matched=true`, MVC gọi `/api/face/verify` để so khớp khuôn mặt.",
            "Nếu `confidence >= 0.75`, MVC sinh `faceToken` có hạn 3 phút.",
            "Người dùng gửi yêu cầu mượn kèm `faceToken`; server xác thực token rồi tạo `RentalRequests` trạng thái `Pending`.",
        ],
    )
    page_break(doc)


def add_chapter_4(doc):
    doc.heading("CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG", 1)
    doc.heading("4.1. Cấu trúc source", 2)
    doc.table(
        [
            ["Thư mục/file", "Nội dung triển khai"],
            ["DongTrieuBookStore.sln", "Solution chính của website quản lý nhà sách"],
            ["BaiTapLon", "Project ASP.NET MVC, controller, view, cấu hình Web.config"],
            ["Mood", "Entity Framework model và lớp Draw truy xuất dữ liệu"],
            ["Common", "Repository ghi log xác thực, geofence và mượn/trả"],
            ["CommomSentMail", "Helper gửi Gmail SMTP"],
            ["sql/create_database.sql", "Script tạo/bổ sung bảng dữ liệu"],
            ["report_assets", "Sơ đồ use case, workflow và ảnh chụp giao diện"],
            ["NHANDIENKHUONMAT-new07040226/app.py", "Flask Face API, OCR và chatbox"],
            ["NHANDIENKHUONMAT-new07040226/sales_chatbox", "Module chatbox tư vấn sách"],
        ]
    )
    caption(doc, "Bảng 4.1. Cấu trúc source")

    doc.heading("4.2. Controller và service chính", 2)
    doc.table(
        [
            ["Thành phần", "Chức năng"],
            ["HomeController", "Trang chủ, slider, danh mục và dữ liệu hiển thị công khai"],
            ["UsersController", "Đăng ký, đăng nhập, hồ sơ người dùng, đăng nhập Facebook, đăng ký khuôn mặt"],
            ["ProductController", "Danh sách sách, tìm kiếm, chi tiết sách, đánh giá và file review"],
            ["RentalController", "Tạo yêu cầu mượn, hủy, admin duyệt/từ chối/trả/quá hạn"],
            ["FaceAuthController", "Nhận ảnh upload, gọi Flask, OCR, action challenge, xác thực và sinh token mượn"],
            ["LogsController", "Xem log xác thực, geofence và mượn/trả"],
            ["CartController", "Giỏ hàng, đặt hàng, thanh toán và hóa đơn"],
            ["GmailNotificationService", "Gửi Gmail theo trạng thái mượn/trả và ghi lỗi gửi mail"],
            ["FaceAuthApiClient", "Gọi HTTP multipart/form-data sang Flask Face API"],
            ["FaceRentalTokenService", "Quản lý token xác thực khuôn mặt khi mượn sách"],
            ["StoreLocationService", "Xử lý dữ liệu vị trí cửa hàng"],
        ]
    )
    caption(doc, "Bảng 4.2. Controller/service chính")

    doc.heading("4.3. Cấu hình tích hợp", 2)
    doc.table(
        [
            ["Key", "Giá trị", "Ý nghĩa"],
            ["FaceAuthAPI", "http://localhost:8000/api/face", "Base URL Flask Face API"],
            ["ChatboxWidgetUrl", "http://localhost:8000/api/chatbox/widget.js", "Script nhúng chatbox vào website"],
            ["FaceAuthMinConfidence", "0.75", "Ngưỡng xác thực khuôn mặt phía ASP.NET"],
            ["FaceAuthRentalTokenMinutes", "3", "Thời hạn token xác thực khuôn mặt khi mượn"],
            ["RentalMaxBorrowDays", "30", "Số ngày mượn tối đa"],
            ["GmailNotificationsEnabled", "true", "Bật gửi Gmail thông báo"],
        ]
    )
    caption(doc, "Bảng 4.3. Cấu hình tích hợp trong Web.config")

    doc.heading("4.4. Endpoint Flask", 2)
    doc.table(
        [
            ["Endpoint", "Method", "Chức năng"],
            ["/api/face/health", "GET", "Kiểm tra Flask, model nhận diện, OCR, action model và chatbox"],
            ["/api/face/register", "POST", "Đăng ký/cập nhật mẫu khuôn mặt cho user"],
            ["/api/face/verify", "POST", "Xác thực khuôn mặt 1:1 theo user"],
            ["/api/face/authenticate", "POST", "Xác thực khuôn mặt cho luồng MFA"],
            ["/api/face/action-check", "POST", "Kiểm tra hành động khuôn mặt"],
            ["/api/face/ocr-cmnd", "POST", "OCR CMND/CCCD mặt trước/mặt sau"],
            ["/api/chatbox/health", "GET", "Kiểm tra trạng thái chatbox"],
            ["/api/chatbox/train", "POST", "Huấn luyện knowledge base từ database sản phẩm"],
            ["/api/chatbox/ask", "POST", "Trả lời câu hỏi tư vấn sách"],
            ["/api/chatbox/widget.js", "GET", "Script nhúng widget chatbox"],
        ]
    )
    caption(doc, "Bảng 4.4. Endpoint Flask và chức năng")

    doc.heading("4.5. Triển khai Face API và OCR", 2)
    p_many(
        doc,
        [
            "Flask server trong `app.py` nhận file ảnh qua `multipart/form-data`, kiểm tra định dạng `.jpg`, `.jpeg`, `.png`, giới hạn dung lượng 5 MB và decode ảnh bằng OpenCV. Với luồng đăng ký/xác thực, server dùng InsightFace để phát hiện đúng một khuôn mặt, kiểm tra chất lượng ảnh và trích xuất embedding.",
            "Với endpoint `/api/face/action-check`, server dùng MediaPipe Face Landmarker để lấy landmark khuôn mặt, tính các chỉ số như yaw, pitch, nose offset, mouth open ratio và smile ratio. Từ đó server xác định người dùng đã thực hiện đúng hành động được yêu cầu hay chưa.",
            "Với endpoint OCR, server đọc ảnh CMND/CCCD bằng PaddleOCR hoặc Tesseract, parse text thành các trường định danh. Kết quả trả về ở dạng JSON để `FaceAuthController` cập nhật hồ sơ người dùng hoặc hiển thị lỗi phù hợp.",
        ],
    )

    doc.heading("4.6. Triển khai quy trình mượn/trả", 2)
    p_many(
        doc,
        [
            "`RentalController` chịu trách nhiệm lấy danh sách yêu cầu mượn, tạo yêu cầu mới, hủy yêu cầu, cập nhật trạng thái bởi admin và ghi log. Khi người dùng gửi yêu cầu mượn, controller kiểm tra user, sản phẩm, số ngày mượn, tồn kho, hồ sơ định danh và token xác thực khuôn mặt.",
            "Khi admin duyệt yêu cầu, trạng thái chuyển sang `Borrowing` và tồn kho giảm. Khi xác nhận trả sách, trạng thái chuyển sang `Returned`, ngày trả thực tế được lưu và tồn kho tăng. Các trạng thái như `Pending`, `Rejected`, `Cancelled`, `Overdue` giúp quản trị viên theo dõi vòng đời yêu cầu rõ ràng.",
        ],
    )

    doc.heading("4.7. Ảnh giao diện", 2)
    doc.image(ASSETS / "screenshot_home.png", "Hình 4.1. Trang chủ hệ thống quản lý nhà sách")
    doc.image(ASSETS / "screenshot_product_list.png", "Hình 4.2. Màn hình danh sách sản phẩm sách")
    doc.image(ASSETS / "screenshot_login.png", "Hình 4.3. Màn hình đăng nhập hệ thống")
    doc.image(ASSETS / "screenshot_rentals.png", "Hình 4.4. Màn hình danh sách mượn/trả sách")
    doc.p("Một số màn hình yêu cầu phiên đăng nhập hoặc camera thật như OCR CMND/CCCD, action challenge khuôn mặt và chatbox cần chụp bổ sung khi chạy đủ website, Flask server và tài khoản kiểm thử.")
    page_break(doc)


def add_chapter_5(doc):
    doc.heading("CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ", 1)
    doc.heading("5.1. Môi trường kiểm thử", 2)
    bullets(
        doc,
        [
            "Hệ điều hành Windows, chạy project ASP.NET MVC bằng Visual Studio/MSBuild phù hợp WebApplication targets.",
            "SQL Server LocalDB hoặc SQL Server tương thích với database `QLNhaSach`.",
            "Flask server chạy tại `http://localhost:8000`, base API `http://localhost:8000/api/face`.",
            "Các dependency Flask gồm Flask, insightface, onnxruntime, mediapipe, opencv-python, paddleocr, pytesseract, pyodbc, scikit-image.",
            "Trình duyệt có quyền webcam để kiểm thử đăng ký/xác thực khuôn mặt.",
        ],
    )

    doc.heading("5.2. Kịch bản kiểm thử", 2)
    doc.table(
        [
            ["Nhóm", "Trường hợp kiểm thử", "Kết quả mong đợi"],
            ["Tài khoản", "Đăng ký hợp lệ, trùng email, đăng nhập đúng/sai", "Tạo tài khoản đúng, báo lỗi rõ khi sai"],
            ["Hồ sơ", "Cập nhật Gmail, số CMND/CCCD, họ tên", "Lưu hồ sơ và dùng được trong mượn sách"],
            ["OCR", "Ảnh rõ, ảnh mờ, thiếu mặt trước/mặt sau, ảnh sai giấy tờ", "Đọc được khi ảnh hợp lệ, trả lỗi khi không hợp lệ"],
            ["Khuôn mặt", "Đăng ký mẫu, xác thực đúng/sai user, nhiều khuôn mặt", "Confidence đúng ngưỡng, có mã lỗi phù hợp"],
            ["Action check", "Quay trái/phải, nhìn lên/xuống, mở miệng, cười", "Chỉ cho qua khi `action_matched=true`"],
            ["Mượn sách", "Còn tồn, hết tồn, thiếu hồ sơ, chưa xác thực, quá số ngày mượn", "Chỉ tạo yêu cầu hợp lệ trạng thái Pending"],
            ["Admin", "Duyệt, từ chối, hủy, trả sách, quá hạn", "Cập nhật trạng thái, tồn kho và log đúng"],
            ["Gmail", "Cấu hình đúng, sai app password, tắt thông báo", "Gửi mail hoặc ghi lỗi rõ ràng"],
            ["Chatbox", "Hỏi tên sách, giá, tồn kho, hướng dẫn mượn", "Trả lời và gợi ý sách nếu có dữ liệu"],
            ["Log", "Xác thực, mượn/trả, lỗi gửi mail", "Ghi vào FaceAuthLogs/RentalLogs"],
        ]
    )
    caption(doc, "Bảng 5.1. Kịch bản kiểm thử")

    doc.heading("5.3. Tiêu chí nghiệm thu", 2)
    bullets(
        doc,
        [
            "Website hiển thị được trang chủ, danh sách sách, chi tiết sách, đăng nhập và các màn hình quản trị cần thiết.",
            "Flask `/api/face/health` trả `status=ok` và phản ánh trạng thái model/OCR/chatbox.",
            "Người dùng không thể gửi yêu cầu mượn nếu chưa xác thực khuôn mặt hoặc thiếu hồ sơ định danh.",
            "Tồn kho thay đổi đúng khi admin duyệt mượn và xác nhận trả sách.",
            "Gmail thông báo được gửi khi cấu hình đúng hoặc ghi log lỗi khi cấu hình sai.",
            "Chatbox hiển thị qua widget và trả lời được các câu hỏi phổ biến về sách.",
            "Báo cáo có đủ chương, bảng, hình, phụ lục và không còn lỗi font tiếng Việt.",
        ],
    )

    doc.heading("5.4. Đánh giá kết quả", 2)
    p_many(
        doc,
        [
            "Hệ thống đáp ứng được mục tiêu kết hợp quản lý nhà sách với xác thực khuôn mặt và OCR hồ sơ định danh trong quy trình mượn/trả. Việc tách Flask Face API thành dịch vụ riêng giúp website ASP.NET MVC dễ tích hợp, dễ thay đổi mô hình nhận diện/OCR mà không ảnh hưởng nhiều đến nghiệp vụ web.",
            "Các bảng log như `FaceAuthLogs` và `RentalLogs` giúp truy vết quá trình xác thực, gửi yêu cầu mượn, duyệt, trả sách và lỗi phát sinh. Chatbox bổ sung kênh hỗ trợ người dùng khi tìm sách hoặc hỏi hướng dẫn mượn.",
        ],
    )
    doc.heading("5.5. Hạn chế và hướng khắc phục", 2)
    doc.table(
        [
            ["Hạn chế/rủi ro", "Ảnh hưởng", "Hướng xử lý"],
            ["Ảnh khuôn mặt kém sáng hoặc nhiều người", "Xác thực thất bại", "Hướng dẫn chụp lại, kiểm tra một khuôn mặt, dùng ngưỡng confidence"],
            ["OCR phụ thuộc chất lượng ảnh", "Hồ sơ định danh thiếu/sai", "Cho phép chỉnh tay và kiểm tra chất lượng ảnh"],
            ["Gmail phụ thuộc app password", "Không gửi được thông báo", "Ghi log SMTP và hướng dẫn cấu hình"],
            ["Flask phải chạy song song", "Website không xác thực/OCR được nếu API tắt", "Kiểm tra health và hiển thị lỗi rõ"],
            ["Chatbox phụ thuộc knowledge base", "Tư vấn chưa đủ dữ liệu", "Huấn luyện lại từ database sản phẩm"],
        ]
    )
    caption(doc, "Bảng 5.2. Rủi ro và phương án xử lý")
    page_break(doc)


def add_closing(doc):
    doc.heading("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 1)
    p_many(
        doc,
        [
            "Đề tài đã hoàn thiện báo cáo cho hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn/trả sách. Báo cáo đã trình bày lý do chọn đề tài, công nghệ sử dụng, phân tích thiết kế, triển khai theo source thực tế, kiểm thử và đánh giá.",
            "Điểm nổi bật của hệ thống là kết hợp website ASP.NET MVC với Flask Face API để xử lý đăng ký/xác thực khuôn mặt, OCR CMND/CCCD, kiểm tra hành động chống thao tác sai quy trình, gửi Gmail thông báo và tích hợp chatbox tư vấn sách.",
            "Hướng phát triển tiếp theo gồm tối ưu OCR trong nhiều điều kiện ánh sáng, bổ sung dashboard thống kê mượn/trả, hoàn thiện phân quyền chi tiết, triển khai production cho Flask API, tăng bảo mật lưu trữ embedding và nâng cấp chatbox theo dữ liệu thực tế của nhà sách.",
        ],
    )
    page_break(doc)

    doc.heading("TÀI LIỆU THAM KHẢO", 1)
    bullets(
        doc,
        [
            "Tài liệu ASP.NET MVC 5 và Entity Framework 6.",
            "Tài liệu Flask framework.",
            "Tài liệu InsightFace, ONNXRuntime, MediaPipe, PaddleOCR và Tesseract OCR.",
            "Source code dự án `QLNhaSach` trong workspace.",
            "Source Flask `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226`.",
            "`Template.pdf`, `QuyTrinhVietBaoCao.md`, `FACE_AUTH_FLASK_API_REQUIREMENTS.md` và các file trong `report_assets`.",
        ],
    )
    page_break(doc)

    doc.heading("PHỤ LỤC", 1)
    doc.heading("Phụ lục A. Hướng dẫn chạy website ASP.NET MVC", 2)
    numbered(
        doc,
        [
            "Mở solution `DongTrieuBookStore.sln` bằng Visual Studio.",
            "Khôi phục NuGet package nếu thiếu.",
            "Tạo database bằng `sql/create_database.sql` và các migration trong `sql/migrations` nếu cần.",
            "Kiểm tra các key cấu hình trong `BaiTapLon/Web.config`.",
            "Chạy project `BaiTapLon` và kiểm tra trang chủ, đăng nhập, sản phẩm, mượn/trả.",
        ],
    )

    doc.heading("Phụ lục B. Hướng dẫn chạy Flask server", 2)
    numbered(
        doc,
        [
            "Mở terminal tại `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226`.",
            "Cài dependency bằng `pip install -r requirements.txt` nếu môi trường mới.",
            "Chạy `python app.py`.",
            "Mở `http://localhost:8000/api/face/health` để kiểm tra trạng thái.",
            "Nếu camera/browser bị mirror trái/phải, đặt `FACE_ACTION_FLIP_HORIZONTAL=true` trước khi chạy server.",
        ],
    )

    doc.heading("Phụ lục C. Contract Face API", 2)
    doc.table(
        [
            ["Field", "Ý nghĩa"],
            ["file", "Ảnh khuôn mặt hoặc ảnh CMND/CCCD gửi bằng multipart/form-data"],
            ["user_id/userId", "ID người dùng trong hệ thống ASP.NET MVC"],
            ["purpose", "Ngữ cảnh Register, Verify, MFA, Login hoặc Rental"],
            ["action_code/actionCode", "Mã hành động dùng cho `/api/face/action-check`"],
            ["success/matched", "Kết quả xử lý hoặc so khớp"],
            ["confidence/quality_score", "Điểm tin cậy 0.0 đến 1.0"],
            ["request_id/requestId", "Mã trace cho mỗi request"],
            ["error_code/error_message", "Mã lỗi và mô tả lỗi nếu thất bại"],
        ]
    )

    doc.heading("Phụ lục D. File sinh kèm báo cáo", 2)
    bullets(
        doc,
        [
            "`report_assets/usecase_quan_ly_nha_sach.drawio`",
            "`report_assets/usecase_quan_ly_nha_sach.png`",
            "`report_assets/workflow_muon_sach.png`",
            "`report_assets/workflow_ocr_face.png`",
            "`report_assets/workflow_admin.png`",
            "`LichSuQuaTrinhVietBaoCao.md`",
            "`scripts/rebuild_baocao_docx.py`",
        ],
    )


def validate_docx(path):
    with zipfile.ZipFile(path, "r") as zip_file:
        names = set(zip_file.namelist())
        required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
        missing = required - names
        if missing:
            raise RuntimeError(f"Missing DOCX parts: {missing}")
        xml = zip_file.read("word/document.xml")
        ET.fromstring(xml)
        return len(xml)


def build_full_report():
    ensure_assets()
    doc = Docx()
    add_front_matter(doc)
    add_chapter_1(doc)
    add_chapter_2(doc)
    add_chapter_3(doc)
    add_chapter_4(doc)
    add_chapter_5(doc)
    add_closing(doc)

    outputs = [
        ROOT / "BaoCao.docx",
        FLASK_ROOT / "BaoCao.docx",
    ]
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output)
        size = validate_docx(output)
        print(f"{output} ({size} bytes document.xml)")

    long_name = ROOT / "BaoCao_QuanLyNhaSach_NhanDienKhuonMat_LeVietThang_2224802010263.docx"
    copied_long_name = False
    try:
        shutil.copy2(outputs[0], long_name)
        validate_docx(long_name)
        copied_long_name = True
        print(long_name)
    except PermissionError:
        print(f"SKIP locked file: {long_name}")

    log(
        "- Đã đọc kế hoạch trong `QuyTrinhVietBaoCao.md` và dựng lại full file `BaoCao.docx`.\n"
        "- Đã xuất đồng thời `D:\\BACKUP_2004_2026_D\\QLNhaSach\\BaoCao.docx` và "
        "`D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226\\BaoCao.docx`.\n"
        "- Nội dung đã bổ sung đủ phần đầu báo cáo, chương 1-5, kết luận, tài liệu tham khảo, phụ lục, bảng công nghệ, bảng endpoint, bảng kiểm thử và hình trong `report_assets`.\n"
        + (
            "- Đã cập nhật thêm file tên dài của báo cáo.\n"
            if copied_long_name
            else "- Bỏ qua cập nhật file tên dài vì Windows đang khóa file đó; hai file `BaoCao.docx` đã được cập nhật.\n"
        )
    )


if __name__ == "__main__":
    build_full_report()
