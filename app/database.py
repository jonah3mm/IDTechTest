from app import db


def init_db(app):
    """Create all database tables within the application context."""
    with app.app_context():
        db.create_all()
