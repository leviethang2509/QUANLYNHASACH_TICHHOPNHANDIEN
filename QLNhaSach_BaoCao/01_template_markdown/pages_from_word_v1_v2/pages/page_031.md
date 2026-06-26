---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 31
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 31

Thêm vào danh sách yêu thích
Mô tả vắn tắt:
Use case này cho phép người dùng (khách hàng) thêm các sản phẩm vào danh sách các sản phẩm yêu thích của mình trong hệ thống.
Luồng sự kiện:
Luồng cơ bản:
Use case này bắt đầu khi khách hàng bắt đầu kích vào nút Yêu thích ở mỗi ô sản phẩm trong màn hình sản phẩm. Hệ thống sẽ lấy thông tin khách hàng đang đăng nhập từ bảng Users và bảng Customers và tiếp tục lấy thông tin về sản phẩm được thêm vào danh sách yêu thích từ bảng Products sau đó thêm một bản ghi vào bảng FavotiteProducts, sau đó hệ thống sẽ hiển thị lên màn hình thông báo “Thêm vào danh sách yêu thích thành công”. Use case kết thúc.
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
