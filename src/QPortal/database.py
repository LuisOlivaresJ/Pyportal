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
    _createUserToleranceTable()
    _createLinearityTable()
    _createUniformityTable()
    _positions_is_empty()
    _tolerances_is_empty()
    #_linearity_is_empty()
    return True

def _createPositionsTable():
    """Create the positions table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS positions (
            Date VARCHAR(25) NOT NULL,
            SID REAL NOT NULL,
            Gantry REAL NOT NULL,
            x  REAL NOT NULL,
            y  REAL NOT NULL,
            dx REAL NOT NULL,
            dy REAL NOT NULL
        )
        """
    )

def _createUserToleranceTable():
    """Table used to create save linearity constancy."""
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS tolerances (
        tolerance_position REAL NOT NULL,
        tolerance_linearity REAL NOT NULL,
        tolerance_uniformity REAL NOT NULL,
        tolerance_reproducibility REAL NOT NULL
        )
        """
    )
    createTableQuery.finish()

def _createLinearityTable():
    """Used to create user settings like tolerances for test."""
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS linearity (
        date VARCHAR(25) NOT NULL,
        mu REAL NOT NULL,
        cu REAL NOT NULL,
        cu_mu REAL NOT NULL,
        variation REAL NOT NULL
        )
        """
    )
    createTableQuery.finish()

def _createUniformityTable():
    """Used to create user settings like tolerances for test."""
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS uniformity (
        Date VARCHAR(25) NOT NULL,
        Mean REAL NOT NULL,
        STD REAL NOT NULL,
        STD_Mean REAL NOT NULL
        )
        """
    )
    createTableQuery.finish()

def _positions_is_empty():
    """ 
    If there are no fields in the record database, opens a QDialog window to ask for a file that is going to be 
    used to get the reference portal position, saving it as the first row. Otherwise, returns 
    """
    isEmptyQuery = QSqlQuery()
    isEmptyQuery.exec("SELECT Date, SID, Gantry, x, y, dx, dy FROM positions")
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
            Date,
            SID,
            Gantry,
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
        insertQuery.addBindValue(xy["Gantry"])
        insertQuery.addBindValue(xy["x"])
        insertQuery.addBindValue(xy["y"])
        insertQuery.addBindValue(0)
        insertQuery.addBindValue(0)
        insertQuery.exec()
        insertQuery.finish()

    else:
        return

def _linearity_is_empty():
    """ 
    If there are no fields in the record database, returns True
    """
    isEmptyQuery = QSqlQuery()
    isEmptyQuery.exec("SELECT * FROM linearity")
    return isEmptyQuery.first()

def _tolerances_is_empty():
    """ 
    Set default tolerances when app is first used. 
    """
    isEmptyQuery = QSqlQuery()
    isEmptyQuery.exec("""
        SELECT tolerance_position,
        tolerance_linearity,
        tolerance_uniformity,
        tolerance_reproducibility FROM tolerances
        """
        )
    if not isEmptyQuery.first():

        insertQuery = QSqlQuery()
        insertQuery.prepare(
        """
        INSERT INTO tolerances (
            tolerance_position,
            tolerance_linearity,
            tolerance_uniformity,
            tolerance_reproducibility
        )
        VALUES (?,?,?,?)
        """
        )

        # Use .addBindingValue() to insert data

        insertQuery.addBindValue(2)
        insertQuery.addBindValue(2)
        insertQuery.addBindValue(2)
        insertQuery.addBindValue(2)
        insertQuery.exec()
        insertQuery.finish()

    else:
        return


def load_reference_positions():
    """
    Get the reference positions from the firts row of the database.

    Returns : dictionary
        {Date: , SID: , G: , x: , y: , dx: , dy: }
    """
    
    getRefQuery = QSqlQuery()
    getRefQuery.exec("SELECT Date, SID, Gantry, x, y, dx, dy FROM positions")
    getRefQuery.first()

    referenceData = {"Date": getRefQuery.value("Date"), 
                     "SID": getRefQuery.value("SID"), 
                     "G": getRefQuery.value("Gantry"), 
                     "x": getRefQuery.value("x"), 
                     "y": getRefQuery.value("y"),
                     "dx": getRefQuery.value("dx"),
                     "dy": getRefQuery.value("dy"),
                     }
    
    getRefQuery.finish()

    return referenceData

def load_tolerances():
    """
    Get the tolerances from the database.

    Returns : dictionary
        {t_position: ,
        t_linearity: ,
        t_uniformity: ,
        t_reproducibility: 
        }
    """
    
    getTolQuery = QSqlQuery()
    getTolQuery.exec(
        """
        SELECT tolerance_position,
        tolerance_linearity, 
        tolerance_uniformity, 
        tolerance_reproducibility
        FROM tolerances
        """
        )
    #while getRefQuery.next():
    getTolQuery.first()

    tolerancesData = {"t_position": getTolQuery.value("tolerance_position"), 
                     "t_linearity": getTolQuery.value("tolerance_linearity"), 
                     "t_uniformity": getTolQuery.value("tolerance_uniformity"), 
                     "t_reproducibility": getTolQuery.value("tolerance_reproducibility"), 
                     }
    
    getTolQuery.finish()

    return tolerancesData

def get_as_pd_dataframe():
    """Get database as pandas DataFrame instance."""
    get_db_con = sqlite3.connect("positions.sqlite")
    df = pandas.read_sql_query("SELECT * FROM positions", get_db_con)
    get_db_con.close()


    df["Date"] = pandas.to_datetime(df["Date"], format="%Y-%m-%d")
    return df

def get_linearity_as_pd_dataframe():
    """Get linearity database as pandas DataFrame instance."""
    get_db_con = sqlite3.connect("positions.sqlite")
    df = pandas.read_sql_query("SELECT * FROM linearity", get_db_con)
    get_db_con.close()


    df["date"] = pandas.to_datetime(df["date"], format="%Y-%m-%d")
    return df
