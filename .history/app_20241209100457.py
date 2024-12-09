# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
# import pandas as pd
# import os

# app = Flask(__name__)

# # Database Configuration (SQLite stored in "instance" folder)
# db_path = os.path.join(os.path.dirname(__file__), 'instance', 'retail.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Models
# class Household(db.Model):
#     __tablename__ = 'Households'
#     Hshd_num = db.Column(db.Integer, primary_key=True)
#     Age_range = db.Column(db.String)
#     Income_range = db.Column(db.String)
#     Hshd_composition = db.Column(db.String)
#     Children = db.Column(db.Integer)

# class Transaction(db.Model):
#     __tablename__ = 'Transactions'
#     Transaction_id = db.Column(db.Integer, primary_key=True)
#     Hshd_num = db.Column(db.Integer)
#     Basket_num = db.Column(db.Integer)
#     Product_num = db.Column(db.Integer)
#     Spend = db.Column(db.Float)
#     Units = db.Column(db.Integer)
#     Date = db.Column(db.String)

# class Product(db.Model):
#     __tablename__ = 'Products'
#     Product_num = db.Column(db.Integer, primary_key=True)
#     Department = db.Column(db.String)
#     Commodity = db.Column(db.String)

# # Routes
# @app.route('/')
# def home():
#     """Home page that links to the dashboard."""
#     return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     """Renders the Retail KPI Dashboard."""
#     return render_template('dashboard.html')

# @app.route('/load_data')
# def load_data():
#     """Load data from CSV files into the database."""
#     datasets_path = os.path.dirname(__file__)

#     # Load Households
#     households_file = os.path.join(datasets_path, 'cleaned_households.csv')
#     households_data = pd.read_csv(households_file)
#     households_data.to_sql('Households', db.engine, if_exists='replace', index=False)

#     # Load Transactions
#     transactions_file = os.path.join(datasets_path, 'cleaned_transactions.csv')
#     transactions_data = pd.read_csv(transactions_file)
#     transactions_data.to_sql('Transactions', db.engine, if_exists='replace', index=False)

#     # Load Products
#     products_file = os.path.join(datasets_path, 'cleaned_products.csv')
#     products_data = pd.read_csv(products_file)
#     products_data.to_sql('Products', db.engine, if_exists='replace', index=False)

#     return "Data loaded successfully from cleaned CSVs!"

# @app.route('/data_pull/<hshd_num>')
# def data_pull(hshd_num):
#     """Pulls data for a specific household."""
#     query = f"""
#     SELECT t.Hshd_num, t.Basket_num, t.Date, t.Product_num, p.Department, p.Commodity, t.Spend
#     FROM Transactions t
#     JOIN Products p ON t.Product_num = p.Product_num
#     WHERE t.Hshd_num = {hshd_num}
#     ORDER BY t.Hshd_num, t.Basket_num, t.Date, t.Product_num;
#     """
#     result = db.engine.execute(query)
#     data = [dict(row) for row in result]
#     return jsonify(data)

# @app.route('/dashboard_data')
# def dashboard_data():
#     """API for seasonal trends on the dashboard."""
#     query = """
#     SELECT strftime('%m', Date) AS Month, SUM(Spend) AS TotalSpend
#     FROM Transactions
#     GROUP BY Month;
#     """
#     result = db.engine.execute(query)
#     data = [{'Month': row['Month'], 'TotalSpend': row['TotalSpend']} for row in result]
#     return jsonify(data)

# if __name__ == '__main__':
#     # Ensure the instance folder exists
#     os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

#     # Create database tables within the application context
#     with app.app_context():
#         db.create_all()

#     # Run the Flask app
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure database (if applicable)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials, please try again."

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)