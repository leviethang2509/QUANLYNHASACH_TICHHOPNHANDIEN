---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 29
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 29

Luồng cơ bản:
Use case này bắt đầu khi khách hàng kích vào nút Đánh giá trên màn hình xem chi tiết sản phẩm. Hệ thống sẽ đọc bảng Customers, Products và bảng Comments để lấy những đánh giá về sản phẩm đang xem và hiển thị tên khách hàng đánh giá, nội dung đánh giá, số sao đánh giá, ngày đánh giá của các đánh giá lên màn hình đánh giá sản phẩm.
Khách hàng tiếp tục kích vào nút Viết đánh giá, sau đó hệ thống sẽ hiển thị một form đánh giá và yêu cầu khách hàng chọn số sao đánh giá và viết đánh giá ở trường text trong form.
Khách hàng nhập đầy đủ thông tin trên form đánh giá và kích vào nút Gửi đánh giá. Hệ thống sẽ lấy thông tin về khách hàng đang đăng nhập từ bảng Users và bảng Customers và tiếp tục lấy thông tin của sản phẩm được đánh giá từ bảng Products, sau khi đã lấy được các thông tin về khách hàng và sản phẩm được đánh giá từ bảng Customers và Products hệ thống sẽ thêm một bản ghi vào bảng Comments sau đó hệ thống sẽ hiển thị tên khách hàng đánh giá, nội dung đánh giá, số sao đánh giá, ngày đánh giá của các đánh giá sau khi đã cập nhật lên màn hình đánh giá sản phẩm cùng với thông báo “Gửi đánh giá thành công”. Use case kết thúc.
Luồng rẽ nhánh:
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có
Tiền điều kiện:
Yêu cầu người dùng phải đăng nhập với tài khoản có quyền là khách hàng.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
