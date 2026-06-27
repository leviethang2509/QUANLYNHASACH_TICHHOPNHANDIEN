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
    
    # Let's inspect rows Y=1010 to Y=1045, where we found many reddish pixels.
    # What are the x coordinates of these pixels?
    # Are they near the bottom taskbar? Or in a VS Code panel?
    # Let's check:
    print("\nInspecting reddish pixels in Y=[1015..1045]:")
    for y in range(1015, 1045):
        xs = []
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r > 120 and r - g >= 35 and r - b >= 35:
                xs.append(x)
        if xs:
            # Print start and end of x coordinates
            # Group into ranges
            ranges = []
            if xs:
                start = xs[0]
                prev = xs[0]
                for px in xs[1:]:
                    if px > prev + 1:
                        ranges.append((start, prev))
                        start = px
                    prev = px
                ranges.append((start, prev))
            
            # Print sample colors for first range
            sample_color = img.getpixel((xs[0], y))
            print(f"  Row Y={y}: {len(xs)} reddish pixels. Ranges of X: {ranges}. Color: {sample_color}")

if __name__ == "__main__":
    main()
