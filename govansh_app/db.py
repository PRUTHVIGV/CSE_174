import sqlite3
from datetime import datetime
from .config import USERS_DB_PATH


def get_db():
    conn = sqlite3.connect(USERS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize SQLite tables (users + predictions)."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                prediction_id TEXT NOT NULL,
                breed TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL,
                model_version TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        conn.commit()


def record_prediction(user_id: int, result: dict):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO predictions (user_id, prediction_id, breed, confidence, created_at, model_version) VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_id,
                result.get("prediction_id", ""),
                result.get("breed", ""),
                float(result.get("confidence", 0.0)),
                result.get("timestamp", datetime.now().isoformat()),
                result.get("model_version", "GOVANSH"),
            ),
        )
        conn.commit()


def user_history(user_id: int, limit: int = 10):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT prediction_id, breed, confidence, created_at FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [
        {
            "prediction_id": r["prediction_id"],
            "breed": r["breed"],
            "confidence": float(r["confidence"]),
            "timestamp": r["created_at"],
        }
        for r in rows
    ]


def stats(user_id: int | None):
    init_db()
    with get_db() as conn:
        total_users = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
        total_predictions = conn.execute("SELECT COUNT(*) AS c FROM predictions").fetchone()["c"]
        top = conn.execute(
            "SELECT breed, COUNT(*) AS c FROM predictions GROUP BY breed ORDER BY c DESC LIMIT 5"
        ).fetchall()
        my_predictions = 0
        if user_id:
            my_predictions = conn.execute(
                "SELECT COUNT(*) AS c FROM predictions WHERE user_id = ?",
                (user_id,),
            ).fetchone()["c"]
    return {
        "total_users": int(total_users),
        "total_predictions": int(total_predictions),
        "top_breeds": [{"breed": r["breed"], "count": int(r["c"])} for r in top],
        "my_predictions": int(my_predictions),
    }

