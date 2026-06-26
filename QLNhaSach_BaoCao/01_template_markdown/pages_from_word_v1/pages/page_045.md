---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 45
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 45

Use case này cho phép quản trị viên có thể xem được doanh số bán hàng theo từng tháng trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi quản trị viên nhấn vào nút Thống kê trên menu quản trị của trang web. Hệ thống bắt đầu đọc các bảng Orders, OrderDetails, Products, Categories, CategoryProducts Brands và hiển thị các thông tin như doanh thu hàng tháng và tổng số lượng bán ra hàng tháng, các sản phẩm được bán nhiều nhất, số lượng sản phẩm theo từng thể loại lên màn hình thống kê.
Luồng rẽ nhánh:
Trong quá trình thực hiện use case nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có.
Tiền điều kiện:
Người dùng phải đăng nhập với quyền quản trị viên trước khi thực hiện use case.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
