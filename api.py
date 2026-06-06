import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Store Intelligence API")

# Allow browser to call this API
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# ── Resolve paths relative to this file (not cwd) ─────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def data_path(filename: str) -> str:
    return os.path.join(BASE_DIR, filename)

def summary_filename(cam: int) -> str:
    """cam1 is stored as summary.json, others as summary_cam{N}.json"""
    return "summary.json" if cam == 1 else f"summary_cam{cam}.json"


# ── Load and merge all 5 camera summaries ─────────────
DATA = {
    "camera": "All Cameras",
    "total_events": 0,
    "footfall": 0,
    "zone_popularity": {},
    "avg_dwell_secs": {},
    "peak_time_sec": 0,
    "peak_count": 0,
    "anomalies": []
}

_dwell_accumulator = {}  # zone -> list of values, for averaging later

for cam in [1, 2, 3, 4, 5]:
    fname = data_path(summary_filename(cam))
    if not os.path.exists(fname):
        print(f"[WARN] {fname} not found — skipping")
        continue
    with open(fname) as f:
        cam_data = json.load(f)

    DATA["total_events"] += cam_data.get("total_events", 0)
    DATA["footfall"]     += cam_data.get("footfall", 0)

    # Keep peak_time_sec from the camera with the highest peak
    if cam_data.get("peak_count", 0) >= DATA["peak_count"]:
        DATA["peak_count"]    = cam_data.get("peak_count", 0)
        DATA["peak_time_sec"] = cam_data.get("peak_time_sec", 0)

    for zone, count in cam_data.get("zone_popularity", {}).items():
        DATA["zone_popularity"][zone] = DATA["zone_popularity"].get(zone, 0) + count

    for zone, secs in cam_data.get("avg_dwell_secs", {}).items():
        _dwell_accumulator.setdefault(zone, []).append(secs)

    DATA["anomalies"] += cam_data.get("anomalies", [])

# Average the dwell times across cameras
DATA["avg_dwell_secs"] = {
    zone: round(sum(vals) / len(vals), 1)
    for zone, vals in _dwell_accumulator.items()
}

print(f"[INFO] Loaded — footfall={DATA['footfall']}, "
      f"zones={list(DATA['zone_popularity'].keys())}, "
      f"anomalies={len(DATA['anomalies'])}")


# ── Load events (merge all cameras) ───────────────────
EVENTS = []
for cam in [1, 2, 3, 4, 5]:
    fname = data_path(f"events_cam{cam}.json")
    if os.path.exists(fname):
        with open(fname) as f:
            cam_events = json.load(f)
        for e in cam_events:
            e["camera"] = cam
        EVENTS.extend(cam_events)
    else:
        print(f"[WARN] {fname} not found — skipping")

try:
    EVENTS.sort(key=lambda e: e.get("time", e.get("frame", 0)))
except Exception:
    pass

print(f"[INFO] Total events across all cameras: {len(EVENTS)}")


# ── ENDPOINT 1: Home ──────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Store Intelligence API is running!",
        "cameras_loaded": sum(
            1 for cam in [1, 2, 3, 4, 5]
            if os.path.exists(data_path(summary_filename(cam)))
        ),
        "endpoints": ["/footfall", "/zones", "/dwell",
                      "/peak", "/anomalies", "/summary", "/events"]
    }


# ── ENDPOINT 2: Footfall ──────────────────────────────
@app.get("/footfall")
def get_footfall():
    """Total unique customers detected across all cameras"""
    return {
        "camera":   DATA["camera"],
        "footfall": DATA["footfall"],
        "message":  f"{DATA['footfall']} unique customers visited"
    }


# ── ENDPOINT 3: Zone popularity ───────────────────────
@app.get("/zones")
def get_zones():
    """Which zones had the most visitors"""
    zones = DATA["zone_popularity"]
    if not zones:
        return {"most_popular": None, "zones": []}
    sorted_zones = sorted(zones.items(), key=lambda x: -x[1])
    return {
        "most_popular": sorted_zones[0][0],
        "zones": [{"zone": z, "visitors": v} for z, v in sorted_zones]
    }


# ── ENDPOINT 4: Dwell time ────────────────────────────
@app.get("/dwell")
def get_dwell():
    """Average time customers spent in each zone"""
    dwell = DATA["avg_dwell_secs"]
    if not dwell:
        return {"longest_dwell_zone": None, "dwell_times": []}
    sorted_dwell = sorted(dwell.items(), key=lambda x: -x[1])
    return {
        "longest_dwell_zone": sorted_dwell[0][0],
        "dwell_times": [{"zone": z, "avg_seconds": s} for z, s in sorted_dwell]
    }


# ── ENDPOINT 5: Peak time ─────────────────────────────
@app.get("/peak")
def get_peak():
    """When was the store busiest"""
    return {
        "peak_time_sec": DATA["peak_time_sec"],
        "peak_count":    DATA["peak_count"],
        "message": f"Busiest at {DATA['peak_time_sec']}s with {DATA['peak_count']} people"
    }


# ── ENDPOINT 6: Anomalies ─────────────────────────────
@app.get("/anomalies")
def get_anomalies():
    """Unusual crowd spikes"""
    return {
        "total_anomalies": len(DATA["anomalies"]),
        "anomalies":       DATA["anomalies"]
    }


# ── ENDPOINT 7: Full summary ──────────────────────────
@app.get("/summary")
def get_summary():
    """Everything at once"""
    return DATA


# ── ENDPOINT 8: Recent events ─────────────────────────
@app.get("/events")
def get_events(limit: int = 20):
    """Last N events across all cameras (default 20)"""
    return {
        "total": len(EVENTS),
        "showing": limit,
        "events": EVENTS[-limit:]
    }
