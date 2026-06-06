# Store Intelligence System
### Purplle Tech Challenge 2026 — Round 2

A real-time store analytics system that uses computer vision to track customer behavior across 5 CCTV cameras.

---

## What It Does

- Detects and tracks customers using **YOLOv8 + ByteTrack**
- Maps customers to store zones in real time
- Computes footfall, dwell time, zone popularity, peak hours, and anomalies
- Exposes all data via a **FastAPI REST API**
- Visualizes everything on a live **dashboard**

---

## Project Structure

```
store-intelligence/
├── main.py              # Run YOLOv8 + ByteTrack on a camera feed
├── pipeline/
│   ├── detector.py      # YOLOv8 person detection
│   └── zone_mapper.py   # Maps bounding boxes to store zones
├── analytics.py         # Computes summary stats from events
├── api.py               # FastAPI server with 8 endpoints
├── dashboard.html       # Live multi-camera dashboard
├── events_cam1-5.json   # Raw detection events per camera
├── summary.json         # CAM 1 summary
└── summary_cam2-5.json  # CAM 2–5 summaries
```

---


## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /footfall` | Total unique customers |
| `GET /zones` | Zone popularity ranking |
| `GET /dwell` | Average dwell time per zone |
| `GET /peak` | Peak hour analysis |
| `GET /anomalies` | Crowd spike detection |
| `GET /summary` | Full analytics summary |
| `GET /events` | Recent detection events |

---

## Results (5 Cameras Combined)

- **Total Footfall:** 418 unique customers
- **Total Events:** 61,202 detections
- **Most Popular Zone:** good_vibes (187 visitors)
- **Longest Dwell Zone:** face_shop (4.4s avg)
- **Peak Time:** 70s with 21 people simultaneously

---

## Tech Stack

- Python 3.x
- YOLOv8 (Ultralytics)
- ByteTrack
- FastAPI
- HTML/CSS/JS Dashboard
