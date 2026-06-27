import os
import sys
import json
import time
import pyautogui

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                if "sidebar_position" not in config:
                    config["sidebar_position"] = "left"  # Default to left as shown in user screenshot
                return config
            except Exception:
                pass
    return {
        "scan_interval_seconds": 5,
        "error_color_rgb_min": [120, 0, 0],
        "error_color_rgb_max": [255, 60, 60],
        "chat_input_coords": None,
        "error_region": None,
        "consecutive_error_pixels_threshold": 30,
        "send_delay_seconds": 1.0,
        "confidence_required": 0.8,
        "sidebar_position": "left"
    }

def save_config(config):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def auto_locate_vs_code():
    """
    Tự động tìm kiếm vị trí cửa sổ VS Code đang mở và suy luận vùng quét lỗi và ô nhập chat.
    Trong VS Code:
    - Sidebar của Cline thường nằm bên phải hoặc bên trái.
    - Dựa vào screenshot và tìm kiếm tiêu đề cửa sổ chứa 'Visual Studio Code',
      chúng ta xác định kích thước cửa sổ để suy luận vùng lỗi đỏ và ô chat.
    """
    try:
        import pygetwindow as gw
    except ImportError:
        return None, None
        
    vs_windows = [w for w in gw.getAllWindows() if 'Visual Studio Code' in w.title]
    if not vs_windows:
        # Nếu không chạy dưới quyền Admin hoặc tiêu đề khác đi, tìm cửa sổ active hoặc lấy toàn màn hình
        print("[AutoLocate] Khong tim thay cua so nao co ten 'Visual Studio Code'.")
        return None, None
        
    # Lấy cửa sổ VS Code đầu tiên tìm thấy
    win = vs_windows[0]
    # Tránh cửa sổ bị thu nhỏ
    if win.isMinimized:
        win.restore()
        time.sleep(0.5)
        
    print(f"[AutoLocate] Tim thay cua so VS Code: '{win.title}'")
    print(f"[AutoLocate] Vi tri: Left={win.left}, Top={win.top}, Width={win.width}, Height={win.height}")
    
    config = load_config()
    sidebar_pos = config.get("sidebar_position", "left").lower()
    print(f"[AutoLocate] Docking position detected/configured: {sidebar_pos}")
    
    if sidebar_pos == "left":
        # Cline is docked on the left side of VS Code
        # Activity Bar is ~50px wide. The sidebar itself is ~350px wide.
        chat_x = win.left + 50 + 175  # ~225px from left edge
        chat_y = win.top + win.height - 65
        
        region_left = win.left + 50
        region_top = win.top + 100
        region_width = 380
        region_height = win.height - 200
    else:
        # Cline is docked on the right side of VS Code
        chat_x = win.left + win.width - 200
        chat_y = win.top + win.height - 65
        
        region_left = win.left + win.width - 450
        region_top = win.top + 100
        region_width = 440
        region_height = win.height - 200
    
    # Giới hạn tọa độ trong màn hình thực tế (tránh số âm)
    region_left = max(0, region_left)
    region_top = max(0, region_top)
    
    chat_coords = [int(chat_x), int(chat_y)]
    error_region = [int(region_left), int(region_top), int(region_width), int(region_height)]
    
    print(f"[AutoLocate] Da tu dong uoc luong toa do ({sidebar_pos} sidebar):")
    print(f"  - Chat input: {chat_coords}")
    print(f"  - Error region: {error_region}")
    
    return chat_coords, error_region

def verify_and_adjust_coords(chat_coords, error_region):
    """
    Ho tro kiem tra bang cach thu click nhe vao o chat.
    """
    if not chat_coords:
        return
    print("\n[AutoLocate] Thu di chuyen chuot den vi tri o chat trong 2 giay de xac nhan...")
    orig_x, orig_y = pyautogui.position()
    pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=1.5)
    time.sleep(0.5)
    pyautogui.moveTo(orig_x, orig_y, duration=0.5)
    print("[AutoLocate] Da thu nghiem vi tri thanh cong.")

def auto_configure():
    config = load_config()
    chat_coords, error_region = auto_locate_vs_code()
    
    if chat_coords and error_region:
        config["chat_input_coords"] = chat_coords
        config["error_region"] = error_region
        save_config(config)
        print("[AutoLocate] Da cap nhat tu dong vao file config.json!")
        verify_and_adjust_coords(chat_coords, error_region)
    else:
        # Fallback to full screen if VS Code window coordinates not accessible
        # Thường màn hình full HD
        screen_w, screen_h = pyautogui.size()
        print(f"[AutoLocate] Su dung fallback toan man hinh ({screen_w}x{screen_h})")
        config["chat_input_coords"] = [screen_w - 200, screen_h - 70]
        config["error_region"] = [screen_w - 450, 100, 440, screen_h - 200]
        save_config(config)
        print("[AutoLocate] Da luu cau hinh mac dinh.")
        
if __name__ == "__main__":
    auto_configure()
