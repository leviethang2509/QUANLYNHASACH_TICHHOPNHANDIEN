---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 40
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 40

Use case này bắt đầu khi người dùng kích vào nút Khách hàng trên thanh menu quản trị. Hệ thống sẽ đọc bảng Customers và Users và hiển thị các thông tin như mã khách hàng, tên khách hàng, giới tính, ngày sinh, địa chỉ, email, số điện thoại các khách hàng lên màn hình.
Vô hiệu hóa khách hàng: Người dùng kích chuột vào nút Khóa trên mỗi dòng khách hàng thì hệ thống sẽ cập nhật lại tài khoản của khách hàng vừa chọn vào bảng Users và sau đó hệ thống sẽ hiển thị danh sách các khách hàng sau khi đã cập nhật từ bảng Customers lên màn hình.
Xóa khách hàng:
Người dùng kích vào nút Xóa trên mỗi dòng khách hàng ở trên màn hình quản lý khách hàng. Hệ thống sẽ hiển thị màn hình yêu cầu xác nhận xóa.
Người dùng kích nút Đồng ý trên màn hình xác nhận. Hệ thống sẽ xóa đi khách hàng vừa được chọn khỏi bảng Customers, xóa đi tài khoản của khách hàng vừa chọn khỏi bảng Users và xóa đi một số bản ghi có liên quan tới tài khoản của khách hàng vừa chọn khỏi bảng UserRoles và hiển thị danh sách các khách hàng từ bảng Customers sau khi cập nhật lên màn hình.
Use case kết thúc khi người dùng đóng cửa sổ quản lý khách hàng.
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
