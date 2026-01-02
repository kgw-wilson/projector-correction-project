import numpy as np


def color_correct(src: np.ndarray, target: np.ndarray) -> np.ndarray:
    """
    Color correct source image to match mean color channels of target

    Values are clipped to [0, 255], which may introduce artifacts.

    Parameters:
        src: numpy array for src image to be color corrected,
            assumes dtype == np.uint8
        target: numpy array for image with desited color means,
            assumes dtype == np.uint8

    Returns:
        corrected_src: color-corrected version of `src` with dtype np.uint8
    """
    src_float = src.astype(np.float32)
    tar_float = target.astype(np.float32)

    src_means = np.mean(src_float, axis=(0, 1))
    tar_means = np.mean(tar_float, axis=(0, 1))

    diff_arr = tar_means - src_means

    corrected_src = np.clip(src_float + diff_arr, 0, 255)

    return corrected_src.astype(np.uint8)
