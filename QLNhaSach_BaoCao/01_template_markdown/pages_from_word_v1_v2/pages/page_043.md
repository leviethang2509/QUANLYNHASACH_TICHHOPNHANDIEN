---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 43
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 43

Quản lý nhân viên
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
Quản trị viên lựa chọn các quyền cho tài khoản của nhân viên vừa chọn và kích nút Xác nhận thì hệ thống sẽ cập nhật các bản ghi có liên quan tới tài khoản của
