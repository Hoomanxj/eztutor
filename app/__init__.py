import os
from flask import Flask
from app.extentions import db, migrate, login_manager, mail
from app.config import Config
from app.dashboard import dashboard_bp
from app.ez_calendar import calendar_bp
from app.sessions import session_bp
from app.assignments import assignment_bp
from app.welcome import welcome_bp
from app.course import course_bp
from app.auth import auth_bp
from app.analytics import analytics_bp

def create_app(config_class=Config):
    """
    Application factory to create and configure the Flask app.

    Args:
        config_class: The configuration class to use.

    Returns:
        The configured Flask app.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions with the app
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_home"
    login_manager.login_message = "You need to login first"
    
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Prevent browser caching (for CSS and other static files)
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached."""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Register blueprints
    app.register_blueprint(welcome_bp, url_prefix="/")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(session_bp, url_prefix="/session")
    app.register_blueprint(calendar_bp, url_prefix="/calendar")
    app.register_blueprint(assignment_bp, url_prefix="/assignment")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(course_bp, url_prefix="/course")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")

    # Import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        from app import models  # Import models inside the app context

    return app
