import sqlite3
import os

DB_PATH = "data/database.db"

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ❌ Weak schema (intentional)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT,
    marks INTEGER
)
""")

# Dummy users
cursor.execute("INSERT INTO users (username, password, role, marks) VALUES ('admin01', 'admin123', 'admin', 0)")
cursor.execute("INSERT INTO users (username, password, role, marks) VALUES ('student01', 'student123', 'student', 85)")
cursor.execute("INSERT INTO users (username, password, role, marks) VALUES ('faculty01', 'faculty123', 'faculty', 0)")

conn.commit()
conn.close()

print("[+] Database initialized")
