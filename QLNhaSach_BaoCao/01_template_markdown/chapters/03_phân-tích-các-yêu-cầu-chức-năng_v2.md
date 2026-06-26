# PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG 
CỦA HỆ THỐNG

## Biểu đồ use case

### Các use case chính

![Hinh minh hoa](media/BaoCaoMau_v2/image3.png)

Hình 21. Biểu đồ use case chính

### Quan hệ giữa các use case

Đăng nhập

![Hinh minh hoa](media/BaoCaoMau_v2/image4.png)

Hình 22. Biểu đồ use case Đăng nhập

Xem sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v2/image5.png)

Hình 23. Biểu đồ use case Xem sản phẩm

Quản lý sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v2/image6.png)

Hình 24. Biểu đồ use case Quản lý sản phẩm

Quản lý đơn hàng

![Hinh minh hoa](media/BaoCaoMau_v2/image7.png)

Hình 25. Biểu đồ use case Quản lý đơn hàng

Đơn hàng của tôi

![Hinh minh hoa](media/BaoCaoMau_v2/image8.png)

Hình 26. Biểu đồ use case Đơn hàng của tôi

Quản lý khách hàng

![Hinh minh hoa](media/BaoCaoMau_v2/image9.png)

Hình 27. Biểu đồ use case Quản lý khách hàng

Quản lý thông tin tài khoản

![Hinh minh hoa](media/BaoCaoMau_v2/image10.png)

Hình 28. Biểu đồ use case Quản lý thông tin tài khoản

Quản lý nhân viên

![Hinh minh hoa](media/BaoCaoMau_v2/image11.png)

Hình 29. Biểu đồ use case Quản lý nhân viên

Quản lý giỏ hàng

![Hinh minh hoa](media/BaoCaoMau_v2/image12.png)

Hình 210. Biểu đồ use case Quản lý giỏ hàng

Quản lý danh sách yêu thích

![Hinh minh hoa](media/BaoCaoMau_v2/image13.png)

Hình 211. Biểu đồ use case Quản lý danh sách yêu thích

## Mô tả chi tiết các use case

### Xem sản phẩm

Mô tả vắn tắt:

Use case này cho phép người dùng (khách hàng, nhân viên và quản trị viên) xem được các sản phẩm của hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi người dùng nhấn vào mục Sản phẩm trên thanh menu chính của trang web. Hệ thống sẽ đọc bảng Products và bảng Images để hiển thị hình ảnh, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn của sản phẩm lên màn hình.

Tìm kiếm sản phẩm: Khi người dùng nhập từ khóa cần tìm vào ô Tìm kiếm trên trang sản phẩm sau đó nhấn nút Tìm kiếm bên cạnh ô nhập. Hệ thống sẽ đọc bảng Products và bảng Images để lấy ra những sản phẩm có tên tồn tại với từ khóa mà người dùng vừa nhập và hiển thị hình ảnh, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn của sản phẩm lên màn hình.

Xem chi tiết sản phẩm: Khi người dùng kích chuột vào nút Chi tiết trên mỗi ô sản phẩm hoặc kích vào tên sản phẩm hay hình ảnh của sản phẩm trên mỗi ô sản phẩm thì hệ thống sẽ lấy ra các thông tin chi tiết về sản phẩm vừa chọn như: mã sản phẩm, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn từ bảng Products, hình ảnh sản phẩm từ bảng Images, tên thể loại của sản phẩm từ bảng Categories, tên thương hiệu của sản phẩm từ bảng Brands, tên tác giả của sản phẩm từ bản Authors lên màn hình hiển thị Chi tiết sản phẩm.

Xem sản phẩm theo thể loại:

Khi người dùng kích chuột vào mục Thể loại trong phần Sidebar của trang web. Hệ thống sẽ đọc bảng Categories và hiển thị tên của các thể loại lên màn hình.

Người dùng tiếp tục kích chuột vào tên của một thể loại thì hệ thống sẽ đọc bảng CategoryProducts và bảng Products và bảng Images để lấy ra các sản phẩm có thể loại tương ứng với thể loại vừa chọn và hiển thị hình ảnh, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn của sản phẩm lên màn hình.

Xem sản phẩm theo thương hiệu:

Khi người dùng kích chuột vào mục Thương hiệu trong phần Sidebar của trang web. Hệ thống sẽ đọc bảng Brands và hiển thị tên của các thương hiệu lên màn hình.

Người dùng tiếp tục kích chuột vào tên của một thương hiệu thì hệ thống sẽ đọc bảng Products và bảng Images để lấy ra các sản phẩm có thương hiệu tương ứng với thương hiệu vừa chọn và hiển thị hình ảnh, tên sản phẩm, giá bán, giá sau khi giảm giá(nếu có), phần trăm giảm giá(nếu có), số lượng còn của sản phẩm lên màn hình.

Xem sản phẩm theo tác giả:

Khi người dùng kích chuột vào mục Tác giả trong phần Sidebar của trang web. Hệ thống sẽ đọc bảng Authors và hiển thị tên của các tác giả lên màn hình.

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

### Đánh giá sản phẩm

Mô tả vắn tắt:

Use case này cho phép khách hàng xem được các đánh giá và viết đánh giá của mình về các sản phẩm của hệ thống.

Luồng sự kiện:

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

### Thêm vào giỏ hàng

Mô tả vắn tắt:

Use case này cho phép khách hàng thêm các sản phẩm vào giỏ hàng của mình trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi khách hàng bắt đầu kích vào nút Thêm vào giỏ hàng ở mỗi ô sản phẩm trong màn hình sản phẩm. Hệ thống sẽ lấy thông tin khách hàng đang đăng nhập từ bảng Users và bảng Customers và tiếp tục lấy thông tin về sản phẩm được thêm vào giỏ hàng từ bảng Products sau đó thêm một bản ghi vào bảng Cart, sau đó hệ thống sẽ hiển thị lên màn hình thông báo “Thêm vào giỏ hàng thành công”. Use case kết thúc.

Luồng rẽ nhánh:

Tại bước 1 của luồng cơ bản nếu số lượng sản phẩm nhỏ hơn số lượng sản phẩm thêm vào giỏ hàng thì hệ thống sẽ đưa ra thông báo “Số lượng thêm vào giỏ hàng vượt quá số lượng cho phép”. Use case kết thúc.

Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.

Các yêu cầu đặc biệt:

Không có

Tiền điều kiện:

Yêu cầu người dùng phải đăng nhập với tài khoản có quyền là khách hàng.

Hậu điều kiện:

Không có.

Điểm mở rộng:

Không có.

### Thêm vào danh sách yêu thích

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

### Mua hàng

Mô tả vắn tắt:

Use case này cho phép khách hàng có thể Đặt hàng và Thanh toán các sản phẩm trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi khách hàng kích vào nút Đặt hàng trên màn hình quản lý giỏ hàng của trang web. Hệ thống sẽ bắt đầu lấy các sản phẩm trong giỏ hàng của khách hàng đang đăng nhập vào hệ thống từ bảng Users, Customers, Products, Images và Cart và hiển thị tên sản phẩm, hình ảnh sản phẩm, giá bán, số lượng sản phẩm trong giỏ hàng, tổng tiền của các sản phẩm trong giỏ hàng lên màn hình và yêu cầu khách hàng nhập các thông tin như số điện thoại người nhận, tên người nhận, địa chỉ người nhận trong form đặt hàng.

Khách hàng nhập đầy đủ thông tin mà hệ thống yêu cầu và sau đó nhấn nút Chuyển đến thanh toán trên form đặt hàng. Hệ thống sẽ hiển thị tên sản phẩm, số lượng đặt, hình ảnh của các sản phẩm vừa đặt từ bảng Products, bảng Images và bảng Cart lên màn hình thanh toán cùng với họ tên, số điện thoại, địa chỉ, phí vận chuyển và yêu cầu khách hàng chọn phương thức thanh toán trong form thanh toán.

Khách hàng chọn phương thức thanh toán và sau đó kích nút Thanh toán trên form thanh toán. Hệ thống sẽ lấy thông tin của khách hàng vừa đặt hàng và thông tin của các sản phẩm mà khách hàng vừa đặt từ các bảng Customers và bảng Products sau đó sẽ tạo một bản ghi trong bảng Orders và tạo các bản ghi trong bảng OrderDetails và sau đó cập nhật lại số lượng của sản phẩm trong bảng Products và đưa ra thông báo “Đặt hàng thành công”. Use case kết thúc.

Luồng rẽ nhánh:

Tại bước 2 của luồng cơ bản nếu khách hàng không nhập một trong 3 trường text địa chỉ nhận hàng, số điện thoại người nhận, tên người nhận thì hệ thống sẽ đưa ra thông báo “Yêu cầu hãy nhập đủ dữ liệu trước khi thanh toán”. Use case kết thúc.

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

### Quản lý thông tin tài khoản

Mô tả vắn tắt:

Use case này cho phép người dùng (khách hàng, nhân viên, quản trị viên) có thể xem thông tin tài khoản, sửa thông tin tài khoản, đổi mật khẩu tài khoản của mình trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi người dùng kích vào nút Tài khoản trên thanh menu chính của trang web. Hệ thống sẽ đọc các bảng Users, Customers và hiển thị các thông tin như họ tên, giới tính, địa chỉ, ngày sinh, email, số điện thoại của người dùng đang đăng nhập lên các trường text ở trên màn hình.

Sửa thông tin tài khoản: Người nhập các thông tin cần sửa trên các trường text và sau đó nhấn nút Thay đổi thông tin thì hệ thống sẽ cập nhật lại thông tin của người dùng đang đăng nhập vào bảng Users và Customers và sau đó hiển thị thông tin của người dùng đang đăng nhập sau khi cập nhật lên màn hình.

Đổi mật khẩu:

Người dùng nhấn vào nút đổi mật khẩu trên màn hình quản lý thông tin tài khoản thì hệ thống sẽ hiển thị màn hình đổi mật khẩu và yêu cầu người dùng nhập vào mật khẩu cũ, mật khẩu mới vào form đổi mật khẩu.

Người dùng nhập đầy đủ thông tin và nhấn nút Xác nhận hệ thống sẽ cập nhật lại mật khẩu của tài khoản đang đăng nhập vào bảng Users sau đó hiển thị thông báo “Đổi mật khẩu thành công”.

Use case kết thúc khi người dùng đóng cửa sổ quản lý thông tin tài khoản.

Luồng rẽ nhánh:

Tại bước 3b của luồng cơ bản nếu kiểm tra mật khẩu cũ không khớp với mật khẩu hiện tại của tài khoản đang đăng nhập trong bảng Users thì hiển thị thông báo “Mật khẩu cũ bị sai”. Use case kết thúc.

Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.

Các yêu cầu đặc biệt:

Không có

Tiền điều kiện:

Yêu cầu người dùng phải đăng nhập.

Hậu điều kiện:

Không có.

Điểm mở rộng:

Không có.

### Đơn hàng của tôi

Mô tả vắn tắt:

Use case này cho phép khách hàng có thể xem danh sách các đơn hàng, hủy đơn hàng và xem chi tiết các đơn hàng của mình trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

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

Không có.

Điểm mở rộng:

Không có.

### Đăng ký

Mô tả vắn tắt:

Use case này cho phép khách hàng có thể đăng ký một tài khoản khách hàng trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi khách hàng kích chuột vào nút Đăng ký trên thanh menu chính của hệ thống sau đó hệ thống hiển thị màn hình đăng ký và một form đăng ký và yêu cầu khách hàng nhập các thông tin như email, họ tên, địa chỉ, số điện thoại, giới tính, ngày sinh, mật khẩu trên form đăng ký.

Khách hàng nhập đầy đủ thông tin và kích vào nút Đăng ký trên form đăng ký sau đó hệ thống sẽ tạo một khách hàng mới trong bảng Customers, một khách hàng mới trong bảng Users, một bản ghi mới trong bảng UserRoles và sau đó quay về màn hình menu chính của hệ thống và hiển thị thông báo “Đăng ký tài khoản thành công”. Use case kết thúc.

Luồng rẽ nhánh:

Tại bước 2 của luồng cơ bản nếu khách hàng không nhập email hoặc mật khẩu thì hệ thống sẽ đưa ra thông báo yêu cầu nhập email và mật khẩu. Use case kết thúc.

Tại bất kì bước nào trong luồng cơ bản nếu hệ thống không thể kết nối được với cơ sở dữ liệu thì sẽ hiển thị một thông báo lỗi và use case kết thúc.

Các yêu cầu đặc biệt:

Không có

Tiền điều kiện:

Không có.

Hậu điều kiện:

Không có.

Điểm mở rộng:

Không có.

### Đăng nhập

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

Không có

Tiền điều kiện:

Không có.

Hậu điều kiện:

Không có.

Điểm mở rộng:

Không có.

### Quản lý đơn hàng

Mô tả vắn tắt:

Use case này cho phép người dùng (nhân viên và quản trị viên)có thể cập nhật trạng thái, xóa các đơn hàng trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi người dùng kích vào nút Đơn hàng trên thanh menu quản trị. Hệ thống sẽ đọc bảng Orders và OrderDetail và hiển thị các thông tin như mã đơn hàng, ngày đặt, người đặt, địa chỉ giao hàng, tổng số lượng, trạng thái, tổng tiền của danh sách các đơn hàng lên màn hình.

Cập nhật trạng thái đơn hàng:

Khi người dùng nhấn vào nút Cập nhật trên mỗi dòng đơn hàng. Hệ thống sẽ hiển thị form cập nhật trạng thái và yêu cầu người dùng lựa chọn trạng thái cho đơn hàng.

Người dùng chọn trạng thái mới cho đơn hàng và nhấn nút Cập nhật trong form cập nhật trạng thái thì hệ thống sẽ cập nhật lại đơn hàng vừa chọn vào bảng Orders và hiển thị danh sách đơn hàng sau khi đã cập nhật từ bảng Orders lên màn hình.

Xóa đơn hàng:

Người dùng kích vào nút Xóa trên mỗi dòng đơn hàng ở trên màn hình quản lý đơn hàng. Hệ thống sẽ hiển thị màn hình yêu cầu xác nhận xóa.

Người dùng kích nút Đồng ý trên màn hình xác nhận. Hệ thống sẽ xóa đi đơn hàng vừa được chọn khỏi bảng Orders và các bản ghi có liên quan tới đơn hàng vừa xóa khỏi bảng OrderDetails và cập nhật lại số lượng của các sản phẩm trong đơn hàng vừa xóa vào bảng Products và hiển thị danh sách các đơn hàng từ bảng Orders sau khi cập nhật lên màn hình.

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

### Quản lý khách hàng

Mô tả vắn tắt:

Use case này cho phép người dùng (nhân viên và quản trị viên) có thể vô hiệu hóa, xóa các khách hàng trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

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

### Quản lý sản phẩm

Mô tả vắn tắt:

Use case này cho phép người dùng (nhân viên và quản trị viên)có thể thêm, sửa, xóa sản phẩm trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi người dùng kích vào nút Sản phẩm trên thanh menu quản trị. Hệ thống sẽ đọc bảng Products, Images, Authors, AuthorProducts, Categories, CategoryProducts, Brands và hiển thị các thông tin nhữ mã sản phẩm, tên sản phẩm, số lượng còn, phần trăm giảm giá, giá bán, mô tả, tên thương hiệu, tên tác giả, tên thể loại của các sản phẩm lên màn hình.

Thêm sản phẩm:

Khi người dùng nhấn vào nút Thêm mới trong màn hình quản lý sản phẩm thì hệ thống sẽ đọc các bảng Authors, Categories, Brands và hiển thị tên tác giả, tên thể loại, tên thương hiệu lên các hộp chọn của form thêm sản phẩm và yêu cầu nhập tên sản phẩm, số lượng còn, phần trăm giảm giá, giá bán, mô tả, tên thương hiệu và chọn tên tác giả, tên thể loại cho banner mới.

Người dùng nhập và chọn đầy đủ các thông tin và nhấn nút Thêm trong form thêm sản phẩm thì hệ thống sẽ sinh ra một ProductId mới và thêm mới một sản phẩm trong bảng Products và thêm một số bản ghi có liên quan tới sản phẩm vừa thêm vào bảng  AuthorProducts và bảng CategoryProducts sau đó hiển thị danh sách các sản phẩm từ bảng Products sau khi đã cập nhật lên màn hình.

Sửa sản phẩm:

Người dùng kích vào nút Sửa trên mỗi dòng thương hiệu ở trên màn hình quản lý thương hiệu. Hệ thống sẽ đọc các bảng Products, Images, Authors, AuthorProducts, Categories, CategoryProducts, Brands và hiển thị tên tác giả, tên thể loại, tên thương hiệu lên các hộp chọn của form sửa và hiển thị các thông tin của sản phẩm vừa chọn như tên sản phẩm, số lượng còn, phần trăm giảm giá, giá bán, mô tả trên các trường text và tên thương hiệu, tên tác giả, tên thể loại trên các hộp chọn của form sửa.

Người dùng nhập và chọn đầy đủ những thông tin cần sửa và kích nút Cập nhật trên form sửa. Hệ thống sẽ cập nhật lại thông tin của sản phẩm vừa được chọn vào bảng Products và cập nhật lại một số bản ghi có liên quan tới sản phẩm vừa sửa vào các bảng AuthorProducts, CategoryProducts sau đó hiển thị danh sách các sản phẩm từ bảng Products sau khi cập nhật lên màn hình.

Xóa sản phẩm:

Người dùng kích vào nút Xóa trên mỗi dòng sản phẩm ở trên màn hình quản lý sản phẩm. Hệ thống sẽ hiển thị màn hình yêu cầu xác nhận xóa.

Người dùng kích nút Đồng ý trên màn hình xác nhận. Hệ thống sẽ xóa đi sản phẩm vừa được chọn khỏi bảng Products và xóa các bản ghi có liên quan tới sản phẩm vừa chọn khỏi bảng AuthorProducts, CategoryProducts và hiển thị danh sách các sản phẩm từ bảng Products sau khi cập nhật lên màn hình.

Use case kết thúc khi người dùng đóng cửa sổ quản lý sản phẩm.

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

### Quản lý nhân viên

Mô tả vắn tắt:

Use case này cho phép quản trị viên có thể thêm, vô hiệu hóa, xóa, phân quyền các nhân viên trong hệ thống.

Luồng sự kiện:

Luồng cơ bản:

Use case này bắt đầu khi quản trị viên click vào nút Nhân viên trên thanh menu quản trị. Hệ thống sẽ đọc bảng Employees và Users, UserRoles, Roles và hiển thị các thông tin như mã nhân viên, tên nhân viên, giới tính, ngày sinh, địa chỉ, email, số điện thoại, quyền các nhân viên lên màn hình.

Thêm nhân viên:

Quản trị viên kích vào nút Thêm mới trong màn hình quản trị nhân viên thì hệ thống sẽ hiển thị một form thêm nhân viên và yêu cầu quản trị viên nhập các thông tin như email, số điện thoại, mật khẩu, họ tên, địa chỉ, giới tính, ngày sinh.

Quản trị viên nhập đầy đủ các thông tin trên from thêm nhân viên và kích nút Thêm thì hệ thống sẽ sinh ra một EmployeeId mới và thêm một nhân viên mới vào bảng Employees và tiếp tục thêm một tài khoản cho nhân viên vừa tạo vào bảng Users và thêm một bản ghi vào bảng UserRoles sau đó hệ thống lấy ra danh sách các nhân viên được cập nhật từ bảng Employees và bảng Users và hiển thị lên màn hình.

Vô hiệu hóa nhân viên: Quản trị viên kích chuột vào nút Khóa trên mỗi dòng nhân viên thì hệ thống sẽ cập nhật lại tài khoản của nhân viên vừa chọn vào bảng Users và sau đó hệ thống sẽ hiển thị danh sách các nhân viên sau khi đã cập nhật từ bảng Employee lên màn hình.

Phân quyền nhân viên:

Quản trị viên kích chuột vào tên quyền trên mỗi dòng nhân viên trên màn hình quản lý nhân viên sau đó hệ thống sẽ đọc các bảng Users, UserRoles, Roles và hiển thị tên các quyền lên hộp chọn trong form phân quyền.

Quản trị viên lựa chọn các quyền cho tài khoản của nhân viên vừa chọn và kích nút Xác nhận thì hệ thống sẽ cập nhật các bản ghi có liên quan tới tài khoản của nhân viên vừa chọn vào bảng UserRoles sau đó hệ thống sẽ hiển thị danh sách các nhân viên sau khi đã cập nhật từ bảng Employee lên màn hình.

Xóa nhân viên:

Quản trị viên kích vào nút Xóa trên mỗi dòng nhân viên ở trên màn hình quản lý nhân viên. Hệ thống sẽ hiển thị màn hình yêu cầu xác nhận xóa.

Quản trị viên kích nút Đồng ý trên màn hình xác nhận. Hệ thống sẽ xóa đi nhân viên vừa được chọn khỏi bảng Employees, xóa đi tài khoản của khách hàng vừa chọn khỏi bảng Users và xóa đi một số bản ghi có liên quan tới tài khoản của nhân viên vừa chọn khỏi bảng UserRoles và hiển thị danh sách các nhân viên từ bảng Employees sau khi cập nhật lên màn hình.

Use case kết thúc khi quản trị viên đóng cửa sổ quản lý nhân viên.

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

### Thống kê

Mô tả vắn tắt:

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
