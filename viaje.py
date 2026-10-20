from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
import re
from flask import flash

class Viaje:

    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.cupo = data.get('cupo')
        self.fecha = data.get('fecha')
        self.fecha_fin = data.get('fecha_fin')
        self.descripcion = data.get('descripcion')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.usuario_id = data.get('usuario_id')
        self.guia_nombre = data.get('guia_nombre')
        self.guia_apellido = data.get('guia_apellido')
        self.inscritos = data.get('inscritos', 0)

    @property
    def cupos_disponibles(self):
        try:
            return max(int(self.cupo) - int(self.inscritos), 0)
        except (TypeError, ValueError):
            return self.cupo

    @property
    def esta_llena(self):
        return self.cupos_disponibles == 0

    # INSERTAR
    @classmethod
    def save(cls, datos):
        query = """
            INSERT INTO viajes (nombre, cupo, fecha, fecha_fin, descripcion, created_at, updated_at, usuario_id)
            VALUES (%(nombre)s, %(cupo)s, %(fecha)s, %(fecha_fin)s, %(descripcion)s, NOW(), NOW(), %(usuario_id)s)
        """
        return connectToMySQL('Viajero_Frecuente').query_db(query, datos)

    # LISTAR TODOS con JOIN al guía y conteo de inscritos
    @classmethod
    def get_all(cls):
        query = """
            SELECT v.*,
                   u.nombre   AS guia_nombre,
                   u.apellido AS guia_apellido,
                   (SELECT COUNT(*) FROM inscripciones i WHERE i.viaje_id = v.id) AS inscritos
            FROM viajes v
            JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.fecha >= CURDATE()
            ORDER BY v.fecha ASC;
        """
        filas = connectToMySQL('Viajero_Frecuente').query_db(query)
        return [cls(f) for f in filas]

    # OBTENER UNO por id
    @classmethod
    def get_one(cls, datos):
        query = """
            SELECT v.*,
                   u.nombre   AS guia_nombre,
                   u.apellido AS guia_apellido,
                   (SELECT COUNT(*) FROM inscripciones i WHERE i.viaje_id = v.id) AS inscritos
            FROM viajes v
            JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.id = %(id)s
            LIMIT 1;
        """
        filas = connectToMySQL('Viajero_Frecuente').query_db(query, datos)
        if filas:
            return cls(filas[0])
        return None

    # ACTUALIZAR
    @classmethod
    def update(cls, datos):
        query = """
            UPDATE viajes
            SET nombre=%(nombre)s, cupo=%(cupo)s, fecha=%(fecha)s,
                fecha_fin=%(fecha_fin)s, descripcion=%(descripcion)s, updated_at=NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL('Viajero_Frecuente').query_db(query, datos)

    # ELIMINAR
    @classmethod
    def delete(cls, datos):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        return connectToMySQL('Viajero_Frecuente').query_db(query, datos)

    # Verificar si el usuario es el dueño del viaje (BONUS)
    @classmethod
    def pertenece_a(cls, viaje_id, usuario_id):
        query = "SELECT id FROM viajes WHERE id = %(v)s AND usuario_id = %(u)s LIMIT 1;"
        return bool(connectToMySQL('Viajero_Frecuente').query_db(query, {"v": viaje_id, "u": usuario_id}))

    # VALIDACIONES
    @staticmethod
    def validar_viaje(formulario):
        errores = []
        nombre = (formulario.get('nombre') or '').strip()
        descripcion = (formulario.get('descripcion') or '').strip()
        cupo_raw = (formulario.get('cupo') or '').strip()
        fecha = (formulario.get('fecha') or '').strip()
        fecha_fin = (formulario.get('fecha_fin') or '').strip()

        # Todos los campos son obligatorios
        if not (nombre and descripcion and cupo_raw and fecha and fecha_fin):
            errores.append("Todos los campos son obligatorios.")

        # Nombre mínimo 3 caracteres
        if nombre and len(nombre) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres.")

        # Descripción mínimo 10 caracteres
        if descripcion and len(descripcion) < 10:
            errores.append("La descripción debe tener al menos 10 caracteres.")

        # Cupo debe ser número > 0
        try:
            cupo = int(cupo_raw)
            if cupo <= 0:
                errores.append("El cupo debe ser mayor a 0.")
        except ValueError:
            errores.append("El cupo debe ser un número.")

        # Fecha no en pasado (BONUS)
        from datetime import date, datetime
        if fecha:
            try:
                f = datetime.strptime(fecha, '%Y-%m-%d').date()
                if f < date.today():
                    errores.append("La fecha no puede ser en el pasado.")
            except ValueError:
                errores.append("La fecha no tiene un formato válido.")

        # fecha_fin >= fecha
        if fecha and fecha_fin:
            try:
                f1 = datetime.strptime(fecha, '%Y-%m-%d').date()
                f2 = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                if f2 < f1:
                    errores.append("La fecha fin no puede ser anterior a la fecha de inicio.")
            except ValueError:
                pass

        for err in errores:
            flash(err, "viaje")

        return len(errores) == 0
