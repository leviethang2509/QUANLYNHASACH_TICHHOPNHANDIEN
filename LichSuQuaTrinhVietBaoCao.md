# Lịch sử quá trình viết báo cáo

## 2026-05-10 - Khởi tạo yêu cầu

- Nhận yêu cầu viết báo cáo theo `Template.pdf` và `QuyTrinhVietBaoCao.md`.
- Yêu cầu đầu ra: file DOCX, font Times New Roman cỡ 12, bố cục sát mẫu, có use case, có ảnh quy trình, có lịch sử quá trình viết báo cáo.
- Sinh viên: Lê Việt Thắng.
- MSSV: 2224802010263.
- Đề tài: Quản lý nhà sách tích hợp nhận diện khuôn mặt để mượn trả sách.

## 2026-05-10 - Kiểm tra dữ liệu và môi trường

- Tìm thấy `Template.pdf` tại thư mục gốc project.
- Đọc nội dung `QuyTrinhVietBaoCao.md` để lấy kế hoạch, công nghệ, quy trình nghiệp vụ và phạm vi đề tài.
- Kiểm tra thư viện/công cụ:
  - Có `PIL` để tạo ảnh sơ đồ và ảnh quy trình.
  - Chưa có `python-docx`, nên DOCX được tạo bằng OpenXML thủ công.
  - Chưa tìm thấy `pdftotext` và `drawio` CLI, nên tạo thêm file `.drawio` dạng XML và ảnh PNG tương ứng.
  - Có Chrome tại `C:\Program Files\Google\Chrome\Application\chrome.exe`.
- Kiểm tra ứng dụng ASP.NET:
  - Cổng `56919` đang lắng nghe.
  - Trang chủ truy cập được.
  - Một số màn hình yêu cầu đăng nhập/admin chưa thể chụp đúng luồng nếu chưa có session.

## 2026-05-10 - Chụp ảnh giao diện ứng dụng

- Đã tạo thư mục `report_assets`.
- Đã chụp ảnh trang chủ ứng dụng:
  - `report_assets/screenshot_home.png`
- Đã chụp ảnh danh sách sản phẩm:
  - `report_assets/screenshot_product_list.png`
- Có thử chụp trang đăng nhập và lịch sử mượn, nhưng trang đăng nhập trực tiếp là child action nên không dùng làm hình chính trong báo cáo.

## 2026-05-10 - Tạo sơ đồ và ảnh quy trình

- Đã tạo file draw.io:
  - `report_assets/usecase_quan_ly_nha_sach.drawio`
- Đã tạo ảnh use case:
  - `report_assets/usecase_quan_ly_nha_sach.png`
- Đã tạo ảnh quy trình mượn sách:
  - `report_assets/workflow_muon_sach.png`
- Đã tạo ảnh quy trình OCR CMND/CCCD và xác thực khuôn mặt:
  - `report_assets/workflow_ocr_face.png`
- Đã tạo ảnh quy trình admin xử lý mượn/trả:
  - `report_assets/workflow_admin.png`

## 2026-05-10 - Tạo báo cáo DOCX

- Đã tạo script sinh báo cáo:
  - `scripts/generate_report_docx.py`
- Đã tạo file báo cáo:
  - `BaoCao_QuanLyNhaSach_NhanDienKhuonMat_LeVietThang_2224802010263.docx`
- Định dạng áp dụng:
  - Font mặc định: Times New Roman.
  - Cỡ chữ nội dung: 12.
  - Khổ giấy: A4.
  - Có phân trang theo các phần/chương chính.
  - Có bảng mô tả công nghệ, bảng tác nhân, bảng kiểm thử, kế hoạch tháng 01-05/2026.
  - Có sơ đồ use case, sơ đồ quy trình và ảnh chụp giao diện ứng dụng.

## 2026-05-10 - Kiểm tra sau khi tạo

- Kiểm tra DOCX là file zip OpenXML hợp lệ.
- Kiểm tra `word/document.xml` tồn tại.
- Kiểm tra DOCX có 6 ảnh được chèn vào.
- Kiểm tra tiếng Việt trong DOCX không bị lỗi mã:
  - Có chuỗi `BÁO CÁO`.
  - Có chuỗi `Lê Việt Thắng`.
  - Có chuỗi `2224802010263`.

## Ghi chú còn lại

- Chưa trích xuất trực tiếp được nội dung `Template.pdf` vì máy thiếu công cụ đọc PDF local (`pdftotext`, `PyPDF2`, `pypdf`, `pdfplumber`, `fitz` đều không có).
- Bố cục hiện tại được dựng theo mẫu báo cáo đồ án phổ biến và nội dung trong `QuyTrinhVietBaoCao.md`/source.
- Để sát `Template.pdf` hơn nữa, cần cài/thêm công cụ đọc PDF hoặc cung cấp ảnh/text của template.
- Các ảnh quy trình yêu cầu đăng nhập/admin nên được chụp bổ sung sau khi có tài khoản và phiên đăng nhập phù hợp.


## 2026-05-10 22:41:28

- Đã đọc kế hoạch trong `QuyTrinhVietBaoCao.md` và dựng lại full file `BaoCao.docx`.
- Đã xuất đồng thời `D:\BACKUP_2004_2026_D\QLNhaSach\BaoCao.docx` và `D:\BACKUP_2004_2026_D\NHANDIENKHUONMAT-new07040226\BaoCao.docx`.
- Nội dung đã bổ sung đủ phần đầu báo cáo, chương 1-5, kết luận, tài liệu tham khảo, phụ lục, bảng công nghệ, bảng endpoint, bảng kiểm thử và hình trong `report_assets`.
- Bỏ qua cập nhật file tên dài vì Windows đang khóa file đó; hai file `BaoCao.docx` đã được cập nhật.

## 2026-05-10 22:50:33

- Đã viết lại full `BaoCaoMauSua.docx` theo cấu trúc mẫu 7 chương, thay nội dung theo kế hoạch QLNhaSach + Flask.
- Output được chia thành 50 trang logic bằng 49 ngắt trang rõ ràng.
- Không sửa source ứng dụng; chỉ tạo script báo cáo và ghi lại file báo cáo.

## 2026-05-10 22:55:48

- Đã cập nhật `BaoCaoMauSua.docx` trực tiếp từ nền `BaoCaoMau.docx`, giữ cấu trúc/media/bảng của báo cáo mẫu.
- Số đoạn văn bản đã thay đổi: 594.
- Media giữ lại: 112; bảng giữ lại: 15.
- Cách làm: không dựng lại tài liệu trắng, chỉ thay câu chữ theo từng đoạn/section để phù hợp dự án QLNhaSach + Flask.

## 2026-05-10 22:56:47

- Đã cập nhật `BaoCaoMauSua.docx` trực tiếp từ nền `BaoCaoMau.docx`, giữ cấu trúc/media/bảng của báo cáo mẫu.
- Số đoạn văn bản đã thay đổi: 592.
- Media giữ lại: 112; bảng giữ lại: 15.
- Cách làm: không dựng lại tài liệu trắng, chỉ thay câu chữ theo từng đoạn/section để phù hợp dự án QLNhaSach + Flask.
