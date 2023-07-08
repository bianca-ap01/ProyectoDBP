from flask import (
    Blueprint,
    request,
    jsonify,
    abort
)

from .models import Cuestionario
from .extensions import db
from config.local import config

cuestionario_bp = Blueprint('cuestionarios', __name__)

@cuestionario_bp.route('/cuestionarios', methods=['POST'])
def crear_cuestionario():
    error_list = []
    return_code = 201
    cuestionario = None
    try:
        body = request.get_json()

        if 'title' not in body:
            error_list.append('Título requerido')
        else:
            title = body.get('title')

        if 'num_prob' not in body:
            error_list.append('Número de problemas requerido')
        else:
            num_prob = body.get('num_prob')

        cuestionario_db = Cuestionario.query.filter(Cuestionario.title==title).first()

        if cuestionario_db is not None :
            if cuestionario_db.title == title:
                error_list.append('Ya existe un cuestionario con este título')

        if len(error_list) > 0:
            return_code = 400
        else:
            cuestionario = Cuestionario(title=title, num_prob=num_prob)
            db.session.add(cuestionario)
            db.session.commit()

    except Exception as e:
        print('e: ', e)
        return_code = 500

    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando el nuevo cuestionario'
        }), return_code
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({'id': cuestionario.id, 'success': True, 'message': 'Cuestionario creado satisfactoriamente'}), return_code

@cuestionario_bp.route('/cuestionarios/<_id>', methods=['PATCH'])
def editar_cuestionario(_id):
    error_list = []
    return_code = 200
    try:
        cuestionario_db = Cuestionario.query.filter(Cuestionario.id==_id).first()

        if cuestionario_db is None:
            error_list.append('No existe el cuestionario')
        else:
            body = request.get_json()

        if 'title' in body:
            cuestionario_db.title = body.get('title')

        if len(error_list) > 0:
            return_code = 400
        else:
            db.session.commit()

    except Exception as e:
        print('e: ', e)
        return_code = 500

    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error modificando el título del cuestionario'
        }), return_code
    elif return_code != 200:
        abort(return_code)
    else:
        return jsonify({
            'success': True, 'message': 'Cuestionario actualizado satisfactoriamente',
        }), return_code

@cuestionario_bp.route('/cuestionarios', methods=['GET'])
def obtener_cuestionario():
    return_code = 200
    lista_cuestionarios = []
    try:
        search_query = request.args.get('search', None)

        if search_query:
            cuestionarios = Cuestionario.query.filter(
                Cuestionario.title.like('%{}%'.format(search_query))).all()
            lista_cuestionarios = [cuestionario.serialize() for cuestionario in cuestionarios]
        else:
            cuestionarios = Cuestionario.query.all()
            lista_cuestionarios = [cuestionario.serialize() for cuestionario in cuestionarios]

        if not lista_cuestionarios:
            return_code = 404

    except Exception as e:
        print('e: ', e)
        return_code = 500

    if return_code == 500:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'cuestionarios': lista_cuestionarios 
        }), return_code

@cuestionario_bp.route('/cuestionarios/<_id>', methods=['GET'])
def obtener_cuestionario_id(_id):
    return_code = 200
    error_list = []
    cuestionario = None
    try:
        cuestionario = Cuestionario.query.get(_id)
        
        if cuestionario is None:
            return_code = 404
            error_list.append('Cuestionario inexistente')

        if len(error_list) > 0:
            return_code = 400

    except Exception as e:
        print('e: ', e)
        return_code = 500

    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error buscando el cuestionario'
        }), return_code
    elif return_code != 200:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'cuestionario': cuestionario.serialize()
        }), return_code
