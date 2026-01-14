from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB connection
client = MongoClient("mongodb+srv://terminator:1234567890@cluster0.kdcjwdl.mongodb.net/?appName=Cluster0")
db = client.health_monitor
members_col = db.members

# Home page
@app.route('/')
def index():
    return render_template("member/index.html")

# Member registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        member = {
            "name": request.form['name'],
            "blood_type": request.form['blood_type'],
            "address": request.form['address'],
            "area": request.form['area'],
            "health_records": []
        }
        members_col.insert_one(member)
        return redirect(url_for('dashboard', member_name=member['name']))
    return render_template("member/register.html")

# Function to evaluate body condition automatically
def evaluate_condition(vitals):
    conditions = []
    try:
        systolic = int(vitals["blood_pressure"].split('/')[0])
        diastolic = int(vitals["blood_pressure"].split('/')[1])
    except:
        systolic = diastolic = 0

    if systolic > 140 or diastolic > 90:
        conditions.append("High Blood Pressure")
    if vitals["blood_sugar"] > 140:
        conditions.append("High Blood Sugar")
    if vitals["oxygen"] < 95:
        conditions.append("Low Oxygen Level")
    if vitals["temperature"] > 100.4:
        conditions.append("Fever")
    if not conditions:
        conditions.append("Healthy / Normal")

    return conditions

# Member dashboard
@app.route('/dashboard/<member_name>', methods=['GET', 'POST'])
def dashboard(member_name):
    member = members_col.find_one({"name": member_name})

    if request.method == 'POST':
        # Collect vitals from the form
        vitals = {
            "heart_rate": int(request.form['heart_rate']),
            "blood_pressure": request.form['blood_pressure'],
            "blood_sugar": float(request.form['blood_sugar']),
            "oxygen": float(request.form['oxygen']),
            "temperature": float(request.form['temperature']),
            "timestamp": datetime.now()
        }

        # Evaluate body condition automatically
        condition = evaluate_condition(vitals)

        # Store new vitals and condition in database
        members_col.update_one(
            {"name": member_name},
            {"$push": {"health_records": {"vitals": vitals, "condition": condition}}}
        )

        # Refresh member data
        member = members_col.find_one({"name": member_name})

    # Get latest condition to display
    latest_condition = member['health_records'][-1]['condition'] if member['health_records'] else ["No data yet"]

    return render_template("member/dashboard.html", member=member, latest_condition=latest_condition)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
