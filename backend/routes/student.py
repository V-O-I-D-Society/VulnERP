from flask import Blueprint, request
from backend.models.user import get_db, User

student_bp = Blueprint("student", __name__)

# ================================
# Student Dashboard
# Broken Access Control
# ================================
@student_bp.route("/dashboard", methods=["GET"])
def dashboard():
    session_id = request.headers.get("Session-Id")

    if not session_id:
        return {"error": "Session required"}, 401

    # 🔴 VULNERABILITY:
    # trusting client-controlled session string
    if not session_id.startswith("student"):
        return {"error": "Access denied"}, 403

    return {
        "message": "Welcome to Student Dashboard",
        "session": session_id,
        "note": "Access granted based on session prefix only"
    }


# ================================
# Student Profile
# Horizontal IDOR + SQL Injection
# ================================
@student_bp.route("/profile/<student_id>", methods=["GET"])
def profile(student_id):
    session_id = request.headers.get("Session-Id")

    if not session_id:
        return {"error": "Session required"}, 401

    # 🔴 No real authentication / authorization
    if not session_id.startswith("student"):
        return {"error": "Access denied"}, 403

    conn = get_db()
    cursor = conn.cursor()

    # 🔴 SQL Injection + IDOR
    query = f"""
        SELECT id, username, role, password, marks
        FROM users
        WHERE id = {student_id}
    """

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Student not found"}, 404

    user = User(*row)

    return {
        "student_profile": user.to_dict(),
        "warning": "No ownership check performed"
    }
