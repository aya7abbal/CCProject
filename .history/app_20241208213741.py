from flask import Flask
import os
import pyodbc

app = Flask(__name__)

@app.route('/')
def home():
    connection_string = os.getenv('RetailDB')
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION;")
        row = cursor.fetchone()
        return f"Connected to Azure SQL Database! SQL Server version: {row[0]}"
    except Exception as e:
        return f"Error: {e}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)