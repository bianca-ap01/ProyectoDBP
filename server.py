from flask import (
    Flask,
    jsonify, 
    render_template, 
    request,
    abort
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate
import uuid
import os
from datetime import datetime

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/dbCPC'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Models
with app.app_context():
   #Convertir el modelo en una tabla
   db.create_all()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    nickname = db.Column(db.String(30), nullable=True)
    codeforces_handle = db.Column(db.String(30), nullable=True)
    atcoder_handle = db.Column(db.String(30), nullable=True)
    vjudge_handle = db.Column(db.String(30), nullable=True)
    fecha_de_nacimiento = db.Column(db.Date(), nullable = True)
    created_at = db.Column(db.DateTime(timezone=True), nullable = False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable = False, server_default=db.text("now()"))
    miembros = db.relationship('Miembro', backref='usuarios', lazy=True)

    def __init__(self, name, lastname, nickname, fecha_de_nacimiento, codeforces_handle, atcoder_handle, vjudge_handle):
        self.name = name
        self.lastname = lastname
        self.nickname = nickname
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.codeforces_handle = codeforces_handle
        self.atcoder_handle = atcoder_handle
        self.vjudge_handle = vjudge_handle
        self.created_at = datetime.utcnow()
        self.modified_at =datetime.utcnow()

    def __repr__(self):
        return f"Usuario {self.name} {self.nickname}"


class Miembro(Usuario):
    __tablename__ = 'miembros'
    user_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False, primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'miembro',
    }
class NoMiembro(Usuario):
    __tablename__ = 'no_miembros'
    user_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False, primary_key=True)
    principiante = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    suscrito = db.Column(db.Boolean, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'no_miembro',
    }
class Profesor(db.Model):
    __tablename__ = 'profesores'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    equipo_id = db.Column(db.String(36), db.ForeignKey('equipos.id'), nullable=True)

class Equipo(db.Model):
    __tablename__ = 'equipos'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    profe_id = db.Column(db.String(36), db.ForeignKey('profesores.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    profesor = db.relationship('Profesor', backref='equipos', lazy=True)

class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    cantidad_problemas = db.Column(db.Integer, nullable=False)
    privacidad = db.Column(db.Boolean, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)

class Problema(db.Model):
    __tablename__ = 'problemas'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    contest_id = db.Column(db.String(36), db.ForeignKey('contests.id'), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    clave = db.Column(db.String(10), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    contest = db.relationship('Contest', backref='problemas', lazy=True)

class Directiva(db.Model):
    __tablename__ = 'directivas'
    id = db.Column(db.String(36), nullable=False, default=lambda:str(uuid.uuid4()), primary_key=True)
    cargo = db.Column(db.String(50), nullable=False)
    fecha_salida_cargo = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_entrada_cargo = db.Column(db.DateTime(timezone=True), nullable=False)

# Routes
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
