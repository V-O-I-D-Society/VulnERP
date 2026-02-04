from flask import Blueprint, request
from backend.models.session import get_user_from_session
from backend.models.user import get_db, User

admin_bp = Blueprint("admin", __name__)

# ================================
# Admin Dashboard
# Broken Access Control (Header Trust)
# ================================
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    session_id = request.headers.get("Session-Id")

    if not session_id:
        return {"error": "Session required"}, 401

    user = get_user_from_session(session_id)
    if not user:
        return {"error": "Invalid session"}, 401

    # 🔴 Client-controlled role header
    role = request.headers.get("Role")
    if role != "admin":
        return {"error": "Access denied"}, 403

    return {
        "message": "Welcome to Admin Dashboard",
        "note": "Role verified using request header",
        "logged_in_as": user.to_dict()
    }


# ================================
# View All Users
# Sensitive Data Exposure
# ================================
@admin_bp.route("/users", methods=["GET"])
def list_users():
    # 🔴 No authentication or authorization

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT id, username, role, password, marks FROM users"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    users = [User(*row).to_dict() for row in rows]

    return {
        "users": users,
        "warning": "Sensitive information exposed"
    }


# ================================
# Public Password Reset
# No Auth + SQL Injection
# ================================
@admin_bp.route("/reset-user", methods=["POST"])
def reset_user():
    data = request.get_json() or {}
    username = data.get("username")

    if not username:
        return {"error": "Username required"}, 400

    conn = get_db()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerable
    query = f"""
        UPDATE users
        SET password = 'password123'
        WHERE username = '{username}'
    """
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {
        "status": "Password reset executed",
        "username": username,
        "new_password": "password123"
    }


# ================================
# Change User Role
# Privilege Escalation
# ================================
@admin_bp.route("/change-role", methods=["POST"])
def change_role():
    data = request.get_json() or {}
    username = data.get("username")
    new_role = data.get("role")

    if not username or not new_role:
        return {"error": "username and role required"}, 400

    # 🔴 No authentication
    # 🔴 No role validation

    conn = get_db()
    cursor = conn.cursor()

    query = f"""
        UPDATE users
        SET role = '{new_role}'
        WHERE username = '{username}'
    """
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {
        "message": f"Role updated for {username}",
        "new_role": new_role
    }


# ================================
# Search Users
# SQL Injection
# ================================
@admin_bp.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "")

    conn = get_db()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerable LIKE query
    query = f"""
        SELECT id, username, role, password, marks
        FROM users
        WHERE username LIKE '%{keyword}%'
    """
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    users = [User(*row).to_dict() for row in rows]

    return {
        "results": users,
        "search_term": keyword
    }
