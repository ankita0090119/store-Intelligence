import cv2
from ultralytics import YOLO


model = YOLO("yolov8n.pt")


def get_detections(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Opened video. Frames: {total}, FPS: {fps:.1f}")

    all_detections = []
    frame_number = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        results = model.track(frame, persist=True, classes=[0], verbose=False)

        for box in results[0].boxes:
            if box.id is None:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            all_detections.append({
                "frame":    frame_number,
                "time_sec": round(frame_number / fps, 2),
                "track_id": int(box.id[0]),
                "center_x": cx,
                "center_y": cy,
                "confidence": round(float(box.conf[0]), 2),
            })

        if frame_number % 100 == 0:
            print(f"  Frame {frame_number}/{total}")

        frame_number += 1

    cap.release()
    print(f"Done! {len(all_detections)} detections found.")
    return all_detections
