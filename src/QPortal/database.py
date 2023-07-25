# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtSql import QSqlDatabase
from PySide6.QtSql import QSqlQuery

from tools import getXY

def createConnection(databaseName):
    """Create and open a database connection.

    Parameters
    ----------

    databaseName : str
        databaseName holds the name or path to the physical SQLite database file in your file system.
    """

    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName(databaseName)
    #db = QSqlDatabase.database('db')

    if not con.open():
        QMessageBox.warning(
            None,
            "QPortal",
            f"Database Error: {con.lastError().text()}",

        )
        return False
    print("SQL Connection Successfully Opened!")
    _createPositionsTable()
    _isEmpty()
    return True

def _createPositionsTable():
    """Create the positions table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS positions (
            date VARCHAR(40) NOT NULL,
            sid REAL NOT NULL,
            x  REAL NOT NULL,
            y  REAL NOT NULL
        )
        """
    )

def _isEmpty():
    """ 
    If there are no fields in the record database, opens a QDialog window to ask for a file that is going to be 
    used to get the reference portal position, saving it as the first row. Otherwise, returns 
    """
    isEmptyQuery = QSqlQuery()
    if isEmptyQuery.record().isEmpty():
        reference_file_name, _ = QFileDialog.getOpenFileName(caption = "Select a reference image.", dir="/home")
        date, sid, x, y = getXY(reference_file_name)
        print(
            f"Date created: {date}, SID: {sid}, x: {x}, y: {y}")
        isEmptyQuery.finish()

        #Create a query for later execution using .prepare()
        insertQuery = QSqlQuery()
        insertQuery.prepare(
        """
        INSERT INTO positions (
            date,
            sid,
            x,
            y
        )
        VALUES (?,?,?,?)
        """
        )

        # Use .addBindingValue() to insert data

        insertQuery.addBindValue(date)
        insertQuery.addBindValue(sid)
        insertQuery.addBindValue(x)
        insertQuery.addBindValue(y)
        insertQuery.exec()
        insertQuery.finish()

    else:
        return
