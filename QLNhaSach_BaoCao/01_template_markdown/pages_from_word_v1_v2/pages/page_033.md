---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 33
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 33

Tại bước 2 của luồng cơ bản nếu như số lượng của sản phẩm được đặt hàng nhỏ hơn số lượng mà khách hàng đặt hàng thì hệ thống sẽ đưa râ thông báo “Đặt hàng thất bại do số lượng của sản phẩm bạn cần đặt không đủ”. Use case kết thúc.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có
Tiền điều kiện:
Yêu cầu người dùng phải đăng nhập với tài khoản có quyền là khách hàng.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
Quản lý thông tin tài khoản
Mô tả vắn tắt:
Use case này cho phép người dùng (khách hàng, nhân viên, quản trị viên) có thể xem thông tin tài khoản, sửa thông tin tài khoản, đổi mật khẩu tài khoản của mình trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi người dùng kích vào nút Tài khoản trên thanh menu chính của trang web. Hệ thống sẽ đọc các bảng Users, Customers và hiển thị các thông tin như họ tên, giới tính, địa chỉ, ngày sinh, email, số điện thoại của người dùng đang đăng nhập lên các trường text ở trên màn hình.
Sửa thông tin tài khoản: Người nhập các thông tin cần sửa trên các trường text và sau đó nhấn nút Thay đổi thông tin thì hệ thống sẽ cập nhật lại thông tin của người dùng đang đăng nhập vào bảng Users và Customers và sau đó hiển thị thông tin của người dùng đang đăng nhập sau khi cập nhật lên màn hình.
Đổi mật khẩu:
