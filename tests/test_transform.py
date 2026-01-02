"""
Tests for the functions in utils.transform_recorded.
"""

import os
import numpy as np
from utils.read_img import pathToCV2
from utils.transform_recorded import manual_perspective_transform

# Paths to files used for tests
actual_example_path = os.path.join("inputs", "actual_example1.png")
recorded_example_path = os.path.join("inputs", "recorded_example1.png")


def test_manual_transform_same_shape() -> None:
    """
    Recorded image can be transformed to match the shape of actual image

    Function tested should resize/crop correctly using the source points
    without throwing errors and produce an output array with the expected dimensions.
    """

    actual = pathToCV2(actual_example_path)
    recorded = pathToCV2(recorded_example_path)
    example_src_pts = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)
    recorded_transformed = manual_perspective_transform(
        actual, recorded, example_src_pts
    )

    assert (
        actual.shape == recorded_transformed.shape
    ), f"Shapes do not match. Actual: {actual.shape}, Transformed Recorded: {recorded_transformed.shape}"
