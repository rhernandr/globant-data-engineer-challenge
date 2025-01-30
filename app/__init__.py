from flask import Flask
from app.config import Config
from app.database import db, migrate
from app.routes import upload_blueprint, metrics_blueprint

def create_app() -> Flask:
    """
    Creates and configures an instance of the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(upload_blueprint, url_prefix='/api')
    app.register_blueprint(metrics_blueprint, url_prefix='/api')

    return app