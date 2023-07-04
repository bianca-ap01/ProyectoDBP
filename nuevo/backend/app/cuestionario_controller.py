from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Cuestionario
from config.local import config

users_bp = Blueprint('/cuestionarios', __name__)



@users_bp.route('/cuestionarios', methods = ['POST'])
def crear_usuario():
    error_list = []
    return_code = 201
    try:
        body = request.get_json()

        if 'title' not in body:
            error_list.append('Título requerido')
        else:
            title = body.get('title')

        cuestionario_db = Cuestionario.query.filter(Cuestionario.title==title).first()

        if cuestionario_db is not None :
            if cuestionario_db.title == title:
                error_list.append('Ya existe un cuestionario con este título')

        if len(error_list) > 0:
            return_code = 400
        else:
            cuestionario = Cuestionario(title=title)
            new_created_id= cuestionario.insert()

            token = jwt.encode({
                'user_created_id': new_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
    except Exception as e:
        print('e: ', e)
        return_code = 500

    
    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando el nuevo cuestionario'
        })
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': new_created_id,
        })

      
@users_bp.route('/cuestionarios/<_id>', methods = ['PATCH'])
def crear_usuario(_id):
    error_list = []
    return_code = 201
    try:
        cuestionario_db = Cuestionario.query.filter(Cuestionario.id==_id).first()
        body = request.get_json()

        if 'title' in body:
            cuestionario_db.title = body.get('title')

        if cuestionario_db is None:
            error_list.append('No existe el cuestionario')

        if len(error_list) > 0:
            return_code = 400
        

    except Exception as e:
        print('e: ', e)
        return_code = 500

    
    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error modificando el título del cuestionario'
        })
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({
            'success': True
        })
    

@users_bp.route('/cuestionarios', methods = ['GET'])
def crear_usuario():
    error_list = []
    return_code = 201
    try:
        search_query = request.args.get('search', None)
        if search_query:
            cuestionarios = Cuestionario.query.filter(Cuestionario.title.like('%{}%'.format(search_query))).all()

            lista_cuestionarios = [cuestionario.serialize() for cuestionario in cuestionarios]
        else:
            cuestionarios = Cuestionario.query.all()
            lista_cuestionarios = [cuestionario.serialize() for cuestionario in cuestionarios]

        if not lista_cuestionarios:
            return_code = 404
            error_list.append('No se encontraron cuestionarios')

    except Exception as e:
        print('e: ', e)
        return_code = 500

    
    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando el nuevo cuestionario'
        })
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({
            'success': True
        })