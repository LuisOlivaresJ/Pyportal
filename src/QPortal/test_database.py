from PySide6.QtSql import QSqlDatabase, QSqlQuery
#from database import createConnection
import sys

#createConnection("positions.sqlite")
# Create the connection
con = QSqlDatabase.addDatabase("QSQLITE", 'con')
con.setDatabaseName("positions.sqlite")
db = QSqlDatabase.database('con', open = False)

# Open the connection
if not con.open():
    print(f"Database Error: {con.lastError().databaseText()}")
    sys.exit(1)

# Create a query and executes it right away using .exec()
createTableQuery = QSqlQuery(db)
createTableQuery.exec(
    """
    CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(40) NOT NULL,
    job VARCHAR(50),
    email VARCHAR(40) NOT NULL
    )
    """
)
print(con.tables())
print(con.isOpen())

#Create a query for later execution using .prepare()
insertQuery = QSqlQuery(db)
insertQuery.prepare(
    """
    INSERT INTO contacts (
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


# Database using pandas
# - # - # - # - # - # -
import sqlite3
import pandas as pd

conect = sqlite3.connect("positions.sqlite")
db = pd.read_sql_query("SELECT * FROM positions", conect)














"""
data2 = [
    ("Luis", "Physicist", "cucei@example"),
    ("Alfonso", "Medical", "alfonso@cucei")
]

query2 = QSqlQuery()
query2.prepare(
    "
    INSERT INTO contacts(
    name,
    job,
    email
    )
    VALUES(?,?,?)
    "
)

for row in data2:
    i = 0
    for item in row:
        query2.bindValue(i, item)
        i += 1
    query2.exec()

"""

#print(con.tables())
#print(con.isOpen())
#date = "2023-01-15"
#x = 2
#y = 4
# Create a query and execute it right away using .exec()
#query = QSqlQuery()
#query.exec(
#    f"""INSERT INTO positions (date, x, y)
#    VALUES ('{date}', '{x}', '{y}')"""
#)