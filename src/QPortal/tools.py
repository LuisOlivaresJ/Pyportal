# -*- coding: utf-8 -*-

"""This module is used for common operations with DICOM portal images."""

from pylinac import FieldAnalysis, Centering

def getXY(path):
    """Get the distance (mm) in x and y directions of the detector's center with respect to the beam's center.
    
    Parameters
    ----------

    path : str
        path to the file
    
    Returns
    -------

    tuple
        (Date created (str), SID (float), Gantry angle (float), distance in x (float), distance in y (float))

    """
    img = FieldAnalysis(path = path)
    img.analyze(centering = Centering.GEOMETRIC_CENTER)
    results = img.results_data()

    # Date created
    dateCreated = img.image.date_created(format="%Y-%m-%d")
    # Distance from radiation machine source to image plane (in mm) along radiation beam axis.
    sid = float(img.image.metadata['RTImageSID'].value)
    gantry_angle = float(img.image.metadata['GantryAngle'].value)

    distance_from_beam_center_to_panel_center_X = round(
        results.geometric_center_index_x_y[0]/img.image.dpmm - results.beam_center_index_x_y[0]/img.image.dpmm, 2)
    distance_from_beam_center_to_panel_center_Y = round(
        results.geometric_center_index_x_y[1]/img.image.dpmm - results.beam_center_index_x_y[1]/img.image.dpmm, 2)
    
    return (dateCreated,
            sid,
            gantry_angle,
            distance_from_beam_center_to_panel_center_X,
            distance_from_beam_center_to_panel_center_Y
            )

