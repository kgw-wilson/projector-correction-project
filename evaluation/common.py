from pathlib import Path
import time
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import cv2
from utils.transform_recorded import ensure_clockwise
from utils.plt_corners import click_corners, check_corners

# Constants for all evaluation scripts
INPUT_DIR = "test_frames"
OUTPUT_DIR = Path("outputs")
NUM_FRAMES = 75

# Figure for use throughout recording
fig, ax = plt.subplots(facecolor=(0, 0, 0))
ax.axis("off")
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)


def show_centered(image: np.ndarray, title: str) -> None:
    ax.set_title(title)
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.01)


def get_video_capture() -> cv2.VideoCapture:
    """
    Initialize and return a video capture stream from a camera.

    Camera indices are system-dependent, but in this project:
    - Index 0 corresponds to the USB-attached webcam mounted on the projector.
    - Index 1 typically corresponds to the front-facing laptop camera.

    All evaluation scripts assume the webcam is used, so index 0 is
    hardcoded here. A short delay is required after initializing the
    VideoCapture object to establish the camera connection.
    """

    cap = cv2.VideoCapture(0)

    time.sleep(0.5)
    if not cap.isOpened():
        raise Exception("Error: could not open webcam")

    return cap


def get_first_test_frame_image(cap: cv2.VideoCapture) -> np.ndarray:
    """
    Record a test frame from the video stream

    If the user has connected their laptop by HDMI to the projector, at the time
    that an evaluation script is run their desktop with a terminal tab will be
    shown on the wall. This is the first recorded image.

    But then, the user clicks to reset the recorded image, switches windows
    to one of the test frame images, and then waits for 3 seconds. After that,
    the recorded image will contain the desired test frame. That image can be
    used to detect the bounds of the projected image on the wall before running
    the full experiment.
    """

    image = None

    # Managing windows and timing can be difficult, keep looping until the
    # desired image is recorded by the user
    while True:
        _, image = cap.read()
        show_centered(image, "Press any key to confirm, click to redo")
        key = plt.waitforbuttonpress()
        if key:
            break
        time.sleep(3)

    return image


def get_projected_image_bounds(
    image: np.ndarray, selected_points: Optional[np.ndarray]
) -> np.ndarray:
    """
    Get bounds of projected image within a recorded image

    Camera and projector are facing a wall, camera recorded image will include
    the wall and the projected image, this allows the user to click on the corners
    of the projected image to find its bounds or to supply those same slected points
    ahead of time if they are already known (this may be the case with repeated
    experiments where the camera hasn't moved and these points are recorded to
    expedite things).
    """

    if not selected_points:
        selected_points = click_corners(image)
        check_corners(image, selected_points)

    return ensure_clockwise(selected_points)
