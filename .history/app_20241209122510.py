from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
    password_hash = db.Column(db.String(120), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

        # Check if the user exists in the database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            print(f"Login failed: username={username}, password={password}")  # Debugging log
            return redirect(url_for('home'))

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

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash)
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