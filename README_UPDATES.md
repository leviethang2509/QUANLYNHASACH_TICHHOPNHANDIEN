# README — Nâng cấp FaceAuth / Geofencing / Logs

Tóm tắt thay đổi:

- Thêm cấu hình `FaceAuthAPI` trong `BaiTapLon/Web.config` để gọi API Python.
- Tích hợp thu thập khuôn mặt: views `Views/Users/RegisterFace.cshtml`, `LoginMFA.cshtml` và `Scripts/FaceCapture.js`.
- Các controller mới: `FaceAuthController`, `GeofenceController`, `RentalController` (ghi logs).
- Logging: models `Mood/EF2/FaceAuthLog.cs`, `GeofenceLog.cs`, `RentalLog.cs`, và `Mood/EF2/LogDbContext.cs`.
- API cho admin lấy logs: `BaiTapLon/Controllers/Api/LogsController.cs`.
- Admin views: `Areas/Admin/Views/Logs/*` và `Areas/Admin/Views/ThongKe/Index.cshtml` (Chart.js).
- Migration SQL mẫu: `sql/migrations/20260508_add_logs.sql` và hướng dẫn `sql/README_migrations.md`.

Chạy nhanh (staging):

1. Tạo bảng logs bằng SQL script hoặc EF migration.
2. Đặt `FaceAuthAPI` trong `BaiTapLon/Web.config` trỏ tới API Python.
3. Đảm bảo thư mục `DataImage/FaceSamples/` có quyền ghi cho ứng dụng.

Ghi chú bảo mật:
- Logs chứa ảnh và vị trí; giới hạn truy cập trang Admin và cân nhắc mã hóa/ẩn dữ liệu nhạy cảm.
 
## Version 5 - Chatbox ban hang

- Ket noi widget chatbox Flask vao layout khach hang `BaiTapLon/Views/Shared/_LayoutHome.cshtml`.
- Them cau hinh `ChatboxWidgetUrl` va `ChatboxEnabled` trong `BaiTapLon/Web.config`.
- Du lieu chatbox duoc train tu database `QLNhaSach.dbo.Sanpham` tai du an Flask `NHANDIENKHUONMAT-new07040226/sales_chatbox`.
## Version 5 - 2026-05-10

- Guest favorites are stored locally in the browser and can be viewed at `/yeu-thich` without logging in.
- Admin products support review-file upload and a YouTube URL.
- Product details show review-file popup, YouTube video tab, and customer rating/comment form.
- Database migration: `sql/migrations/20260510_add_product_reviews_version5.sql`.
