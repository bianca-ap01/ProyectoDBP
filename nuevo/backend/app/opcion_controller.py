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

opciones_bp = Blueprint('/opciones', __name__)

@opciones_bp.route('/opciones', methods = ['POST'])
def crear_opcion():
    error_list = []
    return_code = 201

    try:
        body = request.get_json()

        if 'descripcion' not in body:
            error_list.append('Descripción requerida')
        else:
            descripcion = body.get('descripcion')
        
        if 'id_problema' not in body:
            error_list.append('Problema requerido')
        else:
            id_problema = body.get('id_problema')

        if 'es_correcta' not in body:
            error_list.append('Es correcta requerido')
        else:
            es_correcta = body.get('es_correcta')

        opcion_db = Opcion.query.filter(Opcion.descripcion==descripcion).first()

        if opcion_db is not None :
            if opcion_db.descripcion == descripcion:
                error_list.append('Ya existe una opción con esta descripción')
        else:
            opcion = Opcion(descripcion=descripcion, id_problema=id_problema, answer=es_correcta)
            opcion.insert()
    except Exception as e:
        print(e)
        error_list.append('Error al crear la opción')
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
                'message': 'Opción creada exitosamente'
            }), return_code