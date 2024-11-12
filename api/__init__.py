from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pages'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets'),
    static_url_path='/assets'
)

# Defina uma chave secreta única e segura
app.config['SECRET_KEY'] = '5d41402abc4b2a76b9719d911017c592'  # Gere uma chave segura com o código sugerido

# Ajuste a string de conexão para o SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql.railway.internal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .routes import *

if __name__ == "__main__":
    app.run(debug=True)
