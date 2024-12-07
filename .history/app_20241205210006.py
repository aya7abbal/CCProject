from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load cleaned datasets
transactions = pd.read_csv("cleaned_transactions.csv")
products = pd.read_csv("cleaned_products.csv")
households = pd.read_csv("cleaned_households.csv")

# Function to generate Plotly chart
def generate_chart(dataframe, x_column, y_column, title):
    fig = px.bar(dataframe, x=x_column, y=y_column, title=title, text_auto=True)
    fig.update_layout(template="plotly_white", xaxis_title=x_column, yaxis_title=y_column)
    return fig.to_html(full_html=False)

@app.route('/')
def homepage():
    return render_template("dashboard.html")

@app.route('/fetch', methods=['POST'])
def fetch_data():
    household_num = request.form.get('household_number')
    if household_num:
        try:
            # Filter data
            household_num = int(household_num)
            transactions_data = transactions[transactions['HSHD_NUM'] == household_num]
            detailed_data = pd.merge(
                transactions_data,
                products,
                on="PRODUCT_NUM",
                how="left"
            ).sort_values(by=["HSHD_NUM", "BASKET_NUM", "PURCHASE_", "PRODUCT_NUM"])

            # Spending over time chart
            transactions_data['PURCHASE_'] = pd.to_datetime(transactions_data['PURCHASE_'])
            spending_chart = generate_chart(
                transactions_data.groupby('PURCHASE_')['SPEND'].sum().reset_index(),
                x_column='PURCHASE_',
                y_column='SPEND',
                title=f"Spending Over Time for Household {household_num}"
            )

            # Top departments chart
            top_departments_chart = generate_chart(
                detailed_data.groupby('DEPARTMENT')['SPEND'].sum().reset_index(),
                x_column='DEPARTMENT',
                y_column='SPEND',
                title=f"Top Departments by Spending for Household {household_num}"
            )

            # Brand preferences pie chart
            brand_pie_chart = generate_chart(
                detailed_data.groupby('BRAND_TY')['SPEND'].sum().reset_index(),
                x_column='BRAND_TY',
                y_column='SPEND',
                title=f"Brand Preferences for Household {household_num}"
            )

            # Render HTML
            detailed_data_html = detailed_data.to_html(classes='table table-striped', index=False)
            return render_template(
                "dashboard.html",
                detailed_data=detailed_data_html,
                spending_chart=spending_chart,
                top_departments_chart=top_departments_chart,
                brand_pie_chart=brand_pie_chart,
                household_num=household_num
            )
        except Exception as e:
            return render_template("dashboard.html", error=f"Error processing household number: {e}")
    else:
        return render_template("dashboard.html", error="Please enter a valid Household Number.")

if __name__ == '__main__':
    app.run(debug=True)