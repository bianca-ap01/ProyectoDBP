import unittest
from config.qa import config
from app import create_app, db
from flask_sqlalchemy import SQLAlchemy
from app.models import Usuario, Quiz, Pregunta, Opcion
import json
import io as io

class Test(unittest.TestCase):
    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_user = {
            'email': 'test@gmail.com',
            'nickname': 'test',
            'password': '87654321',
            'confirmation_password': '87654321'
        }

        self.new_user_fail = {
            'email': 'zzz',
            'nickname': 'zzz',
            'password': '321',
            'confirmation_password': '321'
        }

        self.new_login = {
            'nickname': 'test',
            'password': '87654321'
        }

        self.new_login_fail = {
            'nickname': 'zzz',
            'password': '321'
        }

    def test_create_user_success(self):
        response = self.client.post('/usuarios', json=self.new_user)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_create_user_fail_1(self):
        response = self.client.post('/usuarios', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_create_user_fail_2(self):
        response = self.client.post('/usuarios', json=self.new_user_fail)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)


    def test_login_success(self):
        response = self.client.post('/usuarios/login', json=self.new_login)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_login_fail(self):
        response = self.client.post('/usuarios/login', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_login_fail_2(self):
        response = self.client.post('/usuarios/login', json=self.new_login_fail)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)

    # def test_get_preguntas_success(self):
    #     response = self.client.get('/preguntas')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_get_preguntas_fail(self):
        response = self.client.get('/preguntas')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], True)
    
