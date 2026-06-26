# Hướng dẫn tránh lỗi font tiếng Việt trong QLNhaSach

## Nguyên nhân

Một số file `.cshtml` mới được lưu ở UTF-8 không BOM. Với ASP.NET MVC trên .NET Framework, Razor/Build provider đôi khi đọc các file này theo ANSI/Windows code page thay vì UTF-8. Khi đó chữ tiếng Việt đúng trong editor sẽ bị render thành dạng mojibake như `SÃ¡ch yÃªu thÃ­ch`, `Thá»‘ng kÃª`, `Äang mÆ°á»£n`.

Lỗi không nằm ở font CSS. Đây là lỗi giải mã byte sai encoding:

- Nội dung thật: UTF-8.
- Runtime/PowerShell cũ đọc nhầm: ANSI/Windows-1252 hoặc code page hệ thống.
- Kết quả trên web: ký tự tiếng Việt bị gãy dù trình duyệt vẫn dùng font bình thường.

## Dấu hiệu nhận biết

- Chỉ một vài view mới bị lỗi, các view cũ vẫn hiển thị đúng.
- `rg "Sách"` có thể tìm thấy chữ đúng, nhưng `Get-Content` trên PowerShell 5 hiển thị `SÃ¡ch`.
- Trình duyệt hiển thị các chuỗi kiểu `Táº¥t cáº£`, `ÄÃ£ tráº£`, `mÆ°á»£n`.

## Quy ước lưu file

Với project ASP.NET MVC .NET Framework này, các file có tiếng Việt nên lưu bằng:

- `.cshtml`: UTF-8 with BOM.
- `.cs`: UTF-8 with BOM nếu có chuỗi tiếng Việt.
- `.config`, `.sql`, `.md`: UTF-8. Nếu file được .NET Framework runtime đọc trực tiếp và có tiếng Việt, ưu tiên UTF-8 with BOM.

Trong Visual Studio:

1. Mở file.
2. Chọn `File > Save As`.
3. Bấm mũi tên cạnh `Save`, chọn `Save with Encoding`.
4. Chọn `Unicode (UTF-8 with signature) - Codepage 65001`.

Trong VS Code:

1. Bấm encoding ở góc phải dưới.
2. Chọn `Save with Encoding`.
3. Chọn `UTF-8 with BOM` cho view Razor có tiếng Việt.

## Cách kiểm tra nhanh

File có UTF-8 BOM sẽ bắt đầu bằng 3 byte:

```text
EF BB BF
```

PowerShell:

```powershell
Format-Hex -Path .\BaiTapLon\Views\Users\Favorites.cshtml | Select-Object -First 1
```

Nếu file không có `EF BB BF` và có tiếng Việt, hãy lưu lại bằng UTF-8 with BOM.

## File đã xử lý

- `BaiTapLon\Views\Users\Favorites.cshtml`
- `BaiTapLon\Areas\Admin\Views\ThongKe\MuonTraChuDe.cshtml`
- `BaiTapLon\Views\Product\ReviewFilePreview.cshtml`

## Ghi nhớ khi thêm view mới

Khi tạo view mới có tiếng Việt, đừng chỉ kiểm tra trong editor. Hãy mở trang qua IIS Express/localhost để xác nhận runtime đọc đúng encoding. Nếu xuất hiện chữ kiểu `SÃ¡ch`, sửa encoding của file trước khi sửa nội dung.
