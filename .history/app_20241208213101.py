import pymssql

try:
    conn = pymssql.connect(
        server='cc-dbserver.database.windows.net',
        user='ccadmin',
        password='aya7abbal!',
        database='RetailDB'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connected successfully!")
    print("SQL Server version:", row[0])
except pymssql.Error as e:
    print("Error while connecting to SQL Server:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")