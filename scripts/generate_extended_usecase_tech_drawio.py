# -*- coding: utf-8 -*-
from pathlib import Path
import datetime as dt
import html
import shutil
import textwrap


ROOT = Path(__file__).resolve().parents[1]
WS = ROOT / "QLNhaSach_BaoCao"
INPUTS = WS / "00_inputs"
KB = WS / "03_knowledge_base"
SECTIONS = WS / "04_generated_sections"
PUML = WS / "05_uml" / "plantuml"
DRAWIO = WS / "05_uml" / "drawio"
IMAGES = WS / "05_uml" / "images"
HISTORY = WS / "13_history"
LOGS = WS / "11_logs"
VALIDATION = WS / "10_validation"


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    for path in [INPUTS, KB, SECTIONS, PUML, DRAWIO, IMAGES, HISTORY, LOGS, VALIDATION]:
        path.mkdir(parents=True, exist_ok=True)


def write(path, content):
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def box_svg(title, subtitle, items, colors):
    blocks = []
    y = 102
    for item in items:
        blocks.append(
            f'<rect x="40" y="{y}" width="560" height="46" rx="8" fill="{colors[2]}" stroke="{colors[1]}" />'
            f'<text x="62" y="{y+29}" font-size="20" fill="#1f2937">{html.escape(item)}</text>'
        )
        y += 58
    height = max(360, y + 35)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}">
  <rect width="640" height="{height}" fill="#ffffff"/>
  <rect x="24" y="24" width="592" height="{height-48}" rx="14" fill="{colors[0]}" stroke="{colors[1]}" stroke-width="2"/>
  <text x="40" y="62" font-family="Arial, sans-serif" font-weight="700" font-size="28" fill="#111827">{html.escape(title)}</text>
  <text x="40" y="88" font-family="Arial, sans-serif" font-size="17" fill="#374151">{html.escape(subtitle)}</text>
  {''.join(blocks)}
</svg>'''


def drawio_file(name, title, nodes, edges):
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        f'<mxCell id="title" value="{html.escape(title)}" style="text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1" vertex="1" parent="1"><mxGeometry x="20" y="10" width="900" height="30" as="geometry"/></mxCell>',
    ]
    for node in nodes:
        nid, label, x, y, w, h, style = node
        cells.append(
            f'<mxCell id="{nid}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
    for index, edge in enumerate(edges, start=1):
        source, target, label = edge
        cells.append(
            f'<mxCell id="e{index}" value="{html.escape(label)}" style="endArrow=block;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1" source="{source}" target="{target}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    xml = f'''<mxfile host="app.diagrams.net" modified="{now()}" agent="Codex" version="24.7.17">
  <diagram id="{name}" name="{html.escape(title)}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    write(DRAWIO / name, xml)


def generate_images():
    write(IMAGES / "illustration_flask_face_api_v1.svg", box_svg(
        "Flask Face API",
        "Nhận diện khuôn mặt, liveness challenge và hồ sơ mẫu",
        [
            "OpenCV giải mã ảnh upload",
            "MediaPipe Face Mesh/Landmarker trích điểm mặt",
            "Histogram HSV tạo descriptor khuôn mặt",
            "So khớp cosine với face_profiles/{user_id}.json",
            "Trả confidence, request_id, liveness_passed"
        ],
        ("#eef7ff", "#2f80ed", "#ffffff"),
    ))
    write(IMAGES / "illustration_ocr_cmnd_v1.svg", box_svg(
        "OCR CMND/CCCD",
        "Đọc ảnh mặt trước/mặt sau và cập nhật hồ sơ mượn sách",
        [
            "Upload front_file/back_file từ ASP.NET MVC",
            "OpenCV tiền xử lý ảnh xám và threshold",
            "pytesseract đọc văn bản vie+eng",
            "Regex tách số giấy tờ, họ tên, ngày sinh, địa chỉ",
            "So khớp ảnh thẻ với mẫu khuôn mặt nếu có user_id"
        ],
        ("#f0fdf4", "#16a34a", "#ffffff"),
    ))
    write(IMAGES / "illustration_search_engine_v1.svg", box_svg(
        "Search Engine nội bộ",
        "Tìm sách bằng LINQ/Entity Framework trên dữ liệu SQL Server",
        [
            "ProductController.ListName trả gợi ý autocomplete",
            "ProductController.Search nhận keyWord, page, pagesize",
            "SanphamDraw.getByKeyWord lọc tên sách, tác giả, thể loại",
            "X.PagedList phân trang 20 sản phẩm/trang",
            "View hiển thị kết quả, gợi ý sách mới và danh mục"
        ],
        ("#fff7ed", "#ea580c", "#ffffff"),
    ))
    write(IMAGES / "illustration_system_architecture_v1.svg", box_svg(
        "Kiến trúc QLNhaSach",
        "ASP.NET MVC kết hợp SQL Server, Flask Face API và Gmail",
        [
            "Razor View và JavaScript xử lý tương tác người dùng",
            "Controller điều phối tài khoản, sản phẩm, mượn sách",
            "Service gọi Face API, Gmail, geofence",
            "Mood.Draw/Mood.EF2 truy vấn Entity Framework",
            "LogDbContext lưu face/geofence/rental logs"
        ],
        ("#f8fafc", "#475569", "#ffffff"),
    ))


def generate_markdown():
    use_cases = [
        ("UC-01", "Khách vãng lai", "Xem trang chủ và danh mục sách", "HomeController.TrangChu, ProductController.ListProduct"),
        ("UC-02", "Khách vãng lai", "Tìm kiếm sách theo từ khóa", "ProductController.Search, SanphamDraw.getByKeyWord"),
        ("UC-03", "Khách vãng lai", "Nhận gợi ý tên sách khi nhập từ khóa", "ProductController.ListName, SanphamDraw.ListName"),
        ("UC-04", "Khách vãng lai", "Xem chi tiết sách, review file, video", "ProductController.Detail, ReviewFilePreview"),
        ("UC-05", "Khách vãng lai", "Đăng ký tài khoản", "UsersController.RegisterUser"),
        ("UC-06", "Người dùng", "Đăng nhập tài khoản/mật khẩu", "UsersController.Login"),
        ("UC-07", "Người dùng", "Đăng nhập MFA bằng khuôn mặt", "UsersController.LoginMFA, FaceAuthController.AuthenticateFace"),
        ("UC-08", "Người dùng", "Đăng ký mẫu khuôn mặt", "FaceAuthController.RegisterFace"),
        ("UC-09", "Người dùng", "Thực hiện challenge liveness", "FaceAuthController.CreateChallenge, CheckChallengeAction"),
        ("UC-10", "Người dùng", "OCR CMND/CCCD nháp trước đăng nhập", "FaceAuthController.OcrCmndDraft"),
        ("UC-11", "Người dùng", "Cập nhật hồ sơ CMND/CCCD", "FaceAuthController.OcrCmnd, RentalController.UpdateRentalProfile"),
        ("UC-12", "Người dùng", "Thêm/xóa sách yêu thích", "UsersController.ToggleFavorite, ProductFavoriteDraw"),
        ("UC-13", "Khách vãng lai", "Lưu yêu thích cục bộ", "UsersController.LocalFavoriteProducts, localStorage"),
        ("UC-14", "Người dùng", "Đồng bộ yêu thích sau đăng nhập", "UsersController.SyncLocalFavorites"),
        ("UC-15", "Người dùng", "Thêm sách vào giỏ hàng", "CartController.AddItem"),
        ("UC-16", "Người dùng", "Cập nhật/xóa giỏ hàng", "CartController.Update, Delete, DeleteAll"),
        ("UC-17", "Người dùng", "Đặt hàng và theo dõi đơn", "CartController.Success, UsersController.ChiTietHoaDon"),
        ("UC-18", "Người dùng", "Thanh toán online MoMo", "CartController.PaymentMoMo, confirm_orderPaymentOnline_momo"),
        ("UC-19", "Người dùng", "Kiểm tra vị trí trước khi mượn", "GeofenceController.CheckGeofence, StoreLocationService"),
        ("UC-20", "Người dùng", "Xác thực khuôn mặt trước khi mượn", "FaceAuthController.VerifyRentalFace"),
        ("UC-21", "Người dùng", "Gửi yêu cầu mượn sách", "RentalController.RequestRental"),
        ("UC-22", "Người dùng", "Hủy yêu cầu mượn đang chờ", "RentalController.CancelRental"),
        ("UC-23", "Người dùng", "Xem danh sách mượn của tôi", "RentalController.MyRentals"),
        ("UC-24", "Người dùng", "Đánh giá sách", "ProductController.AddReview, ProductReviewDraw"),
        ("UC-25", "Quản trị viên", "Quản lý sách, file đọc thử, tồn kho", "Admin/SanPhamController"),
        ("UC-26", "Quản trị viên", "Quản lý danh mục", "Admin/CategoryController"),
        ("UC-27", "Quản trị viên", "Quản lý tài khoản", "Admin/UserController"),
        ("UC-28", "Quản trị viên", "Quản lý đơn hàng", "Admin/HoaDonController"),
        ("UC-29", "Quản trị viên", "Duyệt mượn/trả sách", "Admin/RentalAdminController.UpdateStatus"),
        ("UC-30", "Quản trị viên", "Gửi nhắc quá hạn", "Admin/RentalAdminController.SendOverdueReminders"),
        ("UC-31", "Quản trị viên", "Quản lý tọa độ nhà sách/geofence", "Admin/WebManagerController.StoreLocation"),
        ("UC-32", "Quản trị viên", "Xem nhật ký face/geofence/rental", "Admin/LogsAdminController, Api/LogsController"),
        ("UC-33", "Quản trị viên", "Thống kê doanh thu, sản phẩm hot, mượn trả", "Admin/ThongKeController"),
        ("UC-34", "Quản trị viên", "Quản lý nhập hàng/nhà cung cấp", "Admin/NhapHangController, NhaCungCapController"),
        ("UC-35", "Hệ thống", "Gửi thông báo Gmail", "GmailNotificationService"),
        ("UC-36", "Hệ thống", "Kiểm tra sức khỏe Face API", "HealthController.FaceApi, /api/face/health"),
    ]
    table = "\n".join(f"| {a} | {b} | {c} | `{d}` |" for a, b, c, d in use_cases)
    write(KB / "use_case_catalog_v2.md", f"""
    # Use Case Catalog v2 - QLNhaSach

    Bảng này mở rộng use case theo đúng controller, service và API hiện có trong source code. Các use case được chia theo tác nhân để đưa vào chương phân tích yêu cầu và làm nguồn cho sơ đồ UML/Draw.io.

    | Mã | Tác nhân | Use case | Bằng chứng source code |
    |---|---|---|---|
    {table}

    ## Quan hệ include/extend quan trọng

    - `UC-07 Đăng nhập MFA bằng khuôn mặt` include `UC-09 Thực hiện challenge liveness` khi cấu hình `FaceAuthRequireActionChallenge=true`.
    - `UC-11 Cập nhật hồ sơ CMND/CCCD` include OCR CMND/CCCD qua Flask API.
    - `UC-21 Gửi yêu cầu mượn sách` include `UC-19 Kiểm tra vị trí`, `UC-20 Xác thực khuôn mặt` và `UC-35 Gửi thông báo Gmail`.
    - `UC-29 Duyệt mượn/trả sách` include ghi `RentalLogs` và có thể include gửi Gmail.
    - `UC-02 Tìm kiếm sách` có quan hệ với `UC-03 Gợi ý tên sách` nhưng không phụ thuộc bắt buộc.
    """)

    write(SECTIONS / "technology_analysis_face_ocr_search_v1.md", """
    # Phân tích công nghệ nhận diện khuôn mặt, OCR CMND/CCCD và tìm kiếm

    ![Minh họa kiến trúc tổng quan](../05_uml/images/illustration_system_architecture_v1.svg)

    ## 1. Kiến trúc tích hợp

    Hệ thống QLNhaSach dùng ASP.NET MVC làm ứng dụng web chính. Các controller trong `BaiTapLon` xử lý request từ Razor View, sau đó gọi lớp nghiệp vụ trong `Mood.Draw`, `BaiTapLon.Services` và `Common.Repositories`. Dữ liệu chính được lưu qua Entity Framework trong `Mood.EF2.QuanLySachDBContext`, còn nhật ký xác thực/vị trí/mượn trả được lưu qua `LogDbContext`.

    Thành phần Flask nằm trong `face_auth_api/app.py` được tách khỏi web MVC để xử lý tác vụ ảnh: nhận diện khuôn mặt, kiểm tra hành động sống và OCR CMND/CCCD. Web MVC gọi Flask qua `FaceAuthApiClient`, gửi multipart form-data gồm ảnh, `userId`, `purpose` và `actionCode` nếu có.

    ## 2. Flask Face API

    ![Minh họa Flask Face API](../05_uml/images/illustration_flask_face_api_v1.svg)

    Flask API cung cấp các route: `/api/face/health`, `/api/face/action-check`, `/api/face/register`, `/api/face/verify`, `/api/face/authenticate`, `/api/face/ocr-cmnd`, `/api/face/qcr-cmnd`, `/api/face/cmnd-ocr`.

    Về xử lý ảnh, API dùng OpenCV để giải mã ảnh upload, chuyển màu và cắt vùng khuôn mặt. MediaPipe được dùng theo hai nhánh: `mp.solutions.face_mesh` nếu có sẵn, hoặc `mediapipe.tasks.python.vision.FaceLandmarker` nếu có model `models/face_landmarker.task`. Sau khi phát hiện điểm khuôn mặt, API tạo descriptor bằng histogram HSV của vùng mặt, lưu mẫu vào `face_profiles/{user_id}.json` khi đăng ký và so khớp bằng cosine similarity khi xác thực.

    Liveness challenge được triển khai bằng cách ASP.NET MVC tạo token/chỉ dẫn trong session tại `FaceAuthController.CreateChallenge`. Người dùng thực hiện hành động như quay trái, quay phải, há miệng, cười, nhìn lên hoặc nhìn xuống. Flask API phân loại hành động qua yaw, pitch, nose offset, mouth open ratio và smile ratio tại `/api/face/action-check`.

    ## 3. OCR CMND/CCCD

    ![Minh họa OCR CMND/CCCD](../05_uml/images/illustration_ocr_cmnd_v1.svg)

    Quy trình OCR bắt đầu tại `FaceAuthController.OcrCmndDraft` hoặc `FaceAuthController.OcrCmnd`. Controller nhận ảnh mặt trước/mặt sau bằng các field `front_file`, `back_file`, `frontFile`, `backFile`, lưu vào `DataImage/IdentityCards`, sau đó gọi `FaceAuthApiClient.OcrIdentityCardAsync`.

    Ở Flask API, hàm `decode_identity_uploads` nhận một hoặc hai ảnh. Ảnh được xử lý xám, lọc bilateral, threshold Otsu rồi đưa vào `pytesseract.image_to_string` với ngôn ngữ mặc định `vie+eng`. Hàm `parse_identity_fields` tách các trường như số giấy tờ, họ tên, ngày sinh, giới tính, quốc tịch, quê quán, nơi thường trú, ngày cấp, nơi cấp và ngày hết hạn. Nếu có `user_id`, API còn cố so khớp ảnh mặt trên giấy tờ với mẫu khuôn mặt đã đăng ký.

    Khi OCR thành công, ASP.NET MVC cập nhật các trường định danh trong `Mood.EF2.User`: `IdentityNumber`, `IdentityFullName`, `IdentityDateOfBirth`, `IdentityAddress`, `IdentityIssueDate`, `IdentityCardFrontImagePath`, `IdentityCardBackImagePath`, `IdentityFaceConfidence`, `IdentityVerifiedAt`. Đây là điều kiện quan trọng trước khi người dùng gửi yêu cầu mượn sách.

    ## 4. Search engine nội bộ

    ![Minh họa search engine](../05_uml/images/illustration_search_engine_v1.svg)

    Dự án không dùng search engine ngoài như Elasticsearch. Phần tìm kiếm được triển khai nội bộ bằng ASP.NET MVC, Entity Framework/LINQ và SQL Server. `ProductController.ListName` phục vụ autocomplete tên sách, còn `ProductController.Search` nhận `keyWord`, `page`, `pagesize` rồi gọi `SanphamDraw.getByKeyWord`.

    Cơ chế tìm kiếm dựa trên điều kiện `Contains` đối với các trường sách và thông tin liên quan như tên sách, tác giả, thể loại hoặc nhà cung cấp tùy hàm truy vấn. Kết quả được sắp xếp và phân trang bằng `X.PagedList`, mặc định 20 sản phẩm/trang. View tìm kiếm còn truyền thêm `listGoiY`, `Category`, `totalKq` và `keyWord` để hiển thị gợi ý, danh mục và số lượng kết quả.

    Cách thiết kế này phù hợp quy mô đồ án vì tận dụng cơ sở dữ liệu sẵn có, không phát sinh hạ tầng mới, dễ giải thích trong báo cáo và dễ bảo trì. Hạn chế là khả năng xếp hạng theo độ liên quan, tìm kiếm không dấu và tìm kiếm toàn văn chưa mạnh như các search engine chuyên dụng.
    """)


def generate_puml():
    write(PUML / "use_case_day_du_v2.puml", r"""
    @startuml
    left to right direction
    skinparam backgroundColor #FFFFFF
    skinparam packageStyle rectangle
    skinparam shadowing false

    actor "Khách vãng lai" as Guest
    actor "Người dùng" as User
    actor "Quản trị viên" as Admin
    actor "Flask Face API" as FaceApi
    actor "Gmail Service" as Gmail
    actor "SQL Server" as Db

    rectangle "QLNhaSach - Website quản lý nhà sách" {
      package "Tra cứu và mua sách" {
        usecase "Xem trang chủ/danh mục" as UC01
        usecase "Tìm kiếm sách" as UC02
        usecase "Gợi ý tên sách" as UC03
        usecase "Xem chi tiết sách" as UC04
        usecase "Xem/tải file đọc thử" as UC05
        usecase "Đánh giá sách" as UC06
        usecase "Quản lý yêu thích" as UC07
        usecase "Giỏ hàng" as UC08
        usecase "Đặt hàng/thanh toán" as UC09
      }

      package "Tài khoản và bảo mật" {
        usecase "Đăng ký tài khoản" as UC10
        usecase "Đăng nhập mật khẩu" as UC11
        usecase "MFA khuôn mặt" as UC12
        usecase "Đăng ký mẫu khuôn mặt" as UC13
        usecase "Challenge liveness" as UC14
        usecase "OCR CMND/CCCD" as UC15
        usecase "Cập nhật hồ sơ mượn sách" as UC16
      }

      package "Mượn/trả sách" {
        usecase "Kiểm tra tồn kho" as UC17
        usecase "Kiểm tra vị trí geofence" as UC18
        usecase "Xác thực mặt trước khi mượn" as UC19
        usecase "Gửi yêu cầu mượn" as UC20
        usecase "Hủy yêu cầu đang chờ" as UC21
        usecase "Xem lịch sử mượn" as UC22
      }

      package "Quản trị" {
        usecase "Quản lý sách/danh mục" as UC23
        usecase "Quản lý đơn hàng" as UC24
        usecase "Duyệt mượn/trả" as UC25
        usecase "Nhắc quá hạn" as UC26
        usecase "Quản lý người dùng" as UC27
        usecase "Quản lý nhập hàng/NCC" as UC28
        usecase "Quản lý tọa độ nhà sách" as UC29
        usecase "Xem nhật ký hệ thống" as UC30
        usecase "Thống kê báo cáo" as UC31
      }

      usecase "Gửi email thông báo" as UC32
      usecase "Ghi log face/geofence/rental" as UC33
    }

    Guest --> UC01
    Guest --> UC02
    Guest --> UC03
    Guest --> UC04
    Guest --> UC07
    Guest --> UC10
    Guest --> UC11

    User --> UC01
    User --> UC02
    User --> UC04
    User --> UC05
    User --> UC06
    User --> UC07
    User --> UC08
    User --> UC09
    User --> UC11
    User --> UC12
    User --> UC13
    User --> UC15
    User --> UC16
    User --> UC17
    User --> UC18
    User --> UC19
    User --> UC20
    User --> UC21
    User --> UC22

    Admin --> UC23
    Admin --> UC24
    Admin --> UC25
    Admin --> UC26
    Admin --> UC27
    Admin --> UC28
    Admin --> UC29
    Admin --> UC30
    Admin --> UC31

    UC12 ..> UC14 : <<include>>
    UC15 ..> UC33 : <<include>>
    UC18 ..> UC33 : <<include>>
    UC19 ..> UC14 : <<include>>
    UC19 ..> UC33 : <<include>>
    UC20 ..> UC17 : <<include>>
    UC20 ..> UC18 : <<include>>
    UC20 ..> UC19 : <<include>>
    UC20 ..> UC32 : <<include>>
    UC25 ..> UC32 : <<include>>
    UC25 ..> UC33 : <<include>>

    FaceApi --> UC12
    FaceApi --> UC13
    FaceApi --> UC14
    FaceApi --> UC15
    FaceApi --> UC19
    Gmail --> UC32
    Db --> UC33
    @enduml
    """)

    write(PUML / "sequence_face_login_v2.puml", r"""
    @startuml
    skinparam backgroundColor #FFFFFF
    actor "Người dùng" as User
    participant "Login View" as View
    participant "UsersController" as Users
    participant "FaceAuthController" as FaceCtrl
    participant "FaceAuthApiClient" as Client
    participant "Flask API\n/verify|/authenticate|/action-check" as Flask
    database "FaceAuthLogs" as Logs

    User -> View : Nhập tài khoản/mật khẩu
    View -> Users : POST Login
    Users -> Users : UserDraw.LoginHomeUser
    alt EnableFaceMFA = true
      Users --> View : tạo FACE_MFA_SESSION, chuyển LoginMFA
      View -> FaceCtrl : CreateChallenge("MFA")
      FaceCtrl --> View : token + action instruction
      User -> View : Thực hiện hành động khuôn mặt
      View -> FaceCtrl : CheckChallengeAction(token, image)
      FaceCtrl -> Client : CheckActionAsync(actionCode)
      Client -> Flask : POST /api/face/action-check
      Flask --> Client : action_matched
      Client --> FaceCtrl : FaceAuthResponse
      User -> View : Chụp ảnh xác thực
      View -> FaceCtrl : AuthenticateFace(image, token)
      FaceCtrl -> Client : AuthenticateAsync(image, userId)
      Client -> Flask : POST /api/face/authenticate
      Flask --> Client : success, confidence, request_id
      FaceCtrl -> Logs : AddFaceAuthLog
      FaceCtrl -> FaceCtrl : CompletePendingMfaSession
      FaceCtrl --> View : success
    else không bật MFA
      Users -> Users : tạo USER_SESSION
      Users --> View : vào trang chủ
    end
    @enduml
    """)

    write(PUML / "sequence_ocr_cmnd_v2.puml", r"""
    @startuml
    skinparam backgroundColor #FFFFFF
    actor "Người dùng" as User
    participant "Razor View\nHồ sơ" as View
    participant "FaceAuthController" as Controller
    participant "FaceAuthApiClient" as Client
    participant "Flask API\n/api/face/ocr-cmnd" as Flask
    database "Users" as Users

    User -> View : Tải ảnh mặt trước/mặt sau CMND/CCCD
    View -> Controller : POST OcrCmnd(front_file, back_file)
    Controller -> Controller : ValidateIdentityFile, lưu DataImage/IdentityCards
    Controller -> Client : OcrIdentityCardAsync(front, back, userId)
    Client -> Flask : multipart form-data
    Flask -> Flask : OpenCV tiền xử lý ảnh
    Flask -> Flask : pytesseract OCR vie+eng
    Flask -> Flask : parse_identity_fields()
    Flask -> Flask : compare_identity_face() nếu có user_id
    Flask --> Client : JSON fields, face_confidence, request_id
    Client --> Controller : JObject
    Controller -> Users : Cập nhật IdentityNumber, FullName, Address...
    Controller --> View : JSON success + fields
    View --> User : Hiển thị thông tin đã đọc
    @enduml
    """)

    write(PUML / "sequence_search_engine_v2.puml", r"""
    @startuml
    skinparam backgroundColor #FFFFFF
    actor "Khách/Người dùng" as User
    participant "Search View" as View
    participant "ProductController" as Controller
    participant "SanphamDraw" as Draw
    database "SQL Server\nSanphams/Categories" as Db

    User -> View : Nhập từ khóa
    alt autocomplete
      View -> Controller : GET ListName(q)
      Controller -> Draw : ListName(q)
      Draw -> Db : Truy vấn tên sách phù hợp
      Db --> Draw : Danh sách gợi ý
      Draw --> Controller : data
      Controller --> View : JSON {data, status=true}
    else tìm kiếm đầy đủ
      View -> Controller : GET Search(keyWord, page, pagesize)
      Controller -> Draw : getByKeyWord(keyWord, page, pagesize)
      Draw -> Db : LINQ Contains + phân trang
      Db --> Draw : Danh sách SanPhamModel
      Draw --> Controller : IPagedList
      Controller -> Draw : listSanphamnew(5), ListCount()
      Controller --> View : Model + ViewBag.totalKq/keyWord/listGoiY
    end
    View --> User : Hiển thị kết quả và danh mục
    @enduml
    """)

    write(PUML / "component_flask_face_ocr_search_v2.puml", r"""
    @startuml
    skinparam backgroundColor #FFFFFF
    skinparam componentStyle rectangle

    component "ASP.NET MVC\nBaiTapLon" as Web {
      [UsersController]
      [ProductController]
      [FaceAuthController]
      [RentalController]
      [GeofenceController]
      [FaceAuthApiClient]
    }

    component "Flask Face API\nface_auth_api/app.py" as Flask {
      [OpenCV decode/preprocess]
      [MediaPipe landmarks]
      [Face descriptor + profile JSON]
      [pytesseract OCR]
      [Action classifier]
    }

    component "Mood.Draw" as Draw
    database "QuanLySachDBContext\nSQL Server" as Db
    database "LogDbContext\nFaceAuthLogs/GeofenceLogs/RentalLogs" as Logs
    folder "face_profiles" as Profiles
    component "GmailNotificationService" as Gmail

    [ProductController] --> Draw : tìm kiếm/sản phẩm
    Draw --> Db : Entity Framework
    [FaceAuthController] --> [FaceAuthApiClient]
    [FaceAuthApiClient] --> Flask : HTTP multipart
    Flask --> Profiles : lưu/đọc mẫu mặt
    [FaceAuthController] --> Logs : ghi nhật ký xác thực
    [GeofenceController] --> Logs : ghi geofence
    [RentalController] --> Logs : ghi mượn/trả
    [RentalController] --> Gmail : thông báo trạng thái
    @enduml
    """)

    write(PUML / "activity_search_engine_v2.puml", r"""
    @startuml
    skinparam backgroundColor #FFFFFF
    start
    :Người dùng nhập từ khóa;
    if (Cần autocomplete?) then (Có)
      :Gọi ProductController.ListName(q);
      :SanphamDraw.ListName truy vấn SQL;
      :Trả JSON gợi ý;
    else (Không)
      :Gọi ProductController.Search(keyWord,page,pagesize);
      :SanphamDraw.getByKeyWord lọc Contains;
      :Phân trang bằng X.PagedList;
      :Nạp danh mục và sách gợi ý;
      :Render view kết quả;
    endif
    stop
    @enduml
    """)


def generate_drawio():
    actor_style = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
    usecase_style = "ellipse;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    sys_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
    nodes = [
        ("guest", "Khách vãng lai", 40, 100, 60, 100, actor_style),
        ("user", "Người dùng", 40, 270, 60, 100, actor_style),
        ("admin", "Quản trị viên", 40, 450, 60, 100, actor_style),
        ("system", "QLNhaSach", 170, 70, 850, 520, sys_style),
        ("uc_search", "Tìm kiếm/gợi ý sách", 220, 120, 150, 60, usecase_style),
        ("uc_detail", "Xem chi tiết/đọc thử/đánh giá", 410, 120, 170, 60, usecase_style),
        ("uc_login", "Đăng nhập + MFA khuôn mặt", 620, 120, 170, 60, usecase_style),
        ("uc_ocr", "OCR CMND/CCCD", 820, 120, 150, 60, usecase_style),
        ("uc_fav", "Yêu thích/giỏ hàng/đặt hàng", 220, 250, 180, 60, usecase_style),
        ("uc_rental", "Mượn sách: tồn kho + geofence + face", 450, 250, 220, 70, usecase_style),
        ("uc_admin_product", "Quản lý sách/danh mục/tồn kho", 220, 430, 190, 60, usecase_style),
        ("uc_admin_rental", "Duyệt mượn/trả + nhắc quá hạn", 450, 430, 190, 60, usecase_style),
        ("uc_logs", "Nhật ký và thống kê", 700, 430, 170, 60, usecase_style),
        ("face", "Flask Face API", 1040, 160, 90, 90, actor_style),
        ("gmail", "Gmail Service", 1040, 350, 90, 90, actor_style),
    ]
    edges = [
        ("guest", "uc_search", ""), ("guest", "uc_detail", ""), ("guest", "uc_login", ""),
        ("user", "uc_search", ""), ("user", "uc_detail", ""), ("user", "uc_fav", ""), ("user", "uc_rental", ""), ("user", "uc_ocr", ""),
        ("admin", "uc_admin_product", ""), ("admin", "uc_admin_rental", ""), ("admin", "uc_logs", ""),
        ("uc_login", "face", "include"), ("uc_ocr", "face", "include"), ("uc_rental", "face", "include"),
        ("uc_admin_rental", "gmail", "include"),
    ]
    drawio_file("use_case_day_du_v2.drawio", "Use case đầy đủ QLNhaSach", nodes, edges)

    comp_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1f5fe;strokeColor=#0288d1;fontStyle=1;"
    db_style = "shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f8cecc;strokeColor=#b85450;"
    nodes = [
        ("view", "Razor View + JavaScript", 60, 120, 160, 70, comp_style),
        ("ctrl", "ASP.NET MVC Controllers", 280, 120, 180, 70, comp_style),
        ("svc", "Services\nFaceAuthApiClient, Gmail, Geofence", 520, 120, 220, 80, comp_style),
        ("draw", "Mood.Draw / Repositories", 280, 290, 190, 70, comp_style),
        ("db", "SQL Server\nQuanLySachDBContext", 520, 290, 180, 80, db_style),
        ("logs", "LogDbContext\nFace/Geofence/Rental", 750, 290, 180, 80, db_style),
        ("flask", "Flask Face API\nOpenCV + MediaPipe + pytesseract", 820, 100, 260, 100, comp_style),
        ("profiles", "face_profiles/*.json", 880, 250, 160, 60, comp_style),
        ("gmail", "Gmail SMTP", 820, 420, 180, 60, comp_style),
    ]
    edges = [
        ("view", "ctrl", "HTTP"), ("ctrl", "svc", "gọi service"), ("ctrl", "draw", "nghiệp vụ dữ liệu"),
        ("draw", "db", "EF/LINQ"), ("svc", "flask", "multipart"), ("flask", "profiles", "đọc/ghi mẫu mặt"),
        ("ctrl", "logs", "ghi log"), ("svc", "gmail", "email"),
    ]
    drawio_file("component_flask_face_ocr_search_v2.drawio", "Component Flask Face/OCR/Search", nodes, edges)

    seq_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;"
    nodes = [
        ("u", "Người dùng", 40, 90, 120, 50, seq_style),
        ("login", "Login View", 200, 90, 120, 50, seq_style),
        ("users", "UsersController", 370, 90, 150, 50, seq_style),
        ("face", "FaceAuthController", 570, 90, 160, 50, seq_style),
        ("client", "FaceAuthApiClient", 780, 90, 160, 50, seq_style),
        ("flask", "Flask Face API", 990, 90, 150, 50, seq_style),
        ("logs", "FaceAuthLogs", 990, 250, 140, 60, db_style),
    ]
    edges = [
        ("u", "login", "nhập tài khoản/mật khẩu"),
        ("login", "users", "POST Login"),
        ("users", "login", "FACE_MFA_SESSION"),
        ("login", "face", "CreateChallenge"),
        ("face", "client", "CheckActionAsync"),
        ("client", "flask", "/action-check"),
        ("login", "face", "AuthenticateFace"),
        ("face", "client", "AuthenticateAsync"),
        ("client", "flask", "/authenticate"),
        ("face", "logs", "AddFaceAuthLog"),
    ]
    drawio_file("sequence_face_login_v2.drawio", "Sequence đăng nhập và xác thực khuôn mặt", nodes, edges)

    nodes = [
        ("u", "Người dùng", 60, 90, 120, 50, seq_style),
        ("v", "View hồ sơ", 230, 90, 130, 50, seq_style),
        ("c", "FaceAuthController", 410, 90, 160, 50, seq_style),
        ("api", "FaceAuthApiClient", 630, 90, 160, 50, seq_style),
        ("f", "Flask /ocr-cmnd", 850, 90, 160, 50, seq_style),
        ("db", "Users", 1060, 90, 90, 50, db_style),
    ]
    edges = [("u", "v", "upload ảnh"), ("v", "c", "POST OcrCmnd"), ("c", "api", "OcrIdentityCardAsync"), ("api", "f", "multipart"), ("f", "api", "fields JSON"), ("c", "db", "update identity")]
    drawio_file("sequence_ocr_cmnd_v2.drawio", "Sequence OCR CMND/CCCD", nodes, edges)

    nodes = [
        ("u", "Khách/Người dùng", 60, 90, 140, 50, seq_style),
        ("v", "Search View", 250, 90, 120, 50, seq_style),
        ("c", "ProductController", 430, 90, 150, 50, seq_style),
        ("d", "SanphamDraw", 650, 90, 140, 50, seq_style),
        ("db", "SQL Server", 860, 90, 130, 60, db_style),
    ]
    edges = [("u", "v", "nhập từ khóa"), ("v", "c", "Search/ListName"), ("c", "d", "getByKeyWord/ListName"), ("d", "db", "LINQ Contains"), ("db", "d", "kết quả"), ("c", "v", "model/json")]
    drawio_file("sequence_search_engine_v2.drawio", "Sequence Search Engine nội bộ", nodes, edges)

    decision_style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    action_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    nodes = [
        ("start", "Bắt đầu", 80, 80, 90, 40, "ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"),
        ("input", "Nhập từ khóa", 230, 70, 130, 60, action_style),
        ("decide", "Autocomplete?", 430, 70, 120, 80, decision_style),
        ("listname", "ListName(q)\ntrả JSON gợi ý", 650, 40, 170, 70, action_style),
        ("search", "Search(keyWord,page)\ngetByKeyWord", 650, 170, 190, 70, action_style),
        ("sql", "SQL Contains\n+ X.PagedList", 910, 120, 170, 80, action_style),
        ("render", "Render kết quả/gợi ý", 1130, 120, 160, 70, action_style),
    ]
    edges = [
        ("start", "input", ""),
        ("input", "decide", ""),
        ("decide", "listname", "Có"),
        ("decide", "search", "Không"),
        ("listname", "render", "JSON"),
        ("search", "sql", ""),
        ("sql", "render", "Model"),
    ]
    drawio_file("activity_search_engine_v2.drawio", "Activity Search Engine nội bộ", nodes, edges)


def update_full_input():
    source = INPUTS / "FULL_INPUT_QLNhaSach_SRC_CODE_v5.md"
    if not source.exists():
        source = INPUTS / "FULL_INPUT_QLNhaSach_SRC_CODE_v4.md"
    target = INPUTS / "FULL_INPUT_QLNhaSach_SRC_CODE_v6.md"
    base = source.read_text(encoding="utf-8") if source.exists() else "# FULL INPUT QLNhaSach\n"
    addendum = f"""

---

# ADDENDUM v5 - Bổ sung use case, công nghệ Flask Face/OCR/Search và sơ đồ Draw.io

Thời điểm bổ sung: {now()} Asia/Bangkok

## File phân tích mới

- `QLNhaSach_BaoCao/03_knowledge_base/use_case_catalog_v2.md`
- `QLNhaSach_BaoCao/04_generated_sections/technology_analysis_face_ocr_search_v1.md`

## Ảnh minh họa mới

- `QLNhaSach_BaoCao/05_uml/images/illustration_system_architecture_v1.svg`
- `QLNhaSach_BaoCao/05_uml/images/illustration_flask_face_api_v1.svg`
- `QLNhaSach_BaoCao/05_uml/images/illustration_ocr_cmnd_v1.svg`
- `QLNhaSach_BaoCao/05_uml/images/illustration_search_engine_v1.svg`

## Sơ đồ PlantUML mới

- `QLNhaSach_BaoCao/05_uml/plantuml/use_case_day_du_v2.puml`
- `QLNhaSach_BaoCao/05_uml/plantuml/sequence_face_login_v2.puml`
- `QLNhaSach_BaoCao/05_uml/plantuml/sequence_ocr_cmnd_v2.puml`
- `QLNhaSach_BaoCao/05_uml/plantuml/sequence_search_engine_v2.puml`
- `QLNhaSach_BaoCao/05_uml/plantuml/activity_search_engine_v2.puml`
- `QLNhaSach_BaoCao/05_uml/plantuml/component_flask_face_ocr_search_v2.puml`

## File Draw.io mới

- `QLNhaSach_BaoCao/05_uml/drawio/use_case_day_du_v2.drawio`
- `QLNhaSach_BaoCao/05_uml/drawio/component_flask_face_ocr_search_v2.drawio`
- `QLNhaSach_BaoCao/05_uml/drawio/sequence_face_login_v2.drawio`
- `QLNhaSach_BaoCao/05_uml/drawio/sequence_ocr_cmnd_v2.drawio`
- `QLNhaSach_BaoCao/05_uml/drawio/sequence_search_engine_v2.drawio`
- `QLNhaSach_BaoCao/05_uml/drawio/activity_search_engine_v2.drawio`

## Quy tắc dùng trong báo cáo

Khi viết lại chương phân tích, lấy `use_case_catalog_v2.md` làm danh mục use case chính. Khi viết chương công nghệ, dùng `technology_analysis_face_ocr_search_v1.md` làm nguồn giải thích Flask Face API, OCR CMND/CCCD và search engine nội bộ. Các hình SVG có thể chèn trực tiếp vào Markdown; các file `.drawio` dùng để chỉnh sửa sơ đồ trong diagrams.net.
"""
    target.write_text(base + addendum, encoding="utf-8")
    return target


def write_history_and_validation(full_input):
    write(HISTORY / "007_bo_sung_usecase_congnghe_drawio_v1.md", f"""
    # 007 - Bổ sung use case, phân tích công nghệ và Draw.io

    Thời điểm: {now()} Asia/Bangkok

    ## Đã thực hiện

    - Bổ sung catalog use case v2 với 36 use case bám controller/service/API.
    - Viết phân tích công nghệ cho Flask Face API, OCR CMND/CCCD và search engine nội bộ.
    - Tạo 4 ảnh minh họa SVG cho kiến trúc, Face API, OCR và Search.
    - Tạo 5 sơ đồ PlantUML mới.
    - Xuất 4 file `.drawio` có thể mở bằng diagrams.net.
    - Tạo full input v5 có addendum liên kết toàn bộ artifact mới.

    ## File đầu vào mới

    - `{full_input.relative_to(ROOT).as_posix()}`
    """)
    with (LOGS / "execution_log.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {now()}\n\n")
        f.write("- Bổ sung use case catalog v2, phân tích công nghệ Face/OCR/Search, SVG minh họa và Draw.io.\n")
        f.write(f"- Tạo `{full_input.relative_to(ROOT).as_posix()}`.\n")

    required = [
        KB / "use_case_catalog_v2.md",
        SECTIONS / "technology_analysis_face_ocr_search_v1.md",
        PUML / "use_case_day_du_v2.puml",
        PUML / "sequence_face_login_v2.puml",
        PUML / "sequence_ocr_cmnd_v2.puml",
        PUML / "sequence_search_engine_v2.puml",
        PUML / "activity_search_engine_v2.puml",
        PUML / "component_flask_face_ocr_search_v2.puml",
        DRAWIO / "use_case_day_du_v2.drawio",
        DRAWIO / "component_flask_face_ocr_search_v2.drawio",
        DRAWIO / "sequence_face_login_v2.drawio",
        DRAWIO / "sequence_ocr_cmnd_v2.drawio",
        DRAWIO / "sequence_search_engine_v2.drawio",
        DRAWIO / "activity_search_engine_v2.drawio",
        IMAGES / "illustration_system_architecture_v1.svg",
        IMAGES / "illustration_flask_face_api_v1.svg",
        IMAGES / "illustration_ocr_cmnd_v1.svg",
        IMAGES / "illustration_search_engine_v1.svg",
        full_input,
    ]
    rows = "\n".join(f"| `{p.relative_to(ROOT).as_posix()}` | {'OK' if p.exists() and p.stat().st_size > 0 else 'CAN KIEM TRA'} |" for p in required)
    write(VALIDATION / "usecase_tech_drawio_validation_v1.md", f"""
    # Validation - Use case, công nghệ và Draw.io

    Thời điểm: {now()} Asia/Bangkok

    | File | Kết quả |
    |---|---|
    {rows}
    """)


def main():
    ensure_dirs()
    generate_images()
    generate_markdown()
    generate_puml()
    generate_drawio()
    full_input = update_full_input()
    write_history_and_validation(full_input)
    print("Generated extended use cases, technology analysis, SVG illustrations and draw.io files.")
    print(full_input.relative_to(ROOT))


if __name__ == "__main__":
    main()
