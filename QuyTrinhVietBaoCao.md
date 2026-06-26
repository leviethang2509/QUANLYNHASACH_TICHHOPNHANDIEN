# KẾ HOẠCH THỰC HIỆN ĐỀ TÀI

**Tên đề tài:** Báo cáo quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn trả sách  
**Sinh viên thực hiện:** Lê Việt Thắng  
**MSSV:** 2224802010263  
**Thời gian thực hiện:** Tháng 01/2026 - Tháng 05/2026  
**Sản phẩm dự kiến:** Website quản lý nhà sách, chức năng mượn/trả sách, xác thực khuôn mặt, OCR CMND/CCCD, gửi thông báo Gmail và chatbox tư vấn sách.

<div style="page-break-after: always;"></div>

## Trang 1 - Mục tiêu và phạm vi thực hiện

### 1. Mục tiêu chung

Đề tài xây dựng hệ thống quản lý nhà sách trên nền tảng web, hỗ trợ quản lý sản phẩm sách, danh mục, đơn hàng, tài khoản người dùng, đánh giá sách, mượn trả sách và nhật ký hệ thống. Điểm mở rộng chính của hệ thống là tích hợp nhận diện khuôn mặt để xác thực người mượn, OCR CMND/CCCD để chuẩn hóa hồ sơ định danh, gửi thông báo Gmail cho các trạng thái mượn trả và chatbox hỗ trợ tư vấn sách.

### 2. Mục tiêu cụ thể

- Khảo sát nghiệp vụ quản lý nhà sách và quy trình mượn/trả sách.
- Phân tích source hiện có, xác định các module chính trong hệ thống ASP.NET MVC.
- Xây dựng quy trình mượn sách có kiểm tra đăng nhập, hồ sơ định danh, tồn kho, xác thực khuôn mặt và thời hạn mượn.
- Xây dựng quy trình duyệt mượn, từ chối, hủy, trả sách, đánh dấu quá hạn và ghi lịch sử xử lý.
- Tích hợp server nhận diện khuôn mặt Flask API để đăng ký, xác thực và kiểm tra hành động khuôn mặt.
- Tích hợp OCR CMND/CCCD bằng PaddleOCR/Tesseract để đọc thông tin giấy tờ định danh.
- Tích hợp Gmail SMTP/API để gửi thông báo trạng thái mượn/trả sách cho người dùng.
- Tích hợp chatbox tư vấn sách, giá, tồn kho và hướng dẫn mượn sách.
- Hoàn thiện báo cáo, sơ đồ use case, quy trình xử lý và kế hoạch kiểm thử.

### 3. Phạm vi chức năng

Hệ thống tập trung vào các nhóm chức năng sau:

- Người dùng: đăng ký, đăng nhập, cập nhật hồ sơ, cập nhật CMND/CCCD, xác thực khuôn mặt, xem sách, đánh giá sách, đặt hàng, yêu thích sách, gửi yêu cầu mượn sách và theo dõi lịch sử mượn.
- Quản trị viên: quản lý sản phẩm, danh mục, kho, hóa đơn, người dùng, nhà cung cấp, nhập hàng, phản hồi, vị trí cửa hàng, nhật ký xác thực và nhật ký mượn trả.
- Mượn/trả sách: tạo yêu cầu mượn, kiểm tra tồn kho, xác thực khuôn mặt, duyệt yêu cầu, cập nhật trạng thái, trả sách, đánh dấu quá hạn và gửi Gmail thông báo.
- AI/API phụ trợ: nhận diện khuôn mặt, OCR CMND/CCCD, kiểm tra chất lượng ảnh, chống thao tác sai quy trình và chatbox tư vấn.

<div style="page-break-after: always;"></div>

## Trang 2 - Cơ sở công nghệ sử dụng trong source

### 1. Công nghệ phía website quản lý nhà sách

Source chính nằm tại thư mục `QLNhaSach`, triển khai theo mô hình ASP.NET MVC.

| Thành phần | Công nghệ sử dụng | Vai trò |
|---|---|---|
| Backend web | ASP.NET MVC 5, C# | Xử lý controller, view, nghiệp vụ nhà sách và mượn/trả |
| Runtime | .NET Framework 4.8 | Nền tảng chạy ứng dụng web |
| ORM | Entity Framework 6 | Ánh xạ bảng dữ liệu sang model C# |
| CSDL | SQL Server LocalDB, database `QLNhaSach` | Lưu người dùng, sách, đơn hàng, mượn trả, log |
| Frontend | Razor View, HTML, CSS, JavaScript | Hiển thị giao diện người dùng và quản trị |
| Thư viện UI | Bootstrap, jQuery, jQuery Validation | Giao diện, tương tác và kiểm tra dữ liệu |
| Phân trang | X.PagedList | Phân trang danh sách sản phẩm, hóa đơn, log |
| Xuất file | ClosedXML, OpenXML | Xuất dữ liệu Excel/tài liệu |
| Mail | SMTP Gmail, `SmtpClient` | Gửi thông báo Gmail cho người dùng |
| Đăng nhập mạng xã hội | Facebook SDK, OWIN | Hỗ trợ đăng nhập Facebook |

### 2. Công nghệ server nhận diện khuôn mặt, OCR và chatbox

Source tham khảo nằm tại `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`.

| Thành phần | Công nghệ sử dụng | Vai trò |
|---|---|---|
| API server | Flask 3 | Cung cấp API `/api/face/*` và `/api/chatbox/*` |
| Nhận diện khuôn mặt | InsightFace, ONNXRuntime | Trích xuất embedding và so khớp khuôn mặt |
| Kiểm tra hành động/liveness | MediaPipe Face Landmarker | Kiểm tra hành động như nhìn trái, nhìn phải, mở miệng |
| Xử lý ảnh | OpenCV, NumPy, scikit-image | Đọc ảnh, tiền xử lý ảnh, kiểm tra chất lượng |
| OCR giấy tờ | PaddleOCR, pytesseract/Tesseract | Đọc CMND/CCCD mặt trước và mặt sau |
| Lưu mẫu khuôn mặt | `face_db.pkl` | Lưu embedding khuôn mặt theo user |
| Kết nối dữ liệu | pyodbc | Huấn luyện chatbox hoặc đọc dữ liệu sản phẩm từ CSDL |
| Chatbox | Flask blueprint, JSON knowledge base | Tư vấn sách, giá, tồn kho và hướng dẫn mượn |

### 3. Cấu hình tích hợp chính

Website kết nối server nhận diện thông qua cấu hình:

- `FaceAuthAPI`: `http://localhost:8000/api/face`
- `ChatboxWidgetUrl`: `http://localhost:8000/api/chatbox/widget.js`
- `FaceAuthMinConfidence`: ngưỡng xác thực khuôn mặt, hiện dùng `0.75`
- `FaceSampleStoragePath`: thư mục lưu ảnh xác thực khuôn mặt
- `IdentityCardStoragePath`: thư mục lưu ảnh CMND/CCCD
- `RentalMaxBorrowDays`: số ngày mượn tối đa, hiện dùng `30`
- `GmailNotificationsEnabled`: bật/tắt gửi Gmail thông báo

<div style="page-break-after: always;"></div>

## Trang 3 - Phân tích nghiệp vụ và các tác nhân

### 1. Tác nhân sử dụng hệ thống

| Tác nhân | Mô tả vai trò |
|---|---|
| Khách vãng lai | Xem trang chủ, xem danh mục, tìm kiếm sản phẩm, xem chi tiết sách |
| Người dùng thành viên | Đăng nhập, cập nhật hồ sơ, OCR CMND/CCCD, xác thực khuôn mặt, yêu cầu mượn sách, theo dõi mượn trả, đặt hàng |
| Quản trị viên | Quản lý sách, danh mục, đơn hàng, tồn kho, người dùng, duyệt mượn/trả sách và xem nhật ký hệ thống |
| Server Face API | Xử lý đăng ký khuôn mặt, xác thực khuôn mặt, OCR CMND/CCCD và kiểm tra hành động |
| Gmail SMTP/API | Gửi thông báo về trạng thái yêu cầu mượn/trả sách |
| Chatbox | Trả lời câu hỏi về sách, tồn kho, giá và hướng dẫn mượn sách |

### 2. Use case dự kiến sẽ vẽ bằng draw.io ở giai đoạn hoàn thiện

Trong bản kế hoạch xem trước này, sơ đồ use case được mô tả bằng nội dung để duyệt trước. Khi chuyển sang bản báo cáo Word/PDF, sơ đồ sẽ được dựng bằng draw.io và chèn hình vào đúng vị trí.

Các use case chính:

- Xem danh sách sách.
- Tìm kiếm sách.
- Xem chi tiết sách.
- Đăng ký tài khoản.
- Đăng nhập bằng tài khoản hoặc khuôn mặt.
- Cập nhật Gmail nhận thông báo.
- Cập nhật hồ sơ CMND/CCCD.
- OCR CMND/CCCD.
- Đăng ký mẫu khuôn mặt.
- Xác thực khuôn mặt trước khi mượn sách.
- Gửi yêu cầu mượn sách.
- Theo dõi lịch sử mượn.
- Hủy yêu cầu đang chờ duyệt.
- Quản trị viên duyệt yêu cầu mượn.
- Quản trị viên từ chối yêu cầu mượn.
- Quản trị viên xác nhận trả sách.
- Hệ thống gửi Gmail thông báo.
- Chatbox tư vấn sách.
- Xem nhật ký xác thực và nhật ký mượn trả.

### 3. Ràng buộc nghiệp vụ chính

- Người dùng phải đăng nhập trước khi gửi yêu cầu mượn sách.
- Người dùng phải có Gmail nhận thông báo, số CMND/CCCD và họ tên định danh.
- Người dùng phải xác thực khuôn mặt thành công trước khi tạo yêu cầu mượn.
- Mỗi lần xác thực khuôn mặt chỉ sinh token ngắn hạn cho đúng user và đúng sách.
- Không cho mượn nếu sách hết tồn kho hoặc người dùng đang có yêu cầu mượn còn hiệu lực với cùng sách.
- Khi admin duyệt mượn, hệ thống giảm tồn kho.
- Khi admin xác nhận trả sách, hệ thống tăng tồn kho.
- Mọi thao tác mượn/trả, xác thực khuôn mặt và gửi thông báo phải được ghi log.

<div style="page-break-after: always;"></div>

## Trang 4 - Quy trình thực hiện theo luồng nghiệp vụ

### 1. Quy trình người dùng đăng ký và chuẩn bị hồ sơ mượn sách

1. Người dùng truy cập website quản lý nhà sách.
2. Người dùng đăng ký tài khoản với tên đăng nhập, mật khẩu, họ tên, số điện thoại, địa chỉ và Gmail nhận thông báo.
3. Hệ thống kiểm tra định dạng email, số điện thoại, tên đăng nhập trùng và email đã tồn tại.
4. Nếu hợp lệ, hệ thống lưu tài khoản vào bảng người dùng.
5. Người dùng cập nhật ảnh CMND/CCCD mặt trước và mặt sau.
6. Website gửi ảnh sang Face API tại endpoint OCR CMND/CCCD.
7. API xử lý ảnh bằng PaddleOCR hoặc Tesseract, trích xuất số giấy tờ, họ tên, ngày sinh, giới tính, quốc tịch, địa chỉ, ngày cấp, ngày hết hạn và cơ quan cấp.
8. Nếu ảnh có khuôn mặt, API so khớp khuôn mặt trên giấy tờ với mẫu khuôn mặt của người dùng.
9. Website cập nhật hồ sơ định danh vào CSDL.

### 2. Quy trình đăng ký/xác thực khuôn mặt

1. Người dùng mở màn hình đăng ký khuôn mặt hoặc xác thực khuôn mặt.
2. Website yêu cầu chụp ảnh khuôn mặt.
3. Ảnh được lưu tạm vào thư mục `DataImage/FaceSamples`.
4. Website gọi API Flask để đăng ký hoặc xác thực.
5. API dùng InsightFace để phát hiện khuôn mặt và trích xuất embedding.
6. API kiểm tra chất lượng ảnh: có khuôn mặt, chỉ một khuôn mặt, ảnh đủ rõ và khuôn mặt đủ lớn.
7. Với đăng ký, embedding được lưu vào `face_db.pkl`.
8. Với xác thực, embedding ảnh hiện tại được so khớp với embedding đã đăng ký.
9. Kết quả trả về gồm `success`, `confidence`, `error_code`, `request_id`.
10. Website ghi log vào `FaceAuthLogs`.

### 3. Quy trình mượn sách

1. Người dùng mở trang chi tiết sách.
2. Người dùng chọn số lượng và số ngày mượn.
3. Website kiểm tra tồn kho và kiểm tra yêu cầu mượn đang còn hiệu lực.
4. Nếu hồ sơ thiếu Gmail/CMND/CCCD/họ tên, website yêu cầu cập nhật hồ sơ.
5. Người dùng xác thực khuôn mặt trước khi mượn.
6. Nếu xác thực thành công và độ tin cậy đạt ngưỡng, hệ thống sinh `faceToken`.
7. Người dùng gửi yêu cầu mượn kèm `faceToken`.
8. Server kiểm tra token, user, product, số ngày mượn và tồn kho.
9. Server tạo bản ghi `RentalRequests` với trạng thái `Pending`.
10. Server ghi log hành động `Request`.
11. Server gửi Gmail thông báo đã nhận yêu cầu mượn.

### 4. Quy trình admin duyệt/trả sách

1. Admin đăng nhập vào khu vực quản trị.
2. Admin mở danh sách yêu cầu mượn sách.
3. Admin xem thông tin người mượn, sách, số lượng, ngày yêu cầu, hạn trả và hồ sơ CMND/CCCD.
4. Nếu duyệt yêu cầu, hệ thống chuyển trạng thái sang `Borrowing`, giảm tồn kho và ghi log.
5. Nếu từ chối yêu cầu, hệ thống chuyển trạng thái sang `Rejected` và ghi log.
6. Khi người dùng trả sách, admin xác nhận trả, hệ thống chuyển trạng thái sang `Returned`, tăng tồn kho và ghi ngày trả thực tế.
7. Nếu quá hạn, admin hoặc hệ thống đánh dấu `Overdue`.
8. Sau mỗi thay đổi trạng thái, hệ thống gửi Gmail thông báo cho người dùng.

<div style="page-break-after: always;"></div>

## Trang 5 - Kế hoạch thực hiện từ tháng 01 đến tháng 05

### Tháng 01/2026 - Khảo sát, phân tích và lập kế hoạch

| Tuần | Nội dung thực hiện | Kết quả dự kiến |
|---|---|---|
| Tuần 1 | Khảo sát yêu cầu đề tài, xác định phạm vi quản lý nhà sách và chức năng mượn/trả sách | Danh sách yêu cầu chức năng và phi chức năng |
| Tuần 2 | Phân tích source ASP.NET MVC hiện có: controller, model, Entity Framework, cấu trúc CSDL | Tài liệu phân tích kiến trúc hiện trạng |
| Tuần 3 | Phân tích source Flask Face API, OCR CMND/CCCD và chatbox | Danh sách API tích hợp và công nghệ AI sử dụng |
| Tuần 4 | Lập kế hoạch triển khai, xác định các rủi ro về nhận diện khuôn mặt, OCR, Gmail và dữ liệu | Bản kế hoạch thực hiện phiên bản đầu |

Nội dung chi tiết trong tháng 01:

- Đọc cấu trúc solution `DongTrieuBookStore.sln`.
- Xác định các module chính: `BaiTapLon`, `Mood`, `Common`, `CommomSentMail`.
- Xác định nhóm controller: `UsersController`, `ProductController`, `CartController`, `RentalController`, `FaceAuthController`, `LogsController`.
- Xác định các bảng chính: Users, Sanpham, Orders, Order_Detail, RentalRequests, FaceAuthLogs, RentalLogs, ProductReviews.
- Xác định các API Flask: `/api/face/register`, `/api/face/verify`, `/api/face/authenticate`, `/api/face/action-check`, `/api/face/ocr-cmnd`, `/api/face/health`, `/api/chatbox/ask`, `/api/chatbox/widget.js`.

### Tháng 02/2026 - Thiết kế hệ thống và cơ sở dữ liệu

| Tuần | Nội dung thực hiện | Kết quả dự kiến |
|---|---|---|
| Tuần 1 | Thiết kế sơ đồ use case cho khách, người dùng, admin, Face API, Gmail và chatbox | Bản nháp use case |
| Tuần 2 | Thiết kế luồng mượn sách có xác thực khuôn mặt và kiểm tra hồ sơ định danh | Sơ đồ activity/sequence bản nháp |
| Tuần 3 | Rà soát bảng dữ liệu phục vụ mượn/trả, log, OCR và hồ sơ người dùng | Danh sách bảng/cột cần dùng |
| Tuần 4 | Thiết kế giao diện nghiệp vụ: chi tiết sách, hồ sơ mượn, xác thực khuôn mặt, quản trị mượn/trả | Wireframe hoặc mô tả giao diện |

Nội dung chi tiết trong tháng 02:

- Hoàn thiện đặc tả bảng `RentalRequests` cho yêu cầu mượn sách.
- Hoàn thiện đặc tả bảng `FaceAuthLogs`, `RentalLogs`, `GeofenceLogs` để lưu nhật ký.
- Thiết kế cơ chế `faceToken` ngắn hạn để tránh gửi yêu cầu mượn khi chưa xác thực.
- Thiết kế luồng OCR CMND/CCCD mặt trước, mặt sau.
- Thiết kế nội dung Gmail cho các sự kiện: Request, ApproveSuccess, Reject, Cancel, Return, Overdue.
- Chuẩn bị nội dung vẽ draw.io cho use case và quy trình.

### Tháng 03/2026 - Xây dựng và tích hợp chức năng chính

| Tuần | Nội dung thực hiện | Kết quả dự kiến |
|---|---|---|
| Tuần 1 | Hoàn thiện đăng ký, đăng nhập, cập nhật hồ sơ người dùng và Gmail nhận thông báo | Module tài khoản hoạt động ổn định |
| Tuần 2 | Tích hợp OCR CMND/CCCD vào hồ sơ người dùng và hồ sơ mượn sách | Người dùng cập nhật định danh từ ảnh giấy tờ |
| Tuần 3 | Tích hợp xác thực khuôn mặt trước khi mượn sách | Người dùng xác thực thành công mới được gửi yêu cầu mượn |
| Tuần 4 | Xây dựng quy trình tạo yêu cầu mượn, kiểm tra tồn kho, kiểm tra yêu cầu đang hiệu lực | Chức năng gửi yêu cầu mượn hoàn chỉnh |

Nội dung chi tiết trong tháng 03:

- Kiểm tra cấu hình `FaceAuthAPI` và timeout kết nối.
- Lưu ảnh khuôn mặt và ảnh CMND/CCCD vào đúng thư mục cấu hình.
- Xử lý phản hồi JSON từ Face API và OCR API.
- Ghi log xác thực khuôn mặt thành công/thất bại.
- Tạo yêu cầu mượn với trạng thái `Pending`.
- Gửi Gmail xác nhận hệ thống đã nhận yêu cầu.
- Kiểm thử các lỗi: chưa đăng nhập, thiếu hồ sơ, ảnh không hợp lệ, xác thực không đạt ngưỡng, sách hết tồn.

### Tháng 04/2026 - Hoàn thiện quản trị, thông báo và chatbox

| Tuần | Nội dung thực hiện | Kết quả dự kiến |
|---|---|---|
| Tuần 1 | Hoàn thiện màn hình admin duyệt mượn, từ chối, trả sách, đánh dấu quá hạn | Admin xử lý vòng đời mượn/trả |
| Tuần 2 | Tích hợp Gmail thông báo theo trạng thái và ghi nhận lỗi gửi mail | Người dùng nhận thông báo trạng thái |
| Tuần 3 | Tích hợp chatbox tư vấn sách và hướng dẫn mượn sách trên website | Chatbox hiển thị và trả lời được câu hỏi cơ bản |
| Tuần 4 | Kiểm thử liên thông website, Face API, OCR, Gmail và chatbox | Bộ test case tích hợp |

Nội dung chi tiết trong tháng 04:

- Duyệt yêu cầu mượn: chuyển `Pending` sang `Borrowing`, giảm tồn kho.
- Từ chối/hủy yêu cầu: chuyển sang `Rejected` hoặc `Cancelled`.
- Trả sách: chuyển sang `Returned`, tăng tồn kho, lưu `ActualReturnDate`.
- Quá hạn: chuyển sang `Overdue`, gửi nhắc nhở.
- Kiểm tra cấu hình Gmail SMTP: host, port, SSL, tài khoản gửi và mật khẩu ứng dụng.
- Tích hợp widget chatbox từ `/api/chatbox/widget.js`.
- Huấn luyện dữ liệu chatbox từ danh sách sản phẩm nếu cần.
- Ghi nhận lịch sử chatbox và phản hồi lỗi khi server chatbox không kết nối được.

### Tháng 05/2026 - Kiểm thử, hoàn thiện báo cáo và bàn giao

| Tuần | Nội dung thực hiện | Kết quả dự kiến |
|---|---|---|
| Tuần 1 | Kiểm thử chức năng người dùng, admin, mượn/trả, OCR, nhận diện và Gmail | Biên bản kiểm thử chức năng |
| Tuần 2 | Tối ưu giao diện, sửa lỗi phát sinh, chuẩn hóa thông báo lỗi | Phiên bản chạy ổn định |
| Tuần 3 | Hoàn thiện báo cáo: mở đầu, phân tích, thiết kế, triển khai, kiểm thử, kết luận | Báo cáo hoàn chỉnh bản nháp |
| Tuần 4 | Chèn sơ đồ draw.io, ảnh quy trình thực tế, phân trang, mục lục và rà soát cuối | Báo cáo hoàn chỉnh để nộp |

Nội dung chi tiết trong tháng 05:

- Kiểm thử đăng ký tài khoản và cập nhật hồ sơ định danh.
- Kiểm thử OCR với ảnh rõ, ảnh mờ, thiếu mặt trước/mặt sau và ảnh không phải CMND/CCCD.
- Kiểm thử xác thực khuôn mặt đúng người, sai người, nhiều khuôn mặt và ảnh chất lượng thấp.
- Kiểm thử mượn sách khi còn tồn, hết tồn, đã có yêu cầu đang chờ, quá số ngày mượn tối đa.
- Kiểm thử admin duyệt, từ chối, trả sách, quá hạn.
- Kiểm thử Gmail khi cấu hình đúng, sai app password, sai email gửi hoặc server SMTP không xác thực.
- Kiểm thử chatbox khi server đang chạy và khi server mất kết nối.
- Chụp ảnh từng quy trình từ ứng dụng thật để chèn vào báo cáo Word/PDF.

<div style="page-break-after: always;"></div>

## Trang 6 - Bảng phân công hạng mục và sản phẩm đầu ra

### 1. Hạng mục thực hiện

| STT | Hạng mục | Nội dung | Sản phẩm đầu ra |
|---|---|---|---|
| 1 | Khảo sát và phân tích | Thu thập yêu cầu, phân tích source, xác định nghiệp vụ | Tài liệu yêu cầu |
| 2 | Thiết kế dữ liệu | Mô tả bảng người dùng, sách, mượn trả, log, OCR | Sơ đồ CSDL và mô tả bảng |
| 3 | Thiết kế use case | Mô tả tác nhân và use case hệ thống | Sơ đồ use case draw.io |
| 4 | Thiết kế luồng xử lý | Mượn sách, trả sách, OCR, xác thực khuôn mặt, Gmail | Sơ đồ quy trình |
| 5 | Xây dựng website | Hoàn thiện chức năng ASP.NET MVC | Website quản lý nhà sách |
| 6 | Tích hợp Face API | Gọi API nhận diện khuôn mặt và OCR | Module xác thực/OCR |
| 7 | Tích hợp Gmail | Gửi thông báo mượn/trả sách | Module thông báo |
| 8 | Tích hợp chatbox | Tư vấn sách và hướng dẫn mượn | Widget chatbox |
| 9 | Kiểm thử | Test case chức năng và tích hợp | Biên bản kiểm thử |
| 10 | Báo cáo | Viết báo cáo, chèn hình, phân trang | File Word/PDF hoàn chỉnh |

### 2. Kết quả dự kiến khi hoàn thành

- Website quản lý nhà sách hoạt động trên môi trường local.
- Người dùng có thể xem sách, đăng ký, đăng nhập, cập nhật hồ sơ định danh và gửi yêu cầu mượn.
- Hệ thống xác thực khuôn mặt trước khi mượn sách.
- Hệ thống đọc CMND/CCCD để hỗ trợ nhập hồ sơ người dùng.
- Admin có thể duyệt, từ chối, trả sách và theo dõi lịch sử mượn/trả.
- Gmail thông báo được gửi theo trạng thái xử lý.
- Chatbox tư vấn được tích hợp vào giao diện website.
- Báo cáo có sơ đồ use case, quy trình, mô tả công nghệ, ảnh minh họa và kế hoạch thực hiện.

<div style="page-break-after: always;"></div>

## Trang 7 - Kế hoạch kiểm thử và tiêu chí nghiệm thu

### 1. Nhóm kiểm thử chức năng

| Nhóm kiểm thử | Trường hợp kiểm thử |
|---|---|
| Tài khoản | Đăng ký hợp lệ, đăng ký trùng email, đăng nhập đúng/sai, cập nhật hồ sơ |
| Sản phẩm | Xem danh sách, tìm kiếm, xem chi tiết, đánh giá, xem file review |
| OCR CMND/CCCD | Ảnh mặt trước, ảnh mặt sau, ảnh mờ, ảnh sai giấy tờ, thiếu ảnh |
| Nhận diện khuôn mặt | Đăng ký mẫu, xác thực đúng người, sai người, ảnh nhiều mặt, ảnh chất lượng thấp |
| Mượn sách | Mượn khi còn tồn, hết tồn, thiếu hồ sơ, chưa xác thực khuôn mặt |
| Admin mượn/trả | Duyệt, từ chối, hủy, trả sách, quá hạn, cập nhật tồn kho |
| Gmail | Gửi thành công, sai app password, sai email gửi, tắt thông báo |
| Chatbox | Hỏi tên sách, hỏi giá, hỏi tồn kho, hỏi hướng dẫn mượn |
| Nhật ký | Ghi log xác thực, log mượn trả, log lỗi thông báo |

### 2. Tiêu chí nghiệm thu

- Các chức năng chính không phát sinh lỗi dừng chương trình.
- Dữ liệu mượn/trả được lưu đúng trạng thái.
- Tồn kho thay đổi đúng khi duyệt mượn và xác nhận trả sách.
- Người dùng không thể gửi yêu cầu mượn nếu chưa xác thực khuôn mặt.
- OCR trích xuất được các trường cơ bản khi ảnh đủ rõ.
- Gmail hiển thị lỗi cụ thể khi cấu hình sai và gửi được khi cấu hình đúng.
- Chatbox hiển thị trên website và phản hồi được câu hỏi phổ biến.
- Báo cáo trình bày đúng bố cục, có phân trang, có sơ đồ và ảnh quy trình.

### 3. Rủi ro và phương án xử lý

| Rủi ro | Ảnh hưởng | Phương án xử lý |
|---|---|---|
| OCR đọc sai do ảnh mờ | Hồ sơ định danh thiếu hoặc sai | Kiểm tra chất lượng ảnh, cho phép người dùng chỉnh tay |
| Nhận diện khuôn mặt sai do ánh sáng/khoảng cách | Không xác thực được khi mượn | Hướng dẫn chụp lại, kiểm tra ảnh có một khuôn mặt, dùng ngưỡng confidence |
| Gmail không xác thực SMTP | Không gửi được thông báo | Dùng đúng app password, đúng email gửi, log lỗi SMTP chi tiết |
| Face API không chạy | Không OCR/xác thực được | Kiểm tra `/api/face/health`, hiển thị lỗi kết nối |
| Chatbox chưa có dữ liệu | Không tư vấn đúng sách | Huấn luyện lại từ database sản phẩm |
| Thiếu targets khi build project web cũ bằng CLI | Không build được bằng `dotnet build` | Build bằng Visual Studio/MSBuild có WebApplication targets |

<div style="page-break-after: always;"></div>

## Trang 8 - Ghi chú cho bản báo cáo Word/PDF sau khi duyệt kế hoạch

### 1. Các hình sẽ bổ sung sau

Trong bản kế hoạch xem trước này chưa chèn hình, theo đúng yêu cầu hiện tại là chỉ viết kế hoạch để xem trước. Khi chuyển sang báo cáo hoàn chỉnh sẽ bổ sung:

- Sơ đồ use case tổng quát bằng draw.io.
- Sơ đồ quy trình đăng ký và cập nhật CMND/CCCD.
- Sơ đồ quy trình xác thực khuôn mặt.
- Sơ đồ quy trình gửi yêu cầu mượn sách.
- Sơ đồ quy trình admin duyệt/trả sách.
- Ảnh chụp giao diện trang chủ, chi tiết sách, hồ sơ người dùng, xác thực khuôn mặt, OCR CMND/CCCD, danh sách mượn, màn hình admin và chatbox.

### 2. Cách đánh phân trang

File Markdown sử dụng thẻ:

```html
<div style="page-break-after: always;"></div>
```

Khi chuyển sang Word/PDF, mỗi phần từ Trang 1 đến Trang 8 sẽ được tách trang giống mẫu báo cáo. Nếu mẫu `Template.pdf` có yêu cầu header/footer/số trang riêng, phần này sẽ được căn chỉnh lại ở bước xuất Word/PDF.

### 3. Nội dung cần xác nhận trước khi viết báo cáo đầy đủ

- Tên trường, khoa, môn học và giảng viên hướng dẫn.
- Tên chính thức của hệ thống: giữ “QLNhaSach” hay đổi thành tên tiếng Việt đầy đủ.
- Có yêu cầu đưa mã nguồn minh họa vào phụ lục hay không.
- Có cần mô tả chi tiết thuật toán InsightFace/OCR hay chỉ mô tả mức ứng dụng.
- Có cần đưa phần đánh giá ưu/nhược điểm và hướng phát triển vào báo cáo chính hay không.

<div style="page-break-after: always;"></div>

## Trang 9 - Kế hoạch tối ưu báo cáo theo `Template.pdf`

### 1. Mục tiêu của lần sửa báo cáo

Lần sửa báo cáo này không chỉ viết lại nội dung theo cảm tính, mà cần chuẩn hóa báo cáo dựa trên ba nguồn chính:

- `Template.pdf`: dùng làm mẫu bố cục, trình tự chương mục, cách trình bày bìa, nhận xét, mục lục, danh mục hình/bảng, chương nội dung, kết luận, tài liệu tham khảo và phụ lục.
- Source website `QLNhaSach`: dùng làm căn cứ mô tả hệ thống ASP.NET MVC, Entity Framework, SQL Server, controller, service, view, cấu hình, bảng dữ liệu và luồng nghiệp vụ mượn/trả sách.
- Source Flask `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`: dùng làm căn cứ mô tả Face API, OCR CMND/CCCD, kiểm tra hành động khuôn mặt và chatbox tư vấn sách.

Ghi chú khi làm việc với `Template.pdf`: file mẫu là PDF nhiều trang, cần dùng để bám cấu trúc và định dạng. Nếu công cụ tự động không trích được toàn bộ chữ trong PDF thì vẫn phải mở mẫu để đối chiếu thủ công các phần: trang bìa, lời cảm ơn, nhận xét, mục lục, danh mục hình/bảng, quy định đánh số chương, kiểu tiêu đề, kiểu bảng, kiểu chú thích hình và phần phụ lục.

### 2. Thứ tự sửa báo cáo

| Bước | Nội dung cần làm | Kết quả cần đạt |
|---|---|---|
| 1 | Đối chiếu `Template.pdf` với file báo cáo hiện tại | Có danh sách mục còn thiếu, mục cần đổi tên và mục cần chuyển vị trí |
| 2 | Chuẩn hóa phần đầu báo cáo | Bìa, lời cảm ơn, nhận xét, mục lục, danh mục hình, danh mục bảng đúng mẫu |
| 3 | Viết lại chương 1 theo đề tài thực tế | Nêu lý do chọn đề tài, mục tiêu, phạm vi, phương pháp và bố cục báo cáo |
| 4 | Viết lại chương 2 theo công nghệ trong source | ASP.NET MVC, EF6, SQL Server, Flask, InsightFace, MediaPipe, OCR, Gmail, chatbox |
| 5 | Viết lại chương 3 theo phân tích thiết kế | Tác nhân, use case, CSDL, luồng mượn/trả, OCR, xác thực khuôn mặt, Gmail |
| 6 | Viết lại chương 4 theo triển khai source | Controller, service, model, view, API Flask, cấu hình tích hợp, ảnh giao diện |
| 7 | Viết chương 5 kiểm thử và đánh giá | Test case, kết quả kiểm thử, rủi ro, hạn chế, hướng khắc phục |
| 8 | Hoàn thiện kết luận, tài liệu tham khảo, phụ lục | Báo cáo có thể xuất Word/PDF để nộp |

### 3. Quy tắc tối ưu nội dung

- Mỗi nhận định kỹ thuật trong báo cáo phải có căn cứ từ source, cấu hình, database, màn hình hoặc tài liệu trong workspace.
- Không mô tả hệ thống như một website bán sách chung chung; cần nhấn mạnh điểm riêng của đề tài là mượn/trả sách có xác thực khuôn mặt, OCR CMND/CCCD, Gmail và chatbox.
- Không viết quá sâu theo kiểu tài liệu code từng hàm; báo cáo cần trình bày ở mức thiết kế, triển khai và kiểm thử.
- Các thuật ngữ phải thống nhất: dùng `người dùng`, `quản trị viên`, `yêu cầu mượn`, `xác thực khuôn mặt`, `OCR CMND/CCCD`, `Face API`, `chatbox`.
- Các tên file, controller, endpoint và bảng dữ liệu phải đặt trong dấu code khi xuất ở phụ lục hoặc phần triển khai.
- Khi nói về AI, cần ghi rõ hệ thống tích hợp mô hình/thư viện có sẵn, không tự huấn luyện mô hình nhận diện khuôn mặt từ đầu.

<div style="page-break-after: always;"></div>

## Trang 10 - Bố cục báo cáo đề xuất theo template

### 1. Phần đầu báo cáo

| Mục | Nội dung cần có | Ghi chú chỉnh sửa |
|---|---|---|
| Trang bìa | Tên trường, khoa, tên đề tài, sinh viên, MSSV, lớp, giảng viên, thời gian | Cần điền đúng thông tin còn thiếu theo mẫu |
| Lời cảm ơn | Cảm ơn giảng viên, khoa, người hỗ trợ | Viết ngắn, trang trọng |
| Nhận xét của giảng viên | Dòng trống hoặc bảng nhận xét theo mẫu | Giữ đúng bố cục `Template.pdf` |
| Mục lục | Tự động hoặc viết theo chương | Cập nhật sau khi hoàn tất báo cáo |
| Danh mục hình | Liệt kê toàn bộ hình minh họa | Hình use case, workflow, giao diện, API |
| Danh mục bảng | Liệt kê bảng công nghệ, chức năng, CSDL, test case | Đánh số bảng theo chương |

### 2. Chương 1 - Tổng quan đề tài

Nội dung cần viết:

- Lý do chọn đề tài: nhu cầu quản lý nhà sách, quản lý mượn/trả, xác thực người mượn và giảm nhập liệu giấy tờ.
- Mục tiêu đề tài: xây dựng website quản lý nhà sách, tích hợp Face API, OCR, Gmail và chatbox.
- Phạm vi đề tài: hệ thống local gồm source ASP.NET MVC `QLNhaSach` và Flask server `NHANDIENKHUONMAT-new07040226`.
- Phương pháp thực hiện: khảo sát source, phân tích nghiệp vụ, thiết kế CSDL, tích hợp API, kiểm thử chức năng.
- Bố cục báo cáo: tóm tắt các chương 1 đến 5.

### 3. Chương 2 - Cơ sở lý thuyết và công nghệ

Nội dung cần viết:

- ASP.NET MVC 5, C#, .NET Framework, Razor View.
- Entity Framework 6 và SQL Server LocalDB.
- Flask API, JSON, multipart form-data.
- InsightFace/ONNXRuntime cho nhận diện khuôn mặt.
- MediaPipe Face Landmarker cho kiểm tra hành động/liveness.
- PaddleOCR/Tesseract cho OCR CMND/CCCD.
- Gmail SMTP/API cho thông báo.
- Chatbox tư vấn sách dựa trên dữ liệu sản phẩm/knowledge base.

### 4. Chương 3 - Phân tích và thiết kế hệ thống

Nội dung cần viết:

- Tác nhân: khách vãng lai, người dùng, quản trị viên, Face API/OCR, Gmail, chatbox.
- Use case tổng quát và use case chi tiết cho mượn sách.
- Luồng xử lý đăng ký, đăng nhập, cập nhật hồ sơ, OCR, xác thực khuôn mặt, gửi yêu cầu mượn, admin duyệt/trả.
- Thiết kế dữ liệu: người dùng, sách, hóa đơn, mượn/trả, log xác thực, log mượn/trả, đánh giá, yêu thích.
- Ràng buộc nghiệp vụ: phải đăng nhập, phải có hồ sơ định danh, phải xác thực khuôn mặt, kiểm tra tồn kho, giới hạn ngày mượn.

### 5. Chương 4 - Triển khai hệ thống

Nội dung cần viết:

- Cấu trúc source `BaiTapLon`, `Mood`, `Common`, `CommomSentMail`, `face_auth_api` và source Flask ngoài.
- Các controller chính: `HomeController`, `ProductController`, `UsersController`, `FaceAuthController`, `RentalController`, `GeofenceController`, `LogsController`, `CartController`, `PromotionController`.
- Các service chính: `FaceAuthApiClient`, `FaceRentalTokenService`, `GmailNotificationService`, `StoreLocationService`.
- Các endpoint Flask: `/api/face/health`, `/api/face/register`, `/api/face/verify`, `/api/face/authenticate`, `/api/face/action-check`, `/api/face/ocr-cmnd`, `/api/chatbox/*`.
- Các cấu hình quan trọng trong `Web.config`: `FaceAuthAPI`, `ChatboxWidgetUrl`, `FaceAuthMinConfidence`, `FaceAuthRentalTokenMinutes`, `RentalMaxBorrowDays`, `GmailNotificationsEnabled`.
- Ảnh giao diện và mô tả từng màn hình.

### 6. Chương 5 - Kiểm thử và đánh giá

Nội dung cần viết:

- Môi trường kiểm thử: Windows, Visual Studio/MSBuild, SQL Server LocalDB, Flask chạy port `8000`.
- Test case theo nhóm: tài khoản, sản phẩm, OCR, khuôn mặt, mượn/trả, admin, Gmail, chatbox, log.
- Kết quả đạt được: mô tả chức năng đã hoạt động và chức năng còn cần hoàn thiện.
- Hạn chế: phụ thuộc camera/ánh sáng, OCR phụ thuộc chất lượng ảnh, Gmail phụ thuộc app password, Flask phải chạy song song.
- Hướng phát triển: dashboard thống kê, tối ưu OCR, triển khai production, phân quyền chi tiết, nâng cấp chatbox.

<div style="page-break-after: always;"></div>

## Trang 11 - Mapping source `QLNhaSach` vào nội dung báo cáo

### 1. Mapping theo thư mục

| Thư mục/file | Vai trò trong hệ thống | Đưa vào phần báo cáo |
|---|---|---|
| `DongTrieuBookStore.sln` | Solution chính của website | Chương 4 - cấu trúc triển khai |
| `BaiTapLon` | Project ASP.NET MVC, chứa controller, view, cấu hình web | Chương 2 và chương 4 |
| `Mood` | Model Entity Framework và lớp truy xuất dữ liệu | Chương 3 - thiết kế dữ liệu, chương 4 - triển khai |
| `Common` | Repository/log dùng chung | Chương 4 - ghi nhật ký |
| `CommomSentMail` | Helper gửi mail | Chương 4 - Gmail thông báo |
| `sql/create_database.sql` | Script tạo CSDL | Chương 3 - thiết kế CSDL, phụ lục |
| `sql/migrations` | Các migration bổ sung chức năng | Phụ lục hoặc chương 4 |
| `report_assets` | Hình use case, workflow, ảnh chụp giao diện | Danh mục hình, chương 3, chương 4 |
| `scripts/generate_report_docx.py` | Script tạo báo cáo Word và hình minh họa | Phụ lục quy trình tạo báo cáo |

### 2. Mapping theo controller/service

| Thành phần | Chức năng cần mô tả | Bằng chứng cần chèn/mô tả |
|---|---|---|
| `UsersController` | Đăng ký, đăng nhập, hồ sơ người dùng, đăng nhập Facebook, đăng ký khuôn mặt | Ảnh đăng nhập, đăng ký, profile, đăng ký face |
| `ProductController` | Danh sách sách, tìm kiếm, chi tiết sách, đánh giá, file review | Ảnh danh sách/chi tiết sách |
| `RentalController` | Tạo yêu cầu mượn, duyệt, từ chối, hủy, trả sách, quá hạn | Workflow mượn/trả và ảnh admin |
| `FaceAuthController` | Upload ảnh, gọi Flask, OCR, verify, action challenge, sinh token mượn | Sequence xử lý Face API |
| `LogsController` | Xem log xác thực, geofence, mượn/trả | Bảng log hoặc ảnh màn hình log |
| `CartController` | Đặt hàng, thanh toán, hóa đơn | Mô tả chức năng bán sách nền tảng |
| `GmailNotificationService` | Gửi Gmail theo trạng thái mượn/trả | Bảng sự kiện gửi mail |
| `FaceAuthApiClient` | Gọi HTTP sang Flask API | Mô tả contract request/response |
| `FaceRentalTokenService` | Quản lý token xác thực khuôn mặt khi mượn sách | Ràng buộc bảo mật nghiệp vụ |

### 3. Mapping cấu hình

| Key cấu hình | Giá trị đang dùng | Ý nghĩa trong báo cáo |
|---|---|---|
| `FaceAuthAPI` | `http://localhost:8000/api/face` | Base URL Flask Face API |
| `ChatboxWidgetUrl` | `http://localhost:8000/api/chatbox/widget.js` | URL nhúng chatbox vào website |
| `FaceAuthMinConfidence` | `0.75` | Ngưỡng chấp nhận xác thực khuôn mặt |
| `FaceAuthRentalTokenMinutes` | `3` | Thời hạn token xác thực khuôn mặt khi mượn |
| `RentalMaxBorrowDays` | `30` | Số ngày mượn tối đa |
| `GmailNotificationsEnabled` | `true` | Bật gửi thông báo Gmail |

<div style="page-break-after: always;"></div>

## Trang 12 - Mapping source Flask vào nội dung báo cáo

### 1. Thành phần Flask cần mô tả

| Thành phần | Vai trò | Đưa vào phần báo cáo |
|---|---|---|
| `app.py` | Server Flask chính, khai báo API nhận diện, OCR, action-check, health | Chương 4 - triển khai Face API |
| `face_db.pkl` | Lưu embedding khuôn mặt theo user | Chương 3 - thiết kế dữ liệu phụ trợ |
| `models/face_landmarker.task` | Model MediaPipe dùng kiểm tra hành động khuôn mặt | Chương 2 - công nghệ, chương 4 - triển khai |
| `requirements.txt` | Danh sách dependency Flask/OCR/AI | Phụ lục cài đặt |
| `sales_chatbox` | Module chatbox tư vấn sách | Chương 4 - chatbox |
| `sales_chatbox/chatbox_knowledge.json` | Knowledge base của chatbox | Chương 4 hoặc phụ lục |
| `LICHSU_THUCHIEN.md` | Log quá trình xử lý phía Flask | Phụ lục hoặc chương kiểm thử |

### 2. Endpoint Face API cần đưa vào bảng báo cáo

| Endpoint | Method | Chức năng |
|---|---|---|
| `/api/face/health` | GET | Kiểm tra Flask, model nhận diện, OCR, action model, chatbox |
| `/api/face/register` | POST | Đăng ký/cập nhật mẫu khuôn mặt cho user |
| `/api/face/verify` | POST | Xác thực khuôn mặt 1:1 theo user |
| `/api/face/authenticate` | POST | Xác thực khuôn mặt cho luồng MFA |
| `/api/face/action-check` | POST | Kiểm tra hành động như quay trái, quay phải, mở miệng, cười |
| `/api/face/ocr-cmnd` | POST | OCR CMND/CCCD mặt trước/mặt sau |
| `/api/chatbox/ask` | POST | Trả lời câu hỏi về sách, giá, tồn kho, hướng dẫn mượn |
| `/api/chatbox/widget.js` | GET | Script nhúng chatbox vào giao diện website |

### 3. Luồng Flask cần viết trong báo cáo

Luồng đăng ký khuôn mặt:

1. ASP.NET MVC nhận ảnh từ trình duyệt.
2. MVC lưu ảnh tạm và gửi `multipart/form-data` sang `/api/face/register`.
3. Flask kiểm tra file, định dạng, dung lượng và ảnh hợp lệ.
4. InsightFace phát hiện khuôn mặt, kiểm tra chỉ một khuôn mặt và chất lượng ảnh.
5. Flask lưu embedding vào `face_db.pkl`.
6. Flask trả JSON gồm `success`, `confidence`, `request_id`, `user_id`.
7. MVC ghi log vào hệ thống.

Luồng xác thực khi mượn sách:

1. Người dùng chọn sách và bắt đầu xác thực khuôn mặt.
2. MVC yêu cầu action challenge như `turn_left`, `turn_right`, `mouth_open`, `smile`.
3. MVC gửi frame webcam sang `/api/face/action-check`.
4. Flask dùng MediaPipe Face Landmarker để tính yaw, pitch, mouth ratio hoặc smile ratio.
5. Khi `action_matched=true`, MVC tiếp tục gọi `/api/face/verify`.
6. Nếu `confidence >= 0.75`, MVC sinh `faceToken` có hạn 3 phút.
7. Người dùng gửi yêu cầu mượn sách kèm `faceToken`.

Luồng OCR CMND/CCCD:

1. Người dùng tải ảnh mặt trước/mặt sau CMND/CCCD.
2. MVC gửi ảnh sang endpoint OCR của Flask.
3. Flask dùng PaddleOCR hoặc Tesseract để đọc text.
4. Flask parse số giấy tờ, họ tên, ngày sinh, địa chỉ, ngày cấp, nơi cấp.
5. Nếu có khuôn mặt trên giấy tờ, Flask có thể so khớp với mẫu khuôn mặt user.
6. MVC cập nhật hồ sơ định danh và ghi nhận lỗi nếu OCR không hợp lệ.

<div style="page-break-after: always;"></div>

## Trang 13 - Danh sách hình, bảng và phụ lục cần bổ sung

### 1. Hình cần có trong báo cáo

| Mã hình | Nội dung | File/nguồn đề xuất |
|---|---|---|
| Hình 3.1 | Use case tổng quát | `report_assets/usecase_quan_ly_nha_sach.png` |
| Hình 3.2 | Quy trình người dùng mượn sách | `report_assets/workflow_muon_sach.png` |
| Hình 3.3 | Quy trình OCR và xác thực khuôn mặt | `report_assets/workflow_ocr_face.png` |
| Hình 3.4 | Quy trình admin xử lý mượn/trả | `report_assets/workflow_admin.png` |
| Hình 4.1 | Trang chủ website | `report_assets/screenshot_home.png` |
| Hình 4.2 | Danh sách sản phẩm | `report_assets/screenshot_product_list.png` |
| Hình 4.3 | Trang đăng nhập | `report_assets/screenshot_login.png` |
| Hình 4.4 | Màn hình mượn/trả hoặc danh sách mượn | `report_assets/screenshot_rentals.png` |
| Hình 4.5 | Màn hình OCR CMND/CCCD | Chụp bổ sung từ ứng dụng |
| Hình 4.6 | Màn hình xác thực khuôn mặt/action challenge | Chụp bổ sung từ ứng dụng |
| Hình 4.7 | Màn hình chatbox tư vấn sách | Chụp bổ sung từ website khi Flask chạy |
| Hình 4.8 | Kết quả health check Flask | Chụp JSON `/api/face/health` hoặc trình bày bảng |

### 2. Bảng cần có trong báo cáo

| Mã bảng | Nội dung |
|---|---|
| Bảng 2.1 | Công nghệ sử dụng phía ASP.NET MVC |
| Bảng 2.2 | Công nghệ sử dụng phía Flask Face API/OCR/chatbox |
| Bảng 3.1 | Tác nhân và vai trò |
| Bảng 3.2 | Danh sách use case chính |
| Bảng 3.3 | Mô tả bảng dữ liệu chính |
| Bảng 4.1 | Cấu trúc thư mục source |
| Bảng 4.2 | Controller/service chính |
| Bảng 4.3 | Endpoint Flask và chức năng |
| Bảng 4.4 | Cấu hình tích hợp trong `Web.config` |
| Bảng 5.1 | Kịch bản kiểm thử chức năng |
| Bảng 5.2 | Rủi ro và phương án xử lý |

### 3. Phụ lục nên đưa vào cuối báo cáo

- Phụ lục A: Hướng dẫn chạy website ASP.NET MVC.
- Phụ lục B: Hướng dẫn chạy Flask server tại `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`.
- Phụ lục C: Contract request/response Face API.
- Phụ lục D: Một số đoạn code minh họa ngắn cho `FaceAuthApiClient`, `RentalController`, `GmailNotificationService`, `app.py`.
- Phụ lục E: Script SQL/migration chính.
- Phụ lục F: Nhật ký viết báo cáo và các file sinh kèm.

<div style="page-break-after: always;"></div>

## Trang 14 - Checklist nghiệm thu file báo cáo sau khi sửa

### 1. Checklist định dạng theo template

- Trang bìa đúng mẫu, có đủ tên trường, khoa, tên đề tài, sinh viên, MSSV, lớp, giảng viên, thời gian.
- Font thống nhất, ưu tiên Times New Roman, cỡ chữ nội dung 13 hoặc theo `Template.pdf`.
- Lề trang, giãn dòng, đánh số trang và header/footer bám theo mẫu.
- Tiêu đề chương, mục, tiểu mục đánh số nhất quán.
- Mục lục, danh mục hình, danh mục bảng cập nhật đúng số trang.
- Hình có chú thích dạng `Hình x.y. ...`.
- Bảng có chú thích dạng `Bảng x.y. ...`.
- Không để hình/bảng bị vỡ trang khó đọc.
- Các đường dẫn file/code chỉ đưa vào phụ lục hoặc phần triển khai, không rải quá nhiều trong chương tổng quan.

### 2. Checklist nội dung kỹ thuật

- Chương 1 nêu đúng vấn đề quản lý nhà sách và nhu cầu xác thực khi mượn/trả.
- Chương 2 có đủ công nghệ ASP.NET MVC, EF6, SQL Server, Flask, InsightFace, MediaPipe, OCR, Gmail, chatbox.
- Chương 3 có use case, luồng nghiệp vụ, thiết kế dữ liệu và ràng buộc mượn/trả.
- Chương 4 mô tả đúng source thực tế, không ghi controller/service không tồn tại.
- Chương 4 có bảng endpoint Flask đúng với `app.py`.
- Chương 4 ghi đúng các cấu hình `FaceAuthAPI`, `ChatboxWidgetUrl`, `FaceAuthMinConfidence`, `FaceAuthRentalTokenMinutes`, `RentalMaxBorrowDays`, `GmailNotificationsEnabled`.
- Chương 5 có test case cho cả website, Face API, OCR, Gmail và chatbox.
- Kết luận có đánh giá kết quả đạt được, hạn chế và hướng phát triển.
- Tài liệu tham khảo có nguồn công nghệ và source nội bộ.
- Phụ lục đủ hướng dẫn chạy và contract API.

### 3. Checklist kiểm tra trước khi xuất PDF

| Mục kiểm tra | Cách kiểm tra | Đạt khi |
|---|---|---|
| Build website | Build bằng Visual Studio/MSBuild phù hợp WebApplication targets | Không lỗi build nghiêm trọng |
| Flask health | Mở `http://localhost:8000/api/face/health` | Trả JSON `status=ok` |
| Ảnh báo cáo | Mở từng file trong `report_assets` | Ảnh rõ, đúng nội dung, không lỗi font |
| Mục lục | Cập nhật trong Word | Số trang đúng |
| Hình/bảng | Kiểm tra danh mục hình/bảng | Không thiếu chú thích |
| Chính tả | Rà soát toàn file | Không còn lỗi font/mojibake |
| PDF cuối | Xuất từ Word sang PDF | Mở được, đúng trang, không lệch bố cục |
