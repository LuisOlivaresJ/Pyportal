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
)

import os
from pylinac import FieldAnalysis, Centering
from model import positionsModel

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
        
        self.positionModel = positionsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.positionModel.model)
        #self.table.set
        self.table.resizeColumnsToContents()
        # Create buttons
        self.addButton = QPushButton("Add...")
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
        """Open the add image dialog."""
        file_name, _ = QFileDialog.getOpenFileName()
        #_ , extension = os.path.splitext(self.last_file_name)
        my_img = FieldAnalysis(path = file_name)
        my_img.analyze(centering = Centering.GEOMETRIC_CENTER)
        results = my_img.results_data()

        distance_from_beam_center_to_panel_center_X = results.geometric_center_index_x_y[0]/my_img.image.dpmm - results.beam_center_index_x_y[0]/my_img.image.dpmm
        distance_from_beam_center_to_panel_center_Y = results.geometric_center_index_x_y[1]/my_img.image.dpmm - results.beam_center_index_x_y[1]/my_img.image.dpmm
        positions = [distance_from_beam_center_to_panel_center_X, distance_from_beam_center_to_panel_center_Y]

        self.positionModel.addPosition(positions)
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
            QMessageBox.StandadButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            self.positionModel.deleteRow(row)

    def clearAll(self):
        """Remove all positions from the database."""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all data?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            self.positionModel.clearAll()

    def exportResults(self):
        """Export database."""
        return