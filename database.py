"""SQLite database layer - replaces all JSON files"""
import sqlite3
import os
from datetime import datetime

DB_FILE = 'cattle.db'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            email       TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            password    TEXT NOT NULL,
            avatar      TEXT,
            created_at  TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            breed       TEXT NOT NULL,
            confidence  REAL NOT NULL,
            image       TEXT,
            timestamp   TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS favorites (
            user_email  TEXT NOT NULL,
            breed       TEXT NOT NULL,
            PRIMARY KEY (user_email, breed)
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            predicted   TEXT,
            correct     INTEGER,
            actual      TEXT,
            timestamp   TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS search_log (
            breed       TEXT PRIMARY KEY,
            count       INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS shares (
            share_id    TEXT PRIMARY KEY,
            breed       TEXT,
            confidence  REAL,
            info        TEXT,
            user_name   TEXT,
            timestamp   TEXT
        );
        CREATE TABLE IF NOT EXISTS suggestions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            category    TEXT,
            title       TEXT,
            description TEXT,
            priority    TEXT,
            timestamp   TEXT
        );
    ''')
    conn.commit()
    conn.close()
    _migrate_json()

def _migrate_json():
    """One-time migration from JSON files to SQLite"""
    import json, hashlib

    # Users
    if os.path.exists('users.json') and not os.path.exists('.migrated'):
        conn = get_db()
        try:
            with open('users.json') as f:
                users = json.load(f)
            for email, u in users.items():
                conn.execute('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)',
                    (email, u.get('name',''), u.get('password',''), u.get('avatar'), u.get('created_at', datetime.now().isoformat())))
        except: pass

        # History
        if os.path.exists('prediction_history.json'):
            try:
                with open('prediction_history.json') as f:
                    hist = json.load(f)
                for email, preds in hist.items():
                    for p in preds:
                        conn.execute('INSERT INTO history (user_email,breed,confidence,image,timestamp) VALUES (?,?,?,?,?)',
                            (email, p['breed'], p['confidence'], p.get('image',''), p['timestamp']))
            except: pass

        # Favorites
        if os.path.exists('favorites.json'):
            try:
                with open('favorites.json') as f:
                    favs = json.load(f)
                for email, breeds in favs.items():
                    for b in breeds:
                        conn.execute('INSERT OR IGNORE INTO favorites VALUES (?,?)', (email, b))
            except: pass

        conn.commit()
        conn.close()
        open('.migrated', 'w').close()

# ── Users ──────────────────────────────────────────────
def load_users():
    conn = get_db()
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return {r['email']: dict(r) for r in rows}

def save_user(email, name, password, created_at=None):
    conn = get_db()
    conn.execute('INSERT OR REPLACE INTO users (email,name,password,created_at) VALUES (?,?,?,?)',
        (email, name, password, created_at or datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_user(email):
    conn = get_db()
    row = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_avatar(email, filename):
    conn = get_db()
    conn.execute('UPDATE users SET avatar=? WHERE email=?', (filename, email))
    conn.commit(); conn.close()

def update_user_password(email, hashed):
    conn = get_db()
    conn.execute('UPDATE users SET password=? WHERE email=?', (hashed, email))
    conn.commit(); conn.close()

def delete_user(email):
    conn = get_db()
    conn.execute('DELETE FROM users WHERE email=?', (email,))
    conn.commit(); conn.close()

# ── History ────────────────────────────────────────────
def add_prediction(user_email, breed, confidence, image_name):
    conn = get_db()
    conn.execute('INSERT INTO history (user_email,breed,confidence,image,timestamp) VALUES (?,?,?,?,?)',
        (user_email, breed, round(confidence, 2), image_name, datetime.now().isoformat()))
    # Keep only last 50
    conn.execute('''DELETE FROM history WHERE user_email=? AND id NOT IN
        (SELECT id FROM history WHERE user_email=? ORDER BY id DESC LIMIT 50)''',
        (user_email, user_email))
    conn.commit(); conn.close()

def get_user_history(user_email):
    conn = get_db()
    rows = conn.execute('SELECT * FROM history WHERE user_email=? ORDER BY id ASC', (user_email,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def clear_user_history(user_email):
    conn = get_db()
    conn.execute('DELETE FROM history WHERE user_email=?', (user_email,))
    conn.commit(); conn.close()

def get_all_history():
    conn = get_db()
    rows = conn.execute('SELECT * FROM history').fetchall()
    conn.close()
    result = {}
    for r in rows:
        result.setdefault(r['user_email'], []).append(dict(r))
    return result

# ── Favorites ──────────────────────────────────────────
def add_favorite(user_email, breed):
    conn = get_db()
    conn.execute('INSERT OR IGNORE INTO favorites VALUES (?,?)', (user_email, breed))
    conn.commit(); conn.close()

def remove_favorite(user_email, breed):
    conn = get_db()
    conn.execute('DELETE FROM favorites WHERE user_email=? AND breed=?', (user_email, breed))
    conn.commit(); conn.close()

def get_user_favorites(user_email):
    conn = get_db()
    rows = conn.execute('SELECT breed FROM favorites WHERE user_email=?', (user_email,)).fetchall()
    conn.close()
    return [r['breed'] for r in rows]

def is_favorite(user_email, breed):
    conn = get_db()
    row = conn.execute('SELECT 1 FROM favorites WHERE user_email=? AND breed=?', (user_email, breed)).fetchone()
    conn.close()
    return row is not None

# ── Feedback ───────────────────────────────────────────
def add_feedback(user_email, predicted, correct, actual=''):
    conn = get_db()
    conn.execute('INSERT INTO feedback (user_email,predicted,correct,actual,timestamp) VALUES (?,?,?,?,?)',
        (user_email, predicted, 1 if correct else 0, actual, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_user_feedback(user_email):
    conn = get_db()
    rows = conn.execute('SELECT * FROM feedback WHERE user_email=?', (user_email,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_feedback():
    conn = get_db()
    rows = conn.execute('SELECT * FROM feedback ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── Search log ─────────────────────────────────────────
def log_search(breed):
    conn = get_db()
    conn.execute('INSERT INTO search_log (breed,count) VALUES (?,1) ON CONFLICT(breed) DO UPDATE SET count=count+1', (breed,))
    conn.commit(); conn.close()

def get_search_counts(limit=8):
    conn = get_db()
    rows = conn.execute('SELECT breed, count FROM search_log ORDER BY count DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return {r['breed']: r['count'] for r in rows}

# ── Shares ─────────────────────────────────────────────
def save_share(share_id, breed, confidence, info_json, user_name):
    conn = get_db()
    conn.execute('INSERT OR REPLACE INTO shares VALUES (?,?,?,?,?,?)',
        (share_id, breed, confidence, info_json, user_name, datetime.now().strftime('%Y-%m-%d %H:%M')))
    conn.commit(); conn.close()

def get_share(share_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM shares WHERE share_id=?', (share_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# ── Suggestions ────────────────────────────────────────
def save_suggestion(name, category, title, description, priority):
    conn = get_db()
    conn.execute('INSERT INTO suggestions (name,category,title,description,priority,timestamp) VALUES (?,?,?,?,?,?)',
        (name, category, title, description, priority, datetime.now().strftime('%Y-%m-%d %H:%M')))
    conn.commit(); conn.close()
