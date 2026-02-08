import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)

# Database
USERS_DB_PATH = os.path.join(PROJECT_DIR, "govansh_users.db")

# Flask
SECRET_KEY = os.environ.get("GOVANSH_SECRET_KEY", "govansh-dev-secret-key-change-me")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

