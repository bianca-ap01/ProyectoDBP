from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Usuario
from .models import db  
from config.local import config

users_bp = Blueprint('/usuarios', __name__)

@users_bp.route('/usuarios', methods = ['POST'])
def crear_usuario():
    error_list = []
    return_code = 201
    user = None 

    try:
        body = request.get_json()

        if 'username' not in body:
            error_list.append('Nombre de usuario requerido')
        else:
            username = body.get('username')

        if 'password' not in body:
            error_list.append('Contraseña requerida')
        else:
            password = body.get('password')
        
        if 'confirmation_password' not in body:
            error_list.append('Contraseña de confimación requerida')
        else:
            confirmation_password = body.get('confirmation_password')

        user_db = Usuario.query.filter(Usuario.username==username).first()

        if user_db is not None:
            if user_db.username == username:
                error_list.append('Ya existe un usuario con este apodo')
        
        if len(password) < 8:
            error_list.append('La contraseña debe tener al menos 8 caracteres')

        if password != confirmation_password:
            error_list.append('Las contraseñas ingresadas son diferentes')

        # Crear el usuario solo si no hay errores
        if len(error_list) == 0:
            user = Usuario(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            token = jwt.encode({
                'user_created_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
    except Exception as e:
        print('e: ', e)
        error_list.append('Error al crear el usuario')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando al nuevo usuario'
        }), return_code
    elif return_code != 201 or user is None:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user.id,
        }), return_code
