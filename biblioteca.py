from datetime import datetime
from typing import List, Optional
from models import *

class SistemaBiblioteca:
    def __init__(self):
        self.usuarios = []
        self.libros = []
        self.prestamos = []
        self.reservas = []
        self._ultimo_id_usuario = 0
        self._ultimo_id_libro = 0
        self._ultimo_id_prestamo = 0
        self._ultimo_id_reserva = 0

    def registrar_usuario(self, nombre: str, email: str, tipo: UserType) -> Usuario:
        self._ultimo_id_usuario += 1
        nuevo_usuario = Usuario(self._ultimo_id_usuario, nombre, email, tipo)
        self.usuarios.append(nuevo_usuario)
        return nuevo_usuario

    def registrar_libro(self, titulo: str, autor: str, isbn: str, copias: int) -> Libro:
        self._ultimo_id_libro += 1
        nuevo_libro = Libro(self._ultimo_id_libro, titulo, autor, isbn, copias)
        self.libros.append(nuevo_libro)
        return nuevo_libro

    def buscar_libros(self, termino: str) -> List[Libro]:
        termino = termino.lower()
        return [libro for libro in self.libros if 
                termino in libro.titulo.lower() or 
                termino in libro.autor.lower() or 
                termino in libro.isbn.lower()]

    def realizar_prestamo(self, usuario_id: int, libro_id: int) -> Optional[Prestamo]:
        usuario = next((u for u in self.usuarios if u.id == usuario_id), None)
        libro = next((l for l in self.libros if l.id == libro_id), None)

        if not usuario or not libro:
            return None

        if libro.copias_disponibles <= 0:
            return None

        if len(usuario.prestamos_activos) >= 3:
            return None

        self._ultimo_id_prestamo += 1
        nuevo_prestamo = Prestamo(self._ultimo_id_prestamo, usuario, libro, datetime.now())
        libro.copias_disponibles -= 1
        usuario.prestamos_activos.append(nuevo_prestamo)
        self.prestamos.append(nuevo_prestamo)
        return nuevo_prestamo

    def realizar_devolucion(self, prestamo_id: int) -> bool:
        prestamo = next((p for p in self.prestamos if p.id == prestamo_id), None)
        if not prestamo or prestamo.estado != "activo":
            return False

        prestamo.fecha_devolucion_real = datetime.now()
        prestamo.estado = "devuelto"
        prestamo.libro.copias_disponibles += 1
        prestamo.usuario.prestamos_activos.remove(prestamo)
        return True

    def realizar_reserva(self, usuario_id: int, libro_id: int) -> Optional[Reserva]:
        usuario = next((u for u in self.usuarios if u.id == usuario_id), None)
        libro = next((l for l in self.libros if l.id == libro_id), None)

        if not usuario or not libro:
            return None

        if libro.copias_disponibles > 0:
            return None  # No se necesita reserva si hay copias disponibles

        self._ultimo_id_reserva += 1
        nueva_reserva = Reserva(self._ultimo_id_reserva, usuario, libro, datetime.now())
        self.reservas.append(nueva_reserva)
        return nueva_reserva

    def obtener_prestamos_usuario(self, usuario_id: int) -> List[Prestamo]:
        return [p for p in self.prestamos if p.usuario.id == usuario_id]

    def obtener_prestamos_vencidos(self) -> List[Prestamo]:
        ahora = datetime.now()
        return [p for p in self.prestamos 
                if p.estado == "activo" and p.fecha_devolucion_esperada < ahora]
