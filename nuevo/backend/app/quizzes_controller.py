from flask import (
    Blueprint,
    request,
    jsonify
)

from .models import Quiz, Pregunta, Opcion, db
from .authentication import authorize
quizzes_bp = Blueprint('/quizzes', __name__)

@quizzes_bp.route('/quizzes', methods = ['GET'])
@authorize
def fetch_quizzes():
    quizzes = Quiz.query.all()
    return_code = 200
    try:
        res = [q.to_dict() for q in quizzes]
    except Exception as e:
        print('e: ', e)
        return_code = 500
        res = jsonify({
            'success': False,
            'message': "Error del servidor"
        })
    return jsonify({
        "success": True,
        "quizzes": res,
        "message": "Éxito obtentiendo quizzes"
    })

@quizzes_bp.route('/quizzes/<id>', methods = ['GET'])
@authorize
def obtener_quiz_por_title(id):
    quiz = Quiz.query.get(id)
    return jsonify(quiz.to_dict())

@quizzes_bp.route('/quizzes/<id>', methods = ['PUT'])
@authorize
def actualizar_quiz(id):
    data = request.get_json()
    for q in data["questions"]:
        opcion = Opcion.query.get(q["choice"])
        opcion.selected += 1
    db.session.commit()
    quiz = Quiz.query.get(id)
    return jsonify(quiz.to_dict()), 200

@quizzes_bp.route('/quizzes', methods = ['POST'])
@authorize
def crear_quiz():
    error_list = []
    return_code = 201
    try:
        data = request.get_json()
        quiz = Quiz(title=data['name'])
        questions = []
        for q in data['questions']:
            question = Pregunta(text=q['question'])
            question.opciones = [Opcion(text=c) for c in q['choices']]
            questions.append(question)
        quiz.preguntas = questions
        quiz.insert()    
    except Exception as e:
        print(e)
        error_list.append('Error al crear el quiz')
        return_code = 500
    
    
    return jsonify(quiz.to_dict()), 201

