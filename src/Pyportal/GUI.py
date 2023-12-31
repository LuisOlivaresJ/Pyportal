# -*- coding: utf-8 -*-

"""This module provides Pyportal application access point."""

import sys
from PySide6.QtWidgets import QApplication

from database import createConnection
from views import Window


"""Pyportal main function."""

# Create the application 
app = QApplication(sys.argv)
# Connect to the database before creating any window
if not createConnection("database.sqlite"):
    sys.exit(1)

# Create the main window if the connection succeeded
win = Window()
win.show()
# Run the event loop
sys.exit(app.exec())

