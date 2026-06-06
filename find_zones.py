import cv2

VIDEO = r"C:\Users\Ankitaa\store-intelligence\footage\CCTV Footage\CAM 1.mp4"

cap = cv2.VideoCapture(VIDEO)
ok, frame = cap.read()
cap.release()

h, w = frame.shape[:2]
print(f"Video size: {w} x {h} pixels")
print("Move mouse over the image to see coordinates.")
print("Note down the corners of each store section.")
print("Press Q to quit.")

def mouse_move(event, x, y, flags, param):
    display = frame.copy()
    # Show crosshair
    cv2.line(display, (x, 0), (x, h), (0,255,0), 1)
    cv2.line(display, (0, y), (w, y), (0,255,0), 1)
    # Show coordinates in big text
    cv2.putText(display, f"({x}, {y})", (x+10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.imshow("Find Zones - Move mouse. Press Q to quit.", display)

cv2.imshow("Find Zones - Move mouse. Press Q to quit.", frame)
cv2.setMouseCallback("Find Zones - Move mouse. Press Q to quit.", mouse_move)
cv2.waitKey(0)
cv2.destroyAllWindows()