import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr.modelos import db, Cancion, Usuario, CancionSchema


class VerCancionesTest(unittest.TestCase):
    
    @staticmethod
    def create_app(self):
        app = Flask(__name__)         
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY']='frase-secreta'       
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
        return app

    def setUp(self):
        app = VerCancionesTest.create_app(self)
        SQLAlchemy(app)
        app_context = app.app_context()
        app_context.push()
        db.init_app(app)
        db.create_all()         

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #Pruebas SCRUD
    def test_crear_cancion(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        db.session.add(u)
        u.canciones.append(c)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        print(usuario.nombre)
        canciones = [ca for ca in usuario.canciones]
        print(canciones[0].titulo)
        self.assertEqual(c.titulo, canciones[0].titulo)
    
    def test_visualizar_canciones_usuario(self):
        c1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='carolina')
        u1 = Usuario(nombre='Angelica R', contrasena='1234')
        c2 = Cancion(titulo='prueba2', minutos=2, segundos=5,interprete='carolina')
        u2 = Usuario(nombre='Maria R', contrasena='1234')
        db.session.add(u1)
        db.session.add(u2)
        u1.canciones.append(c1)
        u2.canciones.append(c2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria R', Usuario.contrasena == '1234').first()
        print(usuario.nombre)
        canciones = [ca for ca in usuario.canciones]
        canciones2 = [ca for ca in usuario2.canciones]
        print(canciones[0].titulo)
        self.assertEqual(len(canciones), 1)
        self.assertEqual(c2.titulo, canciones2[0].titulo)

    def test_no_visualizar_canciones_de_otro_usuario(self):
        c1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='carolina')
        u1 = Usuario(nombre='Angelica R', contrasena='1234')
        c2 = Cancion(titulo='prueba2', minutos=2, segundos=5,interprete='carolina')
        u2 = Usuario(nombre='Maria R', contrasena='1234')
        db.session.add(u1)
        db.session.add(u2)
        u1.canciones.append(c1)
        u2.canciones.append(c2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria R', Usuario.contrasena == '1234').first()
        print(usuario.nombre)
        canciones = [ca for ca in usuario.canciones]
        canciones2 = [ca for ca in usuario2.canciones]
        print(canciones[0].titulo)
        self.assertEqual(len(canciones), 1)
        self.assertNotEqual(c1.titulo, canciones2[0].titulo)
