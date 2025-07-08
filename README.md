# Graubalken-Scanner für Bilddateien

Ein CLI-basiertes Python-Tool zum automatisierten Erkennen beschädigter Bilder, insbesondere solcher mit grauen Balken oder Flächen durch unvollständige Dateiübertragungen. Es ist für große Mengen an Bildern in tief verschachtelten Ordnerstrukturen optimiert und prüft jedes Bild auf charakteristische visuelle Defekte.

---

## 🔍 Funktionsweise

Das Skript analysiert Bilder in horizontalen Streifen (Bändern) und erkennt sogenannte „graue Balken“, die typischerweise durch beschädigte oder abgeschnittene Daten entstehen. Verdächtige Bilder werden mit Dateipfad und Position der Auffälligkeit in eine Log-Datei geschrieben.

---

## ✅ Erkennungslogik

Ein Band (z. B. 20 Pixel hoch) wird als verdächtig eingestuft, wenn:
- die Helligkeit innerhalb des Bandes **wenig variiert** (Standardabweichung unter Grenzwert)
- der Durchschnittswert **im mittleren Helligkeitsbereich** liegt (kein Schwarz, kein Weiß)

---

## 📦 Voraussetzungen

Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

---

## 🚀 Nutzung

```bash
python scan_images.py /pfad/zum/bilderordner
```

Beispiel:

```bash
python scan_images.py ./fotosammlung
```

---

## 📝 Ausgabe

- Alle verdächtigen Dateien werden in einer Textdatei mit Zeitstempel geloggt, z. B.:

  ```
  graubalken_log_20250708_131500.txt
  ```

- Format:

  ```
  /pfad/zum/bild.jpg — Grauer Balken bei Zeile 460–480
  ```

---

## ⚙️ Konfigurierbare Parameter

Diese Parameter sind im Code leicht anpassbar:

| Parameter         | Bedeutung                                | Standardwert |
|------------------|-------------------------------------------|--------------|
| `band_height`     | Höhe der analysierten Bildstreifen       | `20`         |
| `flatness_thresh`| Max. Helligkeits-Standardabweichung      | `5`          |
| `brightness_min` | Mindesthelligkeit für "grau"              | `30`         |
| `brightness_max` | Maximalhelligkeit für "grau"              | `230`        |

---

## 📂 Unterstützte Dateiformate

- `.jpg`
- `.jpeg`
- `.png`

---

## 🔧 Erweiterungsideen (optional)

- Parallelisierung (Multithreading)
- YAML-Konfiguration für Thresholds
- Thumbnails mit Fehler-Markierung
- Duplikatvergleich per Hash
- Web-Interface (z. B. Flask-basiert)
