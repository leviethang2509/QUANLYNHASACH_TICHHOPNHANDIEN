# Ke hoach xay dung bieu do trinh tu va lop phan tich bang draw.io cho BaoCaoMauSua_Version4

## 1. Muc tieu

- Dung lai toan bo nhom so do trong phan **THIET KE CAC CHUC NANG CUA HE THONG** cua `BaoCaoMauSua_Version4.docx`.
- Giu dung so hinh va ten hinh dang co trong bao cao Version4: `Hinh 4-1` den `Hinh 4-28`.
- Moi hinh phai co file nguon `.drawio` de sau nay mo bang diagrams.net/draw.io va sua tiep.
- Tu file `.drawio` xuat/chup lai PNG theo cung layout, sau do thay anh vao `BaoCaoMauSua_Version4.docx`.
- Noi dung so do phai bam source hien co tai `D:\BACKUP_2004_2026_D\QLNhaSach`, gom website ASP.NET MVC, EF model va API nhan dien/OCR Flask.

Ghi chu ve ten chuong: trong yeu cau co ghi "CHUONG 2. THIET KE CAC CHUC NANG CUA HE THONG", nhung trong file Version4 thuc te phan nay dang nam o nhom hinh `Hinh 4-1` den `Hinh 4-28` voi tieu de **THIET KE CAC CHUC NANG CUA HE THONG**. Ke hoach nay giu dung so hinh theo Version4.

## 2. Cau truc bao cao Version4 can giu

| Nhom | Noi dung trong Version4 | Cach dung lai |
|---|---|---|
| Danh muc hinh | Co san `Hinh 4-1` den `Hinh 4-28` | Giu so hinh, ten hinh; chi thay anh noi dung |
| Than bao cao | Moi use case gom 1 bieu do trinh tu va 1 bieu do lop phan tich | Giu vi tri cu, thay bang anh moi xuat tu draw.io |
| Style | Hinh cu dang co dang sequence/class UML mau do/vang | Dung style draw.io thong nhat, ro net khi chen Word |
| File Word dich | `BaoCaoMauSua_Version4.docx` | Backup truoc, neu file bi khoa thi tao fallback |

Thu muc can tao:

| Thu muc | Muc dich |
|---|---|
| `sequence_class_drawio_v4` | Chua 28 file `.drawio` nguon |
| `sequence_class_drawio_v4_exports` | Chua 28 file PNG xuat/chup tu `.drawio` |

## 3. Nguon doi chieu bat buoc

| Nhom chuc nang | File source can bam | Noi dung dua vao so do |
|---|---|---|
| Xem/tim kiem san pham | `BaiTapLon\Controllers\ProductController.cs`, `Mood\EF2\Sanpham.cs`, `Mood\EF2\Category.cs`, `Mood\EF2\ProductReview.cs` | `Index`, `Search`, `ListProduct`, `Detail`, `ReviewFilePreview`, doc san pham/danh muc/danh gia |
| Danh gia san pham | `ProductController.AddReview`, `Mood\EF2\ProductReview.cs`, `Mood\EF2\User.cs`, `Mood\EF2\Sanpham.cs` | User dang nhap, validate rating/comment, luu review, reload chi tiet |
| Gio hang | `BaiTapLon\Controllers\CartController.cs`, `Mood\EF2\Sanpham.cs` | `Index`, `AddItem`, `Update`, `Delete`, session cart |
| Dat hang | `CartController.PaymentMoMo`, `confirm_orderPaymentOnline`, `Success`, `cancel_order`, `Mood\EF2\Orders.cs`, `Mood\EF2\Order_Detail.cs` | Tao order, tao chi tiet don, cap nhat thanh toan |
| Muon/tra sach | `BaiTapLon\Controllers\RentalController.cs`, `Mood\EF2\RentalRequest.cs`, `Mood\EF2\RentalLog.cs`, `Mood\EF2\Sanpham.cs` | Check stock, profile, active rental, tao yeu cau, huy, duyet, tra, qua han |
| Xac thuc khuon mat/OCR | `BaiTapLon\Controllers\FaceAuthController.cs`, `BaiTapLon\Services\FaceAuthApiClient.cs`, `BaiTapLon\Services\FaceRentalTokenService.cs`, `face_auth_api\app.py` | `/api/face/register`, `/verify`, `/authenticate`, `/action-check`, `/ocr-cmnd`, tao token muon |
| Gmail thong bao | `BaiTapLon\Services\GmailNotificationService.cs`, `CommomSentMail\MailHelper.cs`, `BaiTapLon\Web.config` | Gui mail khi Request/Approve/Reject/Cancel/Return/Overdue |
| Tai khoan | `BaiTapLon\Controllers\UsersController.cs`, `BaiTapLon\Models\AccountViewModels.cs`, `Mood\EF2\User.cs`, `Mood\EF2\Quyen.cs` | Dang ky, dang nhap, doi mat khau, profile, MFA, dashboard |
| Yeu thich | `UsersController.ToggleFavorite`, `LocalFavoriteProducts`, `SyncLocalFavorites`, `Mood\EF2\ProductFavorite.cs` | Them/xoa/sync favorite, cap nhat UI |
| Don hang cua toi | `UsersController.ChiTietHoaDon`, `RentalController.MyRentals`, `Orders`, `Order_Detail`, `RentalRequest` | Xem don mua va lich su muon |
| Quan tri san pham | `ProductController.cs`, `Mood\EF2\Sanpham.cs`, `Category.cs`, `NhaCungCap.cs`, `KhoHang.cs` | CRUD sach, danh muc, kho, review/file preview |
| Quan tri nguoi dung | `UsersController.cs`, `Mood\EF2\User.cs`, `Quyen.cs`, `FaceAuthLog.cs`, `RentalRequest.cs`, `RentalLog.cs` | List/edit user, quyen, ho so dinh danh, log |
| Thong ke | `UsersController.Dashboard`, `Mood\ThongKeModel`, `Orders`, `RentalRequest`, `Sanpham`, log entities | Dashboard, tong hop don, muon, sach, log |

## 4. Quy tac style draw.io

### 4.1 Bieu do trinh tu

- Dung UML sequence diagram.
- Actor ben trai: `Khach vang lai`, `Nguoi dung`, `Quan tri vien` tuy use case.
- Boundary/View dat sau actor: ten view Razor nhu `Product/Detail.cshtml`, `Cart/Index.cshtml`, `Users/Login.cshtml`.
- Controller/Service/Entity dat theo thu tu tu trai sang phai:
  - View/Browser
  - Controller
  - Service neu co
  - EF/DbContext/Entity
  - API ngoai neu co, vi du Flask Face API, Gmail
- Loi goi dong bo dung mui ten lien; ket qua tra ve dung mui ten net dut.
- Cac nhanh dieu kien dung frame `alt`:
  - dang nhap/chua dang nhap
  - hop le/khong hop le
  - face verify thanh cong/that bai
  - con hang/het hang
  - Gmail bat/tat hoac loi SMTP
- Bieu do phai co ten message trung voi action/service that trong source, vi du `CheckStock()`, `CreateChallenge()`, `VerifyRentalFace()`, `RequestRental()`.

### 4.2 Bieu do lop phan tich

- Dung style UML class analysis gom stereotype:
  - `<<boundary>>` cho View/Razor/UI
  - `<<control>>` cho Controller/Service
  - `<<entity>>` cho EF model/domain object
  - `<<external>>` cho Flask API, Gmail, Chatbox neu co
- Moi class co 2 phan:
  - Thuoc tinh chinh neu la entity
  - Phuong thuc/action chinh neu la controller/service
- Lien ket:
  - View -> Controller
  - Controller -> Service
  - Controller/Service -> Entity/DbContext
  - Service -> External API
- Khong ve lop khong ton tai trong source, tru truong hop cau truc logic nhu `FaceRentalToken` thi ghi ro `memory/logical`.

### 4.3 Dinh dang anh xuat

- PNG nen trang, chu den, vien do/xam hoac xanh dam nhe de ro trong Word.
- Bieu do trinh tu nen co chieu ngang tu 1800px den 2400px.
- Bieu do lop phan tich nen co chieu ngang tu 1600px den 2200px.
- Ten file dung ASCII khong dau de tranh loi Word/zip.
- Khi thay vao Word, neu media cu la `.emf` thi van co the thay bang PNG nhung can cap nhat content type va relationship neu script thay doi duoi file. Cach an toan hon: tao PNG va sua relationship target sang `.png`.

## 5. Mapping so do can ve va vi tri thay the

| So hinh | Ten/vitri trong Version4 | Media hien tai | File draw.io du kien | File PNG export du kien |
|---|---|---|---|---|
| Hinh 4-1 | Bieu do trinh tu usecase xem san pham | `word/media/image44.png` | `sequence_class_drawio_v4/hinh_4_01_sequence_xem_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_01_sequence_xem_san_pham.png` |
| Hinh 4-2 | Bieu do lop phan tich usecase xem san pham | `word/media/image45.emf` | `sequence_class_drawio_v4/hinh_4_02_class_xem_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_02_class_xem_san_pham.png` |
| Hinh 4-3 | Bieu do trinh tu usecase danh gia san pham | `word/media/image47.png` | `sequence_class_drawio_v4/hinh_4_03_sequence_danh_gia_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_03_sequence_danh_gia_san_pham.png` |
| Hinh 4-4 | Bieu do lop phan tich usecase danh gia san pham | `word/media/image48.emf` | `sequence_class_drawio_v4/hinh_4_04_class_danh_gia_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_04_class_danh_gia_san_pham.png` |
| Hinh 4-5 | Bieu do trinh tu usecase them vao gio hang va quy trinh muon sach | `word/media/image50.png` | `sequence_class_drawio_v4/hinh_4_05_sequence_gio_hang_muon_sach.drawio` | `sequence_class_drawio_v4_exports/hinh_4_05_sequence_gio_hang_muon_sach.png` |
| Hinh 4-6 | Bieu do lop phan tich usecase them vao gio hang va quy trinh muon sach | `word/media/image51.emf` | `sequence_class_drawio_v4/hinh_4_06_class_gio_hang_muon_sach.drawio` | `sequence_class_drawio_v4_exports/hinh_4_06_class_gio_hang_muon_sach.png` |
| Hinh 4-7 | Bieu do trinh tu usecase them vao danh sach yeu thich | `word/media/image53.png` | `sequence_class_drawio_v4/hinh_4_07_sequence_yeu_thich.drawio` | `sequence_class_drawio_v4_exports/hinh_4_07_sequence_yeu_thich.png` |
| Hinh 4-8 | Bieu do lop phan tich usecase them vao danh sach yeu thich | `word/media/image54.emf` | `sequence_class_drawio_v4/hinh_4_08_class_yeu_thich.drawio` | `sequence_class_drawio_v4_exports/hinh_4_08_class_yeu_thich.png` |
| Hinh 4-9 | Bieu do trinh tu usecase dat hang hoac gui yeu cau muon sach | `word/media/image58.png` | `sequence_class_drawio_v4/hinh_4_09_sequence_dat_hang_muon_sach.drawio` | `sequence_class_drawio_v4_exports/hinh_4_09_sequence_dat_hang_muon_sach.png` |
| Hinh 4-10 | Bieu do lop phan tich usecase dat hang hoac gui yeu cau muon sach | `word/media/image59.emf` | `sequence_class_drawio_v4/hinh_4_10_class_dat_hang_muon_sach.drawio` | `sequence_class_drawio_v4_exports/hinh_4_10_class_dat_hang_muon_sach.png` |
| Hinh 4-11 | Bieu do trinh tu usecase quan ly thong tin tai khoan | `word/media/image62.png` | `sequence_class_drawio_v4/hinh_4_11_sequence_quan_ly_tai_khoan.drawio` | `sequence_class_drawio_v4_exports/hinh_4_11_sequence_quan_ly_tai_khoan.png` |
| Hinh 4-12 | Bieu do lop phan tich usecase quan ly thong tin tai khoan | `word/media/image63.emf` | `sequence_class_drawio_v4/hinh_4_12_class_quan_ly_tai_khoan.drawio` | `sequence_class_drawio_v4_exports/hinh_4_12_class_quan_ly_tai_khoan.png` |
| Hinh 4-13 | Bieu do trinh tu usecase don hang cua toi | `word/media/image66.png` | `sequence_class_drawio_v4/hinh_4_13_sequence_don_hang_cua_toi.drawio` | `sequence_class_drawio_v4_exports/hinh_4_13_sequence_don_hang_cua_toi.png` |
| Hinh 4-14 | Bieu do lop phan tich usecase don hang cua toi | `word/media/image67.emf` | `sequence_class_drawio_v4/hinh_4_14_class_don_hang_cua_toi.drawio` | `sequence_class_drawio_v4_exports/hinh_4_14_class_don_hang_cua_toi.png` |
| Hinh 4-15 | Bieu do trinh tu usecase dang ky | `word/media/image69.png` | `sequence_class_drawio_v4/hinh_4_15_sequence_dang_ky.drawio` | `sequence_class_drawio_v4_exports/hinh_4_15_sequence_dang_ky.png` |
| Hinh 4-16 | Bieu do lop phan tich usecase dang ky | `word/media/image70.png` | `sequence_class_drawio_v4/hinh_4_16_class_dang_ky.drawio` | `sequence_class_drawio_v4_exports/hinh_4_16_class_dang_ky.png` |
| Hinh 4-17 | Bieu do trinh tu usecase dang nhap | `word/media/image71.png` | `sequence_class_drawio_v4/hinh_4_17_sequence_dang_nhap.drawio` | `sequence_class_drawio_v4_exports/hinh_4_17_sequence_dang_nhap.png` |
| Hinh 4-18 | Bieu do lop phan tich usecase dang nhap | `word/media/image72.png` | `sequence_class_drawio_v4/hinh_4_18_class_dang_nhap.drawio` | `sequence_class_drawio_v4_exports/hinh_4_18_class_dang_nhap.png` |
| Hinh 4-19 | Bieu do trinh tu usecase quan ly don hang | `word/media/image76.png` | `sequence_class_drawio_v4/hinh_4_19_sequence_quan_ly_don_hang.drawio` | `sequence_class_drawio_v4_exports/hinh_4_19_sequence_quan_ly_don_hang.png` |
| Hinh 4-20 | Bieu do lop phan tich usecase quan ly don hang | `word/media/image77.emf` | `sequence_class_drawio_v4/hinh_4_20_class_quan_ly_don_hang.drawio` | `sequence_class_drawio_v4_exports/hinh_4_20_class_quan_ly_don_hang.png` |
| Hinh 4-21 | Bieu do trinh tu usecase quan ly nguoi dung | `word/media/image80.png` | `sequence_class_drawio_v4/hinh_4_21_sequence_quan_ly_nguoi_dung.drawio` | `sequence_class_drawio_v4_exports/hinh_4_21_sequence_quan_ly_nguoi_dung.png` |
| Hinh 4-22 | Bieu do lop phan tich usecase quan ly nguoi dung | `word/media/image81.png` | `sequence_class_drawio_v4/hinh_4_22_class_quan_ly_nguoi_dung.drawio` | `sequence_class_drawio_v4_exports/hinh_4_22_class_quan_ly_nguoi_dung.png` |
| Hinh 4-23 | Bieu do trinh tu usecase quan ly san pham | `word/media/image90.png` | `sequence_class_drawio_v4/hinh_4_23_sequence_quan_ly_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_23_sequence_quan_ly_san_pham.png` |
| Hinh 4-24 | Bieu do lop phan tich usecase quan ly san pham | `word/media/image91.emf` | `sequence_class_drawio_v4/hinh_4_24_class_quan_ly_san_pham.drawio` | `sequence_class_drawio_v4_exports/hinh_4_24_class_quan_ly_san_pham.png` |
| Hinh 4-25 | Bieu do trinh tu usecase quan ly quan tri vien | `word/media/image97.png` | `sequence_class_drawio_v4/hinh_4_25_sequence_quan_ly_quan_tri_vien.drawio` | `sequence_class_drawio_v4_exports/hinh_4_25_sequence_quan_ly_quan_tri_vien.png` |
| Hinh 4-26 | Bieu do lop phan tich usecase quan ly quan tri vien | `word/media/image98.emf` | `sequence_class_drawio_v4/hinh_4_26_class_quan_ly_quan_tri_vien.drawio` | `sequence_class_drawio_v4_exports/hinh_4_26_class_quan_ly_quan_tri_vien.png` |
| Hinh 4-27 | Bieu do trinh tu usecase thong ke | `word/media/image100.png` | `sequence_class_drawio_v4/hinh_4_27_sequence_thong_ke.drawio` | `sequence_class_drawio_v4_exports/hinh_4_27_sequence_thong_ke.png` |
| Hinh 4-28 | Bieu do lop phan tich usecase thong ke | `word/media/image101.emf` | `sequence_class_drawio_v4/hinh_4_28_class_thong_ke.drawio` | `sequence_class_drawio_v4_exports/hinh_4_28_class_thong_ke.png` |

## 6. Noi dung chi tiet tung so do

| So hinh | Loai | Noi dung bat buoc can co | Source doi chieu |
|---|---|---|---|
| Hinh 4-1 | Sequence | Khach/Nguoi dung mo trang san pham -> `ProductController.ListProduct` hoac `Search` -> EF doc `Sanpham`, `Category` -> View hien danh sach; khi vao chi tiet goi `Detail(idDetail)`, doc review/file preview neu co. | `ProductController.cs`, `Sanpham.cs`, `Category.cs`, `ProductReview.cs` |
| Hinh 4-2 | Class analysis | `<<boundary>> Product/ListProduct, Product/Detail`; `<<control>> ProductController`; `<<entity>> Sanpham, Category, ProductReview, User`; lien ket tim kiem, loc danh muc, xem chi tiet, xem file review. | `ProductController.cs`, `Mood\EF2` |
| Hinh 4-3 | Sequence | User dang nhap o trang chi tiet -> nhap rating/comment -> `ProductController.AddReview(productId, rating, comment)` -> validate session/rating/comment -> tao `ProductReview` -> save DB -> redirect/reload Detail. | `ProductController.AddReview`, `ProductReview.cs` |
| Hinh 4-4 | Class analysis | `Product/Detail.cshtml`, `ProductController`, `ProductReview`, `Sanpham`, `User`; the hien quan he User viet nhieu review, Sanpham co nhieu review. | `ProductController.cs`, `ProductReview.cs` |
| Hinh 4-5 | Sequence | Nhanh gio hang: Detail/List -> `CartController.AddItem(productID, quantity)` -> doc `Sanpham` -> them vao Session cart. Nhanh muon sach: `RentalController.CheckStock` -> `RentalProfileStatus` -> `FaceAuthController.CreateChallenge` -> `CheckChallengeAction` -> `VerifyRentalFace` -> `FaceRentalTokenService` tao token. | `CartController.cs`, `RentalController.cs`, `FaceAuthController.cs`, `FaceRentalTokenService.cs` |
| Hinh 4-6 | Class analysis | `CartController`, `RentalController`, `FaceAuthController`, `FaceAuthApiClient`, `FaceRentalTokenService`, `GmailNotificationService`, `Sanpham`, `RentalRequest`, `RentalLog`, `FaceAuthLog`. | Controllers/Services, `Mood\EF2` |
| Hinh 4-7 | Sequence | User bam icon yeu thich -> `UsersController.ToggleFavorite(productId)` -> kiem tra session dang nhap -> them/xoa `ProductFavorite`; neu khach vang lai thi cap nhat local favorite qua JS/local storage; co nhanh `LocalFavoriteProducts` va `SyncLocalFavorites`. | `UsersController.cs`, `ProductFavorite.cs`, `FavoriteBooks.js` |
| Hinh 4-8 | Class analysis | `Favorites.cshtml`, `LocalFavorites.cshtml`, `UsersController`, `ProductFavorite`, `User`, `Sanpham`; quan he many-to-many logic User - Sanpham qua ProductFavorites. | `UsersController.cs`, `ProductFavorite.cs` |
| Hinh 4-9 | Sequence | Tach 2 nhanh: Dat hang qua cart -> `PaymentMoMo`/confirm -> tao `Orders` va `Order_Detail`; Muon sach -> kiem tra active rental, consume faceToken, validate borrowDays <= `RentalMaxBorrowDays`, tao `RentalRequests`, ghi `RentalLogs`, gui Gmail. | `CartController.cs`, `RentalController.RequestRental`, `GmailNotificationService.cs` |
| Hinh 4-10 | Class analysis | `CartController`, `RentalController`, `Orders`, `Order_Detail`, `RentalRequest`, `Sanpham`, `User`, `GmailNotificationService`, `FaceRentalTokenService`; the hien 2 nghiep vu mua va muon cung su dung Sanpham. | `Mood\EF2`, Controllers/Services |
| Hinh 4-11 | Sequence | User vao `ProfileUser` -> sua thong tin qua `EditUser`, doi mat khau qua `EditPassWord`, cap nhat ho so muon qua `UpdateRentalProfile`; OCR CMND/CCCD goi `FaceAuthController.OcrCmnd` -> Flask `/api/face/ocr-cmnd` -> tra fields -> cap nhat ho so. | `UsersController.cs`, `RentalController.cs`, `FaceAuthController.cs`, `face_auth_api\app.py` |
| Hinh 4-12 | Class analysis | `ProfileUser.cshtml`, `UsersController`, `RentalController`, `FaceAuthController`, `FaceAuthApiClient`, `User`, `FaceAuthLog`; co `<<external>> Flask Face API`. | Controllers, `User.cs`, `FaceAuthLog.cs` |
| Hinh 4-13 | Sequence | User xem don hang cua toi -> `UsersController.ChiTietHoaDon(id)` doc `Orders`/`Order_Detail`; xem lich su muon -> `RentalController.MyRentals(status)` doc `RentalRequests`; tra view danh sach/trang thai. | `UsersController.ChiTietHoaDon`, `RentalController.MyRentals` |
| Hinh 4-14 | Class analysis | `ChiTietHoaDon.cshtml`, `MyRentals.cshtml`, `UsersController`, `RentalController`, `Orders`, `Order_Detail`, `RentalRequest`, `Sanpham`. | `UsersController.cs`, `RentalController.cs`, EF models |
| Hinh 4-15 | Sequence | Khach mo Register -> submit `RegisterUser(RegisterModel)` -> validate username/email/phone/password -> tao `User` -> gan quyen mac dinh -> tra JSON; sau dang ky co nhanh sang `RegisterFace` -> `FaceAuthController.RegisterFace(userId)` -> Flask `/api/face/register`. | `UsersController.RegisterUser`, `AccountViewModels.cs`, `FaceAuthController.RegisterFace` |
| Hinh 4-16 | Class analysis | `Register.cshtml`, `RegisterModel`, `UsersController`, `User`, `Quyen`, `FaceAuthController`, `FaceAuthApiClient`, `FaceAuthLog`; neu ve luong face sau dang ky thi ghi ro tuy chon. | `AccountViewModels.cs`, `UsersController.cs`, `User.cs` |
| Hinh 4-17 | Sequence | User submit login -> `UsersController.Login(LoginModel)` -> validate account/password -> neu can MFA thi `CreateChallenge` -> `CheckChallengeAction` -> `AuthenticateFaceLogin` -> Flask `/api/face/authenticate` -> set Session -> ghi `FaceAuthLogs`. | `UsersController.Login`, `FaceAuthController.AuthenticateFaceLogin`, `face_auth_api\app.py` |
| Hinh 4-18 | Class analysis | `Login.cshtml`, `LoginMFA.cshtml`, `LoginModel`, `UsersController`, `FaceAuthController`, `FaceAuthApiClient`, `User`, `FaceAuthLog`. | `UsersController.cs`, `FaceAuthController.cs` |
| Hinh 4-19 | Sequence | Admin vao quan ly don -> doc danh sach `Orders` -> xem chi tiet `Order_Detail` -> cap nhat trang thai giao/nhan/thanh toan neu source co action; neu co huy/thanh cong thi the hien `ChangeSuccessOrder`/confirm/cancel. | `CartController.cs`, `UsersController.ChangeSuccessOrder`, `Orders.cs` |
| Hinh 4-20 | Class analysis | Admin view order, `CartController`, `UsersController`, `Orders`, `Order_Detail`, `User`, `Sanpham`; the hien quan he Order - OrderDetails - Sanpham. | `Orders.cs`, `Order_Detail.cs` |
| Hinh 4-21 | Sequence | Admin vao danh sach nguoi dung -> `UsersController` doc `User`, `Quyen`; sua user qua `EditUser`; xem ho so dinh danh, rental, face log; neu co thao tac rental thi lien ket `RentalController.UpdateRentalStatus`. | `UsersController.cs`, `User.cs`, `Quyen.cs`, `FaceAuthLog.cs`, `RentalRequest.cs` |
| Hinh 4-22 | Class analysis | Admin user view, `UsersController`, `User`, `Quyen`, `RentalRequest`, `RentalLog`, `FaceAuthLog`, `GeofenceLog`; quan he User co quyen, log, rental. | `Mood\EF2` |
| Hinh 4-23 | Sequence | Admin quan ly san pham -> list/search -> create/update/delete `Sanpham`; doc `Category`, `NhaCungCap`, `KhoHang`; upload anh/file review neu co; save DB va tra view. | `ProductController.cs`, `Sanpham.cs`, `Category.cs`, `NhaCungCap.cs`, `KhoHang.cs` |
| Hinh 4-24 | Class analysis | Product admin view, `ProductController`, `Sanpham`, `Category`, `NhaCungCap`, `KhoHang`, `ProductReview`, `Slide`; the hien quan he danh muc, nha cung cap, kho va review. | `Mood\EF2`, `ProductController.cs` |
| Hinh 4-25 | Sequence | Admin quan ly quyen/tai khoan admin -> doc `User` va `Quyen` -> them/sua/xoa/phan quyen tai khoan quan tri -> save DB -> ghi log neu co repository. | `UsersController.cs`, `User.cs`, `Quyen.cs`, `Common\Repositories\LogRepository.cs` |
| Hinh 4-26 | Class analysis | Admin role view, `UsersController`, `User`, `Quyen`, `LogRepository`; ghi ro User.IDQuyen -> Quyen.IDQuyen, khong ve bang UserQuyens vat ly neu source khong co. | `UsersController.cs`, `Quyen.cs` |
| Hinh 4-27 | Sequence | Admin vao Dashboard -> `UsersController.Dashboard()` -> tong hop `Orders`, `RentalRequests`, `Sanpham`, log -> tao model thong ke -> View render chart/table. | `UsersController.Dashboard`, `Mood\ThongKeModel`, EF models |
| Hinh 4-28 | Class analysis | `Dashboard.cshtml`, `UsersController`, `ThongKeModelView`, `Orders`, `RentalRequest`, `Sanpham`, `FaceAuthLog`, `RentalLog`, `GeofenceLog`. | `UsersController.cs`, `Mood\ThongKeModel`, log models |

## 7. Cac luong nhan dien/OCR/Gmail phai the hien trong so do lien quan

| Luong | Chen vao hinh | Noi dung bat buoc |
|---|---|---|
| Dang ky khuon mat | Hinh 4-15, Hinh 4-16 | `RegisterFace.cshtml` -> `FaceAuthController.RegisterFace(userId)` -> `FaceAuthApiClient.Register` -> Flask `/api/face/register` -> luu profile -> ghi `FaceAuthLogs` |
| Dang nhap MFA bang khuon mat | Hinh 4-17, Hinh 4-18 | `CreateChallenge` -> `CheckChallengeAction` -> `AuthenticateFaceLogin` -> Flask `/api/face/authenticate` -> set session |
| Xac thuc khi muon sach | Hinh 4-5, Hinh 4-6, Hinh 4-9, Hinh 4-10 | `CheckStock` -> `RentalProfileStatus` -> `CreateChallenge` -> `CheckChallengeAction` -> `VerifyRentalFace` -> tao faceToken -> `RequestRental` |
| OCR CMND/CCCD | Hinh 4-11, Hinh 4-12 | Upload front/back -> `FaceAuthController.OcrCmnd` -> Flask `/api/face/ocr-cmnd` -> parse identity fields -> cap nhat User/Rental profile |
| Gmail thong bao muon/tra | Hinh 4-9, Hinh 4-10, Hinh 4-19 | Sau Request/Approve/Reject/Cancel/Return/Overdue goi `GmailNotificationService` va ghi log loi neu gui that bai |
| Log he thong | Hinh 4-5, 4-9, 4-17, 4-21, 4-22 | `FaceAuthLogs`, `RentalLogs`, `GeofenceLogs`; the hien actor/admin va action tao log |

## 8. Thu tu thuc hien

| Buoc | Viec can lam | Ket qua |
|---|---|---|
| 1 | Backup `BaoCaoMauSua_Version4.docx` | Co file `BaoCaoMauSua_Version4.before_sequence_class_update.docx` |
| 2 | Tao/cap nhat thu muc `sequence_class_drawio_v4` va `sequence_class_drawio_v4_exports` | Co noi luu source va anh export |
| 3 | Sinh 28 file `.drawio` theo mapping Hinh 4-1 den Hinh 4-28 | File import duoc len diagrams.net |
| 4 | Xuat/chup 28 PNG tu chinh layout `.drawio` | PNG ro net, dung style |
| 5 | Thay media trong `BaoCaoMauSua_Version4.docx` theo bang mapping | Word hien hinh moi o dung vi tri |
| 6 | Neu media cu la `.emf`, cap nhat relationship/content type sang `.png` | Word khong loi anh |
| 7 | Ghi lich su vao file rieng | De truy vet file draw.io, PNG va media da thay |
| 8 | Kiem tra DOCX bang zip test va mo Word xem nhanh | Dam bao file khong hong |

## 9. Script nen tao

Script de thuc hien ve/chup/thay anh nen dat ten:

- `scripts\generate_sequence_class_drawio_and_update_version4.py`

Script nen co cac nhiem vu:

1. Doc danh sach 28 `DiagramSpec`.
2. Sinh `.drawio` vao `sequence_class_drawio_v4`.
3. Render/chup PNG vao `sequence_class_drawio_v4_exports`.
4. Backup `BaoCaoMauSua_Version4.docx`.
5. Thay dung media target trong `word/media`.
6. Neu target cu la `.emf`, tao target PNG moi hoac sua relationship/content type cho hop le.
7. Ghi lich su vao `LichSuXayDungHinhSequenceClass_Version4.md`.
8. In ket qua: so file draw.io, so PNG, so anh da thay, file Word ket qua.

## 10. Checklist nghiem thu

- Co du 28 file `.drawio`.
- Co du 28 file PNG export.
- Hinh 4-1 den Hinh 4-28 trong Word da duoc thay dung vi tri.
- Ten hinh/caption trong Word khong doi sai so.
- Moi sequence diagram co actor, boundary, control, entity/external API ro rang.
- Moi class analysis co stereotype `boundary/control/entity/external`.
- Cac luong face/OCR/muon sach bat buoc co MVC -> Service -> Flask API -> JSON -> ghi log/token.
- Cac luong rental bat buoc co check stock, profile, active rental, face token, request, log, Gmail.
- Cac lop/action ve trong so do ton tai trong source.
- File Word sau khi update la zip hop le va mo duoc trong Word.

## 11. Ghi chu sua ve sau

- Khi can sua mot so do, sua file `.drawio` tuong ung trong `sequence_class_drawio_v4`, xuat lai PNG cung ten, roi thay lai media trong Word.
- Khong sua truc tiep PNG neu thay doi noi dung nghiep vu; nguon chinh phai la `.drawio`.
- Neu Version4 da duoc Word mo va khoa file, script phai ghi fallback, vi du `BaoCaoMauSua_Version4_SequenceClassDrawIO.docx`.
