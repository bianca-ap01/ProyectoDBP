from flask_sqlalchemy import SQLAlchemy
from config.local import config
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys

db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config['DATABASE_URI'] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    codeforces_handle = db.Column(db.String(30), nullable=True)
    atcoder_handle = db.Column(db.String(30), nullable=True)
    vjudge_handle = db.Column(db.String(30), nullable=True)
    image = db.Column(db.String(500), nullable=True)
    hpassword = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=True)
    cuestionarios = db.relationship('Cuestionario', backref = 'usuario')

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    admin = db.relationship('Admin', backref='usuario',
                            lazy='joined', uselist=False)

    def __init__(self, nickname, email, codeforces_handle, atcoder_handle, vjudge_handle, key):
        self.nickname = nickname
        self.email = email
        self.codeforces_handle = codeforces_handle
        self.atcoder_handle = atcoder_handle
        self.vjudge_handle = vjudge_handle
        self.hpassword = generate_password_hash(key)

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
            
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()

class Admin(db.Model):
    __tablename__ = 'administradores'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    status = db.Column(db.Boolean(), default=True, nullable=False)
    admin_since = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey(
        'usuarios.id'), nullable=False)

    def __repr__(self):
        return f"<Usuario ID: {self.usuario_id}>"
    
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
class Cuestionario(db.Model):
    __tablename__ = 'cuestionarios'
    id = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    num_prob = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=True)
    problemas = db.relationship('Problema', backref='cuestionarios', lazy=True)

    def __init__(self, title, num_prob):
        self.title = title
        self.num_prob = num_prob
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"<Cuestionario {self.title}>"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()

class Problema(db.Model):
    __tablename__ = 'problemas'
    id = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    cuestionario_id = db.Column(db.String(36), db.ForeignKey('cuestionarios.id'), nullable=False)
    statement = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    opciones = db.relationship('Opcion', backref='problemas', lazy=True)

    def __init__(self, statement, cuestionario_id):
        self.cuestionario_id = cuestionario_id
        self.statement = statement
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"<Problema: {self.statement}>"

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
class Opcion(db.Model):
    __tablename__ = 'opciones'
    id = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    problema_id = db.Column(db.String(36), db.ForeignKey('problemas.id'), nullable=False)

    def __init__(self, description, problema_id):
        self.problema_id = problema_id
        self.description = description
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f"<Opcion: {self.description}>"

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e', e)
            db.session.rollback()
        finally:
            db.session.close()
