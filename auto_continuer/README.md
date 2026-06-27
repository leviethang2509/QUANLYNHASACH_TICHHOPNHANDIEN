# BOT TỰ ĐỘNG GỬI "TIEP TUC" KHI GẶP LỖI CLINE/AIDER

Bộ công cụ này giúp tự động phát hiện thông báo lỗi màu đỏ của Cline (ví dụ: `[YOLO MODE] Task failed: Too many consecutive mistakes...`) và tự động gõ tin nhắn "tiep tuc" rồi gửi đi để Agent tiếp tục công việc của mình mà không cần con người nhấp chuột thủ công.

---

## 1. Thành phần trong thư mục `auto_continuer`

- **`config.json`**: File cấu hình chứa thông tin tọa độ ô chat, vùng quét lỗi và thông số màu sắc.
- **`calibrate.py`**: Script hỗ trợ bạn lấy tọa độ pixel chính xác trên màn hình bằng cách click chuột.
- **`auto_continuer.py`**: Bot chính quét màn hình định kỳ và thực thi hành động gửi lệnh "tiep tuc".

---

## 2. Chuẩn bị môi trường

Yêu cầu máy cài sẵn Python 3. Bạn cần cài các thư viện bổ sung bằng lệnh sau:

```bash
pip install pyautogui pillow pynput
```

---

## 3. Hướng dẫn cấu hình tọa độ (Calibrate)

Vì độ phân giải và vị trí cửa sổ VS Code của mỗi màn hình khác nhau, bạn nên chạy file calibrate trước để xác định tọa độ chính xác:

1. Chạy lệnh:
   ```bash
   python auto_continuer/calibrate.py
   ```
2. Di chuột đến **ô nhập chat** của Cline (nơi hiển thị dòng chữ *"Type a message..."*) rồi click chuột trái.
   - Script sẽ in ra tọa độ ví dụ: `[Calibrate] Da click chuot tai toa do: X=100, Y=950`.
   - Lưu lại giá trị này để điền vào trường `"chat_input_coords"` trong file `config.json`.
3. Di chuột đến **góc trên bên trái của khu vực thông báo lỗi màu đỏ** thường xuất hiện rồi click chuột trái để ghi nhận tọa độ.
   - Bạn có thể điền tọa độ góc này cùng kích thước quét vào trường `"error_region": [X, Y, Width, Height]` trong file `config.json`. Mặc định quét từ `[0, 0]` đến `[500, 1080]` là toàn bộ nửa trái màn hình.
4. Cập nhật các thông số đó vào file `config.json`.

---

## 4. Chạy Bot tự động

Sau khi đã cấu hình xong tọa độ, hãy mở một cửa sổ Terminal (cmd/powershell) mới bên ngoài và chạy bot để nó chạy ngầm:

```bash
python auto_continuer/auto_continuer.py
```

### Các thông số tùy chỉnh trong `config.json`:
- `scan_interval_seconds`: Số giây giãn cách giữa các lần quét màn hình (mặc định: `5`).
- `chat_input_coords`: Tọa độ X, Y của ô chat Cline (nếu đặt `null` bot sẽ tự động nhận diện cửa sổ VS Code).
- `error_region`: Vùng quét tìm màu đỏ lỗi dạng `[X_bắt_đầu, Y_bắt_đầu, Chiều_rộng, Chiều_cao]`. Nếu để `null` bot sẽ tự động khoanh vùng theo cửa sổ VS Code.
- `consecutive_error_pixels_threshold`: Số pixel màu đỏ liên tục tối thiểu để xác nhận là lỗi đỏ thật sự chứ không phải là một chi tiết nhỏ khác (mặc định: `30` pixel).
- `error_color_rgb_min` và `error_color_rgb_max`: Dải màu đỏ đặc trưng để phát hiện lỗi.

### Cách tắt Bot:
- Nhấn `Ctrl + C` tại cửa sổ Terminal đang chạy bot.
- Hoặc di chuyển chuột thật nhanh vào 1 trong 4 góc màn hình để kích hoạt tính năng dừng khẩn cấp (Fail-Safe) của `PyAutoGUI`.

---

## 5. Chế độ Tự Động Định Vị (Auto-Locate) và Tự Cài Đặt (Auto-Install)

Bot đã được nâng cấp để bạn **chỉ cần chạy**:
- Khi bắt đầu khởi chạy, bot sẽ tự động phát hiện nếu máy thiếu thư viện (`pyautogui`, `pillow`, `pygetwindow`, `pynput`...) và cài đặt tự động qua pip.
- Tiếp theo, bot tìm kiếm cửa sổ có tên `Visual Studio Code` đang hoạt động, sau đó tính toán tự động:
  - Tọa độ ô nhập tin nhắn của Cline (Sidebar góc dưới bên phải).
  - Vùng quét thông báo lỗi đỏ (phần Sidebar bên phải VS Code).
  - Ghi đè tự động vào tệp cấu hình `config.json` để sử dụng mãi mãi.

**Lưu ý**: Bạn hãy đảm bảo cửa sổ VS Code hiển thị đầy đủ trên màn hình (không bị thu nhỏ xuống taskbar) khi khởi chạy bot lần đầu.
