from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pages'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets'),
    static_url_path='/assets'
)

# Ajuste a string de conexão para o SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@DESKTOP-R69VPG8\\SQLEXPRESS/onHour?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .routes import *

if __name__ == "__main__":
    app.run(debug=True)
