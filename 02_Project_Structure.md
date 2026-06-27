# 02. Project Structure

This document breaks down the physical and logical structure of the `DongTrieuBookStore` Visual Studio solution.

## 1. Directory Tree Overview

Below is the directory mapping of the main workspace elements:

```text
D:\DUANNGHIENCUU\QLNhaSacha\
├── DongTrieuBookStore.sln                 # Main Visual Studio Solution File
├── db.sql                                 # SQL script containing database schemas
├── face_auth_api/                         # Python Flask Facial Auth & OCR Service
│   ├── app.py                             # Main Flask application logic
│   ├── face_profiles/                     # Folder holding enrolled JSON face descriptors
│   ├── models/                            # MediaPipe task models (face_landmarker.task)
│   └── requirements.txt                   # Python dependencies (mediapipe, pytesseract, etc.)
├── CommomSentMail/                        # Class Library for sending emails
│   ├── MailHelper.cs                      # SMTP client configuration and transmission
│   └── CommomSentMail.csproj              # Project configuration
├── Common/                                # Shared infrastructure components
│   └── Repositories/                      # Repositories shared between web and tests
│       └── LogRepository.cs               # Logic for logging Face, Geofence, and Rentals
├── Mood/                                  # Business Logic and Database Model project
│   ├── EF2/                               # Entity Framework DbContext and Entities
│   │   ├── QuanLySachDBContext.cs         # Principal DB context for business domain
│   │   ├── LogDbContext.cs                # Secondary DB context for log separation
│   │   ├── User.cs                        # Domain representation of users
│   │   ├── Sanpham.cs                     # Domain representation of books
│   │   ├── StoreLocation.cs               # physical store geolocation details
│   │   ├── RentalRequest.cs               # Book rental details and identity upload
│   │   └── [Entity].cs                    # Other database entities (Category, Orders, etc.)
│   ├── Draw/                              # Data Access Objects (DAO / Repositories)
│   │   ├── UserDraw.cs                    # Direct query operations on Users and Orders
│   │   ├── SanphamDraw.cs                 # Query and write actions for Books
│   │   └── [Entity]Draw.cs                # DAO classes for remaining domain objects
│   └── Mood.csproj                        # Class library configuration
├── BaiTapLon/                             # Presentation Layer (ASP.NET MVC 5 Web App)
│   ├── App_Start/                         # Setup scripts (RouteConfig, BundleConfig)
│   ├── Areas/                             # MVC sub-areas
│   │   └── Admin/                         # Back-office administration panel
│   │       ├── Controllers/               # Admin specific control logic
│   │       ├── Models/                    # ViewModels for Admin login and log filtering
│   │       └── Views/                     # Layout templates and management dashboards
│   ├── Controllers/                       # End-user portal Controllers
│   │   ├── FaceAuthController.cs          # Orchestrator for face verification, enrollment, and CMND OCR
│   │   ├── RentalController.cs            # Book renting validation, workflow and return logic
│   │   ├── GeofenceController.cs          # User coordinates evaluation
│   │   └── UsersController.cs             # Registration, legacy auth, and Face MFA enforcement
│   ├── Models/                            # View-specific request binders (RegisterModel, etc.)
│   ├── Services/                          # Integration Clients
│   │   ├── FaceAuthApiClient.cs           # HTTP wrapper communicating with face_auth_api
│   │   ├── FaceRentalTokenService.cs      # Volatile memory-token validator for rental workflow
│   │   ├── GmailNotificationService.cs    # Mail formatting service for rental updates
│   │   └── StoreLocationService.cs        # Retrieval helper for active geofenced store
│   ├── Web.config                         # Global app configuration and connection strings
│   └── DongTrieuBookStoreOnline.csproj    # Main project file
└── Tests/                                 # Unit Tests project
    ├── FaceAuthControllerTests.cs         # Verification scenarios for face controller
    ├── GeofenceControllerTests.cs         # Validation test for geofencing boundary logic
    ├── RentalControllerTests.cs           # Business logic test for book renting states
    └── Tests.csproj                       # Unit testing configuration
```

## 2. Layer Responsibilities

| Project / Directory | Responsibility |
| :--- | :--- |
| **`BaiTapLon`** | Presentation layer. Renders HTML views, binds incoming HTTP requests, handles session state, and queries outer services. |
| **`Mood.EF2`** | Database schema representation using EF6. Includes entities and fluent mappings for tables. |
| **`Mood.Draw`** | Data Access Layer (DAOs). Contains specific functions to query tables, update inventory, check credentials, and write transaction records. |
| **`Common`** | Core infrastructure including logs repo. Implements direct SQL executions to guarantee table availability for audit trails. |
| **`CommomSentMail`** | Mailer service utilizing system SMTP settings to dispatch transactional notifications. |
| **`face_auth_api`** | Python computer vision service. Enrollment, matching, and OCR processing. |
| **`Tests`** | Automated testing project containing unit tests checking control flow responses. |
