from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

# Initialize Flask
app = Flask(__name__)

# Correct paths to the datasets
transactions = pd.read_csv("./cleaned_transactions.csv")
households = pd.read_csv("./cleaned_households.csv")
products = pd.read_csv("./cleaned_products.csv")

# Merge datasets for easier analysis
merged_data = transactions.merge(households, on="HSHD_NUM").merge(products, on="PRODUCT_NUM")

@app.route("/")
def homepage():
    return render_template("dashboard.html")

@app.route("/visualization", methods=["GET", "POST"])
def visualization():
    # Handle Filters
    hshd_num = request.form.get("household_number")
    region = request.form.get("store_region")
    income_group = request.form.get("income_group")

    filtered_data = merged_data

    # Apply filters to the data
    if hshd_num and hshd_num.isdigit():
        filtered_data = filtered_data[filtered_data["HSHD_NUM"] == int(hshd_num)]
    if region:
        filtered_data = filtered_data[filtered_data["STORE_R"] == region]
    if income_group:
        filtered_data = filtered_data[filtered_data["INCOME_RANGE"] == income_group]

    # Calculate KPIs
    total_sales = round(filtered_data["SPEND"].sum(), 2)
    avg_price = round(filtered_data["SPEND"].mean(), 2)
    total_units = int(filtered_data["UNITS"].sum())

    # Generate Charts
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

    spending_trends = px.line(
        filtered_data.groupby(filtered_data["PURCHASE_"].str[:7])["SPEND"].sum().reset_index(),
        x="PURCHASE_", y="SPEND", title="Customer Engagement Over Time"
    )

    # Convert Charts to JSON
    sales_by_division_json = sales_by_division.to_json()
    avg_price_chart_json = avg_price_chart.to_json()
    top_items_chart_json = top_items_chart.to_json()
    spending_trends_json = spending_trends.to_json()

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        total_units=total_units,
        sales_by_division_json=sales_by_division_json,
        avg_price_chart_json=avg_price_chart_json,
        top_items_chart_json=top_items_chart_json,
        spending_trends_json=spending_trends_json,
    )

if __name__ == "__main__":
    app.run(debug=True)