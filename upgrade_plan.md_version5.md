# Ke hoach nang cap QLNhaSach - Version 5

Version 5 ke thua version 4, tap trung lam ro luong CMND/CCCD va Gmail nhan thong bao de nguoi dung khong bi chan dot ngot khi muon sach.

## 1. Ke thua version 4

- Giu nguyen luong xac thuc khuon mat, challenge hanh dong va Face API rieng tai `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`.
- Giu route OCR CMND/CCCD o MVC va Flask, QLNhaSach chi gui input anh va nhan JSON ket qua.
- Giu yeu cau khi muon sach phai co thong tin CMND/CCCD va anh CMND/CCCD da doi chieu voi khuon mat tai khoan.

## 2. Dang ky tai khoan co buoc OCR CMND/CCCD tuy chon

- Sau khi nhap thong tin dang ky, nguoi dung co the chon anh CMND/CCCD de OCR.
- Buoc CMND/CCCD khong bat buoc; neu co anh thi he thong goi `/FaceAuth/OcrCmndDraft` de doc nhap cac truong chinh.
- Them truong `NotificationEmail` de nguoi dung nhap Gmail nhan thong bao muon/tra/qua han.
- Neu khong nhap Gmail rieng, he thong mac dinh dung email tai khoan.

## 3. Quan ly thong tin khach hang

- Man hinh ho so khach hang hien Gmail nhan thong bao, thong tin CMND/CCCD, link anh CMND/CCCD neu da co va do khop khuon mat.
- Nguoi dung co the tai anh CMND/CCCD len de OCR va tu fill thong tin, sau do luu vao ho so.

## 4. Muon sach voi popup cap nhat ho so

- Khi bam `Muon sach`, truoc khi vao buoc ngay muon/khuon mat, client goi `/Rental/RentalProfileStatus`.
- Neu thieu Gmail nhan thong bao, so CMND/CCCD, ho ten tren giay to hoac anh CMND/CCCD thi hien popup cap nhat.
- Popup cho nhap Gmail, CMND/CCCD, tai anh CMND/CCCD va goi OCR.
- Khi luu popup, server goi Face API de so khop khuon mat tren CMND/CCCD voi face profile da dang ky.
- Chi khi ho so du thong tin va anh CMND/CCCD hop le moi tiep tuc luong muon sach.

## 5. Gmail thong bao

- `GmailNotificationService` uu tien gui den `User.NotificationEmail`, neu trong thi fallback ve `User.Email`.
- Khi admin duyet muon sach, event `ApproveSuccess` tiep tuc gui thong bao muon thanh cong.

## 6. Database va kiem thu

- Them cot `NotificationEmail` vao bang `User`.
- Migration: `sql/migrations/20260509_add_notification_email_version5.sql`.
- Can test:
  - Dang ky: chon anh CMND/CCCD, OCR fill du lieu, submit van khong bat buoc CMND.
  - Ho so: thay Gmail thong bao, CMND/CCCD, anh da luu.
  - Muon sach: tai khoan thieu thong tin hien popup cap nhat, tai khoan du thong tin di tiep.
  - Gmail: admin duyet gui den `NotificationEmail`.
## Version 5 - Product review, local favorites, and video tabs

- Favorite books now support guests by saving selected product ids in browser `localStorage`; logged-in users still use account-backed favorites.
- Admin product create/edit can upload an attached review file and save a YouTube link per book.
- Product detail can open the admin review file in a Bootstrap popup, shows a dynamic YouTube tab, and accepts one rating/comment per logged-in customer.
- Added migration `sql/migrations/20260510_add_product_reviews_version5.sql` for product review metadata and `ProductReviews`.

## Version 5 - Bo sung quan ly yeu thich, logs va thong bao muon sach

- Icon tim tren header client/mobile dieu huong den trang quan ly sach yeu thich theo user dang nhap; khach chua dang nhap vao trang yeu thich local.
- Nut them/bot yeu thich tren client chi hien icon tim, khong chen text vao nut icon.
- Trang yeu thich cua user dang nhap hien dang bang giong gio hang, co them vao gio va bo yeu thich theo tung dong.
- Admin va client dung chung tai khoan dang nhap; khi dang nhap bang trang admin, he thong kiem tra quyen de vao admin hoac quay ve client.
- Layout admin co nut chuyen nhanh sang trang khach hang; header client hien nut quay ve admin neu tai khoan dang co quyen admin.
- File review/demo sach duoc stream qua `Product/ReviewFile` voi `Content-Disposition: inline` de uu tien xem tren trinh duyet.
- Logs FaceAuth tu can chinh page ve trang hop le de tranh truong hop tong co du lieu nhung bang rong do page vuot qua tong trang.
- Logs Rental co them timeline truc quan theo tung khach hang va ma muon sach.
- Thong ke `Admin/ThongKe/MuonTraChuDe` duoc ghi lai dung tieng Viet/UTF-8.
- Gmail thong bao muon sach uu tien Gmail API neu du OAuth, neu chua co token thi fallback SMTP Gmail dang cau hinh trong `Web.config`; bat `GmailNotificationsEnabled=true`.
