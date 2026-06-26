# Ke hoach nang cap QLNhaSach - Version 3

Version 3 tiep tuc cac viec con thieu cua version 2 va tap trung vao cac diem nghiep vu dang loi khi test man hinh that.

## 1. Hoan thien logic man hinh nhat ky admin

Can dam bao cac URL sau co logic hien thi that, co thong ke, co empty state va filter hoat dong:

- `/Admin/LogsAdmin/FaceAuth`
- `/Admin/LogsAdmin/Geofence`
- `/Admin/LogsAdmin/Rental`

Yeu cau:

- FaceAuth log hien tong so log, thanh cong, that bai, log trong ngay.
- Geofence log hien tong so log, trong vung, ngoai vung, log trong ngay.
- Rental log hien tong so log, tao yeu cau, duyet/cho muon, tra sach, qua han.
- Cac man hinh khong bi loi khi chua co log.
- Cac link phan trang giu filter hien tai.

## 2. Man hinh admin quan ly thong tin nha sach

Khong duoc gan cung thong tin nha sach trong code. Admin can sua duoc:

- Ten nha sach.
- Dia chi.
- So dien thoai.
- Vi do, kinh do.
- Ban kinh cho phep muon sach.
- Trang thai active.
- Thu tu hien thi.

Can hien map de admin kiem tra vi tri. Giai phap tam thoi dung OpenStreetMap iframe theo toa do trong DB.

Route de xay dung:

- `GET /Admin/WebManager/StoreLocation`
- `POST /Admin/WebManager/StoreLocation`

## 3. Chan muon trung sach dang duoc tai khoan muon

Neu tai khoan da co rental cho cung sach voi trang thai:

- `Pending`
- `Approved`
- `Borrowed`
- `Borrowing`
- `Overdue`

thi khong duoc tao yeu cau muon moi cho sach do.

Yeu cau UI:

- Trang chi tiet sach doi nut `Muon sach` thanh `Dang muon sach` neu tai khoan dang co yeu cau active cho sach do.
- Khong mo form muon neu dang muon.

Yeu cau backend:

- `RentalController.RequestRental` phai kiem tra trung tren server.
- Them endpoint `CheckActiveRental(productId)` cho UI.

## 4. Cap nhat tai lieu va lich su

- Cap nhat file ke hoach version3.
- Ghi lai lich su vao `LichSu.md`.
- Cac file view moi/sua phai luu UTF-8 BOM de tranh loi font voi ASP.NET MVC cu.

## 5. Dieu chinh bo sung ngay 2026-05-09

Can sua tiep theo phan test thuc te:

- `/Admin/WebManager/StoreLocation/3` phai sua dung ban ghi theo id va luu duoc cac thong tin nha sach mo rong.
- Trang `/gioi-thieu/` khong duoc hard-code noi dung; phai doc tu `StoreLocations` de admin co the cap nhat truc tiep.
- Admin co the thay doi icon/logo, email, loi chao, noi dung gioi thieu, muc tieu va cac thong tin lien quan den nha sach.
- Nhat ky xac thuc va nhat ky muon tra phai co logic tao/kiem tra bang log truoc khi ghi/doc de tranh viec khong hien du lieu do bang chua ton tai hoac ghi log bi nuot loi.
- Sau khi sua can build lai solution va ghi lich su vao `LichSu.md`.

## 6. Sua loi runtime va nang cap editor gioi thieu ngay 2026-05-09

Can sua tiep theo phan test tren IIS Express:

- `/Admin/LogsAdmin/FaceAuth` va `/Admin/LogsAdmin/Geofence` dang loi LINQ to Entities vi goi ham C# `NormalizeToExclusive` ben trong expression. Phai tinh moc `toDateExclusive` truoc khi dua vao `Where`.
- Trang `/gioi-thieu/` bi loi font chu. Can dam bao view luu UTF-8 BOM va noi dung dong tu database render dung Unicode.
- Man hinh admin sua thong tin nha sach can gan voi vai tro editor:
  - Cho sua toan bo noi dung gioi thieu bang editor truc quan.
  - Cac truong URL anh/icon/banner co nut chon anh tu CKFinder, khong bat admin tu go URL.
  - Khu map co thanh tim kiem dia chi. Khi chon ket qua thi cap nhat dia chi, vi do, kinh do va preview map.
  - Cac cum tu lien quan den nha sach trong trang gioi thieu phai lay tu cau hinh DB, khong gan cung trong view/controller.
- Sau khi sua can build, chay migration neu can, va ghi lai lich su.
