from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load datasets
transactions = pd.read_csv("cleaned_transactions.csv")
households = pd.read_csv("cleaned_households.csv")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

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

if __name__ == "__main__":
    app.run(debug=True)