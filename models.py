from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

class UserType(Enum):
    ESTUDIANTE = "estudiante"
    BIBLIOTECARIO = "bibliotecario"
    ADMINISTRADOR = "administrador"

class Usuario:
    def __init__(self, id: int, nombre: str, email: str, tipo: UserType):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        self.prestamos_activos = []

class Libro:
    def __init__(self, id: int, titulo: str, autor: str, isbn: str, copias_disponibles: int):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.copias_disponibles = copias_disponibles
        self.copias_totales = copias_disponibles

class Prestamo:
    def __init__(self, id: int, usuario: Usuario, libro: Libro, fecha_prestamo: datetime):
        self.id = id
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion_esperada = fecha_prestamo + timedelta(days=14)
        self.fecha_devolucion_real = None
        self.estado = "activo"

class Reserva:
    def __init__(self, id: int, usuario: Usuario, libro: Libro, fecha_reserva: datetime):
        self.id = id
        self.usuario = usuario
        self.libro = libro
        self.fecha_reserva = fecha_reserva
        self.estado = "pendiente"  # pendiente, completada, cancelada
