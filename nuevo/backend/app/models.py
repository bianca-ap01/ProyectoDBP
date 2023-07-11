from flask_sqlalchemy import SQLAlchemy
from config.qa import config
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


usuario_quiz = db.Table('usuario_quiz',
    db.Column('usuario_id', db.String(36), db.ForeignKey('usuarios.id')),
    db.Column('quiz_id', db.String(36), db.ForeignKey('quizzes.id'))
    )


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)

    codeforces_handle = db.Column(db.String(30), nullable=True, unique=False)
    atcoder_handle = db.Column(db.String(30), nullable=True, unique=False)
    vjudge_handle = db.Column(db.String(30), nullable=True, unique=False)
    
    hpassword = db.Column(db.String(1000), nullable=False, unique=False)
    
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))

    imagenes = db.relationship('Imagen', backref='usuarios', lazy=True)


    def __init__(self, nickname, email, key, codeforces_handle = "", atcoder_handle = "", vjudge_handle = ""):
        self.nickname = nickname
        self.email = email
        self.codeforces_handle = codeforces_handle
        self.atcoder_handle = atcoder_handle
        self.vjudge_handle = vjudge_handle
        self.hpassword = key
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()


    def __repr__(self):
        return f"Usuario {self.nickname}"

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
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
            created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return created_id
    
    def update(self):
        try:
            self.modified_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
    
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    num_preg = db.Column(db.Integer, nullable = False)
    max_score = db.Column(db.Integer, nullable = False, default = 20)
    score = db.Column(db.Integer, nullable = True, default = 0)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))

    preguntas = db.relationship('Pregunta', backref = 'quizzes')

    def __init__(self, title, num_preg, max_score, score=0):
        self.title = title
        self.num_preg = num_preg
        self.max_score = max_score
        self.score = score
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()


    def __repr__(self):
        return f"<Quiz {self.title}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'num_preg': self.num_preg,
            'score': self.score,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return created_id
    
    def update(self):
        try:
            self.modified_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
    
    def delete(self):
        try:
            preguntas = Pregunta.query.filter(Pregunta.quiz_id == self.id)
            
            for pregunta in preguntas:
                pregunta.delete()

            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e', e)
            db.session.rollback()
        finally:
            db.session.close()


class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    statement = db.Column(db.String(500), nullable=False)
    
    max_score = db.Column(db.Integer, nullable = False, default = 0)
    score = db.Column(db.Integer, nullable = True, default = 0)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    
    quiz_id = db.Column(db.String(36), db.ForeignKey('quizzes.id'))
    opciones = db.relationship('Opcion', backref = "preguntas")


    def __init__(self, statement, quiz_id, max_score, score):
        self.quiz_id = quiz_id
        self.statement = statement
        self.max_score = max_score
        self.score = score
        self.created_at = datetime.utcnow()
        self.modified_at_at = datetime.utcnow()

    def __repr__(self):
        return f"<Pregunta: {self.statement}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'statement': self.statement,
            'max_score': self.max_score,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return created_id
    
    def update(self):
        try:
            self.modified_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
    
    def delete(self):
        try:
            opciones = Opcion.query.filter(Opcion.pregunta_id == self.id)
            for opcion in opciones:
                opcion.delete()
            
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e', e)
            db.session.rollback()
        finally:
            db.session.close()


class Opcion(db.Model):
    __tablename__ = 'opciones'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    answer  = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    pregunta_id = db.Column(db.String(36), db.ForeignKey('preguntas.id'))


    def __init__(self, description, pregunta_id, answer):
        self.pregunta_id = pregunta_id,
        self.description = description,
        self.answer = answer
        self.created_at = datetime.utcnow(),
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f"<Opcion: {self.description}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at,
            'answer': self.answer,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return created_id


    def update(self):
        try:
            self.modified_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
    
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


class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(120), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True)

    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)


    def __init__(self, filename, user_id):
        self.filename = filename
        self.usuario_id = user_id
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def serialize(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return created_id


    def update(self):
        try:
            self.modified_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
    
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