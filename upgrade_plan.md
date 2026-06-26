# Kế hoạch nâng cấp hệ thống QLNhaSach

Tài liệu này mô tả cụ thể các việc cần làm theo đúng cấu trúc dự án hiện tại, để khi đọc kế hoạch có thể triển khai lần lượt từng file. Dự án hiện là ASP.NET MVC 5, Entity Framework 6, solution `DongTrieuBookStore.sln`; web chính nằm trong `BaiTapLon`, entity/context nằm trong `Mood`, repository dùng chung nằm trong `Common`, script SQL nằm trong `sql`, test nằm trong `Tests`.

## 1. Mục tiêu nâng cấp

- Hoàn thiện xác thực khuôn mặt trong luồng đăng ký, đăng nhập và MFA.
- Hoàn thiện geofence để chỉ cho mượn sách khi người dùng ở gần cửa hàng.
- Hoàn thiện nghiệp vụ mượn/trả sách thay vì chỉ ghi log mẫu.
- Chuẩn hóa hệ thống audit log: face auth, geofence, rental.
- Bổ sung màn hình admin/API để tra cứu log và theo dõi mượn sách.
- Làm rõ cấu hình, migration, test và tiêu chí nghiệm thu để triển khai an toàn.

## 2. Hiện trạng đáng chú ý

- `BaiTapLon\Controllers\FaceAuthController.cs` đã có 3 action `RegisterFace`, `VerifyFace`, `AuthenticateFace`, có lưu ảnh vào `DataImage/FaceSamples/` và gọi API Python qua `FaceAuthAPI`.
- `BaiTapLon\Controllers\GeofenceController.cs` đã có `CheckGeofence` nhưng đang hard-code `storeId = 1`, tọa độ `10.0, 106.0`, bán kính `0.5 km`.
- `BaiTapLon\Controllers\RentalController.cs` mới là khung ghi `RentalLog`, chưa thấy xử lý nghiệp vụ mượn/trả thật.
- `Mood\EF2\FaceAuthLog.cs`, `GeofenceLog.cs`, `RentalLog.cs`, `StoreLocation.cs`, `LogDbContext.cs` đã tồn tại.
- `Common\Repositories\LogRepository.cs` mới có hàm thêm log, chưa có truy vấn/phân trang/lọc.
- `BaiTapLon\Controllers\Api\LogsController.cs` đã có API đọc log nhưng còn thiếu lọc ngày, tổng bản ghi, validate page/pageSize và dispose context.
- `Mood\EF2\QuanLySachDBContext.cs` chưa khai báo `DbSet<StoreLocation>` và các log table trong context chính; hiện log dùng `LogDbContext` với connection `DefaultConnection`.
- `Tests\FaceAuthControllerTests.cs` hiện có test rất nhỏ và có nguy cơ lỗi do controller chưa được mock `Request`.

## 3. Thứ tự triển khai đề xuất

1. Chuẩn hóa database và EF model.
2. Hoàn thiện lớp repository/service dùng chung.
3. Hoàn thiện FaceAuth controller và view.
4. Hoàn thiện Geofence controller và UI sản phẩm.
5. Hoàn thiện Rental workflow và admin dashboard.
6. Hoàn thiện Logs API/admin views.
7. Bổ sung test, script chạy migration, kiểm thử tích hợp.

## 4. Thay đổi chi tiết theo file

### `BaiTapLon\Web.config`

Mục tiêu: đưa toàn bộ endpoint, timeout và ngưỡng kiểm tra ra cấu hình.

Việc cần làm:
- Thêm hoặc kiểm tra `appSettings`:
  - `FaceAuthAPI`: base URL API Python, ví dụ `http://localhost:8000/api/face`.
  - `FaceAuthTimeoutSeconds`: thời gian chờ khi gọi API, đề xuất `15`.
  - `FaceAuthMinConfidence`: ngưỡng nhận diện, đề xuất `0.75`.
  - `GeofenceDefaultRadiusKm`: bán kính mặc định nếu cửa hàng chưa cấu hình.
  - `FaceSampleStoragePath`: mặc định `DataImage/FaceSamples`.
- Kiểm tra connection string:
  - `QuanLySachDBContext` dùng cho dữ liệu nghiệp vụ.
  - `DefaultConnection` đang được `LogDbContext` dùng cho log. Nếu hai connection thực chất cùng database, ghi rõ trong README; nếu không, cần migration riêng cho database log.

### `Mood\EF2\QuanLySachDBContext.cs`

Mục tiêu: context chính biết các bảng mới cần dùng trong nghiệp vụ.

Việc cần làm:
- Thêm:
  - `public virtual DbSet<StoreLocation> StoreLocations { get; set; }`
  - Cân nhắc thêm `DbSet<FaceAuthLog>`, `DbSet<GeofenceLog>`, `DbSet<RentalLog>` nếu quyết định dùng chung context thay cho `LogDbContext`.
- Trong `OnModelCreating`, cấu hình các chuỗi không cần unicode nếu cần tương thích database cũ:
  - `StoreLocation.StoreName`
  - `FaceAuthLog.Action`, `IP`, `DeviceInfo`, `ImagePath`
  - `RentalLog.Action`, `Details`
- Quyết định một hướng rõ ràng:
  - Hướng A: giữ `LogDbContext` riêng, mọi log đi qua `DefaultConnection`.
  - Hướng B: gộp log vào `QuanLySachDBContext`, sửa `LogRepository` và `LogsController` dùng context chính.

### `Mood\EF2\LogDbContext.cs`

Mục tiêu: ổn định context log và tránh nhầm connection.

Việc cần làm:
- Nếu giữ context riêng, bổ sung `OnModelCreating` để map table name rõ ràng: `FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`.
- Kiểm tra connection `DefaultConnection` có tồn tại trong `BaiTapLon\Web.config`.
- Thêm constructor nhận connection string hoặc dependency injection nếu cần test dễ hơn.

### `Mood\EF2\FaceAuthLog.cs`

Mục tiêu: log đủ thông tin nhưng không lộ dữ liệu nhạy cảm quá mức.

Việc cần làm:
- Thêm annotation/validation:
  - `Action` giới hạn độ dài khoảng 50.
  - `IP` giới hạn 45 để hỗ trợ IPv6.
  - `DeviceInfo` giới hạn 500.
  - `ImagePath` giới hạn 500.
- Cân nhắc thêm:
  - `ErrorMessage` để lưu lỗi API Python.
  - `RequestId` để truy vết một lần đăng nhập.
  - `CreatedAtUtc` thay cho `Timestamp` hoặc thống nhất `Timestamp` luôn là UTC.

### `Mood\EF2\GeofenceLog.cs`

Mục tiêu: log đủ dữ liệu kiểm tra vị trí.

Việc cần làm:
- Đổi hoặc bổ sung tên trường rõ nghĩa:
  - `Distance` nên là `DistanceKm` nếu có thể migration.
- Thêm `StoreName` hoặc join qua `StoreID` khi hiển thị admin.
- Cân nhắc thêm `AllowedRadiusKm` để biết lúc kiểm tra hệ thống dùng bán kính nào.

### `Mood\EF2\RentalLog.cs`

Mục tiêu: audit đầy đủ vòng đời mượn sách.

Việc cần làm:
- Chuẩn hóa `Action`: `Request`, `Approve`, `Reject`, `Borrow`, `Return`, `Overdue`, `Cancel`.
- Cân nhắc tách `ActorUserID` và `TargetUserID`; hiện `UserID` đang vừa là người mượn vừa là admin trong `UpdateRentalStatus`, dễ sai báo cáo.
- Thêm `OldStatus`, `NewStatus` nếu cần truy vết thay đổi trạng thái.

### `Mood\EF2\StoreLocation.cs`

Mục tiêu: dùng dữ liệu cửa hàng thật cho geofence.

Việc cần làm:
- Thêm annotation/validation:
  - `StoreName` bắt buộc, độ dài khoảng 200.
  - `Latitude`, `Longitude` có range hợp lệ.
  - `GeofenceRadius` > 0.
- Thêm seed data trong SQL migration cho cửa hàng mặc định.
- Nếu có nhiều chi nhánh, thêm `Address`, `Phone`, `SortOrder`.

### `Common\Repositories\LogRepository.cs`

Mục tiêu: repository không chỉ thêm log mà còn hỗ trợ tra cứu có lọc/phân trang.

Việc cần làm:
- Thêm các method:
  - `GetFaceAuthLogs(page, pageSize, userId, action, fromDate, toDate)`
  - `GetGeofenceLogs(page, pageSize, userId, storeId, fromDate, toDate)`
  - `GetRentalLogs(page, pageSize, userId, rentalId, action, fromDate, toDate)`
- Trả về object có `Items`, `Total`, `Page`, `PageSize`.
- Validate `page >= 1`, `pageSize` nằm trong khoảng 1-200.
- Bọc lỗi ghi log để không làm hỏng luồng chính; ví dụ nếu ghi log lỗi thì trả về nghiệp vụ vẫn rõ ràng, đồng thời ghi lỗi vào trace.

### `BaiTapLon\Controllers\FaceAuthController.cs`

Mục tiêu: biến khung face auth thành luồng ổn định, an toàn và dễ test.

Việc cần làm:
- Tách phần gọi Python API ra service riêng, ví dụ `BaiTapLon\Services\FaceAuthApiClient.cs`.
- Không dùng `ReadAsAsync<dynamic>` trực tiếp; tạo DTO rõ ràng:
  - `FaceAuthResponse { bool Success; double Confidence; string UserId; string Error; }`
- Kiểm tra file upload:
  - Chỉ nhận `.jpg`, `.jpeg`, `.png`.
  - Giới hạn dung lượng, ví dụ 2-5 MB.
  - Tạo tên file bằng `Guid`, không tin `file.FileName`.
- Khi API URL chưa cấu hình, trả lỗi rõ ràng thay vì mặc định logic có thể gây hiểu nhầm.
- `AuthenticateFace` hiện `overallSuccess = faceVerified || passwordOk`; với MFA nên đổi thành:
  - Đăng nhập thường: password đúng.
  - MFA khuôn mặt: password đúng và face đúng.
  - Chỉ cho fallback password-only khi có cấu hình cho phép.
- Rate limit hiện theo IP bằng `MemoryCache`; cần đưa số lần và thời gian ra `Web.config`.
- Khi ghi `FaceAuthLog`, lưu thêm lỗi API/timeout nếu có.
- Đảm bảo action nhạy cảm có `[ValidateAntiForgeryToken]` nếu gọi từ form MVC, hoặc cơ chế token nếu gọi AJAX.

### `BaiTapLon\Controllers\UsersController.cs`

Mục tiêu: nối face auth vào luồng đăng ký/đăng nhập thật của người dùng.

Việc cần làm:
- Trong đăng ký:
  - Sau khi tạo user thành công, chuyển người dùng đến `RegisterFace`.
  - Nếu người dùng bỏ qua, đánh dấu tài khoản chưa có face profile.
- Trong đăng nhập:
  - Sau khi username/password hợp lệ, nếu user yêu cầu MFA thì chuyển sang `LoginMFA`.
  - Không set auth cookie trước khi MFA thành công.
- Chuẩn hóa session/temp data dùng để truyền `userId` sang bước MFA, tránh nhận `userId` tùy ý từ client.

### `BaiTapLon\Views\Users\RegisterFace.cshtml`

Mục tiêu: giao diện đăng ký khuôn mặt dùng webcam ổn định.

Việc cần làm:
- Dùng `BaiTapLon\Scripts\FaceCapture.js` để bật/tắt camera, chụp ảnh, upload.
- Hiển thị trạng thái: đang mở camera, đang gửi, thành công, lỗi.
- Không hiển thị thông tin kỹ thuật dài; lỗi kỹ thuật ghi log, UI chỉ thông báo ngắn.
- Thêm fallback upload ảnh nếu trình duyệt không hỗ trợ camera, nếu nghiệp vụ cho phép.

### `BaiTapLon\Views\Users\LoginMFA.cshtml`

Mục tiêu: màn hình xác thực khuôn mặt sau bước password.

Việc cần làm:
- Không nhận `userId` trực tiếp từ query string nếu có thể; lấy từ session MFA.
- Gọi action `AuthenticateFace` hoặc `VerifyFace` bằng AJAX.
- Sau khi thành công redirect đến dashboard/trang trước đó.
- Sau khi thất bại cho phép thử lại theo giới hạn rate limit.

### `BaiTapLon\Scripts\FaceCapture.js`

Mục tiêu: dùng chung logic webcam cho đăng ký và MFA.

Việc cần làm:
- Tách các hàm:
  - `startCamera(videoElement)`
  - `stopCamera(stream)`
  - `captureBlob(videoElement)`
  - `uploadFace(url, blob, extraFields)`
- Xử lý quyền camera bị từ chối.
- Dọn stream khi rời trang.
- Gửi kèm anti-forgery token nếu action MVC yêu cầu.

### `BaiTapLon\Controllers\GeofenceController.cs`

Mục tiêu: dùng tọa độ cửa hàng thật và trả kết quả đáng tin.

Việc cần làm:
- Thay hard-code bằng truy vấn `StoreLocation` từ database:
  - Lấy tất cả cửa hàng `IsActive = true`.
  - Tính khoảng cách tới từng cửa hàng.
  - Chọn cửa hàng gần nhất.
  - `inZone = nearest.DistanceKm <= nearest.GeofenceRadius`.
- Nếu không có cửa hàng active, trả lỗi cấu hình rõ ràng.
- Không nhận `userId` tự do từ client nếu người dùng đã đăng nhập; lấy từ session/auth.
- Ghi `GeofenceLog` với `StoreID`, tọa độ user, khoảng cách, bán kính dùng kiểm tra.
- Validate `lat` trong `[-90, 90]`, `lon` trong `[-180, 180]`.

### `BaiTapLon\Views\Product\Detail.cshtml`

Mục tiêu: hiển thị nút mượn sách theo kết quả geofence.

Việc cần làm:
- Khi trang load, gọi browser geolocation.
- Gửi lat/lon đến `GeofenceController.CheckGeofence`.
- Nếu `inZone = true`, bật nút `Mượn sách`.
- Nếu ngoài vùng, ẩn hoặc disable nút và hiển thị thông báo ngắn: `Chỉ hỗ trợ mượn tại cửa hàng`.
- Xử lý trường hợp người dùng từ chối quyền vị trí.

### `BaiTapLon\Views\Product\ListProduct.cshtml` và `Search.cshtml`

Mục tiêu: trải nghiệm nhất quán ở danh sách sản phẩm.

Việc cần làm:
- Không gọi geofence lặp lại cho từng sản phẩm.
- Gọi một lần trên trang, lưu kết quả trong biến JS hoặc session ngắn hạn.
- Render trạng thái mượn sách đồng nhất với trang chi tiết.

### `BaiTapLon\Controllers\RentalController.cs`

Mục tiêu: triển khai nghiệp vụ mượn/trả thật, không chỉ log.

Việc cần làm:
- Xác định entity nghiệp vụ đang dùng:
  - Nếu mượn sách dựa trên `Orders`/`Order_Detail`, mở rộng status phù hợp.
  - Nếu cần bảng riêng, tạo entity `Rental`/`RentalDetail`.
- `RequestRental`:
  - Kiểm tra user đăng nhập.
  - Kiểm tra geofence còn hiệu lực.
  - Kiểm tra sách còn tồn kho.
  - Tạo yêu cầu mượn với trạng thái `Pending`.
  - Ghi `RentalLog` action `Request`.
- `UpdateRentalStatus`:
  - Chỉ admin được gọi.
  - Validate status.
  - Cập nhật trạng thái thật.
  - Ghi `RentalLog` với admin là actor, người mượn là target.
- Bổ sung action `ReturnRental` nếu trả sách là thao tác riêng.

### `BaiTapLon\Controllers\Api\LogsController.cs`

Mục tiêu: API log dùng được cho admin dashboard.

Việc cần làm:
- Dùng `LogRepository` thay vì query trực tiếp trong controller.
- Thêm filter:
  - `fromDate`, `toDate`
  - `userId`
  - `storeId`
  - `rentalId`
  - `result`
- Trả response gồm:
  - `items`
  - `total`
  - `page`
  - `pageSize`
- Validate `page` và `pageSize`.
- Sửa `[Authorize(Roles = "Admin")]` theo cơ chế role thật của project; nếu project dùng `Quyen` riêng, cần custom authorize hoặc kiểm tra session.
- Dispose `_db` nếu vẫn giữ context trực tiếp.

### `BaiTapLon\Areas\Admin\Views\Logs\*.cshtml`

Mục tiêu: admin xem log không cần gọi API thủ công.

Việc cần làm:
- Kiểm tra `BaiTapLon\Areas` đã tồn tại; nếu chưa có đúng `Admin`, tạo:
  - `Areas\Admin\Controllers\LogsController.cs`
  - `Areas\Admin\Views\Logs\FaceAuthLogs.cshtml`
  - `Areas\Admin\Views\Logs\GeofenceLogs.cshtml`
  - `Areas\Admin\Views\Logs\RentalLogs.cshtml`
- Mỗi trang có bảng, phân trang, filter ngày, user/action/result.
- Với log ảnh khuôn mặt, chỉ hiển thị đường dẫn/preview cho admin được phép.
- Không show toàn bộ `DeviceInfo` dài trong bảng; đưa vào modal/chi tiết.

### `BaiTapLon\Controllers\HomeController.cs` hoặc menu admin hiện có

Mục tiêu: thêm đường dẫn đến màn hình quản trị mới.

Việc cần làm:
- Tìm menu admin hiện tại rồi thêm mục:
  - `Quản lý mượn sách`
  - `Nhật ký xác thực`
  - `Nhật ký vị trí`
  - `Nhật ký mượn/trả`
- Chỉ hiển thị cho tài khoản admin.

### `sql\migrations\20260508_add_stores.sql`

Mục tiêu: tạo bảng cửa hàng và dữ liệu mặc định.

Việc cần làm:
- Kiểm tra script tạo bảng `StoreLocations` có đủ:
  - `ID`
  - `StoreName`
  - `Latitude`
  - `Longitude`
  - `GeofenceRadius`
  - `IsActive`
- Thêm dữ liệu cửa hàng thật thay vì tọa độ mẫu.
- Đảm bảo script idempotent: chạy lại không lỗi.

### `sql\migrations\20260508_add_logs.sql`

Mục tiêu: tạo bảng log đúng với entity.

Việc cần làm:
- Kiểm tra tên bảng/cột khớp `FaceAuthLog`, `GeofenceLog`, `RentalLog`.
- Thêm index:
  - `FaceAuthLogs(Timestamp, UserID, Action)`
  - `GeofenceLogs(Timestamp, UserID, StoreID)`
  - `RentalLogs(Timestamp, RentalID, UserID, Action)`
- Nếu thêm cột mới như `ErrorMessage`, `AllowedRadiusKm`, `ActorUserID`, cập nhật script.
- Đảm bảo script idempotent.

### `scripts\apply_sql_migrations.ps1`

Mục tiêu: chạy migration có thứ tự và dễ lặp lại.

Việc cần làm:
- Kiểm tra script nhận connection string/server/database từ tham số.
- Chạy theo thứ tự file trong `sql\migrations`.
- Log file nào đã chạy thành công/thất bại.
- Không chạy nhầm vào production nếu chưa xác nhận.

### `Tests\FaceAuthControllerTests.cs`

Mục tiêu: test controller mà không phụ thuộc camera/API thật.

Việc cần làm:
- Mock `ControllerContext`, `HttpRequestBase`, `HttpFileCollectionBase`.
- Thêm test:
  - Không có file trả BadRequest/JSON lỗi.
  - File sai định dạng bị từ chối.
  - API Python timeout trả lỗi và ghi log.
  - MFA yêu cầu password đúng và face đúng nếu bật MFA nghiêm ngặt.
- Sau khi tách `FaceAuthApiClient`, mock service thay vì gọi HTTP thật.

### `Tests\GeofenceControllerTests.cs` cần tạo mới

Mục tiêu: kiểm tra tính khoảng cách và lựa chọn cửa hàng gần nhất.

Việc cần làm:
- Test lat/lon không hợp lệ.
- Test không có cửa hàng active.
- Test trong vùng và ngoài vùng.
- Test chọn đúng cửa hàng gần nhất khi có nhiều cửa hàng.

### `Tests\RentalControllerTests.cs` cần tạo mới

Mục tiêu: kiểm tra luồng mượn/trả.

Việc cần làm:
- User chưa đăng nhập không được mượn.
- Ngoài geofence không được mượn.
- Hết tồn kho không được mượn.
- Admin approve/reject/return cập nhật status và ghi log.

## 5. Tiêu chí nghiệm thu

- Build solution `DongTrieuBookStore.sln` thành công.
- Migration SQL chạy được trên database mới và chạy lại không lỗi.
- Đăng ký user có thể đăng ký khuôn mặt, lưu ảnh mẫu, gọi API Python, ghi `FaceAuthLog`.
- Đăng nhập MFA không set auth cookie trước khi xác thực đủ điều kiện.
- Geofence dùng dữ liệu `StoreLocation` thật, không còn tọa độ hard-code.
- Nút `Mượn sách` chỉ bật khi người dùng trong vùng hợp lệ.
- Rental workflow có trạng thái rõ ràng và ghi log ở mọi bước chính.
- Admin xem được face/geofence/rental logs với phân trang và filter.
- Test controller chính chạy được mà không cần API Python thật.

## 6. Rủi ro và lưu ý bảo mật

- Ảnh khuôn mặt và vị trí GPS là dữ liệu nhạy cảm; chỉ admin được cấp quyền mới xem được.
- Không lưu ảnh xác thực thất bại lâu hơn cần thiết nếu không có yêu cầu nghiệp vụ.
- Không tin `userId` gửi từ client trong các action nhạy cảm; ưu tiên lấy từ auth/session.
- API Python phải có timeout, retry hợp lý và xử lý lỗi rõ ràng.
- Nếu dùng HTTPS ở production, `FaceAuthAPI` cũng nên là HTTPS.
- Cần chính sách dọn log/ảnh cũ, ví dụ script định kỳ trong `sql\cleanup\cleanup_old_logs.sql`.

## 7. Gợi ý chia phase

### Phase 1: Nền tảng dữ liệu
- Cập nhật SQL migrations.
- Cập nhật EF models/context.
- Chạy migration local.

### Phase 2: FaceAuth
- Tách service gọi Python API.
- Sửa controller theo MFA đúng.
- Hoàn thiện `RegisterFace.cshtml`, `LoginMFA.cshtml`, `FaceCapture.js`.
- Viết test.

### Phase 3: Geofence
- Hoàn thiện `StoreLocation`.
- Sửa `GeofenceController`.
- Gắn UI ở product detail/list/search.
- Viết test.

### Phase 4: Rental và Admin
- Hoàn thiện nghiệp vụ mượn/trả.
- Hoàn thiện logs API.
- Thêm admin views và menu.
- Viết test và kiểm thử thủ công.

