from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Pregunta, Opcion
from config.local import config
from .authentication import authorize

preguntas_bp = Blueprint('/preguntas', __name__)


@preguntas_bp.route('/preguntas', methods = ['GET'])
def listar_preguntas(_id=None):
    error_list = []
    return_code = 201

    try:
        preguntas_list = []
        preguntas = Pregunta.query.all() #filter(Pregunta.quiz_id == _id)
        preguntas_list = [pregunta.serialize() for pregunta in preguntas]

        if not preguntas_list:
            return_code = 404
            error_list.append('No se encontraron preguntas para esta cuestionario')

    except Exception as e:
        print(e)
        error_list.append('Error al obtener las pregunta')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': True,
            'error': error_list,
        }), return_code
    elif return_code != 201 and return_code != 404:
            abort(return_code)
    else:
        return jsonify({'success': True, 'preguntas': preguntas_list}), return_code


@preguntas_bp.route('/preguntas', methods = ['POST'])
@authorize
def crear_pregunta():
    error_list = []
    return_code = 201

    try:
        body = request.get_json()

        if 'statement' not in body:
            error_list.append('statement requerida')
        else:
            statement = body.get('statement')
        
        if 'quiz_id' not in body:
            error_list.append('Quiz asociada requerido')
        else:
            quiz_id = body.get('quiz_id')
        
        if 'max_score' not in body:
            error_list.append('Puntaje requerida')
        else:
            max_score = body.get('max_score')

        pregunta_db = Pregunta.query.filter(Pregunta.statement==statement).first()

        if pregunta_db is not None :
            if pregunta_db.statement.lower() == statement.lower():
                error_list.append('Ya existe un pregunta con este statement')
        else:
            pregunta = Pregunta(statement=statement, quiz_id=quiz_id, max_score= max_score, score = 0)
            pregunta_id =  pregunta.insert()
                 
    except Exception as e:
        print(e)
        error_list.append('Error al crear la pregunta')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error creando la pregunta'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'id': pregunta_id, 'success': True, 'message': 'Pregunta creado satisfactoriamente'}), return_code


@preguntas_bp.route('/preguntas/<_id>', methods = ['PATCH'])
@authorize
def actualizar_pregunta(_id):
    error_list = []
    return_code = 201

    try:
        pregunta = Pregunta.query.filter(Pregunta.id == _id).first()

        if not pregunta:
            return_code = 404
            error_list.append('No se encontró la pregunta')
        else:
            body = request.json

            if 'description' in body:
                pregunta.description = body['description']

            if 'quiz_id' in body:
                pregunta.pregunta_id = body['quiz_id']

            if 'max_score' in body:
                pregunta.max_score = body['max_score']

            if 'score' in body:
                pregunta.score = body['score']

            pregunta.update()

    except Exception as e:
        print(e)
        error_list.append('Error al actualizar la pregunta')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error actualizando la Pregunta'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Pregunta actualizada correctamente'}), return_code

@preguntas_bp.route('/preguntas/<_id>', methods = ['DELETE'])
@authorize
def borrar_pregunta(_id):
    error_list = []
    return_code = 201

    try:
        pregunta = Pregunta.query.filter(Pregunta.id == _id).first()

        if not pregunta:
            return_code = 404
            error_list.append('No se encontró la pregunta')
        else:
            pregunta.delete()

    except Exception as e:
        print(e)
        error_list.append('Error al borrar la pregunta')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error eliminando la pregunta'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Pregunta eliminada satisfactoriamente'}), return_code