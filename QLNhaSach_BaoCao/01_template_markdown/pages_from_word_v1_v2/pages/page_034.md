---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 34
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 34

Người dùng nhấn vào nút đổi mật khẩu trên màn hình quản lý thông tin tài khoản thì hệ thống sẽ hiển thị màn hình đổi mật khẩu và yêu cầu người dùng nhập vào mật khẩu cũ, mật khẩu mới vào form đổi mật khẩu.
Người dùng nhập đầy đủ thông tin và nhấn nút Xác nhận hệ thống sẽ cập nhật lại mật khẩu của tài khoản đang đăng nhập vào bảng Users sau đó hiển thị thông báo “Đổi mật khẩu thành công”.
Use case kết thúc khi người dùng đóng cửa sổ quản lý thông tin tài khoản.
Luồng rẽ nhánh:
Tại bước 3b của luồng cơ bản nếu kiểm tra mật khẩu cũ không khớp với mật khẩu hiện tại của tài khoản đang đăng nhập trong bảng Users thì hiển thị thông báo “Mật khẩu cũ bị sai”. Use case kết thúc.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có
Tiền điều kiện:
Yêu cầu người dùng phải đăng nhập.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
Đơn hàng của tôi
Mô tả vắn tắt:
Use case này cho phép khách hàng có thể xem danh sách các đơn hàng, hủy đơn hàng và xem chi tiết các đơn hàng của mình trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
