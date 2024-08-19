from flask import render_template, send_from_directory, jsonify, Blueprint
from api.models import get_db_connection

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/pages/<path:path>')
def serve_pages(path):
    try:
        # Serve HTML pages from the 'pages' folder
        return render_template(f'{path}')
    except Exception as e:
        print(f'Error serving {path}: {e}')
        return "Page not found", 404

@routes_bp.route('/assets/<path:path>')
def serve_assets(path):
    # Serve static files from the 'assets' folder
    return send_from_directory('assets', path)

@routes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(resultados)
    return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
