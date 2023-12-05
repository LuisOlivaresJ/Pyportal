# Pyportal

Pyportal is a graphical user interface for performing [TG-307](https://doi.org/10.1002/mp.16536) quality assurance (QA) tools for routine QA of EPID systems.

## Features

* SQL database storage for constancy analysis.
* One-click fast test assessment.  

## Recommended tests to ensure the EPID will function accurately as a dosimeter.

* EPID positioning
* EPID positioning with gantry rotation
* Linearity with dose
* Uniformity
* Reproducibility (In progress...)

## Requirements

The program depends on the following:
* Python (3.10+)
* PySide6 (6.6+)
* Pylinac (3.16+)
* Pandas (2.1+)

## Installation

1. Download the source code from the repository.
2. (Optional but highly recommended) Create a virtual environment for Pyportal to avoid dependency conflicts
with existing python libraries.
3. Install all the required dependencies using `pip` (e.g `pip install pyside6`).

## Quick start

To run the application simply navigate to the source code directory and run the following command:\
`python GUI.py`

### EPID positioning

  Tolerance: Vendor specification or ≤2 mm

Determine the reproducibility of EPID positioning at gantry zero by three EPID deployments with a 10 cm × 10 cm field acquired after each deployment. Establish the center of each field in X and Y directions and measure the distance to the center of the panel for all three acquisitions to determine reproducibility.

## EPID positioning with gantry rotation

  Tolerance: Vendor specification or ≤2 mm

Repeat the 10 cm × 10 cm image at 45° gantry angle increments. Measure the center of each field in X and Y. Measure the difference relative to gantry zero position. Convert to mm using the known pixel dimension.

### Results

![Positioning](/docs/images/Positioning.PNG)

From the columns

* SID: Source to image distance
* G°: Gantry angle
* x (or y): Distance from beam center to the center of the panel in x (y) direction.
* dx (or dy): Difference in x (y) with respect the first loaded data in the dataset (first row in the table).

## Linearity with dose

  Tolerance: Vendor specification or within 2% (5% for MU < 5)
  
First determine that the Linac MU linearity is within TG-142 tolerance, then irradiate a 10 cm × 10 cm field with varying MU settings from 2 to 500. Measure the IPV at the center of each field. Determine the IPV per MU relative to 100 MU.

### Results

![Positioning](/docs/images/Linearity_results.png)

* MU: Monitor units used for irradiation.
* CU: Mean pixel value (ROI area of 10% respect to entire image, at the center.)
* Variation: Percentage difference with respect the image acquired using 100 MU.

## Uniformity

  Tolerance: Uniformity following panel calibration ±2% (SD as a percentage of the mean)
  
After flood-field calibration, irradiate the entire EPID sensitive area with 100 MU at the same SID. Measure the mean and SD of the pixel values within a large region that excludes the detector edges and penumbra (2 cm inside the panel edges and 0.5 cm inside field edges). Calculate the SD as a percentage of the mean.

### Results

![Positioning](/docs/images/Uniformity.png)

* Mean: Mean pixel over the image. %5 of each border is exluded.
* STD: Standar deviation.
* Uniformity: STD as a percentage of the mean.
* Num. pixels: Number of pixels in the ROI.

## Reproducibility (in progress...)

  Tolerance: Dosimetric reproducibility of ±2%
  
EPID reproducibility is important and needs to be stable over months and this should be confirmed over the first months following installation. The EPID response reproducibility at the center of the 10 cm × 10 cm field needs to be sampled weekly for at least 1 month period and be stable (adjusted for linac output). The frequency of EPID dose response recalibrations should be tracked over time to ensure EPID panel has consistent performance.
