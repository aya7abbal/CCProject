from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json  # Import json for handling empty plots

# Initialize Flask
app = Flask(__name__)

# Load datasets
transactions = pd.read_csv("./cleaned_transactions.csv")
households = pd.read_csv("./cleaned_households.csv")
products = pd.read_csv("./cleaned_products.csv")

# Merge datasets for easier analysis
merged_data = transactions.merge(households, on="HSHD_NUM").merge(products, on="PRODUCT_NUM")

@app.route("/")
def homepage():
    # Provide empty graphs data for the initial page load
    empty_graph = json.dumps({"data": [], "layout": {}})
    return render_template("dashboard.html", total_sales=0, avg_price=0, graphs={
        'sales_by_division': empty_graph, 'avg_price_chart': empty_graph
    })

@app.route("/visualization", methods=["POST"])
def visualization():
    hshd_num = request.form.get("household_number", "")
    region = request.form.get("store_region", "")
    income_group = request.form.get("income_group", "")

    filtered_data = merged_data
    if hshd_num.isdigit():
        filtered_data = filtered_data[filtered_data["HSHD_NUM"] == int(hshd_num)]
    if region:
        filtered_data = filtered_data[filtered_data["STORE_R"] == region]
    if income_group:
        filtered_data = filtered_data[filtered_data["INCOME_RANGE"] == income_group]

    # Calculate KPIs
    total_sales = round(filtered_data["SPEND"].sum(), 2)
    avg_price = round(filtered_data["SPEND"].mean(), 2)

    # Generate Charts
    sales_by_division = px.bar(
        filtered_data.groupby("STORE_R")["SPEND"].sum().reset_index(),
        x="STORE_R", y="SPEND", title="Sales by Division"
    )

    avg_price_chart = px.line(
        filtered_data.groupby("PURCHASE_")["SPEND"].mean().reset_index(),
        x="PURCHASE_", y="SPEND", title="Average Price Over Time"
    )

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        graphs={
            'sales_by_division': sales_by_division.to_json(),
            'avg_price_chart': avg_price_chart.to_json()
        }
    )

if __name__ == "__main__":
    app.run(debug=True)