from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        return f"Hello, {username}! Your email is {email}."

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)