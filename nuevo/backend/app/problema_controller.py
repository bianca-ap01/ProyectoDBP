from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Problema
from config.local import config

problemas_bp = Blueprint('/problemas', __name__)

@problemas_bp.route('/problemas', methods = ['POST'])
def crear_problema():
    error_list = []
    return_code = 201

    try:
        body = request.get_json()

        if 'descripcion' not in body:
            error_list.append('Descripción requerida')
        else:
            descripcion = body.get('descripcion')
        
        if 'id_cuestionario' not in body:
            error_list.append('Cuestionario requerido')
        else:
            id_cuestionario = body.get('id_cuestionario')

        problema_db = Problema.query.filter(Problema.descripcion==descripcion).first()

        if problema_db is not None :
            if problema_db.descripcion == descripcion:
                error_list.append('Ya existe un problema con esta descripción')
        else:
            problema = Problema(descripcion=descripcion, id_cuestionario=id_cuestionario)
            problema.insert()
    except Exception as e:
        print(e)
        error_list.append('Error al crear el problema')
        return_code = 500
    finally:
        if len(error_list) > 0:
            return jsonify({
                'success': False,
                'error': return_code,
                'message': error_list
            }), return_code
        else:
            return jsonify({
                'success': True,
                'error': return_code,
                'message': 'Problema creado exitosamente'
            }), return_code


        