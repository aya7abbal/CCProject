import os
import pyodbc

# Fetch the connection string from Azure App Service environment variables
connection_string = os.getenv('RetailDB')

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    version = cursor.fetchone()
    print(f"Connected to Azure SQL Database! SQL Server version: {version[0]}")
except Exception as e:
    print(f"Error connecting to database: {e}")
finally:
    if conn:
        conn.close()