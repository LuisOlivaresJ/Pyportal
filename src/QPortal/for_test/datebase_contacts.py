from PySide6.QtSql import QSqlQuery, QSqlDatabase

con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("contacts.sqlite")
con.open()

# Creating a query for later execution using .prepare()
insertDataQuery = QSqlQuery()
insertDataQuery.prepare(
    """
    INSERT INTO contacts (
        name,
        job,
        email
    )
    VALUES (?, ?, ?)
    """
)

# Sample data
data = [
    ("Joe", "Senior Web Developer", "joe@example.com"),
    ("Lara", "Project Manager", "lara@example.com"),
    ("David", "Data Analyst", "david@example.com"),
    ("Jane", "Senior Python Developer", "jane@example.com"),
]

# Use .addBindValue() to insert data
for name, job, email in data:
    insertDataQuery.addBindValue(name)
    insertDataQuery.addBindValue(job)
    insertDataQuery.addBindValue(email)
    insertDataQuery.exec()