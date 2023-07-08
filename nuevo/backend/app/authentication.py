from flask import Flask, request, jsonify
import sys
import jwt
from config.local import config
from functools import wraps

app = Flask(__name__)

def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('X-ACCESS-TOKEN')

        if not token:
            return jsonify({
                'success': False,
                'message': 'Usuario no autentificado, por favor presentar credenciales válidas'
            }), 401

        try:
            jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORITHM']])
        except jwt.exceptions.DecodeError as e:
            print('Error al decodificar el token:', e)
            return jsonify({
                'success': False,
                'message': 'Token inválido, probar con otro token'
            }), 401
        except jwt.exceptions.InvalidSignatureError as e:
            print('Error de firma del token:', e)
            return jsonify({
                'success': False,
                'message': 'Token inválido, probar con otro token'
            }), 401
        except Exception as e:
            print('Error al verificar el token:', e)
            return jsonify({
                'success': False,
                'message': 'Error al verificar el token'
            }), 401

        return f(*args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator

@app.route('/protected')
@authorize
def protected_route():
    return jsonify({
        'success': True,
        'message': 'Acceso permitido'
    })

if __name__ == '__main__':
    app.run()
