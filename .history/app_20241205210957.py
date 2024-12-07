from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load cleaned datasets
transactions = pd.read_csv("cleaned_transactions.csv")
households = pd.read_csv("cleaned_households.csv")
products = pd.read_csv("cleaned_products.csv")

# Convert date column to datetime
transactions["PURCHASE_"] = pd.to_datetime(transactions["PURCHASE_"])

@app.route("/")
def homepage():
    return render_template("dashboard.html")

@app.route("/filtered_data", methods=["POST"])
def get_filtered_data():
    filters = request.get_json()
    start_date = filters.get("start_date", None)
    end_date = filters.get("end_date", None)
    store_region = filters.get("store_region", "all")
    product_category = filters.get("product_category", "all")

    filtered_data = transactions.copy()

    # Apply filters
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data["PURCHASE_"] >= start_date) & (filtered_data["PURCHASE_"] <= end_date)
        ]
    if store_region != "all":
        filtered_data = filtered_data[filtered_data["STORE_R"] == store_region]
    if product_category != "all":
        filtered_data = filtered_data[
            filtered_data["COMMODITY"] == product_category
        ]

    # Aggregate data
    total_sales = round(filtered_data["SPEND"].sum(), 2)
    total_units = filtered_data["UNITS"].sum()
    average_price = round(total_sales / total_units, 2) if total_units > 0 else 0

    return jsonify({
        "total_sales": total_sales,
        "average_price": average_price,
        "total_units": total_units,
    })

@app.route("/additional_metrics", methods=["GET"])
def additional_metrics():
    unique_customers = transactions["HSHD_NUM"].nunique()
    retention_rate = round((unique_customers / len(households)) * 100, 2)
    average_revenue_per_customer = round(transactions["SPEND"].sum() / unique_customers, 2)

    return jsonify({
        "retention_rate": f"{retention_rate}%",
        "average_revenue_per_customer": f"${average_revenue_per_customer}"
    })

@app.route("/visualization")
def visualization():
    # Sample visualization using Plotly
    sales_by_division = transactions.groupby("STORE_R")["SPEND"].sum().reset_index()
    fig = px.bar(sales_by_division, x="STORE_R", y="SPEND", title="Sales by Division")

    top_commodities = transactions.groupby("COMMODITY")["SPEND"].sum().reset_index().sort_values(by="SPEND", ascending=False).head(5)
    fig_commodities = px.bar(top_commodities, x="COMMODITY", y="SPEND", title="Top 5 Selling Commodities")

    fig_json = pio.to_html(fig, full_html=False)
    fig_commodities_json = pio.to_html(fig_commodities, full_html=False)

    return render_template("visualization.html", bar_chart=fig_json, top_commodities_chart=fig_commodities_json)

if __name__ == "__main__":
    app.run(debug=True)