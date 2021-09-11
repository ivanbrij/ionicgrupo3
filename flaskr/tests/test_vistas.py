import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..modelos import Usuario, db


class VistasTest(unittest.TestCase):
    
    @staticmethod
    def create_app(self):
        app = Flask(__name__)         
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY']='frase-secreta'       
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones_test.db'
        return app
    
    def setUp(self):
        app = VistasTest.create_app(self)
        SQLAlchemy(app)
        app_context = app.app_context()
        app_context.push()
        db.init_app(app)
        db.create_all()         

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    def test_crear_usuario(self):
        user = Usuario(nombre='test', contrasena='12345')
        db.session.add(user)
        db.session.commit()
        usuarioTest = Usuario.query.filter(Usuario.nombre == 'test').first()
        print(usuarioTest.nombre)
        self.assertIsNotNone(usuarioTest)