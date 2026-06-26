---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 91
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 91

dụng. Trường hợp sử dụng ASP.NET, các thực thể này được sử dụng để tạo các bảng trong cơ sở dữ liệu (database model).
Repository Layer: Lớp repository hoạt động như một lớp trung gian giữa lớp service và các đối tượng mô hình, các lớp model và database context sẽ được thực hiện trong lớp này. Các lập trình viên sẽ thêm các interface bao gồm các thao tác truy cập dữ liệu cho các thao tác đọc và ghi với cơ sở dữ liệu.
Service Layer: Lớp này được sử dụng để giao tiếp với lớp presentation và repository. Lớp service chứa tất cả logic nghiệp vụ của thực thể (entity). Trong lớp này, các service interface được giữ tách biệt với việc triển khai chúng để các lớp ít phụ thuộc vào nhau
Presentation Layer:  Tương tự như lớp Presentation trong kiến trúc 3 tầng. Nhiệm vụ chính của lớp này là hiển thị dữ liệu với người dùng. Trong trường hợp lớp Presentation API dữ liệu đối tượng từ cơ sở dữ liệu được truyền tải thông qua HTTP request dưới dạng json.
Ưu nhược điểm của kiến trúc onion
Ưu điểm:
Kiến trúc onion cung cấp cho chúng ta khả năng bảo trì code tốt hơn vì code phụ thuộc vào các lớp
Nó cung cấp khả năng kiểm thử tốt cho các unit tests, chúng ta có thể viết các test cases riêng biệt theo lớp mà không ảnh hưởng đến mô-đun khác trong ứng dụng.
Với kiến trúc onion, các lớp trong ứng dụng sẽ không phụ thuộc lẫn nhau vì các lớp giao tiếp với nhau một cách trừu tượng (thông qua interface)
Các domain entity là cốt lõi và trung tâm của kiến trúc và có quyền truy cập vào cơ sở dữ liệu và Lớp UI.
Lớp bên trong không bao giờ phụ thuộc vào lớp bên ngoài (chiều phụ thuộc từ bên ngoài vào trong)
