from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import Usuario
from config.local import config

users_bp = Blueprint('/usuarios', __name__)


@users_bp.route('/usuarios', methods = ['POST'])
def crear_usuario():
    error_list = []
    return_code = 201
    try:
        body = request.get_json()