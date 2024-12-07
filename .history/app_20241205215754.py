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

    pie_chart = px.pie(
        filtered_data.groupby("COMMODITY")["SPEND"].sum().reset_index(),
        values="SPEND", names="COMMODITY", title="Spend Distribution by Commodity"
    )
    pie_chart.update_layout(
        autosize=False,
        width=800,  # Adjust width
        height=600,  # Adjust height
        margin=dict(l=40, r=40, t=80, b=40),  # Adjust margins
        title=dict(
            font=dict(size=20)  # Increase title font size
        ),
        legend=dict(
            font=dict(size=12)  # Adjust legend font size
        )
    )

    histogram = px.histogram(
        filtered_data, x="SPEND", nbins=20, title="Distribution of Spend Amounts"
    )

    # Convert charts to JSON for rendering
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