# -*- coding: utf-8 -*-
from pathlib import Path
import datetime
import html
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "report_assets"
OUTPUT = ROOT / "BaoCaoMauSua.docx"
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
        ["Đăng nhập", "Cập nhật hồ sơ", "Chọn sách", "Xác thực mặt", "Gửi yêu cầu", "Admin duyệt", "Gmail thông báo"],
    )
    make_flow(
        ASSETS / "workflow_ocr_face.png",
        "Quy trình OCR CMND/CCCD và xác thực khuôn mặt",
        ["Tải ảnh giấy tờ", "Gọi Flask", "OCR", "Parse thông tin", "So khớp khuôn mặt", "Cập nhật hồ sơ"],
    )
    make_flow(
        ASSETS / "workflow_admin.png",
        "Quy trình admin xử lý mượn trả",
        ["Xem yêu cầu", "Kiểm tra hồ sơ", "Duyệt/từ chối", "Cập nhật tồn", "Xác nhận trả", "Ghi log"],
    )


def bullets(doc, items):
    for item in items:
        doc.bullet(item)


def numbered(doc, items):
    for index, item in enumerate(items, start=1):
        doc.p(f"{index}. {item}")


def para(doc, *items):
    for item in items:
        doc.p(item)


def page(doc, title=None, paragraphs=None, bullets_list=None, table=None, image=None, caption=None, break_after=True):
    if title:
        doc.heading(title, 1 if re.match(r"^(CHƯƠNG|KẾT LUẬN|TÀI LIỆU|PHỤ LỤC|LỜI|DANH MỤC|MỤC LỤC)", title) else 2)
    if paragraphs:
        para(doc, *paragraphs)
    if bullets_list:
        bullets(doc, bullets_list)
    if table:
        doc.table(table)
    if image:
        doc.image(image, caption or "", width_px=560)
    if break_after:
        doc.page_break()


def add_cover_pages(doc):
    doc.p("BỘ CÔNG THƯƠNG", align="center", bold=True, size=26)
    doc.p("TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI", align="center", bold=True, size=26)
    doc.p("---------------------------------------", align="center")
    doc.p("")
    doc.p("ĐỒ ÁN TỐT NGHIỆP", align="center", bold=True, size=34)
    doc.p("NGÀNH KỸ THUẬT PHẦN MỀM", align="center", bold=True, size=28)
    doc.p("")
    doc.p("QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH", align="center", bold=True, size=32)
    doc.p("")
    doc.p("CBHD: ........................................", align="center", size=24)
    doc.p("Sinh viên: Lê Việt Thắng", align="center", bold=True, size=24)
    doc.p("Mã số sinh viên: 2224802010263", align="center", bold=True, size=24)
    doc.p("")
    doc.p("Hà Nội - Năm 2026", align="center", bold=True, size=24)
    doc.page_break()

    doc.p("BỘ CÔNG THƯƠNG", align="center", bold=True, size=26)
    doc.p("TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI", align="center", bold=True, size=26)
    doc.p("---------------------------------------", align="center")
    doc.p("")
    doc.p("ĐỒ ÁN TỐT NGHIỆP ĐẠI HỌC", align="center", bold=True, size=34)
    doc.p("NGÀNH KỸ THUẬT PHẦN MỀM", align="center", bold=True, size=28)
    doc.p("")
    doc.p("QUẢN LÝ NHÀ SÁCH TÍCH HỢP NHẬN DIỆN KHUÔN MẶT ĐỂ MƯỢN TRẢ SÁCH", align="center", bold=True, size=32)
    doc.p("")
    doc.p("CBHD: ........................................", align="center")
    doc.p("Sinh viên: Lê Việt Thắng", align="center")
    doc.p("Mã số sinh viên: 2224802010263", align="center")
    doc.p("")
    doc.p("Hà Nội - Năm 2026", align="center", bold=True)
    doc.page_break()


def build_report():
    ensure_assets()
    doc = Docx()

    add_cover_pages(doc)

    page(
        doc,
        "PHIẾU GIAO ĐỀ TÀI",
        [
            "Trang này đặt phiếu giao đề tài hoặc nhiệm vụ đồ án theo mẫu của khoa.",
            "Tên đề tài: Quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn trả sách.",
            "Sản phẩm: website quản lý nhà sách, module mượn/trả, Face API, OCR CMND/CCCD, Gmail thông báo và chatbox tư vấn sách.",
            "Ghi chú: Báo cáo được chuẩn hóa theo cấu trúc mẫu `BaoCaoMauSua.docx` và nội dung kế hoạch trong `QuyTrinhVietBaoCao.md`.",
        ],
    )

    page(
        doc,
        "LỜI NÓI ĐẦU",
        [
            "Lời đầu tiên em xin chân thành cảm ơn quý thầy cô trong khoa công nghệ thông tin đã hỗ trợ em trong quá trình học tập, rèn luyện và thực hiện đề tài. Em xin gửi lời cảm ơn đến giảng viên hướng dẫn đã góp ý, định hướng và giúp em hoàn thiện báo cáo.",
            "Thông qua đề tài này, em có cơ hội vận dụng kiến thức về ASP.NET MVC, Entity Framework, SQL Server, Flask API, nhận diện khuôn mặt, OCR và gửi email thông báo vào một hệ thống có quy trình nghiệp vụ cụ thể. Báo cáo tập trung vào hệ thống quản lý nhà sách có bổ sung quy trình mượn/trả sách an toàn hơn nhờ xác thực khuôn mặt và hồ sơ định danh.",
            "Em xin chân thành cảm ơn!",
        ],
    )

    page(
        doc,
        "DANH MỤC CÁC TỪ VIẾT TẮT",
        table=[
            ["Từ viết tắt", "Ý nghĩa"],
            ["CSDL", "Cơ sở dữ liệu"],
            ["SQL", "Structured Query Language"],
            ["MVC", "Model - View - Controller"],
            ["API", "Application Programming Interface"],
            ["OCR", "Optical Character Recognition"],
            ["CMND/CCCD", "Chứng minh nhân dân/Căn cước công dân"],
            ["SMTP", "Simple Mail Transfer Protocol"],
            ["MFA", "Multi-factor Authentication"],
        ],
    )

    page(
        doc,
        "DANH MỤC CÁC HÌNH ẢNH",
        bullets_list=[
            "Hình 2-1. Biểu đồ use case tổng quát.",
            "Hình 2-2. Quy trình người dùng gửi yêu cầu mượn sách.",
            "Hình 2-3. Quy trình OCR CMND/CCCD và xác thực khuôn mặt.",
            "Hình 2-4. Quy trình admin xử lý mượn/trả sách.",
            "Hình 5-1. Trang chủ hệ thống quản lý nhà sách.",
            "Hình 5-2. Màn hình danh sách sản phẩm sách.",
            "Hình 5-3. Màn hình đăng nhập.",
            "Hình 5-4. Màn hình danh sách mượn/trả.",
        ],
    )

    page(
        doc,
        "MỤC LỤC",
        bullets_list=[
            "CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG",
            "CHƯƠNG 2. PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG CỦA HỆ THỐNG",
            "CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU",
            "CHƯƠNG 4. THIẾT KẾ CÁC CHỨC NĂNG CỦA HỆ THỐNG",
            "CHƯƠNG 5. THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT",
            "CHƯƠNG 6. KIỂM THỬ HỆ THỐNG",
            "CHƯƠNG 7. TỔNG KẾT VÀ ĐÁNH GIÁ",
            "TÀI LIỆU THAM KHẢO",
        ],
    )

    page(
        doc,
        "CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG",
        [
            "Chương này mô tả bối cảnh, mục tiêu, phạm vi và nhóm yêu cầu chính của hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn/trả sách.",
            "Hệ thống không chỉ phục vụ bán sách mà còn bổ sung quy trình mượn/trả có kiểm tra hồ sơ định danh, xác thực khuôn mặt, giới hạn số ngày mượn, gửi Gmail thông báo và ghi log nghiệp vụ.",
        ],
        break_after=False,
    )

    page(
        doc,
        "1.1. Mục tiêu và phạm vi hệ thống",
        [
            "Mục tiêu chính là xây dựng website quản lý nhà sách trên nền tảng ASP.NET MVC, sử dụng Entity Framework và SQL Server để lưu dữ liệu. Hệ thống tích hợp Flask Face API để nhận diện khuôn mặt, OCR CMND/CCCD và chatbox tư vấn sách.",
            "Phạm vi source gồm thư mục `QLNhaSach` cho website và thư mục `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226` cho server Flask. Báo cáo mô tả ở mức phân tích, thiết kế, triển khai và kiểm thử, không đi sâu huấn luyện mô hình AI từ đầu.",
        ],
        bullets_list=[
            "Quản lý người dùng, sách, danh mục, đơn hàng, kho, đánh giá và yêu thích.",
            "Quản lý yêu cầu mượn/trả sách, trạng thái, ngày mượn, hạn trả và tồn kho.",
            "Xác thực người mượn bằng khuôn mặt trước khi tạo yêu cầu.",
            "OCR CMND/CCCD để chuẩn hóa hồ sơ định danh.",
            "Gửi Gmail thông báo và hỗ trợ chatbox tư vấn sách.",
        ],
    )

    page(
        doc,
        "1.2. Yêu cầu chức năng phía người dùng",
        bullets_list=[
            "Đăng ký tài khoản với thông tin cá nhân, email, số điện thoại và địa chỉ.",
            "Đăng nhập bằng tài khoản; có thể kết hợp MFA hoặc xác thực khuôn mặt theo luồng cấu hình.",
            "Cập nhật hồ sơ, Gmail nhận thông báo và thông tin CMND/CCCD.",
            "Tải ảnh giấy tờ để hệ thống OCR và gợi ý thông tin định danh.",
            "Đăng ký mẫu khuôn mặt và xác thực khuôn mặt trước khi mượn sách.",
            "Xem danh sách sách, tìm kiếm, xem chi tiết, đánh giá, yêu thích và đặt hàng.",
            "Gửi yêu cầu mượn sách, theo dõi lịch sử mượn và hủy yêu cầu đang chờ duyệt.",
        ],
    )

    page(
        doc,
        "1.3. Yêu cầu chức năng phía quản trị viên",
        bullets_list=[
            "Quản lý sản phẩm sách, danh mục, nhà cung cấp, nhập hàng, kho và hóa đơn.",
            "Quản lý người dùng, phản hồi, tin nhắn và vị trí cửa hàng.",
            "Xem danh sách yêu cầu mượn sách theo trạng thái.",
            "Duyệt yêu cầu mượn, từ chối, xác nhận trả sách hoặc đánh dấu quá hạn.",
            "Theo dõi nhật ký xác thực khuôn mặt, nhật ký mượn/trả và lỗi gửi Gmail.",
            "Kiểm tra tồn kho khi duyệt mượn và cập nhật tồn kho khi trả sách.",
        ],
    )

    page(
        doc,
        "1.4. Yêu cầu tích hợp AI/API phụ trợ",
        bullets_list=[
            "Flask server phải chạy tại `http://localhost:8000/api/face` để ASP.NET MVC gọi thông qua `FaceAuthApiClient`.",
            "Endpoint `/api/face/register` dùng để đăng ký/cập nhật mẫu khuôn mặt.",
            "Endpoint `/api/face/verify` và `/api/face/authenticate` dùng để xác thực khuôn mặt theo user.",
            "Endpoint `/api/face/action-check` dùng để kiểm tra hành động khuôn mặt như quay trái, quay phải, mở miệng, cười.",
            "Endpoint `/api/face/ocr-cmnd` dùng để OCR CMND/CCCD.",
            "Endpoint `/api/chatbox/ask` và `/api/chatbox/widget.js` dùng để tư vấn sách và nhúng widget chatbox.",
        ],
    )

    page(
        doc,
        "1.5. Yêu cầu phi chức năng",
        bullets_list=[
            "Giao diện rõ ràng, dễ sử dụng cho khách, người dùng và quản trị viên.",
            "Dữ liệu mượn/trả phải nhất quán với tồn kho.",
            "Mỗi thao tác quan trọng cần được ghi log để truy vết.",
            "Ảnh upload giới hạn dung lượng, định dạng JPG/JPEG/PNG.",
            "Response giữa MVC và Flask phải là JSON hợp lệ, có `success`, `confidence`, `request_id` và mã lỗi khi thất bại.",
            "Hệ thống phải hiển thị lỗi thân thiện khi Flask, OCR hoặc Gmail không sẵn sàng.",
        ],
    )

    page(
        doc,
        "CHƯƠNG 2. PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG CỦA HỆ THỐNG",
        [
            "Chương này phân tích các tác nhân, use case và luồng nghiệp vụ chính. Nội dung được chuẩn hóa từ kế hoạch sửa báo cáo và đối chiếu với source ASP.NET MVC/Flask.",
        ],
        break_after=False,
    )

    page(
        doc,
        "2.1. Tác nhân hệ thống",
        table=[
            ["Tác nhân", "Vai trò"],
            ["Khách vãng lai", "Xem trang chủ, danh mục, tìm kiếm và xem chi tiết sách"],
            ["Người dùng", "Đăng nhập, cập nhật hồ sơ, OCR CMND/CCCD, xác thực khuôn mặt, mượn sách"],
            ["Quản trị viên", "Quản lý sách, đơn hàng, người dùng, duyệt/trả sách và xem log"],
            ["Face API/OCR", "Xử lý đăng ký mặt, xác thực, action-check và OCR"],
            ["Gmail", "Gửi thông báo trạng thái mượn/trả"],
            ["Chatbox", "Tư vấn sách, giá, tồn kho và hướng dẫn mượn"],
        ],
    )

    page(doc, "2.2. Biểu đồ use case tổng quát", image=ASSETS / "usecase_quan_ly_nha_sach.png", caption="Hình 2-1. Biểu đồ use case tổng quát")

    page(
        doc,
        "2.3. Use case người dùng",
        bullets_list=[
            "Đăng ký tài khoản.",
            "Đăng nhập và đăng xuất.",
            "Cập nhật thông tin cá nhân và Gmail nhận thông báo.",
            "Cập nhật CMND/CCCD bằng OCR.",
            "Đăng ký mẫu khuôn mặt.",
            "Xác thực khuôn mặt trước khi mượn sách.",
            "Gửi yêu cầu mượn sách và theo dõi lịch sử mượn.",
            "Đặt hàng, đánh giá sách và quản lý danh sách yêu thích.",
        ],
    )

    page(
        doc,
        "2.4. Use case quản trị viên",
        bullets_list=[
            "Quản lý sản phẩm, danh mục, nhà cung cấp và kho.",
            "Quản lý người dùng, phản hồi, đơn hàng và hóa đơn.",
            "Xem yêu cầu mượn sách đang chờ xử lý.",
            "Duyệt, từ chối, hủy, xác nhận trả sách và đánh dấu quá hạn.",
            "Xem nhật ký FaceAuthLogs, RentalLogs và GeofenceLogs.",
            "Theo dõi lỗi gửi Gmail và trạng thái xử lý mượn/trả.",
        ],
    )

    page(
        doc,
        "2.5. Use case Face API, Gmail và chatbox",
        bullets_list=[
            "Face API nhận ảnh và `user_id` từ MVC để đăng ký/xác thực.",
            "Action-check kiểm tra frame webcam và hành động được yêu cầu.",
            "OCR nhận ảnh giấy tờ, đọc text, parse thông tin và trả JSON.",
            "Gmail gửi thông báo khi tạo yêu cầu mượn, duyệt, từ chối, hủy, trả hoặc quá hạn.",
            "Chatbox trả lời câu hỏi về sách, giá, tồn kho và hướng dẫn mượn.",
        ],
    )

    page(
        doc,
        "2.6. Quy trình mượn sách",
        paragraphs=[
            "Quy trình mượn sách bắt đầu từ trang chi tiết sách. Người dùng chọn số lượng và số ngày mượn, hệ thống kiểm tra hồ sơ, tồn kho và trạng thái mượn hiện có. Sau đó người dùng phải xác thực khuôn mặt trước khi gửi yêu cầu.",
        ],
        image=ASSETS / "workflow_muon_sach.png",
        caption="Hình 2-2. Quy trình người dùng gửi yêu cầu mượn sách",
    )

    page(
        doc,
        "2.7. Quy trình OCR và xác thực khuôn mặt",
        paragraphs=[
            "OCR CMND/CCCD và xác thực khuôn mặt được tách sang Flask server. MVC chịu trách nhiệm nhận ảnh từ trình duyệt, lưu tạm, gọi API, đọc JSON và cập nhật hồ sơ/log trong database.",
        ],
        image=ASSETS / "workflow_ocr_face.png",
        caption="Hình 2-3. Quy trình OCR CMND/CCCD và xác thực khuôn mặt",
    )

    page(
        doc,
        "2.8. Quy trình admin xử lý mượn/trả",
        image=ASSETS / "workflow_admin.png",
        caption="Hình 2-4. Quy trình admin xử lý mượn/trả sách",
        break_after=False,
    )

    page(
        doc,
        "2.9. Ràng buộc nghiệp vụ",
        bullets_list=[
            "Người dùng phải đăng nhập trước khi gửi yêu cầu mượn sách.",
            "Người dùng phải có hồ sơ định danh và Gmail nhận thông báo.",
            "Mỗi lần xác thực khuôn mặt chỉ sinh token ngắn hạn cho đúng user và đúng sách.",
            "Không cho mượn nếu sách hết tồn kho hoặc đã có yêu cầu còn hiệu lực cùng sách.",
            "Khi admin duyệt mượn, tồn kho giảm; khi xác nhận trả, tồn kho tăng.",
            "Mọi thao tác mượn/trả và xác thực phải được ghi log.",
        ],
    )

    page(
        doc,
        "CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU",
        [
            "Chương này trình bày thiết kế dữ liệu dựa trên các model trong `Mood\\EF2`, script `sql/create_database.sql` và repository ghi log trong `Common`.",
        ],
        break_after=False,
    )

    page(
        doc,
        "3.1. Tổng quan cơ sở dữ liệu",
        [
            "Database `QLNhaSach` lưu dữ liệu người dùng, sách, danh mục, hóa đơn, chi tiết hóa đơn, nhà cung cấp, nhập hàng, kho, phản hồi, tin nhắn, vị trí cửa hàng, yêu cầu mượn, log xác thực, log mượn/trả, đánh giá và yêu thích.",
            "Entity Framework 6 ánh xạ dữ liệu thông qua `QuanLySachDBContext` và các model trong thư mục `Mood\\EF2`.",
        ],
    )

    page(
        doc,
        "3.2. Nhóm bảng quản lý nhà sách",
        table=[
            ["Bảng/model", "Mục đích"],
            ["Users", "Lưu tài khoản và hồ sơ người dùng"],
            ["Sanphams", "Lưu sách/sản phẩm, giá, hình ảnh và tồn kho"],
            ["Categories", "Lưu danh mục sách"],
            ["Orders", "Lưu đơn hàng"],
            ["Order_Detail", "Lưu chi tiết đơn hàng"],
            ["NhaCungCaps", "Lưu nhà cung cấp"],
            ["NhapHangs", "Lưu dữ liệu nhập hàng"],
            ["KhoHang", "Lưu thông tin kho"],
        ],
    )

    page(
        doc,
        "3.3. Nhóm bảng mượn/trả và log",
        table=[
            ["Bảng/model", "Mục đích"],
            ["RentalRequests", "Lưu yêu cầu mượn, trạng thái, ngày mượn, hạn trả và ngày trả thực tế"],
            ["RentalLogs", "Lưu lịch sử Request, Cancel, Approve, Reject, Return, Overdue"],
            ["FaceAuthLogs", "Lưu lịch sử đăng ký/xác thực mặt, confidence, request_id, lỗi"],
            ["GeofenceLogs", "Lưu log kiểm tra vị trí nếu sử dụng geofence"],
            ["ProductReviews", "Lưu đánh giá sách và file review"],
            ["ProductFavorites", "Lưu sách yêu thích của người dùng"],
            ["StoreLocations", "Lưu vị trí cửa hàng"],
        ],
    )

    page(
        doc,
        "3.4. Thiết kế bảng RentalRequests",
        [
            "`RentalRequests` là bảng trung tâm của quy trình mượn/trả. Bảng liên kết người dùng với sách, lưu số lượng, ngày tạo yêu cầu, ngày bắt đầu mượn, hạn trả, ngày trả thực tế, trạng thái và ghi chú xử lý.",
            "Các trạng thái nghiệp vụ gồm `Pending`, `Borrowing`, `Rejected`, `Cancelled`, `Returned` và `Overdue`. Trạng thái này giúp admin lọc danh sách và cập nhật vòng đời mượn/trả rõ ràng.",
        ],
    )

    page(
        doc,
        "3.5. Thiết kế bảng FaceAuthLogs và RentalLogs",
        [
            "`FaceAuthLogs` lưu thông tin hành động xác thực như Register, Verify, Login, MFA, Rental, OCR hoặc ActionCheck. Các trường quan trọng gồm UserID, Action, Result, Confidence, RequestId, Purpose, ErrorCode và LivenessPassed.",
            "`RentalLogs` lưu lịch sử thao tác mượn/trả, bao gồm RentalId, UserId, ActorUserId, Action, OldStatus, NewStatus, Details và CreatedAt. Bảng này hỗ trợ truy vết khi cần kiểm tra yêu cầu đã được xử lý bởi ai và vào thời điểm nào.",
        ],
    )

    page(
        doc,
        "3.6. Dữ liệu phụ trợ phía Flask",
        [
            "Flask server lưu embedding khuôn mặt vào `face_db.pkl`. Đây là dữ liệu phụ trợ ngoài SQL Server, được ánh xạ theo `user_id` của website ASP.NET MVC.",
            "Chatbox lưu tri thức vào `sales_chatbox/chatbox_knowledge.json` và lịch sử hội thoại vào `sales_chatbox/chatbox_history.md`. Khi cần cập nhật dữ liệu tư vấn, endpoint `/api/chatbox/train` có thể đọc sản phẩm từ database thông qua `pyodbc`.",
        ],
        break_after=False,
    )

    page(
        doc,
        "3.7. Ràng buộc dữ liệu và toàn vẹn nghiệp vụ",
        bullets_list=[
            "Không cho tạo yêu cầu mượn nếu sản phẩm không tồn tại.",
            "Không cho mượn quá số ngày tối đa `RentalMaxBorrowDays=30`.",
            "Không cho mượn nếu số lượng yêu cầu vượt tồn kho.",
            "Không cho tạo yêu cầu trùng khi user đang có yêu cầu còn hiệu lực với cùng sách.",
            "Mọi thay đổi trạng thái cần ghi vào `RentalLogs`.",
            "Mọi kết quả xác thực cần ghi vào `FaceAuthLogs` để phục vụ kiểm tra.",
        ],
    )

    page(
        doc,
        "CHƯƠNG 4. THIẾT KẾ CÁC CHỨC NĂNG CỦA HỆ THỐNG",
        [
            "Chương này mô tả các module chức năng chính theo controller, service và API thực tế trong source.",
        ],
        break_after=False,
    )

    page(
        doc,
        "4.1. Cấu trúc source và module",
        table=[
            ["Thư mục/file", "Vai trò"],
            ["BaiTapLon", "Project ASP.NET MVC, chứa controller, view và Web.config"],
            ["Mood", "Model Entity Framework và lớp Draw truy xuất dữ liệu"],
            ["Common", "Repository ghi log dùng chung"],
            ["CommomSentMail", "Helper gửi Gmail SMTP"],
            ["sql", "Script tạo database và migration"],
            ["report_assets", "Sơ đồ và ảnh minh họa báo cáo"],
            ["NHANDIENKHUONMAT-new07040226", "Flask Face API, OCR và chatbox"],
        ],
    )

    page(
        doc,
        "4.2. Module tài khoản và hồ sơ",
        [
            "`UsersController` xử lý đăng ký, đăng nhập, hồ sơ người dùng và các luồng liên quan đến tài khoản. Người dùng cần cập nhật đầy đủ email, họ tên và thông tin định danh để đủ điều kiện mượn sách.",
            "Màn hình đăng ký khuôn mặt được triển khai ở view `Users/RegisterFace.cshtml`, phối hợp với `FaceAuthController` để upload ảnh và gọi Flask endpoint `/api/face/register`.",
        ],
    )

    page(
        doc,
        "4.3. Module sản phẩm sách",
        [
            "`ProductController` xử lý danh sách sách, tìm kiếm, chi tiết, đánh giá và file review. Đây là điểm bắt đầu của quy trình mượn sách vì người dùng gửi yêu cầu từ trang chi tiết sản phẩm.",
            "Ngoài nghiệp vụ bán sách, sản phẩm còn có thông tin tồn kho để phục vụ kiểm tra khả năng cho mượn.",
        ],
    )

    page(
        doc,
        "4.4. Module FaceAuthController",
        bullets_list=[
            "Validate file upload: bắt buộc có file, dung lượng hợp lệ và đúng định dạng ảnh.",
            "Lưu ảnh tạm vào thư mục cấu hình như `FaceSampleStoragePath` hoặc `IdentityCardStoragePath`.",
            "Gọi Flask API bằng `FaceAuthApiClient`.",
            "Đọc JSON response, kiểm tra `success` và `confidence >= FaceAuthMinConfidence`.",
            "Ghi log vào `FaceAuthLogs` qua `LogRepository`.",
            "Sinh `faceToken` khi xác thực khuôn mặt thành công trong luồng mượn sách.",
        ],
    )

    page(
        doc,
        "4.5. Module RentalController",
        bullets_list=[
            "Hiển thị danh sách yêu cầu mượn của người dùng hoặc admin.",
            "Tạo yêu cầu mượn trạng thái `Pending` sau khi kiểm tra token khuôn mặt.",
            "Cho phép người dùng hủy yêu cầu đang chờ duyệt.",
            "Cho phép admin duyệt, từ chối, xác nhận trả và đánh dấu quá hạn.",
            "Cập nhật tồn kho khi duyệt mượn hoặc trả sách.",
            "Ghi log thao tác bằng `AddRentalLog`.",
        ],
    )

    page(
        doc,
        "4.6. Module gửi Gmail thông báo",
        [
            "`GmailNotificationService` gửi thông báo theo trạng thái xử lý mượn/trả. Các sự kiện chính gồm Request, ApproveSuccess, Reject, Cancel, Return và Overdue.",
            "Cấu hình `GmailNotificationsEnabled=true` cho phép bật/tắt gửi mail. Khi gửi thất bại, hệ thống ghi lỗi để admin kiểm tra cấu hình SMTP, email gửi hoặc app password.",
        ],
    )

    page(
        doc,
        "4.7. Module chatbox tư vấn sách",
        bullets_list=[
            "`/api/chatbox/health` kiểm tra trạng thái chatbox.",
            "`/api/chatbox/train` huấn luyện tri thức từ database sản phẩm.",
            "`/api/chatbox/ask` nhận câu hỏi và trả lời kèm danh sách sản phẩm phù hợp.",
            "`/api/chatbox/widget.js` trả script nhúng widget vào website.",
            "Chatbox hỗ trợ hỏi tên sách, giá, tồn kho và hướng dẫn mượn sách.",
        ],
    )

    page(
        doc,
        "4.8. Cấu hình tích hợp chính",
        table=[
            ["Key", "Giá trị", "Ý nghĩa"],
            ["FaceAuthAPI", "http://localhost:8000/api/face", "Base URL Flask Face API"],
            ["ChatboxWidgetUrl", "http://localhost:8000/api/chatbox/widget.js", "URL nhúng chatbox"],
            ["FaceAuthMinConfidence", "0.75", "Ngưỡng xác thực khuôn mặt"],
            ["FaceAuthRentalTokenMinutes", "3", "Thời hạn faceToken khi mượn"],
            ["RentalMaxBorrowDays", "30", "Số ngày mượn tối đa"],
            ["GmailNotificationsEnabled", "true", "Bật gửi Gmail"],
        ],
    )

    page(
        doc,
        "CHƯƠNG 5. THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT",
        [
            "Chương này trình bày giao diện minh họa và hướng dẫn cài đặt/chạy hệ thống local theo đúng source được cung cấp.",
        ],
        break_after=False,
    )

    page(doc, "5.1. Giao diện trang chủ", image=ASSETS / "screenshot_home.png", caption="Hình 5-1. Trang chủ hệ thống quản lý nhà sách")
    page(doc, "5.2. Giao diện danh sách sản phẩm", image=ASSETS / "screenshot_product_list.png", caption="Hình 5-2. Màn hình danh sách sản phẩm sách")
    page(doc, "5.3. Giao diện đăng nhập", image=ASSETS / "screenshot_login.png", caption="Hình 5-3. Màn hình đăng nhập")
    page(doc, "5.4. Giao diện mượn/trả sách", image=ASSETS / "screenshot_rentals.png", caption="Hình 5-4. Màn hình danh sách mượn/trả")

    page(
        doc,
        "5.5. Cài đặt website ASP.NET MVC",
        bullets_list=[
            "Mở solution `DongTrieuBookStore.sln` bằng Visual Studio.",
            "Khôi phục NuGet package nếu thiếu.",
            "Tạo database từ `sql/create_database.sql` và các migration trong `sql/migrations`.",
            "Kiểm tra cấu hình trong `BaiTapLon/Web.config`.",
            "Chạy project `BaiTapLon` và kiểm thử trang chủ, đăng nhập, sản phẩm, mượn/trả.",
        ],
    )

    page(
        doc,
        "5.6. Cài đặt Flask Face API",
        bullets_list=[
            "Mở terminal tại `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226`.",
            "Cài dependency bằng `pip install -r requirements.txt` nếu môi trường mới.",
            "Chạy `python app.py`.",
            "Mở `http://localhost:8000/api/face/health` để kiểm tra trạng thái.",
            "Nếu camera bị đảo trái/phải, đặt biến môi trường `FACE_ACTION_FLIP_HORIZONTAL=true`.",
        ],
    )

    page(
        doc,
        "5.7. Các dependency Flask",
        table=[
            ["Package", "Vai trò"],
            ["Flask", "Cung cấp API server"],
            ["insightface, onnxruntime", "Nhận diện và so khớp khuôn mặt"],
            ["mediapipe", "Face Landmarker cho action-check"],
            ["opencv-python, numpy", "Xử lý ảnh"],
            ["paddleocr, pytesseract", "OCR CMND/CCCD"],
            ["pyodbc", "Đọc database cho chatbox"],
            ["scikit-image", "Hỗ trợ xử lý ảnh/chất lượng ảnh"],
        ],
    )

    doc.heading("5.8. Quy trình chạy thử liên thông", 2)
    numbered(
        doc,
        [
            "Khởi động SQL Server/LocalDB và đảm bảo database đã có dữ liệu.",
            "Khởi động Flask server ở port 8000.",
            "Chạy website ASP.NET MVC.",
            "Đăng nhập tài khoản người dùng.",
            "Đăng ký khuôn mặt, cập nhật hồ sơ CMND/CCCD, chọn sách và xác thực khi mượn.",
            "Đăng nhập admin để duyệt/trả sách và kiểm tra Gmail/log.",
        ],
    )
    doc.page_break()

    page(
        doc,
        "CHƯƠNG 6. KIỂM THỬ HỆ THỐNG",
        [
            "Chương này mô tả kế hoạch kiểm thử theo nhóm chức năng. Các kịch bản kiểm thử bám vào ràng buộc nghiệp vụ và endpoint thực tế trong source.",
        ],
        break_after=False,
    )

    page(
        doc,
        "6.1. Kiểm thử tài khoản và sản phẩm",
        table=[
            ["ID", "Trường hợp", "Kết quả mong đợi"],
            ["TK_01", "Đăng ký tài khoản hợp lệ", "Tạo tài khoản thành công"],
            ["TK_02", "Đăng nhập sai mật khẩu", "Báo lỗi đăng nhập"],
            ["SP_01", "Xem danh sách sách", "Hiển thị danh sách và phân trang"],
            ["SP_02", "Tìm kiếm sách", "Trả về sách phù hợp"],
            ["SP_03", "Xem chi tiết sách", "Hiển thị giá, tồn kho, đánh giá và nút mượn"],
        ],
    )

    page(
        doc,
        "6.2. Kiểm thử OCR và khuôn mặt",
        table=[
            ["ID", "Trường hợp", "Kết quả mong đợi"],
            ["OCR_01", "Ảnh CMND/CCCD rõ", "Đọc được số giấy tờ và thông tin cơ bản"],
            ["OCR_02", "Ảnh mờ hoặc sai giấy tờ", "Trả lỗi và yêu cầu chụp lại"],
            ["FACE_01", "Đăng ký một khuôn mặt rõ", "Lưu embedding thành công"],
            ["FACE_02", "Xác thực đúng người", "success=true, confidence >= 0.75"],
            ["FACE_03", "Nhiều khuôn mặt trong ảnh", "Trả lỗi MULTIPLE_FACES"],
            ["ACT_01", "Thực hiện đúng action challenge", "action_matched=true"],
        ],
    )

    page(
        doc,
        "6.3. Kiểm thử mượn/trả sách",
        table=[
            ["ID", "Trường hợp", "Kết quả mong đợi"],
            ["MT_01", "Mượn sách khi còn tồn và đã xác thực", "Tạo yêu cầu Pending"],
            ["MT_02", "Mượn khi thiếu hồ sơ", "Yêu cầu cập nhật hồ sơ"],
            ["MT_03", "Mượn khi hết tồn", "Không cho tạo yêu cầu"],
            ["MT_04", "Admin duyệt", "Chuyển Borrowing và giảm tồn kho"],
            ["MT_05", "Admin xác nhận trả", "Chuyển Returned và tăng tồn kho"],
            ["MT_06", "Đánh dấu quá hạn", "Chuyển Overdue và gửi thông báo"],
        ],
    )

    page(
        doc,
        "6.4. Kiểm thử Gmail, chatbox và log",
        table=[
            ["ID", "Trường hợp", "Kết quả mong đợi"],
            ["MAIL_01", "Gửi mail khi cấu hình đúng", "Người dùng nhận thông báo"],
            ["MAIL_02", "Sai app password", "Ghi log lỗi SMTP"],
            ["CHAT_01", "Hỏi tên sách", "Chatbox trả lời và gợi ý sản phẩm"],
            ["CHAT_02", "Server chatbox tắt", "Website hiển thị lỗi kết nối"],
            ["LOG_01", "Xác thực mặt", "Ghi FaceAuthLogs"],
            ["LOG_02", "Duyệt/trả sách", "Ghi RentalLogs"],
        ],
    )

    page(
        doc,
        "6.5. Tiêu chí nghiệm thu",
        bullets_list=[
            "Các chức năng chính không phát sinh lỗi dừng chương trình.",
            "Dữ liệu mượn/trả được lưu đúng trạng thái.",
            "Tồn kho thay đổi đúng khi duyệt mượn và xác nhận trả sách.",
            "Không thể gửi yêu cầu mượn nếu chưa xác thực khuôn mặt.",
            "OCR đọc được thông tin cơ bản khi ảnh đủ rõ.",
            "Gmail gửi được khi cấu hình đúng hoặc ghi lỗi rõ khi cấu hình sai.",
            "Chatbox hiển thị và phản hồi được câu hỏi phổ biến.",
        ],
    )

    page(
        doc,
        "CHƯƠNG 7. TỔNG KẾT VÀ ĐÁNH GIÁ",
        [
            "Đề tài đã chuẩn hóa báo cáo cho hệ thống quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn/trả sách. Nội dung báo cáo bám theo cấu trúc mẫu và thay toàn bộ thông tin cũ bằng thông tin từ kế hoạch, source QLNhaSach và source Flask.",
            "Hệ thống có điểm nổi bật là tách Face API thành Flask server riêng, giúp website ASP.NET MVC dễ tích hợp nhận diện khuôn mặt, OCR CMND/CCCD, action-check và chatbox tư vấn sách.",
        ],
        break_after=False,
    )

    page(
        doc,
        "7.1. Kết quả đạt được",
        bullets_list=[
            "Mô tả được nghiệp vụ quản lý nhà sách và quy trình mượn/trả.",
            "Phân tích được tác nhân, use case, ràng buộc nghiệp vụ và luồng xử lý.",
            "Thiết kế được nhóm bảng dữ liệu phục vụ người dùng, sách, mượn/trả, log và đánh giá.",
            "Trình bày được cách tích hợp ASP.NET MVC với Flask Face API, OCR, Gmail và chatbox.",
            "Bổ sung sơ đồ, ảnh giao diện, bảng endpoint, bảng kiểm thử và phụ lục cài đặt.",
        ],
    )

    page(
        doc,
        "7.2. Hạn chế và hướng phát triển",
        bullets_list=[
            "OCR vẫn phụ thuộc chất lượng ảnh giấy tờ và điều kiện ánh sáng.",
            "Nhận diện khuôn mặt phụ thuộc webcam, khoảng cách, ánh sáng và việc chỉ có một người trong khung hình.",
            "Gmail phụ thuộc app password và cấu hình SMTP.",
            "Flask server cần chạy song song với website để xác thực/OCR/chatbox hoạt động.",
            "Hướng phát triển gồm dashboard thống kê, tối ưu OCR, triển khai production, nâng cấp chatbox và tăng bảo mật lưu trữ embedding.",
        ],
    )

    page(
        doc,
        "TÀI LIỆU THAM KHẢO",
        bullets_list=[
            "Tài liệu ASP.NET MVC 5 và Entity Framework 6.",
            "Tài liệu Flask framework.",
            "Tài liệu InsightFace, ONNXRuntime, MediaPipe, PaddleOCR và Tesseract OCR.",
            "Source code dự án `QLNhaSach`.",
            "Source Flask `D:\\BACKUP_2004_2026_D\\NHANDIENKHUONMAT-new07040226`.",
            "`Template.pdf`, `BaoCaoMauSua.docx`, `QuyTrinhVietBaoCao.md`, `FACE_AUTH_FLASK_API_REQUIREMENTS.md`.",
        ],
        break_after=False,
    )

    doc.save(OUTPUT)
    with zipfile.ZipFile(OUTPUT, "r") as z:
        xml = z.read("word/document.xml").decode("utf-8")
        page_breaks = xml.count('w:type="page"')
        texts = " ".join(html.unescape(x) for x in re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml))
        missing = [
            key
            for key in [
                "CHƯƠNG 1. MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG",
                "CHƯƠNG 2. PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG CỦA HỆ THỐNG",
                "CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU",
                "CHƯƠNG 4. THIẾT KẾ CÁC CHỨC NĂNG CỦA HỆ THỐNG",
                "CHƯƠNG 5. THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT",
                "CHƯƠNG 6. KIỂM THỬ HỆ THỐNG",
                "CHƯƠNG 7. TỔNG KẾT VÀ ĐÁNH GIÁ",
            ]
            if key not in texts
        ]
    if page_breaks != 49:
        raise RuntimeError(f"Expected 49 page breaks for 50 logical pages, got {page_breaks}")
    if missing:
        raise RuntimeError("Missing headings: " + ", ".join(missing))

    log(
        "- Đã viết lại full `BaoCaoMauSua.docx` theo cấu trúc mẫu 7 chương, thay nội dung theo kế hoạch QLNhaSach + Flask.\n"
        "- Output được chia thành 50 trang logic bằng 49 ngắt trang rõ ràng.\n"
        "- Không sửa source ứng dụng; chỉ tạo script báo cáo và ghi lại file báo cáo."
    )
    print(OUTPUT)
    print("logical_pages=50")


if __name__ == "__main__":
    build_report()
