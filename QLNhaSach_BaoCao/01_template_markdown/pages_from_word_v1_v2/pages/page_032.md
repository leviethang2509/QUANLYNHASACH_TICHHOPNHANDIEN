---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 32
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 32

Mua hàng
Mô tả vắn tắt:
Use case này cho phép khách hàng có thể Đặt hàng và Thanh toán các sản phẩm trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi khách hàng kích vào nút Đặt hàng trên màn hình quản lý giỏ hàng của trang web. Hệ thống sẽ bắt đầu lấy các sản phẩm trong giỏ hàng của khách hàng đang đăng nhập vào hệ thống từ bảng Users, Customers, Products, Images và Cart và hiển thị tên sản phẩm, hình ảnh sản phẩm, giá bán, số lượng sản phẩm trong giỏ hàng, tổng tiền của các sản phẩm trong giỏ hàng lên màn hình và yêu cầu khách hàng nhập các thông tin như số điện thoại người nhận, tên người nhận, địa chỉ người nhận trong form đặt hàng.
Khách hàng nhập đầy đủ thông tin mà hệ thống yêu cầu và sau đó nhấn nút Chuyển đến thanh toán trên form đặt hàng. Hệ thống sẽ hiển thị tên sản phẩm, số lượng đặt, hình ảnh của các sản phẩm vừa đặt từ bảng Products, bảng Images và bảng Cart lên màn hình thanh toán cùng với họ tên, số điện thoại, địa chỉ, phí vận chuyển và yêu cầu khách hàng chọn phương thức thanh toán trong form thanh toán.
Khách hàng chọn phương thức thanh toán và sau đó kích nút Thanh toán trên form thanh toán. Hệ thống sẽ lấy thông tin của khách hàng vừa đặt hàng và thông tin của các sản phẩm mà khách hàng vừa đặt từ các bảng Customers và bảng Products sau đó sẽ tạo một bản ghi trong bảng Orders và tạo các bản ghi trong bảng OrderDetails và sau đó cập nhật lại số lượng của sản phẩm trong bảng Products và đưa ra thông báo “Đặt hàng thành công”. Use case kết thúc.
Luồng rẽ nhánh:
Tại bước 2 của luồng cơ bản nếu khách hàng không nhập một trong 3 trường text địa chỉ nhận hàng, số điện thoại người nhận, tên người nhận thì hệ thống sẽ đưa ra thông báo “Yêu cầu hãy nhập đủ dữ liệu trước khi thanh toán”. Use case kết thúc.
