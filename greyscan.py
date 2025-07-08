import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

def is_gray_band(band, flatness_thresh=5, brightness_min=30, brightness_max=230):
    gray_stddev = np.std(band)
    gray_mean = np.mean(band)
    return gray_stddev < flatness_thresh and brightness_min < gray_mean < brightness_max

def scan_image_for_gray_bands(image_path, band_height=20):
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return False, "Not readable or not an image"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height = gray.shape[0]

        for y in range(0, height, band_height):
            band = gray[y:y+band_height, :]
            if band.shape[0] < band_height:
                continue
            if is_gray_band(band):
                return True, f"Gray bar at line {y}-{y+band_height}"
        return False, None

    except Exception as e:
        return True, f"Error while processing: {str(e)}"

def batch_scan_images(root_path, extensions=(".jpg", ".jpeg", ".png")):
    all_images = list(Path(root_path).rglob("*"))
    image_files = [p for p in all_images if p.suffix.lower() in extensions]

    results = []

    for image_path in tqdm(image_files, desc="Checking images"):
        corrupted, reason = scan_image_for_gray_bands(image_path)
        if corrupted:
            results.append((image_path, reason))

    return results

if __name__ == "__main__":
    import sys
    from datetime import datetime

    if len(sys.argv) < 2:
        print("Usage: python greyscan.py <path_to_folder>")
        sys.exit(1)

    folder = sys.argv[1]
    print(f"Starting scan in '{folder}'...\n")
    found = batch_scan_images(folder)

    if found:
        logname = f"graybar_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(logname, "w", encoding="utf-8") as f:
            for path, info in found:
                line = f"{path} — {info}"
                print("⚠️ ", line)
                f.write(line + "\n")
        print(f"\n🔍 Done. {len(found)} suspicious images found. Log: {logname}")
    else:
        print("\n✅ No corrupted images found.")
