# MÔ TẢ CÁC YÊU CẦU CỦA HỆ THỐNG

## Lý do chọn đề tài

Trong thời đại công nghệ số ngày nay, việc phát triển các website chất lượng cao không chỉ đòi hỏi sự hiểu biết sâu rộng về lập trình mà còn yêu cầu kiến thức chuyên sâu về các công nghệ xây dựng web. Chính vì vậy, đề tài xây dựng một ứng dụng website bán sách sẽ giúp sinh viên có cơ hội áp dụng và phát triển những kỹ năng quan trọng để chuẩn bị cho sự nghiệp sau này.

Thị trường bán lẻ trực tuyến đang ngày càng phát triển, và sách cũng là một trong những mặt hàng có nhu cầu mua sắm lớn.

Sử dụng ASP.NET Core mang lại sự ổn định, bảo mật và hiệu suất cao cho hệ thống và còn được hỗ trợ đa nền tảng. Xây dựng một website bán sách bằng ASP.NET Core đòi hỏi lập trình viên phải nắm vững các kiến thức về lập trình web, xử lý dữ liệu, bảo mật, và quản lý phiên làm việc của người dùng.

Xây dựng một ứng dụng thương mại điện tử đòi hỏi sinh viên đối mặt với những thách thức thực tế như quản lý đơn hàng, thanh toán trực tuyến, và quản lý sản phẩm. Đây là cơ hội tốt để nâng cao kỹ năng lập trình và hiểu biết về phát triển web hiện đại.

## Khảo sát hệ thống

### Tổng quan về hệ thống

Hệ thống của nhà sách Minh Tiến chuyên bán về sách và ngoài ra còn bán thêm cả về một số mặt hàng liên quan khác như vở ghi, bút, dụng cụ học tập, đồ lưu niệm, đồ chơi giáo dục.

Hệ thống nhà sách Minh Tiến gồm các thể loại sách chính như: sách thiếu nhi, sách khoa học, sách giáo khoa và các loại sách khác.

Định hướng của hệ thống nhà sách Minh Tiến là tập trung kinh doanh các mặt hàng là sách và văn phòng phẩm và hướng tới các đối tượng khách hàng của hệ thống bao gồm: trẻ em, thanh niên, trung niên và người già.

Đến với không gian mua sắm trực tuyến của hệ thống nhà sách Minh Tiến, khách hàng có thể dễ dàng tìm thấy những cuốn sách hay, đa thể loại của nhiều nhà xuất bản, công ty sách trong và ngoài nước cùng nhiều dụng cụ học tập, văn phòng phẩm, quà lưu niệm, đồ chơi giáo dục chính hãng của những thương hiệu uy tín.

Quy mô: Diện tích của các cửa hàng thuộc hệ thống nhà sách Minh Tiến không rộng mà nhu cầu của người mua càng ngày càng lớn dẫn đến các cửa hàng thuộc hệ thống bị quá tải vào các ngày cuối tuần.

Nhân lực:

Nhân viên bán hàng

Quản lý cửa hàng

Nhược điểm: Khi khách quá đông mà diện tích của cửa hàng lại nhỏ, không đủ để phục vụ hết tất cả khách hàng.

Hướng phát triển của hệ thống hiện tại: Cần xây dưng 1 phần mềm bán các sản phẩm của hệ thống qua nền tảng trực tuyến. Phần mềm có các chức năng giúp cho khách hàng có thể mua sắm trực tuyến và thanh toán online, giúp cho nhân viên và người quản lý có thể quản lý các sản phẩm và danh mục cũng như là xem được thống kê việc bán hàng của hệ thống.

## Các hoạt động của hệ thống

### Hoạt động bán hàng

Hoạt động nghiệp vụ

Khi khách hàng truy cập vào hệ thống thì hệ thống sẽ hiển thị các sản phẩm của hệ thống lên màn hình, nếu khách có nhu cầu mua mặt hàng nào thì khách có thể nhấn vào nút “Thêm vào giỏ hàng” ở mỗi sản phẩm.

Sau khi thêm sản phẩm vào giỏ hàng thì khách nhấn vào nút “Giỏ hàng” và sau đó hệ thống sẽ hiển thị các sản phẩm mà khách vừa thêm vào giỏ hàng.

Khách hàng tiếp tục nhấn vào nút “Đặt hàng” sau đó hệ thống sẽ hiển thị màn hình của trang Đặt hàng, khách hàng sẽ phải nhập địa chỉ giao hàng, số điện thoại người nhận, tên người nhân, ghi chú (nếu có), sau khi nhập thông tin xong thì khách hàng sẽ chọn phương thức thanh toán và sau đó nhấn nút “Mua hàng” sau đó hệ thống sẽ hiển thị tới màn hình thông báo về đơn hàng vừa đặt.

Sau khi giao hàng tới khách hàng thành công, đơn vị vận chuyển sẽ thông báo lại với nhân viên của hệ thống về đơn hàng đã được giao, và sau đó Nhân viên hệ thống sẽ truy cập vào trang quản lý của hệ thống bán hàng và sửa trạng thái đơn hàng thành “Giao hàng thành công”.

Tài liệu khảo sát:

Sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v4/image1.jpeg)

Hình 1-1. Sản phẩm của hệ thống

![Hinh minh hoa](media/BaoCaoMau_v4/image2.jpeg)

Hình 1-2. Sản phẩm của hệ thống

### Báo cáo, thống kê

Khi có yêu cầu thống kê doanh số bán hàng Nhân viên của hệ thống sẽ vào trang quản trị của phần mềm sau đó mở phần thống kê thì hệ thống sẽ hiển thị doanh thu và số mặt hàng bán được theo từng tháng.

### Cập nhật thông tin hệ thống

Nhân viên và người quản lý có thể thêm, sửa, xóa thông tin:

Sản phẩm.

Thể loại.

Thương hiệu.

Tác giả.

Banner.

Nhân viên.

Khách hàng.

## Các yêu cầu của hệ thống

### Yêu cầu chức năng

Hệ thống cần có các chức năng sau:

Quản lý thông tin về: sản phẩm, khách hàng, nhân viên,… .

Tạo đơn hàng online và thanh toán trực tuyến bằng VnPay và PayPal.

Tìm kiếm sản phẩm qua nhiều cách thức như: qua từ khóa, qua thể loại, qua tác giả, qua thương hiệu.

Đánh giá các sản phẩm của hệ thống.

Thống kê doanh thu và lượng hàng bán ra hàng tháng.

Ngoài ra hệ thống cần phải đáp ứng:

Khả năng hoạt động ổn định.

Hệ thống làm việc nhanh chóng và đảm bảo tin cậy.

Giao diện dễ sử dụng, thân thiện với người dùng.

Độ bảo mật hệ thống cao.

### Yêu cầu phi chức năng

Phần Cứng:

Bộ xử lý 32 bit (x86) hoặc 64 bit (x64) có tốc độ từ 1 GHz trở lên.

Ram 8GB.

Đĩa cứng có dung lượng trống từ 20GB trở lên.

Ngoài ra cần lắp đặt thêm các thiết bị ngoại vi khác phục vụ cho hệ thống mới vận hành.

Phần Mềm:

Hệ điều hành Windows 7 trở lên

Hệ quản trị cơ sở dữ liệu SQL Server 2018 trở lên.

Chi phí thay thế, năng cấp hệ thống máy tính là lớn.

Bên cạnh đó còn các chi phí về bản quyền các phần mềm.
