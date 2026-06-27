# 05. API Endpoints

This document maps the API endpoints exposed by both the ASP.NET Web App and the Python Flask backend service.

---

## 1. Web Portal Audit Log API (Admin Restricted)
- **Base Controller**: `BaiTapLon.Controllers.Api.LogsController`
- **Authentication**: Admin cookie session with role validation (`[Authorize(Roles = "Admin")]`).

| HTTP Method | Route | Parameters | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/Api/Logs/Face` | `page` (int), `pageSize` (int), `userId` (long?), `action` (str), `fromDate` (date?), `toDate` (date?), `result` (bool?) | `JSON` (`PagedResult<FaceAuthLog>`) | Retrieves filtered facial authentication records. |
| **GET** | `/Api/Logs/Geofence` | `page` (int), `pageSize` (int), `userId` (long?), `storeId` (int?), `fromDate` (date?), `toDate` (date?), `inZone` (bool?) | `JSON` (`PagedResult<GeofenceLog>`) | Retrieves geofencing access control attempts. |
| **GET** | `/Api/Logs/Rental` | `page` (int), `pageSize` (int), `userId` (long?), `rentalId` (int?), `action` (str), `fromDate` (date?), `toDate` (date?) | `JSON` (`PagedResult<RentalLog>`) | Retrieves physical books lending history logs. |

---

## 2. Geofence Boundary Check API
- **Base Controller**: `BaiTapLon.Controllers.GeofenceController`

| HTTP Method | Route | Parameters | Response | Authentication | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/Geofence/CheckGeofence` | `lat` (decimal?), `lon` (decimal?), `userId` (int) | `JSON` (proximity status, distance, store name, error string) | Public (Reads coordinate inputs from browser GPS) | Computes distance using Haversine formula against store coordinate records. |

---

## 3. Facial Verification & OCR Integration API
- **Base Controller**: `BaiTapLon.Controllers.FaceAuthController`

| HTTP Method | Route | Body / Upload Files | Response | Auth Requirement | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/FaceAuth/OcrCmndDraft` | `front_file` (image), `back_file` (image) | `JSON` (parsed fields map, paths, error string) | Public | Performs trial OCR extraction from identity cards without updating user profile. |
| **POST** | `/FaceAuth/OcrCmnd` | `front_file` (image), `back_file` (image) | `JSON` (success status, fields map, error) | User Session Required | Extracts card data, matches card photo against user avatar, updates database fields. |
| **POST** | `/FaceAuth/RegisterFace` | `file` (image payload) | `JSON` (success status, confidence score, error) | User Session Required | Enrolls facial descriptors into filesystem-based cache registry. |
| **POST** | `/FaceAuth/VerifyFace` | `file` (image payload) | `JSON` (success status, similarity value, error) | User Session Required | Authenticates user face profile against enrolled registry templates. |
| **POST** | `/FaceAuth/InitiateRentalAuth` | Query string: `productId` (long) | `JSON` (success, actionCode e.g. `look_left`, message) | User Session Required | Generates liveness check challenges for the book checkout transaction. |
| **POST** | `/FaceAuth/VerifyRentalAuth` | `productId` (long), `token` (str), `actionImage` (file) | `JSON` (success status, validationToken, message) | User Session Required | Evaluates liveness image challenge, returning a transient rental verification token. |

---

## 4. Python Flask Service Internal Endpoints (`face_auth_api`)
- **Server File**: `face_auth_api/app.py`
- **Execution Port**: Defaults to `8000` (Configured in Web app config as `http://localhost:8082/api/face`)

| HTTP Method | Route | Body Inputs | Response Payload | Description |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/face/register` | `user_id` (str), `file` (multipart upload) | `JSON` (success status, embedding dimension vector) | Registers profile face embedding vectors. |
| **POST** | `/api/face/verify` | `user_id` (str), `file` (multipart upload) | `JSON` (success status, confidence score, match status) | Compares current image embed vector with registered file template. |
| **POST** | `/api/face/action-check` | `user_id` (str), `file` (multipart), `action_code` (str) | `JSON` (success status, liveness validation flags) | Evaluates eye/mouth keypoint landmarks to confirm user movement directions. |
| **POST** | `/api/face/ocr-cmnd` | `user_id` (str), `front_file` (file), `back_file` (file) | `JSON` (success, parsed fields: DOB, Name, ID, address) | Runs Tesseract OCR on ID card files and matches the card photo with the user profile. |
