from flask import Blueprint, request, send_from_directory
import os
from backend.models.user import get_db, User

faculty_bp = Blueprint("faculty", __name__)

# ================================
# Faculty Dashboard (Broken Access Control)
# ================================
@faculty_bp.route("/dashboard", methods=["GET"])
def dashboard():
    # 🔴 Session optional
    session_id = request.headers.get("Session-Id")

    # 🔴 No real validation
    # Anyone can access dashboard directly
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    HTML_DIR = os.path.join(BASE_DIR, "..", "..", "frontend", "html", "faculty")

    return send_from_directory(
        HTML_DIR,
        "faculty-dashboard.html"
    )


# ================================
# View Student Marks
# IDOR + SQL Injection
# ================================
@faculty_bp.route("/marks", methods=["GET"])
def view_marks():
    student_id = request.args.get("student_id")

    if not student_id:
        return {"error": "student_id required"}, 400

    # 🔴 No session validation
    # 🔴 No role check

    conn = get_db()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerable
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

    student = User(*row)

    return {
        "student": student.username,
        "marks": student.marks,
        "warning": "No access control enforced"
    }


# ================================
# Update Student Marks
# Missing Auth + SQLi
# ================================
@faculty_bp.route("/update-marks", methods=["POST"])
def update_marks():
    data = request.get_json() or {}

    student_id = data.get("student_id")
    marks = data.get("marks")

    if not student_id or marks is None:
        return {"error": "student_id and marks required"}, 400

    # 🔴 No authentication
    # 🔴 Any user can update marks

    conn = get_db()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerable
    query = f"""
        UPDATE users
        SET marks = {marks}
        WHERE id = {student_id}
    """
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {
        "message": "Marks updated successfully",
        "warning": "No authorization checks performed"
    }
