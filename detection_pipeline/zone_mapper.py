# Zone coordinates for CAM 1 (1920x1080)
# Based on actual store layout visible in footage

ZONES = {
    # Left section — Korean skincare (FarmStay, COSRX, Klairs)
    "korean_skincare": [0, 400, 400, 1080],

    # Middle-left — The Face Shop / Clean Beauty
    "face_shop":       [400, 400, 750, 1080],

    # Middle-right — Good Vibes / DE-TAN
    "good_vibes":      [750, 400, 1100, 1080],

    # Right — Dermaco, Minimalist, Aqualogica
    "premium_brands":  [1100, 400, 1920, 1080],

    # Top shelf area (products on upper shelves — no customers)
    "shelves_top":     [0, 0, 1920, 400],
}


def get_zone(cx, cy):
    """Return which zone a person is standing in."""
    for name, (x1, y1, x2, y2) in ZONES.items():
        if x1 <= cx <= x2 and y1 <= cy <= y2:
            return name
    return "unknown"