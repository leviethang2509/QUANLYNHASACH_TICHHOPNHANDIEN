---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
converted_at: 2026-05-13 06:19:06
converter: scripts/convert_template_and_rebuild_input.py
---

> So trang docProps/app.xml: 1

| NGUYỄN THANH LÂM NGÀNH KỸ THUẬT PHẦN MỀM | BỘ CÔNG THƯƠNG TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI --------------------------------------- ĐỒ ÁN TỐT NGHIỆP NGÀNH KỸ THUẬT PHẦN MỀM XÂY DỰNG WEBSITE BÁN SÁCH BẰNG ASP.NET CORE CBHD : ThS. Nguyễn Thiện Thanh Sinh viên : Nguyễn Thanh Lâm Mã số sinh viên : 1234 Hà Nội – Năm 2024 |
| --- | --- |

BỘ CÔNG THƯƠNG

TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI

---------------------------------------

ĐỒ ÁN TỐT NGHIỆP ĐẠI HỌC

NGÀNH KỸ THUẬT PHẦN MỀM

XÂY DỰNG WEBSITE BÁN SÁCH BẰNG ASP.NET CORE

| CBHD | : | ThS. Nguyễn Thiện Thanh |
| --- | --- | --- |
| Sinh viên | : | Nguyễn Thanh Lâm |
| Mã số sinh viên | : | 1234 |

Hà Nội – Năm  2024

Trang này đặt phiếu giao đề tài vào đây

(BÁO CÁO NÊN LÀM TỪ 50 đến 80 TRANG)

LỜI NÓI ĐẦU

Lời đầu tiên em xin trân thành cảm ơn quý thầy cô trong khoa công nghệ thông tin đã hỗ trợ em trong suốt quá trình học tập, rèn luyện tại trường và khi em thực hiện đề tài này. Em xin gửi lời cảm ơn đến cô ThS. Nguyễn Thiện Thanhngười đã tận tình hướng dẫn, giúp đỡ, chỉ bảo em trong suốt thời gian thực hiện đồ án tốt nghiệp. Đồng thời em xin trân trọng cảm ơn những tình cảm quý báu mà các thầy cô trong Trường Đại học Công nghiệp Hà Nội truyền đạt cho em những những kinh nghiệm, kỹ thuật và cách thức trong việc xây dựng đề tài này.

Thông qua đồ án tốt nghiệp này, em đã tiếp thu được vô số kiến thức bổ ích, trau dồi kỹ năng chuyên môn và củng cố nền tảng lý thuyết đã được học. Sự hướng dẫn, khuyến khích, đồng hành và hỗ trợ của giáo viên hướng dẫn đã giúp em có cơ hội nghiên cứu, áp dụng kiến thức vào thực tiễn và phát triển kỹ năng chuyên môn. Em rất biết ơn vì sự quan tâm và kiến thức mà cô đã chia sẻ với em. Thông qua đồ án tốt nghiệp lần này em mong muốn tiếp tục học hỏi và trau dồi để hoàn thiện bản thân, xứng đáng với sự tin tưởng và kỳ vọng của thầy cô.

Em xin chân thành cảm ơn!

DANH MỤC CÁC TỪ VIẾT TẮT

| CSDL | Cơ sở dữ liệu |
| --- | --- |
| SQL | Structured Query Language |
| HTCSDL | Hệ thống cơ sở dữ liệu |

DANH MỤC CÁC HÌNH ẢNH

Hình 1-1. Sản phẩm của hệ thống	3

Hình 1-2. Sản phẩm của hệ thống	3

Hình 21. Biểu đồ use case chính	6

Hình 22. Biểu đồ use case Đăng nhập	7

Hình 23. Biểu đồ use case Xem sản phẩm	8

Hình 24. Biểu đồ use case Quản lý sản phẩm	8

Hình 25. Biểu đồ use case Quản lý đơn hàng	9

Hình 26. Biểu đồ use case Đơn hàng của tôi	9

Hình 27. Biểu đồ use case Quản lý khách hàng	10

Hình 28. Biểu đồ use case Quản lý thông tin tài khoản	10

Hình 29. Biểu đồ use case Quản lý nhân viên	11

Hình 210. Biểu đồ use case Quản lý giỏ hàng	11

Hình 211. Biểu đồ use case Quản lý danh sách yêu thích	12

Hình 3-1. Cấu trúc database của dự án sau khi thiết kế	32

Hình 3-2. Chi tiết bảng Authors của dự án	35

Hình 3-3. Chi tiết bảng AuthorProducts của dự án	35

Hình 3-4. Chi tiết bảng Banners của dự án	36

Hình 3-5. Chi tiết bảng Brands của dự án.	36

Hình 3-6. Chi tiết bảng Categories của dự án.	36

Hình 3-7. Chi tiết bảng CategoryProducts của dự án	37

Hình 3-8. Chi tiết bảng Comments của dự án.	37

Hình 3-9. Chi tiết bảng Customers của dự án.	37

Hình 3-10. Chi tiết bảng Employees của dự án.	38

Hình 3-11. Chi tiết bảng FavouriteProducts của dự án.	38

Hình 3-12. Chi tiết bảng Images của dự án	38

Hình 3-13. Chi tiết bảng Orders của dự án	39

Hình 3-14. Chi tiết bảng OrderDetails của dự án.	39

Hình 3-15. Chi tiết bảng Products của dự án.	40

Hình 3-16. Chi tiết bảng Users của dự án.	40

Hình 3-17. Chi tiết bảng UserClaims của dự án.	41

Hình 3-18. Chi tiết bảng Roles của dự án.	41

Hình 3-19. Chi tiết bảng RoleClaims của dự án	41

Hình 3-20. Chi tiết bảng UserRoles của dự án	42

Hình 3-21. Chi tiết bảng UserLogins của dự án	42

Hình 3-22. Chi tiết bảng UserTokens của dự án.	42

Hình 3-23. Chi tiết bảng Provinces của dự án	43

Hình 3-24. Chi tiết bảng Districts của dự án.	43

Hình 3-25. Chi tiết bảng Wards của dự án	43

Hình 3-26. Cấu trúc database của dự án sau khi đã cài đặt.	44

Hình 4-1. Biểu đồ trình tự usecase xem sản phẩm	47

Hình 4-2. Biểu đồ lớp phân tích usecase xem sản phẩm	47

Hình 4-3. Biểu đồ trình tự usecase đánh giá sản phẩm	48

Hình 4-4. Biểu đồ lớp phân tích usecase đánh giá sản phẩm	49

Hình 4-5. Biểu đồ trình tự usecase thêm vào giỏ hàng.	50

Hình 4-6. Biểu đồ lớp phân tích usecase thêm vào giỏ hàng.	51

Hình 4-7. Biểu đồ trình tự usecase thêm vào danh sách yêu thích	52

Hình 4-8. Biểu đồ lớp phân tích usecase thêm vào danh sách yêu thích	53

Hình 4-9. Biểu đồ trình tự usecase mua hàng	55

Hình 4-10. Biểu đồ lớp phân tích usecase mua hàng	55

Hình 4-11. Biểu đồ trình tự usecase quản lý thông tin tài khoản	57

Hình 4-12. Biểu đồ lớp phân tích usecase quản lý thông tin tài khoản.	57

Hình 4-13. Biểu đồ trình tự usecase đơn hàng của tôi.	59

Hình 4-14. Biểu đồ lớp phân tích usecase đơn hàng của tôi.	59

Hình 4-15. Biểu đồ trình tự usecase đăng ký	60

Hình 4-16. Biểu đồ lớp phân tích usecase đăng ký	61

Hình 4-17. Biểu đồ trình tự usecase đăng nhập	61

Hình 4-18. Biểu đồ lớp phân tích usecase đăng nhập	62

Hình 4-19. Biểu đồ trình tự usecase quản lý đơn hàng.	64

Hình 4-20. Biểu đồ lớp phân tích usecase quản lý đơn hàng	64

Hình 4-21. Biểu đồ trình tự usecase quản lý khách hàng.	66

Hình 4-22. Biểu đồ lớp phân tích usecase quản lý khách hàng.	66

Hình 4-23. Biểu đồ trình tự usecase quản lý sản phẩm	70

Hình 4-24. Biểu đồ lớp phân tích usecase quản lý sản phẩm	70

Hình 4-25. Biểu đồ trình tự usecase quản lý nhân viên	73

Hình 4-26. Biểu đồ lớp phân tích usecase quản lý nhân viên	74

Hình 4-27. Biểu đồ trình tự usecase thống kê	75

Hình 4-28. Biểu đồ lớp phân tích usecase thống kê	75

Hình 5-1. Mô hình kiến trúc onion	76

Hình 5-2 Giới thiệu Asp.Net Core	78

Hình 5-3. Biểu đồ điều hướng màn hình của nhóm usecase chính.	85

Hình 5-4. Biểu đồ điều hướng màn hình của nhóm usecase thứ cấp.	86

Hình 5-5. Giao diện xem sản phẩm	87

Hình 5-6. Thiết kế chi tiết màn hình chức năng đánh giá sản phẩm	87

Hình 5-7. Giao diện giỏ hàng	88

Hình 5-8. Giao diện danh sách yêu thích	88

Hình 5-9. Giao diện trang đặt hàng	89

Hình 5-10. Giao diện trang quản lý thông tin tài khoản	90

Hình 5-11. Giao diện trang đơn hàng của tôi	90

Hình 5-12. Giao diện trang đăng ký	91

Hình 5-13. Giao diện trang đăng nhập	92

Hình 5-14. Giao diện trang quản lý đơn hàng	92

Hình 5-15. Giao diện trang quản lý khách hàng	93

Hình 5-16. Giao diện trang quản lý sản phẩm	93

Hình 5-17. Giao diện trang quản lý nhân viên	94

Hình 5-18. Giao diện trang thống kê	94

MỤC LỤC

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

![Hinh minh hoa](media/BaoCaoMau_v1/image1.jpeg)

Hình 1-1. Sản phẩm của hệ thống

![Hinh minh hoa](media/BaoCaoMau_v1/image2.jpeg)

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

# PHÂN TÍCH CÁC YÊU CẦU CHỨC NĂNG 
CỦA HỆ THỐNG

## Biểu đồ use case

### Các use case chính

![Hinh minh hoa](media/BaoCaoMau_v1/image3.png)

Hình 21. Biểu đồ use case chính

### Quan hệ giữa các use case

Đăng nhập

![Hinh minh hoa](media/BaoCaoMau_v1/image4.png)

Hình 22. Biểu đồ use case Đăng nhập

Xem sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image5.png)

Hình 23. Biểu đồ use case Xem sản phẩm

Quản lý sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image6.png)

Hình 24. Biểu đồ use case Quản lý sản phẩm

Quản lý đơn hàng

![Hinh minh hoa](media/BaoCaoMau_v1/image7.png)

Hình 25. Biểu đồ use case Quản lý đơn hàng

Đơn hàng của tôi

![Hinh minh hoa](media/BaoCaoMau_v1/image8.png)

Hình 26. Biểu đồ use case Đơn hàng của tôi

Quản lý khách hàng

![Hinh minh hoa](media/BaoCaoMau_v1/image9.png)

Hình 27. Biểu đồ use case Quản lý khách hàng

Quản lý thông tin tài khoản

![Hinh minh hoa](media/BaoCaoMau_v1/image10.png)

Hình 28. Biểu đồ use case Quản lý thông tin tài khoản

Quản lý nhân viên

![Hinh minh hoa](media/BaoCaoMau_v1/image11.png)

Hình 29. Biểu đồ use case Quản lý nhân viên

Quản lý giỏ hàng

![Hinh minh hoa](media/BaoCaoMau_v1/image12.png)

Hình 210. Biểu đồ use case Quản lý giỏ hàng

Quản lý danh sách yêu thích

![Hinh minh hoa](media/BaoCaoMau_v1/image13.png)

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

# THIẾT KẾ CƠ SỞ DỮ LIỆU

## Mô hình hóa dữ liệu

![Hinh minh hoa](media/BaoCaoMau_v1/image14.png)

Hình 3-1. Cấu trúc database của dự án sau khi thiết kế

Authors: Dùng để lưu trữ các tác giả trong hệ thống và gồm các thông tin AuthorId, AuthorCode, AuthorName, CodeNumber, AuthorSlug, Information, ImageName, UrlImage. Một tác giả có 0, 1 hoặc nhiều sản phẩm. Một sản phẩm có 0, 1 hoặc nhiều tác giả.

AuthorProducts: Dùng để lưu trữ chi tiết từng tác giả trong hệ thống và gồm các thông tin AuthorId, ProductId.

Banners: Dùng để lưu trữ banner quảng cáo cho các chiến dịch quảng cáo của hệ thống gồm có các thông tin như BannerId, Title, Content, ImageName, UrlImage.

Brands: Dùng để lưu trữ các thương hiệu sản phẩm trong hệ thống và gồm các thông tin BrandId, BrandCode, BrandName, BrandSlug, CodeNumber, Description, ImageName, UrlImage. Một thương hiệu gồm có 0, 1 hoặc nhiều sản phẩm, một sản phẩm thuộc 1 thương hiệu.

Categories: Dùng để lưu trữ các thể loại của hệ thống và gồm có CategoryId, CategoryName, CategoryCode, CategorySlug, CodeNumber, Description. Một thể loại thuộc 0, 1 hoặc nhiều sản phẩm, một sản phẩm có 1 hoặc nhiều thể loại.

CategoryProducts: Dùng để lưu trữ chi tiết từng thể loại trong hệ thống và gồm có các thông tin CategoryId, ProductId.

Comments: Dùng để lưu trữ các đánh giá của khách hàng về sản phẩm trong hệ thống và gồm có các thông tin CommentId, Vote, Message, DateCreated, CustomerId, ProductId. Một đánh giá thuộc 1 sản phẩm, một sản phẩm có 0, 1 hoặc nhiều đánh giá. Một đánh giá thuộc về một khách hàng, một khách hàng sẽ có 0, 1 hoặc nhiều đánh giá.

Customers: Dùng để lưu trữ các khách hàng của hệ thống và gồm có các thông tin CustomerId, FullName, DateOfBirth, Gender, CustomerCode, CodeNumber, Address. Một khách hàng có một tài khoản. Một tài khoản thuộc về 0 hoặc 1 khách hàng.

Cart: Dùng để lưu trữ các dòng trong giỏ hàng của khách hàng gồm có các thông tin Customers, ProductId, Quantity. Một khách hàng có 0, 1 hoặc nhiều dòng giỏ hàng, một dòng giỏ hàng thuộc về một khách hàng. Một sản phẩm có thuộc 0, 1 hoặc nhiều dòng giỏ hàng, một dòng giỏ hàng có một sản phẩm.

Employees: Dùng để lưu trữ các nhân viên của hệ thống gồm có các thông tin EmployeeId, EmployeeName, EmployeeCode, CodeNumber, Gender, Address, DateOfBirth. Một nhân viên có 1 tài khoản, một tài khoản thuộc về 0 hoặc một nhân viên.

FavoriteProducts: Dùng để lưu trữ từng dòng sản phẩm yêu thích của khách hàng và gồm có các thông tin CustomerId, ProductId. Một dòng sản phẩm yêu thích sẽ thuộc về 1 khách hàng, một khách hàng có 0, 1 hoặc nhiều dòng sản phẩm yêu thích. Một dòng sản phẩm yêu thích có 1 sản phẩm, một sản phẩm thuộc về 0, 1 hoặc nhiều dòng sản phẩm yêu thích.

Images: Dùng để lưu trữ các ảnh của sản phẩm và gồm các thông tin ImageId, ImageName, Url, ProductId. Một ảnh thuộc về một sản phẩm, một sản phẩm có 0, 1 hoặc nhiều ảnh.

Orders: Dùng để lưu trữ các đơn hàng của khách hàng trong hệ thống và gồm các thông tin OrderId, OrderCode, DateCreated, PhoneNumber, Address, Status, TransportFee, Note, DateDelivery, CodeNumber, FullName, CustomerId. Một đơn hàng thuộc về 1 khách hàng,  một khách hàng có 0, 1 hoặc nhiều đơn hàng.

OrderDetials: Dùng để lưu trữ chi tiết đơn hàng của hệ thống và gồm các thông tin OrderId, ProductId, Price, Quantity. Một chi tiết đơn hàng thuộc về một đơn hàng, một đơn hàng có nhiều chi tiết đơn hàng. Một chi tiết đơn hàng có một sản phẩm, một sản phẩm thuộc 0, 1 hoặc nhiều chi tiết đơn hàng.

Products: Dùng để lưu trữ các sản phẩm trong hệ thống và gồm các thông tin ProductId, ProductCode, CodeNumber, ProductSlug, ProductName, Price, PercentDiscount, Description, Quantity, IsActive, BrandId.

Users: Dùng để lưu trữ các tài khoản trong hệ thống gồm các thông tin UserId, EmployeeId, CustomerId, UserName, NormalizedUserName, Email, NormalizedEmail, EmailConfirmed, SecurityStamp, ConcurrencyStamp, PhoneNumber, PhoneNumberConfirmed, TwoFactorEnabled, LockoutEnd, LockoutEnable, AccessFailedCount.

Roles: Dùng để lưu trữ quyền trong hệ thống và gồm các thông tin RoleId, Name, NormalizedName, ConccurrencyStamp. Một quyền thuộc về 0, 1 hoặc nhiều tài khoản, một tài khoản có 0, 1 hoặc nhiều quyền.

UserRoles: Dùng để lưu trữ chi tiết các quyền và gồm các thông tin RoleId, UserId.

UseClaims: Dùng để lưu trữ thuộc tính người dùng gồm các thông tin Id, ClaimType, ClaimValue, UseId.

RoleClaims: Dùng để lưu trữ thuộc tính của quyền và gồm các thông tin Id, RoleId, ClaimType, ClaimValue.

UserLogins: Dùng để lưu trữ thông tin về người dùng đăng nhập và gồm các thông tin LoginProvider, ProviderKey, ProviderDisplayName, UserName.

UserTokens: Dùng để lưu trữ token của người dùng và gồm các thông tin LoginProvider, UserId, Name, Value.

Provinces: Dùng để lưu trữ dữ liệu các tỉnh thành Việt Nam và gồm các thông tin: CodeProvince, Name, NameEn, FullName, FullNameEn, CodeName.

Districts: Dùng để lưu trữ dữ liệu các quận huyện Việt Nam và gồm các thông tin: CodeDistrict, Name, NameEn, FullName, FullNameEn, CodeName, CodeProvince.

Wards: Dùng để lưu trữ dữ liệu các phường xã Việt Nam và gồm các thông tin: CodeWard, Name, NameEn, FullName, FullNameEn, CodeName, CodeDistrict.

## Thiết kế bảng

Bảng Authors

![Hinh minh hoa](media/BaoCaoMau_v1/image15.png)

Hình 3-2. Chi tiết bảng Authors của dự án

Bảng AuthorProducts

![Hinh minh hoa](media/BaoCaoMau_v1/image16.png)

Hình 3-3. Chi tiết bảng AuthorProducts của dự án

Bảng Banners

![Hinh minh hoa](media/BaoCaoMau_v1/image17.png)

Hình 3-4. Chi tiết bảng Banners của dự án

Bảng Brands

![Hinh minh hoa](media/BaoCaoMau_v1/image18.png)

Hình 3-5. Chi tiết bảng Brands của dự án.

Bảng Categories

![Hinh minh hoa](media/BaoCaoMau_v1/image19.png)

Hình 3-6. Chi tiết bảng Categories của dự án.

Bảng CategoryProducts

![Hinh minh hoa](media/BaoCaoMau_v1/image20.png)

Hình 3-7. Chi tiết bảng CategoryProducts của dự án

Bảng Comments

![Hinh minh hoa](media/BaoCaoMau_v1/image21.png)

Hình 3-8. Chi tiết bảng Comments của dự án.

Bảng Customers

![Hinh minh hoa](media/BaoCaoMau_v1/image22.png)

Hình 3-9. Chi tiết bảng Customers của dự án.

Bảng Employees

![Hinh minh hoa](media/BaoCaoMau_v1/image23.png)

Hình 3-10. Chi tiết bảng Employees của dự án.

Bảng FavouriteProducts

![Hinh minh hoa](media/BaoCaoMau_v1/image24.png)

Hình 3-11. Chi tiết bảng FavouriteProducts của dự án.

Bảng Images

![Hinh minh hoa](media/BaoCaoMau_v1/image25.png)

Hình 3-12. Chi tiết bảng Images của dự án

Bảng Orders

![Hinh minh hoa](media/BaoCaoMau_v1/image26.png)

Hình 3-13. Chi tiết bảng Orders của dự án

Bảng OrderDetails

![Hinh minh hoa](media/BaoCaoMau_v1/image27.png)

Hình 3-14. Chi tiết bảng OrderDetails của dự án.

Bảng Products

![Hinh minh hoa](media/BaoCaoMau_v1/image28.png)

Hình 3-15. Chi tiết bảng Products của dự án.

Bảng Users

![Hinh minh hoa](media/BaoCaoMau_v1/image29.png)

Hình 3-16. Chi tiết bảng Users của dự án.

Bảng UserClaims

![Hinh minh hoa](media/BaoCaoMau_v1/image30.png)

Hình 3-17. Chi tiết bảng UserClaims của dự án.

Bảng Roles

![Hinh minh hoa](media/BaoCaoMau_v1/image31.png)

Hình 3-18. Chi tiết bảng Roles của dự án.

Bảng RoleClaims

![Hinh minh hoa](media/BaoCaoMau_v1/image32.png)

Hình 3-19. Chi tiết bảng RoleClaims của dự án

Bảng UserRoles

![Hinh minh hoa](media/BaoCaoMau_v1/image33.png)

Hình 3-20. Chi tiết bảng UserRoles của dự án

Bảng UserLogins

![Hinh minh hoa](media/BaoCaoMau_v1/image34.png)

Hình 3-21. Chi tiết bảng UserLogins của dự án

Bảng UserTokens

![Hinh minh hoa](media/BaoCaoMau_v1/image35.png)

Hình 3-22. Chi tiết bảng UserTokens của dự án.

Bảng Provinces

![Hinh minh hoa](media/BaoCaoMau_v1/image36.png)

Hình 3-23. Chi tiết bảng Provinces của dự án

Bảng Districts

![Hinh minh hoa](media/BaoCaoMau_v1/image37.png)

Hình 3-24. Chi tiết bảng Districts của dự án.

Bảng Wards

![Hinh minh hoa](media/BaoCaoMau_v1/image38.png)

Hình 3-25. Chi tiết bảng Wards của dự án

## Quan hệ các bảng

![Hinh minh hoa](media/BaoCaoMau_v1/image39.png)

Hình 3-26. Cấu trúc database của dự án sau khi đã cài đặt.

# THIẾT KẾ CÁC CHỨC NĂNG CỦA HỆ THỐNG

## Use case Xem sản phẩm

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image40.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image41.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image42.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image43.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image44.png)

Hình 4-1. Biểu đồ trình tự usecase xem sản phẩm

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image45.emf)

Hình 4-2. Biểu đồ lớp phân tích usecase xem sản phẩm

## Use case Đánh giá sản phẩm

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image46.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image47.png)

Hình 4-3. Biểu đồ trình tự usecase đánh giá sản phẩm

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image48.emf)

Hình 4-4. Biểu đồ lớp phân tích usecase đánh giá sản phẩm

## Use case Thêm vào giỏ hàng

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image49.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image50.png)

Hình 4-5. Biểu đồ trình tự usecase thêm vào giỏ hàng.

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image51.emf)

Hình 4-6. Biểu đồ lớp phân tích usecase thêm vào giỏ hàng.

## Use case Thêm vào danh sách yêu thích

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image52.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image53.png)

Hình 4-7. Biểu đồ trình tự usecase thêm vào danh sách yêu thích

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image54.emf)

Hình 4-8. Biểu đồ lớp phân tích usecase thêm vào danh sách yêu thích

## Use case Mua hàng

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image55.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image56.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image57.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image58.png)

Hình 4-9. Biểu đồ trình tự usecase mua hàng

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image59.emf)

Hình 4-10. Biểu đồ lớp phân tích usecase mua hàng

## Use case Quản lý thông tin tài khoản

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image60.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image61.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image62.png)

Hình 4-11. Biểu đồ trình tự usecase quản lý thông tin tài khoản

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image63.emf)

Hình 4-12. Biểu đồ lớp phân tích usecase quản lý thông tin tài khoản.

## Use case Đơn hàng của tôi

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image64.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image65.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image66.png)

Hình 4-13. Biểu đồ trình tự usecase đơn hàng của tôi.

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image67.emf)

Hình 4-14. Biểu đồ lớp phân tích usecase đơn hàng của tôi.

## Use case Đăng ký

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image68.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image69.png)

Hình 4-15. Biểu đồ trình tự usecase đăng ký

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image70.png)

Hình 4-16. Biểu đồ lớp phân tích usecase đăng ký

## Use case Đăng nhập

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image71.png)

Hình 4-17. Biểu đồ trình tự usecase đăng nhập

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image72.png)

Hình 4-18. Biểu đồ lớp phân tích usecase đăng nhập

## Use case Quản lý đơn hàng

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image73.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image74.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image75.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image76.png)

Hình 4-19. Biểu đồ trình tự usecase quản lý đơn hàng.

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image77.emf)

Hình 4-20. Biểu đồ lớp phân tích usecase quản lý đơn hàng

## Use case Quản lý khách hàng

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image78.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image79.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image80.png)

Hình 4-21. Biểu đồ trình tự usecase quản lý khách hàng.

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image81.png)

Hình 4-22. Biểu đồ lớp phân tích usecase quản lý khách hàng.

## Use case Quản lý sản phẩm

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image82.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image83.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image84.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image85.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image86.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image87.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image88.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image89.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image90.png)

Hình 4-23. Biểu đồ trình tự usecase quản lý sản phẩm

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image91.emf)

Hình 4-24. Biểu đồ lớp phân tích usecase quản lý sản phẩm

## Use case Quản lý nhân viên

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image92.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image93.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image94.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image95.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image96.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image97.png)

Hình 4-25. Biểu đồ trình tự usecase quản lý nhân viên

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image98.emf)

Hình 4-26. Biểu đồ lớp phân tích usecase quản lý nhân viên

## Use case Thống kê

### Biểu đồ trình tự:

![Hinh minh hoa](media/BaoCaoMau_v1/image99.png)

![Hinh minh hoa](media/BaoCaoMau_v1/image100.png)

Hình 4-27. Biểu đồ trình tự usecase thống kê

### Biểu đồ lớp phân tích:

![Hinh minh hoa](media/BaoCaoMau_v1/image101.emf)

Hình 4-28. Biểu đồ lớp phân tích usecase thống kê

# THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT

## Mô hình kiến trúc dự án

![Hinh minh hoa](media/BaoCaoMau_v1/image102.png)

Hình 5-1. Mô hình kiến trúc onion

### Giới thiệu về kiến trúc onion

Kiến trúc Onion (Onion Architecture) là một kiểu kiến trúc phần mềm được phát triển bởi Jeffrey Palermo nhằm giải quyết các vấn đề về độ phức tạp và sự phụ thuộc trong các ứng dụng lớn. Mục tiêu của kiến trúc này là tạo ra một hệ thống có khả năng bảo trì và mở rộng dễ dàng, đồng thời giảm thiểu sự phụ thuộc giữa các thành phần.

### Các lớp trong kiến trúc onion

Kiến trúc Onion sử dụng khái niệm lớp, nhưng nó khác với kiến trúc N-layer và kiến trúc 3-Tier.

Domain Layer: Lớp này nằm ở trung tâm của kiến trúc nơi chúng ta có các thực thể (entity) của ứng dụng gồm các lớp application model của ứng dụng hoặc các lớp database model phụ thuộc vào cách tiếp cận về code trong quá trình phát triển ứng dụng. Trường hợp sử dụng ASP.NET, các thực thể này được sử dụng để tạo các bảng trong cơ sở dữ liệu (database model).

Repository Layer: Lớp repository hoạt động như một lớp trung gian giữa lớp service và các đối tượng mô hình, các lớp model và database context sẽ được thực hiện trong lớp này. Các lập trình viên sẽ thêm các interface bao gồm các thao tác truy cập dữ liệu cho các thao tác đọc và ghi với cơ sở dữ liệu.

Service Layer: Lớp này được sử dụng để giao tiếp với lớp presentation và repository. Lớp service chứa tất cả logic nghiệp vụ của thực thể (entity). Trong lớp này, các service interface được giữ tách biệt với việc triển khai chúng để các lớp ít phụ thuộc vào nhau

Presentation Layer:  Tương tự như lớp Presentation trong kiến trúc 3 tầng. Nhiệm vụ chính của lớp này là hiển thị dữ liệu với người dùng. Trong trường hợp lớp Presentation API dữ liệu đối tượng từ cơ sở dữ liệu được truyền tải thông qua HTTP request dưới dạng json.

### Ưu nhược điểm của kiến trúc onion

Ưu điểm:

Kiến trúc onion cung cấp cho chúng ta khả năng bảo trì code tốt hơn vì code phụ thuộc vào các lớp

Nó cung cấp khả năng kiểm thử tốt cho các unit tests, chúng ta có thể viết các test cases riêng biệt theo lớp mà không ảnh hưởng đến mô-đun khác trong ứng dụng.

Với kiến trúc onion, các lớp trong ứng dụng sẽ không phụ thuộc lẫn nhau vì các lớp giao tiếp với nhau một cách trừu tượng (thông qua interface)

Các domain entity là cốt lõi và trung tâm của kiến trúc và có quyền truy cập vào cơ sở dữ liệu và Lớp UI.

Lớp bên trong không bao giờ phụ thuộc vào lớp bên ngoài (chiều phụ thuộc từ bên ngoài vào trong)

Nhược điểm

Việc triển khai kiến trúc này đòi hỏi đầu tư thời gian và công sức ban đầu lớn để thiết kế và xây dựng các tầng một cách đúng đắn, dẫn đến chi phí phát triển ban đầu cao hơn.

Đối với các dự án nhỏ, lợi ích của kiến trúc Onion có thể không đáng kể so với độ phức tạp và chi phí phát sinh, làm cho nó trở thành một lựa chọn không phù hợp.

## Giới thiệu ngôn ngữ cài đặt

### ASP.NET Core

![Hinh minh hoa](media/BaoCaoMau_v1/image103.jpeg)

Hình 5-2 Giới thiệu Asp.Net Core

ASP.NET Core là một framework phát triển ứng dụng web mã nguồn mở, hiệu suất cao, do Microsoft và cộng đồng phát triển. Nó được thiết kế để xây dựng các ứng dụng web hiện đại, kết nối IoT và các dịch vụ đám mây. Đây là phiên bản cải tiến và đa nền tảng của ASP.NET, giúp các nhà phát triển xây dựng ứng dụng trên Windows, macOS và Linux. Sau đây là một số đặc điểm của framework này:

Đa nền tảng: Chạy trên Windows, macOS, và Linux.

Hiệu suất cao: Thường đứng đầu trong các bảng xếp hạng hiệu suất.

Mã nguồn mở: Phát triển trên GitHub với sự đóng góp của cộng đồng.

Modular và Lightweight: Sử dụng kiến trúc modular, giảm thiểu footprint.

Middleware: Cấu hình pipeline xử lý yêu cầu HTTP linh hoạt.

Dependency Injection (DI): Tích hợp sẵn, quản lý phụ thuộc dễ dàng.

Razor Pages: Mô hình trang đơn giản hóa giao diện người dùng.

Blazor: Xây dựng ứng dụng web tương tác bằng C#.

Web API: Tạo dịch vụ RESTful APIs dễ dàng.

Công cụ phát triển: Hỗ trợ mạnh mẽ qua Visual Studio, Visual Studio Code, và CLI.

Triển khai linh hoạt: Self-contained hoặc framework-dependent, hỗ trợ Docker.

Tính năng nổi bật: Razor View Engine, Tag Helpers, SignalR, Identity.

Cộng đồng và Tài liệu: Cộng đồng mạnh mẽ và tài liệu phong phú từ Microsoft.

Ưu điểm

Đa nền tảng (Cross-platform): ASP.NET Core cho phép phát triển và triển khai ứng dụng trên nhiều hệ điều hành như Windows, macOS và Linux, tăng tính linh hoạt và khả năng tiếp cận đối với người dùng.

Hiệu suất cao (High Performance): ASP.NET Core được tối ưu hóa để cung cấp hiệu suất cao hơn so với các phiên bản trước đó của ASP.NET, nhờ sử dụng Kestrel và xử lý non-blocking.

Modular và linh hoạt (Modular and Flexible): ASP.NET Core được thiết kế theo mô hình modular, cho phép bạn chỉ cài đặt các thành phần cần thiết, giảm kích thước ứng dụng và tăng tốc độ khởi động.

Hỗ trợ Docker (Docker Support): ASP.NET Core tích hợp tốt với Docker, giúp dễ dàng triển khai và vận hành ứng dụng trên các môi trường khác nhau một cách đồng nhất.

Dependency Injection (DI): ASP.NET Core tích hợp sẵn Dependency Injection, giúp quản lý các phụ thuộc và cung cấp các dịch vụ một cách linh hoạt và dễ dàng kiểm soát.

Configuration cấu hình linh hoạt: ASP.NET Core cung cấp cơ chế cấu hình mạnh mẽ, cho phép bạn cấu hình ứng dụng từ nhiều nguồn khác nhau như file JSON, XML, hoặc các biến môi trường.

Hỗ trợ Web API mạnh mẽ: ASP.NET Core cung cấp một bộ công cụ mạnh mẽ cho việc phát triển các dịch vụ API Web, bao gồm hỗ trợ cho RESTful API và giao thức HTTP.

Nhược điểm:

Thư viện và công cụ hạn chế: Mặc dù hệ sinh thái của ASP.NET Core ngày càng phát triển, nhưng vẫn có một số thư viện và công cụ hạn chế so với các nền tảng phát triển ứng dụng web khác.

Khả năng tương thích: Một số tính năng của ASP.NET Framework không được hỗ trợ hoặc hoạt động khác biệt trên ASP.NET Core, điều này có thể gây khó khăn khi di chuyển từ phiên bản cũ sang phiên bản mới.

### Entity Framework

Entity Framework (EF) là một ORM (Object-Relational Mapping) framework được phát triển bởi Microsoft. Nó là một thành phần của công nghệ .NET và cung cấp một cách tiếp cận dễ dàng và linh hoạt để làm việc với cơ sở dữ liệu trong ứng dụng. Sau đây là một số tổng quan về Entity Framework:

Đối tượng - Quan hệ (Object-Relational): Entity Framework cung cấp một cách tiếp cận đối tượng - quan hệ, cho phép bạn làm việc với cơ sở dữ liệu bằng cách sử dụng các đối tượng và quan hệ giống như trong mã lập trình. Nó ánh xạ các đối tượng trong ứng dụng của bạn vào cơ sở dữ liệu tương ứng, và tự động thực hiện các thao tác CRUD (Create, Read, Update, Delete) trên cơ sở dữ liệu.

Mô hình dữ liệu: Entity Framework cho phép bạn xác định mô hình dữ liệu của ứng dụng bằng cách sử dụng các lớp (classes) và thuộc tính (properties). Bằng cách xác định mối quan hệ giữa các lớp, bạn có thể tạo ra một mô hình dữ liệu logic và dễ dàng thao tác với các thực thể (entities) trong cơ sở dữ liệu.

Linq to Entities: Entity Framework hỗ trợ Linq (Language-Integrated Query) để truy vấn dữ liệu từ cơ sở dữ liệu. Linq to Entities cho phép bạn sử dụng các truy vấn LINQ mạnh mẽ để lấy dữ liệu từ cơ sở dữ liệu một cách linh hoạt và tự nhiên.

Tự động tạo câu lệnh SQL: Entity Framework tự động tạo câu lệnh SQL cần thiết để thao tác với cơ sở dữ liệu dựa trên các thao tác trên đối tượng. Bạn không cần viết câu lệnh SQL thủ công, EF sẽ tự động xử lý việc chuyển đổi giữa đối tượng và cơ sở dữ liệu.

Migration: Entity Framework cung cấp công cụ Migration để quản lý việc thay đổi cấu trúc cơ sở dữ liệu theo thời gian. Bạn có thể thay đổi mô hình dữ liệu và EF sẽ tự động tạo và áp dụng các tác động lên cơ sở dữ liệu mà không làm mất dữ liệu hiện có.

Hỗ trợ đa nền tảng: Entity Framework không chỉ hỗ trợ SQL Server mà còn hỗ trợ nhiều hệ quản trị cơ sở dữ liệu khác như MySQL, PostgreSQL, SQLite và Oracle. Điều này cho phép bạn dễ dàng chuyển đổi giữa các hệ quản trị cơ sở dữ liệu khác nhau mà không cần thay đổi mã lập trình chính.

### Bootstrap

Bootstrap là một framework CSS phổ biến được sử dụng để phát triển các giao diện web thân thiện với thiết bị di động và sau đây là một số tổng quan về Bootstrap.

Responsive Design (Thiết kế đáp ứng): Bootstrap giúp bạn xây dựng các trang web đáp ứng tự động, có nghĩa là giao diện sẽ tự thích ứng và hiển thị phù hợp trên các thiết bị khác nhau như máy tính bàn, máy tính xách tay, điện thoại di động và máy tính bảng.

Grid System (Hệ thống lưới): Bootstrap cung cấp một hệ thống lưới linh hoạt và dễ sử dụng, giúp bạn tạo ra bố cục trang web có cấu trúc gọn gàng và chia cột một cách dễ dàng. Hệ thống lưới của Bootstrap cho phép bạn tạo ra các khu vực và cột có độ rộng linh hoạt, tạo điểm neo cho các phần tử trên trang.

CSS Components (Các thành phần CSS): Bootstrap cung cấp một loạt các thành phần CSS tiện ích như nút, bảng, biểu đồ, thanh điều hướng, hộp thoại, biểu mẫu và nhiều hơn nữa. Các thành phần này đã được thiết kế sẵn và có thể được sử dụng trực tiếp hoặc tùy chỉnh để xây dựng giao diện web.

Typography (Chữ viết): Bootstrap cung cấp một bộ CSS giúp điều chỉnh kiểu chữ, định dạng văn bản và các thành phần liên quan đến typography. Bạn có thể dễ dàng tùy chỉnh các thuộc tính như font-family, font-size, font-weight và màu sắc chữ viết.

JavaScript Plugins (Các plugin JavaScript): Bootstrap đi kèm với một số plugin JavaScript được tích hợp sẵn như carousel (trình chạy hình ảnh), modal (cửa sổ popup), dropdown (menu thả xuống), và nhiều plugin khác. Các plugin này giúp tạo ra các hiệu ứng và chức năng tương tác trên trang web của bạn một cách dễ dàng.

Customization (Tùy chỉnh): Bootstrap cho phép người dùng tùy chỉnh giao diện của mình bằng cách chọn và tùy chỉnh các thành phần, biểu đồ và màu sắc theo ý muốn. Người dùng có thể sử dụng Sass (một ngôn ngữ CSS mở rộng) và các công cụ biên dịch để thay đổi và tạo ra phiên bản tùy chỉnh của Bootstrap.

### Jquery

JQuery là một thư viện JavaScript phổ biến, được thiết kế để đơn giản hóa việc lập trình JavaScript trên các trang web. Được tạo ra bởi John Resig và ra mắt lần đầu vào năm 2006, jQuery đã trở thành một trong những thư viện JavaScript được sử dụng rộng rãi nhất. Dưới đây là một tổng quan về jQuery

JQuery cung cấp một cú pháp đơn giản và ngắn gọn để thực hiện các tác vụ JavaScript phổ biến như thao tác DOM (Document Object Model), xử lý sự kiện, và thực hiện các hiệu ứng động.

JQuery giúp giải quyết vấn đề tương thích giữa các trình duyệt, đảm bảo mã JavaScript hoạt động nhất quán trên các trình duyệt khác nhau như Chrome, Firefox, Safari, và Internet Explorer.

JQuery cung cấp các hàm tiện ích để thực hiện các yêu cầu AJAX dễ dàng, giúp tải dữ liệu không đồng bộ mà không cần làm mới trang.

JQuery có các hàm tích hợp để tạo hiệu ứng và hoạt hình đơn giản mà không cần phải viết nhiều mã phức tạp.

JQuery có một hệ sinh thái plugin phong phú, cho phép mở rộng chức năng của nó mà không cần phải viết lại từ đầu. Có hàng ngàn plugin có sẵn để giải quyết các nhu cầu khác nhau của người dùng.

jQuery cho phép thay đổi các thuộc tính CSS của các phần tử HTML một cách dễ dàng.

### Hệ quản trị cơ sở dữ liệu SQL Server

SQL Server là một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) được phát triển bởi Microsoft. Nó là một trong những hệ quản trị cơ sở dữ liệu phổ biến nhất trên thế giới và được sử dụng rộng rãi trong các ứng dụng doanh nghiệp, web và di động.Dưới đây là một tổng quan về SQL Server:

Tính năng và khả năng: SQL Server cung cấp một loạt các tính năng và khả năng mạnh mẽ để quản lý, lưu trữ và truy vấn dữ liệu. Nó hỗ trợ ngôn ngữ truy vấn SQL, có khả năng xử lý các tác vụ phức tạp như truy vấn dữ liệu, tạo, sửa đổi và xóa cơ sở dữ liệu, và quản lý quyền truy cập. SQL Server cũng cung cấp các tính năng mở rộng như dịch vụ phân tích, khai thác dữ liệu và xử lý dữ liệu trực quan.

Bảo mật: SQL Server cung cấp các cơ chế bảo mật mạnh mẽ để bảo vệ dữ liệu. Nó hỗ trợ xác thực và phân quyền, cho phép quản trị viên quản lý quyền truy cập vào cơ sở dữ liệu và đảm bảo tính bảo mật của dữ liệu.

Quản lý hiệu suất: SQL Server cung cấp các công cụ và tính năng để quản lý hiệu suất của cơ sở dữ liệu. Nó bao gồm trình tối ưu hóa truy vấn, các công cụ giám sát và xử lý lỗi, cơ chế lập lịch và sao lưu dữ liệu.

Khả năng mở rộng: SQL Server cho phép mở rộng hệ thống cơ sở dữ liệu để đáp ứng nhu cầu tăng trưởng của ứng dụng. Nó hỗ trợ cụm cơ sở dữ liệu (database clustering), phân tán dữ liệu và khả năng chia sẻ tài nguyên.

Tích hợp: SQL Server tích hợp tốt với các công nghệ và dịch vụ khác của Microsoft như .NET Framework, Visual Studio và Azure. Điều này giúp việc phát triển ứng dụng và triển khai cơ sở dữ liệu trở nên thuận tiện và liên kết chặt chẽ với các công nghệ Microsoft khác.

Hỗ trợ và cộng đồng: SQL Server có một cộng đồng lớn và mạnh mẽ, với tài liệu phong phú, các diễn đàn thảo luận và các nguồn tài nguyên hữu ích khác. Microsoft cũng cung cấp hỗ trợ chính thức và cập nhật thường xuyên để đảm bảo tính ổn định và an toàn của SQL Server.

## Sơ đồ điều hướng giữa các màn hình

### Biểu đồ điều hướng màn hình của nhóm use case chính

![Hinh minh hoa](media/BaoCaoMau_v1/image104.emf)

Hình 5-3. Biểu đồ điều hướng màn hình của nhóm usecase chính.

### Biểu đồ điều hướng màn hình của nhóm use case thứ cấp

![Hinh minh hoa](media/BaoCaoMau_v1/image105.emf)

Hình 5-4. Biểu đồ điều hướng màn hình của nhóm usecase thứ cấp.

## Thiết kế chi tiết màn hình

### Xem sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image106.png)

Hình 5-5. Giao diện xem sản phẩm

### Đánh giá sản phẩm

Hình 5-6. Thiết kế chi tiết màn hình chức năng đánh giá sản phẩm

### Giỏ hàng

![Hinh minh hoa](media/BaoCaoMau_v1/image107.png)

Hình 5-7. Giao diện giỏ hàng

### Danh sách yêu thích

![Hinh minh hoa](media/BaoCaoMau_v1/image108.png)

Hình 5-8. Giao diện danh sách yêu thích

### Mua hàng

Hình 5-9. Giao diện trang đặt hàng

### Quản lý thông tin tài khoản

Hình 5-10. Giao diện trang quản lý thông tin tài khoản

### Đơn hàng của tôi

Hình 5-11. Giao diện trang đơn hàng của tôi

### Đăng ký

![Hinh minh hoa](media/BaoCaoMau_v1/image109.png)

Hình 5-12. Giao diện trang đăng ký

### Đăng nhập

![Hinh minh hoa](media/BaoCaoMau_v1/image110.png)

Hình 5-13. Giao diện trang đăng nhập

### Quản lý đơn hàng

Hình 5-14. Giao diện trang quản lý đơn hàng

### Quản lý khách hàng

Hình 5-15. Giao diện trang quản lý khách hàng

### Quản lý sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image111.png)

Hình 5-16. Giao diện trang quản lý sản phẩm

### Quản lý nhân viên

Hình 5-17. Giao diện trang quản lý nhân viên

### Thống kê

![Hinh minh hoa](media/BaoCaoMau_v1/image112.png)

Hình 5-18. Giao diện trang thống kê

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

# TỔNG KẾT VÀ ĐÁNH GIÁ

## Kết quả đạt được

Qua quá trình thực hiện đề tài “Xây dựng website bán sách bằng ASP.NET Core” em đã đạt được những kết quả sau:

Hoàn thiện được các chức năng: Trong quá trình thực hiện đồ án em đã xây dựng được các chức năng như xem hàng, xem hàng qua tác giả, thương hiệu, thể loại, xem chi tiết sản phẩm, tích hợp được thanh toán online bằng vnpay, paypal, giúp khách hàng quản lý được đơn hàng, giúp nhân viên và quản trị viên quản lý được sản phẩm, thể loại, khách hàng và xem được báo cáo thống kê.

Giỏ hàng và thanh toán: Hệ thống giỏ hàng hoạt động hiệu quả, cho phép người dùng thêm, xóa, và cập nhật số lượng sách trong giỏ hàng. Chức năng thanh toán được tích hợp với hai phương thức thanh toán trực tuyến phổ biến là vnpay và paypal, đảm bảo giao dịch an toàn và thuận tiện.

Báo cáo và thống kê: Hệ thống báo cáo và thống kê cung cấp cho quản trị viên cái nhìn tổng quan về doanh thu, số lượng sản phẩm bán ra, các sản phẩm được bán nhiều nhất. Điều này hỗ trợ quản trị viên trong việc ra quyết định kinh doanh và chiến lược marketing.

Giao diện thân thiện và tương tác: Giao diện website được thiết kế thân thiện với người dùng, dễ dàng tương tác và điều hướng. Đặc biệt, giao diện này được tối ưu hóa cho cả thiết bị di động và máy tính để bàn, đảm bảo trải nghiệm người dùng tốt trên mọi nền tảng.

Bảo mật: Website được xây dựng với các biện pháp bảo mật tiên tiến nhằm bảo vệ thông tin người dùng và dữ liệu giao dịch.

Áp dụng được kiến trúc Onion: Website được xây dựng theo kiến trúc Onion giúp tách biệt các thành phần ứng dụng, đảm bảo tính độc lập và dễ dàng kiểm thử. Nó tăng cường khả năng bảo trì và mở rộng ứng dụng, giảm thiểu sự phụ thuộc giữa các lớp.

## Hướng phát triển

Đề xuất phát triển: Để hệ thống “Website bán sách bằng ASP.NET Core ” có thể có nhiều chức năng hơn phù hợp với người tiêu dùng và mang đến những trải nghiệm mới mẻ cùng với việc cập nhật liên tục trong tương lai với mong muốn hệ thống có thể được sử dụng chính thức và đưa những sản phẩm thông tin hữu ích đến người dùng, em xin đề xuất một số hướng phát triển tiếp theo:

Tối ưu hóa hiệu suất: Tiếp tục tối ưu hóa hiệu suất hệ thống để đảm bảo đáp ứng nhu cầu người dùng, đặc biệt là trong các quá trình xử lý lớn.

Mở rộng tính năng: Phát triển thêm các tính năng mới như chat trực tiếp với nhân viên hỗ trợ khách hàng, tạo được tính năng tích điểm khách hàng qua các lần mua hàng, theo dõi đơn hàng và thông báo tự động để tăng được khả năng trải nghiệm cho khách hàng.

Tích hợp AI: Phát triển thêm tính năng tư vấn sản phẩm bằng chat bot AI để khách hàng có thêm những sự lựa chọn phù hợp khi mua sản phẩm.

TÀI LIỆU THAM KHẢO

| [1] | Phát triển thương mại điện tử tại Việt Nam: Thực trạng và giải pháp , Tạp chí Kinh tế và Dự báo số 11 - tháng 4/2023 . |
| --- | --- |
| [2] | Microsoft, https://learn.microsoft.com/vi-vn/dotnet/welcome . |
| [3] | Tài liệu kiến trúc onion: https://cafedevcode.com/kien-truc-cu-hanh-onion-architecture-39.html . |
| [4] | Phạm Quang Huy, Nguyễn Tất Bảo Thiện, Hướng Dẫn Lập Trình C#, Thanh Niên, 2023. |
| [5] | Tài liệu ASP.NET Core: https://xuanthulab.net/ . |
| [6] | Josephine Bush, trong Sách Learn SQL Database Programming, ACB Bookstore, 2020. |
| [7] | Tài liệu boostrap: https://getbootstrap.com/docs/ . |
| [8] | Tài liệu Jquery: https://jquery.com/ . |
| [ 9 ] | Tài liệu tích hợp thanh toán VnPay: https://sandbox.vnpayment.vn/apis/. |
| [ 10 ] | Tài liệu tích hợp thanh toán PayPal: https://developer.paypal.com/ . |
| [1 1 ] | Tài liệu Cloudinary: https://cloudinary.com/documentation/ . |
| [12] | https://stackoverflow.com/ . |
