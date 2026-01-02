# Evaluation

This directory contains the final scripts used to generate
the output for the project and to calculate the 
distance metrics for each of the various experiments.
In each case, the experiment involved projecting the actual image
(1 of the 75 images from the test_frames suite)
onto the wall, recording the result with a camera, and then 
transforming the recorded image to match the dimensions 
of the actual image. The distance metric was generated 
between the actual image and the transformed recorded image.

## Baseline

No corrections were applied to the actual image being projected.

## Single Adjustment

For both the "Static Correction" and "Mean adjusted" measures present
in our results graph (see /results/results.png), one correction was 
calculated using the first frame and then was applied to every subsequent
frame. In the case of static correction, this was the pixelwise difference
between the actual and the transformed recorded for frame 1. In the case
of mean adjustment, this pixel-wise difference was averaged along axes 
(0, 1) to get an adjustment that applied the same color difference at every
location to perform global color correction based on frame 1.

## Average Buffer / Median Buffer

A buffer of different sizes was used to record the corrections generated, 
according to the same process as in the single adjustment experiment, except
for every frame. These corrections were stored in a buffer of various lengths
(10, 5, 1) and we took the median or the average of the buffer to generate the
correction applied to the current frame.

## Iterative

Instead of generating only one correction for each frame, we allowed the 
system to make multiple corrections for a single frame, where each correction
was created using the pixel-wise difference between the actual for that 
frame and the transformed image for that adjustment instance 
(and then smoothed using a Gaussian filter).
Although this method beat every other method on the distance metric we created, 
it generated noticeable artifacts.
