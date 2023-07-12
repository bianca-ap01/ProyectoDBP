from flask import (
    request,
    jsonify
)

import sys
import jwt
from config.local import config
from functools import wraps
from .models import Usuario



def authorize(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, config['SECRET_KEY'], config["ALGORYTHM"])
            user = Usuario.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

# def authorize(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         if 'X-ACCESS-TOKEN' in request.headers:
#             token = request.headers['X-ACCESS-TOKEN']

#         if token is None:
#             return jsonify({
#                 'success': False,
#                 'message': 'Usuario no autentificado, por favor presentar credenciales válidas'
#             }), 401
        
#         try:
#             data = jwt.decode(token, config['SECRET_KEY'], config['ALGORYTHM'])
#             print("data:", data)
#         except Exception as e:
#             print('e: ', e)
#             print('sys.exc_info(): ', sys.exc_info())
#             return jsonify({
#                 'success': False,
#                 'message': 'Token inválido, probar con otro token'
#             })
        
#         return f(*args, **kwargs)
#     decorator.__name__ = f.__name__
#     return decorator
