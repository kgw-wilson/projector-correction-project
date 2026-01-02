"""
Evaluation to get distance
metric for each frame between transformed
recorded and actual when recording 
corrections in a buffer and applying
the average correction to the current frame.
"""

import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
sys.path.append("..")
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform, ensure_clockwise
from utils.color import color_correct
from utils.plt_corners import click_corners, check_corners

# Figure for use throughout recording
fig, ax = plt.subplots(facecolor=(0, 0, 0))
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

def show_centered(image, title):
    ax.set_title(title)
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.01)

# index 1 for front-facing laptop camera, index 0 for usb-attached webcam
cap = cv2.VideoCapture(0) 
time.sleep(0.5)
if not cap.isOpened():
    raise Exception("Error: Could not open webcam")

INPUT_DIR = "../test_frames"
OUTPUT_DIR = "../outputs/cc_avg_buffer_"
NUM_FRAMES = 75

# Keep looping until the desired image is recorded by the user
while True:
    ret, image = cap.read()
    show_centered(image, "Press any key to confirm, click to redo")
    key = plt.waitforbuttonpress()
    if key:
        # plt.close()
        break
    time.sleep(3) # Wait 3 seconds for user to readjust/change screen

# Variable for storing selected points, initialize to [] if points are needed
# find_points, selected_points = True, []
# old: find_points, selected_points = False, np.array([(468, 633), (460, 231), (1426, 230), (1417, 629)], dtype=np.float32) # OR []
find_points, selected_points = False, np.array([(471, 614), (462, 214), (1424, 214), (1415, 610)], dtype=np.float32) # OR []
if find_points:
    selected_points = click_corners(image)
    check_corners(image, selected_points)
points_clockwise = ensure_clockwise(selected_points)

for limit in [10,5,1]:
    curr_output_dir = f"{OUTPUT_DIR}{limit}" # like outputs/median_buffer_5
    print("\n------")
    print(f"Starting for limit: {limit}")
    corrections = []

    for num in range(1, NUM_FRAMES+1):
        actual = cv2.imread(f"{INPUT_DIR}/output_{num}.png")
        corrections_np = np.array(corrections, dtype=np.int32)
        print(f"Corrections shape at {num}: {corrections_np.shape}")
        if len(corrections) > 0:
            correction = np.mean(corrections_np, axis=0, dtype=np.float32)
        else:
            correction = 0
        corrected_actual = np.clip((actual.astype(np.float32) + correction), 0, 255).astype(np.uint8)
        show_centered(corrected_actual, "Actual")
        if num == 1:
            print("Prep for correction")
            plt.waitforbuttonpress(0)
        time.sleep(0.5)
        _, rec = cap.read()

        trans_rec = manual_perspective_transform(actual, rec, points_clockwise)
        
        curr_corr = actual.astype(np.int32) - trans_rec.astype(np.int32)
        channel_means = np.mean(curr_corr, axis=(0, 1))
        channel_means_expanded = np.expand_dims(channel_means, axis=(0, 1))
        curr_corr_cc = np.tile(channel_means_expanded, (curr_corr.shape[0], curr_corr.shape[1], 1))
        corrections.append(curr_corr_cc)
        if len(corrections) > limit:
            corrections.pop(0)
        dist = distance(corrected_actual, trans_rec)
        print(f"Distance for {num}: {dist}")
        cv2.imwrite(f"{curr_output_dir}/trans_rec_{num}.png", trans_rec)
