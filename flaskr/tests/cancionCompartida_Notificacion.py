import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from modelos import Usuario, db, Cancion, Notificacion
from datetime import datetime



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

    
    def test_usuario_compartir_cancion(self):
        c1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='p1')
        u1 = Usuario(nombre='user1', contrasena='1234')
        u2 = Usuario(nombre='user2', contrasena='1234')
        db.session.add(u1)
        db.session.add(u2)
        u1.canciones.append(c1)
        c1.usuarios.append(u2)
        db.session.commit()
        cancion_compartida = Cancion.query.filter(Cancion.titulo == 'prueba1').first()
        usuario_compartido = cancion_compartida.usuarios[0]
        self.assertEqual(usuario_compartido.nombre, u2.nombre)

# Se agrega pruebas unitarias para las notificaciones que recibe el usuario cuando se le comparte una cancion

    def test_usuario_notificacion(self):
        c1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='p1')
        u1 = Usuario(nombre='user1', contrasena='1234')
        u2 = Usuario(nombre='user2', contrasena='1234')
        db.session.add(u1)
        db.session.add(u2)
        u1.canciones.append(c1)
        c1.usuarios.append(u2)
        n_mensaje = "El usuario " + u1.nombre + " te ha compartido la cancion " + c1.titulo
        n_fecha = datetime.now()
        n_notificacion = Notificacion(mensaje=n_mensaje, fecha=n_fecha, cancioncompartida=c1.id, mensaje_leido=False)
        u2.notificaciones.append(n_notificacion)
        db.session.commit()
        usuario_notificado = Usuario.query.filter(Usuario.nombre == 'user2').first()
        notificacion_recibida = usuario_notificado.notificaciones[0]
        self.assertEqual(notificacion_recibida.mensaje, n_mensaje)