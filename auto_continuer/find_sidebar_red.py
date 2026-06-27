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
    
    # We want to check the region Y=600 to Y=800, X=0 to X=450 to see if there is any red warning box.
    # In VS Code, Cline failed banner has:
    # "Task failed: Too many consecutive mistakes..." with a red/orange-ish background or border.
    # Let's inspect all pixels in this specific sidebar region:
    # X from 42 to 42+380 (which is 422), Y from 92 to 92+856 (which is 948).
    # Let's list any rows in this sidebar region that have reddish pixels.
    print("\nScanning sidebar region X=[42..422], Y=[92..948] for reddish pixels:")
    sidebar_row_counts = {}
    for y in range(92, 948):
        for x in range(42, 422):
            r, g, b = img.getpixel((x, y))
            # Let's check for reddish: r > 100, g < 100, b < 100
            if r > 100 and g < 100 and b < 100:
                sidebar_row_counts[y] = sidebar_row_counts.get(y, 0) + 1
                
    sorted_sidebar_rows = sorted(sidebar_row_counts.items(), key=lambda item: item[1], reverse=True)
    print(f"Found {len(sorted_sidebar_rows)} rows in sidebar containing reddish pixels.")
    for y, count in sorted_sidebar_rows[:20]:
        sample_pixels = []
        for x in range(42, 422):
            r, g, b = img.getpixel((x, y))
            if r > 100 and g < 100 and b < 100:
                sample_pixels.append((x, (r, g, b)))
                if len(sample_pixels) >= 5:
                    break
        print(f"  Sidebar Row Y={y}: count = {count} reddish pixels. Samples: {sample_pixels}")

if __name__ == "__main__":
    main()
