---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 36
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 36

Không có.
Điểm mở rộng:
Không có.
Đăng ký
Mô tả vắn tắt:
Use case này cho phép khách hàng có thể đăng ký một tài khoản khách hàng trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi khách hàng kích chuột vào nút Đăng ký trên thanh menu chính của hệ thống sau đó hệ thống hiển thị màn hình đăng ký và một form đăng ký và yêu cầu khách hàng nhập các thông tin như email, họ tên, địa chỉ, số điện thoại, giới tính, ngày sinh, mật khẩu trên form đăng ký.
Khách hàng nhập đầy đủ thông tin và kích vào nút Đăng ký trên form đăng ký sau đó hệ thống sẽ tạo một khách hàng mới trong bảng Customers, một khách hàng mới trong bảng Users, một bản ghi mới trong bảng UserRoles và sau đó quay về màn hình menu chính của hệ thống và hiển thị thông báo “Đăng ký tài khoản thành công”. Use case kết thúc.
Luồng rẽ nhánh:
Tại bước 2 của luồng cơ bản nếu khách hàng không nhập email hoặc mật khẩu thì hệ thống sẽ đưa ra thông báo yêu cầu nhập email và mật khẩu. Use case kết thúc.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có
Tiền điều kiện:
Không có.
Hậu điều kiện:
Không có.
