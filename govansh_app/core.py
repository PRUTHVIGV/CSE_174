from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
import cv2
import numpy as np
from PIL import Image

from .breeds import BREED_DATABASE
from .db import init_db, record_prediction, user_history, stats as stats_fn, get_db
from .recognition.heuristic_recognizer import HeuristicRecognizer


core_bp = Blueprint("core", __name__)
recognizer = HeuristicRecognizer()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    with get_db() as conn:
        row = conn.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (uid,)).fetchone()
        return dict(row) if row else None


def login_required_json(fn):
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Login required"}), 401
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


@core_bp.route("/")
def index():
    return render_template("index.html")


@core_bp.route("/predict", methods=["POST"])
@login_required_json
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "No image selected"}), 400

    image = Image.open(file.stream)
    image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    result = recognizer.predict_breed(image_np)
    record_prediction(session["user_id"], result)
    return jsonify(result)


@core_bp.route("/api/me")
def api_me():
    u = current_user()
    if not u:
        return jsonify({"authenticated": False})
    return jsonify({"authenticated": True, "username": u.get("username", ""), "email": u.get("email", "")})


@core_bp.route("/api/breeds")
def api_breeds():
    breeds_list = []
    for name, info in BREED_DATABASE.items():
        breeds_list.append(
            {"name": name, "hindi_name": info.get("hindi_name", ""), "type": info.get("type", ""), "state": info.get("state", "")}
        )
    return jsonify({"breeds": breeds_list, "total": len(BREED_DATABASE)})


@core_bp.route("/api/breed/<name>")
def api_breed(name):
    info = BREED_DATABASE.get(name)
    if not info:
        return jsonify({"error": "Breed not found"}), 404
    return jsonify({"breed": name, "info": info})


@core_bp.route("/api/history")
def api_history():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"history": []})
    return jsonify({"history": user_history(uid, limit=10)})


@core_bp.route("/api/stats")
def api_stats():
    return jsonify(stats_fn(session.get("user_id")))


@core_bp.route("/api/compare/<breed1>/<breed2>")
def api_compare(breed1, breed2):
    b1 = breed1.replace("_", " ")
    b2 = breed2.replace("_", " ")
    info1 = BREED_DATABASE.get(b1)
    info2 = BREED_DATABASE.get(b2)
    if not info1 or not info2:
        return jsonify({"error": "Breed not found"}), 404
    return jsonify({"breed1": {"name": b1, "info": info1}, "breed2": {"name": b2, "info": info2}})


@core_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")


@core_bp.route("/explore")
def explore():
    return render_template("explore.html", breeds=BREED_DATABASE)


@core_bp.route("/compare")
def compare():
    return render_template("compare.html", breed_names=list(BREED_DATABASE.keys()))


def init_app():
    init_db()

