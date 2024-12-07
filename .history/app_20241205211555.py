from flask import Flask, render_template, request, jsonify, redirect, url_for
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
def login():
    return render_template("login.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    return render_template("dashboard.html", username=username, email=email)


@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    hshd_num = request.json.get("hshd_num", None)
    filtered_data = transactions[transactions["HSHD_NUM"] == int(hshd_num)] if hshd_num else transactions

    total_sales = round(filtered_data["SPEND"].sum(), 2)
    total_units = filtered_data["UNITS"].sum()
    average_price = round(total_sales / total_units, 2) if total_units > 0 else 0

    return jsonify({
        "total_sales": total_sales,
        "average_price": average_price,
        "total_units": total_units,
    })


@app.route("/data_loading", methods=["GET", "POST"])
def data_loading():
    if request.method == "POST":
        transactions_file = request.files["transactions_file"]
        households_file = request.files["households_file"]
        products_file = request.files["products_file"]

        if transactions_file:
            transactions_file.save("cleaned_transactions.csv")
        if households_file:
            households_file.save("cleaned_households.csv")
        if products_file:
            products_file.save("cleaned_products.csv")

        return "Datasets uploaded successfully!"
    return render_template("data_loading.html")


@app.route("/visualization")
def visualization():
    sales_by_division = transactions.groupby("STORE_R")["SPEND"].sum().reset_index()
    fig = px.bar(sales_by_division, x="STORE_R", y="SPEND", title="Sales by Division")

    top_commodities = transactions.groupby("COMMODITY")["SPEND"].sum().reset_index().sort_values(by="SPEND", ascending=False).head(5)
    fig_commodities = px.bar(top_commodities, x="COMMODITY", y="SPEND", title="Top 5 Selling Commodities")

    fig_json = pio.to_html(fig, full_html=False)
    fig_commodities_json = pio.to_html(fig_commodities, full_html=False)

    return render_template("visualization.html", bar_chart=fig_json, top_commodities_chart=fig_commodities_json)


if __name__ == "__main__":
    app.run(debug=True)