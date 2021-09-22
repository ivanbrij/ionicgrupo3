from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, Notificacion, NotificacionSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
notificacion_schema = NotificacionSchema()

def getNombres(amigos):
    #minusculas = amigos.lower()
    sinespacios = amigos.replace(" ","")
    nombres = sinespacios.split(',')
    return nombres


class VistaCancionesUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una cancion con dicho nombre',409

        return cancion_schema.dump(nueva_cancion)


    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [cancion_schema.dump(ca) for ca in usuario.canciones]

class VistaUsuarios(Resource):

    def get(self):
        return [usuario_schema.dump(us) for us in Usuario.query.all()]

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo", cancion.titulo)
        cancion.minutos = request.json.get("minutos", cancion.minutos)
        cancion.segundos = request.json.get("segundos", cancion.segundos)
        cancion.interprete = request.json.get("interprete", cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '', 204


class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]


class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class VistaUsuario(Resource):

    @jwt_required()
    def get(self,id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario)


class VistaAlbumsUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"],
                            descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre', 409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]


class VistaCancionesUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una cancion con dicho nombre', 409

        return cancion_schema.dump(nueva_cancion)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [cancion_schema.dump(ca) for ca in usuario.canciones]


class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():

            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea', 404
        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                    segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]


class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo", album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '', 204

# Se agrega la vista UsuariosCancionCompartida como parte del release para Sprint 1
# En esta vista se puede agregar o listar los usuarios a los que se comparte una cancion
# Se actualiza la vista UsuariosCancionCompartida comp parte del Sprint 2
# En esta actualizacion de crean las notificaciones para los usuarios con los que se ha compartido la cancion

class VistaUsuariosCancionCompartida(Resource):

    def post(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        idUser = request.json["idUser"]
        usuario_cancion = Usuario.query.filter(Usuario.id == idUser).first() 
        amigos = request.json["amigos"]
        nombres = getNombres(amigos)

        for n in nombres:
            usuario = Usuario.query.filter(Usuario.nombre == n).first()
            db.session.commit()
            if usuario is None:
                return "Uno de los usuarios no existe", 404

        n_mensaje = "El usuario " + usuario_cancion.nombre + " te ha compartido la cancion " + cancion.titulo
        n_fecha = datetime.now()

        for n in nombres:
            usuario = Usuario.query.filter(Usuario.nombre == n).first()
            nueva_notificacion = Notificacion(mensaje=n_mensaje, fecha=n_fecha, cancioncompartida=id_cancion, mensaje_leido=False)
            usuario.notificaciones.append(nueva_notificacion)
            db.session.commit()
            cancion.usuarios.append(usuario)
        db.session.commit()
        return "La cancion se compartio con exito", 200

    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [usuario_schema.dump(us) for us in cancion.usuarios]

# Se agrega la vista CancionesCompartidasUsuario como parte del release para Sprint 1
# En esta vista se puede listar todas las canciones que se han compartido con el usuario

class VistaCancionesCompartidasUsuario(Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [cancion_schema.dump(ca) for ca in usuario.cancionescompartidas]

# Se agrega la vista NotificacionesUsuario como parte del release para Sprint2
# En esta vista se pueden listar todas las notificaciones recibidas por el usuario ordenadas a partir de la mas reciente

class VistaNotificacionesUsuario(Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        notificaciones = sorted(usuario.notificaciones, key=lambda objeto: objeto.fecha, reverse=True)
        return [notificacion_schema.dump(no) for no in notificaciones]

# Se agrega la vista Notificacion como parte del release para Sprint2
# En esta vista se puede ver el detalle de una notificacion o marcarla como leida

class VistaNotificacion(Resource):

    def get(self, id_notificacion):
        notificacion = Notificacion.query.get_or_404(id_notificacion)
        return [notificacion_schema.dump(notificacion)]

    def put(self, id_notificacion):
        notificacion = Notificacion.query.get_or_404(id_notificacion)
        notificacion.mensaje_leido = True
        db.session.commit()
        return notificacion_schema.dump(notificacion)