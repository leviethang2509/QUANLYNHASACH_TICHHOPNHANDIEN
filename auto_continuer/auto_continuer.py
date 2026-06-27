import os
import sys
import time
import json
import pyautogui
from PIL import Image
import threading

# Global variables for GUI
last_periodic_send_time = time.time()
root_pin1 = None
root_pin2 = None
send_btn = None

# Drag variables for individual pins
drag_x1 = 0
drag_y1 = 0
drag_x2 = 0
drag_y2 = 0

def save_config(config):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

# Pin 1 Dragging Handlers
def start_drag_pin1(event):
    global drag_x1, drag_y1
    drag_x1 = event.x
    drag_y1 = event.y

def drag_pin1(event):
    global root_pin1
    if root_pin1:
        x = root_pin1.winfo_x() - drag_x1 + event.x
        y = root_pin1.winfo_y() - drag_y1 + event.y
        root_pin1.geometry(f"+{x}+{y}")

def stop_drag_pin1(event):
    global root_pin1
    if root_pin1:
        try:
            config = load_config()
            win_w = 120
            win_h = 40
            win_x = root_pin1.winfo_x()
            win_y = root_pin1.winfo_y()
            
            click_x = win_x + win_w // 2
            click_y = win_y + win_h // 2
            config["click_coords_1"] = [click_x, click_y]
            save_config(config)
            print(f"[GUI] Saved Pin 1 coordinates to config.json: [{click_x}, {click_y}]")
        except Exception as e:
            print(f"[GUI] Error saving Pin 1 coordinates: {e}")

# Pin 2 Dragging Handlers
def start_drag_pin2(event):
    global drag_x2, drag_y2
    drag_x2 = event.x
    drag_y2 = event.y

def drag_pin2(event):
    global root_pin2
    if root_pin2:
        x = root_pin2.winfo_x() - drag_x2 + event.x
        y = root_pin2.winfo_y() - drag_y2 + event.y
        root_pin2.geometry(f"+{x}+{y}")

def stop_drag_pin2(event):
    global root_pin2
    if root_pin2:
        try:
            config = load_config()
            win_w = 120
            win_h = 50
            win_x = root_pin2.winfo_x()
            win_y = root_pin2.winfo_y()
            
            click_x = win_x + win_w // 2
            click_y = win_y + win_h // 2
            config["click_coords_2"] = [click_x, click_y]
            config["chat_input_coords"] = [click_x, click_y]
            save_config(config)
            print(f"[GUI] Saved Pin 2 coordinates to config.json: [{click_x}, {click_y}]")
        except Exception as e:
            print(f"[GUI] Error saving Pin 2 coordinates: {e}")

def trigger_action():
    global last_periodic_send_time, root_pin1, root_pin2
    last_periodic_send_time = time.time()
    
    # Hide both windows during execution to avoid clicking them
    if root_pin1:
        root_pin1.withdraw()
        root_pin1.update()
    if root_pin2:
        root_pin2.withdraw()
        root_pin2.update()
        
    time.sleep(0.5)
        
    try:
        config = load_config()
        send_continue_command(config)
    except Exception as e:
        print(f"[GUI] Error sending command: {e}")
        
    if root_pin1:
        root_pin1.deiconify()
        root_pin1.update()
    if root_pin2:
        root_pin2.deiconify()
        root_pin2.update()

def periodic_worker():
    global last_periodic_send_time, root_pin2
    while True:
        try:
            config = load_config()
            interval = config.get("scan_interval_seconds", 5)
            current_time = time.time()
            
            periodic_interval = config.get("periodic_send_interval_seconds", 300)
            time_since_last_periodic = current_time - last_periodic_send_time
            
            if time_since_last_periodic >= periodic_interval:
                print(f"\n[System] Periodic check triggered (after {int(time_since_last_periodic)}s)...")
                if root_pin2:
                    root_pin2.after(0, trigger_action)
                else:
                    send_continue_command(config)
                    last_periodic_send_time = current_time
            
            time.sleep(interval)
        except Exception as e:
            print(f"[Worker] Error in periodic loop: {e}")
            time.sleep(5)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "scan_interval_seconds": 5,
        "error_color_rgb_min": [120, 0, 0],
        "error_color_rgb_max": [255, 60, 60],
        "chat_input_coords": [100, 950],
        "error_region": [0, 0, 500, 1080],
        "consecutive_error_pixels_threshold": 30,
        "red_pixels_count_threshold": 10,
        "send_delay_seconds": 1.0,
        "confidence_required": 0.8,
        "periodic_send_enabled": True,
        "periodic_send_interval_seconds": 300,
        "detect_error_enabled": True
    }

def is_reddish(r, g, b):
    # Dùng logic lọc màu đỏ chủ đạo đã kiểm thử thành công:
    # R > 100, R gấp đôi G và R gấp đôi B
    return r > 100 and r > g * 2.0 and r > b * 2.0

def detect_red_error(config):
    """
    Chụp ảnh màn hình và tìm kiếm vùng màu đỏ đặc trưng của thông báo lỗi Cline/Aider.
    Dựa trên số lượng pixel màu đỏ (reddish pixels) vượt quá ngưỡng (threshold).
    """
    region = config.get("error_region", [0, 0, 1920, 1080])
    # region format: [left, top, width, height]
    left, top, width, height = int(region[0]), int(region[1]), int(region[2]), int(region[3])
    
    # Chụp ảnh khu vực nghi ngờ
    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
    except Exception as e:
        print(f"[Detector] Loi khi chup anh man hinh: {e}")
        return False
        
    # Chuyển sang ảnh RGB
    img = screenshot.convert("RGB")
    w, h = img.size
    
    # Ngưỡng số pixel đỏ tối thiểu để phát hiện lỗi
    threshold = config.get("red_pixels_count_threshold", 10)
    
    reddish_count = 0
    # Quét toàn bộ ảnh để đếm số pixel đỏ
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if is_reddish(r, g, b):
                reddish_count += 1
                if reddish_count >= threshold:
                    # Lưu lại ảnh debug để dễ dàng kiểm tra khi cần thiết
                    debug_dir = os.path.dirname(__file__)
                    debug_path = os.path.join(debug_dir, "debug_region.png")
                    try:
                        screenshot.save(debug_path)
                    except:
                        pass
                    print(f"[Detector] Phat hien loi do: tim thay >= {threshold} pixel mau do (tong so pixel do quet duoc hien tai: {reddish_count})")
                    return True
                
    return False

def send_continue_command(config):
    """
    Tự động click tuần tự: Click Pin 1 -> sleep -> Click Pin 2 (o chat),
    sau đó gõ tin nhắn và nhấn Enter.
    """
    # 1. Click Pin 1
    pin1_coords = config.get("click_coords_1", [100, 800])
    p1_x, p1_y = int(pin1_coords[0]), int(pin1_coords[1])
    print(f"[Action] Dang click vao Pin 1 tai X={p1_x}, Y={p1_y}...")
    pyautogui.click(p1_x, p1_y)
    time.sleep(0.8)

    # 2. Click Pin 2 (Chat input)
    pin2_coords = config.get("click_coords_2", config.get("chat_input_coords", [100, 950]))
    p2_x, p2_y = int(pin2_coords[0]), int(pin2_coords[1])
    print(f"[Action] Dang click vao Pin 2 tai X={p2_x}, Y={p2_y}...")
    pyautogui.click(p2_x, p2_y)
    time.sleep(0.8)
    
    # Xóa văn bản cũ bằng cách nhấn Ctrl+A và Delete/Backspace sử dụng keyDown/keyUp để tăng độ tin cậy
    print("[Action] Dang thuc hien Ctrl+A va Delete/Backspace de xoa van ban cu...")
    
    # Lượt 1: Chọn tất cả và xóa
    pyautogui.keyDown('ctrl')
    time.sleep(0.1)
    pyautogui.press('a')
    time.sleep(0.1)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.2)
    
    # Lượt 2: Double check chọn tất cả và xóa phòng trường hợp lượt 1 chưa ăn focus hoàn toàn
    pyautogui.keyDown('ctrl')
    time.sleep(0.1)
    pyautogui.press('a')
    time.sleep(0.1)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    # Gõ tin nhắn
    message = config.get("continue_message", "Continue from the current project state without restarting or repeating completed work; if the current task is unfinished, continue it, otherwise analyze the project and implement the next highest-priority feature that fits the existing architecture and roadmap; avoid reimplementing existing code, preserve backward compatibility, make only incremental changes, update tests and documentation only when affected, do not build or rebuild the entire solution, do not run Clean or Rebuild, only build the modified project or affected module when absolutely necessary, skip compilation when unnecessary, run only relevant tests, batch changes before validation, and provide a concise summary of completed work, changed files, remaining tasks, and the recommended next feature.")
    print(f"[Action] Dang nhap tin nhan '{message}'...")
    pyautogui.write(message, interval=0.05)
    time.sleep(0.5)
    
    # Nhấn Enter
    print("[Action] Dang nhan Enter de gui...")
    pyautogui.press("enter")
    
    # Đợi thời gian giãn cách để tránh gửi trùng lặp liên tục
    delay = config.get("send_delay_seconds", 5.0)
    print(f"[Action] Cho {delay} giay truoc khi tiep tuc quet...")
    time.sleep(delay)

def main():
    global root_pin1, root_pin2, send_btn, last_periodic_send_time
    
    print("=================================================================")
    print("     BOT TU DONG NHAN DIEN LOI VA GUI 'TIEP TUC' CHO CLINE       ")
    print("=================================================================")
    
    # Tự động cài đặt dependencies trước khi chạy
    try:
        import pygetwindow as gw
    except ImportError:
        print("[System] Dang tu dong kiem tra va cai dat dependencies...")
        import subprocess
        required_packages = ["pyautogui", "pillow", "pygetwindow", "opencv-python", "pynput"]
        for pkg in required_packages:
            try:
                __import__(pkg)
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                
    # Tắt tính năng fail-safe của PyAutoGUI nếu người dùng muốn kéo chuột ra góc màn hình để dừng
    pyautogui.FAILSAFE = True

    # Khởi tạo tọa độ nếu chưa có
    config = load_config()
    if config.get("chat_input_coords") is None:
        print("[System] Chua co cau hinh toa do. Tien hanh auto-locate...")
        try:
            from auto_locate import auto_configure
            auto_configure()
            config = load_config()
        except Exception as e:
            print(f"[System] Khong the auto-locate: {e}")

    # Thử khởi tạo GUI bằng Tkinter
    has_gui = False
    root_pin2_temp = None
    try:
        import tkinter as tk
        root_pin2_temp = tk.Tk()
        has_gui = True
    except Exception as e:
        print(f"[System] Khong the khoi tao GUI (Tkinter): {e}. Bot se chay o che do CLI (Command Line Interface).")
        has_gui = False

    if has_gui and root_pin2_temp is not None:
        print("[System] Khoi chay bot voi Giao dien 2 nut keo tha (GUI mode)...")
        
        # Setup GUI root_pin2 (which acts as the main orchestrator window containing close/send buttons)
        root_pin2 = root_pin2_temp
        root_pin2.title("Auto Continuer - Pin 2")
        root_pin2.overrideredirect(True)
        root_pin2.attributes("-topmost", True)
        try:
            root_pin2.attributes("-alpha", 0.85)
        except Exception:
            pass
            
        root_pin2.configure(bg="#2d2d30")
        
        # Setup GUI root_pin1 (separate borderless widget representing the 1st click location)
        root_pin1 = tk.Toplevel(root_pin2)
        root_pin1.title("Auto Continuer - Pin 1")
        root_pin1.overrideredirect(True)
        root_pin1.attributes("-topmost", True)
        try:
            root_pin1.attributes("-alpha", 0.85)
        except Exception:
            pass
            
        root_pin1.configure(bg="#2d2d30")
        
        # Calculate start position based on saved coordinates
        pin1_coords = config.get("click_coords_1")
        pin2_coords = config.get("click_coords_2", config.get("chat_input_coords"))
        
        screen_w, screen_h = pyautogui.size()
        if not pin1_coords:
            pin1_coords = [screen_w - 200, screen_h - 220]
        if not pin2_coords:
            pin2_coords = [screen_w - 200, screen_h - 70]
            
        # Win dimensions
        W1_WIDTH, W1_HEIGHT = 120, 40
        W2_WIDTH, W2_HEIGHT = 120, 50
        
        w1_x = int(pin1_coords[0] - W1_WIDTH // 2)
        w1_y = int(pin1_coords[1] - W1_HEIGHT // 2)
        w2_x = int(pin2_coords[0] - W2_WIDTH // 2)
        w2_y = int(pin2_coords[1] - W2_HEIGHT // 2)
        
        root_pin1.geometry(f"{W1_WIDTH}x{W1_HEIGHT}+{w1_x}+{w1_y}")
        root_pin2.geometry(f"{W2_WIDTH}x{W2_HEIGHT}+{w2_x}+{w2_y}")
        
        # --- UI elements for Pin 1 ---
        drag_frame1 = tk.Frame(root_pin1, bg="#a83232")  # Distinct reddish theme for Pin 1
        drag_frame1.pack(fill=tk.BOTH, expand=True)
        
        drag_label1 = tk.Label(drag_frame1, text=" ☩ Pin 1 (Click 1)\nDrag to Target", bg="#a83232", fg="#ffffff", font=("Segoe UI", 9, "bold"), cursor="fleur")
        drag_label1.pack(fill=tk.BOTH, expand=True)
        
        # Bindings for Pin 1 dragging
        drag_label1.bind("<Button-1>", start_drag_pin1)
        drag_label1.bind("<B1-Motion>", drag_pin1)
        drag_label1.bind("<ButtonRelease-1>", stop_drag_pin1)
        drag_frame1.bind("<Button-1>", start_drag_pin1)
        drag_frame1.bind("<B1-Motion>", drag_pin1)
        drag_frame1.bind("<ButtonRelease-1>", stop_drag_pin1)
        
        # --- UI elements for Pin 2 (Main window) ---
        drag_frame2 = tk.Frame(root_pin2, bg="#3e3e42")
        drag_frame2.pack(fill=tk.X)
        
        drag_label2 = tk.Label(drag_frame2, text=" ☩ Pin 2 (Chat)", bg="#3e3e42", fg="#ffffff", font=("Segoe UI", 9, "bold"), cursor="fleur")
        drag_label2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def on_close():
            print("[GUI] Dang tat bot...")
            if root_pin1:
                root_pin1.destroy()
            if root_pin2:
                root_pin2.destroy()
            os._exit(0)
            
        close_btn = tk.Button(drag_frame2, text="×", bg="#3e3e42", fg="#ffffff", activebackground="#e81123", activeforeground="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, command=on_close, width=2, height=1)
        close_btn.pack(side=tk.RIGHT)
        
        # Bindings for Pin 2 dragging
        drag_label2.bind("<Button-1>", start_drag_pin2)
        drag_label2.bind("<B1-Motion>", drag_pin2)
        drag_label2.bind("<ButtonRelease-1>", stop_drag_pin2)
        drag_frame2.bind("<Button-1>", start_drag_pin2)
        drag_frame2.bind("<B1-Motion>", drag_pin2)
        drag_frame2.bind("<ButtonRelease-1>", stop_drag_pin2)
        
        # Send Button
        send_btn = tk.Button(root_pin2, text="▶ Send Now", bg="#007acc", fg="#ffffff", activebackground="#0062a3", activeforeground="#ffffff", font=("Segoe UI", 9, "bold"), bd=0, command=trigger_action)
        send_btn.pack(pady=4, padx=6, fill=tk.BOTH, expand=True)
        
        # Bắt đầu thread chạy ngầm
        last_periodic_send_time = time.time()
        worker_thread = threading.Thread(target=periodic_worker, daemon=True)
        worker_thread.start()
        
        # Bắt đầu đếm ngược cập nhật nút bấm
        def update_countdown():
            global last_periodic_send_time
            try:
                cfg = load_config()
                periodic_interval = cfg.get("periodic_send_interval_seconds", 300)
                current_time = time.time()
                time_since_last_periodic = current_time - last_periodic_send_time
                remaining = int(periodic_interval - time_since_last_periodic)
                if remaining < 0:
                    remaining = 0
                send_btn.config(text=f"▶ Send Now ({remaining}s)")
            except Exception:
                pass
            root_pin2.after(1000, update_countdown)
            
        root_pin2.after(1000, update_countdown)
        root_pin2.mainloop()
        
    else:
        # CLI Mode
        print("[System] Khoi chay bot o che do CLI...")
        last_periodic_send_time = time.time()
        
        while True:
            try:
                config = load_config()
                interval = config.get("scan_interval_seconds", 5)
                current_time = time.time()
                
                periodic_interval = config.get("periodic_send_interval_seconds", 300)
                time_since_last_periodic = current_time - last_periodic_send_time
                
                if time_since_last_periodic >= periodic_interval:
                    print(f"\n[System] Kich hoat gui 'tiep tuc' dinh ky (sau {int(time_since_last_periodic)} giay)...")
                    send_continue_command(config)
                    last_periodic_send_time = current_time
                else:
                    remaining = int(periodic_interval - time_since_last_periodic)
                    print(f"[System] Thoi gian cho den lan gui dinh ky tiep theo: {remaining} giay...", end="\r")
                    
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nDa dung bot bang phim Ctrl+C.")
                break
            except Exception as e:
                print(f"\n[Error] Gap loi khi dang chay: {e}")
                time.sleep(5)

if __name__ == "__main__":
    main()
