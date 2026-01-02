from typing import Optional
import numpy as np
import cv2
from skimage.filters import threshold_otsu


def manual_perspective_transform(
    actual_img: np.ndarray,
    recorded_img: np.ndarray,
    src_points: np.ndarray,
) -> np.ndarray:
    """
    Crop region in recorded_img specified by src_points and warp to match dimensions of actual_img

    Parameters:
        actual_img: numpy array for the actual image (from source video)
        recorded_img: numpy array for the recorded image (from camera)
        src_pts: numpy array for desired region of recorded image, like:
            np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)

    Returns:
        warped_recorded: numpy array for cropped and resized recorded patch
    """

    # Define four destination points (coordinates of the desired output rectangle)
    target_width, target_height = actual_img.shape[1], actual_img.shape[0]
    dst_points = np.array(
        [[0, 0], [target_width, 0], [target_width, target_height], [0, target_height]],
        dtype=np.float32,
    )

    # Define perspective transform matrix
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply perspective transformation
    warped_recorded = cv2.warpPerspective(
        recorded_img, M, (target_width, target_height)
    )

    return warped_recorded


def contour_perspective_transform(
    actual_img: np.ndarray,
    recorded_img: np.ndarray,
    manual_threshold: Optional[tuple[int, int]] = None,
) -> np.ndarray:
    """
    Transform recorded_img to shape of actual_img using OpenCV's contour detection

    Uses OpenCV's contour detection to find the contour with the largest area
    in the recorded image. That area is assumed to be the image projected by the
    projector, which it should always be if the lighting is right and the camera
    is pointing at the projected image. The area is cropped and resized, then returned.

    This approach was found to be the best in notebooks/transform.ipynb.

    Parameters:
        actual_img: cv2 image for actual image (from source video)
        recorded_img: cv2 image for recorded image (from camera)
        manual_threshold: tuple/arr of (low, high) representing manual threshold
            override if threshold_otsu doesn't work

    Returns:
        transformed_img: cv2 image for projector image cropped out of recorded_img
            and resized to shape of actual_img
    """

    # Find edge map using Canny edge detection on slightly blurred gray image
    # calculating threshold values based on median
    gray_image = cv2.cvtColor(recorded_img, cv2.COLOR_RGB2GRAY)
    blurred_gray = cv2.GaussianBlur(gray_image, (5, 5), 0)
    if not manual_threshold:
        threshold = threshold_otsu(blurred_gray)
        edges = cv2.Canny(blurred_gray, threshold * 0.4, threshold)
    else:
        edges = cv2.Canny(blurred_gray, manual_threshold[0], manual_threshold[1])

    # Apply dilation to close gaps in between object edges
    kernel_dilation = np.ones((11, 11), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel_dilation, iterations=1)

    # Apply erosion to reduce noise and fine-tune object boundaries
    kernel_erosion = np.ones((7, 7), np.uint8)
    eroded_image = cv2.erode(dilated_edges, kernel_erosion, iterations=1)

    # Find largest contour by area (should be screen)
    contours_edge, _ = cv2.findContours(
        eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    largest_contour_edge = sorted(contours_edge, key=cv2.contourArea, reverse=True)[0]

    # Apply Douglas-Peucker algorithm to simplify the contour into a quadrilateral
    epsilon = 0.02 * cv2.arcLength(largest_contour_edge, True)
    approx_contour = cv2.approxPolyDP(largest_contour_edge, epsilon, True)
    if approx_contour.shape != (4, 1, 2):
        raise Exception("Function failed to find largest contour")
    found_contour = np.reshape(approx_contour, (4, 2)).astype(np.float32)

    # Check and make sure contour runs in clockwise direction
    found_contour = ensure_clockwise(found_contour)

    # Use the found contour (corner points) to shift the image
    return manual_perspective_transform(actual_img, recorded_img, found_contour)


def ensure_clockwise(contour: np.ndarray) -> np.ndarray:
    """
    Ensures a quadrilateral contour is ordered clockwise, top-left point first

    Parameters:
        contour: numpy array for a contour of shape (4,2)

    Returns:
        clockwise_contour: numpy array for clockwise version of
            input contour
    """

    # Find top-left index
    top_left_idx = np.argmin(np.sum(contour, axis=1))

    # Determine direction based on next point
    next_idx = (top_left_idx + 1) % 4
    direction = 1 if contour[next_idx][0] > contour[top_left_idx][0] else -1

    output = np.zeros_like(contour)
    for i in range(4):
        pt_idx = (top_left_idx + direction * i) % 4
        output[i] = contour[pt_idx]

    return output
