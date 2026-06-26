from __future__ import annotations

import html
import math
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_DIR = ROOT / "use_case_drawio"
EXPORT_DIR = ROOT / "use_case_drawio_exports"
REPORT = ROOT / "BaoCaoMauSua_Version2.docx"
BACKUP = ROOT / "BaoCaoMauSua_Version2.before_drawio_usecase_update.docx"
FALLBACK_REPORT = ROOT / "BaoCaoMauSua_Version2_DrawIOUseCase.docx"
HISTORY = ROOT / "LichSuXayDungHinhUseCase.md"


@dataclass(frozen=True)
class Diagram:
    code: str
    title: str
    drawio_name: str
    png_name: str
    media_target: str
    actors: list[str]
    usecases: list[str]
    externals: list[str]
    associations: list[tuple[str, str]]
    extends: list[tuple[str, str]]
    source_note: str


DIAGRAMS = [
    Diagram(
        "Hình 21",
        "Biểu đồ use case chính",
        "hinh_21_usecase_chinh.drawio",
        "hinh_21_usecase_chinh.png",
        "word/media/image3.png",
        ["Khách vãng lai", "Người dùng", "Quản trị viên"],
        [
            "Xem sản phẩm",
            "Tìm kiếm sách",
            "Đăng ký / Đăng nhập",
            "Quản lý hồ sơ",
            "Đặt hàng",
            "Mượn sách",
            "Đánh giá / Yêu thích",
            "Quản lý sản phẩm",
            "Quản lý đơn hàng",
            "Quản lý người dùng",
            "Xem log / Thống kê",
        ],
        ["Face API", "Gmail", "Chatbox"],
        [
            ("Khách vãng lai", "Xem sản phẩm"),
            ("Khách vãng lai", "Tìm kiếm sách"),
            ("Người dùng", "Đăng ký / Đăng nhập"),
            ("Người dùng", "Quản lý hồ sơ"),
            ("Người dùng", "Đặt hàng"),
            ("Người dùng", "Mượn sách"),
            ("Người dùng", "Đánh giá / Yêu thích"),
            ("Quản trị viên", "Quản lý sản phẩm"),
            ("Quản trị viên", "Quản lý đơn hàng"),
            ("Quản trị viên", "Quản lý người dùng"),
            ("Quản trị viên", "Xem log / Thống kê"),
        ],
        [("Face API", "Đăng ký / Đăng nhập"), ("Face API", "Mượn sách"), ("Gmail", "Mượn sách"), ("Chatbox", "Xem sản phẩm")],
        "ProductController, UsersController, RentalController, FaceAuthController, GmailNotificationService",
    ),
    Diagram(
        "Hình 22",
        "Biểu đồ use case Đăng nhập",
        "hinh_22_usecase_dang_nhap.drawio",
        "hinh_22_usecase_dang_nhap.png",
        "word/media/image4.png",
        ["Người dùng"],
        ["Nhập tài khoản", "Đăng nhập", "Tạo challenge", "Kiểm tra hành động", "Xác thực khuôn mặt", "Ghi log đăng nhập"],
        ["Face API"],
        [("Người dùng", "Nhập tài khoản"), ("Người dùng", "Đăng nhập"), ("Người dùng", "Xác thực khuôn mặt")],
        [("Tạo challenge", "Đăng nhập"), ("Kiểm tra hành động", "Xác thực khuôn mặt"), ("Face API", "Xác thực khuôn mặt"), ("Ghi log đăng nhập", "Đăng nhập")],
        "UsersController.Login, FaceAuthController.AuthenticateFaceLogin, /api/face/action-check",
    ),
    Diagram(
        "Hình 23",
        "Biểu đồ use case Xem sản phẩm",
        "hinh_23_usecase_xem_san_pham.drawio",
        "hinh_23_usecase_xem_san_pham.png",
        "word/media/image5.png",
        ["Khách vãng lai", "Người dùng"],
        ["Xem danh sách sách", "Tìm kiếm", "Lọc danh mục", "Xem chi tiết", "Xem đánh giá", "Xem file preview", "Kiểm tra tồn kho"],
        [],
        [
            ("Khách vãng lai", "Xem danh sách sách"),
            ("Khách vãng lai", "Tìm kiếm"),
            ("Khách vãng lai", "Xem chi tiết"),
            ("Người dùng", "Xem đánh giá"),
            ("Người dùng", "Xem file preview"),
            ("Người dùng", "Kiểm tra tồn kho"),
        ],
        [("Lọc danh mục", "Xem danh sách sách"), ("Xem đánh giá", "Xem chi tiết"), ("Xem file preview", "Xem chi tiết")],
        "ProductController.Index/Search/ListProduct/Detail/ReviewFilePreview",
    ),
    Diagram(
        "Hình 24",
        "Biểu đồ use case Quản lý sản phẩm",
        "hinh_24_usecase_quan_ly_san_pham.drawio",
        "hinh_24_usecase_quan_ly_san_pham.png",
        "word/media/image6.png",
        ["Quản trị viên"],
        ["Thêm sách", "Sửa sách", "Ẩn/Xóa sách", "Quản lý danh mục", "Quản lý kho", "Quản lý file review", "Cập nhật tồn kho"],
        ["CSDL"],
        [("Quản trị viên", "Thêm sách"), ("Quản trị viên", "Sửa sách"), ("Quản trị viên", "Ẩn/Xóa sách"), ("Quản trị viên", "Quản lý kho")],
        [("CSDL", "Thêm sách"), ("CSDL", "Sửa sách"), ("CSDL", "Cập nhật tồn kho"), ("Quản lý danh mục", "Thêm sách"), ("Quản lý file review", "Sửa sách")],
        "ProductController, SanphamDraw, Sanpham, Category, KhoHang",
    ),
    Diagram(
        "Hình 25",
        "Biểu đồ use case Quản lý đơn hàng",
        "hinh_25_usecase_quan_ly_don_hang.drawio",
        "hinh_25_usecase_quan_ly_don_hang.png",
        "word/media/image7.png",
        ["Quản trị viên"],
        ["Xem danh sách đơn", "Xem chi tiết đơn", "Cập nhật trạng thái", "Xử lý thanh toán", "Hủy đơn", "Tra cứu hóa đơn"],
        ["CSDL"],
        [("Quản trị viên", "Xem danh sách đơn"), ("Quản trị viên", "Xem chi tiết đơn"), ("Quản trị viên", "Cập nhật trạng thái")],
        [("CSDL", "Xem danh sách đơn"), ("CSDL", "Xem chi tiết đơn"), ("Xử lý thanh toán", "Cập nhật trạng thái"), ("Hủy đơn", "Cập nhật trạng thái")],
        "CartController, Orders, Order_Detail",
    ),
    Diagram(
        "Hình 26",
        "Biểu đồ use case Đơn hàng của tôi",
        "hinh_26_usecase_don_hang_cua_toi.drawio",
        "hinh_26_usecase_don_hang_cua_toi.png",
        "word/media/image8.png",
        ["Người dùng"],
        ["Xem đơn hàng của tôi", "Xem chi tiết hóa đơn", "Theo dõi trạng thái", "Xem lịch sử mượn", "Xem chi tiết mượn"],
        ["CSDL"],
        [("Người dùng", "Xem đơn hàng của tôi"), ("Người dùng", "Xem chi tiết hóa đơn"), ("Người dùng", "Xem lịch sử mượn")],
        [("CSDL", "Xem đơn hàng của tôi"), ("CSDL", "Xem lịch sử mượn"), ("Theo dõi trạng thái", "Xem đơn hàng của tôi"), ("Xem chi tiết mượn", "Xem lịch sử mượn")],
        "UsersController.ChiTietHoaDon, RentalController.MyRentals",
    ),
    Diagram(
        "Hình 27",
        "Biểu đồ use case Quản lý người dùng",
        "hinh_27_usecase_quan_ly_nguoi_dung.drawio",
        "hinh_27_usecase_quan_ly_nguoi_dung.png",
        "word/media/image9.png",
        ["Quản trị viên"],
        ["Xem người dùng", "Cập nhật quyền", "Kiểm tra hồ sơ", "Xem lịch sử mượn", "Xem log xác thực", "Khóa/Mở tài khoản"],
        ["Log API"],
        [("Quản trị viên", "Xem người dùng"), ("Quản trị viên", "Cập nhật quyền"), ("Quản trị viên", "Kiểm tra hồ sơ")],
        [("Log API", "Xem log xác thực"), ("Xem lịch sử mượn", "Xem người dùng"), ("Khóa/Mở tài khoản", "Cập nhật quyền")],
        "UsersController, LogsController, User, Quyen, FaceAuthLog, RentalRequest",
    ),
    Diagram(
        "Hình 28",
        "Biểu đồ use case Quản lý thông tin tài khoản",
        "hinh_28_usecase_quan_ly_thong_tin_tai_khoan.drawio",
        "hinh_28_usecase_quan_ly_thong_tin_tai_khoan.png",
        "word/media/image10.png",
        ["Người dùng"],
        ["Cập nhật thông tin", "Đổi mật khẩu", "Cập nhật Gmail", "Nhập CMND/CCCD", "Upload ảnh giấy tờ", "OCR CMND/CCCD", "Quản lý yêu thích"],
        ["Face API"],
        [("Người dùng", "Cập nhật thông tin"), ("Người dùng", "Đổi mật khẩu"), ("Người dùng", "Upload ảnh giấy tờ"), ("Người dùng", "Quản lý yêu thích")],
        [("OCR CMND/CCCD", "Upload ảnh giấy tờ"), ("Face API", "OCR CMND/CCCD"), ("Cập nhật Gmail", "Cập nhật thông tin"), ("Nhập CMND/CCCD", "Cập nhật thông tin")],
        "UsersController.ProfileUser/EditUser, RentalController.UpdateRentalProfile, FaceAuthController.OcrCmnd",
    ),
    Diagram(
        "Hình 29",
        "Biểu đồ use case Quản lý quản trị viên",
        "hinh_29_usecase_quan_ly_quan_tri_vien.drawio",
        "hinh_29_usecase_quan_ly_quan_tri_vien.png",
        "word/media/image11.png",
        ["Quản trị viên"],
        ["Đăng nhập admin", "Quản lý tài khoản admin", "Phân quyền", "Xem dashboard", "Xem nhật ký", "Tổng hợp thống kê"],
        ["CSDL"],
        [("Quản trị viên", "Đăng nhập admin"), ("Quản trị viên", "Quản lý tài khoản admin"), ("Quản trị viên", "Xem dashboard")],
        [("Phân quyền", "Quản lý tài khoản admin"), ("CSDL", "Tổng hợp thống kê"), ("Xem nhật ký", "Xem dashboard")],
        "UsersController, Quyen, LogRepository",
    ),
    Diagram(
        "Hình 210",
        "Biểu đồ use case Quản lý giỏ hàng và quy trình mượn sách",
        "hinh_210_usecase_gio_hang_muon_sach.drawio",
        "hinh_210_usecase_gio_hang_muon_sach.png",
        "word/media/image12.png",
        ["Người dùng", "Quản trị viên"],
        ["Thêm giỏ hàng", "Cập nhật giỏ", "Đặt hàng", "Kiểm tra hồ sơ mượn", "Xác thực khuôn mặt", "Gửi yêu cầu mượn", "Duyệt mượn", "Từ chối", "Xác nhận trả", "Đánh dấu quá hạn"],
        ["Face API", "Gmail"],
        [
            ("Người dùng", "Thêm giỏ hàng"),
            ("Người dùng", "Đặt hàng"),
            ("Người dùng", "Kiểm tra hồ sơ mượn"),
            ("Người dùng", "Xác thực khuôn mặt"),
            ("Người dùng", "Gửi yêu cầu mượn"),
            ("Quản trị viên", "Duyệt mượn"),
            ("Quản trị viên", "Từ chối"),
            ("Quản trị viên", "Xác nhận trả"),
        ],
        [("Face API", "Xác thực khuôn mặt"), ("Gmail", "Gửi yêu cầu mượn"), ("Cập nhật giỏ", "Thêm giỏ hàng"), ("Đánh dấu quá hạn", "Duyệt mượn")],
        "CartController, RentalController, FaceAuthController, FaceRentalTokenService, GmailNotificationService",
    ),
    Diagram(
        "Hình 211",
        "Biểu đồ use case Quản lý danh sách yêu thích",
        "hinh_211_usecase_danh_sach_yeu_thich.drawio",
        "hinh_211_usecase_danh_sach_yeu_thich.png",
        "word/media/image13.png",
        ["Người dùng"],
        ["Thêm vào yêu thích", "Xóa khỏi yêu thích", "Xem danh sách yêu thích", "Đồng bộ yêu thích local", "Lấy sản phẩm yêu thích"],
        ["CSDL"],
        [("Người dùng", "Thêm vào yêu thích"), ("Người dùng", "Xóa khỏi yêu thích"), ("Người dùng", "Xem danh sách yêu thích")],
        [("Đồng bộ yêu thích local", "Xem danh sách yêu thích"), ("CSDL", "Lấy sản phẩm yêu thích"), ("Lấy sản phẩm yêu thích", "Xem danh sách yêu thích")],
        "UsersController.ToggleFavorite/Favorites/SyncLocalFavorites, ProductFavorite",
    ),
]


def load_font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(30, True)
FONT_TEXT = load_font(23)
FONT_SMALL = load_font(18)


def positions(diagram: Diagram):
    width, height = 1600, 900
    actor_pos = {}
    if len(diagram.actors) == 1:
        actor_pos[diagram.actors[0]] = (150, 360)
    else:
        step = 520 // max(1, len(diagram.actors) - 1)
        for idx, actor in enumerate(diagram.actors):
            actor_pos[actor] = (150, 180 + idx * step)

    usecase_pos = {}
    cols = 2 if len(diagram.usecases) <= 7 else 3
    xs = [580, 920] if cols == 2 else [500, 800, 1100]
    rows = math.ceil(len(diagram.usecases) / cols)
    y0 = 190
    y_step = 130 if rows <= 4 else 105
    for idx, uc in enumerate(diagram.usecases):
        usecase_pos[uc] = (xs[idx % cols], y0 + (idx // cols) * y_step)

    external_pos = {}
    if len(diagram.externals) == 1:
        external_pos[diagram.externals[0]] = (1370, 360)
    else:
        step = 460 // max(1, len(diagram.externals) - 1)
        for idx, ext in enumerate(diagram.externals):
            external_pos[ext] = (1370, 230 + idx * step)
    return width, height, actor_pos, usecase_pos, external_pos


def mx_cell(id_: str, value: str, style: str, x: int, y: int, w: int, h: int, parent: str = "1") -> str:
    return (
        f'<mxCell id="{id_}" value="{escape(value)}" style="{style}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )


def mx_edge(id_: str, value: str, source: str, target: str, style: str) -> str:
    return (
        f'<mxCell id="{id_}" value="{escape(value)}" style="{style}" edge="1" parent="1" source="{source}" target="{target}">'
        '<mxGeometry relative="1" as="geometry"/></mxCell>'
    )


def make_drawio(diagram: Diagram) -> Path:
    DRAWIO_DIR.mkdir(exist_ok=True)
    width, height, actor_pos, usecase_pos, external_pos = positions(diagram)
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        mx_cell("title", f"{diagram.code}. {diagram.title}", "text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;align=left;", 30, 20, 900, 40),
    ]
    ids: dict[str, str] = {}
    idx = 2
    actor_style = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;fontSize=15;"
    ellipse_style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#ffffff;strokeColor=#000000;fontSize=15;"
    for actor, (x, y) in actor_pos.items():
        cid = f"a{idx}"
        ids[actor] = cid
        cells.append(mx_cell(cid, actor, actor_style, x - 35, y - 65, 70, 110))
        idx += 1
    for uc, (x, y) in usecase_pos.items():
        cid = f"u{idx}"
        ids[uc] = cid
        cells.append(mx_cell(cid, uc, ellipse_style, x - 115, y - 55, 230, 110))
        idx += 1
    for ext, (x, y) in external_pos.items():
        cid = f"e{idx}"
        ids[ext] = cid
        cells.append(mx_cell(cid, ext, ellipse_style, x - 115, y - 55, 230, 110))
        idx += 1

    assoc_style = "endArrow=none;html=1;rounded=0;strokeColor=#000000;"
    extend_style = "endArrow=open;html=1;rounded=0;dashed=1;strokeColor=#000000;fontSize=15;"
    for source, target in diagram.associations:
        if source in ids and target in ids:
            cells.append(mx_edge(f"r{idx}", "", ids[source], ids[target], assoc_style))
            idx += 1
    for source, target in diagram.extends:
        if source in ids and target in ids:
            cells.append(mx_edge(f"r{idx}", "<<extend>>", ids[source], ids[target], extend_style))
            idx += 1

    graph = (
        f'<mxfile host="app.diagrams.net" modified="{datetime.utcnow().isoformat()}Z" agent="Codex" version="24.7.17">'
        f'<diagram id="{html.escape(diagram.code)}" name="{html.escape(diagram.code)}">'
        f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">'
        f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
    )
    out = DRAWIO_DIR / diagram.drawio_name
    out.write_text(graph, encoding="utf-8")
    return out


def text_center(draw: ImageDraw.ImageDraw, xy, text: str, font, fill=(0, 0, 0)):
    x, y, w, h = xy
    lines = []
    for part in text.split(" "):
        candidate = (lines[-1] + " " + part) if lines else part
        if lines and draw.textbbox((0, 0), candidate, font=font)[2] > w - 26:
            lines.append(part)
        elif lines:
            lines[-1] = candidate
        else:
            lines.append(part)
    total_h = len(lines) * 28
    yy = y + h / 2 - total_h / 2
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        draw.text((x + w / 2 - (box[2] - box[0]) / 2, yy), line, font=font, fill=fill)
        yy += 28


def draw_actor(draw: ImageDraw.ImageDraw, x: int, y: int, name: str):
    draw.ellipse((x - 22, y - 70, x + 22, y - 26), outline=(0, 0, 0), width=2)
    draw.line((x, y - 26, x, y + 42), fill=(0, 0, 0), width=2)
    draw.line((x - 48, y, x + 48, y), fill=(0, 0, 0), width=2)
    draw.line((x, y + 42, x - 42, y + 95), fill=(0, 0, 0), width=2)
    draw.line((x, y + 42, x + 42, y + 95), fill=(0, 0, 0), width=2)
    box = draw.textbbox((0, 0), name, font=FONT_TEXT)
    draw.text((x - (box[2] - box[0]) / 2, y + 108), name, font=FONT_TEXT, fill=(0, 0, 0))


def draw_dashed_line(draw: ImageDraw.ImageDraw, p1, p2, dash=10, gap=7):
    x1, y1 = p1
    x2, y2 = p2
    length = math.hypot(x2 - x1, y2 - y1)
    if length == 0:
        return
    dx, dy = (x2 - x1) / length, (y2 - y1) / length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line((x1 + dx * pos, y1 + dy * pos, x1 + dx * end, y1 + dy * end), fill=(0, 0, 0), width=1)
        pos += dash + gap
    # Open arrow head at target.
    angle = math.atan2(y2 - y1, x2 - x1)
    for a in (angle + math.pi * 0.83, angle - math.pi * 0.83):
        draw.line((x2, y2, x2 + math.cos(a) * 18, y2 + math.sin(a) * 18), fill=(0, 0, 0), width=1)


def make_png(diagram: Diagram) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    width, height, actor_pos, usecase_pos, external_pos = positions(diagram)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    draw.text((30, 25), f"{diagram.code}. {diagram.title}", font=FONT_TITLE, fill=(0, 0, 0))

    rects = {}
    for actor, (x, y) in actor_pos.items():
        rects[actor] = (x - 35, y - 65, 70, 110)
    for uc, (x, y) in usecase_pos.items():
        rects[uc] = (x - 115, y - 55, 230, 110)
    for ext, (x, y) in external_pos.items():
        rects[ext] = (x - 115, y - 55, 230, 110)

    def center(name):
        x, y, w, h = rects[name]
        return (x + w / 2, y + h / 2)

    for source, target in diagram.associations:
        if source in rects and target in rects:
            draw.line((*center(source), *center(target)), fill=(0, 0, 0), width=2)
    extend_labels = []
    for source, target in diagram.extends:
        if source in rects and target in rects:
            p1, p2 = center(source), center(target)
            draw_dashed_line(draw, p1, p2)
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            extend_labels.append((mx, my))

    # Draw vertices after edges so connector lines do not cut through labels.
    for actor, (x, y) in actor_pos.items():
        draw_actor(draw, x, y, actor)
    for uc, (x, y) in usecase_pos.items():
        rect = (x - 115, y - 55, x + 115, y + 55)
        draw.ellipse(rect, fill="white", outline=(0, 0, 0), width=2)
        text_center(draw, (x - 115, y - 55, 230, 110), uc, FONT_TEXT)
    for ext, (x, y) in external_pos.items():
        rect = (x - 115, y - 55, x + 115, y + 55)
        draw.ellipse(rect, fill="white", outline=(0, 0, 0), width=2)
        text_center(draw, (x - 115, y - 55, 230, 110), ext, FONT_TEXT)

    for mx, my in extend_labels:
        label = "<<extend>>"
        box = draw.textbbox((0, 0), label, font=FONT_SMALL)
        w, h = box[2] - box[0], box[3] - box[1]
        draw.rectangle((mx - w / 2 - 4, my - h / 2 - 3, mx + w / 2 + 4, my + h / 2 + 3), fill="white")
        draw.text((mx - w / 2, my - h / 2), label, font=FONT_SMALL, fill=(0, 0, 0))

    draw.text((30, height - 45), f"Nguồn đối chiếu: {diagram.source_note}", font=FONT_SMALL, fill=(0, 0, 0))
    out = EXPORT_DIR / diagram.png_name
    img.save(out, "PNG", optimize=True)
    return out


def update_report(image_map: dict[str, Path]) -> tuple[list[str], Path, str]:
    if not BACKUP.exists():
        shutil.copy2(REPORT, BACKUP)
    temp = REPORT.with_suffix(".tmp.docx")
    replaced = []
    with zipfile.ZipFile(REPORT, "r") as zin, zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in image_map:
                data = image_map[item.filename].read_bytes()
                replaced.append(item.filename)
            zout.writestr(item, data)
    try:
        temp.replace(REPORT)
        return replaced, REPORT, "updated_original"
    except PermissionError:
        shutil.copy2(temp, FALLBACK_REPORT)
        return replaced, FALLBACK_REPORT, "saved_fallback_because_original_locked"


def append_history(drawios: list[Path], pngs: list[Path], replaced: list[str], output_report: Path, status: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"## {now} - Sinh file draw.io use case va cap nhat anh trong BaoCaoMauSua_Version2",
        "",
        "- Tao/cap nhat thu muc `use_case_drawio` chua file `.drawio` co the import len diagrams.net de sua.",
        "- Tao/cap nhat thu muc `use_case_drawio_exports` chua PNG xuat tu cung layout de thay vao Word.",
        "- Style: UML actor, use case ellipse nen trang vien den, association line, quan he `<<extend>>` net dut mui ten mo.",
        "- Backup truoc khi thay anh: `BaoCaoMauSua_Version2.before_drawio_usecase_update.docx`.",
        f"- Ket qua cap nhat Word: `{output_report.name}` ({status}).",
        "- Media da thay:",
    ]
    for media in replaced:
        diagram = next(d for d in DIAGRAMS if d.media_target == media)
        lines.append(f"  - `{media}` <- `use_case_drawio_exports/{diagram.png_name}`; source `use_case_drawio/{diagram.drawio_name}` ({diagram.code})")
    lines.extend(["", "- File draw.io da sinh:"])
    for path in drawios:
        lines.append(f"  - `use_case_drawio/{path.name}`")
    lines.append("")
    previous = HISTORY.read_text(encoding="utf-8") if HISTORY.exists() else "# Lich su xay dung hinh use case\n\n"
    HISTORY.write_text(previous + "\n".join(lines), encoding="utf-8")


def main():
    drawios = [make_drawio(d) for d in DIAGRAMS]
    pngs = [make_png(d) for d in DIAGRAMS]
    image_map = {d.media_target: EXPORT_DIR / d.png_name for d in DIAGRAMS}
    replaced, output_report, status = update_report(image_map)
    append_history(drawios, pngs, replaced, output_report, status)
    print(f"Generated {len(drawios)} draw.io files in {DRAWIO_DIR}")
    print(f"Generated {len(pngs)} exported PNG files in {EXPORT_DIR}")
    print(f"Replaced {len(replaced)} use case images in {output_report.name}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
