from flask import render_template, send_from_directory, jsonify, Blueprint
from api.models import get_db_connection
from flask import Flask
from api.models import fetch_data

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/pages/<path:path>')
def serve_pages(path):
    try:
        # Serve HTML pages from the 'pages' folder
        return render_template(f'{path}', data=data)
    except Exception as e:
        print(f'Error serving {path}: {e}')
        return "Page not found", 404

@routes_bp.route('/assets/<path:path>')
def serve_assets(path):
    # Serve static files from the 'assets' folder
    return send_from_directory('assets', path)

