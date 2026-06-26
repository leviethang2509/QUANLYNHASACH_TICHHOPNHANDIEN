# Controller va Action Inventory v1

Nguon quet: `BaiTapLon/**/*.cs`

## Frontend/User Controllers

| Controller | Vai tro chinh | Action tieu bieu |
|---|---|---|
| `UsersController` | Dang ky, dang nhap, ho so ca nhan, don hang cua toi, tin nhan, yeu thich | `RegisterUser`, `Login`, `ProfileUser`, `Dashboard`, `Favorites`, `ToggleFavorite`, `LocalFavoriteProducts`, `SyncLocalFavorites`, `ChiTietHoaDon`, `MessengerUser`, `MessengerReply` |
| `ProductController` | Hien thi, tim kiem, chi tiet sach, file doc thu, danh gia san pham | `Search`, `ListProduct`, `Detail`, `ReviewFile`, `ReviewFilePreview`, `ReviewFileDownload`, `AddReview` |
| `CartController` | Gio hang, thanh toan, xac nhan don hang, MoMo | `Index`, `AddItem`, `Update`, `Delete`, `DeleteAll`, `PaymentMoMo`, `Success`, `confirm_orderPaymentOnline`, `cancel_order` |
| `RentalController` | Quy trinh muon/tra sach phia nguoi dung va cap nhat trang thai | `MyRentals`, `CheckStock`, `CheckActiveRental`, `RentalProfileStatus`, `UpdateRentalProfile`, `RequestRental`, `CancelRental`, `UpdateRentalStatus` |
| `FaceAuthController` | OCR CMND/CCCD, xac thuc khuon mat, challenge hanh dong | `OcrCmnd`, `VerifyRentalFace`, `AuthenticateFaceLogin`, `CreateChallenge`, `CheckChallengeAction`, `RegisterFace`, `VerifyFace`, `AuthenticateFace` |
| `GeofenceController` | Kiem tra vi tri nguoi dung khi muon sach | `CheckGeofence` |
| `ContactController` | Trang lien he va gui lien he | `Index`, `Send` |
| `HomeController` | Trang chu, menu, header, footer | `TrangChu`, `MainMenu`, `TopMenu`, `HeaderCart`, `Footer` |
| `AboutUsController` | Trang gioi thieu nha sach | `Index` |
| `HealthController` | Kiem tra trang thai he thong/API | `Ping`, `FaceApi` |

## API Controllers

| Controller | Vai tro chinh | Action tieu bieu |
|---|---|---|
| `Api/LogsController` | API tra cuu log | `Face`, `Geofence`, `Rental` |

## Admin Controllers

| Controller | Vai tro chinh | Action tieu bieu |
|---|---|---|
| `Admin/LoginController` | Dang nhap/dang xuat quan tri | `Index`, `Login`, `Logout` |
| `Admin/HomesController` | Dashboard quan tri | `Index` |
| `Admin/SanPhamController` | Quan ly sach, ton kho, file doc thu | `Index`, `LocSach`, `KhoHang`, `Create`, `Edit`, `Delete`, `ExportExelTonKho` |
| `Admin/CategoryController` | Quan ly danh muc | `Index`, `Create`, `Edit`, `Delete` |
| `Admin/UserController` | Quan ly tai khoan | `Index`, `Create`, `Edit`, `Delete`, `ChangeStatus` |
| `Admin/HoaDonController` | Quan ly don hang va trang thai giao hang | `Index`, `XacNhan`, `Details`, `DongGoi`, `XuatKho`, `HoanThanh`, `TraLai`, `ExportExel` |
| `Admin/RentalAdminController` | Quan ly yeu cau muon/tra sach | `Index`, `UpdateStatus`, `SendOverdueReminders` |
| `Admin/LogsAdminController` | Xem nhat ky xac thuc, vi tri, muon tra | `FaceAuth`, `Geofence`, `Rental` |
| `Admin/WebManagerController` | Quan ly thong tin hien thi, menu, slider, vi tri nha sach | `StoreLocation`, `Menu`, `MenuCreate`, `MenuEdit`, `Silder`, `SliderCreate`, `SliderEdit` |
| `Admin/ThongKeController` | Bao cao/thong ke doanh thu, san pham hot, muon tra theo chu de | `Index`, `ThongKeSanPhamHot`, `DoanhThu`, `DoanhThuChart`, `MuonTraChuDe`, `ExportExel` |
| `Admin/NhapHangController` | Quan ly nhap hang, duyet, nhap kho | `Index`, `Duyet`, `NhapKho`, `HoanThanh`, `LapPhieuNhap`, `Edit`, `DuyetDon`, `ExportExel` |
| `Admin/NhaCungCapController` | Quan ly nha cung cap | `Index`, `Create`, `Edit`, `Delete` |
| `Admin/FeedBackController` | Quan ly lien he/phan hoi | `Index`, `Reply`, `ChiTiet`, `Delete` |

## Ghi chu

Inventory nay la ban dau, duoc tao tu viec quet controller/action. Cac mo ta se duoc doi chieu them voi view, service, repository va database o cac buoc sau.
