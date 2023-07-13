from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Opcion
from config.local import config
from .authentication import authorize 


opciones_bp = Blueprint('/opciones', __name__)

@opciones_bp.route('/opciones/<_id>', methods = ['GET'])
def listar_opciones(_id):
    error_list = []
    return_code = 201

    try:
        opciones_list = []
        opciones = Opcion.query.filter(Opcion.pregunta_id == _id)

        opciones_list = [opcion.serialize() for opcion in opciones]

        if not opciones_list:
            return_code = 404
            error_list.append('No se encontraron opciones para esta pregunta')

    except Exception as e:
        print(e)
        error_list.append('Error al crear la opción')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': True,
            'error': error_list,
        }), return_code
    elif return_code != 201 and return_code != 404:
            abort(return_code)
    else:
        return jsonify({'success': True, 'opciones': opciones_list}), return_code



@opciones_bp.route('/opciones', methods = ['POST'])
@authorize
def crear_opcion():
    error_list = []
    return_code = 201

    try:
        body = request.get_json()

        if 'description' not in body:
            error_list.append('Descripción requerida')
        else:
            description = body.get('description')
        
        if 'pregunta_id' not in body:
            error_list.append('Pregunta asociada requerida')
        else:
            pregunta_id = body.get('pregunta_id')

        if 'is_answer' not in body:
            error_list.append("No se ha marcado si la opción es correcta o no")
        else:
            is_answer = body.get('is_answer')

        opcion = Opcion(description=description, pregunta_id = pregunta_id, answer = is_answer)
        opcion_id = opcion.insert()

    except Exception as e:
        print(e)
        error_list.append('Error al crear la opción')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error creando la opcion'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'id': opcion_id, 'success': True, 'message': 'Opcion creada satisfactoriamente'}), return_code


@opciones_bp.route('/opciones/<_id>', methods = ['PATCH'])
@authorize
def actualizar_opcion(_id):
    error_list = []
    return_code = 201

    try:
        opcion = Opcion.query.filter(Opcion.id == _id).first()

        if not opcion:
            return_code = 404
            error_list.append('No se encontró la opción')
        else:
            body = request.json

            if 'description' in body:
                opcion.description = body['description']

            if 'pregunta_id' in body:
                opcion.pregunta_id = body['pregunta_id']

            if 'is_answer' in body:
                opcion.is_answer = body['is_answer']

            opcion.update()

    except Exception as e:
        print(e)
        error_list.append('Error al crear la opción')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error creando la opcion'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Opcion actualizada correctamente'}), return_code

@opciones_bp.route('/opciones/<_id>', methods = ['DELETE'])
@authorize
def borrar_opcion(_id):
    error_list = []
    return_code = 201

    try:
        opcion = Opcion.query.filter(Opcion.id == _id).first()

        if not opcion:
            return_code = 404
            error_list.append('No se encontró la opción')
        else:
            opcion.delete()

    except Exception as e:
        print(e)
        error_list.append('Error al actualizar la opción')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error creando la opcion'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Opcion eliminada satisfactoriamente'}), return_code






 