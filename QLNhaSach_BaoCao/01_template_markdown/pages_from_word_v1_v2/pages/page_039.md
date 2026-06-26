---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 39
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 39

vừa xóa khỏi bảng OrderDetails và cập nhật lại số lượng của các sản phẩm trong đơn hàng vừa xóa vào bảng Products và hiển thị danh sách các đơn hàng từ bảng Orders sau khi cập nhật lên màn hình.
Xem chi tiết đơn hàng: Người dùng nhấn nút Chi tiết trên mỗi dòng đơn hàng thì hệ thống sẽ lấy chi tiết của đơn hàng vừa được chọn từ bảng Orders, OrderDetails, Customers và bảng Products, Images và hiển thị các thông tin như mã đơn hàng, ngày đặt, tên người đặt, số điện thoại người nhận, địa chỉ nhận hàng, tổng số lượng sản phẩm, trạng thái đơn hàng, phí vận chuyển, tổng tiền, tên sản phẩm, số lượng, đơn giá, hình ảnh sản phẩm lên màn hình.
Use case kết thúc khi người dùng đóng cửa sổ quản lý đơn hàng.
Luồng rẽ nhánh:
Trong quá trình thực hiện use case nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có.
Tiền điều kiện:
Người dùng phải đăng nhập với quyền quản trị hoặc nhân viên trước khi thực hiện use case.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
Quản lý khách hàng
Mô tả vắn tắt:
Use case này cho phép người dùng (nhân viên và quản trị viên) có thể vô hiệu hóa, xóa các khách hàng trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
