import sqlite3

DB_PATH = "data/database.db"


class User:
    def __init__(self, user_id, username, role, password="test123", marks=0):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.password = password
        self.marks = marks

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "marks": self.marks
        }


def get_db():
    return sqlite3.connect(DB_PATH)


# ================================
# VULNERABLE USER LOOKUP (SQLi)
# ================================
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()

    # ❌ SQL INJECTION VULNERABILITY
    query = f"SELECT id, username, role, password, marks FROM users WHERE username = '{username}'"
    cursor.execute(query)

    row = cursor.fetchone()
    conn.close()

    if row:
        return User(*row)

    return None


# ================================
# USER SEARCH (SQLi)
# ================================
def search_users(keyword):
    conn = get_db()
    cursor = conn.cursor()

    # ❌ SQL INJECTION
    query = f"SELECT id, username, role, marks FROM users WHERE username LIKE '%{keyword}%'"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [User(*row) for row in rows]
