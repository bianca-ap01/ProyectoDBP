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
from .models import db   
from config.local import config

opciones_bp = Blueprint('/opciones', __name__)

@opciones_bp.route('/opciones', methods = ['POST'])
def crear_opcion():
    error_list = []
    return_code = 201
    opcion = None  # Inicializa la opcion como None

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

        opcion_db = Opcion.query.filter(Opcion.descripcion==descripcion).first()

        if opcion_db is not None :
            if opcion_db.descripcion == descripcion:
                error_list.append('Ya existe esta opción')

        
        if len(error_list) == 0:
            opcion = Opcion(descripcion=descripcion, id_problema=id_problema)
            db.session.add(opcion)
            db.session.commit()

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
    elif return_code != 201 or opcion is None:
        abort(return_code)
    else:
        return jsonify({'id': opcion.id, 'success': True, 'message': 'Opcion creada satisfactoriamente'}), return_code
