from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    abort,
    redirect,
    url_for,
    session,
    flash,
    Blueprint,
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
app.secret_key = 'clave_super_secreta'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/users'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Models
with app.app_context():
    # Convertir el modelo en una tabla
    db.create_all()

session = {}    # Session
current_user = {}   # Current User


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    codeforces_handle = db.Column(db.String(30), nullable=True, unique=False)
    atcoder_handle = db.Column(db.String(30), nullable=True, unique=False)
    vjudge_handle = db.Column(db.String(30), nullable=True, unique=False)
    image = db.Column(db.String(500), nullable=True)
    hpassword = db.Column(db.String(1000), nullable=False, unique=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    members = db.relationship('Member', backref='users', lazy=True)
    board = db.relationship('Board', backref='users', lazy=True)

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

    def __init__(self, nickname, email, codeforces_handle, atcoder_handle, vjudge_handle, hpassword):
        super().__init__(nickname, email, codeforces_handle,
                         atcoder_handle, vjudge_handle, hpassword)
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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'status': self.status,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


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
        'Professor', backref='teams', lazy=True, secondary=professor_team)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Team {self.name}>"


# user_contest = db.Table('user_contest', db.Column('user_id', db.String(36), db.ForeignKey(
#     'users.id')), db.Column('contest_id', db.String(36), db.ForeignKey('contests.id')))


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
    # user = db.relationship(
    #     'User', backref='users', lazy=True, secondary=user_contest)

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
        'Contest', backref='problems', lazy=True, secondary=contest_problem)

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
    board_since = db.Column(db.DateTime(timezone=True),
                            nullable=False, server_default=db.text("now()"))
    member_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'board',
    }

    def __init__(self, nickname, email, codeforces_handle, atcoder_handle, vjudge_handle, hpassword):
        super().__init__(nickname, email, codeforces_handle,
                         atcoder_handle, vjudge_handle, hpassword)
        self.board_since = datetime.utcnow()

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
        'Professor', secondary=professor_video, backref='videos')

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __repr__(self):
        return f"<Video {self.title}>"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'professors': self.professors
        }


# Routes


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('Debes iniciar sesión para acceder a esta página')
    return redirect(url_for('login'))


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

        _input = request.form['nickname']
        if '@' in _input:
            user = User.query.filter_by(email=_input).first()
        else:
            user = User.query.filter_by(nickname=_input).first()
            
        if user:
            if check_password_hash(user.hpassword, request.form['password']):
                login_user(user)
                flash('Has iniciado sesión correctamente')
                return redirect(url_for('home'), 200)
            else:
                flash('Contraseña incorrecta')
                return redirect(url_for('login'), 401)
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('login'), 401)

    else:
        return render_template('login.html')


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            _nickname = request.form['user_nickname']
            _email = request.form['user_email']
            _codeforces_handle = request.form['user_codeforces_handle']
            _atcoder_handle = request.form['user_atcoder_handle']
            _vjudge_handle = request.form['user_vjudge_handle']
            _password = request.form['user_password']
            _confirm_password = request.form['user_confirmation']
            _image = request.files['user_image']

            if _password != _confirm_password:
                flash('Las contraseñas no coinciden')
                return jsonify({'error': 'Las contraseñas no coinciden'}), 401

            if len(User.query.all()) != 0 and User.query.filter_by(nickname=_nickname).first() != None:
                flash('El nickname ya está registrado')
                return jsonify({'error': 'El nickname ya está registrado'}), 401

            if len(User.query.all()) != 0 and User.query.filter_by(email=_email).first() != None:
                flash('El email ya está registrado')
                return jsonify({'error': 'El email ya está registrado'}), 401

            if _email.split('@')[1] != 'utec.edu.pe':
                flash('El email no es válido')
                return jsonify({'error': 'El email no es válido'}), 401

            if _image.filename == "":
                flash("No ha seleccionado una imagen")
                return jsonify({'error': 'No ha seleccionado una imagen'}), 401

            if not allowed_file(_image.filename):
                flash("El formato de la imagen no es válido")
                return jsonify({'error': 'El formato de la imagen no es válido'}), 401

            user = User(nickname=_nickname, email=_email, codeforces_handle=_codeforces_handle,
                        atcoder_handle=_atcoder_handle, vjudge_handle=_vjudge_handle, key=generate_password_hash(_password))

            db.session.add(user)
            db.session.commit()

            cwd = os.getcwd()
            users_dir = os.path.join(app.config['UPLOAD_FOLDER'], user.id)
            os.makedirs(users_dir, exist_ok=True)

            upload_folder = os.path.join(cwd, users_dir)
            _image.save(os.path.join(upload_folder, _image.filename))

            db.session.commit()

            flash('El usuario ha sido registrado exitosamente')

            return jsonify({'success': 'El usuario ha sido registrado exitosamente'}), 200

        except:
            flash("Ha ocurrido un error")
            db.session.rollback()
            return jsonify({'error': 'Ha ocurrido un error'}), 500

        finally:
            db.session.close()

    else:
        return render_template('signup.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente')
    return redirect(url_for('home'), 200)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        try:
            _nickname = request.form['nickname']
            _codeforces_handle = request.form['codeforces_handle']
            _atcoder_handle = request.form['atcoder_handle']
            _vjudge_handle = request.form['vjudge_handle']
            _image = request.form['image']
            _password = request.form['password']
            if check_password_hash(current_user.password, _password):
                flash('Contraseña incorrecta')
                return redirect(url_for('profile'), 401)
            else:
                user = User.query.filter_by(id=current_user.id).first()

                if _nickname != '':
                    user.nickname = _nickname
                if _codeforces_handle != '':
                    user.codeforces_handle = _codeforces_handle
                if _atcoder_handle != '':
                    user.atcoder_handle = _atcoder_handle
                if _vjudge_handle != '':
                    user.vjudge_handle = _vjudge_handle
                if _image != '':
                    user.image = _image

                user.modified_at = datetime.datetime.now()
                db.session.commit()
                flash('Se han actualizado tus datos correctamente')
                return redirect(url_for('profile'), 200)
        except:
            flash('Ha ocurrido un error')
            return redirect(url_for('profile'), 500)

    else:
        return render_template('profile.html')


@app.route('/profile/<int:id>', methods=['GET'])
def profile_id(_id):
    if _id == '':
        _id = current_user.id
    _user = User.query.filter_by(id=_id).first()
    return render_template('perfil.html', user=_user.serialize())


@app.route('/lectures', methods=['GET'])
def lectures():
    _lectures = Video.query.all()
    return render_template('lectures.html', lectures=_lectures.serialize())


@app.route('/lectures/<int:id>', methods=['GET'])
@login_required
def lecture(id):
    _lecture = Video.query.filter_by(id=id).first()
    return render_template('lecture.html', lecture=_lecture.serialize())


@app.route('/lectures/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lecture(_id):
    _lecture = Video.query.filter_by(id=_id).first()
    if request.method == 'POST':
        try:
            _title = request.form['title']
            _link = request.form['link']
            _professors = request.form['professors']
            if _title != '':
                _lecture.title = _title
            if _link != '':
                _lecture.link = _link
            if _professors != '':
                _lecture.professors = _professors
            _lecture.modified_at = datetime.datetime.now()
            db.session.commit()
            flash('Se han actualizado los datos correctamente')
            return redirect(url_for('lecture', id=_id), 200)
        except:
            flash('Ha ocurrido un error')
            return redirect(url_for('lecture', id=_id), 500)
    else:
        return render_template('edit_lecture.html', lecture=_lecture.serialize())


@app.route('/lectures/new', methods=['GET', 'POST'])
@login_required
def new_lecture():
    if request.method == 'POST':
        try:
            _title = request.form['title']
            _link = request.form['link']
            _professors = request.form['professors']
            _lecture = Video(
                title=_title,
                link=_link,
                professors=_professors
            )
            db.session.add(_lecture)
            db.session.commit()
            flash('Se ha creado la clase correctamente')
            return redirect(url_for('lectures'), 200)
        except:
            flash('Ha ocurrido un error')
            return redirect(url_for('lectures'), 500)
    else:
        return render_template('new_lecture.html')


@app.route('/pendings', methods=['GET'])
@login_required
def pendings():
    pass


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
