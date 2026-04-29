import os
import sys

from flask import Flask, render_template, request, jsonify

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import backend.kundli_milan as km

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/milan', methods=['POST'])
def api_milan():
    data = request.get_json() or {}
    boy_payload = data.get('boy', {})
    girl_payload = data.get('girl', {})

    if isinstance(boy_payload, str):
        boy_payload = {"name": boy_payload}
    if isinstance(girl_payload, str):
        girl_payload = {"name": girl_payload}

    boy_name = boy_payload.get('name', '').strip()
    girl_name = girl_payload.get('name', '').strip()

    result = km.naam_se_kundli_milan(
        boy_name,
        girl_name,
        boy_birth=boy_payload,
        girl_birth=girl_payload,
    )
    # Add percentage field
    if 'total_gunas' in result:
        try:
            total = float(result['total_gunas'].split()[0])
            percent = round((total / 36.0) * 100, 1)
            result['percentage'] = f"{percent}%"
        except Exception:
            result['percentage'] = None
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
