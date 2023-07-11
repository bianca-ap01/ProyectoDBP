from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from .models import db, setup_db, Imagen
from flask_cors import CORS
from .utilities import allowed_file
from .users_controller import users_bp
from .preguntas_controller import preguntas_bp
from .quizzes_controller import quizzes_bp
from .opciones_controller import opciones_bp

# from .authentication import authorize

import os
import sys


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/usuarios'
        app.register_blueprint(users_bp)
        app.register_blueprint(preguntas_bp)
        app.register_blueprint(quizzes_bp)
        app.register_blueprint(opciones_bp)
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins=['http://localhost:8080'])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Max-Age', '10')
        return response
    
    # @app.route('/imagenes', methods = ["POST"])
    # def subir_imagen():
    #     returned_code = 201
    #     list_errors = []
    #     try:
    #         if 'usuario_id' not in request.form:
    #             list_errors.append('Usuario asociado requerido')
    #         else:
    #             user_id = request.form['usuario_id']

    #         if 'image' not in request.files:
    #             list_errors.append('Imagen requerida')
    #         else:
    #             file = request.files['image']

    #             if not allowed_file(file.filename):
    #                 return jsonify({'success': False, 'message': 'Formato de imagen no permitido'}), 400

    #         if len(list_errors) > 0:
    #             returned_code = 400
    #         else:
    #             cwd = os.getcwd()

    #             user_dir = os.path.join(
    #                 app.config['UPLOAD_FOLDER'], user_id)
    #             os.makedirs(user_dir, exist_ok=True)

    #             upload_folder = os.path.join(cwd, user_dir)

    #             file.save(os.path.join(upload_folder, file.filename))

    #             file = Imagen(file.filename, user_id)

    #             file.insert()

    #     except Exception as e:
    #         db.session.rollback()
    #         returned_code = 500
    #     finally:
    #         db.session.close()

    #     if returned_code == 400:
    #         return jsonify({'success': False, 'message': 'Error subiendo imagen', 'errors': list_errors}), returned_code
    #     elif returned_code != 201:
    #         abort(returned_code)
    #     else:
    #         return jsonify({'success': True, 'message': 'Imagen subida satisfactoriamente'}), returned_code

        


    return app