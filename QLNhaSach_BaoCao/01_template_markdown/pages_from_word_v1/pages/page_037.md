---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 37
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 37

Điểm mở rộng:
Không có.
Đăng nhập
Mô tả vắn tắt:
Use case này cho phép người dùng (khách hàng, nhân viên, quản trị viên) có thể đăng nhập tài khoản của mình vào trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi người dùng kích vào nút Đăng nhập trên màn hình menu chính của trang web sau đó hệ thống hiển thị màn hình đăng nhập và yêu cầu người dùng nhập địa chỉ email và mật khẩu trong form đăng nhập.
Sau khi nhập đầy đủ thông tin thì người dùng tiếp tục kích vào nút Đăng nhập trên form đăng nhập. Hệ thống sẽ kiểm tra các tài khoản ở trong bảng Users và tiến hành đăng nhập và sau đó hiển thị màn hình menu chính và thông báo “Đăng nhập thành công”. Use case kết thúc.
Luồng rẽ nhánh:
Tại bước 2 của luồng cơ bản nếu người dùng không nhập địa chỉ email hoặc mật khẩu thì hệ thống sẽ đưa ra thông báo yêu cầu nhập email và mật khẩu. Use case kết thúc.
Tại bước 2 của luồng cơ bản nếu kiểm tra tài khoản mà không có tài khoản nào có địa chỉ chỉ email vừa nhập thì đưa ra thông báo “Email không tồn tại tài khoản”. Use case kết thúc
Tại bước 2 của luồng cơ bản nếu kiểm tra mật khẩu của tài khoản vừa tìm được bằng email mà không trùng với mật khẩu người dùng vừa nhập thì đưa ra thông báo “Sai mật khẩu”. Use case kết thúc.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
