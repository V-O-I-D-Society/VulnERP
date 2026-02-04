import os
from flask import Flask, request, jsonify, redirect, send_from_directory
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

    # -------------------------------
    # Frontend path mapping
    # -------------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
    HTML_DIR = os.path.join(FRONTEND_DIR, "html")
    CSS_DIR = os.path.join(FRONTEND_DIR, "css")
    ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

    # -------------------------------
    # Static file routes
    # -------------------------------
    @app.route("/css/<path:filename>")
    def css_files(filename):
        return send_from_directory(CSS_DIR, filename)

    @app.route("/assets/<path:filename>")
    def asset_files(filename):
        return send_from_directory(ASSETS_DIR, filename)

    # -------------------------------
    # Public pages
    # -------------------------------
    @app.route("/")
    def landing_page():
        return send_from_directory(HTML_DIR, "index.html")

    @app.route("/login")
    def login_page():
        return send_from_directory(HTML_DIR, "login.html")

    @app.route("/role-select")
    def role_select():
        return send_from_directory(HTML_DIR, "role-select.html")

    # -------------------------------
    # 🔴 About page – Reflected XSS
    # -------------------------------
    @app.route("/about")
    def about_page():
        feedback = request.args.get("message")
        about_path = os.path.join(HTML_DIR, "about.html")

        # Read raw HTML file
        with open(about_path, "r", encoding="utf-8") as f:
            html = f.read()

        # 🔴 Intentionally unsafe reflection(reflected xss)
        if feedback:
            html = html.replace(
                "</section>",
                f"""
                <div class="feedback-output">
                    <h3>Preview:</h3>
                    {feedback}
                </div>
                </section>
                """
            )

        # ✅ ALWAYS return HTML
        return html

    # -------------------------------
    # Dashboards (frontend only)
    # -------------------------------
    @app.route("/student/dashboard")
    def student_dashboard():
        return send_from_directory(
            os.path.join(HTML_DIR, "student"),
            "student-dashboard.html"
        )

    @app.route("/faculty/dashboard")
    def faculty_dashboard():
        return send_from_directory(
            os.path.join(HTML_DIR, "faculty"),
            "faculty-dashboard.html"
        )

    @app.route("/admin/dashboard")
    def admin_dashboard():
        return send_from_directory(
            os.path.join(HTML_DIR, "admin"),
            "admin-dashboard.html"
        )

    # -------------------------------
    # 🔴 Weak dashboard router
    # -------------------------------
    @app.route("/dashboard")
    def dashboard_router():
        session_id = request.headers.get("Session-Id")

        if not session_id:
            return jsonify({"error": "Session-Id header missing"}), 401

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
