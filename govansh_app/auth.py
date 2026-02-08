from datetime import datetime
import sqlite3
from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db, init_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    init_db()
    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if len(username) < 3:
            error = "Username must be at least 3 characters."
        elif "@" not in email or "." not in email:
            error = "Enter a valid email address."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            try:
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                        (username, email, generate_password_hash(password), datetime.now().isoformat()),
                    )
                    conn.commit()
                    uid = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()["id"]
                session["user_id"] = uid
                return redirect(url_for("core.index"))
            except sqlite3.IntegrityError:
                error = "Email already registered. Please login."
    return render_template(
        "auth.html",
        title="Sign up",
        subtitle="Create your GOVANSH account",
        button="SIGN UP",
        error=error,
        fields=[
            {"id": "username", "label": "Username", "type": "text", "placeholder": "Your name"},
            {"id": "email", "label": "Email", "type": "email", "placeholder": "name@example.com"},
            {"id": "password", "label": "Password", "type": "password", "placeholder": "Minimum 6 characters"},
        ],
        links='Already have an account? <a href="/login">Login</a>',
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    init_db()
    error = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        with get_db() as conn:
            row = conn.execute(
                "SELECT id, username, password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
        if not row or not check_password_hash(row["password_hash"], password):
            error = "Invalid email or password."
        else:
            session["user_id"] = row["id"]
            return redirect(url_for("core.index"))
    return render_template(
        "auth.html",
        title="Login",
        subtitle="Login to use breed recognition",
        button="LOGIN",
        error=error,
        fields=[
            {"id": "email", "label": "Email", "type": "email", "placeholder": "name@example.com"},
            {"id": "password", "label": "Password", "type": "password", "placeholder": "Your password"},
        ],
        links='New here? <a href="/signup">Create account</a>',
    )


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

