import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm


def is_gray_band(band, flatness_thresh=5, brightness_min=30, brightness_max=230):
    gray_stddev = np.std(band)
    gray_mean = np.mean(band)
    return gray_stddev < flatness_thresh and brightness_min < gray_mean < brightness_max


def scan_image_for_gray_bands(image_path, band_height=20, flatness_thresh=5, brightness_min=30, brightness_max=230):
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return False, "Not readable or not an image"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height = gray.shape[0]

        for y in range(0, height, band_height):
            band = gray[y:y + band_height, :]
            if band.shape[0] < band_height:
                continue
            if is_gray_band(band, flatness_thresh, brightness_min, brightness_max):
                return True, f"Gray bar at line {y}-{y + band_height}"
        return False, None

    except Exception as e:
        return True, f"Error while processing: {str(e)}"


def batch_scan_images(
    root_path,
    extensions=(".jpg", ".jpeg", ".png"),
    band_height=20,
    flatness_thresh=5,
    brightness_min=30,
    brightness_max=230,
    verbose=False,
):
    root = Path(root_path)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {root_path}")

    all_images = list(root.rglob("*"))
    image_files = [p for p in all_images if p.suffix.lower() in extensions]

    if not image_files:
        if verbose:
            print("No images found in the provided path.")
        return []

    results = []

    for image_path in tqdm(image_files, desc="Checking images"):
        corrupted, reason = scan_image_for_gray_bands(
            image_path,
            band_height=band_height,
            flatness_thresh=flatness_thresh,
            brightness_min=brightness_min,
            brightness_max=brightness_max,
        )
        if corrupted:
            results.append((image_path, reason))

    return results
