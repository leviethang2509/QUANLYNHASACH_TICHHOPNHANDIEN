# -*- coding: utf-8 -*-
from __future__ import annotations

import copy
import shutil
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "BaoCaoMauSua_Version3_DatabaseDrawIO.docx"
if not SOURCE.exists():
    SOURCE = ROOT / "BaoCaoMauSua_Version3.docx"
OUTPUT = ROOT / "BaoCaoMauSua_Version3_TableFields.docx"
BACKUP = ROOT / "BaoCaoMauSua_Version3.before_table_fields_update.docx"
HISTORY = ROOT / "LichSuXayDungHinhDatabase.md"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(name: str) -> str:
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def el(name: str, attrs: dict[str, str] | None = None, text: str | None = None) -> ET.Element:
    node = ET.Element(q(name), attrs or {})
    if text is not None:
        node.text = text
    return node


def para_text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.findall(".//w:t", NS)).strip()


def paragraph(text: str = "", style: str | None = None, bold: bool = False, size: int = 24, align: str | None = None) -> ET.Element:
    p = el("w:p")
    ppr = el("w:pPr")
    if style:
        ppr.append(el("w:pStyle", {q("w:val"): style}))
    if align:
        ppr.append(el("w:jc", {q("w:val"): align}))
    p.append(ppr)
    r = el("w:r")
    rpr = el("w:rPr")
    if bold:
        rpr.append(el("w:b"))
    rpr.append(el("w:sz", {q("w:val"): str(size)}))
    rpr.append(el("w:szCs", {q("w:val"): str(size)}))
    r.append(rpr)
    t = el("w:t", {q("xml:space"): "preserve"}, text)
    r.append(t)
    p.append(r)
    return p


def page_break() -> ET.Element:
    p = el("w:p")
    r = el("w:r")
    r.append(el("w:br", {q("w:type"): "page"}))
    p.append(r)
    return p


def table(rows: list[list[str]]) -> ET.Element:
    tbl = el("w:tbl")
    tbl_pr = el("w:tblPr")
    tbl_pr.append(el("w:tblStyle", {q("w:val"): "TableGrid"}))
    borders = el("w:tblBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        borders.append(el(f"w:{side}", {q("w:val"): "single", q("w:sz"): "6", q("w:space"): "0", q("w:color"): "000000"}))
    tbl_pr.append(borders)
    tbl.append(tbl_pr)
    for row_index, row in enumerate(rows):
        tr = el("w:tr")
        for cell_text in row:
            tc = el("w:tc")
            tc_pr = el("w:tcPr")
            tc_pr.append(el("w:tcW", {q("w:w"): "2400", q("w:type"): "dxa"}))
            if row_index == 0:
                tc_pr.append(el("w:shd", {q("w:fill"): "D9EAF7"}))
            tc.append(tc_pr)
            tc.append(paragraph(cell_text, bold=row_index == 0, size=22))
            tr.append(tc)
        tbl.append(tr)
    return tbl


def image_paragraph(rel_id: str, name: str, width_emu: int = 5600000, height_emu: int = 3600000) -> ET.Element:
    p = el("w:p")
    ppr = el("w:pPr")
    ppr.append(el("w:jc", {q("w:val"): "center"}))
    p.append(ppr)
    r = el("w:r")
    drawing = el("w:drawing")
    inline = el("wp:inline", {"distT": "0", "distB": "0", "distL": "0", "distR": "0"})
    inline.append(el("wp:extent", {"cx": str(width_emu), "cy": str(height_emu)}))
    inline.append(el("wp:effectExtent", {"l": "0", "t": "0", "r": "0", "b": "0"}))
    inline.append(el("wp:docPr", {"id": "3301", "name": name}))
    inline.append(el("wp:cNvGraphicFramePr"))
    graphic = el("a:graphic")
    graphic_data = el("a:graphicData", {"uri": "http://schemas.openxmlformats.org/drawingml/2006/picture"})
    pic = el("pic:pic")
    nv = el("pic:nvPicPr")
    nv.append(el("pic:cNvPr", {"id": "0", "name": name}))
    nv.append(el("pic:cNvPicPr"))
    pic.append(nv)
    blip_fill = el("pic:blipFill")
    blip_fill.append(el("a:blip", {q("r:embed"): rel_id}))
    stretch = el("a:stretch")
    stretch.append(el("a:fillRect"))
    blip_fill.append(stretch)
    pic.append(blip_fill)
    sp_pr = el("pic:spPr")
    xfrm = el("a:xfrm")
    xfrm.append(el("a:off", {"x": "0", "y": "0"}))
    xfrm.append(el("a:ext", {"cx": str(width_emu), "cy": str(height_emu)}))
    sp_pr.append(xfrm)
    prst = el("a:prstGeom", {"prst": "rect"})
    prst.append(el("a:avLst"))
    sp_pr.append(prst)
    pic.append(sp_pr)
    graphic_data.append(pic)
    graphic.append(graphic_data)
    inline.append(graphic)
    drawing.append(inline)
    r.append(drawing)
    p.append(r)
    return p


TABLES = [
    (
        "Users",
        [
            ["IDUser", "long", "PK", "Mã định danh người dùng trong hệ thống."],
            ["UserName", "string", "UNIQUE", "Tên đăng nhập của tài khoản."],
            ["PassWord", "string", "", "Mật khẩu đã mã hóa/được lưu theo cơ chế hiện tại của project."],
            ["Name", "string", "", "Họ tên hiển thị của người dùng."],
            ["Email", "string", "", "Email đăng ký tài khoản."],
            ["NotificationEmail", "string", "", "Email nhận thông báo mượn/trả sách."],
            ["Phone", "string", "", "Số điện thoại liên hệ."],
            ["Adress", "string", "", "Địa chỉ người dùng."],
            ["Status", "bool/int", "", "Trạng thái hoạt động của tài khoản."],
            ["IDQuyen", "long", "FK", "Liên kết tới bảng Quyens để xác định quyền."],
            ["IdentityNumber", "string", "", "Số CMND/CCCD dùng cho hồ sơ mượn sách."],
            ["IdentityFullName", "string", "", "Họ tên đọc từ giấy tờ định danh."],
            ["IdentityDateOfBirth", "date", "", "Ngày sinh trong hồ sơ định danh."],
            ["IdentityGender", "string", "", "Giới tính trong giấy tờ."],
            ["IdentityAddress", "string", "", "Địa chỉ trên CMND/CCCD."],
            ["IdentityIssueDate", "date", "", "Ngày cấp giấy tờ."],
            ["IdentityCardFrontImagePath", "string", "", "Đường dẫn ảnh mặt trước CMND/CCCD."],
            ["IdentityCardBackImagePath", "string", "", "Đường dẫn ảnh mặt sau CMND/CCCD."],
            ["IdentityFaceConfidence", "decimal", "", "Độ tin cậy khi so khớp khuôn mặt với giấy tờ."],
        ],
    ),
    (
        "Quyens",
        [
            ["IDQuyen", "long", "PK", "Mã quyền."],
            ["TenQuyen", "string", "", "Tên quyền như người dùng, quản trị viên."],
            ["Status", "bool/int", "", "Trạng thái sử dụng của quyền."],
        ],
    ),
    (
        "Sanphams",
        [
            ["IDContent", "long", "PK", "Mã sách/sản phẩm."],
            ["Name", "string", "", "Tên sách."],
            ["MetaTitle", "string", "", "Tên dùng cho SEO/URL."],
            ["TacGia", "string", "", "Tác giả."],
            ["NhaXuatBan", "string", "", "Nhà xuất bản."],
            ["Soluong", "int", "", "Số lượng nhập hoặc tổng số lượng."],
            ["TonKho", "int", "", "Số lượng còn trong kho."],
            ["Images", "string", "", "Đường dẫn ảnh bìa sách."],
            ["CategoryID", "long", "FK", "Liên kết danh mục sách."],
            ["NgayTao", "datetime", "", "Ngày tạo dữ liệu sách."],
            ["IDNguoiTao", "long", "", "Người tạo bản ghi."],
            ["Status", "bool/int", "", "Trạng thái hiển thị."],
            ["Tophot", "datetime/bool", "", "Đánh dấu sách nổi bật."],
            ["Mota", "string", "", "Mô tả ngắn."],
            ["ChiTiet", "string", "", "Nội dung chi tiết."],
            ["IDNCC", "long", "FK", "Nhà cung cấp nếu có."],
            ["GiaTien", "decimal", "", "Giá bán."],
            ["GiaNhap", "decimal", "", "Giá nhập."],
            ["PriceSale", "decimal", "", "Giá khuyến mãi."],
            ["ReviewFilePath", "string", "", "Đường dẫn file review/preview."],
            ["ReviewFileName", "string", "", "Tên file review/preview."],
            ["YoutubeUrl", "string", "", "Đường dẫn video giới thiệu nếu có."],
        ],
    ),
    (
        "Categories",
        [
            ["IDCategory", "long", "PK", "Mã danh mục."],
            ["TenTheloai", "string", "", "Tên thể loại/danh mục."],
            ["MetaTitle", "string", "", "Tên SEO."],
            ["ParentID", "long", "FK", "Danh mục cha nếu có."],
            ["SEOTitle", "string", "", "Tiêu đề SEO."],
            ["NgayTao", "datetime", "", "Ngày tạo danh mục."],
            ["DisPlayOrder", "int", "", "Thứ tự hiển thị."],
            ["MetaDescriptions", "string", "", "Mô tả SEO."],
            ["Status", "bool/int", "", "Trạng thái hiển thị."],
        ],
    ),
    (
        "Slides",
        [
            ["Id", "int", "PK", "Mã slide/banner."],
            ["Image", "string", "", "Đường dẫn ảnh slide."],
            ["DisPlayOrder", "int", "", "Thứ tự hiển thị."],
            ["Title", "string", "", "Tiêu đề slide."],
            ["Link", "string", "", "Liên kết khi bấm vào slide."],
            ["Status", "bool/int", "", "Trạng thái hiển thị."],
        ],
    ),
    (
        "Orders",
        [
            ["IDOder", "long", "PK", "Mã đơn hàng."],
            ["CustomerID", "long", "FK", "Người đặt hàng."],
            ["NgayTao", "datetime", "", "Ngày tạo đơn."],
            ["ShipName", "string", "", "Tên người nhận."],
            ["ShipMobile", "string", "", "Số điện thoại nhận hàng."],
            ["ShipAddress", "string", "", "Địa chỉ nhận hàng."],
            ["ShipEmail", "string", "", "Email nhận thông tin đơn."],
            ["Status", "int", "", "Trạng thái đơn hàng."],
            ["GiaoHang", "bool/int", "", "Trạng thái giao hàng."],
            ["NhanHang", "bool/int", "", "Trạng thái nhận hàng."],
            ["DeliveryPaymentMethod", "string", "", "Phương thức thanh toán/giao nhận."],
            ["StatusPayment", "int", "", "Trạng thái thanh toán."],
            ["OrderCode", "string", "", "Mã đơn dùng cho đối soát."],
        ],
    ),
    (
        "OrderDetails",
        [
            ["OderID", "long", "PK/FK", "Liên kết tới Orders."],
            ["ProductID", "long", "PK/FK", "Liên kết tới Sanphams."],
            ["Quanlity", "int", "", "Số lượng mua."],
            ["Price", "decimal", "", "Đơn giá tại thời điểm mua."],
        ],
    ),
    (
        "RentalRequests",
        [
            ["ID", "int", "PK", "Mã yêu cầu mượn sách."],
            ["UserID", "long", "FK", "Người gửi yêu cầu."],
            ["ProductID", "long", "FK", "Sách được yêu cầu mượn."],
            ["Quantity", "int", "", "Số lượng mượn."],
            ["Status", "string/int", "", "Trạng thái Pending, Approved, Rejected, Returned, Overdue."],
            ["RequestedAt", "datetime", "", "Thời điểm gửi yêu cầu."],
            ["RequestDate", "date", "", "Ngày yêu cầu mượn."],
            ["BorrowDays", "int", "", "Số ngày mượn."],
            ["ExpectedReturnDate", "date", "", "Hạn trả dự kiến."],
            ["ApprovedAt", "datetime", "", "Thời điểm admin duyệt."],
            ["ReturnedAt", "datetime", "", "Thời điểm xác nhận trả."],
            ["ActualReturnDate", "date", "", "Ngày trả thực tế."],
            ["AdminID", "long", "FK", "Admin xử lý yêu cầu."],
            ["RejectReason", "string", "", "Lý do từ chối nếu có."],
            ["Details", "string", "", "Ghi chú xử lý."],
            ["IdentityNumber", "string", "", "Số giấy tờ tại thời điểm mượn."],
            ["IdentityFullName", "string", "", "Họ tên định danh tại thời điểm mượn."],
            ["IdentityCardFrontImagePath", "string", "", "Ảnh mặt trước giấy tờ kèm yêu cầu."],
            ["IdentityCardBackImagePath", "string", "", "Ảnh mặt sau giấy tờ kèm yêu cầu."],
            ["IdentityOcrRawJson", "string", "", "JSON OCR gốc để đối chiếu khi cần."],
        ],
    ),
    (
        "ProductFavorites",
        [
            ["ID", "long", "PK", "Mã bản ghi yêu thích."],
            ["UserID", "long", "FK", "Người dùng yêu thích sách."],
            ["ProductID", "long", "FK", "Sách được yêu thích."],
            ["CreatedAt", "datetime", "", "Thời điểm thêm vào yêu thích."],
            ["Unique(UserID, ProductID)", "constraint", "UNIQUE", "Mỗi người dùng chỉ yêu thích một sách một lần."],
        ],
    ),
    (
        "ProductReviews",
        [
            ["IDReview", "long", "PK", "Mã đánh giá."],
            ["ProductID", "long", "FK", "Sách được đánh giá."],
            ["UserID", "long", "FK", "Người đánh giá."],
            ["UserName", "string", "", "Tên hiển thị của người đánh giá."],
            ["Rating", "int", "", "Điểm đánh giá."],
            ["Comment", "string", "", "Nội dung nhận xét."],
            ["CreatedAt", "datetime", "", "Thời điểm đánh giá."],
            ["Status", "bool/int", "", "Trạng thái hiển thị/duyệt đánh giá."],
        ],
    ),
    (
        "StoreLocations",
        [
            ["ID", "int", "PK", "Mã cửa hàng."],
            ["StoreName", "string", "", "Tên cửa hàng."],
            ["Address", "string", "", "Địa chỉ."],
            ["Phone", "string", "", "Số điện thoại."],
            ["Email", "string", "", "Email cửa hàng."],
            ["Latitude", "decimal", "", "Vĩ độ."],
            ["Longitude", "decimal", "", "Kinh độ."],
            ["GeofenceRadius", "decimal", "", "Bán kính kiểm tra vị trí."],
            ["IsActive", "bool", "", "Trạng thái hoạt động."],
            ["IconPath", "string", "", "Biểu tượng cửa hàng."],
            ["BannerPath", "string", "", "Ảnh banner."],
            ["WelcomeTitle", "string", "", "Tiêu đề giới thiệu."],
            ["WelcomeMessage", "string", "", "Nội dung chào mừng."],
            ["AboutContent", "string", "", "Nội dung giới thiệu."],
            ["MissionContent", "string", "", "Nội dung sứ mệnh."],
            ["SortOrder", "int", "", "Thứ tự hiển thị."],
        ],
    ),
    (
        "FaceAuthLogs",
        [
            ["ID", "int", "PK", "Mã log xác thực."],
            ["UserID", "long", "FK", "Người dùng liên quan."],
            ["Action", "string", "", "Hành động register, verify, authenticate, action-check."],
            ["Timestamp", "datetime", "", "Thời điểm ghi log."],
            ["IP", "string", "", "Địa chỉ IP nếu có."],
            ["DeviceInfo", "string", "", "Thông tin thiết bị/trình duyệt."],
            ["ImagePath", "string", "", "Ảnh đầu vào hoặc ảnh tạm."],
            ["Result", "string/bool", "", "Kết quả xác thực."],
            ["Confidence", "decimal", "", "Độ tin cậy nhận diện."],
            ["ErrorMessage", "string", "", "Thông báo lỗi."],
            ["RequestId", "string", "", "Mã request trả từ Flask API."],
            ["Purpose", "string", "", "Mục đích đăng nhập, mượn sách, OCR."],
            ["ErrorCode", "string", "", "Mã lỗi chuẩn hóa."],
            ["LivenessPassed", "bool", "", "Kết quả kiểm tra hành động sống."],
        ],
    ),
    (
        "RentalLogs",
        [
            ["ID", "int", "PK", "Mã log mượn/trả."],
            ["RentalID", "int", "FK", "Yêu cầu mượn liên quan."],
            ["UserID", "long", "FK", "Người dùng mượn sách."],
            ["ActorUserID", "long", "FK", "Người thực hiện thao tác."],
            ["Action", "string", "", "Request, Cancel, Approve, Reject, Return, Overdue."],
            ["Timestamp", "datetime", "", "Thời điểm thao tác."],
            ["Details", "string", "", "Ghi chú chi tiết."],
            ["OldStatus", "string", "", "Trạng thái trước khi đổi."],
            ["NewStatus", "string", "", "Trạng thái sau khi đổi."],
        ],
    ),
    (
        "GeofenceLogs",
        [
            ["ID", "int", "PK", "Mã log geofence."],
            ["UserID", "long", "FK", "Người dùng được kiểm tra vị trí."],
            ["StoreID", "int", "FK", "Cửa hàng liên quan."],
            ["IsInZone", "bool", "", "Có nằm trong vùng cho phép hay không."],
            ["Timestamp", "datetime", "", "Thời điểm kiểm tra."],
            ["UserLat", "decimal", "", "Vĩ độ người dùng."],
            ["UserLon", "decimal", "", "Kinh độ người dùng."],
            ["Distance", "decimal", "", "Khoảng cách đến cửa hàng."],
            ["AllowedRadiusKm", "decimal", "", "Bán kính cho phép."],
            ["StoreName", "string", "", "Tên cửa hàng tại thời điểm ghi log."],
        ],
    ),
    (
        "FaceSamples / FaceRentalTokens",
        [
            ["FaceSamples", "logical/storage", "", "Mẫu khuôn mặt/embedding lưu phía Flask, không phải bảng vật lý trong SQL Server."],
            ["FaceSampleStoragePath", "config", "", "Đường dẫn lưu ảnh/mẫu khuôn mặt."],
            ["FaceRentalToken.Token", "string", "", "Token sinh sau khi xác thực khuôn mặt để gửi yêu cầu mượn."],
            ["FaceRentalToken.UserID", "long", "", "Người dùng sở hữu token."],
            ["FaceRentalToken.ProductID", "long", "", "Sách gắn với token."],
            ["FaceRentalToken.ExpiresAt", "datetime", "", "Thời điểm hết hạn token."],
            ["FaceRentalToken.Consumed", "bool", "", "Đánh dấu token đã dùng."],
        ],
    ),
]


RELATIONS = [
    ["Users.IDQuyen", "Quyens.IDQuyen", "Một người dùng thuộc một quyền chính."],
    ["Sanphams.CategoryID", "Categories.IDCategory", "Một sách thuộc một danh mục."],
    ["Orders.CustomerID", "Users.IDUser", "Một người dùng có thể có nhiều đơn hàng."],
    ["OrderDetails.OderID", "Orders.IDOder", "Một đơn hàng có nhiều dòng chi tiết."],
    ["OrderDetails.ProductID", "Sanphams.IDContent", "Một dòng chi tiết ứng với một sách."],
    ["RentalRequests.UserID", "Users.IDUser", "Một người dùng có thể gửi nhiều yêu cầu mượn."],
    ["RentalRequests.ProductID", "Sanphams.IDContent", "Một yêu cầu mượn ứng với một sách."],
    ["ProductFavorites.UserID", "Users.IDUser", "Một người dùng có nhiều sách yêu thích."],
    ["ProductFavorites.ProductID", "Sanphams.IDContent", "Một sách có thể được nhiều người yêu thích."],
    ["ProductReviews.UserID", "Users.IDUser", "Một người dùng có thể đánh giá nhiều sách."],
    ["ProductReviews.ProductID", "Sanphams.IDContent", "Một sách có nhiều đánh giá."],
    ["FaceAuthLogs.UserID", "Users.IDUser", "Log xác thực gắn với người dùng."],
    ["RentalLogs.RentalID", "RentalRequests.ID", "Log nghiệp vụ gắn với yêu cầu mượn."],
    ["GeofenceLogs.StoreID", "StoreLocations.ID", "Log vị trí gắn với cửa hàng."],
]


def build_chapter3(rel_id: str) -> list[ET.Element]:
    nodes: list[ET.Element] = [
        paragraph("CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU", "Heading1", bold=True, size=32),
        paragraph("3.1. Mô hình hóa dữ liệu", "Heading2", bold=True, size=28),
        paragraph(
            "Chương này mô tả thiết kế cơ sở dữ liệu của hệ thống quản lý nhà sách. "
            "Thay vì trình bày từng bảng bằng hình draw.io, báo cáo sử dụng bảng mô tả field để thể hiện rõ tên cột, kiểu dữ liệu, khóa và ý nghĩa sử dụng.",
            size=24,
        ),
        table(
            [
                ["Nhóm dữ liệu", "Các bảng/cấu trúc", "Mục đích"],
                ["Tài khoản và phân quyền", "Users, Quyens", "Lưu tài khoản, hồ sơ định danh và quyền truy cập."],
                ["Sách và danh mục", "Sanphams, Categories, Slides", "Lưu thông tin sách, phân loại và banner hiển thị."],
                ["Đơn hàng", "Orders, OrderDetails", "Lưu giao dịch đặt mua sách."],
                ["Mượn/trả sách", "RentalRequests, RentalLogs", "Lưu yêu cầu mượn, trạng thái xử lý và lịch sử thao tác."],
                ["Tương tác người dùng", "ProductFavorites, ProductReviews", "Lưu sách yêu thích và đánh giá sách."],
                ["Xác thực/vị trí", "FaceAuthLogs, StoreLocations, GeofenceLogs", "Lưu log xác thực khuôn mặt, cửa hàng và kiểm tra vị trí."],
                ["Cấu trúc logic", "FaceSamples, FaceRentalTokens", "Lưu ngoài DB hoặc trong bộ nhớ phục vụ Face API và luồng mượn sách."],
            ]
        ),
        paragraph("3.2. Thiết kế bảng dữ liệu", "Heading2", bold=True, size=28),
    ]
    for name, rows in TABLES:
        nodes.append(paragraph(f"Bảng {name}", "Heading3", bold=True, size=26))
        nodes.append(table([["Field", "Kiểu dữ liệu", "Khóa/Ràng buộc", "Mô tả"]] + rows))
    nodes.extend(
        [
            paragraph("3.3. Quan hệ các bảng", "Heading2", bold=True, size=28),
            paragraph("Các quan hệ chính trong cơ sở dữ liệu được tổng hợp ở bảng sau và minh họa bằng sơ đồ quan hệ bảng.", size=24),
            table([["Khóa ngoại", "Tham chiếu", "Ý nghĩa"]] + RELATIONS),
            image_paragraph(rel_id, "Quan he cac bang"),
            paragraph("Hình 3-1. Quan hệ các bảng trong cơ sở dữ liệu", "Caption", bold=True, size=22, align="center"),
            page_break(),
        ]
    )
    return nodes


def main() -> None:
    if not BACKUP.exists() and SOURCE.exists():
        shutil.copy2(SOURCE, BACKUP)

    with zipfile.ZipFile(SOURCE, "r") as zin:
        document_xml = zin.read("word/document.xml")
        rels_xml = zin.read("word/_rels/document.xml.rels")
        root = ET.fromstring(document_xml)
        rels_root = ET.fromstring(rels_xml)
        body = root.find("w:body", NS)
        if body is None:
            raise RuntimeError("Cannot find document body")

        children = list(body)
        start = end = None
        for index, child in enumerate(children):
            text = para_text(child)
            if start is None and "THIẾT KẾ CƠ SỞ DỮ LIỆU" in text:
                start = index
            elif start is not None and "THIẾT KẾ CÁC CHỨC NĂNG" in text:
                end = index
                break
        if start is None or end is None:
            raise RuntimeError("Cannot locate Chapter 3 boundaries")

        rel_id = None
        for rel in rels_root:
            if rel.attrib.get("Target") == "media/image39.png":
                rel_id = rel.attrib.get("Id")
                break
        if rel_id is None:
            for rel in rels_root:
                if rel.attrib.get("Target") == "media/image14.png":
                    rel_id = rel.attrib.get("Id")
                    break
        if rel_id is None:
            raise RuntimeError("Cannot find database relationship image relationship id")

        new_nodes = build_chapter3(rel_id)
        for child in children[start:end]:
            body.remove(child)
        insert_at = start
        for node in new_nodes:
            body.insert(insert_at, node)
            insert_at += 1

        children = list(body)
        seen_chapter3_figure = False
        chapter3_index = next(
            (
                index
                for index, child in enumerate(children)
                if para_text(child).startswith("CHƯƠNG 3. THIẾT KẾ CƠ SỞ DỮ LIỆU")
            ),
            len(children),
        )
        for child in children[:chapter3_index]:
            text = para_text(child)
            if text.startswith("Hình 3-"):
                if not seen_chapter3_figure:
                    for t in child.findall(".//w:t", NS):
                        t.text = "Hình 3-1. Quan hệ các bảng trong cơ sở dữ liệu"
                        break
                    seen_chapter3_figure = True
                else:
                    body.remove(child)

        updated_document = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = updated_document
                zout.writestr(item, data)

    with zipfile.ZipFile(OUTPUT, "r") as check:
        bad = check.testzip()
        if bad:
            raise RuntimeError(f"Invalid DOCX zip member: {bad}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with HISTORY.open("a", encoding="utf-8") as file:
        file.write(
            f"\n## {now} - Chuyen Chuong 3 sang bang mo ta field\n\n"
            f"- File nguon: `{SOURCE.name}`.\n"
            f"- File ket qua: `{OUTPUT.name}`.\n"
            "- Da bo cac hinh draw.io chi tiet tung bang trong Chuong 3.\n"
            "- Da viet lai muc 3.2 bang cac bang mo ta field, kieu du lieu, khoa/rang buoc va mo ta.\n"
            "- Chi giu lai mot hinh tai muc 3.3: `Quan he cac bang trong co so du lieu`.\n"
        )

    print(f"Updated Chapter 3 in {OUTPUT.name}")
    print("Kept one database relationship figure in section 3.3")


if __name__ == "__main__":
    main()
