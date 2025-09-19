from flask import Blueprint, current_app, request, jsonify, escape
from .db import get_db

def register_routes(app):
    bp = Blueprint("main", __name__)

    @bp.route("/")
    def index():
        return "<h2>Vuln Flask App Pro — endpoints: /search (demo XSS) & /user (demo SQLi)</h2>"

    # HEALTHCHECK
    @bp.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # Note: This endpoint intentionally demonstrates INSECURE patterns for demo.
    # In production you would USE parameterized queries and escape output.
    @bp.route("/user")
    def user():
        user_id = request.args.get("id", "")
        # Vulnerable usage (for demo only) kept but we also show safe alternative below:
        vuln_query = "SELECT id, name, email FROM users WHERE id = " + user_id
        try:
            db = get_db()
            cur = db.cursor()
            # Execute vulnerable query (demonstration)
            cur.execute(vuln_query)
            rows = [dict(r) for r in cur.fetchall()]
            return jsonify({"vulnerable_result": rows})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Safe version for comparison (always prefer this)
    @bp.route("/user_safe")
    def user_safe():
        user_id = request.args.get("id", None)
        if not user_id:
            return jsonify({"error": "id required"}), 400
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            rows = [dict(r) for r in cur.fetchall()]
            return jsonify({"safe_result": rows})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route("/search")
    def search():
        q = request.args.get("q", "")
        # intentionally demonstrate XSS vulnerability by rendering raw (for demo)
        # Provide an escaped alternative example in /search_safe
        return f"<html><body><h1>Search results for: {q}</h1></body></html>"

    @bp.route("/search_safe")
    def search_safe():
        q = request.args.get("q", "")
        return f"<html><body><h1>Search results for: {escape(q)}</h1></body></html>"

    app.register_blueprint(bp)
