# En este server se creo la clase CREDENCIALES ,para tener una tabla adicional donde se guarde el USERNAME, EMAIL, PASSWORD, al momento de registrarse EN SIGN UP
# ADEMAS SE AGREGARON LAS RUTA /BLOG, /ABOUTUS, Y /signup/success, Y SE HIZO ALGUNAS MODIFICACIONES EN LA RUTA @app.route('/signup', methods=['GET', 'POST'])

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    abort,
    redirect,
    url_for,
    session,
    flash
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate
import uuid
import os
from datetime import datetime
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask import redirect


# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/dbCPC'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'mi_clave_secreta_super_segura'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Models


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    nickname = db.Column(db.String(30), nullable=True)
    codeforces_handle = db.Column(db.String(30), nullable=True)
    atcoder_handle = db.Column(db.String(30), nullable=True)
    vjudge_handle = db.Column(db.String(30), nullable=True)
    fecha_de_nacimiento = db.Column(db.Date(), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
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
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f"Usuario {self.name} {self.nickname}"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'nickname': self.nickname,
            'codeforces_handle': self.codeforces_handle,
            'atcoder_handle': self.atcoder_handle,
            'vjudge_handle': self.vjudge_handle,
            'fecha_de_nacimiento': self.fecha_de_nacimiento,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


class Miembro(Usuario):
    __tablename__ = 'miembros'
    user_id = db.Column(db.String(36), db.ForeignKey(
        'usuarios.id'), nullable=False, primary_key=True)
    miembro_directiva = db.relationship(
        'Directiva', backref='miembros', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'miembro',
    }


class Credenciales(db.Model):
    __tablename__ = 'credenciales'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Profesor(db.Model):
    __tablename__ = 'profesores'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    equipo_id = db.Column(db.String(36), db.ForeignKey(
        'equipos.id'), nullable=False)


profesor_equipo = db.Table('profesor_equipo',
                           db.Column('profesor_id',  db.String(36), db.ForeignKey(
                               'profesores.id')),
                           db.Column('equipo_id', db.String(36), db.ForeignKey('equipos.id')))


class Equipo(db.Model):
    __tablename__ = 'equipos'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    profe_id = db.Column(db.String(36), db.ForeignKey(
        'profesores.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    profesor = db.relationship(
        'Profesor', backref='equipos', lazy=True, secondary=profesor_equipo)


class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    cantidad_problemas = db.Column(db.Integer, nullable=False)
    privacidad = db.Column(db.Boolean, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)


contest_problema = db.Table('contest_problema', db.Column('contest_id', db.String(36), db.ForeignKey(
    'contests.id')), db.Column('problema_id', db.String(36), db.ForeignKey('problemas.id')))


class Problema(db.Model):
    __tablename__ = 'problemas'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    contest_id = db.Column(db.String(36), db.ForeignKey(
        'contests.id'), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    clave = db.Column(db.String(10), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    contest = db.relationship(
        'Contest', backref='problemas', lazy=True, secondary=contest_problema)


class Directiva(db.Model):
    __tablename__ = 'directiva'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    cargo = db.Column(db.String(50), nullable=False)
    fecha_salida_cargo = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_entrada_cargo = db.Column(db.DateTime(timezone=True), nullable=False)
    member_id = db.Column(db.String(36), db.ForeignKey(
        'miembros.user_id'), nullable=True)

# Routes


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('aboutus.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(
            nickname=request.form['username']).first()
        if user:
            if user.password == request.form['password']:
                login_user(user)
                flash('Has iniciado sesión correctamente')
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta')
                return redirect(url_for('login'))
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmation = request.form['confirmation']

        # Verificar si el usuario ya existe en la tabla de credenciales
        existing_user = Credenciales.query.filter_by(username=username).first()
        if existing_user:
            flash('error: El nombre de usuario ya está registrado')
            return redirect(url_for('signup'))

        # Verificar si el correo electrónico ya existe en la tabla de credenciales
        existing_email = Credenciales.query.filter_by(email=email).first()
        if existing_email:
            flash('error: El correo electrónico ya está registrado')
            return redirect(url_for('signup'))

        # Verificar si las contraseñas coinciden
        if password != confirmation:
            flash('error: Las contraseñas no coinciden')
            return redirect(url_for('signup'))

        # Crear un nuevo usuario en la tabla de credenciales
        new_user = Credenciales(
            username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('signup_success'))

    return render_template('signup.html')


@app.route('/signup/success', methods=['GET'])
def signup_success():
    return render_template('signup_success.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente')
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()


with app.app_context():
    # Convertir el modelo en una tabla
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
