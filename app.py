"""
Full Stack Python Developer Interview Assignment — Reference Implementation
============================================================================
Stack: Python 3, Flask, SQLite, HTML5, CSS3, Bootstrap 5, JavaScript

This app implements every backend task from Section D of the assignment:
  Q16 - Simple Flask route (/welcome)
  Q17 - SQLite database connection
  Q18 - SQL SELECT / INSERT / UPDATE queries
  Q19 - CRUD operations (Create, Read, Update, Delete)
  Q20 - REST API endpoint (/api/students)

...and serves the Section C frontend (registration form with Bootstrap 5,
custom CSS, and JavaScript validation) from templates/index.html.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000/
"""

import os
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")


# ---------------------------------------------------------------------------
# Database helpers  (Q17 — Connecting to SQLite)
# ---------------------------------------------------------------------------

def get_db_connection():
    """Open a new SQLite connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the students table if it doesn't exist and seed sample data."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT NOT NULL UNIQUE,
            phone    TEXT NOT NULL,
            password TEXT NOT NULL,
            marks    INTEGER DEFAULT 0
        )
        """
    )
    already_seeded = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if already_seeded == 0:
        sample_students = [
            ("Aditi Sharma", "aditi.sharma@example.com", "9876543210",
             generate_password_hash("password123"), 88),
            ("Rahul Verma", "rahul.verma@example.com", "9876500000",
             generate_password_hash("password123"), 76),
            ("Nandini Rao", "nandini.rao@example.com", "9876511111",
             generate_password_hash("password123"), 92),
        ]
        conn.executemany(
            "INSERT INTO students (name, email, phone, password, marks) "
            "VALUES (?, ?, ?, ?, ?)",
            sample_students,
        )
        conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Frontend routes  (Section C)
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Registration form page (HTML form + CSS + Bootstrap + JS validation)."""
    return render_template("index.html")


@app.route("/students")
def students_page():
    """READ — list every student in a responsive Bootstrap table."""
    conn = get_db_connection()
    students = conn.execute(
        "SELECT id, name, email, phone, marks FROM students ORDER BY id"
    ).fetchall()
    conn.close()
    return render_template("students.html", students=students)


# ---------------------------------------------------------------------------
# Section D — Backend & Database
# ---------------------------------------------------------------------------

@app.route("/welcome")
def welcome():
    """Q16 — Simple Flask route returning a JSON response."""
    return jsonify({"message": "Welcome to Full Stack Development"})


@app.route("/register", methods=["POST"])
def register():
    """
    Q19 (CREATE) — Insert a new student.

    Accepts either a normal HTML form POST (redirects to /students) or a
    JSON/AJAX POST from the registration page's fetch() call (returns JSON),
    so the same endpoint powers both the server-rendered flow and the
    JavaScript-driven "instant card + table" UI described in Q15.
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    password = data.get("password") or ""

    if not (name and email and phone and password):
        if request.is_json:
            return jsonify({"error": "All fields are required."}), 400
        flash("All fields are required.", "danger")
        return redirect(url_for("index"))

    conn = get_db_connection()
    try:
        cur = conn.execute(
            "INSERT INTO students (name, email, phone, password, marks) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, generate_password_hash(password), 0),
        )
        conn.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        message = "A student with this email already exists."
        if request.is_json:
            return jsonify({"error": message}), 409
        flash(message, "danger")
        return redirect(url_for("index"))
    conn.close()

    if request.is_json:
        return jsonify({
            "id": new_id, "name": name, "email": email,
            "phone": phone, "marks": 0,
        }), 201

    flash(f"Student '{name}' registered successfully!", "success")
    return redirect(url_for("students_page"))


@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    """Q19 (UPDATE) — Edit a student's marks."""
    marks = request.form.get("marks", "0")
    conn = get_db_connection()
    conn.execute("UPDATE students SET marks = ? WHERE id = ?", (marks, student_id))
    conn.commit()
    conn.close()
    flash("Student record updated.", "success")
    return redirect(url_for("students_page"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """Q19 (DELETE) — Remove a student record."""
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student record deleted.", "info")
    return redirect(url_for("students_page"))


@app.route("/api/students", methods=["GET"])
def api_students():
    """Q20 — REST API endpoint: all students as a JSON array."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, name, email, phone, marks FROM students ORDER BY id"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/students/top", methods=["GET"])
def api_students_top():
    """Q18 (SELECT example) — students who scored more than 80 marks."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, name, marks FROM students WHERE marks > 80 ORDER BY marks DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
