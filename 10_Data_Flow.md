# 10. Data Flow

This document details the movement of data throughout the bookstore and authentication subsystems.

---

## 1. General Processing Paths

### Transactional checkout flow:
```text
Client Browser (HTML Form)
      ↓
Controller Action (CartController.Payment)
      ↓
Model Validation (Model Binding)
      ↓
DAO Query Verification (SanphamDraw - checks remaining stock)
      ↓
EF DBContext Mapping (QuanLySachDBContext - builds Orders and Order_Detail rows)
      ↓
SQL Server Database (Committed transaction rows)
      ↓
SMTP Dispatcher (Dispatches email alert to customer)
```

---

## 2. Facial Authentication and OCR Flow

The diagram below details the data flow of the Face Verification & OCR engine:

```mermaid
graph TD
    Client[Web Client] -->|Upload front/back photos| WebApp[ASP.NET Web MVC - BaiTapLon]
    WebApp -->|Saves temporary files| Disk[Physical Disk Storage]
    WebApp -->|Sends file streams| ApiClient[FaceAuthApiClient]
    ApiClient -->|HTTP Multipart POST| Flask[Python Flask API - app.py]
    
    subgraph face_auth_api
        Flask -->|Decodes Stream| CV2[OpenCV Image Decoder]
        CV2 -->|Bitmap Array| MediaPipe[MediaPipe Face Mesh]
        CV2 -->|Bitmap Array| Tesseract[Tesseract OCR Engine]
        MediaPipe -->|Landmark Descriptors| Verification[Emb Similarity Checker]
        Tesseract -->|Raw text| Parser[Regex Identity Parser]
    end
    
    Verification -->|Match status & confidence| ApiResponse[JSON Payload]
    Parser -->|Identity fields metadata| ApiResponse
    ApiResponse -->|HTTP Response JSON| WebApp
    WebApp -->|Binds values to DB Entity| EF[Entity Framework 6]
    EF -->|Updates User table columns| SQL[(SQL Server)]
```

---

## 3. Data Transformation Formats
- **Form Data**: Captured from user registration forms or webcam capture scripts.
- **Multipart Form-Data**: Sent over HTTP from the Web App to the Flask server containing files (`file`, `front_file`, `back_file`) and metadata fields (`user_id`, `purpose`, `action_code`).
- **JSON Metadata**: Returned by the Flask server to C# Web services (containing confidence scores, match flags, character segments parsed from ID cards).
- **Relational Tables**: Stored inside MS SQL Server using corresponding database data types (e.g. `DateTime` fields mapped from OCR date formats, strings mapped from names).
