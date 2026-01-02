"""
Evaluation for the iterative process.
"""

import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
sys.path.append("..")
from utils.metrics import distance
from utils.transform_recorded import manual_perspective_transform, ensure_clockwise
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
OUTPUT_DIR = "../outputs/iterative"
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

kernel_size = 25
sigma = 5.0
kernel_x = cv2.getGaussianKernel(kernel_size, sigma)
kernel_y = cv2.getGaussianKernel(kernel_size, sigma)
kernel = np.outer(kernel_x, kernel_y)
kernel /= np.sum(kernel)

NUM_ADJUSTMENTS = 5

for num in range(1, NUM_FRAMES+1):
    actual = cv2.imread(f"{INPUT_DIR}/frame_{num}.png")
    correction = 0
    curr_actual = actual.astype(np.float32)
    for i in range(NUM_ADJUSTMENTS):
        curr_actual = np.clip((curr_actual + correction), 0, 255).astype(np.uint8)
        show_centered(curr_actual, "Actual")
        if num == 1 and i == 0:
            print("Prep for correction")
            plt.waitforbuttonpress(0)
        time.sleep(0.5)
        _, rec = cap.read()

        trans_rec = manual_perspective_transform(actual, rec, points_clockwise)
        if not isinstance(correction, np.ndarray):
            correction = np.clip(curr_actual - trans_rec.astype(np.float32), -2,2)
            filtered_corr = cv2.filter2D(correction, -1, kernel)

        dist = distance(curr_actual, trans_rec)
        print(f"Distance for {num, i}: {dist}")
        curr_actual = np.clip((curr_actual + filtered_corr), 0, 255)
    cv2.imwrite(f"{OUTPUT_DIR}/trans_rec_{num}.png", trans_rec)
