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
from config.local import config

users_bp = Blueprint('/usuarios', __name__)


@users_bp.route('/usuarios', methods = ['POST'])
def crear_usuario():
    error_list = []
    return_code = 201
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

        if user_db is not None :
            if user_db.username == username:
                error_list.append('Ya existe un usuario con este apodo')
        else:
            if len(password) < 8:
                error_list.append('La contraseña debe tener al menos 8 caracteres')

            if password != confirmation_password:
                error_list.append('Las contraseñas ingresadas son diferentes')

        if len(error_list) > 0:
            return_code = 400
        else:
            user = Usuario(username=username, password=password)
            user_created_id = user.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
    except Exception as e:
        print('e: ', e)
        return_code = 500

    
    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando al nuevo usuario'
        })
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        })

