---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 28
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 28

Người dùng tiếp tục kích chuột vào tên của một tác giả thì hệ thống sẽ đọc bảng AuthorProducts và bảng Products và bảng Images để lấy ra các sản phẩm có tác giả tương ứng với tác giả vừa chọn và hiển thị hình ảnh, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn của sản phẩm lên màn hình.
Use case kết thúc khi người dùng đóng cửa sổ xem sản phẩm.
Luồng rẽ nhánh:
Tại bước 1 trong luồng cơ bản nếu dữ liệu trong bảng Products bị trống thì hệ thống sẽ đưa ra thông báo “Không có dữ liệu về sản phẩm”. Use case kết thúc khi người dùng kích chuột vào các mục khác trên thanh menu chính của trang web.
Tại bước 2, 3, 4b, 5b, 6b trong luồng cơ bản nếu hệ thống không tìm thấy được sản phẩm tương ứng với lựa chọn của người dùng thì hệ thống sẽ đưa ra thông báo “Không tìm thấy sản phẩm cần tìm”. Use case kết thúc khi người dùng kích chuột vào các mục khác trên thanh menu chính của trang web.
Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.
Các yêu cầu đặc biệt:
Không có.
Tiền điều kiện:
Không có.
Hậu điều kiện:
Không có.
Điểm mở rộng:
Không có.
Đánh giá sản phẩm
Mô tả vắn tắt:
Use case này cho phép khách hàng xem được các đánh giá và viết đánh giá của mình về các sản phẩm của hệ thống.
Luồng sự kiện:
