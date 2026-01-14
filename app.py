from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    vitals = {}

    if request.method == 'POST':
        vitals = {
            "heart_rate": request.form.get("heart_rate"),
            "bp": request.form.get("bp"),
            "sugar": request.form.get("sugar"),
            "oxygen": request.form.get("oxygen"),
            "temperature": request.form.get("temperature"),
        }

    return render_template('dashboard.html', vitals=vitals)

if __name__ == '__main__':
    app.run(debug=True)
