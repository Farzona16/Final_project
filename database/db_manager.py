import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-M57USD6C\\SQLEXPRESS;'
        'DATABASE=BankAppDB;'
        'Trusted_Connection=yes;'
    )
    return conn

