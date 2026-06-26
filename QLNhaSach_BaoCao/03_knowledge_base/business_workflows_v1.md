# Business Workflows v1

## 1. Dang nhap va xac thuc khuon mat

1. Nguoi dung nhap tai khoan va mat khau tren giao dien dang nhap.
2. `UsersController.Login` kiem tra thong tin qua `UserDraw.LoginHomeUser`.
3. Neu tai khoan hop le va cau hinh `EnableFaceMFA=true`, he thong tao `FACE_MFA_SESSION`.
4. Nguoi dung duoc dieu huong sang man hinh xac thuc MFA.
5. `FaceAuthController` tao challenge hanh dong va gui anh khuon mat sang `face_auth_api`.
6. Neu xac thuc thanh cong, he thong tao `USER_SESSION` va cho phep truy cap.

## 2. Muon sach co kiem tra vi tri

1. Nguoi dung mo trang chi tiet sach.
2. JavaScript cua trang goi API trinh duyet de lay toa do hien tai.
3. Toa do duoc gui den `GeofenceController.CheckGeofence`.
4. Controller lay dia diem nha sach dang hoat dong bang `StoreLocationService`.
5. He thong tinh khoang cach giua nguoi dung va nha sach.
6. Ket qua duoc ghi vao `GeofenceLogs`.
7. Neu nguoi dung nam trong ban kinh cho phep, nut muon sach duoc kich hoat.

## 3. Gui yeu cau muon sach

1. Nguoi dung chon thoi gian muon va xac nhan thong tin CMND/CCCD.
2. He thong kiem tra ho so muon qua `RentalController.RentalProfileStatus`.
3. Nguoi dung xac thuc khuon mat qua `FaceAuthController.VerifyRentalFace`.
4. Neu xac thuc thanh cong, `FaceRentalTokenService` tao token ngan han.
5. `RentalController.RequestRental` kiem tra token, ton kho, ngay muon va so ngay muon.
6. He thong tao `RentalRequest` voi trang thai `Pending`.
7. He thong ghi `RentalLog` va goi `GmailNotificationService`.

## 4. Quan tri duyet va xac nhan tra sach

1. Quan tri vien vao `Admin/RentalAdmin/Index` de xem danh sach yeu cau.
2. Khi bam duyet, `RentalAdminController.UpdateStatus` goi `RentalController.UpdateRentalStatus`.
3. Neu trang thai hop le, he thong chuyen yeu cau sang `Borrowing`.
4. Khi nguoi dung tra sach, quan tri vien chon thao tac tra.
5. He thong cap nhat `ReturnedAt`, `ActualReturnDate`, trang thai `Returned`.
6. Moi thay doi trang thai duoc ghi vao `RentalLogs` va gui thong bao email neu cau hinh cho phep.

## 5. Yeu thich san pham

1. Nguoi dung bam nut yeu thich tren danh sach hoac chi tiet sach.
2. Neu da dang nhap, `UsersController.ToggleFavorite` goi `ProductFavoriteDraw.Toggle`.
3. Neu chua dang nhap, JavaScript luu danh sach yeu thich vao localStorage.
4. Trang `/yeu-thich` hien thi danh sach local favorite cho khach vang lai.
5. Khi nguoi dung dang nhap, `SyncLocalFavorites` dong bo cac ID san pham local vao bang `ProductFavorites`.

## 6. Quan ly thong tin nha sach va geofence

1. Quan tri vien vao `Admin/WebManager/StoreLocation`.
2. He thong hien thi thong tin nha sach, toa do, ban kinh muon sach va ban do.
3. Quan tri vien cap nhat `Latitude`, `Longitude`, `GeofenceRadius`.
4. Controller parse toa do theo `InvariantCulture` de tranh loi dau cham/dau phay.
5. Du lieu luu vao `StoreLocations` va duoc dung trong quy trinh geofence.
