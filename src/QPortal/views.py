# -*- coding: utf-8 -*-

"""This module provides views to manage
the positions table. Views (QTableView)
are responsible for displaying the data 
to the user.
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT

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
from pylinac import FieldAnalysis, Centering
from model import positionsModel

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent = None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("QPortal Positioning")
        self.resize(950, 350)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.hlayout = QHBoxLayout()
        self.centralWidget.setLayout(self.hlayout)
        
        self.positionsModel = positionsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        
        # Create widgets
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
        # Create canvas plot view
        self.view_canvas = FigureCanvas(Figure(figsize=(5,3)))
        self.axes = self.view_canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view_canvas, self)

        
        #Lay out the GUI

        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.exportButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.view_canvas)

        self.hlayout.addLayout(layout)
        self.hlayout.addWidget(self.table)
        self.hlayout.addLayout(plot_layout)



    def openAddDialog(self):
        """Open an image dialog."""
        file_name, _ = QFileDialog.getOpenFileName()
        #_ , extension = os.path.splitext(self.last_file_name)
        my_img = FieldAnalysis(path = file_name)
        my_img.analyze(centering = Centering.GEOMETRIC_CENTER)
        results = my_img.results_data()

        distance_from_beam_center_to_panel_center_X = results.geometric_center_index_x_y[0]/my_img.image.dpmm - results.beam_center_index_x_y[0]/my_img.image.dpmm
        distance_from_beam_center_to_panel_center_Y = results.geometric_center_index_x_y[1]/my_img.image.dpmm - results.beam_center_index_x_y[1]/my_img.image.dpmm
        date_ = my_img.image.date_created(format = "%Y-%m-%d")
        positions = [date_, 
                     f"{distance_from_beam_center_to_panel_center_X:0.2f}", 
                     f"{distance_from_beam_center_to_panel_center_Y:0.2f}"
                     ]

        self.positionsModel.addPosition(positions)
        self.table.resizeColumnsToContents()
        self.update_plot()

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
    
    def update_plot(self):
        """Update the plot loading the database."""
        
        