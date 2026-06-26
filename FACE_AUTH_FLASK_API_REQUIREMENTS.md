# Yeu cau Flask API nhan dien khuon mat

Tai lieu nay tong hop contract ma source ASP.NET MVC trong du an `QLNhaSach` dang can khi goi server Flask nhan dien khuon mat.

## 1. Tong quan luong tich hop

Trinh duyet khong goi Flask truc tiep. Trinh duyet dung webcam trong `BaiTapLon/Scripts/FaceCapture.js`, chup anh JPEG va upload len cac endpoint MVC cua `FaceAuthController`.

`FaceAuthController` se:

- Validate file upload: bat buoc co file, dung luong > 0, toi da theo `FaceAuthMaxUploadBytes`.
- Chi chap nhan file `.jpg`, `.jpeg`, `.png`.
- Luu anh vao `FaceSampleStoragePath`, mac dinh `DataImage/FaceSamples`.
- Goi Flask API bang `BaiTapLon/Services/FaceAuthApiClient.cs`.
- Doc JSON tu Flask va quyet dinh thanh cong khi `success=true` va `confidence >= FaceAuthMinConfidence`.

Base URL dang cau hinh trong `BaiTapLon/Web.config`:

```xml
<add key="FaceAuthAPI" value="http://localhost:8000/api/face"/>
```

Vi vay Flask server can chay duoc tai:

```text
http://localhost:8000/api/face
```

## 2. Endpoint Flask bat buoc

Flask can ho tro 3 endpoint POST sau:

```http
POST /api/face/register
POST /api/face/verify
POST /api/face/authenticate
POST /api/face/action-check
```

Nen co them endpoint health check:

```http
GET /api/face/health
```

## 3. Dinh dang request tu ASP.NET sang Flask

Tat ca endpoint POST dung `multipart/form-data`.

Fields ASP.NET luon gui:

| Field | Kieu | Bat buoc | Ghi chu |
|---|---:|---:|---|
| `file` | file | Co | Anh khuon mat, ten file dang GUID + extension. |
| `userId` | string/long | Co | ID user trong he thong ASP.NET. |
| `user_id` | string/long | Co | Cung gia tri voi `userId`, gui kem de Flask de mapping. |
| `purpose` | string | Co | Ngu canh: `Register`, `Verify`, `MFA`, `Login`, `Rental`. |
| `actionCode` | string | Co voi `/action-check` | Ma hanh dong can kiem tra. |
| `action_code` | string | Co voi `/action-check` | Alias cua `actionCode`. |

Vi source hien tai gui ca `userId` va `user_id`, Flask nen chap nhan ca hai. Neu ca hai cung ton tai, uu tien `user_id` hoac kiem tra hai gia tri phai trung nhau.

Vi du Flask doc request:

```python
uploaded_file = request.files.get("file")
user_id = request.form.get("user_id") or request.form.get("userId")
purpose = request.form.get("purpose", "")
```

## 4. Dinh dang response Flask

ASP.NET doc cac field sau trong JSON:

| Field uu tien | Alias duoc chap nhan | Kieu | Bat buoc | Ghi chu |
|---|---|---:|---:|---|
| `success` | `matched` | bool | Co | Ket qua model/verify. |
| `confidence` | `quality_score` | number | Co | Diem tin cay 0.0 den 1.0. ASP.NET se so sanh voi `FaceAuthMinConfidence`. |
| `userId` | `user_id` | string | Nen co | User ID duoc xu ly. |
| `externalUserId` | `external_user_id`, `face_id` | string | Nen co | ID profile/embedding trong Flask neu co. |
| `livenessPassed` | `liveness_passed` | bool | Nen co | Ket qua chong anh gia/liveness. |
| `errorCode` | `error_code` | string | Khi loi | Ma loi ngan, de ghi log. |
| `errorMessage` | `error`, `message`, `error_message` | string | Khi loi | Noi dung loi de ghi log. |
| `requestId` | `request_id` | string | Nen co | ID trace cho moi request. |
| `purpose` | | string | Nen co | Echo lai purpose neu co. |
| `actionMatched` | `action_matched`, `matched` | bool | Co voi `/action-check` | Ket qua nguoi dung da lam dung hanh dong. |
| `actionCode` | `action_code` | string | Nen co voi `/action-check` | Echo ma hanh dong da kiem tra. |
| `actionMessage` | `action_message` | string | Tuy chon | Noi dung goi y/loi khi chua match. |

Response thanh cong mau:

```json
{
  "success": true,
  "confidence": 0.91,
  "user_id": "12",
  "external_user_id": "face-profile-12",
  "liveness_passed": true,
  "request_id": "9b8f7c6d5e4a4b3c",
  "purpose": "Login"
}
```

Response that bai mau:

```json
{
  "success": false,
  "confidence": 0.42,
  "user_id": "12",
  "liveness_passed": true,
  "error_code": "FACE_NOT_MATCHED",
  "error_message": "Face does not match registered user",
  "request_id": "9b8f7c6d5e4a4b3d",
  "purpose": "Login"
}
```

Neu Flask tra HTTP khac 2xx, ASP.NET se coi la loi va tao response noi bo voi `errorCode = HTTP_<statusCode>`. Tot nhat Flask nen tra HTTP 200 cho cac truong hop model xu ly duoc nhung khong match, va chi tra 4xx/5xx cho loi request/he thong.

## 5. Y nghia tung endpoint

### POST `/api/face/register`

Dung khi nguoi dung dang ky khuon mat.

Input:

- `file`: anh khuon mat.
- `user_id`/`userId`: ID user can gan face profile.
- `purpose`: `Register`.

Xu ly mong doi:

- Detect dung 1 khuon mat hop le.
- Kiem tra chat luong anh: mat ro, khong qua toi/sang, khuon mat du lon.
- Tao/cap nhat embedding cho user.
- Tra `success=true` neu dang ky thanh cong.

### POST `/api/face/verify`

Dung cho cac luong xac thuc 1:1 khi da biet user:

- Xac thuc khuon mat thong thuong: `purpose=Verify`.
- Dang nhap bang username + khuon mat: `purpose=Login`.
- Xac nhan truoc khi muon sach: `purpose=Rental`.

Input:

- `file`: anh khuon mat.
- `user_id`/`userId`: ID user can verify.
- `purpose`: `Verify`, `Login` hoac `Rental`.

Xu ly mong doi:

- Lay embedding da dang ky cua user.
- So khop anh moi voi embedding cua user.
- Tra `confidence` theo thang 0.0 den 1.0.
- `success=true` khi cung mot nguoi va qua nguong model cua Flask.

Luu y: ASP.NET van se ap dung nguong rieng `FaceAuthMinConfidence`, mac dinh `0.75`.

### POST `/api/face/authenticate`

Dung trong luong MFA sau khi dang nhap mat khau.

Input:

- `file`: anh khuon mat.
- `user_id`/`userId`: ID user can xac thuc MFA.
- `purpose`: `MFA`.

Xu ly mong doi tuong tu `/verify`, nhung Flask nen log/trace la luong MFA.

### POST `/api/face/action-check`

Dung trong luong challenge chong gia mao truoc khi dang nhap bang guong mat hoac muon sach.

Input:

- `file`: frame webcam hien tai.
- `user_id`/`userId`: ID user neu MVC da biet user; co the la `0` neu chi can detect hanh dong.
- `purpose`: `Login` hoac `Rental`.
- `action_code`: mot trong cac ma:
  - `turn_left`: quay mat sang trai.
  - `turn_right`: quay mat sang phai.
  - `mouth_open`: ha mieng.
  - `smile`: cuoi.
  - `look_up`: nhin len.
  - `look_down`: nhin xuong.

Xu ly mong doi:

- Detect dung 1 khuon mat.
- Dung MediaPipe Face Mesh hoac engine tuong duong de lay landmark/head pose.
- Tra `action_matched=true` khi frame dung hanh dong duoc yeu cau.
- Tra `action_matched=false` khi chua dung hanh dong; khong nen coi day la loi he thong.

Response mau:

```json
{
  "success": true,
  "action_matched": true,
  "action_code": "turn_left",
  "confidence": 0.86,
  "request_id": "9b8f7c6d5e4a4b3e",
  "purpose": "Login"
}
```

Goi y tich hop:

- Neu xay service .NET: dung OpenCVSharp de doc/xu ly frame, ket hop MediaPipe Face Mesh de detect landmark.
- Neu xay service Python: dung OpenCV + MediaPipe Face Mesh.
- Head pose trai/phai/len/xuong co the tinh tu landmark mui, mat, cam; `mouth_open` tu khoang cach moi tren/duoi; `smile` tu ti le/corner mouth landmark.

## 6. Endpoint health check nen co

```http
GET /api/face/health
```

Response mau:

```json
{
  "status": "ok",
  "service": "face-auth-api",
  "model_loaded": true,
  "storage_ready": true,
  "version": "1.0.0"
}
```

## 7. Cau hinh ASP.NET can khop voi Flask

Trong `BaiTapLon/Web.config`, cac key quan trong:

| Key | Gia tri hien tai | Y nghia |
|---|---|---|
| `FaceAuthAPI` | `http://localhost:8000/api/face` | Base URL Flask. |
| `FaceAuthTimeoutSeconds` | `15` | Timeout moi request sang Flask. |
| `FaceAuthMinConfidence` | `0.75` | Nguong confidence toi thieu de ASP.NET chap nhan. |
| `FaceAuthMaxUploadBytes` | `5242880` | Toi da 5 MB moi anh. |
| `FaceSampleStoragePath` | `DataImage/FaceSamples` | Noi ASP.NET luu anh upload. |
| `EnableFaceMFA` | `true` | Bat buoc face MFA. |
| `AllowPasswordOnlyFallback` | `false` | Khong cho bo qua face bang password-only. |
| `FaceAuthRentalTokenMinutes` | `3` | Thoi han token xac thuc mat khi muon sach. |
| `FaceAuthMaxAttempts` | `5` | So lan sai truoc khi khoa face login. |
| `FaceAuthLockoutMinutes` | `10` | Thoi gian khoa face login. |

Neu Flask chay cong/host khac, sua `FaceAuthAPI`. Vi du:

```xml
<add key="FaceAuthAPI" value="http://127.0.0.1:5000/api/face"/>
```

## 8. Yeu cau server Flask

Server Flask can dam bao:

- Bind host/port dung voi `FaceAuthAPI`, mac dinh de du an goi la `localhost:8000`.
- Nhan `multipart/form-data` voi field file ten `file`.
- Gioi han upload toi thieu 5 MB hoac cao hon cau hinh ASP.NET.
- Ho tro anh JPEG/PNG.
- Response luon la JSON hop le.
- Moi response nen co `request_id` de doi chieu voi bang log ASP.NET.
- Thoi gian xu ly nen duoi `FaceAuthTimeoutSeconds`, mac dinh 15 giay.
- Luu embedding theo `user_id` on dinh, khong phu thuoc ten file upload.
- Neu chua co face profile cua user, tra `success=false`, `error_code=FACE_PROFILE_NOT_FOUND`.
- Neu khong detect duoc mat, tra `success=false`, `error_code=NO_FACE_DETECTED`.
- Neu detect nhieu mat, tra `success=false`, `error_code=MULTIPLE_FACES`.
- Neu anh kem chat luong, tra `success=false`, `error_code=LOW_IMAGE_QUALITY`.
- Nen co liveness detection; neu chua co, van tra `liveness_passed=true/false` ro rang theo kha nang hien tai.

## 8.1. Yeu cau rieng cho nhan dien hanh dong version 4

Do luong Login/Rental hien tai bat buoc qua `/api/face/action-check`, Flask khong duoc tra `action_matched=true` theo cach gia lap. Endpoint nay can nhan frame webcam that va detect hanh dong theo landmark khuon mat.

Vi du an `QLNhaSach` chi truyen input/frame sang Face API, server xu ly anh thuc te dat tai:

```text
D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226
```

Da tich hop vao server Flask dich:

- File chay: `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\app.py`.
- Model MediaPipe Tasks: `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\models\face_landmarker.task`.
- Dependency `mediapipe` da them vao `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\requirements.txt`.

Chay server dich:

```bash
cd /d D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226
python app.py
```

Cai dependency neu may moi chua co:

```bash
pip install -r requirements.txt
```

Luu y: thu muc `QLNhaSach` khong xu ly anh truc tiep; MVC chi goi URL `FaceAuthAPI`.

Neu can chay Flask mau rieng de test doc lap thi co the dung `face_auth_api/app.py`, nhung luong chinh cua he thong nen chay server trong `NHANDIENKHUONMAT-new07040226`.

Health dung khi san sang phai co:

```json
{
  "status": "ok",
  "model_loaded": true,
  "action_model_loaded": true,
  "action_landmark_backend": "tasks.face_landmarker",
  "version": "1.1.0-action-check"
}
```
Hoac neu InsightFace dang lazy-load, `face_model_loaded=false` luc moi start la binh thuong; khi register/verify lan dau thi model face se duoc load.

Thuat toan action-check toi thieu:

| Action | Tin hieu can detect | Nguong goi y |
|---|---|---:|
| `turn_left` | yaw am hoac mui lech ngang qua trai | `yaw <= -14 do` hoac `nose_offset <= -0.18` |
| `turn_right` | yaw duong hoac mui lech ngang qua phai | `yaw >= 14 do` hoac `nose_offset >= 0.18` |
| `look_up` | pitch am | `pitch <= -12 do` |
| `look_down` | pitch duong | `pitch >= 12 do` |
| `mouth_open` | khoang cach moi tren/duoi chia chieu cao mat | `mouth_open_ratio >= 0.055` |
| `smile` | do rong mieng chia khoang cach hai mat | `smile_ratio >= 1.18` |

Neu camera/browser bi mirror va trai/phai bi nguoc, dat bien moi truong:

```bash
set FACE_ACTION_FLIP_HORIZONTAL=true
python app.py
```

Response `/action-check` nen co them field debug de test thu cong:

```json
{
  "success": true,
  "action_matched": false,
  "action_code": "turn_left",
  "detected_action": "turn_right",
  "action_message": "Detected turn_right; waiting for turn_left",
  "metrics": {
    "pitch": 1.2,
    "yaw": 18.4,
    "nose_offset": 0.21,
    "mouth_open_ratio": 0.02,
    "smile_ratio": 0.9
  }
}
```

`success=true` nghia la server xu ly frame thanh cong; MVC chi cho qua khi `action_matched=true`.

## 9. Goi thu bang curl

Dang ky:

```bash
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@face.jpg" \
  -F "user_id=12" \
  -F "userId=12" \
  -F "purpose=Register"
```

Verify:

```bash
curl -X POST http://localhost:8000/api/face/verify \
  -F "file=@face.jpg" \
  -F "user_id=12" \
  -F "userId=12" \
  -F "purpose=Login"
```

Action check:

```bash
curl -X POST http://localhost:8000/api/face/action-check \
  -F "file=@frame.jpg" \
  -F "user_id=12" \
  -F "purpose=Login" \
  -F "action_code=turn_left"
```

MFA:

```bash
curl -X POST http://localhost:8000/api/face/authenticate \
  -F "file=@face.jpg" \
  -F "user_id=12" \
  -F "userId=12" \
  -F "purpose=MFA"
```

## 10. Cac luong trong du an dang phu thuoc Flask

### Dang ky khuon mat

View `Users/RegisterFace.cshtml` upload anh len MVC endpoint:

```text
POST /FaceAuth/RegisterFace
```

MVC goi Flask:

```text
POST /api/face/register
```

### MFA khuon mat

View `Users/LoginMFA.cshtml` va partial `_FaceMFA.cshtml` upload anh len MVC endpoint:

```text
POST /FaceAuth/AuthenticateFace
```

MVC goi Flask:

```text
POST /api/face/authenticate
```

### Dang nhap bang khuon mat

View `Users/Login.cshtml` gui `userName` va anh len MVC endpoint:

```text
POST /FaceAuth/AuthenticateFaceLogin
```

MVC tim user theo username, lay `IDUser`, sau do goi Flask:

```text
POST /api/face/action-check
purpose=Login
action_code=<challenge>
```

Khi `action_matched=true`, MVC moi cho dung token challenge de goi:

```text
POST /api/face/verify
purpose=Login
```

### Xac nhan khuon mat khi muon sach

View `Product/Detail.cshtml` gui `productId` va anh len MVC endpoint:

```text
POST /FaceAuth/VerifyRentalFace
```

MVC goi Flask:

```text
POST /api/face/action-check
purpose=Rental
action_code=<challenge>
```

Khi `action_matched=true`, MVC moi goi:

```text
POST /api/face/verify
purpose=Rental
```

Neu thanh cong, MVC tra ve `faceToken`. Sau do view goi:

```text
POST /Rental/RequestRental
```

voi `faceToken`. Flask khong can tao token muon sach; token nay do ASP.NET tao va quan ly.

## 11. Checklist chap nhan

- `GET /api/face/health` tra `status=ok`.
- `/api/face/register` nhan anh + user ID va tao/cap nhat face profile.
- `/api/face/verify` tra `success=true`, `confidence >= 0.75` voi dung user.
- `/api/face/verify` tra `success=false` voi sai user, khong co profile, khong co mat, nhieu mat.
- `/api/face/authenticate` hoat dong tuong tu verify cho luong MFA.
- Tat ca response JSON co `success`, `confidence`, `request_id`.
- Loi model/request co `error_code` va `error_message`.
- Xu ly moi request duoi 15 giay.
- Khong can CORS neu Flask chi duoc goi tu ASP.NET backend tren cung may/server.
