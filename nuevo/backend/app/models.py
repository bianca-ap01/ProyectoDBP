from flask_sqlalchemy import SQLAlchemy
from config.local import config
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys


db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE"] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    codeforces_handle = db.Column(db.String(30), nullable=True, unique=False)
    atcoder_handle = db.Column(db.String(30), nullable=True, unique=False)
    vjudge_handle = db.Column(db.String(30), nullable=True, unique=False)
    image = db.Column(db.String(500), nullable=True)
    hpassword = db.Column(db.String(1000), nullable=False, unique=False)
    status = db.Column(db.Boolean(), nullable=False, default=True)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    board = db.relationship('Admin', backref='usuarios',
                            lazy='joined', uselist=False)

    def __init__(self, nickname, email, codeforces_handle, atcoder_handle, vjudge_handle, key):
        self.nickname = nickname
        self.email = email
        self.codeforces_handle = codeforces_handle
        self.atcoder_handle = atcoder_handle
        self.vjudge_handle = vjudge_handle
        self.hpassword = key
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"User {self.nickname}"

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'image': self.image,
            'codeforces_handle': self.codeforces_handle,
            'atcoder_handle': self.atcoder_handle,
            'vjudge_handle': self.vjudge_handle,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    @property
    def password(self):
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self, password):
        self.hpassword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hpassword, password)
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            user_created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return user_created_id
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()


class Admin(db.Model):
    __tablename__ = 'administradores'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    status = db.Column(db.Boolean(), default=True, nullable=False)
    admin_since = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey(
        'usuarios.id'), nullable=False)

    # def __init__(self):
    #     self.board_since = datetime.utcnow()

    def __repr__(self):
        return f"<Usuario ID: {self.usuario_id}>"


usuario_cuestionario = db.Table('usuario_cuestionario', db.Column('usuario_id', db.String(36), db.ForeignKey(
    'usuario.id')), db.Column('cuestionario_id', db.String(36), db.ForeignKey('cuestionarios.id')))

class Cuestionario(db.Model):
    __tablename__ = 'cuestionarios'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    user = db.relationship(
         'Usuario', backref='usuarios', lazy=True, secondary=usuario_cuestionario)

    def __init__(self, title, link, platform, num_prob):
        self.title = title
        self.link = link
        self.platform = platform
        self.num_prob = num_prob

    def __repr__(self):
        return f"<Cuestionario {self.title}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

cuestionario_problema = db.Table('cuestionario_problema', db.Column('cuestionario_id', db.String(36), db.ForeignKey(
    'cuestionario.id')), db.Column('problema_id', db.String(36), db.ForeignKey('problemas.id')))

class Problema(db.Model):
    __tablename__ = 'problemas'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    cuestionario_id = db.Column(db.String(36), db.ForeignKey(
        'cuestionario.id'), nullable=False)
    statement = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    contest = db.relationship(
        'Cuestionario', backref='problemas', lazy=True, secondary=cuestionario_problema)

    def __init__(self, statement, cuestionario_id):
        self.cuestionario_id = cuestionario_id,
        self.statement = statement

    def __repr__(self):
        return f"<Problema: {self.title}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'statement': self.statement,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            problema_created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return problema_created_id
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
    
problema_opcion = db.Table('problema_opcion', db.Column('problema_id', db.String(36), db.ForeignKey(), nullable=False), db.Column('opcion_id', db.String(36), db.ForeignKey('opciones.id'), nullable=False))

class Opcion(db.Model):
    __tablename__ = 'opciones'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    problema_id= db.Column(db.String(36), db.ForeignKey(
        'problema.id'), nullable=False)
    descripction = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    contest = db.relationship(
        'Problema', backref='opciones', lazy=True, secondary=problema_opcion)

    def __init__(self, description, problema_id, answer):
        self.problema_id = problema_id,
        self.descripction = description,
        self.answer = answer,
        self.created_at = datetime.utcnow(),
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f"<Opcion: {self.descripction}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'descripction': self.descripction,
            'answer': self.answer,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


