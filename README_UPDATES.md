# README — Nâng cấp FaceAuth / Geofencing / Logs

Tóm tắt thay đổi:

- Thêm cấu hình `FaceAuthAPI` trong `BaiTapLon/Web.config` để gọi API Python.
- Tích hợp thu thập khuôn mặt: views `Views/Users/RegisterFace.cshtml`, `LoginMFA.cshtml` và `Scripts/FaceCapture.js`.
- Các controller mới: `FaceAuthController`, `GeofenceController`, `RentalController` (ghi logs).
- Logging: models `Mood/EF2/FaceAuthLog.cs`, `GeofenceLog.cs`, `RentalLog.cs`, và `Mood/EF2/LogDbContext.cs`.
- API cho admin lấy logs: `BaiTapLon/Controllers/Api/LogsController.cs`.
- Admin views: `Areas/Admin/Views/Logs/*` và `Areas/Admin/Views/ThongKe/Index.cshtml` (Chart.js).
- Migration SQL mẫu: `sql/migrations/20260508_add_logs.sql` và hướng dẫn `sql/README_migrations.md`.

Chạy nhanh (staging):

1. Tạo bảng logs bằng SQL script hoặc EF migration.
2. Đặt `FaceAuthAPI` trong `BaiTapLon/Web.config` trỏ tới API Python.
3. Đảm bảo thư mục `DataImage/FaceSamples/` có quyền ghi cho ứng dụng.

Ghi chú bảo mật:
- Logs chứa ảnh và vị trí; giới hạn truy cập trang Admin và cân nhắc mã hóa/ẩn dữ liệu nhạy cảm.
 
## Version 5 - Chatbox ban hang

- Ket noi widget chatbox Flask vao layout khach hang `BaiTapLon/Views/Shared/_LayoutHome.cshtml`.
- Them cau hinh `ChatboxWidgetUrl` va `ChatboxEnabled` trong `BaiTapLon/Web.config`.
- Du lieu chatbox duoc train tu database `QLNhaSach.dbo.Sanpham` tai du an Flask `NHANDIENKHUONMAT-new07040226/sales_chatbox`.

## Version 5 - 2026-05-10

- Guest favorites are stored locally in the browser and can be viewed at `/yeu-thich` without logging in.
- Admin products support review-file upload and a YouTube URL.
- Product details show review-file popup, YouTube video tab, and customer rating/comment form.
- Database migration: `sql/migrations/20260510_add_product_reviews_version5.sql`.

---

## TÀI LIỆU API HỆ THỐNG QUẢN LÝ NHÀ SÁCH & NHẬN DIỆN KHUÔN MẶT (API SPECIFICATION)

Tài liệu này đặc tả chi tiết toàn bộ các API Endpoints trong hệ thống DongTrieuBookStore, bao gồm các ASP.NET MVC Controllers (C#) phía Backend Web và các Python Flask API Services phía AI/Microservices.

---

### PHẦN I: ASP.NET MVC CONTROLLERS (C# BACKEND)

Các endpoint này xử lý phiên làm việc của người dùng, giao tiếp với cơ sở dữ liệu SQL Server thông qua Entity Framework (`QuanLySachDBContext`, `LogDbContext`) và điều phối các yêu cầu nhận dạng đến microservice Python Flask.

#### 1. FaceAuthController (`Controllers/FaceAuthController.cs`)
Controller chịu trách nhiệm xử lý các luồng đăng ký khuôn mặt, đăng nhập xác thực đa yếu tố (MFA), tạo và kiểm tra các thử thách hành động (Liveness Challenge), xác thực khuôn mặt khi mượn sách, và kiểm tra OCR giấy tờ tùy thân.

*   **1.1 Kiểm tra OCR CMND/CCCD Nháp (Draft OCR)**
    *   **Route:** `/FaceAuth/OcrCmndDraft`
    *   **HTTP Method:** `POST`
    *   **Yêu cầu xác thực:** Không (AllowAnonymous)
    *   **Đầu vào (Multipart Form-Data):**
        *   `front_file` hoặc `frontFile` hoặc `front` hoặc `file` (HttpPostedFileBase): Ảnh mặt trước CMND/CCCD.
        *   `back_file` hoặc `backFile` hoặc `back` (HttpPostedFileBase, optional): Ảnh mặt sau CMND/CCCD.
    *   **Phản hồi (JSON):**
        *   *Thành công:* `{ "success": true, "imagePath": "...", "frontImagePath": "...", "backImagePath": "...", "fields": { "identityNumber": "...", "fullName": "...", "dateOfBirth": "...", "address": "...", "placeOfBirth": "...", "gender": "...", "nationality": "...", "issueDate": "...", "issuePlace": "...", "expiryDate": "...", "issuingAuthority": "...", "mrz": "..." }, "message": "..." }`
        *   *Thất bại:* `{ "success": false, "message": "Mô tả lỗi..." }`

*   **1.2 Kiểm tra OCR CMND/CCCD Chính thức & Cập nhật User**
    *   **Route:** `/FaceAuth/OcrCmnd`
    *   **HTTP Method:** `POST`
    *   **Yêu cầu xác thực:** Có (Yêu cầu đăng nhập, kiểm tra User Session)
    *   **Đầu vào (Multipart Form-Data):**
        *   `front_file` hoặc `frontFile` hoặc `front` hoặc `file` (HttpPostedFileBase): Ảnh mặt trước CMND/CCCD.
        *   `back_file` hoặc `backFile` hoặc `back` (HttpPostedFileBase, optional): Ảnh mặt sau CMND/CCCD.
    *   **Phản hồi (JSON):**
        *   *Thành công:* `{ "success": true, "imagePath": "...", "frontImagePath": "...", "backImagePath": "...", "fields": { "identityNumber": "...", "fullName": "...", "dateOfBirth": "...", "address": "...", "placeOfBirth": "...", "gender": "...", "nationality": "...", "issueDate": "...", "issuePlace": "...", "expiryDate": "...", "issuingAuthority": "...", "mrz": "..." }, "faceMatched": true, "faceConfidence": 0.85, "message": "..." }`
        *   *Thất bại:* `{ "success": false, "message": "Lỗi session hoặc lỗi OCR..." }`
    *   **Mô tả hoạt động:** Gửi ảnh sang Flask `/api/face/ocr-cmnd`. Nếu thành công, tự động trích xuất thông tin, cập nhật thông tin chi tiết vào bảng `Users` và so khớp ảnh thẻ với khuôn mặt đã đăng ký của user đó.

*   **1.3 Xác thực khuôn mặt mượn sách (Rental Face Verification)**
    *   **Route:** `/FaceAuth/VerifyRentalFace`
    *   **HTTP Method:** `POST`
    *   **Yêu cầu xác thực:** Có
    *   **Đầu vào (Form-Data):**
        *   `productId` (long): Mã sách đang muốn mượn.
        *   `challengeToken` (string, optional): Token thử thách hành động (nếu hệ thống yêu cầu liveness).
        *   `file` (HttpPostedFileBase): File ảnh chụp khuôn mặt trực tiếp từ webcam.
    *   **Phản hồi (JSON):**
        *   *Thành công:* `{ "success": true, "confidence": 0.92, "faceToken": "token-cho-phep-muon-sach" }`
        *   *Thất bại:* `{ "success": false, "confidence": 0.45, "message": "Xác nhận khuôn mặt thất bại..." }`
    *   **Mô tả hoạt động:** Xác thực khuôn mặt 1-1 với ảnh mẫu của user. Nếu khớp, sinh ra mã xác thực dùng một lần `faceToken` lưu trong `FaceRentalTokenService` để thực hiện gửi yêu cầu mượn sách ngay sau đó. Lưu log hành động `RentalFaceVerifySuccess` hoặc `RentalFaceVerifyFailed` vào `FaceAuthLogs`.

*   **1.4 Xác thực đăng nhập khuôn mặt (Face Login)**
    *   **Route:** `/FaceAuth/AuthenticateFaceLogin`
    *   **HTTP Method:** `POST`
    *   **Yêu cầu xác thực:** Không
    *   **Đầu vào (Multipart Form-Data):**
        *   `userName` (string): Tên đăng nhập của tài khoản.
        *   `challengeToken` (string, optional): Token thử thách hành động.
        *   `file` (HttpPostedFileBase): File ảnh khuôn mặt từ webcam.
    *   **Phản hồi (JSON):**
        *   *Thành công:* `{ "success": true, "redirectUrl": "/Home/TrangChu" }`
        *   *Thất bại:* `{ "success": false, "confidence": 0.35, "error": "Chi tiết lỗi..." }`
    *   **Mô tả hoạt động:** Kiểm tra sự tồn tại và trạng thái tài khoản. Gửi ảnh đến Flask `/api/face/verify` để xác thực 1-1 với ảnh mẫu đã đăng ký của tài khoản này. Nếu thành công, tiến hành thiết lập Cookie đăng nhập cho người dùng.

*   **1.5 Yêu cầu tạo thử thách liveness (Create Action Challenge)**
    *   **Route:** `/FaceAuth/CreateChallenge`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form/JSON):**
        *   `purpose` (string): Mục đích kiểm tra (`Login`, `Rental`, `MFA`, hoặc `Verify`).
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "actionRequired": true, "token": "uuid-token", "actionCode": "turn_left", "instruction": "Quay mat sang trai", "expiresInSeconds": 90 }`
    *   **Mô tả hoạt động:** Trích xuất ngẫu nhiên 1 trong các hành động cử chỉ (`turn_left`, `turn_right`, `mouth_open`, `smile`, `look_up`, `look_down`) và lưu thông tin thử thách vào Session trong vòng 90 giây.

*   **1.6 Xác minh cử chỉ hành động thử thách (Check Challenge Action)**
    *   **Route:** `/FaceAuth/CheckChallengeAction`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `purpose` (string): Mục đích thực hiện.
        *   `challengeToken` (string): Token thử thách vừa nhận từ `/FaceAuth/CreateChallenge`.
        *   `userName` (string, optional): Tên tài khoản.
        *   `file` (HttpPostedFileBase): Khung hình ảnh webcam chụp khi thực hiện cử chỉ.
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "actionMatched": true, "actionCode": "turn_left", "instruction": "Quay mat sang trai", "requestId": "...", "message": "Hanh dong da khop." }`
    *   **Mô tả hoạt động:** Gửi ảnh đến Flask `/api/face/action-check` kèm mã hành động để xác định liveness. Nếu chính xác, cập nhật trạng thái `ActionPassed` trong Session thành `true` làm điều kiện cần cho bước xác thực chính.

*   **1.7 Đăng ký khuôn mặt mới (Register Face)**
    *   **Route:** `/FaceAuth/RegisterFace`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `userId` (int): ID người dùng đăng ký.
        *   `file` (HttpPostedFileBase): File ảnh khuôn mặt mẫu.
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "confidence": 1.0, "message": "Đăng ký khuôn mặt thành công.", "requestId": "..." }`

*   **1.8 Xác thực khuôn mặt thông thường (Verify Face)**
    *   **Route:** `/FaceAuth/VerifyFace`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `userId` (int): ID người dùng.
        *   `file` (HttpPostedFileBase): File ảnh khuôn mặt.
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "confidence": 0.88 }`

*   **1.9 Xác thực đa yếu tố MFA (Authenticate Face)**
    *   **Route:** `/FaceAuth/AuthenticateFace`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `userId` (int): ID người dùng.
        *   `password` (string, optional): Mật khẩu tài khoản (nếu cần xác thực kết hợp).
        *   `challengeToken` (string, optional): Token thử thách hành động.
        *   `file` (HttpPostedFileBase, optional): File ảnh xác thực.
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "confidence": 0.91 }`

---

#### 2. GeofenceController (`Controllers/GeofenceController.cs`)
Controller thực hiện việc định vị và kiểm tra vị trí thực tế của khách hàng so với bán kính cho phép của các chi nhánh cửa hàng sách hoạt động.

*   **2.1 Kiểm tra hàng rào địa lý (Geofencing Verification)**
    *   **Route:** `/Geofence/CheckGeofence`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form/Query):**
        *   `lat` (decimal, optional): Vĩ độ của người dùng.
        *   `lon` (decimal, optional): Kinh độ của người dùng.
        *   `userId` (int, optional): Mã người dùng gửi lên.
    *   **Phản hồi (JSON):**
        *   *Thành công (nằm trong vùng):* `{ "inZone": true, "distance": 1.25, "radiusKm": 5.0, "storeId": 1, "storeName": "Dong Trieu Bookstore Center" }`
        *   *Không nằm trong vùng hoặc lỗi:* `{ "inZone": false, "distance": 12.8, "radiusKm": 5.0, "storeId": 1, "storeName": "..." }` hoặc `{ "inZone": false, "error": "Không nhận được tọa độ từ trình duyệt. Vui lòng cấp quyền vị trí và thử lại." }`
    *   **Mô tả hoạt động:** 
        1. Sử dụng công thức Haversine để tính khoảng cách thực giữa tọa độ người dùng gửi lên và tọa độ của các cửa hàng đang kích hoạt trong DB.
        2. So khớp khoảng cách với bán kính được cấu hình trên cửa hàng đó (hoặc bán kính mặc định trong cấu hình Web.config).
        3. Ghi log lịch sử xác thực địa lý vào bảng `GeofenceLogs`.

---

#### 3. RentalController (`Controllers/RentalController.cs`)
Xử lý các nghiệp vụ liên quan đến mượn sách, quản lý số lượng tồn kho, kiểm tra trạng thái tài khoản và thông báo kết quả qua Email.

*   **3.1 Lấy danh sách sách đang mượn cá nhân**
    *   **Route:** `/Rental/MyRentals`
    *   **HTTP Method:** `GET`
    *   **Tham số:** `status` (string, optional: `Pending`, `Borrowing`, `Overdue`, `Returned`).
    *   **Phản hồi:** Trả về giao diện HTML danh sách đơn mượn của cá nhân.

*   **3.2 Lấy số lượng yêu cầu mượn đang hoạt động**
    *   **Route:** `/Rental/ActiveRentalCount`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (JSON):** `{ "success": true, "count": 2 }`

*   **3.3 Kiểm tra tồn kho sách**
    *   **Route:** `/Rental/CheckStock`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form):**
        *   `productId` (int): Mã sách.
        *   `quantity` (int, optional, mặc định là 1): Số lượng sách cần mượn.
    *   **Phản hồi (JSON):** `{ "success": true, "available": true, "stock": 15 }`

*   **3.4 Kiểm tra sách có đang trong đơn mượn hoạt động nào không**
    *   **Route:** `/Rental/CheckActiveRental`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form):**
        *   `productId` (int): Mã sách.
    *   **Phản hồi (JSON):** `{ "success": true, "hasActiveRental": false }`

*   **3.5 Kiểm tra thông tin hồ sơ mượn sách**
    *   **Route:** `/Rental/RentalProfileStatus`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (JSON):** 
        *   `{ "success": true, "requireUpdate": false, "missingNotificationEmail": false, "missingIdentity": false, "missingIdentityImage": false, "notificationEmail": "khachhang@gmail.com", "identityNumber": "...", "identityFullName": "..." }`

*   **3.6 Cập nhật thông tin mượn sách & OCR giấy tờ**
    *   **Route:** `/Rental/UpdateRentalProfile`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `notificationEmail` (string): Gmail nhận thông báo.
        *   `identityNumber` (string): Số CMND/CCCD.
        *   `identityFullName` (string): Họ tên trên giấy tờ.
        *   `identityCardFrontFile` / `front_file` / `identityCardFile` (HttpPostedFileBase, optional): Ảnh mặt trước.
        *   `identityCardBackFile` / `back_file` (HttpPostedFileBase, optional): Ảnh mặt sau.
    *   **Phản hồi (JSON):** `{ "success": true, "identityCardImagePath": "...", "identityCardFrontImagePath": "...", "identityCardBackImagePath": "...", "identityNumber": "...", "identityFullName": "..." }`

*   **3.7 Gửi yêu cầu mượn sách mới**
    *   **Route:** `/Rental/RequestRental`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form):**
        *   `productId` hoặc `rentalId` (int): Mã sách.
        *   `userId` (long, optional): ID người mượn.
        *   `details` (string, optional): Ghi chú mượn sách.
        *   `quantity` (int, mặc định 1): Số lượng mượn.
        *   `borrowDays` (int, mặc định 1): Số ngày mượn mong muốn (tối đa 30 ngày).
        *   `faceToken` (string): Token xác thực khuôn mặt đã hoàn tất tại `/FaceAuth/VerifyRentalFace`.
    *   **Phản hồi (JSON):**
        *   *Thành công:* `{ "success": true, "rentalId": 12, "status": "Pending", "expectedReturnDate": "2026-07-10", "activeRentalCount": 1 }`
        *   *Thất bại:* `{ "success": false, "error": "Chi tiết lỗi..." }`

*   **3.8 Hủy yêu cầu mượn sách**
    *   **Route:** `/Rental/CancelRental`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Form):**
        *   `id` (int): ID của yêu cầu mượn sách.
    *   **Phản hồi:** Redirect về trang cá nhân `MyRentals`.

*   **3.9 Cập nhật trạng thái phê duyệt mượn/trả sách (Dành cho Admin)**
    *   **Route:** `/Rental/UpdateRentalStatus`
    *   **HTTP Method:** `POST`
    *   **Yêu cầu xác thực:** Có (Quyền quản trị viên)
    *   **Đầu vào (Form):**
        *   `rentalId` (int): Mã đơn mượn.
        *   `status` (string): Trạng thái hành động duyệt (`Approve`, `Reject`, `Return`, `Overdue`, `Cancel`).
        *   `adminId` (long, optional): ID admin duyệt.
    *   **Phản hồi (JSON):**
        *   `{ "success": true, "status": "Borrowing", "mailSent": true, "mailMessage": "Gửi mail thành công", "mailRecipient": "khachhang@gmail.com" }`

---

#### 4. HealthController (`Controllers/HealthController.cs`)
Cung cấp dịch vụ kiểm tra nhanh trạng thái vận hành của Backend và kết nối với Face API.

*   **4.1 Kiểm tra hoạt động hệ thống (System Ping)**
    *   **Route:** `/Health/Ping`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (Plain Text):** `OK`

*   **4.2 Kiểm tra kết nối cấu hình Face API**
    *   **Route:** `/Health/FaceApi`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (Plain Text):** `OK` (Trả về lỗi `500 Face API not configured` nếu chuỗi cấu hình `FaceAuthAPI` trong Web.config trống).

---

#### 5. LogsController (`Controllers/Api/LogsController.cs`)
Cung cấp dữ liệu log hệ thống phục vụ hiển thị biểu đồ và bảng dữ liệu phía quản trị. Yêu cầu tài khoản có phân quyền `Admin`.

*   **5.1 Lấy Logs xác thực khuôn mặt**
    *   **Route:** `/Api/Logs/Face`
    *   **HTTP Method:** `GET` hoặc `POST`
    *   **Tham số truy vấn:** `page`, `pageSize`, `userId`, `action`, `fromDate`, `toDate`, `result`.
    *   **Phản hồi (JSON):** Mảng danh sách các bản ghi log khuôn mặt từ DB.

*   **5.2 Lấy Logs vị trí Geofence**
    *   **Route:** `/Api/Logs/Geofence`
    *   **HTTP Method:** `GET` hoặc `POST`
    *   **Tham số truy vấn:** `page`, `pageSize`, `userId`, `storeId`, `fromDate`, `toDate`, `inZone`.
    *   **Phản hồi (JSON):** Mảng danh sách các bản ghi log vị trí từ DB.

*   **5.3 Lấy Logs mượn trả sách**
    *   **Route:** `/Api/Logs/Rental`
    *   **HTTP Method:** `GET` hoặc `POST`
    *   **Tham số truy vấn:** `page`, `pageSize`, `userId`, `rentalId`, `action`, `fromDate`, `toDate`.
    *   **Phản hồi (JSON):** Mảng danh sách các bản ghi log mượn trả sách từ DB.

---

### PHẦN II: PYTHON FLASK APIS (AI & MICROSERVICES)

Dịch vụ Python chạy ngầm (mặc định cổng `8082`) cung cấp khả năng xử lý học sâu (Deep Learning) về nhận diện khuôn mặt, phát hiện hành động liveness chống giả mạo, trích xuất dữ liệu thẻ CCCD/CMND bằng OCR, và Chatbox tư vấn bán hàng.

#### 1. Dịch vụ Face Analysis & OCR (`app.py`)

*   **1.1 Kiểm tra trạng thái dịch vụ (Health Check)**
    *   **Route:** `/api/face/health`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (JSON):**
        ```json
        {
          "status": "ok",
          "models_loaded": {
            "insightface": true,
            "mediapipe_landmarker": true
          },
          "liveness_backend": "tasks.face_landmarker",
          "ocr_backends": {
            "paddleocr": true,
            "tesseract": true
          },
          "storage_ready": true,
          "version": "1.4.1-face-action-required"
        }
        ```

*   **1.2 Đăng ký vector khuôn mặt (Register Face Embedding)**
    *   **Route:** `/api/face/register`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `file` (File Binary): Ảnh chụp chân dung khuôn mặt trực tiếp.
        *   `user_id` hoặc `userId` (string): ID duy nhất của người dùng.
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "matched": true,
          "confidence": 1.0,
          "quality_score": 1.0,
          "user_id": "10025",
          "userId": "10025",
          "external_user_id": "face-profile-10025",
          "externalUserId": "face-profile-10025",
          "liveness_passed": true,
          "livenessPassed": true,
          "request_id": "9a5d12ef...",
          "requestId": "9a5d12ef...",
          "purpose": "Register"
        }
        ```

*   **1.3 So khớp khuôn mặt (Verify Face)**
    *   **Route:** `/api/face/verify`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `file` (File Binary): Ảnh khuôn mặt cần kiểm tra.
        *   `user_id` hoặc `userId` (string): ID người dùng đã đăng ký mẫu trước đó.
        *   `purpose` (string, optional): Mục đích (ví dụ: `Rental`).
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "matched": true,
          "confidence": 0.8924,
          "quality_score": 0.8924,
          "user_id": "10025",
          "userId": "10025",
          "liveness_passed": true,
          "livenessPassed": true,
          "request_id": "5f1a238b...",
          "requestId": "5f1a238b...",
          "purpose": "Rental"
        }
        ```
    *   **Cơ chế hoạt động:** So sánh vector (embedding 512 chiều trích xuất từ InsightFace) của ảnh gửi lên với các mẫu đã đăng ký của `user_id` trong cơ sở dữ liệu file `face_db.pkl`. Nếu cosine similarity sau khi chuẩn hóa vượt qua ngưỡng `VERIFY_THRESHOLD` (mặc định `0.50`), hệ thống xác nhận khớp (`success: true`).

*   **1.4 Đăng nhập bằng khuôn mặt (Authenticate Face)**
    *   **Route:** `/api/face/authenticate`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `file` (File): Ảnh camera chụp.
        *   `user_id` hoặc `userId` (string, optional): Xác thực 1-1 nếu truyền ID, hoặc xác thực 1-N (quét tìm kiếm toàn bộ database) nếu bỏ trống ID.
    *   **Phản hồi (JSON):** Định dạng tương tự `/api/face/verify`.

*   **1.5 Kiểm tra cử chỉ liveness (Liveness Action Detection)**
    *   **Route:** `/api/face/action-check`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `file` (File): Khung hình ảnh webcam chụp khi thực hiện hành động.
        *   `action_code` hoặc `actionCode` (string): Hành động yêu cầu gồm: `turn_left`, `turn_right`, `look_up`, `look_down`, `mouth_open`, `smile`.
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "action_matched": true,
          "actionMatched": true,
          "action_code": "mouth_open",
          "actionCode": "mouth_open",
          "detected_action": "mouth_open",
          "detectedAction": "mouth_open",
          "liveness_passed": true,
          "livenessPassed": true,
          "request_id": "3c1aef56...",
          "requestId": "3c1aef56...",
          "metrics": {
            "yaw": -2.4,
            "pitch": 1.1,
            "roll": 0.5,
            "mouth_open_ratio": 0.082,
            "smile_ratio": 1.02
          }
        }
        ```
    *   **Thuật toán phát hiện:**
        Sử dụng MediaPipe Face Landmarker để trích xuất các điểm mốc 3D trên mặt người.
        *   `turn_left` / `turn_right`: Dựa trên góc xoay ngang (Yaw). Điều kiện vượt qua: `yaw > 14` độ (quay trái) hoặc `yaw < -14` độ (quay phải).
        *   `look_up` / `look_down`: Dựa trên góc gật đầu dọc (Pitch). Điều kiện: `pitch > 12` độ (ngẩng lên) hoặc `pitch < -12` độ (cúi xuống).
        *   `mouth_open`: Tính toán tỷ lệ khoảng cách giữa môi trên và môi dưới chia cho khoảng cách mép miệng. Điều kiện vượt qua: `mouth_open_ratio > 0.055`.
        *   `smile`: Tính tỷ lệ khoảng cách giữa hai mép miệng chia cho khoảng cách hai mắt. Điều kiện vượt qua: `smile_ratio > 1.18`.

*   **1.6 Trích xuất OCR thẻ CMND/CCCD & Đối khớp khuôn mặt chân dung**
    *   **Route:** `/api/face/ocr-cmnd` (Bí danh: `/api/face/qcr-cmnd`, `/api/face/cmnd-ocr`)
    *   **HTTP Method:** `POST`
    *   **Đầu vào (Multipart Form-Data):**
        *   `front_file` hoặc `frontFile` hoặc `front` (File): Ảnh mặt trước CCCD chip hoặc mã vạch.
        *   `back_file` hoặc `backFile` or `back` (File, optional): Ảnh mặt sau CCCD.
        *   `user_id` hoặc `userId` (string, optional): ID người dùng hiện tại để đối khớp ảnh thẻ với khuôn mặt đã đăng ký trên hệ thống.
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "fields": {
            "identity_number": "036098001234",
            "full_name": "NGUYỄN VĂN A",
            "date_of_birth": "1998-05-15",
            "gender": "Nam",
            "nationality": "Việt Nam",
            "address": "Phường Long Thành Trung, Thị xã Hòa Thành, Tây Ninh",
            "place_of_residence": "Phường Long Thành Trung, Thị xã Hòa Thành, Tây Ninh",
            "place_of_birth": "Thị xã Hòa Thành, Tây Ninh",
            "issue_date": "2023-10-20",
            "expiry_date": "2038-05-15",
            "issue_place": "Cục Cảnh sát QLHC về trật tự xã hội",
            "issuing_authority": "Cục Cảnh sát QLHC về trật tự xã hội",
            "mrz": "IDVNM0360980012348<<<<<<<<<<<<<<\n9805152M3805151VNM<<<<<<<<<<<5\nNGUYEN<<VAN<<A<<<<<<<<<<<<<<<<<"
          },
          "face_matched": true,
          "face_confidence": 0.8256,
          "request_id": "7d91e8aa..."
        }
        ```
    *   **Công nghệ xử lý:**
        1. Sử dụng PaddleOCR (ưu tiên cao nhất) hoặc Tesseract OCR để đọc văn bản tiếng Việt trên thẻ.
        2. Tự động cắt các vùng chứa thông tin trên thẻ (mã số, họ tên, ngày sinh, nơi thường trú, vùng mã đọc máy MRZ ở mặt sau).
        3. Phân tích vùng MRZ ở mặt sau để trích xuất nhanh số CCCD, ngày sinh, ngày hết hạn và họ tên không dấu để đối chiếu chéo thông tin.
        4. Tự động crop ảnh chân dung nhỏ in trên thẻ CCCD mặt trước bằng mô hình phát hiện khuôn mặt của InsightFace.
        5. So sánh vector đặc trưng khuôn mặt trên thẻ này với khuôn mặt của người dùng đang đăng nhập hệ thống để xác thực đây là giấy tờ chính chủ (`face_matched: true`).

---

#### 2. Dịch vụ Chatbox Tư vấn Bán hàng (`sales_chatbox/routes.py`)
Mô-đun chatbox bán hàng cung cấp widget nhúng trực tiếp vào giao diện và hỗ trợ trả lời tự động các thắc mắc về sách bằng thuật toán tìm kiếm ngữ nghĩa và lọc từ khóa.

*   **2.1 Trạng thái huấn luyện Chatbox (Health Check)**
    *   **Route:** `/api/chatbox/health`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (JSON):**
        ```json
        {
          "status": "ok",
          "chatbox": {
            "enabled": true,
            "knowledge_path": "d:\\DUANNGHIENCUU\\NHANDIENKHUONMAT-new07040226_fix\\sales_chatbox\\knowledge.json",
            "trained_at": "2026-06-25 15:30:12",
            "product_count": 142,
            "source": "database"
          }
        }
        ```

*   **2.2 Huấn luyện tri thức Chatbox (Train/Rebuild Knowledge Base)**
    *   **Route:** `/api/chatbox/train`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (JSON):**
        *   `connection_string` (string, optional): Chuỗi kết nối đến SQL Server. Nếu để trống sẽ sử dụng cấu hình mặc định trong file môi trường.
        *   `limit` (int, optional): Giới hạn số lượng sách tối đa đưa vào bộ nhớ (mặc định 1000).
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "message": "Đã huấn luyện chatbox từ database.",
          "product_count": 142,
          "trained_at": "2026-06-26 22:10:45",
          "elapsed_seconds": 0.452
        }
        ```
    *   **Cơ chế hoạt động:** Truy vấn trực tiếp từ bảng `Sanpham` trong cơ sở dữ liệu SQL Server để lấy các thông tin: tên sách, tác giả, giá tiền, số lượng tồn kho, mô tả, ảnh bìa, liên kết xem chi tiết sách. Sau đó chuyển đổi thành dạng chỉ mục không dấu hỗ trợ tìm kiếm nhanh (Knowledge Base).

*   **2.3 Đặt câu hỏi tư vấn bán hàng (Ask Chatbox)**
    *   **Route:** `/api/chatbox/ask`
    *   **HTTP Method:** `POST`
    *   **Đầu vào (JSON):**
        *   `message` hoặc `question` (string): Nội dung câu hỏi từ khách hàng (Ví dụ: "Sách Đắc Nhân Tâm giá bao nhiêu?" hoặc "Tìm sách lập trình").
    *   **Phản hồi (JSON):**
        ```json
        {
          "success": true,
          "request_id": "4b5d2345...",
          "answer": "Chào bạn, bên mình hiện có sách Đắc Nhân Tâm với giá 86.000 VND, hiện tại trong kho còn 12 cuốn.",
          "products": [
            {
              "id": 482,
              "name": "Đắc Nhân Tâm",
              "price": 86000,
              "final_price": 86000,
              "author": "Dale Carnegie",
              "category": "Sách kỹ năng",
              "image": "/assets/img/imgbook/dacnhantam.jpg",
              "url": "/chi-tiet/sach-482"
            }
          ],
          "trained_at": "2026-06-26 22:10:45",
          "elapsed_seconds": 0.015
        }
        ```

*   **2.4 Nhúng script giao diện (Get Widget Script)**
    *   **Route:** `/api/chatbox/widget.js`
    *   **HTTP Method:** `GET`
    *   **Phản hồi (MIME `application/javascript`):** Trả về file script Javascript được cấu hình sẵn base URL của API để client nhúng vào website chính. Script này sẽ tự động khởi tạo giao diện trò chuyện bong bóng (chat bubble) nổi ở góc dưới bên phải màn hình, có khả năng render các card sản phẩm trực quan khi chatbox gợi ý sách.
