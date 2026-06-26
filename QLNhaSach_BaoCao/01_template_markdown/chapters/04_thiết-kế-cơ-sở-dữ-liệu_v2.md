# THIẾT KẾ CƠ SỞ DỮ LIỆU

## Mô hình hóa dữ liệu

![Hinh minh hoa](media/BaoCaoMau_v2/image14.png)

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

![Hinh minh hoa](media/BaoCaoMau_v2/image15.png)

Hình 3-2. Chi tiết bảng Authors của dự án

Bảng AuthorProducts

![Hinh minh hoa](media/BaoCaoMau_v2/image16.png)

Hình 3-3. Chi tiết bảng AuthorProducts của dự án

Bảng Banners

![Hinh minh hoa](media/BaoCaoMau_v2/image17.png)

Hình 3-4. Chi tiết bảng Banners của dự án

Bảng Brands

![Hinh minh hoa](media/BaoCaoMau_v2/image18.png)

Hình 3-5. Chi tiết bảng Brands của dự án.

Bảng Categories

![Hinh minh hoa](media/BaoCaoMau_v2/image19.png)

Hình 3-6. Chi tiết bảng Categories của dự án.

Bảng CategoryProducts

![Hinh minh hoa](media/BaoCaoMau_v2/image20.png)

Hình 3-7. Chi tiết bảng CategoryProducts của dự án

Bảng Comments

![Hinh minh hoa](media/BaoCaoMau_v2/image21.png)

Hình 3-8. Chi tiết bảng Comments của dự án.

Bảng Customers

![Hinh minh hoa](media/BaoCaoMau_v2/image22.png)

Hình 3-9. Chi tiết bảng Customers của dự án.

Bảng Employees

![Hinh minh hoa](media/BaoCaoMau_v2/image23.png)

Hình 3-10. Chi tiết bảng Employees của dự án.

Bảng FavouriteProducts

![Hinh minh hoa](media/BaoCaoMau_v2/image24.png)

Hình 3-11. Chi tiết bảng FavouriteProducts của dự án.

Bảng Images

![Hinh minh hoa](media/BaoCaoMau_v2/image25.png)

Hình 3-12. Chi tiết bảng Images của dự án

Bảng Orders

![Hinh minh hoa](media/BaoCaoMau_v2/image26.png)

Hình 3-13. Chi tiết bảng Orders của dự án

Bảng OrderDetails

![Hinh minh hoa](media/BaoCaoMau_v2/image27.png)

Hình 3-14. Chi tiết bảng OrderDetails của dự án.

Bảng Products

![Hinh minh hoa](media/BaoCaoMau_v2/image28.png)

Hình 3-15. Chi tiết bảng Products của dự án.

Bảng Users

![Hinh minh hoa](media/BaoCaoMau_v2/image29.png)

Hình 3-16. Chi tiết bảng Users của dự án.

Bảng UserClaims

![Hinh minh hoa](media/BaoCaoMau_v2/image30.png)

Hình 3-17. Chi tiết bảng UserClaims của dự án.

Bảng Roles

![Hinh minh hoa](media/BaoCaoMau_v2/image31.png)

Hình 3-18. Chi tiết bảng Roles của dự án.

Bảng RoleClaims

![Hinh minh hoa](media/BaoCaoMau_v2/image32.png)

Hình 3-19. Chi tiết bảng RoleClaims của dự án

Bảng UserRoles

![Hinh minh hoa](media/BaoCaoMau_v2/image33.png)

Hình 3-20. Chi tiết bảng UserRoles của dự án

Bảng UserLogins

![Hinh minh hoa](media/BaoCaoMau_v2/image34.png)

Hình 3-21. Chi tiết bảng UserLogins của dự án

Bảng UserTokens

![Hinh minh hoa](media/BaoCaoMau_v2/image35.png)

Hình 3-22. Chi tiết bảng UserTokens của dự án.

Bảng Provinces

![Hinh minh hoa](media/BaoCaoMau_v2/image36.png)

Hình 3-23. Chi tiết bảng Provinces của dự án

Bảng Districts

![Hinh minh hoa](media/BaoCaoMau_v2/image37.png)

Hình 3-24. Chi tiết bảng Districts của dự án.

Bảng Wards

![Hinh minh hoa](media/BaoCaoMau_v2/image38.png)

Hình 3-25. Chi tiết bảng Wards của dự án

## Quan hệ các bảng

![Hinh minh hoa](media/BaoCaoMau_v2/image39.png)

Hình 3-26. Cấu trúc database của dự án sau khi đã cài đặt.
