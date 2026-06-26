---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 41
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 41

Quản lý sản phẩm
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
