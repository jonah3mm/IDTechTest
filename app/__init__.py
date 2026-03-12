import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key enforcement for SQLite."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__, static_folder='static')

    from config import config
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        from app.routes.assets import assets_bp
        from app.routes.clients import clients_bp
        app.register_blueprint(assets_bp)
        app.register_blueprint(clients_bp)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve the built Vue SPA. Only used in production (Docker)."""
        dist_dir = os.path.join(app.static_folder, 'dist')
        if path and os.path.exists(os.path.join(dist_dir, path)):
            return send_from_directory(dist_dir, path)
        return send_from_directory(dist_dir, 'index.html')

    return app
