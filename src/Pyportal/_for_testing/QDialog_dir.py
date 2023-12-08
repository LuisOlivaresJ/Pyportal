import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog

from pylinac import FieldAnalysis, Centering


"""QDialog main function."""
# Create the application 
app = QApplication(sys.argv)

win = QWidget()

dir = QFileDialog.getExistingDirectory(caption = "Open Directory", dir="/home")
# dir is a class str
files = list(Path(dir).glob("RI*.dcm"))
for file in files:
    my_img = FieldAnalysis(path = f"{file}")
    #my_img.analyze(centering = Centering.GEOMETRIC_CENTER)
    #results = my_img.results_data()
    print(f"SID: {my_img.image.metadata['RTImageSID'].value}")

win.show()
# Run the event loop
sys.exit(app.exec())
