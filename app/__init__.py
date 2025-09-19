import sqlite3
from flask import Flask
from .db import init_db
from .routes import register_routes

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping({
        "DATABASE": config.get("DATABASE", ":memory:") if config else ":memory:",
        "ENV": config.get("ENV", "development") if config else "development"
    })

    # init DB (for demo we init simple sqlite)
    init_db(app)

    # register blueprints / routes
    register_routes(app)
    return app
