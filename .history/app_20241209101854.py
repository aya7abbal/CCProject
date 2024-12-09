from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up application secret key and database configuration
app.secret_key = 'your_secret_key'

# Ensure the `instance` directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

# Configure the SQLite database path
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'retail.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

# Define other models if necessary (example: Household, Transaction, Product)
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

# Routes
@app.route('/')
def home():
    """Home page with login functionality."""
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('home'))

    # If the request method is GET, render the login page
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard after login."""
    if 'user_id' not in session:
        flash('You need to login first!', 'warning')
        return redirect(url_for('home'))

    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Database setup: Create tables if they do not exist
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)