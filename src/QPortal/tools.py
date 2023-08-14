# -*- coding: utf-8 -*-

"""This module is used for common operations with DICOM portal images."""

from pylinac import FieldAnalysis, Centering
import pydicom
from pylinac.core import image
from pylinac.core.exceptions import NotAnalyzed

from skimage.draw import rectangle
from skimage import measure

import numpy as np

def getXY(path):
    """Get the distance (mm) in x and y directions of the detector's center with respect to the beam's center.
    
    Parameters
    ----------

    path : str
        path to the file
    
    Returns
    -------

    dictionary
        {Date, SID, Gantry, x, y}

    """
    img = FieldAnalysis(path = path)
    img.analyze(centering = Centering.GEOMETRIC_CENTER)
    results = img.results_data()

    # Date created
    #dateCreated = img.image.date_created(format="%Y-%m-%d")
    dateCreated = img.image.date_created(format="%Y-%m-%d")
    # Distance from radiation machine source to image plane (in mm) along radiation beam axis.
    sid = float(img.image.metadata['RTImageSID'].value)
    gantry_angle = float(img.image.metadata['GantryAngle'].value)

    distance_from_beam_center_to_panel_center_X = round(
        results.geometric_center_index_x_y[0]/img.image.dpmm - results.beam_center_index_x_y[0]/img.image.dpmm, 2)
    distance_from_beam_center_to_panel_center_Y = round(
        results.geometric_center_index_x_y[1]/img.image.dpmm - results.beam_center_index_x_y[1]/img.image.dpmm, 2)
    
    return {"Date": dateCreated,
            "SID": sid,
            "Gantry": gantry_angle,
            "x": distance_from_beam_center_to_panel_center_X,
            "y": distance_from_beam_center_to_panel_center_Y
    }

def getMU(path):

    ds = pydicom.dcmread(path)
    um = float(ds.ExposureSequence[0].MetersetExposure)
    return um

def getCUperMU(path):
    """Function to get calibration Units and other parameters."""

    img = FieldAnalysis(path)
    dateCreated = img.image.date_created(format="%Y-%m-%d")
    img.analyze(vert_width = 0.1, horiz_width = 0.1)
    mean_cu = round(img.central_roi.mean, 3)
    mu = getMU(path)
    cu_mu = round(mean_cu/mu, 3)
    
    #CUperUM = CU/um
    return {"Date": dateCreated,
            "MU": mu,
            "CU": mean_cu,
            "CU/MU": cu_mu,
    }

class UniformityAnalysis:
    """Class for analyzing uniformity of a radiaton image where full detector were irradiated."""

    def __init__(self, path):
        """

        Parameters
        ----------
        path
            The path to the image.
            
        """
        self._path: str = path
        self.image: image.ImageLike = image.load(path)
        self._is_analyzed = False

    def _get_vert_idx(
        self, vert_position: float, vert_width: float
        ) -> (float, float):
        left_edge = int(
        round(
            self.image.array.shape[1] * vert_position
            - self.image.array.shape[1] * vert_width / 2
            )
        )
        left_edge = max(left_edge, 0)  # clip to 0
        right_edge = int(
            round(
                self.image.array.shape[1] * vert_position
                + self.image.array.shape[1] * vert_width / 2
            )
            + 1
        )
        right_edge = min(right_edge, self.image.array.shape[1])  # clip to image limit
        return (
            left_edge,
            right_edge,
        )

    def _get_horiz_idx(
        self, horiz_position: float, horiz_width: float
        ) -> (float, float):
        
        bottom_edge = int(
            round(
                self.image.array.shape[0] * horiz_position
                - self.image.array.shape[0] * horiz_width / 2
            )
        )
        bottom_edge = max(bottom_edge, 0)
        top_edge = int(
            round(
                self.image.array.shape[0] * horiz_position
                + self.image.array.shape[0] * horiz_width / 2
            )
            + 1
        )
        top_edge = min(top_edge, self.image.array.shape[0])
        return (
            bottom_edge,
            top_edge,
        )
    
    def get_uniformity(
        self, 
        horiz_position = 0.5,
        horiz_width = 0.85,
        vert_position = 0.5,
        vert_width = 0.85):
        """Calculate the central ROI uniformity.
        
        Parameters
        ----------

        vert_position
            The distance ratio of the image to sample. E.g. at the default of 0.5 the ROI is extracted
            in the middle of the image. 0.0 is at the left edge of the image and 1.0 is at the right edge of the image.

        horiz_position
            The distance ratio of the image to sample. E.g. at the default of 0.5 the ROI is extracted
            in the middle of the image. 0.0 is at the top edge of the image and 1.0 is at the bottom edge of the image.

        vert_width
            The width ratio of the image to sample. E.g. at the default of 0.0 a 1 pixel wide ROI is extracted.
            0.0 would be 1 pixel wide and 1.0 would be the vertical image width.

        horiz_width
            The width ratio of the image to sample. E.g. at the default of 0.0 a 1 pixel wide ROI is extracted.
            0.0 would be 1 pixel wide and 1.0 would be the horizontal image width.

        
        """
        
        left_v_idx, right_v_idx = self._get_vert_idx(vert_position, vert_width)
        upper_h_idx, lower_h_idx = self._get_horiz_idx(horiz_position, horiz_width)
        
        width =  max(abs(left_v_idx - right_v_idx), 2)
        height = max(abs(upper_h_idx - lower_h_idx), 2)

        label_rectangle = np.zeros(self.image.shape, dtype = np.uint8)
        start = (left_v_idx, upper_h_idx)
        end = (left_v_idx + height, upper_h_idx + width)
        rr, cc = rectangle(start, end = end, shape = label_rectangle.shape)
        label_rectangle[rr, cc] = 1

        def stdev(region, intensities):
            # note the ddof arg to get the sample var if you so desire!
            return np.std(intensities[region], ddof=1)

        props = measure.regionprops(label_rectangle, intensity_image = self.image.array, extra_properties=[stdev])
        print(props[0].intensity_mean)
                
        self.mean = props[0].intensity_mean
        self.std = props[0].stdev
        self.num_pixels = props[0].num_pixels

        self.uniformity = self.std / self.mean * 100
        self._is_analyzed = True
        return self.uniformity

    def results(self, as_str=True) -> str:
        """Get the results of the analysis.

        Parameters
        ----------
        as_str
            If True, return a simple string. If False, return a list of each line of text.
        """
        if not self._is_analyzed:
            raise NotAnalyzed("Image is not analyzed yet. Use get_uniformity() first.")

        results = [
            "Uniformity Analysis Results",
            "---------------------------",
            f"File: {self._path}",
        ]
        results += [
                "Central ROI stats:",
                f"Mean: {self.mean}",
                f"Standard deviation: {self.std}",
                f"Uniformity [%]: {self.uniformity}",
                f"Num. pixels: {self.num_pixels}",
            ]
        return results