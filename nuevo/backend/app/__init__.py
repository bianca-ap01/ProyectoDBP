from flask import Flask, request, jsonify, abort
from .models import db, setup_db, Usuario, Admin, Cuestionario, Problema
from flask_cors import CORS
from .utilities import allowed_file
from .users_controller import users_bp
from .problema_controller import problemas_bp
from .cuestionario_controller import cuestionario_bp
from .opcion_controller import opciones_bp

import os
import sys


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/usuarios'
        app.register_blueprint(users_bp)
        app.register_blueprint(problemas_bp)
        app.register_blueprint(cuestionario_bp)
        app.register_blueprint(opciones_bp)
        setup_db(app, test_config.get('database_path') if test_config else None)
        CORS(app, origins=['http://localhost:8080'])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Max-Age', '10')
        return response
    
    return app
