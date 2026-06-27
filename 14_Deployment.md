# 14. Deployment & Environment Setup

This document provides a guide for deploying the application on a Windows IIS environment with the Python Flask API.

---

## 1. Environment Requirements

### Web Server (Windows Server)
- **IIS 8.0+** with ASP.NET 4.8 enabled.
- **.NET Framework 4.8 runtime**.
- **SQL Server 2012+** (Express, Standard, or Developer).

### Face Auth Microservice Server
- **Python 3.8 - 3.11** installation.
- **Tesseract OCR Windows binary** (installed to `C:\Program Files\Tesseract-OCR\`).
- **MediaPipe face landmarker task model**: `face_landmarker.task` downloaded and placed under `/face_auth_api/models/`.

---

## 2. Database Provisioning
1. Open SQL Server Management Studio (SSMS) and connect to your SQL Server instance.
2. Create a new database named `QLTV_BTL`.
3. Open and run the `db.sql` script located in the project root to create the tables.
4. Verify that tables such as `User`, `Sanpham`, `Category`, and `StoreLocations` are created.
5. The logging tables (`FaceAuthLogs`, `GeofenceLogs`, `RentalLogs`) will be generated automatically on system startup by `EnsureLogTables()` in `LogRepository.cs`.

---

## 3. Configuring the Python Flask API
1. Navigate to `/face_auth_api/`.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set configuration parameters in the environment:
   ```cmd
   set FACE_AUTH_PORT=8000
   set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   set FACE_AUTH_MAX_UPLOAD_BYTES=5242880
   ```
4. Start the server (or run it as a service using NSSM):
   ```bash
   python app.py
   ```
5. Confirm the API is running by hitting `http://localhost:8000/`.

---

## 4. Deploying the ASP.NET Web App to IIS
1. Open the solution in Visual Studio. Publish `DongTrieuBookStoreOnline` to a local folder.
2. Open IIS Manager. Add a new website pointing to the published folder.
3. Configure the IIS Application Pool:
   - **.NET CLR Version**: `.NET CLR Version v4.0.30319`
   - **Managed Pipeline Mode**: `Integrated`
   - **Identity**: Ensure it has write permissions to local upload folders: `/DataImage/IdentityCards` and `/DataImage/FaceSamples`.
4. Edit the published `Web.config`:
   - Set the `QuanLySachDBContext` and `DefaultConnection` connection strings to point to your SQL Server instance.
   - Update `FaceAuthAPI` to match the URL of the running Flask service (e.g., `http://localhost:8000/api/face`).
5. Open your browser and navigate to the configured site binding to test the application.
