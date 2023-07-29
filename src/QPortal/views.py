# -*- coding: utf-8 -*-

"""This module provides views to manage
the positions table. Views (QTableView)
are responsible for displaying the data 
to the user.
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import(
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QDialog,
    QDialogButtonBox,
)

from pathlib import Path

from model import positionsModel, PandasModel
from tools import getXY
from database import get_reference_data

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent = None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("QPortal Positioning")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        self.positionsModel = positionsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.positionsModel.model)
        #self.table.set
        self.table.resizeColumnsToContents()
        # Create buttons
        self.addButton = QPushButton("Open...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteRow)
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.exportResults)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearAll)
        #Lay out the GUI

        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.exportButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)

        self.layout.addLayout(layout)
        self.layout.addWidget(self.table)


    def openAddDialog(self):
        "Load reference data."
        ref = get_reference_data()

        """Open an image dialog to ask for a directory."""
        dir = QFileDialog.getExistingDirectory(caption = "Open the folder with the images...", dir="/home")
        files = list(Path(dir).glob("RI*.dcm"))
     
        for file in files:

            xy = getXY(path = f"{file}")

            dif_x = round(xy["x"] - ref["x"], 2)
            dif_y = round(xy["y"] - ref["y"], 2)

            dif = {"dx": dif_x, "dy": dif_y}

            xy_results = {**xy, **dif}
            self.positionsModel.addPosition(xy_results)

        self.table.resizeColumnsToContents()
        self.show_last_results(len(files))


    def deleteRow(self):
        """Delete the selected row from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected rwo?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            self.positionsModel.deleteRow(row)

    def clearAll(self):
        """Remove all positions from the database."""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all data?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            self.positionsModel.clearAll()

    def exportResults(self):
        """Export database."""
        return
    
    def show_last_results(n):
        """Show n results. """
        df = get_reference_data().tail(n)
        ShowDialog(df)


class ShowDialog(QDialog):
    """Show results dialog."""
    def __init__(self, dataFrame, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Results")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.dataFrame = dataFrame

        self.setupUI()

    def setupUI(self):
        """Setup the Show dialog's GUI."""
        view = QTableView()
        view.resize(800, 500)
        view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(self.dataFrame)
        view.setModel(model)

        self.layout.addWidget(view)
        # Add standar buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonsBox.accepted.connect(self.acept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def acept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.nameField, self.jobField, self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}"
                )
                self.data = None #Reset .data
                return
            self.data.append(field.text())
        
        super().accept()