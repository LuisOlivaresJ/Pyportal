# -*- coding: utf-8 -*-

"""This module provides views to manage
the positions table. Views (QTableView)
are responsible for displaying the data 
to the user.
"""

from PySide6.QtWidgets import(
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from pylinac import FieldAnalysis

from pathlib import Path

from model import positionsModel
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