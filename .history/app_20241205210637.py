from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Initialize Flask
app = Flask(__name__)

# Load datasets
transactions = pd.read_csv("cleaned_transactions.csv")
households = pd.read_csv("cleaned_households.csv")
products = pd.read_csv("cleaned_products.csv")

# Merge datasets for easier analysis
merged_data = transactions.merge(households, on="HSHD_NUM").merge(products, on="PRODUCT_NUM")

@app.route("/")
def homepage():
    return render_template("dashboard.html")

@app.route("/visualization", methods=["GET", "POST"])
def visualization():
    hshd_num = request.form.get("household_number", None)
    if hshd_num:
        filtered_data = merged_data[merged_data["HSHD_NUM"] == int(hshd_num)]
    else:
        filtered_data = merged_data

    # Calculate KPIs
    total_sales = round(filtered_data["SPEND"].sum(), 2)
    avg_price = round(filtered_data["SPEND"].mean(), 2)
    total_units = int(filtered_data["UNITS"].sum())

    # Generate charts
    sales_by_division = px.bar(
        filtered_data.groupby("STORE_R")["SPEND"].sum().reset_index(),
        x="STORE_R", y="SPEND", title="Sales by Division", color="STORE_R"
    )

    avg_price_chart = px.line(
        filtered_data.groupby("PURCHASE_")["SPEND"].mean().reset_index(),
        x="PURCHASE_", y="SPEND", title="Average Price per Date"
    )

    top_items_chart = px.bar(
        filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index().nlargest(5, "SPEND"),
        x="COMMODITY", y="SPEND", title="Top 5 Selling Commodities", color="COMMODITY"
    )

    # Convert charts to JSON for rendering
    sales_by_division_json = sales_by_division.to_json()
    avg_price_chart_json = avg_price_chart.to_json()
    top_items_chart_json = top_items_chart.to_json()

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        total_units=total_units,
        sales_by_division_json=sales_by_division_json,
        avg_price_chart_json=avg_price_chart_json,
        top_items_chart_json=top_items_chart_json,
    )

if __name__ == "__main__":
    app.run(debug=True)