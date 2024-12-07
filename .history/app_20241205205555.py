from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load datasets (use local files for now)
data_folder = "data"  # Ensure this folder exists in your project directory

transactions_file = os.path.join(data_folder, "cleaned_transactions.csv")
households_file = os.path.join(data_folder, "cleaned_households.csv")
products_file = os.path.join(data_folder, "cleaned_products.csv")

# Load local datasets
try:
    transactions = pd.read_csv(transactions_file)
    households = pd.read_csv(households_file)
    products = pd.read_csv(products_file)
    print("Datasets loaded successfully!")
except FileNotFoundError as e:
    print(f"Error: {e}. Ensure the CSV files are in the 'data' folder.")

@app.route("/")
def homepage():
    return render_template("dashboard.html")

@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    # Get household number from form
    hshd_num = request.form.get("hshd_num", type=int)

    # Filter transactions based on household number
    filtered_transactions = transactions[transactions["HSHD_NUM"] == hshd_num]

    # Merge with households and products datasets for more information
    merged_data = (
        filtered_transactions.merge(households, on="HSHD_NUM", how="left")
        .merge(products, on="PRODUCT_NUM", how="left")
    )

    # Convert merged data to a dictionary for rendering in the template
    data = merged_data.sort_values(
        ["HSHD_NUM", "BASKET_NUM", "PURCHASE_", "PRODUCT_NUM"]
    ).to_dict(orient="records")

    return render_template("dashboard.html", data=data, hshd_num=hshd_num)

# Transition to Azure setup
def load_data_from_azure():
    import pyodbc

    # Azure SQL Database connection details
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server.database.windows.net;"
        "DATABASE=your_database;"
        "UID=your_username;"
        "PWD=your_password;"
    )

    # Fetch data from Azure
    global transactions, households, products
    transactions = pd.read_sql_query("SELECT * FROM Transactions", conn)
    households = pd.read_sql_query("SELECT * FROM Households", conn)
    products = pd.read_sql_query("SELECT * FROM Products", conn)
    print("Data loaded from Azure!")

# Uncomment below to load data from Azure when ready
# load_data_from_azure()

if __name__ == "__main__":
    app.run(debug=True)