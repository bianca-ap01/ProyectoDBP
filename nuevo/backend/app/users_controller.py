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
            error_list.append('username is required')
        else:
            username = body.get('username')

        if 'password' not in body:
            error_list.append('password is required')
        else:
            password = body.get('password')
        
        if 'confirmationPassword' not in body:
            error_list.append('confirmationPassword is required')
        else:
            confirmationPassword = body.get('confirmationPassword')

        user_db = Usuario.query.filter(Usuario.username==username).first()

        if user_db is not None :
            if user_db.username == username:
                error_list.append('An account with this username already exists')
        else:
            if len(password) < 8:
                error_list.append('Password must have at least 8 characters')

            if password != confirmationPassword:
                error_list.append('password and confirmationPassword does not match')


        if len(error_list) > 0:
            returned_code = 400
        else:
            user = Usuario(username=username, password=password)
            user_created_id = user.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
    except Exception as e:
        print('e: ', e)
        returned_code = 500

    
    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creating a new user'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        })

        