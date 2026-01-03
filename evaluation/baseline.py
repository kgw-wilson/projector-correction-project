"""
Baseline evaluation to get distance
metric for each frame between transformed
recorded and actual
"""

import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
from evaluation.common import (
    plt,
    show_centered,
    get_video_capture,
    get_first_test_frame_image,
    get_projected_image_bounds,
    INPUT_DIR,
    OUTPUT_DIR,
    NUM_FRAMES,
)
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform

cap = get_video_capture()

output_dir = OUTPUT_DIR / "baseline"

test_frame_recorded = get_first_test_frame_image(cap)

known_projector_image_bounds = np.array(
    [(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32
)

points_clockwise = get_projected_image_bounds(
    test_frame_recorded, known_projector_image_bounds
)

for num in range(1, NUM_FRAMES + 1):

    # Show the actual image without any corrections
    actual = cv2.imread(f"{INPUT_DIR}/frame_{num}.png")
    show_centered(actual, "Actual")

    # Wait for user to begin flow of subsequent frames
    if num == 1:
        print("Prep for correction")
        plt.waitforbuttonpress(0)

    # Wait for user to begin flow of subsequent frames
    if num == 1:
        print("Prep for correction")
        plt.waitforbuttonpress(0)

    # Wait so that the camera can see the currently shown corrected_actual image
    time.sleep(0.5)

    # Read from the camera and crop/transform read image to line up with actual
    _, rec = cap.read()
    trans_rec = manual_perspective_transform(actual, rec, points_clockwise)

    dist = distance(actual, trans_rec)
    print(f"Distance for {num}: {dist}")

    cv2.imwrite(f"{output_dir}/trans_rec_{num}.png", trans_rec)
