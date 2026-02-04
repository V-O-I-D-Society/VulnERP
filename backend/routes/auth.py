from flask import Blueprint, request
from backend.models.user import get_user_by_username
from backend.models.session import create_session, get_user_from_session

auth_bp = Blueprint("auth", __name__)

# 🔴 Broken Authentication + Role Trust
@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"error": "JSON required"}, 415

    data = request.get_json()

    # 🔴 trusting client-controlled input
    username = data.get("username")
    requested_role = data.get("role")  # attacker-controlled

    if not username:
        return {"error": "Username required"}, 400

    user = get_user_by_username(username)

    if not user:
        return {"error": "Invalid username"}, 401

    # 🔴 ROLE OVERRIDE (intentional vulnerability)
    if requested_role:
        user.role = requested_role

    # 🔴 weak / predictable session
    session_id = create_session(user)

    return {
        "message": "Login successful",
        "session_id": session_id,
        "role": user.role
    }


# 🔴 Broken Access Control
@auth_bp.route("/me", methods=["GET"])
def current_user():
    session_id = request.headers.get("Session-Id")

    if not session_id:
        return {"error": "Session-Id header missing"}, 401

    user = get_user_from_session(session_id)

    if not user:
        return {"error": "Invalid session"}, 401

    # 🔴 no role / privilege validation
    return user.to_dict()
