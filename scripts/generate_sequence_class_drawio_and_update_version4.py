# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_DIR = ROOT / "sequence_class_drawio_v4"
EXPORT_DIR = ROOT / "sequence_class_drawio_v4_exports"
REPORT = ROOT / "BaoCaoMauSua_Version4.docx"
BACKUP = ROOT / "BaoCaoMauSua_Version4.before_sequence_class_update.docx"
FALLBACK_REPORT = ROOT / "BaoCaoMauSua_Version4_SequenceClassDrawIO.docx"
HISTORY = ROOT / "LichSuXayDungHinhSequenceClass_Version4.md"

NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
ET.register_namespace("", NS_REL)


@dataclass(frozen=True)
class DiagramSpec:
    num: int
    kind: str
    title: str
    media_target: str
    drawio_name: str
    png_name: str
    participants: list[str]
    messages: list[tuple[str, str, str]]
    classes: list[tuple[str, str, list[str], list[str]]]
    note: str

    @property
    def code(self) -> str:
        return f"Hình 4-{self.num}"


def font(size=22, bold=False):
    for path in [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_TITLE = font(32, True)
FONT_HEAD = font(18, True)
FONT_TEXT = font(15)
FONT_SMALL = font(13)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    words = str(text).split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [""]


def draw_center(draw: ImageDraw.ImageDraw, box, text: str, fnt, fill=(0, 0, 0)):
    x1, y1, x2, y2 = box
    lines = wrap(draw, text, fnt, int(x2 - x1 - 16))
    line_h = fnt.size + 4
    y = y1 + (y2 - y1 - len(lines) * line_h) / 2
    for line in lines:
        w = draw.textbbox((0, 0), line, font=fnt)[2]
        draw.text((x1 + (x2 - x1 - w) / 2, y), line, font=fnt, fill=fill)
        y += line_h


def arrow(draw: ImageDraw.ImageDraw, start, end, fill=(170, 0, 35), width=3, dashed=False):
    if dashed:
        x1, y1 = start
        x2, y2 = end
        length = max(1, math.hypot(x2 - x1, y2 - y1))
        dx, dy = (x2 - x1) / length, (y2 - y1) / length
        step, dash = 18, 10
        dist = 0
        while dist < length:
            a = dist
            b = min(dist + dash, length)
            draw.line((x1 + dx * a, y1 + dy * a, x1 + dx * b, y1 + dy * b), fill=fill, width=width)
            dist += step
    else:
        draw.line((start[0], start[1], end[0], end[1]), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 10
    p1 = (end[0] - size * math.cos(angle - 0.45), end[1] - size * math.sin(angle - 0.45))
    p2 = (end[0] - size * math.cos(angle + 0.45), end[1] - size * math.sin(angle + 0.45))
    draw.polygon([end, p1, p2], fill=fill)


def base_classes(usecase: str, control: str, entities: list[str], extra_methods: list[str]) -> list[tuple[str, str, list[str], list[str]]]:
    return [
        (f"{usecase} View", "boundary", ["Razor/Browser UI"], ["submit()", "render()"]),
        (control, "control", ["DbContext", "Session"], extra_methods),
        *[(entity, "entity", ["ID", "Status/fields"], ["get()", "save()"]) for entity in entities],
    ]


def seq(num, slug, title, media, participants, messages, note):
    return DiagramSpec(num, "sequence", title, media, f"hinh_4_{num:02d}_{slug}.drawio", f"hinh_4_{num:02d}_{slug}.png", participants, messages, [], note)


def cls(num, slug, title, media, classes, note):
    return DiagramSpec(num, "class", title, media, f"hinh_4_{num:02d}_{slug}.drawio", f"hinh_4_{num:02d}_{slug}.png", [], [], classes, note)


DIAGRAMS: list[DiagramSpec] = [
    seq(1, "sequence_xem_san_pham", "Biểu đồ trình tự usecase xem sản phẩm", "word/media/image44.png", ["Khách/Người dùng", "Product View", "ProductController", "QuanLySachDBContext", "Sanpham/Category"], [("Khách/Người dùng", "Product View", "Mở danh sách/tìm kiếm"), ("Product View", "ProductController", "ListProduct()/Search()/Detail()"), ("ProductController", "QuanLySachDBContext", "Truy vấn sách, danh mục, review"), ("QuanLySachDBContext", "Sanpham/Category", "Đọc dữ liệu"), ("Sanpham/Category", "ProductController", "Trả kết quả"), ("ProductController", "Product View", "Render danh sách/chi tiết")], "ProductController.cs, Sanpham.cs, Category.cs, ProductReview.cs"),
    cls(2, "class_xem_san_pham", "Biểu đồ lớp phân tích usecase xem sản phẩm", "word/media/image45.emf", base_classes("Product/ListProduct", "ProductController", ["Sanpham", "Category", "ProductReview", "User"], ["Index()", "Search()", "ListProduct()", "Detail()", "ReviewFilePreview()"]), "ProductController.cs, Mood\\EF2"),
    seq(3, "sequence_danh_gia_san_pham", "Biểu đồ trình tự usecase đánh giá sản phẩm", "word/media/image47.png", ["Người dùng", "Detail View", "ProductController", "ProductReview", "DbContext"], [("Người dùng", "Detail View", "Nhập rating/comment"), ("Detail View", "ProductController", "AddReview(productId,rating,comment)"), ("ProductController", "ProductController", "Kiểm tra đăng nhập và dữ liệu"), ("ProductController", "ProductReview", "Tạo đánh giá"), ("ProductReview", "DbContext", "SaveChanges()"), ("ProductController", "Detail View", "Reload chi tiết sách")], "ProductController.AddReview, ProductReview.cs"),
    cls(4, "class_danh_gia_san_pham", "Biểu đồ lớp phân tích usecase đánh giá sản phẩm", "word/media/image48.emf", base_classes("Product/Detail", "ProductController", ["ProductReview", "Sanpham", "User"], ["AddReview()", "Detail()"]), "ProductController.cs, ProductReview.cs"),
    seq(5, "sequence_gio_hang_muon_sach", "Biểu đồ trình tự usecase thêm vào giỏ hàng và quy trình mượn sách", "word/media/image50.png", ["Người dùng", "Product/Cart View", "CartController", "RentalController", "FaceAuthController", "Flask Face API", "FaceRentalTokenService"], [("Người dùng", "Product/Cart View", "Bấm thêm giỏ/mượn"), ("Product/Cart View", "CartController", "AddItem(productID,quantity)"), ("CartController", "Product/Cart View", "Cập nhật Session cart"), ("Product/Cart View", "RentalController", "CheckStock(), RentalProfileStatus()"), ("RentalController", "FaceAuthController", "CreateChallenge()"), ("FaceAuthController", "Flask Face API", "action-check / verify"), ("Flask Face API", "FaceAuthController", "JSON success/confidence"), ("FaceAuthController", "FaceRentalTokenService", "Create token 3 phút")], "CartController.cs, RentalController.cs, FaceAuthController.cs"),
    cls(6, "class_gio_hang_muon_sach", "Biểu đồ lớp phân tích usecase thêm vào giỏ hàng và quy trình mượn sách", "word/media/image51.emf", base_classes("Cart/Rental View", "CartController + RentalController", ["Sanpham", "RentalRequest", "RentalLog", "FaceAuthLog"], ["AddItem()", "CheckStock()", "RequestRental()", "VerifyRentalFace()"]) + [("FaceAuthApiClient", "control", ["BaseUrl"], ["Verify()", "ActionCheck()"]), ("Flask Face API", "external", ["/api/face/*"], ["register()", "verify()"])], "Controllers, Services, Mood\\EF2"),
    seq(7, "sequence_yeu_thich", "Biểu đồ trình tự usecase thêm vào danh sách yêu thích", "word/media/image53.png", ["Người dùng", "Favorite UI", "UsersController", "ProductFavorite", "DbContext"], [("Người dùng", "Favorite UI", "Bấm icon yêu thích"), ("Favorite UI", "UsersController", "ToggleFavorite(productId)"), ("UsersController", "DbContext", "Tìm User/ProductFavorite"), ("UsersController", "ProductFavorite", "Thêm hoặc xóa"), ("ProductFavorite", "DbContext", "SaveChanges()"), ("UsersController", "Favorite UI", "JSON trạng thái mới")], "UsersController.ToggleFavorite, ProductFavorite.cs"),
    cls(8, "class_yeu_thich", "Biểu đồ lớp phân tích usecase thêm vào danh sách yêu thích", "word/media/image54.emf", base_classes("Favorites/LocalFavorites", "UsersController", ["ProductFavorite", "User", "Sanpham"], ["ToggleFavorite()", "LocalFavoriteProducts()", "SyncLocalFavorites()"]), "UsersController.cs, ProductFavorite.cs"),
    seq(9, "sequence_dat_hang_muon_sach", "Biểu đồ trình tự usecase đặt hàng hoặc gửi yêu cầu mượn sách", "word/media/image58.png", ["Người dùng", "Cart/Rental View", "CartController", "RentalController", "Orders/RentalRequests", "GmailNotificationService"], [("Người dùng", "Cart/Rental View", "Thanh toán hoặc gửi yêu cầu mượn"), ("Cart/Rental View", "CartController", "PaymentMoMo()/confirm_order"), ("CartController", "Orders/RentalRequests", "Tạo Orders + Order_Detail"), ("Cart/Rental View", "RentalController", "RequestRental(faceToken,borrowDays)"), ("RentalController", "Orders/RentalRequests", "Tạo RentalRequest Pending"), ("RentalController", "GmailNotificationService", "Send request mail"), ("RentalController", "Cart/Rental View", "Kết quả")], "CartController.cs, RentalController.RequestRental"),
    cls(10, "class_dat_hang_muon_sach", "Biểu đồ lớp phân tích usecase đặt hàng hoặc gửi yêu cầu mượn sách", "word/media/image59.emf", base_classes("Payment/Rental View", "CartController + RentalController", ["Orders", "Order_Detail", "RentalRequest", "Sanpham", "User"], ["PaymentMoMo()", "RequestRental()", "UpdateRentalStatus()"]) + [("GmailNotificationService", "control", ["Enabled"], ["SendRentalNotification()"])], "CartController.cs, RentalController.cs, GmailNotificationService.cs"),
    seq(11, "sequence_quan_ly_tai_khoan", "Biểu đồ trình tự usecase quản lý thông tin tài khoản", "word/media/image62.png", ["Người dùng", "Profile View", "UsersController", "RentalController", "FaceAuthController", "Flask OCR", "User"], [("Người dùng", "Profile View", "Sửa hồ sơ/OCR"), ("Profile View", "UsersController", "EditUser()/EditPassWord()"), ("UsersController", "User", "Cập nhật tài khoản"), ("Profile View", "RentalController", "UpdateRentalProfile()"), ("Profile View", "FaceAuthController", "OcrCmnd()"), ("FaceAuthController", "Flask OCR", "/api/face/ocr-cmnd"), ("Flask OCR", "Profile View", "Trả identity fields")], "UsersController.cs, RentalController.cs, FaceAuthController.cs"),
    cls(12, "class_quan_ly_tai_khoan", "Biểu đồ lớp phân tích usecase quản lý thông tin tài khoản", "word/media/image63.emf", base_classes("ProfileUser", "UsersController + RentalController", ["User", "FaceAuthLog"], ["ProfileUser()", "EditUser()", "EditPassWord()", "UpdateRentalProfile()"]) + [("FaceAuthController", "control", ["FaceAuthApiClient"], ["OcrCmnd()"]), ("Flask Face API", "external", ["/api/face/ocr-cmnd"], ["ocr_cmnd()"])], "UsersController.cs, RentalController.cs, FaceAuthController.cs"),
    seq(13, "sequence_don_hang_cua_toi", "Biểu đồ trình tự usecase đơn hàng của tôi", "word/media/image66.png", ["Người dùng", "My Orders View", "UsersController", "RentalController", "Orders/RentalRequests", "DbContext"], [("Người dùng", "My Orders View", "Mở đơn hàng/lịch sử mượn"), ("My Orders View", "UsersController", "ChiTietHoaDon(id)"), ("UsersController", "Orders/RentalRequests", "Đọc Orders + Order_Detail"), ("My Orders View", "RentalController", "MyRentals(status)"), ("RentalController", "Orders/RentalRequests", "Đọc RentalRequests"), ("UsersController", "My Orders View", "Render trạng thái")], "UsersController.ChiTietHoaDon, RentalController.MyRentals"),
    cls(14, "class_don_hang_cua_toi", "Biểu đồ lớp phân tích usecase đơn hàng của tôi", "word/media/image67.emf", base_classes("ChiTietHoaDon/MyRentals", "UsersController + RentalController", ["Orders", "Order_Detail", "RentalRequest", "Sanpham"], ["ChiTietHoaDon()", "MyRentals()"]), "UsersController.cs, RentalController.cs"),
    seq(15, "sequence_dang_ky", "Biểu đồ trình tự usecase đăng ký", "word/media/image69.png", ["Khách", "Register View", "UsersController", "User/Quyen", "FaceAuthController", "Flask Face API"], [("Khách", "Register View", "Nhập thông tin"), ("Register View", "UsersController", "RegisterUser(RegisterModel)"), ("UsersController", "User/Quyen", "Validate + tạo User"), ("UsersController", "Register View", "JSON thành công"), ("Register View", "FaceAuthController", "RegisterFace(userId) tùy chọn"), ("FaceAuthController", "Flask Face API", "/api/face/register")], "UsersController.RegisterUser, FaceAuthController.RegisterFace"),
    cls(16, "class_dang_ky", "Biểu đồ lớp phân tích usecase đăng ký", "word/media/image70.png", base_classes("Register View", "UsersController", ["RegisterModel", "User", "Quyen", "FaceAuthLog"], ["RegisterUser()", "RegisterFace()"]) + [("FaceAuthApiClient", "control", ["BaseUrl"], ["Register()"])], "AccountViewModels.cs, UsersController.cs"),
    seq(17, "sequence_dang_nhap", "Biểu đồ trình tự usecase đăng nhập", "word/media/image71.png", ["Người dùng", "Login View", "UsersController", "FaceAuthController", "Flask Face API", "FaceAuthLogs"], [("Người dùng", "Login View", "Nhập tài khoản/mật khẩu"), ("Login View", "UsersController", "Login(LoginModel)"), ("UsersController", "Login View", "Nếu cần MFA -> yêu cầu face"), ("Login View", "FaceAuthController", "CreateChallenge()/AuthenticateFaceLogin()"), ("FaceAuthController", "Flask Face API", "action-check + authenticate"), ("FaceAuthController", "FaceAuthLogs", "Ghi log"), ("UsersController", "Login View", "Set Session")], "UsersController.Login, FaceAuthController.AuthenticateFaceLogin"),
    cls(18, "class_dang_nhap", "Biểu đồ lớp phân tích usecase đăng nhập", "word/media/image72.png", base_classes("Login/LoginMFA", "UsersController + FaceAuthController", ["LoginModel", "User", "FaceAuthLog"], ["Login()", "CreateChallenge()", "AuthenticateFaceLogin()"]) + [("FaceAuthApiClient", "control", ["BaseUrl"], ["Authenticate()", "ActionCheck()"])], "UsersController.cs, FaceAuthController.cs"),
    seq(19, "sequence_quan_ly_don_hang", "Biểu đồ trình tự usecase quản lý đơn hàng", "word/media/image76.png", ["Quản trị viên", "Order Admin View", "CartController/UsersController", "Orders", "Order_Detail", "Sanpham"], [("Quản trị viên", "Order Admin View", "Mở danh sách đơn"), ("Order Admin View", "CartController/UsersController", "Đọc đơn hàng"), ("CartController/UsersController", "Orders", "Lọc trạng thái"), ("CartController/UsersController", "Order_Detail", "Xem chi tiết"), ("Quản trị viên", "Order Admin View", "Cập nhật trạng thái"), ("Order Admin View", "CartController/UsersController", "ChangeSuccessOrder()/confirm/cancel")], "CartController.cs, UsersController.ChangeSuccessOrder"),
    cls(20, "class_quan_ly_don_hang", "Biểu đồ lớp phân tích usecase quản lý đơn hàng", "word/media/image77.emf", base_classes("Order Admin View", "CartController + UsersController", ["Orders", "Order_Detail", "User", "Sanpham"], ["PaymentMoMo()", "Success()", "ChangeSuccessOrder()"]), "Orders.cs, Order_Detail.cs"),
    seq(21, "sequence_quan_ly_nguoi_dung", "Biểu đồ trình tự usecase quản lý người dùng", "word/media/image80.png", ["Quản trị viên", "User Admin View", "UsersController", "User/Quyen", "RentalRequest", "FaceAuthLog"], [("Quản trị viên", "User Admin View", "Mở danh sách user"), ("User Admin View", "UsersController", "DanhSachHang()/ProfileUser()"), ("UsersController", "User/Quyen", "Đọc/sửa tài khoản"), ("UsersController", "RentalRequest", "Xem lịch sử mượn"), ("UsersController", "FaceAuthLog", "Xem log xác thực"), ("UsersController", "User Admin View", "Render kết quả")], "UsersController.cs, User.cs, Quyen.cs"),
    cls(22, "class_quan_ly_nguoi_dung", "Biểu đồ lớp phân tích usecase quản lý người dùng", "word/media/image81.png", base_classes("User Admin View", "UsersController", ["User", "Quyen", "RentalRequest", "RentalLog", "FaceAuthLog", "GeofenceLog"], ["EditUser()", "DanhSachHang()", "ProfileUser()"]), "Mood\\EF2 user/log/rental models"),
    seq(23, "sequence_quan_ly_san_pham", "Biểu đồ trình tự usecase quản lý sản phẩm", "word/media/image90.png", ["Quản trị viên", "Product Admin View", "ProductController", "Sanpham", "Category/NhaCungCap/KhoHang", "DbContext"], [("Quản trị viên", "Product Admin View", "Mở CRUD sách"), ("Product Admin View", "ProductController", "List/Create/Edit/Delete"), ("ProductController", "Category/NhaCungCap/KhoHang", "Đọc dữ liệu phụ"), ("ProductController", "Sanpham", "Thêm/sửa/xóa sách"), ("Sanpham", "DbContext", "SaveChanges()"), ("ProductController", "Product Admin View", "Render kết quả")], "ProductController.cs, Sanpham.cs, Category.cs"),
    cls(24, "class_quan_ly_san_pham", "Biểu đồ lớp phân tích usecase quản lý sản phẩm", "word/media/image91.emf", base_classes("Product Admin View", "ProductController", ["Sanpham", "Category", "NhaCungCap", "KhoHang", "ProductReview", "Slide"], ["Index()", "Create()", "Edit()", "Delete()", "ReviewFilePreview()"]), "ProductController.cs, Mood\\EF2"),
    seq(25, "sequence_quan_ly_quan_tri_vien", "Biểu đồ trình tự usecase quản lý quản trị viên", "word/media/image97.png", ["Quản trị viên", "Admin Role View", "UsersController", "User", "Quyen", "LogRepository"], [("Quản trị viên", "Admin Role View", "Mở quản lý admin/quyền"), ("Admin Role View", "UsersController", "Đọc User + Quyen"), ("UsersController", "User", "Thêm/sửa tài khoản admin"), ("UsersController", "Quyen", "Gán IDQuyen"), ("UsersController", "LogRepository", "Ghi log nếu có"), ("UsersController", "Admin Role View", "Render kết quả")], "UsersController.cs, User.cs, Quyen.cs"),
    cls(26, "class_quan_ly_quan_tri_vien", "Biểu đồ lớp phân tích usecase quản lý quản trị viên", "word/media/image98.emf", base_classes("Admin Role View", "UsersController", ["User", "Quyen"], ["EditUser()", "RegisterUser()", "Dashboard()"]) + [("LogRepository", "control", ["DbContext"], ["WriteLog()"])], "UsersController.cs, Quyen.cs"),
    seq(27, "sequence_thong_ke", "Biểu đồ trình tự usecase thống kê", "word/media/image100.png", ["Quản trị viên", "Dashboard View", "UsersController", "Orders/RentalRequests", "Sanpham", "Log entities"], [("Quản trị viên", "Dashboard View", "Mở Dashboard"), ("Dashboard View", "UsersController", "Dashboard()"), ("UsersController", "Orders/RentalRequests", "Tổng hợp đơn/mượn"), ("UsersController", "Sanpham", "Tổng hợp sách/tồn kho"), ("UsersController", "Log entities", "Tổng hợp log"), ("UsersController", "Dashboard View", "Render chart/table")], "UsersController.Dashboard, Mood\\ThongKeModel"),
    cls(28, "class_thong_ke", "Biểu đồ lớp phân tích usecase thống kê", "word/media/image101.emf", base_classes("Dashboard View", "UsersController", ["ThongKeModelView", "Orders", "RentalRequest", "Sanpham", "FaceAuthLog", "RentalLog", "GeofenceLog"], ["Dashboard()", "Aggregate()"]), "UsersController.cs, Mood\\ThongKeModel"),
]


def render_sequence_png(spec: DiagramSpec) -> Path:
    n = len(spec.participants)
    width = max(1900, 180 + n * 240)
    height = 360 + len(spec.messages) * 86
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    red = (190, 0, 45)
    draw.text((50, 28), f"{spec.code}. {spec.title}", font=FONT_TITLE, fill=(25, 25, 25))
    x_positions = {}
    top = 110
    for i, p in enumerate(spec.participants):
        x = 95 + i * ((width - 190) / max(n - 1, 1))
        x_positions[p] = x
        box = (x - 82, top, x + 82, top + 56)
        draw.rectangle(box, fill=(248, 248, 248), outline=(60, 60, 60), width=2)
        draw_center(draw, box, p, FONT_SMALL)
        draw.line((x, top + 56, x, height - 75), fill=(150, 150, 150), width=2)
    y = top + 92
    for idx, (src, dst, msg) in enumerate(spec.messages, start=1):
        x1 = x_positions[src]
        x2 = x_positions[dst]
        dashed = "Trả" in msg or "JSON" in msg or "Render" in msg or "Kết quả" in msg
        arrow(draw, (x1, y), (x2, y), fill=red, width=2, dashed=dashed)
        label = f"{idx}. {msg}"
        tx = min(x1, x2) + 8
        draw.rectangle((tx - 4, y - 24, tx + min(520, abs(x2 - x1) + 160), y - 3), fill="white")
        draw.text((tx, y - 23), label[:80], font=FONT_SMALL, fill=(0, 0, 0))
        if idx in (3, 5) and len(spec.messages) > 5:
            draw.rectangle((45, y - 40, width - 45, y + 42), outline=(120, 120, 120), width=1)
        y += 86
    draw.text((50, height - 42), f"Nguồn đối chiếu: {spec.note}", font=FONT_SMALL, fill=(60, 60, 60))
    out = EXPORT_DIR / spec.png_name
    img.save(out, "PNG", optimize=True)
    return out


def render_class_png(spec: DiagramSpec) -> Path:
    cols = 3
    rows = math.ceil(len(spec.classes) / cols)
    width = 1800
    height = 180 + rows * 310
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    red = (190, 0, 45)
    draw.text((50, 28), f"{spec.code}. {spec.title}", font=FONT_TITLE, fill=(25, 25, 25))
    boxes = []
    for i, (name, stereo, attrs, methods) in enumerate(spec.classes):
        col, row = i % cols, i // cols
        x = 90 + col * 560
        y = 115 + row * 300
        box = (x, y, x + 420, y + 230)
        fill = (255, 250, 205) if stereo == "entity" else (255, 238, 238) if stereo == "control" else (235, 246, 255) if stereo == "boundary" else (240, 240, 240)
        draw.rectangle(box, fill=fill, outline=red, width=2)
        draw.rectangle((x, y, x + 420, y + 55), fill=(255, 245, 210), outline=red, width=2)
        draw_center(draw, (x + 5, y + 4, x + 415, y + 26), f"<<{stereo}>>", FONT_SMALL)
        draw_center(draw, (x + 5, y + 26, x + 415, y + 54), name, FONT_HEAD)
        yy = y + 66
        for attr in attrs[:4]:
            draw.text((x + 12, yy), f"- {attr}", font=FONT_TEXT, fill=(0, 0, 0))
            yy += 22
        draw.line((x, yy + 4, x + 420, yy + 4), fill=red, width=1)
        yy += 14
        for method in methods[:5]:
            draw.text((x + 12, yy), f"+ {method}", font=FONT_TEXT, fill=(0, 0, 0))
            yy += 22
        boxes.append((name, box))
    for (_, a), (_, b) in zip(boxes, boxes[1:]):
        ax, ay = a[2], (a[1] + a[3]) / 2
        bx, by = b[0], (b[1] + b[3]) / 2
        arrow(draw, (ax, ay), (bx, by), fill=red, width=2)
    draw.text((50, height - 42), f"Nguồn đối chiếu: {spec.note}", font=FONT_SMALL, fill=(60, 60, 60))
    out = EXPORT_DIR / spec.png_name
    img.save(out, "PNG", optimize=True)
    return out


def mx_cell(id_: str, value: str, style: str, x, y, w, h) -> str:
    return f'<mxCell id="{id_}" value="{escape(value)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'


def mx_edge(id_: str, source: str, target: str, value: str = "") -> str:
    return f'<mxCell id="{id_}" value="{escape(value)}" style="endArrow=block;html=1;rounded=0;strokeColor=#b00028;fontSize=12;" edge="1" parent="1" source="{source}" target="{target}"><mxGeometry relative="1" as="geometry"/></mxCell>'


def render_drawio(spec: DiagramSpec) -> Path:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    cells.append(mx_cell("title", f"{spec.code}. {spec.title}", "text;html=1;strokeColor=none;fillColor=none;fontSize=20;fontStyle=1;align=left;", 40, 30, 1200, 40))
    if spec.kind == "sequence":
        ids = {}
        for i, p in enumerate(spec.participants):
            x = 60 + i * 210
            cid = f"p{i}"
            ids[p] = cid
            cells.append(mx_cell(cid, p, "rounded=0;whiteSpace=wrap;html=1;fillColor=#f8f8f8;strokeColor=#333333;fontSize=12;", x, 105, 155, 50))
            cells.append(mx_cell(f"l{i}", "", "shape=line;html=1;strokeColor=#999999;dashed=1;", x + 77, 155, 1, 720))
        for i, (src, dst, msg) in enumerate(spec.messages, start=1):
            cells.append(mx_edge(f"e{i}", ids[src], ids[dst], f"{i}. {msg}"))
    else:
        ids = {}
        for i, (name, stereo, attrs, methods) in enumerate(spec.classes):
            x = 70 + (i % 3) * 360
            y = 110 + (i // 3) * 240
            value = f"&lt;&lt;{escape(stereo)}&gt;&gt;&lt;br&gt;&lt;b&gt;{escape(name)}&lt;/b&gt;&lt;hr&gt;" + "&lt;br&gt;".join(escape(a) for a in attrs + methods)
            cid = f"c{i}"
            ids[name] = cid
            cells.append(mx_cell(cid, value, "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff6cc;strokeColor=#b00028;fontSize=12;align=left;verticalAlign=top;spacing=8;", x, y, 300, 180))
        class_names = [c[0] for c in spec.classes]
        for i in range(len(class_names) - 1):
            cells.append(mx_edge(f"e{i}", ids[class_names[i]], ids[class_names[i + 1]], "uses"))
    xml = (
        f'<mxfile host="app.diagrams.net" modified="{datetime.now(UTC).isoformat()}" agent="Codex" version="24.7.17">'
        f'<diagram id="{spec.code}" name="{escape(spec.code)}"><mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1100" math="0" shadow="0"><root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
    )
    out = DRAWIO_DIR / spec.drawio_name
    out.write_text(xml, encoding="utf-8")
    return out


def update_report(image_map: dict[str, Path]) -> tuple[list[str], Path, str]:
    if not BACKUP.exists():
        shutil.copy2(REPORT, BACKUP)
    temp = REPORT.with_suffix(".sequence_class.tmp.docx")
    replaced = []
    rel_target_updates: dict[str, str] = {}
    with zipfile.ZipFile(REPORT, "r") as zin:
        rel_root = ET.fromstring(zin.read("word/_rels/document.xml.rels"))
        for rel in rel_root:
            target = rel.attrib.get("Target", "")
            full = f"word/{target}" if target.startswith("media/") else target
            if full in image_map and target.lower().endswith(".emf"):
                new_target = f"media/{image_map[full].name}"
                rel_target_updates[full] = f"word/{new_target}"
                rel.attrib["Target"] = new_target
        rels_xml = ET.tostring(rel_root, encoding="utf-8", xml_declaration=True)
        new_media_written = set()
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in rel_target_updates:
                    continue
                data = zin.read(item.filename)
                if item.filename == "word/_rels/document.xml.rels":
                    data = rels_xml
                elif item.filename in image_map:
                    data = image_map[item.filename].read_bytes()
                    replaced.append(item.filename)
                zout.writestr(item, data)
            for old_target, new_target in rel_target_updates.items():
                zout.writestr(new_target, image_map[old_target].read_bytes())
                new_media_written.add(new_target)
                replaced.append(f"{old_target} -> {new_target}")
    try:
        temp.replace(REPORT)
        return replaced, REPORT, "updated_original"
    except PermissionError:
        shutil.copy2(temp, FALLBACK_REPORT)
        return replaced, FALLBACK_REPORT, "saved_fallback_because_original_locked"


def append_history(drawios: list[Path], pngs: list[Path], replaced: list[str], output_report: Path, status: str):
    lines = [
        f"## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Xây dựng biểu đồ trình tự/lớp phân tích draw.io cho Version4",
        "",
        "- Kế hoạch: `KeHoach_XayDung_BieuDoTrinhTu_LopPhanTich_DrawIO_Version4.md`.",
        "- Thư mục draw.io: `sequence_class_drawio_v4`.",
        "- Thư mục PNG export: `sequence_class_drawio_v4_exports`.",
        f"- Kết quả Word: `{output_report.name}` ({status}).",
        f"- Số file draw.io: {len(drawios)}.",
        f"- Số PNG export: {len(pngs)}.",
        f"- Số media đã thay/cập nhật: {len(replaced)}.",
        "",
        "- Media đã thay:",
    ]
    for item in replaced:
        lines.append(f"  - `{item}`")
    lines.append("")
    previous = HISTORY.read_text(encoding="utf-8") if HISTORY.exists() else "# Lịch sử xây dựng hình sequence/class Version4\n\n"
    HISTORY.write_text(previous + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    DRAWIO_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)
    for path in DRAWIO_DIR.glob("*.drawio"):
        path.unlink()
    for path in EXPORT_DIR.glob("*.png"):
        path.unlink()
    drawios = [render_drawio(d) for d in DIAGRAMS]
    pngs = [render_sequence_png(d) if d.kind == "sequence" else render_class_png(d) for d in DIAGRAMS]
    image_map = {d.media_target: EXPORT_DIR / d.png_name for d in DIAGRAMS}
    replaced, output_report, status = update_report(image_map)
    append_history(drawios, pngs, replaced, output_report, status)
    print(f"Generated {len(drawios)} draw.io files")
    print(f"Generated {len(pngs)} PNG exports")
    print(f"Updated {len(replaced)} media entries in {output_report.name}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
