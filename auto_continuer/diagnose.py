import os
import json
import pyautogui
from PIL import Image
import ctypes

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def main():
    print("=================================================================")
    print("             DIAGNOSE SCRIPT FOR AUTO-CONTINUER                  ")
    print("=================================================================")
    
    config = load_config()
    region = config.get("error_region", [0, 0, 1920, 1080])
    chat_coords = config.get("chat_input_coords", [100, 950])
    
    print(f"Configured Error Region: {region}")
    print(f"Configured Chat Coordinates: {chat_coords}")
    
    # Get screen sizes
    pyautogui_size = pyautogui.size()
    print(f"PyAutoGUI Screen Size: {pyautogui_size}")
    
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware() # Make process DPI aware so we get actual physical coordinates
        physical_w = user32.GetSystemMetrics(0)
        physical_h = user32.GetSystemMetrics(1)
        print(f"Physical Screen Size (DPI Aware): {physical_w}x{physical_h}")
    except Exception as e:
        print(f"Could not get DPI aware screen size: {e}")
        
    left, top, width, height = int(region[0]), int(region[1]), int(region[2]), int(region[3])
    
    # Let's take a fullscreen screenshot first to see where things are
    print("Taking fullscreen screenshot...")
    fullscreen = pyautogui.screenshot()
    fullscreen.save(os.path.join(os.path.dirname(__file__), "debug_fullscreen.png"))
    print(f"Saved fullscreen screenshot to auto_continuer/debug_fullscreen.png (size: {fullscreen.size})")
    
    # Let's take the region screenshot
    print("Taking region screenshot...")
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(os.path.join(os.path.dirname(__file__), "debug_region.png"))
    print(f"Saved region screenshot to auto_continuer/debug_region.png (size: {screenshot.size})")
    
    # Analyze colors in the region
    img = screenshot.convert("RGB")
    w, h = img.size
    
    # Let's count red pixels
    min_rgb = config.get("error_color_rgb_min", [120, 0, 0])
    max_rgb = config.get("error_color_rgb_max", [255, 60, 60])
    
    red_pixel_coords = []
    
    print(f"Searching for red pixels in range R: {min_rgb[0]}-{max_rgb[0]}, G: {min_rgb[1]}-{max_rgb[1]}, B: {min_rgb[2]}-{max_rgb[2]}...")
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if (min_rgb[0] <= r <= max_rgb[0]) and (min_rgb[1] <= g <= max_rgb[1]) and (min_rgb[2] <= b <= max_rgb[2]):
                red_pixel_coords.append((x, y, (r, g, b)))
                
    print(f"Found {len(red_pixel_coords)} red pixels matching the criteria in region.")
    if len(red_pixel_coords) > 0:
        print("Sample matching pixels (up to 20):")
        for i, (rx, ry, rgb) in enumerate(red_pixel_coords[:20]):
            print(f"  Pixel inside region at x={rx}, y={ry} (Absolute: X={left + rx}, Y={top + ry}) -> RGB: {rgb}")
            
    # Let's print out common colors (color histogram check) or some non-zero colors that might be red
    print("\nLooking for any reddish pixels in the region (r > 100, g < 100, b < 100):")
    reddish_pixels = []
    for y in range(0, h, max(1, h // 50)): # sample rows
        for x in range(0, w, max(1, w // 50)): # sample columns
            r, g, b = img.getpixel((x, y))
            if r > 100 and g < 100 and b < 100:
                reddish_pixels.append((x, y, (r, g, b)))
    print(f"Found {len(reddish_pixels)} sampled reddish pixels.")
    for i, (rx, ry, rgb) in enumerate(reddish_pixels[:20]):
        print(f"  Sample reddish at x={rx}, y={ry} -> RGB: {rgb}")

if __name__ == "__main__":
    main()
