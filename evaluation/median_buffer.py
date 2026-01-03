"""
Apply the median color correction from a trailing
list of mean color corrections required for the previous
n frames, with n in {10, 5, 1}.
"""

import cv2
import time
import numpy as np
from evaluation.common import (
    plt,
    get_video_capture,
    show_centered,
    INPUT_DIR,
    OUTPUT_DIR,
    NUM_FRAMES,
    get_first_test_frame_image,
    get_projected_image_bounds,
)
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform


output_dir = OUTPUT_DIR / "/cc_median_buffer_"

cap = get_video_capture()

test_frame_recorded = get_first_test_frame_image(cap)

known_projector_image_bounds = np.array(
    [(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32
)

points_clockwise = get_projected_image_bounds(
    test_frame_recorded, known_projector_image_bounds
)

# Try 3 different values for the number of trailing frames
# to consider when correcting the current frame
for limit in [10, 5, 1]:

    curr_output_dir = f"{output_dir}{limit}"

    print(f"\n------\nStarting for limit: {limit}")

    corrections = []

    for num in range(1, NUM_FRAMES + 1):

        # Show the actual image for the frame with any corrections applied
        actual = cv2.imread(f"{INPUT_DIR}/frame_{num}.png")
        corrections_np = np.array(corrections, dtype=np.int32)
        if len(corrections) > 0:
            correction = np.median(corrections_np, axis=0).astype(np.float32)
        else:
            correction = 0
        corrected_actual = np.clip(
            (actual.astype(np.float32) + correction), 0, 255
        ).astype(np.uint8)
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

        # Record the current correction needed to get from the recorded image
        # to the actual image
        curr_corr = actual.astype(np.int32) - trans_rec.astype(np.int32)
        channel_means = np.mean(curr_corr, axis=(0, 1))
        channel_means_expanded = np.expand_dims(channel_means, axis=(0, 1))
        curr_corr_cc = np.tile(
            channel_means_expanded, (curr_corr.shape[0], curr_corr.shape[1], 1)
        )
        corrections.append(curr_corr_cc)

        # Keep the list of corrections at or below the limit for the experiment
        if len(corrections) > limit:
            corrections.pop(0)

        dist = distance(actual, trans_rec)
        print(f"Distance for {num}: {dist}")

        cv2.imwrite(f"{curr_output_dir}/trans_rec_{num}.png", trans_rec)
