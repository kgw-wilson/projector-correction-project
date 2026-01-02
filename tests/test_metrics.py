"""Tests for utils/metrics.py"""

import numpy as np
from utils.metrics import distance


def test_distance_white() -> None:
    """Distance between two identical white images should be 0"""

    white_img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    d = distance(white_img, white_img)
    assert d == 0


def test_distance_white_to_black() -> None:
    """
    Test distance between white image and black image

    Result should be 1, since they are maximally dissimilar.
    """

    white_img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    black_img = np.zeros_like(white_img)
    d = distance(white_img, black_img)
    assert d == 1


def test_distance_noise() -> None:
    """Test distance between two random noisy images

    Should fall within the expected range [0, 1].
    """

    random_array1 = np.random.randint(0, 256, size=(200, 220, 3), dtype=np.uint8)
    random_array2 = np.random.randint(0, 256, size=(200, 220, 3), dtype=np.uint8)
    d = distance(random_array1, random_array2)
    assert 0 <= d <= 1
