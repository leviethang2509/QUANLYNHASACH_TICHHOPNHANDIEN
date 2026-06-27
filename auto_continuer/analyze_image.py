import os
from PIL import Image

def main():
    region_img_path = os.path.join(os.path.dirname(__file__), "debug_region.png")
    if not os.path.exists(region_img_path):
        print("debug_region.png not found!")
        return
        
    img = Image.open(region_img_path).convert("RGB")
    w, h = img.size
    print(f"Loaded debug_region.png: {w}x{h}")
    
    # Let's count different ranges of red
    # Red is high R, low/medium G and B.
    # For example, standard red error banner color in VS Code / Cline might be:
    # background: #5a1d1d or #f14c4c or similar.
    # Let's inspect all pixels and group reddish colors.
    red_groups = {}
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # If r is significantly larger than g and b:
            if r > 80 and r > g * 1.5 and r > b * 1.5:
                # Group by rounding to nearest 10
                key = (r // 10 * 10, g // 10 * 10, b // 10 * 10)
                red_groups[key] = red_groups.get(key, 0) + 1
                
    print("\nReddish colors found (grouped by rounding to 10):")
    sorted_groups = sorted(red_groups.items(), key=lambda item: item[1], reverse=True)
    for rgb, count in sorted_groups[:30]:
        print(f"  RGB around {rgb}: count = {count} pixels")

    # Let's search specifically for the red error box from the screenshot.
    # In VS Code dark mode, the red error box or red text could have colors like:
    # - Red error banner background: e.g., (241, 76, 76) or (190, 40, 40) or (161, 41, 41) or (244, 135, 135)
    # - The word "failed" or "Mistakes" or the text: (241, 76, 76)
    # Let's check if there are horizontal lines or large clusters.
    print("\nScanning for horizontal lines/clusters of reddish pixels:")
    for y in range(h):
        reddish_in_row = []
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # A generous definition of reddish: R > 100 and R > G + 30 and R > B + 30
            if r > 100 and r > g + 25 and r > b + 25:
                reddish_in_row.append(x)
        if len(reddish_in_row) > 10:
            # check if there are contiguous blocks
            contiguous = 0
            max_contiguous = 0
            for i in range(len(reddish_in_row)):
                if i == 0 or reddish_in_row[i] == reddish_in_row[i-1] + 1:
                    contiguous += 1
                else:
                    max_contiguous = max(max_contiguous, contiguous)
                    contiguous = 1
            max_contiguous = max(max_contiguous, contiguous)
            if max_contiguous > 15:
                # print row details
                sample_pixels = [img.getpixel((rx, y)) for rx in reddish_in_row[:5]]
                print(f"  Row {y}: {len(reddish_in_row)} reddish pixels, max contiguous: {max_contiguous}. Samples: {sample_pixels}")

if __name__ == "__main__":
    main()
