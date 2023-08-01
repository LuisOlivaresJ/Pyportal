# -*- coding: utf-8 -*-

"""This module provides views to manage
the positions table. Views (QTableView)
are responsible for displaying the data 
to the user.
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT
import matplotlib.dates as mdates

from PySide6.QtWidgets import(
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QDialog,
    QAbstractItemView,
    QTabWidget,
)
from PySide6.QtCore import Qt

from pathlib import Path

from model import positionsModel, PandasModel
from tools import getXY
from database import load_reference_positions, load_tolerances, get_as_pd_dataframe, _positions_is_empty
from settings_gui import Settings_Gui

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent = None):
        """Initializer.
        
        centralWidget
            main_layout
                tab_widget
                    PositioningTab
                    LinearityTab
        """
        super().__init__(parent)
        self.setWindowTitle("QPortal")
        self.resize(1000, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
              
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)
              
        tab_widget = QTabWidget()
        self.main_layout.addWidget(tab_widget)

        tab_widget.addTab(PositionsTab(), "Positioning")
        tab_widget.addTab(LinearityTab(), "Linearity")
        tab_widget.addTab(UniformityTab(), "Uniformity")
        tab_widget.addTab(ReproducibilityTab(), "Reproducibility")
        

class PositionsTab(QWidget):
    def __init__(self, parent = None):
        """Initializer."""
        super().__init__(parent)
        self.positionsModel = positionsModel()

        # Secondary windows
        self.settings_window = None

        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        
        # Create widgets

        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.positionsModel.model)
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Create buttons
        self.addButton = QPushButton("Open...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteRow)
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.exportResults)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearAll)
        self.settingsButton = QPushButton("Settings")
        self.settingsButton.clicked.connect(self.settings)
        # Create canvas plot view
        self.view_canvas = FigureCanvas(Figure(figsize=(5,3), layout = 'constrained'))
        self.axes = self.view_canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view_canvas, self)
        self.update_plot()

        #Lay out the GUI
        self.hlayout = QHBoxLayout()

        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.exportButton)
        layout.addWidget(self.settingsButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.view_canvas)

        self.hlayout.addLayout(layout)
        self.hlayout.addWidget(self.table)
        self.hlayout.addLayout(plot_layout)

        self.setLayout(self.hlayout)

# Methods for buttons

    def openAddDialog(self):
        """This method is used to add data from new aquired images."""

        # Load reference data.
        ref = load_reference_positions()

        # Open an image dialog to ask for a directory.
        dir = QFileDialog.getExistingDirectory(caption = "Open the folder with the images...", dir="/home")
        # Filter 
        files = list(Path(dir).glob("RI*.dcm"))
     
        for file in files:

            xy = getXY(path = f"{file}")

            dif_x = round(xy["x"] - ref["x"], 2)
            dif_y = round(xy["y"] - ref["y"], 2)

            dif = {"dx": dif_x, "dy": dif_y}
            
            xy_results = {**xy, **dif}
            
            self.positionsModel.addPosition(xy_results)

        self.table.resizeColumnsToContents()
        self.update_plot()
        print("Número de archivos:")
        print(type(len(files)))

        self.show_results(len(files))

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
            _positions_is_empty()
            self.update_plot()

    def exportResults(self):
        """Export database."""
        return

    def settings(self):
        """This method is used to define user's settings."""
        if self.settings_window == None:
            self.settings_window = Settings_Gui()
        self.settings_window.exec()
        self.update_plot()

#___ end of methods for buttons


    def update_plot(self):
        """Update the plot loading the database."""

        df = get_as_pd_dataframe()
        tolerances = load_tolerances()
        t_position = tolerances["t_position"]
        self.axes.clear()
        #df.plot(x = "Date", y = ["dx", "dy"], kind = "bar", ax = self.axes)
        df.plot(x = "Date", y = ["dx", "dy"], ax = self.axes, style="o")
        #self.axes.bar(x = df["Date"], height = df["dx"])
        self.axes.xaxis.set_major_formatter(mdates.ConciseDateFormatter(self.axes.xaxis.get_major_locator()))
        self.axes.axhline(t_position, linestyle = "--", linewidth = 3, color = "g", alpha = 0.7)
        self.axes.axhline(-t_position, linestyle = "--", linewidth = 3, color = "g", alpha = 0.7)
        self.axes.grid(which="both")
        self.axes.set_ylim(bottom = -5, top = 5)
        self.axes.legend(loc = 'upper left')
        self.axes.set_ylabel("Variation [mm]")

        self.view_canvas.draw()

    def show_results(self, n):
        """A method to show the last n results from n loaded files."""
        df = get_as_pd_dataframe()
        #show_dialog = ShowDialog(df.tail(n))
        dialog = ShowDialog(df.tail(n))
        dialog.exec()
        #if dialog.exec() == 1:
        #    self.contactsModel.addContact(dialog.data)
        #    self.table.resizeColumnsToContents()

class LinearityTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        """"""

class UniformityTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        """"""

class ReproducibilityTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        """"""

class ShowDialog(QDialog):
    """Show results dialog."""
    def __init__(self, dataFrame, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Results")
        self.resize(750, 350)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.dataFrame = dataFrame

        self.setupUI()

    def setupUI(self):
        """Setup the Show dialog's GUI."""

        view = QTableView()
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        view.resizeColumnsToContents()
        view.resize(800, 500)
        view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(self.dataFrame, load_tolerances())
        view.setModel(model)

        self.layout.addWidget(view)
        # Add standar buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonsBox)



    