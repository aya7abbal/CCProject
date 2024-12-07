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






<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail KPI Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.25.2/plotly.min.js"></script>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Retail KPI Dashboard</h1>
        <form method="POST" action="/visualization" class="mb-4">
            <div class="row">
                <div class="col-md-6">
                    <label for="household_number" class="form-label">Household Number:</label>
                    <input type="text" name="household_number" id="household_number" class="form-control" placeholder="e.g., 10" value="{{ request.form.get('household_number') }}">
                </div>
                <div class="col-md-6">
                    <label for="store_region" class="form-label">Store Region:</label>
                    <select name="store_region" id="store_region" class="form-control">
                        <option value="">All Regions</option>
                        <option value="EAST" {% if request.form.get('store_region') == 'EAST' %}selected{% endif %}>East</option>
                        <option value="WEST" {% if request.form.get('store_region') == 'WEST' %}selected{% endif %}>West</option>
                        <option value="NORTH" {% if request.form.get('store_region') == 'NORTH' %}selected{% endif %}>North</option>
                        <option value="SOUTH" {% if request.form.get('store_region') == 'SOUTH' %}selected{% endif %}>South</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Apply Filters</button>
        </form>

        <!-- KPI Section -->
        <div class="row text-center">
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>Total Sales</h5>
                    <h3>${{ total_sales }}</h3>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>Average Price</h5>
                    <h3>${{ avg_price }}</h3>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>Total Units Sold</h5>
                    <h3>{{ total_units }}</h3>
                </div>
            </div>
        </div>

        <!-- Visualization Section -->
        <div class="row mt-5">
            <div class="col-md-6">
                <div id="sales-by-division"></div>
            </div>
            <div class="col-md-6">
                <div id="avg-price-chart"></div>
            </div>
        </div>
        <div class="row mt-5">
            <div class="col-md-6">
                <div id="top-items-chart"></div>
            </div>
            <div class="col-md-6">
                <div id="spending-trends"></div>
            </div>
        </div>
    </div>

    <script>
        // Render Sales by Division Chart
        var salesByDivisionData = {{ sales_by_division_json | safe }};
        Plotly.newPlot('sales-by-division', salesByDivisionData.data, salesByDivisionData.layout);

        // Render Average Price Chart
        var avgPriceData = {{ avg_price_chart_json | safe }};
        Plotly.newPlot('avg-price-chart', avgPriceData.data, avgPriceData.layout);

        // Render Top Items Chart
        var topItemsData = {{ top_items_chart_json | safe }};
        Plotly.newPlot('top-items-chart', topItemsData.data, topItemsData.layout);

        // Render Customer Engagement Over Time Chart
        var spendingTrendsData = {{ spending_trends_json | safe }};
        Plotly.newPlot('spending-trends', spendingTrendsData.data, spendingTrendsData.layout);
    </script>
</body>
</html>