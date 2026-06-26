# Use Case Catalog v2 - QLNhaSach

    Bảng này mở rộng use case theo đúng controller, service và API hiện có trong source code. Các use case được chia theo tác nhân để đưa vào chương phân tích yêu cầu và làm nguồn cho sơ đồ UML/Draw.io.

    | Mã | Tác nhân | Use case | Bằng chứng source code |
    |---|---|---|---|
    | UC-01 | Khách vãng lai | Xem trang chủ và danh mục sách | `HomeController.TrangChu, ProductController.ListProduct` |
| UC-02 | Khách vãng lai | Tìm kiếm sách theo từ khóa | `ProductController.Search, SanphamDraw.getByKeyWord` |
| UC-03 | Khách vãng lai | Nhận gợi ý tên sách khi nhập từ khóa | `ProductController.ListName, SanphamDraw.ListName` |
| UC-04 | Khách vãng lai | Xem chi tiết sách, review file, video | `ProductController.Detail, ReviewFilePreview` |
| UC-05 | Khách vãng lai | Đăng ký tài khoản | `UsersController.RegisterUser` |
| UC-06 | Người dùng | Đăng nhập tài khoản/mật khẩu | `UsersController.Login` |
| UC-07 | Người dùng | Đăng nhập MFA bằng khuôn mặt | `UsersController.LoginMFA, FaceAuthController.AuthenticateFace` |
| UC-08 | Người dùng | Đăng ký mẫu khuôn mặt | `FaceAuthController.RegisterFace` |
| UC-09 | Người dùng | Thực hiện challenge liveness | `FaceAuthController.CreateChallenge, CheckChallengeAction` |
| UC-10 | Người dùng | OCR CMND/CCCD nháp trước đăng nhập | `FaceAuthController.OcrCmndDraft` |
| UC-11 | Người dùng | Cập nhật hồ sơ CMND/CCCD | `FaceAuthController.OcrCmnd, RentalController.UpdateRentalProfile` |
| UC-12 | Người dùng | Thêm/xóa sách yêu thích | `UsersController.ToggleFavorite, ProductFavoriteDraw` |
| UC-13 | Khách vãng lai | Lưu yêu thích cục bộ | `UsersController.LocalFavoriteProducts, localStorage` |
| UC-14 | Người dùng | Đồng bộ yêu thích sau đăng nhập | `UsersController.SyncLocalFavorites` |
| UC-15 | Người dùng | Thêm sách vào giỏ hàng | `CartController.AddItem` |
| UC-16 | Người dùng | Cập nhật/xóa giỏ hàng | `CartController.Update, Delete, DeleteAll` |
| UC-17 | Người dùng | Đặt hàng và theo dõi đơn | `CartController.Success, UsersController.ChiTietHoaDon` |
| UC-18 | Người dùng | Thanh toán online MoMo | `CartController.PaymentMoMo, confirm_orderPaymentOnline_momo` |
| UC-19 | Người dùng | Kiểm tra vị trí trước khi mượn | `GeofenceController.CheckGeofence, StoreLocationService` |
| UC-20 | Người dùng | Xác thực khuôn mặt trước khi mượn | `FaceAuthController.VerifyRentalFace` |
| UC-21 | Người dùng | Gửi yêu cầu mượn sách | `RentalController.RequestRental` |
| UC-22 | Người dùng | Hủy yêu cầu mượn đang chờ | `RentalController.CancelRental` |
| UC-23 | Người dùng | Xem danh sách mượn của tôi | `RentalController.MyRentals` |
| UC-24 | Người dùng | Đánh giá sách | `ProductController.AddReview, ProductReviewDraw` |
| UC-25 | Quản trị viên | Quản lý sách, file đọc thử, tồn kho | `Admin/SanPhamController` |
| UC-26 | Quản trị viên | Quản lý danh mục | `Admin/CategoryController` |
| UC-27 | Quản trị viên | Quản lý tài khoản | `Admin/UserController` |
| UC-28 | Quản trị viên | Quản lý đơn hàng | `Admin/HoaDonController` |
| UC-29 | Quản trị viên | Duyệt mượn/trả sách | `Admin/RentalAdminController.UpdateStatus` |
| UC-30 | Quản trị viên | Gửi nhắc quá hạn | `Admin/RentalAdminController.SendOverdueReminders` |
| UC-31 | Quản trị viên | Quản lý tọa độ nhà sách/geofence | `Admin/WebManagerController.StoreLocation` |
| UC-32 | Quản trị viên | Xem nhật ký face/geofence/rental | `Admin/LogsAdminController, Api/LogsController` |
| UC-33 | Quản trị viên | Thống kê doanh thu, sản phẩm hot, mượn trả | `Admin/ThongKeController` |
| UC-34 | Quản trị viên | Quản lý nhập hàng/nhà cung cấp | `Admin/NhapHangController, NhaCungCapController` |
| UC-35 | Hệ thống | Gửi thông báo Gmail | `GmailNotificationService` |
| UC-36 | Hệ thống | Kiểm tra sức khỏe Face API | `HealthController.FaceApi, /api/face/health` |

    ## Quan hệ include/extend quan trọng

    - `UC-07 Đăng nhập MFA bằng khuôn mặt` include `UC-09 Thực hiện challenge liveness` khi cấu hình `FaceAuthRequireActionChallenge=true`.
    - `UC-11 Cập nhật hồ sơ CMND/CCCD` include OCR CMND/CCCD qua Flask API.
    - `UC-21 Gửi yêu cầu mượn sách` include `UC-19 Kiểm tra vị trí`, `UC-20 Xác thực khuôn mặt` và `UC-35 Gửi thông báo Gmail`.
    - `UC-29 Duyệt mượn/trả sách` include ghi `RentalLogs` và có thể include gửi Gmail.
    - `UC-02 Tìm kiếm sách` có quan hệ với `UC-03 Gợi ý tên sách` nhưng không phụ thuộc bắt buộc.
