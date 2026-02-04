from flask import Flask, request, jsonify, redirect
from backend.config.settings import Settings

# route blueprints import
from backend.routes.auth import auth_bp
from backend.routes.student import student_bp
from backend.routes.faculty import faculty_bp
from backend.routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def index():
        return {
            "project": "VulnERP",
            "status": "Backend running",
            "message": "Welcome to VulnERP backend"
        }

    # 🔴 Intentionally weak dashboard router (for access control testing)
    @app.route("/dashboard")
    def dashboard_router():
        session_id = request.headers.get("Session-Id")

        # no session → no auth check (intentional vulnerability later)
        if not session_id:
            return jsonify({"error": "Session-Id header missing"}), 401

        # very naive role routing (to be abused later)
        if session_id.startswith("student"):
            return redirect("/student/dashboard")
        elif session_id.startswith("faculty"):
            return redirect("/faculty/dashboard")
        elif session_id.startswith("admin"):
            return redirect("/admin/dashboard")

        return jsonify({"error": "Invalid session"}), 403

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
