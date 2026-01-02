import numpy as np
import cv2


def pathToCV2(path: str) -> np.ndarray:
    """
    Read an image from a file and return it as an RGB image.

    OpenCV reads images in BGR format by default. This function converts the
    image to RGB format for consistency with typical workflows.

    Parameters:
        path: str Path to the image file.

    Returns:
        rgb: Image in RGB format as a NumPy array.
    """

    bgr = cv2.imread(path)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb
