# -*- coding: utf-8 -*-

"""
This module provides a model to manage
the positions table. Models communicate
with and access the data in the database."""

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel

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
        headers = ("Date", "SID", "G. angle", "x", "y")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
    
    def addPosition(self, position):
        """Add a position to the database."""
        print(position)
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(position):
            self.model.setData(self.model.index(rows, column), field)
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