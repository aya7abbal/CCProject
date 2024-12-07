from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Serve the dashboard page
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Sample API to fetch data for a specific household
@app.route('/get_data', methods=['GET'])
def get_data():
    hshd_num = request.args.get('hshd_num')
    # Load your cleaned datasets
    transactions = pd.read_csv('cleaned_transactions.csv')
    products = pd.read_csv('cleaned_products.csv')
    households = pd.read_csv('cleaned_households.csv')
    
    # Merge the datasets to create the display table
    data = pd.merge(transactions, products, on='PRODUCT_NUM', how='inner')
    data = pd.merge(data, households, on='HSHD_NUM', how='inner')
    filtered_data = data[data['HSHD_NUM'] == int(hshd_num)]
    
    # Sort by required columns
    filtered_data = filtered_data.sort_values(by=['HSHD_NUM', 'BASKET_NUM', 'PURCHASE_', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
    return jsonify(filtered_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)