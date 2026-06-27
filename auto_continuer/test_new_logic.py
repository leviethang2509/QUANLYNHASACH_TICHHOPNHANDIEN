import os
from PIL import Image

def is_reddish(r, g, b):
    # In Cline, the red text "Task failed: Too many consecutive mistakes" is typically pure red/crimson.
    # In VS Code dark mode, the failed block text is around RGB (241, 76, 76) or similar.
    # Or in high contrast/dark themes it might be darker red: (125, 26, 27) or (143, 0, 0).
    # G and B must be relatively small. Let's make sure r is significantly higher than g and b.
    # We should exclude brownish/yellowish pixels (like (153, 87, 27) which has G=87 and B=27, R is only 1.7x G).
    # Red text/banners should have R > 100, and R > G * 2.0, R > B * 2.0.
    # Let's check this constraint.
    return r > 100 and r > g * 2.0 and r > b * 2.0

def main():
    region_img_path = os.path.join(os.path.dirname(__file__), "debug_region.png")
    if not os.path.exists(region_img_path):
        print("debug_region.png not found!")
        return
        
    img = Image.open(region_img_path).convert("RGB")
    w, h = img.size
    print(f"Loaded debug_region.png: {w}x{h}")
    
    reddish_pixels = []
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if is_reddish(r, g, b):
                reddish_pixels.append((x, y, (r, g, b)))
                
    print(f"Total reddish pixels found: {len(reddish_pixels)}")
    if len(reddish_pixels) > 0:
        print("Sample reddish pixels:")
        for idx, (x, y, rgb) in enumerate(reddish_pixels[:30]):
            print(f"  Pixel at x={x}, y={y} -> RGB: {rgb}")
            
if __name__ == "__main__":
    main()
