from __future__ import annotations

import math
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
import unicodedata
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_DIR = ROOT / "database_drawio"
EXPORT_DIR = ROOT / "database_drawio_exports"
REPORT = ROOT / "BaoCaoMauSua_Version3.docx"
BACKUP = ROOT / "BaoCaoMauSua_Version3.before_database_update.docx"
FALLBACK_REPORT = ROOT / "BaoCaoMauSua_Version3_DatabaseDrawIO.docx"
HISTORY = ROOT / "LichSuXayDungHinhDatabase.md"


@dataclass(frozen=True)
class TableSpec:
    name: str
    fields: list[str]
    note: str


@dataclass(frozen=True)
class DiagramSpec:
    code: str
    title: str
    drawio_name: str
    png_name: str
    media_target: str
    tables: list[TableSpec]
    relations: list[tuple[str, str, str]]
    source: str


def t(name: str, fields: list[str], note: str = "") -> TableSpec:
    return TableSpec(name, fields, note)


TABLES = {
    "Users": t(
        "User / Users",
        [
            "PK IDUser: long",
            "UserName, PassWord, Name",
            "Email, NotificationEmail, Phone",
            "Adress, Status, IDQuyen",
            "IdentityNumber, IdentityFullName",
            "IdentityDateOfBirth, IdentityGender",
            "IdentityAddress, IdentityIssueDate",
            "IdentityCardFront/BackImagePath",
            "IdentityFaceConfidence",
        ],
        "Nguồn: Mood\\EF2\\User.cs",
    ),
    "RentalRequests": t(
        "RentalRequests",
        [
            "PK ID: int",
            "FK UserID -> User.IDUser",
            "FK ProductID -> Sanpham.IDContent",
            "Quantity, Status",
            "RequestedAt, RequestDate",
            "BorrowDays, ExpectedReturnDate",
            "ApprovedAt, ReturnedAt, ActualReturnDate",
            "AdminID, RejectReason, Details",
            "IdentityNumber, IdentityFullName",
            "IdentityCardFront/BackImagePath",
            "Identity OCR fields + raw JSON",
        ],
        "Nguồn: RentalRequest.cs, migration identity_card_rental_flow",
    ),
    "Slides": t("Slide", ["PK Id", "Image", "DisPlayOrder", "Title", "Link", "Status"], "Nguồn: Slide.cs"),
    "StoreLocations": t(
        "StoreLocations",
        [
            "PK ID: int",
            "StoreName, Address, Phone, Email",
            "Latitude, Longitude",
            "GeofenceRadius, IsActive",
            "IconPath, BannerPath",
            "WelcomeTitle, WelcomeMessage",
            "AboutContent, MissionContent, SortOrder",
        ],
        "Nguồn: StoreLocation.cs, 20260508_add_stores.sql",
    ),
    "Categories": t(
        "Category / Categories",
        ["PK IDCategory", "TenTheloai", "MetaTitle", "ParentID", "SEOTitle", "NgayTao", "DisPlayOrder", "MetaDescriptions", "Status"],
        "Nguồn: Category.cs",
    ),
    "ProductFavorites": t(
        "ProductFavorites",
        ["PK ID: long", "FK UserID -> User.IDUser", "FK ProductID -> Sanpham.IDContent", "CreatedAt", "Unique(UserID, ProductID)"],
        "Nguồn: ProductFavorite.cs, 20260509_add_product_favorites.sql",
    ),
    "ProductReviews": t(
        "ProductReviews",
        ["PK IDReview: long", "FK ProductID -> Sanpham.IDContent", "FK UserID -> User.IDUser", "UserName", "Rating", "Comment", "CreatedAt", "Status"],
        "Nguồn: ProductReview.cs, 20260510_add_product_reviews_version5.sql",
    ),
    "FaceAuthLogs": t(
        "FaceAuthLogs",
        ["PK ID: int", "UserID", "Action", "Timestamp", "IP, DeviceInfo", "ImagePath", "Result", "Confidence", "ErrorMessage", "RequestId", "Purpose", "ErrorCode", "LivenessPassed"],
        "Nguồn: FaceAuthLog.cs, 20260508_add_logs.sql",
    ),
    "FaceSamples": t(
        "FaceSamples / face profile",
        ["Logical UserID", "ImagePath / FaceSampleStoragePath", "Embedding profile", "Quality result", "CreatedAt/UpdatedAt", "Storage: face_auth_api\\face_profiles"],
        "Cấu trúc logic/lưu ngoài DB. Nguồn: face_auth_api\\app.py, Web.config",
    ),
    "Orders": t(
        "Orders",
        ["PK IDOder: long", "CustomerID", "NgayTao", "ShipName", "ShipMobile", "ShipAddress", "ShipEmail", "Status", "GiaoHang, NhanHang", "DeliveryPaymentMethod", "StatusPayment", "OrderCode"],
        "Nguồn: Orders.cs",
    ),
    "OrderDetails": t(
        "Order_Detail / OrderDetails",
        ["PK/FK ProductID -> Sanpham.IDContent", "PK/FK OderID -> Orders.IDOder", "Quanlity", "Price"],
        "Nguồn: Order_Detail.cs",
    ),
    "Sanphams": t(
        "Sanpham / Sanphams",
        ["PK IDContent: long", "Name, MetaTitle", "TacGia, NhaXuatBan", "Soluong, TonKho", "Images, CategoryID", "NgayTao, IDNguoiTao", "Status, Tophot", "Mota, ChiTiet", "IDNCC, GiaTien, GiaNhap, PriceSale", "ReviewFilePath, ReviewFileName, YoutubeUrl"],
        "Nguồn: Sanpham.cs",
    ),
    "Quyens": t("Quyen / Quyens", ["PK IDQuyen: long", "TenQuyen", "Status"], "Nguồn: Quyen.cs"),
    "RentalLogs": t(
        "RentalLogs",
        ["PK ID: int", "FK RentalID -> RentalRequests.ID", "UserID", "ActorUserID", "Action", "Timestamp", "Details", "OldStatus", "NewStatus"],
        "Nguồn: RentalLog.cs, 20260508_add_logs.sql",
    ),
    "UserQuyens": t(
        "UserQuyens (logic)",
        ["User.IDQuyen -> Quyen.IDQuyen", "1 User có 1 quyền chính", "Không có bảng vật lý UserQuyens riêng trong source hiện tại"],
        "Cấu trúc logic theo User.cs và Quyen.cs",
    ),
    "FaceRentalTokens": t(
        "FaceRentalTokens (memory)",
        ["Token", "UserID", "ProductID", "ExpiresAt", "Consumed", "Purpose = rental_verify", "TTL = FaceAuthRentalTokenMinutes"],
        "Cấu trúc logic trong FaceRentalTokenService.cs",
    ),
    "GeofenceLogs": t(
        "GeofenceLogs",
        ["PK ID: int", "UserID", "StoreID", "IsInZone", "Timestamp", "UserLat, UserLon", "Distance", "AllowedRadiusKm", "StoreName"],
        "Nguồn: GeofenceLog.cs, 20260508_add_logs.sql",
    ),
}


def diag(num: int, title: str, tables: list[TableSpec], relations=None, source: str = "") -> DiagramSpec:
    return DiagramSpec(
        f"Hình 3-{num}",
        title,
        f"hinh_3_{num:02d}_{slug(title)}.drawio",
        f"hinh_3_{num:02d}_{slug(title)}.png",
        f"word/media/image{13 + num}.png",
        tables,
        relations or [],
        source,
    )


def slug(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    out = unicodedata.normalize("NFD", text.lower())
    out = "".join(c for c in out if unicodedata.category(c) != "Mn")
    out = out.replace("/", "_").replace(" ", "_")
    return "".join(c for c in out if c.isalnum() or c == "_")[:60]


OVERVIEW_TABLES = [
    TABLES["Users"],
    TABLES["Quyens"],
    TABLES["Sanphams"],
    TABLES["Categories"],
    TABLES["Orders"],
    TABLES["OrderDetails"],
    TABLES["RentalRequests"],
    TABLES["ProductFavorites"],
    TABLES["ProductReviews"],
    TABLES["FaceAuthLogs"],
    TABLES["RentalLogs"],
    TABLES["StoreLocations"],
    TABLES["GeofenceLogs"],
]

OVERVIEW_RELATIONS = [
    ("User / Users", "Quyen / Quyens", "IDQuyen"),
    ("Sanpham / Sanphams", "Category / Categories", "CategoryID"),
    ("Orders", "User / Users", "CustomerID"),
    ("Order_Detail / OrderDetails", "Orders", "OderID"),
    ("Order_Detail / OrderDetails", "Sanpham / Sanphams", "ProductID"),
    ("RentalRequests", "User / Users", "UserID"),
    ("RentalRequests", "Sanpham / Sanphams", "ProductID"),
    ("ProductFavorites", "User / Users", "UserID"),
    ("ProductFavorites", "Sanpham / Sanphams", "ProductID"),
    ("ProductReviews", "User / Users", "UserID"),
    ("ProductReviews", "Sanpham / Sanphams", "ProductID"),
    ("RentalLogs", "RentalRequests", "RentalID"),
    ("GeofenceLogs", "StoreLocations", "StoreID"),
]

DIAGRAMS = [
    diag(1, "Cấu trúc database của dự án sau khi thiết kế", OVERVIEW_TABLES, OVERVIEW_RELATIONS, "QuanLySachDBContext, LogDbContext, sql/migrations"),
    diag(2, "Chi tiết bảng Users", [TABLES["Users"]], source="Mood\\EF2\\User.cs"),
    diag(3, "Chi tiết bảng RentalRequests", [TABLES["RentalRequests"]], source="Mood\\EF2\\RentalRequest.cs"),
    diag(4, "Chi tiết bảng Slides", [TABLES["Slides"]], source="Mood\\EF2\\Slide.cs"),
    diag(5, "Chi tiết bảng StoreLocations", [TABLES["StoreLocations"]], source="Mood\\EF2\\StoreLocation.cs"),
    diag(6, "Chi tiết bảng Categories", [TABLES["Categories"]], source="Mood\\EF2\\Category.cs"),
    diag(7, "Chi tiết bảng ProductFavorites", [TABLES["ProductFavorites"]], source="Mood\\EF2\\ProductFavorite.cs"),
    diag(8, "Chi tiết bảng ProductReviews", [TABLES["ProductReviews"]], source="Mood\\EF2\\ProductReview.cs"),
    diag(9, "Chi tiết bảng Users - hồ sơ định danh", [t("User / Users - Identity Profile", TABLES["Users"].fields[4:], "Phần hồ sơ định danh trong User.cs")], source="Mood\\EF2\\User.cs"),
    diag(10, "Chi tiết bảng FaceAuthLogs", [TABLES["FaceAuthLogs"]], source="Mood\\EF2\\FaceAuthLog.cs"),
    diag(11, "Chi tiết bảng ProductFavorites - quan hệ User và sách", [TABLES["ProductFavorites"], TABLES["Users"], TABLES["Sanphams"]], [("ProductFavorites", "User / Users", "UserID"), ("ProductFavorites", "Sanpham / Sanphams", "ProductID")], "ProductFavorite.cs"),
    diag(12, "Chi tiết bảng FaceSamples", [TABLES["FaceSamples"]], source="face_auth_api\\app.py"),
    diag(13, "Chi tiết bảng Orders", [TABLES["Orders"]], source="Mood\\EF2\\Orders.cs"),
    diag(14, "Chi tiết bảng OrderDetails", [TABLES["OrderDetails"], TABLES["Orders"], TABLES["Sanphams"]], [("Order_Detail / OrderDetails", "Orders", "OderID"), ("Order_Detail / OrderDetails", "Sanpham / Sanphams", "ProductID")], "Order_Detail.cs"),
    diag(15, "Chi tiết bảng Sanphams", [TABLES["Sanphams"]], source="Mood\\EF2\\Sanpham.cs"),
    diag(16, "Chi tiết bảng Users - tài khoản và phân quyền", [t("User / Users - Account", TABLES["Users"].fields[:4], "Phần tài khoản và phân quyền trong User.cs"), TABLES["Quyens"]], [("User / Users - Account", "Quyen / Quyens", "IDQuyen")], "User.cs, Quyen.cs"),
    diag(17, "Chi tiết bảng FaceAuthLogs - vòng đời xác thực", [TABLES["FaceAuthLogs"], t("Actions", ["Register", "Verify", "Authenticate", "RentalVerify", "ActionCheck"], "Các action ghi log")], [("FaceAuthLogs", "Actions", "Action")], "FaceAuthController, LogRepository"),
    diag(18, "Chi tiết bảng Quyens", [TABLES["Quyens"]], source="Mood\\EF2\\Quyen.cs"),
    diag(19, "Chi tiết bảng RentalLogs", [TABLES["RentalLogs"]], source="Mood\\EF2\\RentalLog.cs"),
    diag(20, "Chi tiết bảng UserQuyens", [TABLES["UserQuyens"], TABLES["Users"], TABLES["Quyens"]], [("User / Users", "Quyen / Quyens", "IDQuyen")], "User.cs, Quyen.cs"),
    diag(21, "Chi tiết bảng FaceRentalTokens", [TABLES["FaceRentalTokens"]], source="FaceRentalTokenService.cs"),
    diag(22, "Chi tiết bảng FaceRentalTokens - vòng đời token", [TABLES["FaceRentalTokens"], t("Token Lifecycle", ["Create after face verify", "Valid for 3 minutes", "Consume in RequestRental", "Reject if expired/used"], "Theo FaceAuthRentalTokenMinutes")], [("FaceRentalTokens (memory)", "Token Lifecycle", "lifecycle")], "FaceRentalTokenService.cs, Web.config"),
    diag(23, "Chi tiết bảng StoreLocations - Geofence", [TABLES["StoreLocations"], TABLES["GeofenceLogs"]], [("GeofenceLogs", "StoreLocations", "StoreID")], "StoreLocation.cs, GeofenceLog.cs"),
    diag(24, "Chi tiết bảng RentalLogs - trạng thái mượn trả", [TABLES["RentalLogs"], t("Rental status flow", ["Request -> Pending", "Approve -> Borrowing", "Reject -> Rejected", "Return -> Returned", "Overdue -> Overdue"], "Theo RentalController.UpdateRentalStatus")], [("RentalLogs", "Rental status flow", "Action")], "RentalController.cs"),
    diag(25, "Chi tiết bảng GeofenceLogs", [TABLES["GeofenceLogs"]], source="Mood\\EF2\\GeofenceLog.cs"),
    diag(26, "Cấu trúc database của dự án sau khi đã cài đặt", OVERVIEW_TABLES + [TABLES["ProductReviews"], TABLES["FaceSamples"], TABLES["FaceRentalTokens"]], OVERVIEW_RELATIONS, "sql/migrations sau khi bổ sung rental, log, favorite, review, store"),
]


def load_font(size: int, bold: bool = False):
    for path in [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_TITLE = load_font(28, True)
FONT_HEAD = load_font(18, True)
FONT_TEXT = load_font(15)
FONT_SMALL = load_font(13)


def layout(diagram: DiagramSpec):
    n = len(diagram.tables)
    if n == 1:
        return 1200, 760, {diagram.tables[0].name: (240, 130, 720, 480)}
    cols = 3 if n > 6 else 2
    rows = math.ceil(n / cols)
    cell_w, cell_h = (410, 210) if n > 6 else (420, 260)
    width = max(1400, 80 + cols * (cell_w + 55))
    height = max(900, 120 + rows * (cell_h + 65))
    pos = {}
    for i, table in enumerate(diagram.tables):
        x = 60 + (i % cols) * (cell_w + 55)
        y = 110 + (i // cols) * (cell_h + 65)
        pos[table.name] = (x, y, cell_w, cell_h)
    return width, height, pos


def draw_table(draw: ImageDraw.ImageDraw, box, table: TableSpec, compact: bool = False):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill="white", outline=(0, 0, 0), width=2)
    draw.rectangle((x, y, x + w, y + 38), fill=(221, 235, 247), outline=(0, 0, 0), width=2)
    draw.text((x + 10, y + 8), table.name, font=FONT_HEAD, fill=(0, 0, 0))
    yy = y + 48
    max_fields = 6 if compact else 11
    for field in table.fields[:max_fields]:
        draw.text((x + 12, yy), field, font=FONT_TEXT, fill=(0, 0, 0))
        yy += 22
    if len(table.fields) > max_fields:
        draw.text((x + 12, yy), f"... +{len(table.fields) - max_fields} trường khác", font=FONT_TEXT, fill=(0, 0, 0))
        yy += 22
    if table.note and not compact:
        draw.text((x + 12, y + h - 24), table.note[:56], font=FONT_SMALL, fill=(80, 80, 80))


def center(box):
    x, y, w, h = box
    return x + w / 2, y + h / 2


def render_png(diagram: DiagramSpec) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    width, height, pos = layout(diagram)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    draw.text((40, 30), f"{diagram.code}. {diagram.title}", font=FONT_TITLE, fill=(0, 0, 0))
    compact = len(diagram.tables) > 6
    for a, b, label in diagram.relations:
        if a in pos and b in pos:
            ax, ay = center(pos[a])
            bx, by = center(pos[b])
            draw.line((ax, ay, bx, by), fill=(0, 0, 0), width=2)
            mx, my = (ax + bx) / 2, (ay + by) / 2
            draw.rectangle((mx - 50, my - 10, mx + 50, my + 10), fill="white")
            draw.text((mx - 45, my - 9), label[:14], font=FONT_SMALL, fill=(0, 0, 0))
    for table in diagram.tables:
        draw_table(draw, pos[table.name], table, compact=compact)
    draw.text((40, height - 38), f"Nguồn đối chiếu: {diagram.source}", font=FONT_SMALL, fill=(0, 0, 0))
    out = EXPORT_DIR / diagram.png_name
    img.save(out, "PNG", optimize=True)
    return out


def mx_cell(id_: str, value: str, style: str, x, y, w, h) -> str:
    return f'<mxCell id="{id_}" value="{escape(value)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'


def mx_edge(id_: str, source: str, target: str, label: str) -> str:
    style = "endArrow=none;html=1;rounded=0;strokeColor=#000000;fontSize=12;"
    return f'<mxCell id="{id_}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{source}" target="{target}"><mxGeometry relative="1" as="geometry"/></mxCell>'


def table_html(table: TableSpec) -> str:
    rows = "".join(f'<div align="left">{escape(field)}</div>' for field in table.fields)
    note = f'<div align="left"><font color="#666666">{escape(table.note)}</font></div>' if table.note else ""
    return f'<b>{escape(table.name)}</b><hr size="1"/>{rows}{note}'


def render_drawio(diagram: DiagramSpec) -> Path:
    DRAWIO_DIR.mkdir(exist_ok=True)
    width, height, pos = layout(diagram)
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    cells.append(mx_cell("title", f"{diagram.code}. {diagram.title}", "text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;align=left;", 40, 25, 900, 40))
    ids = {}
    for i, table in enumerate(diagram.tables, start=2):
        x, y, w, h = pos[table.name]
        cid = f"t{i}"
        ids[table.name] = cid
        style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=13;align=left;verticalAlign=top;spacing=8;"
        cells.append(mx_cell(cid, table_html(table), style, x, y, w, h))
    eid = 100
    for a, b, label in diagram.relations:
        if a in ids and b in ids:
            cells.append(mx_edge(f"e{eid}", ids[a], ids[b], label))
            eid += 1
    xml = (
        f'<mxfile host="app.diagrams.net" modified="{datetime.now(UTC).isoformat()}" agent="Codex" version="24.7.17">'
        f'<diagram id="{escape(diagram.code)}" name="{escape(diagram.code)}">'
        f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">'
        f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
    )
    out = DRAWIO_DIR / diagram.drawio_name
    out.write_text(xml, encoding="utf-8")
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


def append_history(drawios: list[Path], pngs: list[Path], replaced: list[str], output_report: Path, status: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"## {now} - Xây dựng sơ đồ database draw.io và cập nhật BaoCaoMauSua_Version3",
        "",
        "- Kế hoạch: `KeHoach_XayDung_CauTrucBang_DrawIO_Version3.md`.",
        "- Thư mục draw.io: `database_drawio`.",
        "- Thư mục PNG export: `database_drawio_exports`.",
        f"- Kết quả Word: `{output_report.name}` ({status}).",
        "- Media đã thay:",
    ]
    for media in replaced:
        d = next(diag for diag in DIAGRAMS if diag.media_target == media)
        lines.append(f"  - `{media}` <- `database_drawio_exports/{d.png_name}`; source `database_drawio/{d.drawio_name}` ({d.code})")
    lines.append("")
    lines.append("- File draw.io đã sinh:")
    for p in drawios:
        lines.append(f"  - `database_drawio/{p.name}`")
    lines.append("")
    previous = HISTORY.read_text(encoding="utf-8") if HISTORY.exists() else "# Lịch sử xây dựng hình database\n\n"
    HISTORY.write_text(previous + "\n".join(lines), encoding="utf-8")


def main():
    DRAWIO_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)
    for path in DRAWIO_DIR.glob("*.drawio"):
        path.unlink()
    for path in EXPORT_DIR.glob("*.png"):
        path.unlink()
    drawios = [render_drawio(d) for d in DIAGRAMS]
    pngs = [render_png(d) for d in DIAGRAMS]
    image_map = {d.media_target: EXPORT_DIR / d.png_name for d in DIAGRAMS}
    replaced, output_report, status = update_report(image_map)
    append_history(drawios, pngs, replaced, output_report, status)
    print(f"Generated {len(drawios)} draw.io database files")
    print(f"Generated {len(pngs)} PNG exports")
    print(f"Replaced {len(replaced)} images in {output_report.name}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
