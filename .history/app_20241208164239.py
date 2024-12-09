

from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Azure SQL database connection details
server = 'your-server-name.database.windows.net'
database = 'RetailDB'
username = 'your-username'
password = 'your-password'
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    try:
        connection = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        )
        return connection
    except Exception as e:
        print("Database connection failed:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_input', methods=['POST'])
def user_input():
    # Handle user input from the first form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    return f"Hello, {username}! Your email is {email}."

@app.route('/query_household', methods=['POST'])
def query_household():
    # Handle household data query from the second form
    hshd_num = request.form['hshd_num']

    # Query the database for the specified household number
    connection = get_db_connection()
    if connection:
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
        cursor.execute(query, (hshd_num,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Render results in a template
        return render_template('results.html', results=results, hshd_num=hshd_num)

    return "Failed to connect to the database."

if __name__ == "__main__":
    app.run(debug=True)