# Evaluation Scripts

## Overview 

Once the bounds of the projected image are known, the user can click to begin showing the test frames. Then, the corrections are applied, the corrected actual image is shown, and the camera records what it sees. The camera's output is transformed to match the shape of the actual image. The distance is measured between the actual image and the trasnformed recorded image from the camera.

## Baseline

No corrections were applied to the actual image being projected.

## Single Adjustment

For both the static correction and mean adjusted measures present in our results graph (see /results/results.png), one correction was calculated using the first frame and then was applied to every subsequent frame. In the case of static correction, this was the pixelwise difference between the actual and the transformed recorded for frame 1. In the case of mean adjustment (the final version shown in `single_adjustment.py`), this pixel-wise difference was averaged along axes (0, 1) to get an adjustment that applied the same color difference at every location to perform global color correction based on frame 1.

## Average Buffer / Median Buffer

A list of different sizes was used to record past corrections made. These corrections were stored in a buffer of various lengths (10, 5, 1) and we took the median or the average of the buffer to generate the correction applied to the current frame.

## Iterative

Instead of generating only one correction for each frame, we allowed the system to make multiple corrections for a single frame, where each correction was created using the pixel-wise difference between the actual image for that frame and the transformed image for that adjustment instance (and then smoothed using a Gaussian filter).Although this method beat every other method on the distance metric we created, it generated noticeable artifacts because of a bug in the code (see below).

## Not Shown

An average buffer was also tested using the code for the color corrected average buffer in `avg_buffer.py`. This was just using the difference directly instead of the channel-wise mean difference. Because results were not very good, (looking at the images in those output directories shows the remnants from previous frames) the file was taken over with slightly adjusted cc_avg_buffer code. A similar thing happeneed with median_buffer and cc_median_buffer.

## Past Bugs:

Iterative adjustments were made with a bug in the code, applying the same correction over and over again without recomputing the correction based on the current output for that iteration. 

Distances were measured from the actual image after corrections were applied rather than the base actual image from the test frames.

The code has been corrected for clarity, but results are reported using the older version.
