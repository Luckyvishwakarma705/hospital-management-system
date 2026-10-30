import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("HOSPITAL_SECRET_KEY", "dev-only-change-this-secret")
DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access your account.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/")
def home():
    return render_template("home.html", page="home")

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/services")
def services():
    service_list = [
        ("heart-pulse", "Cardiology", "Heart health assessments and specialist consultations."),
        ("stethoscope", "General Medicine", "Everyday care, prevention and treatment guidance."),
        ("activity", "Diagnostics", "Reliable diagnostic services to support clinical teams."),
        ("users", "Patient Support", "Friendly help with appointments and hospital information.")
    ]
    return render_template("services.html", page="services", services=service_list)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        if not all([name, email, subject, message]):
            flash("Please complete every field.", "error")
        else:
            with get_db() as db:
                db.execute(
                    "INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)",
                    (name, email, subject, message)
                )
            flash("Your message has been saved. Our demo team will review it.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html", page="contact")

@app.route("/help")
def help_page():
    return render_template("help.html", page="help")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back, " + user["name"] + "!", "success")
            return redirect(url_for("account"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html", page="login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter your name and email, and use a password of at least 8 characters.", "error")
        else:
            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO users (name,email,password_hash) VALUES (?,?,?)",
                        (name, email, generate_password_hash(password))
                    )
                flash("Account created. You can now log in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An account with that email already exists.", "error")
    return render_template("register.html", page="register")

@app.route("/account")
@login_required
def account():
    return render_template("account.html", page="account")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

init_db()

if __name__ == "__main__":
    app.run(debug=True)
