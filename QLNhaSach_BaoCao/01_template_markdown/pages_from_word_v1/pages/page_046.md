---
source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx
page: 46
total_pages: 131
extracted_by: Microsoft Word COM page range
---

# Trang 46

## THIẾT KẾ CƠ SỞ DỮ LIỆU
Mô hình hóa dữ liệu
/
Hình 3-1. Cấu trúc database của dự án sau khi thiết kế
Authors: Dùng để lưu trữ các tác giả trong hệ thống và gồm các thông tin AuthorId, AuthorCode, AuthorName, CodeNumber, AuthorSlug, Information, ImageName, UrlImage. Một tác giả có 0, 1 hoặc nhiều sản phẩm. Một sản phẩm có 0, 1 hoặc nhiều tác giả.
AuthorProducts: Dùng để lưu trữ chi tiết từng tác giả trong hệ thống và gồm các thông tin AuthorId, ProductId.
Banners: Dùng để lưu trữ banner quảng cáo cho các chiến dịch quảng cáo của hệ thống gồm có các thông tin như BannerId, Title, Content, ImageName, UrlImage.
Brands: Dùng để lưu trữ các thương hiệu sản phẩm trong hệ thống và gồm các thông tin BrandId, BrandCode, BrandName, BrandSlug, CodeNumber, Description, ImageName, UrlImage. Một thương hiệu gồm có 0, 1 hoặc nhiều sản phẩm, một sản phẩm thuộc 1 thương hiệu.
