from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

from .models import Quiz, Pregunta, Opcion
from .authentication import authorize
quizzes_bp = Blueprint('/quizzes', __name__)

@quizzes_bp.route('/quizzes', methods = ['GET'])
def obtener_quiz():
    return_code = 201
    error_list = []
    try:
        quizzes_list = []
        search_query = request.args.get('search', None)

        if search_query:
            quizzes = Quiz.query.filter(Quiz.title.like('%{}%'.format(search_query))).all()
            quizzes_list = [quiz.serialize() for quiz in quizzes]
        else:
            quizzes = Quiz.query.all()
            quizzes_list = [quiz.serialize() for quiz in quizzes]

            if quizzes_list is None:
                return_code = 404
                error_list.append('Quiz inexistente')

        if len(error_list) > 0:
            return_code = 404

    except Exception as e:
        print('e: ', e)
        return_code = 500
        error_list.append('Error del servidor')


    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'errors': error_list
        }), return_code
    elif return_code != 201 and return_code != 404:
        abort(return_code)
    else:
        return jsonify({
            'success': True,
            'quizzes': quizzes_list
        }), return_code

@quizzes_bp.route('/quizzes/<_title>', methods = ['GET'])
def obtener_quiz_por_title(_title):
    return_code = 201
    error_list = []
    try:
        quiz = Quiz.query.filter(Quiz.title == _title).first()

        if quiz is None:
            return_code = 404
            error_list.append('Quiz inexistente')
        else:
            quiz = quiz.serialize()
            preguntas = Pregunta.query.filter(Pregunta.quiz_id == quiz['id']).all()
            preguntas_list = [pregunta.serialize() for pregunta in preguntas]
            quiz['preguntas'] = preguntas_list

            for pregunta in preguntas_list:
                opciones = Opcion.query.filter(Opcion.pregunta_id == pregunta['id']).all()
                answer = 0
                flag = False
                opciones_list = []
                for opcion in opciones:
                    serialize_opcion = opcion.serialize()
                    opciones_list.append(serialize_opcion['statement'])
                    if not flag:
                        answer += 1
                    flag = flag or serialize_opcion['is_correct'] 
                pregunta['answer'] = answer
                pregunta['opciones'] = opciones_list

    except Exception as e:
        print('e: ', e)
        return_code = 500
        error_list.append('Error del servidor')
    
    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'errors': error_list
        }), return_code

    else:
        return jsonify({
            'success': True,
            'title': quiz['title'],
            'preguntas': quiz['preguntas'],
            'max_score': quiz['max_score']
        }), return_code

@quizzes_bp.route('/quizzes', methods = ['POST'])
@authorize
def crear_quiz():
    error_list = []
    return_code = 201
    try:
        body = request.get_json()

        if 'title' not in body:
            error_list.append('Título requerido')
        else:
            title = body.get('title')

        if 'num_preg' not in body:
            error_list.append('Número de preguntas requerido')
        else:
            num_preg = body.get('num_preg')

        if 'max_score' not in body:
            error_list.append('Puntaje requerido')
        else:
            max_score = body.get('max_score')

        quiz_db = Quiz.query.filter(Quiz.title==title).first()

        if quiz_db is not None :
            if quiz_db.title.lower() == title.lower():
                error_list.append('Ya existe un quiz con este título')

        if len(error_list) > 0:
            return_code = 400
        else:
            quiz = Quiz(title=title, num_preg=num_preg, max_score = max_score, score=0)
            quiz_id = quiz.insert()

    except Exception as e:
        print('e: ', e)
        return_code = 500
    
    if return_code == 400:
        return jsonify({
            'success': False,
            'errors': error_list,
            'message': 'Error creando quiz'
        }), return_code
    elif return_code != 201:
        abort(return_code)
    else:
        return jsonify({'id': quiz.serialize(), 'success': True, 'message': 'Quiz creado satisfactoriamente'}), return_code


@quizzes_bp.route('/quizzes/<_id>', methods = ['PATCH'])
@authorize
def actualizar_quiz(_id):
    error_list = []
    return_code = 201
    try:
        quiz = Quiz.query.filter(Quiz.id == _id).first()

        if not quiz:
            return_code = 404
            error_list.append('No se encontró el quiz')
        else:
            body = request.json

            if 'title' in body:
                quiz.description = body['title']

            if 'num_preg' in body:
                quiz.num_preg = body['num_preg']

            if 'max_score' in body:
                quiz.max_score = body['max_score']

            if 'score' in body:
                quiz.score = body['score']

            quiz.update()

    except Exception as e:
        print(e)
        error_list.append('Error al actualizar quiz')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error actualizando la quiz'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Quiz actualizado correctamente'}), return_code

@quizzes_bp.route('/quizzes/<_id>', methods = ['DELETE'])
@authorize
def borrar_quiz(_id):
    error_list = []
    return_code = 201

    try:
        quiz = Quiz.query.filter(Quiz.id == _id).first()

        if not quiz:
            return_code = 404
            error_list.append('No se encontró el quiz')
        else:
            quiz.delete()

    except Exception as e:
        print(e)
        error_list.append('Error al actualizar el quiz')
        return_code = 500

    if len(error_list) > 0:
        return jsonify({
            'success': False,
            'error': error_list,
            'message': 'Error eliminando el quiz'
        }), return_code
    elif return_code != 201:
            abort(return_code)
    else:
        return jsonify({'success': True, 'message': 'Quiz eliminado satisfactoriamente'}), return_code


# @quizzes_bp.route('/quizzes/<_quiz_id>/preguntas', methods  = ['POST'])
# def crear_pregunta_quiz(_quiz_id):
#     error_list = []
#     return_code = 201

#     try:
#         body = request.get_json()

#         quiz = Quiz.query.filter(Quiz.id == _quiz_id)

#         if quiz is None:
#             error_list.append("No existe el quiz solicitado")
#         else: 
#             quiz_id = _quiz_id

#         if 'statement' not in body:
#             error_list.append('statement requerida')
#         else:
#             statement = body.get('statement')
        
#         if 'max_score' not in body:
#             error_list.append('Puntaje requerida')
#         else:
#             max_score = body.get('max_score')

#         pregunta_db = Pregunta.query.filter(Pregunta.statement==statement).first()

#         if pregunta_db is not None :
#             if pregunta_db.statement.lower() == statement.lower():
#                 error_list.append('Ya existe un pregunta con este enunciado')
#         else:
#             pregunta = Pregunta(statement=statement, quiz_id=quiz_id, max_score= max_score, score = 0)
#             pregunta_id =  pregunta.insert()
                 
#     except Exception as e:
#         print(e)
#         error_list.append('Error al crear la pregunta')
#         return_code = 500

#     if len(error_list) > 0:
#         return jsonify({
#             'success': False,
#             'error': error_list,
#             'message': 'Error creando la pregunta'
#         }), return_code
#     elif return_code != 201:
#             abort(return_code)
#     else:
#         return jsonify({'id': pregunta_id, 'success': True, 'message': 'Pregunta creado satisfactoriamente'}), return_code
