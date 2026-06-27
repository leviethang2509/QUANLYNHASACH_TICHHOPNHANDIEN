import sys
import subprocess

def auto_install_deps():
    required_packages = ["pyautogui", "pillow", "pygetwindow", "opencv-python", "pynput"]
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"[AutoInstall] Dang tu dong cai dat thu vien: {pkg}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                print(f"[AutoInstall] Cai dat {pkg} thanh cong!")
            except Exception as e:
                print(f"[AutoInstall] Loi khi cai dat {pkg}: {e}")

if __name__ == "__main__":
    auto_install_deps()
    import pygetwindow as gw
    import pyautogui
    print("Windows found:")
    for w in gw.getAllWindows():
        if w.title:
            print(f" - {w.title} (Pos: {w.left}, {w.top}, Size: {w.width}x{w.height})")
