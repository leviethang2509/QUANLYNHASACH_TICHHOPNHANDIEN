# Ke hoach nang cap QLNhaSach - Version 4

Version 4 tiep tuc tren nen version 3, tap trung sua loi test thuc te va bo sung lop chong gia mao cho xac thuc guong mat.

## 1. Sua loi them sach vao yeu thich

- Tao bang luu sach yeu thich theo tung tai khoan: `ProductFavorites`.
- Khong dung `Tophot` thay cho yeu thich ca nhan nua.
- Them endpoint toggle yeu thich, chan khi chua dang nhap va chan sach khong ton tai.
- Them man hinh `/yeu-thich-{id}` de khach xem danh sach sach da luu.
- Gan nut trai tim tren trang chi tiet sach va cac danh sach san pham vao endpoint moi.

## 2. Sua loi StoreLocation bi chan HTML editor

- Man hinh `/Admin/WebManager/StoreLocation` dang luu HTML tu CKEditor vao `WelcomeMessage`, `AboutContent`, `MissionContent`.
- ASP.NET MVC cu bat `ValidateRequest` nen request co `<p>...</p>` bi chan truoc khi vao action.
- Cho phep rieng action POST `StoreLocation` nhan HTML va tiep tuc luu noi dung editor.

## 3. Bo sung challenge guong mat ngau nhien

- Tao endpoint sinh yeu cau thao tac ngau nhien cho guong mat.
- Moi lan dang nhap bang guong mat hoac xac nhan muon sach phai co challenge token hop le, dung purpose va chua het han.
- UI hien yeu cau theo flow: quay trai, quay phai, ha mieng, cuoi, nhin len, nhin xuong.
- Sau khi camera san sang, client tu gui frame webcam len endpoint kiem tra hanh dong; AI phia Face API phai xac nhan dung hanh dong thi MVC moi cho dung token de xac thuc dang nhap/muon sach.
- Huong tich hop khuyen nghi cho Face API:
  - .NET: OpenCVSharp de xu ly frame/webcam neu xay service .NET.
  - Python/AI service: MediaPipe Face Mesh de lay landmark khuon mat.
  - Co the detect head pose trai/phai/len/xuong, mouth open, smile, eye/mouth landmark va tracking realtime.
  - Browser chi chup/gui frame; server AI quyet dinh `actionMatched=true/false`.
- Log xac thuc tiep tuc ghi `Purpose`, `RequestId`, `LivenessPassed`; challenge web giup chan viec gui lai form cu hoac gui anh khong qua luong thao tac.

## 4. Hien thuc Flask action-check de sua loi khong nhan dien hanh dong

- `QLNhaSach` chi truyen input/frame; server xu ly anh chinh la `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226`.
- Tich hop vao `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`, chay tai `http://localhost:8000/api/face`.
- Them `mediapipe` vao requirements cua server dich.
- Them model `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\models\face_landmarker.task` de MediaPipe Tasks chay duoc tren Python 3.14.
- `/api/face/action-check` tren server dich dung MediaPipe Face Landmarker:
  - Head pose bang `solvePnP` de lay `pitch`, `yaw`, `roll`.
  - Landmark ratio de ho tro quay trai/phai khi yaw yeu va detect `mouth_open`, `smile`.
  - Tra `detected_action`, `metrics`, `action_message` de debug frame that.
- Nguong version 4:
  - `turn_left`: yaw <= -14 do hoac nose_offset <= -0.18.
  - `turn_right`: yaw >= 14 do hoac nose_offset >= 0.18.
  - `look_up`: pitch <= -12 do.
  - `look_down`: pitch >= 12 do.
  - `mouth_open`: mouth_open_ratio >= 0.055.
  - `smile`: smile_ratio >= 1.18.
- Neu webcam bi lat ngang lam trai/phai nguoc, chay Flask voi `FACE_ACTION_FLIP_HORIZONTAL=true`.
- Giữ `success=true` cho frame xu ly duoc nhung chua khop, va chi cho MVC qua khi `action_matched=true`.

## 5. Bo sung CMND/CCCD va Gmail cho luong muon sach

- Sua loi font chu tai `/Admin/ThongKe/MuonTraChuDe` bang cach luu lai view Razor dung UTF-8 va thay cac chuoi mojibake bang tieng Viet dung.
- Dang ky tai khoan co them cac truong CMND/CCCD co ban nhung khong bat buoc: so giay to, ho ten, ngay sinh, dia chi, ngay cap, noi cap.
- Khi muon sach thi hien popup bo sung Gmail, so CMND/CCCD va ho ten tren giay to neu tai khoan con thieu; anh CMND/CCCD/OCR la tuy chon, khong chan luong neu may chu chua cai Tesseract.
- Luu snapshot CMND/CCCD vao `RentalRequests` de admin doi chieu luc duyet.
- Them luu thong tin CMND/CCCD vao `User` de nguoi dung co the cap nhat ho so.
- Them route MVC `/FaceAuth/OcrCmnd` va Flask `/api/face/ocr-cmnd`/`/api/face/qcr-cmnd` de upload CMND/CCCD, OCR thong tin chinh va so khop khuon mat tren giay to voi face profile da dang ky.
- Khong thay doi cac route nhan dien khuon mat hien co; chi dung lai descriptor/profile va them route OCR/doi chieu rieng.
- Gmail thong bao khi admin duyet dung OAuth Gmail hien tai trong `Web.config`: `GmailClientId`, `GmailClientSecret`, `GmailRefreshToken`, `GmailSenderEmail`. Neu cac key con trong hoac `GmailNotificationsEnabled=false`, he thong log skipped va khong lam hong luong duyet.
- Them migration `sql/migrations/20260509_add_identity_card_rental_flow.sql`.
- Them dependency Flask `pytesseract` cho OCR. May chay Flask can cai Tesseract OCR binary va goi ngon ngu `vie` neu muon doc tieng Viet tot; health API phai bao `ocr_available=false` neu chi co package Python nhung thieu binary Tesseract.

## 5.1 Dieu chinh bo sung theo test thuc te

- Man hinh yeu thich hien ten tai khoan dang dang nhap, username va trang thai dang nhap; khi chua dang nhap hien loi moi dang nhap thay vi trang rong.
- Luong dang ky tach 3 buoc: thong tin chung -> CMND/CCCD tuy chon -> xac thuc khuon mat/ket thuc.
- Nut doc CMND/CCCD trong dang ky va popup muon sach chi la ho tro tu dien; neu OCR loi `Tesseract is not installed` thi nguoi dung van nhap tay va tiep tuc.
- `RentalProfileStatus`, `UpdateRentalProfile`, `RequestRental` khong con bat buoc anh CMND/CCCD; chi yeu cau Gmail, so CMND/CCCD va ho ten tren giay to.
- Server Face API trong `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226` cap nhat health `ocr_available` bang cach kiem tra binary Tesseract thuc te.

## 5.2 Nang cap OCR CMND/CCCD bang PaddleOCR

- Chon PaddleOCR lam backend OCR uu tien cho CMND/CCCD vi repo chinh `https://github.com/PaddlePaddle/PaddleOCR` ho tro nhan dien van ban da ngon ngu, 100+ ngon ngu va co pipeline image/PDF -> text/JSON.
- Giu Tesseract la fallback de khong lam hong may chu chua cai PaddleOCR.
- Them `CMND_OCR_BACKEND=auto|paddle|tesseract`, mac dinh `auto`: thu PaddleOCR truoc, khong co thi fallback Tesseract.
- Them `CMND_PADDLE_LANG=vi` de uu tien tieng Viet cho CMND/CCCD.
- API `/api/face/ocr-cmnd` tra them `ocr_backend`, `ocrBackend`, field ngay sinh/ngay cap dung `yyyy-MM-dd` de form HTML date cua QLNhaSach fill duoc.
- Them `OCR_BACKENDS.md` trong du an Face API de luu link GitHub va cach cau hinh backend OCR.

## 5.3 Dong bo CMND/CCCD mat truoc/mat sau voi Flask

- MVC client gui OCR bang multipart `front_file` va `back_file`; giu tuong thich request cu chi co `file`.
- Flask dich `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py` da nhan `front_file/frontFile/front` va `back_file/backFile/back`, route `/api/face/ocr-cmnd` tra `fields`, `face_matched`, `face_confidence`, `ocr_backend`.
- Bo sung snapshot tren `User` va `RentalRequests`: duong dan anh mat truoc/mat sau, ngay sinh, ngay cap, ngay het han, gioi tinh, quoc tich, que quan/noi cu tru, noi cap/co quan cap.
- Popup cap nhat nhanh khi muon sach cho chon rieng mat truoc/mat sau, OCR qua `/FaceAuth/OcrCmnd`, nhap tay van luu duoc neu chua co anh hoac OCR that bai.
- Luong dang ky 3 buoc cho phep doc mat truoc/mat sau de tu dien, sau do tiep tuc sang dang ky khuon mat.
- Dieu kien hoan tat dang ky khuon mat tren client chi chap nhan `success === true` de tranh response loi bi hieu la thanh cong.
- Migration `20260509_add_identity_card_rental_flow.sql` them cac cot bo sung va da ap vao LocalDB `QLNhaSach`.

## 5.4 Dieu chinh ho so, Gmail thong bao va khoa du lieu OCR

- Chi hien mot truong Gmail nhan thong bao tren cac man hinh dang ky/ho so/popup lien quan; server tiep tuc dong bo ve cot `Email` cu de tranh vo cac luong dang nhap, reset mat khau, don hang cu.
- Man hinh ho so hien san 2 o anh CMND/CCCD mat truoc va mat sau; bam vao tung o de chon file, hien preview ngay tren giao dien.
- Khi OCR CMND/CCCD thanh cong va fill du thong tin chinh, dong bo ho ten tren giay to ve ho ten tai khoan, sau do khoa cac truong OCR bang `readonly` de van submit duoc nhung nguoi dung khong sua tay sau khi da xac thuc bang anh.
- Buoc dang ky CMND/CCCD dung cung hanh vi: preview anh, loading khi cho OCR, thong bao thanh cong/that bai, fill va khoa cac truong CMND/CCCD/ho ten khi doc duoc du lieu.
- Them lien ket quan ly sach yeu thich ro rang trong menu tai khoan de nguoi dung quay lai danh sach sach da luu.
- OCR tren UI phai co trang thai dang xu ly, khoa nut trong luc cho API, va hien message chi tiet neu that bai.

## 5.5 Dieu chinh sau test ngay 2026-05-10

- Trang chi tiet sach `/chi-tiet/...` chi cho nguoi dung thay doi `So ngay muon`; so CMND/CCCD va ho ten tren giay to chi doc tu ho so va hien readonly.
- Trang `/thong-tin-ca-nhan-{id}` sap xep lai thu tu: Anh CMND/CCCD -> Doc thong tin -> Thong tin CMND/CCCD -> So dien thoai -> Noi o -> Gmail -> Luu thong tin.
- Neu ho so da co du anh CMND/CCCD hai mat khi load trang thi khoa toan bo thong tin nhap tay; nguoi dung chi cap nhat lai anh CMND/CCCD bang OCR/upload.
- MVC chi luu thong tin/duong dan CMND/CCCD khi OCR tra `success=true`; anh sai loai hoac sai mat se tra message loi thay vi ghi vao ho so.
- Server Flask `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226` bo sung kiem tra anh khong phai CMND/CCCD, anh mat truoc bi dua vao o mat sau va nguoc lai; API tra `IDENTITY_CARD_INVALID`, `IDENTITY_CARD_FRONT_INVALID`, `IDENTITY_CARD_BACK_INVALID`.
- Man hinh dang ky buoc OCR CMND/CCCD hien spinner trong luc cho API va toastr thanh cong/that bai sau khi doc xong.

## 6. Xac minh va lich su

- Chay migration tao bang yeu thich tren DB local.
- Build solution bang MSBuild.
- Kiem tra `GET /api/face/health` tra `model_loaded=true`.
- Health version 4 ky vong tra `action_landmark_backend=tasks.face_landmarker`, `version=1.1.0-action-check`.
- Test action-check bang frame webcam that cho 4 huong trai/phai/len/xuong.
- Test OCR CMND/CCCD bang anh that, xac nhan `fields` co so giay to va `face_matched=true` khi anh giay to khop tai khoan.
- Ghi lai cac thay doi vao `LichSu.md`.
