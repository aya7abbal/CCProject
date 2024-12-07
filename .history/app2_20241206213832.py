from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)

# Configure database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Household(db.Model):
    __tablename__ = 'Households'
    Hshd_num = db.Column(db.Integer, primary_key=True)
    Age_range = db.Column(db.String)
    Income_range = db.Column(db.String)
    Hshd_composition = db.Column(db.String)
    Children = db.Column(db.Integer)

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    Transaction_id = db.Column(db.Integer, primary_key=True)
    Hshd_num = db.Column(db.Integer)
    Basket_num = db.Column(db.Integer)
    Product_num = db.Column(db.Integer)
    Spend = db.Column(db.Float)
    Units = db.Column(db.Integer)
    Date = db.Column(db.String)

class Product(db.Model):
    __tablename__ = 'Products'
    Product_num = db.Column(db.Integer, primary_key=True)
    Department = db.Column(db.String)
    Commodity = db.Column(db.String)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Upload CSV Data
@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    data = pd.read_csv(file)
    table_name = request.form['table']
    data.to_sql(table_name, con=db.engine, if_exists='append', index=False)
    return "Data uploaded successfully!"

# Data Pull for a Household
@app.route('/data_pull/<hshd_num>')
def data_pull(hshd_num):
    query = f"""
    SELECT t.Hshd_num, t.Basket_num, t.Date, t.Product_num, p.Department, p.Commodity, t.Spend
    FROM Transactions t
    JOIN Products p ON t.Product_num = p.Product_num
    WHERE t.Hshd_num = {hshd_num}
    ORDER BY t.Hshd_num, t.Basket_num, t.Date, t.Product_num;
    """
    result = db.engine.execute(query)
    data = [dict(row) for row in result]
    return jsonify(data)

# API for Dashboard Data
@app.route('/dashboard_data')
def dashboard_data():
    # Example data: Return dummy seasonal trends for now
    query = """
    SELECT strftime('%m', Date) AS Month, SUM(Spend) AS TotalSpend
    FROM Transactions
    GROUP BY Month;
    """
    result = db.engine.execute(query)
    data = [dict(row) for row in result]
    return jsonify(data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)