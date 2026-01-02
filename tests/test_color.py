"""Tests for utils/colors.py"""

import numpy as np
import cv2
from utils.color import color_correct


def test_color_correct_white_to_black() -> None:
    """
    Test that a completely white image is color-corrected to a
    completely black image. After correction, all pixel values
    should be 0.
    """

    # Create white images (255 values all channels)
    white_img = np.ones((200, 200, 3), dtype=np.uint8) * 255

    # Create black image (0 values all channels)
    black_img = np.zeros_like(white_img)

    # Resulting image should have its mean values aligned
    # with the blak image, so all pixels should be black
    result = color_correct(white_img, black_img)
    assert np.all(result == 0)


def test_color_correct_general() -> None:
    """
    Test a general color correction scenario:

    The input image has:
      - Green pixels in top-left and bottom-right
      - Blue pixels in top-right and bottom-left

    The target image is all green. After correction:
      - Green pixels remain unchanged
      - Blue pixels shift towards green (become cyan)

    Checks approximate equality since pixel rounding may occur.
    """

    img = np.array(
        [[[0, 255, 0], [0, 0, 255]], [[0, 0, 255], [0, 255, 0]]], dtype=np.uint8
    )
    green = np.array(
        [[[0, 255, 0], [0, 255, 0]], [[0, 255, 0], [0, 255, 0]]], dtype=np.uint8
    )
    expected_result = np.array(
        [[[0, 255, 0], [0, 127, 127]], [[0, 127, 127], [0, 255, 0]]], dtype=np.uint8
    )

    result = color_correct(img, green)
    assert np.allclose(result, expected_result, atol=1)
