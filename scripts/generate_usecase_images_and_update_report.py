from __future__ import annotations

import io
import math
import shutil
import textwrap
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "use_case"
REPORT = ROOT / "BaoCaoMauSua_Version2.docx"
BACKUP = ROOT / "BaoCaoMauSua_Version2.before_usecase_update.docx"
HISTORY = ROOT / "LichSuXayDungHinhUseCase.md"


@dataclass(frozen=True)
class UseCaseDiagram:
    code: str
    title: str
    filename: str
    media_target: str
    actors: dict[str, list[str]]
    notes: list[str]


DIAGRAMS = [
    UseCaseDiagram(
        "Hinh 21",
        "Bieu do use case chinh",
        "hinh_21_usecase_chinh.png",
        "word/media/image3.png",
        {
            "Khach vang lai": ["Xem trang chu", "Xem danh sach sach", "Tim kiem sach", "Xem chi tiet sach"],
            "Nguoi dung": [
                "Dang ky / Dang nhap",
                "Quan ly ho so",
                "OCR CMND/CCCD",
                "Xac thuc khuon mat",
                "Dat hang / Muon sach",
                "Danh gia, yeu thich",
            ],
            "Quan tri vien": [
                "Quan ly san pham",
                "Quan ly don hang",
                "Duyet muon/tra",
                "Quan ly nguoi dung",
                "Xem log, thong ke",
            ],
            "Face API": ["Register face", "Verify face", "Action challenge", "OCR CMND/CCCD"],
            "Gmail": ["Gui thong bao trang thai"],
            "Chatbox": ["Tu van sach", "Huong dan muon"],
        },
        ["Bam source: ProductController, UsersController, RentalController, FaceAuthController, GmailNotificationService"],
    ),
    UseCaseDiagram(
        "Hinh 22",
        "Bieu do use case Dang nhap",
        "hinh_22_usecase_dang_nhap.png",
        "word/media/image4.png",
        {
            "Nguoi dung": ["Nhap tai khoan", "Dang nhap", "Dang nhap MFA bang khuon mat", "Dang xuat"],
            "He thong MVC": ["Kiem tra tai khoan", "Tao challenge", "Luu session", "Ghi FaceAuthLogs"],
            "Face API": ["Kiem tra action", "Xac thuc khuon mat"],
        },
        ["Bam source: UsersController.Login, FaceAuthController.AuthenticateFaceLogin, /api/face/action-check"],
    ),
    UseCaseDiagram(
        "Hinh 23",
        "Bieu do use case Xem san pham",
        "hinh_23_usecase_xem_san_pham.png",
        "word/media/image5.png",
        {
            "Khach vang lai": ["Xem san pham", "Tim kiem", "Loc theo danh muc", "Xem chi tiet"],
            "Nguoi dung": ["Xem review", "Xem file preview", "Kiem tra ton kho", "Them gio hang", "Muon sach"],
            "He thong MVC": ["Doc Sanpham", "Doc Category", "Doc ProductReview", "Tra view"],
        },
        ["Bam source: ProductController.Index/Search/ListProduct/Detail/ReviewFilePreview"],
    ),
    UseCaseDiagram(
        "Hinh 24",
        "Bieu do use case Quan ly san pham",
        "hinh_24_usecase_quan_ly_san_pham.png",
        "word/media/image6.png",
        {
            "Quan tri vien": ["Them sach", "Sua sach", "Xoa/an sach", "Quan ly danh muc", "Quan ly kho", "Quan ly file review"],
            "He thong MVC": ["Validate du lieu", "Cap nhat Sanpham", "Cap nhat KhoHang", "Cap nhat Category"],
            "CSDL": ["Sanpham", "Category", "NhaCungCap", "KhoHang", "ProductReviews"],
        },
        ["Bam source: ProductController, Mood/Draw/SanphamDraw.cs, Mood/EF2/Sanpham.cs"],
    ),
    UseCaseDiagram(
        "Hinh 25",
        "Bieu do use case Quan ly don hang",
        "hinh_25_usecase_quan_ly_don_hang.png",
        "word/media/image7.png",
        {
            "Quan tri vien": ["Xem danh sach don", "Xem chi tiet", "Cap nhat trang thai", "Xu ly thanh toan", "Huy don"],
            "He thong MVC": ["Doc Orders", "Doc Order_Detail", "Cap nhat don", "Tra ket qua"],
            "Nguoi dung": ["Nhan trang thai don hang", "Xem lich su don"],
        },
        ["Bam source: CartController, Orders.cs, Order_Detail.cs"],
    ),
    UseCaseDiagram(
        "Hinh 26",
        "Bieu do use case Don hang cua toi",
        "hinh_26_usecase_don_hang_cua_toi.png",
        "word/media/image8.png",
        {
            "Nguoi dung": ["Xem don hang cua toi", "Xem chi tiet hoa don", "Theo doi trang thai", "Xem lich su muon"],
            "He thong MVC": ["Kiem tra session", "Lay Orders", "Lay Order_Detail", "Lay RentalRequests"],
            "CSDL": ["Orders", "Order_Detail", "RentalRequests", "Sanpham"],
        },
        ["Bam source: UsersController.ChiTietHoaDon, RentalController.MyRentals"],
    ),
    UseCaseDiagram(
        "Hinh 27",
        "Bieu do use case Quan ly nguoi dung",
        "hinh_27_usecase_quan_ly_nguoi_dung.png",
        "word/media/image9.png",
        {
            "Quan tri vien": ["Xem nguoi dung", "Cap nhat quyen", "Kiem tra ho so", "Xem lich su muon", "Xem log xac thuc"],
            "He thong MVC": ["Doc User", "Doc Quyen", "Doc RentalRequests", "Doc FaceAuthLogs"],
            "Log API": ["Face logs", "Rental logs", "Geofence logs"],
        },
        ["Bam source: UsersController, LogsController, User.cs, Quyen.cs, FaceAuthLog.cs"],
    ),
    UseCaseDiagram(
        "Hinh 28",
        "Bieu do use case Quan ly thong tin tai khoan",
        "hinh_28_usecase_quan_ly_thong_tin_tai_khoan.png",
        "word/media/image10.png",
        {
            "Nguoi dung": ["Cap nhat thong tin", "Doi mat khau", "Cap nhat Gmail", "Nhap CMND/CCCD", "Upload anh giay to", "Quan ly yeu thich"],
            "He thong MVC": ["EditUser", "EditPassWord", "UpdateRentalProfile", "Goi OCR"],
            "Face API": ["OCR CMND/CCCD", "So khop anh giay to neu co"],
        },
        ["Bam source: UsersController.ProfileUser/EditUser, RentalController.UpdateRentalProfile, FaceAuthController.OcrCmnd"],
    ),
    UseCaseDiagram(
        "Hinh 29",
        "Bieu do use case Quan ly quan tri vien",
        "hinh_29_usecase_quan_ly_quan_tri_vien.png",
        "word/media/image11.png",
        {
            "Quan tri vien": ["Dang nhap admin", "Quan ly tai khoan admin", "Phan quyen", "Xem dashboard", "Xem nhat ky"],
            "He thong MVC": ["Kiem tra quyen", "Cap nhat User/Quyen", "Tong hop thong ke", "Ghi log"],
            "CSDL": ["User", "Quyen", "Orders", "RentalRequests", "Logs"],
        },
        ["Bam source: UsersController, Quyen.cs, LogRepository.cs"],
    ),
    UseCaseDiagram(
        "Hinh 210",
        "Bieu do use case Quan ly gio hang va quy trinh muon sach",
        "hinh_210_usecase_gio_hang_muon_sach.png",
        "word/media/image12.png",
        {
            "Nguoi dung": ["Them gio hang", "Cap nhat gio", "Dat hang", "Kiem tra ho so muon", "Xac thuc khuon mat", "Gui yeu cau muon"],
            "He thong MVC": ["CheckStock", "CheckActiveRental", "RentalProfileStatus", "Sinh faceToken", "RequestRental"],
            "Face API": ["Action challenge", "Verify face"],
            "Gmail": ["Thong bao Request/Approve/Reject/Return"],
            "Quan tri vien": ["Duyet muon", "Tu choi", "Xac nhan tra", "Danh dau qua han"],
        },
        ["Bam source: CartController, RentalController, FaceAuthController, FaceRentalTokenService, GmailNotificationService"],
    ),
    UseCaseDiagram(
        "Hinh 211",
        "Bieu do use case Quan ly danh sach yeu thich",
        "hinh_211_usecase_danh_sach_yeu_thich.png",
        "word/media/image13.png",
        {
            "Nguoi dung": ["Them vao yeu thich", "Xoa khoi yeu thich", "Xem danh sach yeu thich", "Dong bo yeu thich local"],
            "He thong MVC": ["ToggleFavorite", "Favorites", "LocalFavoriteProducts", "SyncLocalFavorites"],
            "CSDL": ["ProductFavorites", "User", "Sanpham"],
        },
        ["Bam source: UsersController.ToggleFavorite/Favorites/SyncLocalFavorites, ProductFavorite.cs"],
    ),
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
        Path("C:/Windows/Fonts/tahoma.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(36, True)
FONT_SUBTITLE = load_font(22, True)
FONT_TEXT = load_font(19)
FONT_SMALL = load_font(16)

VI_TEXT = {
    "Bieu do use case chinh": "Biểu đồ use case chính",
    "Bieu do use case Dang nhap": "Biểu đồ use case Đăng nhập",
    "Bieu do use case Xem san pham": "Biểu đồ use case Xem sản phẩm",
    "Bieu do use case Quan ly san pham": "Biểu đồ use case Quản lý sản phẩm",
    "Bieu do use case Quan ly don hang": "Biểu đồ use case Quản lý đơn hàng",
    "Bieu do use case Don hang cua toi": "Biểu đồ use case Đơn hàng của tôi",
    "Bieu do use case Quan ly nguoi dung": "Biểu đồ use case Quản lý người dùng",
    "Bieu do use case Quan ly thong tin tai khoan": "Biểu đồ use case Quản lý thông tin tài khoản",
    "Bieu do use case Quan ly quan tri vien": "Biểu đồ use case Quản lý quản trị viên",
    "Bieu do use case Quan ly gio hang va quy trinh muon sach": "Biểu đồ use case Quản lý giỏ hàng và quy trình mượn sách",
    "Bieu do use case Quan ly danh sach yeu thich": "Biểu đồ use case Quản lý danh sách yêu thích",
    "Khach vang lai": "Khách vãng lai",
    "Nguoi dung": "Người dùng",
    "Quan tri vien": "Quản trị viên",
    "He thong MVC": "Hệ thống MVC",
    "CSDL": "CSDL",
    "Face API": "Face API",
    "Gmail": "Gmail",
    "Chatbox": "Chatbox",
    "Log API": "Log API",
    "Xem trang chu": "Xem trang chủ",
    "Xem danh sach sach": "Xem danh sách sách",
    "Tim kiem sach": "Tìm kiếm sách",
    "Xem chi tiet sach": "Xem chi tiết sách",
    "Dang ky / Dang nhap": "Đăng ký / Đăng nhập",
    "Quan ly ho so": "Quản lý hồ sơ",
    "OCR CMND/CCCD": "OCR CMND/CCCD",
    "Xac thuc khuon mat": "Xác thực khuôn mặt",
    "Dat hang / Muon sach": "Đặt hàng / Mượn sách",
    "Danh gia, yeu thich": "Đánh giá, yêu thích",
    "Quan ly san pham": "Quản lý sản phẩm",
    "Quan ly don hang": "Quản lý đơn hàng",
    "Duyet muon/tra": "Duyệt mượn/trả",
    "Quan ly nguoi dung": "Quản lý người dùng",
    "Xem log, thong ke": "Xem log, thống kê",
    "Register face": "Đăng ký khuôn mặt",
    "Verify face": "Xác thực khuôn mặt",
    "Action challenge": "Kiểm tra hành động",
    "Gui thong bao trang thai": "Gửi thông báo trạng thái",
    "Tu van sach": "Tư vấn sách",
    "Huong dan muon": "Hướng dẫn mượn",
    "Nhap tai khoan": "Nhập tài khoản",
    "Dang nhap": "Đăng nhập",
    "Dang nhap MFA bang khuon mat": "Đăng nhập MFA bằng khuôn mặt",
    "Dang xuat": "Đăng xuất",
    "Kiem tra tai khoan": "Kiểm tra tài khoản",
    "Tao challenge": "Tạo challenge",
    "Luu session": "Lưu session",
    "Ghi FaceAuthLogs": "Ghi FaceAuthLogs",
    "Kiem tra action": "Kiểm tra hành động",
    "Loc theo danh muc": "Lọc theo danh mục",
    "Xem review": "Xem đánh giá",
    "Xem file preview": "Xem file preview",
    "Kiem tra ton kho": "Kiểm tra tồn kho",
    "Them gio hang": "Thêm giỏ hàng",
    "Muon sach": "Mượn sách",
    "Doc Sanpham": "Đọc Sanpham",
    "Doc Category": "Đọc Category",
    "Doc ProductReview": "Đọc ProductReview",
    "Tra view": "Trả view",
    "Them sach": "Thêm sách",
    "Sua sach": "Sửa sách",
    "Xoa/an sach": "Xóa/ẩn sách",
    "Quan ly danh muc": "Quản lý danh mục",
    "Quan ly kho": "Quản lý kho",
    "Quan ly file review": "Quản lý file review",
    "Validate du lieu": "Kiểm tra dữ liệu",
    "Cap nhat Sanpham": "Cập nhật Sanpham",
    "Cap nhat KhoHang": "Cập nhật KhoHang",
    "Cap nhat Category": "Cập nhật Category",
    "Xem danh sach don": "Xem danh sách đơn",
    "Xem chi tiet": "Xem chi tiết",
    "Cap nhat trang thai": "Cập nhật trạng thái",
    "Xu ly thanh toan": "Xử lý thanh toán",
    "Huy don": "Hủy đơn",
    "Doc Orders": "Đọc Orders",
    "Doc Order_Detail": "Đọc Order_Detail",
    "Cap nhat don": "Cập nhật đơn",
    "Tra ket qua": "Trả kết quả",
    "Nhan trang thai don hang": "Nhận trạng thái đơn hàng",
    "Xem lich su don": "Xem lịch sử đơn",
    "Xem don hang cua toi": "Xem đơn hàng của tôi",
    "Xem chi tiet hoa don": "Xem chi tiết hóa đơn",
    "Theo doi trang thai": "Theo dõi trạng thái",
    "Xem lich su muon": "Xem lịch sử mượn",
    "Kiem tra session": "Kiểm tra session",
    "Lay Orders": "Lấy Orders",
    "Lay Order_Detail": "Lấy Order_Detail",
    "Lay RentalRequests": "Lấy RentalRequests",
    "Xem nguoi dung": "Xem người dùng",
    "Cap nhat quyen": "Cập nhật quyền",
    "Kiem tra ho so": "Kiểm tra hồ sơ",
    "Xem lich su muon": "Xem lịch sử mượn",
    "Xem log xac thuc": "Xem log xác thực",
    "Doc User": "Đọc User",
    "Doc Quyen": "Đọc Quyen",
    "Doc RentalRequests": "Đọc RentalRequests",
    "Doc FaceAuthLogs": "Đọc FaceAuthLogs",
    "Face logs": "Log khuôn mặt",
    "Rental logs": "Log mượn/trả",
    "Geofence logs": "Log vị trí",
    "Cap nhat thong tin": "Cập nhật thông tin",
    "Doi mat khau": "Đổi mật khẩu",
    "Cap nhat Gmail": "Cập nhật Gmail",
    "Nhap CMND/CCCD": "Nhập CMND/CCCD",
    "Upload anh giay to": "Upload ảnh giấy tờ",
    "Quan ly yeu thich": "Quản lý yêu thích",
    "Goi OCR": "Gọi OCR",
    "So khop anh giay to neu co": "So khớp ảnh giấy tờ nếu có",
    "Dang nhap admin": "Đăng nhập admin",
    "Quan ly tai khoan admin": "Quản lý tài khoản admin",
    "Phan quyen": "Phân quyền",
    "Xem dashboard": "Xem dashboard",
    "Xem nhat ky": "Xem nhật ký",
    "Kiem tra quyen": "Kiểm tra quyền",
    "Cap nhat User/Quyen": "Cập nhật User/Quyen",
    "Tong hop thong ke": "Tổng hợp thống kê",
    "Ghi log": "Ghi log",
    "Cap nhat gio": "Cập nhật giỏ",
    "Dat hang": "Đặt hàng",
    "Kiem tra ho so muon": "Kiểm tra hồ sơ mượn",
    "Gui yeu cau muon": "Gửi yêu cầu mượn",
    "CheckStock": "CheckStock",
    "CheckActiveRental": "CheckActiveRental",
    "RentalProfileStatus": "RentalProfileStatus",
    "Sinh faceToken": "Sinh faceToken",
    "RequestRental": "RequestRental",
    "Thong bao Request/Approve/Reject/Return": "Thông báo Request/Approve/Reject/Return",
    "Duyet muon": "Duyệt mượn",
    "Tu choi": "Từ chối",
    "Xac nhan tra": "Xác nhận trả",
    "Danh dau qua han": "Đánh dấu quá hạn",
    "Them vao yeu thich": "Thêm vào yêu thích",
    "Xoa khoi yeu thich": "Xóa khỏi yêu thích",
    "Xem danh sach yeu thich": "Xem danh sách yêu thích",
    "Dong bo yeu thich local": "Đồng bộ yêu thích local",
    "Bien gioi he thong QLNhaSach": "Biên giới hệ thống QLNhaSach",
    "He thong Quan ly nha sach tich hop nhan dien khuon mat": "Hệ thống Quản lý nhà sách tích hợp nhận diện khuôn mặt",
    "Nguon doi chieu:": "Nguồn đối chiếu:",
}


def vi(text: str) -> str:
    return VI_TEXT.get(text, text)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(text: str, width: int) -> list[str]:
    # Rough character wrapping works consistently with proportional fonts for diagram labels.
    return textwrap.wrap(text, width=width, break_long_words=False) or [text]


def rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill, outline, width: int = 2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_actor(draw: ImageDraw.ImageDraw, x: int, y: int, name: str, color: tuple[int, int, int]) -> None:
    draw.ellipse((x - 18, y, x + 18, y + 36), outline=color, width=4)
    draw.line((x, y + 36, x, y + 96), fill=color, width=4)
    draw.line((x - 35, y + 58, x + 35, y + 58), fill=color, width=4)
    draw.line((x, y + 96, x - 32, y + 145), fill=color, width=4)
    draw.line((x, y + 96, x + 32, y + 145), fill=color, width=4)
    lines = wrap_text(vi(name), 16)
    yy = y + 156
    for line in lines:
        tw, _ = text_size(draw, line, FONT_SMALL)
        draw.text((x - tw / 2, yy), line, fill=color, font=FONT_SMALL)
        yy += 20


def draw_use_case(draw: ImageDraw.ImageDraw, cx: int, cy: int, label: str, fill, outline) -> tuple[int, int, int, int]:
    rx, ry = 150, 38
    box = (cx - rx, cy - ry, cx + rx, cy + ry)
    draw.ellipse(box, fill=fill, outline=outline, width=2)
    lines = wrap_text(vi(label), 28)
    total_h = len(lines) * 20
    yy = cy - total_h / 2
    for line in lines:
        tw, _ = text_size(draw, line, FONT_SMALL)
        draw.text((cx - tw / 2, yy), line, fill=(35, 47, 62), font=FONT_SMALL)
        yy += 20
    return box


def draw_connector(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], color=(107, 114, 128)) -> None:
    draw.line((p1[0], p1[1], p2[0], p2[1]), fill=color, width=2)


def render_diagram(diagram: UseCaseDiagram) -> Path:
    width, height = 1800, 1120
    image = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(image)

    # Header
    draw.rectangle((0, 0, width, 92), fill=(30, 64, 175))
    draw.text((50, 24), f"{diagram.code}. {vi(diagram.title)}", fill="white", font=FONT_TITLE)
    draw.text((50, 98), vi("He thong Quan ly nha sach tich hop nhan dien khuon mat"), fill=(51, 65, 85), font=FONT_SUBTITLE)

    # System boundary
    system_box = (310, 155, 1490, 970)
    rounded_rect(draw, system_box, 18, fill=(255, 255, 255), outline=(37, 99, 235), width=3)
    draw.text((system_box[0] + 24, system_box[1] + 16), vi("Bien gioi he thong QLNhaSach"), fill=(30, 64, 175), font=FONT_SUBTITLE)

    actor_items = list(diagram.actors.items())
    left_actors = actor_items[: math.ceil(len(actor_items) / 2)]
    right_actors = actor_items[math.ceil(len(actor_items) / 2) :]

    actor_positions: dict[str, tuple[int, int]] = {}
    for idx, (actor, _) in enumerate(left_actors):
        y = 205 + idx * max(150, 690 // max(1, len(left_actors)))
        actor_positions[actor] = (135, y)
        draw_actor(draw, 135, y, actor, (15, 76, 129))
    for idx, (actor, _) in enumerate(right_actors):
        y = 205 + idx * max(150, 690 // max(1, len(right_actors)))
        actor_positions[actor] = (1665, y)
        draw_actor(draw, 1665, y, actor, (126, 34, 206))

    # Use cases distributed by actor groups.
    palette = [
        ((239, 246, 255), (37, 99, 235)),
        ((240, 253, 244), (22, 163, 74)),
        ((255, 247, 237), (234, 88, 12)),
        ((250, 245, 255), (147, 51, 234)),
        ((236, 253, 245), (5, 150, 105)),
        ((254, 242, 242), (220, 38, 38)),
    ]

    all_cases: list[tuple[str, str]] = []
    for actor, cases in actor_items:
        for case in cases:
            all_cases.append((actor, case))

    cols = 3 if len(all_cases) > 12 else 2
    rows = math.ceil(len(all_cases) / cols)
    x_positions = [560, 900, 1240] if cols == 3 else [690, 1110]
    y_start = 265
    y_step = min(115, max(86, 620 // max(1, rows - 1))) if rows > 1 else 120

    case_centers: list[tuple[str, tuple[int, int]]] = []
    for idx, (actor, label) in enumerate(all_cases):
        col = idx % cols
        row = idx // cols
        cx = x_positions[col]
        cy = y_start + row * y_step
        fill, outline = palette[idx % len(palette)]
        draw_use_case(draw, cx, cy, label, fill, outline)
        case_centers.append((actor, (cx, cy)))

    for actor, center in case_centers:
        ax, ay = actor_positions[actor]
        if ax < width / 2:
            start = (ax + 42, ay + 70)
        else:
            start = (ax - 42, ay + 70)
        draw_connector(draw, start, center)

    # Notes/source footer.
    note_box = (330, 990, 1470, 1085)
    rounded_rect(draw, note_box, 12, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    draw.text((note_box[0] + 18, note_box[1] + 12), vi("Nguon doi chieu:"), fill=(51, 65, 85), font=FONT_SMALL)
    yy = note_box[1] + 38
    for note in diagram.notes:
        for line in wrap_text(note, 120):
            draw.text((note_box[0] + 18, yy), f"- {line}", fill=(51, 65, 85), font=FONT_SMALL)
            yy += 20

    out_path = OUT_DIR / diagram.filename
    image.save(out_path, "PNG", optimize=True)
    return out_path


def update_report(image_map: dict[str, Path]) -> list[str]:
    if not REPORT.exists():
        raise FileNotFoundError(f"Khong tim thay file bao cao: {REPORT}")

    if not BACKUP.exists():
        shutil.copy2(REPORT, BACKUP)

    temp_report = REPORT.with_suffix(".tmp.docx")
    replaced: list[str] = []
    with zipfile.ZipFile(REPORT, "r") as zin, zipfile.ZipFile(temp_report, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in image_map:
                data = image_map[item.filename].read_bytes()
                replaced.append(item.filename)
            zout.writestr(item, data)
    temp_report.replace(REPORT)
    return replaced


def append_history(rendered: list[Path], replaced: list[str]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"## {now} - Xay dung hinh use case va cap nhat BaoCaoMauSua_Version2",
        "",
        "- Tao/cap nhat thu muc `use_case`.",
        "- Sinh 11 hinh use case theo `KeHoach_DungLai_UseCase_SoDo_Version1.md`.",
        "- Sao luu bao cao truoc khi thay anh: `BaoCaoMauSua_Version2.before_usecase_update.docx`.",
        "- Thay the cac media use case trong `BaoCaoMauSua_Version2.docx`:",
    ]
    for media in replaced:
        diagram = next((d for d in DIAGRAMS if d.media_target == media), None)
        name = diagram.filename if diagram else ""
        code = diagram.code if diagram else ""
        lines.append(f"  - `{media}` <- `use_case/{name}` ({code})")
    lines.extend(["", "- Danh sach anh da sinh:"])
    for path in rendered:
        lines.append(f"  - `use_case/{path.name}`")
    lines.append("")

    previous = HISTORY.read_text(encoding="utf-8") if HISTORY.exists() else "# Lich su xay dung hinh use case\n\n"
    HISTORY.write_text(previous + "\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rendered = [render_diagram(diagram) for diagram in DIAGRAMS]
    image_map = {diagram.media_target: OUT_DIR / diagram.filename for diagram in DIAGRAMS}
    replaced = update_report(image_map)
    append_history(rendered, replaced)
    print(f"Generated {len(rendered)} use case images in {OUT_DIR}")
    print(f"Replaced {len(replaced)} images in {REPORT.name}")
    print(f"History written to {HISTORY.name}")


if __name__ == "__main__":
    main()
