import os
import pyodbc

conn_str = os.getenv('RetailDB')
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connected to Azure SQL Database!")
    print("SQL Server version:", row[0])
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        conn.close()