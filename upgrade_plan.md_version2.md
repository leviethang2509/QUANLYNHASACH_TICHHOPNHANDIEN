# Kế hoạch nâng cấp QLNhaSach - Version 2

Tài liệu này tiếp nối `upgrade_plan.md`, tập trung vào các phần còn chưa hoàn thành và bổ sung yêu cầu mới:

- Vị trí nhà sách dùng để xác định vùng cho phép mượn sách là **Nhà sách Tân Hạnh, 75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam**.
- Khi mượn sách, người dùng nhập ngày yêu cầu, số ngày mượn, bấm xác nhận rồi mới hiện form xác nhận khuôn mặt.
- Khi xác nhận khuôn mặt thành công/thất bại phải hiển thị thông báo rõ ràng.
- Khi đăng nhập bỏ OCR hình ảnh và toàn bộ logic liên quan đến OCR.
- Bổ sung lựa chọn đăng nhập bằng khuôn mặt.
- Màn hình khách hàng cần có trang theo dõi sách đã mượn và trạng thái xử lý.
- Trước khi mượn phải kiểm tra sách còn tồn kho.
- Khi admin xác nhận mượn thì trừ tồn kho; khi trả sách thì cộng lại tồn kho.
- Chuẩn hóa yêu cầu đầu vào/đầu ra cho Flask API nhận diện khuôn mặt để tối ưu dự án API riêng.

## 1. Phạm vi tiếp tục thực hiện

Các việc đã nêu trong `upgrade_plan.md` vẫn giữ nguyên nếu chưa hoàn thành, nhưng thứ tự ưu tiên trong version 2 như sau:

1. Dọn luồng đăng nhập: bỏ OCR, tách rõ đăng nhập mật khẩu và đăng nhập khuôn mặt.
2. Cấu hình vị trí geofence theo Nhà sách Tân Hạnh.
3. Hoàn thiện form yêu cầu mượn sách: ngày yêu cầu, số ngày mượn.
4. Bổ sung popup xác nhận khuôn mặt sau khi người dùng xác nhận thông tin mượn.
5. Nối xác thực khuôn mặt vào `RentalController.RequestRental`.
6. Hoàn thiện logic tồn kho: kiểm tra trước khi tạo yêu cầu, trừ khi admin duyệt, cộng khi trả sách.
7. Thêm màn hình khách hàng theo dõi sách mượn.
8. Hoàn thiện `FaceAuthApiClient` và DTO trả về từ Flask API.
9. Hoàn thiện log cho các lần xác thực khuôn mặt trong đăng nhập và mượn sách.
10. Viết đặc tả Flask API nhận diện khuôn mặt làm đầu vào cho dự án tối ưu API riêng.

## 2. Bỏ OCR hình ảnh khỏi luồng đăng nhập

Mục tiêu: đăng nhập không còn xử lý OCR, không upload ảnh để đọc chữ, không còn service/controller/view/script nào phục vụ OCR trong authentication.

Việc cần làm:

- Tìm toàn bộ logic OCR bằng các từ khóa:
  - `OCR`
  - `Ocr`
  - `Tesseract`
  - `ReadText`
  - `ExtractText`
  - `ImageLogin`
  - `LoginByImage`
- Trong controller đăng nhập, xóa hoặc vô hiệu hóa các nhánh:
  - Nhận ảnh từ form đăng nhập để OCR.
  - Gọi service OCR.
  - So sánh text OCR với username/password/captcha.
  - Ghi session/temp data liên quan đến OCR.
- Trong view đăng nhập, bỏ:
  - Input upload ảnh cho OCR.
  - Button đăng nhập bằng OCR.
  - Script preview ảnh OCR.
  - Thông báo lỗi dành riêng cho OCR.
- Trong `Web.config`, bỏ appSettings OCR nếu không còn dùng:
  - `OcrApiUrl`
  - `OcrTimeoutSeconds`
  - `TesseractPath`
  - Các cấu hình tương tự nếu có.
- Nếu có package OCR không dùng nữa, chỉ gỡ sau khi kiểm tra không ảnh hưởng module khác.
- Nếu có bảng/log OCR trong database, không xóa ngay; đánh dấu deprecated và không ghi thêm dữ liệu mới.

Tiêu chí hoàn thành:

- Người dùng đăng nhập bằng mật khẩu bình thường không cần upload ảnh.
- Không còn action đăng nhập nào gọi OCR.
- Build không còn lỗi reference OCR.
- Nếu tìm `OCR`/`Tesseract` trong project, chỉ còn tài liệu cũ hoặc migration cũ đã ghi chú deprecated.

## 3. Thêm lựa chọn đăng nhập bằng khuôn mặt

Mục tiêu: màn hình đăng nhập có thêm một option rõ ràng: đăng nhập bằng tài khoản/mật khẩu hoặc đăng nhập bằng khuôn mặt.

File cần kiểm tra:

- `BaiTapLon\Views\Users\Login.cshtml`
- `BaiTapLon\Controllers\UsersController.cs`
- `BaiTapLon\Controllers\FaceAuthController.cs`
- `BaiTapLon\Scripts\FaceCapture.js`

Việc cần làm:

- Thêm vùng chọn phương thức đăng nhập:
  - `Đăng nhập bằng mật khẩu`
  - `Đăng nhập bằng khuôn mặt`
- Với đăng nhập mật khẩu:
  - Giữ form username/password hiện có.
  - Nếu tài khoản bật MFA khuôn mặt thì sau bước password chuyển sang `LoginMFA`.
- Với đăng nhập khuôn mặt:
  - Hiển thị webcam capture.
  - Giai đoạn đầu nên yêu cầu `username/email + khuôn mặt`.
  - Chỉ cho face-only login nếu Flask API đã hỗ trợ nhận diện 1:N ổn định, có liveness, rate limit và confidence threshold rõ ràng.
- Thêm endpoint AJAX:
  - `POST /FaceAuth/AuthenticateFaceLogin`
  - hoặc `POST /Users/LoginWithFace`
- Khi xác thực thành công:
  - Kiểm tra user tồn tại, còn hoạt động, không bị khóa.
  - Kiểm tra confidence >= `FaceAuthMinConfidence`.
  - Set auth cookie/session.
  - Ghi `FaceAuthLog` action `FaceLoginSuccess`.
- Khi thất bại:
  - Không set auth cookie.
  - Tăng bộ đếm rate limit.
  - Ghi `FaceAuthLog` action `FaceLoginFailed`.

Không được:

- Nhận `userId` từ client rồi đăng nhập thẳng.
- Cho phép `faceVerified = true` bỏ qua kiểm tra trạng thái tài khoản.
- Dùng logic `passwordOk || faceVerified` cho MFA. Với MFA phải là `passwordOk && faceVerified`.

DTO cần có:

```csharp
public class FaceAuthResponse
{
    public bool Success { get; set; }
    public string UserId { get; set; }
    public string ExternalUserId { get; set; }
    public double Confidence { get; set; }
    public bool LivenessPassed { get; set; }
    public string ErrorCode { get; set; }
    public string ErrorMessage { get; set; }
    public string RequestId { get; set; }
}
```

## 4. Cấu hình vị trí nhà sách dùng cho geofence

Mục tiêu: chỉ cho phép mượn sách khi người dùng ở gần Nhà sách Tân Hạnh.

Vị trí nghiệp vụ:

- Tên: `Nhà sách Tân Hạnh`
- Địa chỉ: `75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam`
- Mục đích: dùng làm vị trí cửa hàng để kiểm tra geofence trước khi cho mượn sách.

Việc cần làm:

- Thay toàn bộ tọa độ mẫu/hard-code hiện tại bằng dữ liệu cửa hàng thật.
- Bảng `StoreLocations` cần có ít nhất:
  - `ID`
  - `StoreName`
  - `Address`
  - `Latitude`
  - `Longitude`
  - `GeofenceRadius`
  - `IsActive`
- Thêm seed/migration cho Nhà sách Tân Hạnh.
- Vì địa chỉ có thể cần geocode, phải xác định tọa độ chính xác trước khi seed production.
- Nếu chưa có tọa độ chính xác, dùng placeholder rõ ràng và ghi chú bắt buộc cập nhật trước nghiệm thu.
- `GeofenceController.CheckGeofence` phải:
  - Lấy cửa hàng active từ database.
  - Tính khoảng cách từ vị trí người dùng đến Nhà sách Tân Hạnh.
  - Trả `inZone = true` khi khoảng cách <= `GeofenceRadius`.
  - Ghi log `GeofenceLog` gồm user, store, lat/lon người dùng, khoảng cách, bán kính.

Script SQL đề xuất:

```sql
IF NOT EXISTS (SELECT 1 FROM StoreLocations WHERE StoreName = N'Nhà sách Tân Hạnh')
BEGIN
    INSERT INTO StoreLocations
        (StoreName, Address, Latitude, Longitude, GeofenceRadius, IsActive)
    VALUES
        (N'Nhà sách Tân Hạnh',
         N'75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam',
         NULL,
         NULL,
         0.5,
         1)
END
```

Ghi chú: `Latitude` và `Longitude` phải được cập nhật bằng tọa độ thật trước khi bật kiểm tra vị trí chính thức.

## 5. Form yêu cầu mượn sách trước khi xác nhận khuôn mặt

Mục tiêu: khi người dùng thao tác mượn sách, hệ thống hiện form nhập thông tin mượn trước, sau đó mới xác nhận khuôn mặt.

File cần kiểm tra:

- `BaiTapLon\Views\Product\Detail.cshtml`
- `BaiTapLon\Views\Product\ListProduct.cshtml`
- `BaiTapLon\Views\Product\Search.cshtml`
- `BaiTapLon\Scripts\RentalFaceConfirm.js`
- `BaiTapLon\Controllers\RentalController.cs`

Luồng UI bắt buộc:

1. Người dùng bấm `Mượn sách`.
2. Hệ thống kiểm tra người dùng đã đăng nhập.
3. Hệ thống kiểm tra vị trí geofence hợp lệ.
4. Hệ thống kiểm tra sách còn tồn kho.
5. Hiện form yêu cầu mượn:
   - `Ngày yêu cầu`: mặc định là ngày hiện tại, chỉ đọc hoặc không cho chọn ngày quá khứ.
   - `Số ngày mượn`: input số, ví dụ từ 1 đến 30 ngày.
   - Nút `Xác nhận`.
   - Nút `Hủy`.
6. Người dùng bấm `Xác nhận`.
7. Hệ thống hiện form/popup xác nhận khuôn mặt.
8. Xác thực khuôn mặt thành công thì gửi yêu cầu mượn.
9. Xác thực thất bại thì không tạo yêu cầu mượn và thông báo thất bại.

Validation form:

- `RequestDate` mặc định là ngày hiện tại theo giờ server.
- Không tin ngày gửi từ client nếu client tự sửa; server phải set hoặc validate lại.
- `BorrowDays` bắt buộc, là số nguyên dương.
- Giới hạn `BorrowDays`, đề xuất 1-30 ngày hoặc theo cấu hình `RentalMaxBorrowDays`.
- `ExpectedReturnDate = RequestDate + BorrowDays`.

Thông báo UI:

- Thành công: `Yêu cầu mượn sách đã được gửi. Vui lòng chờ admin xác nhận.`
- Thất bại do khuôn mặt: `Xác nhận khuôn mặt thất bại. Vui lòng thử lại.`
- Thất bại do tồn kho: `Sách hiện đã hết hàng, không thể gửi yêu cầu mượn.`
- Thất bại do vị trí: `Chỉ hỗ trợ mượn sách tại Nhà sách Tân Hạnh.`

## 6. Popup xác nhận khuôn mặt khi mượn sách

Mục tiêu: trước khi gửi yêu cầu mượn sách, hệ thống bắt buộc người dùng xác nhận khuôn mặt trong popup. Chỉ khi xác thực thành công mới gọi nghiệp vụ tạo yêu cầu mượn.

Popup cần có các trạng thái:

- Đang mở camera.
- Không có quyền camera.
- Đang xác thực.
- Xác thực thành công.
- Xác thực thất bại.
- Hết lượt thử tạm thời.

Script đề xuất:

```javascript
async function submitRentalRequest(productId, requestDate, borrowDays) {
    const stockResult = await checkStock(productId);
    if (!stockResult.available) {
        showRentalError('Sách hiện đã hết hàng, không thể gửi yêu cầu mượn.');
        return;
    }

    const faceResult = await openRentalFaceConfirm(productId);
    if (!faceResult.success) {
        showRentalError('Xác nhận khuôn mặt thất bại. Vui lòng thử lại.');
        return;
    }

    const rentalResult = await requestRental({
        productId: productId,
        requestDate: requestDate,
        borrowDays: borrowDays,
        faceToken: faceResult.faceToken
    });

    if (rentalResult.success) {
        showRentalSuccess('Yêu cầu mượn sách đã được gửi. Vui lòng chờ admin xác nhận.');
    } else {
        showRentalError(rentalResult.message);
    }
}
```

Lưu ý:

- `faceToken` phải là token ngắn hạn do server cấp sau khi xác thực khuôn mặt thành công.
- Không chỉ dựa vào biến JS `faceVerified = true`, vì client có thể sửa.
- Token nên hết hạn sau 1-3 phút và chỉ dùng cho đúng user/product/purpose.

Endpoint xác thực khuôn mặt:

- `POST /FaceAuth/VerifyRentalFace`

Input:

- Ảnh khuôn mặt từ webcam.
- `productId`.
- Anti-forgery token nếu gọi từ MVC form/AJAX.

Server xử lý:

1. Lấy user hiện tại từ session/auth, không nhận `userId` từ client.
2. Validate file ảnh.
3. Gọi Flask API verify face theo user hiện tại.
4. Nếu thành công và confidence đạt ngưỡng:
   - Tạo `faceRentalToken`.
   - Token chứa: `UserID`, `ProductID`, `Purpose = Rental`, `ExpiresAtUtc`, `RequestId`.
   - Ghi `FaceAuthLog` action `RentalFaceVerifySuccess`.
   - Trả JSON `{ success: true, faceToken: "..." }`.
5. Nếu thất bại:
   - Ghi `FaceAuthLog` action `RentalFaceVerifyFailed`.
   - Trả JSON `{ success: false, message: "Xác nhận khuôn mặt thất bại. Vui lòng thử lại." }`.

## 7. Rental workflow và tồn kho

Mục tiêu: nghiệp vụ mượn/trả sách phải kiểm soát tồn kho đúng thời điểm.

Trạng thái đề xuất:

- `Pending`: người dùng đã gửi yêu cầu, chờ admin xác nhận.
- `Approved`: admin đã xác nhận cho mượn, tồn kho đã bị trừ.
- `Rejected`: admin từ chối yêu cầu.
- `Borrowing`: người dùng đang mượn sách, có thể gộp với `Approved` nếu hệ thống không tách bước nhận sách.
- `Returned`: người dùng đã trả sách, tồn kho đã được cộng lại.
- `Cancelled`: người dùng hoặc admin hủy trước khi duyệt.
- `Overdue`: quá hạn trả.

### 7.1 RequestRental

Khi tạo yêu cầu mượn:

- Kiểm tra user đã đăng nhập.
- Kiểm tra geofence hợp lệ tại Nhà sách Tân Hạnh.
- Kiểm tra sách còn tồn kho.
- Kiểm tra `faceRentalToken` hợp lệ.
- Validate `BorrowDays`.
- Tạo yêu cầu trạng thái `Pending`.
- Ghi `RentalLog` action `Request`.
- Chưa trừ tồn kho ở bước này, vì admin chưa xác nhận.

DTO/input đề xuất:

```csharp
public class RentalRequestInput
{
    public int ProductId { get; set; }
    public DateTime RequestDate { get; set; }
    public int BorrowDays { get; set; }
    public string FaceToken { get; set; }
}
```

Server phải tự tính:

```csharp
ExpectedReturnDate = RequestDate.Date.AddDays(BorrowDays);
```

### 7.2 Admin xác nhận mượn

Khi admin approve:

- Chỉ admin được gọi action.
- Kiểm tra yêu cầu đang ở trạng thái `Pending`.
- Kiểm tra lại tồn kho ngay tại thời điểm duyệt.
- Nếu tồn kho > 0:
  - Trừ tồn kho 1 cuốn hoặc theo số lượng yêu cầu.
  - Cập nhật trạng thái `Approved` hoặc `Borrowing`.
  - Ghi `RentalLog` action `Approve`.
- Nếu tồn kho không còn:
  - Không duyệt.
  - Trả lỗi: `Sách đã hết tồn kho, không thể xác nhận mượn.`
  - Có thể chuyển trạng thái `Rejected` với lý do hết tồn kho hoặc giữ `Pending` để admin xử lý.

Yêu cầu kỹ thuật:

- Thao tác trừ tồn kho và cập nhật trạng thái phải nằm trong cùng transaction.
- Cần chống duyệt trùng bằng kiểm tra trạng thái trong transaction.
- Không trừ tồn kho nếu yêu cầu đã `Approved`, `Borrowing`, `Returned`, `Rejected`, `Cancelled`.

### 7.3 Trả sách

Khi admin xác nhận trả sách:

- Chỉ admin được gọi action.
- Chỉ cho trả nếu trạng thái hiện tại là `Approved` hoặc `Borrowing`.
- Cộng tồn kho đúng số lượng đã mượn.
- Cập nhật trạng thái `Returned`.
- Lưu `ActualReturnDate`.
- Ghi `RentalLog` action `Return`.
- Thao tác cộng tồn kho và cập nhật trạng thái phải nằm trong cùng transaction.

### 7.4 Hủy hoặc từ chối

- Nếu yêu cầu đang `Pending`, admin có thể `Reject`, user có thể `Cancel` nếu nghiệp vụ cho phép.
- Không thay đổi tồn kho khi `Reject` hoặc `Cancel` vì tồn kho chưa bị trừ.
- Nếu đã `Approved/Borrowing`, không dùng `Cancel`; phải dùng luồng `Return` hoặc điều chỉnh riêng có log rõ ràng.

## 8. Màn hình khách hàng theo dõi sách mượn

Mục tiêu: khách hàng có màn hình riêng để xem các sách đã yêu cầu mượn và trạng thái hiện tại.

File/action cần tạo hoặc cập nhật:

- `BaiTapLon\Controllers\RentalController.cs`
- `BaiTapLon\Views\Rental\MyRentals.cshtml`
- Menu khách hàng/layout hiện tại.

Route đề xuất:

- `GET /Rental/MyRentals`
- Tên menu: `Sách đang mượn` hoặc `Theo dõi mượn sách`.

Dữ liệu hiển thị:

- Tên sách.
- Ảnh sách nếu có.
- Ngày yêu cầu.
- Số ngày mượn.
- Ngày dự kiến trả.
- Ngày trả thực tế nếu có.
- Trạng thái:
  - `Chờ xác nhận`
  - `Đã xác nhận`
  - `Đang mượn`
  - `Đã trả`
  - `Từ chối`
  - `Đã hủy`
  - `Quá hạn`
- Ghi chú/lý do từ chối nếu có.

Yêu cầu bảo mật:

- Người dùng chỉ xem rental của chính mình.
- Không nhận `userId` từ query string để lọc dữ liệu.
- Lấy user hiện tại từ auth/session.

Tính năng nên có:

- Filter theo trạng thái.
- Phân trang.
- Nút hủy yêu cầu nếu trạng thái còn `Pending` và nghiệp vụ cho phép.
- Cảnh báo quá hạn nếu `ExpectedReturnDate < today` và chưa trả.

## 9. Hoàn thiện service gọi Flask API

File nên tạo:

- `BaiTapLon\Services\FaceAuthApiClient.cs`
- `BaiTapLon\Services\IFaceAuthApiClient.cs`
- `BaiTapLon\Models\FaceAuth\*.cs` hoặc thư mục DTO tương ứng.

Yêu cầu:

- Không gọi HTTP trực tiếp rải rác trong controller.
- Có timeout từ `FaceAuthTimeoutSeconds`.
- Có base URL từ `FaceAuthAPI`.
- Có DTO rõ ràng, không dùng `dynamic`.
- Log được `RequestId`, `ErrorCode`, `Confidence`.
- Phân biệt các mục đích gọi:
  - `Register`
  - `Login`
  - `MFA`
  - `Rental`

Các method đề xuất:

```csharp
Task<FaceAuthResponse> RegisterFaceAsync(int userId, Stream image, string fileName);
Task<FaceAuthResponse> VerifyFaceAsync(int userId, Stream image, string fileName, string purpose);
Task<FaceAuthResponse> IdentifyFaceAsync(Stream image, string fileName);
```

## 10. Cập nhật cấu hình

File:

- `BaiTapLon\Web.config`

AppSettings cần có:

```xml
<add key="FaceAuthAPI" value="http://localhost:8000/api/face" />
<add key="FaceAuthTimeoutSeconds" value="15" />
<add key="FaceAuthMinConfidence" value="0.75" />
<add key="FaceAuthRentalTokenMinutes" value="3" />
<add key="FaceAuthLoginMode" value="UsernameAndFace" />
<add key="FaceAuthMaxAttempts" value="5" />
<add key="FaceAuthLockoutMinutes" value="10" />
<add key="RentalMaxBorrowDays" value="30" />
<add key="GeofenceDefaultRadiusKm" value="0.5" />
```

Giải thích:

- `FaceAuthLoginMode = UsernameAndFace`: yêu cầu username/email + khuôn mặt.
- `RentalMaxBorrowDays`: số ngày mượn tối đa.
- `GeofenceDefaultRadiusKm`: bán kính mặc định quanh Nhà sách Tân Hạnh nếu database chưa cấu hình.

## 11. Database và log cần bổ sung

### 11.1 Rental

Nếu chưa có bảng rental riêng, tạo entity/bảng `Rentals`:

- `ID`
- `UserID`
- `ProductID`
- `Quantity`
- `RequestDate`
- `BorrowDays`
- `ExpectedReturnDate`
- `ActualReturnDate`
- `Status`
- `RejectReason`
- `ApprovedByUserID`
- `ApprovedAtUtc`
- `CreatedAtUtc`
- `UpdatedAtUtc`

### 11.2 FaceAuthLogs

Nếu có thể migration, bổ sung cột cho `FaceAuthLogs`:

- `Purpose`: `Register`, `Login`, `MFA`, `Rental`.
- `Confidence`.
- `LivenessPassed`.
- `RequestId`.
- `ErrorCode`.
- `ErrorMessage`.
- `CreatedAtUtc`.

### 11.3 RentalLogs

`RentalLog` nên ghi:

- `RentalID`
- `ActorUserID`
- `TargetUserID`
- `ProductID`
- `Action`: `Request`, `Approve`, `Reject`, `Cancel`, `Return`, `Overdue`.
- `OldStatus`
- `NewStatus`
- `Details`
- `CreatedAtUtc`

## 12. Test cần bổ sung

### Face auth

- Login bằng mật khẩu thành công không gọi OCR.
- Login bằng khuôn mặt thành công khi API trả `success = true`, confidence đủ ngưỡng.
- Login bằng khuôn mặt thất bại khi confidence thấp.
- MFA yêu cầu password đúng và face đúng.
- Không nhận `userId` tùy ý từ client trong các action nhạy cảm.

### Geofence

- Vị trí cửa hàng là Nhà sách Tân Hạnh.
- Ngoài bán kính geofence thì không mở form mượn.
- Trong bán kính geofence thì được mở form mượn nếu còn tồn kho.
- Không có tọa độ cửa hàng thì trả lỗi cấu hình rõ ràng.

### Rental

- Bấm mượn sách nhưng hết tồn kho thì không hiện bước xác nhận khuôn mặt.
- Form mượn mặc định ngày yêu cầu là ngày hiện tại.
- Số ngày mượn <= 0 bị từ chối.
- Số ngày mượn vượt `RentalMaxBorrowDays` bị từ chối.
- Bấm xác nhận form mượn thì hiện popup xác nhận khuôn mặt.
- Xác thực khuôn mặt thất bại không tạo rental.
- Xác thực khuôn mặt thành công, geofence hợp lệ, còn tồn kho thì tạo rental `Pending`.
- Tạo rental `Pending` chưa trừ tồn kho.
- Admin approve thì trừ tồn kho trong transaction.
- Admin approve khi hết tồn kho thì bị từ chối.
- Admin return thì cộng tồn kho trong transaction.
- User chỉ xem được rental của chính mình ở màn hình `MyRentals`.

### OCR removal

- Build project sau khi bỏ OCR.
- Không còn route/action OCR đăng nhập được gọi.
- UI login không còn input upload ảnh OCR.

## 13. Tiêu chí nghiệm thu version 2

- Màn hình đăng nhập có 2 lựa chọn rõ ràng: mật khẩu và khuôn mặt.
- Đăng nhập không còn OCR hình ảnh.
- Đăng nhập bằng khuôn mặt gọi Flask API và chỉ đăng nhập khi kết quả hợp lệ.
- Geofence dùng Nhà sách Tân Hạnh, 75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam.
- Người dùng bấm mượn sách sẽ thấy form ngày yêu cầu và số ngày mượn.
- Sau khi bấm xác nhận mới hiện popup xác nhận khuôn mặt.
- Xác thực khuôn mặt thành công thì gửi yêu cầu mượn và thông báo thành công.
- Xác thực khuôn mặt thất bại thì không tạo yêu cầu và thông báo thất bại.
- Trước khi mượn có kiểm tra tồn kho.
- Yêu cầu mượn mới ở trạng thái `Pending` và chưa trừ tồn kho.
- Khi admin xác nhận mượn, hệ thống trừ tồn kho.
- Khi trả sách, hệ thống cộng lại tồn kho.
- Khách hàng có màn hình theo dõi sách mượn và trạng thái.
- `RequestRental` kiểm tra token xác thực khuôn mặt ở phía server.
- Log phân biệt được xác thực khuôn mặt cho login, MFA và rental.
- Build solution thành công.
- Có test hoặc checklist thủ công cho các luồng chính.

## 14. Yêu cầu đầu vào/đầu ra cho Flask API nhận diện khuôn mặt

Phần này là đầu vào cần thiết để bắt đầu tối ưu dự án Flask API riêng.

### 14.1 Nguyên tắc chung

Flask API phải hỗ trợ tối thiểu 3 nhóm chức năng:

1. Đăng ký khuôn mặt cho user.
2. Xác thực khuôn mặt 1:1 cho user đã biết.
3. Nhận diện khuôn mặt 1:N nếu muốn đăng nhập chỉ bằng khuôn mặt.

Tất cả response nên có:

- `success`
- `request_id`
- `error_code`
- `message`
- `confidence`
- `liveness_passed`

### 14.2 API đăng ký khuôn mặt

Endpoint:

```http
POST /api/face/register
Content-Type: multipart/form-data
```

Input:

- `user_id`: string hoặc int, bắt buộc.
- `image`: file `.jpg`, `.jpeg`, `.png`, bắt buộc.
- `source`: ví dụ `webcam`, tùy chọn.
- `request_id`: tùy chọn, nếu client không gửi thì API tự tạo.

Output thành công:

```json
{
  "success": true,
  "request_id": "uuid",
  "user_id": "123",
  "face_id": "face-profile-id",
  "embedding_version": "model-name-or-version",
  "quality_score": 0.91,
  "liveness_passed": true,
  "message": "Face registered successfully"
}
```

Output thất bại:

```json
{
  "success": false,
  "request_id": "uuid",
  "error_code": "NO_FACE_DETECTED",
  "message": "No valid face detected",
  "quality_score": 0.0,
  "liveness_passed": false
}
```

### 14.3 API xác thực khuôn mặt 1:1

Endpoint:

```http
POST /api/face/verify
Content-Type: multipart/form-data
```

Input:

- `user_id`: user cần xác thực, bắt buộc.
- `image`: ảnh webcam, bắt buộc.
- `purpose`: `Login`, `MFA`, `Rental`, bắt buộc.
- `request_id`: tùy chọn.

Output thành công:

```json
{
  "success": true,
  "request_id": "uuid",
  "user_id": "123",
  "matched": true,
  "confidence": 0.88,
  "threshold": 0.75,
  "liveness_passed": true,
  "purpose": "Rental",
  "message": "Face verified"
}
```

Output thất bại:

```json
{
  "success": false,
  "request_id": "uuid",
  "user_id": "123",
  "matched": false,
  "confidence": 0.42,
  "threshold": 0.75,
  "liveness_passed": true,
  "purpose": "Rental",
  "error_code": "FACE_NOT_MATCH",
  "message": "Face does not match this user"
}
```

### 14.4 API nhận diện khuôn mặt 1:N

Chỉ dùng cho đăng nhập bằng khuôn mặt không cần username khi API đã đủ ổn định.

Endpoint:

```http
POST /api/face/identify
Content-Type: multipart/form-data
```

Input:

- `image`: ảnh webcam, bắt buộc.
- `request_id`: tùy chọn.

Output:

```json
{
  "success": true,
  "request_id": "uuid",
  "matched": true,
  "user_id": "123",
  "confidence": 0.9,
  "threshold": 0.82,
  "liveness_passed": true,
  "candidates": [
    {
      "user_id": "123",
      "confidence": 0.9
    }
  ],
  "message": "Face identified"
}
```

### 14.5 Mã lỗi Flask API nên chuẩn hóa

- `NO_FACE_DETECTED`
- `MULTIPLE_FACES_DETECTED`
- `LOW_IMAGE_QUALITY`
- `LIVENESS_FAILED`
- `USER_NOT_FOUND`
- `FACE_PROFILE_NOT_FOUND`
- `FACE_NOT_MATCH`
- `CONFIDENCE_TOO_LOW`
- `UNSUPPORTED_IMAGE_TYPE`
- `IMAGE_TOO_LARGE`
- `MODEL_NOT_READY`
- `INTERNAL_ERROR`

### 14.6 Yêu cầu phi chức năng cho Flask API

- Timeout mục tiêu dưới 3 giây cho verify/login thông thường.
- Giới hạn dung lượng ảnh, đề xuất tối đa 5 MB.
- Không lưu ảnh xác thực thất bại lâu hơn cần thiết.
- Có request id để web MVC và Flask API đối chiếu log.
- Có version model trong response để truy vết khi thay đổi model.
- Có liveness detection hoặc ít nhất chừa trường `liveness_passed`.
- Có endpoint health check:

```http
GET /api/face/health
```

Response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "model-name-or-version",
  "time_utc": "2026-05-08T00:00:00Z"
}
```

## 15. Thứ tự triển khai khuyến nghị

1. Bỏ OCR khỏi login và build lại.
2. Cấu hình seed Nhà sách Tân Hạnh và xác định tọa độ thật.
3. Tạo `FaceAuthApiClient` dùng DTO rõ ràng.
4. Thêm option đăng nhập bằng khuôn mặt ở UI.
5. Hoàn thiện endpoint đăng nhập bằng khuôn mặt.
6. Tạo form yêu cầu mượn sách gồm ngày yêu cầu và số ngày mượn.
7. Tạo popup xác nhận khuôn mặt sau bước xác nhận form mượn.
8. Tạo token xác thực khuôn mặt ngắn hạn cho rental.
9. Sửa `RentalController.RequestRental` bắt buộc kiểm tra tồn kho, geofence và face token.
10. Sửa admin approve để trừ tồn kho trong transaction.
11. Sửa trả sách để cộng tồn kho trong transaction.
12. Thêm màn hình khách hàng `MyRentals`.
13. Bổ sung log và test.
14. Dùng mục 14 làm yêu cầu đầu vào cho dự án Flask API nhận diện khuôn mặt.
## 16. Cap nhat luong form dang nhap

- Form dang nhap tai khoan/mat khau khong hien form xac nhan khuon mat va khong khoi dong camera.
- Chi khi nguoi dung bam `Dang nhap bang khuon mat` moi hien popup giua man hinh de nhan dien khuon mat va dang nhap.
- Popup dang nhap khuon mat phai co nut dong, bam nen mo/nen dong deu phai dung camera va tra trang ve binh thuong.
- Popup xac nhan khuon mat khong co o nhap tai khoan rieng; he thong lay tai khoan tu o `Tai khoan` cua form dang nhap chinh.
- Neu chua nhap tai khoan ma bam dang nhap bang khuon mat, UI bao nguoi dung nhap tai khoan truoc.
- Dang nhap bang tai khoan/mat khau tiep tuc goi luong `Users/Login` nhu cu, khong bi bat xac nhan khuon mat.

## 17. Cap nhat log va bao ve dang nhap khuon mat

- `FaceAuthResponse` map them `RequestId`, `ErrorCode`, `ErrorMessage`, `LivenessPassed`, `Purpose`, `ExternalUserId` tu response Flask API.
- `FaceAuthApiClient` gui them `user_id` va `purpose` de tuong thich voi API version2, dong thoi van giu `userId` cho API cu.
- `FaceAuthLogs` bo sung `Purpose`, `ErrorCode`, `LivenessPassed` de admin truy vet ro login/MFA/rental/register.
- Admin FaceAuth log hien them `Purpose`, `Liveness`, `RequestId`, `ErrorCode`.
- Dang nhap bang khuon mat su dung `FaceAuthMaxAttempts` va `FaceAuthLockoutMinutes` de khoa tam thoi theo IP + tai khoan khi that bai lien tiep.

## 18. Cap nhat CSS popup va sua loi font cac view moi

- Tao CSS dung chung cho popup xac thuc khuon mat tai `assets/css/face-auth-modal.css`.
- Popup xac thuc khuon mat phai can giua man hinh, co nen mo, hop thoai gon, video ti le on dinh va khong lam lech layout trang.
- Dang nhap bang khuon mat tren desktop/mobile dung popup giua man hinh, chi co chuc nang nhan dien va dang nhap, co nut `Dong`.
- Xac thuc khuon mat khi muon sach dung popup giua man hinh tuong tu, co nut `Dong`, dong popup thi dung camera.
- Cac view moi phai dung tieng Viet co dau dung encoding, khong de chu bi mojibake nhu `QuÃ¡`, `Äang`, `Lá»c`.
- Viet hoa cac view admin/log moi them: rental admin, face auth logs, geofence logs, rental logs.

## 19. Cap nhat quan ly muon tra sach cho khach hang va log admin

- Khach hang co man hinh `Rental/MyRentals` de quan ly thong tin sach muon:
  - Sach, anh sach, ma yeu cau.
  - Ngay yeu cau, so ngay muon, ngay du kien tra, ngay tra thuc te.
  - Trang thai: cho duyet, dang muon, tra tre, da tra, tu choi, da huy.
  - Tong hop so luong theo trang thai va filter theo trang thai.
  - Cho phep huy yeu cau khi con `Pending`.
- Menu khach hang `Sach dang muon` hien badge so luong yeu cau dang hoat dong:
  - Tinh cac yeu cau chua `Returned`, `Rejected`, `Cancelled`.
  - Khi tao yeu cau muon thanh cong, response `/Rental/RequestRental` tra them `activeRentalCount`.
  - Trang chi tiet sach cap nhat span badge bang `activeRentalCount` ma khong can reload.
- Geofence muon sach cap nhat ban kinh nghiep vu duoi 5km:
  - `GeofenceDefaultRadiusKm = 5`.
  - Seed `StoreLocations` cua `Nha sach Tan Hanh` dat `GeofenceRadius = 5`.
  - `GeofenceController` fallback ve 5km neu DB chua cau hinh ban kinh.
- Man hinh quan ly admin can kiem tra duoc log:
  - `LogsAdmin/FaceAuth` hien Purpose, Liveness, RequestId, ErrorCode, ErrorMessage, co empty state va xoa loc.
  - `LogsAdmin/Rental` hien log tao yeu cau, duyet muon, tu choi, huy, tra sach, qua han, co empty state va xoa loc.
  - `LogRepository` tiep tuc dung `DefaultConnection`, cung database `QLNhaSach`.
- Can xac minh thu cong:
  - Tao yeu cau muon thanh cong thi badge `Sach dang muon` tang.
  - Ngoai ban kinh 5km thi khong duoc mo luong muon sach.
  - Trong ban kinh 5km, con ton kho, face token hop le thi tao rental `Pending`.
  - Admin duyet/tra sach thi `RentalLogs` co ban ghi tuong ung.
  - Xac thuc khuon mat login/MFA/rental thi `FaceAuthLogs` co ban ghi tuong ung.
