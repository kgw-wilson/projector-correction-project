"""Tests for utils.read_img.py"""

import os
import numpy as np
from utils.read_img import pathToCV2

# Paths to files used for tests
actual_example_path = os.path.join("inputs", "actual_example1.png")
recorded_example_path = os.path.join("inputs", "recorded_example1.png")


def test_can_open_example_files() -> None:
    """
    Test that example images can be read using `pathToCV2`

    Returned values should be NumPy arrays with the expected 3-channel shape.
    Checks that no errors are thrown during reading and conversion.
    """

    actual = pathToCV2(actual_example_path)
    recorded = pathToCV2(recorded_example_path)
    actual_np = np.array(actual)
    recorded_np = np.array(recorded)

    assert len(actual_np.shape) == 3, "Error: Actual image shape is not valid."
    assert len(recorded_np.shape) == 3, "Error: Recorded image shape is not valid."
