# Lich su trien khai upgrade

File nay dung de tiep tuc cong viec neu phien lam viec bi ngat hoac het token. Moi buoc nen ghi: thoi gian, file da sua, noi dung chinh, viec con lai.

## 2026-05-08 - Khoi dong trien khai theo `upgrade_plan.md`

### Da doc hien trang
- Solution: `DongTrieuBookStore.sln`
- Project web: `BaiTapLon\DongTrieuBookStoreOnline.csproj`
- Project EF/model: `Mood\Mood.csproj`
- Khong co `Common.csproj`; thu muc `Common` dang nam ngoai solution rieng.
- Cac controller/model moi da co tren o dia nhung nhieu file chua duoc include vao `.csproj`.

### Quyet dinh ky thuat ban dau
- Giu `LogDbContext` rieng cho audit log.
- Cho `DefaultConnection` tro cung connection string voi `QuanLySachDBContext` de log va nghiep vu cung chay duoc tren database local hien tai.
- Chuan hoa appSettings cho face auth/geofence/rate limit theo plan.
- Lam phase nen tang truoc: config, EF model, migration SQL, repository.

### Viec dang lam
- Cap nhat `BaiTapLon\Web.config`.
- Include cac entity log/store vao `Mood\Mood.csproj`.
- Bo sung validation/annotation cho entity log/store.
- Lam migration SQL idempotent.

### Da hoan thanh trong dot nay
- Tao file `LichSu.md`.
- Cap nhat `BaiTapLon\Web.config`: them `DefaultConnection`, chuan hoa key face auth/geofence/rate limit.
- Cap nhat `Mood\Mood.csproj`: include `FaceAuthLog`, `GeofenceLog`, `RentalLog`, `StoreLocation`, `LogDbContext`.
- Cap nhat entity log/store: them annotation, cot audit bo sung (`ErrorMessage`, `RequestId`, `AllowedRadiusKm`, `ActorUserID`, `OldStatus`, `NewStatus`...).
- Cap nhat `LogDbContext`: map bang plural `FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`.
- Cap nhat `QuanLySachDBContext`: them `DbSet<StoreLocation>`.
- Cap nhat migration SQL thanh idempotent va them index log.
- Cap nhat `Common\Repositories\LogRepository.cs`: them query phan trang/lọc va boc loi ghi log.
- Chuyen `BaiTapLon\Controllers\Api\LogsController.cs` sang MVC `Controller` de khong can WebApi package.
- Include cac controller/log repository/view/script moi vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Sua `FaceAuthController` bo `ReadAsAsync<dynamic>`, dung `Newtonsoft.Json.Linq` va `HttpRuntime.Cache`.
- Build bang Visual Studio MSBuild thanh cong sau cac thay doi nen tang.
- Cap nhat `GeofenceController`: bo toa do hard-code, doc `StoreLocation` active tu DB, chon cua hang gan nhat, validate lat/lon, ghi `AllowedRadiusKm` va `StoreName`.

### Lenh da chay
- `dotnet build DongTrieuBookStore.sln -v:minimal`: that bai do .NET SDK thieu `WebApplication.targets` cho project MVC cu.
- `MSBuild.exe DongTrieuBookStore.sln /v:minimal`: lan 1 loi `FaceAuthController`, lan 2 thanh cong.

### Viec tiep theo
- Build lai sau khi sua `GeofenceController`.
- Hoan thien `FaceAuthController`: validate file upload, timeout, confidence threshold, MFA password + face theo config.
- Hoan thien UI `FaceCapture.js`, `RegisterFace.cshtml`, `LoginMFA.cshtml`.
- Gan geofence vao `Product\Detail.cshtml`, `ListProduct.cshtml`, `Search.cshtml`.
- Hoan thien rental workflow.

## 2026-05-08 - Cap nhat tiep phase FaceAuth, Geofence, Rental

### Da hoan thanh them
- Build lai sau `GeofenceController`: thanh cong.
- Cap nhat `BaiTapLon\Controllers\FaceAuthController.cs`:
  - Validate file upload: bat buoc co file, khong rong, gioi han dung luong theo `FaceAuthMaxUploadBytes`.
  - Chi nhan `.jpg`, `.jpeg`, `.png`.
  - Dung `FaceSampleStoragePath` thay vi hard-code `DataImage/FaceSamples`.
  - Dung `FaceAuthTimeoutSeconds` cho `HttpClient.Timeout`.
  - Dung `FaceAuthMinConfidence` de quyet dinh ket qua.
  - Dung `FaceAuthRateLimitAttempts` va `FaceAuthRateLimitSeconds`.
  - Sua logic MFA: mac dinh khong con `password OR face`; neu `EnableFaceMFA=true` thi can face pass, va neu co password thi password cung phai pass. Chi fallback password-only khi `AllowPasswordOnlyFallback=true`.
- Cap nhat `BaiTapLon\Scripts\FaceCapture.js`:
  - Tach `startCamera`, `stopCamera`, `captureBlob`, `uploadFace`, `init`.
  - Xu ly loi camera/upload va hien status.
  - Dung `credentials: same-origin`.
- Cap nhat view face:
  - `BaiTapLon\Views\Users\RegisterFace.cshtml`
  - `BaiTapLon\Views\Users\LoginMFA.cshtml`
  - `BaiTapLon\Views\Shared\_FaceMFA.cshtml`
  - Doi layout ve `_LayoutHome.cshtml`, bo noi dung loi encoding cu.
- Cap nhat `BaiTapLon\Views\Product\Detail.cshtml`:
  - Them nut `Muon sach` bi disable mac dinh.
  - Goi browser geolocation, POST `/Geofence/CheckGeofence`.
  - Chi enable nut khi `inZone=true`.
  - Khi bam nut, POST `/Rental/RequestRental`.
- Cap nhat `BaiTapLon\Controllers\RentalController.cs`:
  - `RequestRental` khong bat buoc client gui `userId`, tu resolve tu auth neu co.
  - Validate user/rentalId co ban.
  - Ghi `ActorUserID`, `NewStatus=Pending`.
  - `UpdateRentalStatus` validate admin/status va ghi `ActorUserID`, `NewStatus`.
- Build bang Visual Studio MSBuild sau moi nhom thay doi: thanh cong.

### Lenh xac minh moi nhat
- `MSBuild.exe DongTrieuBookStore.sln /v:minimal`: thanh cong, tao `BaiTapLon\bin\BaiTapLon.dll`.

### Viec con lai theo plan
- Gan geofence vao `BaiTapLon\Views\Product\ListProduct.cshtml` va `Search.cshtml` de danh sach san pham dong nhat voi trang chi tiet.
- Hoan thien rental workflow that su voi entity/bang nghiep vu rieng hoac mo rong `Orders`/`Order_Detail`; hien tai `RentalController` moi validate/log request, chua tru ton kho/chua luu request vao bang nghiep vu.
- Them admin views cho logs:
  - `Areas\Admin\Controllers\LogsController.cs`
  - `Areas\Admin\Views\Logs\FaceAuthLogs.cshtml`
  - `Areas\Admin\Views\Logs\GeofenceLogs.cshtml`
  - `Areas\Admin\Views\Logs\RentalLogs.cshtml`
- Them menu admin tro den cac trang log/rental.
- Bo sung tests cho face auth/geofence/rental. Luu y test hien tai `Tests\FaceAuthControllerTests.cs` co nguy co can mock `Request`.
- Chay migration SQL tren database local bang `scripts\apply_sql_migrations.ps1` sau khi xac nhan connection.

## 2026-05-08 - Tiep tuc theo thu tu uu tien

### Da hoan thanh them
- Sua admin logs:
  - `Areas\Admin\Controllers\LogsAdminController.cs` khong con dung `HttpClient`/`ReadAsAsync<dynamic>`.
  - Controller ke thua `BaseController` de dung session admin hien co.
  - Dung truc tiep `Common\Repositories\LogRepository.cs`.
  - Them `Areas\Admin\Models\LogFilterModel.cs`.
  - Cap nhat 3 view log co filter va phan trang co ban:
    - `Areas\Admin\Views\Logs\FaceAuthLogs.cshtml`
    - `Areas\Admin\Views\Logs\GeofenceLogs.cshtml`
    - `Areas\Admin\Views\Logs\RentalLogs.cshtml`
  - Include controller/model/views vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Cap nhat SQL:
  - `sql\cleanup\cleanup_old_logs.sql` dung bang moi `FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`.
  - `sql\README_migrations.md` dung ten bang/index moi.
  - Sua `scripts\apply_sql_migrations.ps1` de root tro ve thu muc repo, khong phai thu muc `scripts`.
- Noi luong `UsersController` vao FaceAuth/MFA:
  - Them session key `FACE_MFA_SESSION`, `FACE_REGISTER_SESSION` trong `BaiTapLon\Common\Constant.cs`.
  - Dang ky thanh cong neu `EnableFaceMFA=true` tra ma `2`, luu pending session va redirect frontend sang `/Users/RegisterFace`.
  - Dang nhap dung mat khau neu `EnableFaceMFA=true` tra ma `2`, luu pending session va redirect frontend sang `/Users/LoginMFA`.
  - Them action `RegisterFace` va `LoginMFA` trong `UsersController`.
  - `FaceAuthController` set `USER_SESSION` sau khi register face/MFA thanh cong.
  - Cap nhat `Content\libs\commonjs\loginCommon.js` de xu ly ma `2`.
- Gan geofence vao danh sach san pham:
  - `Views\Product\ListProduct.cshtml`
  - `Views\Product\Search.cshtml`
  - Moi trang goi geofence mot lan, enable cac nut muon sach neu trong vung.
- Tach service FaceAuth:
  - Them `Services\FaceAuthApiClient.cs`.
  - Them `Services\FaceAuthResponse.cs`.
  - `FaceAuthController` dung service moi thay vi tu goi `HttpClient`.
- Da chay migration local:
  - `powershell.exe -ExecutionPolicy Bypass -File scripts\apply_sql_migrations.ps1 -ServerInstance "(localdb)\MSSQLLocalDB" -Database "QLNhaSach"`
  - Ket qua: thanh cong.

### Xac minh
- `MSBuild.exe DongTrieuBookStore.sln /v:minimal`: thanh cong sau moi cum thay doi.
- Migration SQL LocalDB `QLNhaSach`: thanh cong.

### Viec con lai lon nhat
- Hoan thien rental workflow that su:
  - Tao entity/bang nghiep vu `Rental`/`RentalDetail` hoac mo rong `Orders`/`Order_Detail`.
  - Kiem tra ton kho, tru ton khi duyet/muon, cong lai khi tra.
  - Trang admin quan ly yeu cau muon/tra sach.
- Them menu admin tro den `LogsAdmin/FaceAuth`, `LogsAdmin/Geofence`, `LogsAdmin/Rental`.
- Bo sung tests:
  - Sua `FaceAuthControllerTests.cs` de mock request/file.
  - Tao `GeofenceControllerTests.cs`.
  - Tao `RentalControllerTests.cs`.
- Can test thu cong voi Python FaceAuth API that va browser co quyen camera/GPS.

## 2026-05-08 - Rental workflow, admin menu, tests

### Da hoan thanh them
- Tao rental workflow that su bang bang rieng:
  - Them entity `Mood\EF2\RentalRequest.cs`.
  - Them `DbSet<RentalRequest>` vao `QuanLySachDBContext`.
  - Include entity vao `Mood\Mood.csproj`.
  - Them migration `sql\migrations\20260508_add_rental_requests.sql`.
- Cap nhat `BaiTapLon\Controllers\RentalController.cs`:
  - `RequestRental` tao `RentalRequest` status `Pending`.
  - Kiem tra user, product ton tai, product active, `Soluong` du.
  - `UpdateRentalStatus` xu ly `Approve/Borrow`, `Reject`, `Cancel`, `Return`, `Overdue`.
  - Approve/Borrow tru `Sanpham.Soluong`.
  - Return cong lai `Sanpham.Soluong`.
  - Dung transaction khi cap nhat rental + product.
  - Ghi `RentalLog` cho tung buoc.
- Them admin quan ly muon sach:
  - `Areas\Admin\Controllers\RentalAdminController.cs`.
  - `Areas\Admin\Views\RentalAdmin\Index.cshtml`.
  - Include vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Them menu admin:
  - Link `/Admin/RentalAdmin/Index`.
  - Link `/Admin/LogsAdmin/FaceAuth`.
  - Link `/Admin/LogsAdmin/Geofence`.
  - Link `/Admin/LogsAdmin/Rental`.
- Chay migration LocalDB lai:
  - Tao/cap nhat `RentalRequests`.
  - Ket qua: thanh cong.
- Them test source:
  - `Tests\GeofenceControllerTests.cs`.
  - `Tests\RentalControllerTests.cs`.
  - Bo sung test `VerifyFace_NoFile_ReturnsJson` vao `Tests\FaceAuthControllerTests.cs`.

### Xac minh
- `MSBuild.exe DongTrieuBookStore.sln /v:minimal`: thanh cong sau khi them rental workflow/admin menu.
- `scripts\apply_sql_migrations.ps1`: thanh cong tren `(localdb)\MSSQLLocalDB`, database `QLNhaSach`.

### Luu y test
- Thu muc `Tests` hien khong co `.csproj`, nen cac test moi dang la source test chua duoc build/run tu solution.
- Can tao/include test project MSTest rieng neu muon chay tu Test Explorer/CI.

### Checklist test thu cong con can lam
- Chay Python FaceAuth API tai URL trong `FaceAuthAPI`.
- Mo browser qua HTTPS/local IIS, vao dang ky user moi, xac nhan redirect `/Users/RegisterFace`.
- Cap quyen camera, chup/gui face, xac nhan tao session user va co log `FaceAuthLogs`.
- Dang xuat, dang nhap lai, xac nhan redirect `/Users/LoginMFA`, face pass moi vao duoc.
- Vao trang chi tiet/list/search san pham, cap quyen GPS, xac nhan nut `Muon sach` chi enable khi trong geofence.
- Bam `Muon sach`, vao `/Admin/RentalAdmin/Index`, duyet yeu cau, xac nhan `Sanpham.Soluong` giam.
- Tra sach trong admin, xac nhan `Sanpham.Soluong` tang lai va `RentalLogs` co ban ghi.

## 2026-05-08 - Trien khai theo `upgrade_plan.md_version2.md`

### Buoc 1 - Bo OCR khoi luong dang nhap/dang ky
- Da sua `BaiTapLon\Controllers\UsersController.cs`: xoa nested `OcrResponse`, xoa action `CallPythonOcrApi`, bo cac using chi phuc vu OCR.
- Da sua `BaiTapLon\Views\Users\Login.cshtml`: xoa khoi UI quet OCR CCCD trong form dang ky desktop va xoa script goi `/Users/CallPythonOcrApi`.
- Viec tiep theo: them dang nhap bang khuon mat, cau hinh vi tri Nha sach Tan Hanh, va nang cap rental workflow theo version2.

### Buoc 2 - Them dang nhap bang khuon mat
- Da sua `BaiTapLon\Controllers\FaceAuthController.cs`: them action `AuthenticateFaceLogin(string userName)` theo luong `username + face`, tim user phia server, validate trang thai tai khoan, goi FaceAuth API, ghi `FaceAuthLog`, set `USER_SESSION` va auth cookie khi thanh cong.
- Da sua `BaiTapLon\Views\Users\Login.cshtml`: them khu vuc dang nhap bang khuon mat cho desktop/mobile, dung webcam qua `FaceCapture.js`, goi `/FaceAuth/AuthenticateFaceLogin` va hien thong bao thanh cong/that bai.
- Viec tiep theo: cau hinh vi tri Nha sach Tan Hanh cho geofence.

### Buoc 3 - Cau hinh geofence Nha sach Tan Hanh
- Da sua `sql\migrations\20260508_add_stores.sql`: vo hieu hoa seed `Dong Trieu Book Store`, them/cap nhat seed `Nha sach Tan Hanh` tai `75 Pham Van Dieu, Bien Hoa, Dong Nai, Viet Nam`.
- Da dat ban kinh mac dinh 0.5 km va ghi chu can xac minh lai toa do GPS chinh xac truoc production.
- Viec tiep theo: bo sung request date/borrow days, face token rental va man hinh theo doi sach muon.

### Buoc 4 - Mo rong rental schema va token xac thuc khuon mat
- Da them `BaiTapLon\Services\FaceRentalTokenService.cs`: tao token ngan han trong `HttpRuntime.Cache`, rang buoc theo user/product, validate mot lan roi consume.
- Da sua `Mood\EF2\RentalRequest.cs`: them `RequestDate`, `BorrowDays`, `ExpectedReturnDate`, `ActualReturnDate`, `RejectReason`.
- Da sua `sql\migrations\20260508_add_rental_requests.sql`: them cac cot ngay/số ngay muon va migration idempotent cho DB cu.
- Da include service token vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Viec tiep theo: them endpoint `VerifyRentalFace` va bat buoc `RequestRental` kiem tra face token.

### Buoc 5 - Noi face token vao luong muon sach backend
- Da sua `BaiTapLon\Controllers\FaceAuthController.cs`: them `VerifyRentalFace(productId)`, lay user tu session, validate file face, goi FaceAuth API, ghi `RentalFaceVerifySuccess/Failed`, tao `faceToken` ngan han khi thanh cong.
- Da sua `BaiTapLon\Controllers\RentalController.cs`: `RequestRental` nhan `productId/requestDate/borrowDays/faceToken`, validate so ngay muon theo `RentalMaxBorrowDays`, bat buoc token face hop le, tao rental `Pending` voi ngay du kien tra.
- Da sua logic ton kho trong `RentalController`: dung helper `GetAvailableStock`, tru ton kho khi admin approve/borrow, cong lai khi return, cap nhat `ActualReturnDate`.
- Viec tiep theo: cap nhat UI chi tiet san pham de hien form ngay muon/so ngay muon va popup khuon mat.

### Buoc 6 - Cap nhat UI muon sach o trang chi tiet
- Da sua `BaiTapLon\Controllers\RentalController.cs`: them `CheckStock(productId, quantity)` de client kiem tra ton kho truoc khi mo xac nhan khuon mat.
- Da sua `BaiTapLon\Views\Product\Detail.cshtml`: them form thong tin muon sach gom ngay yeu cau mac dinh ngay hien tai va so ngay muon.
- Da them popup/khoi xac nhan khuon mat tren trang chi tiet: mo camera sau khi xac nhan form, goi `/FaceAuth/VerifyRentalFace`, sau do gui `/Rental/RequestRental` kem `faceToken`.
- Da cap nhat thong bao UI: trong vung Nha sach Tan Hanh, het ton kho, face thanh cong/that bai, gui yeu cau thanh cong.
- Viec tiep theo: them man hinh khach hang theo doi sach muon va cap nhat admin view hien ngay muon.

### Buoc 7 - Man hinh khach hang theo doi sach muon
- Da sua `BaiTapLon\Controllers\RentalController.cs`: them action `MyRentals(status)` lay rental cua user hien tai tu session/auth, join voi sach va khong nhan `userId` tu query.
- Da them `BaiTapLon\Views\Rental\MyRentals.cshtml`: hien sach, ngay yeu cau, so ngay muon, ngay du kien tra, ngay tra thuc te, trang thai va canh bao qua han.
- Da sua `BaiTapLon\Views\Shared\TopMenu.cshtml`: them link `Sach dang muon` khi khach hang da dang nhap.
- Da sua `BaiTapLon\Areas\Admin\Views\RentalAdmin\Index.cshtml`: hien them `RequestDate`, `BorrowDays`, `ExpectedReturnDate`.
- Da include view `Views\Rental\MyRentals.cshtml` vao web csproj.
- Viec tiep theo: cap nhat cac nut muon o danh sach/tim kiem va chay build xac minh.

### Buoc 8 - Dong bo nut muon sach tren danh sach/tim kiem
- Da sua `BaiTapLon\Views\Product\ListProduct.cshtml` va `BaiTapLon\Views\Product\Search.cshtml`: nut `Muon sach` khong con goi truc tiep `/Rental/RequestRental` vi endpoint nay bat buoc face token; thay vao do thong bao nguoi dung mo trang chi tiet de nhap ngay muon va xac nhan khuon mat.
- Da chinh `BaiTapLon\Views\Rental\MyRentals.cshtml` de dung ham map trang thai gon hon, tranh helper Razor phuc tap khi build.
- Viec tiep theo: chay build va sua loi neu co.

### Buoc 9 - Xac minh build va don sach OCR con sot
- Da build Release bang Visual Studio MSBuild: thanh cong, tao `BaiTapLon\bin\BaiTapLon.dll`.
- Build Debug bi loi do `BaiTapLon\obj\Debug\BaiTapLon.pdb` dang bi tien trinh khac khoa, khong phai loi compile.
- Da kiem tra OCR trong code chinh, chi con `BaiTapLon\Models\OcrResponse.cs`.
- Da xoa `BaiTapLon\Models\OcrResponse.cs` va bo include khoi `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Viec tiep theo: build Release lai sau khi xoa model OCR.

### Buoc 10 - Build lai sau khi xoa OCR model
- Da build Release lai bang Visual Studio MSBuild: thanh cong.
- Da chay `rg` cac tu khoa OCR trong `Controllers`, `Views`, `Scripts`, `Models`: khong con ket qua.
- Viec tiep theo: chay migration local de cap nhat DB neu co san LocalDB.

### Buoc 11 - Migration local va bo sung appSettings version2
- Da chay `scripts\apply_sql_migrations.ps1 -ServerInstance "(localdb)\MSSQLLocalDB" -Database "QLNhaSach"`: thanh cong.
- Migration da ap dung lai `add_logs`, `add_rental_requests`, `add_stores`; DB local co cot rental moi va seed Nha sach Tan Hanh.
- Da sua `BaiTapLon\Web.config`: them `FaceAuthRentalTokenMinutes`, `FaceAuthLoginMode`, `FaceAuthMaxAttempts`, `FaceAuthLockoutMinutes`, `RentalMaxBorrowDays`.
- Viec tiep theo: build Release lan cuoi sau khi cap nhat Web.config.

### Buoc 12 - Xac minh cuoi dot version2
- Da build Release lan cuoi bang Visual Studio MSBuild: thanh cong.
- Ket qua dau ra: `BaiTapLon\bin\BaiTapLon.dll`.
- Luu y: build Debug truoc do bi khoa file PDB do tien trinh khac dang giu `BaiTapLon\obj\Debug\BaiTapLon.pdb`; Release build xac nhan code compile duoc.
- Con can test thu cong voi browser: GPS tai Nha sach Tan Hanh, camera, Flask FaceAuth API, luong admin approve/return.

### Buoc 13 - Dieu chinh form dang nhap khuon mat
- Da sua `BaiTapLon\Views\Users\Login.cshtml`: bo partial `_FaceMFA` khoi form dang nhap desktop/mobile de dang nhap tai khoan/mat khau khong hien form xac nhan khuon mat.
- Da doi khu vuc dang nhap bang khuon mat thanh khoi an; chi hien va moi khoi dong camera khi nguoi dung bam `Dang nhap bang khuon mat`.
- Form xac nhan khuon mat khong con o nhap tai khoan rieng; lay tai khoan tu o `Tai khoan` cua form dang nhap chinh.
- Da cap nhat `upgrade_plan.md_version2.md` voi yeu cau luong form dang nhap moi.

### Buoc 14 - Hoan thien DTO/log FaceAuth version2 va lockout face-login
- Da sua `BaiTapLon\Services\FaceAuthResponse.cs`: bo sung `ExternalUserId`, `LivenessPassed`, `ErrorCode`, `ErrorMessage`, `RequestId`, `Purpose`, giu `Error` de tuong thich code cu.
- Da sua `BaiTapLon\Services\FaceAuthApiClient.cs`: map response Flask API theo ca camelCase va snake_case (`request_id`, `error_code`, `liveness_passed`, `message`), gui them `user_id` va `purpose`, tra error co `ErrorCode`.
- Da sua `Mood\EF2\FaceAuthLog.cs` va `sql\migrations\20260508_add_logs.sql`: them cot `Purpose`, `ErrorCode`, `LivenessPassed` cho `FaceAuthLogs` theo migration idempotent.
- Da sua `BaiTapLon\Controllers\FaceAuthController.cs`: cac luong Register/Login/MFA/Rental/Verify ghi them `RequestId`, `Purpose`, `ErrorCode`, `ErrorMessage`, `LivenessPassed`; rental/login truyen dung purpose sang API.
- Da them khoa tam thoi dang nhap khuon mat theo IP + tai khoan bang `FaceAuthMaxAttempts` va `FaceAuthLockoutMinutes`; that bai thi tang dem, thanh cong thi xoa dem.
- Da sua `BaiTapLon\Areas\Admin\Views\Logs\FaceAuthLogs.cshtml`: hien them `Purpose`, `Liveness`, `RequestId`, `ErrorCode`.
- Da chay migration LocalDB `QLNhaSach`: thanh cong.
- Da build Release bang Visual Studio MSBuild: thanh cong, tao `BaiTapLon\bin\BaiTapLon.dll`.

### Buoc 15 - Popup face auth giua man hinh va sua loi font view moi
- Da them `BaiTapLon\assets\css\face-auth-modal.css`: CSS dung chung cho popup xac thuc khuon mat, can giua man hinh, nen mo, video ti le on dinh, khoa scroll body khi mo popup.
- Da sua `BaiTapLon\Views\Shared\_LayoutHome.cshtml` va `BaiTapLon\DongTrieuBookStoreOnline.csproj` de nap/include CSS popup moi.
- Da sua `BaiTapLon\Views\Users\Login.cshtml`: dang nhap bang khuon mat desktop/mobile khong hien inline trong sidebar nua; bam nut moi mo popup giua man hinh, co nut dong, dong popup thi dung camera.
- Da sua `BaiTapLon\Views\Product\Detail.cshtml`: popup xac thuc khuon mat khi muon sach duoc dua ra giua man hinh, co nut dong, bam ngoai popup/dong/huy deu dung camera va tra ve form thong tin muon sach.
- Da sua cac file face/view bi chu khong dau hoac loi font:
  - `BaiTapLon\Views\Users\RegisterFace.cshtml`
  - `BaiTapLon\Views\Users\LoginMFA.cshtml`
  - `BaiTapLon\Views\Shared\_FaceMFA.cshtml`
  - `BaiTapLon\Scripts\FaceCapture.js`
- Da viet lai cac view moi bi mojibake/nhan tieng Anh:
  - `BaiTapLon\Views\Rental\MyRentals.cshtml`
  - `BaiTapLon\Areas\Admin\Views\RentalAdmin\Index.cshtml`
  - `BaiTapLon\Areas\Admin\Views\Logs\FaceAuthLogs.cshtml`
  - `BaiTapLon\Areas\Admin\Views\Logs\GeofenceLogs.cshtml`
  - `BaiTapLon\Areas\Admin\Views\Logs\RentalLogs.cshtml`
- Da quet lai cac view/script moi them de tim chu loi kieu `QuÃ¡`, `Äang`, `Lá»c`; cac ket qua con lai la status code/tieng Viet hop le hoac file cu khong lien quan.
- Da build Release bang Visual Studio MSBuild: thanh cong, tao `BaiTapLon\bin\BaiTapLon.dll`.

## 2026-05-09 - Bo sung quan ly muon tra sach phia khach hang va log admin

### Da hoan thanh
- Khoi phuc va viet lai `BaiTapLon\Views\Rental\MyRentals.cshtml` sau khi file bi rong do loi ghi file/lock.
- Man hinh khach hang `Rental/MyRentals` co tong hop: cho duyet, dang muon, tra tre, da tra; co filter trang thai va nut huy yeu cau khi con `Pending`.
- `BaiTapLon\Controllers\RentalController.cs` tinh count theo trang thai cho MyRentals, tra them `activeRentalCount` khi tao yeu cau muon thanh cong.
- `BaiTapLon\Controllers\HomeController.cs` tinh `ActiveRentalCount` cho menu khach hang.
- `BaiTapLon\Views\Shared\TopMenu.cshtml` them badge span `activeRentalCountBadge` tren menu `Sach dang muon`.
- `BaiTapLon\Views\Product\Detail.cshtml` cap nhat badge `Sach dang muon` ngay sau khi `/Rental/RequestRental` thanh cong.
- Cap nhat ban kinh geofence muon sach duoi 5km:
  - `BaiTapLon\Web.config`: `GeofenceDefaultRadiusKm=5`.
  - `BaiTapLon\Controllers\GeofenceController.cs`: fallback radius 5km.
  - `sql\migrations\20260508_add_stores.sql`: seed/update `Nha sach Tan Hanh` voi `GeofenceRadius=5` va sua font SQL.
- Kiem tra/fix view log admin:
  - `Areas\Admin\Views\Logs\FaceAuthLogs.cshtml` co empty state, xoa loc, hien Purpose/Liveness/RequestId/ErrorCode/ErrorMessage an toan khi null.
  - `Areas\Admin\Views\Logs\RentalLogs.cshtml` them xoa loc va action display cho trang thai/luong muon.
- Cap nhat `upgrade_plan.md_version2.md` them muc 19 de tiep tuc theo doi yeu cau nay.

### Luu y xac minh
- Can chay lai migration `20260508_add_stores.sql` tren DB local neu ban kinh trong bang `StoreLocations` van la 0.5.
- Can test thu cong tren browser: tao yeu cau muon thanh cong, badge `Sach dang muon` tang; admin duyet/tra sach va xem `RentalLogs`; face login/rental va xem `FaceAuthLogs`.
- `dotnet build` tren may hien tai van bi chan boi project MVC cu thieu `Microsoft.WebApplication.targets`; can build bang Visual Studio/MSBuild day du.
- Dieu chinh bo sung: `RentalController.MyRentals` tinh tong hop theo toan bo rental cua khach, filter `Tra tre` gom ca ban ghi qua ngay du kien tra du chua duoc admin danh dau `Overdue`; them endpoint `GET /Rental/ActiveRentalCount` de lay count badge khi can refresh.

## 2026-05-09 - Version3: log admin, quan ly nha sach, chan muon trung

### Da hoan thanh
- Tao `upgrade_plan.md_version3.md` tu cac viec con thieu cua version2.
- Bo sung logic thong ke cho cac man hinh log admin:
  - `LogsAdmin/FaceAuth`: tong, thanh cong, that bai, hom nay.
  - `LogsAdmin/Geofence`: tong, trong vung, ngoai vung, hom nay.
  - `LogsAdmin/Rental`: tong, tao yeu cau, duyet muon, tra/qua han.
- Cap nhat view log admin co empty state, xoa loc, format thoi gian va thong tin null an toan.
- Them man hinh admin `Admin/WebManager/StoreLocation` de cap nhat thong tin nha sach, dia chi, phone, toa do, ban kinh, active, sort order.
- Man hinh `StoreLocation` hien ban do OpenStreetMap theo toa do hien tai, khong con phai gan cung vi tri trong code.
- Them link `Thong tin nha sach` vao menu admin `Quan li Website`.
- Them `RentalController.CheckActiveRental(productId)` de kiem tra sach dang duoc tai khoan muon/cho duyet.
- `RentalController.RequestRental` chan tao yeu cau moi neu user dang co rental active cho cung sach.
- Trang chi tiet sach goi `CheckActiveRental`; neu dang muon thi nut doi thanh `Dang muon sach` va khong mo form muon.
- Trang danh sach/tim kiem sau khi qua geofence se kiem tra tung sach, doi nut thanh `Dang muon sach` voi sach dang co rental active.

### Can test thu cong
- Mo `/Admin/LogsAdmin/FaceAuth`, `/Admin/LogsAdmin/Geofence`, `/Admin/LogsAdmin/Rental` de xac nhan thong ke/filter/empty state.
- Mo `/Admin/WebManager/StoreLocation`, sua toa do/ban kinh va xac nhan map thay doi.
- Dang nhap khach, tao yeu cau muon sach, sau do vao lai chi tiet/danh sach de xac nhan nut thanh `Dang muon sach`.
- Thu goi tao rental trung sach de xac nhan backend tra loi khong cho muon trung.

## 2026-05-09 - Bo sung StoreLocation/3, gioi thieu va sua log admin khong hien du lieu

### Da hoan thanh
- Cap nhat `upgrade_plan.md_version3.md` them muc dieu chinh bo sung theo yeu cau test thuc te:
  - `/Admin/WebManager/StoreLocation/3` sua duoc thong tin nha sach mo rong.
  - `/gioi-thieu/` doc noi dung tu database, khong hard-code.
  - Nhat ky xac thuc va nhat ky muon tra co logic tao/kiem tra bang truoc khi ghi/doc.
- Mo rong `Mood\EF2\StoreLocation.cs`:
  - Them `Email`, `IconPath`, `WelcomeTitle`, `WelcomeMessage`, `AboutContent`, `MissionContent`.
- Cap nhat `BaiTapLon\Areas\Admin\Controllers\WebManagerController.cs`:
  - Tao gia tri mac dinh cho cac truong nha sach mo rong.
  - Khi luu mot nha sach active thi tu dong tat active cac nha sach khac de trang gioi thieu/geofence chi dung mot cau hinh chinh.
- Cap nhat `BaiTapLon\Areas\Admin\Views\WebManager\StoreLocation.cshtml`:
  - Them form sua email, icon/logo, tieu de gioi thieu, loi chao, noi dung gioi thieu, muc tieu.
  - Hien preview icon/logo neu co duong dan.
- Cap nhat `BaiTapLon\Controllers\AboutUsController.cs` va `BaiTapLon\Views\AboutUs\Index.cshtml`:
  - Trang `/gioi-thieu/` lay nha sach active tu `StoreLocations`.
  - Hien ten nha sach, icon, loi chao, gioi thieu, muc tieu, dia chi, email, so dien thoai theo DB.
- Da luu lai cac view vua sua bang UTF-8 BOM:
  - `BaiTapLon\Views\AboutUs\Index.cshtml`
  - `BaiTapLon\Areas\Admin\Views\WebManager\StoreLocation.cshtml`
- Cap nhat `Common\Repositories\LogRepository.cs`:
  - Them `EnsureLogTables` truoc khi ghi/doc `FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`.
  - Sua loc `toDate` thanh moc ket thuc exclusive de chon ngay nao lay het log trong ngay do.
- Cap nhat `sql\migrations\20260508_add_stores.sql`:
  - Them cac cot nha sach mo rong idempotent.
  - Tach batch bang `GO` de SQL Server nhan cot moi truoc khi insert/update.
  - Dien gia tri mac dinh cho cac ban ghi StoreLocations cu bi thieu thong tin.

### Xac minh
- Da chay migration local:
  - `sqlcmd -S "(localdb)\MSSQLLocalDB" -d "QLNhaSach" -i "sql\migrations\20260508_add_stores.sql"`: thanh cong sau khi tach batch.
- Da kiem tra DB local:
  - `StoreLocations` co cac cot `Email`, `IconPath`, `WelcomeTitle`.
  - Ban ghi ID 3 `Nhà sách Thắng lê` da co email, icon va tieu de gioi thieu mac dinh.
  - `FaceAuthLogs` co 31 dong, log moi nhat co `FaceLoginSuccess/FaceLoginFailed`.
  - `RentalLogs` co 14 dong, log moi nhat co `Return`, `Approve`, `Request`.
- Build solution bang Visual Studio MSBuild thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`

### Luu y test thu cong
- Mo `/Admin/WebManager/StoreLocation/3`, chinh thong tin va tick active, bam luu.
- Mo `/gioi-thieu/` de xac nhan noi dung, icon/logo, email, so dien thoai doi theo ban ghi vua luu.
- Mo `/Admin/LogsAdmin/FaceAuth` va `/Admin/LogsAdmin/Rental`; DB local hien co du lieu nen neu trang van rong can kiem tra session admin/connection string runtime cua IIS Express co tro dung `QLNhaSach` hay khong.

## 2026-05-09 - Sua loi LogsAdmin, font gioi thieu va nang editor StoreLocation

### Da hoan thanh
- Cap nhat `upgrade_plan.md_version3.md` them muc 6 theo loi test moi:
  - Sua loi LINQ `NormalizeToExclusive` tren `/Admin/LogsAdmin/FaceAuth` va `/Admin/LogsAdmin/Geofence`.
  - Sua font trang `/gioi-thieu/`.
  - Nang man hinh admin sua thong tin hien thi thanh editor co chon anh va tim map.
- Sua `Common\Repositories\LogRepository.cs`:
  - Tinh `toDateExclusive` thanh bien truoc khi dua vao `Where`.
  - Khong con goi method C# ben trong expression LINQ to Entities.
- Mo rong `Mood\EF2\StoreLocation.cs` va `sql\migrations\20260508_add_stores.sql`:
  - Them `BannerPath`.
  - Migration them cot idempotent va dien banner mac dinh cho du lieu cu.
- Viet lai `BaiTapLon\Views\AboutUs\Index.cshtml`:
  - Sua het chu mojibake.
  - Dung `BannerPath`, `IconPath`, `StoreName`, `WelcomeTitle`, `WelcomeMessage`, `AboutContent`, `MissionContent`, `Address`, `Email`, `Phone` tu DB.
  - Cho render noi dung editor bang `Html.Raw`.
- Nang `BaiTapLon\Areas\Admin\Views\WebManager\StoreLocation.cshtml`:
  - Tach thanh cac khoi editor: noi dung gioi thieu, anh/thong tin lien he, ban do/ban kinh, trang thai.
  - Them CKEditor cho loi chao, noi dung gioi thieu va muc tieu.
  - Them nut chon anh CKFinder cho icon/logo va banner.
  - Them o tim vi tri bang OpenStreetMap Nominatim; chon ket qua se cap nhat dia chi, vi do, kinh do va iframe map.
- Dong bo cau hinh dong tren layout/footer:
  - `BaiTapLon\Views\Shared\_LayoutHome.cshtml` doc ten/icon tu `StoreLocations` cho title/favicon.
  - `BaiTapLon\Controllers\HomeController.cs` truyen `StoreInfo` vao footer.
  - `BaiTapLon\Views\Shared\Footer.cshtml` dung logo, dia chi, email, so dien thoai va copyright theo cau hinh DB.
- Luu cac view tieng Viet vua sua bang UTF-8 BOM:
  - `Views\AboutUs\Index.cshtml`
  - `Areas\Admin\Views\WebManager\StoreLocation.cshtml`
  - `Views\Shared\_LayoutHome.cshtml`
  - `Views\Shared\Footer.cshtml`

### Xac minh
- Chay migration store local thanh cong:
  - `sqlcmd -S "(localdb)\MSSQLLocalDB" -d "QLNhaSach" -i "sql\migrations\20260508_add_stores.sql"`
- Build solution bang Visual Studio MSBuild thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`
- Goi thu localhost:
  - `http://localhost:56919/gioi-thieu/`: HTTP 200, co chu `Giới thiệu`, khong thay chu mojibake trong HTML tra ve.
  - `http://localhost:56919/Admin/LogsAdmin/FaceAuth`: HTTP 200, khong con `Server Error`/`NormalizeToExclusive`.
  - `http://localhost:56919/Admin/LogsAdmin/Geofence`: HTTP 200, khong con `Server Error`/`NormalizeToExclusive`.
- Quet lai cac file vua sua:
  - Khong con mau mojibake `Giá»`, `NhÃ`, `â€œ`, `á»`.
  - Khong con goi `NormalizeToExclusive` truc tiep trong `Where`.

### Luu y
- Tim kiem map dung dich vu cong khai Nominatim tu trinh duyet. Neu may offline hoac bi chan internet, admin van co the nhap tay dia chi/toa do va map iframe van cap nhat theo toa do.

## 2026-05-09 - Version4: yeu thich, StoreLocation HTML va challenge guong mat

### Da hoan thanh
- Tao `upgrade_plan.md_version4.md` dua tren version3, gom 3 viec chinh:
  - Sua loi khong them duoc sach vao yeu thich.
  - Sua loi `A potentially dangerous Request.Form value` o `/Admin/WebManager/StoreLocation`.
  - Bo sung luong thao tac guong mat ngau nhien khi dang nhap va khi muon sach.
- Sua `BaiTapLon\Areas\Admin\Controllers\WebManagerController.cs`:
  - Them `[ValidateInput(false)]` cho POST `StoreLocation` de nhan HTML tu CKEditor trong `WelcomeMessage`, `AboutContent`, `MissionContent`.
- Them bang va EF cho yeu thich:
  - `sql\migrations\20260509_add_product_favorites.sql`
  - `Mood\EF2\ProductFavorite.cs`
  - `Mood\Draw\ProductFavoriteDraw.cs`
  - `QuanLySachDBContext.ProductFavorites`
- Them luong yeu thich phia user:
  - `UsersController.ToggleFavorite(productId)` de them/bo yeu thich bang AJAX.
  - `UsersController.Favorites(id)` va route `/yeu-thich-{id}`.
  - View `BaiTapLon\Views\Users\Favorites.cshtml`.
  - Script `BaiTapLon\Scripts\FavoriteBooks.js`.
  - Nut yeu thich tren trang chi tiet sach goi endpoint moi.
  - Nut trai tim tren trang danh sach san pham va trang tim kiem cung goi endpoint moi.
  - Link yeu thich trong dashboard va menu tai khoan tro ve `/yeu-thich-{userId}`.
- Bo sung challenge guong mat:
  - `FaceAuthController.CreateChallenge(purpose)` sinh token va yeu cau ngau nhien.
  - `AuthenticateFaceLogin` va `VerifyRentalFace` bat buoc co challenge token hop le, dung purpose va chua het han.
  - UI dang nhap bang guong mat va UI muon sach hien yeu cau thao tac truoc khi chup/gui anh.

### Xac minh
- Da chay migration local:
  - `sqlcmd -S "(localdb)\MSSQLLocalDB" -d "QLNhaSach" -i "sql\migrations\20260509_add_product_favorites.sql"`
- Da kiem tra DB local:
  - Bang `ProductFavorites` ton tai.
  - Bang hien co 0 dong luc moi tao.
- Build solution thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`

### Luu y test thu cong
- Hai lenh curl thu `http://localhost:56919/Admin/WebManager/StoreLocation` va trang chi tiet sach bi timeout trong phien nay, co the do IIS Express/localhost dang treo hoac server khong phan hoi dung luc test.
- Can mo lai browser va test:
  - Luu StoreLocation voi noi dung CKEditor co the `<p>...</p>`.
  - Dang nhap user, vao chi tiet sach, bam `Them vao yeu thich`, sau do mo `/yeu-thich-{userId}`.
  - Dang nhap bang guong mat va muon sach: man hinh phai hien mot yeu cau ngau nhien truoc khi bam nhan dien.

## 2026-05-09 - Version4: tu xac thuc guong mat sau khi thuc hien challenge

### Da hoan thanh
- Cap nhat `upgrade_plan.md_version4.md` them yeu cau:
  - Sau khi camera san sang, UI tu cho nguoi dung thuc hien thao tac trong vai giay roi tu chup/gui xac thuc.
  - Nut nhan dien chi giu lai lam fallback thu cong.
- Cap nhat `BaiTapLon\Views\Users\Login.cshtml`:
  - Dang nhap bang guong mat tu tao challenge, mo camera, doi khoang ngan de nguoi dung lam dong tac, sau do tu chup/gui xac thuc.
  - Neu xac thuc that bai, token cu bi huy va UI tu tao challenge moi de thu lai.
- Cap nhat `BaiTapLon\Views\Product\Detail.cshtml`:
  - Luong muon sach bang guong mat cung tu tao challenge, tu chup/gui xac thuc sau khi camera san sang.
  - Neu xac thuc khuon mat that bai, UI tao challenge moi va tu thu lai.

### Xac minh
- Build solution thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`

### Luu y test thu cong
- Can test tren browser co camera:
  - Dang nhap bang guong mat: nhap username, bam mo dang nhap guong mat, lam theo yeu cau, he thong tu xac thuc khong can bam nut.
  - Muon sach: sau khi nhap so ngay muon va xac nhan, lam theo yeu cau guong mat, he thong tu xac thuc va gui yeu cau muon.

## 2026-05-09 - Version4: action-check realtime cho challenge guong mat

### Da hoan thanh
- Cap nhat `upgrade_plan.md_version4.md` theo huong flow tu nhan dien hanh dong:
  - Quay trai/phai.
  - Ha mieng.
  - Cuoi.
  - Nhin len/xuong.
  - Client webcam gui frame, Face API kiem tra dung hanh dong truoc khi cho xac thuc cuoi.
- Cap nhat contract `FACE_AUTH_FLASK_API_REQUIREMENTS.md`:
  - Them endpoint `POST /api/face/action-check`.
  - Them field request `actionCode`/`action_code`.
  - Them response `actionMatched`/`action_matched`, `actionCode`, `actionMessage`.
  - Ghi chu huong tich hop OpenCVSharp + MediaPipe Face Mesh hoac Python OpenCV + MediaPipe.
- Cap nhat `BaiTapLon\Services\FaceAuthApiClient.cs`:
  - Them `CheckActionAsync(...)`.
  - Gui `actionCode` va `action_code` sang Face API.
  - Map response `actionMatched`, `actionCode`, `actionMessage`.
- Cap nhat `BaiTapLon\Services\FaceAuthResponse.cs`:
  - Them `ActionMatched`, `ActionCode`, `ActionMessage`.
- Cap nhat `BaiTapLon\Controllers\FaceAuthController.cs`:
  - Challenge random gio dung action code: `turn_left`, `turn_right`, `mouth_open`, `smile`, `look_up`, `look_down`.
  - Them `CheckChallengeAction(purpose, challengeToken, userName)` de nhan frame tu browser, goi `/api/face/action-check`.
  - Challenge chi duoc dung cho login/rental khi action da pass.
  - `ValidateFaceChallenge` se tu choi token neu chua qua action-check.
- Cap nhat `BaiTapLon\Views\Users\Login.cshtml`:
  - Sau khi mo camera, client tu chup frame lap lai va goi `/FaceAuth/CheckChallengeAction`.
  - Khi `actionMatched=true`, moi tu goi `/FaceAuth/AuthenticateFaceLogin`.
  - Nut nhan dien chi con dung de thu lai action-check neu auto loop chua bat duoc hanh dong.
- Cap nhat `BaiTapLon\Views\Product\Detail.cshtml`:
  - Luong muon sach cung tu gui frame check action truoc.
  - Khi action pass moi goi `/FaceAuth/VerifyRentalFace`, sau do tao yeu cau muon.

### Xac minh
- Build solution thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`

### Luu y
- Can cap nhat Face API thuc te de ho tro `/api/face/action-check`; neu API chua co endpoint nay thi UI se khong pass challenge va se khong cho xac thuc cuoi.

## 2026-05-09 - Update version4: hien thuc Flask action-check nhan dien hanh dong

- Them `face_auth_api/app.py`: Flask API mau chay tai `localhost:8000/api/face`, co cac endpoint `health`, `register`, `verify`, `authenticate`, `action-check`.
- `/api/face/action-check` dung MediaPipe Face Mesh/MediaPipe Tasks Face Landmarker + OpenCV `solvePnP` de detect `turn_left`, `turn_right`, `look_up`, `look_down`, `mouth_open`, `smile`.
- Response action-check co `detected_action`, `metrics`, `action_message` de debug khi frame chua khop hanh dong.
- Them `face_auth_api/requirements.txt` de cai Flask/OpenCV/MediaPipe/NumPy.
- Them model `face_auth_api/models/face_landmarker.task` va backend tuong thich MediaPipe 0.10.35/Python 3.14.
- Cap nhat `FACE_AUTH_FLASK_API_REQUIREMENTS.md`: bo sung muc 8.1 ve nguong nhan dien hanh dong, cach chay Flask, va bien `FACE_ACTION_FLIP_HORIZONTAL` neu trai/phai bi nguoc do mirror camera.
- Cap nhat `upgrade_plan.md_version4.md`: them ke hoach hien thuc Flask action-check va checklist test `health`/frame webcam.
- Da cai dependency bang `python -m pip install --user -r face_auth_api\requirements.txt`.
- Da thay process Python cu tren port 8000 vi endpoint `/api/face/action-check` cu tra 404.
- Da chay Flask API v4 va kiem tra:
  - `GET /api/face/health` tra `model_loaded=true`, `landmark_backend=tasks.face_landmarker`, `version=1.0.0-v4`.
  - `POST /api/face/action-check` khong gui file tra JSON loi `ACTION_CODE_MISSING`, xac nhan endpoint da ton tai va response JSON hop le.

## 2026-05-09 - Chuyen luong Face API sang server xu ly anh rieng

- Xac nhan `QLNhaSach` chi truyen input/frame qua `FaceAuthAPI`; server xu ly anh thuc te la `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`.
- Cap nhat `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`:
  - Giu InsightFace cho `register`, `verify`, `authenticate`.
  - Them MediaPipe Tasks Face Landmarker cho `/api/face/action-check`.
  - Them debug response `detected_action`, `metrics`, `action_landmark_backend`.
  - Sua logic trai/phai/len/xuong theo yaw/pitch va co `FACE_ACTION_FLIP_HORIZONTAL` neu camera bi mirror.
- Them `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\models\face_landmarker.task`.
- Cap nhat `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\requirements.txt` them `mediapipe`.
- Dung process Flask mau trong `QLNhaSach\face_auth_api` tren port 8000 va restart server dich `NHANDIENKHUONMAT-new07040226\app.py`.
- Da test:
  - `python -m py_compile app.py` tren server dich thanh cong.
  - Import `app.py` va load `get_face_landmarker()` thanh cong voi backend `tasks.face_landmarker`.
  - `GET /api/face/health` tren port 8000 tra `action_model_loaded=true`, `action_landmark_backend=tasks.face_landmarker`, `version=1.1.0-action-check`.
  - `POST /api/face/action-check` khong gui file tra JSON `FILE_REQUIRED`, xac nhan route da ton tai tren server dich.

## 2026-05-09 - Update popup xac thuc muon sach

- Cap nhat `BaiTapLon\Views\Product\Detail.cshtml`:
  - Sau khi `/FaceAuth/VerifyRentalFace` thanh cong, popup xac thuc khuon mat se dong ngay va camera dung.
  - Trang chinh doi trang thai sang `Da xac thuc khuon mat. Dang gui yeu cau muon sach...`.
  - Khi `/Rental/RequestRental` thanh cong, nut `Muon sach` bi khoa va doi thanh `Dang cho duyet`.
  - Neu gui yeu cau muon that bai sau khi face da pass, trang thai quay lai cho phep thu lai va hien loi ro rang.
- Kiem tra tren browser co camera voi tung action: quay trai, quay phai, ha mieng, cuoi, nhin len, nhin xuong.

## 2026-05-09 - Tao ke hoach Version5

### Da hoan thanh
- Tao `upgrade_plan.md_version5.md` dua tren version4 va cac yeu cau moi.
- Bo sung cac hang muc version5:
  - Tat ca thong tin nha sach nhu icon, ten, banner, dia chi, email, phone, toa do/geofence phai lay tu `/Admin/WebManager/StoreLocation`, khong gan cung trong code.
  - Sua/xac minh cac trang `/Admin/LogsAdmin/Rental`, `/Admin/LogsAdmin/FaceAuth`, `/Admin/LogsAdmin/Geofence` chua hien du lieu.
  - Bo sung thong ke chu de muon tra sach co bieu do lien quan.
  - Cho admin dang nhap tu trang client va dieu huong theo vai tro, khong bat vao trang dang nhap admin rieng.
  - Them ke hoach Gmail API de thong bao trang thai muon sach/tre han qua email.
- Ghi ro luu y bao mat Gmail API: khong commit client secret/refresh token vao source; cau hinh qua moi truong/Web.config transform/bang cau hinh an toan.

### Viec tiep theo
- Bat dau trien khai theo thu tu trong `upgrade_plan.md_version5.md`.
- Neu thuc hien Gmail API, can dang nhap Google Cloud Console bang tai khoan co quyen project va lay OAuth secret/refresh token ngoai source code.

## 2026-05-09 - Version5 buoc 1: dong bo cau hinh nha sach

### Da hoan thanh
- Them `BaiTapLon\Services\StoreLocationService.cs` de lay nha sach active tu `StoreLocations` theo quy tac chung, co fallback an toan khi DB chua co cau hinh.
- Include service moi vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Cap nhat `AboutUsController` dung `StoreLocationService`, xoa fallback hard-code/loi font trong controller.
- Cap nhat `HomeController.Header` va `HomeController.Footer` truyen `StoreInfo` tu service.
- Cap nhat `_LayoutHome.cshtml`, `Header.cshtml`, `Footer.cshtml` tiep tuc hien ten/logo/icon theo StoreLocation active.
- Cap nhat `WebManagerController` dung fallback mac dinh tu service khi tao cau hinh nha sach moi.
- Cap nhat `GeofenceController` lay cua hang active qua service, khong phu thuoc vi tri gan cung trong controller.
- Cap nhat trang lien he lay ten, dia chi, email, phone va map tu StoreLocation active.
- Cap nhat thong bao mượn sách ở `Product\Detail.cshtml` dùng `storeName` trả về từ geofence thay vì gắn cứng tên nhà sách.

### Viec tiep theo
- Sua/xac minh 3 trang log admin chua len du lieu va them thong tin debug bo loc/tong ban ghi.

## 2026-05-09 - Version5 buoc 2: sua/xac minh log admin

### Da hoan thanh
- Cap nhat `Common\Repositories\LogRepository.cs` them `GetRuntimeDatabaseInfo()` de hien datasource/database runtime cua `LogDbContext`.
- Cap nhat `LogsAdminController` cho 3 trang:
  - `/Admin/LogsAdmin/FaceAuth`
  - `/Admin/LogsAdmin/Geofence`
  - `/Admin/LogsAdmin/Rental`
- Moi trang log nay truyen them:
  - `RuntimeDatabase`: DB IIS Express/runtime dang doc log.
  - `AllCount`: tong so ban ghi khong loc trong bang log tuong ung.
- Cap nhat 3 view log admin hien alert debug nhe: DB runtime, tong tat ca va tong theo bo loc.
- Muc tieu: neu trang van khong co du lieu, admin co the nhin ngay runtime dang doc sai database hay bo loc dang lam rong ket qua.

### Viec tiep theo
- Them thong ke chu de muon tra sach co bieu do trong khu admin.

## 2026-05-09 - Version5 buoc 3: thong ke chu de muon tra sach

### Da hoan thanh
- Cap nhat `Areas\Admin\Controllers\ThongKeController.cs`:
  - Them action `/Admin/ThongKe/MuonTraChuDe`.
  - Join `RentalRequests` voi `Sanpham` va `Category`.
  - Ho tro loc `fromDate`, `toDate`, `status`.
  - Tinh tong luot muon, so luong sach, cho duyet, dang muon, da tra, qua han va ty le qua han theo chu de.
  - Tinh xu huong muon sach theo ngay.
- Them view `Areas\Admin\Views\ThongKe\MuonTraChuDe.cshtml`:
  - Bang thong ke theo chu de.
  - Bieu do cot so luot muon theo chu de.
  - Bieu do donut ty le trang thai.
  - Bieu do duong xu huong muon theo ngay.
  - Dung Chart.js local san co tai `Content\Client\vendor\chart.js\Chart.min.js`.
- Them link `Mượn trả theo chủ đề` vao menu thong ke admin.
- Include view moi vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.

### Viec tiep theo
- Dong bo dang nhap client cho tai khoan admin: sau khi dang nhap thanh cong se set `ADMIN_SESSION` va dieu huong vao admin.

## 2026-05-09 - Version5 buoc 4: admin dang nhap tu trang client

### Da hoan thanh
- Cap nhat `UsersController.Login`:
  - Khi dang nhap thanh cong va `IDQuyen == 1`, he thong set ca `USER_SESSION` va `ADMIN_SESSION`.
  - `ADMIN_SESSION` dung dung model `AdminLogin` ma `BaseController` khu admin dang kiem tra.
  - Tra ma `10` cho client de phan biet dang nhap quan tri thanh cong.
- Cap nhat `Content\libs\commonjs\loginCommon.js`:
  - Form dang nhap desktop/mobile xu ly ma `10`.
  - Dieu huong admin ve `/Admin/Homes/Index` sau khi dang nhap tu trang client.
- Tai khoan user thuong van giu luong cu ve trang chu; tai khoan bi khoa/sai mat khau/khong ton tai van theo ma loi cu.

### Viec tiep theo
- Them Gmail notification service va noi vao rental workflow de thong bao trang thai muon sach/tre han.

## 2026-05-09 - Version5 buoc 5: Gmail API notification cho muon sach

### Da hoan thanh
- Them `BaiTapLon\Services\GmailNotificationService.cs`:
  - Doc cau hinh `GmailNotificationsEnabled`, `GmailClientId`, `GmailClientSecret`, `GmailRefreshToken`, `GmailSenderEmail`, `GmailSenderName`.
  - Dung OAuth refresh token de lay access token tu Google.
  - Goi Gmail API `users.me.messages.send`.
  - Tao MIME UTF-8 cho email HTML tieng Viet/khong dau an toan compile.
  - Ghi `RentalLog` khi gui/thieu cau hinh/loi gui mail.
- Cap nhat `BaiTapLon\Web.config` them appSettings placeholder Gmail, mac dinh `GmailNotificationsEnabled=false` de khong gui mail khi chua cau hinh secret.
- Include service moi vao `BaiTapLon\DongTrieuBookStoreOnline.csproj`.
- Noi notification vao `RentalController`:
  - Sau khi tao yeu cau muon: gui event `Request`.
  - Sau khi user huy yeu cau: gui event `Cancel`.
  - Sau khi admin cap nhat trang thai: gui event theo action `Approve/Borrow/Reject/Return/Overdue`.
- Cap nhat `RentalAdminController` them action `SendOverdueReminders`:
  - Quet rental qua han chua tra/chua huy/chua bi tu choi.
  - Khong gui lap lai neu da co log `EmailOverdueReminder` trong ngay.
- Cap nhat `Areas\Admin\Views\RentalAdmin\Index.cshtml` them nut `Gửi email nhắc quá hạn`.

### Luu y cau hinh
- Chua dua secret that vao source. Can lay OAuth client/refresh token tu Google Cloud Console va dien qua cau hinh local/IIS truoc khi bat `GmailNotificationsEnabled=true`.

### Viec tiep theo
- Build solution va sua loi compile neu co.

## 2026-05-09 - Version5 xac minh build

### Da hoan thanh
- Build solution bang Visual Studio MSBuild thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`
  - Ket qua tao `BaiTapLon\bin\BaiTapLon.dll`.
- Quet lai cac chuoi hard-code nha sach chinh:
  - Khong con ten `Nhà sách Tân Hạnh`, email `dongtrieubookstore@gmail.com`, `Cơ Sở Đông Triều` trong controller/view chinh.
  - Chi con fallback icon/logo mac dinh `/assets/img/imgbook/anhlogo.jpg` khi DB chua co `IconPath`.

### Luu y can test thu cong
- Mo `/Admin/WebManager/StoreLocation`, sua ten/icon/banner/dia chi/email/phone/toa do va kiem tra client hien theo DB.
- Mo `/Admin/LogsAdmin/FaceAuth`, `/Admin/LogsAdmin/Geofence`, `/Admin/LogsAdmin/Rental`; neu trang rong, xem dong `DB runtime` va `Tổng tất cả` tren dau trang.
- Mo `/Admin/ThongKe/MuonTraChuDe` de xem bang/bieu do thong ke.
- Dang nhap tai trang client bang tai khoan admin, xac nhan duoc dieu huong vao `/Admin/Homes/Index`.
- Dien Gmail OAuth secret/refresh token ngoai source, bat `GmailNotificationsEnabled=true`, sau do test tao/duyet/tra/qua han rental va nut gui email nhac qua han.

## 2026-05-09 - Version4 update CMND/CCCD, OCR va Gmail duyet muon

### Da hoan thanh
- Sua loi font chu tai `BaiTapLon\Areas\Admin\Views\ThongKe\MuonTraChuDe.cshtml`.
- Bo sung thong tin CMND/CCCD khong bat buoc khi dang ky va cap nhat ho so nguoi dung.
- Khi gui yeu cau muon sach, bat buoc nhap so CMND/CCCD, ho ten tren giay to va dinh kem anh CMND/CCCD.
- Luu snapshot CMND/CCCD vao `RentalRequests`; man hinh admin quan ly muon sach hien so giay to, link anh giay to va diem khop khuon mat neu co.
- Them route MVC `/FaceAuth/OcrCmnd` va route Flask `/api/face/ocr-cmnd`, `/api/face/qcr-cmnd`, `/api/face/cmnd-ocr` de OCR CMND/CCCD va so khop khuon mat tren giay to voi face profile da dang ky.
- Khong thay doi cac route nhan dien khuon mat hien co; chi dung lai descriptor/profile de doi chieu CMND/CCCD.
- Cap nhat Gmail event `ApproveSuccess` de gui thong bao "Muon sach thanh cong" khi admin duyet, dung OAuth Gmail hien tai tu `Web.config`.
- Them `IdentityCardStoragePath`, migration `sql\migrations\20260509_add_identity_card_rental_flow.sql`, va dependency Flask `pytesseract`.

### Luu y
- Khong the tu lay secret tu Google Cloud Console neu khong co phien dang nhap/quyen truy cap. Cac key Gmail hien tai trong `Web.config` dang trong va `GmailNotificationsEnabled=false`, nen can dien `GmailClientId`, `GmailClientSecret`, `GmailRefreshToken`, `GmailSenderEmail` roi bat enabled de gui mail that.
- Flask OCR can cai Tesseract OCR binary tren may chay service; `pytesseract` chi la wrapper Python.

## 2026-05-09 - Version5 ho so Gmail va CMND/CCCD truoc khi muon sach

### Da hoan thanh
- Tao file ke hoach `upgrade_plan.md_version5.md` dua tren version 4.
- Them cot `NotificationEmail` vao bang `User`, migration `sql\migrations\20260509_add_notification_email_version5.sql`.
- Ap migration vao LocalDB `QLNhaSach`, xac nhan cot `NotificationEmail` da ton tai.
- Dang ky tai khoan:
  - Them truong Gmail nhan thong bao muon/tra/qua han.
  - Them nut chon anh CMND/CCCD de OCR nhap du lieu CMND/CCCD khong bat buoc.
  - Them route `/FaceAuth/OcrCmndDraft` cho OCR nhap, khong yeu cau dang nhap va khong luu vao ho so.
- Ho so khach hang:
  - Hien Gmail nhan thong bao.
  - Hien thong tin CMND/CCCD, link anh CMND/CCCD neu co, va diem khop khuon mat neu co.
- Luong muon sach:
  - Khi bam `Muon sach`, client goi `/Rental/RentalProfileStatus`.
  - Neu thieu Gmail nhan thong bao, CMND/CCCD hoac anh CMND/CCCD thi hien popup cap nhat.
  - Popup cho nhap Gmail, CMND/CCCD, tai anh CMND/CCCD va OCR qua `/FaceAuth/OcrCmnd`.
  - Server luu qua `/Rental/UpdateRentalProfile` va so khop khuon mat CMND/CCCD voi face profile truoc khi cho tiep tuc.
- Gmail thong bao:
  - `GmailNotificationService` uu tien gui den `NotificationEmail`, neu trong thi fallback ve `Email`.

### Xac minh
- `python -m py_compile D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`: thanh cong.
- Build solution bang Visual Studio MSBuild thanh cong:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`
- SQL verify:
  - `COL_LENGTH('dbo.[User]','NotificationEmail') = 500`.

### Luu y can test thu cong
- Dang ky tai khoan moi, chon anh CMND/CCCD de OCR, kiem tra du lieu duoc fill va van co the bo qua buoc nay.
- Dung tai khoan chua co CMND/CCCD/Gmail thong bao bam `Muon sach`, kiem tra popup cap nhat hien dung.
- Tai khoan da co ho so day du bam `Muon sach`, kiem tra di tiep den buoc ngay muon va xac thuc khuon mat.
## 2026-05-10 - Bo sung yeu thich theo tai khoan, CMND tuy chon va dang ky 3 buoc

- Cap nhat `BaiTapLon\Controllers\UsersController.cs`: truyen ten tai khoan/username sang man hinh sach yeu thich.
- Viet lai `BaiTapLon\Views\Users\Favorites.cshtml`: hien ten tung tai khoan dang dang nhap, username, trang thai dang nhap va thong bao khi chua dang nhap.
- Cap nhat `BaiTapLon\Views\Users\Login.cshtml` va `BaiTapLon\Content\libs\commonjs\loginCommon.js`:
  - Tach dang ky thanh 3 buoc: thong tin chung -> CMND/CCCD khong bat buoc -> xac thuc khuon mat/hoan tat.
  - Doc CMND/CCCD chi de tu dien; neu OCR loi thieu Tesseract thi nguoi dung van co the nhap tay va tiep tuc.
- Cap nhat `BaiTapLon\Controllers\RentalController.cs` va `BaiTapLon\Views\Product\Detail.cshtml`:
  - Popup bo sung ho so khi muon sach chi bat buoc Gmail, so CMND/CCCD va ho ten.
  - Anh CMND/CCCD/OCR/face-match la tuy chon, khong con chan luong muon sach khi may chu chua cai Tesseract.
  - Snapshot CMND/CCCD trong `RentalRequests` tiep tuc lay tu thong tin tai khoan da luu.
- Cap nhat `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`: `health.ocr_available` kiem tra binary Tesseract thuc te bang `pytesseract.get_tesseract_version()`, version API thanh `1.2.1-action-check-ocr-optional`.
- Cap nhat `upgrade_plan.md_version4.md` voi dieu chinh CMND tuy chon, popup muon sach va luong dang ky 3 buoc.

## 2026-05-10 - Nang cap OCR CMND/CCCD bang PaddleOCR

- Kiem tra nguon OCR GitHub:
  - PaddleOCR: `https://github.com/PaddlePaddle/PaddleOCR`, ho tro OCR da ngon ngu/100+ ngon ngu, phu hop lam backend uu tien cho CMND/CCCD.
  - VietOCR: `https://github.com/ADTC/VietOCR`, la frontend cho Tesseract nen van phu thuoc binary Tesseract.
- Cap nhat `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`:
  - Them import optional `PaddleOCR` va cache instance `get_paddle_ocr()`.
  - Them `CMND_OCR_BACKEND=auto|paddle|tesseract`, mac dinh `auto`: thu PaddleOCR truoc, fallback Tesseract.
  - Them parser OCR moi: bo dau de bat label tieng Viet, tach so CMND/CCCD 9/12 so, ho ten, ngay sinh, dia chi, ngay cap, noi cap.
  - Chuan hoa ngay sinh/ngay cap sang `yyyy-MM-dd` de input date trong QLNhaSach fill duoc.
  - `/api/face/ocr-cmnd` tra them `ocr_backend`/`ocrBackend`; `/api/face/health` tra `ocr_backend`, `paddleocr_available`, `tesseract_available`, version `1.3.0-action-check-paddleocr-cmnd`.
- Cap nhat `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\requirements.txt`: them `paddleocr>=2.7.0`.
- Them `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\OCR_BACKENDS.md` luu link GitHub va cach cau hinh backend OCR.
- Cap nhat `BaiTapLon\Content\libs\commonjs\loginCommon.js` va `userProfileCommon.js`: chuan hoa ngay OCR `dd/mm/yyyy`, `dd-mm-yyyy`, `dd.mm.yyyy` ve `yyyy-MM-dd` truoc khi fill text/date vao form.
- Cap nhat `upgrade_plan.md_version4.md` muc 5.2 theo ke hoach OCR PaddleOCR.
- Kiem tra nhanh moi truong Python hien tai: `pytesseract=True`, `paddleocr=False`; PaddleOCR da duoc them vao requirements va backend se tu kich hoat sau khi cai dependency.

## 2026-05-10 - Dong bo CMND/CCCD mat truoc/mat sau va sua luong dang ky/muon sach

- Doc lai lien ket API: `BaiTapLon\Web.config` dang tro `FaceAuthAPI=http://localhost:8000/api/face`; Flask dich `NHANDIENKHUONMAT-new07040226\app.py` da nhan `front_file/back_file` tai `/api/face/ocr-cmnd`.
- Cap nhat `BaiTapLon\Services\FaceAuthApiClient.cs`: them ham OCR CMND/CCCD gui rieng `front_file` va `back_file`, giu ham cu cho luong mot file.
- Cap nhat `FaceAuthController.OcrCmndDraft/OcrCmnd`: nhan file mat truoc/mat sau, luu rieng duong dan, map them `place_of_birth`, `gender`, `nationality`, `expiry_date`, `issuing_authority`, `mrz`.
- Cap nhat `RentalController.UpdateRentalProfile`: popup cap nhat nhanh khi muon sach luu duoc ca khi nhap tay, va neu co anh thi OCR/lap day thong tin, luu mat truoc/mat sau vao `User`.
- Cap nhat snapshot `RentalRequests`: luu them anh mat truoc/mat sau va cac field lien quan CMND/CCCD tu ho so tai khoan tai thoi diem gui yeu cau muon.
- Cap nhat entity/model/UI: `User`, `RentalRequest`, `RegisterModel`, `UsersController`, `ProfileUser`, `Login`, `Detail`, `loginCommon.js`, `userProfileCommon.js`.
- Sua loi client dang ky khuon mat: chi coi thanh cong khi response `success === true`, tranh loi response rong/khac format lam UI di tiep sai.
- Cap nhat `sql\migrations\20260509_add_identity_card_rental_flow.sql` va da ap vao LocalDB `QLNhaSach`.
- SQL verify: `COL_LENGTH` cho `IdentityCardFrontImagePath`/`IdentityCardBackImagePath` tren `dbo.[User]` va `dbo.RentalRequests` deu tra `1000`.
- Kiem tra Flask: `python -m py_compile app.py` thanh cong; `D:\APython\python.exe -c "import app; ..."` tra `app` va OCR available `True`.
- Goi `curl.exe http://localhost:8000/api/face/health`: `status=ok`, `model_loaded=true`, `ocr_available=true`, `ocr_backend=tesseract`, version `1.3.0-action-check-paddleocr-cmnd`.
- Build ASP.NET chua hoan tat do may hien tai thieu `Microsoft.WebApplication.targets`/Visual Studio Web targets; `dotnet build` va MSBuild .NET Framework deu dung o loi moi truong nay, khong vao loi code moi.
- Cap nhat `upgrade_plan.md_version4.md` muc 5.3.

## 2026-05-10 - Sua loi UploadIdentityCard undefined

- Nguyen nhan: `ProfileUser.cshtml` goi inline `onclick="UploadIdentityCard()"`, trong khi `userProfileCommon.js` khai bao ham bang bien cuc bo/kha nang khong nam tren `window` khi browser chay script.
- Cap nhat `BaiTapLon\Content\libs\commonjs\userProfileCommon.js`: gan `ChangeUserProfile`, `ChangePass`, `UploadIdentityCard` vao `window`.
- Cap nhat `BaiTapLon\Views\Users\ProfileUser.cshtml`: them query version cho script `userProfileCommon.js?v=20260510-cmnd-global` de tranh cache JS cu.
- Xac minh bang `Select-String`: da co `window.UploadIdentityCard`, `window.ChangeUserProfile`, `window.ChangePass`; view van load script va onclick dung.

## 2026-05-10 - Chuyen sua Flask OCR ve dung dich NHANDIENKHUONMAT

- Xac nhan cac sua doi Flask phai nam tai `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`; thu muc `QLNhaSach\face_auth_api` chi la ban copy/phu, khong phai dich dang chay.
- Cap nhat Flask that: them alias `ocr_error` va `error` trong response `/api/face/ocr-cmnd` de MVC/JS hien dung loi OCR.
- Cap nhat health version Flask that thanh `1.3.1-action-check-paddleocr-cmnd-mvc-response`.
- Giu phia QLNhaSach la ben goi API: UI ho so/dang ky va timeout `FaceAuthTimeoutSeconds=60` tiep tuc nam trong MVC.

## 2026-05-10 - Ho so CMND 2 mat, Gmail duy nhat va khoa du lieu OCR

- Cap nhat `upgrade_plan.md_version4.md` them muc 5.4: Gmail duy nhat, preview CMND 2 mat, loading OCR, khoa truong sau khi OCR va lien ket sach yeu thich.
- Cap nhat dang ky/ho so chi hien mot truong `NotificationEmail`; server dong bo `Email = NotificationEmail` de giu tuong thich cac luong cu.
- Cap nhat `ProfileUser.cshtml`: them link `Sách yêu thích`, hien mac dinh 2 o anh CMND/CCCD mat truoc/mat sau, bam vao o de chon anh va preview.
- Cap nhat `Login.cshtml` va `loginCommon.js`: dang ky mobile/desktop dung mot Gmail bat buoc, preview anh CMND 2 mat, loading khi OCR, thong bao thanh cong/that bai, fill ho ten tai khoan tu ho ten tren giay to va khoa cac truong da OCR bang `readonly`.
- Cap nhat `userProfileCommon.js`: OCR ho so co loading, khoa nut khi dang xu ly, fill `Name` theo `IdentityFullName`, va khoa cac truong CMND/ho ten sau khi doc thanh cong.
- Cap nhat `FaceAuthController.OcrCmnd`: khi OCR doc duoc `full_name`, dong bo ve `User.Name` tren server.
- Doi nhan menu trong cac trang tai khoan thanh `Sách yêu thích` de nguoi dung vao lai danh sach sach da luu.
- Xac minh:
  - `python -m py_compile D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`: thanh cong.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.
## 2026-05-10 - Sua rule OCR CMND/CCCD sai mat

- Kiem tra lai nguyen nhan anh khong phai CMND/CCCD van duoc chap nhan: OCR vung crop co dinh co the tao ra field gia, lam `has_fields=true`.
- Cap nhat Flask Face API de yeu cau bang chung giay to (`identity_card_evidence`) truoc khi chap nhan OCR.
- MRZ duoc xem la dau hieu mat sau; neu upload vao o mat truoc thi tra loi sai mat truoc, neu mat truoc dua vao o mat sau thi tra loi sai mat sau.
- Anh khong co tu khoa/neo CMND/CCCD hoac bo field du manh se tra `IDENTITY_CARD_INVALID` thay vi `success=true`.
- Da restart Face API tren port 8000 va test bang anh bia sach `book1.jpg`: API tra `IDENTITY_CARD_INVALID` dung mong doi.

## 2026-05-10 - Version 4 bo sung khoa CMND/CCCD va OCR

- Cap nhat `upgrade_plan.md_version4.md` muc 5.5 theo yeu cau test moi.
- Trang chi tiet sach chi cho sua `So ngay muon`; so CMND/CCCD va ho ten trong panel muon sach duoc lay tu ho so va de readonly.
- Sap xep lai trang thong tin ca nhan theo thu tu anh CMND/CCCD, doc thong tin, thong tin CMND/CCCD, so dien thoai, noi o, Gmail, luu thong tin.
- Khi ho so da co du anh CMND/CCCD hai mat, form thong tin ca nhan bi khoa va chi con cho cap nhat lai anh CMND/CCCD.
- MVC khong ghi ho so CMND/CCCD neu OCR tra loi that bai; popup cap nhat thong tin muon sach hien loi khi anh CMND/CCCD sai loai.
- Buoc dang ky OCR CMND/CCCD hien spinner dang xu ly va toastr thanh cong/that bai.

## 2026-05-10 - Ket noi chatbox Version 5 voi QLNhaSach

- Cap nhat `BaiTapLon\Web.config`: them `ChatboxWidgetUrl=http://localhost:8000/api/chatbox/widget.js` va `ChatboxEnabled=true`.
- Cap nhat `BaiTapLon\Views\Shared\_LayoutHome.cshtml`: nap widget chatbox ban hang tu Flask Face API o cuoi layout khach hang.
- Chatbox su dung module rieng tai `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\sales_chatbox`, da train tu database `QLNhaSach.dbo.Sanpham`.
- Khi dua len server chi can doi `ChatboxWidgetUrl` ve URL Flask that; neu can tat chatbox tam thoi dat `ChatboxEnabled=false`.
- Sua widget Flask de tu lay origin tu `document.currentScript.src`, tranh goi nham ve origin MVC khi script duoc nhung vao QLNhaSach.
- Restart Flask tren port 8000 tu thu muc `NHANDIENKHUONMAT-new07040226`.
- Xac minh:
  - `GET http://localhost:8000/api/chatbox/health`: `product_count=53`, `trained_at=2026-05-10 15:23:41`.
  - `GET http://localhost:8000/api/chatbox/widget.js`: tra ve script widget moi.
  - `POST http://localhost:8000/api/chatbox/ask`: tra loi duoc cau hoi `sach giao duc con hang khong`.
  - Build `DongTrieuBookStore.sln` bang MSBuild Visual Studio 2022 thanh cong.
## 2026-05-10 - Version 5: yêu thích local, review sách, video và đánh giá

- Bổ sung trang yêu thích cho khách chưa đăng nhập, lưu theo `localStorage` trên từng trình duyệt/máy.
- Bổ sung upload file review sách và link YouTube trong quản lý sách của admin.
- Bổ sung popup xem file review ở trang chi tiết sách; nếu chưa có file, nút hiển thị trạng thái chưa xem được review.
- Bổ sung tab video YouTube theo từng sản phẩm và form khách hàng đăng nhập đánh giá/bình luận.
- Thêm migration `20260510_add_product_reviews_version5.sql`.

## 2026-05-10 - Trang quản lý sách yêu thích và sửa lỗi cập nhật file sách

- Cập nhật `BaiTapLon\Views\Users\Favorites.cshtml`: trang sách yêu thích của user đăng nhập chuyển sang bảng quản lý giống giỏ hàng, có ảnh/tên sách, giá, tình trạng còn/hết hàng, thêm vào giỏ và bỏ yêu thích theo từng dòng.
- Cập nhật `BaiTapLon\Scripts\FavoriteBooks.js`: khi bỏ yêu thích trong trang dạng bảng sẽ xóa đúng dòng sản phẩm; nút icon-only không bị đổi thành chữ.
- Sửa `BaiTapLon\Areas\Admin\Controllers\SanPhamController.cs`: sau khi admin chọn file review sách và bấm cập nhật, controller trả lại đúng model `Sanpham` cho view, tránh `System.NullReferenceException` khi view đọc `Model.ReviewFilePath`.
- Bổ sung kiểm tra sản phẩm không tồn tại ở màn hình sửa admin để chuyển về danh sách thay vì render view rỗng.
- Xác minh: build `DongTrieuBookStore.sln` bằng MSBuild Visual Studio 2022 thành công.

## 2026-05-10 - Hoan thien Version 5: yeu thich, admin/client, logs va Gmail

- Gan icon tim header client va mobile vao trang `yeu-thich`/`yeu-thich-{userId}`; cac nut yeu thich tren client chi con icon, khong chen chu vao nut icon.
- Cap nhat dang nhap admin: dung chung tai khoan voi client, sau khi login se check `IDQuyen` de vao `/Admin/Homes` hoac quay ve `/trang-chu`.
- Them nut `Trang khách hàng` tren layout admin de di nhanh tu admin ve client; khi admin dang o client, header hien nut quay ve `/Admin/Homes`.
- Them `ProductController.ReviewFile`: stream file review/demo voi header inline; trang chi tiet sach va admin mo file qua action nay de uu tien xem tren trinh duyet thay vi tai ve.
- Sua log FaceAuth: repository tu dua page ve trang hop le neu page vuot tong trang, tranh tong co du lieu nhung bang rong.
- Cap nhat log Rental: them timeline truc quan theo tung khach hang va tung ma muon sach.
- Viet lai `Admin/ThongKe/MuonTraChuDe` dung tieng Viet UTF-8 va sua nhan `Chưa phân loại`.
- Cap nhat `GmailNotificationService`: neu chua co Gmail OAuth token thi fallback SMTP Gmail da cau hinh; bat `GmailNotificationsEnabled=true` trong `Web.config`.
- Cap nhat `upgrade_plan.md_version5.md`.
- Xac minh: build `DongTrieuBookStore.sln` bang MSBuild Visual Studio 2022 thanh cong.

## 2026-05-10 - Sua font yeu thich/thong ke va preview file review

- Sua loi font tai `/yeu-thich-{userId}` va `/Admin/ThongKe/MuonTraChuDe` bang cach luu lai `Favorites.cshtml` va `MuonTraChuDe.cshtml` theo UTF-8 BOM; xac minh byte dau file la `EF BB BF`.
- Them `FONT_ENCODING_GUIDE.md`: ghi ro nguyen nhan UTF-8 khong BOM bi ASP.NET MVC .NET Framework/PowerShell cu doc nham thanh ANSI, dau hieu nhan biet va cach luu file de tranh tai dien.
- Them `ProductController.ReviewFilePreview` va `ReviewFileDownload`: tach logic xem file demo/review khoi logic tai file, ho tro preview PDF/anh/Markdown/TXT va de nut tai file rieng.
- Cap nhat popup chi tiet sach va link admin sang trang preview moi; bo hanh vi bam xem file ma trinh duyet lai tai truc tiep doi voi dinh dang khong ho tro inline.
- Bo sung file demo `BaiTapLon\Resource\ProductReviews\demo-review-sach.md` va khai bao trong `.csproj` de co san mau preview trong thu muc du an.
- Mo rong upload file review cho admin: ho tro them `.md` va `.txt` ben canh PDF/anh/Word.
- Da tham khao huong GitHub-style markdown viewer (`sindresorhus/github-markdown-css`) nhung giu ban noi bo nhe/offline de khong phu thuoc tai package/CDN.
- Xac minh:
  - `Format-Hex` hai view loi font: co BOM `EF BB BF`.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.

## 2026-05-10 - Sua preview file DOCX va an ten file

- Kiem tra loi `Trinh duyet khong xem truc tiep duoc dinh dang nay tren localhost`: nguyen nhan la file review dang la `.docx`, iframe/browser khong render truc tiep nhu PDF/anh.
- Cap nhat `ProductController.ReviewFilePreview`: them doc noi dung `.docx` bang `DocumentFormat.OpenXml` da co san trong project, render van ban trong trang preview noi bo.
- Cap nhat `ReviewFilePreview.cshtml`: bo hien ten file that tren toolbar/title, thay bang `Review sách`; bo nut `Mo raw`, them nut `Quay về`, giu nut `Tai file` cho truong hop can ban goc.
- Doi thong bao unsupported thanh thong bao he thong chua ho tro dinh dang do; cac dinh dang ho tro xem truc tiep hien tai: PDF, anh, Markdown/TXT va DOCX.
- Cap nhat admin `SanPham/Edit.cshtml`: link file hien tai chi hien `Xem file review hiện tại`, khong lo ten file upload.
- Luu cac view vua sua bang UTF-8 BOM de tranh loi font tieng Viet.
- Xac minh:
  - `Format-Hex Views\Product\ReviewFilePreview.cshtml`: co BOM `EF BB BF`.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.

## 2026-05-10 - Nang cap preview file sach theo dang PDF va sua update file

- Kiem tra DB `QLNhaSach.dbo.Sanpham`: cac cot `ReviewFilePath`, `ReviewFileName`, `YoutubeUrl` da ton tai nen loi cap nhat file khong do thieu migration.
- Sua `Mood\Draw\SanphamDraw.cs`: khong nuot exception khi update san pham; them `LastError` de controller hien dung ly do neu cap nhat DB that bai.
- Sua `BaiTapLon\Areas\Admin\Controllers\SanPhamController.cs`: neu update that bai se hien thong bao kem loi goc; gioi han ten file luu trong DB theo do dai cot de tranh loi truncate khi upload file co ten qua dai.
- Nang cap `ProductController.ReviewFilePreview`: voi file `.doc/.docx`, he thong thu chuyen sang PDF cache tai `Resource\ProductReviewPreviews` roi hien bang iframe PDF de giu tung trang nhu ban goc.
- Ho tro 2 converter:
  - LibreOffice headless qua appSetting `ReviewLibreOfficePath` hoac duong dan mac dinh `C:\Program Files\LibreOffice\program\soffice.exe`.
  - OfficeToPDF qua appSetting `ReviewOfficeToPdfPath` hoac file `bin\OfficeToPDF.exe`/`App_Data\Tools\OfficeToPDF.exe`.
- Neu chua co converter tren may, `.docx` van fallback doc text bang OpenXML va hien canh bao can cau hinh converter de giu nguyen trang nhu PDF.
- Them appSettings `ReviewLibreOfficePath`, `ReviewOfficeToPdfPath` vao `BaiTapLon\Web.config` va them folder cache `Resource\ProductReviewPreviews` vao `.csproj`.
- Tham khao repo:
  - `scivision/office-headless`: LibreOffice headless co the convert `.doc/.docx` sang PDF.
  - `cognidox/OfficeToPDF`: CLI convert Office sang PDF bang tinh nang export cua Microsoft Office.
  - `smartinmedia/Net-Core-DocX-HTML-To-PDF-Converter`: huong NuGet/DocX to PDF cho .NET Core, khong phu hop truc tiep voi MVC .NET Framework hien tai nen khong chen vao project.
- Xac minh:
  - May hien tai chua tim thay `soffice.exe`/`WINWORD.EXE`, nen can cai/cau hinh converter neu muon `.docx` render dung tung trang nhu PDF tren localhost.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.

## 2026-05-10 - Cau hinh Gmail app password va thong bao admin

- Cap nhat `BaiTapLon\Web.config`: doi `FromEmailPassword` sang ma app password Gmail `uwiw rhpu imtf jhcu` theo yeu cau.
- Cap nhat `CommomSentMail\MailHelper.cs`: tu bo khoang trang trong app password truoc khi dang nhap SMTP Gmail de tranh loi xac thuc.
- Cap nhat `GmailNotificationService`: them ket qua gui Gmail chi tiet, validate email khach hang truoc khi gui, log ro cac truong hop khong tim thay Gmail, Gmail khong hop le, Gmail tat cau hinh hoac gui that bai.
- Cap nhat luong admin duyet muon sach: duyet van thanh cong neu Gmail khach hang sai/khong gui duoc; thong bao admin hien ro `Duyet muon sach thanh cong. Khong gui duoc Gmail: ...`.
- Ap dung cung cach ghi log that bai cho thong bao nhac tre han/qua han bang action `EmailOverdueReminderFailed`.
- Xac minh:
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.
  - Thu muc hien tai khong co `.git`, nen lich su duoc luu vao `LichSu.md`.
  - `winget.exe` co alias tai `C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\winget.exe` nhung chay lenh cai LibreOffice bi Windows bao `The system cannot find the file specified`.
  - Chua tim thay `C:\Program Files\LibreOffice\program\soffice.exe` va chua co `BaiTapLon\App_Data\Tools\OfficeToPDF.exe`; de Word hien y het PDF tren localhost van can cai LibreOffice thu cong hoac dat OfficeToPDF.exe vao thu muc nay.

## 2026-05-10 - Cai OfficeToPDF vao du an

- Tao thu muc `BaiTapLon\App_Data\Tools`.
- Tai `OfficeToPDF.exe` ban `1.9.0.2` tu GitHub release chinh thuc `cognidox/OfficeToPDF` vao `BaiTapLon\App_Data\Tools\OfficeToPDF.exe`.
- Xac minh `OfficeToPDF.exe /version` tra ve `1.9.0.2` va file co chu ky EXE `MZ`.
- Them `App_Data\Tools\OfficeToPDF.exe` vao `BaiTapLon\DongTrieuBookStoreOnline.csproj` de file di kem web project khi build/publish.
- Luu y ky thuat: `OfficeToPDF` dung tinh nang export PDF cua Microsoft Office, nen neu may khong co `WINWORD.EXE` thi converter nay co the khong chuyen duoc DOC/DOCX; khi do he thong van fallback doc text bang OpenXML. Muon chuyen DOC/DOCX sang PDF ma khong can Microsoft Office thi can cai LibreOffice va cau hinh `ReviewLibreOfficePath`.
- Xac minh:
  - `BaiTapLon\App_Data\Tools\OfficeToPDF.exe /version`: `1.9.0.2`.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.

## 2026-05-10 - Sua luu sach yeu thich

- Kiem tra luong yeu thich: nut client goi `Users/ToggleFavorite`, trang tai khoan doc tu bang `ProductFavorites`.
- Nguyen nhan de bi mat yeu thich tren trang tai khoan: `sql/create_database.sql` chua tao bang `ProductFavorites` va JS co fallback luu localStorage khi server loi, nen co the bam thay doi trang thai nhung trang `/yeu-thich-{id}` khong doc duoc du lieu tai khoan.
- Cap nhat `Mood\Draw\ProductFavoriteDraw.cs`: moi thao tac yeu thich tu dam bao bang/index `ProductFavorites` ton tai truoc khi doc/ghi.
- Them `ProductFavoriteDraw.AddMissing` va endpoint `Users/SyncLocalFavorites` de dong bo cac sach da bam yeu thich luc chua dang nhap tu localStorage vao tai khoan sau khi dang nhap.
- Cap nhat `BaiTapLon\Scripts\FavoriteBooks.js`: khi co local favorites va nguoi dung da dang nhap, tu goi sync len server, xoa localStorage sau khi dong bo thanh cong va reload trang yeu thich tai khoan.
- Cap nhat `sql/create_database.sql`: them tao bang `ProductFavorites`, unique index `(UserID, ProductID)` va index doc danh sach theo `UserID, CreatedAt`.
- Xac minh:
  - DB local hien co bang `dbo.ProductFavorites`.
  - `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe DongTrieuBookStore.sln /v:minimal`: build thanh cong.

## 2026-06-26 - Audit, Port alignment, Tool setup, and Cursorrules Update

### Ke hoach thuc hien (Implementation Plan)
1. **Audit & Port Syncing**: Check ports across Python Flask app (`app.py`), C# `Web.config`, and `README_UPDATES.md`.
2. **Environment Port Sync**: Standardize configuration port mapping to `8082`.
3. **Repository Clones**: Clone repomix, OpenHands, and aider into separate directories.
4. **Development Rules Integration**: Update `.cursorrules` with rules on task splitting, automated workflows, planning/history logs, model bottleneck mitigation, and Aider UI requirements.
5. **Execution Logging**: Record execution details in `LichSu.md` and `LICHSU_THUCHIEN.md` per Rule 3.

### Ket qua hoan thanh (Execution Log)
- **Port Standardization**: Verified that the Flask API is listening on port `8082` (configured in `run.bat` and `run.ps1` of the Flask project).
- **C# Configuration**: Aligned `FaceAuthAPI` and `ChatboxWidgetUrl` settings in `QLNhaSacha/BaiTapLon/Web.config` to `localhost:8082`.
- **System Documentation**: Corrected port references from `5000`/`8000` to `8082` in `QLNhaSacha/README_UPDATES.md`.
- **Administrative Credentials**: Inspected `QLNhaSacha/db.sql` and confirmed the admin account: `admin1` / password `12345678` (hash `25d55ad283aa400af464c76d713c07ad`).
- **Tool Repositories**: Cloned `repomix`, `OpenHands`, and `aider` repositories into `d:\DUANNGHIENCUU` workspace.
- **Cursor Rules Update**: Formulated and wrote Rules 1 through 5 in `.cursorrules` to define strict coding, logging, and integration guidelines.

## 2026-06-26 - C# Compilation and Port 8082 Verification

### Execution Details:
- **MSBuild Path**: Located MSBuild.exe at `C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe`.
- **C# Solution Compilation**: Successfully compiled the C# solution `QLNhaSacha/DongTrieuBookStore.sln` using MSBuild under the Release configuration.
- **Port 8082 Verification**: Confirmed port `8082` is active and listening under PID `19812`.
- **Health Check**: Verified the Flask API health status by hitting `/api/face/health` (returned `200 OK` with models and configurations loaded).

## 2026-06-27 - Integration, Verification, and Database Audit

### Execution Details:
- **C# Build & Integration**: Aligned all microservice port references in `QLNhaSacha/BaiTapLon/Web.config` to `localhost:8082`. Successfully verified MSBuild execution on `QLNhaSacha/DongTrieuBookStore.sln`, ensuring that `CommomSentMail.dll`, `Mood.dll`, and `BaiTapLon.dll` compile without errors under Release configuration.
- **Python Face API Status**: Checked integration with the Python Flask Face API/Chatbox service. Verified it is listening and healthy on port `8082`.
- **Database Schema & Geofence Verification**: Inspected the database connection with SQL Server LocalDB `(localdb)\MSSQLLocalDB` for the database `QLNhaSach`. Resolved a query column mapping mismatch:
  - Verified that the `StoreLocations` table utilizes the column name `GeofenceRadius` (mapped in `StoreLocation.cs`).
  - Confirmed the `GeofenceLogs` table maps the column name `AllowedRadiusKm` (mapped in `GeofenceLog.cs`).
  - Ran `sqlcmd` to query `StoreLocations` using the correct column `GeofenceRadius`, validating that "Nhà sách Tân Hạnh" contains the configured geofence radius of `5.0`.
- **Auto Continuer Script Integration**: Verified and launched the background screen keep-alive bot:
  - The script `auto_continuer/auto_continuer.py` is configured with `"periodic_send_enabled": true`, `"periodic_send_interval_seconds": 300`, and `"detect_error_enabled": false`.
  - Confirmed that tests run and pass cleanly via `python auto_continuer/test_auto_continuer.py`.
  - Started the bot in the background (`start /B python auto_continuer/auto_continuer.py > auto_continuer/bot.log 2>&1`), logging actions to `auto_continuer/bot.log`.

## 2026-06-27 - Verification of Log Pagination Auto-Correction

### Execution Details:
- **Audit of Log Repository Pagination**: Inspected `Common/Repositories/LogRepository.cs` and verified that pagination auto-correction is implemented within `ToPagedResult<T>`.
  - Specifically, it safely checks if `page > totalPages` and caps it to `totalPages` (with a floor of 1 page).
  - Validated that `LogsAdminController.cs` uses `LogRepository` methods (`GetFaceAuthLogs`, `GetGeofenceLogs`, and `GetRentalLogs`) for querying logs, thus fully inheriting this auto-correction behavior.
- **MSBuild Compilation Check**: Re-ran MSBuild on the solution (`DongTrieuBookStore.sln`) with the Release configuration. The build succeeded without errors:
  - `CommomSentMail -> CommomSentMail.dll`
  - `Mood -> Mood.dll`
  - `DongTrieuBookStoreOnline -> BaiTapLon.dll`

## 2026-06-27 - Evaluate and Select GitHub Open-Source Auto Clicker

### Execution Details:
- **Research on Open-Source Tools**: Identified and compared multiple open-source clicker/typing tools from GitHub, including Pulover's Macro Creator (PMC), Actiona, AutoHotkey, and AutoKey.
- **Evaluation Document Created**: Documented the comparison matrix, step-by-step setup guides, and detailed workflow parameters in `auto_continuer/GITHUB_AUTOCLICKER_EVALUATION.md`.
- **AutoHotkey Integration**: Wrote a complete AutoHotkey script template (`.ahk`) mapping the user's dual-pin coordinates (Pin 1: `238, 906` and Pin 2: `304, 957`) and sending the custom "tiep tuc" long-text message efficiently using Windows Clipboard pasting.
- **Task Logging**: Appended all activities to `auto_continuer/LICHSU_THUCHIEN.md`.

## 2026-06-27 - UI/UX Modernization of DongTrieuBookStore

### Implementation Plan:
1. **Analyze Requirements**: Deep-dive into global layouts, CSS theme variables, dark/light theme triggers, responsive cart, profile card designs, order history & detailed invoice layouts.
2. **Setup Modern Stylesheet**: Create `BaiTapLon/assets/css/modern-premium.css` supporting light and dark themes via CSS variables.
3. **Layout Overrides**: Adapt `_LayoutHome.cshtml` and `_LayoutAdmin.cshtml` to import the modern stylesheet and apply theme-initialization JavaScript.
4. **Auth & Profile Pages**: Redesign `Login.cshtml`, `RegisterFace.cshtml`, and `ProfileUser.cshtml` with premium glassmorphic forms and futuristic scan visualizers.
5. **Transactions & Cart Pages**: Modernize cart summary, item list cards, invoice tracking status badges, and receipt confirmations in `Index.cshtml`, `DanhSachHang.cshtml`, and `ChiTietHoaDon.cshtml`.
6. **Verification & Testing**: Build with MSBuild to ensure compile safety.

### Execution Log:
- **Created modern-premium.css**: Implemented global SaaS variables, dark mode overrides (`[data-theme="dark"]`), responsive custom table stylings, premium input focuses, dynamic hovering cards, and high-tech `.face-scanner-box` scan indicators.
- **Redesigned Shared Layouts**: Modified `_LayoutHome.cshtml` and `_LayoutAdmin.cshtml` to embed the theme loader script, prevent Flash of Unstyled Content (FOUC), and import `modern-premium.css`. Included `#themeToggleBtn` in `TopMenu.cshtml` with reactive Sun/Moon icons toggle.
- **Modernized Authenticators & Cam Controllers**: 
  - Restructured `Login.cshtml` separating standard registration from biometric face login. Integrated automatic scan timers, neon scanners, and feedback overlays.
  - Revamped `RegisterFace.cshtml` and `ProfileUser.cshtml` supporting OCR document file drag-drop and card profile forms.
- **Upgraded Transactions, Cart, & Order Detail pages**: 
  - Redesigned `Cart/Index.cshtml` changing table structures to flexible flexbox layout cards.
  - Revamped order tracker lists `DanhSachHang.cshtml` and item status details `ChiTietHoaDon.cshtml` using elegant border themes, dynamic badge colors, and modern layout structures.
- **Solution Verification**: Verified project compilation using MSBuild tool against `DongTrieuBookStore.sln`. Output: Successful Release compilation without breaking Razor tags or route mappings.
