from flask import Blueprint, request
from backend.models.session import get_user_from_session
from backend.models.user import get_db, User

faculty_bp = Blueprint("faculty", __name__)

# ================================
# Faculty Dashboard
# ================================
@faculty_bp.route("/dashboard", methods=["GET"])
def dashboard():
    session_id = request.headers.get("Session-Id")

    if not session_id:
        return {"error": "Session required"}, 401

    user = get_user_from_session(session_id)
    if not user:
        return {"error": "Invalid session"}, 401

    if user.role != "faculty":
        return {"error": "Access denied"}, 403

    return {
        "message": "Welcome to Faculty Dashboard",
        "faculty": user.to_dict()
    }


# ================================
# View Student Marks (IDOR)
# ================================
@faculty_bp.route("/marks", methods=["GET"])
def view_marks():
    student_id = request.args.get("student_id")
    if not student_id:
        return {"error": "student_id required"}, 400

    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT id, username, role, password, marks FROM users WHERE id = {student_id}"
    cursor.execute(query)  # ❌ SQLi + IDOR

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Student not found"}, 404

    student = User(*row)

    return {
        "student": student.username,
        "marks": student.marks
    }


# ================================
# Update Marks (NO AUTH)
# ================================
@faculty_bp.route("/update-marks", methods=["POST"])
def update_marks():
    data = request.get_json()
    student_id = data.get("student_id")
    marks = data.get("marks")

    if not student_id or marks is None:
        return {"error": "student_id and marks required"}, 400

    conn = get_db()
    cursor = conn.cursor()

    query = f"UPDATE users SET marks = {marks} WHERE id = {student_id}"
    cursor.execute(query)  # ❌ SQLi
    conn.commit()
    conn.close()

    return {
        "message": "Marks updated successfully"
    }
