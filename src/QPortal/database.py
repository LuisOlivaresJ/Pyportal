# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMessageBox
from PySide6.QtSql import QSqlDatabase
from PySide6.QtSql import QSqlQuery

def createConnection(databaseName):
    """Create and open a database connection.

    Parameters
    ----------

    databaseName : str
        databaseName holds the name or path to the physical SQLite database file in your file system.
    """

    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "QPortal",
            f"Database Error: {connection.lastError().text()}",

        )
        return False
    print("SQL Connection Successfully Opened!")
    _createPositionsTable()
    return True

def _createPositionsTable():
    """Create the contacts table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        Create TABLE IF NOT EXISTS positions (
            date DATE NOT NULL,
            x  REAL NOT NULL,
            y  REAL NOT NULL,
            dx  REAL NOT NULL,
            dy  REAL NOT NULL  
        )
        """
    )