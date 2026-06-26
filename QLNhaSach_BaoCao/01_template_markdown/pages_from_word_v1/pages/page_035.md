---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 35
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 35

Use case này bắt đầu khi khách hàng kích vào nút Đơn hàng của tôi trên thanh menu chính của trang web. Hệ thống sẽ bắt đầu lấy danh sách đơn hàng của khách hàng đang đăng nhập từ các bảng User, Customer, Orders, OrderDetails và hiển thị các thông tin về các đơn hàng như mã đơn hàng, ngày đặt, tên người đặt, số điện thoại người nhận, địa chỉ nhận hàng, tổng số lượng sản phẩm, trạng thái đơn hàng, tổng tiền lên màn hình danh sách đơn hàng của tôi.
Hủy đơn hàng: Khách hàng nhấn chuột vào nút Hủy đơn hàng trên mỗi dòng đơn hàng thì hệ thống sẽ cập nhật trạng thái của đơn hàng vừa chọn thành “Đơn hàng bị hủy” trong bảng Orders sau đó hệ thống sẽ hiển thị thông báo “Hủy đơn hàng thành công” lên màn hình hệ thống.
Xem chi tiết đơn hàng: Khách hàng nhấn nút Chi tiết trên mỗi dòng đơn hàng thì hệ thống sẽ lấy chi tiết của đơn hàng vừa được chọn từ bảng Orders, OrderDetails và bảng Products, Images và hiển thị các thông tin như mã đơn hàng, ngày đặt, tên người đặt, số điện thoại người nhận, địa chỉ nhận hàng, tổng số lượng sản phẩm, trạng thái đơn hàng, phí vận chuyển, tổng tiền, tên sản phẩm, số lượng, đơn giá, hình ảnh sản phẩm lên màn hình.
Use case kết thúc khi khách hàng khi khách hàng đóng của sổ đơn hàng của tôi.
Luồng rẽ nhánh:
Tại bước 2 của luồng cơ bản nếu như đơn hàng đang ở trạng thái “Đang giao hàng” hoặc “Đã hoàn thành” thì hệ thống sẽ đưa ra thông báo “Đơn hàng này không thể hủy được”.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có
Tiền điều kiện:
Yêu cầu người dùng phải đăng nhập với tài khoản có quyền là khách hàng.
Hậu điều kiện:
