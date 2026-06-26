# KIỂM THỬ HỆ THỐNG

## Kế hoạch kiểm thử

### Tổng quan

#### Giới thiệu chung

Tài liệu kế hoạch kiểm thử này đưa ra các mục đích sau:

Xác định thông tin cơ bản về dự án và các thành phần chức năng được kiểm thử và không được kiểm thử.

Liệt kê những yêu cầu cho việc kiểm thử (Test Requirements).

Những chiến lược kiểm thử nên được sử dụng.

#### Giới thiệu chung về dự án

Website bán sách bằng Asp.Net Core này là một website cung cấp những cuốn sách chính hãng từ những nhà xuất bản lớn ở trong nước cũng như quốc tế, những cuốn sách tại đây đa dạng các thể loại và dành cho đa dạng các đối tượng từ trẻ em tới người già ngoài ra website còn bán thêm cả đồ chơi giáo dục trẻ em và dụng cụ học tập làm cho tập sản phẩm của website trở lên đa dạng hơn. Tại đây khách hàng có thể thoải mái mua hàng với đa dạng phương thức từ thanh toán bằng tiền mặt tới thanh toán online giúp cho trải nghiệm của người dùng trở lên dễ dàng và thuận tiện nhất có thể.

#### Phạm vi kiểm thử

##### Những chức năng được kiểm thử

Đăng nhập: Kiểm tra chức năng đăng nhập vào hệ thống

Xem sản phẩm: Kiểm tra các chức năng xem sản phẩm theo thể loại, xem sản phẩm theo tác giả, xem sản phẩm theo thương hiệu, xem chi tiết sản phẩm

Mua hàng: Kiểm tra chức năng đặt hàng và thanh toán khi mua một đơn hàng

Thêm vào giỏ hàng: Kiểm tra chức năng thêm một sản phẩm vào giỏ hàng

Quản lý sản phẩm: Kiểm tra các chức năng xem, thêm, sửa, xóa sản phẩm

Quản lý nhân viên: Kiểm tra các chức năng xem, thêm, sửa, xóa nhân viên

##### Những giao diện được kiểm thử

Đăng nhập

Xem sản phẩm

Quản lý sản phẩm

Quản lý thể loại

Quản lý nhân viên

Quản lý khách hàng

#### Các rủi ro

| STT | Rủi ro | Cách khắc phục | Mức độ rủi ro |
| --- | --- | --- | --- |
| 1 | Thay đổi yêu cầu làm ảnh hưởng đến nguồn nhân lực và chiến lược test. | Lập lại plan sao cho phù hợp với lịch trình thực tế khi thay đổi yêu cầu, có thể chọn cách tăng thêm nguồn nhân lực cho dự án, hoặc tăng thời gian làm việc ngoài giờ cho nhân viên. | Cao |
| 2 | Sản phẩm mà lập trình viên thực hiện không kịp theo thời gian như lịch trình đề ra. | Yêu cầu cập nhật tiến độ công việc thường xuyên để quản ly kịp thời các thay đổi về thời gian và kĩ thuật. | Cao |

### Các tiêu chí chấp nhận sản phẩm

Tỉ lệ test case đạt( passed): 100%

Tỉ lệ test case không đạt (failed): 0%

Hệ thống chạy ổn định trên các trình duyệt web khác nhau (IE, Firefox và Google Chrome, Microsoft Edge).

### Chiến lược kiểm thử

Kiểm thử ở mức hệ thống (ST) và kiểm thử chấp thuận (UAT)

Dùng kiểu kiểm thử thủ công (manual test) bao gồm kiểm thử GUI và từng chức năng.

Việc kiểm thử chỉ bắt đầu khi đã hoàn thiện bộ test case để kiểm thử GUI và chức năng.

Thiết kế test case theo phương pháp phân vùng tương đương.

Chỉ thực hiện kiểm thử hồi quy, không thực hiện kiểm thử lại.

Các yêu cầu phi chức năng khác: tải trọng, hiệu năng…không được kiểm thử

### Lịch trình công việc

| Mốc công việc | Sản phẩm | Thời gian | Bắt đầu | Kết thúc |
| --- | --- | --- | --- | --- |
| Lập kế hoạch kiểm thử | Test plan | 2 ngày | 6 / 05 /202 4 | 8 / 05 /202 4 |
| Xem lại các tài liệu | Test plan | 2 ngày | 8 / 05 /202 4 | 1 0 / 05 /202 4 |
| Thiết kế các testcase | Test case | 1 ngày | 10/05/2024 | 11/05/2024 |
| Viết các testcase | Test case | 2 ngày | 11/05/2024 | 13/05/2024 |
| Xem lại các testcase | Test case | 1 ngày | 13/05/2024 | 14/05/2024 |
| Thực thi các testcase | Test case | 1 ngày | 14/05/2024 | 15/05/2024 |
| Ghi nhận và đánh giá kết quả kiểm thử | Test report | 2 ngày | 15/05/2024 | 17/05/2024 |

## Test Case

### Test Case Đăng nhập

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Đăng nhập |  |  |  |  |  |  |  |
| DN _ 01 | Đăng nhập thành công | F | Người dùng nhập đúng tên email và mật khẩu của tài khoản | 1. Người dùng nhấn nút Đăng nhập trên thanh menu. 2. Người dùng nhập email và mật khẩu của tài khoản cần đăng nhập và sau đó kích nút Đăng nhập trên form Đăng nhập | Hệ thống hiển thị màn hình chính và đưa ra thông báo đăng nhập thành công. | Pass |  |
| DN_02 | Đăng nhập không thành công 1 | F | Người dùng không nhập không nhập email và mật khẩu hoặc không nhập cả 2 | 1. Người dùng nhấn nút Đăng nhập trên thanh menu. 2. Người dùng không nhập email , mật khẩu hoặc không nhập cả 2 | Hệ thống hiển thị màn hình đăng nhập cùng với thông báo lỗi yêu cầu nhập đầy đủ các trường còn thiếu. | Pass |  |
| DN_0 3 | Đăng nhập không thành công 3 | F | Người dùng nhập sai mật khẩu. | 1. Người dùng nhấn nút Đăng nhập trên thanh menu. 2. Người dùng nhập email đã có trong hệ thống và nhập mật khẩu sai. | Hệ thống hiển thị màn hình đăng nhập cùng với thông báo lỗi mật khẩu bị sai. | Pass |  |

### Test Case Xem sản phẩm

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Xem sản phẩm |  |  |  |  |  |  |  |
| XSP_ 01 | Xem sản phẩm thành công | F | Đảm bảo trong cơ sở dữ liệu có tồn tại sản phẩm | 1. Người dùng nhấn nút Sản phẩm trên thanh menu. | Hệ thống hiển thị màn hình Sản phẩm và hiển thị các thông tin về sản phẩm như: tên sản phẩm, số lượng, hình ảnh, giá bán. | Pass |  |
| XSP_ 0 2 | Xem sản phẩm không thành công 1 | F | Kh ông tồn tại sản phẩm trong cơ sở dữ liệu | 1. Người dùng nhấn nút Sản phẩm trên thanh menu. | Hệ thống hiển thị màn hình trắng cùng thông báo không có sản phẩm. | Pass |  |
| XSP_ 0 3 | Xem sản phẩm t heo thể loại thành công | F | Đảm báo trong cơ sở dữ liệu có đầy đủ dữ liệu về thể loại và sản phẩm | 1. Người dùng nhấn nút Thể loại trên thanh menu dọc. 2. Người dùng kích vào tên của một thể loại ở trong danh sách thể loại hiển thị ở bước 1. | 1. Hệ thống hiển thị danh sách tên các thể loại ở ngay dưới nút Thể loại lên màn hình. 2. Hệ thống hiển thị danh sách các sản phẩm theo thể loại vừa chọn. | Pass |  |
| XSP_ 0 4 | Xem sản phẩm t heo thể loại không thành công 1 | F | Không có dữ liệu về thể loại trong cơ sở dữ liệu | 1. Người dùng nhấn nút Thể loại trên thanh menu dọc. | 1. Hệ thống hiển thị danh sách trắng ở ngay dưới nút Thể loại lên màn hình. | Pass |  |
| XSP_ 0 5 | Xem sản phẩm t heo thương hiệu thành công | F | Đảm báo trong cơ sở dữ liệu có đầy đủ dữ liệu về thương hiệu và sản phẩm | 1. Người dùng nhấn nút Thương hiệu trên thanh menu dọc. 2. Người dùng kích vào tên của một thương hiệu ở trong danh sách thương hiệu hiển thị ở bước 1. | 1. Hệ thống hiển thị danh sách tên các thương hiệu ở ngay dưới nút Thương hiệu lên màn hình. 2. Hệ thống hiển thị danh sách các sản phẩm theo thương hiệu vừa chọn. | Pass |  |
| XSP_ 0 6 | Xem sản phẩm t heo thương hiệu không thành công 1 | F | Không có dữ liệu về thương hiệu trong cơ sở dữ liệu | 1. Người dùng nhấn nút Thương hiệu trên thanh menu dọc. | 1. Hệ thống hiển thị danh sách trắng ở ngay dưới nút Thương hiệu lên màn hình. | Pass |  |
| XSP_ 0 7 | Xem sản phẩm t heo tác giả thành công | F | Đảm báo trong cơ sở dữ liệu có đầy đủ dữ liệu về tác giả và sản phẩm | 1. Người dùng nhấn nút Tác giả trên thanh menu dọc. 2. Người dùng kích vào tên của một tác giả ở trong danh sách tác giả hiển thị ở bước 1. | 1. Hệ thống hiển thị danh sách tên các tác giả ở ngay dưới nút Tác giả lên màn hình. 2. Hệ thống hiển thị danh sách các sản phẩm theo tác giả vừa chọn. | Pass |  |
| XSP_ 0 8 | Xem sản phẩm t heo tác giả không thành công 1 | F | Không có dữ liệu về tác giả trong cơ sở dữ liệu | 1. Người dùng nhấn nút Tác giả trên thanh menu dọc. | 1. Hệ thống hiển thị danh sách trắng ở ngay dưới nút Tác giả lên màn hình. | Pass |  |
| XSP_ 0 9 | Xem chi tiết sản phẩm thành công | F | Đảm bảo trong cơ sở dữ liệu có tồn tại sản phẩm | Người dùng nhấn nút vào một sản phẩm trên màn hình hiển thị danh sách sản phẩm. | Hệ thống hiển thị các thông tin của sản phẩm vừa chọn gồm: tên sản phẩm, giá bán, giảm giá, mã sản phẩm, mô tả, số lượng, tên thể loại, tên thương hiệu, tên tác giả. | Pass |  |

### Test Case Mua hàng

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mua h àng |  |  |  |  |  |  |  |
| Người dùng đăng nhập với tài khoản khách hàng |  |  |  |  |  |  |  |
| M H_ 01 | Đăng hàng thành công | F | Khách hàng nhập đầy đủ các thông tin họ tên, số điện thoại , địa chỉ và số lượng của các sản phẩm phải lớn hơn hoặc bằng số lượng của nó trong giỏ hàng | 1. Khách hàng kích nút Đặt hàng trong màn hình giỏ hàng. 2. Khách hàng nhập đầy đủ các thông tin số điện thoại, họ tên, địa chỉ trong form đặt hàng và nhấn nút Chuyển đến thanh toán . 3. Khách hàng chọn phương thức thức thanh toán ở trên màn hình thanh toán sau đó nhấn nút Thanh toán. | 1. Hệ thống hiển thị danh sách các sản phẩm trong giỏ hàng và form đặt hàng lên màn hình. 2. Hệ thống hiển thị danh sách các sản phẩm trong giỏ hàng và form chọn phương thức thanh toán. 3. Hệ thống hiển thị màn hình đặt hàng thành công à thông báo đặt hàng thành công. | Pass |  |
| M H_ 0 2 | Đăng hàng không thành công 1 | F | Số lượng sản phẩm nhỏ hơn số lượng của các sản phẩm trong giỏ hàng. | 1. Khách hàng kích nút Đặt hàng trong màn hình giỏ hàng. | 1. Hệ thống hiển thị màn hình giỏ hàng kèm thông thông số lượng hàng không đủ . | Pass |  |
| M H_ 0 3 | Đăng hàng không thành công 2 | F | Khách hàng nhập thiếu 1 trong các trường họ tên, số điện thoại, địa chỉ hoặc không nhập tất cả các trường. | 1. Khách hàng nhập thiếu 1 trong các trường họ tên, điện thoại, địa chỉ hoặc không nhập tất cả các trường sau đó nhấn nút chuyển đến thanh toán. | 1. Hệ thống hiển thị màn hình đặt hàng và đưa ra thông báo yêu cầu nhập thông tin vào các trường còn thiếu. | Pass |  |

### Test Case Thêm vào giỏ hàng

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Thêm vào giỏ hàng |  |  |  |  |  |  |  |
| Người dùng đăng nhập với tài khoản khách hàng |  |  |  |  |  |  |  |
| AGH_01 | Thêm vào giỏ hàng thành công | F | Đảm bảo số lượng của giỏ hàng lớn hơn hoặc bằng với số lượng của sản phẩm đó khi được thêm vào giỏ hàng | 1. Khách hàng kích nút Thêm ở trong mỗi ô sản phẩm trong màn hình hiển thị sản phẩm | 1. Hệ thống hiển thị màn hình sản phẩm kèm thông báo thêm vào giỏ hàng thành công. | Pass |  |
| AGH_02 | Thêm vào giỏ hàng không thành công | F | Số lượng sản phẩm nhỏ hơn số lượng của các sản phẩm trong giỏ hàng sau khi thêm. | 1. Khách hàng kích nút Thêm ở trong mỗi ô sản phẩm trong màn hình hiển thị sản phẩm. | 1. Hệ thống hiển thị màn hình giỏ hàng kèm thông báo Thêm thất bại do số lượng hàng không đủ. | Pass |  |

### Test Case Quản lý sản phẩm

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Quản lý sản phẩm |  |  |  |  |  |  |  |
| Người dùng đăng nhập với tài khoản có quyền nhân viên hoặc quản trị viên |  |  |  |  |  |  |  |
| QLSP_01 | Xem sản phẩm thành công | F | Đảm bảo trong cơ sở dữ liệu có tồn tại sản phẩm . | Người dùng nhấn nút Sản phẩm trên thanh menu quản trị . | Hệ thống hiển thị màn hình danh sách sản phẩm gồm các thông tin: mã sản phẩm, tên sản phẩm, slug, số lượng, giảm giá( nếu có), hình ảnh, trạng thái . | Pass |  |
| QLSP_02 | Xem sản phẩm không thành công | F | Trong cơ sở dữ liệu không có dữ liệu về sản phẩm. | Người dùng nhấn nút Sản phẩm trên thanh menu quản trị. | Hệ thống hiển thị màn hình gồm có một bảng trắng. | Pass |  |
| QLSP_03 | Thêm sản phẩm thành công. | F | Người dùng nhập đầy đủ thông tin các trường ở trên form thêm sản phẩm | 1. Người dùng nhấn nút Thêm ở trong màn hình danh sách sản phẩm. 2. Người dùng nhập đầy đủ các thông tin trên form thêm sản phẩm sau đó nhấn nút Thêm | 1. Hệ thống hiển thị form thêm sản phẩm lên màn hình. 2. Hệ thống hiển thị danh sách sản phẩm kèm thông báo thêm sản phẩm thành công lên màn hình. | Pass |  |
| QLSP_04 | Thêm sản phẩm không thành công 1. | F | Người dùng không nhập đầy đủ thông tin. | 1. Người dùng nhấn nút Thêm ở trong màn hình danh sách sản phẩm. 2. Người dùng nhập không đầy đủ các thông tin trên form thêm sản phẩm sau đó nhấn nút Thêm | 1. Hệ thống hiển thị form thêm sản phẩm lên màn hình. 2. Hệ thống hiển thị thông báo lỗi yêu cầu nhập đầy đủ thông tin. | Pass |  |
| QLSP_0 5 | Sửa sản phẩm thành công. | F | Đảm bảo trong cơ sở dữ liệu có ít nhất một sản phẩm | 1. Người dùng nhấn nút Sửa trong mỗi dòng sản phẩm trong màn hình danh sách sản phẩm. 2. Người dùng nhập đầy đủ các thông tin trên form sửa sản phẩm sau đó nhấn nút Sửa | 1. Hệ thống hiển thị form sửa sản phẩm lên màn hình. 2. Hệ thống hiển thị màn hính danh sách sản phẩm kèm thông báo sửa sản phẩm thành công lên màn hình. | Pass |  |
| QLSP_0 6 | Sửa sản phẩm không thành công 1. | F | Người dùng không nhập đầy đủ thông tin. | 1. Người dùng nhấn nút Sửa trong mỗi dòng sản phẩm trong màn hình danh sách sản phẩm . 2. Người dùng nhập không đầy đủ các thông tin trên form sửa sản phẩm sau đó nhấn nút Sửa | 1. Hệ thống hiển thị form sửa sản phẩm lên màn hình. 2. Hệ thống hiển thị thông báo lỗi yêu cầu nhập đầy đủ thông tin. | Pass |  |
| QLSP_ 0 7 | Xóa sản phẩm thành công | F | Đảm bảo trong cơ sở dữ liệu có ít nhất một sản phẩm | 1. Người dùng nhấn nút Xóa trên mỗi dòng sản phẩm trong màn hình danh sách sản phẩm. 2. Người dùng kích nút Đồng ý | 1. Hệ thống hiển thị màn hình yêu cầu xác nhận xóa. 2. Hệ thống hiển thị màn hình danh sách sản phẩm kèm th ông báo xóa sản phẩm thành công | Pass |  |
| QLSP_ 0 8 | Xóa sản phẩm không thành công | F | Người dùng chọn nút Không đồng ý | 1. Người dùng nhấn nút Xóa trên mỗi dòng sản phẩm trong màn hình danh sách sản phẩm. 2. Người dùng kích nút Không đồng ý | 1. Hệ thống hiển thị màn hình yêu cầu xác nhận xóa. 2. H ệ thống hiển thị màn hình danh sách sản phẩm | Pass |  |

### Test Case Quản lý nhân viên

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Quản lý nhân viên |  |  |  |  |  |  |  |
| Người dùng đăng nhập với tài khoản có quyền Quản trị viên |  |  |  |  |  |  |  |
| QLNV _01 | Xem nhân viên thành công | F | Đảm bảo trong cơ sở dữ liệu có tồn tại nhân viên. | Quản trị viên nhấn nút Nhân viên trên thanh menu quản trị. | Hệ thống hiển thị màn hình danh sách nhân viên gồm các thông tin: mã nhân viên, tên nhân viên, ngày sinh, email, địa chỉ số điện thoại, quyền của tài khoản nhân viên, trạng thái. | Pass |  |
| QLNV _02 | Xem nhân viên không thành công | F | Trong cơ sở dữ liệu không có dữ liệu về nhân viên. | Quản trị viên nhấn nút Nhân viên trên thanh menu quản trị. | Hệ thống hiển thị màn hình gồm có một bảng trắng. | Pass |  |
| QLNV _03 | Thêm nhân viên thành công. | F | Quản trị viên nhập đầy đủ thông tin các trường ở trên form thêm nhân viên | 1. Quản trị viên nhấn nút Thêm ở trong màn hình danh sách nhân viên. 2. Quản trị viên nhập đầy đủ các thông tin trên form thêm nhân viên sau đó nhấn nút Thêm | 1. Hệ thống hiển thị form thêm nhân viên lên màn hình. 2. Hệ thống hiển thị màn hình danh sách nhân viên kèm thông báo thêm nhân viên thành công lên màn hình. | Pass |  |
| QLNV _04 | Thêm nhân viên không thành công 1. | F | Quản trị viên không nhập đầy đủ thông tin. | 1. Quản trị viên nhấn nút Thêm ở trong màn hình danh sách nhân viên. 2. Quản trị viên nhập không đầy đủ các thông tin trên form thêm nhân viên sau đó nhấn nút Thêm | 1. Hệ thống hiển thị form thêm nhân viên lên màn hình. 2. Hệ thống hiển thị thông báo lỗi yêu cầu nhập đầy đủ thông tin. | Pass |  |
| QLNV _0 5 | Phân quyền nhân viên thành công. | F | Đảm bảo trong cơ sở dữ liệu có ít nhất một nhân viên | 1. Quản trị viên nhấn vào tên quyền trong mỗi dòng nhân viên trong màn hình danh sách nhân viên. 2. Quản trị viên chọn tên các quyền trên form phân quyền nhân viên sau đó nhấn nút Cập nhật | 1. Hệ thống hiển thị form phân quyền nhân viên lên màn hình. 2. Hệ thống hiển thị màn hình danh sách nhân viên kèm thông báo phân quyền nhân viên thành công lên màn hình. | Pass |  |
| QLNV _0 6 | Phân quyền nhân viên không thành công 1 . | F | Quản trị viên không chọn quyền nhân viên. | 1. Quản trị viên nhấn vào tên quyền trong mỗi dòng nhân viên trong màn hình danh sách nhân viên. 2. Quản trị viên không chọn quyền nhân viên sau đó nhấn nút Sửa | 1. Hệ thống hiển thị form phân quyền nhân viên lên màn hình. 2. Hệ thống hiển thị thông báo lỗi yêu cầu chọn quyền nhân viên cho nhân viên . | Pass |  |
| QLNV _ 0 7 | Xóa nhân viên thành công | F | Đảm bảo trong cơ sở dữ liệu có ít nhất một nhân viên | 1. Quản trị viên nhấn nút Xóa trên mỗi dòng nhân viên trong màn hình danh sách nhân viên. 2. Quản trị viên kích nút Đồng ý | 1. Hệ thống hiển thị màn hình yêu cầu xác nhận xóa. 2. H ệ thống hiển thị màn hình danh sách nhân viên kèm th ô ng báo xóa nhân viên thành công | Pass |  |
| QLNV _ 08 | Xóa nhân viên không thành công | F | Quản trị viên chọn nút Không đồng ý | 1. Quản trị viên nhấn nút Xóa trên mỗi dòng nhân viên trong màn hình danh sách nhân viên. 2. Quản trị viên kích nút Không đồng ý | 1. Hệ thống hiển thị màn hình yêu cầu xác nhận xóa. 2. Hệ thống hiển thị màn hình danh sách nhân viên | Pass |  |

### Test Case Giao diện

| Test case ID | Tên Test Case | Loại kiểm thử | Kịch bản kiểm thử | Các bước thực hiện | Kết quả mong đợi | Pass or Fail | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Giao diện người dùng |  |  |  |  |  |  |  |
| GD_01 | Màn hình chung | U | Đảm bảo có thể dùng chuột, các phím tab, lên, xuống, trái, phải...để điều hướng các từ màn hình này sang màn hình khác, từ trường này qua trường khác. | 1. Người dùng bật màn hình giao diện người dùng. 2. Chọn di chuyển giữa các trường bằng các phím tab, phím điều hướng (lên xuống trái phải) | 1. Hệ thống hiển thị giao diện người dùng đang bật 2. Trỏ chuột di chuyển đúng yêu cầu nghiệp vụ. | Pass |  |
| GD_0 2 | Dấu hiệu của các trường bắt buộc | U | Tất cả các trường bắt buộc phải nhập dữ liệu đều được đánh dấu | Nhìn vào các giao diện đang mở và đối chiếu với mock-up | 1. Hệ thống hiển thị những trường cần nhập dữ liệu có dấu * | Pass |  |
| GD_0 3 | Màn hình hiển thị danh sách sản phẩm | U | Có dữ liệu về sản phẩm để hiện thị | Nhìn vào giao diện danh sách sản phẩm và đối chiếu với mock-up | 1. Đảm bảo không có dữ liệu lặp được hiển thị. 2. Danh sách sản phẩm hiển thị với đầy đủ các trường ảnh, tên, slug, số lượng, giá bán, giảm giá. 3. Nếu số lượng sản phẩm lớn hơn 2 0 thì xuất hiện nút điều hướng để chuyển trang | Pass |  |
| GD_0 4 | Màn hình quản lý nhân viên | U | Hiển thị đầy đủ các nút và không có dữ liệu lặp | Nhìn vào giao diện quản lý nhân viên và đối chiếu với mock-up | 1. Đảm bảo không có dữ liệu lặp 2. Hiển thị danh sách nhân viên với mã nhân viên , tên nhân viên và địa chỉ, ngày sinh, trạng thái, email, tên quyền cùng nút Xóa hoặc hiển thị bảng trống. 3.Hiển thị nút Thêm mới ở góc trái phía trên bảng dữ liệu | Pass |  |
| GD_ 0 5 | Màn hình quản lý sản phẩm | U | Hiển thị đầy đủ các nút và không có dữ liệu lặp | Nhìn vào giao diện quản lý sản phẩm và đối chiếu với mock-up | 1. Đảm bảo không có dữ liệu lặp 2. Hiển thị danh sách sản phẩm với mã sản phẩm , tên sản phẩm giá bán, trạng thái, hình ảnh, slug, giảm giá cùng nút Xóa hoặc hiển thị bảng trống. 3.Hiển thị nút Thêm mới ở góc trái phía trên bảng dữ liệu | Pass |  |
| GD_ 0 6 | Màn hình quản lý thể loại | U | Hiển thị đầy đủ các nút và không có dữ liệu lặp | Nhìn vào giao diện quản lý thể loại và đối chiếu với mock-up | 1. Đảm bảo không có dữ liệu lặp 2. Hiển thị danh sách thể loại với mã thể loại , tên thể loại số lượng sản phẩm của thể loại cùng nút Xóa hoặc hiển thị bảng trống. 3.Hiển thị nút Thêm mới ở góc trái phía trên bảng dữ liệu | Pass |  |
| GD_ 0 7 | Màn hình quản lý khách hàng | U | Hiển thị đầy đủ các nút và không có dữ liệu lặp | Nhìn vào giao diện quản lý khách hàng và đối chiếu với mock-up | 1. Đảm bảo không có dữ liệu lặp 2. Hiển thị danh sách khách hàng với mã khách hàng , tên khách hàng , email, ngày sinh, tạng thái, địa chỉ, giới tính cùng nút Xóa hoặc hiển thị bảng trống. | Pass |  |
| GD_ 0 8 | Màn hình đăng nhập | U | Điều hướng thành công từ menu chính | Nhìn vào giao diện đăng nhập và đối chiếu với mock-up | 1. Hiển thị dấu * với các trường bắt buộc nhập dữ liệu 2. Trỏ chuột đặt ở trường Email đăng nhập 3. Màn hình có nút Đăng Nhập. | Pass |  |
| GD_ 09 | Màn hình trên các trình duyệt | U | Kiểm tra vị trí hiển thị các ảnh, các trường dữ liệu trên các trình duyệt khác nhau | Chạy tất cả các test case trên các trình duyệt được yêu cầu. | 1. Không bị vỡ form. 2. Trỏ chuột đặt đúng chỗ 3. Có thể điều hướng bằng tất cả các nút điều hướng hoặc trỏ chuột | Pass |  |
| GD_ 1 0 | Thông báo lỗi | U | Kiểm tra các thông báo lỗi đúng đặc tả và không sai chính tả. | Chạy tất cả các test case có thông báo lỗi | 1. Thông báo lỗi đúng đặc tả 2. Thông báo lỗi không sai chính tả 3. Thông báo lỗi có nút tắt. | Pass |  |

## Test Report

| STT | Loại kiểm thử | Pass | Fail | Untested | N/A | Số test case |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FTC | 3 3 | 0 | 0 | 0 | 33 |
| 2 | NFTC | 10 | 0 | 0 | 0 | 10 |
|  | Tổng | 43 | 0 | 0 | 0 | 43 |
