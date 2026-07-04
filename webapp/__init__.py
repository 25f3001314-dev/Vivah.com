from flask import Flask

from .routes import bp as routes_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.register_blueprint(routes_bp)
    return app


# Expose an `app` object for WSGI servers
app = create_app()
