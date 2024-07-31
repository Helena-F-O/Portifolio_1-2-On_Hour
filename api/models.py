from . import db

class User(db.Model):
    __tablename__ = 'usuarios'
    cpf = db.Column(db.String, primary_key=True)
    usuario = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    horas_exigidas = db.Column(db.String)
