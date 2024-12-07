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
    region = request.form.get("store_region", None)

    filtered_data = merged_data

    if hshd_num:
        filtered_data = filtered_data[filtered_data["HSHD_NUM"] == int(hshd_num)]
    if region:
        filtered_data = filtered_data[filtered_data["STORE_R"] == region]

    # KPIs
    total_sales = round(filtered_data["SPEND"].sum(), 2)
    avg_price = round(filtered_data["SPEND"].mean(), 2)
    total_units = int(filtered_data["UNITS"].sum())

    # Visualizations
    sales_by_month = px.line(
        filtered_data.groupby(filtered_data["PURCHASE_"].str[:7])["SPEND"].sum().reset_index(),
        x="PURCHASE_", y="SPEND", title="Spending Trends Over Time"
    )

    loyalty_impact = px.bar(
        filtered_data.groupby("L")["SPEND"].sum().reset_index(),
        x="L", y="SPEND", title="Loyalty Program Impact", color="L"
    )

    basket_analysis = px.bar(
        filtered_data.groupby("COMMODITY")["SPEND"].sum().nlargest(5).reset_index(),
        x="COMMODITY", y="SPEND", title="Top 5 Product Combinations"
    )

    churn_trends = px.line(
        filtered_data.groupby("HSHD_NUM")["SPEND"].sum().reset_index(),
        x="HSHD_NUM", y="SPEND", title="Customer Spending Trends (Potential Churn)"
    )

    region_preference = px.pie(
        filtered_data.groupby("STORE_R")["SPEND"].sum().reset_index(),
        values="SPEND", names="STORE_R", title="Regional Spending Preferences"
    )

    # Convert Charts to JSON
    sales_by_month_json = sales_by_month.to_json()
    loyalty_impact_json = loyalty_impact.to_json()
    basket_analysis_json = basket_analysis.to_json()
    churn_trends_json = churn_trends.to_json()
    region_preference_json = region_preference.to_json()

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        avg_price=avg_price,
        total_units=total_units,
        sales_by_month_json=sales_by_month_json,
        loyalty_impact_json=loyalty_impact_json,
        basket_analysis_json=basket_analysis_json,
        churn_trends_json=churn_trends_json,
        region_preference_json=region_preference_json,
    )

if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, render_template, request
# import pandas as pd
# import plotly.express as px

# # Initialize Flask
# app = Flask(__name__)

# # Load datasets
# transactions = pd.read_csv("cleaned_transactions.csv")
# households = pd.read_csv("cleaned_households.csv")
# products = pd.read_csv("cleaned_products.csv")

# # Merge datasets for easier analysis
# merged_data = transactions.merge(households, on="HSHD_NUM").merge(products, on="PRODUCT_NUM")

# @app.route("/")
# def homepage():
#     return render_template("dashboard.html")

# @app.route("/visualization", methods=["GET", "POST"])
# def visualization():
#     # Handle Filters
#     hshd_num = request.form.get("household_number", None)
#     region = request.form.get("store_region", None)

#     filtered_data = merged_data

#     if hshd_num:
#         filtered_data = filtered_data[filtered_data["HSHD_NUM"] == int(hshd_num)]
#     if region:
#         filtered_data = filtered_data[filtered_data["STORE_R"] == region]

#     # Calculate KPIs
#     total_sales = round(filtered_data["SPEND"].sum(), 2)
#     avg_price = round(filtered_data["SPEND"].mean(), 2)
#     total_units = int(filtered_data["UNITS"].sum())

#     # Generate Charts
#     sales_by_division = px.bar(
#         filtered_data.groupby("STORE_R")["SPEND"].sum().reset_index(),
#         x="STORE_R", y="SPEND", title="Sales by Division", color="STORE_R"
#     )

#     avg_price_chart = px.line(
#         filtered_data.groupby("PURCHASE_")["SPEND"].mean().reset_index(),
#         x="PURCHASE_", y="SPEND", title="Average Price per Date"
#     )

#     top_items_chart = px.bar(
#         filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index().nlargest(5, "SPEND"),
#         x="COMMODITY", y="SPEND", title="Top 5 Selling Commodities", color="COMMODITY"
#     )

#     pie_chart = px.pie(
#         filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index(),
#         values="SPEND", names="COMMODITY", title="Spend Distribution by Commodity"
#     )
#     pie_chart.update_traces(
#         textinfo='percent',  # Show only the label and percent inside the chart
#         textposition='inside'  # Place all text inside the pie
#     )
#     pie_chart.update_layout(
#         height=500,  # Set the height of the chart
#         width=600,   # Set the width of the chart
#         margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins to prevent compression
#     )

#     histogram = px.histogram(
#         filtered_data,
#         x="SPEND",
#         nbins=20,
#         title="Distribution of Spend Amounts",
#         color_discrete_sequence=["#636EFA"],  # Clean and consistent color
#         template="plotly_white",  # Use a clean template
#         labels={"SPEND": "Spend Amount ($)", "count": "Frequency"}  # Better axis labels
#     )
#     histogram.update_layout(
#         height=400,  # Compact height
#         margin=dict(l=40, r=40, t=50, b=40),  # Adjust margins
#         title={
#             "text": "Distribution of Spend Amounts",
#             "x": 0.5,  # Center the title
#             "xanchor": "center",
#         },
#         xaxis=dict(
#             title="Spend Amount ($)",
#             tickangle=0,
#             gridcolor="lightgray",
#         ),
#         yaxis=dict(
#             title="Frequency",
#             gridcolor="lightgray",
#         ),
#     )
#     histogram.update_traces(
#         opacity=0.8,  # Add slight transparency
#     )

#     # Convert Charts to JSON
#     sales_by_division_json = sales_by_division.to_json()
#     avg_price_chart_json = avg_price_chart.to_json()
#     top_items_chart_json = top_items_chart.to_json()
#     pie_chart_json = pie_chart.to_json()
#     histogram_json = histogram.to_json()

#     return render_template(
#         "dashboard.html",
#         total_sales=total_sales,
#         avg_price=avg_price,
#         total_units=total_units,
#         sales_by_division_json=sales_by_division_json,
#         avg_price_chart_json=avg_price_chart_json,
#         top_items_chart_json=top_items_chart_json,
#         pie_chart_json=pie_chart_json,
#         histogram_json=histogram_json,
#     )

# if __name__ == "__main__":
#     app.run(debug=True)