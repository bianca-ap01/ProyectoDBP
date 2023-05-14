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
from werkzeug.security import generate_password_hash, check_password_hash
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

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/dbCPC'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/users'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Models
with app.app_context():
    # Convertir el modelo en una tabla
    db.create_all()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nickname = db.Column(db.String(30), nullable=True, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    codeforces_handle = db.Column(db.String(30), nullable=True, unique=True)
    atcoder_handle = db.Column(db.String(30), nullable=True, unique=True)
    vjudge_handle = db.Column(db.String(30), nullable=True, unique=True)
    date_of_birth = db.Column(db.Date(), nullable=True, unique=False)
    image = db.Column(db.String(500), nullable=True, unique=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    members = db.relationship('members', backref='users', lazy=True)
    board = db.relationship('board', backref='users', lazy=True)

    def __init__(self, nickname, date_of_birth, codeforces_handle, atcoder_handle, vjudge_handle, image):
        self.nickname = nickname
        self.date_of_birth = date_of_birth
        self.codeforces_handle = codeforces_handle
        self.atcoder_handle = atcoder_handle
        self.vjudge_handle = vjudge_handle
        self.image = image
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f"User {self.nickname}"

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'codeforces_handle': self.codeforces_handle,
            'atcoder_handle': self.atcoder_handle,
            'vjudge_handle': self.vjudge_handle,
            'date_of_birth': self.date_of_birth,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


class Member(User):
    __tablename__ = 'members'
    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False, primary_key=True)
    member_since = db.Column(db.DateTime(timezone=True),
                             nullable=False, server_default=db.text("now()"))
    comp_status = db.Column(db.Boolean(), default=True, nullable=False)
    member_status = db.Column(db.Boolean(), default=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'members',
        'polymorphic_load': 'inline'
    }

    def __init__(self, nickname, date_of_birth, codeforces_handle, atcoder_handle, vjudge_handle, image):
        super().__init__(nickname, date_of_birth, codeforces_handle,
                         atcoder_handle, vjudge_handle, image)
        self.member_since = datetime.utcnow()

    def __repr__(self):
        return f"<Member {self.user_id}>"


class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    # team_id = db.Column(db.String(36), db.ForeignKey(
    # 'teams.id'), nullable=False)

    def __init__(self, name, lastname, email):
        self.name = name
        self.lastname = lastname
        self.email = email

    def __repr__(self):
        return f"<Professor {self.email}>"


professor_team = db.Table('professor_team',
                          db.Column('professor_id',  db.String(36), db.ForeignKey(
                              'professors.id')),
                          db.Column('team_id', db.String(36), db.ForeignKey('teams.id')))


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.String(36), db.ForeignKey(
        'professors.id'), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=True)
    professor = db.relationship(
        'professors', backref='teams', lazy=True, secondary=professor_team)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Team {self.name}>"


class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    num_prob = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))

    def __init__(self, title, link, platorm, num_prob):
        self.title = title
        self.link = link
        self.platform = platorm
        self.num_prob = num_prob

    def __repr__(self):
        return f"<Contest {self.title}>"


contest_problem = db.Table('contest_problem', db.Column('contest_id', db.String(36), db.ForeignKey(
    'contests.id')), db.Column('problem_id', db.String(36), db.ForeignKey('problems.id')))


class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    contest_id = db.Column(db.String(36), db.ForeignKey(
        'contests.id'), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    contest = db.relationship(
        'contests', backref='problems', lazy=True, secondary=contest_problem)

    def __init__(self, title, link, platform):
        self.title = title
        self.link = link
        self.platform = platform

    def __repr__(self):
        return f"<Problem: {self.title}>"


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean(), default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    member_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'board',
    }

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return f"<Role: {self.role}>"


professor_video = db.Table('professor_video', db.Column('video_id', db.String(36), db.ForeignKey(
    'videos.id')), db.Column('professor_id', db.String(36), db.ForeignKey('professors.id')))


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    link = db.Column(db.String(500), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    professors = db.relationship(
        'professors', secondary=professor_video, backref='videos')

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __repr__(self):
        return f"<Video {self.title}>"


# Routes


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('aboutus.html')


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
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
        mail = User.query.filter_by(email=request.form['email']).first()
        nusername = User.query.filter_by(
            nickname=request.form['username']).first()
        if mail and nusername:
            if mail.email == request.form['email']:
                flash('El correo ya está registrado')
                return redirect(url_for('signup'))
            elif nusername.username == request.form['username']:
                flash('El nickname ya está registrado')
                return redirect(url_for('signup'))
            elif request.form['password'] != request.form['confirm_password']:
                flash('Las contraseñas no coinciden')
                return redirect(url_for('signup'))
            else:
                user = User(
                    nickname=request.form['username'],
                    email=request.form['email'],
                    password=request.form['password'],
                    nombre=request.form['nombre'],
                    apellido=request.form['apellido'],
                    vjudge_handle=request.form['vjudge_handle'],
                    fecha_de_nacimiento=request.form['fecha_de_nacimiento']
                )
                db.session.add(user)
                db.session.commit()
                flash('Te has registrado correctamente')
                return redirect(url_for('home'))
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente')
    return redirect(url_for('home'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
