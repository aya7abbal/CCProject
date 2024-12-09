from flask import Flask, render_template, request
import pytds

app = Flask(__name__)

# Azure SQL database connection details
server = 'cc-dbserver.database.windows.net'
database = 'RetailDB'
username = 'ccadmin'
password = 'aya7abbal!'

def get_db_connection():
    try:
        connection = pytds.connect(
            server=server,
            database=database,
            user=username,
            password=password,
            port=1433,
            timeout=30
        )
        print("Database connection established.")
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
                    Retail_Transactions t
                JOIN 
                    Retail_Products p ON t.product_num = p.product_num
                WHERE 
                    t.hshd_num = %s
                ORDER BY 
                    t.hshd_num, t.basket_num, t.purchase, t.product_num;
            """
            cursor.execute(query, [hshd_num])
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            # Render results in a template
            return render_template('results.html', results=results, hshd_num=hshd_num)

        except Exception as e:
            print("Query execution failed:", e)
            return "An error occurred while executing the query."
    else:
        return "Failed to connect to the database."

if __name__ == "__main__":
    app.run(debug=True)