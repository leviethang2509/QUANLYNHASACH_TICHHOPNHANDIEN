# Bang du lieu chinh v1

| Bang/Entity | Vai tro trong he thong | Lien quan chinh |
|---|---|---|
| `Users` | Luu tai khoan, thong tin ca nhan, email thong bao, thong tin CMND/CCCD | `Quyens`, `Orders`, `RentalRequests`, `ProductFavorites`, logs |
| `Quyens` | Luu vai tro/quyen | `Users` |
| `Sanphams` | Luu sach/san pham | `Categories`, `Order_Detail`, `RentalRequests`, `ProductFavorites`, `ProductReviews` |
| `Categories` | Luu danh muc sach | `Sanphams` |
| `Orders` | Luu don hang | `Users`, `Order_Detail` |
| `Order_Detail` | Luu chi tiet don hang | `Orders`, `Sanphams` |
| `RentalRequests` | Luu yeu cau muon/tra sach | `Users`, `Sanphams`, `RentalLogs` |
| `StoreLocations` | Luu thong tin nha sach, toa do, ban kinh geofence | `GeofenceLogs`, quy trinh muon sach |
| `ProductFavorites` | Luu sach yeu thich theo nguoi dung | `Users`, `Sanphams` |
| `ProductReviews` | Luu danh gia sach | `Users`, `Sanphams` |
| `FaceAuthLogs` | Luu log xac thuc khuon mat/OCR/challenge | `Users` |
| `GeofenceLogs` | Luu log kiem tra vi tri | `Users`, `StoreLocations` |
| `RentalLogs` | Luu log thay doi trang thai muon tra | `RentalRequests`, `Users` |
| `Slides` | Luu slider/banner | Trang chu |
| `Menus` | Luu menu dieu huong | Giao dien |
| `NhaCungCaps` | Luu nha cung cap | Nhap hang |
| `NhapHangs` | Luu nghiep vu nhap hang | `Sanphams`, `NhaCungCaps` |
| `KhoHang` | Luu ton kho | `Sanphams` |
| `Feedbacks` | Luu lien he/phan hoi | `Users`, admin feedback |
| `Messengers` | Luu tin nhan/thong bao | `Users` |
