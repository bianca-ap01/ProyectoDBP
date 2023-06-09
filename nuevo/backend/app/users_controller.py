from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .authentication import authorize
from .models import Usuario
from config.local import config
from werkzeug.security import generate_password_hash, check_password_hash


users_bp = Blueprint('/usuarios', __name__)

@users_bp.route('/usuarios', methods = ['POST'])
def crear_usuario():
    error_list = []
    return_code = 201
    try:
        body = request.get_json()

        if 'email' not in body:
            error_list.append('Email requerido')
        else:
            email = body.get('email')

        if 'nickname' not in body:
            error_list.append('Nombre de usuario requerido')
        else:
            nickname = body.get('nickname')

        if 'password' not in body:
            error_list.append('Contraseña requerida')
        else:
            password = body.get('password')
        
        if 'confirmation_password' not in body:
            error_list.append('Contraseña de confimación requerida')
        else:
            confirmation_password = body.get('confirmation_password')

        user_db = Usuario.query.filter(Usuario.nickname==nickname).first()

        if user_db is not None :
            if user_db.nickname == nickname:
                error_list.append('Ya existe un usuario con este apodo')
        else:
            if len(password) < 8:
                error_list.append('La contraseña debe tener al menos 8 caracteres')

            if password != confirmation_password:
                error_list.append('Las contraseñas ingresadas son diferentes')

        if len(error_list) > 0:
            return_code = 400
        else:
            user = Usuario(nickname=nickname, key=generate_password_hash(password), email=email)
            user_created_id = user.insert()

    except Exception as e:
        print('e: ', e)
        return_code = 500

    if return_code == 500:
        return jsonify({
           "success": False,
           "message": "Error creando usuario" 
        })
    elif return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
        })
    else:
        return jsonify({
            'success': True,
            'message': "Usuario creado :D",
        })


@users_bp.route('/usuarios/login', methods=['POST'])
def login():
    returned_code = 201
    error_list = []

    try:
        body = request.get_json()

        
        nickname = body.get("nickname")

        if not nickname:
            error_list.append("No se ha ingresado un usuario")
        else:
            user = Usuario.query.filter(Usuario.nickname == nickname).first()

            if user is None:
                error_list.append("El usuario no existe")
            else:
                if "password" not in body:
                    error_list.append("Contraseña no ingresada")
                else:
                    password = body.get("password")
                    if not password:
                        error_list.append("Contraseña no ingresada")
                    else:
                        if not check_password_hash(user.hpassword, password):
                            error_list.append("Usuario o contraseña incorrectos")

                user = Usuario.query.filter(Usuario.nickname == nickname).first()

                token = jwt.encode({                    
                        'sub': user.id,
                        'iat': datetime.datetime.utcnow(),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                    }, config['SECRET_KEY'], config['ALGORYTHM'])

        
        if len(error_list) > 0:
            returned_code = 400

    except Exception as e:
        print("e", e)
        returned_code = 500
    
    if returned_code == 500:
        return jsonify({
           "success": False,
           "message": "Error verificando usuario" 
        })
    elif returned_code == 400:
        return jsonify({
            "success": False,
            "errors": error_list
        })
    else:
        return jsonify({
            "success": True,
            "token": token,
            "user": user.serialize()
        })          


@users_bp.route("/usuarios/<token>", methods = ["GET"])
def obtener_usuario_token(token):
    data = jwt.decode(token, config['SECRET_KEY'], config['ALGORYTHM'])
    user = Usuario.query.filter(Usuario.id == data['sub']).first()
    if user is not None:
        return user.serialize()





# @users_bp.route("/usuarios", methods = ["PATCH"])
# @authorize
# def update_profile(current_user):
