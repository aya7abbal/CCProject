from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("app.html")  # Flask will now find it in the `templates` folder

# Route to fetch data for a specific household
@app.route('/get_data', methods=['GET'])
def get_data():
    hshd_num = request.args.get('hshd_num')
    transactions = pd.read_csv('cleaned_transactions.csv')
    products = pd.read_csv('cleaned_products.csv')
    households = pd.read_csv('cleaned_households.csv')
    
    # Merge datasets
    data = pd.merge(transactions, products, on='PRODUCT_NUM', how='inner')
    data = pd.merge(data, households, on='HSHD_NUM', how='inner')
    filtered_data = data[data['HSHD_NUM'] == int(hshd_num)]
    
    # Sort results
    filtered_data = filtered_data.sort_values(by=['HSHD_NUM', 'BASKET_NUM', 'PURCHASE_', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
    return jsonify(filtered_data.to_dict(orient='records'))

# Dashboard route using Dash
@app.route('/dashboard')
def create_dashboard():
    # Dash app
    app_dash = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')
    
    # Load transactions dataset
    transactions = pd.read_csv('cleaned_transactions.csv')
    spending_trends = transactions.groupby('PURCHASE_')['SPEND'].sum().reset_index()

    # Create a Plotly figure
    fig = px.line(spending_trends, x='PURCHASE_', y='SPEND', title='Spending Trends Over Time')

    # Define Dash layout
    app_dash.layout = html.Div([
        html.H1('Retail Dashboard', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig)
    ])
    
    return app_dash.server

# Run the app
if __name__ == '__main__':
    app.run(debug=True)