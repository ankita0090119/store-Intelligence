import json
from pipeline.detector    import get_detections
from pipeline.zone_mapper import get_zone

# Your CAM 1 video path — already filled in for you!
VIDEO = r"C:\Users\Ankitaa\store-intelligence\footage\CCTV Footage\CAM 5.mp4"

detections = get_detections(VIDEO)

events = []
last_zone = {}

for d in detections:
    tid  = d["track_id"]
    zone = get_zone(d["center_x"], d["center_y"])

    if tid not in last_zone:
        etype = "person_entered"
    elif last_zone[tid] != zone:
        etype = "zone_changed"
    else:
        etype = "still_in_zone"

    last_zone[tid] = zone
    events.append({
        "type":     etype,
        "time_sec": d["time_sec"],
        "person":   tid,
        "zone":     zone,
    })

with open("events.json", "w") as f:
    json.dump(events, f, indent=2)

print(f"\n✅ Done! {len(events)} events saved to events.json")
print("First 3 events:")
for e in events[:3]:
    print(" ", e)