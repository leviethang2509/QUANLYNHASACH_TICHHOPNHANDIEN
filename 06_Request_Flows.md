# 06. Request & Execution Flows

This document details the execution paths of major features with step-by-step descriptions and Sequence Diagrams.

---

## 1. User Registration & OCR ID Verification Flow
```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant UsersCtrl as UsersController
    participant FaceClient as FaceAuthApiClient
    participant Flask as Flask OCR/Face API
    participant UserDAO as UserDraw (DAO)
    participant DB as SQL Database

    User->>UsersCtrl: POST /Users/RegisterUser (Form + CMND uploads)
    UsersCtrl->>FaceClient: OcrIdentityCardAsync(frontPath, backPath, userId, "Register")
    FaceClient->>Flask: POST /api/face/ocr-cmnd
    Note over Flask: Extract text & match similarity
    Flask-->>FaceClient: JSON (parsed fields, face_matched)
    FaceClient-->>UsersCtrl: JObject
    alt Validation Successful
        UsersCtrl->>UserDAO: AddUser(model + parsed ID Details)
        UserDAO->>DB: INSERT INTO dbo.User
        DB-->>UserDAO: Success
        UserDAO-->>UsersCtrl: Returns ID
        UsersCtrl-->>User: JSON (success = true)
    else Validation Failed
        UsersCtrl-->>User: JSON (success = false)
    end
```

---

## 2. Login Flow with Face MFA Enforcement
```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant UsersCtrl as UsersController
    participant UserDAO as UserDraw (DAO)
    participant FaceCtrl as FaceAuthController
    participant FaceClient as FaceAuthApiClient
    participant Flask as Flask Face API
    participant DB as SQL Database

    User->>UsersCtrl: POST /Users/Login (Username + Password)
    UsersCtrl->>UserDAO: LoginHomeUser(user, md5(pass))
    UserDAO->>DB: SELECT FROM User
    DB-->>UserDAO: User Entity
    UserDAO-->>UsersCtrl: Match Success (e.g. 1)
    
    alt EnableFaceMFA == true and User Has Face Registered
        UsersCtrl-->>User: JSON (success = true, mfaRequired = true)
        Note over User: Capture facial photo
        User->>FaceCtrl: POST /FaceAuth/VerifyFace
        FaceCtrl->>FaceClient: VerifyAsync(tempPath, userId)
        FaceClient->>Flask: POST /api/face/verify
        Flask-->>FaceClient: JSON (matched, confidence)
        FaceClient-->>FaceCtrl: FaceAuthResponse
        FaceCtrl->>DB: INSERT INTO FaceAuthLogs
        alt Face Match Score >= Threshold
            FaceCtrl-->>User: JSON (success = true, redirectUrl)
        else Face Match Score < Threshold
            FaceCtrl-->>User: JSON (success = false)
        end
    else MFA Disabled
        UsersCtrl-->>User: JSON (success = true, redirectUrl)
    end
```

---

## 3. Geofenced Book Rental & Liveness Verification Flow
```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant GeoCtrl as GeofenceController
    participant StoreService as StoreLocationService
    participant FaceCtrl as FaceAuthController
    participant FaceClient as FaceAuthApiClient
    participant Flask as Flask Face API
    participant TokenService as FaceRentalTokenService
    participant RentalCtrl as RentalController
    participant DB as SQL Database

    User->>GeoCtrl: POST /Geofence/CheckGeofence (lat, lon)
    GeoCtrl->>StoreService: GetActiveStore()
    StoreService->>DB: SELECT * FROM StoreLocations
    DB-->>StoreService: Store Coordinates
    GeoCtrl->>GeoCtrl: Compute distance (Haversine)
    GeoCtrl->>DB: INSERT INTO GeofenceLogs
    alt User is within Geofence Radius
        GeoCtrl-->>User: JSON (inZone = true)
        User->>FaceCtrl: POST /FaceAuth/InitiateRentalAuth
        FaceCtrl-->>User: JSON (success, actionCode)
        Note over User: Capture selfie matching challenge action
        User->>FaceCtrl: POST /FaceAuth/VerifyRentalAuth (actionImage)
        FaceCtrl->>FaceClient: CheckActionAsync
        FaceClient->>Flask: POST /api/face/action-check
        Flask-->>FaceClient: JSON (matched, actionMatched)
        FaceClient-->>FaceCtrl: FaceAuthResponse
        FaceCtrl->>TokenService: Create(userId, productId)
        Note over TokenService: Save token in memory cache
        TokenService-->>FaceCtrl: checkoutToken
        FaceCtrl-->>User: JSON (success, token = checkoutToken)
        User->>RentalCtrl: POST /Rental/RequestRental (token)
        RentalCtrl->>TokenService: ValidateAndConsume(token)
        TokenService-->>RentalCtrl: Token Validated
        RentalCtrl->>DB: Decrease stock & insert RentalRequest
        RentalCtrl->>DB: INSERT INTO RentalLogs
        RentalCtrl-->>User: JSON (success = true)
    else User is Out of Geofence
        GeoCtrl-->>User: JSON (inZone = false)
    end
```
