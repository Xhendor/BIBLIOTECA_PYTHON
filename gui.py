import tkinter as tk
from tkinter import ttk, messagebox
from biblioteca import SistemaBiblioteca
from models import UserType, Usuario, Libro
import datetime

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x600")
        
        # Initialize the library system
        self.sistema = SistemaBiblioteca()
        
        # Create some sample data
        self._crear_datos_ejemplo()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self._crear_tab_libros()
        self._crear_tab_usuarios()
        self._crear_tab_prestamos()
        self._crear_tab_reservas()
    
    def _crear_datos_ejemplo(self):
        # Create sample users
        self.admin = self.sistema.registrar_usuario("Admin", "admin@biblioteca.com", UserType.ADMINISTRADOR)
        self.bibliotecario = self.sistema.registrar_usuario("Bibliotecario", "biblio@biblioteca.com", UserType.BIBLIOTECARIO)
        
        # Create sample books
        self.sistema.registrar_libro("Don Quijote", "Miguel de Cervantes", "978-84-376-0494-7", 2)
        self.sistema.registrar_libro("Cien años de soledad", "Gabriel García Márquez", "978-84-397-2121-4", 3)
    
    def _crear_tab_libros(self):
        tab_libros = ttk.Frame(self.notebook)
        self.notebook.add(tab_libros, text='Libros')
        
        # Search frame
        search_frame = ttk.Frame(tab_libros)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self._buscar_libros).pack(side='left')
        
        # Books list
        self.tree_libros = ttk.Treeview(tab_libros, columns=('ID', 'Título', 'Autor', 'ISBN', 'Disponibles'))
        self.tree_libros.heading('ID', text='ID')
        self.tree_libros.heading('Título', text='Título')
        self.tree_libros.heading('Autor', text='Autor')
        self.tree_libros.heading('ISBN', text='ISBN')
        self.tree_libros.heading('Disponibles', text='Disponibles')
        self.tree_libros.column('ID', width=50)
        self.tree_libros.column('Título', width=200)
        self.tree_libros.column('Autor', width=150)
        self.tree_libros.column('ISBN', width=120)
        self.tree_libros.column('Disponibles', width=80)
        self.tree_libros['show'] = 'headings'
        self.tree_libros.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add book frame
        add_frame = ttk.LabelFrame(tab_libros, text="Agregar Libro")
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Título:").grid(row=0, column=0, padx=5, pady=2)
        self.titulo_entry = ttk.Entry(add_frame)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Autor:").grid(row=0, column=2, padx=5, pady=2)
        self.autor_entry = ttk.Entry(add_frame)
        self.autor_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(add_frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=2)
        self.isbn_entry = ttk.Entry(add_frame)
        self.isbn_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Copias:").grid(row=1, column=2, padx=5, pady=2)
        self.copias_entry = ttk.Entry(add_frame)
        self.copias_entry.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Button(add_frame, text="Agregar Libro", command=self._agregar_libro).grid(row=2, column=0, columnspan=4, pady=5)
        
        self._actualizar_lista_libros()
    
    def _crear_tab_usuarios(self):
        tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(tab_usuarios, text='Usuarios')
        
        # Users list
        self.tree_usuarios = ttk.Treeview(tab_usuarios, columns=('ID', 'Nombre', 'Email', 'Tipo'))
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Email', text='Email')
        self.tree_usuarios.heading('Tipo', text='Tipo')
        self.tree_usuarios['show'] = 'headings'
        self.tree_usuarios.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add user frame
        add_frame = ttk.LabelFrame(tab_usuarios, text="Registrar Usuario")
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=2)
        self.nombre_entry = ttk.Entry(add_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Email:").grid(row=0, column=2, padx=5, pady=2)
        self.email_entry = ttk.Entry(add_frame)
        self.email_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=2)
        self.tipo_usuario = ttk.Combobox(add_frame, values=[t.value for t in UserType])
        self.tipo_usuario.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(add_frame, text="Registrar Usuario", command=self._registrar_usuario).grid(row=2, column=0, columnspan=4, pady=5)
        
        self._actualizar_lista_usuarios()
    
    def _crear_tab_prestamos(self):
        tab_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(tab_prestamos, text='Préstamos')
        
        # Loans list
        self.tree_prestamos = ttk.Treeview(tab_prestamos, columns=('ID', 'Usuario', 'Libro', 'Fecha', 'Estado'))
        self.tree_prestamos.heading('ID', text='ID')
        self.tree_prestamos.heading('Usuario', text='Usuario')
        self.tree_prestamos.heading('Libro', text='Libro')
        self.tree_prestamos.heading('Fecha', text='Fecha Préstamo')
        self.tree_prestamos.heading('Estado', text='Estado')
        self.tree_prestamos['show'] = 'headings'
        self.tree_prestamos.pack(fill='both', expand=True, padx=5, pady=5)
        
        # New loan frame
        loan_frame = ttk.LabelFrame(tab_prestamos, text="Realizar Préstamo")
        loan_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(loan_frame, text="Usuario ID:").grid(row=0, column=0, padx=5, pady=2)
        self.prestamo_usuario_id = ttk.Entry(loan_frame)
        self.prestamo_usuario_id.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(loan_frame, text="Libro ID:").grid(row=0, column=2, padx=5, pady=2)
        self.prestamo_libro_id = ttk.Entry(loan_frame)
        self.prestamo_libro_id.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(loan_frame, text="Realizar Préstamo", command=self._realizar_prestamo).grid(row=1, column=0, columnspan=4, pady=5)
        
        self._actualizar_lista_prestamos()
    
    def _crear_tab_reservas(self):
        tab_reservas = ttk.Frame(self.notebook)
        self.notebook.add(tab_reservas, text='Reservas')
        
        # Reservations list
        self.tree_reservas = ttk.Treeview(tab_reservas, columns=('ID', 'Usuario', 'Libro', 'Fecha', 'Estado'))
        self.tree_reservas.heading('ID', text='ID')
        self.tree_reservas.heading('Usuario', text='Usuario')
        self.tree_reservas.heading('Libro', text='Libro')
        self.tree_reservas.heading('Fecha', text='Fecha Reserva')
        self.tree_reservas.heading('Estado', text='Estado')
        self.tree_reservas['show'] = 'headings'
        self.tree_reservas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # New reservation frame
        reserva_frame = ttk.LabelFrame(tab_reservas, text="Realizar Reserva")
        reserva_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(reserva_frame, text="Usuario ID:").grid(row=0, column=0, padx=5, pady=2)
        self.reserva_usuario_id = ttk.Entry(reserva_frame)
        self.reserva_usuario_id.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(reserva_frame, text="Libro ID:").grid(row=0, column=2, padx=5, pady=2)
        self.reserva_libro_id = ttk.Entry(reserva_frame)
        self.reserva_libro_id.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(reserva_frame, text="Realizar Reserva", command=self._realizar_reserva).grid(row=1, column=0, columnspan=4, pady=5)
        
        self._actualizar_lista_reservas()
    
    def _buscar_libros(self):
        termino = self.search_entry.get()
        resultados = self.sistema.buscar_libros(termino)
        self._actualizar_lista_libros(resultados)
    
    def _agregar_libro(self):
        try:
            titulo = self.titulo_entry.get()
            autor = self.autor_entry.get()
            isbn = self.isbn_entry.get()
            copias = int(self.copias_entry.get())
            
            if not all([titulo, autor, isbn, copias]):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return
            
            self.sistema.registrar_libro(titulo, autor, isbn, copias)
            self._actualizar_lista_libros()
            self._limpiar_campos_libro()
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
        except ValueError:
            messagebox.showerror("Error", "El número de copias debe ser un número entero")
    
    def _registrar_usuario(self):
        try:
            nombre = self.nombre_entry.get()
            email = self.email_entry.get()
            tipo = UserType(self.tipo_usuario.get())
            
            if not all([nombre, email, tipo]):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return
            
            self.sistema.registrar_usuario(nombre, email, tipo)
            self._actualizar_lista_usuarios()
            self._limpiar_campos_usuario()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Tipo de usuario inválido")
    
    def _realizar_prestamo(self):
        try:
            usuario_id = int(self.prestamo_usuario_id.get())
            libro_id = int(self.prestamo_libro_id.get())
            
            prestamo = self.sistema.realizar_prestamo(usuario_id, libro_id)
            if prestamo:
                self._actualizar_lista_prestamos()
                self._actualizar_lista_libros()
                self._limpiar_campos_prestamo()
                messagebox.showinfo("Éxito", "Préstamo realizado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo realizar el préstamo")
        except ValueError:
            messagebox.showerror("Error", "Los IDs deben ser números enteros")
    
    def _realizar_reserva(self):
        try:
            usuario_id = int(self.reserva_usuario_id.get())
            libro_id = int(self.reserva_libro_id.get())
            
            reserva = self.sistema.realizar_reserva(usuario_id, libro_id)
            if reserva:
                self._actualizar_lista_reservas()
                self._limpiar_campos_reserva()
                messagebox.showinfo("Éxito", "Reserva realizada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo realizar la reserva")
        except ValueError:
            messagebox.showerror("Error", "Los IDs deben ser números enteros")
    
    def _actualizar_lista_libros(self, libros=None):
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        
        if libros is None:
            libros = self.sistema.libros
        
        for libro in libros:
            self.tree_libros.insert('', 'end', values=(
                libro.id,
                libro.titulo,
                libro.autor,
                libro.isbn,
                libro.copias_disponibles
            ))
    
    def _actualizar_lista_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        for usuario in self.sistema.usuarios:
            self.tree_usuarios.insert('', 'end', values=(
                usuario.id,
                usuario.nombre,
                usuario.email,
                usuario.tipo.value
            ))
    
    def _actualizar_lista_prestamos(self):
        for item in self.tree_prestamos.get_children():
            self.tree_prestamos.delete(item)
        
        for prestamo in self.sistema.prestamos:
            self.tree_prestamos.insert('', 'end', values=(
                prestamo.id,
                prestamo.usuario.nombre,
                prestamo.libro.titulo,
                prestamo.fecha_prestamo.strftime('%Y-%m-%d'),
                prestamo.estado
            ))
    
    def _actualizar_lista_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        
        for reserva in self.sistema.reservas:
            self.tree_reservas.insert('', 'end', values=(
                reserva.id,
                reserva.usuario.nombre,
                reserva.libro.titulo,
                reserva.fecha_reserva.strftime('%Y-%m-%d'),
                reserva.estado
            ))
    
    def _limpiar_campos_libro(self):
        self.titulo_entry.delete(0, 'end')
        self.autor_entry.delete(0, 'end')
        self.isbn_entry.delete(0, 'end')
        self.copias_entry.delete(0, 'end')
    
    def _limpiar_campos_usuario(self):
        self.nombre_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.tipo_usuario.set('')
    
    def _limpiar_campos_prestamo(self):
        self.prestamo_usuario_id.delete(0, 'end')
        self.prestamo_libro_id.delete(0, 'end')
    
    def _limpiar_campos_reserva(self):
        self.reserva_usuario_id.delete(0, 'end')
        self.reserva_libro_id.delete(0, 'end')

def main():
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
