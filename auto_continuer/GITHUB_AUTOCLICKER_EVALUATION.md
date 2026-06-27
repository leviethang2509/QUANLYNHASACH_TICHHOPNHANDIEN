# Đánh giá & Lựa chọn Dự án Auto Clicker/Macro mã nguồn mở từ GitHub

Tài liệu này đánh giá các dự án Auto Clicker và Macro Runner mã nguồn mở phổ biến trên GitHub, đồng thời hướng dẫn cài đặt và cấu hình chi tiết cho công việc tự động hóa click tọa độ và nhập văn bản tùy chỉnh (auto-click + auto-type) trên môi trường Windows 10.

---

## 1. Danh sách đề xuất các dự án mã nguồn mở trên GitHub

Dựa trên yêu cầu: **Click theo tọa độ** và **Cấu hình nội dung nhập liệu (Auto Type)**.

### Thống kê so sánh các dự án nổi bật:

| Tên dự án (GitHub) | Ngôn ngữ | Hệ điều hành hỗ trợ | Giao diện cấu hình (GUI) | Đánh giá tính năng (Click + Type) | Ưu điểm & Nhược điểm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[Pulover's Macro Creator](https://github.com/Pulover/PuloversMacroCreator)** | AutoHotkey / C++ | Windows | Cực kỳ trực quan, kéo thả, ghi lại thao tác, chỉnh sửa tọa độ và nhập chữ | **Xuất sắc** (Hỗ trợ click tọa độ, gõ text tùy chỉnh, vòng lặp, biến số, logic điều kiện, phím tắt) | **Ưu**: Tốt nhất trên Windows, xuất bản ra file `.ahk` hoặc `.exe` độc lập.<br>**Nhược**: Chỉ chạy trên Windows. |
| **[Actiona](https://github.com/Jmgr/actiona)** (Actionaz) | C++ (Qt) | Windows, Linux | Kéo thả trực quan với các danh mục Action (Click, Text, Key, Loop...) | **Rất tốt** (Cho phép cấu hình chi tiết tọa độ click, nhập liệu text, thời gian chờ) | **Ưu**: Đa nền tảng (chạy được cả Windows và Linux), giao diện hiện đại.<br>**Nhược**: Ít cập nhật gần đây nhưng rất ổn định. |
| **[AutoHotkey](https://github.com/AutoHotkey/AutoHotkey)** | C++ / Assembly | Windows | Không có GUI mặc định (dùng code scripting) | **Xuất sắc** (Là nhân của hầu hết các clicker chuyên nghiệp, hiệu năng cao nhất) | **Ưu**: Siêu nhẹ, mạnh mẽ tuyệt đối, cộng đồng khổng lồ.<br>**Nhược**: Phải viết code script `.ahk` thay vì kéo thả trực quan. |
| **[AutoKey](https://github.com/autokey/autokey)** | Python | Linux (X11) | Có GUI quản lý phím tắt và nội dung văn bản | **Khá** (Thích hợp cho auto-type hơn click) | **Ưu**: Mã nguồn mở Python tốt nhất cho Linux.<br>**Nhược**: Không hỗ trợ Windows natively. |

---

## 2. Lựa chọn khuyến nghị: Pulover's Macro Creator (PMC)

Với môi trường phát triển hiện tại của bạn là **Windows 10**, dự án **Pulover's Macro Creator (PMC)** là lựa chọn tối ưu nhất vì:
1. **Giao diện trực quan**: Cho phép bạn định cấu hình các điểm click (Pin 1, Pin 2) bằng cách lấy tọa độ trực tiếp từ màn hình.
2. **Cấu hình text động**: Hỗ trợ nhập nội dung chat tùy chỉnh dễ dàng qua hộp thoại "Send Text" hoặc "Type Key".
3. **Mã nguồn mở hoàn toàn**: Được lưu trữ tại GitHub `Pulover/PuloversMacroCreator`.
4. **Xuất ra mã nguồn AHK**: Có thể xuất trực tiếp sang kịch bản AutoHotkey (`.ahk`) để chạy ngầm siêu nhẹ mà không cần mở giao diện PMC.

---

## 3. Hướng dẫn thiết lập kịch bản Auto-Click & Auto-Type với Pulover's Macro Creator

Để tái tạo luồng công việc của `auto_continuer` (Click Pin 1 -> Đợi -> Click Pin 2 -> Xóa Text cũ -> Nhập Text mới -> Nhấn Enter) bằng Pulover's Macro Creator, hãy thực hiện theo các bước sau:

### Bước 1: Tải và cài đặt
- Truy cập kho mã nguồn GitHub: [Pulover/PuloversMacroCreator Releases](https://github.com/Pulover/PuloversMacroCreator/releases)
- Tải file cài đặt `.exe` hoặc bản Portable `.zip`.
- Tiến hành cài đặt và khởi động chương trình.

### Bước 2: Tạo kịch bản tự động hóa (Macro)
Trong giao diện PMC, thêm các hành động (Actions) tương ứng với luồng xử lý:

1. **Hành động 1: Click Pin 1 (Target/Run Button)**
   - Click nút **Mouse** (Hình con chuột) trên thanh công cụ.
   - Chọn hành động `Left Click`.
   - Nhập tọa độ `X` và `Y` (Ví dụ: `238`, `906` lấy từ `config.json`).
   - Đặt thời gian chờ sau khi click (Delay): `800 ms`.

2. **Hành động 2: Click Pin 2 (Chat Input Area)**
   - Click tiếp nút **Mouse**.
   - Chọn `Left Click`.
   - Nhập tọa độ `X` và `Y` (Ví dụ: `304`, `957`).
   - Đặt thời gian chờ sau khi click (Delay): `800 ms`.

3. **Hành động 3: Nhấn Ctrl + A để chọn toàn bộ text cũ**
   - Click nút **Keyboard** (Hình bàn phím).
   - Chọn Key: `a` và tích chọn phím bổ trợ `Ctrl` (hoặc gửi tổ hợp `{Ctrl Down}a{Ctrl Up}`).
   - Đặt Delay: `200 ms`.

4. **Hành động 4: Nhấn Delete/Backspace để xóa**
   - Click nút **Keyboard**.
   - Chọn Key: `Delete` hoặc `Backspace`.
   - Đặt Delay: `200 ms`.

5. **Hành động 5: Nhập tin nhắn tiếp tục tùy chỉnh (Auto-Type Text)**
   - Click nút **Text** (Biểu tượng chữ T hoặc Text trong Keyboard).
   - Nhập nội dung tin nhắn của bạn (Ví dụ: kịch bản nhắc AI tiếp tục chạy).
   - Chọn kiểu gửi: `SendRaw` hoặc `SendEvent` (tương đương `pyautogui.write` để giả lập gõ phím mượt mà).
   - Đặt Delay: `500 ms`.

6. **Hành động 6: Nhấn Enter để gửi**
   - Click nút **Keyboard**.
   - Chọn Key: `Enter`.
   - Đặt Delay: `300000 ms` (tương đương 5 phút - 300 giây nếu muốn lặp lại định kỳ).

---

## 4. Kịch bản AutoHotkey (.ahk) tương đương cấu hình của bạn

Dưới đây là file kịch bản AutoHotkey (`.ahk`) mã nguồn mở có thể chạy độc lập. Bạn chỉ cần cài đặt AutoHotkey từ GitHub/Trang chủ và chạy file này:

```autohotkey
#Persistent
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; Biến lưu trữ nội dung tin nhắn và cấu hình
Message := "Continue the current task if it is not yet complete. If the current task has already been completed, analyze the project and automatically implement the next meaningful feature that best fits the existing architecture and roadmap. Ensure the new feature is fully integrated, follows the project's coding style, does not break existing functionality, and includes all necessary code, tests, and documentation where applicable. Repeat this workflow until no further meaningful improvements can be identified"

IntervalMs := 300000 ; 5 phút (300 giây)
Pin1X := 238
Pin1Y := 906
Pin2X := 304
Pin2Y := 957

; Đăng ký Hotkey kích hoạt thủ công bằng Ctrl+Shift+S
^+s::
    GoSub, TriggerSend
return

; Thiết lập bộ hẹn giờ tự động chạy định kỳ
SetTimer, TriggerSend, %IntervalMs%
return

TriggerSend:
    ; 1. Click Pin 1
    Click, %Pin1X%, %Pin1Y%
    Sleep, 800

    ; 2. Click Pin 2 (Chat input)
    Click, %Pin2X%, %Pin2Y%
    Sleep, 800

    ; 3. Xóa tin nhắn cũ (Ctrl+A -> Backspace)
    Send, ^a
    Sleep, 200
    Send, {Backspace}
    Sleep, 200
    Send, ^a
    Sleep, 200
    Send, {Backspace}
    Sleep, 300

    ; 4. Nhập tin nhắn mới bằng Clipboard (cho tốc độ siêu nhanh và chính xác không bị lỗi gõ dấu)
    ClipboardBackup := ClipboardAll
    Clipboard := Message
    ClipWait, 1
    Send, ^v
    Sleep, 500
    Clipboard := ClipboardBackup ; Khôi phục lại bộ nhớ đệm cũ
    
    ; 5. Nhấn Enter để gửi
    Send, {Enter}
    ToolTip, Sent continue message successfully!
    Sleep, 1500
    ToolTip
return
```

### Ưu việt của script AHK này so với Python `auto_continuer.py`:
1. **Dùng Clipboard để Paste**: Tránh được tình trạng gõ chậm từng chữ của PyAutoGUI (giảm thiểu rủi ro bị AI chen ngang hoặc người dùng vô tình di chuột làm hỏng chữ).
2. **Không tốn tài nguyên**: Chạy ngầm tốn chưa đầy 2MB RAM.
3. **Kích hoạt nhanh**: Có thể nhấn tổ hợp phím `Ctrl + Shift + S` bất kỳ lúc nào để gửi tin nhắn ngay lập tức.
