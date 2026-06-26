---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 47
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 47

Categories: Dùng để lưu trữ các thể loại của hệ thống và gồm có CategoryId, CategoryName, CategoryCode, CategorySlug, CodeNumber, Description. Một thể loại thuộc 0, 1 hoặc nhiều sản phẩm, một sản phẩm có 1 hoặc nhiều thể loại.
CategoryProducts: Dùng để lưu trữ chi tiết từng thể loại trong hệ thống và gồm có các thông tin CategoryId, ProductId.
Comments: Dùng để lưu trữ các đánh giá của khách hàng về sản phẩm trong hệ thống và gồm có các thông tin CommentId, Vote, Message, DateCreated, CustomerId, ProductId. Một đánh giá thuộc 1 sản phẩm, một sản phẩm có 0, 1 hoặc nhiều đánh giá. Một đánh giá thuộc về một khách hàng, một khách hàng sẽ có 0, 1 hoặc nhiều đánh giá.
Customers: Dùng để lưu trữ các khách hàng của hệ thống và gồm có các thông tin CustomerId, FullName, DateOfBirth, Gender, CustomerCode, CodeNumber, Address. Một khách hàng có một tài khoản. Một tài khoản thuộc về 0 hoặc 1 khách hàng.
Cart: Dùng để lưu trữ các dòng trong giỏ hàng của khách hàng gồm có các thông tin Customers, ProductId, Quantity. Một khách hàng có 0, 1 hoặc nhiều dòng giỏ hàng, một dòng giỏ hàng thuộc về một khách hàng. Một sản phẩm có thuộc 0, 1 hoặc nhiều dòng giỏ hàng, một dòng giỏ hàng có một sản phẩm.
Employees: Dùng để lưu trữ các nhân viên của hệ thống gồm có các thông tin EmployeeId, EmployeeName, EmployeeCode, CodeNumber, Gender, Address, DateOfBirth. Một nhân viên có 1 tài khoản, một tài khoản thuộc về 0 hoặc một nhân viên.
FavoriteProducts: Dùng để lưu trữ từng dòng sản phẩm yêu thích của khách hàng và gồm có các thông tin CustomerId, ProductId. Một dòng sản phẩm yêu thích sẽ thuộc về 1 khách hàng, một khách hàng có 0, 1 hoặc nhiều dòng sản phẩm yêu thích. Một dòng sản phẩm yêu thích có 1 sản phẩm, một sản phẩm thuộc về 0, 1 hoặc nhiều dòng sản phẩm yêu thích.
Images: Dùng để lưu trữ các ảnh của sản phẩm và gồm các thông tin ImageId, ImageName, Url, ProductId. Một ảnh thuộc về một sản phẩm, một sản phẩm có 0, 1 hoặc nhiều ảnh.
