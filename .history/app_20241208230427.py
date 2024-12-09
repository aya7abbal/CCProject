from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='your-database-host',  # Replace with your Azure MySQL host
        user='azureadmin',         # Replace with your admin username
        password='yourpassword',   # Replace with your admin password
        database='RetailDB'        # Replace with your database name
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Save data to database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, password, email),
        )
        connection.commit()
        cursor.close()
        connection.close()

        return f"Hello, {username}! Your email is {email}."

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)