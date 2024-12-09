from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Azure SQL database connection details
server = os.getenv('DB_SERVER', 'cc-dbserver.database.windows.net')
database = os.getenv('DB_NAME', 'RetailDB')
username = os.getenv('DB_USERNAME', 'ccadmin')
password = os.getenv('DB_PASSWORD', 'aya7abbal!')
driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

UPLOAD_FOLDER = './uploads'  # Folder to save uploaded files
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection function
def get_db_connection():
    try:
        connection = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        )
        return connection
    except Exception as e:
        print("Database connection failed:", e)
        return None

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

# Sample Data Pull for HSHD_NUM #10
@app.route('/sample_data', methods=['GET'])
def sample_data():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT 
                    t.hshd_num, t.basket_num, t.purchase AS Purchase_Date, 
                    t.product_num, p.department, p.commodity
                FROM 
                    dbo.Retail_Transactions t
                JOIN 
                    dbo.Retail_Products p ON t.product_num = p.product_num
                WHERE 
                    t.hshd_num = 10
                ORDER BY 
                    t.hshd_num, t.basket_num, t.purchase, t.product_num;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('sample_data.html', results=results)
        except Exception as e:
            print("Query execution failed:", e)
            return "An error occurred while executing the query."
    else:
        return "Failed to connect to the database."

# Search Web Page for Data Pulls by HSHD_NUM
@app.route('/query_household', methods=['GET', 'POST'])
def query_household():
    if request.method == 'POST':
        hshd_num = request.form['hshd_num']
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT 
                        t.hshd_num, t.basket_num, t.purchase AS Purchase_Date, 
                        t.product_num, p.department, p.commodity
                    FROM 
                        dbo.Retail_Transactions t
                    JOIN 
                        dbo.Retail_Products p ON t.product_num = p.product_num
                    WHERE 
                        t.hshd_num = ?
                    ORDER BY 
                        t.hshd_num, t.basket_num, t.purchase, t.product_num;
                """
                cursor.execute(query, (hshd_num,))
                results = cursor.fetchall()
                cursor.close()
                connection.close()
                return render_template('results.html', results=results, hshd_num=hshd_num)
            except Exception as e:
                print("Query execution failed:", e)
                return "An error occurred while executing the query."
        else:
            return "Failed to connect to the database."
    return render_template('query_form.html')

# Data Loading Web App
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Process the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                # Assuming CSV format
                df = pd.read_csv(file_path)
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    table_name = filename.split('.')[0]  # Use filename to decide table
                    for _, row in df.iterrows():
                        # Build an insert query dynamically based on table_name
                        query = f"INSERT INTO dbo.{table_name} VALUES ({','.join(['?' for _ in row])})"
                        cursor.execute(query, tuple(row))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    flash('File uploaded and processed successfully.')
                else:
                    flash('Database connection failed.')
            except Exception as e:
                print("File processing failed:", e)
                flash('An error occurred while processing the file.')
            return redirect(url_for('upload_file'))
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)