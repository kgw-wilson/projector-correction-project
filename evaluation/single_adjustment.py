"""
In this experiment, the correction applied is the same for every
frame after the first frame.
"""

import time
import numpy as np
import cv2
from evaluation.common import (
    plt,
    show_centered,
    INPUT_DIR,
    OUTPUT_DIR,
    NUM_FRAMES,
    get_video_capture,
    get_first_test_frame_image,
    get_projected_image_bounds,
)
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform

experiment_output_dir = OUTPUT_DIR / "mean_adjusted"


cap = get_video_capture()
test_frame_recorded = get_first_test_frame_image(cap)

known_projector_image_bounds = np.array(
    [(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32
)

points_clockwise = get_projected_image_bounds(
    test_frame_recorded, known_projector_image_bounds
)

correction = 0

for num in range(1, NUM_FRAMES + 1):

    # Show the actual image for the frame with any corrections applied
    actual = cv2.imread(f"{INPUT_DIR}/frame_{num}.png")
    corrected_actual = np.clip((actual.astype(np.float32) + correction), 0, 255).astype(
        np.uint8
    )
    show_centered(corrected_actual, "Actual")

    # Wait for user to begin flow of subsequent frames
    if num == 1:
        print("Prep for correction")
        plt.waitforbuttonpress(0)

    # Wait so that the camera can see the currently shown corrected_actual image
    time.sleep(0.5)

    # Read from the camera and crop/transform read image to line up with actual
    _, rec = cap.read()
    trans_rec = manual_perspective_transform(actual, rec, points_clockwise)

    # For the first frame, apply static mean-based correction and use that
    # correction for all subsequent frames
    if not isinstance(correction, np.ndarray):
        correction = np.mean(actual, axis=(0, 1)) - np.mean(trans_rec, axis=(0, 1))

    dist = distance(actual, trans_rec)
    print(f"Distance for {num}: {dist}")

    cv2.imwrite(str(experiment_output_dir / "trans_rec_{num}.png"), trans_rec)
