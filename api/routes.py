from flask import render_template, send_from_directory, jsonify
from . import app
from flask import jsonify
from . import app, db
from .models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pages/<path:path>')
def serve_pages(path):
    try:
        print(f'Trying to serve: {path}')  # Debug message
        return render_template(path)
    except Exception as e:
        print(f'Error serving {path}: {e}')  # Debug message
        return "Page not found", 404


@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(app.static_folder, path)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'cpf': user.cpf, 'usuario': user.usuario, 'email': user.email, 'senha': user.senha, 'horas_exigidas': user.horas_exigidas} for user in users]
    return jsonify(users_list)