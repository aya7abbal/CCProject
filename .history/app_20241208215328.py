from flask import Flask
import os
import pyodbc

app = Flask(__name__)

@app.route("/")
def test_db_connection():
    try:
        # Get the connection string from environment variables
        conn_str = os.getenv("RetailDB")
        
        # Establish connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION;")
        version = cursor.fetchone()
        
        return f"Connected to Azure SQL Database! SQL Server version: {version[0]}"
    except Exception as e:
        return f"Error connecting to database: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)