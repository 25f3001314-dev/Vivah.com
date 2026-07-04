import os

from . import create_app


if __name__ == '__main__':
    # Run locally with debug; production deployments should use a WSGI/ASGI server
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=debug_mode)
