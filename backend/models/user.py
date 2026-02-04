import sqlite3

DB_PATH = "data/database.db"


class User:
    def __init__(self, user_id, username, role, password="test123", marks=0):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.password = password  # 🔴 Weak: plain text
        self.marks = marks

    def to_dict(self):
        """
        🔴 Includes only non-sensitive info
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "marks": self.marks
        }


# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    return sqlite3.connect(DB_PATH)


# ==============================
# VULNERABLE USER LOOKUP
# SQL Injection Demo
# ==============================
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()

    # 🔴 Direct string interpolation
    query = f"""
        SELECT id, username, role, password, marks
        FROM users
        WHERE username = '{username}'
    """
    cursor.execute(query)

    row = cursor.fetchone()
    conn.close()

    if row:
        return User(*row)

    return None


# ==============================
# USER SEARCH
# SQL Injection Demo
# ==============================
def search_users(keyword):
    conn = get_db()
    cursor = conn.cursor()

    # 🔴 Unsafe LIKE query
    query = f"""
        SELECT id, username, role, marks
        FROM users
        WHERE username LIKE '%{keyword}%'
    """
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [User(*row, password="test123") for row in rows]  # 🔴 Weak password default
