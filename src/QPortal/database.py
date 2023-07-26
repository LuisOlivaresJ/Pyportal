# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtSql import QSqlDatabase
from PySide6.QtSql import QSqlQuery

import sys

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
            gantry_angle REAL NOT NULL,
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
    isEmptyQuery.exec("SELECT date, sid, gantry_angle, x, y FROM positions")
    if not isEmptyQuery.first():
        reference_file_name, _ = QFileDialog.getOpenFileName(caption = "Select a reference image.", dir="/home")
        date, sid, gantry_angle, x, y = getXY(reference_file_name)
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
            gantry_angle,
            x,
            y
        )
        VALUES (?,?,?,?,?)
        """
        )

        # Use .addBindingValue() to insert data

        insertQuery.addBindValue(date)
        insertQuery.addBindValue(sid)
        insertQuery.addBindValue(gantry_angle)
        insertQuery.addBindValue(x)
        insertQuery.addBindValue(y)
        insertQuery.exec()
        insertQuery.finish()

    else:
        return

def get_reference_data():
    """
    Get the reference positions from the database

    """
    refCon = QSqlDatabase.addDatabase("QSQLITE", "refCon")
    refCon.setDatabaseName("positions.sqlite")
    db = QSqlDatabase.database("refCon")
    if not refCon.open():
        print(f"Reference database error: {refCon.lastError().databaseText()}")
        sys.exit(1)
    
    getRefQuery = QSqlQuery(db)
    getRefQuery.exec("SELECT date, sid, gantry_angle, x, y FROM positions")
    #while getRefQuery.next():
    getRefQuery.first()

    referenceData = {"Date": getRefQuery.value("date"), 
                     "SID": getRefQuery.value("sid"), 
                     "G": getRefQuery.value("gantry_angle"), 
                     "x": getRefQuery.value("x"), 
                     "y": getRefQuery.value("y")
                     }
    
    getRefQuery.finish()
    refCon.close()

    return referenceData

def insertData(data):
    insertCon = QSqlDatabase.addDatabase("QSQLITE", "insertCon")
    insertCon.setDatabaseName("positions.sqlite")
    db = QSqlDatabase.database("insertCon")
    if not insertCon.open():
        print(f"Insert database error: {insertCon.lastError().databaseText()}")
        sys.exit(1)

    insertQuery = QSqlQuery(db)
    insertQuery.prepare(
        """
        INSERT INTO positions (
            name,
            job,
            email
        )
        VALUES (?,?,?)
        """
    )

    # sample data
    data = [
        ("Joe","Senior","joe@example"),
        ("Lara", "Project", "lara@example"),
    ]

    # Use .addBindingValue() to insert data
    for name, job, email in data:
        insertQuery.addBindValue(name)
        insertQuery.addBindValue(job)
        insertQuery.addBindValue(email)
        insertQuery.exec()
