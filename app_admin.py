from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.health_monitor
members_col = db.members

@app.route('/')
def index():
    return render_template("admin/index.html")

@app.route('/dashboard')
def dashboard():
    members = list(members_col.find())
    return render_template("admin/dashboard.html", members=members)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
