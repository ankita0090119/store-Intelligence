import json
from collections import defaultdict
import sys

# Change this number for each camera: 1, 2, 3, 4, 5
CAM_NUMBER = 3

filename = f"events_cam{CAM_NUMBER}.json"

try:
    with open(filename) as f:
        events = json.load(f)
except FileNotFoundError:
    print(f"ERROR: {filename} not found! Did you run main.py for this camera?")
    sys.exit(1)

print(f"Loaded {len(events)} events from {filename}")

footfall = len(set(e["person"] for e in events))
print(f"👥 FOOTFALL: {footfall} unique customers")

zone_entry_time = {}
zone_dwell = defaultdict(list)
for e in events:
    pid, zone, t = e["person"], e["zone"], e["time_sec"]
    if pid not in zone_entry_time:
        zone_entry_time[pid] = (zone, t)
    else:
        last_zone, entry_t = zone_entry_time[pid]
        if last_zone != zone:
            dwell = round(t - entry_t, 2)
            if dwell > 0:
                zone_dwell[last_zone].append(dwell)
            zone_entry_time[pid] = (zone, t)

print("⏱️  DWELL TIME:")
for zone, times in sorted(zone_dwell.items()):
    print(f"   {zone:<20} avg={round(sum(times)/len(times),1)}s")

zone_visits = defaultdict(set)
for e in events:
    zone_visits[e["zone"]].add(e["person"])

print("🔥 ZONE POPULARITY:")
for zone, v in sorted(zone_visits.items(), key=lambda x: -len(x[1])):
    print(f"   {zone:<20} {len(v)} visitors")

time_buckets = defaultdict(set)
for e in events:
    bucket = int(e["time_sec"] // 10) * 10
    time_buckets[bucket].add(e["person"])
peak_bucket = max(time_buckets, key=lambda b: len(time_buckets[b]))
peak_count  = len(time_buckets[peak_bucket])
print(f"🕐 PEAK: {peak_bucket}s–{peak_bucket+10}s | {peak_count} people")

counts    = [len(v) for v in time_buckets.values()]
avg_count = sum(counts) / len(counts)
anomalies = [
    {"time_sec": b, "count": len(v)}
    for b, v in time_buckets.items()
    if len(v) > avg_count * 2
]
print(f"⚠️  ANOMALIES: {len(anomalies)} spikes")

summary = {
    "camera":          f"CAM {CAM_NUMBER}",
    "total_events":    len(events),
    "footfall":        footfall,
    "zone_popularity": {z: len(v) for z, v in zone_visits.items()},
    "avg_dwell_secs":  {z: round(sum(t)/len(t),1) for z, t in zone_dwell.items()},
    "peak_time_sec":   peak_bucket,
    "peak_count":      peak_count,
    "anomalies":       anomalies,
}

out = f"summary_cam{CAM_NUMBER}.json"
with open(out, "w") as f:
    json.dump(summary, f, indent=2)

print(f"✅ {out} saved!")