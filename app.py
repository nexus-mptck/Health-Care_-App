from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("database.db")

# Create table
with get_db() as db:
    db.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        blood TEXT,
        address TEXT,
        area TEXT,
        family TEXT,
        heart_rate INTEGER,
        bp TEXT,
        sugar INTEGER,
        oxygen INTEGER,
        temperature REAL,
        organ_problem TEXT,
        condition TEXT,
        disease TEXT
    )
    """)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        db = get_db()

        # AI-like disease matching (rule-based)
        disease = detect_disease(
            int(data['heart_rate']),
            int(data['sugar']),
            int(data['oxygen']),
            float(data['temperature']),
            data['organ_problem']
        )

        condition = "Normal"
        if disease != "No major disease detected":
            condition = "Needs Attention"

        db.execute("""
            INSERT INTO patients 
            (name, blood, address, area, family, heart_rate, bp, sugar, oxygen, temperature, organ_problem, condition, disease)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data['name'], data['blood'], data['address'], data['area'], data['family'],
            data['heart_rate'], data['bp'], data['sugar'], data['oxygen'],
            data['temperature'], data['organ_problem'], condition, disease
        ))
        db.commit()

        return render_template('result.html', disease=disease, condition=condition)

    return render_template('register.html')

# Simple AI Disease Detection
def detect_disease(hr, sugar, oxygen, temp, organ):
    if sugar > 180:
        return "Diabetes Risk"
    if oxygen < 92:
        return "Respiratory Issue"
    if hr > 110:
        return "Heart Condition Risk"
    if temp > 38:
        return "Possible Infection"
    if "lung" in organ.lower():
        return "Possible Lung Disease"
    if "kidney" in organ.lower():
        return "Kidney-related Disorder"
    return "No major disease detected"

if __name__ == '__main__':
    app.run(debug=True)
