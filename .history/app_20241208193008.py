from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

# Azure SQL database connection details using environment variables
server = os.getenv('DB_SERVER', 'cc-dbserver.database.windows.net')
database = os.getenv('DB_NAME', 'RetailDB')
username = os.getenv('DB_USERNAME', 'ccadmin')
password = os.getenv('DB_PASSWORD', 'aya7abbal!')
driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

def get_db_connection():
    """
    Establish a database connection using pyodbc.
    Returns the connection object if successful, None otherwise.
    """
    try:
        connection = pyodbc.connect(
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'PORT=1433;'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        print("Database connection established.")
        return connection
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None

@app.route('/')
def index():
    """
    Renders the main index page.
    """
    return render_template('index.html')

@app.route('/user_input', methods=['POST'])
def user_input():
    """
    Handles user input from the first form.
    """
    try:
        username = request.form['username']
        email = request.form['email']
        return f"Hello, {username}! Your email is {email}."
    except KeyError as e:
        print("Error handling user input:", e)
        return "Invalid form submission."

@app.route('/query_household', methods=['POST'])
def query_household():
    """
    Handles household data query from the second form and returns results.
    """
    hshd_num = request.form.get('hshd_num')
    if not hshd_num:
        return "Household number is required."

    # Query the database for the specified household number
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT 
                    t.hshd_num,
                    t.basket_num,
                    t.purchase AS Purchase_Date,
                    t.product_num,
                    p.department,
                    p.commodity
                FROM 
                    dbo.Retail_Transactions t
                JOIN 
                    dbo.Retail_Products p ON t.product_num = p.product_num
                WHERE 
                    t.hshd_num = ?
                ORDER BY 
                    t.hshd_num, t.basket_num, t.purchase, t.product_num;
            """
            cursor.execute(query, hshd_num)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            # Check if results are empty
            if not results:
                return f"No records found for Household Number: {hshd_num}"

            # Render results in a template
            return render_template('results.html', results=results, hshd_num=hshd_num)

        except pyodbc.Error as e:
            print("Query execution failed:", e)
            return "An error occurred while executing the query."
    else:
        return "Failed to connect to the database."

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error page.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Custom 500 error page.
    """
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)