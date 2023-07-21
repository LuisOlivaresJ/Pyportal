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