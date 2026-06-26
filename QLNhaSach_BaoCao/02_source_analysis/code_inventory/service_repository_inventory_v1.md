# Service va Repository Inventory v1

Nguon quet: `BaiTapLon/Services`, `Mood/Draw`, `Common/Repositories`, `Mood/EF2`

## Services

| Service | Vai tro |
|---|---|
| `StoreLocationService` | Lay/cau hinh thong tin nha sach dang hoat dong, tao cau hinh mac dinh cho dia diem va ban kinh geofence. |
| `GmailNotificationService` | Gui thong bao lien quan den yeu cau muon sach, duyet, tra, huy va qua han. |
| `FaceRentalTokenService` | Tao va xac thuc token ngan han sau khi nguoi dung xac thuc khuon mat de gui yeu cau muon sach. |
| `FaceAuthApiClient` | Ket noi API Flask nhan dien khuon mat/OCR. |

## Draw/Repository classes

| Lop | Vai tro |
|---|---|
| `UserDraw` | Dang nhap, dang ky, cap nhat tai khoan, quyen nguoi dung. |
| `SanphamDraw` | Truy van va quan ly sach/san pham. |
| `CategoryDraw` | Quan ly danh muc sach. |
| `OrderDraw` | Xu ly don hang va thong ke don hang. |
| `Order_DetailDraw` | Chi tiet don hang. |
| `ProductFavoriteDraw` | Them, bo, dong bo va liet ke sach yeu thich. |
| `ProductReviewDraw` | Quan ly danh gia san pham. |
| `MessengerDraw` | Tin nhan/thong bao cua nguoi dung. |
| `Feed_BackDraw` | Lien he va phan hoi. |
| `NhapHangDraw` | Nghiep vu nhap hang. |
| `NhaCungCapDraw` | Quan ly nha cung cap. |
| `MenuDraw` | Quan ly menu hien thi. |
| `SildeDraw` | Quan ly slider/banner. |
| `ContactDraw` | Du lieu lien he. |
| `FooterDraw` | Noi dung footer. |
| `LogRepository` | Ghi va truy van nhat ky xac thuc khuon mat, geofence va muon tra. |

## Database contexts

| Context | Vai tro |
|---|---|
| `QuanLySachDBContext` | DbContext chinh cua website nha sach. |
| `LogDbContext` | DbContext rieng cho cac bang log: `FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`. |
