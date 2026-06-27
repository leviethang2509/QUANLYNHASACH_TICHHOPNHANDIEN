# BÁO CÁO KẾT QUẢ KIỂM THỬ WEB ĐỘC LẬP (WEB TEST REPORT)
**Dự án:** Hệ thống quản lý Nhà Sách Tân Hạnh (DongTrieuBookStoreOnline)  
**Ngày thực hiện:** 27/06/2026  
**Công cụ kiểm thử:** Playwright (NodeJS Engine) & Visual Studio Build  
**Môi trường:** Local Server (http://localhost:56919/)

---

## 1. MỤC TIÊU KIỂM THỬ
* Kiểm thử toàn bộ luồng hoạt động chính (Full End-to-End User Flow) bao gồm: Xem trang chủ, Thêm giỏ hàng, Xác minh logic khi chưa đăng nhập, Đăng nhập quyền Admin, và Luồng thanh toán đối với người dùng đã đăng nhập.
* Phát hiện và lập hồ sơ chi tiết các lỗi (Bugs) bao gồm hình ảnh minh họa để chuyển giao cho đội phát triển sửa lỗi.

---

## 2. KỊCH BẢN KIỂM THỬ (TEST CASES & RESULTS)

| Mã kịch bản | Tên kịch bản | Các bước thực hiện | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **TC001** | Homepage Load & Visual Check | 1. Truy cập `http://localhost:56919/` <br> 2. Xác minh Title trang web hiển thị đúng tên "Nhà sách Tân Hạnh" | Trang chủ tải thành công, giao diện hiển thị đầy đủ. Title khớp regex. | **PASSED** |
| **TC002** | Add Item to Cart (Anonymous) & Redirection Verify | 1. Chọn sách bất kỳ ở trang chủ, click "Thêm vào giỏ" <br> 2. Chuyển hướng tới `/gio-hang/` <br> 3. Click nút "Thanh Toán" mà không đăng nhập | Hệ thống hiển thị cảnh báo từ Toastr: "Bạn cần đăng nhập để thanh toán". | **PASSED** |
| **TC003** | Login Admin & Access Admin Dashboard | 1. Mở sidebar đăng nhập <br> 2. Điền `admin`/`123456` <br> 3. Kiểm tra chuyển hướng an toàn tới trang `/Admin/Homes/Index` | Đăng nhập thành công, admin được chuyển hướng đúng về trang tổng quan. | **PASSED** |
| **TC004** | Cart Checkout Flow with Logged In User | 1. Đăng nhập quyền Admin <br> 2. Quay lại trang chủ, click thêm sách vào giỏ <br> 3. Chuyển hướng tới giỏ hàng `/gio-hang` <br> 4. Nhấn nút "Thanh Toán" trực tuyến | Hệ thống xác thực đăng nhập và điều hướng thành công vào trang thanh toán trực tuyến MoMo. | **PASSED** |

---

## 3. CÁC LỖI NGHIÊM TRỌNG ĐÃ PHÁT HIỆN VÀ KHẮC PHỤC (BUGS FOUND & SOLVED)

### Bug #1: Lỗi HTTP 404 khi truy cập Giỏ Hàng (`/gio-hang/`)
* **Mô tả lỗi:** Khi click xem giỏ hàng hoặc sau khi nhấn Thêm sản phẩm, trang web chuyển hướng đến `/gio-hang/` nhưng IIS báo lỗi **404 - Resource cannot be found**.
* **Nguyên nhân:** Thiếu cấu hình định nghĩa Route cho `gio-hang` trong file `RouteConfig.cs` ở tầng ứng dụng web ASP.NET MVC.
* **Cách sửa (Đã khắc phục):** Đã bổ sung Route cấu hình trong file `d:\DUANNGHIENCUU\QLNhaSacha\BaiTapLon\App_Start\RouteConfig.cs`:
  ```csharp
  routes.MapRoute(
      name: "GioHang",
      url: "gio-hang",
      defaults: new { controller = "Cart", action = "Index" }
  );
  ```

### Bug #2: Lỗi không lưu sản phẩm vào Giỏ Hàng do thiếu gán Session (`AddItem`)
* **Mô tả lỗi:** Khi click thêm sách vào giỏ hàng, server trả về thành công nhưng giỏ hàng hiển thị `0 sản phẩm`.
* **Nguyên nhân:** Lỗi logic code trong Action `AddItem` của `CartController.cs`. Khi thêm sản phẩm mới vào danh sách, ứng dụng thực hiện `list.Add(item)` nhưng lại bỏ quên không cập nhật lưu ngược lại vào `Session[CartSession]`.
* **Cách sửa (Đã khắc phục):** Bổ sung dòng code gán lại session tại dòng 84 trong `d:\DUANNGHIENCUU\QLNhaSacha\BaiTapLon\Controllers\CartController.cs`:
  ```csharp
  Session[CartSession] = list;
  ```

### Bug #3: Lỗi HTTP 404 khi thanh toán trực tuyến (`/thanh-toan-truc-tuyen`)
* **Mô tả lỗi:** Khi người dùng đã đăng nhập nhấn "Thanh toán", website điều hướng tới `/thanh-toan-truc-tuyen` và gặp lỗi **404 - Not Found**.
* **Nguyên nhân:** Thiếu ánh xạ router cho link thanh toán trực tuyến.
* **Cách sửa (Đã khắc phục):** Thêm cấu hình route trong `RouteConfig.cs`:
  ```csharp
  routes.MapRoute(
      name: "ThanhToanTrucTuyen",
      url: "thanh-toan-truc-tuyen",
      defaults: new { controller = "Cart", action = "PaymentMoMo" }
  );
  ```


---

# BÁO CÁO KẾT QUẢ KIỂM THỬ MỞ RỘNG (EXTENDED WEB TEST REPORT)
**Ngày thực hiện:** 27/06/2026  
**Công cụ kiểm thử:** Playwright (NodeJS Engine) & Local IIS Express  
**Môi trường:** Local Server (http://localhost:56919/)

---

## 1. MỤC TIÊU KIỂM THỬ MỞ RỘNG
* Tiếp tục kiểm thử các chức năng độc lập còn lại của trang web nằm ngoài phạm vi luồng thanh toán (TC001 - TC004), bao gồm:
  1. Gửi phản hồi/liên hệ từ khách hàng (Contact Form).
  2. Giao diện Chi tiết sách, bao gồm tính năng Đánh giá/Bình luận sách (Product Reviews & Ratings).
  3. Tính năng thêm sách vào Danh sách yêu thích (Favorite Toggle).
  4. Tính năng Tìm kiếm sách theo từ khóa (Search Results Verification).
  5. Kiểm tra vùng bán kính địa lý cho việc mượn sách (Geofence Check & Rental Eligibility).
  6. Thiết lập vị trí cửa hàng và cấu hình Geofence bán kính tại khu vực Admin Dashboard.
  7. Khả năng tương thích giao diện tối (Dark Mode UI Adaptability).
  8. API OCR CMND/CCCD và tính năng kiểm tra lỗi (OCR ID Card Upload Draft API and Validation).
  9. Tạo mới Nhà cung cấp ở khu vực Admin (Admin Supplier Create Validation and Error Handling).
  10. Tìm kiếm và lọc danh sách Nhà cung cấp ở Admin (Admin Supplier Index and Search Functionality).

## 2. KỊCH BẢN KIỂM THỬ MỞ RỘNG (EXTENDED TEST CASES & RESULTS)

| Mã kịch bản | Tên kịch bản | Các bước thực hiện | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **TC005** | Contact Form Submission & Verification | 1. Truy cập trang Liên Hệ \/Lien-He\ <br> 2. Điền đầy đủ thông tin vào Form phản hồi <br> 3. Click nút "Gửi câu hỏi" | Hệ thống gửi AJAX thành công và hiển thị popup thông báo gửi thành công. | **PASSED** |
| **TC006** | Product Detail & Review Form UI Check | 1. Truy cập trực tiếp trang chi tiết sách \/chi-tiet/mo-hinh-tai-chinh-co-ban-40\ <br> 2. Mở Tab "Đánh giá" <br> 3. Viết bình luận và click gửi khi chưa đăng nhập | Hệ thống nhận dạng user ẩn danh, thực hiện chặn/hiển thị cảnh báo yêu cầu đăng nhập. | **PASSED** |
| **TC007** | Favorite Toggle Functionality | 1. Truy cập trang chi tiết sách và nhấn "Thêm vào yêu thích" (Anonymous) <br> 2. Đăng nhập quyền Admin <br> 3. Truy cập lại trang chi tiết sách và toggle lại yêu thích | - Anonymous: Lưu tạm thời cục bộ vào LocalStorage. <br> - Logged In: AJAX gửi lên backend và cập nhật trạng thái yêu thích thành công. | **PASSED** |
| **TC008** | Product Search Results Verification | 1. Điền từ khóa tìm kiếm "tai-chinh" vào ô tìm kiếm ở Header <br> 2. Nhấn phím Enter <br> 3. Kiểm tra redirect về trang \/tim-kiem?keyWord=tai-chinh\ | Trang kết quả tìm kiếm hiển thị danh sách sách tìm thấy và tổng số kết quả. | **PASSED** |
| **TC009** | Geofence Check & Rental Eligibility | 1. Cấp quyền định vị (Hanoi) <br> 2. Đăng nhập Admin và vào trang chi tiết sách \/chi-tiet/mo-hinh-tai-chinh-co-ban-40\ <br> 3. Kiểm tra trạng thái nút "Mượn sách" | Hệ thống định vị người dùng nằm ngoài vùng cho phép và hiển thị cảnh báo "Chỉ hỗ trợ mượn sách tại Nhà sách Tân Hạnh". | **PASSED** |
| **TC010** | Store Setup in Admin Dashboard | 1. Đăng nhập Admin <br> 2. Truy cập \/Admin/WebManager/StoreLocation\ <br> 3. Xác minh form thông tin nhà sách | Form hiển thị đúng dữ liệu, cấu hình Geofence bán kính và tọa độ hoạt động bình thường. | **PASSED** |
| **TC011** | Theme Toggle & Dark Mode Adaptability | 1. Nhấn nút chuyển đổi theme (\#themeToggleBtn\) tại trang chủ <br> 2. Xác minh thuộc tính \data-theme="dark"\ trên \<html>\ <br> 3. Chuyển sang trang chi tiết sách để kiểm tra tính nhất quán | Giao diện toàn trang được cập nhật theo bộ biến màu Dark Mode (\--bg-app: #0f172a\, \--bg-card: #1e293b\), các thành phần tương phản tốt, không bị lỗi màu văn bản. | **PASSED** |
| **TC012** | OCR ID Card Upload Draft API and Validation | 1. Mở Sidebar tạo tài khoản mới <br> 2. Bấm "Tiếp theo" đến bước CCCD <br> 3. Bấm "Đọc CMND/CCCD" mà không chọn ảnh | Hệ thống nhận diện lỗi và hiển thị thông báo "Vui lòng chọn ảnh CMND/CCCD...". | **PASSED** |
| **TC013** | Admin Supplier Create Validation and Error Handling | 1. Vào Admin -> Thêm nhà cung cấp <br> 2. Nhập số điện thoại sai định dạng, email sai định dạng <br> 3. Bấm submit tạo mới | Hệ thống hiển thị thông báo lỗi chi tiết: "Số điện thoại không đúng định dạng !!!". | **PASSED** |
| **TC014** | Admin Supplier Index and Search Functionality | 1. Vào Admin -> Quản lý nhà cung cấp <br> 2. Nhập "Tân Hạnh" vào ô tìm kiếm <br> 3. Bấm Tìm kiếm và xác minh kết quả | Hệ thống lọc danh sách nhà cung cấp đúng theo từ khóa truy vấn. | **PASSED** |
| **TC015** | Admin Category Creation Validation | 1. Vào Admin -> Thêm thể loại <br> 2. Nhập tên thể loại trùng lặp <br> 3. Click submit tạo mới | Hệ thống hiển thị thông báo lỗi chi tiết: 'Tên thể loại đã tồn tại!!!'. | **PASSED** |
| **TC016** | Admin Rental Requests List & Filters | 1. Vào Admin -> Quản lý mượn sách <br> 2. Chọn bộ lọc trạng thái 'Chờ xác nhận' <br> 3. Click Lọc và xác minh kết quả | Hệ thống lọc danh sách mượn sách đúng theo trạng thái được chọn. | **PASSED** |
| **TC017** | Admin User Management: Invalid Form Fields & Validation | 1. Vào Admin -> Quản lý người dùng -> Thêm mới <br> 2. Nhập Email sai định dạng, Phone sai định dạng <br> 3. Click submit tạo mới | Hệ thống hiển thị thông báo lỗi chi tiết: 'Bạn đã nhập sai định dạng email'. | **PASSED** |
| **TC018** | Admin User Management: User Search & List Page | 1. Vào Admin -> Quản lý người dùng <br> 2. Nhập 'admin' vào ô tìm kiếm <br> 3. Click Tìm kiếm và xác minh kết quả | Hệ thống lọc danh sách người dùng đúng theo từ khóa truy vấn. | **PASSED** |
| **TC019** | Admin Feedback Management: View & Reply Validation | 1. Vào Admin -> Phản hồi liên hệ <br> 2. Chọn liên hệ đầu tiên và bấm Trả lời <br> 3. Điền nội dung trả lời và bấm gửi | Hệ thống xử lý cập nhật trạng thái liên hệ thành công. | **PASSED** |
| **TC020** | Admin Orders Management: Order States Navigation | 1. Vào Admin -> Quản lý hóa đơn <br> 2. Duyệt qua các liên kết bước xử lý (Xác nhận, Đóng gói, Xuất kho, Hoàn thành) | Các trang giao diện tải chính xác dữ liệu và bộ lọc theo trạng thái. | **PASSED** |


---

## 3. CÁC LỖI PHÁT HIỆN TRONG QUÁ TRÌNH KIỂM THỬ MỞ RỘNG VÀ KHẮC PHỤC

### Bug #4: Lỗi HTTP 404 khi truy cập trang Liên Hệ (/Lien-He)
* **Mô tả lỗi:** Khi click vào menu "Liên Hệ" hoặc truy cập trực tiếp url /Lien-He thì IIS báo lỗi **404 - The resource cannot be found**.
* **Nguyên nhân:** Lớp cấu hình Route trong ASP.NET MVC chưa định nghĩa Router cho url Lien-He trỏ về ContactController.
* **Cách sửa (Đã khắc phục):** Thêm cấu hình route trong file RouteConfig.cs:
  `csharp
  routes.MapRoute(
      name: "LienHe",
      url: "Lien-He",
      defaults: new { controller = "Contact", action = "Index" }
  );
  `

### Bug #5: Lỗi HTTP 404 khi sử dụng chức năng tìm kiếm sách (/tim-kiem)
* **Mô tả lỗi:** Khi người dùng nhập từ khóa tìm kiếm (ví dụ: 	ai-chinh) tại ô tìm kiếm trên Header và nhấn Enter, hệ thống chuyển hướng đến /tim-kiem?keyWord=tai-chinh nhưng gặp lỗi **404 - Not Found**.
* **Nguyên nhân:** Lớp cấu hình Route trong ASP.NET MVC chưa định nghĩa Router cho url 	im-kiem trỏ về Action Search thuộc ProductController.
* **Cách sửa (Đã khắc phục):** Thêm cấu hình route trong file RouteConfig.cs:
  `csharp
  routes.MapRoute(
      name: "TimKiem",
      url: "tim-kiem",
      defaults: new { controller = "Product", action = "Search" }
  );
  `

---

## 4. CHI TIẾT BẰNG CHỨNG KIỂM THỬ MỞ RỘNG (SCREENSHOTS EVIDENCE)
Các ảnh chụp màn hình tương ứng với các bước trong quá trình kiểm thử mở rộng được lưu trữ tại thư mục local D:\DUANNGHIENCUU\QLNhaSacha\web-tests\javascript\screenshots\:

1. ** 9_contact_page.png**: Giao diện trang Liên hệ hiển thị bản đồ địa điểm và form nhập thông tin.
2. **10_contact_filled.png**: Form liên hệ đã điền đầy đủ dữ liệu thử nghiệm.
3. **11_contact_result.png**: Popup Toastr thông báo gửi thành công thông tin liên hệ.
4. **12_product_detail.png**: Giao diện chi tiết sách Mô hình tài chính cơ bản.
5. **13_review_anonymous_result.png**: Thông báo yêu cầu đăng nhập hiển thị khi người dùng ẩn danh cố tình gửi đánh giá sách.
6. **14_favorite_anonymous_result.png**: Toastr lưu yêu thích cục bộ trên trình duyệt đối với người dùng vãng lai.
7. **15_favorite_logged_in_result.png**: Toastr cập nhật yêu thích thành công vào cơ sở dữ liệu sau khi Admin đăng nhập.
8. **16_search_results.png**: Giao diện trang kết quả tìm kiếm với từ khóa "tai-chinh" hiển thị đầy đủ sách liên quan.
9. **17_geofence_status.png**: Trạng thái nút "Mượn sách" khi định vị ở khu vực ngoài vùng bán kính địa lý quy định.
10. **18_admin_store_location.png**: Giao diện thiết lập thông tin cơ sở nhà sách và cấu hình Geofence bán kính tại khu vực Admin.
11. **19_theme_light.png**: Giao diện trang chủ mặc định ở chế độ sáng (Light Mode).
12. **20_theme_dark.png**: Giao diện trang chủ sau khi bấm nút chuyển đổi sang chế độ tối (Dark Mode) với cấu trúc màu sắc đồng bộ.
13. **21_detail_dark.png**: Giao diện trang chi tiết cuốn sách "Mô hình tài chính cơ bản" hiển thị chuẩn xác ở chế độ tối (Dark Mode).
14. **22_signup_identity_step.png**: Giao diện Sidebar đăng ký bước 2 - thông tin CMND/CCCD.
15. **23_ocr_validation_error.png**: Giao diện Sidebar đăng ký lỗi validation khi chưa chọn ảnh OCR.
16. **24_admin_ncc_create_empty.png**: Trang thêm mới Nhà cung cấp ban đầu.
17. **25_admin_ncc_create_invalid_filled.png**: Trang thêm mới Nhà cung cấp với dữ liệu sai định dạng đã điền.
18. **26_admin_ncc_create_error_result.png**: Trang hiển thị lỗi validation của Nhà cung cấp từ backend.
19. **27_admin_ncc_list.png**: Giao diện danh sách nhà cung cấp của admin.
20. **28_admin_ncc_search_result.png**: Kết quả tìm kiếm nhà cung cấp theo từ khóa "Tân Hạnh".
21. **29_admin_cat_create_empty.png**: Giao diện trang Thêm thể loại ban đầu.
22. **30_admin_cat_create_filled.png**: Form Thêm thể loại đã điền tên thể loại trùng lặp.
23. **31_admin_cat_create_error_result.png**: Màn hình lỗi thông báo Thêm thể loại trùng lặp từ backend.
24. **32_admin_rental_list.png**: Danh sách yêu cầu mượn sách trong Admin.
25. **33_admin_rental_filtered.png**: Kết quả sau khi lọc danh sách yêu cầu mượn sách theo trạng thái 'Chờ xác nhận'.
26. **34_admin_user_create_empty.png**: Giao diện trang Thêm mới quản trị viên ban đầu.
27. **35_admin_user_create_invalid_filled.png**: Form Thêm mới quản trị viên với dữ liệu lỗi đã điền.
28. **36_admin_user_create_error.png**: Màn hình lỗi thông báo email sai định dạng từ backend.
29. **37_admin_user_list.png**: Giao diện danh sách quản trị viên và người dùng.
30. **38_admin_user_search_result.png**: Kết quả lọc danh sách quản trị viên theo từ khóa 'admin'.
31. **39_admin_feedback_list.png**: Giao diện danh sách các phản hồi liên hệ từ khách hàng.
32. **40_admin_feedback_reply_page.png**: Trang soạn thảo phản hồi liên hệ của Admin.
33. **41_admin_feedback_reply_filled.png**: Trang phản hồi đã điền nội dung trả lời mẫu.
34. **42_admin_feedback_reply_result.png**: Kết quả phản hồi liên hệ thành công.
35. **43_admin_orders_all.png**: Giao diện danh sách toàn bộ hóa đơn.
36. **44_admin_orders_xacnhan.png**: Hóa đơn chờ xác nhận.
37. **45_admin_orders_donggoi.png**: Hóa đơn trong giai đoạn đóng gói.
38. **46_admin_orders_xuatkho.png**: Hóa đơn đã xuất kho.
39. **47_admin_orders_hoanthanh.png**: Hóa đơn đã hoàn thành.

---
**Người báo cáo:** *Hệ thống kiểm thử tự động Antigravity QA Agent*

