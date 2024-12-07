from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

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
    # Handle Filters
    hshd_num = request.form.get("household_number", None)
    start_date = request.form.get("start_date", None)
    end_date = request.form.get("end_date", None)
    region = request.form.get("store_region", None)

    filtered_data = merged_data

    if hshd_num:
        filtered_data = filtered_data[filtered_data["HSHD_NUM"] == int(hshd_num)]
    if start_date and end_date:
        filtered_data = filtered_data[(filtered_data["PURCHASE_"] >= start_date) & (filtered_data["PURCHASE_"] <= end_date)]
    if region:
        filtered_data = filtered_data[filtered_data["STORE_R"] == region]

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

    pie_chart = px.pie(
        filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index(),
        values="SPEND", names="COMMODITY", title="Spend Distribution by Commodity"
    )
    pie_chart.update_layout(
        height=500,  # Set the height of the chart
        width=600,   # Set the width of the chart
        margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins to prevent compression
    )

    histogram = px.histogram(
        filtered_data, x="SPEND", nbins=20, title="Distribution of Spend Amounts"
    )

    # Convert Charts to JSON
    sales_by_division_json = sales_by_division.to_json()
    avg_price_chart_json = avg_price_chart.to_json()
    top_items_chart_json = top_items_chart.to_json()
    pie_chart_json = pie_chart.to_json()
    histogram_json = histogram.to_json()

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        total_units=total_units,
        sales_by_division_json=sales_by_division_json,
        avg_price_chart_json=avg_price_chart_json,
        top_items_chart_json=top_items_chart_json,
        pie_chart_json=pie_chart_json,
        histogram_json=histogram_json,
    )

if __name__ == "__main__":
    app.run(debug=True)