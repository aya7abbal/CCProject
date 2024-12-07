from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load datasets
transactions = pd.read_csv("cleaned_transactions.csv")
households = pd.read_csv("cleaned_households.csv")

# Login credentials for simplicity
users = {'testuser': 'password123'}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password!")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    hshd_num = request.form.get('hshd_num')
    if not hshd_num:
        return jsonify({'error': 'Household number is required'})

    try:
        hshd_num = int(hshd_num)
    except ValueError:
        return jsonify({'error': 'Invalid Household Number'})

    # Filter data
    filtered_transactions = transactions[transactions['HSHD_NUM'] == hshd_num]
    household_details = households[households['HSHD_NUM'] == hshd_num]

    if filtered_transactions.empty or household_details.empty:
        return jsonify({'error': 'No data found for this Household Number'})

    total_sales = filtered_transactions['SPEND'].sum()
    avg_price = filtered_transactions['SPEND'].mean()
    total_units = filtered_transactions['UNITS'].sum()

    sales_by_division = (
        filtered_transactions.groupby('STORE_R')['SPEND']
        .sum()
        .reset_index()
        .to_dict(orient='records')
    )

    top_commodities = (
        filtered_transactions.groupby('COMMODITY')['SPEND']
        .sum()
        .nlargest(5)
        .reset_index()
        .to_dict(orient='records')
    )

    demographics = household_details.iloc[0].to_dict()

    return jsonify({
        'total_sales': f"${total_sales:.2f}",
        'average_price': f"${avg_price:.2f}",
        'total_units_sold': int(total_units),
        'sales_by_division': sales_by_division,
        'top_commodities': top_commodities,
        'demographics': demographics
    })

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)