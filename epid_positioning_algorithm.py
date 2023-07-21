from pylinac import FieldAnalysis, Centering
from datetime import date

#my_file = r"C:/Users/Luis/Documents/GitHub/Pyportal/Files/Positioning/13_07_2023/RI1.dcm"
my_file = r"C:/GitHub/Pyportal/Files/Positioning/13_07_2023/RI1.dcm"
my_img = FieldAnalysis(path = my_file)
my_img.analyze(centering = Centering.GEOMETRIC_CENTER)
results = my_img.results_data()

# Date
#   As string
print(my_img.image.date_created(format="%Y-%m-%d"))
#   As class datetime.date
print(type(date.fromisoformat(my_img.image.date_created(format="%Y-%m-%d"))))

distance_from_beam_center_to_panel_center_X = results.geometric_center_index_x_y[0]/my_img.image.dpmm - results.beam_center_index_x_y[0]/my_img.image.dpmm
distance_from_beam_center_to_panel_center_Y = results.geometric_center_index_x_y[1]/my_img.image.dpmm - results.beam_center_index_x_y[1]/my_img.image.dpmm

print("Distance from beam center to detector center.")
print(f"X: {distance_from_beam_center_to_panel_center_X:0.1f} mm, Y: {distance_from_beam_center_to_panel_center_Y:0.1f} mm")


# The Dots-per-mm of the image, defined at isocenter. E.g. if an EPID image is taken at 150cm SID, the dpmm will scale back to 100cm.
# my_img.image.dpmm

# Geometric center index
# results.geometric_center_index_x_y

# Beam center index
# results.beam_center_index_x_y