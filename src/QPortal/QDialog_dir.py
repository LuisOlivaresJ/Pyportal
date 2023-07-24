import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog


"""QDialog main function."""
# Create the application 
app = QApplication(sys.argv)

win = QWidget()

dir = QFileDialog.getExistingDirectory(caption = "Open Directory", dir="/home")
print(dir)

win.show()
# Run the event loop
sys.exit(app.exec())
