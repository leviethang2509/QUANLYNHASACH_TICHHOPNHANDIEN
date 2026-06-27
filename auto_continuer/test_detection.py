import os
import json
from PIL import Image

def is_reddish(r, g, b, config):
    min_r = config.get("red_min_r", 100)
    diff_g = config.get("red_diff_g", 40)
    diff_b = config.get("red_diff_b", 40)
    
    # Relative check:
    if r >= min_r and (r - g) >= diff_g and (r - b) >= diff_b:
        return True
        
    # Absolute check fallback:
    min_rgb = config.get("error_color_rgb_min", [120, 0, 0])
    max_rgb = config.get("error_color_rgb_max", [255, 60, 60])
    if (min_rgb[0] <= r <= max_rgb[0]) and (min_rgb[1] <= g <= max_rgb[1]) and (min_rgb[2] <= b <= max_rgb[2]):
        return True
        
    return False

def test_on_image(img_path, config):
    if not os.path.exists(img_path):
        print(f"Image {img_path} not found!")
        return
        
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    print(f"Testing on {img_path} ({w}x{h})...")
    
    threshold = config.get("consecutive_error_pixels_threshold", 30)
    
    # Horizontal check
    found_horizontal = False
    for y in range(h):
        consecutive = 0
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if is_reddish(r, g, b, config):
                consecutive += 1
                if consecutive >= threshold:
                    print(f"  [Horizontal] Triggered at y={y}, x={x} (RGB: {r},{g},{b})")
                    found_horizontal = True
                    break
            else:
                consecutive = 0
        if found_horizontal:
            break
            
    # Vertical check
    found_vertical = False
    for x in range(w):
        consecutive = 0
        for y in range(h):
            r, g, b = img.getpixel((x, y))
            if is_reddish(r, g, b, config):
                consecutive += 1
                if consecutive >= threshold:
                    print(f"  [Vertical] Triggered at x={x}, y={y} (RGB: {r},{g},{b})")
                    found_vertical = True
                    break
            else:
                consecutive = 0
        if found_vertical:
            break
            
    if not found_horizontal and not found_vertical:
        print("  No red error triggered on this image (Status Normal).")
    else:
        print("  RED ERROR TRIGGERED!")

def main():
    config = {
        "red_min_r": 100,
        "red_diff_g": 40,
        "red_diff_b": 40,
        "error_color_rgb_min": [120, 0, 0],
        "error_color_rgb_max": [255, 60, 60],
        "consecutive_error_pixels_threshold": 30
    }
    
    # Test on debug_region.png
    region_path = os.path.join(os.path.dirname(__file__), "debug_region.png")
    test_on_image(region_path, config)
    
    # Let's also check if we relax the threshold or adjust settings
    print("\nTesting with relaxed settings (threshold=15, red_min_r=80, diff=30):")
    relaxed_config = {
        "red_min_r": 80,
        "red_diff_g": 30,
        "red_diff_b": 30,
        "error_color_rgb_min": [120, 0, 0],
        "error_color_rgb_max": [255, 60, 60],
        "consecutive_error_pixels_threshold": 15
    }
    test_on_image(region_path, relaxed_config)

if __name__ == "__main__":
    main()
