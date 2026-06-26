---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 48
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 48

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
