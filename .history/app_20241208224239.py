import pytds

try:
    # Establish connection to Azure SQL Database with encryption
    conn = pytds.connect(
        server='cc-dbserver.database.windows.net',
        database='RetailDB',
        user='ccadmin@cc-dbserver',
        password='aya7abbal!',
        port=1433,
        autocommit=True,
        encrypt=True  # Enable encryption
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to test the connection
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()

    # Print the SQL Server version
    print(f"Connected to Azure SQL Database. SQL Server version: {row[0]}")

except Exception as e:
    print(f"Error connecting to database: {e}")

finally:
    # Close the connection
    if 'conn' in locals() and conn:
        conn.close()