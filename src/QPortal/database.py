# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtSql import QSqlDatabase
from PySide6.QtSql import QSqlQuery

import sys
import sqlite3
import pandas

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
            y  REAL NOT NULL,
            dx REAL NOT NULL,
            dy REAL NOT NULL
        )
        """
    )

def _isEmpty():
    """ 
    If there are no fields in the record database, opens a QDialog window to ask for a file that is going to be 
    used to get the reference portal position, saving it as the first row. Otherwise, returns 
    """
    isEmptyQuery = QSqlQuery()
    isEmptyQuery.exec("SELECT date, sid, gantry_angle, x, y, dx, dy FROM positions")
    if not isEmptyQuery.first():
        reference_file_name, _ = QFileDialog.getOpenFileName(caption = "Select a reference image.", dir="/home")
        #date, sid, gantry_angle, x, y = getXY(reference_file_name)
        xy = getXY(reference_file_name)
        print(xy)
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
            y,
            dx,
            dy
        )
        VALUES (?,?,?,?,?,?,?)
        """
        )

        # Use .addBindingValue() to insert data

        insertQuery.addBindValue(xy["Date"])
        insertQuery.addBindValue(xy["SID"])
        insertQuery.addBindValue(xy["G"])
        insertQuery.addBindValue(xy["x"])
        insertQuery.addBindValue(xy["y"])
        insertQuery.addBindValue(0)
        insertQuery.addBindValue(0)
        insertQuery.exec()
        insertQuery.finish()

    else:
        return

def get_reference_data():
    """
    Get the reference positions from the database.

    """
    refCon = QSqlDatabase.addDatabase("QSQLITE", "refCon")
    refCon.setDatabaseName("positions.sqlite")
    db = QSqlDatabase.database("refCon")
    if not refCon.open():
        print(f"Reference database error: {refCon.lastError().databaseText()}")
        sys.exit(1)
    
    getRefQuery = QSqlQuery(db)
    getRefQuery.exec("SELECT date, sid, gantry_angle, x, y, dx, dy FROM positions")
    #while getRefQuery.next():
    getRefQuery.first()

    referenceData = {"Date": getRefQuery.value("date"), 
                     "SID": getRefQuery.value("sid"), 
                     "G": getRefQuery.value("gantry_angle"), 
                     "x": getRefQuery.value("x"), 
                     "y": getRefQuery.value("y"),
                     "dx": getRefQuery.value("dx"),
                     "dy": getRefQuery.value("dy"),
                     }
    
    getRefQuery.finish()
    refCon.close()

    return referenceData

def get_as_pd_dataframe():
    """Get database as pandas DataFrame instance."""
    get_db_con = sqlite3.connect("positions.sqlite")
    df = pandas.read_sql_query("SELECT * FROM positions", get_db_con)
    get_db_con.close()


    df["Date"] = pandas.to_datetime(df["date"], format = "ISO8601")
    del df["date"]
    print(df)
    return df

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
