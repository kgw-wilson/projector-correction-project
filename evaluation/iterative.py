"""
Evaluation for the iterative correction process (making a set number
of adaptive adjustments for every frame).
"""

import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
from evaluation.common import (
    plt,
    NUM_FRAMES,
    show_centered,
    get_video_capture,
    get_first_test_frame_image,
    get_projected_image_bounds,
    INPUT_DIR,
    OUTPUT_DIR,
)
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform

cap = get_video_capture()

INPUT_DIR = "../test_frames"

output_dir = OUTPUT_DIR / "iterative"

test_frame_recorded = get_first_test_frame_image(cap)

known_projector_image_bounds = np.array(
    [(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32
)

points_clockwise = get_projected_image_bounds(
    test_frame_recorded, known_projector_image_bounds
)


# Define a kernel for use in blurring the correction
# to hopefully help reduce artifacts and make gradual
# adjustments over a small area
kernel_size = 25
sigma = 5.0
kernel_x = cv2.getGaussianKernel(kernel_size, sigma)
kernel_y = cv2.getGaussianKernel(kernel_size, sigma)
kernel = np.outer(kernel_x, kernel_y)
kernel /= np.sum(kernel)

NUM_ADJUSTMENTS = 5

for num in range(1, NUM_FRAMES + 1):

    base_actual = cv2.imread(f"{INPUT_DIR}/frame_{num}.png")
    curr_actual = base_actual.astype(np.float32)
    correction = np.zeros_like(base_actual)

    for i in range(NUM_ADJUSTMENTS):

        # Show the actual image for the frame with any corrections applied
        curr_actual = np.clip((curr_actual + correction), 0, 255)
        show_centered(curr_actual.astype(np.uint8), "Actual")

        # Wait for user to begin flow of subsequent frames
        if num == 1 and i == 0:
            print("Prep for correction")
            plt.waitforbuttonpress(0)

        # Wait so that the camera can see the currently shown corrected_actual image
        time.sleep(0.5)

        # Read from the camera and crop/transform read image to line up with actual
        _, rec = cap.read()
        trans_rec = manual_perspective_transform(base_actual, rec, points_clockwise)

        # Calculate the error between what is projected (curr_actual) and
        # what is read by the camera (trans_rec). Limit corrections to 2 pixel
        # values in either direction to prevent oscillations and artifacts.
        error = curr_actual - trans_rec.astype(np.float32)
        filtered_error = cv2.filter2D(error, -1, kernel)
        filtered_error = np.clip(filtered_error, -2, 2)
        correction += error + filtered_error

        dist = distance(base_actual, trans_rec)
        print(f"Distance for {num, i}: {dist}")

    cv2.imwrite(f"{output_dir}/trans_rec_{num}.png", trans_rec)
