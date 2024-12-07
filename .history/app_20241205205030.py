from flask import Flask, request, render_template
import sqlite3  # or use your database library (e.g., psycopg2 for PostgreSQL)

app = Flask(__name__)

# Database connection function
def query_database(household_number):
    conn = sqlite3.connect('your_database.db')  # Update with your database path
    cursor = conn.cursor()
    query = """
        SELECT transactions.BASKET_NUM, transactions.PURCHASE_, transactions.PRODUCT_NUM, 
               products.DEPARTMENT, products.COMMODITY, transactions.SPEND, transactions.UNITS,
               transactions.STORE_R, transactions.WEEK_NUM, transactions.YEAR, 
               households.L, households.AGE_RANGE, households.MARITAL, households.INCOME_RANGE,
               households.HOMEOWNER, households.HSHD_COMPOSITION, households.HH_SIZE, households.CHILDREN
        FROM transactions
        JOIN households ON transactions.HSHD_NUM = households.HSHD_NUM
        JOIN products ON transactions.PRODUCT_NUM = products.PRODUCT_NUM
        WHERE households.HSHD_NUM = ?
        ORDER BY transactions.HSHD_NUM, transactions.BASKET_NUM, transactions.PURCHASE_;
    """
    cursor.execute(query, (household_number,))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def homepage():
    return render_template('dashboard.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    household_number = request.form.get('household_number')
    if not household_number:
        return render_template('dashboard.html', error="Please enter a Household Number.")
    
    data = query_database(household_number)
    if not data:
        return render_template('dashboard.html', error="No data found for this Household Number.")
    
    return render_template('dashboard.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)