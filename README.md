# Project README (high level)

# Vivah.com (refactor)

This repository contains a Flask-based frontend (webapp/) and a Python API package (api/) implementing Vedic matchmaking logic.

PR 1: Refactor project structure

What changed in this PR
- Removed sys.path and os.chdir usage from webapp/app.py.
- Split the previous monolithic webapp/app.py into a small package with:
  - webapp/__init__.py (application factory)
  - webapp/app.py (module entrypoint to run the app)
  - webapp/routes.py (Flask routes, previously in app.py)
  - webapp/i18n.py (translation dicts and helpers)
- Kept all routes, endpoints, and JSON outputs unchanged.
- Updated run instructions.

How to run the webapp (after PR1)

Recommended (runs with correct imports):

python -m webapp.app

This starts the Flask development server on port 8000 by default.

Run the API server (ASGI) separately:

python -m api.main

Notes
- This PR removes the previous sys.path and cwd hacks and makes the webapp import the api package as a normal top-level package; therefore the webapp should be launched using the "-m" module form or via a WSGI server so that the repository root is on sys.path.
- No business logic was changed.
