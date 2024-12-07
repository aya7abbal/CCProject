from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

# Initialize Flask app
app = Flask(__name__)

# Load datasets
transactions = pd.read_csv("cleaned_transactions.csv")
households = pd.read_csv("cleaned_households.csv")
products = pd.read_csv("cleaned_products.csv")

# Merge datasets for easier analysis
merged_data = transactions.merge(households, on="HSHD_NUM").merge(products, on="PRODUCT_NUM")

@app.route("/")
def homepage():
    return render_template("dashboard.html", total_sales=0, avg_price=0, total_units=0)

@app.route("/visualization", methods=["POST"])
def visualization():
    hshd_num = request.form.get("household_number")
    if hshd_num:
        try:
            hshd_num = int(hshd_num)
            filtered_data = merged_data[merged_data["HSHD_NUM"] == hshd_num]
        except ValueError:
            return render_template("dashboard.html", error="Invalid Household Number")
    else:
        filtered_data = merged_data

    if filtered_data.empty:
        return render_template("dashboard.html", error="No data found for this Household Number")

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

    top_commodities = px.bar(
        filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index().nlargest(5, "SPEND"),
        x="COMMODITY", y="SPEND", title="Top 5 Selling Commodities", color="COMMODITY"
    )

    pie_chart = px.pie(
        filtered_data, values="SPEND", names="COMMODITY",
        title="Spend Distribution by Commodity"
    )

    histogram = px.histogram(
        filtered_data, x="SPEND", nbins=20,
        title="Distribution of Spend Amounts"
    )

    # Convert charts to JSON
    charts = {
        "sales_by_division": sales_by_division.to_json(),
        "avg_price_chart": avg_price_chart.to_json(),
        "top_commodities": top_commodities.to_json(),
        "pie_chart": pie_chart.to_json(),
        "histogram": histogram.to_json()
    }

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        total_units=total_units,
        charts=charts
    )

if __name__ == "__main__":
    app.run(debug=True)