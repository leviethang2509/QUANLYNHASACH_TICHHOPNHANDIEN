# Database Context Inventory v1

Nguon: `Mood/EF2/QuanLySachDBContext.cs`, `Mood/EF2/LogDbContext.cs`

## DbSet chinh trong `QuanLySachDBContext`

| DbSet | Y nghia du kien trong he thong |
|---|---|
| `Categories` | Danh muc sach/san pham. |
| `Footers` | Noi dung footer website. |
| `Menus` | Menu dieu huong. |
| `MenuType` | Loai menu. |
| `Quyens` | Vai tro/quyen nguoi dung. |
| `Sanphams` | Sach/san pham trong nha sach. |
| `Slides` | Slider/banner trang chu. |
| `Users` | Tai khoan nguoi dung va quan tri vien. |
| `NhaCungCaps` | Nha cung cap. |
| `Oders` | Don hang. |
| `Oder_Details` | Chi tiet don hang. |
| `Contacts` | Thong tin lien he. |
| `Feedbacks` | Phan hoi/lien he tu nguoi dung. |
| `Messengers` | Tin nhan/thong bao. |
| `NhapHangs` | Phieu/yeu cau nhap hang. |
| `KhoHang` | Ton kho. |
| `StoreLocations` | Dia diem nha sach, toa do va ban kinh cho geofence. |
| `RentalRequests` | Yeu cau muon/tra sach. |
| `ProductFavorites` | Danh sach sach yeu thich theo nguoi dung. |
| `ProductReviews` | Danh gia sach/san pham. |

## DbSet log trong `LogDbContext`

| DbSet | Y nghia |
|---|---|
| `FaceAuthLogs` | Nhat ky dang ky/xac thuc khuon mat va challenge hanh dong. |
| `GeofenceLogs` | Nhat ky kiem tra vi tri khi muon sach. |
| `RentalLogs` | Nhat ky trang thai muon/tra sach. |

## Ghi chu phan tich

He thong su dung Entity Framework voi SQL Server LocalDB theo cau hinh `QuanLySachDBContext` trong `Web.config`. Cac migration SQL bo sung nam trong `sql/migrations`, lien quan den store location, rental request, log, identity card rental flow, favorites, review va notification email.
