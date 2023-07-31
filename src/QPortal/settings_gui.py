from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QTableView, QDialog, QDialogButtonBox
from model import ToleranceModel
from PySide6.QtCore import Qt

class Settings_Gui(QDialog):
    """
    This class is used to set up a settings window.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(480, 200)

        self.setUpWindow()

    def setUpWindow(self):
        """"""

        self.main_layout = QVBoxLayout()

        tab_widget = QTabWidget()
        tab_widget.addTab(ToleranceTab(self), "Set tolerance")

        self.main_layout.addWidget(tab_widget)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.main_layout.addWidget(self.buttonsBox)
        self.setLayout(self.main_layout)
        
class ToleranceTab(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        view = QTableView()
        view.horizontalHeader().setStretchLastSection(True)

        tolerance_model = ToleranceModel()
        view.setModel(tolerance_model.model)

        layout = QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)
        