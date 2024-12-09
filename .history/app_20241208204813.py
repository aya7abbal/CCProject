import mysql.connector
from mysql.connector import errorcode

print('test')


config = {
  'host':'cc-dbserver.database.windows.net',
  'user':'ccadmin',
  'password':'aya7abbal!',
  'database':'RetailDB'
}

try:
    # Unpack the dictionary with **
    conn = mysql.connector.connect(**config)
    print("Connection successful:", conn)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Invalid credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(f"Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()