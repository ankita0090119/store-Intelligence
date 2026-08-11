import json
from pathlib import Path

from pipeline.detector import get_detections
from pipeline.zone_mapper import get_zone


# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Input video
VIDEO = BASE_DIR / "data" / "videos" / "CAM 5.mp4"

# Output events file
OUTPUT = BASE_DIR / "data" / "events" / "events_cam5.json"


# Run detection and tracking
detections = get_detections(str(VIDEO))

events = []
last_zone = {}

for d in detections:
    tid = d["track_id"]
    zone = get_zone(d["center_x"], d["center_y"])

    if tid not in last_zone:
        etype = "person_entered"
    elif last_zone[tid] != zone:
        etype = "zone_changed"
    else:
        etype = "still_in_zone"

    last_zone[tid] = zone

    events.append({
        "type": etype,
        "time_sec": d["time_sec"],
        "person": tid,
        "zone": zone,
    })


# Save generated events
with open(OUTPUT, "w") as f:
    json.dump(events, f, indent=2)


print(f"\n✅ Done! {len(events)} events saved to {OUTPUT}")
print("First 3 events:")

for event in events[:3]:
    print(" ", event)