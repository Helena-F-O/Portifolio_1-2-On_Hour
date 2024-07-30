from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pages'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets'),
    static_url_path='/assets'
)

# Configuração do SQLAlchemy
DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = 'localhost\\SQLEXPRESS'
DATABASE = 'onHour'
USERNAME = 'root'
PASSWORD = ''

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .routes import *
