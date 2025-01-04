# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.dashboard import dashboard_bp
from app.calendar import calendar_bp
from app.sessions import sessions_bp
from app.assignments import assignments_bp
from app.registry import registery_bp
from app.welcome import welcome_bp

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory to create and configure the Flask app."""
    # Create the Flask app
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')

    print("Template Folder:", app.template_folder)
    print("Template Folder:", app.template_folder)    # Load configuration
    app.config.from_object(config_class)

    app.debug = app.config["DEBUG"]
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        from app import models  # Import models inside the app context

    # Register blueprints or routes
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(sessions_bp, url_prefix="/sessions")
    # app.register_blueprint(calendar_bp, url_prefix="/calendar")
    app.register_blueprint(assignments_bp, url_prefix="/assignments")
    app.register_blueprint(registery_bp, url_prefix="/registry")
    app.register_blueprint(welcome_bp, url_prefix="/")
    # from app.routes import main
    # app.register_blueprint(main)

    return app

# Create an app instance globally (optional for simple use cases)
app = create_app()
