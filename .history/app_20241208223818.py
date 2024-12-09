import pymssql

try:
    # Establish connection
    conn = pymssql.connect(
        server='cc-dbserver.database.windows.net',
        user='ccadmin@cc-dbserver',
        password='aya7abbal!',
        database='RetailDB'
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to test the connection
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()

    # Print the result
    print(f"Connected to Azure SQL Database. SQL Server version: {row[0]}")

except Exception as e:
    print(f"Error connecting to database: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()