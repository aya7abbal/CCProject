import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=cc-dbserver.database.windows.net;'
        'DATABASE=RetailDB;'
        'UID=ccadmin;'
        'PWD=aya7abbal!'
    )

    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connected successfully!")
    print("SQL Server Version:", row[0])
    
except pyodbc.Error as e:
    print("Error while connecting to SQL Server:", e)
    
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")