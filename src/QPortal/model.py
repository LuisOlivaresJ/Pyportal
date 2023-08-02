# -*- coding: utf-8 -*-

"""
This module provides a model to manage
the positions table. Models communicate
with and access the data in the database."""

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtSql import QSqlTableModel
from PySide6 import QtGui
import pandas

class positionsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        #tableModel.setFilter("")
        tableModel.setTable("positions")
        #tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("Date", "SID", "G°", "x", "y", "dx", "dy")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
    
    def addPosition(self, position):
        """Add a position to the database."""
        print(position)
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(position):
            self.model.setData(self.model.index(rows, column), position[field])
        self.model.submitAll()
        self.model.select()

    def deleteRow(self, row):
        """Remove a row from the database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearAll(self):
        """Remoce all data in the database."""
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()

class LinearityModel:
    """"""
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        #tableModel.setFilter("")
        tableModel.setTable("linearity")
        #tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("Date", "MU", "CU", "CU/MU", "Variation [%]")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
    
    def addNewResults(self, results):
        """Add new results to the database."""
        print(results)
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(results):
            self.model.setData(self.model.index(rows, column), results[field])
        self.model.submitAll()
        self.model.select()

    def deleteRow(self, row):
        """Remove a row from the database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearAll(self):
        """Remoce all data in the database."""
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()

class PandasModel(QAbstractTableModel):
    # Copyright (C) 2022 The Qt Company Ltd.
    # SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pandas.DataFrame, tolerance, columns, headers, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        self.tolerance = tolerance
        self.columns = columns
        self.headers = headers
    
    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        """
        if role == Qt.ForegroundRole:   # To change color font
            value = self._dataframe.iloc[index.row()][index.column()]
            #value = self._dataframe.iloc[index.row(), ["dx","dy"]]

            if index.column() == 5 or index.column() == 6:
                "Columns 5 and 6 refers to dx and dy in the pandas dataframe."
                if (
                    (isinstance(value, int) or isinstance(value, float))
                    and value >= 2
                ):
                    return QtGui.QColor('red')
                        
        if role == Qt.BackgroundRole:
            value = self._dataframe.iloc[index.row()][index.column()]

            if index.column() == 5 or index.column() == 6:  # change background only for ccolumns(5,6)
                if (
                    (isinstance(value, int) or isinstance(value, float))
                    and value >= 2
                ):
                    return QtGui.QColor('red')
                else:
                    return QtGui.QColor('green')
        """        
        if role == Qt.DecorationRole:
            value = self._dataframe.iloc[index.row()][index.column()]

            if index.column() in self.columns:  # change icon decoration only for columns(5,6)
                if (
                    (isinstance(value, int) or isinstance(value, float))
                    and abs(value) >= self.tolerance
                ):
                    return QtGui.QIcon('.\icons\cross.png')
                else:
                    return QtGui.QIcon('.\icons\\accept.png')
                
        if role == Qt.FontRole:
            if index.column() in self.columns:  # change font
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                return bold_font

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None

class ToleranceModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        #tableModel.setFilter("")
        tableModel.setTable("tolerances")
        tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("Position [mm]", "Linearity [%]", "Uniformity [%]", "Reproducibility ")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
    