from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import  VistaCancionesUsuario, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, \
        VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaUsuario, VistaCancionesCompartidasUsuario, VistaUsuariosCancionCompartida, \
        VistaNotificacion, VistaNotificacionesUsuario
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCancionesUsuario, '/usuario/<int:id_usuario>/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaUsuario,'/usuario/<int:id_usuario>')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaUsuariosCancionCompartida, '/cancion/<int:id_cancion>/usuarios')
api.add_resource(VistaCancionesCompartidasUsuario, '/usuario/<int:id_usuario>/cancionescompartidas')
api.add_resource(VistaNotificacionesUsuario, '/usuario/<int:id_usuario>/notificaciones')
api.add_resource(VistaNotificacion, '/notificacion/<int:id_notificacion>')

jwt = JWTManager(app)
