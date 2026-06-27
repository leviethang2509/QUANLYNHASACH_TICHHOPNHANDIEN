import os
from PIL import Image

def main():
    fs_img_path = os.path.join(os.path.dirname(__file__), "debug_fullscreen.png")
    if not os.path.exists(fs_img_path):
        print("debug_fullscreen.png not found!")
        return
        
    img = Image.open(fs_img_path).convert("RGB")
    w, h = img.size
    print(f"Loaded debug_fullscreen.png: {w}x{h}")
    
    # We want to find clusters of red pixels.
    # Let's define reddish:
    # 1. R > 120 and R > G + 40 and R > B + 40
    # Or 2. R > 180 and G < 100 and B < 100
    # Let's count how many reddish pixels we find in the entire screen and group them by y coordinate
    row_counts = {}
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r > 120 and r - g >= 35 and r - b >= 35:
                row_counts[y] = row_counts.get(y, 0) + 1
                
    print("\nRows with most reddish pixels:")
    sorted_rows = sorted(row_counts.items(), key=lambda item: item[1], reverse=True)
    for y, count in sorted_rows[:30]:
        # Sample some pixels in this row to see what they are
        sample_pixels = []
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r > 120 and r - g >= 35 and r - b >= 35:
                sample_pixels.append((x, (r, g, b)))
                if len(sample_pixels) >= 5:
                    break
        print(f"  Row Y={y}: count = {count} reddish pixels. Samples: {sample_pixels}")

if __name__ == "__main__":
    main()
