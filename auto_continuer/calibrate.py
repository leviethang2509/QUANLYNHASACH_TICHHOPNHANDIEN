import sys
import time
import json
import pyautogui

def on_click(x, y, button, pressed):
    if pressed:
        print(f"\n[Calibrate] Da click chuot tai toa do: X={x}, Y={y}")
        print("Hay ghi lai toa do nay de cap nhat vao file config.json")
        print("  - 'chat_input_coords': vi tri o nhap chat cua Cline")
        print("  - 'error_region' (X_start, Y_start): góc trên bên trái của vùng lỗi đỏ")
        return False  # Dung listener

try:
    from pynput import mouse
except ImportError:
    print("[Calibration] Dang tai va cai dat pynput de ho tro click toa do...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import mouse

print("=================================================================")
print("             CHUONG TRINH CAN CHINH TOA DO CHUOT                 ")
print("=================================================================")
print("Huong dan:")
print("1. Di chuot toi vi tri o nhap chat cua Cline (khu vuc 'Type a message...')")
print("2. Click chuot trai. Toa do se duoc in ra ben duoi.")
print("3. Di chuot toi goc tren ben trai cua khu vuc tin nhan do bi loi.")
print("4. Click chuot trai de lay toa do.")
print("Nhan Ctrl+C de thoat bat ky luc nao.")
print("=================================================================\n")

while True:
    print("Vui long CLICK vao vi tri ban muon lay toa do...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
    cont = input("Ban co muon lay toa do vi tri khac khong? (y/n): ").strip().lower()
    if cont != 'y':
        print("Ket thuc can chinh.")
        break
