# UML Screen Navigation Flow Diagram

This document contains a comprehensive User Interface (UI) Navigation Flow Diagram showing all screens of the bookstore system (Client Portal and Admin Dashboard) and how they link together.

---

## 1. Full Screen Navigation Diagram

```mermaid
flowchart TD
    %% Define Styles
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef public fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef gate fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef customer fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef admin fill:#ffebee,stroke:#d32f2f,stroke-width:2px;

    %% Client Public Screens
    subgraph PortalPublic [Public Client Portal]
        Home["Trang Chủ (Home/Index)"]:::public
        Register["Trang Đăng Ký (Users/Register)<br/>[Upload CMND/CCCD + Chụp Selfie]"]:::public
        Login["Trang Đăng Nhập (Users/Login)<br/>[Nhập Acc/Pass + CAPTCHA]"]:::public
        BookDetail["Chi Tiết Sách (Product/Detail)<br/>[Xem PDF Review, Xem Trailer]"]:::public
        Cart["Giỏ Hàng (Cart/Index)<br/>[Cập nhật giỏ hàng]"]:::public
        Checkout["Thanh Toán (Cart/Payment)<br/>[Điền thông tin giao hàng, Chọn thanh toán]"]:::public
        Contact["Trang Liên Hệ / Giới Thiệu"]:::public
    end

    %% Security Gateways
    subgraph Gateways [Identity & Verification Gateways]
        MfaLogin["Xác Thực Login MFA (FaceAuth/MfaLogin)<br/>[Chụp Webcam đối sánh khuôn mặt]"]:::gate
        RentalVerify["Thách Thức Liveness Mượn Sách (FaceAuth/RentalVerify)<br/>[Chụp hành động Smile/Look Left...]"]:::gate
    end

    %% Client Private Protected Screens
    subgraph PortalPrivate [Private Customer Portal]
        MyRentals["Lịch Sử Mượn Sách (Rental/MyRentals)<br/>[Xem trạng thái, Yêu cầu trả sách]"]:::customer
    end

    %% Admin Screens
    subgraph PortalAdmin [Admin Dashboard Panel]
        AdminLogin["Đăng Nhập Admin (Admin/Login)"]:::admin
        AdminHome["Dashboard Thống Kê (Admin/Home/Index)<br/>[Xem doanh thu, biểu đồ]"]:::admin
        AdminUsers["Quản Lý User (Admin/User/Index)<br/>[Xem danh sách, Cấp quyền, Khóa]"]:::admin
        AdminBooks["Quản Lý Sách (Admin/SanPham/Index)<br/>[Thêm, sửa, xóa sách, Upload File]"]:::admin
        AdminCats["Quản Lý Thể Loại (Admin/Category/Index)"]:::admin
        AdminOrders["Quản Lý Đơn Hàng (Admin/HoaDon/Index)<br/>[Duyệt giao hàng, thanh toán]"]:::admin
        AdminRentals["Quản Lý Mượn Sách (Admin/RentalAdmin/Index)<br/>[Phê duyệt/Từ chối, nhận trả sách]"]:::admin
        AdminStores["Quản Lý Geofence Chi Nhánh (Admin/StoreLocation/Index)"]:::admin
        AdminLogs["Nhật Ký Hệ Thống (Admin/LogsAdmin/Index)<br/>[Audit Face, Geofence, Rental logs]"]:::admin
    end

    %% Navigation Links / Transitions
    Home -->|"1. Click Đăng ký"| Register
    Home -->|"2. Click Đăng nhập"| Login
    Home -->|"3. Chọn sách"| BookDetail
    Home -->|"4. Xem Giỏ Hàng"| Cart
    Home -->|"5. Xem Liên hệ"| Contact

    Register -->|"Đăng ký thành công"| Login
    
    Login -->|"Nhập đúng Acc/Pass & bật MFA"| MfaLogin
    Login -->|"Nhập đúng Acc/Pass & tắt MFA"| Home
    MfaLogin -->|"Xác thực mặt khớp"| Home

    Cart -->|"Click Thanh toán"| Checkout
    Checkout -->|"Đặt hàng thành công (Momo/NganLuong/COD)"| Home

    BookDetail -->|"Click Thêm vào giỏ"| Cart
    
    %% Geofence & Rental Verification Navigation
    BookDetail -->|"Click Mượn sách (Yêu cầu GPS Geofence)"| RentalVerify
    RentalVerify -->|"Vượt qua Liveness Challenge"| MyRentals

    MyRentals -->|"Click Trả sách"| MyRentals

    %% Admin Navigation Links
    AdminLogin -->|"Nhập đúng tài khoản Admin"| AdminHome
    
    AdminHome -->|"Menu Điều Hướng"| AdminUsers
    AdminHome -->|"Menu Điều Hướng"| AdminBooks
    AdminHome -->|"Menu Điều Hướng"| AdminCats
    AdminHome -->|"Menu Điều Hướng"| AdminOrders
    AdminHome -->|"Menu Điều Hướng"| AdminRentals
    AdminHome -->|"Menu Điều Hướng"| AdminStores
    AdminHome -->|"Menu Điều Hướng"| AdminLogs

    %% Cross-Links between Customer actions and Admin operations
    Checkout -->|"Tạo hóa đơn mới"| AdminOrders
    RentalVerify -->|"Tạo yêu cầu mượn sách mới"| AdminRentals
    MfaLogin -->|"Ghi nhật ký Face Log"| AdminLogs
