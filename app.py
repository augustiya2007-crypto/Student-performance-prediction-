from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "student_prediction_secret_key"

# Load Model
try:
    model = joblib.load("model/model.pkl")
except:
    model = None

# Database Connection
def get_db():
    conn = sqlite3.connect("student.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create Tables
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        study_hours REAL,
        attendance REAL,
        internal_marks REAL,
        assignment REAL,
        prediction TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# Home
@app.route("/")
def home():
    return render_template("index.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO students(name,email,password) VALUES(?,?,?)",
                (name,email,password)
            )

            conn.commit()
            flash("Registration Successful")
            return redirect("/login")

        except:
            flash("Email already exists")

        finally:
            conn.close()

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Admin Login
        if email == "admin@gmail.com" and password == "admin123":
            session["admin"] = True
            return redirect("/admin_dashboard")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email,password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            session["student_id"] = user["id"]
            session["student_name"] = user["name"]
            return redirect("/dashboard")

        flash("Invalid Email or Password")

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["student_name"]
    )

# ---------------- PREDICT ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    if "student_id" not in session:
        return redirect("/login")

    if model is None:
        flash("Machine Learning model not found.")
        return redirect("/dashboard")

    study = float(request.form["study"])
    attendance = float(request.form["attendance"])
    internal = float(request.form["internal"])
    assignment = float(request.form["assignment"])

    input_data = pd.DataFrame(
        [[study, attendance, internal, assignment]],
        columns=[
            "StudyHours",
            "Attendance",
            "InternalMarks",
            "Assignment"
        ]
    )

    prediction = model.predict(input_data)[0]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions(
            student_id,
            study_hours,
            attendance,
            internal_marks,
            assignment,
            prediction
        )
        VALUES(?,?,?,?,?,?)
    """,
    (
        session["student_id"],
        study,
        attendance,
        internal,
        assignment,
        prediction
    ))

    conn.commit()
    conn.close()

    return render_template(
        "dashboard.html",
        name=session["student_name"],
        result=prediction
    )


# ---------------- HISTORY ---------------- #

@app.route("/history")
def history():

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM predictions
        WHERE student_id=?
        ORDER BY id DESC
    """, (session["student_id"],))

    rows = cur.fetchall()

    conn.close()

    return render_template("history.html", data=rows)


# ---------------- ADMIN DASHBOARD ---------------- #

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    cur.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        predictions=predictions,
        total_students=len(students),
        total_predictions=len(predictions)
    )


# ---------------- DELETE STUDENT ---------------- #

@app.route("/delete_student/<int:id>")
def delete_student(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))
    cur.execute("DELETE FROM predictions WHERE student_id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin_dashboard")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
