from biblioteca import SistemaBiblioteca
from models import UserType

def main():
    # Crear instancia del sistema
    biblioteca = SistemaBiblioteca()

    # Registrar algunos usuarios
    admin = biblioteca.registrar_usuario("Admin Principal", "admin@biblioteca.edu", UserType.ADMINISTRADOR)
    bibliotecario = biblioteca.registrar_usuario("Juan Bibliotecario", "juan@biblioteca.edu", UserType.BIBLIOTECARIO)
    estudiante = biblioteca.registrar_usuario("María Estudiante", "maria@estudiantes.edu", UserType.ESTUDIANTE)

    # Registrar algunos libros
    libro1 = biblioteca.registrar_libro("Don Quijote", "Miguel de Cervantes", "978-84-376-0494-7", 2)
    libro2 = biblioteca.registrar_libro("Cien años de soledad", "Gabriel García Márquez", "978-84-397-2121-4", 1)

    # Realizar un préstamo
    prestamo = biblioteca.realizar_prestamo(estudiante.id, libro1.id)
    if prestamo:
        print(f"Préstamo realizado: {prestamo.libro.titulo} a {prestamo.usuario.nombre}")
    
    # Buscar libros
    resultados = biblioteca.buscar_libros("Quijote")
    print("\nResultados de búsqueda para 'Quijote':")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor} ({libro.copias_disponibles} copias disponibles)")

    # Realizar una reserva
    reserva = biblioteca.realizar_reserva(estudiante.id, libro2.id)
    if reserva:
        print(f"\nReserva realizada: {reserva.libro.titulo} para {reserva.usuario.nombre}")

if __name__ == "__main__":
    main()
