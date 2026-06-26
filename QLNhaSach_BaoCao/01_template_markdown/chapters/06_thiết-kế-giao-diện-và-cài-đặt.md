# THIẾT KẾ GIAO DIỆN VÀ CÀI ĐẶT

## Mô hình kiến trúc dự án

![Hinh minh hoa](media/BaoCaoMau_v1/image102.png)

Hình 5-1. Mô hình kiến trúc onion

### Giới thiệu về kiến trúc onion

Kiến trúc Onion (Onion Architecture) là một kiểu kiến trúc phần mềm được phát triển bởi Jeffrey Palermo nhằm giải quyết các vấn đề về độ phức tạp và sự phụ thuộc trong các ứng dụng lớn. Mục tiêu của kiến trúc này là tạo ra một hệ thống có khả năng bảo trì và mở rộng dễ dàng, đồng thời giảm thiểu sự phụ thuộc giữa các thành phần.

### Các lớp trong kiến trúc onion

Kiến trúc Onion sử dụng khái niệm lớp, nhưng nó khác với kiến trúc N-layer và kiến trúc 3-Tier.

Domain Layer: Lớp này nằm ở trung tâm của kiến trúc nơi chúng ta có các thực thể (entity) của ứng dụng gồm các lớp application model của ứng dụng hoặc các lớp database model phụ thuộc vào cách tiếp cận về code trong quá trình phát triển ứng dụng. Trường hợp sử dụng ASP.NET, các thực thể này được sử dụng để tạo các bảng trong cơ sở dữ liệu (database model).

Repository Layer: Lớp repository hoạt động như một lớp trung gian giữa lớp service và các đối tượng mô hình, các lớp model và database context sẽ được thực hiện trong lớp này. Các lập trình viên sẽ thêm các interface bao gồm các thao tác truy cập dữ liệu cho các thao tác đọc và ghi với cơ sở dữ liệu.

Service Layer: Lớp này được sử dụng để giao tiếp với lớp presentation và repository. Lớp service chứa tất cả logic nghiệp vụ của thực thể (entity). Trong lớp này, các service interface được giữ tách biệt với việc triển khai chúng để các lớp ít phụ thuộc vào nhau

Presentation Layer:  Tương tự như lớp Presentation trong kiến trúc 3 tầng. Nhiệm vụ chính của lớp này là hiển thị dữ liệu với người dùng. Trong trường hợp lớp Presentation API dữ liệu đối tượng từ cơ sở dữ liệu được truyền tải thông qua HTTP request dưới dạng json.

### Ưu nhược điểm của kiến trúc onion

Ưu điểm:

Kiến trúc onion cung cấp cho chúng ta khả năng bảo trì code tốt hơn vì code phụ thuộc vào các lớp

Nó cung cấp khả năng kiểm thử tốt cho các unit tests, chúng ta có thể viết các test cases riêng biệt theo lớp mà không ảnh hưởng đến mô-đun khác trong ứng dụng.

Với kiến trúc onion, các lớp trong ứng dụng sẽ không phụ thuộc lẫn nhau vì các lớp giao tiếp với nhau một cách trừu tượng (thông qua interface)

Các domain entity là cốt lõi và trung tâm của kiến trúc và có quyền truy cập vào cơ sở dữ liệu và Lớp UI.

Lớp bên trong không bao giờ phụ thuộc vào lớp bên ngoài (chiều phụ thuộc từ bên ngoài vào trong)

Nhược điểm

Việc triển khai kiến trúc này đòi hỏi đầu tư thời gian và công sức ban đầu lớn để thiết kế và xây dựng các tầng một cách đúng đắn, dẫn đến chi phí phát triển ban đầu cao hơn.

Đối với các dự án nhỏ, lợi ích của kiến trúc Onion có thể không đáng kể so với độ phức tạp và chi phí phát sinh, làm cho nó trở thành một lựa chọn không phù hợp.

## Giới thiệu ngôn ngữ cài đặt

### ASP.NET Core

![Hinh minh hoa](media/BaoCaoMau_v1/image103.jpeg)

Hình 5-2 Giới thiệu Asp.Net Core

ASP.NET Core là một framework phát triển ứng dụng web mã nguồn mở, hiệu suất cao, do Microsoft và cộng đồng phát triển. Nó được thiết kế để xây dựng các ứng dụng web hiện đại, kết nối IoT và các dịch vụ đám mây. Đây là phiên bản cải tiến và đa nền tảng của ASP.NET, giúp các nhà phát triển xây dựng ứng dụng trên Windows, macOS và Linux. Sau đây là một số đặc điểm của framework này:

Đa nền tảng: Chạy trên Windows, macOS, và Linux.

Hiệu suất cao: Thường đứng đầu trong các bảng xếp hạng hiệu suất.

Mã nguồn mở: Phát triển trên GitHub với sự đóng góp của cộng đồng.

Modular và Lightweight: Sử dụng kiến trúc modular, giảm thiểu footprint.

Middleware: Cấu hình pipeline xử lý yêu cầu HTTP linh hoạt.

Dependency Injection (DI): Tích hợp sẵn, quản lý phụ thuộc dễ dàng.

Razor Pages: Mô hình trang đơn giản hóa giao diện người dùng.

Blazor: Xây dựng ứng dụng web tương tác bằng C#.

Web API: Tạo dịch vụ RESTful APIs dễ dàng.

Công cụ phát triển: Hỗ trợ mạnh mẽ qua Visual Studio, Visual Studio Code, và CLI.

Triển khai linh hoạt: Self-contained hoặc framework-dependent, hỗ trợ Docker.

Tính năng nổi bật: Razor View Engine, Tag Helpers, SignalR, Identity.

Cộng đồng và Tài liệu: Cộng đồng mạnh mẽ và tài liệu phong phú từ Microsoft.

Ưu điểm

Đa nền tảng (Cross-platform): ASP.NET Core cho phép phát triển và triển khai ứng dụng trên nhiều hệ điều hành như Windows, macOS và Linux, tăng tính linh hoạt và khả năng tiếp cận đối với người dùng.

Hiệu suất cao (High Performance): ASP.NET Core được tối ưu hóa để cung cấp hiệu suất cao hơn so với các phiên bản trước đó của ASP.NET, nhờ sử dụng Kestrel và xử lý non-blocking.

Modular và linh hoạt (Modular and Flexible): ASP.NET Core được thiết kế theo mô hình modular, cho phép bạn chỉ cài đặt các thành phần cần thiết, giảm kích thước ứng dụng và tăng tốc độ khởi động.

Hỗ trợ Docker (Docker Support): ASP.NET Core tích hợp tốt với Docker, giúp dễ dàng triển khai và vận hành ứng dụng trên các môi trường khác nhau một cách đồng nhất.

Dependency Injection (DI): ASP.NET Core tích hợp sẵn Dependency Injection, giúp quản lý các phụ thuộc và cung cấp các dịch vụ một cách linh hoạt và dễ dàng kiểm soát.

Configuration cấu hình linh hoạt: ASP.NET Core cung cấp cơ chế cấu hình mạnh mẽ, cho phép bạn cấu hình ứng dụng từ nhiều nguồn khác nhau như file JSON, XML, hoặc các biến môi trường.

Hỗ trợ Web API mạnh mẽ: ASP.NET Core cung cấp một bộ công cụ mạnh mẽ cho việc phát triển các dịch vụ API Web, bao gồm hỗ trợ cho RESTful API và giao thức HTTP.

Nhược điểm:

Thư viện và công cụ hạn chế: Mặc dù hệ sinh thái của ASP.NET Core ngày càng phát triển, nhưng vẫn có một số thư viện và công cụ hạn chế so với các nền tảng phát triển ứng dụng web khác.

Khả năng tương thích: Một số tính năng của ASP.NET Framework không được hỗ trợ hoặc hoạt động khác biệt trên ASP.NET Core, điều này có thể gây khó khăn khi di chuyển từ phiên bản cũ sang phiên bản mới.

### Entity Framework

Entity Framework (EF) là một ORM (Object-Relational Mapping) framework được phát triển bởi Microsoft. Nó là một thành phần của công nghệ .NET và cung cấp một cách tiếp cận dễ dàng và linh hoạt để làm việc với cơ sở dữ liệu trong ứng dụng. Sau đây là một số tổng quan về Entity Framework:

Đối tượng - Quan hệ (Object-Relational): Entity Framework cung cấp một cách tiếp cận đối tượng - quan hệ, cho phép bạn làm việc với cơ sở dữ liệu bằng cách sử dụng các đối tượng và quan hệ giống như trong mã lập trình. Nó ánh xạ các đối tượng trong ứng dụng của bạn vào cơ sở dữ liệu tương ứng, và tự động thực hiện các thao tác CRUD (Create, Read, Update, Delete) trên cơ sở dữ liệu.

Mô hình dữ liệu: Entity Framework cho phép bạn xác định mô hình dữ liệu của ứng dụng bằng cách sử dụng các lớp (classes) và thuộc tính (properties). Bằng cách xác định mối quan hệ giữa các lớp, bạn có thể tạo ra một mô hình dữ liệu logic và dễ dàng thao tác với các thực thể (entities) trong cơ sở dữ liệu.

Linq to Entities: Entity Framework hỗ trợ Linq (Language-Integrated Query) để truy vấn dữ liệu từ cơ sở dữ liệu. Linq to Entities cho phép bạn sử dụng các truy vấn LINQ mạnh mẽ để lấy dữ liệu từ cơ sở dữ liệu một cách linh hoạt và tự nhiên.

Tự động tạo câu lệnh SQL: Entity Framework tự động tạo câu lệnh SQL cần thiết để thao tác với cơ sở dữ liệu dựa trên các thao tác trên đối tượng. Bạn không cần viết câu lệnh SQL thủ công, EF sẽ tự động xử lý việc chuyển đổi giữa đối tượng và cơ sở dữ liệu.

Migration: Entity Framework cung cấp công cụ Migration để quản lý việc thay đổi cấu trúc cơ sở dữ liệu theo thời gian. Bạn có thể thay đổi mô hình dữ liệu và EF sẽ tự động tạo và áp dụng các tác động lên cơ sở dữ liệu mà không làm mất dữ liệu hiện có.

Hỗ trợ đa nền tảng: Entity Framework không chỉ hỗ trợ SQL Server mà còn hỗ trợ nhiều hệ quản trị cơ sở dữ liệu khác như MySQL, PostgreSQL, SQLite và Oracle. Điều này cho phép bạn dễ dàng chuyển đổi giữa các hệ quản trị cơ sở dữ liệu khác nhau mà không cần thay đổi mã lập trình chính.

### Bootstrap

Bootstrap là một framework CSS phổ biến được sử dụng để phát triển các giao diện web thân thiện với thiết bị di động và sau đây là một số tổng quan về Bootstrap.

Responsive Design (Thiết kế đáp ứng): Bootstrap giúp bạn xây dựng các trang web đáp ứng tự động, có nghĩa là giao diện sẽ tự thích ứng và hiển thị phù hợp trên các thiết bị khác nhau như máy tính bàn, máy tính xách tay, điện thoại di động và máy tính bảng.

Grid System (Hệ thống lưới): Bootstrap cung cấp một hệ thống lưới linh hoạt và dễ sử dụng, giúp bạn tạo ra bố cục trang web có cấu trúc gọn gàng và chia cột một cách dễ dàng. Hệ thống lưới của Bootstrap cho phép bạn tạo ra các khu vực và cột có độ rộng linh hoạt, tạo điểm neo cho các phần tử trên trang.

CSS Components (Các thành phần CSS): Bootstrap cung cấp một loạt các thành phần CSS tiện ích như nút, bảng, biểu đồ, thanh điều hướng, hộp thoại, biểu mẫu và nhiều hơn nữa. Các thành phần này đã được thiết kế sẵn và có thể được sử dụng trực tiếp hoặc tùy chỉnh để xây dựng giao diện web.

Typography (Chữ viết): Bootstrap cung cấp một bộ CSS giúp điều chỉnh kiểu chữ, định dạng văn bản và các thành phần liên quan đến typography. Bạn có thể dễ dàng tùy chỉnh các thuộc tính như font-family, font-size, font-weight và màu sắc chữ viết.

JavaScript Plugins (Các plugin JavaScript): Bootstrap đi kèm với một số plugin JavaScript được tích hợp sẵn như carousel (trình chạy hình ảnh), modal (cửa sổ popup), dropdown (menu thả xuống), và nhiều plugin khác. Các plugin này giúp tạo ra các hiệu ứng và chức năng tương tác trên trang web của bạn một cách dễ dàng.

Customization (Tùy chỉnh): Bootstrap cho phép người dùng tùy chỉnh giao diện của mình bằng cách chọn và tùy chỉnh các thành phần, biểu đồ và màu sắc theo ý muốn. Người dùng có thể sử dụng Sass (một ngôn ngữ CSS mở rộng) và các công cụ biên dịch để thay đổi và tạo ra phiên bản tùy chỉnh của Bootstrap.

### Jquery

JQuery là một thư viện JavaScript phổ biến, được thiết kế để đơn giản hóa việc lập trình JavaScript trên các trang web. Được tạo ra bởi John Resig và ra mắt lần đầu vào năm 2006, jQuery đã trở thành một trong những thư viện JavaScript được sử dụng rộng rãi nhất. Dưới đây là một tổng quan về jQuery

JQuery cung cấp một cú pháp đơn giản và ngắn gọn để thực hiện các tác vụ JavaScript phổ biến như thao tác DOM (Document Object Model), xử lý sự kiện, và thực hiện các hiệu ứng động.

JQuery giúp giải quyết vấn đề tương thích giữa các trình duyệt, đảm bảo mã JavaScript hoạt động nhất quán trên các trình duyệt khác nhau như Chrome, Firefox, Safari, và Internet Explorer.

JQuery cung cấp các hàm tiện ích để thực hiện các yêu cầu AJAX dễ dàng, giúp tải dữ liệu không đồng bộ mà không cần làm mới trang.

JQuery có các hàm tích hợp để tạo hiệu ứng và hoạt hình đơn giản mà không cần phải viết nhiều mã phức tạp.

JQuery có một hệ sinh thái plugin phong phú, cho phép mở rộng chức năng của nó mà không cần phải viết lại từ đầu. Có hàng ngàn plugin có sẵn để giải quyết các nhu cầu khác nhau của người dùng.

jQuery cho phép thay đổi các thuộc tính CSS của các phần tử HTML một cách dễ dàng.

### Hệ quản trị cơ sở dữ liệu SQL Server

SQL Server là một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) được phát triển bởi Microsoft. Nó là một trong những hệ quản trị cơ sở dữ liệu phổ biến nhất trên thế giới và được sử dụng rộng rãi trong các ứng dụng doanh nghiệp, web và di động.Dưới đây là một tổng quan về SQL Server:

Tính năng và khả năng: SQL Server cung cấp một loạt các tính năng và khả năng mạnh mẽ để quản lý, lưu trữ và truy vấn dữ liệu. Nó hỗ trợ ngôn ngữ truy vấn SQL, có khả năng xử lý các tác vụ phức tạp như truy vấn dữ liệu, tạo, sửa đổi và xóa cơ sở dữ liệu, và quản lý quyền truy cập. SQL Server cũng cung cấp các tính năng mở rộng như dịch vụ phân tích, khai thác dữ liệu và xử lý dữ liệu trực quan.

Bảo mật: SQL Server cung cấp các cơ chế bảo mật mạnh mẽ để bảo vệ dữ liệu. Nó hỗ trợ xác thực và phân quyền, cho phép quản trị viên quản lý quyền truy cập vào cơ sở dữ liệu và đảm bảo tính bảo mật của dữ liệu.

Quản lý hiệu suất: SQL Server cung cấp các công cụ và tính năng để quản lý hiệu suất của cơ sở dữ liệu. Nó bao gồm trình tối ưu hóa truy vấn, các công cụ giám sát và xử lý lỗi, cơ chế lập lịch và sao lưu dữ liệu.

Khả năng mở rộng: SQL Server cho phép mở rộng hệ thống cơ sở dữ liệu để đáp ứng nhu cầu tăng trưởng của ứng dụng. Nó hỗ trợ cụm cơ sở dữ liệu (database clustering), phân tán dữ liệu và khả năng chia sẻ tài nguyên.

Tích hợp: SQL Server tích hợp tốt với các công nghệ và dịch vụ khác của Microsoft như .NET Framework, Visual Studio và Azure. Điều này giúp việc phát triển ứng dụng và triển khai cơ sở dữ liệu trở nên thuận tiện và liên kết chặt chẽ với các công nghệ Microsoft khác.

Hỗ trợ và cộng đồng: SQL Server có một cộng đồng lớn và mạnh mẽ, với tài liệu phong phú, các diễn đàn thảo luận và các nguồn tài nguyên hữu ích khác. Microsoft cũng cung cấp hỗ trợ chính thức và cập nhật thường xuyên để đảm bảo tính ổn định và an toàn của SQL Server.

## Sơ đồ điều hướng giữa các màn hình

### Biểu đồ điều hướng màn hình của nhóm use case chính

![Hinh minh hoa](media/BaoCaoMau_v1/image104.emf)

Hình 5-3. Biểu đồ điều hướng màn hình của nhóm usecase chính.

### Biểu đồ điều hướng màn hình của nhóm use case thứ cấp

![Hinh minh hoa](media/BaoCaoMau_v1/image105.emf)

Hình 5-4. Biểu đồ điều hướng màn hình của nhóm usecase thứ cấp.

## Thiết kế chi tiết màn hình

### Xem sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image106.png)

Hình 5-5. Giao diện xem sản phẩm

### Đánh giá sản phẩm

Hình 5-6. Thiết kế chi tiết màn hình chức năng đánh giá sản phẩm

### Giỏ hàng

![Hinh minh hoa](media/BaoCaoMau_v1/image107.png)

Hình 5-7. Giao diện giỏ hàng

### Danh sách yêu thích

![Hinh minh hoa](media/BaoCaoMau_v1/image108.png)

Hình 5-8. Giao diện danh sách yêu thích

### Mua hàng

Hình 5-9. Giao diện trang đặt hàng

### Quản lý thông tin tài khoản

Hình 5-10. Giao diện trang quản lý thông tin tài khoản

### Đơn hàng của tôi

Hình 5-11. Giao diện trang đơn hàng của tôi

### Đăng ký

![Hinh minh hoa](media/BaoCaoMau_v1/image109.png)

Hình 5-12. Giao diện trang đăng ký

### Đăng nhập

![Hinh minh hoa](media/BaoCaoMau_v1/image110.png)

Hình 5-13. Giao diện trang đăng nhập

### Quản lý đơn hàng

Hình 5-14. Giao diện trang quản lý đơn hàng

### Quản lý khách hàng

Hình 5-15. Giao diện trang quản lý khách hàng

### Quản lý sản phẩm

![Hinh minh hoa](media/BaoCaoMau_v1/image111.png)

Hình 5-16. Giao diện trang quản lý sản phẩm

### Quản lý nhân viên

Hình 5-17. Giao diện trang quản lý nhân viên

### Thống kê

![Hinh minh hoa](media/BaoCaoMau_v1/image112.png)

Hình 5-18. Giao diện trang thống kê
