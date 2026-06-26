---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
converted_at: 2026-05-13 06:21:54
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
