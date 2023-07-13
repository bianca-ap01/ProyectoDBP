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

    def test_create_user_success(self):
        response = self.client.post('/usuarios', json=self.new_user)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_create_user_fail(self):
        response = self.client.post('/usuarios', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)
    
