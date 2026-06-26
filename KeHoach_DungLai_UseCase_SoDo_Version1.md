# Ke hoach dung lai use case va so do theo BaoCaoMauSua_Version1

**Can cu thuc hien**

- Bao cao goc: `BaoCaoMauSua_Version1.docx`.
- Source QLBanSach/QLNhaSach: `D:\BACKUP_2004_2026_D\QLNhaSach`.
- Website ASP.NET MVC: `BaiTapLon`, model/EF: `Mood`, mail: `CommomSentMail`, log dung chung: `Common`.
- API nhan dien/OCR hien co trong workspace: `face_auth_api\app.py`.
- Anh/so do da co: `report_assets`.

**Muc tieu**

Dung lai toan bo use case, so do CSDL, bieu do trinh tu, bieu do lop phan tich, so do kien truc, dieu huong man hinh va anh giao dien theo dung so hinh trong version1. Moi hinh phai bam source thuc te, dac biet cac luong moi: muon/tra sach, xac thuc khuon mat, OCR CMND/CCCD, Gmail thong bao, chatbox va nhat ky he thong.

## 1. Cau truc bao cao version1 can giu

| Phan | Noi dung can giu | Ghi chu khi dung lai |
|---|---|---|
| Phan dau | Loi noi dau, danh muc tu viet tat, danh muc hinh anh, muc luc | Cap nhat lai danh muc sau khi thay hinh |
| Chuong 1 | Mo ta cac yeu cau cua he thong | Giu cac muc 1.1 den 1.4, bo sung diem nhan dien/OCR/muon tra |
| Chuong 2 | Phan tich cac yeu cau chuc nang cua he thong | Giu so Hinh 21 den Hinh 211, dung lai use case tong quat va tung nhom |
| Chuong 3 | Thiet ke co so du lieu | Giu Hinh 3-1 den Hinh 3-26, dung lai theo bang/model SQL thuc te |
| Chuong 4 | Thiet ke cac chuc nang cua he thong | Giu Hinh 4-1 den Hinh 4-28, moi use case co 1 sequence va 1 class analysis |
| Chuong 5 | Thiet ke giao dien va cai dat | Giu Hinh 5-1 den Hinh 5-18, cap nhat kien truc MVC + Flask va anh man hinh that |
| Chuong 6 | Kiem thu he thong | Cap nhat test case cho login, xem san pham, mua/muon, face, OCR, Gmail, log |
| Chuong 7 | Tong ket va danh gia | Viet ket qua, han che, huong phat trien |

## 2. Nguyen tac dung lai so do

- Khong doi so hinh neu khong bat buoc; thay noi dung trong dung vi tri cu cua version1.
- Ten hinh giu gan version1, nhung duoc bo sung cum "muon sach", "OCR", "xac thuc khuon mat" neu dung nghiep vu hien tai.
- Tat ca actor va lop trong bieu do phai co can cu trong source: controller, service, model, view, API endpoint, SQL migration.
- Cac so do chuong 2 ve muc use case; chuong 4 ve muc thiet ke dong chay va lop phan tich; chuong 5 ve kien truc, dieu huong, giao dien.
- Voi nhom nhan dien, phai the hien bien gioi he thong: ASP.NET MVC goi Flask API qua `FaceAuthApiClient`, Flask tra JSON, MVC ghi log va sinh token.

## 3. Mapping source chinh dung cho cac so do

| Nhom | File source can doi chieu | Noi dung dua vao so do |
|---|---|---|
| Tai khoan | `BaiTapLon\Controllers\UsersController.cs`, `Mood\EF2\User.cs` | Dang ky, dang nhap, profile, doi mat khau, Facebook login, yeu thich |
| San pham | `BaiTapLon\Controllers\ProductController.cs`, `Mood\EF2\Sanpham.cs`, `Mood\EF2\ProductReview.cs` | Danh sach, tim kiem, chi tiet, review, file preview |
| Gio hang/don hang | `BaiTapLon\Controllers\CartController.cs`, `Mood\EF2\Orders.cs`, `Mood\EF2\Order_Detail.cs` | Them gio hang, thanh toan, don hang cua toi |
| Muon/tra sach | `BaiTapLon\Controllers\RentalController.cs`, `Mood\EF2\RentalRequest.cs`, `Mood\EF2\RentalLog.cs` | Tao yeu cau, kiem tra ton, huy, duyet, tu choi, tra sach, qua han |
| Nhan dien/OCR | `BaiTapLon\Controllers\FaceAuthController.cs`, `BaiTapLon\Services\FaceAuthApiClient.cs`, `BaiTapLon\Services\FaceRentalTokenService.cs`, `face_auth_api\app.py` | Register face, verify, MFA, action challenge, OCR CMND/CCCD, token muon |
| Gmail | `BaiTapLon\Services\GmailNotificationService.cs`, `CommomSentMail\MailHelper.cs`, `BaiTapLon\Web.config` | Gui mail theo trang thai muon/tra |
| Log | `Common\Repositories\LogRepository.cs`, `BaiTapLon\Controllers\Api\LogsController.cs`, `Mood\EF2\FaceAuthLog.cs`, `Mood\EF2\GeofenceLog.cs`, `Mood\EF2\RentalLog.cs` | Log face, geofence, rental |
| Cau hinh | `BaiTapLon\Web.config` | `FaceAuthAPI`, `ChatboxWidgetUrl`, `FaceAuthMinConfidence`, `FaceAuthRentalTokenMinutes`, `RentalMaxBorrowDays`, `GmailNotificationsEnabled` |
| Database | `sql\create_database.sql`, `sql\migrations\*.sql`, `Mood\EF2\QuanLySachDBContext.cs` | Bang, cot, khoa chinh/ngoai, log, rental, favorites, reviews |

## 4. Ke hoach thay the so do chuong 2 - Use case

| So hinh version1 | Ten/vitri can thay the | Noi dung can dung lai theo source | Actor/thanh phan bat buoc |
|---|---|---|---|
| Hinh 21 | Bieu do use case chinh, muc 2.1.1 | Use case tong quat cua he thong: xem sach, tim kiem, dang ky/dang nhap, gio hang, dat hang, muon sach, yeu thich, review, profile, OCR, face auth, admin quan ly, Gmail, chatbox, log | Khach vang lai, Nguoi dung, Quan tri vien, Face API, Gmail SMTP/API, Chatbox |
| Hinh 22 | Bieu do use case Dang nhap, muc 2.1.2 | Dang nhap tai khoan, dang nhap MFA bang khuon mat, tao challenge, kiem tra action, xac thuc face, ghi log | Nguoi dung, `UsersController.Login`, `FaceAuthController.AuthenticateFaceLogin`, `face_auth_api` |
| Hinh 23 | Bieu do use case Xem san pham | Xem trang chu, xem danh sach sach, tim kiem, xem chi tiet, xem review/file preview, kiem tra ton kho truoc khi mua/muon | Khach, Nguoi dung, `ProductController`, `Sanpham`, `ProductReview` |
| Hinh 24 | Bieu do use case Quan ly san pham | Admin them/sua/xoa san pham, danh muc, nha cung cap, kho, review/file, ton kho | Admin, `ProductController`, `SanphamDraw`, `KhoHang`, `Category`, `NhaCungCap` |
| Hinh 25 | Bieu do use case Quan ly don hang | Admin xem don, cap nhat trang thai, xu ly thanh toan, xem chi tiet hoa don | Admin, `CartController`, `Orders`, `Order_Detail` |
| Hinh 26 | Bieu do use case Don hang cua toi | Nguoi dung xem lich su don hang, chi tiet hoa don, trang thai don | Nguoi dung, `UsersController.ChiTietHoaDon`, `Orders`, `Order_Detail` |
| Hinh 27 | Bieu do use case Quan ly nguoi dung | Admin quan ly tai khoan, quyen, ho so dinh danh, lich su muon, log xac thuc | Admin, `UsersController`, `User`, `Quyen`, `FaceAuthLogs`, `RentalRequests` |
| Hinh 28 | Bieu do use case Quan ly thong tin tai khoan | Nguoi dung cap nhat ho so, Gmail, CMND/CCCD, upload anh giay to, OCR, doi mat khau, quan ly sach yeu thich | Nguoi dung, `UsersController.ProfileUser`, `RentalController.UpdateRentalProfile`, `FaceAuthController.OcrCmnd` |
| Hinh 29 | Bieu do use case Quan ly quan tri vien | Admin dang nhap, quan ly tai khoan admin/quyen, xem dashboard, thong ke, log | Admin, `User`, `Quyen`, `LogsController` |
| Hinh 210 | Bieu do use case Quan ly gio hang va quy trinh muon sach | Tach ro 2 nhanh: mua sach qua gio hang va muon sach co xac thuc khuon mat; muon sach gom check profile, check stock, face token, request, Gmail | Nguoi dung, `CartController`, `RentalController`, `FaceAuthController`, `GmailNotificationService` |
| Hinh 211 | Bieu do use case Quan ly danh sach yeu thich | Them/xoa/sync yeu thich, xem danh sach yeu thich local/server | Nguoi dung, `UsersController.ToggleFavorite`, `LocalFavoriteProducts`, `SyncLocalFavorites`, `ProductFavorite` |

## 5. Ke hoach thay the so do chuong 3 - Co so du lieu

| So hinh version1 | Ten/vitri can thay the | Noi dung can co | Nguon doi chieu |
|---|---|---|---|
| Hinh 3-1 | Cau truc database sau khi thiet ke | ERD logic tong quat: User, Quyen, Sanpham, Category, Orders, Order_Detail, RentalRequests, ProductFavorites, ProductReviews, FaceAuthLogs, RentalLogs, GeofenceLogs, StoreLocations | `QuanLySachDBContext.cs`, `LogDbContext.cs`, `sql\migrations` |
| Hinh 3-2 | Chi tiet bang Users | Cot tai khoan, email, phone, address, role/quyen, thong tin ho so dinh danh neu co trong DB | `Mood\EF2\User.cs` |
| Hinh 3-3 | Chi tiet bang RentalRequests | ID, UserID, ProductID, Quantity, Status, RequestedAt/RequestDate, BorrowDays, ExpectedReturnDate, ActualReturnDate, RejectReason, IdentityNumber, IdentityFullName, IdentityCardFront/Back | `RentalRequest.cs`, `20260508_add_rental_requests.sql`, `20260509_add_identity_card_rental_flow.sql` |
| Hinh 3-4 | Chi tiet bang Slides | Banner/slide trang chu, anh, link, thu tu, trang thai | `Slide.cs` |
| Hinh 3-5 | Chi tiet bang StoreLocations | Ten cua hang, toa do, ban kinh geofence, email, icon/banner, noi dung gioi thieu | `StoreLocation.cs`, `20260508_add_stores.sql` |
| Hinh 3-6 | Chi tiet bang Categories | ID, Name, MetaTitle, ParentID, DisplayOrder, Status | `Category.cs` |
| Hinh 3-7 | Chi tiet bang ProductFavorites | UserID, ProductID, CreatedAt, unique User/Product | `ProductFavorite.cs`, `20260509_add_product_favorites.sql` |
| Hinh 3-8 | Chi tiet bang ProductReviews | ProductID, UserID, Rating, Comment, CreatedAt, Status | `ProductReview.cs`, `20260510_add_product_reviews_version5.sql` |
| Hinh 3-9 | Chi tiet bang Users | Neu version1 lap lai Users thi thay bang bang bo sung UserQuyen/ho so nguoi dung, hoac giu Users nhung ghi ro khong trung noi dung Hinh 3-2 | `User.cs`, `Quyen.cs` |
| Hinh 3-10 | Chi tiet bang FaceAuthLogs | UserID, Action, Purpose, Result, Confidence, RequestId, ErrorCode, LivenessPassed, Timestamp | `FaceAuthLog.cs`, `20260508_add_logs.sql` |
| Hinh 3-11 | Chi tiet bang ProductFavorites | Co the thay bang quan he User-Sanpham qua Favorites neu Hinh 3-7 da la table detail | `ProductFavorite.cs` |
| Hinh 3-12 | Chi tiet bang FaceSamples | Neu DB khong co model rieng, mo ta luu tru file/embedding phu tro: anh trong storage va profile trong `face_profiles`; neu co bang cu thi cap nhat theo thuc te | `face_auth_api\app.py`, `Web.config` |
| Hinh 3-13 | Chi tiet bang Orders | ID, UserID, ShipName, ShipAddress, ShipMobile, ShipEmail, CreatedDate, Status, payment fields | `Orders.cs` |
| Hinh 3-14 | Chi tiet bang OrderDetails | OrderID, ProductID, Quantity, Price | `Order_Detail.cs` |
| Hinh 3-15 | Chi tiet bang Sanphams | ID, Name, Code, Price, PromotionPrice, Quantity, CategoryID, Image, Detail, Status | `Sanpham.cs` |
| Hinh 3-16 | Chi tiet bang Users | Nen doi thanh bang User profile/identity neu can them ho so muon sach, tranh trung lap | `User.cs`, `RentalController.UpdateRentalProfile` |
| Hinh 3-17 | Chi tiet bang FaceAuthLogs | Neu lap lai, dung de mo ta index/log lifecycle: register, verify, authenticate, rental_verify, action_check | `LogRepository.cs`, `FaceAuthController.cs` |
| Hinh 3-18 | Chi tiet bang Quyens | ID, ten quyen, mo ta, lien ket user | `Quyen.cs` |
| Hinh 3-19 | Chi tiet bang RentalLogs | RentalID, UserID, Action, Message, Timestamp, Status truoc/sau neu co | `RentalLog.cs`, `20260508_add_logs.sql` |
| Hinh 3-20 | Chi tiet bang UserQuyens | Neu DB khong co bang rieng thi mo ta quan he User-Quyen theo source, khong ve bang ao neu khong ton tai | `User.cs`, `Quyen.cs` |
| Hinh 3-21 | Chi tiet bang FaceRentalTokens | Neu token luu memory trong service, ghi ro la cau truc logic token: token, userId, productId, expiresAt, consumed | `FaceRentalTokenService.cs` |
| Hinh 3-22 | Chi tiet bang FaceRentalTokens | Dung lam so do vong doi token: tao sau verify, het han sau 3 phut, consume khi request rental | `FaceRentalTokenService.cs`, `Web.config` |
| Hinh 3-23 | Chi tiet bang StoreLocations | Neu lap lai, mo ta quan he StoreLocations-GeofenceLogs | `StoreLocation.cs`, `GeofenceLog.cs` |
| Hinh 3-24 | Chi tiet bang RentalLogs | Neu lap lai, mo ta log theo trang thai Request/Cancel/Approve/Reject/Return/Overdue | `RentalController.cs`, `RentalLog.cs` |
| Hinh 3-25 | Chi tiet bang GeofenceLogs | UserID, StoreID, Lat, Lon, Distance, AllowedRadius, InZone, Timestamp | `GeofenceLog.cs`, `GeofenceController.cs` |
| Hinh 3-26 | Cau truc database sau khi da cai dat | ERD vat ly sau migration, danh dau bang moi: RentalRequests, ProductFavorites, ProductReviews, StoreLocations, FaceAuthLogs, RentalLogs, GeofenceLogs | `sql\migrations\*.sql` |

## 6. Ke hoach thay the so do chuong 4 - Sequence va class analysis

| So hinh version1 | Vi tri | Noi dung sequence/class can ve lai | File can bam |
|---|---|---|---|
| Hinh 4-1 | 4.1.1 sequence xem san pham | Khach/Nguoi dung -> `ProductController.ListProduct/Search/Detail` -> `SanphamDraw`/EF -> View; co nhanh review/file preview | `ProductController.cs`, `Sanpham.cs`, `ProductReview.cs` |
| Hinh 4-2 | 4.1.2 class xem san pham | Boundary View, Control ProductController, Entity Sanpham/Category/ProductReview | `ProductController.cs`, `Mood\EF2` |
| Hinh 4-3 | 4.2.1 sequence danh gia san pham | User dang nhap -> Detail -> AddReview -> ProductReview -> reload danh gia; validate rating/comment | `ProductController.AddReview`, `ProductReview.cs` |
| Hinh 4-4 | 4.2.2 class danh gia san pham | View Detail, ProductController, ProductReview, User, Sanpham | `ProductController.cs` |
| Hinh 4-5 | 4.3.1 sequence them gio hang va muon sach | Nhanh gio hang: AddItem -> Session cart; nhanh muon: CheckStock -> RentalProfileStatus -> CreateChallenge/VerifyRentalFace -> RequestRental -> Gmail/log | `CartController.cs`, `RentalController.cs`, `FaceAuthController.cs` |
| Hinh 4-6 | 4.3.2 class them gio hang va muon sach | CartController, RentalController, FaceAuthController, FaceRentalTokenService, RentalRequest, Sanpham, GmailNotificationService | `BaiTapLon\Controllers`, `BaiTapLon\Services` |
| Hinh 4-7 | 4.4.1 sequence them yeu thich | User -> ToggleFavorite -> ProductFavoriteDraw/EF -> JSON result -> cap nhat icon UI | `UsersController.ToggleFavorite`, `ProductFavorite.cs` |
| Hinh 4-8 | 4.4.2 class yeu thich | UsersController, ProductFavorite, User, Sanpham, View Favorites | `UsersController.cs`, `ProductFavorite.cs` |
| Hinh 4-9 | 4.5.1 sequence mua hang hoac gui yeu cau muon | Mua: Cart -> Payment -> Orders/OrderDetail; Muon: Rental request co faceToken, check max days 30, check active rental | `CartController.cs`, `RentalController.RequestRental` |
| Hinh 4-10 | 4.5.2 class mua hang/muon | CartController, RentalController, Orders, Order_Detail, RentalRequest, Sanpham | `Mood\EF2` |
| Hinh 4-11 | 4.6.1 sequence quan ly thong tin tai khoan | User -> ProfileUser/EditUser/EditPassWord/UpdateRentalProfile/OcrCmnd -> User/Rental profile -> Save | `UsersController.cs`, `RentalController.cs`, `FaceAuthController.OcrCmnd` |
| Hinh 4-12 | 4.6.2 class quan ly tai khoan | UsersController, RentalController, FaceAuthController, User, FaceAuthApiClient | `BaiTapLon\Controllers`, `BaiTapLon\Services` |
| Hinh 4-13 | 4.7.1 sequence don hang cua toi | User -> ChiTietHoaDon/MyRentals -> Orders/RentalRequests -> View | `UsersController.ChiTietHoaDon`, `RentalController.MyRentals` |
| Hinh 4-14 | 4.7.2 class don hang cua toi | UsersController, RentalController, Orders, Order_Detail, RentalRequest, Sanpham | `UsersController.cs`, `RentalController.cs` |
| Hinh 4-15 | 4.8.1 sequence dang ky | User -> RegisterUser -> validate username/email/phone -> UserDraw/EF -> result; tuy chon chuyen sang RegisterFace | `UsersController.RegisterUser` |
| Hinh 4-16 | 4.8.2 class dang ky | Register View, UsersController, RegisterModel, User, UserDraw | `UsersController.cs`, `Mood\UserModel` |
| Hinh 4-17 | 4.9.1 sequence dang nhap | User -> Login -> validate account; neu MFA face thi CreateChallenge -> action-check -> authenticate -> session | `UsersController.Login`, `FaceAuthController.AuthenticateFaceLogin` |
| Hinh 4-18 | 4.9.2 class dang nhap | Login View, UsersController, FaceAuthController, FaceAuthApiClient, User, FaceAuthLog | `UsersController.cs`, `FaceAuthController.cs` |
| Hinh 4-19 | 4.10.1 sequence quan ly don hang | Admin -> danh sach don -> cap nhat status -> Orders/OrderDetail -> thong bao/log neu co | `CartController.cs`, admin views neu co |
| Hinh 4-20 | 4.10.2 class quan ly don hang | Admin View, Cart/Order controller, Orders, Order_Detail, User | `Mood\EF2\Orders.cs` |
| Hinh 4-21 | 4.11.1 sequence quan ly nguoi dung | Admin -> list/edit user -> UserDraw/EF; xem identity, rental, face logs | `UsersController.cs`, `LogsController.cs` |
| Hinh 4-22 | 4.11.2 class quan ly nguoi dung | UsersController, User, Quyen, FaceAuthLog, RentalRequest, RentalLog | `Mood\EF2` |
| Hinh 4-23 | 4.12.1 sequence quan ly san pham | Admin -> CRUD Sanpham -> Category/NhaCungCap/KhoHang -> View | `ProductController.cs`, `SanphamDraw.cs`, `KhoHang.cs` |
| Hinh 4-24 | 4.12.2 class quan ly san pham | ProductController, Sanpham, Category, NhaCungCap, KhoHang, ProductReview | `Mood\EF2`, `Mood\Draw` |
| Hinh 4-25 | 4.13.1 sequence quan ly quan tri vien | Admin -> quan ly quyen/tai khoan admin -> User/Quyen -> log | `UsersController.cs`, `Quyen.cs` |
| Hinh 4-26 | 4.13.2 class quan ly quan tri vien | Admin boundary, UsersController, User, Quyen, LogRepository | `Common\Repositories\LogRepository.cs` |
| Hinh 4-27 | 4.14.1 sequence thong ke | Admin -> Dashboard/thong ke -> Orders/RentalRequests/Sanpham/Logs -> Chart/table | `UsersController.Dashboard`, `Mood\ThongKeModel` |
| Hinh 4-28 | 4.14.2 class thong ke | Dashboard View, UsersController, ThongKeModelView, Orders, RentalRequest, Log entities | `Mood\ThongKeModel\ThongKeModelView.cs` |

## 7. Bo sung so do rieng cho nhan dien, OCR, Gmail va chatbox

Version1 chua tach so hinh rieng cho cac luong nay, nen dua vao cac hinh co san sau:

| Luong moi | Chen/thay trong hinh nao | Noi dung bat buoc |
|---|---|---|
| Dang ky khuon mat | Hinh 4-15/4-16 hoac Hinh 4-17/4-18 | `RegisterFace.cshtml` -> `FaceAuthController.RegisterFace` -> `FaceAuthApiClient.Register` -> `/api/face/register` -> luu profile -> `FaceAuthLogs` |
| Xac thuc khi dang nhap | Hinh 22, Hinh 4-17, Hinh 4-18 | CreateChallenge -> action-check -> authenticate -> set session -> ghi log |
| Xac thuc khi muon sach | Hinh 210, Hinh 4-5, Hinh 4-6, Hinh 4-9, Hinh 4-10 | Check profile/stock -> action challenge -> verify -> tao faceToken 3 phut -> `RequestRental` |
| OCR CMND/CCCD | Hinh 28, Hinh 4-11, Hinh 4-12, Hinh 5-10 | Upload front/back -> `FaceAuthController.OcrCmnd` -> `/api/face/ocr-cmnd` -> parse fields -> update profile |
| Gmail thong bao | Hinh 210, Hinh 4-5, Hinh 4-9, Hinh 5-1 | Sau Request/Approve/Reject/Cancel/Return/Overdue goi `GmailNotificationService` |
| Chatbox | Hinh 21, Hinh 5-1, Hinh 5-3/5-4 | Website nhung `ChatboxWidgetUrl`, chatbox goi Flask `/api/chatbox/*` neu endpoint duoc bo sung/chay |
| Nhat ky he thong | Hinh 27, Hinh 3-10, Hinh 3-19, Hinh 3-25 | `LogRepository` ghi FaceAuthLogs, RentalLogs, GeofenceLogs; `LogsController` doc log |

## 8. Ke hoach thay the so do chuong 5 - Kien truc, dieu huong, giao dien

| So hinh version1 | Ten/vitri can thay the | Noi dung can co | Anh/nguon |
|---|---|---|---|
| Hinh 5-1 | Mo hinh kien truc MVC ket hop API phu tro | Browser/Razor -> Controllers -> Services -> EF/SQL Server; FaceAuthApiClient -> Flask `face_auth_api`; GmailNotificationService -> Gmail; Chatbox widget -> Flask | Tao moi bang draw.io |
| Hinh 5-2 | Gioi thieu ASP.NET MVC 5 | So do MVC: View, Controller, Model, EF, SQL; bo sung service layer | Tao moi hoac hinh ly thuyet |
| Hinh 5-3 | Dieu huong man hinh nhom use case chinh | Home -> Product list/detail -> Cart/Payment -> Rental verify/request -> MyRentals -> Profile -> Login/Register | Tao moi bang draw.io |
| Hinh 5-4 | Dieu huong man hinh nhom use case thu cap | Admin dashboard -> product/order/user/rental/log; Face/OCR screens; chatbox | Tao moi bang draw.io |
| Hinh 5-5 | Giao dien xem san pham | Danh sach sach/tim kiem/phan trang | `report_assets\screenshot_product_list.png` hoac chup lai |
| Hinh 5-6 | Giao dien danh gia san pham | Detail + rating/comment + file review/preview | Chup bo sung tu `Product\Detail.cshtml` |
| Hinh 5-7 | Giao dien gio hang va quy trinh muon sach | Gio hang + nut muon/kiem tra ton/xac thuc face | `report_assets\screenshot_rentals.png` hoac chup lai luong muon |
| Hinh 5-8 | Giao dien danh sach yeu thich | Favorites/LocalFavorites, icon yeu thich | Chup bo sung |
| Hinh 5-9 | Giao dien trang dat hang | Payment/confirm/cancel | Chup bo sung tu `Views\Cart` |
| Hinh 5-10 | Giao dien quan ly thong tin tai khoan | Profile, Gmail, CMND/CCCD, OCR upload | Chup bo sung tu `ProfileUser.cshtml` |
| Hinh 5-11 | Giao dien don hang cua toi | Chi tiet hoa don va/hoac MyRentals | Chup bo sung tu `ChiTietHoaDon.cshtml`, `MyRentals.cshtml` |
| Hinh 5-12 | Giao dien dang ky | Register form | Chup bo sung |
| Hinh 5-13 | Giao dien dang nhap | Login + MFA/face login neu co | `report_assets\screenshot_login.png` hoac chup lai |
| Hinh 5-14 | Giao dien quan ly don hang | Admin order list/status | Chup bo sung |
| Hinh 5-15 | Giao dien quan ly nguoi dung | User list/profile/log | Chup bo sung |
| Hinh 5-16 | Giao dien quan ly san pham | Product admin CRUD | Chup bo sung |
| Hinh 5-17 | Giao dien quan ly quan tri vien | Admin/role management | Chup bo sung |
| Hinh 5-18 | Giao dien thong ke | Dashboard, thong ke don/muon/sach/log | Chup bo sung |

## 9. Noi dung chi tiet can ve trong cac luong nhan dien

### 9.1 Luong Face API trong so do sequence

1. Browser gui anh/webcam frame ve `FaceAuthController`.
2. `FaceAuthController` validate file, purpose, challenge token.
3. `FaceAuthApiClient` goi base URL `FaceAuthAPI=http://localhost:8000/api/face`.
4. Flask endpoint xu ly:
   - `/api/face/health`: kiem tra API.
   - `/api/face/register`: dang ky mau khuon mat.
   - `/api/face/verify`: xac thuc 1:1.
   - `/api/face/authenticate`: dang nhap/MFA.
   - `/api/face/action-check`: kiem tra quay trai/quay phai/mo mieng/cuoi.
   - `/api/face/ocr-cmnd`, `/api/face/qcr-cmnd`, `/api/face/cmnd-ocr`: OCR CMND/CCCD.
5. Flask tra JSON: `success`, `confidence`, `request_id`, `error_code`, `message`.
6. MVC ghi `FaceAuthLogs`.
7. Neu la muon sach va `confidence >= 0.75`, `FaceRentalTokenService` tao token 3 phut.

### 9.2 Luong muon/tra sach trong so do sequence

1. User mo chi tiet sach va bam muon.
2. `RentalController.CheckStock` kiem tra ton kho.
3. `RentalController.CheckActiveRental` chan trung yeu cau dang hieu luc.
4. `RentalController.RentalProfileStatus` kiem tra Gmail, CMND/CCCD, ho ten.
5. `FaceAuthController.CreateChallenge` tao challenge.
6. `FaceAuthController.CheckChallengeAction` goi Flask action-check.
7. `FaceAuthController.VerifyRentalFace` goi Flask verify, tao `faceToken`.
8. `RentalController.RequestRental` consume token, validate ngay muon toi da `RentalMaxBorrowDays=30`.
9. Tao `RentalRequests` trang thai `Pending`, ghi `RentalLogs`.
10. `GmailNotificationService` gui mail da nhan yeu cau.
11. Admin goi `UpdateRentalStatus` de Approve/Reject/Return/Overdue, cap nhat ton kho va gui Gmail.

### 9.3 Luong OCR trong so do sequence

1. User upload anh mat truoc/mat sau CMND/CCCD.
2. MVC validate dinh dang va dung luong.
3. MVC goi `/api/face/ocr-cmnd`.
4. Flask dung OCR de doc text, parse so giay to, ho ten, ngay sinh, dia chi, ngay cap/noi cap.
5. Neu co user_id, Flask co the so khop khuon mat tren giay to voi face profile.
6. MVC cap nhat ho so dinh danh hoac gan vao `RentalRequests` khi tao yeu cau muon.

## 10. Thu tu thuc hien

| Buoc | Viec can lam | Ket qua |
|---|---|---|
| 1 | Sao luu `BaoCaoMauSua_Version1.docx` truoc khi thay hinh | Co file backup |
| 2 | Dung lai Hinh 21 den Hinh 211 bang draw.io | Use case dung actor va source hien tai |
| 3 | Dung lai Hinh 3-1 den Hinh 3-26 | ERD/table detail khop SQL/model |
| 4 | Dung lai Hinh 4-1 den Hinh 4-28 | Sequence/class analysis khop controller/service/model |
| 5 | Dung lai Hinh 5-1 den Hinh 5-4 | Kien truc va dieu huong khop MVC + Flask |
| 6 | Chup lai Hinh 5-5 den Hinh 5-18 | Anh giao dien ro, dung chuc nang |
| 7 | Cap nhat danh muc hinh anh trong Word | So hinh va so trang dung |
| 8 | Doc lai chuong 2-5 | Khong con mo ta chung chung hoac sai source |

## 11. Checklist nghiem thu tung so do

- Co dung so hinh version1.
- Ten hinh khong lech voi muc luc/danh muc hinh.
- Moi actor deu co vai tro ro rang.
- Moi controller/service/model xuat hien trong so do deu ton tai trong source.
- Luong muon sach bat buoc co: profile -> stock -> face challenge -> face verify -> token -> rental request -> log -> Gmail.
- Luong OCR bat buoc co upload anh, Flask OCR, parse field, cap nhat ho so.
- Luong admin muon/tra bat buoc co doi trang thai va cap nhat ton kho.
- Bieu do CSDL khong ve bang ao neu source khong co; voi token/face sample luu ngoai DB phai ghi ro la cau truc logic/phu tro.
- Hinh giao dien phai chup tu ung dung hien tai hoac file trong `report_assets`, khong dung hinh minh hoa khong lien quan.

