# Gray Bar Scanner for Image Files

A CLI-based Python tool to automatically detect corrupted images, especially those with gray bars or areas caused by incomplete file transfers. It is optimized for large collections of images in deeply nested folder structures and checks each image for characteristic visual defects.

---

## 🔍 How It Works

The script analyzes images in horizontal strips (bands) and detects so-called "gray bars" that typically occur due to corrupted or truncated data. Suspicious images are written to a log file with their path and the position of the anomaly.

---

## ✅ Detection Logic

A band (e.g. 20 pixels high) is considered suspicious when:
- the brightness within the band **varies little** (standard deviation below a threshold)
- the average value is **in the mid brightness range** (neither black nor white)

---

## 📦 Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python greyscan.py /path/to/images
```

Example:

```bash
python greyscan.py ./photo_collection
```

---

## 📝 Output

- All suspicious files are logged in a text file with a timestamp, e.g.:

  ```
  graybar_log_20250708_131500.txt
  ```

- Format:

  ```
  /path/to/image.jpg — Gray bar at line 460–480
  ```

---

## ⚙️ Configurable Parameters

These parameters can be adjusted in the code:

| Parameter         | Meaning                                   | Default |
|------------------|-------------------------------------------|---------|
| `band_height`     | Height of the analyzed image bands        | `20`    |
| `flatness_thresh`| Max. brightness standard deviation        | `5`     |
| `brightness_min` | Minimum brightness for "gray"             | `30`    |
| `brightness_max` | Maximum brightness for "gray"             | `230`   |

---

## 📂 Supported File Formats

- `.jpg`
- `.jpeg`
- `.png`

---

## 🔧 Extension Ideas (optional)

- Parallelization (multithreading)
- YAML configuration for thresholds
- Thumbnails with error markings
- Duplicate comparison via hash
- Web interface (e.g. Flask based)
