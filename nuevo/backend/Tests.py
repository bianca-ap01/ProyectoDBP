import unittest  # libreria de python para realizar test
from config.qa import config
from app.models import Employee, Department, User
from app.authentication import authorize
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
import io as io
import random
import string

class Tests(unittest.Testcase):
    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()


    # Cuestionarios

    def test_post_cuestionario_exitoso_201():
        pass
    def test_post_cuestionario_fallido_400():
        pass
    def test_post_cuestionario_fallido_500():
        pass


    def test_get_cuestionario_exitoso_201():
        pass
    def test_get_cuestionario_fallido_400():
        pass
    def test_get_cuestionario_fallido_500():
        pass


    def test_patch_cuestionario_exitoso_201():
        pass
    def test_patch_cuestionario_fallido_400():
        pass
    def test_patch_cuestionario_fallido_500():
        pass


    # Problemas

    def test_post_problema_exitoso_201():
        pass
    def test_post_problema_fallido_400():
        pass
    def test_post_problema_fallido_500():
        pass
    
    # Opciones

    def test_post_opcion_exitoso_201():
        pass
    def test_post_opcion_fallido_400():
        pass
    def test_post_opcion_fallido_500():
        pass
